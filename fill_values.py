"""
Populates persistence.json file with the selected values from a test. To be used in conjunction with an external
interface after each test.

Usage:
    fill_values.py <session-id>
"""

import json
import numpy as np
from CLI_helpers import separator
import paths
from docopt import docopt


args = docopt(__doc__)
session_id = args["<session-id>"]
path = paths.json_folder + separator() + session_id + ".json"

# Load persistence
with open(path, mode='r') as file:
    persistence = json.load(file)

dummy = persistence["session"]["previous_tests"][-1]

if dummy["test_name"] == "track height vs printing speed":
    if dummy["executed"]:
        persistence["settings"]["track_height"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
elif dummy["test_name"] == "first-layer track height vs first-layer printing speed":
    print("hello")
    if dummy["executed"]:
        persistence["settings"]["track_height_raft"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing_raft"] = dummy["selected_parameter_two_value"]
elif dummy["test_name"] == "track width":
    if dummy["executed"]:
        persistence["settings"]["track_width"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
elif dummy["test_name"] == "extrusion temperature vs printing speed":
    if dummy["executed"]:
        persistence["settings"]["temperature_extruder"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
elif dummy["test_name"] == "extrusion multiplier vs printing speed":
    if dummy["executed"]:
        persistence["settings"]["extrusion_multiplier"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_two_value"]
elif dummy["test_name"] == "bridging extrusion-multiplier":
    if dummy["executed"]:
        persistence["settings"]["bridging_extrusion_multiplier"] = dummy["selected_parameter_one_value"]
        persistence["settings"]["bridging_speed_printing"] = dummy["selected_parameter_two_value"]

index_one = dummy["tested_parameter_one_values"].index(dummy["selected_parameter_one_value"])
index_two = dummy["tested_parameter_two_values"].index(dummy["selected_parameter_two_value"])
persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][index_two][index_one]

if (dummy["test_name"] == "printing speed") or (dummy["test_name"] == "first-layer track width") or (dummy["test_name"] == "retraction distance"):
    if dummy["executed"]:
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_one_value"]
        index_one = dummy["tested_parameter_one_values"].index(dummy["selected_parameter_one_value"])
        persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"] = persistence["session"]["previous_tests"][-1]["tested_volumetric_flow-rate_values"][0][index_one]


persistence["session"]["previous_tests"][-1]["estimated_printing_time_s"] = round(persistence["session"]["previous_tests"][-1]["extruded_filament_mm"]*np.pi*(persistence["material"]["size_od"]/2)**2/persistence["session"]["previous_tests"][-1]["selected_volumetric_flow-rate_value"],1)
persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*persistence["settings"]["track_height"]/persistence["settings"]["track_width"])),0)

with open(path, mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)
