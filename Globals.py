from Definitions import Material, Settings, Machine, TestInfo, DryingProcess, Parameter
import json
from session_loader import session_uid
from paths import json_folder
from CLI_helpers import separator, exception_handler
from get_test_info import get_test_info, get_comment


try:
    try:
        print("Attempting to load the persistence file with ID {}".format(session_uid))
        with open(str(json_folder + separator() + session_uid + ".json"), mode="r") as file:
            persistence = json.load(file)
        print("Loaded a testing session ID {} from the existing JSON file".format(persistence["session"]["uid"]))
        file.close()
    except:
        exception_handler("Session not found")
except:
    exception_handler("Falling back to hardcoded JSON")
    persistence = {
    "machine": {
        "model": "model name",
        "buildarea_maxdim1": 200,
        "buildarea_maxdim2": 200,
        "form": "elliptic",
        "temperature_controllers": {
            "extruder": {
                "tool": "",
                "gcode_command": "M109 S$temp $tool",
                "temperature_max": 350,
                "part_cooling": True,
                "nozzle": {
                    "size_id": 0.8
                }
            },
            "chamber": {
                "tool": "",
                "gcode_command": "M141 S$temp",
                "temperature_max": 80,
                "chamber_heatable": False
            },
            "printbed": {
                "tool": "",
                "gcode_command": "M190 S$temp",
                "gcode_command_immediate": "M140 S$temp",
                "printbed_heatable": true,
                "temperature_printbed_setpoint": 30
            }
        }
    },
    "material": {
        "drying": {
            "dried": true
        },
        "size_od": 1.75,
        "name": "material name"
    },
    "session": {
        "uid": 211,
        "target": "mechanical_strength",
        "test_number": "03",
        "min_max_parameter_one": [],
        "min_max_parameter_two": [
            40,
            100
        ],
        "min_max_parameter_three": [],
        "test_type": "A",
        "user_id": "user name",
        "offset": [
            0,
            0
        ],
        "slicer": "prusa slic3r",
        "previous_tests": []
    },
    "settings": {
        "speed_travel": 140,
        "raft_density": 100,
        "speed_printing_raft": 25,
        "track_height": 0.2,
        "track_height_raft": 0.2,
        "track_width": 0.3,
        "track_width_raft": 0.3,
        "extrusion_multiplier": 1.0,
        "temperature_extruder": 260,
        "temperature_extruder_raft": 260,
        "retraction_restart_distance": 0,
        "retraction_speed": 100,
        "retraction_distance": 2.6,
        "bridging_extrusion_multiplier": 1,
        "bridging_part_cooling": 100,
        "bridging_speed_printing": 40,
        "speed_printing": 80,
        "coasting_distance": 0,
        "critical_overhang_angle": 53.0,
        "temperature_printbed_setpoint": 90,
        "temperature_chamber_setpoint": 80,
        "part_cooling_setpoint": 0
    }
}

test_info = get_test_info(persistence)
comment = get_comment(test_info)

material = Material(**persistence["material"])
material.drying = DryingProcess(**persistence["material"]["drying"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(nozzle=machine.temperaturecontrollers.extruder.nozzle,
                            material=material,
                            machine=machine,
                            **persistence["settings"])
