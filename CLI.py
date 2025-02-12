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

from CheckCompatibility import check_compatibility
from Globals import machine, material, persistence  # TODO Why machine is inactive?
from TestStructureGeometriesA import *
from generate_label import generate_label
from update_persistence import update_persistence
from initialize_test import OptimizerSession

if __name__ == '__main__':

    arguments = docopt(__doc__, version='FabControl Feedstock Testing Suite')

    verbose = arguments["-v"]
    quiet = arguments["-q"]
    session_id = str(arguments["<session-id>"])

    start = time.time()

    # Check compatibility
    check_compatibility(machine, material)

    if quiet:
        values = OptimizerSession(persistence).values
        update_persistence(persistence, values)

    import os
    os.system("python3 generate_suggested_values.py "+session_id)
    os.system("python3 generate_report.py "+session_id)
    generate_label(persistence)

    end = time.time()
    time_elapsed = end - start
    print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')
