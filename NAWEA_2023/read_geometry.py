from json import load
import numpy as np
import matplotlib.pyplot as plt
from plotting_functions import plot_poly
import pickle

ax = plt.gca()
threshold = 0.0
for k in range(1):
    threshold += 0.3
    threshold = np.round(threshold,2)
    with open('geometry_new_new_new/polygons_T%s'%threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)
    ax.cla()
    plot_poly(loaded_polygon,ax=ax)
    plt.axis("equal")
    # plt.pause(0.25)
    plt.show()