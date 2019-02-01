"""
FabControl 3D Printing Testing Framework
Command Line Interface
Usage:
    CLI.py [-v] [-q]
    CLI.py <session-id> [-v] [-q]
    CLI.py --help
"""

import re
import time
from datetime import datetime
from docopt import docopt
from CLI_helpers import evaluate, clear, extruded_filament
from CheckCompatibility import check_compatibility
from Definitions import *
from DefinitionsTestsA import flat_test_parameter_one_vs_parameter_two, retraction_restart_distance_vs_coasting_distance, retraction_distance, bridging_test
# from DefinitionsTestsB import dimensional_test TODO not working at all
from Globals import machine, material, persistence, filename, session_idn
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
from generate_label import generate_label
from session_loader import session_uid
from test_info import test_info

quiet = True
verbose = False


def initialize_test():
    if persistence["session"]["test_type"] == "A":
        ts = TestSetupA(machine, material, test_info,
                        path=filename(session_id, "gcode"),
                        parameter_one_min_max=parameter_one_min_max,
                        parameter_two_min_max=parameter_two_min_max,
                        parameter_three_min_max=parameter_three_min_max,
                        offset=persistence["session"]["offset"] if persistence["session"]["offset"] else None)

        if persistence["session"]["test_name"] == "08" or "10":
            retraction_distance(ts)
        elif persistence["session"]["test_name"] == "12":
            retraction_restart_distance_vs_coasting_distance(ts)
        elif persistence["session"]["test_name"] == "13":
            bridging_test(ts)
        else:
            flat_test_parameter_one_vs_parameter_two(ts)

    elif persistence["session"]["test_type"] == "B":  # 'perimeter', 'overlap', 'path height', 'temperature'
        ts = TestSetupB(machine, material, test_info,
                        path=filename(session_id, "gcode"),
                        min_max_argument=parameter_one_min_max,
                        min_max_speed_printing=parameter_two_min_max,
                        raft=True if persistence["settings"]["raft_density"] > 0 else False)

        dimensional_test(ts)

    return ts


if __name__ == '__main__':
    arguments = docopt(__doc__, version='MP Feedstock Testing Suite')

    verbose = arguments["-v"]
    quiet = arguments["-q"]
    session_id = arguments["<session-id>"] if arguments["<session-id>"] is not None else session_idn

session = persistence["session"]
start = time.time()

# Check compatibility
check_compatibility(machine, material)

# Some calculations
# these functions work, but they need MVI data for them to work
#from OptimizeSettings import check_printing_speed_shear_rate, check_printing_speed_pressure
from Calculations import shear_rate, pressure_drop, rheology
from Plotting import plotting_mfr
if machine.settings.optimize_speed_printing:
    gamma_dot_estimate = shear_rate(machine, [1000, 0.4])  # starting values (just to get the order of magnitude right)
    delta_p_estimate, _ = pressure_drop(machine, [1000, 0.4])  # starting values (just to get the order of magnitude right)

    number_of_iterations = 5

    for dummy0 in range(0, number_of_iterations + 1):
        gamma_dot, visc, param_power_law = rheology(material, machine, delta_p_estimate, 7)
        gamma_dot_out = shear_rate(machine, param_power_law[int(len(param_power_law)/2)])
        delta_p_out, comment = pressure_drop(machine, param_power_law[int(len(param_power_law)/2)])

        if dummy0 == number_of_iterations:
            plotting_mfr(material, machine, gamma_dot, visc, param_power_law, 7)

    # check_printing_speed_shear_rate(machine, gamma_dot_out, quiet)
    # check_printing_speed_pressure(machine, material, delta_p_out, param_power_law)

