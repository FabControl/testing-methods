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
        "sn": 12345,
        "model": "--",
        "manufacturer": "MP",
        "buildarea_maxdim1": 200,
        "buildarea_maxdim2": 200,
        "max_dimension_z": 215,
        "form": "elliptic",
        "temperature_controllers": {
            "extruder": {
                "tool": "",
                "gcode_command": "M109 S{0} {1}",
                "gcode_command_immediate": "M104 S{0} {1}",
                "temperature_max": 300,
                "temperature_min": 30,
                "part_cooling": True,
                "part_cooling_gcode_command": "M106 S{0}",
                "nozzle": {
                    "type": "brass",
                    "size_id": 0.8,
                    "size_od": 1.04,
                    "size_capillary_length": 5,
                    "size_angle": 60,
                    "size_extruder_id": 1.95
                }
            },
            "chamber": {
                "tool": "",
                "gcode_command": "M141 S{0}",
                "temperature_min": 30,
                "temperature_max": 80,
                "chamber_heatable": False,
                "temperature_chamber_setpoint": 80,
                "ventilator_exit": False,
                "ventilator_exit_tool": "P1",
                "ventilator_exit_gcode_command": "M106 {0} S{1}",
                "ventilator_entry": False,
                "ventilator_entry_tool": "P2",
                "ventilator_entry_gcode_command": "M106 {0} S{1}"
            },
            "printbed": {
                "tool": "",
                "gcode_command": "M190 S{0}",
                "gcode_command_immediate": "M140 S{0}",
                "temperature_min": 20,
                "temperature_max": 115,
                "printbed_heatable": True,
                "temperature_printbed_setpoint": 30,
                "material": "?",
                "coating": "None"
            }
        },
        "software": {
            "version": "version"
        },
        "firmware": {
            "version": "2.0",
            "fw_type": "fw_type"
        }
    },
    "material": {
        "id": "80",
        "drying": {
            "dried": False,
            "drying_time": 0,
            "feeding_airflow": 0,
            "drying_airflow": 0,
            "feeding_temperature": 0,
            "drying_temperature": 0
        },
        "size_od": 1.75,
        "material_group": "non-filled",
        "density_rt": 1.13,
        "mvr": 2.3,
        "load_mfr": 2.16,
        "temperature_mfr": 200,
        "temperature_glass": 255,
        "name": "PA6 with Exolit",
        "manufacturer": "Clariant"
    },
    "session": {
        "uid": 210,
        "target": "mechanical_strength",
        "test_number": "11",
        "min_max_parameter_one": [
            0,
            5
        ],
        "min_max_parameter_two": [
            100,
            120
        ],
        "min_max_parameter_three": [],
        "test_type": "A",
        "user_id": "Georgijs Bakradze",
        "offset": [
            0,
            0
        ],
        "slicer": "prusa slic3r",
        "previous_tests": [],
        "number_of_test_structures": 7
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
        "temperature_chamber_setpoint": 0,
        "part_cooling_setpoint": 0
    }
}

#session_idn = str(persistence["session"]["uid"])
test_info = get_test_info(persistence)
comment = get_comment(test_info)

material = Material(**persistence["material"])
material.drying = DryingProcess(**persistence["material"]["drying"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(nozzle=machine.temperaturecontrollers.extruder.nozzle, material=material, machine=machine, **persistence["settings"])


