# v53 STAGE 2 — GRASP. The chain lengthens and the hands come off it, the design's headline claim is false on the built relic, and half of Gravemourn's kills were invisible to the camera.

**2026-08-31, Claude Code.** The build of `06-docs/v51/hands-v51.md` under the
plan in `06-docs/v51/umbral-build-brief-v51.md` §3. Stage 1 and 1b are in
`curse-build-v53.md` beside this.

```
in    02-chain/sc-curse.html          27 relics, curse remembers
out   02-chain/sc-gravemourn.html     27 relics, + GRASP
new   tools/gravemourn_build.py       the builder
      tools/gravemourn_hands.js       the hand art, its own file
      tools/gravemourn_relic_probe.py the probe, 12 checks
      tools/hand_art_lab.py           two rounds of spreads for Rick
      tools/hand_art_cands.js         the candidates
      tools/grasp_price.py            four ways to weaken it, priced
edit  tools/umbral_sweep.py           --lo/--hi, and a bigger joint sample
```

---

# 1. WHAT SHIPPED

| | |
|---|---|
| `kind` | **"sling"** — NOT `pull`. Pull-and-cash is the Crucible's verb |
| `dur` | 8.0s window |
| `reachMul` | **1.35**, PER-FIGHTER |
| `handFly` | **1.8s** — Rick's, priced |
| `handStag` | 0.45s between hands off one blow |
| `handMul` | **1.0**, clamped from above |
| `knock` | **700** — Rick's, priced |
| `ult.dmg` | 0 — the cast opens the window and does nothing else |
| blade | 39.79 -> **24.03** (stage 2b) |
| name | **Grasp** — Rick's |
| tip | `"Lengthens the chain; every hit throws a cursed hand"` — 51/72 |

Every blow the wielder lands inside the window throws **one hand per entry in
the foe's curse pool**, each taking its entry. On landing a hand deals exactly
the memory it carries, **re-parks that memory as a fresh curse stack**, and
knocks back hard.

---

# 2. THE DESIGN'S HEADLINE CLAIM IS FALSE ON THE BUILT RELIC

v51's title is *"The chain is the ultimate and the hand is the payload, which
is the opposite of how it reads."* `hand_lab.py` priced the chain ALONE, no
payload at all, at **+12.8 points** and concluded it was about 75% of Grasp's
value.

**Removing the chain buff entirely costs 3.8 points.** n=780 an arm:

```
  control (Grasp as built)              76.3%
  reachMul 1.0, no chain buff at all    72.4%   -3.8pp
  dur 3.0, a quarter of the window      64.1%  -12.2pp
  handMul 0.3, hands hit for a third    55.8%  -20.5pp
  charge 42, it fires rarely            52.6%  -23.7pp
```

**THE HANDS ARE THE ULTIMATE.** The lab measured a chain with nothing coming
off it; once the hands exist and carry pool entries as their damage, they
dominate and the chain is swamped.

**The mechanism the doc described is still real — only its SHARE was wrong.**
With `reachMul` at 1.0 the foe's damage into this relic goes **203 -> 244**, so
the chain is defensive exactly as priced. It simply is not what wins.

**AND `charge` IS A BALANCE LEVER, WHICH THE BRIEF EXPLICITLY RULED OUT.**
§3.2: *"Charge is NOT a balance lever here: at 42 the ult fires in a quarter of
fights and the relic still wins 61.5%."* Measured at this tip, charge 42 is the
single strongest lever in the table at **-23.7pp**. That reading was taken
before the ultimate existed in the form it now has.

---

# 3. THE BLADE AND THE HANDS ARE THE SAME DAMAGE COUNTED TWICE

A hand carries a curse pool entry as its damage, and a pool entry IS a blade
blow. So `dmg` and `handMul` are two taps on one budget and they trade almost
one for one. Rick asked to *"bring back the blade and lets do a weaker grasp"*;
priced across the curve, n=676 an arm:

```
  blade 24.03  handMul 1.00   53.8%     <- SHIPPED
  blade 30.00  handMul 0.50   46.0%
  blade 34.00  handMul 0.30   47.2%
  blade 39.79  handMul 0.15   49.6%
```

Restoring the blade in full costs the hand **six sevenths** of its bite. Shown
the curve, he chose to keep 24.03 and a full-strength Grasp — the row where
"a hand deals exactly the blow it remembers" survives, and the only one already
verified end to end.

## 3.1 AND THE FIRST VERSION OF THAT TABLE WAS WRONG

Two measurements of the SAME arm — `handMul 0.30` — came back **50.6% and
63.9%**, at n=156 and n=208, differing only in seed. A roster win rate is 26
pairings of correlated fights, not N independent flips, and its real precision
is far worse than the binomial figure.

