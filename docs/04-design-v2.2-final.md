# PV-Clean Rain – Design v2.2 (finale Fassung nach kritischem Review)

Stand: 12.09.2026 · ersetzt v2.1 als Referenz · Prototyp für die 20,48-kWp-Anlage (16° Dachneigung)

## 0. Kurzfassung

PV-Clean Rain ist ein kleiner, akkubetriebener Kriechroboter ohne Wassertank. Er fährt **nur bei Regen** über die Module und zieht mit einer pendelnden Silikon-Wischleiste Wasser und gelösten Schmutz **bergab** über die untere Modulkante. Er fährt fast nur entlang der Falllinie (bergab reinigen, bergauf diagonal zurück in die nächste Bahn), erkennt Fugen und Anlagenkanten mit vier nach unten gerichteten Laser-Abstandssensoren und wartet zwischen den Regenfällen **komplett abgeschaltet** in einer Parkstation am oberen Rand der Anlage. Dort halten ihn Niederhalter gegen Wind fest, eine weiße Haube schützt ihn vor Sonne, und über Federkontakte wird er geladen.

Gehirn: Raspberry Pi Model B (2011.12, vorhanden). Energie: GOODaaa D4004 25 000 mAh (vorhanden). Zukauf ca. **179 €**.

## 1. Kritisches Review: Schwachstellen in v2.1 und Änderungen

