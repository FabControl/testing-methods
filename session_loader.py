"""
FabControl Feedstock Testing Suite
Command Line Interface
Usage:
    CLI.py [-v] [-q]
    CLI.py <session-id> [-v] [-q]
    CLI.py new-test
    CLI.py --help
"""
from docopt import docopt

args = docopt(__doc__, version='MP Feedstock Testing Suite')
session_uid = args["<session-id>"]
