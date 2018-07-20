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
path = paths.cwd + paths.json_folder + separator() + session_id + ".json"

# Load persistence
with open(path, mode='r') as file:
    persistence = json.load(file)

for dummy in persistence["session"]["previous_tests"]:
    if dummy["test_name"] == "printing speed":
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_value"]
    elif dummy["test_name"] == "track height":
        persistence["settings"]["track_height"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "first-layer track height":
        persistence["settings"]["track_height_raft"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing_raft"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "first-layer track width":
        persistence["settings"]["track_width_raft"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing_raft"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "track width":
        persistence["settings"]["track_width"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "extrusion temperature":
        persistence["settings"]["temperature_extruder"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "extrusion multiplier":
        persistence["settings"]["extrusion_multiplier"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "retraction distance":
        persistence["settings"]["retraction_distance"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
    elif dummy["test_name"] == "bridging extrusion-multiplier":
        persistence["settings"]["bridging_extrusion_multiplier"] = dummy["selected_parameter_value"]
        persistence["settings"]["bridging_speed_printing"] = dummy["selected_printing-speed_value"]

persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*persistence["settings"]["track_height"]/persistence["settings"]["track_width"])),0)

with open(path, mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)
