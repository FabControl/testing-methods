from CLI_helpers import exception_handler


def check_compatibility(machine, material):

    # if abs(machine.nozzle.size_extruder_id - material.size_od) > 0.2: # Stratasys patent
    #     # Compare the inner diameter of the liquefier with the outer diameter of the filament
    #     output = ("The inner diameter of the liquefier ({:0.2f} mm) is not compatible with the outer diameter of the filament ({:0.2f} mm)!"
    #         .format(machine.id, machine.nozzle.size_extruder_id, material.size_od))
    #     exception_handler("Compatibility issue: " + output, fatal=True)


    if machine.temperature_extruder_max < material.temperature_melting:
        # Compare the 'melting/softening point' of the material and the maximum achievable temperature of the liquefier
        output = ("{} {} 3D printer is incapable of printing this material: "
                  "the melting (softening) temperature of {:0.0f} degC is higher than the maximum achievable temperature in the liquefier {:0.0f} degC!"
            .format(machine.manufacturer, machine.model, material.temperature_melting, machine.temperature_extruder_max))
        exception_handler("Compatibility issue: " + output, fatal=True)


    # if max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft) > material.temperature_destr:
    #     # Compare the preset extrusion temperature and the destruction temperature:
    #     output = ("The set extrusion temperature of {:0.0f} degC is higher than the destruction temperature of feedstock material {:0.0f} degC"
    #         .format(max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft),material.temperature_destr))
    #     print("Compatibility issue: " + output)
    #     quit()

    if machine.printbed.printbed_heatable:
        if machine.settings.temperature_printbed > machine.printbed.temperature_printbed_max:
            # Compare the preset extrusion temperature and the destruction temperature:
            output = ("The set printbed temperature of {:0.0f} degC is higher than the maximum achievable printbed temperature of {:0.0f} degC"
                .format(machine.settings.temperature_printbed,machine.printbed.temperature_printbed_max))
            exception_handler("Compatibility issue: " + output, fatal=True)
