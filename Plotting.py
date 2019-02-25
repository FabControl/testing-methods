import math, os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from Definitions import minmax_temperature
from Calculations import func1, shear_rate


def plotting_mfr(material, machine, gamma_dot, visc, param_power_law, number_of_test_structures):
    fig1 = plt.figure()  # Plot viscosity

    colors = linear_gradient(start_hex='#0000ff',
                             finish_hex="#ff0000",
                             n=number_of_test_structures)  # Create a gradient color string for different lines (blue - cold, red - hot)

    # Log-log subplot
    axes1 = fig1.add_subplot(111)
    axes1.set_title('Calculated rheogram for ' + material.name + ' from ' + material.manufacturer)

    temperature_all = minmax_temperature(machine, number_of_test_structures)

    for dummy2 in range(0, number_of_test_structures):
        label = str("T = " + str(round(temperature_all[dummy2], 0)) + " degC")
        plt.loglog(gamma_dot, visc[dummy2], 'o', color=colors[dummy2], markerfacecolor='none', markevery=100, markersize=4, label=label)
        plt.loglog(gamma_dot, func1(gamma_dot, *param_power_law[dummy2]), '-', color=colors[dummy2], markevery=100)
        plt.grid(True, which="both", ls=":")

    gamma_dot_calc = shear_rate(machine, param_power_law[int((number_of_test_structures - 1) / 2)])

    for dummy4 in range(0, 4):
        label = ['gamma_dot in cone', 'gamma_dot in nozzle', 'gamma_dot effective', 'gamma_dot_effective_raft']
        linestyles = ['--', '-.', ':', '-']
        plt.axvline(x=gamma_dot_calc[dummy4], label=label[dummy4], linestyle=linestyles[dummy4])

    plt.xlabel('shear rate (1 / s)')
    plt.ylabel('viscosity (Pa s)')
    plt.legend(loc='center left', prop={'size': 5})
    #plt.ioff()
    #plt.gcf().show()  # https://stackoverflow.com/questions/12358312/keep-plotting-window-open-in-matplotlib

    directory = 'graphs/'
    file_name = str(directory + material.manufacturer + ' ' + material.name + ' rheogram')
    plt.savefig(file_name + '.png', format='png', dpi=300)

    return


def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    return [int(hex[i:i + 2], 16) for i in range(1, 6, 2)] # Pass 16 to the integer function for change of base


def linear_gradient(start_hex, finish_hex, n):
    ''' Returns a gradient list of (n) colors between two hex colors. start_hex and finish_hex
        should be the full six-digit color string, including the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initialize a list of the output colors with the starting color
    RGB_list = []
    # Calculate a color at each evenly spaced value of t from 1 to n
    for t in range(0, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [round(int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j])) / 255, 3) for j in range(3)]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return RGB_list