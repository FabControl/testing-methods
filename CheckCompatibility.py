from CLI_helpers import exception_handler


def check_compatibility(machine, material):

    # if abs(machine.nozzle.size_extruder_id - material.size_od) > 0.2: # Stratasys patent
    #     # Compare the inner diameter of the liquefier with the outer diameter of the filament
    #     output = ("The inner diameter of the liquefier ({:0.2f} mm) is not compatible with the outer diameter of the filament ({:0.2f} mm)!"
    #         .format(machine.id, machine.nozzle.size_extruder_id, material.size_od))
    #     exception_handler("Compatibility issue: " + output, fatal=True)

    temperature_limit = []

    if material.temperature_melting is not None:
        temperature_limit.append(material.temperature_melting)
    if material.temperature_glass is not None:
        temperature_limit.append(material.temperature_glass)

    if machine.temperaturecontrollers.extruder.temperature_max < max(temperature_limit):
        # Compare the 'melting/softening point' of the material and the maximum achievable temperature of the liquefier
        output = ("{} {} 3D printer is incapable of printing this material:\n the melting (glass transition or softening) temperature of {:0.0f} degC is higher than the maximum achievable temperature in the liquefier {:0.0f} degC!"
            .format(machine.manufacturer, machine.model, max(temperature_limit), machine.temperaturecontrollers.extruder.temperature_max))
        exception_handler("Compatibility issue: " + output, fatal=True)

    # if max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft) > material.temperature_destr:
    #     # Compare the preset extrusion temperature and the destruction temperature:
    #     output = ("The set extrusion temperature of {:0.0f} degC is higher than the destruction temperature of feedstock material {:0.0f} degC"
    #         .format(max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft),material.temperature_destr))
    #     print("Compatibility issue: " + output)
    #     quit()

    if machine.temperaturecontrollers.printbed.printbed_heatable:
        if machine.temperaturecontrollers.printbed.temperature_printbed_setpoint > machine.temperaturecontrollers.printbed.temperature_max:
            # Compare the preset extrusion temperature and the destruction temperature:
            output = ("The set printbed temperature of {:0.0f} degC is higher than the maximum achievable printbed temperature of {:0.0f} degC"
                .format(machine.temperaturecontrollers.printbed.temperature_printbed_setpoint,machine.temperaturecontrollers.printbed.temperature_max))
            exception_handler("Compatibility issue: " + output, fatal=True)

    if machine.temperaturecontrollers.printbed.printbed_heatable:
        if machine.temperaturecontrollers.printbed.temperature_printbed_setpoint > machine.temperaturecontrollers.printbed.temperature_max:
            # Compare the preset extrusion temperature and the destruction temperature:
            output = ("The set printbed temperature of {:0.0f} degC is higher than the maximum achievable printbed temperature of {:0.0f} degC"
                .format(machine.temperaturecontrollers.printbed.temperature_printbed_setpoint,machine.temperaturecontrollers.printbed.temperature_max))
            exception_handler("Compatibility issue: " + output, fatal=True)