"""
Mass Portal Feedstock Testing Suite
Command Line Interface
Usage:
    CLI.py [-v] [-q] [--flash]
    CLI.py new-test
    CLI.py generate-report
    CLI.py generate-configuration <slicer>
    CLI.py generate-gcode-iso <orientation> <count> <rotation> <config> <path>
    CLI.py --help
"""
#python CLI.py slice-iso horizontal 4 90 "Carbodeon_Nanodiamond PLA A_1-75_0-8.ini" ISO527-1A.stl

# TODO standardize function and scripts names! generate-report, generate-config, generate-gcode etc

import subprocess
from docopt import docopt
quiet = None
verbose = True
flash = False

if __name__ == '__main__':
    arguments = docopt(__doc__, version='MP Feedstock Testing Suite')

    verbose = arguments["-v"]
    quiet = arguments["-q"]
    flash = arguments["--flash"]

    from Globals import machine, material, import_json_dict

    if arguments["generate-configuration"]:
        slicer_arg = str(arguments["<slicer>"]).lower()
        if slicer_arg == 'prusa' or slicer_arg == "simplify3d":
            import_json_dict["session"]["slicer"] = slicer_arg
            import config_writer
        else:
            raise ValueError("{} not recognized. Accepted slicers are 'Prusa', 'Simplify3D'.".format(slicer_arg))
        quit()

from Calculations import shear_rate, pressure_drop, rheology
from CheckCompatibility import check_compatibility
from Definitions import *
from OptimizeSettings import check_printbed_temperature, check_printing_speed_shear_rate, check_printing_speed_pressure
from Plotting import plotting_mfr
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
from CLI_helpers import evaluate, clear, extruded_filament, spawn_iso_slicer, separator, spawn_slicer, exclusive_write
from paths import cwd, gcode_folder
import time

session = import_json_dict["session"]

start = time.time()

if arguments["generate-gcode-iso"]:
    config = arguments["<config>"]
    spawn_iso_slicer(arguments['<orientation>'], arguments['<count>'], arguments['<rotation>'], arguments["<path>"], config)
    quit()

# Check compatibility
#check_compatibility(machine, material)

# Checking some settings for better starting values
if machine.settings.optimize_temperature_printbed: check_printbed_temperature(material, machine)

# Some calculations
if machine.settings.optimize_speed_printing:

    gamma_dot_estimate = shear_rate(machine, [1000, 0.4])  # starting values (just to get the order of magnitude right)
    delta_p_estimate = pressure_drop(machine, [1000, 0.4])  # starting values (just to get the order of magnitude right)

    number_of_iterations = 5

    for dummy0 in range(0, number_of_iterations + 1):
        gamma_dot, visc, param_power_law = rheology(material, machine, delta_p_estimate)

        gamma_dot_out = shear_rate(machine, param_power_law[int(len(param_power_law) / 2)])
        delta_p_out = pressure_drop(machine, param_power_law[int(len(param_power_law) / 2)])

        if dummy0 == number_of_iterations:
            plotting_mfr(material, machine, gamma_dot, visc, param_power_law)

    check_printing_speed_shear_rate(machine, gamma_dot_out)
    check_printing_speed_pressure(machine, material, delta_p_out, param_power_law)

if not verbose:
    clear()

if import_json_dict["session"]["test_type"] == "A":
    from Globals import test_number_list, test_name_list, test_list
    test_number = import_json_dict["session"]["test_name"] if quiet else int(input("Parameter to be tested:" + "".join("\n[{0}] for '{1}'".format(*k) for k in zip(test_number_list, test_name_list)) + ": "))
    test_info = test_list[test_number-1]

    min_max_argument_input = evaluate(input("Parameter range values [min, max] or None: ")) if not quiet else session["min_max"]
    min_max_argument = min_max_argument_input if min_max_argument_input != "" else None

    if test_info.name == 'retraction distance':
        min_max_speed_printing = [import_json_dict["settings"]["speed_printing"]] * 4
    elif test_info.name == 'printing speed':
        min_max_speed_printing = None
    else:
        min_max_speed_printing = evaluate(input("Printing speed range values [min, max] or None: ")) if not quiet else session["min_max_speed"]

    from DefinitionsTestsA import flat_test_single_parameter_vs_speed_printing, retraction_restart_distance_vs_coasting_distance, retraction_distance

    path = str(cwd + gcode_folder + separator() + test_info.name + ' test' + '.gcode')

    ts = TestSetupA(machine, material, test_info, path,
                    min_max_argument=min_max_argument,
                    min_max_speed_printing=min_max_speed_printing,
                    raft=True if import_json_dict["settings"]["raft_density"] > 0 else False)

    if test_info.name == 'retraction distance':
        retraction_distance(ts)
    elif test_info.name == 'retraction restart distance':
        retraction_restart_distance_vs_coasting_distance(ts)
    else:
        flat_test_single_parameter_vs_speed_printing(ts)

