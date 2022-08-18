from json import load
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
import scipy
import yaml

from floris.tools import FlorisInterface
from shapely.geometry import Polygon, MultiPolygon

plt.style.use('presentation')

def objective_function(turbine_x, turbine_y, args):
    (fi, turbine_rating, capex_function, om_function) = args

    fi.reinitialize( layout=( turbine_x, turbine_y ) )
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

    return aep, coe, capacity
    

capex_cost = np.array([1.15*1438.0, 1438.0, 1316.0, 1244.0, 1199.0, 1173.0, 1133.0, 1124.0, 1120.0])
capex_size = np.array([1.0, 20.0, 50.0, 100.0, 150.0, 200.0, 400.0, 1000.0, 10000.0]) # MW
cost = capex_size*capex_cost*1000.0

capex_function = scipy.interpolate.interp1d(capex_size, cost, kind='cubic')

def om_function(capacity):
    return 37.0*capacity*1000.0

min_spacing = 6
rotor_diameter = 198.0
turbine_rating = 10.0
threshold_array = np.arange(10)/100.0 + 0.01
threshold_array = threshold_array[::-1] 

lowy_array = [3, 0, 1, 2, 5, 4, 6, 7, 8, 9]
lowy_array = [3,9,0]
lowy_array = [3]

scale = 1.4
plt.figure(figsize=(10*scale, 4*scale))
ax1 = plt.subplot(121)
ax2 = plt.subplot(122)
# ax3 = plt.subplot(133)
for j in range(len(lowy_array)):
    aep_array = np.zeros(len(threshold_array))
    coe_array = np.zeros(len(threshold_array))
    capacity_array = np.zeros(len(threshold_array))
    area_array = np.zeros(len(threshold_array))
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
        total_area = 10000.0 * 5000.0

        limited_area = Polygon(((lowx, lowy), (lowx, highy), (highx, highy), (highx, lowy)))
        full_area = Polygon(((-10.0, -10.0), (-10.0, 50010), (50010, 50010), (50010, -10.0)))
        subtract_polygon = full_area.difference(limited_area)
        limited_polygon = loaded_polygon.difference(subtract_polygon)
        print(type(limited_polygon))
        if type(limited_polygon) == Polygon:
            limited_polygon = MultiPolygon([limited_polygon])

        available_area = limited_polygon.area
        
        fi = FlorisInterface("../conference.yaml")
        fi.reinitialize(wind_directions=[270.], wind_speeds=[11.0])

        args = (fi, turbine_rating, capex_function, om_function)

        # with open("../optimization_results/capacity/capacity%s_%s.yml"%(int(lowy_array[j]), threshold), "r") as stream:
        with open("../optimization_results/coe/coe%s_%s.yml"%(int(lowy_array[j]), threshold), "r") as stream:
            results_data = yaml.safe_load(stream)
        # results_data = yaml.load(results_file)
        turbine_x = results_data["turbine_x"]
        turbine_y = results_data["turbine_y"]

        aep_array[k], coe_array[k], capacity_array[k] = objective_function(turbine_x, turbine_y, args)
        area_array[k] = available_area / total_area 
    
    
    # ax1.cla()
    # ax2.cla()
    # ax3.cla()
    ax1.plot(threshold_array, capacity_array, linewidth=4, color="C%s"%j)
    ax2.plot(threshold_array, coe_array, linewidth=4, color="C%s"%j)
    # ax3.plot(threshold_array, area_array, color="C%s"%j)
    # ax3.plot(area_array, capacity_array, color="C%s"%j)
    # ax3.plot(area_array, coe_array, color="C%s"%j)

    # plt.suptitle("maximize capacity", fontsize=24)
    plt.suptitle("minimize COE", fontsize=24)
    # ax1.set_title("capacity")
    # ax2.set_title("COE")
    ax1.set_xlabel("exclusion threshold", fontsize=24)
    ax2.set_xlabel("exclusion threshold", fontsize=24)
    ax1.set_ylabel("capacity (MW)")
    ax2.set_ylabel("COE ($/MWh)")
    # ax3.set_title("area fraction")
    

    ax1.set_ylim((-20,420))
    ax2.set_ylim((29, 41))
    ax1.set_xticks((0,0.05,0.1))
    ax2.set_xticks((0,0.05,0.1))
    # ax3.set_ylim((-0.05,1.05))
    # ax3.set_ylim((-20,420))
    # ax3.set_ylim((30, 40))

    plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.2, wspace=0.6)
    
    plt.pause(0.001)
plt.savefig("figures/coe1.png")
plt.show()

