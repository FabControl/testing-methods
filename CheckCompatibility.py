import sys


def check_compatibility(machine, material):
    # Compare the inner diameter of the liquefier with the outer diameter of the filament:
    if abs(machine.size_extruder_id - material.size_od) > 0.2:
        output = ("3D printer %s: The inner diameter of the liquefier (%.1f mm) is not compatible with the outer diameter of the filament (%.1f mm)!" % (
            machine.id, 1000 * machine.size_extruder_id, 1000 * material.size_od))
        sys.exit("Compatibility issue: " + output)
    else:
        pass

    # Compare the 'melting/softening point' of the material and the maximum achievable temperature of the liquefier:
    if machine.temperature_max < material.temperature_melting:
        output = ("%s %s 3D printer is incapable of printing this material: \nthe melting (softening) temperature is higher than the maximum achievable temperature in the liquefier!" % (
            machine.manufacturer, machine.model))
        sys.exit("Compatibility issue: " + output)
    else:
        pass

    # Compare the preset extrusion temperature and the destruction temperature:
    if max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft) > material.temperature_destr:
        output = ("The extrusion temperature is higher than the destruction temperature")
        sys.exit("Compatibility issue: " + output)
    else:
        pass