| # | Schwachstelle v2.1 | Befund (erste Prinzipien) | Änderung in v2.2 |
|---|---|---|---|
| 1 | Anforderung „40-mm-Rahmen überklettern“ | Die 40 mm sind die **Moduldicke**. Die Glasflächen benachbarter Module liegen in einer Ebene, der Rahmen steht nur ca. 1–2 mm über dem Glas. Echte Hindernisse sind die **20-mm-Fuge** zwischen den Spalten (mit Mittelklemmen) und die ca. **50-mm-Fuge** zwischen den Reihen (Verlegemaß 1690 − 1640 mm). | Klettern gestrichen. Ein Rad mit Ø80 mm sinkt über 20 mm nur 1,3 mm und über 50 mm ca. 9 mm ein; das schaffen 4 angetriebene Räder. |
| 2 | Kantenerkennung mit TCRT5000 (IR-Reflex) | PV-Glas ist transparent und Zellen schlucken Infrarot (dafür sind sie gebaut). Ein Reflexsensor sieht deshalb Glas und Abgrund ähnlich „dunkel“, hat nur ca. 2–15 mm Reichweite und Regentropfen stören. | **4× VL53L0X-Laser-Abstandssensor nach unten** (Glas ≈ 25 mm, Fuge/Abgrund > 80 mm), auf Auslegern **120 mm vor bzw. hinter den Achsen**. Fuge oder Kante wird über die zurückgelegte Strecke (Encoder) und die Dachkarte unterschieden. |
| 3 | 2 angetriebene Räder, Verdrahtung ohne PWM/STBY | Auf nassem Glas bei 16° braucht schon das Stehenbleiben eine Reibzahl μ ≥ tan 16° = 0,29. Bei 2WD trägt nur die Hälfte des Gewichts zur Traktion bei (μ ≥ 0,57 nötig, unrealistisch nass). Der TB6612 läuft außerdem nur mit PWM- und STBY-Pin, die in v2.1 fehlten. | **4WD**, Getriebe 1:120, 2 Motoren mit Encoder, **2× TB6612** (je eine Seite) mit PWM + STBY. Sanfte Rampen, Kurzschlussbremse im Stand. |
| 4 | 90°-Drehungen und Querfahrten | Auf nassem, geneigtem Glas rutscht ein Kettenlenk-Fahrzeug beim Drehen und bei Querfahrt seitlich ab. | **Keine 90°-Drehungen.** Bergab gerade reinigen, bergauf rückwärts mit 2–4° Kurswinkel diagonal in die nächste Bahn (Sägezahn-Muster). Kurs relativ zur Falllinie misst der Beschleunigungssensor (Schwerkraftvektor in der Modulebene): absolut, ohne Drift, ohne Kompass. |
| 5 | Passives Microfaser-Bauch-Pad | Ein Pad sammelt Sand (Kratzgefahr für die Antireflexschicht), sättigt sich mit Schmutz und verschmiert ihn auf ca. 104 m². Bei geringer Neigung liegt der meiste Schmutz als **Schmutzlinie an der unteren Rahmenkante**. | **Pendelnde Silikon-Wischleiste vorne**: bergab drückt sie mit ca. 2 N und schiebt Wasser und Schmutz über die untere Kante; bergauf klappt sie weg und schleift nur mit Eigengewicht (ca. 0,3 N). Regen spült die Lippe frei. Microfaser bleibt nur als A/B-Option im Test B. |
| 6 | Energie: „1 Woche Standby“ | Ein Pi Model B zieht dauerhaft ca. 3,5 W, auch im Leerlauf (er hat keinen Schlafmodus). Bei 60–65 Wh nutzbarer Kapazität ist der Akku **nach weniger als 1 Tag leer**. Die Solarzelle der D4004 (ca. 1–2 W) gleicht das nicht aus und wäre im Gehäuse ohnehin verdeckt. | **Pi wird komplett abgeschaltet** (Lastschalter). Ein Zeitgeber (TPL5110, alle 2 h) oder der Regensensor schaltet ihn ein. Standby ≈ 1,2 Wh/Tag, also ca. 8 Wh/Woche. Die Solarklappe der D4004 wird nicht genutzt; die D4004 dient nur als Akku. |
| 7 | Powerbank-Abschaltautomatik | Powerbanks schalten bei geringer Last (typisch < 50–100 mA) ab. Dann hat auch der Weckschaltkreis keinen Strom mehr. | **Test 0** vor allem anderen, mit Entscheidungsbaum (§ 9.3). |
| 8 | Freies Parken auf der Modulkante, kein Seil | **Wind:** Ein Roboter mit ca. 1,6 kg und ca. 0,05 m² Seitenfläche rutscht rechnerisch schon bei Böen von ca. 45–60 km/h ab. **Verschattung:** Ein geparkter Roboter deckt Zellen ab (Ertragsverlust, Hotspot-Risiko). **Hitze:** Ein dunkles Modul in der Sonne wird bis ca. 70 °C heiß, schlecht für Li-Ionen-Akkus. | **Parkstation (Dock) direkt an der Oberkante einer Modulspalte**, außerhalb der Zellfläche. Niederhalter halten formschlüssig, eine weiße Haube schattet ab, Federkontakte laden. Wetter-Sperre: Böen > 30 km/h, Gewitter, < 2 °C. |
| 9 | Software hängt beim Fahren | Ein abgestürzter Pi würde die Motoren weiterlaufen lassen, im schlimmsten Fall bergab über die Kante. | **Hardware-Watchdog:** Der Pi gibt ein 200-Hz-Taktsignal aus. Eine Ladungspumpe hält damit STBY der Motortreiber high. Fehlt der Takt länger als ca. 100 ms, sind die Motoren stromlos. |
| 10 | Pinbelegung | „Raspberry Pi (c) 2011.12“ steht auf Rev 1 **und** Rev 2. GPIO 27 gibt es auf Rev 1 nicht (dort GPIO 21), und der I²C-Bus ist 0 statt 1. | Nur Pins, die auf **beiden** Revisionen gleich sind. Revision vorab mit `grep Revision /proc/cpuinfo` prüfen. |
| 11 | Elektronik im Zip-Beutel | Kabel treten aus, Kondenswasser, Treibhauseffekt. | **IP65-Gehäuse** 200×120×75 mm, hellgrau/weiß, mit Kabelverschraubungen und Trockenmittel. |
| 12 | Strom für die Motoren | Out1 der D4004 liefert nur 1 A. | Die 4 Motoren ziehen bei Last ca. 0,6–0,8 A. Die 1-A-Grenze wirkt als natürliche Strombegrenzung, und ein Encoder-Stillstand > 1 s führt zum Stopp. |

