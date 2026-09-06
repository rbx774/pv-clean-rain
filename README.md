# PV-Clean Rain

Minimaler, regenbasierter Reinigungsroboter für die PV-Dachanlage **Röötger (20,48 kWp, 16°)**.

Prototyp-Ziele: Teile **&lt; 200 €**, Bauch-Pad (passiv), große weiche Räder, ESP32, Kanten-Stopp ohne Fangseil, Software-Kantenpark, Klemmen umfahren.

## Dokumente

| Dokument | Inhalt |
|---|---|
| [docs/01-stueckliste.md](docs/01-stueckliste.md) | Komponenten / BOM |
| [docs/02-bauplan.md](docs/02-bauplan.md) | Aufbau & Inbetriebnahme |
| [docs/03-anforderungen-v1.md](docs/03-anforderungen-v1.md) | Anforderungen v1 |
| [assets/exploded-v2-minimal.png](assets/exploded-v2-minimal.png) | Exploded View v2 |
| [assets/pv-clean-rain-demo-v2.mp4](assets/pv-clean-rain-demo-v2.mp4) | Konzept-Demo |

## Firmware

Siehe [`firmware/`](firmware/) — PlatformIO, Serial-JSON-API (115200 Baud).

```bash
cd firmware && pio run -t upload && pio device monitor -b 115200
```

## Status

- Anforderungen & Minimaldesign akzeptiert  
- Einkaufsliste vorbereitet, **Bestellung bewusst zurückgestellt**  
- Nächster physikalischer Schritt: **Cycle A** (Rahmen/Spalt am 16°-Mock)

## Lizenz

Prototype documentation — siehe `LICENSE`.
