# v117 — THE BATCH'S BALANCE PASS: every batch blade to the point nearest 50%, on the roster the game will carry

**Rick, 2026-09-29, after the designs and most of the builds:** "you pick the blades. do whatevers best for
balance." This pass is that. Every batch relic's blade goes to the measured point whose win rate BOTH SIDES
is nearest 50%. That replaces each design's own blade target (the shipped rate, "confirm 9.17", "Rick's
target") and the builds' earlier picks. Claude Code on DESKTOP-DERRAFT, claimed 2026-09-30 (`CLAIMS.md`).

- **The link:** `02-chain/sc-balance.html`, on the batch line's tip `sc-goreshard-fxout`. It moves eleven
  numbers (the eleven relics' `dmg`) and nothing else, each with a comment saying where it came from.
- **The builder:** `tools/balance_build.py`. Its `BLADES` table is the numbers' only home.
- **The measurements:** `tools/balance_sweep.py`, driving `tools/relic_rate.py`. Runs are in `runs/`.

## 0. The roster it is measured on

Balance is measured where the game will be, not on the batch line alone. When Rick passes the batch, GAME
moves to the batch tip with yert's seven staves carried onto it (`staff_carry.py`). The Daybreak on the
batch line is the LINE, which "does not ship"; Rick's CIRCLE (yert's `sunrise_build.py`, v99) replaces it.
So the measuring roster, built IN SCRATCH only (`make_roster.sh`), is:

  the batch tip -> the circle (sunrise_build.py stages 1, 3, 5) -> the seven staves (staff_carry.py) = **49 relics**

Nothing of yert's is committed as a link here: both builders are run into scratch to measure on.

**In scope:** the nineteen v68-v86 designs' relics, less Dawnbringer. Its blade (10.4) belongs to the
circle, and the circle's build confirmed it at about 50% (48.9% / 50.4%, v99). That leaves eighteen. The
base roster's other relics and the staves are not the batch's, and are not moved.

## 1. The method

**One measurement** is `relic_rate.py`:
- the relic against all 48 others, the same seeds from BOTH sides;
- n = 10 seeds per foe per side, on two seed blocks (2207 and 2317), pooled: 1920 fights;
- about 1.1 points of standard error.

**Per relic** (`balance_sweep.py`):
- measure at the current blade;
- if it is not within the tolerance of 50, step: first from the roster's typical sensitivity, then by
  secants through the nearest measured points, rounded to quarters;
- the pick is the MEASURED blade nearest 50, never an interpolated number.

`--set dmg=` mutates the relic's own row live and restores it, so one page state is measured throughout.

**Two rounds, because blades interact:**
- **Round 1:** every relic measured on the tip's roster, tolerance 1.0 point, up to four measurements.
- **Round 2:** the eleven round-1 moves applied together in a scratch link (`sc-balance-r1`), the 49-relic
  roster rebuilt on it, then all eighteen re-measured, tolerance 1.5, up to three measurements.

Round 2 moved one more relic, Bindweed, from 18.75 to 19.0. The final blades are round 2's picks.

## 2. The numbers

