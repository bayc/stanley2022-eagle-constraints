import matplotlib.pyplot as plt
# plt.style.use('presentation')
import numpy as np
import scipy
from wind_design_tools import plotting_functions

plt.figure(figsize=(6,5))
ax = plt.subplot(111)

H = 119.0
D = 198.0
plotting_functions.plot_turbine_def(H, D, ax=ax, color="C0", angle=92.0, labels=True, labelfontsize=24, linewidth=2, labellinewidth=2)
# plt.savefig("figures/cost_curve.png", transparent=True)
plt.show()

