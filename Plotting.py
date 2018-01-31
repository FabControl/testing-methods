import math, os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from Definitions import minmax_temperature
from Calculations import func1, shear_rate


def plotting_mfr(material, machine, gamma_dot, visc, param_power_law):
    fig1 = plt.figure()  # Plot viscosity

    colors = linear_gradient(start_hex='#0000ff', finish_hex="#ff0000",
                             n=machine.settings.number_of_test_structures)  # Create a gradient color string for different lines (blue - cold, red - hot)

    # Log-log subplot
    axes1 = fig1.add_subplot(111)
    axes1.set_title('Calculated rheogram for ' + material.name + ' from ' + material.manufacturer)

    # Major and minor ticks controls
    #majorLocator = MultipleLocator(500)
    #majorFormatter = FormatStrFormatter('%.0f')
    #minorLocator = MultipleLocator(250)
    #minorFormatter = FormatStrFormatter('%.0f')

    #axes1.xaxis.set_major_locator(majorLocator)
    #axes1.xaxis.set_major_formatter(majorFormatter)
    # axes1.get_xaxis().get_major_formatter().labelOnlyBase = False

    temperature_all = minmax_temperature(material, machine)

    for dummy2 in range(0, machine.settings.number_of_test_structures):
        label = str("T = " + str(round(temperature_all[dummy2], 0)) + " degC")
        plt.loglog(gamma_dot, visc[dummy2], 'o', color=colors[dummy2], markerfacecolor='none', markevery=100, markersize=4, label=label)
        plt.loglog(gamma_dot, func1(gamma_dot, *param_power_law[dummy2]), '-', color=colors[dummy2], markevery=100)
        plt.grid(True, which="both", ls=":")

    #plt.ylabel('viscosity (Pa s)')

    # # Normal subplot
    # axes2 = fig1.add_subplot(212)
    #
    # # Major and minor ticks controls
    # #x_majorLocator = MultipleLocator(1000)
    # x_majorFormatter = FormatStrFormatter('%.0f')
    # x_minorLocator = MultipleLocator(500)
    # # x_minorFormatter = FormatStrFormatter('%.0f')
    #
    # #axes2.xaxis.set_major_locator(x_majorLocator)
    # #axes2.xaxis.set_major_formatter(x_majorFormatter)
    # #axes2.xaxis.set_minor_locator(x_minorLocator)
    # # axes2.xaxis.set_minor_formatter(x_minorFormatter)
    #
    # #y_majorLocator = MultipleLocator(1000)
    # y_majorFormatter = FormatStrFormatter('%.0f')
    # #y_minorLocator = MultipleLocator(500)
    # y_minorFormatter = FormatStrFormatter('%.0f')
    #
    # #axes2.yaxis.set_major_locator(y_majorLocator)
    # axes2.yaxis.set_major_formatter(y_majorFormatter)
    # #axes2.yaxis.set_minor_locator(y_minorLocator)
    # # axes2.yaxis.set_minor_formatter(y_minorFormatter)
    #
    # for dummy3 in range(0, machine.settings.number_of_test_structures):
    #     label = str("T = " + str(round(temperature_all[dummy3], 0)) + " degC")
    #     plt.plot(gamma_dot, visc[dummy3], 'o', color=colors[dummy3], markerfacecolor='none', markevery=100,
    #              markersize=4, label=label)
    #     plt.plot(gamma_dot, func1(gamma_dot, *param_power_law[dummy3]), '-', color=colors[dummy3], markevery=100)
    #     plt.grid(True, which="both", ls=":")

    gamma_dot_calc = shear_rate(machine, param_power_law[int((machine.settings.number_of_test_structures - 1) / 2)])

    for dummy4 in range(0, 5):
        label = ['gamma_dot in tube', 'gamma_dot in cone', 'gamma_dot in nozzle', 'gamma_dot effective', 'gamma_dot_effective_raft']
        linestyles = ['-', '--', '-.', ':', '-']
        plt.axvline(x=gamma_dot_calc[dummy4], label=label[dummy4], linestyle=linestyles[dummy4])

    plt.xlabel('shear rate (1 / s)')
    plt.ylabel('viscosity (Pa s)')
    plt.legend(loc='center left', prop={'size': 5})
    #plt.ioff()
    #plt.gcf().show()  # https://stackoverflow.com/questions/12358312/keep-plotting-window-open-in-matplotlib

    directory = 'graphs/'
    file_name = str(directory + material.manufacturer + ' ' + material.name + ' rheogram')
    plt.savefig(file_name + '.png', format='png', dpi=300)

###############################################
    fig2 = plt.figure()  # Plot storage modulus

    storage_modulus = visc * gamma_dot / 1000000
    dummy = storage_modulus.shape
    stress = np.zeros((machine.settings.number_of_test_structures, dummy[1]))

    axes1 = fig2.add_subplot(211)
    axes1.set_title('Calculated storage modulus for ' + material.name + ' from ' + material.manufacturer)

    # Major and minor ticks controls:
    majorLocator = MultipleLocator(1000)
    majorFormatter = FormatStrFormatter('%.0f')
    minorLocator = MultipleLocator(500)
    minorFormatter = FormatStrFormatter('%.0f')
    axes1.xaxis.set_major_locator(majorLocator)
    axes1.xaxis.set_major_formatter(majorFormatter)
    axes1.get_xaxis().get_major_formatter().labelOnlyBase = False

    for dummy5 in range(0, machine.settings.number_of_test_structures):
        label = str("T = " + str(round(temperature_all[dummy5],0)) + " degC")
        plt.loglog(gamma_dot, storage_modulus[dummy5],
                   'o', color=colors[dummy5], markerfacecolor='none', markevery=100, markersize=4, label=label)
        plt.grid(True, which="both", ls=":")

    plt.xlabel('shear rate (1 / s)')
    plt.ylabel('storage modulus (MPa)')

    axes2 = fig2.add_subplot(212)
    axes2.xaxis.set_major_locator(majorLocator)
    axes2.xaxis.set_major_formatter(majorFormatter)
    axes2.xaxis.set_minor_locator(minorLocator)

    for dummy6 in range(0,  machine.settings.number_of_test_structures):
        m = param_power_law[dummy6, 0]  # m, proportionality coefficient (N s^n/m2)
        n = param_power_law[dummy6, 1]  # n, power law constant (1)
        dummy_stress = m * gamma_dot**(n)
        stress[dummy6] = dummy_stress

    for dummy7 in range(0, machine.settings.number_of_test_structures):
        label = str("T = " + str(round(temperature_all[dummy7],0)) + " degC")
        plt.plot(stress[dummy7]/1000000, storage_modulus[dummy7],
                 'o', color=colors[dummy7], markerfacecolor='none', markevery=100, markersize=4, label=label)
        plt.grid(True, which="both", ls=":")

    plt.xlabel('shear stress (MPa)')
    plt.ylabel('storage modulus (MPa)')
    plt.legend(loc='right', prop={'size': 5})
    #plt.ioff()
    #plt.gcf().show()  # https://stackoverflow.com/questions/12358312/keep-plotting-window-open-in-matplotlib

    directory = 'graphs/'
    file_name = str(directory + material.manufacturer + ' ' + material.name + ' storage modulus')
    # plt.savefig(file_name + '.png', format='png', dpi=300)

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