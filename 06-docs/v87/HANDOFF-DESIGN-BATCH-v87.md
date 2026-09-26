# THE DESIGN BATCH — nineteen ultimates designed by Cowork on 2026-09-26, handed off whole. READ THIS BEFORE BUILDING ANY OF THEM.

**Rick, 2026-09-25:** *"how do you feel about designing the rest of the fighters yourself?"* → *"Nothing — you run it all."* **2026-09-26:** *"can we also redesign some of the old fighters to bring them up to the new standard?"* → open cells first, then the redesigns → *"do it all. we will hand off the whole thing at once."*

This is the whole thing. **Nothing is built.** Every design is claimed in `06-docs/CLAIMS.md` as `DESIGNED, AWAITING RICK'S VETO — THEN CODE'S`. Rick has read none of them; the first thing that happens after this lands is his veto pass, cell by cell, and only the survivors are Code's to build (rule 0 as ever: Code builds from the doc and does not design; a vetoed cell goes back to Cowork).

## The eight open cells — THE GRID IS FULL (42 of 42)

```
#   cell                     fighter / ultimate           the sentence                                                            body → whole (Chromium 141)      blade      doc
35  verdant x flail          BINDWEED / TENDRIL           the chain becomes a vine that hunts the foe, bites, and roots it        1.5% → 54–56% at 19             ~18        06-docs/v68/
36  verdant x warhammer      IRONWOOD / CANOPY            the hammer roots itself and grows into a three-boughed tree            14.5% → 47% at 23.5 (54 at 25)   ~24        06-docs/v69/
37  runic x warhammer        LODESTONE / REBUTTAL         the walls are runed: touch one and you are hexed and hurled back        21.4% → 57% at 23.5 (50 at 22)   ~22        06-docs/v70/
38  sanctified x flail       MORNINGSTAR / ZENITH         the head is a sun; its light smites, and each burn heals the bearer     7.6% → 50% at 24.03              24 (kept)  06-docs/v71/
39  vigil x flail            PORTCULLIS / ONSLAUGHT       the ball is the weapon: it charges, slams for the shield, banks more   28% → 54% at 24.03               ~23        06-docs/v72/
40  dwarven x twinblade      COLDIRON / TEMPER            the blades are cold iron: it wins its binds, each win sunders past cap 35% → 50% at 9 (cap 9)           ~9.3       06-docs/v73/
41  sanctified x twinblade   ANGELUS / ASCENSION          it rises; its blades are shafts of light; each hit heals               28.5% → 63% at 11.95 (54 at 10)  ~9.3       06-docs/v74/
42  runic x bow              ORACLE / FORESIGHT           every arrow flies to where the foe will be; each hit hexes twice        31% → 73% at 16.23 (51 at 12)    ~12        06-docs/v75/
```

## The eleven redesigns — each priced against the shipped ultimate (arm SHIP)

```
relic / ultimate            was                     now                                                              SHIP → new (same blade)   blade      doc
Widowmaker / Exsanguinate   nova + 3 bleed          the foe's bleed drains into her                                  46 → 57                   ~10.7      06-docs/v76/
Lightkeeper / Bulwark       nova + knock            a wall of light ahead of the sword; blocks bank ward             48.5 → 61                 ~9.5       06-docs/v77/
Censer / Consecration       nova + 3 smite          holy ground where each blow lands; smites foes, heals Censer     50 → 58                   ~26.5      06-docs/v78/
Spellbreaker / Unmaking     bolt + 3 hex            hex stuns last twice as long; every hit hexes twice              50 → 55                   ~8.4       06-docs/v79/
Axiom / Corollary           bolt + 3 hex            every blow is followed by its corollary, hexing                  40 → 38 (parity)          7.42       06-docs/v80/
Goreshard / Bloodprice      beam + 3 bleed          blows hit +30% per bleed stack on the foe                        38 → 42                   9.17       06-docs/v81/
Aureole / Benediction       beam, heals 28          a halo: foes inside smitten; she is blessed while one is         55.5 → 69                 ~14        06-docs/v82/
Ironhail / Quarrelstorm     arrow nova              iron hail drops on the foe; each landing sunders                 56 → 61.5                 ~15.3      06-docs/v83/
Thornwake / Bramblesnare    1.6s root               brambles where each blow lands; root on entry, bite inside       48 → 60                   ~29        06-docs/v84/
Heartwood / Rootfast        1.3s root               every blow roots the foe 1.0s, ball and weapon                   40 → 56 (the floor lifts) Rick's     06-docs/v85/
Dawnbringer / Daybreak      sparks, heal            a dawn line climbs the hall; foes below it are smitten and burn  57 → 55 (parity)          10.4       06-docs/v86/
```

