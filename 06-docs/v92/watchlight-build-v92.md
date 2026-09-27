# v92 — WATCHLIGHT / BEACON, BUILD. STAGES 1-6 BUILT AND GATED on the staff branch (`sc-watchlight-fx`); blade 9.3, the design's, MEASURED; the clip is with Rick. Claude Code on yert.

Input: `WATCHLIGHT-BUILD-BRIEF.md` + `vigil-staff-design-v92.md` (Cowork). Builder `tools/watchlight_build.py` (on `tools/staffkit.py`), probe `tools/watchlight_probe.py`, voices `tools/watchlight_voice_lab.py`, picker `tools/_watchlight_pick.py`. Runs in `runs/build/`. Rick: "build them all".

```
sc-cipher-fx.html          the base: the staff branch's tip (Culverin, Briarwand, Cipher 1-6)
  -> sc-watchlight.html      stage 1  the relic, ult stubbed, the bow's arrow, ward 2.5   d63ea69ef05181ab
  -> sc-wardbolt.html        stage 2  WARDBOLT: the shove                               af8fed8fe8059b68
  -> sc-beacon.html          stage 3  BEACON: the lantern, charge 14                     2026a93e7a1bf509
     (stage 5: the blade is the design's 9.3, measured -- no link, nothing moved)
  -> sc-watchlight-fx.html   stage 6  picture, voices, the blade's note                  0fd579e1cd0df0d3
```

Engine names are all free: `f.ultBeacon`, `kind:"beacon"`, the lantern's shot flagged `lamp`. The relic carries Farwarden's `onSelf:{ ward:2.5 }` (the staff keeps the bow's bank, design "why this cell").

## Stage 0 on 151 — the lab reproduces (`stage0_*`)
A 6.4 / B 23.8 / S 19.1 / U 50.2% (block 2207; 2427: 5.9 / 23.2 / 19.7 / 48.6) against the brief's ~6 / ~23 / ~21 / ~50: 6.63 lantern shots a cast (6.67), 4.48 blows a window (4.52), shield 31.8 on a window frame (32.5).

## Stage 1 — arm B to the decimal (23.8%, 25.0 blows a fight against 25.04). engine_ab 6660/6660 on the 37.
The stage-1 relic is arm B, not arm A: it already carries the bow's ward 2.5 (§3.1's "fair baseline for the spell").

## Stage 2 — the shove, from the barrel
§5: "`spawnShot` copies `knock`". The lab set it from `fresh()`, AFTER the step a bolt was loosed on — the third staff whose lab tagged a new shot one step late (Briarwand's fan, Cipher's wall-stop) — so a bolt that landed on its first step shoved nothing there. On the lab's field the built spell reads **22.0%** against arm S's 19.1%; **with the lab's late shove put back (`watchlight_probe --labtag`) it reads 19.1% — arm S exactly.** Every landing shoves by exactly `knock` along the bolt's travel: **3583 of 3583** read off the foe's velocity on the write that follows `resolveHit` (an accessor on the foe, not a model of the rule). engine_ab 6660/6660.

## Stage 3 — Beacon. Probe 12/12, both sides, every foe (`stage3_probe.txt`)
The lantern is set down at the caster's centre; every lantern shot leaves it aimed at the foe with its numbers, every 1.2s of the window clock; it never fires outside a window or after a death; an ult beat a cast. 6.56 lantern shots a cast, 4.83 blows a window (2.21 the lantern's), shield 32.4 on a window frame; `maxLive` refused **0**. On the lab's field: **49.7% against arm U's 50.2%**, 6.61 lantern shots (6.63), shield 31.8 (31.8), 4.86 blows a window against 4.48 (the engine's longer window: the staff fires through it). **Charge 14 is the lab's 16** for this fighter: 4.39 casts a fight against 4.46. engine_ab 6660/6660.
**The probe was wrong twice before the build was**: "~4.5 blows a window" is the lab's `hitsInWin`, every blow in the window, not the lantern's (2.2); and 6 landings "banked nothing" were all against **Bulwarden, whose wall REFLECTS the blow inside the same call** and eats the plate just banked — the engine's shared rule, now classified rather than failed.

## Stage 5 — the blade is the design's 9.3, measured (`stage5_*`)
Both sides, two seed blocks, 1480 fights a row, no bisection: 9.1 → 46.2% (47.4/45.0), **9.3 → 49.4% (50.4/48.4)**, 9.6 → 51.2% (51.4/51.1). Nothing moves, so no link: the relic's note says so in stage 6's. Ladder at 9.3 (block 2207): bow 60, warhammer 58, flail 57, scythe 55, staff 48, greatsword 40, **twinblade 35** (the brief's ~35).

## Stage 6 — picture and voices (Rick's "you pick i overrule")
Voices (`stage6_voice_lab*.txt`, two rounds; round 1's chimes ran 0.25s against the design's 0.35 and each missed one rule narrowly): cast **SETDOWN** (a knock and a settle into an F6 chime, audible 0.35s), lantern shot **BRIGHTEST** (the staff's own release carried to 1520 Hz, 3 dB under it, a semitone a shot, 8.5 over seven), thump **DRUM** under a wardbolt's hit (its own arm, so no other relic's hit moves; 6 dB over the release on a phone, where the pure sine thump vanished), close **STAGGER2** (the chime reversed, 0.19s). The vigil head stays **A** (the cage lantern). The lantern is drawn off the fighter — an iron cage over its light in a ground ring, a flare on every shot, motes rising, guttering out over 0.4s — and **the staff's own cage goes dark while the lamp is on the floor**, relighting as it goes out. The wardbolt is a broad short bolt with a bright head and a streak; the lantern's shot the smaller bolt with a trail.
**Gates:** probe 12/12; shipped voices 4/4 inside the renderer's floor; render_ab 24/24 others identical + Watchlight's control differs 9/10; shell_identity 200/200; insert audit 24/24. **Clip:** `07-shorts/v92/beacon-window.mp4` (watchlight vs cindercleave, seed 4418, 4 lantern hits and 8 shoves in the window) — nobody has watched it.

## The last two gates
`stage6_engine_ab38.txt`: sc-beacon -> sc-watchlight-fx over all 38 **WITH Watchlight**, **7030/7030** — stage 6 is presentation. `stage5_verify.txt` (verify --n 40 at the shipped numbers): **10/13**. Watchlight **46.3%** (side B in every pairing), every relic 30-70% (Heartwood 31.6 .. Gloamwire 63.0). The reds:
- **the pairing ceiling, and Watchlight is its new worst: Lightkeeper/Watchlight 122.9s** — two ward relics, one of them the known four; Watchlight's own mean fight is ~78s (a turret and a bank make long fights). Accepted as before (Rick's ruling on the ceiling), and worth his eye.
- the overall-mean band (61.1s against 28-54), stale since the minute pace.
- **"both sides can win every matchup": Starwarden vs Watchlight 40/0** — the design's own prediction ("Worst Starwarden 0", §4). The other three pairings on that line (Heartwood v Twinshade, Axiom v Twinshade, Axiom v Bloodmirror, each 0/40) do not involve Watchlight, which moves none of them (6660/6660); a lopsided pairing's forty seeds are re-drawn when a relic joins the roster, and the check is zero-tolerance. Items 12/32, Rick's.

## Open
Rick's eye on the clip. Then Crozier, Bloodwick, Nightglass — check each lab for the one-step-late `fresh()` tagging.
