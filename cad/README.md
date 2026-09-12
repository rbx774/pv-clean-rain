# CAD — PV-Clean Rain v2.1

Blender 4.3 Modell (blocky first pass), gebaut auf meinem Computer.

| Datei | Inhalt |
|---|---|
| `pv_clean_rain_v21.blend` | Editierbare Blender-Datei |
| `pv_clean_rain_v21.glb` | GLB-Export (Viewer / Web) |
| `pv_clean_rain_v21_preview.png` | Render-Vorschau |
| `build_pv_clean_rain_v21.py` | Headless-Build-Skript |

## Enthalten
- Chassis, Bauch-Pad, 4× Ø80-mm-Räder, Motoren
- Raspberry Pi 2011.12 (Block), GOODaaa D4004 + Solar-Klappe
- TB6612, IR, ToF, Zip-Bag-Haube
- Kontext: 2 PV-Module bei 16°

## Neu bauen
```bash
blender --background --python cad/build_pv_clean_rain_v21.py
```
