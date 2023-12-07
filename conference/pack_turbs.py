# -*- coding: utf-8 -*-
"""
turbine packing module.
"""
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, Point
from plotting_functions import get_xy

class PackTurbines():
    """Framework to maximize plant capacity in a provided wind plant area.
    """

    def __init__(self, min_spacing, safe_polygons, weight_x=1E-6):
        """
        Parameters
        ----------
        min_spacing : float
            The minimum allowed spacing between wind turbines.
        safe_polygons : Polygon | MultiPolygon
            The "safe" area(s) where turbines can be placed without
            violating boundary, setback, exclusion, or other constraints.
        weight_x : float, optional
        """

        self.min_spacing = min_spacing
        self.safe_polygons = safe_polygons
        self.weight_x = weight_x

        # turbine locations
        self.turbine_x = np.array([])
        self.turbine_y = np.array([])

    def pack_turbines_poly(self):
        """Fast packing algorithm that maximizes plant capacity in a
        provided wind plant area. Sets the the optimal locations to
        self.turbine_x and self.turbine_y
        """

        if self.safe_polygons.area > 0.0:
            can_add_more = True
            leftover = MultiPolygon(self.safe_polygons)
            while can_add_more:
                if leftover.area > 0:
                    nareas = len(leftover.geoms)
                    areas = np.zeros(len(leftover.geoms))
                    for i in range(nareas):
                        areas[i] = leftover.geoms[i].area
                    m = min(i for i in areas if i > 0)
                    ind = np.where(areas == m)[0][0]
                    smallest_area = leftover.geoms[ind]
                    exterior_coords = smallest_area.exterior.coords[:]
                    x, y = get_xy(exterior_coords)
                    metric = self.weight_x * x + y
                    index = np.argmin(metric)
                    self.turbine_x = np.append(self.turbine_x,
                                               x[index])
                    self.turbine_y = np.append(self.turbine_y,
                                               y[index])
                    new_turbine = Point(x[index],
                                        y[index]
                                        ).buffer(self.min_spacing)
                else:
                    break
                leftover = leftover.difference(new_turbine)
                if isinstance(leftover, Polygon):
                    leftover = MultiPolygon([leftover])

    def clear(self):
        """Reset the packing algorithm by clearing the x and y turbine arrays
        """
        self.turbine_x = np.array([])
        self.turbine_y = np.array([])

