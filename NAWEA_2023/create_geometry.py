import numpy as np
from shapely.geometry import Polygon, MultiPolygon
import pickle
from plotting_functions import plot_poly
import matplotlib.pyplot as plt

filename = "new_eagle_data_cropped.npy"
# filename = "eagle_probability_data.npy"
full_data = np.load(filename)
full_data = full_data / np.max(full_data)
# print(full_data)
# print(np.shape(full_data))
# print(np.min(np.nan_to_num(full_data)))
# print(np.max(np.nan_to_num(full_data)))
# lkj

threshold = np.linspace(0.1,1,10)
# threshold = np.linspace(0.01,1,10)
nx, ny = np.shape(full_data)
print(nx)
print(ny)
# side_x = np.linspace(0.0,50000.0,nx+1)
# side_y = np.linspace(0.0,50000.0,ny+1)
side_x = np.linspace(0.0,2500.0,nx+1)
side_y = np.linspace(0.0,2500.0,ny+1)

for k in range(len(threshold)):
    print(threshold[k])
    included_polygons = MultiPolygon()
    for i in range(nx):
        for j in range(ny):
            if full_data[j,i] < threshold[k]:
                added_poly = Polygon(((side_x[i],side_y[j]),(side_x[i+1],side_y[j]),
                                        (side_x[i+1],side_y[j+1]),(side_x[i],side_y[j+1])))
                included_polygons = included_polygons.union(added_poly)
    save_polygon = "geometry_new_new_new/polygons_T%s"%threshold[k]
    with open(save_polygon, "wb") as poly_file:
        pickle.dump(included_polygons, poly_file, pickle.HIGHEST_PROTOCOL)

# ax = plt.gca()
# ax.cla()
# plot_poly(included_polygons,ax=ax)
# plt.axis("equal")
# plt.show()