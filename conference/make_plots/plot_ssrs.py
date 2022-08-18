import matplotlib.cm as cm
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec
import os
from wind_design_tools import plotting_functions


yellow = 'FBCE07'
red = 'DD1D21'
white = 'FFFFFF'
colormap = plotting_functions.get_continuous_cmap([red, white])


import matplotlib.pyplot as plt
plt.style.use('presentation')
import numpy as np


filename = "../../abstract/eagle_probability_data.npy"
full_data = np.load(filename)

plt.pcolor(full_data, vmax=0.15, cmap=colormap)
cbar = plt.colorbar()
cbar.set_label('relative presence', fontsize=12)
plt.axis("square")

plt.xticks((0, 200, 400, 600, 800, 1000))
plt.gca().set_xticklabels(("0", "10", "20", "30", "40", "50"))
plt.yticks((0, 200, 400, 600, 800, 1000))
plt.gca().set_yticklabels(("0", "10", "20", "30", "40", "50"))
plt.xlabel("West to East (km)")
plt.ylabel("South to North (km)")

plt.savefig("figures/ssrs_fig.png", transparent=True)
plt.show()
