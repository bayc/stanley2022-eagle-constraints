import matplotlib.pyplot as plt
plt.style.use('presentation')
import numpy as np
import scipy

capex_cost = np.array([1.15*1438.0, 1438.0, 1316.0, 1244.0, 1199.0, 1173.0, 1133.0, 1124.0, 1120.0])
capex_size = np.array([1.0, 20.0, 50.0, 100.0, 150.0, 200.0, 400.0, 1000.0, 10000.0]) # MW
capex_function = scipy.interpolate.interp1d(capex_size, capex_cost, kind='cubic')

capacity = np.linspace(1,400,100)

plt.figure(figsize=(4,4.5))
ax = plt.subplot(111)
ax.plot(capacity, capex_function(capacity), color="C0")

ax.set_xlabel("capacity (MW)")
ax.set_ylabel("capital cost ($/kW)")

ax.grid()

plt.tight_layout()

plt.savefig("figures/cost_curve.png", transparent=True)
plt.show()

