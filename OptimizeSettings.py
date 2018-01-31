import math
from Calculations import flow_rate


def check_printing_speed_shear_rate(machine, gamma_dot):
    gamma_dot_out = [0, 0]
    del gamma_dot[-1:]
    gamma_dot_out[0] = max(gamma_dot)  # max shear rate in the polymer melt going through the given nozzle (with the set path width, path height, printing speed)
    output = ('maximum shear rate in the nozzle is %.3f 1/s' % (gamma_dot_out[0]))
    print(output)

    gamma_dot_out[1] = machine.settings.speed_printing / machine.settings.path_height  # shear rate in the polymer melt during bonding (constant path height and printing speed)
    output = ('maximum shear rate during bonding is %.3f 1/s' % (gamma_dot_out[1]))
    print(output)

    q_v = flow_rate(machine)

    # Suggest another printing speed:
    if gamma_dot_out[1] > gamma_dot_out[0]:
        output = ("With the current path height value of %.2f mm, the printing speed should be around %.2f mm/s!" % (
            machine.settings.path_height,
            int(round(machine.settings.path_height * gamma_dot_out[0]))))
        print(output)

        machine.settings.speed_printing = round(machine.settings.path_height * gamma_dot_out[0], 3)

        output = ("maximum printing speed (mine): %.2f mm/s, maximum printing speed (Crocket): %.2f mm/s!" % (
            round(machine.settings.path_height * gamma_dot_out[0], 3),
            round(q_v * math.pi / (machine.settings.path_height) ** 2, 3)))
        print(output)
        print('--> printing_speed optimized! (shear rate)')
    else: pass

    return


def check_printing_speed_pressure(machine, material, delta_p, param_power_law):
    str = ('total pressure drop in liquefier and nozzle is %.1f bar' % (round(delta_p, 3)))
    print(str)

    force = (delta_p * 100000) * math.pi * (machine.size_extruder_id / 2000) ** 2  # the force on the filament (N)
    force2 = (0.5 * material.density_rt * 1000 * (machine.settings.speed_printing/1000)**2 + delta_p * 100000) * (machine.size_extruder_id/1000)**2 * (math.pi / 4) # the force on the filament (N)
    force_max = 2 * (machine.moment_max / 10) / (machine.gear_size_od / 2000)  # TODO: check machine.moment_max value!!!
    print(force)
    print(force2)
    print(force_max)

    output = ('actual tangential force on the gears is %.1f N, maximum allowed tangential force of the gears is %.1f N' % (
            round(force2, 3),
            round(force_max, 3)))
    print(output)

    parameters = (param_power_law[int(len(param_power_law)/ 2)])

    print(feeder_speed(machine, material))

    # Suggest another printing speed:
    if force2 > force_max:
        output = ('filament is likely to slip! maximum printing speed should be below %.2f mm/s!' % (
               force_max / (0.5 * material.density_rt * flow_rate(machine) * 10**(-6))))
        print(output)
        machine.settings.speed_printing = round(machine.settings.speed_printing * (flow_rate(machine)/flow_rate(machine,  machine.settings.speed_printing))**(parameters[1]), 2)
        print('--> printing_speed optimized! (pressure)')
    else: pass

    return


def check_path_height(machine, gamma_dot):
    gamma_dot_nozzle = max(gamma_dot)  # max shear rate in the polymer melt going through the given nozzle (with the set path width, path height, printing speed)
    output = ('maximum shear rate in nozzle is %.3f 1/s' % (gamma_dot_nozzle))
    print(output)

    gamma_dot_bonding = machine.settings.speed_printing / machine.settings.path_height  # shear rate in the polymer melt during bonding (constant path height and printing speed)
    output = ('maximum shear rate during bonding is %.3f 1/s' % (gamma_dot_bonding))
    print(output)

    q_v = flow_rate(machine)

    # Suggest another printing speed:
    if gamma_dot_bonding > gamma_dot_nozzle:
        output = ("for printing speed value of %.2f mm/s the path height should be below %.2f mm!" % (
            machine.settings.speed_printing,
            round(gamma_dot_nozzle * machine.settings.path_height, 2)))
        print(output)
        machine.settings.speed_printing = round(machine.settings.path_height * gamma_dot_nozzle, 3)
    else:
        pass

    output = ("maximum printing speed (mine): %.2f mm/s, maximum printing speed (Crocket): %.2f mm/s!" % (
        round(machine.settings.path_height * gamma_dot_nozzle, 2),
        round(q_v * math.pi / (machine.settings.path_height) ** 2, 2)))
    print(output)

    print('--> path_height optimized! (height)')
    return


def check_printbed_temperature(material, machine):
    # Suggest another printbed temperature
    try:
        machine.settings.temperature_printbed
    except AttributeError:
        try:
            machine.settings.temperature_printbed = material.temperature_vicat #TODO
        except AttributeError:
            machine.settings.temperature_printbed = material.temperature_glass #TODO

    if abs(machine.settings.temperature_printbed - material.temperature_vicat) > 5:
        output = ("suggested printbed temperature is %.2f degC" % (material.temperature_vicat + 5))
        print(output)
        machine.settings.temperature_printbed = material.temperature_vicat + 5
    else:
        pass

    print('--> printbed_temperature optimized!')
    return


def feeder_speed(machine, material):
    feeder_speed = machine.settings.extrusion_multiplier * (4 / math.pi) * (machine.nozzle.size_id / material.size_od)**2 * (machine.settings.path_height/machine.nozzle.size_id) * (machine.settings.path_width/machine.settings.path_height - 1 + math.pi/4) * machine.settings.speed_printing

    return feeder_speed