if quiet:
    parameter_one_min_max = session["min_max_parameter_one"] if session["min_max_parameter_one"] != "" else None

    test_info = test_info(persistence)
    parameter_three_min_max = session["min_max_parameter_three"] if "min_max_parameter_three" in session else None

    if test_info.name == "retraction distance":
        parameter_two_min_max = [persistence["settings"]["speed_printing"]] * test_info.number_of_substructures
        ts = initialize_test()
    elif test_info.name == "printing speed":
        parameter_two_min_max = None
        ts = initialize_test()
    elif test_info.name == "first-layer track width":
        parameter_two_min_max = None
        ts = initialize_test()
    elif test_info.name == "track width":
        parameter_two_min_max = None
        ts = initialize_test()
    else:
        parameter_two_min_max = session["min_max_parameter_two"]
        ts = initialize_test()

    # Add a step for selecting/approving of the result
    previous_tests = persistence["session"]["previous_tests"]

    persistence["settings"]["temperature_printbed_setpoint"] = machine.settings.temperature_printbed_setpoint
    persistence["settings"]["temperature_chamber_setpoint"] = machine.settings.temperature_chamber_setpoint
    persistence["settings"]["part_cooling_setpoint"] = machine.settings.part_cooling_setpoint

    current_test = {"test_name": ts.test_name,
                    "executed": True,
                    "tested_parameter_one_values": [round(k, int(re.search("[0-9]", ts.test_info.parameter_one.precision).group())) for k in ts.get_values_parameter_one()],
                    "tested_parameter_two_values": None if ts.test_info.parameter_two.name is None else [round(k, int(re.search("[0-9]", ts.test_info.parameter_two.precision).group())) for k in ts.get_values_parameter_two()],
                    "tested_volumetric_flow-rate_values": ts.volumetric_flow_rate,
                    "selected_parameter_one_value": 0,
                    "selected_parameter_two_value": None if ts.test_info.parameter_two.name is None else 0,
                    "selected_volumetric_flow-rate_value": np.mean(ts.volumetric_flow_rate) if ts.test_info.name == ("retraction distance" or "extrusion temperature vs retraction distance") else 0,
                    "parameter_one_units": ts.test_info.parameter_one.units,
                    "parameter_two_units": None if ts.test_info.parameter_two.name is None else ts.test_info.parameter_two.units,
                    "parameter_one_precision": ts.test_info.parameter_one.precision,
                    "parameter_two_precision": None if ts.test_info.parameter_two.name is None else ts.test_info.parameter_two.precision,
                    "extruded_filament_mm": extruded_filament(filename(session_id, "gcode")),
                    "gcode_path": filename(session_id, "gcode"),
                    "label_path": filename(session_id, "png"),
                    "comments": 0,
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    if test_info.parameter_three:
        current_test["tested_parameter_three_values"] = [ts.test_info.parameter_three.values[0], ts.test_info.parameter_three.values[-1]]
        current_test["selected_parameter_three_value"] = 0
        current_test["parameter_three_units"] = ts.test_info.parameter_three.units
        current_test["parameter_three_precision"] = ts.test_info.parameter_three.precision

    previous_tests.append(current_test)

    persistence["session"]["previous_tests"] = previous_tests

else:
    # TODO: to be rewritten
    test_list = {"01": "first-layer track height vs first-layer printing speed",
                 "02": "first-layer track width",
                 "03": "extrusion temperature vs printing speed",
                 "04": "track height vs printing speed",
                 "05": "track width",
                 "06": "extrusion multiplier vs printing speed",
                 "07": "printing speed",
                 "08": "retraction distance",
                 "09": "retraction-restart distance vs coasting distance",
                 "10": "bridging extrusion-multiplier vs bridging printing speed",
                 "11": "extrusion temperature vs retraction distance"}

    test_number = str(input("Parameter to be tested:" + "".join("\n[{0}] for '{1}'".format(*k) for k in zip(list(test_list.keys()), list(test_list.values()))) + ": "))

    persistence["session"]["test_name"] = test_number.strip()
    test_info = test_info(persistence)

    min_max_argument_input = evaluate(input("Parameter range values [min, max] or None: "))
    parameter_one_min_max = min_max_argument_input if min_max_argument_input != "" else None

    if test_info.name == "retraction distance" or "extrusion temperature vs retraction distance":
        parameter_two_min_max = [persistence["settings"]["speed_printing"]] * 4
        ts = initialize_test()
        tested_speed_values = [np.mean(ts.speed_printing)]
    elif test_info.name == "printing speed":
        parameter_two_min_max = None
        ts = initialize_test()
        tested_speed_values = ts.get_values_parameter_one()
    else:
        parameter_two_min_max = evaluate(input("Printing-speed range [min, max] or None: "))
        ts = initialize_test()
        tested_speed_values = ts.parameter_two_min_max

    ts = initialize_test()

    if not verbose:
        clear()
    print("Tested Parameter values:")
    print([round(k,int(re.search("[0-9]",ts.test_info.parameter_one.precision).group())) for k in ts.get_values_parameter_one()[::-1]])
    print("Corresponding Volumetric flow-rate values (mm3/s):")
    [print(x[::-1]) for x in ts.volumetric_flow_rate]

    if parameter_two_min_max is not None:
        print("Printing-speed values (mm/s):")
        parameter_two_min_max = ts.parameter_two_min_max
        print([round(k, 1) for k in parameter_two_min_max])

    # Add a step for selecting/approving of the result
    previous_tests = persistence["session"]["previous_tests"]

    if ts.test_name == "printing speed":
        tested_speed_values = ts.get_values()
    elif ts.test_name == "retraction distance":
        tested_speed_values = [np.mean(ts.speed_printing)]
    else:
        tested_speed_values = persistence["settings"]["speed_printing"] if parameter_two_min_max is None else ts.parameter_two_min_max

    if ts.test_name == "retraction distance" or parameter_two_min_max is None:
        tested_speed_values = []

    current_test = {"test_name": ts.test_name,
                    "executed": True,
                    "tested_parameter_values": [round(k, int(re.search("[0-9]",ts.test_info.precision).group())) for k in ts.get_values()],
                    "tested_printing-speed_values": [round(k, 1) for k in tested_speed_values],
                    "tested_volumetric_flow-rate_values": ts.volumetric_flow_rate,
                    "selected_parameter_value": evaluate(input("Enter the best parameter value: ")),
                    "selected_printing-speed_value": evaluate(input("Enter the printing-speed value (mm/s) which corresponds to the best strucuture: ")),
                    "selected_volumetric_flow-rate_value": evaluate(input("Enter the volumetric flow-rate value (mm3/s) which corresponds to the best strucuture: ")),
                    "units": ts.test_info.units,
                    "parameter_precision": ts.test_info.precision,
                    "extruded_filament": extruded_filament(filename(session_id, "gcode")),
                    "gcode_path": filename(session_id, "gcode"),
                    "label_path": filename(session_id, "png"),
                    "comments": input("Comments: "),
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    previous_tests.append(current_test)
    persistence["session"]["previous_tests"] = previous_tests

    for dummy in persistence["session"]["previous_tests"]:
        if dummy["executed"]:
            if dummy["test_name"] == "printing speed":
                persistence["settings"]["speed_printing"] = dummy["selected_parameter_value"]
            elif dummy["test_name"] == "track height":
                persistence["settings"]["track_height"] = dummy["selected_parameter_value"]
                persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "first-layer track height":
                persistence["settings"]["track_height_raft"] = dummy["selected_parameter_value"]
                persistence["settings"]["track_width_raft"] = np.mean(ts.coef_w_raft) * machine.nozzle.size_id
                persistence["settings"]["speed_printing_raft"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "first-layer track width":
                persistence["settings"]["track_height_raft"] = np.mean(ts.coef_h_raft) * machine.nozzle.size_id
                persistence["settings"]["track_width_raft"] = dummy["selected_parameter_value"]
                persistence["settings"]["speed_printing_raft"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "track width":
                persistence["settings"]["track_width"] = dummy["selected_parameter_value"]
                persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "extrusion temperature":
                persistence["settings"]["temperature_extruder"] = dummy["selected_parameter_value"]
                persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "extrusion multiplier":
                persistence["settings"]["extrusion_multiplier"] = dummy["selected_parameter_value"]
                persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "retraction distance":
                persistence["settings"]["retraction_distance"] = dummy["selected_parameter_value"]
                persistence["settings"]["speed_printing"] = dummy["selected_printing-speed_value"]
            elif dummy["test_name"] == "bridging extrusion-multiplier":
                persistence["settings"]["bridging_extrusion_multiplier"] = dummy["selected_parameter_value"]
                persistence["settings"]["bridging_speed_printing"] = dummy["selected_printing-speed_value"]

persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2 * persistence["settings"]["track_height"] / persistence["settings"]["track_width"])), 0)

with open(filename(session_id, "json"), mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)

generate_label(persistence)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')
