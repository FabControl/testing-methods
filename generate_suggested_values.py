"""
FabControl Optimizer: Feedstock Material Testing
Suggested Values Generator

Returns suggested values of the testing parameters, based on session specific GetTestInfo.py.

Usage:
   generate_suggested_values.py <session-id>
"""
from Definitions import *
from Globals import persistence
from GetTestInfo import get_test_info
from docopt import docopt

arguments = docopt(__doc__)

def border_values(_list: list):
   return [_list[0], _list[-1]]

machine = Machine(**persistence["machine"])
machine.settings = Settings(**persistence["settings"])

if len(persistence["session"]["previous_tests"]) > 0:
    speed = 2 * persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"]/machine.temperaturecontrollers.extruder.nozzle.size_id**2

if len(persistence["session"]["previous_tests"]) > 0:
    temperature = persistence["settings"]["temperature_extruder"]

test_info = get_test_info(persistence)

if persistence["session"]["test_name"] == "01":
    suggested_values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in border_values(get_minmax_track_height_raft_coef(machine, test_info.number_of_test_structures))]
elif persistence["session"]["test_name"] == "02":
    suggested_values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in border_values(get_minmax_track_width_raft_coef(machine, test_info.number_of_test_structures))]
elif persistence["session"]["test_name"] == "03":
    suggested_values = border_values(get_minmax_temperature(machine, 7))
elif persistence["session"]["test_name"] == "04":
    suggested_values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in border_values(get_minmax_track_height_coef(machine, test_info.number_of_test_structures))]
elif persistence["session"]["test_name"] == "05":
    suggested_values = [x * machine.temperaturecontrollers.extruder.nozzle.size_id for x in border_values(get_minmax_track_width_coef(machine, test_info.number_of_test_structures))]
elif persistence["session"]["test_name"] == "06":
    suggested_values = [0.75, 1.5]
elif persistence["session"]["test_name"] == "07":
    suggested_values = [0.75*speed, 1.25*speed] if speed is not None else None
elif persistence["session"]["test_name"] == "08":
    suggested_values = [temperature-5, temperature+5] if temperature is not None else None
elif persistence["session"]["test_name"] == "09":
    suggested_values = test_info.parameter_one.default_value
elif persistence["session"]["test_name"] == "10":
    suggested_values = test_info.parameter_one.default_value
elif persistence["session"]["test_name"] == "13":
    suggested_values = [1.25, 2.0]

print(suggested_values)
