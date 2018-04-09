import math, sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from Definitions import  minmax_temperature, minmax_path_width_height_raft


def rheology(material, machine, delta_p_out, number_of_test_structures):
    # Function to get the rheological data from the MFR data.

    try:
        mfr = material.mvr / 1000000
    except AttributeError or TypeError:
        try:
            mfr = material.mfi / 1000 / (material.density_rt * 1000 / (1 + 3 * material.lcte * (material.temperature_mfr - 20)))
        except AttributeError:
            raise ValueError("You have to specify either both MFI AND density values OR MVR values!")

    points = int(10000)  # smoothness of the curves

    # Calculation of viscosities
    try:
        delta_p = delta_p_out
    except AttributeError:
        delta_p = 20  # respect the units: bar

    # Define the range of the axes
    gamma_dot = np.logspace(-2, 4, points, base = 10)  # 1/s

    # Fitting parameters for Vinogradov's equation
    a1 = 1.380 * 10 ** (-2)  # 0.00612
    a2 = 1.462 * 10 ** (-3)  # 0.000285
    alpha = 0.355

    visc = np.zeros((number_of_test_structures, points))
    param_power_law = np.zeros((number_of_test_structures, 2))

    p_star = (1 / 2) * (material.load_mfr * 9.81) / (math.pi * ((material.capillary_diameter_mfr / 1000) / 2) ** 2) / 100000
    eta_mfr = ((1 / 8) * (material.load_mfr * 9.81 / (material.capillary_length_mfr / 1000)) * (material.time_mfr * 60 / mfr) * ((material.capillary_diameter_mfr / 1000) / 2) ** 2)

    temperature_all = minmax_temperature(material, machine, number_of_test_structures)

    for dummy1 in range(0, number_of_test_structures):
        correction = temperature_all[dummy1] - (material.temperature_glass + 43 - 0.02 * (p_star - delta_p))
        correction_mfr = material.temperature_mfr - (material.temperature_glass + 43 - 0.02 * (p_star - delta_p))

        shift = np.power(10, 8.86 * correction_mfr / (101.6 + correction_mfr) - 8.86 * correction / (101.6 + correction))
        eta_0 = eta_mfr * shift
        dummy_visc = eta_0 * np.power((1 + a1 * np.power(eta_0 * gamma_dot, alpha) + a2 * np.power(eta_0 * gamma_dot, 2 * alpha)), -1)
        visc[dummy1] = dummy_visc

        index = int(2*points/3)
        gamma_dot_fit = gamma_dot[index:]
        visc_fit = visc[dummy1]
        visc_fit = visc_fit[index:]

        dummy_param_power_law, pcov1 = curve_fit(func1, gamma_dot_fit, visc_fit)
        param_power_law[dummy1] = dummy_param_power_law

    return gamma_dot, visc, param_power_law


def shear_rate(machine, param_power_law):
    # def shear_rate(machine: Machine, material: Material, settings: Settings, nozzle: Nozzle, param_power_law):
    # Function to estimate shear deformation rates in the nozzle.

    m = param_power_law[0]  # m, proportionality coefficient (N s^n/m2)
    n = param_power_law[1]  # n, power law constant (1)
    k = 1 / n

    q_v = flow_rate(machine)

    gamma_dot_tube = 8 * (k + 3) * q_v / (math.pi * (machine.size_extruder_id) ** 3)
    gamma_dot_cone = 64 * (k + 3) * q_v / (math.pi * (machine.nozzle.size_capillary_length * math.tan(machine.nozzle.size_angle / 2) + machine.nozzle.size_id) ** 3)
    gamma_dot_nozzle = 8 * (k + 3) * q_v / (math.pi * (machine.nozzle.size_id) ** 3)
    gamma_dot_eff = 32 * q_v / (math.pi * (machine.nozzle.size_id) ** 3)

    q_v_raft = flow_rate_raft(machine)

    gamma_dot_eff_raft = 32 * q_v_raft / (math.pi * (machine.nozzle.size_id) ** 3)

    gamma_dot = [gamma_dot_tube, gamma_dot_cone, gamma_dot_nozzle, gamma_dot_eff, gamma_dot_eff_raft]

    # print(gamma_dot)
    return gamma_dot


def pressure_drop(machine, param_power_law):
    # Function to estimate maximum pressure drop in the nozzle.

    m = param_power_law[0]  # m, proportionality coefficient (N s^n/m2)
    n = param_power_law[1]  # n, power law constant (1)

    q_v = flow_rate(machine)

    multiplier = ((32 * (q_v / 10 ** 9) / (math.pi * (machine.nozzle.size_id / 1000) ** 3)) * ((3 * n + 1) /(4 * n)))**n

    delta_p_cone = m * multiplier * (2 / (3 * n * math.sin(machine.nozzle.size_angle/2))) * ((3 * math.sin(machine.nozzle.size_angle/2)) / (4 * n * (1 - math.cos(machine.nozzle.size_angle/2)) ** (2) * (1 + 2 * math.cos(machine.nozzle.size_angle/2)))) ** (n)
    delta_p_cone_capillary = m * multiplier * 1.18 * n ** (-0.7)
    delta_p_capillary = m * multiplier * 4 * (machine.nozzle.size_capillary_length / machine.nozzle.size_id)
    delta_p = (delta_p_cone + delta_p_cone_capillary + delta_p_capillary) / 10 ** 5  # total pressure drop (bar)

    tau_wall = (delta_p_capillary * (machine.nozzle.size_id / 2000) / (2 * machine.nozzle.size_capillary_length / 1000)) / 1000000  # shear stress on the wall (MPa)
    shear_stress = "the shear stress at the walls is {:.2f} MPa, the total pressure drop is {:.1f} MPa".format(tau_wall, delta_p/10)
    q_v_output = "the volumetric flow rate at the deposition speed of {:.3f} mm/s is {:.3f} mm3/s".format(machine.settings.speed_printing, q_v)
    comment = shear_stress + "\n" + q_v_output

    return delta_p, comment


def flow_rate(machine, speed_override = None):
    if speed_override is not None:
        machine.settings.speed_printing = speed_override
    if machine.settings.path_height < machine.settings.path_width / (2 - math.pi / 2):
        q_v = machine.settings.speed_printing * (machine.settings.path_height * (machine.settings.path_width - machine.settings.path_height) + math.pi * (machine.settings.path_height / 2) ** 2)
    else:
        q_v = machine.settings.speed_printing * machine.settings.path_height * machine.settings.path_width

    return q_v


def flow_rate_raft(machine):
    coef_h_raft, coef_w_raft = minmax_path_width_height_raft(machine)

    if machine.settings.path_height < machine.settings.path_width / (2 - math.pi / 2):
        q_v_raft = machine.settings.extrusion_multiplier_raft * machine.settings.speed_printing_raft * (machine.nozzle.size_id * coef_h_raft * (machine.nozzle.size_id * coef_w_raft - machine.nozzle.size_id * coef_h_raft) + math.pi * (machine.nozzle.size_id * coef_h_raft / 2) ** 2)
    else:
        q_v_raft = machine.settings.extrusion_multiplier_raft * machine.settings.speed_printing_raft * machine.nozzle.size_id * coef_h_raft * machine.nozzle.size_id * coef_w_raft

    return q_v_raft


def func1(gamma_dot, m, n):
    return m * gamma_dot ** (n - 1)


def func2(gamma_dot, m, n):
    return m * gamma_dot ** (n)