**Bewusst gestrichen (Musk-Schritt 2):** mechanische Kantenkufen (eine Kufe müsste über 100 mm lang sein, um 50-mm-Fugen zu überbrücken), Magnetometer, Zusatztank, Seil im Betrieb, Solarklappe am Roboter.

**Bleibt offen und wird bewusst getragen:** Ein Totalausfall aller Sensoren kann zum Absturz führen (ca. 1,6 kg vom Dach). Deshalb bei allen Dachtests eine **temporäre Sicherungsleine unter Aufsicht** (nicht Teil des Designs), bis die Kantenerkennung über mehrere Missionen bewiesen ist.

## 2. Einsatzumgebung (Referenz)

- 64 Module IBC PolySol 320 VL5-HC, 1640 × 992 × 40 mm, Hochformat, Schletter-Unterkonstruktion
- Verlegemaß 1012 mm (quer) × 1690 mm (entlang Gefälle): **Spaltenfuge ≈ 20 mm** mit Mittelklemmen auf Höhe der Schienen, **Reihenfuge ≈ 50 mm** ohne Klemmen (vor Ort nachmessen)
- 12 Spalten, unregelmäßiger Umriss, ca. 3 Dachdurchführungen; Glasfläche ≈ 104 m²
- Dachneigung **16°**; unter der Anlage Dachziegel (ca. 10–15 cm tiefer)

## 3. Abmessungen und Bauteile

Koordinaten: Ursprung = Robotermitte auf der Glasebene; **x = vorwärts (bergab)**, y = links, z = senkrecht zur Glasfläche. Alle Maße in mm; Massen geschätzt, beim Bau nachwiegen.

| Bauteil | Maße | Lage (Mitte x, y, z) | Masse |
|---|---|---|---|
| Chassisplatte (6-mm-Siebdruckplatte oder PETG) | 240 × 170 × 6 | (0, 0, 55), Unterseite z = 52 | 220 g |
| 4 Softwheels (Silikon) | Ø80 × 17 | (±75, ±97,5, 40) | 4 × 40 g |
| 4 Getriebemotoren 1:120 (vorne 2 mit Encoder) | 70 × 22 × 18 | unter der Platte, Welle auf z = 40 | 4 × 35 g |
| Spurweite / Radstand | 195 / 150 | – | – |
| Bodenfreiheit (unter Motoren / Platte) | 29 / 52 | – | – |
| IP65-Gehäuse | 200 × 120 × 75 | (−10, 0, 96), z 58–133 | 250 g |
| ↳ GOODaaa D4004 (Boden des Gehäuses) | 165 × 85 × 30 | im Gehäuse unten | ca. 520 g |
| ↳ Raspberry Pi Model B (auf 12-mm-Abstandsbolzen) | 85,6 × 56,5 × 17 | über der D4004 | 45 g |
| ↳ Steuerplatine: 2× TB6612, TCA9548A, 2× INA219, TPL5110, Lastschalter, Watchdog | ca. 90 × 60 | Gehäuseseite | 40 g |
| ↳ MPU-6050 (Beschleunigung + Gyro) | 21 × 16 | starr auf der Gehäusebodenmitte | – |
| Wischleiste, pendelnd (Silikon-Abzieherlippe) | 200 breit, Lippe 25 × 3 | Gelenkachse (135, 0, 50), Kontaktlinie x ≈ 145 | 70 g |
| Ausleger vorne/hinten (Alu-Flach 20 × 2) | je 2 Stück, 125 lang | von x = ±75 bis ±200 | 80 g |
| 4 VL53L0X nach unten (FL, FR, RL, RR) | 25 × 13 × 7 | (±195, ±80, 25) | 4 × 3 g |
| 1 VL53L0X vorne, 45° nach unten (Hindernisse) | 25 × 13 × 7 | (200, 0, 60) | 3 g |
| Regensensor-Platte | 40 × 55 | Gehäusedeckel oben, 10° geneigt | 10 g |
| Ladekontakte (2 Messingplatten) | 15 × 15 | Heck (−200, ±30, 45) | 10 g |
| USB-WLAN-Stick | – | am Pi | 10 g |
| **Gesamt** | **L 400 (über Ausleger) × B 212 × H 135** | – | **≈ 1,6 kg** |

