# v65 — THE MINUTE. Moving the mean fight from ~48s to ~60s, priced.

**2026-09-02, Cowork.** Rick: *"we also did some work to make fights last
longer. id really like to get the average closer to a minute. how do we
achieve that."*

**Status: CHOSEN, NOT BUILT.** Rick, 2026-09-02 (~21:10 UTC), picked
**S = H = 1.30** and ruled **accept the pairing ceiling, as before**. Nothing
in the chain has moved yet. §5 is the build, and it is Code's.

Runtime: **Cowork container, Chromium 141**, not the repo's pinned 151. The
reproduction control is in §1. `tools/pace_roster_probe.py` is the
instrument; `tools/pace_sweep.py` is the one it extends.

---

## 0. The lever is the one pace_build.py already pulled

`pace_build.py` (2026-08-29) took the mean from 37.3s to ~49s by scaling
**health and the clock together**: baseHP 300→400, seals 15/35 → 21/49, the
hall closing with the Second Seal, timeout 80→120, plus one nerf
(Grudgebearer). Its reasoning still holds and is the reason this is a scale
and not a knob: damage escalates on a wall clock (×1.00, ×1.35 at the Second
Seal, ×1.85 at the Third), so health alone spends the extra fight inside the
Third Seal at ×1.85 and changes the fight's *shape*. Scaling the seals with
the health keeps the proportions and changes the length.

So the question is only *how much*, and that was measured rather than
guessed.

## 1. Where it is today, roster-wide

`pace_roster_probe.py --game ../02-chain/sc-lastthree.html --cells 1.0:1.0 --n 3`
— every one of the 528 pairings on the 33-relic build the app loads, 3 seeds,
1,584 fights:

```
                       mean   med   p90    max   timeouts  ults/fight   worst pairing
today (400, 21/49)     47.5  47.7  60.3   79.9      0         4.2       Lightkeeper/Farwarden 77.7s
```

**Control:** `pace_sweep.py` at S=1 H=1 on its own ten pairings reads 47.6s
here against the 49.3s it published on 2026-08-29 (different build, 25
relics, Chromium 151). CLAUDE.md's roster mean at 26 relics was 49.2s. Within
what two readings of one arm come back apart; the runtime is declared above.

## 2. The grid

`pace_sweep.py --scales 1.0,1.15,1.3,1.45 --hp 1.0,1.15,1.3,1.45 --n 10`
(ten pairings, 100 fights a cell; the timeout is removed in this tool). S is
the clock scale (seals, hall, timeout), H the baseHP multiplier:

```
   S     H  baseHP  seal2  seal3    dur   p90  ults
 1.00  1.00    400   21.0   49.0   47.6  61.1   4.7
 1.00  1.45    580   21.0   49.0   59.6  77.6   6.1    health only
 1.15  1.30    520   24.1   56.3   59.4  74.2   6.0
 1.30  1.15    460   27.3   63.7   57.2  74.7   5.9
 1.30  1.30    520   27.3   63.7   61.6  79.0   6.3    same shape, scaled
 1.45  1.00    400   30.4   71.0   54.4  71.6   5.6    clock only
```

Duration goes roughly as scale^0.9 on the diagonal — not linear, because the
escalated acts still eat a growing share of the extra health.

## 3. The three cells that land, roster-wide

Same instrument as §1, all 528 pairings, timeout KEPT and scaled with the
clock so the timeout column can come back non-zero:

```
   S     H  baseHP  seals    t/o   mean   med   p90    max   t/out  ults   worst pairing
 1.30  1.30    520  27/64    156   60.1  59.7  75.7  107.5     0    5.5    Lightkeeper/Axiom 99.2s
 1.27  1.27    508  27/62    152   58.6  58.1  74.7  107.8     0    5.4    Farwarden/Axiom 104.9s
 1.15  1.30    520  24/56    138   58.0  57.6  73.6   98.1     0    5.3    Lightkeeper/Farwarden 96.2s
 1.00  1.45    580  21/49    120   58.7  57.3  73.5  108.0     0    5.3    Lightkeeper/Axiom 98.8s
```

**Recommendation: S = H = 1.30** — baseHP 520, Second Seal 27s (the hall
closes with it), Third Seal 64s, timeout 156. It is the only cell that reads
60 on the roster, and it is the same fight stretched, which is what "longer"
has meant in this project since pace_build.

What every cell costs, and none of it is optional to know:

