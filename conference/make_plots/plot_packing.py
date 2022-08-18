from json import load
from turtle import fillcolor
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
import scipy
import yaml

from shapely.geometry import Polygon, MultiPolygon
from wind_design_tools import plotting_functions

plt.style.use('presentation')

min_spacing = 6
rotor_diameter = 198.0
turbine_rating = 10.0
threshold_array = np.arange(10)/100.0 + 0.01
threshold_array = threshold_array[::-1] 

lowy_int = 8
threshold = 0.02

with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/abstract/geometry/polygons_T%s'%threshold, "rb") as poly_file:
    loaded_polygon = pickle.load(poly_file)

lowx = 0.0
highx = 10000.0
lowy = lowy_int * 5000.0
highy = lowy + 5000.0
total_area = 10000.0 * 5000.0

limited_area = Polygon(((lowx, lowy), (lowx, highy), (highx, highy), (highx, lowy)))
full_area = Polygon(((-10.0, -10.0), (-10.0, 50010), (50010, 50010), (50010, -10.0)))
subtract_polygon = full_area.difference(limited_area)
limited_polygon = loaded_polygon.difference(subtract_polygon)
print(type(limited_polygon))
if type(limited_polygon) == Polygon:
    limited_polygon = MultiPolygon([limited_polygon])

with open("../optimization_results/capacity/capacity%s_%s.yml"%(int(lowy_int), threshold), "r") as stream:
# with open("../optimization_results/coe/coe%s_%s.yml"%(int(lowy_int), threshold), "r") as stream:
    results_data = yaml.safe_load(stream)
# results_data = yaml.load(results_file)
turbine_x = results_data["turbine_x"]
turbine_y = results_data["turbine_y"]


scale = 1.
plt.figure(figsize=(12*scale, 6*scale))
ax1 = plt.subplot(111)
ax1.set_xlim(lowx-100, highx+100)
ax1.set_ylim(lowy-100, highy+100)

plotting_functions.plot_poly(limited_polygon, ax=ax1, color="C0", alpha=1.0)
plotting_functions.plot_turbines(turbine_x, turbine_y, rotor_diameter/2.0, ax=ax1, color="C1")


# for i in range(len(turbine_x)):
#     t = plt.Circle((turbine_x[i], turbine_y[i]), min_spacing*rotor_diameter, fill=False, edgecolor="black")
#     ax1.add_patch(t)


ax1.axis("equal")
ax1.axis("off")
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

plt.pause(0.001)
plt.savefig("figures/packing.png")
plt.show()

