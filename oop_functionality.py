import math

import numpy as np

import slicing_functionality as sf
from Globals import machine, g

path = "gcode.gcode"
tests = {}
header = r'header'
footer = r'footer'


class Prism(object):
    def __init__(self, edges, x, y, z, circumradius, layers, coef_h, coef_w, perimeters=1, outline_overlap=1, cooling = 100, extrusion_multiplier=1, raft: bool = True, g= g): # TODO here all of the relevant properties should be explicitly defined!
        points = [[0, 0, 0, False]]

        self.origin = (x, y, z)  # To be used for Shapely drawing
        self.center = (self.origin[0] + circumradius * math.cos(np.pi * (edges - 2) / (2 * edges)),
                       self.origin[1] + circumradius * math.sin(np.pi * (edges - 2) / (2 * edges)))
        temp_speed = g.speed
        g.feed(100) # TODO
        if raft:
            g.abs_move(self.center[0], self.center[1], machine.settings.path_height, extrude=False)
            g.feed(8)  # set speed for raft TODO
            sf.infill(sf.raft_structure(circumradius*1.35, "square"),1, g=g)
            g.feed(temp_speed / 60)
        g.abs_move(x, y, z if not raft else z + 2 * machine.settings.path_height, extrude=False)  # TODO

        g.set_part_cooling(cooling)

        side = circumradius * 2 * math.sin(np.pi / edges)
        # angle = np.rad2deg(np.pi * (edges - 2) / edges)

        for l in range(0, layers):
            if l > 0:
                points.append([0, 0, machine.nozzle.size_id*coef_h, False])

            for p in range(0, perimeters):
                step = (100 - outline_overlap) * machine.nozzle.size_id*coef_w / 100

                if p != 0:
                    if edges == 3:
                        step_x = step / np.abs(math.sin(np.pi * (edges - 2) / (2*edges)))
                        step_y = step
                    elif edges == 4:
                        step_x = step
                        step_y = step * (1 / np.abs(math.sin(np.pi * (edges - 2) / edges)) + 1 / np.abs(math.tan(np.pi * (edges - 2) / edges)))
                    elif edges > 4:
                        step_x = step / np.abs(math.tan(np.pi * (edges - 2) / (2 * edges)))
                        step_y = step

                elif p == 0:
                        step_x = 0
                        step_y = 0

                points.append([step_x, step_y, 0, False])

                for n in range(0, edges):

                    offset = 2 * step / np.abs(math.tan(np.pi * (edges - 2) / (2 * edges)))

                    x_coord = (side - p * offset) * math.cos(2 * np.pi * n / edges)
                    y_coord = (side - p * offset) * math.sin(2 * np.pi * n / edges)
                    points.append([x_coord, y_coord, 0, True])

            points.append([-step_x * p, -step_y * p, 0, False])

        for i, point in enumerate(points):
            if point[3] is True:
                g.move(x=point[0], y=point[1], z=point[2], coef_h=coef_h, coef_w=coef_w, extrude=True)
            elif point[3] is False:
                #temp_speed = g.speed
                #g.feed(100)
                g.move(x=point[0], y=point[1], z=point[2], coef_h=0, coef_w=0, extrude=False)
                #g.feed(temp_speed / 60)

        g.move(z=10, extrude=False) # Large lift between structures
        g.extrude = False

    def points(self):
        return self.points


def points_to_toolpaths(points: list, coef_h, coef_w, g=g):
    for i, point in enumerate(points):
        if point[2] is None:
            point[2] = 0
        if point[3] is None:
            point[3] = True
        if point[3] is True:
            g.move(x=point[0], y=point[1], z=point[2], coef_h=coef_h, coef_w=coef_w, extrude=True)
        elif point[3] is False:
            g.move(x=point[0], y=point[1], z=point[2], coef_h=coef_h, coef_w=coef_w, extrude=True)


def clean_nozzle():
    """
    Wipes nozzle from a starting point, in a direction
    :return:
    """
    g.write("; --- starting to clean the nozzle ---")
    g.dwell(10)
    output = "G1 F1000 E5; extrude 5 mm of material"
    g.write(output)
    g.dwell(5)