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
        "temperature_vicat": 90, # optional
        "temperature_glass": -35, # optional
        "mvr": 10, # optional
        "load_mfr": 1, # optional
        "temperature_mfr": 220, # optional
        "capillary_diameter_mfr": 4, # optional
        "capillary_length_mfr": 8, # optional
        "time_mfr": 10, # optional
        "density_rt": 1 # optional
    },
    "machine": {
        "manufacturer": "Mass Portal",
        "model": "Pharaoh D20",
        "sn": 0,
        "buildarea_maxdim1": 145,
        "buildarea_maxdim2": 145,
        "max_dimension_z": 200,
        "temperature_extruder_max": 300,
        "temperature_extruder_min": 190,
        "temperature_printbed_max": 115,
        "temperature_printbed_min": 40,
        "nozzle": {
            "size_id": 0.6,
            "size_od": 0.84,
            "size_capillary_length": 5,
            "size_angle": 60,
            "size_extruder_id": 1.95,
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
        "optimize_speed_printing": True, # optional
        "ventilator_part_cooling": 100,
        "ventilator_entry": 0,
        "ventilator_exit": 0,
        "raft_density": 90,
        "temperature_printbed": 50,
        "temperature_extruder_raft": 250,
        "path_height_raft": 0.3,
        "path_width_raft": 0.72,
        "speed_printing_raft": 15,
        "temperature_extruder": 275,
        "path_height": 0.2,
        "path_width": 0.6,
        "speed_printing": 52.5,
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
                           number_of_layers=1, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=False),
             '2': TestInfo('first layer width', 'path_width_raft', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=False),
             '3': TestInfo('extrusion temperature', 'temperature_extruder', 'degC', '{:.0f}',
                           number_of_layers=2, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=True),
             '4': TestInfo('path height', 'path_height', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=True),
             '5': TestInfo('path width', 'path_width', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=True),
             '6': TestInfo('extrusion multiplier', 'extrusion_multiplier', '-', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=True, default_value=[0.80, 1.40]),
             '7': TestInfo('printing speed', 'speed_printing', 'mm/s', '{:.1f}',
                           number_of_layers=2, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=1, raft=True, default_value=[0.80, 1.75]),
             '8': TestInfo('retraction distance', 'retraction_distance', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=None, raft=True, default_value=[0., 4]),
             '9': TestInfo('retraction restart distance', 'retraction_restart_distance', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=import_json_dict["session"]["number_of_test_structures"], number_of_substructures=4, raft=True, default_value=[0., 0.4])}

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
