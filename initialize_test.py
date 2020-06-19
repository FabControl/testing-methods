from get_test_info import *
from TestStructureGeometriesA import TestStructure as TS
from get_values_A import get_values_A
from persistence import Persistence


class OptimizerSession(object):
    def __init__(self, persistence: Persistence):
        self.values = None
        self.values = get_values_A(persistence, persistence.test_info,
                                   path=save_session_file_as(persistence.dict, extension="gcode", session_id=str(persistence.id)),
                                   offset=persistence.dict["session"]["offset"] if persistence.dict["session"]["offset"] else [0, 0])
        self.test_structure = TS(persistence)
        if persistence.dict["session"]["test_number"] in ["08", "09", "10", "11"]:
            self.test_structure.retraction_distance(self.values)
        elif persistence.dict["session"]["test_number"] == "12":
            self.test_structure.retraction_restart_distance_vs_coasting_distance(self.values)
        elif persistence.dict["session"]["test_number"] == "13":
            self.test_structure.bridging_test(self.values)
        else:
            self.test_structure.flat_test_parameter_one_vs_parameter_two(self.values)

        self.g = self.values.g
