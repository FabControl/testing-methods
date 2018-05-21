"""
Usage:

blender -b -P stl_modifier.py <horizontal|vertical> <count> <rotation_Z> <object_path> <cwd> <maxdim>
"""
import bpy
import math
import sys
import json

argv = sys.argv
argv = argv[argv.index("--") + 1:]

max_dim_y = argv[5]
object_path = argv[3]
cwd = argv[4]
placement = {"vertical": 90, "horizontal": 0}

rotation_Z = float(argv[2])
count = int(argv[1])
orientation = argv[0]

scene = bpy.context.scene

imported_object = bpy.ops.import_mesh.stl(filepath=cwd + object_path, global_scale=0.1)  # get the stl file

dimension_Y = bpy.context.object.dimensions[1]
while (count + 1) * dimension_Y > max_dim_y * 0.1:
    count = count - 1

# Array operations
bpy.ops.object.modifier_add(type='ARRAY')
bpy.context.object.modifiers["Array"].use_relative_offset = False
bpy.context.object.modifiers["Array"].use_constant_offset = True
bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0

if orientation == "vertical":
    bpy.context.object.modifiers["Array"].constant_offset_displace[2] = 0.5
    bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 1.5
else:
    bpy.context.object.modifiers["Array"].constant_offset_displace[1] = dimension_Y + 0.5
    bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 1.2
bpy.context.object.modifiers["Array"].count = count

# Set rotation
bpy.ops.transform.rotate(value= math.radians(placement[orientation]), axis=(0, 1, 0))  # Rotate Y
bpy.ops.transform.rotate(value= math.radians(rotation_Z), axis=(0, 0, 1))  # Rotate Z

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