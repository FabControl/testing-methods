from Definitions import Material, Settings, Machine, TestInfo, minmax_path_width_height_raft
import json

try:
    print("Attempting to load the JSON")
    with open("persistence.json", mode="r") as file:
        import_json_dict = json.load(file)
    print("Loaded a testing session ID {} from outer scope".format(import_json_dict["session"]["uid"]))
except:
    print("falling back to hardcoded JSON")
    import_json_dict = {
    "material": {
        "name": "Arnitel ID2045",
        "manufacturer": "Nexeo Solutions",
        "id": "123456",
        "size_od": 1.75,
        "temperature_melting": 158,
        "temperature_destr": 300,
        "temperature_vicat": 90,
        "temperature_glass": -35,
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
            "size_id": 0.6,
            "size_od": 0.84,
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
             "version": "2.1"
        },
        "firmware": {
            "fw_type": "Repetier",
            "version": "2.0"
        }
    },
    "settings": {
        "aim": "aesthetics",
        "temperature_printbed_raft": 50,
        "temperature_printbed": 50,
        "ventilator_part_cooling": 100,
        "ventilator_entry": 0,
        "ventilator_exit": 0,
        "raft_density": 90,
        "temperature_extruder_raft": 250,
        "path_height_raft": 0.3,
        "speed_printing_raft": 15,
        "temperature_extruder": 275,
        "speed_printing": 52.5,
        "path_height": 0.2,
        "path_width": 0.6,
        "extrusion_multiplier": 1,
        "retraction_distance": 5,
        "retraction_restart_distance": 0.0,
        "retraction_speed": 120,
        "coasting_distance": 0.0,
        "overlap": 0,
        "perimeter": 1,
        "matrix_size": 3,
        "layer_count": 15,
        "safe_distance": 50,
        "edges": 30,
        "path_width_raft": 0.72,
        "critical_overhang_angle": 36.0
    },
        "session": {
            "uid": 123456,
            "previous_tests": [],
            "test_type": 'A',
            "test_name": 'first layer height',
            "min_max": [0.1, 0.3],
            "min_max_speed": [10, 30],
            "number_of_test_structures": 7,
            "slicer": "Prusa Slic3r"
        }
    }
# TODO Add to json for report generation
# TODO Create a similar dict for B tests
test_dict = {'1': TestInfo('first layer height', 'path_height_raft', 'mm', '{:.3f}',
                           number_of_layers = 1, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = 4),
             '2': TestInfo('extrusion temperature', 'temperature_extruder', 'degC', '{:.0f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = 4),
             '3': TestInfo('path height', 'path_height', 'mm', '{:.3f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = 4),
             '4': TestInfo('path width', 'path_width', 'mm', '{:.3f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = 4),
             '5': TestInfo('extrusion multiplier', 'extrusion_multiplier', '-', '{:.3f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = 4, default_value = [0.75, 1.50]),
             '6': TestInfo('printing speed', 'speed_printing', 'mm/s', '{:.1f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = 1, default_value = [0.80, 1.75]),
             '7': TestInfo('retraction distance', 'retraction_distance', 'mm', '{:.3f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = None, default_value = [0., 4]),
             '8': TestInfo('retraction restart distance', 'retraction_restart_distance', 'mm', '{:.3f}',
                           number_of_layers = 2, number_of_test_structures = import_json_dict["session"]["number_of_test_structures"], number_of_substructures = None, default_value = [0., 0.4])}

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
#coef_h_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine) TODO was it needed for B tests?