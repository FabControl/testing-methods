"""
Populates persistence.json file with the selected values from a test. To be used in conjunction with an external
interface after each test. Arguments are one or two indices (for one or two parameters) and a value for the third parameter.

Usage:
    fill_values.py <session-id> <ind_one> [<ind_two>...]
"""

from docopt import docopt
import sys
import json
import numpy as np
from CLI_helpers import separator
import paths

args = docopt(__doc__)

session_id = str(sys.argv[1])

path = paths.json_folder + separator() + session_id + ".json"

# Load persistence
with open(path, mode='r') as file:
    persistence = json.load(file)

dummy = persistence["session"]["previous_tests"][-1]
ind_parameter_one = int(sys.argv[2])
dummy["selected_parameter_one_value"] = dummy["tested_parameter_one_values"][ind_parameter_one]

if len(sys.argv) > 3:
    ind_parameter_two = int(sys.argv[3])
    dummy["selected_parameter_two_value"] = dummy["tested_parameter_two_values"][ind_parameter_two]
    if len(sys.argv) > 4:
        value_parameter_three = int(sys.argv[4])
        dummy["selected_parameter_three_value"] = value_parameter_three


if dummy["test_number"] == "01":
    if dummy["executed"]:
        persistence["settings"]["track_height_raft"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing_raft"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_two][ind_parameter_one]
elif dummy["test_number"] == "02":
    if dummy["executed"]:
        persistence["settings"]["track_width_raft"] = dummy["selected_parameter_one_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_one]
elif dummy["test_number"] == "03":
    if dummy["executed"]:
        persistence["settings"]["temperature_extruder"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_two][ind_parameter_one]
elif dummy["test_number"] == "04":
    if dummy["executed"]:
        persistence["settings"]["track_height"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_two][ind_parameter_one]
elif dummy["test_number"] == "05":
    if dummy["executed"]:
        persistence["settings"]["track_width"] = dummy["selected_parameter_one_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_one]
elif dummy["test_number"] == "06":
    if dummy["executed"]:
        persistence["settings"]["extrusion_multiplier"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_two][ind_parameter_one]
elif dummy["test_number"] == "07":
    if dummy["executed"]:
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_one_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_one]
elif dummy["test_number"] == "08":
    if dummy["executed"]:
        persistence["settings"]["temperature_extruder"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["retraction_distance"] = dummy["selected_parameter_two_value"]
        persistence["settings"]["retraction_speed"] = dummy["selected_parameter_three_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][0]
elif dummy["test_number"] == "09":
    if dummy["executed"]:
        persistence["settings"]["retraction_distance"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_two][ind_parameter_one]
elif dummy["test_number"] == "10":
    if dummy["executed"]:
        persistence["settings"]["retraction_distance"] = dummy["selected_parameter_one_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][0]
elif dummy["test_number"] == "11":
    if dummy["executed"]:
        persistence["settings"]["retraction_distance"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["retraction_speed"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][0]
elif dummy["test_number"] == "13":
    if dummy["executed"]:
        persistence["settings"]["bridging_extrusion_multiplier"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["bridging_speed_printing"] = dummy["selected_parameter_two_value"]
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][ind_parameter_two][ind_parameter_one]

persistence["session"]["previous_tests"][-1]["estimated_printing_time_s"] = round(persistence["session"]["previous_tests"][-1]["extruded_filament_mm"]*np.pi*(persistence["material"]["size_od"]/2)**2/persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"],1)
persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*persistence["settings"]["track_height"]/persistence["settings"]["track_width"])),0)

with open(path, mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)