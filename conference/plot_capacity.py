from json import load
import matplotlib.pyplot as plt
plt.style.use('presentation')
import numpy as np
import pickle
import time
import yaml

from shapely.geometry import Polygon, MultiPolygon
from wind_design_tools import plotting_functions, pack_turbs

# shell_red = (221 / 255, 29 / 255, 33 / 255)
# shell_yellow = (251 / 255, 206 / 255, 7 / 255)

min_spacing = 6
rotor_diameter = 198.0
turbine_rating = 10.0
threshold_array = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1])

plt.figure(figsize=(4,4))
ax = plt.subplot(111)
for k in range(len(threshold_array)):
    start = time.time()

    threshold = threshold_array[k]
    threshold = np.round(threshold,2)
    with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/conference/geometry/polygons_T%s'%threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)

    lowx = 0.0
    highx = 10000.0
    low_y_value = 0
    lowy = low_y_value * 5000.0
    highy = lowy + 5000.0

    limited_area = Polygon(((lowx, lowy), (lowx, highy), (highx, highy), (highx, lowy)))
    full_area = Polygon(((-10.0, -10.0), (-10.0, 50010), (50010, 50010), (50010, -10.0)))
    subtract_polygon = full_area.difference(limited_area)
    limited_polygon = loaded_polygon.difference(subtract_polygon)
    if type(limited_polygon) == Polygon:
        limited_polygon = MultiPolygon([limited_polygon])

    # with open("optimization_results/capacity/capacity%s_%s.yml"%(int(low_y_value), threshold), "r") as stream:
    with open("optimization_results/coe/coe%s_%s.yml"%(int(low_y_value), threshold), "r") as stream:
        results_data = yaml.safe_load(stream)
    # results_data = yaml.load(results_file)
    turbine_x = results_data["turbine_x"]
    turbine_y = results_data["turbine_y"]

    plt.cla()
    plotting_functions.plot_poly(limited_polygon, ax=ax, color="C0")
    plotting_functions.plot_turbines(turbine_x, turbine_y, rotor_diameter/2.0,
                                     ax=ax, color="C1")
    ax.axis("square")
    ax.set_xlim(lowx-rotor_diameter, highx+rotor_diameter)
    ax.set_ylim(lowy-rotor_diameter, highy+rotor_diameter)
    ax.set_title("threshold: %s"%threshold)
    ax.axis("off")
    plt.pause(1.5)