"""
Mass Portal Feedstock Testing Suite
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
from DefinitionsTestsA import flat_test_single_parameter_vs_speed_printing, retraction_restart_distance_vs_coasting_distance, retraction_distance, bridging_test
# from DefinitionsTestsB import dimensional_test TODO not working at all
from Globals import machine, material, persistence, test_number_list, test_name_list, test_dict, filename, session_idn
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
from paths import cwd
from generate_label import generate_label
from session_loader import session_uid

quiet = True
verbose = False

def initialize_test():
    if persistence["session"]["test_type"] == "A":
        ts = TestSetupA(machine, material, test_info, path=filename(cwd, session_id, "gcode"),
                        min_max_argument=min_max_argument,
                        min_max_speed_printing=min_max_speed_printing)

        if test_info.name == 'retraction distance':
            retraction_distance(ts)
        elif test_info.name == 'retraction-restart distance':
            retraction_restart_distance_vs_coasting_distance(ts)
        elif test_info.name == 'bridging extrusion-multiplier':
            bridging_test(ts)
        else:
            flat_test_single_parameter_vs_speed_printing(ts)

    elif persistence["session"]["test_type"] == "B":  # 'perimeter', 'overlap', 'path height', 'temperature'
        ts = TestSetupB(machine, material, test_info, path=filename(cwd, session_id, "gcode"),
                        min_max_argument=min_max_argument,
                        min_max_speed_printing=min_max_speed_printing,
                        raft=True if persistence["settings"]["raft_density"] > 0 else False)

        dimensional_test(ts)

    return ts


if __name__ == '__main__':
    arguments = docopt(__doc__, version='MP Feedstock Testing Suite')

    verbose = arguments["-v"]
    quiet = arguments["-q"]
    session_id = arguments["<session-id>"] if arguments["<session-id>"] is not None else session_idn

#     if arguments["generate-configuration"]:
#         slicer_arg = str(arguments["<slicer>"]).lower()
#         if slicer_arg == 'prusa' or slicer_arg == "simplify3d":
#             persistence["session"]["slicer"] = slicer_arg
#             import generate_configuration
#         else:
#             raise ValueError("{} not recognized. Accepted slicers are 'Prusa', 'Simplify3D'.".format(slicer_arg))
#         quit()
#
# if arguments["generate-gcode-iso"]:
#     config = arguments["<config>"]
#     generate_gcode(arguments['<orientation>'], arguments['<count>'], arguments['<rotation>'], arguments["<file>"], config)
#     quit()

session = persistence["session"]
start = time.time()

# Check compatibility
check_compatibility(machine, material)

# # Some calculations
# these functions work, but they need MVI data for them to work
# from Calculations import shear_rate, pressure_drop, rheology
# from OptimizeSettings import check_printing_speed_shear_rate, check_printing_speed_pressure
# from Plotting import plotting_mfr
# if machine.settings.optimize_speed_printing:
#     gamma_dot_estimate = shear_rate(machine, [1000, 0.4])  # starting values (just to get the order of magnitude right)
#     delta_p_estimate, _ = pressure_drop(machine, [1000, 0.4])  # starting values (just to get the order of magnitude right)
#
#     number_of_iterations = 5
#
#     for dummy0 in range(0, number_of_iterations + 1):
#         gamma_dot, visc, param_power_law = rheology(material, machine, delta_p_estimate, session["number_of_test_structures"])
#         gamma_dot_out = shear_rate(machine, param_power_law[int(len(param_power_law) / 2)])
#         delta_p_out, comment = pressure_drop(machine, param_power_law[int(len(param_power_law) / 2)])
#
#         if dummy0 == number_of_iterations:
#             print(comment)
#             plotting_mfr(material, machine, gamma_dot, visc, param_power_law, session["number_of_test_structures"] )
#
#     check_printing_speed_shear_rate(machine, gamma_dot_out, quiet)
#     check_printing_speed_pressure(machine, material, delta_p_out, param_power_law)

if quiet:
    test_info = test_dict[str(persistence["session"]["test_name"])]
    min_max_argument = session["min_max"] if session["min_max"] != "" else None

    if test_info.name == 'retraction distance':
        min_max_speed_printing = [persistence["settings"]["speed_printing"]] * 4
    elif test_info.name == 'printing speed':
        min_max_speed_printing = None
    else:
        min_max_speed_printing = session["min_max_speed"]

    ts = initialize_test()

    # Add a step for selecting/approving of the result
    previous_tests = persistence["session"]["previous_tests"]

    if ts.test_name == "printing speed":
        tested_speed_values = ts.get_values()
    elif ts.test_name == "retraction distance":
        tested_speed_values = [np.mean(ts.speed_printing)]
    else:
        tested_speed_values = ts.min_max_speed_printing

    if ts.test_name == "first-layer track height":
        persistence["settings"]["track_width_raft"] = np.mean(ts.track_width)

    current_test = {"test_name": ts.test_name,
                    "tested_parameter_values": [round(k, int(re.search("[0-9]", ts.test_info.precision).group())) for k in ts.get_values()],
                    "tested_printing-speed_values": [round(k, 1) for k in tested_speed_values],
                    "tested_volumetric_flow-rate_values": ts.volumetric_flow_rate,
                    "selected_parameter_value": 0,
                    "selected_printing-speed_value": 0,
                    "selected_volumetric_flow-rate_value": 0,
                    "units": ts.test_info.units,
                    "parameter_precision": ts.test_info.precision,
                    "extruded_filament": extruded_filament(filename(cwd, session_id, "gcode")),
                    "gcode_path": filename(cwd, session_id, "gcode"),
                    "label_path": filename(cwd, session_id, "png"),
                    "comments": 0,
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    previous_tests.append(current_test)
    persistence["session"]["previous_tests"] = previous_tests

else:
    test_number = str(input("Parameter to be tested:" + "".join("\n[{0}] for '{1}'".format(*k) for k in zip(test_number_list, test_name_list)) + ": "))
    persistence["session"]["test_name"] = test_number.strip()
    test_info = test_dict[test_number]
    min_max_argument_input = evaluate(input("Parameter range values [min, max] or None: "))
    min_max_argument = min_max_argument_input if min_max_argument_input != "" else None
    session["number_of_test_structures"] = test_info.number_of_test_structures

    if test_info.name == 'retraction distance':
        min_max_speed_printing = [persistence["settings"]["speed_printing"]] * 4
    elif test_info.name == 'printing speed':
        min_max_speed_printing = None
    else:
        min_max_speed_printing = evaluate(input("Printing-speed range [min, max] or None: "))

    ts = initialize_test()

    if not verbose:
        clear()
    print("Tested Parameter values:")
    print([round(k,int(re.search("[0-9]",ts.test_info.precision).group())) for k in ts.get_values()[::-1]])
    print("Corresponding Volumetric flow-rate values (mm3/s):")
    [print(x[::-1]) for x in ts.volumetric_flow_rate]

    if min_max_speed_printing is not None:
        print("Printing-speed values (mm/s):")
        min_max_speed_printing = ts.min_max_speed_printing
        print([round(k, 1) for k in min_max_speed_printing])

    # Add a step for selecting/approving of the result
    previous_tests = persistence["session"]["previous_tests"]

    if ts.test_name == "printing speed":
        tested_speed_values = ts.get_values()
    elif ts.test_name == "retraction distance":
        tested_speed_values = [np.mean(ts.speed_printing)]
    else:
        tested_speed_values = persistence["settings"]["speed_printing"] if min_max_speed_printing is None else ts.min_max_speed_printing

    if ts.test_name == "retraction distance" or min_max_speed_printing is None:
        tested_speed_values = []

    current_test = {"test_name": ts.test_name,
                    "tested_parameter_values": [round(k, int(re.search("[0-9]", ts.test_info.precision).group())) for k in ts.get_values()],
                    "tested_printing-speed_values": [round(k, 1) for k in tested_speed_values],
                    "tested_volumetric_flow-rate_values": ts.volumetric_flow_rate,
                    "selected_parameter_value": evaluate(input("Enter the best parameter value: ")),
                    "selected_printing-speed_value": evaluate(input("Enter the printing-speed value (mm/s) which corresponds to the best strucuture: ")),
                    "selected_volumetric_flow-rate_value": evaluate(input("Enter the volumetric flow-rate value (mm3/s) which corresponds to the best strucuture: ")),
                    "units": ts.test_info.units,
                    "parameter_precision": ts.test_info.precision,
                    "extruded_filament": extruded_filament(filename(cwd, session_id, "gcode")),
                    "gcode_path": filename(cwd, session_id, "gcode"),
                    "label_path": filename(cwd, session_id, "png"),
                    "comments": input("Comments: "),
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    previous_tests.append(current_test)
    persistence["session"]["previous_tests"] = previous_tests

if not quiet:
    for dummy in persistence["session"]["previous_tests"]:
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

persistence["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2 * persistence["settings"]["track_height"] / persistence["settings"]["track_width"])), 0)

with open(filename(cwd, session_id, "json"), mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)

generate_label(persistence)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')
