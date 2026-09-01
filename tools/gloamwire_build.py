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

    BUT CHARACTERS ARE THE WRONG UNIT AND THE PANEL IS THE REAL GATE. The
    scrunch panel is 536px on one line at 25px and a 48-character tip can be
    583px. `tip_audit.py` measures pixels. A tip that passes `verify` and
    overflows the card is exactly what happened to the curse line in v53.

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
TUNED_GW = 9.0       # MEASURED, and it is a WIDE DIRECT MEASUREMENT rather than
                     # a bisection: `gloamwire_sweep.py --only 1`, three blades
                     # x both sides x two seed blocks x 1020 fights a cell,
                     # 12,240 in total, on the pin at 31 relics.
                     #
                     #     dmg    A-side  B-side  blockA  blockB   POOLED
                     #    8.60     45.3%   44.7%   44.3%   45.7%    45.0%
                     #    9.20     53.3%   51.2%   51.4%   53.1%    52.3%
                     #    9.80     57.6%   58.6%   58.1%   58.1%    58.1%
                     #
                     # Monotone, side asymmetry +0.6pp, worst block
                     # disagreement 1.8pp, 50% crossing at 9.01.
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
    "dmgmul":       1.4,   # design 6, the +40% arm. Rick took all four
                           # strength clauses and the blade pays.
    "strandw":     90.0,   # design 4.2. Above the crossover at shot.r = 24, so
                           # "arrow only" is near zero BY CONSTRUCTION. Rick
                           # took above the line.
    "strandknock": 260.0,  # design 6.2. A COST, monotone -9 points across the
                           # sweep, bought for the look and worth ~a point of
                           # blade.
}

ULT_NAME = "Crossweave"
# 48 characters against verify's 72. See the header: the 40 in both documents
# is the status-tip figure. `tip_audit` is still the gate that matters.
ULT_TIP = "24 volleys of 3 strung arrows; the strand shoves"
ULT_TIP1 = "—"          # stage 1, stubbed. verify only asks that it is non-empty.

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
    ap.add_argument("--stage", type=int, required=True, choices=(1, 2, 3, 4))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
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
                "which is art"
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
            "%STRANDW%": f"{A.strandw:g}", "%STRANDKNOCK%": f"{A.strandknock:g}"}

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

    if A.stage == 4:
        # THE SIX BOWS SHARE A STAT LINE, so the blade is found by walking
        # forward from this relic's own id and never by a global replace --
        # `dmg:9.2` would be a plausible value on any of them.
        i = s.index(f'id:"{RELIC}"')
        j = s.find(f"dmg:{BLADE_IN:g},", i)
        if j < 0 or j - i > 400:
            raise SystemExit(f"cannot retune: dmg:{BLADE_IN:g} is not in "
                             f"Gloamwire's own entry. Already tuned?")
        s = s[:j] + f"dmg:{A.dmg:g}," + s[j + len(f"dmg:{BLADE_IN:g},"):]
        print(f"  blade dmg {BLADE_IN:g} -> {A.dmg:g}"
              f"   (the placeholder read 52.3% at n=4080; 9.0 is the crossing)")

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