- **The pairing ceiling gets worse, not better.** The four relics that
  already run over verify's 18-70s band — Lightkeeper, Axiom, Farwarden,
  Spellbreaker — now run to ~100s against each other. verify's thirteenth
  check was already red at 74.8s (CLAUDE.md §1, "accepted rather than
  fixed"); at 60s mean it is red by thirty seconds and the choice is the
  same one deferred last time: tune those four, or accept.
- **Ults per fight 4.2 → 5.5.** Charge is pure wall time, so a longer fight
  buys 1.3 more set-pieces for free. That is a change to the film's rhythm;
  it is probably the point, but it is not free of consequence for the
  director's cut bar when it comes back on.
- **The music bed renders `timeout + 6` seconds offline at every match
  start**: 162s against today's 126s. Same class of cost pace_build
  accepted at 130 against 90.
- **A `--full` clip of a mean fight is now a minute plus the open and the
  hold.** The posting pipeline films back from the kill with `--lead`, so
  the length of a posted short is a separate dial from the length of a
  fight — but "a short films ~45s of a fight" (CLAUDE.md) stops being the
  whole fight.

## 4. The balance drift, and who it is

Same 1,584-fight run at 1.30, per-relic roster winrate against today. n≈96
a relic, so **±5pp at 1σ**: this names who moved, it does not tune anyone.

```
 moves DOWN                  moves UP
 Ravelbone    63.5 → 43.8   Axiom        27.1 → 43.8
 Marrowdraw   62.5 → 46.9   Bloodmirror  49.0 → 61.5
 Aureole      65.6 → 56.2   Cindercleave 46.9 → 57.3
 Oathwound    40.6 → 31.2   Farwarden    54.2 → 63.5
 Redflail     54.2 → 44.8   Bulwarden    44.8 → 54.2
 Vesper       62.5 → 54.2   Censer       42.7 → 51.0
```

Nothing lands outside 30-70 at this sample and the spread narrows (38.5 →
32.3pp), which is the opposite of what pace_build met — but Ravelbone and
Marrowdraw at −16 to −20 and Axiom at +17 are three to four sigma and will
show up in `verify --n 40`. The direction is legible: relics whose damage is
front-loaded or bank-limited lose ground when the pool is 30% deeper; relics
that scale with time or with the foe's hits gain it. Oathwound at 31% is one
bad reading from the floor.

**Expect verify to want two or three damage touches**, the way pace_build
wanted Grudgebearer's. Which ones is verify's to say on the pinned runtime,
not this document's.

## 5. What Code builds

A `pace60_build.py` in the shape of `pace_build.py` — anchored edits, refuses
if the source already carries them, syntax-checks its output, asserts the
upstream inserts survive — from the link Rick names (the app loads
`sc-lastthree`; the chain tip is `sc-static` with Arclight stage 4 stopped
on a ruling, so the pace change has to land on whichever link is going to
carry forward, and that is a chain question for the session that builds it):

```
combat.baseHP        400 → 520
SECOND SEAL          t: 21 → 27      collapse.startT 21 → 27, with it
THIRD SEAL           t: 49 → 64
timeout              120 → 156       backstop, not a win condition
```

Then, none of it optional:

```
python verify.py --game <out> --n 40           THE gate; expect the duration band red as before
python engine_ab.py --a <src> --b <out> --n 9  EXPECT A DIFF
python pace_roster_probe.py --game <out> --cells 1.0:1.0 --n 3   should read ~60 on Chromium 151
```

and a fight watched end to end in the app before anyone calls it done —
film before you tune, if the ultimate is a picture, and this changes every
picture's length.

## Decisions

1. **Which cell — RULED: 1.30 / 1.30.** baseHP 520, seals 27/64, the hall
   closes at 27s, timeout 156. (1.15/1.30 was offered — three seconds
   earlier collapse, worst pairing under 100s, two seconds less mean — and
   not taken.)
2. **The pairing ceiling — RULED: accept, as before.** Lightkeeper, Axiom,
   Farwarden and Spellbreaker run to ~100s against each other; verify's
   thirteenth check stays red and known, the same call pace_build made.

## Open decision

3. **Which link carries it** — the app's `sc-lastthree`, or the Arclight
   chain that is stopped at stage 4. Not asked yet; it is the building
   session's question and depends on the Arclight ruling.

## 6. The clip pipeline, checked against a minute (2026-09-03)

Rick: *"how about the clip maker on the app? will it hold up to the longer
videos?"* Read end to end: app `Create Short` -> `shorts_build.py` ->
`cinema_clip.py`. Three findings, two of them fixed in the same session:

- **`shorts_build.py` gated delivery on `dur < 60.0`** — the Shorts limit
  from the day it was written. A whole fight delivers at the fight plus ~8s
  of open and verdict tail, so a 60s mean would have failed nearly every
  whole-fight short. Worse, the check sat inside the limiter ladder: a
  length-only failure walked all three rungs, shipped at 0.50 / −4 dBTP (a
  mix nobody chose), retained `_clip_frames`, exited 1, and the app showed
  a failure with a misleading reason line. **Fixed:** `MAX_SECONDS = 180`
  (the platform's — Rick's pick, 2026-09-03) and only the two loudness marks
  climb the ladder (`LADDER_MARKS`). Falsified against the original with
  ffmpeg stubbed: original walks 3 rungs on a length-only fail; edit stops
  at 1 and still climbs on a real true-peak fail.
- **`cinema_clip.py` capped a `--full` capture at a bare 150s of video.**
  1.25x the timeout it was written against; at timeout 156 the longest
  pairings (~108s match) would have sat one dilation from "no ending, do not
  ship". **Fixed:** `cap = AC.CONFIG.timeout * 1.3 + 16`, read off the page
  (172 today, 219 at the v65 cell).
- **Everything else is linear.** Frames go to disk one at a time, the bed is
  sized off `CONFIG.timeout`, the app puts no timeout on the job. A whole
  fight goes from ~2,800 frames / 3–4 min to ~4,000 / ~5 min; a worst
  pairing ~7,000 / ~8 min. The lead path (default 18s, max 40) is untouched.

The app's note beside the Whole-fight box now says 180s. `main.js`'s
"1,400–2,800 frames" comment is stale by the same ratio and was left.