Reinigungsbreite 200 mm, Bahnabstand 180 mm (20 mm Überlappung).

## 4. Aufbau (Reihenfolge)

1. Chassisplatte zuschneiden. Motorhalter so unter der Platte verschrauben, dass die Wellen auf z = 40 liegen; Encodermotoren vorne.
2. Räder aufstecken (Spur 195, Radstand 150) und Ausleger vorne und hinten verschrauben.
3. VL53L0X an die Auslegerenden (Optik nach unten, 25 mm über Glas) und den Vorwärtssensor 45° geneigt montieren.
4. Wischleiste: Scharnier an Platten-Vorderkante. Anschlag + Zugfeder sorgen für ca. 2 N Anpressdruck bei Bewegung vorwärts/bergab; rückwärts klappt die Leiste bis zum oberen Anschlag weg.
5. IP65-Gehäuse mit 4 Kabelverschraubungen (Motoren links/rechts, Sensoren vorne/hinten) aufsetzen; D4004 unten, Pi darüber auf Abstandsbolzen, Steuerplatine seitlich, MPU-6050 starr in Bodenmitte, Trockenmittelbeutel.
6. Regensensor auf den Deckel (Power-LED ablöten → ca. 3 mA statt 10 mA), Ladekontakte ans Heck.
7. Verdrahtung nach § 10; erst Test 0, dann Tests A–E.

## 5. Antrieb und Traktion (Rechnung)

- Hangabtrieb: 1,6 kg × 9,81 × sin 16° = **4,3 N**.
- Bergauf mit weggeklappter Leiste (+0,1 N): Antrieb muss **≈ 4,4 N** an den Rädern liefern, also 0,18 N·m gesamt bzw. **≈ 0,45 kg·cm pro Motor**. Ein TT-Getriebemotor 1:120 schafft bei 5 V knapp das Doppelte; Reserve ≈ 2 (Test A misst).
- Traktion: verfügbar = μ × 1,6 × 9,81 × cos 16° = μ × 15,1 N. Mit μ = 0,5 (Silikon auf nassem Glas, zu messen) sind es 7,5 N, also 1,7-fache Reserve. **Untergrenze μ ≈ 0,30.**
- Bergab: Hangabtrieb 4,3 N minus Leistenreibung ca. 0,8 N. Die Motoren bremsen geregelt (Encoder); im Stand hält die Kurzschlussbremse.
- Geschwindigkeit: reinigen 0,06 m/s, zurück 0,08 m/s, andocken 0,03 m/s.
- Schlupferkennung: Encoderweg ≠ erwartete Bewegung (Fugen-Landmarken, Beschleunigung) → Stopp, bremsen, warten, Bahn neu ansetzen.

## 6. Reinigung

- Wasser kommt nur vom Regen (kein Tank). Mission nur, wenn der Regensensor nass meldet; bis 20 min nach Regenende darf weitergefahren werden (Glas noch nass).
- **Reinigungshub = immer bergab.** Die Wischleiste vorne schiebt den Wasserfilm mit gelöstem Pollen, Staub und Vogelkot vor sich her, über jede Reihenfuge hinweg (Schmutz fällt in die Fuge und wird abgespült) bis zur unteren Anlagenkante.
- **Schmutzkanten-Manöver** an der untersten Modulkante: Die Karte weiß, dass hier keine Fuge, sondern die Kante kommt. Nach der Erkennung fährt der Roboter noch 55 mm weiter, so dass die Leiste über die untere Rahmenlippe streicht (Schmutzlinie). Das Vorderrad steht dann noch 65 mm vor der Kante.
- **Rückhub bergauf:** rückwärts, Leiste weggeklappt (kaum Reibung, kein Zurückschmieren), diagonal um eine Bahnbreite versetzt.
- Wartung: Lippe 2× pro Saison sichtprüfen, jährlich tauschen (ca. 3 €). Kein Einsatz bei Frost/Schnee (Wetter-Sperre).

## 7. Navigation und Bewegungsablauf

