"""
Headless Blender builder: PV-Clean Rain prototype v2.1
Raspberry Pi 2011.12 + GOODaaa D4004 + belly pad + soft wheels
"""
import bpy
import math
from mathutils import Vector
from pathlib import Path

OUT = Path("/workspace/pv-clean-rain/cad")
OUT.mkdir(parents=True, exist_ok=True)

# --- reset ---
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def mat(name, color, roughness=0.45, metallic=0.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metallic
    return m

MAT_CHASSIS = mat("Chassis", (0.55, 0.57, 0.60), 0.55)
MAT_WHEEL = mat("Wheel", (0.12, 0.13, 0.14), 0.7)
MAT_HUB = mat("Hub", (0.45, 0.45, 0.48), 0.35, 0.2)
MAT_PAD = mat("Pad", (0.65, 0.78, 0.88), 0.85)
MAT_PI = mat("PiGreen", (0.15, 0.45, 0.18), 0.4)
MAT_PORT = mat("Port", (0.05, 0.05, 0.05), 0.3, 0.1)
MAT_PB = mat("Powerbank", (0.08, 0.08, 0.09), 0.4)
MAT_ORANGE = mat("Accent", (0.85, 0.35, 0.08), 0.4)
MAT_SOLAR = mat("Solar", (0.05, 0.12, 0.28), 0.25, 0.3)
MAT_DRV = mat("Driver", (0.15, 0.35, 0.7), 0.4)
MAT_IR = mat("IR", (0.8, 0.15, 0.1), 0.35)
MAT_TOF = mat("ToF", (0.1, 0.7, 0.25), 0.35)
MAT_BAG = mat("Bag", (0.7, 0.85, 0.95), 0.2)
# make bag a bit glassy
bsdf = MAT_BAG.node_tree.nodes.get("Principled BSDF")
if "Alpha" in bsdf.inputs:
    bsdf.inputs["Alpha"].default_value = 0.35
MAT_BAG.blend_method = 'BLEND'

def link(obj, collection_name="Robot"):
    col = bpy.data.collections.get(collection_name)
    if col is None:
        col = bpy.data.collections.new(collection_name)
        scene.collection.children.link(col)
    if obj.name not in col.objects:
        # unlink from scene root if present
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        col.objects.link(obj)
    return obj

def add_cube(name, size, location, material=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if material:
        obj.data.materials.append(material)
    return link(obj)

def add_cylinder(name, radius, depth, location, material=None, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return link(obj)

# Units: meters. Robot ~0.25 x 0.18 x 0.12 m
# Chassis plate
chassis = add_cube("Chassis", (0.22, 0.16, 0.008), (0, 0, 0.045), MAT_CHASSIS)

# Belly pad under chassis
pad = add_cube("BellyPad", (0.14, 0.10, 0.012), (0, 0, 0.028), MAT_PAD)

# Wheels Ø80mm = 0.08m — four corners
wheel_z = 0.04
wheel_y = 0.095
wheel_xs = (-0.07, 0.07)
for i, (wx, wy) in enumerate([
    (-0.07, -0.095), (0.07, -0.095), (-0.07, 0.095), (0.07, 0.095)
]):
    w = add_cylinder(f"Wheel_{i+1}", 0.04, 0.017, (wx, wy, wheel_z), MAT_WHEEL, rotation=(math.pi/2, 0, 0))
    hub = add_cylinder(f"Hub_{i+1}", 0.012, 0.02, (wx, wy, wheel_z), MAT_HUB, rotation=(math.pi/2, 0, 0))

# Gear motors (simplified boxes near rear driven wheels)
add_cube("Motor_L", (0.055, 0.022, 0.018), (-0.07, -0.055, 0.055), MAT_PORT)
add_cube("Motor_R", (0.055, 0.022, 0.018), (0.07, -0.055, 0.055), MAT_PORT)

# TB6612 driver board
add_cube("TB6612", (0.04, 0.03, 0.006), (0.06, 0.02, 0.058), MAT_DRV)

# Raspberry Pi Model B-ish slab + ports
pi = add_cube("RaspberryPi_2011_12", (0.085, 0.056, 0.015), (-0.04, 0.0, 0.062), MAT_PI)
add_cube("Pi_USB", (0.015, 0.012, 0.01), (-0.005, -0.03, 0.062), MAT_PORT)
add_cube("Pi_USB2", (0.015, 0.012, 0.01), (0.012, -0.03, 0.062), MAT_PORT)
add_cube("Pi_Eth", (0.02, 0.014, 0.012), (-0.06, -0.03, 0.062), MAT_PORT)

# GOODaaa D4004 powerbank + solar flap
pb = add_cube("GOODaaa_D4004", (0.15, 0.08, 0.028), (0.02, 0.04, 0.085), MAT_PB)
add_cube("PB_Accent_L", (0.008, 0.08, 0.028), (-0.05, 0.04, 0.085), MAT_ORANGE)
add_cube("PB_Accent_R", (0.008, 0.08, 0.028), (0.09, 0.04, 0.085), MAT_ORANGE)
# solar flap hinged / slightly open
solar = add_cube("SolarFlap", (0.14, 0.002, 0.09), (0.02, 0.09, 0.12), MAT_SOLAR)
solar.rotation_euler = (math.radians(-55), 0, 0)

# Zip bag / shroud over electronics (thin box)
bag = add_cube("ZipBagShroud", (0.18, 0.12, 0.07), (0.0, 0.01, 0.095), MAT_BAG)

# IR sensors front down
add_cube("IR_L", (0.012, 0.012, 0.01), (-0.05, -0.07, 0.035), MAT_IR)
add_cube("IR_R", (0.012, 0.012, 0.01), (0.05, -0.07, 0.035), MAT_IR)

# Forward ToF
add_cube("VL53_ToF", (0.02, 0.012, 0.01), (0.0, -0.085, 0.055), MAT_TOF)

# Ground reference PV modules (context, separate collection)
mod_col = bpy.data.collections.new("Context_PV")
scene.collection.children.link(mod_col)
MAT_GLASS = mat("PVGlass", (0.1, 0.25, 0.35), 0.15, 0.05)
MAT_FRAME = mat("PVFrame", (0.2, 0.2, 0.22), 0.5, 0.3)

def add_module(name, x):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -0.02))
    m = bpy.context.active_object
    m.name = name
    m.scale = (0.164, 0.099, 0.004)  # approx module footprint scaled
    bpy.ops.object.transform_apply(scale=True)
    m.rotation_euler = (math.radians(16), 0, 0)
    m.data.materials.append(MAT_GLASS)
    for c in list(m.users_collection):
        c.objects.unlink(m)
    mod_col.objects.link(m)
    # frame rim as slightly larger thin cube
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -0.025))
    f = bpy.context.active_object
    f.name = name + "_Frame"
    f.scale = (0.168, 0.103, 0.008)
    bpy.ops.object.transform_apply(scale=True)
    f.rotation_euler = (math.radians(16), 0, 0)
    f.data.materials.append(MAT_FRAME)
    for c in list(f.users_collection):
        c.objects.unlink(f)
    mod_col.objects.link(f)

