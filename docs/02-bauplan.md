# Bauplan & Aufbauanleitung — PV-Clean Rain Prototyp v2.1

**Brain:** Raspberry Pi **2011.12** (vorrätig)  
**Power:** GOODaaa **D4004** 25 000 mAh + Solar (vorrätig)  
**Rest:** Minimal-Crawler (Bauch-Pad, Ø80-Räder, TB6612, 2× IR, 1× ToF)

```
   [Solar-Klappe D4004]----lädt----[Powerbank D4004]
                                      | Out2 5V/2.1A
                                      v
                               [Raspberry Pi 2011.12]
                                      |
                    GPIO -----------> [TB6612] --> Motoren
                    ADC/GPIO -------> IR ↓↓
                    I2C ------------> VL53 →
                                      |
                               === Chassis ===
                          [Bauch-Pad]  [4× Softwheels]
```

---

## 1. Stromversorgung (wichtig)

1. D4004 **Output 2 (5 V / 2,1 A)** → micro-USB **POWER** am Pi (nicht Out1).  
2. Motortreiber **VMOT**: möglichst **nicht** den Pi-5V-Pin belasten.  
   - **Empfohlen v1:** zweiter USB-Ausgang der Powerbank (Out1) nur für TB6612+Motoren **oder** Y-Kabel von Out2 mit dicker Leitung + Elko am TB6612, Motorstrom am Pi-USB **vorbei**.  
   - Gemeinsames **GND** zwischen Pi und TB6612 zwingend.  
3. Solar-Klappe bei Idle ausklappen / zum Himmel — verbessert Wochen-Standby; Fahren nur aus Akku.  
4. Brownout-Symptom am alten Pi: bunter Screen / Reboot unter Motorlast → Verkabelung prüfen, Strompfade trennen.

---

## 2. Mechanik

Unverändert zu v2:
1. Chassis ~200×150 mm.  
2. 2–4 Getriebemotoren, 4× weiche Räder Ø≥80 mm.  
3. Passives Microfaser-Bauch-Pad mit leichtem Anpressdruck.  
4. Pi + Powerbank auf dem Chassis; Powerbank so, dass Solar-Klappe nutzbar bleibt (oder Powerbank fest, Solar bei Idle manuell/aufgestellt — für Prototyp OK).  
5. IR nach unten an der Front, ToF nach vorne.

**Gewicht:** D4004 + Pi sind schwerer als ESP+kleine Zelle → Traktion besser, Rahmenklettern ggf. leichter; Kanten-Risiko bleibt — Soft-Stopp muss sitzen.

---

## 3. Elektrik / GPIO (Pi Model B)

Pi 2011.12: **3,3 V**-GPIO — TB6612-Logik 2,7–5,5 V OK; niemals 5 V in einen Pi-GPIO.

| Funktion | Pi-Pin (BCM, typisch Model B) | Ziel |
|---|---|---|
| Motor L IN1 / IN2 | GPIO 17 / 18 | TB6612 A |
| Motor R IN1 / IN2 | GPIO 22 / 23 | TB6612 B |
| IR Front L / R | GPIO 27 / 24 (digital) *oder* USB-ADC später | TCRT5000 DO/AO |
| VL53L0X | SDA/SCL (GPIO 2/3 auf späteren Boards; Model B: P1-03/05) | I²C 3,3 V |
| E-Stop | GPIO 25 → GND | Pull-up |
| 5 V / GND | nur Versorgung | D4004 Out2 |
| VMOT / GND | Motorzweig | D4004 Out1 oder paralleler 5 V-Pfad |

*Pinnummern in Software-Config festhalten und am Board nach P1-Header-Belegung 2011.12 verifizieren (Rev1 vs Rev2).*

Original-Pi hat oft **keinen** Onboard-ADC: IR besser als **Digital-Out**-Module (DO-Schwellwert am Poti) oder günstiges ADS1115 (Add-back nur wenn nötig).

---

## 4. Software (Pi statt ESP32)

1. Raspberry Pi OS **Legacy Lite** auf microSD (armhf für alten Pi).  
2. Python 3: `RPi.GPIO` oder `gpiozero`, `smbus` für VL53, optional Serial-Debug.  
3. Zustände wie geplant: `SLEEP → WAKE_RAIN → CRAWL → AVOID → EDGE_PARK → IDLE`.  
4. Kanten-IR: bei „unsicher“ **sofort** Motoren aus (höchste Priorität in der Loop, &lt;50 ms Ziel).  
5. ESP32-Ordner `firmware/` bleibt als Referenz; neue Pi-Skripte unter `software/` (wird angelegt).

Minimal-Start:

```bash
sudo apt update && sudo apt install -y python3-gpiozero python3-smbus i2c-tools
# I2C im raspi-config aktivieren
python3 software/crawl_v01.py   # nach Anlage
```

---

## 5. Testzyklen (unverändert in der Reihenfolge)

| Cycle | Ziel |
|---|---|
| A | 40 mm-Rahmen + 20 mm-Spalt nass bei 16° |
| B | Bauch-Pad reinigt sichtbar |
| C | IR-Kantenstopp 10/10 am Mock |
| D | ToF umfährt Klemme |
| E | Edge-Park → IDLE; Powerbank-Solar Idle-Test |

Dach erst nach E, mit Aufsicht.

---

## 6. Abnahme-Zusatz v2.1

- [ ] Pi läuft stabil an D4004 **Out2**  
- [ ] Motoren verursachen keinen Pi-Brownout  
- [ ] Solar-Klappe lädt Powerbank (sichtbar / Status-LEDs)  
- [ ] Cycles A–E  

---

*First principles: vorhandene Teile nutzen. Musk Step 2: kein zweites Brain/keinen Extra-Akku kaufen, solange Vorrat reicht.*
