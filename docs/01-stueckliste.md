# Stückliste — PV-Clean Rain Prototyp v2 (minimal)

**Projekt:** PV-Clean Rain  
**Zielanlage:** Röötger 20,48 kWp, 64 Module, **16°** Dachneigung (Limburg)  
**Budget:** Teile &lt; **200 €**  
**Stand:** 2026-09-06  

Anforderungen (Kurz): regenbasierte Nassreinigung (kein Wassertank), Module selbstständig überqueren, Klemmen/Lüfter umfahren, Kanten-Parken, ~1 Woche Standby auf einer Ladung, **kein** Fangseil.

Preise sind **Richtwerte** (DE-Shops). Vor Bestellung aktuelle Preise prüfen. Bestellung bewusst noch offen.

---

## A. Kernbauteile (empfohlen)

| Pos. | Komponente | Menge | Spezifikation / Hinweis | Beispiel-Bezugsquelle | ca. € |
|---:|---|---:|---|---|---:|
| 1 | Weiche Silikonräder | 4 | **Ø ≥ 80 mm**, Breite möglichst ≥ 17 mm; Nabe passend zum Motor | Botland DFRobot 80×17 mm | 8 |
| 2 | Getriebemotoren TT/SJ | 2–4 | 3–6 V, Metallgetriebe bevorzugt; 2 Antrieb + 2 Mitläufer oder 4WD | Funduinoshop / Botland SJ01·SJ02 | 9–17 |
| 3 | Motortreiber | 1 | **TB6612FNG** Dual-H-Bridge | Botland Pololu 713 | 5 |
| 4 | Mikrocontroller | 1 | **ESP32** DevKit (CP2102) | Amazon AZ-Delivery | 7 |
| 5 | IR-Kantensensoren | ≥2 | **TCRT5000**-Module (nach unten) | Amazon 10er-Pack | 5 |
| 6 | ToF-Sensor | 1 | **VL53L0X** (nach vorne, Klemmen/Hindernis) | Amazon | 8 |
| 7 | Energieversorgung | 1 | USB-Powerbank ≥10 000 mAh *oder* 2S-18650 + BMS | Amazon / Fachhandel | 15–25 |
| 8 | Breadboard + Jumper | 1 Set | Prototyp-Verdrahtung | Amazon / Conrad | 8 |
| 9 | Microfaser + Schaumstoff | 1 | Passiveiger **Bauch-Pad** (passiv, gefedert/geschäumt) | dm / Amazon | 5 |
| 10 | Regensensor (analog) | 1 | optional für Wake | Amazon | 3 |
| 11 | M3-Schrauben, Kabelbinder | 1 | Mechanik | Baumarkt | 6 |
| 12 | Schutz | 1 | Zip-Beutel / kleines IP-Gehäuse für Elektronik | Baumarkt | 3 |
| 13 | Chassis | 1 | Rechteckplatte 3D-Druck / Sperrholz / Acryl | Eigenbau | 5–15 |

**Kernsumme (Richt):** ca. **90–120 €** + Versand + Reserve bis 200 €.

---

## B. Prüfstand / Mock (Cycle A–E)

| Pos. | Teil | Menge | Zweck |
|---:|---|---:|---|
| M1 | Holzbrett mit **16°**-Auflage | 1 | Neigung |
| M2 | Leiste **~40 mm** Höhe | 1 | Modulrahmen simulieren |
| M3 | Spalt **~20 mm** | 1 | Fugenüberfahrt |
| M4 | Wasserschlauch / Gießkanne | 1 | „Regen“ |
| M5 | Klemmen-Attrappe | 1 | ToF-Ausweichen testen |

---

## C. Bewusst *nicht* in v1

- Fangseil / Tether  
- Deckel-Solar  
- zweites Wisch-Aggregat / angetriebene Scheiben  
- Bogie-Achsen (erst nach Fail von festen Rädern)  
- Saugskirt, Kamera, Cloud, Eigen-PCB  

---

## D. Software / Doku (dieses Repo)

| Inhalt | Pfad |
|---|---|
| Firmware-Skelett (Serial-JSON) | `firmware/` |
| Aufbauanleitung | `docs/02-bauplan.md` |
| Anforderungen | `docs/03-anforderungen-v1.md` |
| Exploded View | `assets/exploded-v2-minimal.png` |
| Konzept-Demo | `assets/pv-clean-rain-demo-v2.mp4` |

---

## E. Kompatibilitäts-Check vor Kauf

- [ ] Radnabe passt zur Motorwelle (DFRobot 80 mm ↔ TT/SJ-Flachwelle)  
- [ ] TB6612 VMOT zur Akkuspannung (≤ 13,5 V)  
- [ ] ESP32 3,3 V Logik ↔ TB6612 VCC 2,7–5,5 V  
- [ ] VL53L0X an 3,3 V I²C  

Wenn Räder nicht auf generische TT passen: SJ01/SJ02 laut Botland-Produktseite zum Rad kaufen.
