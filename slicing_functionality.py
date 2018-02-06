from shapely.geometry import Polygon, LineString, LinearRing, MultiLineString, Point
from shapely import affinity
from Globals import machine, g
import numpy as np
import math

# rotation = 90

def make_islands(points: list):
    """
    Takes a list of points and returns a list of lists - a list for each island.
    An island is the same collection of points as the input, ordered for efficient traversal.
    :param points: points to be analyzed
    :return:
    """
    from operator import itemgetter
    from itertools import groupby, islice

    points.sort(key=lambda x: (x[0], x[1]))
    islands = []

    #  Pathtrace islands
    while len(points) > 0:
        islands.append([e for _, g in groupby(points, itemgetter(0)) for e in islice(g, 2)])
        points = [e for _, g in groupby(points, itemgetter(0)) for e in islice(g, 2, None)]
    #  Sort the points in a zig-zag order
    zig_zag_islands = []
    for island in islands:
        for i, x in enumerate(island):
            if i != 0 and i % 4 == 0:
                if x[0] == island[i - 1][0]:
                    island[i], island[i - 1] = island[i - 1], island[i]
        zig_zag_islands.append(island)

    return islands


def find_intersections(polygon: Polygon, coef_w_raft):
    """
    Takes a shapely polygon as an input, finds the bounding box,
    plots vertical lines through the bounding box, using nozzle path width
    as the spacing interval.
    :param polygon:
    :return:
    """

    # if rotation != 0:
    #     polygon = affinity.rotate(polygon, rotation)

    ring = LinearRing(polygon.exterior)
    bounds = polygon.bounds
    width = machine.nozzle.size_id * coef_w_raft

    lines = []
    for line in range(int(abs(bounds[0]-bounds[2]) / width) + 1):
        temp = []
        temp.append((bounds[0] + line * width, bounds[1]))
        temp.append((bounds[0] + line * width, bounds[3]))

        lines.append(LineString(temp))

    multiline = MultiLineString(lines)

    intersections = ring.intersection(multiline)
    return intersections


def points_to_coords(points, mode : str ="absolute"):
    """
    Takes shapely points as input and converts to a list of lists of floats,
    containing the respective points
    :param points:
    :param mode: Can be either "absolute" or "relative"
    :return:
    """
    output = []
    for point in points:
        output.append([point.x, point.y])
    return output


def sort_coords(coords: list):
    """
    Takes a list of lists of floats or ints, and sorts them in an ascending order.
    X is the primary key, Y is secondary.
    :param coords:
    :return:
    """
    return coords.sort(key=lambda x: (x[0], x[1]))


def make_perimeter(polygon: Polygon, outlines: int = 1):
    """
    Takes an input Polygon object, saves its perimeter and erodes it.
    Repeats it "outlines" amount of times
    :param polygon:
    :param outlines:
    :return:
    """
    perimeters = []
    for outline in range(outlines):
        perimeters.append(LinearRing(polygon.exterior))
        polygon = polygon.buffer(-machine.settings.path_width)

    return polygon, perimeters


def make_raft_structures(origin_matrix, circumradius, edges, safe_distance):
    """
    Takes 2D origin points of test structures, the circumradius of those structures, their edge count, as well as
    the safe printing distance offset. It first finds the bounding cases of the origins in order to determine the border
    case scenarios.
    :param origin_matrix:
    :param circumradius:
    :param edges:
    :param safe_distance:
    :return:
    """
    figures = []
    min_origin = min(origin_matrix)
    max_origin = max(origin_matrix)
    for origin in origin_matrix:
        center = (origin[0] + circumradius * math.cos(np.pi * (edges - 2) / (2 * edges)),
                  origin[1] + circumradius * math.sin(np.pi * (edges - 2) / (2 * edges)))

        square = [(center[0] - circumradius, center[1] - circumradius),
                  (center[0] - circumradius, center[1] + circumradius),
                  (center[0] + circumradius, center[1] + circumradius),
                  (center[0] + circumradius, center[1] - circumradius)]

        structure = Polygon(square) # Polygon(Point(center).buffer(circumradius).simplify(0.05))


        dilated = structure.buffer(2)
        # for direction in range(4):
        #     # Filter out the border cases
        #     if origin[0] == min_origin[0] and direction == 3:
        #         pass
        #     elif origin[0] == max_origin[0] and direction == 0:
        #         pass
        #     elif origin[1] == min_origin[1] and direction == 2:
        #         pass
        #     elif origin[1] == max_origin[1] and direction == 1:
        #         pass
        #     else:
        #         _turn = {0: (1, 0),
        #                  1: (0, 1),
        #                  2: (0, -1),
        #                  3: (-1, 0)}
        #         if direction != 1 & direction != 3:
        #             start = (center[0], center[1])
        #             _line_coords = np.array(start) + np.array(_turn[direction]) * (safe_distance - circumradius - 2.8)
        #             line = LineString([start, _line_coords])
        #             line_dilated = line.buffer(2)
        #             dilated = dilated.union(line_dilated)
        figures.append(structure)  # dilated
    return figures


