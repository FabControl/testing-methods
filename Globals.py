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
        "name": "Novamid ID1030",
        "manufacturer": "Nexeo Solutions",
        "id": "123456",
        "size_od": 1.75,
        "temperature_melting": 200,
        "temperature_destr": 320,
        "temperature_vicat": 90, # optional
        "temperature_glass": -35, # optional
        "mvr": 10, # optional
        "load_mfr": 1, # optional
        "temperature_mfr": 220, # optional
        "capillary_diameter_mfr": 4, # optional
        "capillary_length_mfr": 8, # optional
        "time_mfr": 10, # optional
        "density_rt": 1.13 # optional
    },
    "machine": {
        "manufacturer": "Mass Portal",
        "model": "Pharaoh D20",
        "sn": 0,
        "buildarea_maxdim1": 145,
        "buildarea_maxdim2": 145,
        "max_dimension_z": 200,
        "temperature_extruder_max": 320,
        "temperature_extruder_min": 190,
        "temperature_printbed_max": 115,
        "temperature_printbed_min": 40,
        "nozzle": {
            "size_id": 1.0,
            "size_od": 1.24,
            "size_capillary_length": 5, # optional
            "size_angle": 60, # optional
            "size_extruder_id": 1.95,
            "type": "steel"
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
        },
        "printbed": {
            "printbed_heatable": False,
            "temperature_printbed_max": 0,
            "temperature_printbed_min": 0
        }
    },
    "settings": {
        "aim": "aesthetics",
        "optimize_speed_printing": True, # optional
        "ventilator_part_cooling": 100,
        "ventilator_entry": 0,
        "ventilator_exit": 0,
        "raft_density": 100,
        "temperature_printbed": 80,
        "temperature_extruder_raft": 255,
        "path_height_raft": 0.4,
        "path_width_raft": 1.0,
        "speed_printing_raft": 20,
        "temperature_extruder": 245,
        "path_height": 0.4,
        "path_width": 1.0,
        "speed_printing": 50,
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
        "slicer": "Prusa Slic3r",
        "number_of_test_structures": 7
        }
    }
# TODO Add to json for report generation
# TODO Create a similar dict for B tests
test_dict = {'1': TestInfo('first layer height', 'first layer height', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=False),
             '2': TestInfo('first layer width', 'first layer width', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=False),
             '3': TestInfo('extrusion temperature', 'extrusion temperature', 'degC', '{:.0f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             '4': TestInfo('path height', 'path height', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             '5': TestInfo('path width', 'path width', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             '6': TestInfo('extrusion multiplier', 'extrusion multiplier', '-', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[0.80, 1.40]),
             '7': TestInfo('printing speed', 'printing speed', 'mm/s', '{:.1f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=1, raft=True, default_value=[0.80, 1.75]),
             '8': TestInfo('retraction distance', 'retraction distance', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=None, raft=True, default_value=[0., 4]),
             '9': TestInfo('retraction restart distance', 'retraction restart distance', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[0., 0.4]),
             '10': TestInfo('bridging', 'bridging extrusion multiplier', '-', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[1.0, 2.0])}

test_name_list, test_precision_list, test_units_list = [], [], []
test_number_list = test_dict.keys()

for test_number in test_number_list:
    test = test_dict[test_number]
    test_name_list.append(test.parameter)
    test_precision_list.append(test.precision)
    test_units_list.append(test.units)

material = Material(**import_json_dict["material"])
machine = Machine(**import_json_dict["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **import_json_dict["settings"])
#coef_h_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine) TODO was it needed for B tests?
