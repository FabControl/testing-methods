"""
Mass Portal Feedstock Testing Suite
Command Line Interface
Usage:
    CLI.py [-v] [-q] [--flash]
    CLI.py new-test
    CLI.py generate-report
    CLI.py generate-configuration <slicer>
    CLI.py generate-gcode-iso <orientation> <count> <rotation> <config> <file>
    CLI.py --help
"""
#python CLI.py generate-gcode-iso horizontal 4 90 "Carbodeon_Nanodiamond PLA A_1-75_0-8.ini" ISO527-1A.stl

from CheckCompatibility import check_compatibility
from CLI_helpers import evaluate, clear, extruded_filament, generate_gcode, separator, exclusive_write
from Definitions import *
from DefinitionsTestsA import flat_test_single_parameter_vs_speed_printing, retraction_restart_distance_vs_coasting_distance, retraction_distance, bridging_test
#from DefinitionsTestsB import dimensional_test TODO not working at all
from datetime import datetime
from docopt import docopt
from Globals import machine, material, import_json_dict
from Globals import test_number_list, test_name_list, test_dict
from paths import cwd, gcode_folder
import re, subprocess
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
import time

quiet = True
verbose = True
flash = False

def initialize_test():
    path = str(cwd + gcode_folder + separator() + test_info.name + ' test' + '.gcode')

    if import_json_dict["session"]["test_type"] == "A":
        ts = TestSetupA(machine, material, test_info, path,
                        min_max_argument=min_max_argument,
                        min_max_speed_printing=min_max_speed_printing)

        if test_info.name == 'retraction distance':
            retraction_distance(ts)
        elif test_info.name == 'retraction restart distance':
            retraction_restart_distance_vs_coasting_distance(ts)
        elif test_info.name == 'bridging':
            bridging_test(ts)
        else:
            flat_test_single_parameter_vs_speed_printing(ts)

    elif import_json_dict["session"]["test_type"] == "B":  # 'perimeter', 'overlap', 'path height', 'temperature'
        ts = TestSetupB(machine, material, test_info, path,
                        min_max_argument=min_max_argument,
                        min_max_speed_printing=min_max_speed_printing,
                        raft=True if import_json_dict["settings"]["raft_density"] > 0 else False)

        dimensional_test(ts)

    return ts

if __name__ == '__main__':
    arguments = docopt(__doc__, version='MP Feedstock Testing Suite')

    verbose = arguments["-v"]
    quiet = arguments["-q"]
    flash = arguments["--flash"]

    if arguments["generate-configuration"]:
        slicer_arg = str(arguments["<slicer>"]).lower()
        if slicer_arg == 'prusa' or slicer_arg == "simplify3d":
            import_json_dict["session"]["slicer"] = slicer_arg
            import generate_configuration
        else:
            raise ValueError("{} not recognized. Accepted slicers are 'Prusa', 'Simplify3D'.".format(slicer_arg))
        quit()

if arguments["generate-gcode-iso"]:
    config = arguments["<config>"]
    generate_gcode(arguments['<orientation>'], arguments['<count>'], arguments['<rotation>'], arguments["<file>"], config)
    quit()

session = import_json_dict["session"]
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

if not verbose:
    clear()

