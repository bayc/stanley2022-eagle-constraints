import matplotlib.pyplot as plt
import numpy as np
import pickle

from floris.tools import FlorisInterface
from shapely.geometry import Polygon, MultiPolygon
from wind_design_tools import plotting_functions, pack_turbs



min_spacing = 6
rotor_diameter = 164.0
threshold = 0.1
threshold = np.round(threshold,2)
with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/abstract/geometry/polygons_T%s'%threshold, "rb") as poly_file:
    print(poly_file)
    loaded_polygon = pickle.load(poly_file)

if type(loaded_polygon) == Polygon:
    loaded_polygon = MultiPolygon([loaded_polygon])

turbine_packing = pack_turbs.PackTurbines(min_spacing*rotor_diameter, loaded_polygon)
turbine_packing.pack_turbines_poly()
turbine_x = turbine_packing.turbine_x
turbine_y = turbine_packing.turbine_y

shell_red = (221 / 255, 29 / 255, 33 / 255)
shell_yellow = (251 / 255, 206 / 255, 7 / 255)

plt.figure()
ax = plt.gca()
plotting_functions.plot_poly(loaded_polygon, color=shell_yellow, alpha=1.0)
plotting_functions.plot_turbines(loaded_polygon, color=shell_red, alpha=1.0)
ax.axis("equal")
plt.show()



# # Initialize FLORIS with the given input file via FlorisInterface.
# # For basic usage, FlorisInterface provides a simplified and expressive
# # entry point to the simulation routines.
# fi = FlorisInterface("gch.yaml")

# # Convert to a simple two turbine layout
# fi.reinitialize( layout=( [0, 500.], [0., 0.] ) )

# # Single wind speed and wind direction
# print('\n============================= Single Wind Direction and Wind Speed =============================')

# # Get the turbine powers assuming 1 wind speed and 1 wind direction
# fi.reinitialize(wind_directions=[270.], wind_speeds=[8.0])

# # Set the yaw angles to 0
# yaw_angles = np.zeros([1,1,2]) # 1 wind direction, 1 wind speed, 2 turbines
# fi.calculate_wake(yaw_angles=yaw_angles)

# # Get the turbine powers
# turbine_powers = fi.get_turbine_powers()/1000.
# print('The turbine power matrix should be of dimensions 1 WD X 1 WS X 2 Turbines')
# print(turbine_powers)
# print("Shape: ",turbine_powers.shape)

# # Single wind speed and wind direction
# print('\n============================= Single Wind Direction and Multiple Wind Speeds =============================')


# wind_speeds = np.array([8.0, 9.0, 10.0])
# fi.reinitialize(wind_speeds=wind_speeds)
# yaw_angles = np.zeros([1,3,2]) # 1 wind direction, 3 wind speeds, 2 turbines
# fi.calculate_wake(yaw_angles=yaw_angles)
# turbine_powers = fi.get_turbine_powers()/1000.
# print('The turbine power matrix should be of dimensions 1 WD X 3 WS X 2 Turbines')
# print(turbine_powers)
# print("Shape: ",turbine_powers.shape)

# # Single wind speed and wind direction
# print('\n============================= Multiple Wind Directions and Multiple Wind Speeds =============================')

# wind_directions = np.array([260., 270., 280.])
# wind_speeds = np.array([8.0, 9.0, 10.0])
# fi.reinitialize(wind_directions=wind_directions, wind_speeds=wind_speeds)
# yaw_angles = np.zeros([1,3,2]) # 1 wind direction, 3 wind speeds, 2 turbines
# fi.calculate_wake(yaw_angles=yaw_angles)
# turbine_powers = fi.get_turbine_powers()/1000.
# print('The turbine power matrix should be of dimensions 3 WD X 3 WS X 2 Turbines')
# print(turbine_powers)
# print("Shape: ",turbine_powers.shape)
