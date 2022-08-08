import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from plotting_functions import plot_poly
import matplotlib.pyplot as plt



filename = "eagle_probability_data.npy"
full_data = np.load(filename)

threshold = 0.00001
nx, ny = np.shape(full_data)
included_polygons = MultiPolygon()
side_x = np.linspace(0.0,50000.0,nx+1)
side_y = np.linspace(0.0,50000.0,ny+1)
for i in range(nx):
    for j in range(ny):
        if full_data[j,i] < threshold:
            added_poly = Polygon(((side_x[i],side_y[j]),(side_x[i+1],side_y[j]),
                                    (side_x[i+1],side_y[j+1]),(side_x[i],side_y[j+1])))
            included_polygons = included_polygons.union(added_poly)

plot_poly(included_polygons)
plt.axis("equal")
plt.show()