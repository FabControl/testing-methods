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
        "manufacturer": "Ultimaker",
        "buildarea_maxdim1": 223,
        "buildarea_maxdim2": 223,
        "max_dimension_z": 205,
        "form": "cartesian",
        "temperature_controllers": {
            "extruder": {
                "gcode_command": "M109 S{0} {1}",
                "temperature_max": 300,
                "temperature_min": 30,
                "part_cooling": False,
                "part_cooling_gcode_command": "M106 S{0}",
                "nozzle": {
                    "type": "brass",
                    "size_id": 0.4,
                    "size_od": 5.0,
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
                "ventilator_exit": False,
                "ventilator_exit_tool": "P1",
                "ventilator_exit_gcode_command": "M106 {0} S{1}",
                "ventilator_entry": False,
                "ventilator_entry_tool": "P2",
                "ventilator_entry_gcode_command": "M106 {0} S{1}"
            },
            "printbed": {
                "tool": "T1",
                "gcode_command": "M190 S{0} {1}",
                "temperature_min": 20,
                "temperature_max": 100,
                "printbed_heatable": True,
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
        "id": "79",
        "drying": {
            "dried": False,
            "drying_time": 0,
            "feeding_airflow": 0,
            "drying_airflow": 0,
            "feeding_temperature": 0,
            "drying_temperature": 0
        },
        "size_od": 2.85,
        "material_group": "non_filled",
        "density_rt": 1.13,
        "mvr": 2.3,
        "load_mfr": 2.16,
        "temperature_mfr": 200,
        "temperature_glass": 255,
        "name": "Novamid ID1030",
        "manufacturer": "DSM"
    },
    "session": {
        "uid": 129,
        "target": "mechanical_strength",
        "test_name": "08",
        "min_max_parameter_one": None,
        "min_max_parameter_two": [
            0,
            6
        ],
        "min_max_parameter_three": [
            35,
            80
        ],
        "test_type": "A",
        "user_id": "Daniel Tomas",
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
        "speed_printing_raft": 30.0,
        "track_height": 0.2,
        "track_height_raft": 0.25,
        "track_width": 0.4,
        "track_width_raft": 0.4,
        "extrusion_multiplier": 1.1,
        "temperature_extruder": 257,
        "temperature_extruder_raft": 255,
        "retraction_restart_distance": 0,
        "retraction_speed": 50,
        "bridging_extrusion_multiplier": 1,
        "bridging_part_cooling": 100,
        "bridging_speed_printing": 40,
        "speed_printing": 50,
        "optimize_speed_printing": True,
        "retraction_distance": 6.0,
        "coasting_distance": 0,
        "critical_overhang_angle": 45.0,
        "temperature_printbed_setpoint": 55,
        "temperature_chamber_setpoint": None,
        "part_cooling_setpoint": None
    }
}

#session_idn = str(persistence["session"]["uid"])
test_info = get_test_info(persistence)
comment = get_comment(test_info)

material = Material(**persistence["material"])
material.drying = DryingProcess(**persistence["material"]["drying"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(nozzle=machine.temperaturecontrollers.extruder.nozzle, material=material, machine=machine, **persistence["settings"])