**Dachkarte** (JSON auf dem Pi, aus der Modulbelegung): Spalten 1–12 mit Reihen von/bis, Fugenpositionen, Klemmzonen (±60 mm um die Schienenhöhen an jeder Spaltenfuge), Durchführungen, Dock-Position.

**Ortung:** Encoder-Wegmessung + Kurs aus dem Schwerkraftvektor (MPU-6050) + **Fugen als Landmarken**. Jede Querung einer Reihenfuge setzt die Position entlang des Gefälles exakt zurück, jede Querung einer Spaltenfuge die Querposition.

**Fuge oder Kante?** Ein Abwärts-Sensor meldet „kein Glas“ (> 30 mm tiefer als Glas).
- Kommt Glas innerhalb von 60 mm Fahrweg wieder, ist es eine Fuge: weiterfahren, Landmarke setzen.
- Bleibt es länger weg oder sagt die Karte „hier ist keine Fuge“, ist es eine **Kante**: sofort stoppen und bremsen.
- Bilanz: 60 mm Entscheidung + ca. 11 mm Bremsweg (0,06 m/s, 100 ms Latenz) bei 120 mm Vorlauf, also ca. 50 mm Reserve bis zum Rad.
- Sensoren seitlich (y = ±80) erkennen auch seitliches Abdriften über eine Seitenkante.

**Sägezahn-Muster je Spalte** (6 Bahnen pro Spalte, Bahnmitten 121 / 271 / 421 / 571 / 721 / 871 mm vom linken Spaltenrand, mindestens 121 mm Abstand zu Klemmen):
1. Oben in Bahn k ausgerichtet (Kurs = Falllinie).
2. **Bergab gerade** reinigen bis zur unteren Kante, inkl. Schmutzkanten-Manöver.
3. **Bergauf rückwärts** mit Kurswinkel θ = atan(180 mm / Bahnlänge) ≈ 2–4°; oben kommt er in Bahn k+1 an. Die obere Kante erkennen die hinteren Sensoren.
4. Wiederholen. **Spaltenwechsel:** Die Diagonale der letzten Bahn quert die 20-mm-Fuge; der Planer legt den Querungspunkt auf Modulmitte (außerhalb der Klemmzonen).
5. Hindernisse (Durchführungen) sind in der Karte eingetragen; zusätzlich stoppt der Vorwärtssensor bei < 80 mm.

**Umfang:** ca. 72 Bahnen, ca. 580 m Reinigungs- + 580 m Rückweg, ca. 4,7 h Fahrzeit, ca. 35 Wh. Das verteilt sich auf mehrere Regenereignisse; der Fortschritt wird gespeichert (M3: langsam ist ok).

## 8. Sicherheit

1. **Karte + 4 Abwärts-Laser** mit Fugen/Kanten-Logik (§ 7).
2. **Hardware-Watchdog:** fehlt das 200-Hz-Signal des Pi länger als ca. 100 ms, sind die Motoren stromlos (STBY low). Test 0 prüft, ob das 1:120-Getriebe den Roboter bei 16° nass hält. Falls nicht: Ruhekontakt-Relais, das die Motoren kurzschließt (+5 €).
3. **IMU-Überwachung:** Neigung > 25°, Ruck oder Kurs springt → Stopp + Bremse.
4. **Wetter-Sperre** (Open-Meteo für Limburg über WLAN): keine Mission bei Böen > 30 km/h, Gewitter, < 2 °C oder Schnee; zieht Wind während einer Mission auf, fährt der Roboter sofort zurück ins Dock.
5. **Dock mit Niederhaltern** gegen Wind im Ruhezustand.
6. **Energiereserve:** Rückkehr ins Dock bei < 25 % (Energiezähler über INA219 + Laufzeitbilanz).
7. **Dachtests** nur nach bewiesenem Kantenstopp, unter Aufsicht, mit temporärer Sicherungsleine.

## 9. Energie, Andocken und Laden

