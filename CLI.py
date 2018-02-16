"""
MP MT Framework.

Usage:
    CLI.py
    CLI.py test [-v] [-q]
    CLI.py new-test
    CLI.py generate-report
"""

from docopt import docopt
quiet = None
verbose = None
if __name__ == '__main__':
    arguments = docopt(__doc__, version='MP Material Testing Suite')

    verbose = arguments["-v"]
    quiet = arguments["-q"]

    if arguments["generate-report"]:
        import generate_report
        quit()

from Calculations import shear_rate, pressure_drop, rheology
from CheckCompatibility import check_compatibility
from Definitions import *
from OptimizeSettings import check_printbed_temperature, check_printing_speed_shear_rate, check_printing_speed_pressure
from Plotting import plotting_mfr
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
from Globals import machine, material, import_json_dict
from CLI_helpers import evaluate
import time
import os

start = time.time()

# from session_builder import *
cwd = os.getcwd()
gcode_folder = '\\gcodes'

# Check compatibility
check_compatibility(machine, material)

# Checking some settings for better starting values
if machine.settings.optimize_temperature_printbed == True:
    check_printbed_temperature(material, machine)
else:
    pass

if machine.settings.optimize_speed_printing == True:
    # Some calculations
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
    os.system('cls' if os.name == 'nt' else 'clear')

if import_json_dict["session"]["test_type"] == "A":
    test = import_json_dict["session"]["test_name"] if quiet else input("Parameter to be tested ['first layer height', 'path height', 'path width', 'printing speed', 'extrusion multiplier', 'retraction distance', 'retraction restart distance and coasting distance']: ")  #

    min_max_argument_input = evaluate(input("Parameter range values [min, max] or None: ")) if not quiet else None
    min_max_argument = min_max_argument_input if min_max_argument_input != "" else None
    min_max_speed_printing_input = evaluate(input("Printing speed range values [min, max] or None: ")) if not quiet else None  # check the jerk value TODO
    min_max_speed_printing = min_max_speed_printing_input if min_max_speed_printing_input != "" else None

    from DefinitionsTestsA import flat_test_single_parameter_vs_speed_printing, flat_test_single_parameter, retraction_restart_distance_vs_coasting_distance, retraction_distance

    if test == 'retraction distance':
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path,
                        min_max_argument = min_max_argument,
                        min_max_speed_printing = min_max_speed_printing,
                        raft = True if import_json_dict["settings"]["raft_density"] > 0 else False)
        retraction_distance(ts)
    elif test == 'retraction restart distance and coasting distance':
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path,
                        min_max_argument = min_max_argument,
                        min_max_speed_printing = min_max_speed_printing,
                        raft = True if import_json_dict["settings"]["raft_density"] > 0 else False)
        retraction_restart_distance_vs_coasting_distance(ts)
    else:
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path,
                        min_max_argument = min_max_argument,
                        min_max_speed_printing = min_max_speed_printing,
                        raft = True if import_json_dict["settings"]["raft_density"] > 0 else False)
        flat_test_single_parameter_vs_speed_printing(ts)

elif import_json_dict["session"]["test_type"] == "B":
    test = 'temperature' # 'overlap', 'path height']  # TODO
    min_max_argument = [270, 300]
    min_max_speed_printing = [30, 75] # check the jerk value

    from DefinitionsTestsB import dimensional_test

    if test == 'perimeter':
            path = str(cwd + gcode_folder + '\\' + test + ' test' + '.gcode')
    elif test == 'overlap':
            path = str(cwd + gcode_folder + '\\' + test + ' test' + '.gcode')
    elif test == 'path height':
            path = str(cwd + gcode_folder + '\\' + test + ' test' + '.gcode')
    elif test == 'temperature':
            path = str(cwd + gcode_folder + '\\' + test + ' test' + '.gcode')

    ts = TestSetupB(machine, material, test, path,
                    min_max_argument = min_max_argument,
                    min_max_speed_printing = min_max_speed_printing,
                    raft = True if import_json_dict["settings"]["raft_density"] > 0 else False)
    dimensional_test(ts)

if not quiet:
    if not verbose:
        os.system('cls' if os.name == 'nt' else 'clear')
    print("Tested values:")
    print(ts.get_values())
    print("Printing speed values:")
    print([round(k,1) for k in np.linspace(min_max_speed_printing[0],min_max_speed_printing[1],4).tolist()])

# Add a step for selecting/approving of the result TODO
## Working with buffered content
previous_tests = import_json_dict["session"]["previous_tests"]

if ts.test_name == "printing speed": # TODO check conditions
    tested_speed_values = ts.get_values()
else:
    if min_max_speed_printing is None:
        tested_speed_values = import_json_dict["settings"]["speed_printing"]
    else:
        tested_speed_values = ts.min_max_speed_printing

if ts.test_name == "retraction distance":
    tested_speed_values = []

current_test = {"test_name": ts.test_name,
                "tested_values": ts.get_values(),
                "tested_speed_values": tested_speed_values,
                "selected_value": evaluate(input("Enter the best parameter value: ")) if not quiet else 0,
                "selected_speed_printing_value": evaluate(input("Enter the printing speed value which corresponds to the best parameter value: ")) if not quiet else 0,
                "units": ts.units}

previous_tests.append(current_test)
import_json_dict["session"]["previous_tests"] = previous_tests

with open("persistence.json", mode="w") as file:
    output = json.dumps(import_json_dict, indent=4, sort_keys=False)
    file.write(output)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')