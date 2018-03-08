"""
Usage:

blender -b -P ISO527A_modifier.py <horizontal|vertical> <count> <rotation_Z> <cwd>
"""
import bpy
import math
import sys



argv = sys.argv
argv = argv[argv.index("--") + 1:]

object_path = "1A.stl"
cwd = argv[3]
placement = {"vertical": 90, "horizontal": 0}

rotation_Z = float(argv[2])
count = int(argv[1])
orientation = argv[0]

scene = bpy.context.scene

mesh = bpy.data.meshes.new("mesh") # make a new empty mesh
obj = bpy.data.objects.new("ISO527A", mesh) # link the mesh to an object
scene.objects.link(obj) # link the object to the scene
imported_object =  bpy.ops.import_mesh.stl(filepath=cwd + object_path, global_scale=0.1) # get the stl file
obj.select = True  # select the empty object

bpy.ops.object.modifier_add(type='ARRAY')
bpy.context.object.modifiers["Array"].use_relative_offset = False
bpy.context.object.modifiers["Array"].use_constant_offset = True

if orientation == "vertical":
    bpy.context.object.modifiers["Array"].constant_offset_displace[2] = 0.8
else:
    bpy.context.object.modifiers["Array"].constant_offset_displace[1] = 2.5
bpy.context.object.modifiers["Array"].count = count

# Set rotation
bpy.ops.transform.rotate(value= math.radians(placement[orientation]), axis=(0, 1, 0)) # Rotate Y
bpy.ops.transform.rotate(value= math.radians(rotation_Z), axis=(0, 0, 1)) # Rotate Z

# Apply modifier and ffset the geometry to center
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
bpy.context.object.location[0] = 0
bpy.context.object.location[1] = 0

# Export
bpy.ops.export_mesh.stl(filepath=cwd + "export" + ".stl",
                        check_existing=False,
                        axis_forward='Y',
                        axis_up='Z',
                        filter_glob="*.stl",
                        use_selection=True,
                        global_scale=10.0,
                        use_scene_unit=False,
                        ascii=False,
                        use_mesh_modifiers=True,
                        batch_mode='OFF')