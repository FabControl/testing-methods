from Definitions import Material, Settings, Machine, TestInfo, minmax_track_width_height_raft
import json
from session_loader import session_id

try:
    try:
        print("Attempting to load the persistence file with ID {}".format(session_id))
        with open("persistence_" + session_id + ".json", mode="r") as file:
            persistence = json.load(file)
        print("Loaded a testing session ID {} from outer scope".format(persistence["session"]["uid"]))
        file.close()
    except:
        print("Attempting to load the persistence file without an ID".format(session_id))
        with open("persistence.json", mode="r") as file:
            persistence = json.load(file)
        print("Loaded a testing session ID {} from outer scope".format(persistence["session"]["uid"]))
        file.close()
except:
    print("falling back to hardcoded JSON")
    persistence = {
    "material": {
        "name": "PC Plus",
        "manufacturer": "Polymaker",
        "material_group": "unfilled polymer",
        "polymer_class": "polycarbonate",
        "id": "123456",
        "size_od": 1.75,
        "temperature_melting": 230,
        "temperature_destr": 320,
        "temperature_vicat": 130, # optional
        "temperature_glass": 112, # optional
        "mvr": 32, # optional
        "load_mfr": 1, # optional
        "temperature_mfr": 220, # optional
        "capillary_diameter_mfr": 4, # optional
        "capillary_length_mfr": 8, # optional
        "time_mfr": 10, # optional
        "density_rt": 1.2 # optional
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
        "nozzle": {
            "size_id": 0.6,
            "size_od": 0.84,
            "size_capillary_length": 5, # optional
            "size_angle": 60, # optional
            "size_extruder_id": 1.95,
            "type": "brass"
        },
        "ventilators": {
             "ventilator_part_cooling": True,
             "ventilator_entry": True,
             "ventilator_exit": True
            },
        "software": {
             "version": "2.1"
        },
        "firmware": {
            "fw_type": "Repetier",
            "version": "2.0"
        },
        "printbed": {
            "printbed_heatable": True,
            "temperature_printbed_max": 115,
            "temperature_printbed_min": 40
        }
    },
    "settings": {
        "aim": "aesthetics",
        "optimize_speed_printing": True, # optional
        "ventilator_part_cooling": 0,
        "ventilator_entry": 0,
        "ventilator_exit": 0,
        "raft_density": 100,
        "temperature_printbed": 115,
        "temperature_extruder_raft": 280,
        "track_height_raft": 0.3,
        "track_width_raft": 0.6,
        "speed_printing_raft": 10,
        "extrusion_multiplier_raft": 1.0,
        "temperature_extruder": 280,
        "track_height": 0.3,
        "track_width": 0.6,
        "speed_printing": 20,
        "extrusion_multiplier": 1,
        "retraction_distance": 4,
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
        "uid": 20180508,
        "previous_tests": [],
        "test_type": 'A',
        "test_name": 1,
        "min_max": None,
        "min_max_speed": [10, 30],
        "slicer": "Prusa Slic3r",
        "number_of_test_structures": 7
        }
    }
# TODO Add to json for report generation
# TODO Create a similar dict for B tests
test_dict = {'1': TestInfo('first-layer track height', 'first-layer-track-height', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=False),
             '2': TestInfo('first-layer track width', 'first-layer-track-width', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=1, raft=False),
             '3': TestInfo('extrusion temperature', 'extrusion-temperature', 'degC', '{:.0f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             '4': TestInfo('track height', 'track-height', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             '5': TestInfo('track width', 'track-width', 'mm', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             '6': TestInfo('extrusion multiplier', 'extrusion-multiplier', '-', '{:.3f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[0.80, 1.40]),
             '7': TestInfo('printing speed', 'printing-speed', 'mm/s', '{:.1f}',
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=1, raft=True, default_value=[0.80, 1.75]),
             '8': TestInfo('retraction distance', 'retraction-distance', 'mm', '{:.3f}',
                           number_of_layers=8, number_of_test_structures=7, number_of_substructures=1, raft=True, default_value=[0., 4.]),
             '9': TestInfo('retraction-restart distance', 'retraction-restart-distance', 'mm', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[0., 0.4]),
             '10': TestInfo('bridging', 'bridging-extrusion-multiplier', '-', '{:.3f}',
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[1.0, 2.0])}

test_info = test_dict[str(persistence["session"]["test_name"])]
persistence["session"]["number_of_test_structures"] = test_info.number_of_test_structures

test_name_list, test_precision_list, test_units_list = [], [], []
test_number_list = test_dict.keys()

for test_number in test_number_list:
    test = test_dict[test_number]
    test_name_list.append(test.parameter)
    test_precision_list.append(test.precision)
    test_units_list.append(test.units)

material = Material(**persistence["material"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **persistence["settings"])
#coef_h_raft, coef_w_raft, coef_h_raft_all = minmax_track_width_height_raft(machine) TODO was it needed for B tests?
