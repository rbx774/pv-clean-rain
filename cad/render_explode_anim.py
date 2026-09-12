import bpy
from pathlib import Path

OUT = Path("/workspace/pv-clean-rain/cad/explode_frames")
OUT.mkdir(parents=True, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 120
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(OUT / "frame_")
# Eevee fast
ee = getattr(scene, "eevee", None)
if ee and hasattr(ee, "taa_render_samples"):
    ee.taa_render_samples = 16
bpy.ops.render.render(animation=True)
print("FRAMES", OUT)
