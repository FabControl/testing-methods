from Definitions import Material, Settings, Machine, TestInfo, minmax_path_width_height_raft
import json

try:
    print("Attempting to load the JSON")
    with open("persistence.json", mode="r") as file:
        import_json_dict = json.load(file)
    print("Loaded a testing session ID {:d} from outer scope".format(import_json_dict["session"]["uid"]))
except:
    print("falling back to hardcoded JSON")
    import_json_dict = {
        "material": {
            "name": "Arnitel ID2045",
            "manufacturer": "Nexeo Solutions",
            "id": "123456",
            "size_od": 1.75,
            "temperature_melting": 200,
            "temperature_destr": 300,
            "temperature_vicat": 144,
            "temperature_glass": -30
        },
        "machine": {
            "manufacturer": "Mass Portal",
            "model": "Pharaoh D20",
            "buildarea_maxdim1": 145,
            "buildarea_maxdim2": 145,
            "max_dimension_z": 200,
            "temperature_max": 300,
            "size_extruder_id": 1.95,
            "nozzle": {
                "size_id": 0.60,
                "size_od": 0.84,
                "size_capillary_length": 5,
                "size_angle": 60,
                "metal": "steel"
            }
        },
        "settings": {
            "aim": "aesthetics",
            "temperature_printbed_raft": 40,
            "temperature_printbed": 40,
            "part_cooling": 100,
            "raft_density": 90,
            "temperature_extruder_raft": 250,
            "path_height_raft": 0.3,
            "speed_printing_raft": 10,
            "temperature_extruder": 250,
            "speed_printing": 30,
            "path_height": 0.3,
            "path_width": 0.6,
            "extrusion_multiplier": 1.0,
            "retraction_distance": 2.0,
            "retraction_restart_distance": 0,
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
            "uid": 123456,
            "previous_tests": [],
            "test_type": 'A',
            "test_name": 'first layer height',
            "min_max": [0.1, 0.3],
            "min_max_speed": [10, 25],
            "slicer": "Prusa Slic3r"

        }
    }

# test_list = [TestInfo('first layer height', 'path_height_raft', 'mm'),  # 0
#              TestInfo('extrusion temperature', 'temperature_extruder', 'degC'),  # 1
#              TestInfo('path height', 'path_height', 'mm'),  # 2
#              TestInfo('path width', 'path_width', 'mm'),  # 3
#              TestInfo('printing speed', 'speed_printing', 'mm/s'),  # 4
#              TestInfo('extrusion multiplier', 'extrusion_multiplier', ''),  # 5
#              TestInfo('retraction distance', 'retraction_distance', 'mm')]  # 6

test_list = ['first layer height', #0
             'extrusion temperature', #1
             'path height', #2
             'path width', #3
             'extrusion multiplier', #4
             'printing speed', #5
             'retraction distance'] #6

material = Material(**import_json_dict["material"])
machine = Machine(**import_json_dict["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **import_json_dict["settings"])
coef_h_raft, coef_h_min_raft, coef_h_max_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine)