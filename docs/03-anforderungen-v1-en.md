# PV-Clean Rain — Requirements v1 (step 1 closed candidate)

**Method:** Musk step 1 — make requirements less dumb.  
**Owners:** Norbert (decider) · PV-Cleaner (challenger / scribe)  
**Date:** 2026-09-06

Every line has an owner. Design parts (discs, bogie, ESP32, lid solar, skirt) are **not** requirements.

---

## Mission

| ID | Requirement | Owner | Acceptance |
|---|---|---|---|
| M1 | After rain passes this season, **visible soiling is mostly gone** on glass the robot could reach | **Norbert** | Before/after photos; no kWh proof required for v1 |
| M2 | Wetting from **rain only** — no onboard water tank | **Norbert** | No tank/pump in v1 BOM |
| M3 | Slow, weather-opportunistic cleaning is acceptable | **Norbert** | Multi-day/week progress OK |

## Site (physics)

| ID | Requirement | Owner | Acceptance |
|---|---|---|---|
| S1 | Target array: Röötger **20.48 kWp**, **64×** IBC PolySol 320 (~**1640×992×40 mm**), Schletter, Limburg | **Norbert** | Matches as-built |
| S2 | Operate at actual **16°** Dachneigung | **Norbert** | Bench + roof at 16° |
| S3 | **Cross modules alone** (frames ~40 mm, gaps ~20 mm) without human repositioning | **Norbert** | Unattended multi-module traverse on wet 16° |
| S4 | **Do not fall** off array perimeter | **Norbert** | Edge hard-stop; no tether (see C3) |
| S5 | **Detect and route around** clamps/vents unattended — no climbing them | **Norbert** | Avoidance behavior in tests |
| S6 | **Self-park on module edge** when idle | **Norbert** | Park pose on outer edge between missions |

## Constraints

| ID | Requirement | Owner | Acceptance |
|---|---|---|---|
| C1 | Prototype **parts budget &lt; €200** | **Norbert** | BOM sum &lt; €200 |
| C2 | Survive **~1 week unattended on a charge** | **Norbert** | Sleep + wake for ≥1 rain window / week-class idle |
| C3 | **No tether** required for v1 | **Norbert** | Edge-stop only |
| C4 | Operable by Norbert without a robotics team | **Norbert** | Simple start/stop + status |
| C5 | Prefer low part count / COTS (within C1) | **Norbert** | Judged at delete/optimize steps |

## Explicitly later (not v1)

| Item | Status |
|---|---|
| Whole-season unattended once placed | **Later goal** (€200 won) |
| Measured yield / PR improvement | Not v1 |
| Theft / vandalism features | Out of scope |
| Overnight-only for shading | Rejected |
| Lid solar / nest solar | Not a v1 requirement (may return in delete/add-back) |
| Dual discs, bogie, ESP32, skirt | **Design**, not requirements |

## First-principles restatement

1. Dirt on wet glass at **16°** must be moved off by a cheap machine.  
2. The machine must **stay on** 64 framed modules and **not fall**.  
3. It must **cross seams**, **avoid clamps/vents**, **park on an edge**, and **live ~1 week per charge**.  
4. Parts **&lt; €200**.  
5. Success = **looks clean enough after this season’s rains**.

---

**Next Musk step (when Norbert accepts this sheet):**  
2 — **Delete** parts/processes from the v1 concept that aren’t forced by the table above.
