"""
Returns suggested testing parameters, based on session specific Globals.

Usage:
   generate_suggested_values.py <session-id>
"""
from Definitions import *
from Globals import persistence, test_info, test_dict
from docopt import docopt

arguments = docopt(__doc__)


def border_values(_list: list):
   return [_list[0], _list[-1]]

material = Material(**persistence["material"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(**persistence["settings"])

if len(persistence["session"]["previous_tests"]) > 0:
    speed = 2 * persistence["session"]["previous_tests"][0]["selected_volumetric_flow-rate_value"]/machine.nozzle.size_id**2
else:
    speed = None

suggested_values = {"temperature": border_values(minmax_temperature(material, machine, 7)),
                   "track_height": [x * machine.nozzle.size_id for x in border_values(minmax_track_height(machine, 7))],
                   "track_width": [x * machine.nozzle.size_id for x in border_values(list(minmax_track_width(machine, 7)[0]))],
                   "track_width_raft": border_values(minmax_track_width_height_raft(machine, 7)[3]),
                   "track_height_raft": [x * machine.nozzle.size_id for x in border_values(minmax_track_width_height_raft(machine, 7)[2])],
                   "speed_printing": [0.75*speed, 1.5*speed] if speed is not None else None,
                   "extrusion_multiplier": border_values([test_dict["06"].min_default, test_dict["06"].max_default]),
                   "retraction_distance": border_values([test_dict["08"].min_default, test_dict["08"].max_default]),
                   "test_name": test_info.name}

for key, value in suggested_values.items():
   if type(value) == list:
       print("{}: ".format(key) + str([x for x in value]))
   else:
       print("{}: {}".format(key, value))