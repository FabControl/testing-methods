import json
import numpy as np
from CLI_helpers import separator
import paths
from pprint import pprint


# Load persistence
with open("persistence.json", mode='r') as file:
    persistence = json.load(file)

for dummy in persistence["session"]["previous_tests"]:
    if dummy["test_name"] == "printing speed": # TODO check conditions
        persistence["settings"]["speed_printing"] = dummy["selected_value"]
    elif dummy["test_name"] == "path height":
        persistence["settings"]["path_height"] = dummy["selected_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "first layer height":
        persistence["settings"]["path_height_raft"] = dummy["selected_value"]
        persistence["settings"]["speed_printing_raft"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "path width":
        persistence["settings"]["path_width"] = dummy["selected_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "extrusion temperature":
        persistence["settings"]["temperature_extruder"] = dummy["selected_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "extrusion multiplier":
        persistence["settings"]["extrusion_multiplier"] = dummy["selected_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]
    elif dummy["test_name"] == "retraction distance":
        persistence["settings"]["retraction_distance"] = dummy["selected_value"]
        persistence["settings"]["speed_printing"] = dummy["selected_speed_value"]

persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*persistence["settings"]["path_height"]/persistence["settings"]["path_width"])),0)

with open(paths.cwd + separator("jsons") + persistence["material"]["manufacturer"] + " " + persistence["material"]["name"] + " " + str(persistence["machine"]["nozzle"]["size_id"]) + " mm" + ".json", mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)

with open(paths.cwd + separator() + "persistence.json", mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)