### 9.1 Energiebilanz
- D4004: 25 000 mAh × 3,7 V = 92,5 Wh nominal, **≈ 60–65 Wh nutzbar** an 5 V.
- Fahren: Pi 3,5 W + Motoren ca. 3 W + Sensoren/WLAN ca. 1 W ≈ 7,5 W.
- Standby (Pi aus): Regensensor ca. 3 mA + Zeitgeber, plus 12 Weckvorgänge/Tag à ca. 60 s ≈ **1,2 Wh/Tag**.
- 1 Woche Standby ≈ 8 Wh plus ca. 1–2 Teilmissionen → Anforderung C2 erfüllt, **sofern Test 0 besteht**.

### 9.2 Parkstation (Dock)
- **Lage:** oberhalb der obersten Reihe, direkt an der Oberkante einer Modulspalte, nahe am Dachzugang. Genaue Stelle vor Ort festlegen.
- **Grundplatte** 300 × 260 mm (9-mm-Siebdruck oder 4-mm-Alu), Oberfläche bündig mit dem Glas (±3 mm). Eine 20-mm-Übergangslippe liegt auf dem oberen Modulrahmen auf (keine Last aufs Glas).
- **Befestigung:** zwei Alu-Ausleger an der obersten Montageschiene (Schletter-Nut, Hammerkopfschrauben) plus zwei höhenverstellbare Stützfüße (Gewindestange + Gummifuß) auf den Ziegeln. Keine Dachdurchdringung; Montagesystem/Statik vor Ort prüfen.
- **Führung:** zwei seitliche Leitbleche als V-Einlauf, 30 mm hoch; fangen ±40 mm Querversatz.
- **Niederhalter:** zwei Winkelleisten auf Höhe z ≈ 60, die 15 mm über die seitlichen Chassisflansche (je 20 mm frei neben dem Gehäuse) greifen. Abheben ist dann formschlüssig auf ca. 2 mm begrenzt.
- **Endanschlag mit 2 Federkontakten** (Pogo-Pins, 5 V/GND) an der oberen Dockwand; sie treffen die Messingplatten am Roboterheck.
- **Haube:** weiß, 320 × 280 × 160 mm, zur Modulseite offen, mit Lüftungsspalt: Schatten, kein Treibhauseffekt.
- **Laden (empfohlene Option, +25 €):** 10-W-Solarpanel mit 5-V-USB-Ausgang auf dem Haubendach. Strompfad: Federkontakte → INA219 (Ladestrom + „angedockt“-Erkennung) → Micro-USB-Eingang der D4004. Im Herbst ca. 8–12 Wh/Tag: deckt Standby und alle 3–4 Tage einen Vollhub, das ist der Weg zum Ziel „ganze Saison unbeaufsichtigt“. Ohne Option wird die D4004 von Hand geladen (Kabel an die Kontakte oder ausbauen).

### 9.3 Test 0: Powerbank-Abschaltautomatik (entscheidet die Weckschaltung)
1. Liefert Out2 der D4004 auch bei ca. 3 mA dauerhaft 5 V? Dann TPL5110 und Regensensor direkt an Out2 vor dem Lastschalter. **Fertig.**
2. Schaltet sie ab: ein Keep-alive-Pulsgeber (150 mA für 100 ms alle 5 s ≈ 3 mA Mittel, ca. 0,4 Wh/Tag). Hält das die Bank wach? Dann **fertig**.
3. Sonst: kleine 1S-LiPo-Zelle (500 mAh) mit Ladeschaltung als Dauerversorgung für Zeitgeber + Transistor parallel zum Einschalttaster der D4004 (Gehäuse öffnen), oder die D4004 als Fahrakku durch ein 2S-18650-Paket mit BMS ersetzen (ca. 18 €, keine Abschaltautomatik).
4. Zusätzlich prüfen: Gibt die D4004 Strom aus, während sie lädt (Pass-Through)? Wichtig für das Laden im Dock.

