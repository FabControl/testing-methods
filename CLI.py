"""
FabControl 3D Printing Testing Framework
Command Line Interface
Usage:
    CLI.py [-v] [-q]
    CLI.py <session-id> [-v] [-q]
    CLI.py --help
"""

import time

from docopt import docopt

from Globals import machine, material, persistence # TODO Why machine is inactive?
from TestStructureGeometriesA import *
from generate_label import generate_label
from update_persistence import update_persistence
from initialize_test import initialize_test

quiet = True
verbose = False

if __name__ == '__main__':
    arguments = docopt(__doc__, version='FabControl Feedstock Testing Suite, v2.0')

    verbose = arguments["-v"]
    quiet = arguments["-q"]
    session_id = str(arguments["<session-id>"])

start = time.time()

if quiet:
    values = initialize_test(machine, material, persistence)

    from gcoder import *
    from paths import *

    gcode_path = str(gcode_folder + separator() + session_id + "_" + values.test_number + ".gcode")
    update_persistence(persistence, values, GCode(open(gcode_path, "rU")))

import os
os.system("python generate_suggested_values.py "+session_id)
os.system("python generate_report.py "+session_id)

generate_label(persistence)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')