This is the third time this session that a number at n~200-400 has been
ranked and then refuted by a wider one (v53 §3.5c is the first two). **Nothing
below n~700 should be used to rank arms on this roster**, and the tables above
are all n=676 or better.

---

# 4. HALF OF GRAVEMOURN'S KILLS WERE INVISIBLE TO THE DIRECTOR

Found by reading a `cinema_clip` log line — `kill: None` on a fight where the
foe was plainly dead — and not by any check in this repo.

`cinema_clip` finds the killing blow with `plan.find(c => c.fatal)`. The hand
filed a `kind:"ult"` beat, which carries no such flag:

```
  30 of 58 Gravemourn kills over 80 fights were landed by a HAND   51.7%
  of those, filing no fatal beat at all                            30 of 30
```

**Over half its wins rendered a clip with no killing blow**, silently falling
back to "the last cut". That is open item 3's defect class and it would have
been the worst instance in the game — Dawnbringer, the current worst, is 22.1%.

**The probe passed throughout**, because [13] asserted *a* beat was filed, not
that a FATAL hand declares itself fatal.

The fix is the Thicket's own precedent, quoted in the engine three lines from
where the bug was: `_cineVine` suppresses every lash beat **and keeps the fatal
one**, because "do not let small hits drive the camera" is a different claim
from "do not film the finish". A fatal fist now files a second beat in
`resolveHit`'s exact shape and takes the kill-stop and finisher weight.
**0 of 30 missing, and no double-counting.**

---

# 5. THE HAZARD THE BRIEF NAMED, AND THE ONE IT DID NOT

## 5.1 `w.reach` IS MODULE-LEVEL — CLOSED, AND ASSERTED

Brief §4.1, "the single most likely way this build gets wasted". `w` is shared
by every match in a page session, so a window that writes `w.reach` and misses
a restore path rewrites the relic for every fight afterwards, **and the symptom
appears in a match that never cast anything.**

The build never touches `w.reach`. It adds a per-fighter `f.reachMul` and
multiplies at every read — five in the simulation, two in the renderer.
`gravemourn_relic_probe [9d]` runs Gravemourn fights that cast, then runs six
other-relic matches AFTER them in the same page, and asserts all 27 reaches are
unmoved.

**THE FIRST PASS OF THE BUILDER MISSED A SITE.** `w.reach` was grepped, six
sites were edited, and a printed count said so reassuringly — but there are
TWO projectile origins, not one, and the seventh sat there reading an
unmultiplied reach. A printed count is something a person has to notice. **The
builder now refuses to write** if any `f.w.reach` read lacks the multiplier.

## 5.2 THE CHAIN GROWS FOR FREE

`tickWeapon` already recomputes `chainLen` from reach every frame and eases
`headR` toward it. Raising `reachMul` at the cast swings the head wider over a
few frames and settles it back when the window closes. **The mechanic and the
animation are the same line and there is no animation code.**

## 5.3 `handMul` > 1.0 COMPOUNDS WITHOUT BOUND — CLAMPED IN BOTH PLACES

The hand deals `mem * M` and re-parks `mem * M`, so above 1.0 every memory
grows each time it is thrown. An 8s window and 1.7 casts a fight hide the
exponent for two or three cycles and it reads as merely strong. Clamped in the
engine AND refused by the builder.

## 5.4 HANDS ARE PER-MATCH STATE, NOT `shots`

`spawnShot` SHIFTS the oldest live entry out at `maxLive` 64 — on a hand in
flight that is a purple fist vanishing in mid-air with no error, no invariant
broken and no win rate moved. The hands are their own list on the Match and it
**declines and counts** instead. Bloodhunt's fork branch is the precedent.

---

# 6. THE PROBE FOUND NOTHING, AND WAS WRONG THREE TIMES

`gravemourn_relic_probe` is 12/12. Every failure it reported during
development was the probe assuming its own rule instead of reconstructing the
engine's:

**[9] "the chain lengthens"** reported 77 against 77 — no lengthening at all,
on a build where it lengthens by exactly 1.35. Both numbers were maxima taken
in DIFFERENT ACTS: `actMods.reach` climbs 1.0 -> 1.1 over a fight, the window
lands early, the late fight is all outside it. Now sampled as a RATIO against
the chain the relic would have without the window, on the same frame.

**[10] "one hand per pool entry"** flagged 18 of 27 blows. A pool of `[35]`
throwing two hands carrying `[58, 35]` is correct: the blow that throws the
hands is one of the blows they remember, so its own push is in the pool by the
time they leave. Now hooks `pushCurse` and reconstructs the expected count.