### 9.4 Andock-Ablauf
1. Auslöser: Mission fertig, Regen vorbei, Wind, Energie < 25 % oder Fehler.
2. Fahrt zur Oberkante der Dock-Spalte; Ausrichtung auf die Falllinie (Schwerkraftvektor).
3. Rückwärts bergauf mit 0,03 m/s; die hinteren Sensoren sehen den Übergang Glas → Dockplatte (laut Karte erwartet, keine Fuge).
4. Die Leitbleche zentrieren, das Chassis gleitet unter die Niederhalter.
5. Die Heckkontakte treffen die Federkontakte. INA219 meldet 5 V, der Roboter fährt noch 5 mm nach (Federweg) und stoppt mit Kurzschlussbremse.
6. Log speichern, Zeitgeber-„fertig“ setzen → Pi stromlos. Das Dock-Panel lädt weiter.
7. **Abdocken:** nach dem Wecken und bestandenen Prüfungen vorwärts bergab aus dem Dock aufs oberste Modul, Wischleiste fällt auf Anpressdruck.

## 10. Elektrik

**Stromversorgung**
- D4004 **Out2 (2,1 A)** → Lastschalter (P-MOSFET-Modul) → Pi (Micro-USB). Der Pi läuft nur an Out2.
- Immer an, vor dem Lastschalter: TPL5110 + Regensensor (je nach Test 0).
- Weckschaltung: Zeitgeber-Ausgang ODER Regensensor-Ausgang (2 Dioden) schaltet den Lastschalter ein. Der Pi hält sich selbst über TPL_DONE, bis er fertig ist.
- D4004 **Out1 (1 A)** → INA219 (Motorstrom) → 1000-µF-Elko → VMOT beider TB6612. Motorstrom fließt nie über den USB des Pi. Gemeinsame Masse.
- Dock-Kontakte → INA219 (Ladestrom) → D4004 Micro-USB-Eingang.

**Bussystem**
- I²C: Pi → TCA9548A (0x70) → Kanäle 0–4: VL53L0X FL, FR, RL, RR, vorne (je 0x29).
- Hauptbus: MPU-6050 (0x68), INA219 Motor (0x40), INA219 Laden (0x41).

**Pinbelegung (BCM, nur Pins, die auf Rev 1 und Rev 2 gleich sind)**

