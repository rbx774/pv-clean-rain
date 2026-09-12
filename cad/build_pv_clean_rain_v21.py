"""
PV-Clean Rain v2.1 — dimensionally sharpened Blender model + exploded animation.
Units: meters. Sources: Stückliste/Bauplan (chassis ~200×150, wheels Ø80×17,
Pi Model B ~85.6×56.5, modules 1640×992×40, gaps ~20 mm, tilt 16°).
D4004 size estimated from typical rugged 25Ah pack (~165×85×30 mm).
"""
from __future__ import annotations

import math
from pathlib import Path

import bpy
from mathutils import Vector

OUT = Path("/workspace/pv-clean-rain/cad")
OUT.mkdir(parents=True, exist_ok=True)

# --- mm helpers ---
def mm(v):
    return v / 1000.0

# --- reset ---
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0

# --- materials ---

def mat(name, color, roughness=0.45, metallic=0.0, alpha=1.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metallic
    if alpha < 1.0 and "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
    return m


MAT_CHASSIS = mat("Chassis", (0.55, 0.57, 0.60), 0.55)
MAT_WHEEL = mat("Wheel", (0.12, 0.13, 0.14), 0.75)
MAT_HUB = mat("Hub", (0.5, 0.5, 0.52), 0.35, 0.25)
MAT_PAD = mat("Pad", (0.65, 0.78, 0.88), 0.85)
MAT_PI = mat("PiGreen", (0.12, 0.42, 0.16), 0.4)
MAT_PORT = mat("Port", (0.05, 0.05, 0.05), 0.3)
MAT_PB = mat("Powerbank", (0.07, 0.07, 0.08), 0.4)
MAT_ORANGE = mat("Accent", (0.9, 0.38, 0.08), 0.4)
MAT_SOLAR = mat("Solar", (0.04, 0.1, 0.25), 0.22, 0.35)
MAT_DRV = mat("Driver", (0.12, 0.32, 0.65), 0.4)
MAT_IR = mat("IR", (0.85, 0.12, 0.08), 0.35)
MAT_TOF = mat("ToF", (0.08, 0.65, 0.22), 0.35)
MAT_BAG = mat("Bag", (0.7, 0.85, 0.95), 0.15, alpha=0.35)
MAT_GLASS = mat("PVGlass", (0.08, 0.22, 0.32), 0.12, 0.05)
MAT_FRAME = mat("PVFrame", (0.18, 0.18, 0.2), 0.5, 0.35)
MAT_MOTOR = mat("Motor", (0.25, 0.35, 0.55), 0.4, 0.15)


def robot_col():
    c = bpy.data.collections.get("Robot")
    if not c:
        c = bpy.data.collections.new("Robot")
        scene.collection.children.link(c)
    return c


def ctx_col():
    c = bpy.data.collections.get("Context_PV")
    if not c:
        c = bpy.data.collections.new("Context_PV")
        scene.collection.children.link(c)
    return c


def link(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def add_cube(name, size_xyz, location, material, col, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size_xyz
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(material)
    return link(obj, col)


def add_cyl(name, radius, depth, location, material, col, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    return link(obj, col)


R = robot_col()
C = ctx_col()

# Empty root for whole robot (assembled pose at origin)
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, mm(40)))
root = bpy.context.active_object
root.name = "RobotRoot"
link(root, R)

parts = {}  # name -> (obj, assembled_loc, explode_offset)


def register(obj, explode_offset):
    obj.parent = root
    # store local location as assembled
    parts[obj.name] = (obj, obj.location.copy(), Vector(explode_offset))
    return obj


# --- Chassis 200×150×8 mm ---
chassis = add_cube(
    "Chassis",
    (mm(200), mm(150), mm(8)),
    (0, 0, 0),
    MAT_CHASSIS,
    R,
)
register(chassis, (0, 0, mm(40)))

# --- Belly pad ~140×100×12 ---
pad = add_cube(
    "BellyPad",
    (mm(140), mm(100), mm(12)),
    (0, 0, mm(-14)),
    MAT_PAD,
    R,
)
register(pad, (0, 0, mm(-50)))

# --- Wheels Ø80 × 17 mm ---
wheel_r = mm(40)
wheel_w = mm(17)
# track: wheels outside chassis width 150 → centers at y=±(75+8.5)≈±83.5
wy = mm(83.5)
wx = mm(70)
wz = mm(-5)  # axle near bottom of chassis
for i, (x, y) in enumerate(
    [(-wx, -wy), (wx, -wy), (-wx, wy), (wx, wy)]
):
    w = add_cyl(
        f"Wheel_{i+1}",
        wheel_r,
        wheel_w,
        (x, y, wz),
        MAT_WHEEL,
        R,
        rotation=(math.pi / 2, 0, 0),
    )
    register(w, (x * 0.15, y * 0.35, mm(-35)))
    h = add_cyl(
        f"Hub_{i+1}",
        mm(12),
        mm(20),
        (x, y, wz),
        MAT_HUB,
        R,
        rotation=(math.pi / 2, 0, 0),
    )
    register(h, (x * 0.15, y * 0.35, mm(-30)))

# --- TT motors ~70×22×18 near rear wheels ---
for name, x in (("Motor_L", -wx), ("Motor_R", wx)):
    m = add_cube(
        name,
        (mm(70), mm(22), mm(18)),
        (x, mm(-45), mm(12)),
        MAT_MOTOR,
        R,
    )
    register(m, (x * 0.2, mm(-40), mm(25)))

# --- TB6612 ~21×21×4 ---
drv = add_cube(
    "TB6612",
    (mm(21), mm(21), mm(4)),
    (mm(55), mm(20), mm(14)),
    MAT_DRV,
    R,
)
register(drv, (mm(80), mm(40), mm(70)))

# --- Raspberry Pi Model B 85.6 × 56.5 × 15 ---
pi = add_cube(
    "RaspberryPi_2011_12",
    (mm(85.6), mm(56.5), mm(15)),
    (mm(-35), 0, mm(20)),
    MAT_PI,
    R,
)
register(pi, (mm(-90), mm(-60), mm(110)))
# ports
for pname, loc in (
    ("Pi_USB1", (mm(-10), mm(-32), mm(20))),
    ("Pi_USB2", (mm(8), mm(-32), mm(20))),
    ("Pi_Eth", (mm(-50), mm(-33), mm(20))),
):
    p = add_cube(pname, (mm(15), mm(12), mm(10)), loc, MAT_PORT, R)
    register(p, (mm(-90), mm(-90), mm(110)))

# --- GOODaaa D4004 ~165×85×30 + solar flap ---
pb = add_cube(
    "GOODaaa_D4004",
    (mm(165), mm(85), mm(30)),
    (mm(25), mm(25), mm(42)),
    MAT_PB,
    R,
)
register(pb, (mm(100), mm(70), mm(150)))
for aname, ax in (("PB_Accent_L", mm(-52)), ("PB_Accent_R", mm(102))):
    a = add_cube(aname, (mm(8), mm(85), mm(30)), (ax, mm(25), mm(42)), MAT_ORANGE, R)
    register(a, (mm(100), mm(70), mm(150)))

solar = add_cube(
    "SolarFlap",
    (mm(155), mm(2), mm(100)),
    (mm(25), mm(70), mm(70)),
    MAT_SOLAR,
    R,
)
solar.rotation_euler = (math.radians(-50), 0, 0)
register(solar, (mm(100), mm(120), mm(200)))

# --- Zip bag shroud covering electronics ~180×120×55 ---
bag = add_cube(
    "ZipBagShroud",
    (mm(180), mm(120), mm(55)),
    (0, mm(10), mm(48)),
    MAT_BAG,
    R,
)
register(bag, (0, 0, mm(220)))

# --- IR TCRT-ish 20×10×8 front underside ---
for name, x in (("IR_L", mm(-45)), ("IR_R", mm(45))):
    ir = add_cube(name, (mm(20), mm(10), mm(8)), (x, mm(-70), mm(-6)), MAT_IR, R)
    register(ir, (x, mm(-100), mm(-40)))

# --- VL53 ~25×13×7 forward ---
tof = add_cube(
    "VL53_ToF",
    (mm(25), mm(13), mm(7)),
    (0, mm(-82), mm(10)),
    MAT_TOF,
    R,
)
register(tof, (0, mm(-130), mm(50)))

# --- Context: two full-size modules 1640×992×40 glass + frame, 20 mm gap, 16° ---
tilt = math.radians(16)
# place modules under robot; robot sits on module 1 center-ish
mod_w, mod_l, mod_t = mm(992), mm(1640), mm(4)
frame_h = mm(40)
gap = mm(20)
# orientation: long edge along Y for portrait-ish travel
for i, name in enumerate(("PV_Module_1", "PV_Module_2")):
    # Verlegemaß short side 1012 → module width 992 + gap 20
    x = i * (mm(992) + gap)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -frame_h / 2 - mm(2)))
    glass = bpy.context.active_object
    glass.name = name
    glass.scale = (mod_w, mod_l, mod_t)
    bpy.ops.object.transform_apply(scale=True)
    glass.rotation_euler = (tilt, 0, 0)
    glass.data.materials.append(MAT_GLASS)
    link(glass, C)

    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, -frame_h / 2 - mm(6)))
    fr = bpy.context.active_object
    fr.name = name + "_Frame"
    fr.scale = (mod_w + mm(8), mod_l + mm(8), frame_h)
    bpy.ops.object.transform_apply(scale=True)
    fr.rotation_euler = (tilt, 0, 0)
    fr.data.materials.append(MAT_FRAME)
    link(fr, C)

