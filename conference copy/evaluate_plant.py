import matplotlib.pyplot as plt
import numpy as np
import pickle
import time

from floris.tools import FlorisInterface
from shapely.geometry import Polygon, MultiPolygon
from wind_design_tools import plotting_functions, pack_turbs



min_spacing = 6
rotor_diameter = 198.0
threshold = 0.05
threshold = np.round(threshold,2)
with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/abstract/geometry/polygons_T%s'%threshold, "rb") as poly_file:
    print(poly_file)
    loaded_polygon = pickle.load(poly_file)

if type(loaded_polygon) == Polygon:
    loaded_polygon = MultiPolygon([loaded_polygon])

start = time.time()
turbine_packing = pack_turbs.PackTurbines(min_spacing*rotor_diameter, loaded_polygon)
turbine_packing.pack_turbines_poly()
turbine_x = turbine_packing.turbine_x
turbine_y = turbine_packing.turbine_y
print("time to pack: ", time.time() - start)
print("number of turbines: ", len(turbine_x))




start = time.time()
# Initialize FLORIS with the given input file via FlorisInterface.
# For basic usage, FlorisInterface provides a simplified and expressive
# entry point to the simulation routines.
fi = FlorisInterface("conference.yaml")
fi.reinitialize( layout=( turbine_x, turbine_y ) )

# Get the turbine powers
fi.reinitialize(wind_directions=[270.], wind_speeds=[8.0])
fi.calculate_wake()
turbine_powers = fi.get_turbine_powers()/1000.
print("time to evaluate: ", time.time() - start)
print(np.sum(turbine_powers))
print("Shape: ",turbine_powers.shape)

shell_red = (221 / 255, 29 / 255, 33 / 255)
shell_yellow = (251 / 255, 206 / 255, 7 / 255)

plt.figure()
ax = plt.gca()
plotting_functions.plot_poly(loaded_polygon, color=shell_yellow, ax=ax, alpha=1.0)
plotting_functions.plot_turbines(turbine_x, turbine_y, rotor_diameter/2.0, ax=ax, color=shell_red)
ax.axis("equal")
plt.show()


