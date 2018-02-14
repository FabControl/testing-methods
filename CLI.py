"""
MP MT Framework.

Usage:
    CLI.py
"""
from Calculations import shear_rate, pressure_drop, rheology
from CheckCompatibility import check_compatibility
from Definitions import *
from OptimizeSettings import check_printbed_temperature, check_printing_speed_shear_rate, check_printing_speed_pressure
from Plotting import plotting_mfr
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
import time
from Globals import machine, material, import_json_dict

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
        else:
            pass

    check_printing_speed_shear_rate(machine, gamma_dot_out)
    check_printing_speed_pressure(machine, material, delta_p_out, param_power_law)

else:
    pass

if import_json_dict["session"]["test_type"] == "A":
    test = 'path height' # 'retraction distance' 'path height' 'extrusion temperature' 'retraction restart distance and coasting distance' 'extrusion temperature', 'first layer height', 'path height', 'path width', 'printing speed', 'extrusion multiplier', 'retraction distance', 'retraction restart distance and coasting distance'
    min_max_argument = [0.3, 0.6]
    min_max_speed_printing = [30, 75]  # check the jerk value


    from DefinitionsTestsA import flat_test_single_parameter_vs_speed_printing, flat_test_single_parameter, retraction_restart_distance_vs_coasting_distance, retraction_distance

    if test == 'retraction distance':
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path, min_max_argument = min_max_argument, min_max_speed_printing = min_max_speed_printing, raft = True)
        retraction_distance(ts)
    elif test == 'retraction restart distance and coasting distance':
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path, min_max_argument = min_max_argument, min_max_speed_printing = min_max_speed_printing, raft = True)
        retraction_restart_distance_vs_coasting_distance(ts)
    else:
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path, min_max_argument = min_max_argument, min_max_speed_printing = min_max_speed_printing, raft = True)
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

    ts = TestSetupB(machine, material, test, path, min_max_argument, min_max_speed_printing, raft = True)
    dimensional_test(ts)

# Add a step for selecting/approving of the result TODO
## Working with buffered content
previous_tests = import_json_dict["session"]["previous_tests"]
current_test = {"test_name": ts.test_name, "tested_values": ts.values, "selected_value": 0, "units": ts.units}
previous_tests.append(current_test)
import_json_dict["session"]["previous_tests"] = previous_tests

with open("persistence.json", mode="w") as file:
    output = json.dumps(import_json_dict, indent=4, sort_keys=True)
    file.write(output)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')