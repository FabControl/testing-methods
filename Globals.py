from Definitions import Material, Settings, Machine, TestInfo, header, footer, minmax_path_width_height_raft
from GcodeStuff import Gplus
import json

try:
    print("Attempting to load the JSON")
    with open("persistence.json", mode="r") as file:
        import_json_dict = json.load(file)
    print("Loaded a testing session ID %d from outer scope" % import_json_dict["session"]["uid"])
except:
    print("falling back to hardcoded JSON")
    import_json_dict = {
        "material": {
            "name": "Arnitel 2045",
            "manufacturer": "DSM",
            "id": "123456",
            "size_od": 1.75,
            "temperature_melting": 200,
            "temperature_destr": 300,
            "temperature_vicat": 20
        },
        "machine": {
            "manufacturer": "Mass Portal",
            "model": "Pharaoh XD20",
            "buildarea_maxdim1": 145,
            "buildarea_maxdim2": 145,
            "max_dimension_z": 200,
            "temperature_max": 300,
            "size_extruder_id": 1.95,
            "nozzle": {
                "size_id": 0.40,
                "size_od": 0.64,
                "size_capillary_length": 5,
                "size_angle": 60,
                "metal": "brass"
            }
        },
        "settings": {
            "temperature_printbed_raft": 25,
            "temperature_printbed": 25,
            "part_cooling": 100,

            "raft_density": 75,

            "temperature_extruder_raft": 235,

            "path_height_raft": 0.2,
            "path_width_raft": 0.4,
            "speed_printing_raft": 20,

            "temperature_extruder": 235,
            "speed_printing": 20,

            "path_height": 0.15,
            "path_width": 0.4,

            "extrusion_multiplier": 1.000,

            "retraction_distance": 2.00,
            "retraction_restart_distance": 0.0,
            "retraction_speed": 80,
            "coasting_distance": 0.0,
            "overlap": 0,
            "perimeter": 1,
            "matrix_size": 3,
            "layer_count": 15,
            "safe_distance": 50,
            "number_of_test_structures": 7,
            "edges": 30
        },
        "session": {
            "uid": 20180313,
            "previous_tests": [],
            "test_type": 'A',
            "test_name": 'first layer height',
            "min_max": [0.1, 0.3],
            "min_max_speed": [10, 25],
            "slicer": "simplify3d"

        }
    }

test_list = ['first layer height',  # 0
             'extrusion temperature',  # 1
             'path height',  # 2
             'path width',  # 3
             'printing speed',  # 4
             'extrusion multiplier',  # 5
             'retraction distance']  # 6


material = Material(**import_json_dict["material"])
machine = Machine(**import_json_dict["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **import_json_dict["settings"])
coef_h_raft, coef_h_min_raft, coef_h_max_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine)
