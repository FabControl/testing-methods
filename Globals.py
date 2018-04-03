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
            "name": "Nanodiamond PLA B",
            "manufacturer": "Carbodeon",
            "id": "123456",
            "size_od": 1.75,
            "temperature_melting": 175,
            "temperature_destr": 250,
            "temperature_vicat": 60,
            "temperature_glass": 70
        },
        "machine": {
            "manufacturer": "Mass Portal",
            "model": "Pharaoh D20",
            "sn": 0,
            "buildarea_maxdim1": 145,
            "buildarea_maxdim2": 145,
            "max_dimension_z": 200,
            "temperature_extruder_max": 300,
            "size_extruder_id": 1.95,
            "nozzle": {
                "size_id": 0.80,
                "size_od": 1.04,
                "size_capillary_length": 5,
                "size_angle": 60,
                "metal": "steel"
            },
            "ventilators": {
                "ventilator_part_cooling": True,
                "ventilator_entry": False,
                "ventilator_exit": False
            },
            "software": {
                "version": "2.1",
            },
            "firmware": {
                "fw_type": "Repetier",
                "version": "2.0",
            }
        },
        "settings": {
            "aim": "strength",
            "temperature_printbed_raft": 40,
            "temperature_printbed": 40,
            "ventilator_part_cooling": 100,
            "ventilator_entry": 0,
            "ventilator_exit": 0,
            "raft_density": 90,
            "temperature_extruder_raft": 230,
            "path_height_raft": 0.3,
            "speed_printing_raft": 10,
            "temperature_extruder": 230,
            "speed_printing": 30,
            "path_height": 0.4,
            "path_width": 0.8,
            "extrusion_multiplier": 1.0,
            "retraction_distance": 2.0,
            "retraction_restart_distance": 0,
            "retraction_speed": 120,
            "coasting_distance": 0.0,
            "overlap": 0,
            "perimeter": 1,
            "matrix_size": 3,
            "layer_count": 15,
            "safe_distance": 50,
            "number_of_test_structures": 7,
            "number_of_substructures": 4,
            "edges": 30
    },
        "session": {
            "uid": 123456,
            "previous_tests": [],
            "test_type": 'A',
            "test_name": 'first layer height',
            "min_max": [0.1, 0.3],
            "min_max_speed": [10, 30],
            "slicer": "Prusa Slic3r"

        }
    }

test_dict = {'1': TestInfo('first layer height', 'path_height_raft', 'mm', '{:.3f}'),
             '2': TestInfo('extrusion temperature', 'temperature_extruder', 'degC', '{:.0f}'),
             '3': TestInfo('path height', 'path_height', 'mm', '{:.3f}'),
             '4': TestInfo('path width', 'path_width', 'mm', '{:.3f}'),
             '5': TestInfo('extrusion multiplier', 'extrusion_multiplier', '-', '{:.3f}', [0.75, 1.50]),
             '6': TestInfo('printing speed', 'speed_printing', 'mm/s', '{:.1f}', [0.80, 1.75]),
             '7': TestInfo('retraction distance', 'retraction_distance', 'mm', '{:.3f}', [0., 4]),
             '8': TestInfo('retraction restart distance', 'retraction_restart_distance', 'mm', '{:.3f}', [0., 0.4])}

test_name_list, test_precision_list, test_units_list = [], [], []
test_number_list = test_dict.keys()

for test_number in test_number_list:
    test = test_dict[test_number]
    test_name_list.append(test.name)
    test_precision_list.append(test.precision)
    test_units_list.append(test.units)

material = Material(**import_json_dict["material"])
machine = Machine(**import_json_dict["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **import_json_dict["settings"])
coef_h_raft, coef_h_min_raft, coef_h_max_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine)