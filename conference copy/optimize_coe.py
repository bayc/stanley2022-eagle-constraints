from json import load
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
import scipy
import yaml

from floris.tools import FlorisInterface
from shapely.geometry import Polygon, MultiPolygon
# from wind_design_tools import plotting_functions, pack_turbs, optimize_gf
from pack_turbs import PackTurbines
from greedy import GreedyAlgorithm
from plotting_functions import plot_poly


def objective_function(design_variables, args):
    (possible_x, possible_y, fi, turbine_rating, capex_function, om_function) = args

    turbine_array = np.array(design_variables, dtype=bool)

    turbine_x = possible_x[turbine_array]
    turbine_y = possible_y[turbine_array]

    # xbnds = [885.88111392,  272.15415826, 1715.87466356, 2366.51661752, 885.88111392]
    # ybnds = np.array([30225.11532624, 27967.16554964, 27568.29420254, 29856.40841755, 30225.11532624]) - 27568.29420254
    # plt.figure()
    # plt.plot(turbine_x, turbine_y, '*')
    # plt.plot(xbnds, ybnds)
    # plt.show()

    if len(turbine_x) == 0:
        return 1E3
    if len(turbine_x) < 7:
        return 1E3
    else:
        fi.reinitialize( layout_x=turbine_x, layout_y=turbine_y )
        fi.calculate_wake()
        turbine_powers = fi.get_turbine_powers()/1E3 # kW to MW
        farm_power = np.sum(turbine_powers)
        capacity_factor = 0.45
        aep = farm_power * 8760.0 * capacity_factor

        capacity = len(turbine_x)*turbine_rating
        additional_losses = 0.088
        fcr = 0.063
        annual_cost = fcr*capex_function(capacity) + om_function(capacity)
        coe = annual_cost/((1-additional_losses)*aep/1000.0) # $/MW

        return coe
    
# capex_cost = np.array([2 * 1382.0, 1382.0, 1124.0, 966.0, 887.0, 849.0, 792.0, 765.0, 760.0]) # $/kW realistic
capex_cost = np.array([1.15*1438.0, 1438.0, 1316.0, 1244.0, 1199.0, 1173.0, 1133.0, 1124.0, 1120.0])
capex_size = np.array([1.0, 20.0, 50.0, 100.0, 150.0, 200.0, 400.0, 1000.0, 10000.0]) # MW
cost = capex_size*capex_cost*1000.0
# plt.plot(capex_size, capex_cost)
# plt.plot(capex_size, capex_cost2, color="blue")
# plt.show()
capex_function = scipy.interpolate.interp1d(capex_size, cost, kind='cubic')

def om_function(capacity):
    return 37.0*capacity*1000.0

min_spacing = 4.0
rotor_diameter = 130.0
turbine_rating = 3.4
threshold_array = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
# threshold_array = np.array([0.9])

