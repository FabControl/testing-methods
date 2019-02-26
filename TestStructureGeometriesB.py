from GettingValuesB import TestSetupB
import slicing_functionality as sf
from Definitions import *
from TestsStructureGeometriesA import wipe
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
    edges = 50
    layers = 15

    speed_printing = ts.argument_row

    wipe(ts, full=False)  # Shortened form of wipe, so that it does not interfere with a test struture

    if ts.test_name == 'perimeter':
        perimeter = ts.argument_column
        overlap = ts.overlap
        coef_h = ts.coef_h
        temperature_extruder = ts.temperature_extruder
    elif ts.test_name == 'overlap':
        perimeter = ts.perimeter
        overlap = ts.argument_column
        coef_h = ts.coef_h
        temperature_extruder = ts.temperature_extruder
    elif ts.test_name == 'path height':
        perimeter = ts.perimeter
        overlap = ts.overlap
        coef_h = ts.argument_column
        temperature_extruder = ts.temperature_extruder
    elif ts.test_name == 'temperature':
        perimeter = ts.perimeter
        overlap = ts.overlap
        coef_h = ts.coef_h
        temperature_extruder = ts.argument_column

    g.write(ts.comment1)

    for row in range(0, number_of_test_structures):

        for column in range(0, number_of_test_structures):
            for stratum in range(0, matrix_vertical_size):

                g.feed(speed_printing[column])

                strata_size = layers

                output = str("; --- Start to print regular %s-polygon with path height of %s mm and path width of %s mm ---" %
                             (edges, round(machine.nozzle.size_id * ts.coef_h[column], 3), round(machine.nozzle.size_id * ts.coef_w[column], 3)))
                g.write(output)

                prism = Prism(edges,
                              (column - (number_of_test_structures - 1)/2) * (safe_distance) - circumradius * math.cos(np.pi * (edges - 2) / (2 * edges)),
                              (row    - (number_of_test_structures - 1)/2) * (safe_distance) - circumradius * math.sin(np.pi * (edges - 2) / (2 * edges)),
                              stratum * strata_size * ts.coef_h[column] * machine.nozzle.size_id,
                              circumradius=circumradius,
                              extrusion_temperature=temperature_extruder[row],
                              layers=strata_size,
                              coef_h=coef_h[column],
                              coef_w=ts.coef_w[column],
                              coef_h_raft=ts.coef_h_raft,
                              coef_w_raft=ts.coef_w_raft,
                              perimeters=perimeter[column],
                              outline_overlap=overlap[column],
                              coasting_distance=0,
                              cooling=100,
                              extrusion_multiplier=1,
                              raft=ts.raft,
                              speed_printing = speed_printing[column],
                              g=g)
                origin_matrix.append(prism.origin) if prism.origin[2] == 0 else None

    g.write("; --- finish to print the test structure ---")
    g.teardown()
    return