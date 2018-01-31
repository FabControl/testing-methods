import Definitions
from TestSetupB import TestSetupB
import slicing_functionality as sf
from Definitions import *
from Globals import machine, material
from oop_functionality import Prism
origin_matrix = []

def dimensional_test(ts: TestSetupB):
    g = ts.g
    g.feed(5)

    number_of_test_structures = ts.number_of_test_structures
    matrix_vertical_size = 1

    safe_distance = 50
    circumradius = 7
    edges = 6
    layers = 1

    speed_printing = ts.argument_row

    if ts.test_name == 'perimeter':
        perimeter = ts.argument_column
        overlap = ts.overlap
        coef_h = ts.coef_h
    elif ts.test_name == 'overlap':
        perimeter = ts.perimeter
        overlap = ts.argument_column
        coef_h = ts.coef_h
    elif ts.test_name == 'path height':
        perimeter = ts.perimeter
        overlap = ts.overlap
        coef_h = ts.argument_column

    g.write(ts.comment1)

    for row in range(0, number_of_test_structures):
        g.set_extruder_temperature(ts.temperature_extruder[row])
        g.feed(speed_printing[row])

        for column in range(0, number_of_test_structures):
            for stratum in range (0, matrix_vertical_size):
                strata_size = int(layers / matrix_vertical_size)

                output = str("; --- Start to print regular %s-polygon with path height of %s mm and path width of %s mm ---" %
                             (edges, round(machine.nozzle.size_id * ts.coef_h[column], 3), round(machine.nozzle.size_id * ts.coef_w[column], 3)))
                g.write(output)

                prism = Prism(edges,
                              (column - (number_of_test_structures - 1)/2) * (safe_distance) - circumradius * math.cos(np.pi * (edges - 2) / (2 * edges)),
                              (row    - (number_of_test_structures - 1)/2) * (safe_distance) - circumradius * math.sin(np.pi * (edges - 2) / (2 * edges)),
                              stratum * strata_size * ts.coef_h[column] * machine.nozzle.size_id,
                              circumradius=circumradius,
                              layers=strata_size,
                              coef_h=coef_h[column],
                              coef_w=ts.coef_w[column],
                              perimeters=perimeter[column],
                              outline_overlap=overlap[column],
                              cooling=100,
                              extrusion_multiplier=1,
                              raft=True,
                              g=g)
                origin_matrix.append(prism.origin) if prism.origin[2] == 0 else None

    g.write("; --- finish to print the test structure ---")
    g.teardown()
    return