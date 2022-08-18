from json import load
import numpy as np
import matplotlib.pyplot as plt
import pickle
from plotting_functions import plot_poly, plot_turbines

from plotting_functions import plot_poly

color_red = "#DE8971"
color_purple = "#7B6079"
color_blue = "#A7D0CD"

rotor_diameter = 164.0
alpha=1.0

plt.figure(figsize=(6,2.1))
ax1 = plt.subplot(131)
ax2 = plt.subplot(132)
ax3 = plt.subplot(133)

ax1.axis("equal")
ax1.axis("off")
ax2.axis("equal")
ax2.axis("off")
ax3.axis("equal")
ax3.axis("off")

threshold = 0.01
with open('geometry/polygons_T%s'%threshold, "rb") as poly_file:
    loaded_polygon = pickle.load(poly_file)
plot_poly(loaded_polygon, ax=ax1, color=color_blue,alpha=alpha)
turbine_x = np.loadtxt("capacity/spacing8/T%s_turbine_x.npy"%threshold)
turbine_y = np.loadtxt("capacity/spacing8/T%s_turbine_y.npy"%threshold)
plot_turbines(turbine_x,turbine_y,rotor_diameter/2.0,ax=ax1,color=color_purple)

threshold = 0.05
with open('geometry/polygons_T%s'%threshold, "rb") as poly_file:
    loaded_polygon = pickle.load(poly_file)
plot_poly(loaded_polygon, ax=ax2, color=color_blue,alpha=alpha)
turbine_x = np.loadtxt("capacity/spacing8/T%s_turbine_x.npy"%threshold)
turbine_y = np.loadtxt("capacity/spacing8/T%s_turbine_y.npy"%threshold)
plot_turbines(turbine_x,turbine_y,rotor_diameter/2.0,ax=ax2,color=color_purple)

threshold = 0.1
with open('geometry/polygons_T%s'%threshold, "rb") as poly_file:
    loaded_polygon = pickle.load(poly_file)
plot_poly(loaded_polygon, ax=ax3, color=color_blue,alpha=alpha)
turbine_x = np.loadtxt("capacity/spacing8/T%s_turbine_x.npy"%threshold)
turbine_y = np.loadtxt("capacity/spacing8/T%s_turbine_y.npy"%threshold)
plot_turbines(turbine_x,turbine_y,rotor_diameter/2.0,ax=ax3,color=color_purple)

p = 0.9
ax1.set_title("1% eagle probability threshold",y=p,fontsize=8)
ax2.set_title("5% eagle probability threshold",y=p,fontsize=8)
ax3.set_title("10% eagle probability threshold",y=p,fontsize=8)
plt.subplots_adjust(top=0.99,right=0.99,left=0.01,bottom=0.01,wspace=0.05)

# plt.savefig("figures/layouts.pdf",transparent=True)
plt.show()