# Move robot root onto module surface (approx)
root.location = (0, 0, mm(8))
root.rotation_euler = (tilt, 0, 0)

# --- Animation: explode ---
scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 24

# assembled key at frame 1 & 20
# exploded at 70-100
# optional settle hold

for name, (obj, loc0, off) in parts.items():
    obj.location = loc0
    obj.keyframe_insert(data_path="location", frame=1)
    obj.keyframe_insert(data_path="location", frame=24)
    obj.location = loc0 + off
    obj.keyframe_insert(data_path="location", frame=72)
    obj.keyframe_insert(data_path="location", frame=100)
    # ease
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.easing = "EASE_IN_OUT"

# Camera
bpy.ops.object.camera_add(
    location=(0.55, -0.85, 0.45), rotation=(math.radians(62), 0, math.radians(35))
)
cam = bpy.context.active_object
cam.name = "Cam_Main"
scene.camera = cam
# slight orbit via keyframes
cam.keyframe_insert(data_path="location", frame=1)
cam.keyframe_insert(data_path="rotation_euler", frame=1)
cam.location = (0.75, -0.55, 0.55)
cam.rotation_euler = (math.radians(58), 0, math.radians(50))
cam.keyframe_insert(data_path="location", frame=120)
cam.keyframe_insert(data_path="rotation_euler", frame=120)

