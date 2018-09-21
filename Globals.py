from Definitions import Material, Settings, Machine, TestInfo, DryingProcess
import json
from session_loader import session_uid
from paths import json_folder
from CLI_helpers import separator, exception_handler

try:
    try:
        print("Attempting to load the persistence file with ID {}".format(session_uid))
        with open(str(json_folder + separator() + session_uid + ".json"), mode="r") as file:
            persistence = json.load(file)
        print("Loaded a testing session ID {} from the existing JSON file".format(persistence["session"]["uid"]))
        file.close()
    except:
        exception_handler("Session not found")
        print("Attempting to load the persistence file without an ID".format(session_uid))
        with open(str("persistence.json"), mode="r") as file:
            persistence = json.load(file)
        print("Loaded a testing session ID {} from the existing JSON file".format(persistence["session"]["uid"]))
        file.close()
except:
    exception_handler("falling back to hardcoded JSON")
    persistence = {
        "material": {
            "name": "Nanodiamond B",
            "manufacturer": "?",
            "material_group": "filled polymer",
            "polymer_class": "PLA",
            "id": "123456",
            "size_od": 1.75,
            "temperature_melting": 178,
            "temperature_destr": 320,
            "density_rt": 1.2,  # optional
            "drying": {
                "dried": True,
                "drying_temperature": 80,
                "drying_time": 240,
                "drying_airflow": 40,
                "feeding_temperature": 40,
                "feeding_airflow": 10
            },
        },
        "machine": {
            "manufacturer": "Mass Portal",
            "model": "Pharaoh D20",
            "sn": 0,
            "form": "elliptic",  # "elliptic", "cartesian"
            "buildarea_maxdim1": 145,
            "buildarea_maxdim2": 145,
            "max_dimension_z": 200,
            "temperature_extruder_max": 320,
            "temperature_extruder_min": 190,
            "nozzle": {
                "size_id": 0.4,
                "size_od": 0.64,
                "size_capillary_length": 5,  # optional
                "size_angle": 60,  # optional
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
            "optimize_speed_printing": True,  # optional
            "ventilator_part_cooling": 0,
            "ventilator_entry": 0,
            "ventilator_exit": 0,
            "raft_density": 100,
            "temperature_printbed": 100,
            "temperature_extruder_raft": 235,
            "track_height_raft": 0.25,
            "track_width_raft": 0.4,
            "speed_printing_raft": 20,
            "temperature_extruder": 235,
            "track_height": 0.2,
            "track_width": 0.4,
            "speed_printing": 40,
            "speed_travel": 150,
            "extrusion_multiplier": 1.0,
            "retraction_distance": 0,
            "retraction_restart_distance": 0.0,
            "retraction_speed": 80,
            "coasting_distance": 0.0,
            "critical_overhang_angle": 36.0,
            "bridging_part_cooling": 100,
            "bridging_extrusion_multiplier": 1,
            "bridging_speed_printing": 40
        },
        "session": {
            "uid": 20180529,
            "user_id": "GB",
            "previous_tests": [],
            "test_type": "A",
            "test_name": "01",
            "min_max": None,
            "min_max_speed": [10, 30],
            "slicer": "Prusa Slic3r",
            "number_of_test_structures": 7,
            "target": "aesthetics"
        }
    }

test_dict = {"01": TestInfo("first-layer track height", "first-layer-track-height", "mm", "{:.3f}",
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=False),
             "02": TestInfo("first-layer track width", "first-layer-track-width", "mm", "{:.3f}",
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=1, raft=False),
             "03": TestInfo("extrusion temperature", "extrusion-temperature", "degC", "{:.0f}",
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             "04": TestInfo("track height", "track-height", "mm", "{:.3f}",
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             "05": TestInfo("track width", "track-width", "mm", "{:.3f}",
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True),
             "06": TestInfo("extrusion multiplier", "extrusion-multiplier", "-", "{:.3f}",
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[0.80, 1.40]),
             "07": TestInfo("printing speed", "printing-speed", "mm/s", "{:.1f}",
                           number_of_layers=2, number_of_test_structures=7, number_of_substructures=1, raft=True, default_value=[0.80, 1.75]),
             "08": TestInfo("retraction distance", "retraction-distance", "mm", "{:.3f}",
                           number_of_layers=3, number_of_test_structures=7, number_of_substructures=1, raft=True, default_value=[0.0, 4.0]),
             "09": TestInfo("retraction-restart distance", "retraction-restart-distance", "mm", "{:.3f}",
                           number_of_layers=1, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[0.0, 0.4]),
             "10": TestInfo("bridging extrusion-multiplier", "bridging-extrusion-multiplier", "-", "{:.3f}",
                           number_of_layers=8, number_of_test_structures=7, number_of_substructures=4, raft=True, default_value=[1.0, 2.0])}

test_info = test_dict[str(persistence["session"]["test_name"])]
session_idn = str(persistence["session"]["uid"])

persistence["session"]["number_of_test_structures"] = test_info.number_of_test_structures

test_name_list, test_precision_list, test_units_list = [], [], []
test_number_list = sorted(test_dict.keys())

for test_number in test_number_list:
    test = test_dict[test_number]
    test_name_list.append(test.name)
    test_precision_list.append(test.precision)
    test_units_list.append(test.units)

material = Material(**persistence["material"])
material.drying = DryingProcess(**persistence["material"]["drying"])
machine = Machine(**persistence["machine"])
machine.settings = Settings(nozzle=machine.nozzle, material=material, **persistence["settings"])


def filename(session_id: str, extension: str) -> str:
    """
    Takes a filename extension and returns a full file-name based on the following convention:
    'cwd\\folder\\YYYYMMDDxxx_TestNumber.extension' where x is a number character from [0-9a-z] and TestNumber is a
    double-digit zero-padded number.
    :param session_id:
    :param extension:
    :return:
    """
    from paths import gcode_folder, json_folder, pdf_folder, stl_folder, png_folder

    if not extension.startswith("."):
        extension = "." + extension

    folder = None

    if extension == ".gcode":
        folder = gcode_folder
    elif extension == ".json":
        folder = json_folder
    elif extension == ".pdf":
        folder = pdf_folder
    elif extension == ".stl":
        folder = stl_folder
    elif extension == ".png":
        folder = png_folder

    if extension == ".gcode":
        output = str(folder + separator() + session_id) + "_{}".format(str(persistence["session"]["test_name"])) + extension
    elif extension == ".png":
        output = str(folder + separator() + session_id) + "_{}".format(str(persistence["session"]["test_name"])) + extension
    else:
        output = str(folder + separator() + session_id + extension)
    return output
