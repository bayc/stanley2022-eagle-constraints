import numpy as np
import matplotlib.pyplot as plt
import pickle

color_red = "#DE8971"
color_purple = "#7B6079"
color_blue = "#A7D0CD"

turbine_capacity = 6.0

threshold = np.linspace(0.01,1,100)
threshold = np.round(threshold,2)
N = 25

plt.figure(figsize=(6,2))

# CAPACITY
ax1 = plt.subplot(131)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
# ax1_b = ax1.twinx()

nturbs_6 = np.loadtxt("capacity/spacing6/nturbs.npy")
ax1.plot(threshold[0:N],nturbs_6[0:N],"o",markersize=3,color=color_red,label="6")
# ax1_b.plot(threshold[0:N],nturbs_6[0:N]*turbine_capacity/1000,"o",markersize=3,color=color_red)

nturbs_8 = np.loadtxt("capacity/spacing8/nturbs.npy")
ax1.plot(threshold[0:N],nturbs_8[0:N],"o",markersize=3,color=color_purple,label="8")
# ax1_b.plot(threshold[0:N],nturbs_8[0:N]*turbine_capacity/1000,"o",markersize=3,color=color_purple)

nturbs_10 = np.loadtxt("capacity/spacing10/nturbs.npy")
ax1.plot(threshold[0:N],nturbs_10[0:N],"o",markersize=3,color=color_blue,label="10")
# ax1_b.plot(threshold[0:N],nturbs_10[0:N]*turbine_capacity/1000,"o",markersize=3,color=color_blue)

ax1.set_xlabel("eagle probablilty\nthreshold",fontsize=8)
ax1.set_ylabel("number of turbines",labelpad=-0.1,fontsize=8)
# ax1_b.set_ylabel("capacity (GW)")
# ax1.legend(title="min spacing (D)")
ax1.text(0.08,2000,"6 D spacing",color=color_red,weight="bold",fontsize=8)
ax1.text(0.08,1600,"8 D spacing",color=color_purple,weight="bold",fontsize=8)
ax1.text(0.08,550,"10 D spacing",color=color_blue,weight="bold",fontsize=8)

# CAPACITY DENSITY

areas = np.zeros(100)
for k in range(100):
    with open('geometry/polygons_T%s'%threshold[k], "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)
    areas[k] = loaded_polygon.area/1E6

ax2 = plt.subplot(132)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
ax2.plot(threshold[0:N],areas[0:N]/areas[-1],"o",markersize=3,color=color_blue)
ax2.set_yticks((0.4,0.6,0.8))
ax2.set_yticklabels(("40","60","80"))
ax2.set_xlabel("eagle probablilty\nthreshold",fontsize=8)
ax2.set_ylabel("non-excluded\narea (%)",labelpad=-0.1,fontsize=8)

ax3 = plt.subplot(133)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
ax3.plot(threshold[0:N],nturbs_6[0:N]*turbine_capacity/areas[0:N],"o",markersize=3,color=color_red)
ax3.plot(threshold[0:N],nturbs_8[0:N]*turbine_capacity/areas[0:N],"o",markersize=3,color=color_purple)
ax3.plot(threshold[0:N],nturbs_10[0:N]*turbine_capacity/areas[0:N],"o",markersize=3,color=color_blue)
ax3.set_xlabel("eagle probablilty\nthreshold",fontsize=8)
ax3.set_ylabel("capacity density\n(MW/km2)",labelpad=-0.1,fontsize=8)

plt.subplots_adjust(top=0.99,right=0.99,left=0.11,bottom=0.3,wspace=0.4)



plt.savefig("figures/nturbs.pdf",transparent=True)
plt.show()