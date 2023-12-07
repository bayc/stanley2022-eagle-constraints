import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
import scipy
import yaml

from floris.tools import FlorisInterface
from shapely.geometry import Polygon, MultiPolygon
from plotting_functions import plot_poly, plot_turbines


color_red = "#DE8971"
color_purple = "#7B6079"
color_blue = "#A7D0CD"

threshold_array = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# threshold_array = [0.5]

for k in range(len(threshold_array)):
    start = time.time()

    threshold = threshold_array[k]
    threshold = np.round(threshold,2)
    with open('../../NAWEA_2023/geometry_new_new_new/polygons_T%s'%threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)

    xbnd_offset = 10.0
    ybnd_offset = 10.0
    xbnds = np.array([885.88111392 + xbnd_offset,  272.15415826 + xbnd_offset, 1715.87466356 - xbnd_offset, 2366.51661752 - xbnd_offset, 885.88111392 + xbnd_offset])
    ybnds = np.array([30225.11532624 - ybnd_offset, 27967.16554964 + ybnd_offset, 27568.29420254 + ybnd_offset, 29856.40841755 - ybnd_offset, 30225.11532624 - ybnd_offset]) - 27568.29420254

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

    fig = plt.figure()
    ax = plt.gca()
    alpha = 1.0
    plot_poly(loaded_polygon, ax=ax, color=color_blue,alpha=alpha)
    # turbine_x = np.loadtxt("capacity/spacing8/T%s_turbine_x.npy"%threshold)
    # turbine_y = np.loadtxt("capacity/spacing8/T%s_turbine_y.npy"%threshold)

    fi = FlorisInterface("../../files_from_eliot/nawea.yaml")
    fi.reinitialize(wind_directions=[245.], wind_speeds=[8.0])
    fi_dict = fi.floris.as_dict()
    x_het = fi_dict['flow_field']['heterogenous_inflow_config']['x']
    y_het = fi_dict['flow_field']['heterogenous_inflow_config']['y']
    speed_ups = fi_dict['flow_field']['heterogenous_inflow_config']['speed_multipliers']

    cmsh = ax.pcolormesh(
        np.reshape(x_het, (266, 266)),
        np.reshape(y_het, (266, 266)),
        np.reshape(speed_ups, (266, 266)),
        alpha=0.5,
    )
    fig.colorbar(cmsh,label='velocity aligned\nwith predominant wind dir\n[m/s]')

    with open("../optimization_results_new_new_new/coe/coe_%s.yml"%(threshold), "r") as stream:
        results_data = yaml.safe_load(stream)

    rotor_diameter = 130.0
    turbine_x = results_data["turbine_x"]
    turbine_y = results_data["turbine_y"]
    plot_turbines(turbine_x,turbine_y,rotor_diameter/2.0,ax=ax,color=color_purple)

    plt.plot(xbnds, ybnds)

    plt.savefig("figures_new/layout_%s.png"%k)
    # plt.show()