| Funktion | GPIO | P1-Pin |
|---|---|---|
| Links PWM / IN1 / IN2 (TB6612 #1, A+B parallel) | 18 / 23 / 24 | 12 / 16 / 18 |
| Rechts PWM / IN1 / IN2 (TB6612 #2, A+B parallel) | 17 / 22 / 25 | 11 / 15 / 22 |
| Watchdog-Takt → Ladungspumpe → STBY beider TB6612 | 4 | 7 |
| Encoder links / rechts (Kanal A) | 7 / 8 | 26 / 24 |
| TPL5110 DONE (Selbstabschaltung) | 11 | 23 |
| Regensensor DO (serielle Konsole deaktivieren) | 15 | 10 |
| I²C SDA / SCL (Bus 0 bei Rev 1, Bus 1 bei Rev 2) | 0/1 bzw. 2/3 | 3 / 5 |
| Reserve | 9, 10, 14 | 21, 19, 8 |

Software: Raspberry Pi OS Legacy Lite, Python 3, gpiozero (pigpio als Pin-Factory für sauberes PWM), smbus2. Siehe `software/config.py` und `software/crawl_v01.py` (Fahrtest A).

## 11. Zustandsautomat

`SLEEP` (Pi aus, im Dock) → Wecken (Regen nass ODER alle 2 h) → `CHECK` (Regen? Böen < 30 km/h? > 2 °C? kein Gewitter? Energie > 40 %?)
- Nein → `SLEEP`
- Ja → `UNDOCK` → `GOTO_LANE` (nächste offene Bahn) → `CLEAN_DOWN` → `EDGE_SWEEP` (Schmutzkanten-Manöver) → `RETURN_UP_DIAGONAL` → … → Abbruchbedingung → `RETURN_DOCK` → `DOCK` → `SLEEP`

Fehler jeder Art → `FAULT`: Stopp, Bremse; wenn sicher möglich, `RETURN_DOCK`, sonst stehen bleiben und Watchdog/Bremse halten lassen. Meldung beim nächsten Wecken über WLAN.

## 12. Stückliste und Kosten (Zukauf, Richtpreise DE)

| Pos. | Teil | Preis |
|---|---|---|
| – | Raspberry Pi Model B 2011.12, GOODaaa D4004 | vorhanden |
| 1 | 4× Silikon-Softwheel Ø80 × 17 | 8 € |
| 2 | 2× Getriebemotor 1:120 mit Encoder | 16 € |
| 3 | 2× Getriebemotor TT 1:120 | 9 € |
| 4 | 2× TB6612FNG | 10 € |
| 5 | 5× VL53L0X | 20 € |
| 6 | TCA9548A I²C-Multiplexer | 4 € |
| 7 | MPU-6050 | 3 € |
| 8 | 2× INA219 | 6 € |
| 9 | TPL5110 + P-MOSFET-Lastschalter | 7 € |
| 10 | Regensensor-Modul | 3 € |
| 11 | USB-WLAN-Stick (Pi-B-tauglich) | 8 € |
| 12 | IP65-Gehäuse 200 × 120 × 75 + 4 Kabelverschraubungen + Trockenmittel | 15 € |
| 13 | Chassisplatte + Alu-Flach für Ausleger | 12 € |
| 14 | Silikon-Abzieherlippe 200 mm + Scharnier + Feder | 6 € |
| 15 | Watchdog-Bauteile (Dioden, Kondensatoren, Transistor) | 1 € |
| 16 | Kabel, Stecker, Lochraster, Elkos, Schrauben, Messingkontakte | 15 € |
| 17 | microSD 8 GB (falls nicht vorhanden) | 6 € |
| | **Roboter** | **149 €** |
| 18 | Dock: Platte, Alu-Winkel, Gewindestangen/Füße, Leitbleche, Niederhalter, Haube, 2 Pogo-Pins | 30 € |
| | **Summe** | **≈ 179 €** (Cap 200 €) |
| Opt. | 10-W-Solarpanel mit 5-V-USB-Ausgang fürs Dock | +25 € (≈ 204 €; ohne microSD ≈ 198 €) |
| Opt. | Ruhekontakt-Bremsrelais (falls Test 0 Rollen zeigt) | +5 € |

Bestellung erst nach Norberts Freigabe.

## 13. Tests (Accelerate)

- **0 – Werkbank-Basics:** Pi-Revision und Stromaufnahme; D4004-Abschaltautomatik und Pass-Through (§ 9.3); μ Silikonrad auf nassem Glas (nasse Glasplatte langsam kippen, bis das Rad rutscht: μ = tan Winkel); VL53L0X auf nassem Modulglas über dunkler Zelle und über einer 50-mm-Fuge; Rollt der Roboter mit stromlosen Motoren bei 16°?
- **A:** Fahren 4WD auf nassem 16°-Testbrett mit 20- und 50-mm-Fuge, bergauf/bergab, diagonaler Rückhub.
- **B:** Reinigung: Wischleiste vs. Microfaser, A/B auf verschmutztem Glas.
- **C:** Kantenstopp: 50× Kante, 50× Fuge, null Fehlstopps über der Kante erlaubt.
- **D:** Andocken: 20× aus ±40 mm Versatz; Niederhalter-Zugtest.
- **E:** Integration: Missionsablauf am Testbrett, dann eine beaufsichtigte Dachfahrt mit Sicherungsleine.

## 14. Dateien

- Dieses Dokument: `docs/04-design-v2.2-final.md`
- Anforderungen: `docs/03-anforderungen-v1.md`; Stückliste/Bauplan v2.1: `docs/01-stueckliste.md`, `docs/02-bauplan.md` (durch § 12 und § 10 hier überholt)
- Pinbelegung + Fahrtest: `software/config.py`, `software/crawl_v01.py`
- Visualisierungen (Stand v2.1, **ohne** Ausleger, Wischleiste und Dock; Bauch-Pad statt Leiste): `assets/exploded-v2.1-pi-d4004.png`, `cad/pv_clean_rain_v21.blend`, `.glb`, `cad/pv_clean_rain_v21_explode_labeled.mp4`
- Powerbank-Foto: `assets/powerbank-goodaaa-d4004.jpg`