## How they were made, and what to trust

- **One harness**: `tools/ult_overlay.py` + a JS module per mechanic in `tools/overlays/`. It is `vine_price` / `ring_price` / `storm_price` lifted out. Every run is in `06-docs/vNN/runs/`. **Chromium 141.0.7390.37 in a Cowork container — NOT the pinned 151.** Every decimal in these nineteen documents is on the other runtime; every brief's stage 0 is the reproduction control on 151, and every gate reads against that run and never against the published decimal (v64 §3aa: 7.8pp between the two).
- **Every open cell's arm A reproduced `cell_ults_on`'s ults-on body to the fight** (the identical fight, same seeds). Every redesign's arm SHIP is the shipped relic with its ultimate live — the thing the redesign has to beat or match.
- **n = 330 an arm for the sweeps, 660 for the settled numbers, two seed blocks where the blade was near the line.** Tiers, not decimals (v60 §2): under ~5pp at 660 is not a difference. Blades are estimates from two or three points; **every build settles its blade wide, both sides, two blocks, on 151, and never by bisection** (v48/v56/v66).
- **What held across all nineteen** (write it down once): the ultimates that pay are the ones that put the school's status on the foe CONTINUOUSLY (v59 §2, confirmed nineteen times — Lodestone's hex from the walls is +32 of its +36; Portcullis's bank is +20 of +26; the bites and roots and canopies are +5 each); anything hung off a flail's head meets the foe 4–20% of a window (v68 §3, v69 §3, v71 §3, v72 §3); seeking is the strongest property in the game on every type that gets it (Tendril +41, Foresight +37, the greatsword's own +50 in August); and the ceiling is a hiding place (Angelus at the top of the hall read 85% by being unreachable, and was moved down).
- **Names are Cowork's** (Rick: "nothing — you run it all"). Every doc has the spread of four they came from. The eleven redesigns keep Rick's fighter names and their ultimate names where the name already meant the new thing (Exsanguinate, Corollary, Rootfast, Bulwark, Consecration, Unmaking, Bloodprice, Benediction, Quarrelstorm, Bramblesnare, Daybreak — all eleven kept).
- **Art and sound are specced, not rendered.** Rule 2's spreads happen at each build's last stage; the specs say what register to render and what number to pick on. Three of the nineteen are sanctified light (Zenith, Ascension, Daybreak) plus Consecration's floor and Benediction's ring — §4.1b/c's bloom gates are written into each of them as numbers.

## The order to build, if the vetoes leave the order alone

1. **The parity swaps first** — Axiom / Corollary and Dawnbringer / Daybreak change no blade and replace a v5 one-liner each; they are the cheapest way to see whether a Cowork-designed ultimate reads.
2. Then the three cells whose blades stay in place: **Morningstar** (24), **Ironwood** (~24), **Portcullis** (~23).
3. Then the rest of the open cells: Bindweed, Lodestone, Coldiron, Angelus, Oracle.
4. Then the remaining nine redesigns in feed order (the worst feeds first): Exsanguinate, Bulwark, Quarrelstorm, Consecration, Benediction, Unmaking, Rootfast, Bramblesnare, Bloodprice.

Each is its own claim row, its own brief, its own stage-0 control. **One at a time; the chain is one chain.**

## What this batch did NOT do

- It did not touch the build. `sc-trunk` is the build of record and `sc-leaf` still waits on Rick's eye (v67).
- It did not settle a single blade. Every blade above is a bracket.
- It did not render a single frame or a single voice.
- It did not answer open item 12/32 (the type spread) — it added fifteen data points to it, including the first relic whose counters are the FAST ones (Angelus: twinblades 19%, hammers 81%).
- It did not decide N. The grid is full at 42; whether that was ever the roster size is Rick's.
