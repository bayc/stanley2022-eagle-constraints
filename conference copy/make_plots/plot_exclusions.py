from json import load
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time
plt.style.use('presentation')

from shapely.geometry import Polygon, MultiPolygon
from wind_design_tools import plotting_functions, pack_turbs

min_spacing = 6
rotor_diameter = 198.0
turbine_rating = 10.0
threshold_array = np.arange(10)/100.0 + 0.01

fig = plt.figure()
ax1 = plt.subplot(111)
ax2 = fig.add_axes([0.85,0.128,0.075,0.79])
for k in range(len(threshold_array)):
    start = time.time()

    threshold = threshold_array[k]
    threshold = np.round(threshold,2)
    with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/conference/geometry/polygons_T%s'%threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)

    ax1.cla()
    ax2.cla()
    plotting_functions.plot_poly(loaded_polygon, ax=ax1, alpha=1.0)
    ax1.axis("square")
    # plt.suptitle("threshold: %s"%threshold)

    ax1.axis("off")
    x = [0,1,1,0]
    y = [0,0,threshold,threshold]
    ax2.fill(x, y, color="C1")
    ax2.axis("off")
    ax2.set_ylim(0,0.1)
    ax2.text(0.5, 0.05, "%s"%np.round(threshold,2), verticalalignment="center", horizontalalignment="center",
             fontsize=12, weight="bold")
            
    plt.tight_layout()
    plt.pause(0.001)
    plt.savefig("figures/exculsions%s.png"%k)

plt.show()
    