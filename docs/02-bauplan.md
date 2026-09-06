# Bauplan & Aufbauanleitung — PV-Clean Rain Prototyp v2

**Ziel:** Minimaler regenbasierter Dach-Crawler mit Bauch-Pad, großen weichen Rädern, ESP32, Kanten-Stopp und Software-Kantenpark.  
**Voraussetzung:** Stückliste `docs/01-stueckliste.md`  
**Sicherheitsregel:** Erste Tests **nur** am Boden-Mock (16°). Dach erst nach erfolgreichem Edge-Stopp, mit menschlicher Aufsicht.

```
        [Zip-Beutel / Haube]
                |
            [ESP32]
                |
           [Powerbank]
                |
            [TB6612]
                |
        === Chassis-Platte ===
           |             |
      [Bauch-Pad]   [4× Ø80 Räder]
           |        2× Motor (+ 2 Idler)
      IR↓  IR↓         ToF →
```

---

## 1. Werkzeug

- Schraubendreher, Seitenschneider, Heißkleber oder M3-Schrauben  
- Optional: Lötkolben (Motorleitungen), Multimeter  
- PC mit USB, PlatformIO oder Arduino-IDE (ESP32-Board-Support)

---

## 2. Mechanik aufbauen

### 2.1 Chassis
1. Rechteckplatte ca. **200 × 150 mm** (Sperrholz 4–6 mm oder 3D-Druck).  
2. Motoren links/rechts so montieren, dass die Antriebsräder die Platte seitlich tragen.  
3. Zwei weitere Räder als Mitläufer (oder zweite Motorachse bei 4WD).  
4. Schwerpunkt möglichst **mittig und tief**.

### 2.2 Räder & Rahmenüberfahrt
1. Vier weiche Räder **Ø ≥ 80 mm** festschrauben.  
2. Prüfen: Ein **40 mm**-Hindernis (Leiste) muss bei 16° nass überfahrbar sein, ohne aufzusetzen.  
3. **20 mm**-Spalt: Rad soll nicht stecken bleiben; ggf. Räder paarweise nebeneinander (Add-back).

### 2.3 Bauch-Pad (Wischen = Fahren)
1. Microfaser auf Schaumstoff/Filz kleben (ca. handtellergroß).  
2. Unter der Platte so befestigen, dass leichter **Anpressdruck** auf Glas entsteht (Feder / Schaum).  
3. **Kein** eigener Wischmotor in v1.  
4. Pad muss austauschbar sein (Schmutz = Kratzer-Risiko).

### 2.4 Elektronik-Schutz
1. ESP32 + Treiber + Akku in Zip-Beutel oder Dose auf der Platte.  
2. Kabelzugentlastung; Stecker nicht unter Zug setzen.  
3. Sensoren **außerhalb** wasserdicht führen (IR nach unten, ToF nach vorne).

---

## 3. Elektrik verdrahten

> Pinbelegung wie `firmware/include/config.h` — bei Abweichung Datei anpassen.

| Signal | ESP32 (Default) | Ziel |
|---|---|---|
| Motor L IN1/IN2 | GPIO 25 / 26 | TB6612 Kanal A |
| Motor R IN1/IN2 | GPIO 27 / 14 | TB6612 Kanal B |
| Wisch-PWM (unbenutzt v1) | GPIO 33 | — frei lassen oder LED |
| IR Fl / Fr | GPIO 34 / 35 | TCRT5000 Analog |
| IR Rl / Rr | GPIO 32 / 39 | optional / Reserve |
| E-Stop-Taster | GPIO 4 → GND | INPUT_PULLUP |
| VL53L0X | SDA/SCL (21/22 typ.) | I²C (Firmware-Erweiterung) |
| VMOT | Akku + | TB6612 VMOT |
| GND | gemeinsam | ESP32 + Treiber + Sensoren |

