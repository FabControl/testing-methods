from get_test_info import *
from get_values_A import *
from TestStructureGeometriesA import *

def initialize_test(machine: Machine, material: Material, persistence):
    if persistence["session"]["test_type"] == "A":
        values = get_values_A(machine, material, get_test_info(persistence),
                              path=save_session_file_as(str(persistence["session"]["uid"]), "gcode"),
                              offset=persistence["session"]["offset"] if persistence["session"]["offset"] else [0.0,0.0])

        if persistence["session"]["test_number"] in ["08", "09", "10", "11"]:
            retraction_distance(values)
        elif persistence["session"]["test_number"] == "12":
            retraction_restart_distance_vs_coasting_distance(values)
        elif persistence["session"]["test_number"] == "13":
            bridging_test(values)
        else:
            flat_test_parameter_one_vs_parameter_two(values)

    return values