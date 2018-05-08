"""
Mass Portal Feedstock Testing Suite
Command Line Interface
Usage:
    CLI.py [-v] [-q]
    CLI.py <session-id> [-v] [-q]
    CLI.py new-test
    CLI.py generate-report
    CLI.py generate-configuration <slicer>
    CLI.py generate-gcode-iso <orientation> <count> <rotation> <config> <file>
    CLI.py --help
"""
from docopt import docopt

args = docopt(__doc__, version='MP Feedstock Testing Suite')
session_id = args["<session-id>"]
