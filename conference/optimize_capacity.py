from json import load
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
import yaml

from shapely.geometry import Polygon, MultiPolygon
from wind_design_tools import plotting_functions, pack_turbs



min_spacing = 6
rotor_diameter = 198.0
turbine_rating = 10.0
threshold_array = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1])

lowy_array = [0,1,2,3,4,5,6,7,8,9]
for j in range(len(lowy_array)):
    turbine_x = np.array([])
    turbine_y = np.array([])
    for k in range(len(threshold_array)):
        start = time.time()

        threshold = threshold_array[k]
        threshold = np.round(threshold,2)
        with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/abstract/geometry/polygons_T%s'%threshold, "rb") as poly_file:
            loaded_polygon = pickle.load(poly_file)

        lowx = 0.0
        highx = 10000.0
        lowy = lowy_array[j] * 5000.0
        highy = lowy + 5000.0

        limited_area = Polygon(((lowx, lowy), (lowx, highy), (highx, highy), (highx, lowy)))
        full_area = Polygon(((-10.0, -10.0), (-10.0, 50010), (50010, 50010), (50010, -10.0)))
        subtract_polygon = full_area.difference(limited_area)
        limited_polygon = loaded_polygon.difference(subtract_polygon)
        print(type(limited_polygon))
        if type(limited_polygon) == Polygon:
            limited_polygon = MultiPolygon([limited_polygon])

        existing_turbines = np.zeros((len(turbine_x), 2))
        existing_turbines[:, 0] = turbine_x[:]
        existing_turbines[:, 1] = turbine_y[:]

        turbine_packing = pack_turbs.PackTurbines(min_spacing*rotor_diameter, limited_polygon, weight_x=1E6)
        turbine_packing.pack_turbines_poly(existing_turbines=existing_turbines)
        new_turbine_x = turbine_packing.turbine_x
        new_turbine_y = turbine_packing.turbine_y

        turbine_x = np.append(turbine_x, new_turbine_x)
        turbine_y = np.append(turbine_y, new_turbine_y)

        opt_capacity = turbine_rating * len(turbine_x)

        results_dict = {}
        results_dict["capacity"] = float(opt_capacity)
        results_dict["opt_time"] = float(time.time() - start)
        results_dict["turbine_x"] = turbine_x.tolist()
        results_dict["turbine_y"] = turbine_y.tolist()
        results_filename = 'optimization_results/capacity/capacity%s_%s.yml'%(int(lowy_array[j]), threshold)
        with open(results_filename, 'w') as outfile:
            yaml.dump(results_dict, outfile)
    