"""Add German part labels to PV-Clean Rain v2.1 and re-render explode animation."""
import math
from pathlib import Path

import bpy

OUT = Path("/workspace/pv-clean-rain/cad")
FRAMES = OUT / "explode_frames_labeled"
FRAMES.mkdir(parents=True, exist_ok=True)

scene = bpy.context.scene

# Remove old labels if re-run
for obj in list(bpy.data.objects):
    if obj.name.startswith("Label_"):
        bpy.data.objects.remove(obj, do_unlink=True)

# Mapping: object name substring / exact -> German label
LABELS = [
    ("ZipBagShroud", "Zip-Bag / Haube"),
    ("RaspberryPi_2011_12", "Raspberry Pi 2011.12"),
    ("GOODaaa_D4004", "GOODaaa D4004 + Solar"),
    ("SolarFlap", "Solar-Klappe"),
    ("TB6612", "TB6612 Motortreiber"),
    ("Chassis", "Chassis 200×150 mm"),
    ("BellyPad", "Bauch-Pad (Microfaser)"),
    ("Wheel_1", "Softwheel Ø80 mm"),
    ("Motor_L", "Getriebemotor"),
    ("IR_L", "IR-Kantensensor"),
    ("VL53_ToF", "VL53 ToF (vorne)"),
]

# Find camera for track-to
cam = scene.camera
if cam is None:
    for o in bpy.data.objects:
        if o.type == "CAMERA":
            cam = o
            break

mat = bpy.data.materials.get("LabelMat")
if mat is None:
    mat = bpy.data.materials.new("LabelMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.05, 0.08, 0.12, 1)
    bsdf.inputs["Roughness"].default_value = 0.4
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (1, 0.85, 0.2, 1)
        bsdf.inputs["Emission Strength"].default_value = 2.0
    elif "Emission" in bsdf.inputs:
        bsdf.inputs["Emission"].default_value = (1, 0.85, 0.2, 1)


def add_label(target_name, text):
    target = bpy.data.objects.get(target_name)
    if target is None:
        print("SKIP missing", target_name)
        return
    bpy.ops.object.text_add(location=(0, 0, 0))
    tobj = bpy.context.active_object
    tobj.name = f"Label_{target_name}"
    tobj.data.body = text
    tobj.data.size = 0.018  # ~18 mm tall text in world units (meters)
    tobj.data.extrude = 0.001
    tobj.data.align_x = "LEFT"
    tobj.data.align_y = "CENTER"
    if mat.name not in [m.name for m in tobj.data.materials]:
        tobj.data.materials.append(mat)
    # offset from part center
    tobj.parent = target
    tobj.location = (0.05, 0.0, 0.04)
    # face camera
    if cam:
        const = tobj.constraints.new(type="TRACK_TO")
        const.target = cam
        const.track_axis = "TRACK_Z"
        const.up_axis = "UP_Y"
    # put in Robot collection if exists
    rob = bpy.data.collections.get("Robot")
    if rob:
        for c in list(tobj.users_collection):
            c.objects.unlink(tobj)
        rob.objects.link(tobj)
    print("LABEL", target_name, "->", text)


for name, label in LABELS:
    add_label(name, label)

# Also label powerbank solar already covered; accent skip

bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "pv_clean_rain_v21.blend"))

# Quick stills
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
ee = getattr(scene, "eevee", None)
if ee and hasattr(ee, "taa_render_samples"):
    ee.taa_render_samples = 24

scene.frame_set(20)
scene.render.filepath = str(OUT / "pv_clean_rain_v21_preview.png")
bpy.ops.render.render(write_still=True)

scene.frame_set(80)
scene.render.filepath = str(OUT / "pv_clean_rain_v21_exploded_still.png")
bpy.ops.render.render(write_still=True)

# Animation
scene.render.resolution_x = 960
scene.render.resolution_y = 540
if ee and hasattr(ee, "taa_render_samples"):
    ee.taa_render_samples = 12
scene.frame_start = 1
scene.frame_end = 120
scene.render.filepath = str(FRAMES / "frame_")
bpy.ops.render.render(animation=True)
print("DONE_LABELED_FRAMES", FRAMES)