# Lights
bpy.ops.object.light_add(type="SUN", location=(3, -2, 6))
bpy.context.active_object.data.energy = 2.5
bpy.ops.object.light_add(type="AREA", location=(-2, 2, 3))
area = bpy.context.active_object
area.data.energy = 80
area.scale = (3, 3, 1)

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.86, 0.89, 0.93, 1)
bg.inputs[1].default_value = 1.0

# Save assembled-looking still at frame 20 later; save blend now
blend_path = OUT / "pv_clean_rain_v21.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

# GLB at exploded mid? export assembled frame 20
scene.frame_set(20)
glb_path = OUT / "pv_clean_rain_v21.glb"
bpy.ops.export_scene.gltf(filepath=str(glb_path), export_format="GLB")

# Still preview assembled
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.image_settings.file_format = "PNG"
scene.frame_set(20)
scene.render.filepath = str(OUT / "pv_clean_rain_v21_preview.png")
bpy.ops.render.render(write_still=True)

# Exploded still
scene.frame_set(80)
scene.render.filepath = str(OUT / "pv_clean_rain_v21_exploded_still.png")
bpy.ops.render.render(write_still=True)

print("SAVED", blend_path)
print("SAVED", glb_path)
print("DIMS_MM chassis=200x150x8 wheel=Dx80x17 pi=85.6x56.5x15 pb~165x85x30 module=1640x992 frameH=40 gap=20 tilt=16deg")
