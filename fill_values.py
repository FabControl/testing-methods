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
from pprint import pprint
from docopt import docopt


args = docopt(__doc__)
session_id = args["<session-id>"]

# Load persistence
with open("persistence_" + session_id + ".json", mode='r') as file:
    persistence = json.load(file)

for dummy in persistence["session"]["previous_tests"]:
    if dummy["test_name"] == "printing speed":
        persistence["settings"]["speed_printing"] = dummy["selected_parameter_value"]
    elif dummy["test_name"] == "path height":
        persistence["settings"]["track_height"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "first layer height":
        persistence["settings"]["track_height_raft"] = dummy["selected_parameter_value"]
        persistence["settings"]["track_width_raft"] = np.mean(ts.coef_w_raft) * persistence["machine"]["nozzle"]["size_id"] #TODO
        persistence["settings"]["speed_printing_raft"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "path width":
        persistence["settings"]["track_width"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "extrusion temperature":
        persistence["settings"]["temperature_extruder"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "extrusion multiplier":
        persistence["settings"]["extrusion_multiplier"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "retraction distance":
        persistence["settings"]["retraction_distance"] = dummy["selected_parameter_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]

persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*persistence["settings"]["track_height"]/persistence["settings"]["track_width"])),0)

# with open(paths.cwd + separator("jsons") + persistence["material"]["manufacturer"] + " " + persistence["material"]["name"] + " " + str(persistence["machine"]["nozzle"]["size_id"]) + " mm" + ".json", mode="w") as file:
#     output = json.dumps(persistence, indent=4, sort_keys=False)
#     file.write(output)

with open(paths.cwd + separator() + "persistence_" + session_id + ".json", mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)
