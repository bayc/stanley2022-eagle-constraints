import numpy as np
from shapely.geometry import Polygon, MultiPolygon
import pickle

filename = "../abstract/eagle_probability_data.npy"
full_data = np.load(filename)

threshold_array = np.linspace(0.03,1,98)
# threshold_array = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1])
threshold_array = np.array([0.06])
nx, ny = np.shape(full_data)
side_x = np.linspace(0.0,50000.0,nx+1)
side_y = np.linspace(0.0,50000.0,ny+1)

counter = 0
for k in range(len(threshold_array)):
    threshold = threshold_array[k]
    threshold = np.round(threshold,2)
    last_threshold = np.round(threshold - 0.01, 2)
    print(threshold)
    with open('C:/Users/PJ.Stanley/PJ/Projects/stanley2022-eagle-constraints/conference/geometry/polygons_T%s'%last_threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)
    included_polygons = MultiPolygon()
    included_polygons = included_polygons.union(loaded_polygon)
    counter = 0
    for i in range(nx):
        for j in range(ny):
            if full_data[j,i] < threshold and full_data[j,i] >= last_threshold:
                counter += 1
                added_poly = Polygon(((side_x[i],side_y[j]),(side_x[i+1],side_y[j]),
                                        (side_x[i+1],side_y[j+1]),(side_x[i],side_y[j+1])))
                included_polygons = included_polygons.union(added_poly)
    print(counter)
    save_polygon = "geometry/polygons_T%s"%threshold
    with open(save_polygon, "wb") as poly_file:
        pickle.dump(included_polygons, poly_file, pickle.HIGHEST_PROTOCOL)
