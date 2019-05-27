from get_test_info import get_test_info
from Definitions import *
import re
from datetime import datetime
from CLI_helpers import extruded_filament
from gcoder import GCode

def update_persistence(persistence, values, gcode: GCode):

    session_id = str(persistence["session"]["uid"])
    test_info = get_test_info(persistence)
    previous_tests = persistence["session"]["previous_tests"]

    current_test = {"test_name": values.test_name,
                    "test_number": values.test_number,
                    "executed": True,
                    "tested_parameter_one_values": values.get_values_parameter_one(),
                    "tested_parameter_two_values": None if values.test_info.parameter_two.name is None else values.get_values_parameter_two(),
                    "tested_volumetric_flow-rate_values": values.volumetric_flow_rate,
                    "selected_parameter_one_value": 0,
                    "selected_parameter_two_value": None if values.test_info.parameter_two.name is None else (values.test_info.parameter_two.values[0] if len(values.test_info.parameter_two.values) == 1 else 0),
                    "selected_volumetric_flow-rate_value": np.mean(values.volumetric_flow_rate) if values.test_info.test_number in ("08", "10", "11", "12") else 0,
                    "parameter_one_name": values.test_info.parameter_one.name,
                    "parameter_two_name": values.test_info.parameter_two.name,
                    "parameter_one_units": values.test_info.parameter_one.units,
                    "parameter_two_units": None if values.test_info.parameter_two.name is None else values.test_info.parameter_two.units,
                    "parameter_one_precision": values.test_info.parameter_one.precision,
                    "parameter_two_precision": None if values.test_info.parameter_two.name is None else values.test_info.parameter_two.precision,
                    "gcode_path": save_session_file_as(session_id, "gcode"),
                    "label_path": save_session_file_as(session_id, "png"),
                    "comments": 0,
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "extruded_filament_mm": round(gcode.filament_length_e,2),
                    "estimated_printing_time": str(gcode.estimate_duration()[1])}

    if test_info.parameter_three:
        current_test["tested_parameter_three_values"] = [values.test_info.parameter_three.values[0], values.test_info.parameter_three.values[-1]]
        current_test["selected_parameter_three_value"] = 0
        current_test["parameter_three_name"] = values.test_info.parameter_three.name
        current_test["parameter_three_units"] = values.test_info.parameter_three.units
        current_test["parameter_three_precision"] = values.test_info.parameter_three.precision


    previous_tests.append(current_test)
    persistence["session"]["previous_tests"] = previous_tests
    persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*persistence["settings"]["track_height"] / persistence["settings"]["track_width"])), 0)

    with open(save_session_file_as(session_id, "json"), mode="w") as file:
        output = json.dumps(persistence, indent=4, sort_keys=False)
        file.write(output)