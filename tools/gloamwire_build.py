#!/usr/bin/env python3
"""GLOAMWIRE, AND ITS ULTIMATE CROSSWEAVE. STAGES 1, 2, 3 AND 4.

    python gloamwire_build.py --stage 1 --src ../02-chain/sc-garrote.html \
                              --out ../02-chain/sc-gloamwire.html
    python gloamwire_build.py --stage 2 --src ../02-chain/sc-gloamwire.html \
                              --out ../02-chain/sc-volley.html
    python gloamwire_build.py --stage 3 --src ../02-chain/sc-volley.html \
                              --out ../02-chain/sc-crossweave.html

**THE DESIGN IS NOT THIS FILE'S AND IT NEVER WAS.**
`06-docs/v61/gloamwire-design-v61.md` is the design and
`06-docs/v61/GLOAMWIRE-BUILD-BRIEF.md` is the brief; `tools/net_lab.py` is the
instrument that measured all of it. Every number below was decided there. This
builder implements and refuses; it does not choose.

CLAUDE.md section 3 rule 0, which exists because of this cell: Claude Code does
not design ultimates. If you are reading this file looking for the reasoning
behind a mechanic, it is in the design doc, and if the design doc is missing the
answer is to stop rather than to invent one.

## FOUR DEPARTURES FROM THE BRIEF, ALL DECLARED HERE

**THE BASE IS `sc-garrote.html` AND THE BRIEF SAYS `sc-breach.html`.** The brief
was written against 29 relics before Ravelbone landed; stage 0 of it says to
chain from the newest link and say which. `WEAPONS` holds 30 on the tip, so
every `engine_ab` below runs over 30 others rather than 29, and every win rate
in the design doc is measured in a world with one fewer relic in it.

**IT IS THE THIRTY-FIRST RELIC AND THE DESIGN DOC SAYS THIRTY-SECOND.**
`CONFLICT-READ-FIRST-v61.md` flagged this drift and asked for it to be settled
in one place. It is settled: CLAUDE.md section 0 calls Ravelbone the THIRTIETH,
counting what is built and in a link. Bloodmirror is designed and is in no link
-- its brief lives in the Cowork project only -- so counting design order gives
a number that no file in this repo can check. **Built count. Gloamwire is 31.**

**THE TIP BUDGET IS 72 AND BOTH DOCUMENTS SAY 40.** `verify.py` line 89 is
`u.tip.length > 72`; the 40 in the brief's open decision 1 and the design's open
decision 5 is the STATUS tip figure (itself 48 in code and 40 in the comment
above it -- CLAUDE.md section 0 records that discrepancy). So
`"24 volleys of 3 strung arrows; the strand shoves"` is 48 characters and
**fits**, and that open decision closes itself.

    BUT CHARACTERS ARE THE WRONG UNIT, AND THE SURFACE NAMED HERE WAS WRONG.
    This said the scrunch panel, at 536px on one line. Cowork's v59 tip-surface
    work corrects it: the panel WRAPS to three lines and always did. The
    surface that can overflow is `_tagFirst` -- one line, 25px, no wrap, no
    clip, no measure -- and `tip_audit.py` measures that box in the bundled
    face. It has still not been run on this relic.

**AND THE 2% FLOOR MEANS GATE 1'S `verify` WILL FAIL THE BAND.** The design
measured Gloamwire at 2% with Crossweave stubbed -- the sharpest
ultimate-dependence on the roster, and Rick's deliberate choice (design section
8). The brief says in as many words that this is not a stage-1 failure. Print
the number, do not tune to it, and do not read a red band here as a defect.

## RICK'S SECTION 1, VERBATIM

    a simple ult.

    purple bow gains a triple shot. each arrow connected by a string of purple
    lightning. Enemies hit by an arrow take extra damage. enemies hit by only
    the lightning take no damage but take extra knockback. Enemies hit by both
    take both

and, on being shown that the fire-rate field already exists:

    can we also give the ult increased fire rate?

## THE THREE THINGS THE BRIEF SAYS WILL BITE, CARRIED HERE SO THEY CANNOT BE LOST

1. **THE STRAND TEST RUNS BEFORE `tickShots`.** If it runs after, an arrow that
   connected this frame has already been spliced out of `this.shots` and its
   strands went with it, so **"hit by both" is unreachable** -- the third of
   Rick's three cases silently never fires and no probe would show it. Running
   first costs one step of lag and makes both outcomes reachable on one frame.

2. **THE CADENCE GATE IS `f.ultBal || f.ultNet` AND NEVER A FAKED `ultBal`.**
   Setting `ultBal` starts `tickBallista`'s clock and Marrowdraw's bolt
   upgrades. And it stays `=== undefined` rather than `|| 1` (CLAUDE.md section
   4.3): a sweep must be able to set `cadMul` to 0.

3. **AN EXPLICIT ANGLE MUST STILL FIRE ONE ARROW.** `spawnShot(f, angle)` is
   called with an angle by other mechanics, and an explicit angle is some other
   system asking for exactly one shot. The volley is three calls to the
   ordinary path, not a new projectile path.

## AND ONE THING THE DESIGN SAYS NOT TO "FIX"

`resolveHit` is untouched. Crossweave's arrows carry `dmgMul 1.4` and
`foe.pushCurse(dmgBase, n)` already runs on every landing arrow, so the ultimate
raises the curse pool 33.8 -> 40.8 with no new code. **v49 section 5b proved an
umbral ultimate cannot ADD to a top-K pool -- measured on ults that applied
Curse from an `apply` field with no blow behind it.** Crossweave adds to it by
landing a bigger blow than the blade, which is the one route v49 never tested.
Do not add `apply:{curse:n}` to the ult: that is the dead clause, measured at
+0.0, and `Fighter.apply` derives the stack count from the pool so it would
refresh a clock and add nothing.

Runtime: on Windows the interpreter is `python` or `py`, never `python3`.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "gloamwire"

# --------------------------------------------------------------- the numbers --
# EVERY ONE OF THESE IS THE DESIGN DOC'S, NOT THIS BUILDER'S. The section it
# comes from is named beside it so a change here is visibly a change to a
# measured thing.
BLADE_IN = 9.2       # design 6/6.1. A PLACEHOLDER in CLAUDE.md section 4.9's
                     # sense: measured on Chromium 141 at 29 relics and it must
                     # be swept on the pin at 31 before it is believed.
TUNED_GW = 9.5       # MEASURED, and it is a WIDE DIRECT MEASUREMENT rather than
                     # a bisection: `gloamwire_sweep.py --only 1`, three blades
                     # x both sides x two seed blocks x 1020 fights a cell,
                     # 12,240 in total, on the pin at 31 relics.
                     #
                     # AT speedMul 1.35 (the shipped one):
                     #     dmg    A-side  B-side  blockA  blockB   POOLED
                     #    9.20     46.5%   46.8%   46.3%   46.9%    46.6%
                     #    9.80     53.8%   52.8%   53.7%   52.9%    53.3%
                     #   10.40     57.1%   55.8%   57.8%   55.0%    56.4%
                     # monotone, side asymmetry +0.7pp, worst block 2.8pp,
                     # crossing at 9.50.
                     #
                     # AT speedMul 1.0, before Rick added the speed:
                     #    8.60 45.0%   9.20 52.3%   9.80 58.1%
                     # monotone, side asymmetry +0.6pp, crossing at 9.01.
                     #
                     # SO THE SPEED COST 0.49 OF BLADE, WHICH IS ~5.5pp AT THIS
                     # SLOPE (11.2pp a damage point) -- and that number is the
                     # only one of three that was measured properly. The speed
                     # sweep said -7.7pp at n=900 an arm and the re-run cheap
                     # curve implied about zero; both were wrong, in opposite
                     # directions, and the wide pass adjudicated without either.
                     #
                     # THE HONEST PRECISION IS THE INTERVAL AND NOT THE DECIMAL.
                     # The slope here is ~11pp a damage point, so the ~1.1pp SE
                     # at n=4080 is about +/- 0.1 of blade: the answer is
                     # 8.9-9.1 and 9.0 is the middle of it. The design's
                     # placeholder 9.2 was not refuted -- it reads 52.3%, inside
                     # `verify`'s band and about 2 SE high -- and this is a
                     # correction rather than a repair.

ULT = {
    "charge":      15.0,   # design 9. The roster mode and v55b's default.
    "volleys":     24.0,   # design 6.1, from a ladder of three. Rick's.
    "n":            3.0,   # Rick's section 1: "a triple shot"
    "spread":       0.90,  # design 4.1, the 52-degree fan. Rick's, over
                           # parallel and over two narrower fans.
    "cadmul":       0.5,   # design 5. Below 1 is FASTER; Marrowdraw uses 4 to
                           # go drastically slower.
    "speedmul":    1.35,   # RICK'S, 2026-09-01, with the sweep in front of
                           # him. 380 -> 513 px/s. NOT free: measured -7.7pp at
                           # n=900 an arm and 0.49 of BLADE on the wide pass,
                           # about 5.5 points -- because a faster arrow reaches
                           # the WALL sooner (wall 83.8% -> 85.7%) and the bow
                           # only ever lands 7.7% of what it fires. A picture
                           # bought with points, like Cindercleave's shove.
    "dmgmul":       1.4,   # design 6, the +40% arm. Rick took all four
                           # strength clauses and the blade pays.
    "strandw":     90.0,   # design 4.2. Above the crossover at shot.r = 24, so
                           # "arrow only" is near zero BY CONSTRUCTION. Rick
                           # took above the line.
    "strandknock": 260.0,
    # ---- STAGE 8, all three PLACEHOLDERS and all three must be swept.
    "novarad":      90.0,  # matches the strand's own reach (34 + 90 = 124), so
                           # a nova covers the ground its own lightning did.
    "novadmg":      0.35,  # x the BLADE. 9.5 x 0.35 = 3.3 against one arrow's
                           # 9.5 x 1.4 = 13.3. Rick: "less than an arrow."
    "novaknock":   420.0,  # against the strand's 260. Rick: "the knockback
                           # should be most of the payoff."  # design 6.2. A COST, monotone -9 points across the
                           # sweep, bought for the look and worth ~a point of
                           # blade.
}

ULT_NAME = "Crossweave"
# 48 characters against verify's 72. See the header: the 40 in both documents
# is the status-tip figure. `tip_audit` is still the gate that matters.
ULT_TIP = "24 volleys of 3 strung arrows; the strand shoves"
ULT_TIP1 = "—"     # stage 1, stubbed. verify only asks that it is non-empty.

# STAGE 5, AND IT IS RICK'S TO CHANGE. Four registers, and the default is the
# one his own words point at -- "a string of purple lightning" is a discharge
# and not a beam. `strand_art_lab.py` renders all four off one real frame.
STRAND_ART = "bolt"

# NOT RICK'S, AND OFFERED RATHER THAN CHOSEN. The design doc's open decision 2
# says the blurb is unwritten. Every other relic's is in his register; this is a
# placeholder that reads like one so it cannot quietly become permanent.
BLURB = ("Three shafts and the dark strung between them. What the arrows miss, "
         "the lightning still moves.")


# ----------------------------------------------------------------- stage one --

S1 = [

("relic", '''    blurb:"Wire off a pit fence, wound round a head that was already heavy. What it catches does not get to walk away from the swing." },

];''',
 '''    blurb:"Wire off a pit fence, wound round a head that was already heavy. What it catches does not get to walk away from the swing." },

  /* GLOAMWIRE -- THE UMBRAL BOW, and the thirty-first relic. Umbral was on 4 of
     6 types and the bow on 5 of 7 schools; this puts the school on 5 and the
     type on 6, and it leaves `runic x bow` as the only cell on the row.

     EVERY PHYSICAL STAT IS THE BOW'S, copied off Ironhail, Farwarden, Aureole,
     Vinesower and Marrowdraw -- all five already carry the `shot` block byte
     for byte and the TYPE owns it (asserted in `net_lab` [0], and again by
     this builder before it writes). `SHAPES.bow` routes `umbral` to a branch
     that has drawn this cell since before there was a relic in it: both limb
     TIPS eaten off with `destination-out`, a gap bitten out of one limb, and a
     translucent shadow flame added back at each -- which on a bow is the one
     place where an absence is also a mechanical claim, because the tips are
     what the string is anchored to. It should not be able to fire, and it does.

     AND THE CELL'S OWN FILE WAS WRONG ABOUT IT FOR TWENTY-ONE RELICS. v40
     section 4.1 is titled "CURSE DELIVERS ZERO" and measured `+0±0` on this
     exact body -- correct when written, because the old curse subtracted
     `maxHpLoss` per application and `hp` only followed when `maxHp` was driven
     under it. That mechanic was deleted in v53. Re-measured on the reworked
     curse the same cell is worth +19.0pp with the field's ultimates off and
     +31.5pp with them on, and this body fills the memory FASTEST IN THE SCHOOL
     -- third-deepest standing pool at 54.2, reached in half Gravemourn's time,
     71% of the fight at the cap. 64% of its blows are arrows, so it is the
     only umbral relic that starts remembering from across the room.

     `dmg` is the tuned knob (gloamwire_build.TUNED_GW). 9.2 is a PLACEHOLDER
     and it is low ON PURPOSE: Crossweave carries four separate strength
     clauses -- three arrows for one, +40% on each, double cadence, and the
     shove -- and design section 6 measured every configuration that keeps all
     four as putting this relic below the row unless the blade pays. The other
     five bows ship at 12.73 to 16.23. */
  { id:"gloamwire", name:"Gloamwire", aff:"umbral", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:%DMG%, spin:2.8, mode:"ranged", mass:1.6,
    shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
           tip:"Fires along its facing · shots can be clanked" },
    onHit:{ curse:1 },
    /* CROSSWEAVE. STUBBED AT `charge:1e9` IN STAGE 1 -- the same "OFF" the
       charge sweep in v55b used and the same one Cindercleave's stage 1 and
       Shroudmaul's stage 2 used: the clock can never reach it, `fireUlt` never
       runs, and the relic is measured as a blade and a channel and nothing
       else. Stage 2 brings the charge down to %CHARGE% and builds the volley;
       stage 3 strings the lightning between the arrows.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       EXPECT THIS RELIC TO FAIL `verify`'s 30-70% BAND WHILE IT IS STUBBED,
       AND DO NOT TUNE TO IT. Measured at 2% without Crossweave -- the sharpest
       ultimate-dependence on the roster, against a field median ultimate worth
       +20.4pp and this one worth +48.8pp. Rick chose that shape knowingly
       (design section 8); the band is a statement about the finished relic and
       stage 1 is not it.

       `kind:"net"` IS ITS OWN. It is not `"volley"` -- Quarrelstorm fires a
       nova once and is done -- and it is not `"ballista"`, which is the other
       windowed bow ultimate and whose `f.ultBal` flag must NOT be borrowed for
       the cadence gate: setting it starts `tickBallista`'s clock and
       Marrowdraw's bolt upgrades. */
    ult:{ name:"%ULT%", charge:1e9, kind:"net", tip:"%TIP1%" },
    blurb:"%BLURB%" },

];'''),

]


# ----------------------------------------------------------------- stage two --
# THE VOLLEY AND THE FAN. No lightning yet -- Rick's second sentence is stage 3,
# and the brief separates them so the fan can be watched before anything is
# strung between its arrows (CLAUDE.md section 4.0: film before you tune, if the
# ultimate is a picture, and this one is entirely a picture).

S2 = [

# --------------------------------------------------- 1. the ult block, for real
("ult-block", '''    /* CROSSWEAVE. STUBBED AT `charge:1e9` IN STAGE 1 -- the same "OFF" the
       charge sweep in v55b used and the same one Cindercleave's stage 1 and
       Shroudmaul's stage 2 used: the clock can never reach it, `fireUlt` never
       runs, and the relic is measured as a blade and a channel and nothing
       else. Stage 2 brings the charge down to %CHARGE% and builds the volley;
       stage 3 strings the lightning between the arrows.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       EXPECT THIS RELIC TO FAIL `verify`'s 30-70% BAND WHILE IT IS STUBBED,
       AND DO NOT TUNE TO IT. Measured at 2% without Crossweave -- the sharpest
       ultimate-dependence on the roster, against a field median ultimate worth
       +20.4pp and this one worth +48.8pp. Rick chose that shape knowingly
       (design section 8); the band is a statement about the finished relic and
       stage 1 is not it.

       `kind:"net"` IS ITS OWN. It is not `"volley"` -- Quarrelstorm fires a
       nova once and is done -- and it is not `"ballista"`, which is the other
       windowed bow ultimate and whose `f.ultBal` flag must NOT be borrowed for
       the cadence gate: setting it starts `tickBallista`'s clock and
       Marrowdraw's bolt upgrades. */
    ult:{ name:"%ULT%", charge:1e9, kind:"net", tip:"%TIP1%" },''',
 '''    /* CROSSWEAVE -- a MAGAZINE of %VOLLEYS% volleys, each of %N% arrows in a
       %SPREAD% rad fan, loosed at %CADMUL%x the cadence, and each volley strung
       with two bars of lightning that shove and never damage.

       `kind:"net"` IS ITS OWN. It is not `"volley"` -- Quarrelstorm fires a
       nova once and is done -- and it is not `"ballista"`, which is the other
       windowed bow ultimate and whose `f.ultBal` flag must NOT be borrowed for
       the cadence gate: setting it starts `tickBallista`'s clock and
       Marrowdraw's bolt upgrades.

       A MAGAZINE AND NOT A CLOCK, AND THAT IS THE DECISION THAT MAKES THE FIRE
       RATE AFFORDABLE. `volleys` counts down per VOLLEY and the window ends at
       zero, so the payload is invariant across the rate and only the delivery
       compresses -- measured at 8.0 / 8.1 / 7.6 arrows landed and 18.1 / 18.8 /
       18.1 shoves across 1x / 2x / 4x, with the window collapsing 8.2s -> 4.1s
       -> 2.0s. Under a DURATION the same rate costs +37pp instead of +13pp.
       THERE IS DELIBERATELY NO `dur` FIELD: a duration and a count together are
       two ways to end one window, and the second one to fire is a silent
       behaviour nobody wrote down.

       `dmgMul` %DMGMUL% IS WHY THE BLADE IS SO LOW, and it is also the only
       route by which an umbral ultimate has ever raised the curse pool. v49
       section 5b proved an ultimate cannot ADD to a capped top-K pool --
       measured on ultimates that applied Curse from an `apply` field with no
       blow behind it. These are real blows at %DMGMUL%x the blade, so
       `resolveHit`'s own `pushCurse(dmgBase, n)` pushes memories the blade
       cannot make: pool 40.8 against 33.8 stubbed. DO NOT ADD
       `apply:{curse:n}` HERE -- that is the dead clause v49 measured at +0.0,
       and `Fighter.apply` derives the stack count from the pool, so it would
       refresh a clock and add nothing.

       `strandW` AND `strandKnock` ARE INERT UNTIL STAGE 3 and are written here
       rather than added later, because v56 shipped an ultimate whose numbers
       its own log did not describe: the stage-2 insert wrote the block and
       stage 3 rewrote one line of it. `ult_matches` refuses to write unless
       every number this run printed is in the block.

       `strandW` %STRANDW% SITS ABOVE THE CROSSOVER AND THAT IS ALGEBRA, NOT
       TUNING. An arrow connects at `R + shot.r` = 58 and a strand at
       `R + strandW`; a strand's endpoints ARE its arrows, so above
       `strandW = shot.r = 24` any ball an arrow can touch is already inside the
       segment, and "hit by the arrow alone" is identically zero. Rick took
       above the line, over equal-width and a hairline. ARROW-ONLY WILL MEASURE
       1-6% AND THAT IS CORRECT -- it is entirely volleys whose other arrow died
       first. Do not tune it up. */
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"net",
          volleys:%VOLLEYS%, n:%N%, spread:%SPREAD%, cadMul:%CADMUL%,
          dmgMul:%DMGMUL%, strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,
          tip:"%TIP%" },'''),

# ------------------------------------------------------- 2. fireUlt opens it
("fireult-net", '''    if (u.kind === "ballista"){
      f.ultBal = { t: 0, dur: u.dur, bolts: 0, hits: 0, forks: 0 };
      this.ultFx.life = u.dur + 0.6;
    }
''',
 '''    if (u.kind === "ballista"){
      f.ultBal = { t: 0, dur: u.dur, bolts: 0, hits: 0, forks: 0 };
      this.ultFx.life = u.dur + 0.6;
    }

    /* CROSSWEAVE. A MAGAZINE, NOT A CLOCK -- `left` counts down per VOLLEY in
       `tickFire` and the window ends when it reaches zero. There is no `dur`
       and there must not be one.

       The fx life is the longest the magazine can take to empty, plus a tail.
       It drives nothing but the picture. NOTE FOR STAGE 4: `ultFx` is ONE SLOT
       for the whole match, so the opponent casting anything erases this relic's
       field (CLAUDE.md open item 25, measured at 0.0% survival against
       Ironhail). What a viewer reads here is the arrows and the strands, which
       are SIM OBJECTS and cannot be erased -- but any field art added later
       should hang off `f.ultNet` the way Deadfall's crackle hangs off
       `f.ultDeadfall`. */
    if (u.kind === "net"){
      f.ultNet = { t: 0, left: u.volleys, fired: 0, shoves: 0 };
      this.ultFx.life = u.volleys * f.w.shot.cadence * u.cadMul + 0.6;
    }
'''),

# --------------------------------------------- 3. the cadence gate and the fan
("tickfire-volley", '''    const cm = f.ultBal && f.w.ult.cadMul !== undefined ? f.w.ult.cadMul : 1;
    f.fireCd += S.cadence * cm;
    this.spawnShot(f);
  }''',
 '''    /* WIDENED TO `f.ultNet`, AND `f.ultBal` IS NOT FAKED TO GET IT. Setting
       `ultBal` would start `tickBallista`'s clock and hand these arrows
       Marrowdraw's bolt upgrades -- homing, forking, a different silhouette and
       a different `life`. Two windows, one gate, and neither borrows the
       other's flag. */
    const cm = (f.ultBal || f.ultNet) && f.w.ult.cadMul !== undefined
             ? f.w.ult.cadMul : 1;
    f.fireCd += S.cadence * cm;
    /* THE VOLLEY, AND IT LIVES HERE RATHER THAN INSIDE `spawnShot`.

       The brief puts the fan in `spawnShot` guarded on `angle === undefined`,
       because an explicit angle is some other mechanic asking for exactly ONE
       shot and must stay one shot -- Quarrelstorm passes fourteen of them.
       Putting the loop at the only call site that fires the ORDINARY stream
       gets the same result and cannot be got wrong: every other caller of
       `spawnShot` is byte-identical and reaches no new code at all.

       The fan is symmetric about the facing -- `off` runs -1, 0, +1 at n=3 --
       so the middle arrow is exactly the arrow this relic would have fired
       anyway, and the ultimate reads as two more beside it rather than as a
       different weapon.

       A VOLLEY IS ONE MAGAZINE ROUND, NOT THREE. The decrement is here and not
       in `spawnShot` for that reason, and the window closes on the volley that
       empties it. */
    if (f.ultNet){
      const u = f.w.ult, N = u.n | 0;
      const vid = this.netSeq = (this.netSeq || 0) + 1;
      for (let k = 0; k < N; k++){
        const off = k - (N - 1) / 2;
        this.spawnShot(f, f.theta + off * u.spread);
        const s = this.shots[this.shots.length - 1];
        /* A MULTIPLIER OF WHAT THE TYPE ALREADY SET, never an assignment, so
           the shot block stays the one thing that decides what an arrow is. */
        s.dmgMul = s.dmgMul * u.dmgMul;
        /* The two fields stage 3 strings the lightning between. `idx` is the
           position in the FAN and never an index into `this.shots`, which
           changes every time anything dies. */
        s.volley = vid; s.idx = k; s.net = true;
      }
      f.ultNet.fired++;
      if (--f.ultNet.left <= 0) f.ultNet = null;
      return;
    }
    this.spawnShot(f);
  }'''),

# ------------------------------------------- 4. the ticker, and WHERE it goes
("step-ticknet", '''    this.tickClank(dt);
    this.tickShots(dt);''',
 '''    this.tickClank(dt);
    /* BEFORE `tickShots`, AND THAT IS LOAD-BEARING RATHER THAN TIDY.

       `tickShots` moves every arrow, resolves it, and SPLICES the dead ones out
       of `this.shots`. A strand exists only between two live arrows of one
       volley, so if this ran afterwards, an arrow that connected on this frame
       would already be gone and its strands with it -- and "hit by BOTH", the
       third of the ultimate's three outcomes, would be unreachable. It would
       never fire, no probe would report anything, and the design would be
       missing a third of itself in a way nothing could see.

       The brief asks for this ticker to sit with the other window tickers
       (`tickWinnow`, `tickGrasp`, `tickBreach`, `tickBallista`) and, in the same
       paragraph, for it to run before `tickShots`. IN THIS BUILD THOSE TWO
       INSTRUCTIONS CONTRADICT EACH OTHER: `tickShots` runs here, and every one
       of those window tickers runs after it. The requirement wins over the
       address.

       It costs one step of lag -- the strand is tested against where the arrows
       were 1/120s ago -- and that is the price of both outcomes being reachable
       on the same frame. */
    this.tickNet(dt);
    this.tickShots(dt);'''),

# ---------------------------------------------------- 5. the ticker itself
("ticknet", '''  tickShots(dt){
    if (!this.shots.length) return;''',
 '''  /* CROSSWEAVE's window. In stage 2 this is the guard and nothing else: the
     magazine empties in `tickFire`, but `tickFire` returns early on a dead or
     stunned fighter and on `this.over`, so without a ticker that runs
     unconditionally a window could outlive the fighter holding it. Stage 3
     fills in the strand. */
  tickNet(dt){
    for (const f of [this.a, this.b]){
      if (!f.ultNet) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultNet = null; continue; }
      f.ultNet.t += dt;
    }
  }

  tickShots(dt){
    if (!this.shots.length) return;'''),

]


# --------------------------------------------------------------- stage three --
# THE STRAND, AND IT IS THE HALF OF RICK'S SECTION 1 THAT HAS NO PRECEDENT.
# "enemies hit by only the lightning take no damage but take extra knockback"
# is a payload that deliberately touches nothing but position -- Grasp is the
# only other thing in the game built that way, and Grasp deals nothing at all.
#
# NOTHING HERE IS DRAWN AND NOTHING HERE MAKES A SOUND. That is the brief's
# staging and not an oversight: the art, the animation and the sound are three
# of Rick's seven things (CLAUDE.md section 3 rule 2) and stage 4 is where they
# are offered as a spread. A stage-3 build shoves the quarry with no bar of
# lightning on screen and no noise, so it is measurable and it is NOT watchable.
# Do not film it and conclude anything.

S3 = [

("ticknet-body", '''  /* CROSSWEAVE's window. In stage 2 this is the guard and nothing else: the
     magazine empties in `tickFire`, but `tickFire` returns early on a dead or
     stunned fighter and on `this.over`, so without a ticker that runs
     unconditionally a window could outlive the fighter holding it. Stage 3
     fills in the strand. */
  tickNet(dt){
    for (const f of [this.a, this.b]){
      if (!f.ultNet) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultNet = null; continue; }
      f.ultNet.t += dt;
    }
  }''',
 '''  /* CROSSWEAVE. The window is a MAGAZINE and it empties in `tickFire`; this
     runs the guard on it and then tests the lightning strung between the
     arrows already in the air.

     WHY IT IS CALLED BEFORE `tickShots` is written where it is called, and it
     is the difference between this ultimate having three outcomes and two. */
  tickNet(dt){
    for (const f of [this.a, this.b]){
      if (!f.ultNet) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultNet = null; continue; }
      f.ultNet.t += dt;
    }

    if (!this.shots.length) return;
    const R = CONFIG.physics.ballR;

    /* THE STRANDS ARE A PROPERTY OF THE VOLLEY AND NOT OF THE WINDOW, so this
       loop deliberately does not test `f.ultNet`. The magazine can empty while
       its last volley is still crossing the room, and lightning that stopped
       existing because a counter reached zero would be a bar that vanished in
       mid-air with the arrows still flying. */
    const byVolley = new Map();
    for (const s of this.shots){
      if (!s.net) continue;
      let g = byVolley.get(s.volley);
      if (!g) byVolley.set(s.volley, g = []);
      g.push(s);
    }
    if (!byVolley.size) return;

    for (const g of byVolley.values()){
      if (g.length < 2) continue;
      g.sort((p, q) => p.idx - q.idx);
      const src = g[0].own === "a" ? this.a : this.b;
      const foe = g[0].own === "a" ? this.b : this.a;
      if (!src.alive || !foe.alive) continue;
      const u = src.w.ult;
      const reach = R + u.strandW;
      for (let i = 0; i + 1 < g.length; i++){
        const p = g[i], q = g[i + 1];
        /* ADJACENT IN THE FAN, and a dead arrow BREAKS its links rather than
           handing them on: idx 0 and idx 2 with 1 gone is not a strand and does
           not re-form into one. This is also the whole of why "hit by the arrow
           alone" is not identically zero at `strandW` 90 -- above the crossover
           a ball an arrow can touch is always inside the segment, so the 1-6%
           that survives is entirely volleys that lost an arrow first. */
        if (q.idx !== p.idx + 1) continue;
        /* ONE HIT PER STRAND, LATCHED ON THE LOWER-INDEX ARROW so the two
           strands of one volley stay two separate events. A line sweeping
           across a ball overlaps it for many frames and without this the strand
           is a blender rather than a shove. */
        if (p.strandSpent) continue;
        if (segDist(p.x, p.y, q.x, q.y, foe.x, foe.y).d >= reach) continue;
        p.strandSpent = true;
        /* NO DAMAGE, NO `onHit`, NO `pushCurse`, NO `apply`. Rick's rule
           verbatim: the lightning alone is knockback and nothing else. It does
           not route through `resolveHit`, which is what would quietly add crit,
           jitter, hit stop, hitstun, the sunder multiplier and a curse stack.

           ALONG THE VOLLEY'S OWN TRAVEL, not away from the archer. The pair's
           velocities are summed rather than one of them taken, because the two
           arrows of a fan are not parallel and picking either would push the
           quarry off to one side of a bar that looks symmetric. This is the
           Thicket's rule -- a hazard that is not the caster needs its own
           bearing, or the shove reads as coming from the wrong place. */
        const vx = p.vx + q.vx, vy = p.vy + q.vy;
        const vl = Math.hypot(vx, vy) || 1;
        foe.vx += (vx / vl) * u.strandKnock;
        foe.vy += (vy / vl) * u.strandKnock;
        /* Counted on the CASTER's window when there is one, so a shove
           delivered by the last volley after the magazine emptied is not
           counted against a window that no longer exists. `netShoves` is the
           per-fighter total and is what the probe reads. */
        if (src.ultNet) src.ultNet.shoves++;
        src.netShoves = (src.netShoves || 0) + 1;
        foe.netShoved = (foe.netShoved || 0) + 1;
      }
    }
  }'''),

]


# ---------------------------------------------------------------- stage five --
# THE STRAND'S ART. Rick, on the stage-3 clip: *"theres no electricity
# connecting the arrow tips. this isnt the ult"* -- and he is right. The
# mechanic was built and measured and the thing on screen was a bow firing
# three arrows.
#
# NUMBERED 5 BECAUSE 4 WAS ALREADY SPENT. The brief's stage 4 is art, sound and
# the director's beat; this builder used stage 4 for the BLADE (gate 3 item 6)
# before the art was asked for. This is the brief's stage 4a. The sound and the
# beat are still unwritten and still Rick's.
#
# PRESENTATION ONLY, AND IT MUST PROVE IT. Nothing here is read by the
# simulation: `engine_ab` must come back identical on every relic INCLUDING
# Gloamwire, which is a stronger control than the earlier stages could run
# because the strand's geometry is unchanged.
#
# FOUR STYLES, BECAUSE RULE 2 SAYS OFFER A SPREAD AND BEING WRONG ABOUT THE
# REGISTER IS WHAT COSTS. `strandArt` selects; the balance cannot see it.
#
# AND THE HOUSE RULES THIS BREAKS IF IT IS CARELESS:
#   * NO `this.rng()`. A relic that is not in the match must not perturb the
#     draw order of one that is, and a field drawn from the sim's RNG would
#     re-invalidate the blade. The flicker is `shellHash` keyed on the volley
#     and on QUANTISED SIM TIME, which is derived rather than accumulated --
#     the same construction rule the splinter's tumble and the kunai's flutter
#     use, and for the same reason: an accumulated angle strobes against the
#     frame interpolator.
#   * NO `createRadialGradient` PER SEGMENT PER FRAME. That is the exact cost
#     that took Cindercleave's capture to 0.19 frames a second -- nine gradient
#     objects a frame became seventy-two inside a lobe loop. Flat strokes under
#     `lighter` do the same job, which is what the fix was.
#   * NO `shadowBlur`. The other half of that same 14x.
#   * AREA, NOT ALPHA, IS WHAT THE BLOOM READS (CLAUDE.md 4.1c/1d). The halo is
#     kept narrow on purpose; 48 strand segments inside four seconds is a
#     full-frame candidate and `ult_bloom_probe` has not been run on it.

S5 = [

("drawstrands", '''  drawShots(m){
    if (!m.shots.length) return;''',
 '''  /* THE STRAND. Rick's section 1: "each arrow connected by a string of purple
     lightning."

     IT IS DRAWN TIP TO TIP AND TESTED CENTRE TO CENTRE, and that is declared
     rather than hidden. `tickNet` measures point-to-segment from the quarry to
     the segment joining the two arrows' CENTRES; this draws from one arrow's
     leading point to the other's, which is where a viewer sees the lightning
     anchored. The two differ by about `s.r` at each end -- 24 units -- against
     a strand that connects at `R + strandW` = 124. Breach's rule is that a beam
     drawn WIDER than it tests is a lie; this is drawn SHORTER than it tests, in
     a mechanic whose reach is five times the discrepancy, and the direction of
     the error is the safe one.

     THE PAIRING RULE IS `tickNet`'s, EXACTLY: adjacent in the fan, both alive,
     and a dead arrow breaks its links rather than handing them on. If these two
     ever disagree the viewer sees lightning that cannot shove, or a shove with
     no lightning, and that is the whole of what this relic is.

     UNDER `drawShots` so the arrows read ON TOP of what connects them: the
     arrows are the objects and the strand is the thing between them. */
  drawStrands(m){
    if (!m.shots.length) return;
    const byVolley = new Map();
    for (const s of m.shots){
      if (!s.net) continue;
      let g = byVolley.get(s.volley);
      if (!g) byVolley.set(s.volley, g = []);
      g.push(s);
    }
    if (!byVolley.size) return;

    const c = this.ctx;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round";
    c.lineJoin = "round";

    /* 30Hz, DERIVED from sim time and never accumulated. A strand redrawn from
       a running counter would strobe against the frame interpolator; this steps
       with the sim and is identical on a replay. */
    const q = Math.floor(m.t * 30);

    for (const g of byVolley.values()){
      if (g.length < 2) continue;
      g.sort((p, r) => p.idx - r.idx);
      const own = g[0].own === "a" ? m.a : m.b;
      const aff = own.aff, U = own.w.ult || {};
      const style = U.strandArt || "%STRANDART%";
      for (let i = 0; i + 1 < g.length; i++){
        const p = g[i], r = g[i + 1];
        if (r.idx !== p.idx + 1) continue;
        const sp0 = Math.hypot(p.vx, p.vy) || 1, sp1 = Math.hypot(r.vx, r.vy) || 1;
        const ax = p.x + p.vx / sp0 * p.r * 1.05;
        const ay = p.y + p.vy / sp0 * p.r * 1.05;
        const bx = r.x + r.vx / sp1 * r.r * 1.05;
        const by = r.y + r.vy / sp1 * r.r * 1.05;
        const dx = bx - ax, dy = by - ay;
        const len = Math.hypot(dx, dy) || 1;
        const nx = -dy / len, ny = dx / len;
        /* SPENT STRANDS GO DIM RATHER THAN DARK. `strandSpent` is the latch
           that says this one has already shoved, so a viewer can see which
           bars are still live -- the same countable-state idea as Breach's
           five chips, for free. */
        const live = p.strandSpent ? 0.45 : 1;
        const key = (p.volley | 0) * 7 + i;

        if (style === "bar"){
          /* A CLEAN BAR. The most legible and the least characterful: two
             strokes, a wide dim halo in the school's core and a thin hot line
             on top of it. This is the control for the other three. */
          c.globalAlpha = 0.26 * live; c.strokeStyle = aff.core;
          c.lineWidth = 9;
          c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();
          c.globalAlpha = 0.95 * live; c.strokeStyle = aff.glow;
          c.lineWidth = 2.4;
          c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke();

        } else if (style === "filament"){
          /* THREE ARCS THAT BOW BY DIFFERENT AMOUNTS. A plasma bundle rather
             than a bolt -- continuous, no jitter, and it reads as tension
             between the two arrows rather than as a discharge. */
          for (let k = 0; k < 3; k++){
            const bow = (k - 1) * len * 0.13
                      + (shellHash(key, k) - 0.5) * len * 0.05;
            const mx = (ax + bx) / 2 + nx * bow, my = (ay + by) / 2 + ny * bow;
            c.globalAlpha = (k === 1 ? 0.95 : 0.55) * live;
            c.strokeStyle = k === 1 ? aff.glow : aff.core;
            c.lineWidth = k === 1 ? 2.2 : 1.4;
            c.beginPath();
            c.moveTo(ax, ay); c.quadraticCurveTo(mx, my, bx, by); c.stroke();
          }

        } else {
          /* A BOLT: a jagged polyline whose lateral offsets are hashed on the
             volley, the segment and quantised time, so it CRACKLES without any
             stored state and without a single call to the sim's RNG.

             The offset is scaled by `sin(pi t)` so the path is pinned at both
             ends -- lightning that wandered away from the arrow tip it is
             supposed to be anchored to is the one thing this picture cannot
             do, because the anchor IS the mechanic. */
          const SEG = 7, amp = Math.min(26, len * 0.17);
          const px = [], py = [];
          for (let k = 0; k <= SEG; k++){
            const t = k / SEG;
            const w = (k === 0 || k === SEG)
                    ? 0
                    : (shellHash(key * 31 + k, q) - 0.5) * 2 * amp
                      * Math.sin(Math.PI * t);
            px.push(ax + dx * t + nx * w);
            py.push(ay + dy * t + ny * w);
          }
          const path = () => {
            c.beginPath(); c.moveTo(px[0], py[0]);
            for (let k = 1; k <= SEG; k++) c.lineTo(px[k], py[k]);
            c.stroke();
          };
          c.globalAlpha = 0.22 * live; c.strokeStyle = aff.core;
          c.lineWidth = 8; path();
          c.globalAlpha = 0.90 * live; c.strokeStyle = aff.glow;
          c.lineWidth = 2.0; path();
          if (style === "chain"){
            /* NODES. The bolt with a bright bead at every vertex, which is the
               one variant that reads as DISCRETE -- a chain of links rather
               than a continuous arc. */
            c.globalAlpha = 0.95 * live; c.fillStyle = aff.glow;
            for (let k = 1; k < SEG; k++){
              c.beginPath(); c.arc(px[k], py[k], 2.1, 0, TAU); c.fill();
            }
          }
        }
      }
    }
    c.globalAlpha = 1;
    c.restore();
  }

  drawShots(m){
    if (!m.shots.length) return;'''),

("draw-order", '''    this.drawDrains(m);
    this.drawShots(m);''',
 '''    this.drawDrains(m);
    /* UNDER the arrows: they are the objects and this is what runs between
       them. Over the fighters, because a strand crosses the room. */
    this.drawStrands(m);
    this.drawShots(m);'''),

("ult-strandart", '''          dmgMul:%DMGMUL%, strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,
          tip:"%TIP%" },''',
 '''          dmgMul:%DMGMUL%, strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,
          /* PURE LOOK, and the balance cannot see it -- `drawStrands` is the
             only reader and `engine_ab` is identical on all 31 relics with it
             set to any value. Four registers were offered as a spread because
             rule 2 asks for one and because being wrong about the REGISTER is
             what costs: "bolt" crackles, "chain" is the same bolt with beads
             at its vertices, "filament" is three continuous arcs under
             tension, and "bar" is a clean two-stroke beam and the control for
             the other three. */
          strandArt:"%STRANDART%",
          tip:"%TIP%" },'''),

]


# ----------------------------------------------------------------- stage six --
# EXTRA PROJECTILE SPEED. Rick, 2026-09-01, on the stage-5 clip: *"lets also
# give the arrows extra projectile speed"* -- a fifth strength clause on an
# ultimate that already had four, and it is his to add.
#
# A RESCALE OF THE VELOCITY THE TYPE ALREADY SET, never a fresh vector. This is
# Marrowdraw's own construction, and its comment says why: everything the TYPE
# owns -- where the shot leaves from, that it inherits none of the ball's
# velocity, that it points along the facing -- has to stay decided by one piece
# of code for all six bows. A bolt built from a new vector can end up travelling
# somewhere the arrow would not have.
#
# AND IT IS NOT FREE, WHICH IS THE PART WORTH MEASURING RATHER THAN ASSUMING:
#   * a faster arrow crosses a spinning blade's swept area in fewer frames, so
#     the PARRY should fall -- and the parry is a property of the foe's
#     geometry, spread 4.6% to 14.4% across the types;
#   * it spends less time in the air, so fewer are alive at once and `maxLive`
#     gets even further away;
#   * the fan's GAP is a function of range and not of speed, so the strand
#     geometry at a given separation is unchanged -- but the volley reaches
#     that separation sooner, which is not the same thing as reaching further.
#
# **IT VOIDS THE BLADE.** `dmg` 9.0 was measured at speed 380 over 12,240
# fights. Anything that moves the contact rate moves the crossing, and
# `gloamwire_sweep.py` has to run again.

S6 = [

("speedmul", '''        /* A MULTIPLIER OF WHAT THE TYPE ALREADY SET, never an assignment, so
           the shot block stays the one thing that decides what an arrow is. */
        s.dmgMul = s.dmgMul * u.dmgMul;''',
 '''        /* A MULTIPLIER OF WHAT THE TYPE ALREADY SET, never an assignment, so
           the shot block stays the one thing that decides what an arrow is. */
        s.dmgMul = s.dmgMul * u.dmgMul;
        /* AND THE SAME RULE FOR THE SPEED. Rick: "lets also give the arrows
           extra projectile speed." Applied as a RESCALE of the velocity
           `spawnShot` already computed rather than as a fresh vector, which is
           Marrowdraw's construction and for its stated reason: the direction
           stays the type's business and only the magnitude is this window's.

           `=== undefined` and not `|| 1` (CLAUDE.md 4.3): a sweep must be able
           to set this to 0 and must be able to say "no change" with 1. */
        if (u.speedMul !== undefined && u.speedMul !== 1){
          s.vx *= u.speedMul; s.vy *= u.speedMul;
        }'''),

("ult-speedmul", '''          dmgMul:%DMGMUL%, strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,''',
 '''          dmgMul:%DMGMUL%, speedMul:%SPEEDMUL%,
          strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,'''),

]


# --------------------------------------------------------------- stage seven --
# HOLD THE TRIO. Rick, after watching the built relic: *"what if the arrows
# stuck until all 3 had a chance to collide? that way their trio is always alive
# together"*, and then *"the stuck arrow is inert, and the strand still
# shoves."*
#
# `06-docs/v61/crossweave-amendment-v61.md` is the design and this implements
# it. WHY IT IS NEEDED, measured: only 51% of volleys still have all three
# arrows by the first frame they can be drawn, and 31.5% of arrow-frames show an
# arrow with no live neighbour -- 28.2% of them a lone survivor with both
# siblings already in the wall.
#
# AND THE TWO THINGS THAT COULD HAVE KILLED IT WERE MEASURED FIRST:
#   * `CONFIG.shot.maxLive` is 64 and `spawnShot` SHIFTS the oldest off the
#     front SILENTLY at the cap -- which would delete the very arrows this
#     exists to keep. Peak live goes 15 -> 23. Asserted by the probe, not
#     assumed.
#   * a stuck arrow sits a median 0.37s and at most 1.84s over 3,204 volleys,
#     so a wall does not grow a hedge.

S7 = [

("stuck-inert", '''      const s = this.shots[i];
      /* --- THE HOMING.''',
 '''      const s = this.shots[i];
      /* A STUCK ARROW IS INERT AND THIS ONE LINE IS THE WHOLE OF IT. Rick's
         ruling, verbatim: "the stuck arrow is inert, and the strand still
         shoves." It has already had its effect -- it hit, or was batted down,
         or reached stone -- so it does not move, cannot hit, cannot be hit,
         cannot be parried and cannot resolve a second time. `continue` before
         any of that is the cheapest possible statement of it, and it is
         auditable: nothing below this line can reach a stuck shot.

         WHAT IT IS STILL DOING is being a strand ENDPOINT. `tickNet` and
         `drawStrands` both walk `m.shots` and neither tests `stuck`, so a
         volley that has lost an arrow to the wall keeps its lightning anchored
         where that arrow landed -- which is the entire reason for this
         stage. */
      if (s.stuck) continue;
      /* --- THE HOMING.'''),

("hold-and-release", '''      if (dead) this.shots.splice(i, 1);
    }
  }''',
 '''      /* HELD, NOT REMOVED. A Crossweave arrow that resolves stays in
         `m.shots` as an inert anchor so its volley's strands survive it. Every
         other projectile in the game is spliced out here exactly as before --
         the branch is gated on `s.net` and reaches nothing else. */
      if (dead && s.net && !s.stuck){
        s.stuck = true; s.vx = 0; s.vy = 0; s.life = 1e9;
      } else if (dead) this.shots.splice(i, 1);
    }
    this.releaseVolleys();
  }

  /* THE VOLLEY CLEARS AS A UNIT, and it is a separate pass rather than part of
     the loop above because releasing a volley touches arrows at other indices
     and a reverse loop that splices its own siblings is how an off-by-one gets
     shipped.

     RELEASED WHEN EVERY ARROW PRESENT IS STUCK, not when three are. A volley
     whose arrow was shifted off the front by `CONFIG.shot.maxLive` would
     otherwise be held for ever -- measured at peak 23 against a cap of 64, so
     it cannot happen today, and this does not rely on that staying true. */
  releaseVolleys(){
    if (!this.shots.length) return;
    const byVolley = new Map();
    for (const s of this.shots){
      if (!s.net) continue;
      let g = byVolley.get(s.volley);
      if (!g) byVolley.set(s.volley, g = []);
      g.push(s);
    }
    if (!byVolley.size) return;
    let done = null;
    for (const [vid, g] of byVolley){
      let all = true;
      for (const s of g) if (!s.stuck){ all = false; break; }
      if (all) (done || (done = [])).push(vid);
    }
    if (!done) return;
    for (const vid of done){
      const g = byVolley.get(vid);
      this.volleyDone(g);
      for (let i = this.shots.length - 1; i >= 0; i--)
        if (this.shots[i].net && this.shots[i].volley === vid)
          this.shots.splice(i, 1);
    }
  }

  /* STAGE 8 FILLS THIS IN. In stage 7 a completed volley simply clears, so the
     hold can be measured on its own before a damage channel is added on top of
     it -- the same reason the brief separated the fan from the strand. */
  volleyDone(g){}'''),

]


# --------------------------------------------------- stage seven, the guard --
# THE CAP IS SHARED AND HOLDING ARROWS MADE IT BITE. `CONFIG.shot.maxLive` is 64
# across BOTH fighters, so Gloamwire's 24 held arrows plus an opponent's volley
# ultimate can cross it -- measured at 3 evictions in 12,327 arrows, on 0.004%
# of frames. Small, and the check exists because a SILENT deletion invalidates
# whatever it deleted.
#
# THE FIX IS WHICH ARROW GOES, NOT HOW MANY THERE ARE. `shift()` drops the
# OLDEST, which may be an arrow still in flight that has not yet had its effect.
# A STUCK arrow has already resolved -- it hit, or was parried, or reached stone
# -- and is inert scenery holding a strand endpoint. Dropping that first costs a
# strand a little early; dropping a flying one costs a shot the relic bought.
#
# GATED ON `s.stuck`, WHICH ONLY THIS RELIC EVER SETS, so all four call sites
# behave exactly as before for every other projectile in the game.

S7B = [

("makeroom", '''  spawnShot(f, angle){
    const S = f.w.shot;''',
 '''  /* ROOM FOR ONE MORE, AND IT CHOOSES WHAT TO LOSE. The plain `shift()` this
     replaces drops the oldest shot in the hall, which may be an arrow still in
     flight; a Crossweave arrow that is STUCK has already resolved and is inert.
     Losing one of those early costs a strand a fraction of a second. Losing a
     flying shot costs a hit that was going to happen.

     Inert for every other relic in the game: nothing else sets `stuck`. */
  makeRoom(){
    if (this.shots.length < CONFIG.shot.maxLive) return;
    for (let i = 0; i < this.shots.length; i++){
      if (this.shots[i].stuck){ this.shots.splice(i, 1); return; }
    }
    this.shots.shift();
  }

  spawnShot(f, angle){
    const S = f.w.shot;'''),

]


# --------------------------------------------------------------- stage eight --
# THE NOVA. Rick: *"how about when all 3 connect the arrows explode in a nova
# for more damage and knockback?"* and, on what "connect" means, *"once all 3
# arrows expire. so either by the wall or by hitting an enemy. should mean all of
# them explode."* And on the scale: *"less than an arrow. its more about the
# visual show. so i think the knockback should be most of the payoff."*
#
# SO THE TRIGGER IS THE VOLLEY COMPLETING, WHICH IS EVERY VOLLEY. 24 a cast at
# 5.9 a second, three detonations each -- 72 novas in 4.1 seconds. The strict
# reading (all three landing ON the quarry) was measured first and is dead: 3
# volleys in 8,315, one fight in fifty.
#
# THE FAILURE MODE IS DEADFALL'S AND IT IS NAMED SO IT CANNOT BE FOUND LATE.
# v54 paid a pentagram in five charges of `stamp/5` -- five damage numbers over
# the ball across 42 milliseconds, every number right, and it read as noise.
# Rick's own fix was ONE large mine. Seventy-two novas in four seconds is that
# shape again, and the question it has to answer is whether three detonations at
# three points read as one event.

S8 = [

("nova", '''  /* STAGE 8 FILLS THIS IN. In stage 7 a completed volley simply clears, so the
     hold can be measured on its own before a damage channel is added on top of
     it -- the same reason the brief separated the fan from the strand. */
  volleyDone(g){}''',
 '''  /* THE VOLLEY DETONATES. Every arrow of a completed volley explodes where it
     stuck -- which is mostly ON THE WALL, because 85.7% of Crossweave arrows
     end there, so this is a rim of blasts around the hall far more often than
     three around the quarry.

     THE KNOCKBACK IS THE PAYOFF AND THE DAMAGE IS NOT. Rick's scale, verbatim:
     "less than an arrow. its more about the visual show. so i think the
     knockback should be most of the payoff." `novaDmg` is a multiplier of the
     BLADE, not of the arrow, so at %NOVADMG% it is about a quarter of what one
     Crossweave arrow carries.

     THE IMPULSE IS FROM THE BLAST, NOT FROM THE ARCHER. `resolveHit`'s own
     knock fires away from the CASTER, which for a nova standing on a wall on
     the far side of the room points the wrong way entirely. The Thicket's rule:
     a hazard that is not the caster needs its own bearing.

     AND IT APPLIES CURSE, WHICH IS RICK'S RULING OVER THIS BUILDER'S SAFE
     DEFAULT. The first cut passed `over.onHit = {}` to suppress it, reasoning
     that seventy-two tiny blows a cast would push seventy-two tiny memories
     into a three-deep pool. Rick, 2026-09-01: "the novas should also apply
     curse."

     UNDER TODAY'S CURSE RULE THE WORRY IS MISPLACED, WHICH IS WHY IT IS SAFE.
     `pushCurse` keeps the three BIGGEST and displaces the WEAKEST, so a
     3.2-damage nova memory offered to a pool already holding the blade's
     13-damage ones is refused. It refreshes the clock and adds nothing --
     v49 section 5b's own finding arriving from the other side.

     ** IT IS NOT SAFE UNDER THE PENDING RULE. ** `06-docs/CLAIMS.md` carries
     a school-wide change, Rick's, 2026-09-02: the pool keeps the LAST 3 hits
     instead of the 3 BIGGEST, marked to land AFTER Gloamwire ships. Under
     LAST-3 these seventy-two tiny memories ARE the last three almost always,
     and this ultimate would overwrite its own school's memory with its own
     noise. Whoever lands that change must re-price this path. */
  volleyDone(g){
    if (!g || !g.length) return;
    const src = g[0].own === "a" ? this.a : this.b;
    const foe = g[0].own === "a" ? this.b : this.a;
    const u = src.w.ult;
    if (!u || u.novaKnock === undefined) return;
    const R = CONFIG.physics.ballR;
    let caught = 0;
    for (const s of g){
      /* A FIRST CUT AND NOTHING MORE. The register is Rick\\'s (rule 2) and this
         is the engine\\'s existing vocabulary -- a ring and a spark burst in the
         school\\'s own palette -- so the payload is not invisible while it waits
         for him. An ultimate that shoves with nothing on screen is the fault he
         rejected on the stage-3 clip. */
      this.ring(s.x, s.y, src.aff.glow, 3, u.novaRad, 0.28, 4);
      this.spawnFx(s.x, s.y, src.aff.core, 10, 280, 0.34, 2.8);
      if (!foe.alive || !src.alive) continue;
      const dx = foe.x - s.x, dy = foe.y - s.y;
      const d = Math.hypot(dx, dy);
      if (d > u.novaRad + R) continue;
      caught++;
      const dl = d || 1;
      foe.vx += (dx / dl) * u.novaKnock;
      foe.vy += (dy / dl) * u.novaKnock;
      const seg = { ax: s.x - 8, ay: s.y, bx: s.x + 8, by: s.y, a: 0 };
      this.resolveHit(src, foe, s.x, s.y, seg, u.novaDmg);
    }
    if (caught){
      this.shake = Math.min(38, this.shake + 4);
      SFX.play("clank");
    }
  }'''),

("ult-nova", '''          strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,''',
 '''          strandW:%STRANDW%, strandKnock:%STRANDKNOCK%,
          /* THE NOVA. PLACEHOLDERS, all three, and they must be swept.
             `novaDmg` is a multiplier of the BLADE: at %NOVADMG% one nova is
             about a quarter of one Crossweave arrow, which is Rick\\'s scale --
             "less than an arrow ... the knockback should be most of the
             payoff." `novaKnock` %NOVAKNOCK% against the strand\\'s
             %STRANDKNOCK% is where that payoff is. */
          novaRad:%NOVARAD%, novaDmg:%NOVADMG%, novaKnock:%NOVAKNOCK%,'''),

]


# ---------------------------------------------------------------- stage nine --
# A BIG PURPLE EXPLOSION. Rick: *"can we make the animation for the novas
# louder? a big purple explosion."*
#
# AND IT IS DRAWN, NOT SPAWNED, WHICH IS THE WHOLE ENGINEERING OF THIS STAGE.
# `spawnFx` draws from `this.rng()`, so every particle it makes is part of the
# simulation's own random stream -- Cindercleave's note, verbatim: "The sparks
# are DRAWN and not spawned: `spawnFx` draws from `this.rng()`, so a debris
# field would have moved every Cindercleave fight and re-invalidated the blade."
# Stage 8's nova used `spawnFx`, so making it louder would have moved every
# Gloamwire fight -- and would do so again every time the explosion was asked to
# grow. This replaces it with a presentation record the RENDERER expands, so the
# art is free and provable: `engine_ab` must come back identical on all 31.
#
# TICKED IN `tickPresentation` AND NOT ON THE NORMAL PATH, which is v54's
# lesson: a detonation sets `hitStop`, and `step()` returns through
# `decayImpactOnly` for as long as that runs, so a clock on the normal path
# freezes for exactly the frames the viewer is staring hardest at. Deadfall's
# blast froze on the floor 96.2% of the time for precisely this reason.
#
# NO GRADIENTS AND NO `shadowBlur`. Seventy-two of these in four seconds is the
# load that took Cindercleave's capture to 0.19 frames a second when a
# `createRadialGradient` went inside a per-lobe loop. Flat discs under
# `lighter` do the same job -- which is what that fix was.

S9 = [

("nova-record", '''      this.ring(s.x, s.y, src.aff.glow, 3, u.novaRad, 0.28, 4);
      this.spawnFx(s.x, s.y, src.aff.core, 10, 280, 0.34, 2.8);''',
 '''      /* A RECORD, NOT A PARTICLE FIELD. `spawnFx` would consume `this.rng()`
         and put this relic's art inside its own simulation; the renderer
         expands this into the whole explosion and the sim never knows. */
      (this.novaFx || (this.novaFx = [])).push({
        x: s.x, y: s.y, t: 0, life: 0.62,
        aff: src.aff, seq: (this.novaSeq = (this.novaSeq || 0) + 1) });
      if (this.novaFx.length > 120) this.novaFx.shift();'''),

("nova-tick", '''  tickPresentation(dt){''',
 '''  /* THE NOVA'S CLOCK, and it is here rather than in a tick for the reason
     `tickPresentation` already gives about status tags: every detonation sets
     `hitStop`, and a clock on the normal path stops for exactly the frames the
     viewer is watching hardest. Deadfall shipped that bug and 96.2% of its
     blasts froze mid-expansion. */
  tickNovaFx(dt){
    if (!this.novaFx || !this.novaFx.length) return;
    for (let i = this.novaFx.length - 1; i >= 0; i--){
      const f = this.novaFx[i];
      f.t += dt;
      if (f.t >= f.life) this.novaFx.splice(i, 1);
    }
  }

  tickPresentation(dt){
    this.tickNovaFx(dt);'''),

("nova-draw", '''    this.drawStrands(m);
    this.drawShots(m);''',
 '''    this.drawNovas(m);
    this.drawStrands(m);
    this.drawShots(m);'''),

("nova-draw-fn", '''  drawStrands(m){
    if (!m.shots.length) return;''',
 '''  /* THE NOVA, EXPANDED FROM ONE RECORD. Everything here is derived from `t`
     and from `shellHash(seq, k)` -- no stored state, no `this.rng()`, no
     gradients and no `shadowBlur`. Seventy-two of these live inside four
     seconds and the last two are why: they are the pair that took
     Cindercleave's capture to 0.19 frames a second.

     THE SHAPE IS A FLASH, A SHELL AND A SPRAY. The flash is one bright disc
     that dies almost at once and is what makes it read as a detonation rather
     than as a bubble. The shell is two rings racing outward at different rates
     so the edge has thickness. The spray is sixteen streaks whose bearings are
     hashed off the record's own sequence number, so every blast is a different
     one and a replay draws the same different one. */
  drawNovas(m){
    if (!m.novaFx || !m.novaFx.length) return;
    const c = this.ctx;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round";
    for (const f of m.novaFx){
      const k = clamp(f.t / f.life, 0, 1);
      const ease = 1 - Math.pow(1 - k, 2.2);
      const fade = 1 - k;
      const R = 96 * ease;

      /* THE FLASH -- gone in the first sixth, and it is the whole "boom". */
      const fl = clamp(1 - k * 6, 0, 1);
      if (fl > 0){
        c.globalAlpha = 0.55 * fl;
        c.fillStyle = f.aff.glow;
        c.beginPath(); c.arc(f.x, f.y, 26 * (0.5 + fl), 0, TAU); c.fill();
      }

      /* THE SHELL -- two rings, the outer one thinner and further. */
      c.globalAlpha = 0.50 * fade;
      c.strokeStyle = f.aff.glow;
      c.lineWidth = 5 * fade + 1;
      c.beginPath(); c.arc(f.x, f.y, R, 0, TAU); c.stroke();
      c.globalAlpha = 0.30 * fade;
      c.strokeStyle = f.aff.core;
      c.lineWidth = 9 * fade + 1;
      c.beginPath(); c.arc(f.x, f.y, R * 0.68, 0, TAU); c.stroke();

      /* THE SPRAY. Sixteen streaks, each on its own hashed bearing and its own
         hashed reach, drawn from a point that leaves the centre so the blast
         opens rather than inflates. */
      c.globalAlpha = 0.60 * fade * fade;
      c.strokeStyle = f.aff.core;
      c.lineWidth = 2.2;
      c.beginPath();
      for (let j = 0; j < 16; j++){
        const a = shellHash(f.seq, j) * TAU;
        const rr = R * (0.72 + 0.55 * shellHash(f.seq + 977, j));
        const ca = Math.cos(a), sa = Math.sin(a);
        c.moveTo(f.x + ca * rr * 0.55, f.y + sa * rr * 0.55);
        c.lineTo(f.x + ca * rr,        f.y + sa * rr);
      }
      c.stroke();
    }
    c.globalAlpha = 1;
    c.restore();
  }

  drawStrands(m){
    if (!m.shots.length) return;'''),

]


# ----------------------------------------------------------------- stage ten --
# THE NOVA'S VOICE, FITTED TO RICK'S REFERENCE BY MEASUREMENT. He supplied
# `Occultist Profane Boom Feels GOOD.wav` and named the two POPS in it (2.2s and
# 3.9s), not the loud hit at the end -- which is a different sound entirely and
# has essentially no sub at all (0.3% below 120 Hz against the pops' 56-64%).
#
# THERE IS NO SAMPLER IN THIS PROJECT, so a reference cannot be used, only
# measured and matched. `nova_voice_lab.py` renders candidates through
# `buildChain` -- the path that ships -- and scores them against five numbers
# taken off the reference. The fit went 48.8 -> 6.4 over three passes and each
# pass failed for a reason worth keeping:
#
#   THE TAIL. `exponentialRampToValueAtTime(0.0001, t+dur)` crosses 10% of peak
#   at ~29% of `dur`, so a 0.52s tone is audible for 150 ms, not 500.
#
#   THE CENTROID. An 18-point grid on the sub/air ratio moved `<120Hz` by one
#   point, because the sub RINGS and the bursts do not: over the window the
#   body outweighs the top whatever its gain. The reference carries 43% of its
#   energy above 120 Hz across the whole pop, so the top is a third of the
#   sound and has to decay WITH the body.
#
#   AND `_burst`'s OWN BUG IS THE RIGHT SHAPE HERE. CLAUDE.md 4.5: it does not
#   loop its 0.6s noise buffer. At `dur` 1.5 the gain envelope is still at ~15%
#   when the buffer runs dry at 0.6s -- which is where this sound should end
#   anyway. The defect and the requirement coincide, and that is worth knowing
#   before somebody "fixes" `_burst`.
#
# ONE POP PER VOLLEY, NOT PER NOVA. Three novas fire together and 72 land in
# 4.1s; at one voice each that is 17.5 a second with a 450 ms tail, which is
# nine overlapping and is a texture rather than a sound. Per volley it is 5.9 a
# second. Deadfall came down the same way for the same reason.

S10 = [

("nova-voice", '''      else if (kind === "clank"){''',
 '''      else if (kind === "nova"){
        /* MEASURED AGAINST RICK'S REFERENCE, not chosen. Rendered through
           `buildChain` in an OfflineAudioContext: peak 0.198, attack 37 ms
           (his pops 40-190), tail to 10% 449 ms (480-630), 67.3% under 120 Hz
           in the first 60 ms (68-74%), centroid 969 Hz (520-710). Sub-heavy at
           the open and broadband through the decay, which is the shape of a
           deathbloom rather than of a crack.

           PEAK 0.198 AGAINST DEADFALL'S 0.605 IS DELIBERATE. That one fires
           three times a fight; this fires 5.9 times a second. */
        this._tone (t, { freq: 92, to: 30, gain: 0.110, dur: 1.15, type:"sine" });
        this._tone (t, { freq: 58, to: 24, gain: 0.083, dur: 1.27, type:"sine" });
        this._burst(t, { freq: 300,  q: 0.7, gain: 0.300, dur: 1.50, type:"lowpass" });
        this._burst(t, { freq: 1300, q: 0.7, gain: 0.255, dur: 1.30, type:"bandpass" });
        this._burst(t, { freq: 3000, q: 0.8, gain: 0.120, dur: 0.75, type:"highpass" });
      }
      else if (kind === "clank"){'''),

("nova-voice-call", '''    if (caught){
      this.shake = Math.min(38, this.shake + 4);
      SFX.play("clank");
    }''',
 '''    /* THE VOICE IS PER VOLLEY AND FIRES WHETHER OR NOT IT CONNECTED -- the
       explosion happens either way and it is most of what this ultimate is for.
       The SHAKE is still gated on a catch, because that is the part that says
       the quarry was in it. */
    SFX.play("nova");
    if (caught) this.shake = Math.min(38, this.shake + 4);'''),

]


# -------------------------------------------------------------- stage eleven --
# ONE POP PER NOVA. Rick, on the clip: *"the pop is perfect. lets do 1 per nova
# instead of 1 per volly."* Stage 10 shipped one per VOLLEY on the reasoning
# that 17.5 voices a second against a 450 ms tail is a texture; he has heard it
# and ruled.
#
# AND THREE ON THE SAME FRAME NEED A STAGGER OR THEY ARE NOT THREE. A volley
# completes when its LAST arrow resolves, so all three novas fire on one frame
# at one `currentTime`. Identical voices scheduled at the same instant are
# phase-coherent: the sines sum to 3x amplitude and the ear hears ONE louder
# pop, which is the opposite of what "one per nova" is for. `clank` already
# solves this in this file -- it spaces five partials by 1.5 ms apiece -- and
# this uses the same trick at a length the ear reads as separate events rather
# than as one thickened one.
#
# THE OFFSET IS DERIVED FROM THE ARROW'S OWN `idx`, so it is deterministic, it
# is the same on a replay, and the three pops arrive in the order the fan was
# fired in rather than in whatever order the volley happened to be stored.

S11 = [

("nova-voice-per-arrow", '''    /* THE VOICE IS PER VOLLEY AND FIRES WHETHER OR NOT IT CONNECTED -- the
       explosion happens either way and it is most of what this ultimate is for.
       The SHAKE is still gated on a catch, because that is the part that says
       the quarry was in it. */
    SFX.play("nova");
    if (caught) this.shake = Math.min(38, this.shake + 4);''',
 '''    if (caught) this.shake = Math.min(38, this.shake + 4);'''),

("nova-voice-in-loop", '''      (this.novaFx || (this.novaFx = [])).push({''',
 '''      /* ONE PER NOVA, STAGGERED BY THE ARROW'S OWN POSITION IN THE FAN.
         Rick's, over one per volley. All three resolve on the same frame, so
         without the offset they are one voice at 3x amplitude rather than
         three voices -- `clank` spaces its five partials by 1.5 ms for the same
         reason. `idx` is 0, 1, 2 across the fan, so the triplet always flams in
         the order the arrows were loosed. */
      SFX.play("nova", { k: s.idx || 0 });
      (this.novaFx || (this.novaFx = [])).push({'''),

("nova-voice-offset", '''        this._tone (t, { freq: 92, to: 30, gain: 0.110, dur: 1.15, type:"sine" });
        this._tone (t, { freq: 58, to: 24, gain: 0.083, dur: 1.27, type:"sine" });
        this._burst(t, { freq: 300,  q: 0.7, gain: 0.300, dur: 1.50, type:"lowpass" });
        this._burst(t, { freq: 1300, q: 0.7, gain: 0.255, dur: 1.30, type:"bandpass" });
        this._burst(t, { freq: 3000, q: 0.8, gain: 0.120, dur: 0.75, type:"highpass" });''',
 '''        /* THE FLAM. `k` is the arrow's index in the fan and the three novas
           of one volley land on one frame; 26 ms apart the ear reads three
           events, and at 0 it reads one pop at three times the amplitude. */
        const tk = t + (p.k || 0) * 0.026;
        this._tone (tk, { freq: 92, to: 30, gain: 0.110, dur: 1.15, type:"sine" });
        this._tone (tk, { freq: 58, to: 24, gain: 0.083, dur: 1.27, type:"sine" });
        this._burst(tk, { freq: 300,  q: 0.7, gain: 0.300, dur: 1.50, type:"lowpass" });
        this._burst(tk, { freq: 1300, q: 0.7, gain: 0.255, dur: 1.30, type:"bandpass" });
        this._burst(tk, { freq: 3000, q: 0.8, gain: 0.120, dur: 0.75, type:"highpass" });'''),

]


# ------------------------------------------------------------------ helpers --

def one(src: str, old: str, new: str, label: str) -> str:
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def alln(src: str, old: str, new: str, label: str, n: int) -> str:
    """The same edit at every one of its N sites, and it refuses on N-1.

    `one()` is the right shape when an anchor is unique. `CONFIG.shot.maxLive`
    is evicted at FOUR call sites and a fix applied to one of them is a fix that
    works until the next relic spawns a projectile.
    """
    got = src.count(old)
    if got != n:
        raise SystemExit(f"ANCHOR {label}: expected {n} occurrences, found {got}")
    print(f"  ok    {label}  ({n} sites)")
    return src.replace(old, new)


def strip_comments(js: str) -> str:
    """Code with the prose taken out.

    CLAUDE.md: "a check that cannot tell code from the comment explaining it
    fires on its own explanation." Every refusal below greps shipped source and
    this build explains itself IN that source -- the relic's own comment has to
    be able to say the words "do not borrow f.ultBal".
    """
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def entry(s: str, rid: str) -> str:
    """One relic's own WEAPONS entry, by brace matching from its id."""
    i = s.index(f'id:"{rid}"')
    j = s.rindex("{", 0, i)
    depth, k = 0, j
    while k < len(s):
        if s[k] == "{":
            depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0:
                return s[j:k + 1]
        k += 1
    raise SystemExit(f"unbalanced braces in the entry for {rid}")