| relic | blade on the tip | rate there | round 1: measured (blade -> rate) | round 2 on the round-1 roster | FINAL blade | final rate (round 2) |
|---|---|---|---|---|---|---|
| Axiom / Corollary | 7.42 | 37.7% | 7.42 -> 37.7, 9.25 -> 52.2, 9 -> 49.9 | 9 -> 50.5 | **9** | 50.5% |
| Morningstar / Zenith | 24.03 | 46.0% | 24.03 -> 46.0, 26.5 -> 51.7, 25.75 -> 50.7 | 25.75 -> 49.7 | **25.75** | 49.7% |
| Ironwood / Canopy | 24 | 50.9% | 24 -> 50.9 | 24 -> 50.7 | 24 (stays) | 50.7% |
| Portcullis / Onslaught | 23 | 50.3% | 23 -> 50.3 | 23 -> 49.2 | 23 (stays) | 49.2% |
| Bindweed / Tendril | 18 | 46.0% | 18 -> 46.0, 19.75 -> 55.4, 18.75 -> 48.4, 19.25 -> 53.2 | 18.75 -> 48.4, 19.5 -> 54.1, 19 -> 50.7 | **19** | 50.7% |
| Coldiron / Temper | 9.3 | 49.1% | 9.3 -> 49.1 | 9.3 -> 48.5, 9.75 -> 55.3, 9.5 -> 52.3 | 9.3 (stays) | 48.5% |
| Ironhail / Quarrelstorm | 16.23 | 59.1% | 16.23 -> 59.1, 12.5 -> 34.5, 14.75 -> 49.9 | 14.75 -> 50.2 | **14.75** | 50.2% |
| Lodestone / Rebuttal | 20.5 | 52.2% | 20.5 -> 52.2, 19.5 -> 46.7, 20 -> 48.3, 20.25 -> 50.9 | 20.25 -> 51.0 | **20.25** | 51.0% |
| Widowmaker / Exsanguinate | 10.75 | 45.8% | 10.75 -> 45.8, 11.75 -> 53.2, 11.25 -> 51.4 | 11.25 -> 50.5 | **11.25** | 50.5% |
| Oracle / Foresight | 10 | 50.9% | 10 -> 50.9 | 10 -> 51.5 | 10 (stays) | 51.5% |
| Angelus / Ascension | 9 | 50.2% | 9 -> 50.2 | 9 -> 49.3 | 9 (stays) | 49.3% |
| Lightkeeper / Bulwark | 9.5 | 49.6% | 9.5 -> 49.6 | 9.5 -> 49.9 | 9.5 (stays) | 49.9% |
| Censer / Consecration | 25.5 | 47.4% | 25.5 -> 47.4, 27.25 -> 53.9, 26.25 -> 51.4, 26 -> 50.2 | 26 -> 50.4 | **26** | 50.4% |
| Aureole / Benediction | 12.5 | 53.5% | 12.5 -> 53.5, 11.5 -> 46.1, 12 -> 49.0 | 12 -> 49.5 | **12** | 49.5% |
| Spellbreaker / Unmaking | 7.5 | 53.1% | 7.5 -> 53.1, 7 -> 48.0, 7.25 -> 50.9 | 7.25 -> 50.8 | **7.25** | 50.8% |
| Heartwood / Rootfast | 11 | 53.6% | 11 -> 53.6, 10 -> 47.0, 10.5 -> 49.8 | 10.5 -> 50.2 | **10.5** | 50.2% |
| Thornwake / Bramblesnare | 26.5 | 49.6% | 26.5 -> 49.6 | 26.5 -> 49.3 | 26.5 (stays) | 49.3% |
| Goreshard / Bloodprice (id oathwound) | 10.25 | 52.6% | 10.25 -> 52.6, 9.5 -> 48.3, 9.75 -> 49.1 | 9.75 -> 48.8 | **9.75** | 48.8% |

**All eighteen now read 48.5-51.5% both sides** on the roster the game will carry. Before this pass they
spread from 37.7% (Axiom) to 59.1% (Ironhail).

Round files: `runs/round1.txt`, `runs/round2.txt`, and `runs/round3_final.txt` (the final link's roster,
§3).

## 3. The gates

The link is `02-chain/sc-balance.html` (sha16 dcc2f046ae28562f), on `sc-goreshard-fxout`, with 11 blades.

- **engine_ab, the tip against the balance link, over the 31 relics it does not touch, n=6: 2790/2790
  identical** (`runs/engine_ab_untouched.txt`). Only the eleven re-bladed relics' fights move.
- **The final numbers, on the roster built on THIS link** (`make_roster.sh` onto `sc-balance`, 49 relics,
  `runs/make_roster_final.txt`; `runs/round3_final.txt`, one measurement each at the final blade): **all
  eighteen at 48.7-51.4% both sides** (coldiron lowest, oracle highest).
