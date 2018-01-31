from __future__ import division
from matplotlib import pyplot
from matplotlib import ticker
from matplotlib import patches
from slicing_functionality import raft_structure
import math
from shapely.geometry import Polygon, LineString, Point, MultiPolygon
from descartes.patch import PolygonPatch
# from testbed import matrix_size, safe_distance, origin_matrix, circumradius, edges
import numpy as np

from figures import BLUE, GREEN, SIZE, RED, set_limits, plot_coords, color_isvalid, plot_line

# diameter = circumradius * 2

fig = pyplot.figure(1, figsize=SIZE, dpi=120)
buffer = 2

# Borderline coordinates for edge case detection
# min_origin = min(origin_matrix)
# max_origin = max(origin_matrix)

# 1: valid polygon
ax = fig.add_subplot(111)  # pirmais subplots
ax.plot(solid_capstyle='round')
set_limits(ax, -110, 110, -110, 110)
circle = patches.Circle((0, 0), 100, fc=GREEN, ec=GREEN, alpha=0.3, zorder=1)
ax.add_patch(circle)

# for origin in origin_matrix:
#     center = (origin[0] + circumradius * math.cos(np.pi * (edges - 2) / (2 * edges)),
#               origin[1] + circumradius * math.sin(np.pi * (edges - 2) / (2 * edges)))
#     line_dilated = None
#     structure = Polygon(Point(center).buffer(circumradius).simplify(0.05))
#     dilated = structure.buffer(buffer)
#     polygons = []
#     for direction in range(4):
#         # Filter out the border cases
#         if origin[0] == min_origin[0] and direction == 3:
#             pass
#         elif origin[0] == max_origin[0] and direction == 0:
#             pass
#         elif origin[1] == min_origin[1] and direction == 2:
#             pass
#         elif origin[1] == max_origin[1] and direction == 1:
#             pass
#         else:
#             _turn = {0: (1, 0),
#                      1: (0, 1),
#                      2: (0, -1),
#                      3: (-1, 0)}
#             if direction != 1 & direction != 3: # Addition for limiting support amount for their longer version
#                 start = (center[0], center[1])
#                 _line_coords = np.array(start) + np.array(_turn[direction]) * (safe_distance - circumradius - 2.8)
#                 line = LineString([start, _line_coords])
#                 line_dilated = line.buffer(2)
#                 line_poly = PolygonPatch(line_dilated.__geo_interface__, fc=BLUE, ec=BLUE, alpha=0.5, zorder=3)
#                 line_dilated = line_dilated.difference(dilated)
#                 polygons.append(line_dilated)
#         multi_poly = MultiPolygon(polygons)
#
#     patch = PolygonPatch(dilated, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
#     [ax.add_patch(PolygonPatch(polygon, fc=RED, ec=RED, alpha=0.5, zorder=2)) for polygon in polygons]
#     ax.add_patch(patch)

ax.add_patch(PolygonPatch(raft_structure(7,"square")))
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.grid(which='major')
ax.grid(which='minor', linestyle='--', linewidth = 0.2)

pyplot.show()