add_module("PV_Module_1", -0.18)
add_module("PV_Module_2", 0.02)

# Lighting + camera for preview
bpy.ops.object.light_add(type='SUN', location=(2, -2, 5))
sun = bpy.context.active_object
sun.data.energy = 3.0

bpy.ops.object.light_add(type='AREA', location=(-1, 1, 2))
area = bpy.context.active_object
area.data.energy = 40
area.scale = (2, 2, 1)

bpy.ops.object.camera_add(location=(0.45, -0.55, 0.32), rotation=(math.radians(65), 0, math.radians(40)))
cam = bpy.context.active_object
scene.camera = cam

# World
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.85, 0.88, 0.92, 1)
bg.inputs[1].default_value = 1.0

# Save .blend
blend_path = OUT / "pv_clean_rain_v21.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

# Export GLB (robot only ideally — export all is fine for first pass)
glb_path = OUT / "pv_clean_rain_v21.glb"
bpy.ops.export_scene.gltf(filepath=str(glb_path), export_format='GLB')

# Render preview
scene.render.engine = "BLENDER_EEVEE_NEXT"
# Blender 4.3 uses EEVEE_NEXT
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.cycles.samples = 32

scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.filepath = str(OUT / "pv_clean_rain_v21_preview.png")
bpy.ops.render.render(write_still=True)

print("WROTE", blend_path)
print("WROTE", glb_path)
print("WROTE", scene.render.filepath)