- **yert's staff carry** applies onto the balance link (all seven staves, every stage), as part of that
  roster build.
- **verify --n 40 on `sc-balance` (42 relics, the batch line alone): 10/13** (`runs/verify_balance.txt`).
  - Every relic is inside 30-70% (Nightfell 40.4 .. Gloamwire 64.0).
  - The reds are the two clock bands, red on every link since the minute pace, and "both sides can win
    every matchup": Spellbreaker v Bloodmirror 0/40, Bloodmirror v Ironwood 40/0, Lodestone v Angelus
    0/40.
  - **Those three were near one-sided BEFORE this pass.** relic_rate on the tip and on the balance link,
    n 20 a side (`runs/pairs_before_after.txt`):
    - Ironwood v Bloodmirror: 2.5%, then 2.5%;
    - Spellbreaker v Bloodmirror: 7.5%, then 7.5%;
    - Lodestone v Angelus: 2.5%, then 0.0% (Lodestone's blade went 20.5 -> 20.25).
  - They are hard counters, like Lightkeeper v Marrowdraw, which Rick accepted (2026-09-29: "i think im
    fine with lightkeeper countering marrowdraw"). They are recorded, not tuned out.
  - verify's per-relic rates on the 42-relic line read lower for the new relics (e.g. Lodestone 44.8%)
    than the balance numbers. verify plays each pairing i < j, so an appended relic is side B in every
    pairing and never meets the staves or the circle. The balance numbers are both sides, on the roster
    the game will carry.
- **tip_audit** exit 0 (`runs/tip_audit_balance.txt`).
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the pointer not moved, the json restored;
  `runs/shell_identity.txt`).

## 4. The type spread (CLAUDE.md items 12 and 32), measured -- and why no blade moves for it

Items 12 and 32 say `verify`'s per-relic band cannot see a relic that loses one weapon type and crushes
another (Thornshear 43.6pp, Shroudmaul 40.1pp). Rick left it to Code (2026-09-29: "the rest of that stuff
looks like stuff for you"). Here is each batch relic's win rate BY FOE TYPE on the game roster (the
final link's 49; `type_spread.py`, relic_rate both sides, n 10, block 2207, 960 fights a relic, about
140 a type, so about 4pp of noise a cell; `runs/type_spread.txt/.json`):

| relic | overall | worst foe type | best foe type | spread |
|---|---|---|---|---|
| Lightkeeper | 49.2% | warhammer 22.1% | staff 88.6% | 66.4pp |
| Angelus | 49.8% | twinblade 16.7% | warhammer 82.9% | 66.2pp |
| Heartwood | 50.7% | warhammer 25.7% | greatsword 83.3% | 57.6pp |
| Axiom | 50.1% | warhammer 22.9% | staff 76.4% | 53.6pp |
| Bindweed | 51.5% | bow 30.0% | greatsword 82.9% | 52.9pp |
| Spellbreaker | 50.6% | scythe 27.9% | staff 71.4% | 43.6pp |
| Lodestone | 50.9% | warhammer 36.7% | greatsword 74.3% | 37.6pp |
| Thornwake | 50.5% | bow 35.0% | greatsword 70.7% | 35.7pp |
| Ironwood | 50.4% | flail 42.9% | greatsword 78.6% | 35.7pp |
| Goreshard (oathwound) | 48.8% | warhammer 35.7% | staff 70.0% | 34.3pp |
| Oracle | 52.1% | greatsword 42.1% | staff 74.3% | 32.1pp |
| Censer | 51.8% | bow 39.3% | greatsword 70.7% | 31.4pp |
| Morningstar | 49.8% | bow 31.4% | greatsword 62.9% | 31.4pp |
| Coldiron | 48.5% | warhammer 29.3% | greatsword 60.7% | 31.4pp |
| Ironhail | 52.2% | greatsword 32.9% | flail 63.6% | 30.7pp |
| Aureole | 49.6% | greatsword 33.6% | warhammer 60.0% | 26.4pp |
| Portcullis | 48.4% | bow 38.6% | greatsword 63.6% | 25.0pp |
| Widowmaker | 50.7% | greatsword 41.4% | staff 57.9% | 16.4pp |

**The call, Code's under that ruling:**
- **A spread is a relic's matchups, not its balance.** Every one of these relics is at 50% overall, and
  the spread comes from its design: what its ultimate and its weapon beat.
- **Tuning a spread out is redesigning, and rule 0 forbids it.** The blade scales every matchup at once
  and cannot flatten one. Changing a type matchup means changing a mechanic, which is Cowork's and Rick's.
- **So this pass records the spreads and moves nothing for them.** This is the same stance as Lightkeeper v
  Marrowdraw, which Rick accepted as a counter.
- **Five relics spread over 50pp:** Lightkeeper, Angelus, Heartwood, Axiom and Bindweed. That is wider
  than the Thornshear and Shroudmaul cases that opened items 12 and 32.

**Staff is the best foe type for 6 of the eighteen** (Axiom, Widowmaker, Oracle, Lightkeeper, Spellbreaker, Goreshard (oathwound)). The staves are
yert's row, balanced on yert's line, which has none of the batch's relics. Their rates on the 49-relic
roster come from verify on the candidate (§5). Their blades are yert's cells, not this pass's.

## 5. The game candidate: `02-chain/sc-candidate-49.html`

The roster the balance was measured on, placed on the chain so Rick can watch it and GAME can move to it.
It is `sc-balance` with Rick's Daybreak circle (`sunrise_build.py` stages 1, 3, 5) and yert's seven staves
(`staff_carry.py`) carried on, built by `make_roster.sh`: **49 relics, sha16 c4a9cd44693eb136**. Byte for
byte, it is the roster of the final check in §3. GAME is NOT moved: that is Rick's.

Gates (`runs/candidate/`):
- **shell_identity 196/196** (app Chromium 152 vs headless 151; the json restored).
- **tip_audit** exit 0.
- **verify --n 40, all 49 (1176 pairings, 47,040 fights): 10/13.**
  - Every relic is inside 30-70% (Vinesower 40.3 .. Gloamwire 63.1). The eighteen batch relics read 47-52%
    here, side B in every pairing; the staves read 45.5-51.4.
  - The reds: the two clock bands, red on every link, and "both sides can win every matchup", with six hard
    counters at 40/0:
    - Spellbreaker v Angelus 40/0;
    - Lodestone v Angelus 0/40;
    - Angelus v Nightglass 40/0;
    - Heartwood v Ironwood 0/40;
    - Lightkeeper v Nightglass 40/0 (on yert's line already: Nightglass's named counter, items 12/32);
    - Lightkeeper v Bloodwick 40/0.
  - They are matchups (§4), not blades, and they are FOR RICK before GAME moves. He accepted Lightkeeper v
    Marrowdraw as a counter; these six are the same kind, and the go-live call is his.

## 6. What it means for the docs before this one

Each relic's build doc records the blade its build picked. Those numbers stay as history: the link that
decides the blade on the chain is this one. A relic's probe that pins its build's blade
(several take it from their builder) will read that one check as moved on `sc-balance`, by design. The
mechanisms are untouched: this link changes eleven numbers and no code.

## 7. LIVE -- 2026-09-30

Rick, having been shown the six hard counters: **"go live"**.
- `app/main.js` GAME: `02-chain/sc-nightglass-fx.html` -> **`02-chain/sc-candidate-49.html`**.
- **shell_identity on the moved pointer: 196/196** (`runs/live/game_app_identity.txt`,
  `runs/live/game_shell_identity.txt`). The app's json is committed with the move, as the staff row's move
  did.
- The staff row stays in the game: it is carried in by `make_roster.sh`.
- **The rule from here:** a new link on the batch line reaches the game only by re-running
  `make_roster.sh` on the new batch tip (the circle + the staves). A GAME move to a bare batch link would
  take the staves and the circle out.
