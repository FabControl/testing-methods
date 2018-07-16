"""
Returns suggested testing parameters, based on session specific Globals.

Usage:
    generate_suggested_values.py <session-id>
"""
from Definitions import *
from Globals import persistence, test_info
from docopt import docopt

arguments = docopt(__doc__)


def border_values(_list: list):
    return [_list[0], _list[-1]]


material = Material(**persistence["material"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(**persistence["settings"])

suggested_values = {"temperature": border_values(minmax_temperature(material, machine, 7)),
                    "track_height": border_values(minmax_track_height(machine, 7)),
                    "track_width": border_values(list(minmax_track_width(machine, 7)[0])),
                    "track_width_raft": border_values(minmax_track_width_height_raft(machine, 7)[2]),
                    "track_height_raft": border_values(minmax_track_width_height_raft(machine, 7)[3]),
                    "test_name": test_info.name}

for key, value in suggested_values.items():
    print("{}: ".format(key) + str([test_info.precision.format(x) for x in value]))
