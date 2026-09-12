# CAD — PV-Clean Rain v2.1

Maßgeschärftes Blender-Modell + Exploded-Animation mit Bauteilnamen.

## Maße (mm)
| Teil | Maß |
|---|---|
| Chassis | 200 × 150 × 8 |
| Softwheels | Ø 80 × 17 |
| Raspberry Pi 2011.12 | 85,6 × 56,5 × 15 |
| GOODaaa D4004 (geschätzt) | ~165 × 85 × 30 |
| PV-Modul (Kontext) | 1640 × 992, Rahmen 40, Spalt 20, Neigung 16° |

## Dateien
| Datei | Inhalt |
|---|---|
| `pv_clean_rain_v21.blend` | Blender-Datei (inkl. Labels + Animation) |
| `pv_clean_rain_v21.glb` | GLB Export |
| `pv_clean_rain_v21_preview.png` | Zusammengebaut |
| `pv_clean_rain_v21_exploded_still.png` | Exploded Still |
| `pv_clean_rain_v21_explode_labeled.mp4` | **Exploded-Animation mit Bauteilnamen** |
| `pv_clean_rain_v21_explode.mp4` | Animation ohne Labels |
| `build_pv_clean_rain_v21.py` | Modell bauen |
| `add_labels_and_rerender.py` | Labels + Anim-Render |

## Neu bauen
```bash
blender --background --python cad/build_pv_clean_rain_v21.py
blender --background cad/pv_clean_rain_v21.blend --python cad/add_labels_and_rerender.py
ffmpeg -framerate 24 -i cad/explode_frames_labeled/frame_%04d.png -c:v libx264 -pix_fmt yuv420p cad/pv_clean_rain_v21_explode_labeled.mp4
```
