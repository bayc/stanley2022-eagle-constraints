import numpy as np
from shapely.geometry import Polygon, MultiPolygon
import pickle

filename = "eagle_probability_data.npy"
full_data = np.load(filename)

threshold = np.linspace(0.01,1,100)
nx, ny = np.shape(full_data)
side_x = np.linspace(0.0,50000.0,nx+1)
side_y = np.linspace(0.0,50000.0,ny+1)

for k in range(len(threshold)):
    print(threshold[k])
    included_polygons = MultiPolygon()
    for i in range(nx):
        for j in range(ny):
            if full_data[j,i] < threshold[k]:
                added_poly = Polygon(((side_x[i],side_y[j]),(side_x[i+1],side_y[j]),
                                        (side_x[i+1],side_y[j+1]),(side_x[i],side_y[j+1])))
                included_polygons = included_polygons.union(added_poly)
    save_polygon = "geometry/polygons_T%s"%threshold[k]
    with open(save_polygon, "wb") as poly_file:
        pickle.dump(included_polygons, poly_file, pickle.HIGHEST_PROTOCOL)