elif import_json_dict["session"]["test_type"] == "B": # 'perimeter', 'overlap', 'path height', 'temperature'
    test = 'temperature'  # 'overlap', 'path height']  # TODO top bottom layers, infill?
    min_max_argument = [270, 300]
    min_max_speed_printing = [30, 75]  # check the jerk value

    from DefinitionsTestsB import dimensional_test

    path = str(cwd + gcode_folder + separator() + test + ' test' + '.gcode')

    ts = TestSetupB(machine, material, test, path,
                    min_max_argument = min_max_argument,
                    min_max_speed_printing = min_max_speed_printing,
                    raft = True if import_json_dict["settings"]["raft_density"] > 0 else False)

    dimensional_test(ts)

if not quiet:
    if not verbose:
        clear()
    print("Tested Parameter values:")
    print(ts.get_values()[::-1])
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

import_json_dict["settings"]["path_width_raft"] = round(ts.coef_w_raft*machine.nozzle.size_id, 2)

current_test = {"test_name": ts.test_name,
                "tested_values": ts.get_values(),
                "tested_speed_values": tested_speed_values,
                "selected_value": evaluate(input("Enter the best parameter value: ")) if not quiet else 0,
                "selected_speed_value": evaluate(input("Enter the printing speed value which corresponds to the best parameter value: ")) if not quiet else 0,
                "units": ts.units[0],
                "extruded_filament": extruded_filament(cwd + gcode_folder + separator() + ts.test_name + " test.gcode"),
                "selected_volumetric_flow_rate_value": evaluate(input("Enter the volumetric flow rate value which corresponds to the best parameter value: ")) if not quiet else 0}

previous_tests.append(current_test)
import_json_dict["session"]["previous_tests"] = previous_tests

if not quiet:
    for dummy in import_json_dict["session"]["previous_tests"]:
        if dummy["test_name"] == "printing speed":
            import_json_dict["settings"]["speed_printing"] = dummy["selected_value"]
        elif dummy["test_name"] == "path height":
            import_json_dict["settings"]["path_height"] = dummy["selected_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "first layer height":
            import_json_dict["settings"]["path_height_raft"] = dummy["selected_value"]
            import_json_dict["settings"]["speed_printing_raft"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "path width":
            import_json_dict["settings"]["path_width"] = dummy["selected_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "extrusion temperature":
            import_json_dict["settings"]["temperature_extruder"] = dummy["selected_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "extrusion multiplier":
            import_json_dict["settings"]["extrusion_multiplier"] = dummy["selected_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]
        elif dummy["test_name"] == "retraction distance":
            import_json_dict["settings"]["retraction_distance"] = dummy["selected_value"]
            import_json_dict["settings"]["speed_printing"] = dummy["selected_speed_value"]

    import_json_dict["settings"]["critical_overhang_angle"] = round(np.rad2deg(np.arctan(2*import_json_dict["settings"]["path_height"]/import_json_dict["settings"]["path_width"])),0)
    with open(cwd + separator("jsons") + material.manufacturer + " " + material.name + " " + "{:.0f}".format(machine.nozzle.size_id*1000) + " um" + ".json", mode="w") as file:
        output = json.dumps(import_json_dict, indent=4, sort_keys=False)
        file.write(output)

    # exclusive_write(cwd + separator("jsons") + material.manufacturer + " " + material.name + " " + "{:.0f}".format(machine.nozzle.size_id*1000) + " um" + ".json", json.dumps(import_json_dict, indent=4, sort_keys=False), limit=True)

with open(cwd + separator() + "persistence.json", mode="w") as file:
    output = json.dumps(import_json_dict, indent=4, sort_keys=False)
    file.write(output)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')
