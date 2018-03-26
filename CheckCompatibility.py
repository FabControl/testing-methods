# hot to implement?

def check_compatibility(machine, material):

    if abs(machine.size_extruder_id - material.size_od) > 0.2: # Stratasys patent
        # Compare the inner diameter of the liquefier with the outer diameter of the filament
        output = ("The inner diameter of the liquefier ({:0.2f} mm) is not compatible with the outer diameter of the filament ({:0.2f} mm)!"
            .format(machine.id, machine.size_extruder_id, material.size_od))
        print("Compatibility issue: " + output)


    if machine.temperature_max < material.temperature_melting:
        # Compare the 'melting/softening point' of the material and the maximum achievable temperature of the liquefier
        output = ("{} {} 3D printer is incapable of printing this material: "
                  "the melting (softening) temperature of {:0.0f} degC is higher than the maximum achievable temperature in the liquefier {:0.0f} degC!"
            .format(machine.manufacturer, machine.model, material.temperature_melting, machine.temperature_max))
        print("Compatibility issue: " + output)


    if max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft) > material.temperature_destr:
        # Compare the preset extrusion temperature and the destruction temperature:
        output = ("The set extrusion temperature of {:0.0f} degC is higher than the destruction temperature of feedstock material {:0.0f} degC"
            .format(max(machine.settings.temperature_extruder, machine.settings.temperature_extruder_raft),material.temperature_destr))
        print("Compatibility issue: " + output)