def shot_block(s: str, rid: str) -> str:
    """The `shot` object of one relic, comments stripped, whitespace collapsed."""
    e = strip_comments(entry(s, rid))
    m = re.search(r"shot:\s*\{", e)
    if not m:
        return ""
    j = e.index("{", m.start())
    depth, k = 0, j
    while k < len(e):
        if e[k] == "{":
            depth += 1
        elif e[k] == "}":
            depth -= 1
            if depth == 0:
                return re.sub(r"\s+", " ", e[j:k + 1]).strip()
        k += 1
    return ""


def ult_matches(s: str, A, stage: int) -> None:
    """The shipped `ult` block carries every number this run printed.

    v56's own failure, verbatim: the stage-2 insert wrote the whole `ult` block
    and stage 3 rewrote only the line carrying `charge`, so `--stage 3
    --cadence 2.0` LOGGED the new rhythm and SHIPPED the old one, and every gate
    downstream measured a relic the log was not describing.
    """
    e = strip_comments(entry(s, RELIC))
    m = re.search(r"ult:\s*\{", e)
    if not m:
        raise SystemExit("the shipped relic has no `ult` block")
    j = e.index("{", m.start())
    depth, k = 0, j
    while k < len(e):
        if e[k] == "{":
            depth += 1
        elif e[k] == "}":
            depth -= 1
            if depth == 0:
                break
        k += 1
    blk = e[j:k + 1]
    want = {"name": f'"{A.ult}"'}
    if stage == 1:
        want["charge"] = "1e9"
        want["kind"] = '"net"'
    else:
        want["charge"] = f"{A.charge:g}"
        want["kind"] = '"net"'
        # EVERY NUMBER, FROM STAGE 2 ON. `strandW` and `strandKnock` are inert
        # until stage 3 and are still checked here, because the failure this
        # guard exists for is v56's: a stage-2 insert wrote the block, stage 3
        # rewrote one line of it, and the run LOGGED numbers it had not shipped.
        for key in ("volleys", "n", "spread", "cadmul", "dmgmul",
                    "strandw", "strandknock"):
            want[{"cadmul": "cadMul", "dmgmul": "dmgMul",
                  "strandw": "strandW", "strandknock": "strandKnock"
                  }.get(key, key)] = f"{getattr(A, key):g}"
        if stage >= 6:
            want["speedMul"] = f"{A.speedmul:g}"
        if stage >= 8:
            for k in ("novarad", "novadmg", "novaknock"):
                want[{"novarad": "novaRad", "novadmg": "novaDmg",
                      "novaknock": "novaKnock"}[k]] = f"{getattr(A, k):g}"
    missing = []
    for key, val in want.items():
        if not re.search(rf"\b{re.escape(key)}\s*:\s*{re.escape(val)}\s*[,}}]", blk):
            missing.append(f"{key}:{val}")
    if missing:
        raise SystemExit(
            "REFUSING TO WRITE -- the shipped `ult` block does not carry what "
            "this run printed:\n  missing " + ", ".join(missing)
            + "\n  (v56 shipped an ultimate whose numbers the log did not "
              "describe. Never again.)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, required=True,
                    choices=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--strandart", default=STRAND_ART,
                    choices=("bolt", "chain", "filament", "bar"),
                    help="stage 5. PURE LOOK -- the balance cannot see it.")
    ap.add_argument("--dmg", type=float, default=None,
                    help="stages 1-3: the starting blade (default %.2f). "
                         "stage 4: the swept one, and it has no default"
                         % BLADE_IN)
    for k, v in ULT.items():
        ap.add_argument(f"--{k}", type=float, default=v)
    A = ap.parse_args()
    if A.dmg is None:
        A.dmg = TUNED_GW if (A.stage == 4 and TUNED_GW is not None) else BLADE_IN

    src = A.src or {1: "../02-chain/sc-garrote.html",
                    2: "../02-chain/sc-gloamwire.html",
                    3: "../02-chain/sc-volley.html",
                    4: "../02-chain/sc-crossweave.html"}[A.stage]
    out = A.out or {1: "../02-chain/sc-gloamwire.html",
                    2: "../02-chain/sc-volley.html",
                    3: "../02-chain/sc-crossweave.html",
                    4: "../02-chain/sc-crossweave.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nGLOAMWIRE -- STAGE {A.stage}: "
          + {1: "the 31st relic, its ultimate stubbed",
             2: "THE VOLLEY -- a triple shot and the fan. No strand",
             3: "CROSSWEAVE -- the strand, the shove, the magazine",
             4: "THE BLADE -- gate 3 item 6, and NOT the brief's stage 4, "
                "which is art",
             5: "THE STRAND'S ART -- the brief's stage 4a. Presentation only",
             6: "EXTRA PROJECTILE SPEED -- Rick's, and it VOIDS THE BLADE",
             7: "HOLD THE TRIO -- a resolved arrow sticks, inert, until its "
                "volley completes",
             8: "THE NOVA -- every completed volley detonates where it stuck",
             9: "A BIG PURPLE EXPLOSION -- Rick's, and DRAWN rather than "
                "spawned so it costs the sheet nothing",
            10: "THE NOVA'S VOICE -- fitted to Rick's reference by measurement",
            11: "ONE POP PER NOVA -- Rick's, over one per volley, flammed 26ms"
             }[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR. Every stage asserts what has to be under it.
    if "cursePool" not in s0:
        raise SystemExit("this source has no cursePool -- the curse rework is "
                         "upstream of this whole chain, and Crossweave's whole "
                         "pool claim rests on it")
    if "tickWire" not in s0:
        raise SystemExit("this source is not the v60 tip -- `tickWire` is "
                         "absent. Build off `sc-garrote.html`; the brief's "
                         "`sc-breach.html` predates Ravelbone.")

    # THE SHOT IS A PROPERTY OF THE TYPE, ASSERTED AND NOT ASSUMED. The design
    # rests on it -- every number in it was measured on Ironhail's body and is
    # only transferable if the block really is shared. `net_lab` [0] asserts the
    # same thing at runtime; this asserts it before a byte is written.
    bows = ["ironhail", "farwarden", "aureole", "vinesower", "marrowdraw"]
    blocks = {b: shot_block(s0, b) for b in bows}
    distinct = set(blocks.values())
    if len(distinct) != 1 or not next(iter(distinct)):
        raise SystemExit(
            "the five bows do NOT share one `shot` block, so the type does not "
            "own it and\n  the design's numbers are not transferable to a sixth "
            "bow:\n  " + "\n  ".join(f"{b}: {v[:70]}" for b, v in blocks.items()))
    print(f"  shot  one block across {len(bows)} bows -- the TYPE owns it")

    tip = A.tip if A.stage > 1 else ULT_TIP1
    if len(tip) > 72:
        raise SystemExit(f"ULT TIP is {len(tip)} characters against verify's "
                         f"72:\n  {tip}")

    # THE STRAND MUST SIT ABOVE THE CROSSOVER, AND THE CROSSOVER IS ALGEBRA.
    # An arrow connects at R + shot.r = 58; a strand at R + strandW. A strand's
    # endpoints ARE its arrows, so "hit by the arrow alone" is identically zero
    # above strandW = shot.r = 24 and "hit by the lightning alone" is
    # identically zero below it. Rick took above the line. A builder run that
    # crossed it would silently change which of his three cases can happen.
    if A.stage >= 3 and A.strandw <= 24.0:
        raise SystemExit(
            f"strandW {A.strandw:g} is at or below the crossover (shot.r = 24, "
            f"design section 4).\n  Below it the design inverts: the strand is "
            f"INSIDE its own arrows and\n  'hit by the lightning alone' becomes "
            f"impossible. Rick took above the line.")

    subs = {"%ULT%": A.ult, "%TIP%": A.tip, "%TIP1%": ULT_TIP1,
            "%BLURB%": BLURB, "%DMG%": f"{A.dmg:g}",
            "%CHARGE%": f"{A.charge:g}", "%VOLLEYS%": f"{A.volleys:g}",
            "%N%": f"{A.n:g}", "%SPREAD%": f"{A.spread:g}",
            "%CADMUL%": f"{A.cadmul:g}", "%DMGMUL%": f"{A.dmgmul:g}",
            "%STRANDW%": f"{A.strandw:g}", "%STRANDKNOCK%": f"{A.strandknock:g}",
            "%STRANDART%": A.strandart,
            "%SPEEDMUL%": f"{A.speedmul:g}",
            "%NOVARAD%": f"{A.novarad:g}", "%NOVADMG%": f"{A.novadmg:g}",
            "%NOVAKNOCK%": f"{A.novaknock:g}"}

    if A.stage == 1:
        if f'id:"{RELIC}"' in s0:
            raise SystemExit("this source already has Gloamwire -- built")
        edits = S1
        print(f"  ult {A.ult}  STUBBED at charge 1e9")
        print(f"  tip {len(tip)}/72  {tip!r}   (stage 2 writes the real one)")
        print(f"  blade {A.dmg:g}   (design 6.1's prediction, NOT its answer)")
    elif A.stage == 2:
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("this source has no Gloamwire -- stage 1 first")
        if "tickNet" in s0:
            raise SystemExit("this source already has tickNet -- built")
        edits = S2
        window = A.volleys * 0.34 * A.cadmul
        print(f"  ult {A.ult}  charge {A.charge:g}")
        print(f"  magazine {A.volleys:g} volleys x {A.n:g} arrows, "
              f"fan {A.spread:g} rad, cadence x{A.cadmul:g}")
        print(f"           -> {window:.1f}s to empty, {A.volleys * A.n:g} arrows")
        print(f"  arrows x{A.dmgmul:g} the blade   NO strand yet (stage 3)")
        print(f"  tip {len(tip)}/72  {tip!r}")
    elif A.stage == 3:
        if "tickNet" not in s0:
            raise SystemExit("this source has no tickNet -- stage 2 first")
        if "strandSpent" in s0:
            raise SystemExit("this source already has the strand -- built")
        edits = S3
        print(f"  strand  width {A.strandw:g} -> reach {34 + A.strandw:g} "
              f"against the arrow's own {34 + 24}")
        print(f"  shove   {A.strandknock:g} along the volley's travel, "
              f"NO damage and NO status")
        print("  NOTHING IS DRAWN AND NOTHING SOUNDS -- that is stage 4, and "
              "it is Rick's")
    elif A.stage == 11:
        if "kind === \"nova\"" not in s0:
            raise SystemExit("this source has no nova voice -- stage 10 first")
        if "const tk = t +" in s0:
            raise SystemExit("this source already pops per nova -- built")
        edits = S11
        print("  3 novas a volley x 5.9 volleys/s = 17.5 voices a second")
        print("  flammed 26ms off the arrow's own idx -- three on one frame at")
        print("  zero offset is ONE pop at 3x amplitude, not three pops.")
    elif A.stage == 10:
        if "drawNovas" not in s0:
            raise SystemExit("this source has no nova art -- stage 9 first")
        if '"nova"' in s0 and "kind === \"nova\"" in s0:
            raise SystemExit("this source already has the nova voice -- built")
        edits = S10
        print("  fitted in nova_voice_lab: 48.8 -> 6.4 over three passes")
        print("  peak 0.198 (Deadfall 0.605), attack 37ms, tail 449ms,")
        print("  67.3% under 120Hz at the open, centroid 969Hz")
        print("  ONE POP PER VOLLEY = 5.9/s. Per nova would be 17.5/s.")
    elif A.stage == 9:
        if "novaKnock" not in s0:
            raise SystemExit("this source has no nova -- stage 8 first")
        if "drawNovas" in s0:
            raise SystemExit("this source already draws the nova -- built")
        edits = S9
        print("  a flash, a two-ring shell and 16 hashed streaks, per nova")
        print("  DRAWN, not spawned: `spawnFx` consumes this.rng() and would")
        print("  put the art inside the simulation -- Cindercleave's note.")
        print("  ticked in tickPresentation, so it cannot freeze in a hitStop.")
        print("  ** engine_ab MUST come back identical on all 31. **")
    elif A.stage == 8:
        if "releaseVolleys" not in s0:
            raise SystemExit("this source does not hold the trio -- stage 7 first")
        if "novaKnock" in s0:
            raise SystemExit("this source already has the nova -- built")
        edits = S8
        arrow = A.dmg * A.dmgmul
        print(f"  nova radius {A.novarad:g} (reach {34 + A.novarad:g}), "
              f"knock {A.novaknock:g} against the strand's {A.strandknock:g}")
        print(f"  nova damage {A.novadmg:g} x blade = {A.dmg * A.novadmg:.1f} "
              f"against one arrow's {arrow:.1f}   ({A.novadmg / A.dmgmul:.0%} of an arrow)")
        print(f"  {A.volleys:g} volleys x {A.n:g} = {A.volleys * A.n:g} novas a cast, "
              f"in {A.volleys * 0.34 * A.cadmul:.1f}s")
        print("  CURSE ON -- Rick's. Safe under TOP-3 (a 3.2 memory is refused")
        print("  by a pool holding 13s); NOT safe under the pending LAST-3 rule.")
        print("  ** THE BLADE IS VOID -- this is a new damage channel. **")
    elif A.stage == 7:
        if "drawStrands" not in s0:
            raise SystemExit("this source has no strand art -- stage 5 first")
        if "releaseVolleys" in s0:
            raise SystemExit("this source already holds the trio -- built")
        edits = S7 + S7B
        print("  a resolved Crossweave arrow STICKS where it expired, inert,")
        print("  and its volley clears as a unit when the last one lands.")
        print("  measured before building: peak live 15 -> 23 against a cap of")
        print("  64, and a stuck arrow sits a median 0.37s (max 1.84s).")
        print("  ** THE BLADE IS VOID AGAIN -- strands now live the whole")
        print("     volley, so there are more frames in which one can shove. **")
    elif A.stage == 6:
        if "drawStrands" not in s0:
            raise SystemExit("this source has no strand art -- stage 5 first")
        retune = "speedMul" in s0
        edits = [] if retune else S6
        if retune:
            print("  RETUNE -- speedMul is already in this build, so only the")
            print("  number moves. The insert is not applied twice.")
        S = 380.0
        print(f"  speedMul {A.speedmul:g}   {S:g} -> {S * A.speedmul:g} px/s")
        print("  a RESCALE of the type's own vector, never a fresh one")
        print("  ** THIS VOIDS THE BLADE. dmg 9.0 was measured at speed 380;")
        print("     re-run gloamwire_sweep.py --only 0 then --only 1. **")
    elif A.stage == 5:
        if "strandSpent" not in s0:
            raise SystemExit("this source has no strand -- stage 3 first")
        if "drawStrands" in s0:
            raise SystemExit("this source already draws the strand -- built")
        edits = S5
        print(f"  strandArt {A.strandart!r}   PRESENTATION ONLY")
        print("  the pairing rule is tickNet's exactly: adjacent in the fan,")
        print("  both alive, and a dead arrow breaks its links.")
        print("  NO this.rng(), NO gradients per segment, NO shadowBlur.")
    elif A.stage == 4:
        if "strandSpent" not in s0:
            raise SystemExit("this source has no strand -- stage 3 first")
        if TUNED_GW is None:
            raise SystemExit("\n".join((
                "TUNED_GW is None and this stage has no default.",
                "  Measure it FIRST, and measure it the way CLAUDE.md says --",
                "  `gloamwire_sweep.py --only 0` for the CURVE (does it bend?),"
                " then",
                "  `--only 1` for a WIDE DIRECT MEASUREMENT at n >= 1000 a"
                " point, on BOTH",
                "  SIDES, repeated on a SECOND SEED BLOCK. Never a bisection:"
                " one converges",
                "  on the noise in its own tail, and the last time that was"
                " trusted it cost",
                "  a whole damage point.")))
        edits = []
    else:
        raise SystemExit(
            f"stage {A.stage} is not written yet. The stage before it must "
            f"pass its gate first --\n  and the brief says to stop at a gate "
            f"that fails rather than carry a broken\n  stage forward.")

    for label, old, new in edits:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    if A.stage == 7:
        # EVERY SITE THAT EVICTS AT THE CAP, and there are four. A fix applied
        # to `spawnShot` alone is a fix that works until the opponent's forks
        # push the roster over the line.
        s = alln(s,
                 "if (this.shots.length >= CONFIG.shot.maxLive) this.shots.shift();",
                 "this.makeRoom();",
                 "cap-eviction", 4)

    if A.stage == 6 and "speedMul" in s0:
        # Walk forward from this relic's own id, never a global replace.
        # THE ENTRY, BY BRACE MATCHING, and not a fixed window. The first cut
        # searched 3000 characters forward from the id and missed: this relic's
        # own `ult` comment is longer than that, which is a good reason for the
        # comment and a bad reason for a magic number.
        e = entry(s, RELIC)
        m = re.search(r"speedMul:\s*([0-9.]+)", e)
        if not m:
            raise SystemExit("cannot retune: speedMul is not in Gloamwire's entry")
        old = m.group(0)
        j = s.index(e) + m.start()
        s = s[:j] + f"speedMul:{A.speedmul:g}" + s[j + len(old):]
        print(f"  speedMul {m.group(1)} -> {A.speedmul:g}"
              f"   ({380 * float(m.group(1)):g} -> {380 * A.speedmul:g} px/s)")
        print("  ** THE BLADE IS VOID AGAIN. Re-run gloamwire_sweep --only 0,1 **")

    if A.stage == 4:
        # THE SIX BOWS SHARE A STAT LINE, so the blade is found by walking
        # forward from this relic's own id and never by a global replace --
        # `dmg:9.2` would be a plausible value on any of them.
        e = entry(s, RELIC)
        m = re.search(r"dmg:\s*([0-9.]+),", e)
        if not m:
            raise SystemExit("cannot retune: no dmg in Gloamwire's own entry")
        j = s.index(e) + m.start()
        print(f"  blade dmg {m.group(1)} -> {A.dmg:g}")
        s = s[:j] + f"dmg:{A.dmg:g}," + s[j + len(m.group(0)):]

    ult_matches(s, A, A.stage)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    # AND THE NEW RELIC'S SHOT BLOCK MUST BE THE TYPE'S, BYTE FOR BYTE. The
    # comment above claims it; this is the claim asserted against what was
    # actually written.
    if A.stage == 1 and shot_block(s, RELIC) != next(iter(distinct)):
        raise SystemExit(
            "the relic just written does not carry the type's own `shot` "
            "block:\n  wrote " + shot_block(s, RELIC)[:80]
            + "\n  type  " + next(iter(distinct))[:80])

    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")

    if A.stage == 1:
        print("\n  GATE 1:")
        print(f"    python engine_ab.py --a {src} --b {out} --n 8")
        print(f"    python verify.py --game {out} --n 40")
        print("      Gloamwire will be near 2% and that is NOT a failure --")
        print("      the brief says so. Print it and carry on.")
        print(f"    python net_lab.py --game {out} --stage 1")
        print("      THE PORTED CONTROL: the umbral-bow row must come back")
        print("      within 6 of pool 54.2 and within 2s of a 13.1s third")
        print("      stack. If it does not, STOP -- what is refuted is the")
        print("      cell's identity, not a tuning number.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