**[11] "a hand re-parks what it dealt"** started failing the moment flight
time went 1.2s -> 1.8s. With hands in the air longer the quarry is hit again
before they land, so a small re-parked memory pushes into a full pool and is
DISPLACED on the same call — curse's top-K rule working. Now asserts the
**push**, not the survivor.

**A probe that encodes its own model of the rule will fail on every legitimate
change to the rule.** All three now read the engine's behaviour instead.

---

# 7. THE ART TOOK TWO ROUNDS AND A REFERENCE

Rick, on the first cut: *"the hands dont read as hands. not detailed enough."*

**MEASURED FIRST** (§4.1 — the deliverable is a measurement of the thing they
saw): 37px across on a 540 frame, 75px on a phone, 78 frames on screen, moving
0.65x its own width per frame. **It was never too small.** It was a filled disc
with four spokes, which is an asterisk, drawn entirely under `lighter` so its
own interior edges saturated and vanished — §4.1b's Daybreak lesson on a new
object.

He then sent `Mage_hand_flying_and_fist.mp4`, **and the reference settled a
register four rounds of guessing had not**: a long streaming forearm, an
edge-lit contour with a dim interior, and knuckle lobes on the fist.

Round two, on the flame hand that came out of it: *"a bit large... and the
forearms look like they are just bone. thats got me thinking. what if the whole
hand was bone?"* **Both notes were one discovery** — the arm was three glowing
strands with dark gaps, which at this size is a radius and an ulna. The art was
already halfway to a skeleton.

Bone is drawn the **exact inverse** of flame: flame is a volume so it is
edge-lit; a skeleton is bright PARTS with dark GAPS, and the gaps are the whole
reading. Same two-pass technique pointed the other way.

**THE SCALE TOOK THREE GOES — 1.15, 0.6, 0.7 — AND NO SHEET COULD HAVE SETTLED
IT.** The spread answered every SHAPE question in one round trip each. The
sheet shows the object still; every size complaint was about it in motion,
among two others. **Shape questions go to a sheet. Scale questions need the
video.**

---

# 8. THE GATES

```
gravemourn_relic_probe   12/12
engine_ab (24 relics)    2760/2760 identical, field for field
verify --n 40            12/13, and the thirteenth is the known one
```

`verify` on the shipped build, 14,040 matches:

```
  Gravemourn 55.2%   Nightfell 50.6%   Twinshade 48.8%
  Goreshard 40.6% .. Slagheart 58.2%   spread 17.6pp
  FAIL  Lightkeeper/Farwarden 77.3s    vigil vs vigil, no umbral relic
```

**The spread is the tightest of the session and tighter than the build this
began from:** 19.0pp (sc-vesper) -> 21.5 (stage 1) -> 18.0 (1b) -> **17.6**.

The 77.3s duration failure is identical to the digit on `sc-vesper.html`, whose
control was run in the same session on the same runtime.

---

# 9. WHAT STAGE 3 INHERITS

- **`f.reachMul` exists and is honoured at all seven read sites.** Nightfell's
  sigils do not need it, but anything that resizes a weapon does.
- **`m.hands` is the precedent for per-match object lists** — declines at a
  ceiling, counts the refusal, discarded with the match. §8.3d asks for exactly
  this for the live charges.
- **A FATAL PAYLOAD MUST FILE A FATAL BEAT.** §4 above. Nightfell's charges
  detonate outside `resolveHit` exactly as the hands do, so a charge that lands
  the killing blow will have the same hole. `nightfell_relic_probe` should
  check the FATAL case, not just that a beat exists.
- **Nothing below n~700 ranks anything on this roster.** §3.1.
- **Eclipse is a dead ultimate right now** — it lost `apply:{curse:3}` in stage
  1 and got nothing back. Nightfell's 50.6% is temporary by construction.

---

# Open decisions

1. **THE ULT TIP IS STILL A PLACEHOLDER.** `"Lengthens the chain; every hit
   throws a cursed hand"` (51/72). The name is settled — Grasp, Rick's.
2. **THE WINDOW `dur` HAS NEVER BEEN CHOSEN**, only inherited at 8.0s from the
   lab. It is worth -12.2pp at 3.0s, so it is a real lever now that its
   companion knobs are priced.
3. **`crowdMul` IS UNSET FOR THIS ULTIMATE.** Grasp puts up to five extra
   contacts on the floor in a window; open item 15 already flags the same
   question for the Winnowing.
4. **THE CHAIN IS 3.8 POINTS AND 75% OF THE PICTURE.** v51 open decision 4 asked
   how the chain buff should READ. It is now known to be nearly free in balance
   terms, which makes it cheap to make MORE visible rather than less.
