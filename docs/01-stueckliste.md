# Stückliste — PV-Clean Rain Prototyp v2.1

**Projekt:** PV-Clean Rain  
**Zielanlage:** Röötger 20,48 kWp, 64 Module, **16°** Dachneigung  
**Budget:** Zukaufteile &lt; **200 €** (Vorratsteile zählen nicht gegen den Cap)  
**Stand:** 2026-09-12  

## Vorrat (bereits vorhanden — fest eingeplant)

| Pos. | Komponente | Spezifikation | Rolle |
|---:|---|---|---|
| V1 | **Raspberry Pi 2011.12** | Original Raspberry Pi Model B (Rev. um 2011/12) | Steuerrechner statt ESP32 |
| V2 | **GOODaaa D4004** Powerbank + Solar | 25 000 mAh; In 5 V/2,1 A; Out1 5 V/1 A; Out2 **5 V/2,1 A**; LED-Lampe | Energie + Trickle über Solarzellen |

Foto: `assets/powerbank-goodaaa-d4004.jpg`

### Hinweise Powerbank ↔ Pi
- Pi **nur** an **Output 2 (5 V / 2,1 A)** betreiben (Out1 1 A ist für den Pi unter Last oft zu schwach).
- Original-Pi hungert bei Unterspannung → kurze, dicke USB-Kabel; bei Brownouts Motorstrom vom Pi-USB **trennen** (siehe Verdrahtung).
- Solar am D4004 lädt langsam nach — passt zu Idle/~1 Woche besser als nackte Powerbank ohne Sonne; reicht nicht zum Fahren allein.

### Hinweise Raspberry Pi 2011.12
- Kein Onboard-WLAN → USB-WLAN-Stick oder Ethernet am Mock.
- GPIO reicht für IR + I²C (VL53) + Ansteuerung TB6612 (PWM/Digital).
- Soft-Echtzeit: Kanten-Stopp in Python/ C am Pi — für v1 OK; bei unsicherem Edge-Verhalten später optional Mini-MCU als Add-back (nicht jetzt kaufen).

---

## A. Noch zu beschaffen (Kern)

| Pos. | Komponente | Menge | Spezifikation | ca. € |
|---:|---|---:|---|---:|
| 1 | Weiche Silikonräder | 4 | Ø ≥ 80 mm | 8 |
| 2 | Getriebemotoren TT/SJ | 2–4 | 3–6 V | 9–17 |
| 3 | Motortreiber **TB6612FNG** | 1 | Dual-H-Bridge, VMOT aus separatem 5–6 V-Zweig oder gleichem Akku-Pfad mit Filter | 5 |
| 4 | IR-Kantensensoren TCRT5000 | ≥2 | nach unten | 5 |
| 5 | VL53L0X ToF | 1 | nach vorne | 8 |
| 6 | Microfaser + Schaum | 1 | Bauch-Pad | 5 |
| 7 | Regensensor (analog) | 1 | optional Wake | 3 |
| 8 | Breadboard / Jumper / Level | 1 | Pi 3,3 V-Logik beachten | 8 |
| 9 | M3 / Kabelbinder / Chassis-Haube | 1 | | 6 |
| 10 | Chassis | 1 | Sperrholz/3D-Druck | 5–15 |
| 11 | USB-WLAN-Stick (falls kein LAN) | 0–1 | nur wenn Remote nötig | 8–15 |
| 12 | microSD mit Raspberry Pi OS (Legacy/Light) | 1 | falls nicht vorhanden | 0–12 |

**Zukauf-Richtwert:** weiterhin klar unter **200 €** (Pi + Powerbank = 0 € Zukauf).

---

## B. Bewusst nicht in v1

- ESP32 (ersetzt durch vorhandenen Pi)  
- Extra-Akkupack / Hot-Swap  
- Fangseil, Saugskirt, Bogie, zweites Wischaggregat, Kamera, Cloud  

---

## C. Prüfstand

Unverändert: 16°-Mock, 40 mm-Leiste, 20 mm-Spalt, Wasserschlauch, Klemmen-Attrappe.

---

## D. Repo-Inhalte

| Pfad | Inhalt |
|---|---|
| `docs/02-bauplan.md` | Aufbau mit Pi + D4004 |
| `docs/03-anforderungen-v1.md` | Anforderungen |
| `firmware/` | bisher ESP32-Skelett — Migration auf Pi folgt (`software/` geplant) |
