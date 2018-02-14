from Definitions import Material, Settings, Machine, header, footer, minmax_path_width_height_raft
from GcodeStuff import Gplus
import json

try:
    with open("persistence.json", mode="r") as file:
        import_json_dict = json.load(file)
except:
    print("falling back to hardcoded JSON")
    import_json_dict = {
        "material": {
            "name": "Nylon",
            "manufacturer": "Filakemp",
            "id": "123456",
            "size_od": 1.75,
            "temperature_melting": 210,
            "temperature_destr": 300,
            "temperature_vicat": 144
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
                "size_id": 0.80,
                "size_od": 1.04,
                "size_capillary_length": 5,
                "size_angle": 60,
                "metal": "brass"
            }
        },
        "settings": {
            "temperature_printbed_raft": 110,
            "temperature_printbed": 110,
            "part_cooling": 100,

            "raft_density": 95,

            "temperature_extruder_raft": 240,

            "path_height_raft": 0.4,
            "speed_printing_raft": 20,

            "temperature_extruder": 240,
            "speed_printing": 50,

            "path_height": 0.4,
            "path_width": 0.800,

            "extrusion_multiplier": 1.000,

            "retraction_distance": 2.00,
            "retraction_restart_distance": 0.45,
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
            "test_name": 'path width'
        }
    }

material = Material(**import_json_dict["material"])
machine = Machine(**import_json_dict["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **import_json_dict["settings"])
g = Gplus(material, machine, outfile="placeholder.gcode", footer=footer, header=header, aerotech_include=False)
coef_h_raft, coef_h_min_raft, coef_h_max_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine) #TODO really needed?