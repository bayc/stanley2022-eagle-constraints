from json import load
from struct import pack
import numpy as np
from pack_turbs import PackTurbines
import pickle
from shapely.geometry import Polygon, MultiPolygon

min_spacing = 6
rotor_diameter = 164.0
threshold = 0.0
for k in range(100):
    threshold += 0.01
    threshold = np.round(threshold,2)
    with open('geometry/polygons_T%s'%threshold, "rb") as poly_file:
        loaded_polygon = pickle.load(poly_file)

    if type(loaded_polygon) == Polygon:
        loaded_polygon = MultiPolygon([loaded_polygon])

    pack_turbs = PackTurbines(min_spacing*rotor_diameter, loaded_polygon)
    pack_turbs.pack_turbines_poly()
    turbine_x = pack_turbs.turbine_x
    turbine_y = pack_turbs.turbine_y

    with open("capacity/spacing6/nturbs.npy", "ab") as f:
        np.savetxt(f, [len(turbine_x)])
    
    np.savetxt("capacity/spacing6/T%s_turbine_x.npy"%threshold, turbine_x)
    np.savetxt("capacity/spacing6/T%s_turbine_y.npy"%threshold, turbine_y)