for k in range(len(threshold_array)):
    start = time.time()

    threshold = threshold_array[k]
    threshold = np.round(threshold,2)
    with open('../NAWEA_2023/geometry_new_new_new/polygons_T%s'%threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)

    # xbnd = np.array([-2106699.19553408, -2107312.92248974, -2105869.20198444,
    #     -2105218.56003048, -2106699.19553408])
    # ybnd = np.array([16437.56800016, 14179.61822356, 13780.74687646, 16068.86109147,
    #     16437.56800016])
    
    # xbnds = [885.88111392,  272.15415826, 1715.87466356, 2366.51661752]
    # ybnds = np.array([30225.11532624, 27967.16554964, 27568.29420254, 29856.40841755]) - 27568.29420254

    xbnd_offset = 10.0
    ybnd_offset = 10.0
    xbnds = np.array([885.88111392 + xbnd_offset,  272.15415826 + xbnd_offset, 1715.87466356 - xbnd_offset, 2366.51661752 - xbnd_offset, 885.88111392 + xbnd_offset])
    ybnds = np.array([30225.11532624 - ybnd_offset, 27967.16554964 + ybnd_offset, 27568.29420254 + ybnd_offset, 29856.40841755 - ybnd_offset, 30225.11532624 - ybnd_offset]) - 27568.29420254

    # lowx = 0.0
    # highx = 10000.0
    # lowy = 5000.0
    # highy = lowy + 5000.0

    # limited_area = Polygon(((lowx, lowy), (lowx, highy), (highx, highy), (highx, lowy)))
    limited_area = Polygon((
        (xbnds[0], ybnds[0]),
        (xbnds[1], ybnds[1]),
        (xbnds[2], ybnds[2]),
        (xbnds[3], ybnds[3])
    ))
    full_area = Polygon(((-10.0, -10.0), (-10.0, 2510), (2510, 2510), (2510, -10.0)))
    subtract_polygon = full_area.difference(limited_area)
    limited_polygon = loaded_polygon.difference(subtract_polygon)
    if type(limited_polygon) == Polygon:
        limited_polygon = MultiPolygon([limited_polygon])

    # existing_turbines = np.zeros((len(possible_x), 2))
    # existing_turbines[:, 0] = possible_x[:]
    # existing_turbines[:, 1] = possible_y[:]

    turbine_packing = PackTurbines(min_spacing*rotor_diameter, limited_polygon, weight_x=1E6)
    # turbine_packing.pack_turbines_poly(existing_turbines=existing_turbines)
    turbine_packing.pack_turbines_poly()

    possible_x = turbine_packing.turbine_x
    possible_y = turbine_packing.turbine_y
    # print(possible_x)
    # print(possible_y)

    # plt.figure()
    # plt.plot(possible_x, possible_y, '*')
    # plt.plot(xbnds, ybnds)
    # plt.show()

    # ax = plt.gca()
    # ax.cla()
    # # plot_poly(loaded_polygon,ax=ax)
    # plot_poly(limited_polygon,ax=ax)
    # plt.plot(possible_x, possible_y, '*')
    # plt.plot(xbnds, ybnds)
    # plt.axis("equal")
    # # plt.pause(0.25)
    # plt.show()
    # klj
    # new_turbine_x = turbine_packing.turbine_x
    # new_turbine_y = turbine_packing.turbine_y
    # possible_x = np.append(possible_x, new_turbine_x)
    # possible_y = np.append(possible_y, new_turbine_y)

    fi = FlorisInterface("../files_from_eliot/nawea.yaml")
    fi.reinitialize(wind_directions=[245.], wind_speeds=[8.0])

    nlocs = len(possible_x)
    bits = np.zeros(nlocs,dtype=int)
    bounds = np.zeros((nlocs,2))
    variable_type = np.array([])
    for i in range(nlocs):
        bits[i] = 1
        bounds[i,:] = (0,1)
        variable_type = np.append(variable_type,"int")

    args = (possible_x, possible_y, fi, turbine_rating, capex_function, om_function)
    greedy_optimization = GreedyAlgorithm(bits, bounds, variable_type, objective_function,
                                                    consecutive_increases=3, start_index=1, start_ones=True,
                                                    args=args)
    greedy_optimization.optimize_greedy(print_progress=True)

    optimized_function_value = greedy_optimization.optimized_function_value
    optimized_design_variables = greedy_optimization.optimized_design_variables
    solution_history = greedy_optimization.solution_history


    turbine_array = np.array(optimized_design_variables, dtype=bool)
    turbine_x = possible_x[turbine_array]
    turbine_y = possible_y[turbine_array]

    results_dict = {}
    results_dict["coe"] = float(optimized_function_value)
    results_dict["opt_time"] = float(time.time() - start)
    results_dict["turbine_x"] = turbine_x.tolist()
    results_dict["turbine_y"] = turbine_y.tolist()
    results_filename = 'optimization_results_new_new_new/coe/coe_%s.yml'%(threshold)
    with open(results_filename, 'w') as outfile:
        yaml.dump(results_dict, outfile)
    