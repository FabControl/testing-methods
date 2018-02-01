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
    test = 'extrusion temperature'#, 'first layer height', 'path height', 'path width', 'printing speed', 'extrusion multiplier', 'retraction distance', 'retraction restart distance and coasting distance'

    from DefinitionsTestsA import flat_test_single_parameter_vs_speed_printing, flat_test_single_parameter, retraction_restart_distance_vs_coasting_distance, retraction_distance

    if test == 'retraction distance':
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path, min_max_argument = None, min_max_speed_printing = [10, 100], raft = True)
        retraction_distance(ts)
    elif test == 'retraction restart distance and coasting distance':
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path, min_max_argument = None, min_max_speed_printing = [10, 100], raft = True)
        retraction_restart_distance_vs_coasting_distance(ts)
    else:
        path = str(cwd + gcode_folder + '\\' + test + ' test'+ '.gcode')
        ts = TestSetupA(machine, material, test, path, min_max_argument = [225, 290], min_max_speed_printing = [10, 100], raft = True)
        flat_test_single_parameter_vs_speed_printing(ts)

elif import_json_dict["session"]["test_type"] == "B":
    test_dictionary = ['perimeter', 'overlap', 'path height']  # TODO
    number = 0

    from DefinitionsTestsB import dimensional_test

    for test in test_dictionary:
        number = number + 1
        if test == 'perimeter':
            path = str(cwd + gcode_folder + '\\test' + str(number) + ' ' + test + '.gcode')
            ts = TestSetupB(machine, material, test, path, None)
            dimensional_test(ts)
        elif test == 'overlap':
            path = str(cwd + gcode_folder + '\\test' + str(number) + ' ' + test + '.gcode')
            ts = TestSetupB(machine, material, test, path, None)
            dimensional_test(ts)
        elif test == 'path height':
            path = str(cwd + gcode_folder + '\\test' + str(number) + ' ' + test + '.gcode')
            ts = TestSetupB(machine, material, test, path, None)
            dimensional_test(ts)

with open("persistence.json", mode="w") as file:
    output = json.dumps(import_json_dict, indent=4, sort_keys=True)
    file.write(output)

end = time.time()
time_elapsed = end - start
print('elapsed time ' + str(round(time_elapsed, 1)) + ' s')