**Schritte:**
1. Gemeinsames GND verbinden.  
2. TB6612 Logik an 3,3 V oder 5 V (laut Modul).  
3. Motoren an Out1/Out2.  
4. IR-Module versorgen, Analogausgänge an ADC-Pins.  
5. USB nur zum Flashen; Fahrbetrieb über Powerbank/Akku.

**Polarität prüfen:** Kurzer Handtest `manual` vor dem Mock.

---

## 4. Firmware flashen

```bash
cd firmware
# PlatformIO:
pio run -t upload
pio device monitor -b 115200
```

Oder Arduino-IDE: Board „ESP32 Dev Module“, Sketch aus `src/main.cpp` + `config.h` + ArduinoJson.

Serielle Kommandos (JSON, Newline):

```json
{"cmd":"ping"}
{"cmd":"status"}
{"cmd":"manual","drive":0.3,"turn":0,"wipe":0}
{"cmd":"stop"}
{"cmd":"start_row","speed":0.35}
{"cmd":"estop"}
{"cmd":"clear_fault"}
```

Kante ausgelöst → Modus `fault`, Motoren aus, bis `clear_fault` und Kante wieder sicher.

---

## 5. Inbetriebnahme (Testzyklen)

### Cycle A — Rahmen & Spalt (ohne smarte Firmware)
1. Mock 16°, nass.  
2. Nur Antrieb (Handschalter oder `manual`).  
3. **Pass:** 40 mm-Leiste und 20 mm-Spalt mehrmals ohne Hochsitzen.  
4. **Fail:** größere Räder / Doppelräder / später Bogie.

### Cycle B — Bauch-Pad
1. Schmutzschlämme auf Glas/Platte.  
2. Passiv wischen durch Fahren.  
3. **Pass:** sichtbare Reinigungsspur.

### Cycle C — Kanten-Stopp
1. IR nach unten justieren (`EDGE_THRESHOLD` in `config.h`).  
2. Über Dachkante (Tischkante) fahren lassen.  
3. **Pass:** Stopp 10/10, kein Sturz.

### Cycle D — Klemme ausweichen
1. ToF nach vorne (Firmware v0.2 — Avoid-Logik ergänzen).  
2. Klemmen-Attrappe.  
3. **Pass:** Anhalten/Abdrehen ohne harten Aufprall.

### Cycle E — Edge-Park + Idle
1. Zustände: CRAWL → EDGE erkannt → zurücksetzen → IDLE/Sleep.  
2. Danach erst **beaufsichtigter** Dachversuch.

---

## 6. Dach (erst nach E)

1. Roboter auf Modul setzen, Ausrichtung prüfen.  
2. Menschliche Aufsicht (trotz „kein Tether“-Anforderung).  
3. Bei Unsicherheit Sofort-Stopp (Taster / `estop`).  
4. Pads nach Einsatz spülen — Grit zerkratzt AR-Glas.

---

## 7. Justage-Tipps

| Problem | Maßnahme |
|---|---|
| IR löst auf Fuge aus | Schwellwert / Timeout „kurze Einzelseite = Naht“ |
| IR löst zu spät | Sensoren weiter nach vorne / tiefer |
| Zu wenig Traktion nass | Weichere Reifen, mehr Gewicht über Antrieb, 4WD |
| Pad streift schlecht | Mehr Anpressdruck, frisches Tuch |
| Akku hält keine Woche | Sleep-Strom messen; später Mini-Solar (Add-back) |

---

## 8. Abnahme-Checkliste Prototyp

- [ ] Cycle A bestanden  
- [ ] Cycle B sichtbare Reinigung  
- [ ] Cycle C kein Sturz am Mock  
- [ ] Cycle D Klemme umfahren  
- [ ] Edge-Park in IDLE  
- [ ] Stückliste &lt; 200 € dokumentiert  
- [ ] Beaufsichtigter Dachlauf geplant  

---

*Bauplan folgt den Musk-Schritten 1–3 (Anforderungen → Delete → Simplify). Nicht optimieren, was die Stückliste nicht erzwingt.*
