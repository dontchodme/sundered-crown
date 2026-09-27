# v97 — DAWNBRINGER / DAYBREAK, BUILD. IN PROGRESS: stages 1-2 done at charge 14 (blade 10.4 confirmed); stage 3 (picture, voice, field) next. Claude Code has it.

Claude Code on **DESKTOP-DERRAFT**, claimed 2026-09-27 01:35 UTC (`CLAIMS.md`, the BUILD row
under Daybreak's). The input is `06-docs/v86/dawnbringer-daybreak-redesign-v86.md` §5 with its
§7 rulings, and nothing else (rule 0). Builder `tools/dawn_build.py`, probe
`tools/dawn_probe.py`. (v89-v96 are the staff row's, claimed by Cowork, hence v97.)

```
sc-corollary-c14.html   the base: the chain tip (sc-leaf + Axiom / Corollary stages 1-6)
  -> sc-dawn.html          stage 1  the dawn; the sparks out     dawn_build --stage 1   fa8703a2e143f59d
                           stage 2  the blade                    10.4 CONFIRMED at charge 14 -- no link
```

## 0. What this build stands on

**The base is the chain tip**, asserted by the builder: the Winnowing's rung stop, Corollary's
`echoShown` and its stage-5 apply fix. (The claim said `sc-corollary-fx`; Corollary's stage 5
landed before stage 1 was built, so the tip moved to `sc-corollary-src`.) The v86 pricing was
on `sc-trunk`; since then Axiom's ultimate changed and Thornshear's kunai lost their hit stop,
which reaches 2 of Dawnbringer's 33 pairings. Stage 0 below is run on this base, and the gates
read against it.

**Rick's rulings** (v86 §7): **charge 16** (the doc did not state it; 16 is what it was priced
at, and the shipped Daybreak was 14). The heal and the line speed are built **as written**: no
heal, and the full floor-to-ceiling rise.

**The readings the build had to make** (in `dawn_build.py`'s docstring):
1. **The tick's cadence is the lab's:** a 0.5s cooldown that runs through the whole window
   and fires on the first lit frame it is clear.
2. **`apply`'s source is a side letter.** §4 and the lab pass the Fighter, but the engine's
   contract is "a"/"b", and smite ticks damage, so a fatal smite tick is attributed by it.
3. **"No beat" for a tick, except the tick that KILLS**, which files its own `fatal` hit beat.
   That is the engine's standing rule for every side-channel kill (Scour's ticks: "ticks file
   nothing, the fatal one does"), and without it a fight won on the dawn has no killing blow.
4. **H is `CONFIG.arena.h`**, the full hall, as the lab reads it. After the hall starts
   closing, the line starts below the visible floor for up to ~1.4s; the lab priced exactly
   that.

**The clock** is the window tickers' (it stops through a hit stop), as for Corollary. The lab
counted every step.

## 1. Stage 0: the control on 151, on sc-corollary-src

`ult_overlay.py --relic dawnbringer --mech overlays/dawn.js --seeds 20`, seed0 2207 and 2317,
660 fights an arm a block:

```
arm                          published 141 (330)   151: block 1   block 2   pooled (1320)   lit    ticks  dmg / cast
A     no ultimate            13.6%                  14.8           17.0      15.9
SHIP  the sparks             57.0%                  58.0           57.9      58.0
B     the dawn (the lab)     54.8%                  54.5           52.4      53.5           60.3%  9.91   19.8
```

The control reproduces within the batch's tier; the dawn's mechanism reproduces to the digit
(published: lit 61%, 10.0 ticks, 20.0 damage a cast).

## 2. Stage 1: the dawn, the sparks out — `sc-dawn.html`

`dawn_build.py --stage 1 --src ../02-chain/sc-corollary-src.html --out ../02-chain/sc-dawn.html`:
src `82433ea61c9701b6`, out `a3fde3a7869fde65`, +3261 characters. Five anchored edits:
- Dawnbringer's ult block (`kind:"dawn"`, charge 16, dur 8, tick 0.5, tickDmg 2, smite 1, the
  doc's 72-character card);
- `ultDawn`/`dawnTally` on the fighter;
- the `kind === "dawn"` cast branch, which opens the window and resolves nothing;
- `tickDawn` beside `tickEcho` among the window tickers;
- `tickDawn` itself.

**The sparks are out by construction.** No relic carries `kind:"radiant"` any more (the builder
refuses otherwise), so nothing sets `ultRadiant` and the spark spawn in `resolveHit` is
unreachable. The spark machinery stays for Lastlight's Harrowing.

**Probe, `dawn_probe.py --game ../02-chain/sc-dawn.html`: 9/9** (396 fights, Dawnbringer on both
sides). Per cast: 9.95 ticks, 19.9 damage, foe lit 59.5% of the window, 2.83 casts a fight
(the lab: 3.3, the frozen-clock effect). 14 killing ticks, each with its fatal beat; 182 wards
broken by a tick. Dawnbringer threw no spark.

### 2a. At charge 16 the dawn came in 10 under the sparks, and the reason was the clock

The first build of stage 1 (on sc-corollary-src, charge 16; `runs/charge16_*`) read **49.8 / 46.8,
pooled 48.3%** at blade 10.4. That is 5 under the lab's arm B and 10 under the sparks. The
probe showed why: **2.83 casts a fight against the lab's 3.3.** The blade curve at charge 16
(pooled 1320): 10.4 → 48.3, 11.2 → 51.0, 12.0 → 58.9, 12.8 → 63.7. Parity with the sparks
would have taken ~12.0.

Corollary had shown the same thing (v88 §4), so it was put to Rick once, for the batch: the
lab's charge counts hit-stop freezes and the engine's does not. Measured before asking, on
scratch copies at charge 14: Daybreak 52.5% at 10.4 (the lab: 53.5%), Corollary 40.0% at 7.42
(the bolt: 40.2%). **Rick, 2026-09-27: "Use the game's equivalent"** — the lab's 16 is the
engine's 14, and the weapons stay as designed. Corollary took it as its stage 6
(`sc-corollary-c14`), and this build was rebuilt on it at charge 14.

### 2b. Stage 1 at charge 14 — `sc-dawn.html` (the link of record)

`dawn_build.py --stage 1 --src ../02-chain/sc-corollary-c14.html --out ../02-chain/sc-dawn.html`:
src `3fc6ec27a5298615`, out `fa8703a2e143f59d`, +3261 characters. The same five edits at
charge 14.
- **Probe: 9/9** (`runs/dawn1_probe.txt`). 9.88 ticks, 19.8 damage a cast, foe lit 58.9%, and
  **3.30 casts a fight: the lab's exactly.**
- **engine_ab sc-corollary-c14 → sc-dawn, the 33 others, n=8: 4224/4224**; Dawnbringer + 8:
  64/288 differ (its 8 pairings × 8 seeds, the pass).
- **The relic at 10.4: 53.2 / 51.2, pooled 52.2%** (`runs/dawn1_built_*`), against the lab's
  arm B at 53.5%. In tier.

## 3. Stage 2: the blade — 10.4 CONFIRMED

v86 §5: "confirm 10.4 wide on 151". At charge 14 the built dawn reads 52.2% against the priced
arm B's 53.5%, inside the tier, so the blade stays at 10.4 and no link is written. (The design's
own "parity with SHIP ±3" does not hold even in its lab on 151: arm B 53.5 against the sparks'
58.0. Rick's ruling is to land where Cowork priced, and it does.)

**verify --n 40 on sc-dawn: 10/13** (`runs/verify_dawn.txt`). Dawnbringer 53.8% (54.2% before
the build); every relic in 30-70% (Heartwood 35.0 .. Gloamwire 63.9). The reds are the two
clock bands and sc-leaf's own Axiom vs Thornshear 0/40.
