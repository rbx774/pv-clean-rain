# PV-Clean Rain

Minimaler, regenbasierter Reinigungsroboter für die PV-Dachanlage **Röötger (20,48 kWp, 16°)**.

## Prototyp v2.1 (aktuell)

| Rolle | Teil | Status |
|---|---|---|
| Rechner | **Raspberry Pi 2011.12** | vorrätig (statt ESP32) |
| Energie | **GOODaaa D4004** 25 000 mAh + Solar | vorrätig · Pi an **Out2 5 V/2,1 A** |
| Mechanik | Bauch-Pad, Ø≥80 mm Softwheels, TB6612, IR+ToF | Zukauf &lt; 200 € |

## Dokumente

| Dokument | Inhalt |
|---|---|
| [docs/01-stueckliste.md](docs/01-stueckliste.md) | Komponenten / BOM |
| [docs/02-bauplan.md](docs/02-bauplan.md) | Aufbau Pi + D4004 |
| [docs/03-anforderungen-v1.md](docs/03-anforderungen-v1.md) | Anforderungen v1 |
| [assets/exploded-v2.1-pi-d4004.png](assets/exploded-v2.1-pi-d4004.png) | Exploded View v2.1 (Pi + D4004) |
| [assets/powerbank-goodaaa-d4004.jpg](assets/powerbank-goodaaa-d4004.jpg) | Powerbank Foto |
| [assets/pv-clean-rain-demo-v2.mp4](assets/pv-clean-rain-demo-v2.mp4) | Konzept-Demo |

## Software

- `software/` — Python auf dem Pi (`crawl_v01.py`)  
- `firmware/` — altes ESP32-Skelett (Referenz)

## Status

- Anforderungen & Minimaldesign akzeptiert  
- Pi + Solar-Powerbank eingeplant  
- Bestellung übriger Mechanik/Sensorik noch zurückgestellt  

## Lizenz

MIT — siehe `LICENSE`.
