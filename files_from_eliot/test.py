from floris.tools import FlorisInterface
from floris.tools.visualization import visualize_cut_plane

import numpy as np
import matplotlib.pyplot as plt


fi = FlorisInterface("heterogeneous_inflow.yaml")
fi.reinitialize(wind_shear=0.0)
fi_dict = fi.floris.as_dict()

print(fi.layout_x)

het_data = np.load('het_wind.npy')
cell_x = np.load('cell_x.npy')
cell_y = np.load('cell_y.npy')

cell_x_min = np.min(cell_x.flatten())
cell_x_max = np.max(cell_x.flatten())
cell_y_min = np.min(cell_y.flatten())
cell_y_max = np.max(cell_y.flatten())
mid_cell_x = (cell_x_max - cell_x_min) / 2 + cell_x_min
mid_cell_y = (cell_y_max - cell_y_min) / 2 + cell_y_min

print(mid_cell_x)
print(mid_cell_y)

x_span = cell_x_max - cell_x_min
y_span = cell_y_max - cell_y_min

# print(x_span)
# print(y_span)
# lkj

xbnd = np.array([-2106699.19553408, -2107312.92248974, -2105869.20198444,
    -2105218.56003048, -2106699.19553408])
ybnd = np.array([16437.56800016, 14179.61822356, 13780.74687646, 16068.86109147,
    16437.56800016])

xbnd_offset = xbnd + np.abs(cell_x_min)
ybnd_offset = ybnd + np.abs(cell_y_min)
# print(xbnd_offset)
# print(ybnd_offset)
# lkj

offset_cell_x = cell_x + np.abs(cell_x_min)
offset_cell_y = cell_y + np.abs(cell_y_min) - 27568.29420254
mid_cell_x_offset = mid_cell_x + np.abs(cell_x_min)
mid_cell_y_offset = mid_cell_y + np.abs(cell_y_min) - 27568.29420254

offset_cell_x_grid, offset_cell_y_grid = np.meshgrid(offset_cell_x, offset_cell_y, indexing='ij')

# print(np.shape(het_data.flatten()))
# print(np.shape(offset_cell_x_grid.flatten()))
# print(np.shape(offset_cell_y_grid.flatten()))
# lkj

fi_dict['flow_field']['heterogenous_inflow_config']['speed_multipliers'] = [het_data.flatten() / 8.0]
fi_dict['flow_field']['heterogenous_inflow_config']['x'] = offset_cell_x_grid.flatten()
fi_dict['flow_field']['heterogenous_inflow_config']['y'] = offset_cell_y_grid.flatten()

# print(mid_cell_x_offset)
# print(mid_cell_y_offset)
# print(np.min(offset_cell_x_grid.flatten()))
# print(cell_x_min)
# lkj

fi_het = FlorisInterface(fi_dict)
fi_het.reinitialize(layout_x = [mid_cell_x_offset], layout_y = [mid_cell_y_offset])
fi_het.floris.to_file('nawea.yaml')

horizontal_plane_2d = fi_het.calculate_horizontal_plane(
    x_resolution=200,
    y_resolution=100,
    height=90.0,
    x_bounds=(np.min(offset_cell_x), np.max(offset_cell_x)),
    y_bounds=(np.min(offset_cell_y), np.max(offset_cell_y))
)
# y_plane_2d = fi_het.calculate_y_plane(x_resolution=200, z_resolution=100, crossstream_dist=mid_cell_x_offset)
# cross_plane_2d = fi_het.calculate_cross_plane(
#     y_resolution=100,
#     z_resolution=100,
#     downstream_dist=mid_cell_x_offset+500.0
# )

# Create the plots
fig, ax_list = plt.subplots(1, 1, figsize=(10, 8))
# ax_list = ax_list.flatten()
visualize_cut_plane(
    horizontal_plane_2d,
    ax=ax_list,
    title="Horizontal",
    color_bar=True,
    label_contours=True
)
xbnds = [885.88111392,  272.15415826, 1715.87466356, 2366.51661752, 885.88111392]
ybnds = np.array([30225.11532624, 27967.16554964, 27568.29420254, 29856.40841755, 30225.11532624])- 27568.29420254
ax_list.plot(xbnds, ybnds)
ax_list.set_xlabel('x')
ax_list.set_ylabel('y')
# visualize_cut_plane(
#     y_plane_2d,
#     ax=ax_list[1],
#     title="Streamwise profile",
#     color_bar=True,
#     label_contours=True
# )
# ax_list[1].set_xlabel('x')
# ax_list[1].set_ylabel('z')
# visualize_cut_plane(
#     cross_plane_2d,
#     ax=ax_list[2],
#     title="Spanwise profile at 500m downstream",
#     color_bar=True,
#     label_contours=True
# )
# ax_list[2].set_xlabel('y')
# ax_list[2].set_ylabel('z')

plt.show()