def get_orientation(polygon: Polygon):
    """
    Take a polygon, gets its bounds gives Y
    :param polygon:
    :return:
    """
    bounds = polygon.bounds

    if abs(bounds[0])+ abs(bounds[2])>abs(bounds[1])+abs(bounds[3]):
        return "horizontal"
    else:
        return "vertical"


def rotate(points, origin, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    angle = math.radians(angle)
    output = []
    for point in points:
        ox, oy = origin
        px, py, extrude = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        output.append((qx, qy, extrude))
    return output


def absolute_to_relative(points: list):
    """
    Takes a list of coordinates, and converts them to relative coordinates by subtracting each set of coordinates
    from the next one. The first set of coordinates is appended to the output without any subtraction.
    :param points:
    :return:
    """
    output = []
    for i, x in enumerate(points):
        if i == 0:
            output.append(x)
        else:
            output.append(tuple(np.subtract(points[i-1], x)))
    return output


def points_to_toolpaths(points, coef_w, coef_h, mode: str = "relative", g = g, rotation: bool = False):
    """
    Takes a list of points, as a list of tuples with 3 fields - x coordinate, y coordinate and extrusion argument (True or False).
    If the extrusion argument is True, it extrudes at a previously defined feedrate.
    If the extrusion argument is False, initiates a travel move by storing the previous feedrate in a temporary variable, changes the feedrate
    to 100 m/s, moves and then switches back to the original feedrate.
    :param points:
    :param coef_w:
    :param coef_h:
    :param mode:
    :param rotation:
    :return:
    """
    move = g.move if mode == "relative" else g.abs_move
    if rotation:
        points = rotate(points, (0,0), 90)
    for i, point in enumerate(points):
        if point[2] == -1.0:
            speed = g.speed
            g.feed(100)
            move(x=point[0], y=point[1], coef_h=coef_h, coef_w=coef_w, extrude=False)
            g.feed(speed / 60)
        else:
            move(x=point[0], y=point[1], coef_h=coef_h, coef_w=coef_w, extrude=True)
    g.extrude = False


def infill(polygon: Polygon, coef_w_raft, coef_h_raft, g = g, outlines: int = 1, debug: bool = False):

    g.write("; Printing raft")
    def extrusion_switch(points: list):
        """
        An assistant function for making sure that extrusion is off when switching between islands and perimeters.
        :param points:
        :return:
        """
        for i, x in enumerate(points):
            if i == len(points) - 1:
                points[i] = (points[i][0], points[i][1], False)
            else:
                points[i] = (points[i][0], points[i][1], True)
        return points

    figure = polygon
    points_final = [(0, 0, False)]
    poly, perimeter = make_perimeter(Polygon(figure).simplify(0.05, preserve_topology=False),
                                     outlines)  # Get outlines, and the remaining polygon

    for x in perimeter:
        points_final.extend(extrusion_switch(list(x.coords)))

    output = make_islands(points_to_coords(find_intersections(poly, coef_w_raft)))
    for island in output:
        # Pass islands to GCODE here
        points_final.extend(extrusion_switch(island))

    points_to_toolpaths(absolute_to_relative(points_final), coef_w_raft, coef_h_raft, g=g, rotation= True)
    g.write("; Raft Finished")


def raft_structure(circumradius:int or float, structure: str = "circle"):
    """
    Takes circumradius (int or float), and exports a shapely circle as a polygon
    :param circumradius: Circumradius of the raft structure
    :type circumradius: int or float
    :param structure: Type of geometry
    :type structure: str
    :return:
    """
    if structure == "circle":
        return Polygon(Point(0, 0).buffer(circumradius).simplify(0.05, preserve_topology=True))
    if structure == "square":
        return Polygon([[-circumradius, -circumradius],
                        [-circumradius, circumradius],
                        [circumradius, circumradius],
                        [circumradius, -circumradius]]).buffer(0.1)