if quiet:
    test_info = test_dict[str(import_json_dict["session"]["test_name"])]
    min_max_argument = session["min_max"] if session["min_max"] != "" else None
    session["number_of_test_structures"] = test_info.number_of_test_structures

    if test_info.name == 'retraction distance':
        min_max_speed_printing = [import_json_dict["settings"]["speed_printing"]] * 4
    elif test_info.name == 'printing speed':
        min_max_speed_printing = None
    else:
        min_max_speed_printing = session["min_max_speed"]

    ts = initialize_test()

    # Add a step for selecting/approving of the result
    previous_tests = import_json_dict["session"]["previous_tests"]

    if ts.test_name == "printing speed":
        tested_speed_values = ts.get_values()
    elif ts.test_name == "retraction distance":
        tested_speed_values = []
    else:
        tested_speed_values = import_json_dict["settings"][
            "speed_printing"] if min_max_speed_printing is None else ts.min_max_speed_printing

    if ts.test_name == "retraction distance" or min_max_speed_printing is None:
        tested_speed_values = []

    current_test = {"test_name": ts.test_name,
                    "tested_parameter_values": [round(k, int(re.search("[0-9]", ts.test_info.precision).group())) for k in ts.get_values()],
                    "tested_speed_values": [round(k, 1) for k in tested_speed_values],
                    "selected_parameter_value": 0,
                    "selected_speed_value": 0,
                    "units": ts.test_info.units,
                    "parameter_precision": ts.test_info.precision,
                    "extruded_filament": extruded_filament(cwd + gcode_folder + separator() + ts.test_name + " test.gcode"),
                    "selected_volumetric_flow_rate_value": 0,
                    "comments": 0,
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    previous_tests.append(current_test)
    import_json_dict["session"]["previous_tests"] = previous_tests

else:
    test_info = test_dict[str(int(input("Parameter to be tested:" + "".join("\n[{0}] for '{1}'".format(*k) for k in zip(test_number_list, test_name_list)) + ": ")))]
    min_max_argument_input = evaluate(input("Parameter range values [min, max] or None: "))
    min_max_argument = min_max_argument_input if min_max_argument_input != "" else None
    session["number_of_test_structures"] = test_info.number_of_test_structures

    if test_info.name == 'retraction distance':
        min_max_speed_printing = [import_json_dict["settings"]["speed_printing"]] * 4
    elif test_info.name == 'printing speed':
        min_max_speed_printing = None
    else:
        min_max_speed_printing = evaluate(input("Printing speed range values [min, max] or None: "))

    ts = initialize_test()

    if not verbose:
        clear()
    print("Tested Parameter values:")
    print([round(k,int(re.search("[0-9]",ts.test_info.precision).group())) for k in ts.get_values()[::-1]])
    print("Corresponding Volumetric flow rate values (mm3/s):")
    [print(x[::-1]) for x in ts.volumetric_flow_rate]

    if min_max_speed_printing is not None:
        print("Printing speed values:")
        min_max_speed_printing = ts.min_max_speed_printing
        print([round(k, 1) for k in min_max_speed_printing])

    # Add a step for selecting/approving of the result
    previous_tests = import_json_dict["session"]["previous_tests"]

    if ts.test_name == "printing speed":
        tested_speed_values = ts.get_values()
    elif ts.test_name == "retraction distance":
        tested_speed_values = []
    else:
        tested_speed_values = import_json_dict["settings"]["speed_printing"] if min_max_speed_printing is None else ts.min_max_speed_printing

    if ts.test_name == "retraction distance" or min_max_speed_printing is None:
        tested_speed_values = []

    current_test = {"test_name": ts.test_name,
                    "tested_parameter_values": [round(k, int(re.search("[0-9]",ts.test_info.precision).group())) for k in ts.get_values()],
                    "tested_speed_values": [round(k, 1) for k in tested_speed_values],
                    "selected_parameter_value": evaluate(input("Enter the best parameter value: ")) if not quiet else 0,
                    "selected_speed_value": evaluate(input("Enter the printing speed value which corresponds to the best parameter value: ")) if not quiet else 0,
                    "units": ts.test_info.units,
                    "parameter_precision": ts.test_info.precision,
                    "extruded_filament": extruded_filament(cwd + gcode_folder + separator() + ts.test_name + " test.gcode"),
                    "selected_volumetric_flow_rate_value": evaluate(input("Enter the volumetric flow rate value which corresponds to the best parameter value: ")) if not quiet else 0,
                    "comments": input("Comments: ") if not quiet else 0,
                    "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    previous_tests.append(current_test)
    import_json_dict["session"]["previous_tests"] = previous_tests

    for dummy in import_json_dict["session"]["previous_tests"]:
        if dummy["test_name"] == "printing speed":
            import_json_dict["settings"]["speed_printing"] = dummy["selected_parameter_value"]
        elif dummy["test_name"] == "path height":
            import_json_dict["settings"]["path_height"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "first layer height":
            import_json_dict["settings"]["path_height_raft"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["path_width_raft"] = np.mean(ts.coef_w_raft) * machine.nozzle.size_id
            import_json_dict["settings"]["speed_printing_raft"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "first layer width":
            import_json_dict["settings"]["path_height_raft"] = np.mean(ts.coef_h_raft) * machine.nozzle.size_id
            import_json_dict["settings"]["path_width_raft"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["speed_printing_raft"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "path width":
            import_json_dict["settings"]["path_width"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "extrusion temperature":
            import_json_dict["settings"]["temperature_extruder"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "extrusion multiplier":
            import_json_dict["settings"]["extrusion_multiplier"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "retraction distance":
            import_json_dict["settings"]["retraction_distance"] = dummy["selected_parameter_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]

    import_json_dict["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*import_json_dict["settings"]["path_height"]/import_json_dict["settings"]["path_width"])),0)

    with open(cwd + separator("jsons") + material.manufacturer + "_" + material.name + "_" + "{:.0f}".format(machine.nozzle.size_id*1000) + "_um" + ".json", mode="w") as file:
        output = json.dumps(import_json_dict, indent=4, sort_keys=False)
        file.write(output)

with open(cwd + separator() + "persistence.json", mode="w") as file:
    output = json.dumps(import_json_dict, indent=4, sort_keys=False)
    file.write(output)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')
