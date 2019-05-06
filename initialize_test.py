from get_test_info import *
from TestStructureGeometriesA import TestStructure as TS
from get_values_A import get_values_A
from persistence import Persistence


def initialize_test(persistence: Persistence, buffer):

    if persistence.dict["session"]["test_type"] == "A":
        test_structure, gcode = TS(persistence)
        values = get_values_A(persistence, persistence.test_info,
                              path=save_session_file_as(persistence.dict, extension="gcode", session_id=str(persistence.id)),
                              offset=persistence.dict["session"]["offset"] if persistence.dict["session"]["offset"] else [0,0])

        if persistence.dict["session"]["test_number"] in ["08", "09", "10", "11"]:
            test_structure.retraction_distance(values)
        elif persistence.dict["session"]["test_number"] == "12":
            test_structure.retraction_restart_distance_vs_coasting_distance(values)
        elif persistence.dict["session"]["test_number"] == "13":
            test_structure.bridging_test(values)
        else:
            test_structure.flat_test_parameter_one_vs_parameter_two(values)

        return values, gcode
