#!/usr/bin/env python3
"""BLOODMIRROR, AND ITS ULTIMATE BLOODLETTING. STAGES 1, 2 AND 3b.

    python bloodmirror_build.py --stage 1 --src ../02-chain/sc-tipfix.html \
                                --out ../02-chain/sc-bloodmirror.html
    python bloodmirror_build.py --stage 2 --src ../02-chain/sc-bloodmirror.html \
                                --out ../02-chain/sc-bloodletting.html
    python bloodmirror_build.py --stage 3b --dmg <the swept blade>

**THE DESIGN IS NOT THIS FILE'S AND IT NEVER WAS.**
`06-docs/v59/spectre-design-v59.md` is the design,
`06-docs/v59/bloodmirror-build-brief-v59.md` is the brief, and
`tools/spectre_lab.py` is the instrument that measured every number in both.
Rick chose the cell, both names, the composition, the knockback and the ceiling
rule. This builder implements and refuses; it does not choose.

CLAUDE.md section 3 rule 0: Claude Code does not design ultimates. If you are
reading this file for the reasoning behind a mechanic, it is in the design doc.

## FOUR DEPARTURES FROM THE BRIEF, ALL DECLARED HERE

**IT IS THE THIRTY-SECOND RELIC AND THE BRIEF SAYS THE THIRTIETH.** The brief
was written on 2026-09-01 against a 29-relic tip and then sat in a chat
transcript for a day while Ravelbone (30) and Gloamwire (31) were built. Count
what is BUILT AND IN A LINK -- CLAUDE.md section 0 is where that number is
settled, and CLAIMS.md records the drift as one of the two costs of the
collisions.

**THE BASE IS `sc-tipfix.html` AND THE BRIEF SAYS "THE CINDERCLEAVE TIP".**
Same reason. Stage T of the brief is built and green (`tipfix_build.py`), so
this chains from it, and every `engine_ab` below runs over 31 others rather
than 29.

**EVERY ABSOLUTE NUMBER IN THE DESIGN DOC IS ON A DIFFERENT ROSTER.** It was
measured against `sc-nightfell.html` with 27 relics and Thornwake standing in
for a relic that did not exist. The brief says so in as many words and says the
DIFFERENCES travel. So section 2's "near 23% at blade 21 with no ultimate" is a
prediction to print and NOT a number to tune to at stage 1.

**THE ART ALREADY EXISTS AND IS OPEN ITEM 34's THIRD INSTANCE.**
`SHAPES.scythe` has routed `bloodsworn` to `_scBarbed` since before there was a
relic in this cell, so stage 1 gets a drawn weapon for free. It is also built
the way Rick rejected on the umbral hammer: five barbs and a tip hook STROKED
ON TOP of `_scBase` rather than added to the type's outline. Brief open decision
6 says look at it early, and "early" means before stage 1 ships, not after 3b.

## THE ONE THING MOST LIKELY TO GO WRONG, AND IT IS NOT IN STAGE 1

`AC.STATUS.hemorrhage.maxStacks` is ONE NUMBER shared by every fighter in the
match and by the four other bloodsworn relics in the field. The ultimate raises
it 4 -> 8 while the spectre stands. The lab moved it globally and restored it
per match; a build that did that would hand a Marrowdraw in the same fight a
window it never cast, silently. Stage 2 scopes it per-fighter. See section 3.2
of both documents, and `bloodletting_relic_probe [5]`.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "bloodmirror"

# ------------------------------------------------------------- the numbers --

# THE BLADE. Brief section 5: start the bisection at 21 and expect the answer in
# 20-22. `final_blade.py` measured 46.6% with the ultimate and 17.8% without at
# blade 20, on the design's own roster -- so the ultimate is worth roughly 28
# points there, just above the roster mean of +20.1, and that is the composition
# Rick chose from three (MEDIUM: 3 a tick, life 4.5).
#
# AND THE SURFACE IS NOT SIMPLE. `dmg` moves the blade AND the curse-free pool
# AND -- through the raised ceiling -- what a blade blow is worth DURING the
# window, because the blade feeds the ceiling too (Rick's ruling). v51 section
# 4.5's superlinear warning applies here where it did not to Shroudmaul.
BLADE_IN = 21.0
TUNED_BM = 9.5       # MEASURED, and it is a WIDE DIRECT MEASUREMENT rather
                     # than a bisection: 1054 fights a point a side a block,
                     # both sides, two seed blocks, 12,648 fights.
                     #
                     #     dmg    A-side  B-side  blockA  blockB  POOLED
                     #     8.00    44.1%   46.6%   47.1%   43.7%   45.4%
                     #     9.00    47.6%   48.8%   47.9%   48.4%   48.2%
                     #    10.00    52.8%   51.5%   52.0%   52.4%   52.2%
                     #
                     # Monotone, crossing at 9.46.
                     #
                     # AND IT WAS MEASURED TWICE, ON TWO BUILDS, BECAUSE THE
                     # SECOND ONE MOVED THE SIM. Fixing the same-frame hit-stop
                     # ordering (see `tickSpectre`) let copies two and three
                     # pay on a frame the first had already frozen, so the
                     # whole thing was re-run at 9/10/11:
                     #
                     #     dmg    A-side  B-side  blockA  blockB  POOLED
                     #     9.00    49.0%   48.0%   49.2%   47.7%   48.5%
                     #    10.00    51.5%   50.3%   52.4%   49.4%   50.9%
                     #    11.00    56.5%   53.2%   53.5%   56.1%   54.8%
                     #
                     # Crossing 9.63. THE SHIPPED VALUE STAYS 9.5, and that is
                     # the rule rather than laziness: 9.46 and 9.63 are 0.17
                     # apart against a block disagreement of 3.0-3.4pp, and
                     # CLAUDE.md is explicit that "a change smaller than the
                     # error bar is not a tune, it is churn that looks like
                     # one." THE HONEST PRECISION IS THE 9-10 INTERVAL, not
                     # either decimal.
                     #
                     # AND IT IS 11.5 POINTS BELOW WHAT THE BRIEF EXPECTED.
                     # Section 5 said "expect the answer in 20-22"; the
                     # one-copy build crossed near 16 and three copies put it
                     # here. That is not a tuning drift, it is Rick changing
                     # the mechanic after seeing it.
                     #
                     # WHAT THIS MAKES THE RELIC: at dmg 3-5 it still wins
                     # 31.5%, so most of what Bloodmirror is, is Bloodletting.
                     # Design section 5 says that composition is Rick's rather
                     # than the bisection's, and this is where the measurement
                     # left it.
                     #
                     # The old text, kept because the rule is the point:
                     # stage 3b refuses to run while this is None, and the
                     # reason is printed. What settles a blade on this roster is
                     # a WIDE DIRECT MEASUREMENT at n >= 1000 a point, on both
                     # sides, repeated on a second block -- never a bisection.
                     # v48, v56 and v59 all learned that separately.

ULT_NAME = "Bloodletting"
ULT_TIP  = "Stands a spectral scythe that mills - bleed stacks to 8"
ULT_TIP1 = "-"       # stage 1, stubbed. verify only asks that it is non-empty.

BLURB = ("A copy of the blade, cut loose and left standing. It does not chase "
         "anything - it makes the room smaller.")


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
    be able to say the words `STATUS.hemorrhage.maxStacks`.
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


def body_block(s: str, rid: str, key: str) -> str:
    """One named sub-object of a relic's entry, comments out, space collapsed."""
    e = strip_comments(entry(s, rid))
    m = re.search(key + r"\s*:\s*\{", e)
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


def phys(s: str, rid: str) -> dict:
    """The physical stats a TYPE owns, off one relic's entry."""
    e = strip_comments(entry(s, rid))
    out = {}
    for f in ("reach", "width", "artW", "spin", "mass", "mode", "arc"):
        m = re.search(rf"\b{f}\s*:\s*(\"[a-z]+\"|[\d.]+)", e)
        if m:
            out[f] = m.group(1)
    return out


def ult_matches(s: str, A, stage) -> None:
    """The shipped `ult` block carries every number this run printed.

    v56's own failure, verbatim: a stage-2 insert wrote the whole `ult` block
    and stage 3 rewrote only the line carrying `charge`, so the run LOGGED the
    new rhythm and SHIPPED the old one, and every gate downstream measured a
    relic the log was not describing.
    """
    blk = body_block(s, RELIC, "ult")
    if not blk:
        raise SystemExit("the shipped relic has no `ult` block")
    want = {"name": f'"{A.ult}"', "kind": '"effigy"'}
    if str(stage) == "1":
        want["charge"] = "1e9"
    else:
        want["charge"] = f"{A.charge:g}"
        for k in ("flight", "speed", "life", "disc", "tick", "dmg",
                  "bleed", "cap", "knock", "spinMul", "artScale",
                  "n", "spread", "drift"):
            want[k] = f"{getattr(A, {'dmg': 'tickdmg', 'spinMul': 'spinmul',
                                    'artScale': 'artscale'}.get(k, k)):g}"
    missing = [f"{k}:{v}" for k, v in want.items()
               if not re.search(rf"\b{re.escape(k)}\s*:\s*{re.escape(v)}\s*[,}}]",
                                blk)]
    if missing:
        raise SystemExit(
            "REFUSING TO WRITE -- the shipped `ult` block does not carry what "
            "this run printed:\n  missing " + ", ".join(missing)
            + "\n  (v56 shipped an ultimate whose numbers the log did not "
              "describe. Never again.)")


# ------------------------------------------------------------------ stage 1 --

S1 = [

("relic", '''    blurb:"Three shafts and the dark strung between them. What the arrows miss, the lightning still moves." },

];''',
 '''    blurb:"Three shafts and the dark strung between them. What the arrows miss, the lightning still moves." },

  /* BLOODMIRROR -- THE BLOODSWORN SCYTHE, and the thirty-second relic. It is
     also the OLDEST DESIGN IN THE PROJECT: `06-docs/v59/` was written on
     2026-09-01 and then spent a day in a chat transcript while two later cells
     were built ahead of it, which is the standing example in `CLAIMS.md` of why
     a deliverable that lives in a chat message does not exist.

     EVERY PHYSICAL STAT IS THE SCYTHE'S, copied off Lastlight, Thornwake,
     Foregone, Vesper and Cindercleave -- the type owns `reach:104, width:11,
     artW:46, spin:3.2, mass:2.4, blades:[0], mode:"spin"` and there is no sixth
     set to invent. This builder asserts that against the shipped file before it
     writes rather than trusting this comment.

     `onHit:{ hemorrhage:2 }` is the school's own weight, as on all four of the
     other bloodsworn relics -- and it is load-bearing here in a way it is not
     anywhere else. Hemorrhage is `{ maxStacks:4, dur:3.2, dps:1.5 }`, a hard
     ceiling of 6 damage a second, and the ULTIMATE'S WHOLE MECHANIC is that
     the ceiling moves while the spectre stands. The blade feeds the raised
     ceiling too -- Rick's ruling, and it is what makes the window read as the
     fighter opening up rather than as an object landing.

     WHY THIS CELL. `budget-v59.md` section 4: bleed is the strongest foe
     channel available on this weapon, +10.0pp against curse's +3.9 and
     sunder's +4.7, beaten only by a shield that is already Vesper's.

     THE ART IS OLDER THAN THE RELIC AND RICK RULED ON IT BEFORE THIS SHIPPED.
     `SHAPES.scythe` has routed `bloodsworn` to `_scBarbed` since before this
     cell had anything in it: five barbs riding the crescent, getting longer
     toward the tip so the fastest part of the sweep is the part that catches.
     Brief open decision 6 says look at it early -- v57 puts this cell at 59.0%
     from its nearest sibling, the CLOSEST PAIR on the row, and v58 is the
     standing warning that the number says nothing about whether the shape is
     any good. Photographed beside sanctified at zoom, it was not the closeness
     that was wrong: it was a SIXTH shape, a grey triangle hung off the
     crescent's outer end point, reading as a detached object rather than as
     part of the weapon. Rick: "the grey triangle at the tip of bloodsworn
     scythe. lets get rid of it. everything else is great." It is gone, the
     barbs are untouched, and the inversion `_scOuter` documents is now a
     CHOSEN STATE on this row rather than an open defect -- he was shown the
     shipped-against-flipped sheet for all seven schools and kept the shipped
     one.

     `dmg` 21 IS A STARTING POINT AND NOT AN ANSWER. Brief section 5 measured
     the curve on the design's own roster -- flat between 18 and 20, steep
     either side -- and says to expect 20-22. `TUNED_BM` is None until a wide
     direct measurement says otherwise, and stage 3b refuses to run without
     it. */
  { id:"bloodmirror", name:"Bloodmirror", aff:"bloodsworn", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:%DMG%, spin:3.2, mode:"spin", mass:2.4,
    onHit:{ hemorrhage:2 },
    /* BLOODLETTING. STUBBED AT `charge:1e9` IN STAGE 1 -- the same "OFF" the
       charge sweep in v55b used and the same one Cindercleave's stage 1,
       Shroudmaul's stage 2 and Gloamwire's stage 1 used: the clock can never
       reach it, `fireUlt` never runs, and the relic is measured as a blade and
       a channel and nothing else.

       Stubbing rather than omitting is deliberate. The `ult` object is read by
       `verify`, by `tip_audit`, by the scrunch panel and by half of `tools/`,
       and a relic with no `ult` at all is a shape none of them have ever been
       handed.

       `kind:"effigy"` IS ITS OWN AND IS NOT `"harrow"`. Lastlight is the
       SANCTIFIED scythe -- the same weapon -- and `smite` is byte-identical to
       `hemorrhage` apart from its name, so without a real separation these two
       relics are one relic in two palettes. Design section 3.4 is the
       separation and it is structural: Harrowing sprays TWELVE small scythes
       that stick to the BODY, burden it and burst once; this stands ONE large
       one in the HALL, milling, and takes the quarry to a stack count nothing
       else in the game can reach. */
    ult:{ name:"%ULT%", charge:1e9, kind:"effigy", tip:"%TIP1%" },
    blurb:"%BLURB%" },

];'''),

# THE TIP HOOK COMES OFF `_scBarbed`. RICK'S, 2026-09-01, shown the bloodsworn
# scythe beside sanctified at zoom before stage 1 shipped: "the grey triangle at
# the tip of bloodsworn scythe. lets get rid of it. everything else is great."
#
# It read as a detached grey triangle floating past the end of the blade -- the
# `_whEaten` complaint ("the hammer with blocks attached to it idea just isnt
# working for me") in a new place, and worse here because the hook is drawn at
# `_scOuter(L, W, 1.0)`, the crescent's outer END POINT, so it hangs off the far
# tip with the blade's own body falling away underneath it.
#
# THE FIVE BARBS STAY EXACTLY AS THEY ARE, and so does the side they are on.
# `_scOuter`'s normal is INWARD at 1921 of 1921 samples and all 37 call sites in
# this file assume otherwise, so `_scBarbed`'s barbs sweep across the concave
# face rather than dragging off the back the way its own comment says. The
# one-character fix moves six of the seven scythe silhouettes (bloodsworn 3.16%
# of the frame, umbral 6.96%, vigil 7.87%, runic 0.00% as the control that does
# not call it). Rick was shown that sheet -- `05-reference/v59/scythe-normal-
# flip.png`, shipped against flipped, all seven schools -- and took "everything
# else is great". SO THE INVERSION IS NOW A CHOSEN STATE ON THIS ROW, the way
# `_whBarbed` became one on the warhammer row. Do not re-raise it and do not
# "fix" it.
#
# PRESENTATION ONLY, AND THAT IS PROVEN RATHER THAN ASSERTED: `SHAPES` is
# render-only, so `engine_ab` over the roster is the cheapest proof this project
# has and v58 is the precedent (`_whGnawed`, 3024/3024 identical on all 28).
("tip-hook", '''    const tip = SHAPES._scOuter(L, W, 1.0);                     // and a tip hook
    c.beginPath();
    c.moveTo(tip.x, tip.y);
    c.lineTo(tip.x + W*0.10, tip.y - W*0.52);
    c.lineTo(tip.x + W*0.34, tip.y - W*0.10);
    c.closePath(); c.fill(); c.stroke();
  },''',
 '''    /* AND NO TIP HOOK. It was a sixth shape -- a triangle from the crescent's
       outer END POINT out past the blade -- and at zoom it read as a detached
       grey triangle floating off the end rather than as part of the weapon,
       which is `_whEaten`'s fault on a second row. Rick, shown this cell beside
       sanctified before the relic shipped: "the grey triangle at the tip of
       bloodsworn scythe. lets get rid of it. everything else is great."

       The five barbs are the grammar and they are untouched. */
  },'''),

]


# ------------------------------------------------------------------ stage 2 --

# EVERY ONE OF THESE IS THE DESIGN'S, AND THE ARRANGEMENT IS FREE. 23 arms
# regressed on the damage the spectre delivers give
#
#     lift = +5.6 + 0.245 x spectreDamage      r2 = 0.80
#     residual sd 2.9pp against a per-arm SE of 3.1pp
#
# -- the residuals are SMALLER than the measurement error, which is the same
# result GRASP had on held seconds. So tick rate, damage a tick, life and flight
# are four ways of writing one quantity: TUNE ON TICKS LANDED, NOT ON WIN RATE,
# and make every remaining choice for the picture.
#
# TWO THINGS ARE NOT ON THAT LINE. The DISC is not a knob -- "a copy of itself"
# fixes it at ball 34 + reach 104 = 138, and it is both the strongest lever in
# the lab (104 -> +10.0, 206 -> +28.8) and the first thing that breaks the
# fiction. And the CEILING is section 3 and is not on the line at all.
ULT = {
    "charge":  15.0,    # the roster mode. AND IT IS A REAL KNOB HERE, unlike
                        # Grasp: this ultimate DOES scale with cast count --
                        # more spectres is strictly more damage -- and v55b
                        # established nobody's charge was ever derived. Open
                        # decision 3 in the brief; one lab, and it belongs
                        # BEFORE the bisection.
    "n":       3.0,     # RICK'S, 2026-09-01: "lets have it shoot out 3 copies
                        # of itself." The design and the brief are written for
                        # ONE, and its arms table prices "two spectres, half
                        # life" at +16.2 against the centre's +11.2 -- inside
                        # the noise -- and nothing anywhere prices THREE AT FULL
                        # LIFE. Each copy is its own hazard with its own
                        # cooldown, so a quarry in an overlap is bitten by each:
                        # this is the largest single change to the priced relic
                        # in this build and the blade is what pays for it.
    "spread":  0.34,    # radians either side of the bearing to the quarry, so
                        # the middle copy is the one the design describes. At
                        # `n` 1 the term is identically zero and this is the
                        # one-copy ultimate that was priced, which is what makes
                        # the two comparable.
    "drift":   26.0,    # RICK'S: "a small amount of movement so they slowly
                        # continue to float in the direction they were fired."
                        # 6% of the throw speed -- about a fifth of a disc over
                        # a whole window, which is enough that the hall is never
                        # quite the same shape twice and far too little to read
                        # as a second flight. IT CHANGES RICK'S OWN SECTION 1,
                        # which said "sticks in place", and the probe's check 2
                        # moved with it.
    "flight":  0.55,    # thrown at where the quarry is NOW. NO HOMING.
    "speed":   420.0,   # 0.55 x 420 = 231 units. A LONG THROW COSTS IT: flight
                        # 1.1s halves the time the foe spends inside (13.1%
                        # against 26.1%) because the spectre spends its life in
                        # transit rather than standing.
    "life":    4.5,     # it stands, then it is gone
    "disc":    138.0,   # NOT A KNOB. See above.
    "tick":    0.22,    # FREE at a fixed total. The rate is the picture.
    "tickdmg": 3.0,     # through `hurt`, scaled by the quarry's own dmgTakenMul.
                        # NAMED `tickdmg` HERE AND `dmg` IN THE SHIPPED BLOCK
                        # because this file already has a `--dmg` and it is the
                        # BLADE. Two numbers called dmg on one relic is how a
                        # sweep tunes the wrong one.
    "bleed":   2.0,     # the school's own rate. Worth +4.0pp over 1 a tick ONCE
                        # THE CAP MOVES (z +2.53) and NOTHING AT ALL before it.
    "cap":     8.0,     # 4 -> 8 WHILE IT STANDS, and the blade feeds it too.
                        # Rick's, from four ways of breaking the ceiling.
    "knock":   120.0,   # Rick's. +7.9pp, z +2.98, and FLAT from 60 to 240 -- so
                        # any knockback buys about seven points and no
                        # particular amount buys more.
    "hitfly":  1.0,     # does it bite while flying? +12.7 against +11.2, inside
                        # the noise, so it is a picture choice and not a number.
    "spinmul": 4.0,     # RICK'S, 2026-09-01, off the first sheet: "lets also
                        # increase the rotational speed by a lot." The copy used
                        # to turn at the weapon's own 3.2 rad/s, which on an
                        # object that is not attached to anybody read as drifting
                        # rather than as milling. 4x is 12.8 rad/s, a hair over
                        # two revolutions a second.
                        #
                        # PRESENTATION ONLY, AND THAT IS PROVEN RATHER THAN
                        # ASSERTED: `S.spin` is read by `drawSpectre` and by the
                        # pool's own pulse and by nothing else in the engine, so
                        # `engine_ab` over the roster is the check.
    "artscale": 1.88,   # how big a copy is drawn. 1.0 is the weapon at its own
                        # size, where its sweep about its CENTRE OF MASS is
                        # 0.6664 x L = 73.3 and covers 53% of the 138 disc it
                        # mills; 1.88 puts the tip back on the rim. RICK'S,
                        # shown both frames -- and it has been 2.26 and 2.34 on
                        # the way, because the number is a function of WHICH
                        # centre the copy turns about and that took three goes
                        # to get right (see `drawSpectre`).
                        #
                        # THE DEFAULT IS HIS ANSWER AND NOT 1.0, and that is
                        # CLAUDE.md 4.9: a chosen number that lives only in the
                        # command line somebody typed is a number the next
                        # rebuild loses. `ult_matches` caught exactly that on
                        # the first run of stage 3b -- the shipped block said
                        # 2.26 and this file still said 1.
}

# ---- 11. AND IT GETS A PARTICLE FIELD ---------------------------------------
# THE 26th SPEC WENT IN WITH A RULE ATTACHED AND TWO RELICS HAVE SINCE MISSED
# IT. `ULTFX.sync` RETURNS SILENTLY on a missing spec -- it is not an error,
# which is exactly why it ships -- and `SPECS` today carries 29 entries in both
# `src/render/fx.js` and the inlined copy, with NO `ravelbone` and NO
# `gloamwire`. So the last two relics built have no particle field and nothing
# said so. This one has one, in BOTH copies, and the builder refuses to write
# unless they match byte for byte afterwards.
FX_SPEC = """,
    /* THE COPY LEAVING THE BLADE, AND `atSelf` IS WHY IT LEAVES THE RIGHT ONE.
       A `burst` is drawn at the FOE -- right for the four novas that mode was
       written for, which are cast AT somebody, and wrong for a thing THROWN
       FROM the caster. Nothing has landed on the quarry when this plays; the
       copy has not even arrived.

       Heavier and wetter than the sparks above it: real gravity, a slow fall
       and a long tail, because what is coming off the weapon is blood rather
       than light. It is gone well before the spectre sticks, which is
       deliberate -- the STICK has its own voice and its own beat, and a field
       still running under it would blunt the one frame the design says has to
       read. */
    bloodmirror: { mode: 'burst', n: 1200, sp: [150, 600], grav: 300,
                   drag: 2.3, life: [0.26, 0.78], heavy: 0.08,
                   size: [0.8, 2.4], spawn: 0.06, up: 20, atSelf: 1 }"""

FX_ANCHOR = """                    size: [0.5, 2.0], spawn: 0.12, up: 40, atSelf: 1 }
  };"""


S2 = [

# ---- 1. THE FIGHTER CARRIES THE COPIES AND ITS OWN CEILING ------------------
("fighter-fields", '''    this.deadfallFade = 0;''',
 '''    this.deadfallFade = 0;
    /* THE COPIES BLOODLETTING HAS IN THE HALL. An ARRAY, and empty on every
       other relic and on this one outside its own window -- which is the whole
       zero-burden argument: `tickSpectre` returns after a two-iteration loop
       that does nothing and `drawSpectre` returns on its first line.

       THREE OF THEM, AND THAT IS RICK'S, 2026-09-01, off the first clip: "lets
       have it shoot out 3 copies of itself." The design and the brief are both
       written for ONE -- design section 1's own arms table has "two spectres,
       half life" at +16.2 against the centre's +11.2, inside the noise, and
       nothing in `06-docs/v59/` prices three at FULL life. So every absolute
       number in those two documents is on the other branch and only the
       relative ones survive. What travels is the one-scalar law -- lift = +5.6
       + 0.245 x spectre damage -- and three copies move the input to it.

       EACH IS ITS OWN OBJECT WITH ITS OWN COOLDOWN, so a quarry standing where
       two discs overlap is bitten by both. That is the plain reading of "three
       copies of itself" and it is the only one that does not need a rule
       written for it, but it is NOT free and nobody has priced it: Breach's
       `spent` is one payment per firing precisely because sweeping several
       bodies with one hazard is either a shield or a multiplier. Here the
       multiplier is deliberate and it is what the blade pays for.

       ONE ARRAY, OWNED BY A FIGHTER. Not `m.shots`: `spawnShot` SHIFTS THE
       OLDEST LIVE ENTRY OUT at `maxLive` 64, so a copy could vanish with no
       error and no invariant broken -- and `tickShots` lets `bladeSegments`
       PARRY a shot with melee's defence winning ties. A spectral scythe the
       quarry can parry is a different mechanic and nobody has decided it is
       this one (design 6.2). And not `m.ultFx`, which is ONE SLOT the
       opponent's cast overwrites (v54 2a, open item 25).

       A DEAD COPY IS KEPT UNTIL ITS `fade` RUNS OUT, because the window
       closing is not the same event as the picture of it ending, and three
       copies drifting apart cannot share one per-fighter fade the way
       `deadfallFade` does -- each dissolves where it was standing. */
    this.ultSpectres = [];
    /* {x, y, t, life} EACH -- THE RINGS THE COPIES THROW WHEN THEY STOP, and
       they are Rick's, off the first sheet. Design 7c says the STICK is the
       frame that tells a viewer the thing is staying and that "if it does not
       read, the ultimate looks like a missed shot"; photographed off a real
       match it did not read at all -- a thin red line arriving in a busy frame
       with nothing marking the arrival. A ring says THIS IS NOW A PLACE, where
       a burst would only say something hit, and nothing was hit: the copies
       land on empty floor.

       Presentation only, and TICKED IN `tickPresentation` rather than in
       `tickSpectre`. v54's lesson: a hit stop runs `decayImpactOnly` and a
       clock on the normal path freezes for exactly the frames the viewer is
       staring hardest at -- which is what Deadfall's blast did, 96.2% of the
       time. The landing does not set `hitStop` itself, but a blade blow on the
       same frame does, and that is the frame these rings are most likely to
       share with something. `life` is in HALF-SECONDS like every other
       presentation clock here, because that method is called once directly and
       once through `decayImpactOnly`. */
    this.spectreRings = [];
    /* THE BLEED CEILING THIS FIGHTER IS UNDER, AND IT IS THE WHOLE OF
       BLOODLETTING.

       Hemorrhage is `{ maxStacks:4, dur:3.2, dps:1.5 }` -- a hard ceiling of 6
       damage a second -- and a copy ticking every 0.22s reaches four stacks in
       under a second, after which every application only refreshes a clock.
       Measured: adding bleed to the spectre at cap 4 is worth -2.5pp at
       z -0.93, and at cap 8 it is +6.9pp at z +2.67. THE SAME COMPARISON,
       TWICE, WITH ONLY THE CEILING CHANGED. Rick's sentence -- "hits rapidly
       applying bleed" -- describes a mechanic the game currently forbids, and
       "rapidly" is exactly the word the cap deletes.

       `AC.STATUS.hemorrhage.maxStacks` IS ONE NUMBER shared by every fighter in
       the match and by all five bloodsworn relics. The lab moved it globally
       and restored it per match; a BUILD that did that has three silent
       failures, all named in the design's 6.3 before anything was built: a
       Marrowdraw in the same fight inherits a window it never cast, the cap is
       left at 8 for the NEXT match, and it is restored on `m.over` but not on a
       window merely expiring.

       So the ceiling is a property of THE FIGHTER BEING BLED, exactly the way
       v53 scoped the curse pool -- "a convention that two call sites must both
       fire is not agreement, it is a promise." `apply` reads this and nothing
       else does. And `tickSpectre` RECOMPUTES it from scratch every frame
       rather than raising and restoring it, so there is no paired write to
       forget and the third failure mode cannot exist. */
    this.bleedCap = STATUS.hemorrhage.maxStacks;'''),

# ---- 2. AND `apply` READS IT ------------------------------------------------
("apply-cap", '''    const cur = this.status[key] || { stacks:0, t:0 };
    cur.stacks = Math.min(def.maxStacks, cur.stacks + n);
    cur.t = def.dur;''',
 '''    const cur = this.status[key] || { stacks:0, t:0 };
    /* HEMORRHAGE READS THE FIGHTER'S OWN CEILING; EVERY OTHER STATUS READS THE
       GLOBAL. `bleedCap` is 4 on every fighter in every match with no standing
       Bloodletting spectre in it, so this is the identity it replaced
       everywhere else -- and `engine_ab` proves that rather than this comment
       asserting it.

       A FIGHTER ALREADY ABOVE THE CEILING IS NOT TRIMMED BY A NEW APPLICATION.
       When the window closes the cap drops back to 4 with the stacks still at
       8, and `Math.min(cap, cur + n)` would CUT them to 4 on the very next
       blow -- which is the instant trim the design's 6.4 rejected as "the
       version that looks like a bug". They run out on hemorrhage's own 3.2s
       clock instead. WHAT THAT COSTS IS WRITTEN ON `tickSpectre`, because this
       engine expires a status as a whole rather than a stack at a time. */
    const cap = key === "hemorrhage" ? this.bleedCap : def.maxStacks;
    if (cur.stacks < cap) cur.stacks = Math.min(cap, cur.stacks + n);
    cur.t = def.dur;'''),

# ---- 3. THE CAST THROWS THEM ------------------------------------------------
("fire-effigy", '''    if (u.kind === "wire"){''',
 '''    if (u.kind === "effigy"){
      /* NOTHING RESOLVES HERE and there is no radius test. The cast throws
         `n` copies of the weapon at where the quarry IS ON THIS FRAME, and the
         ultimate is what they do after they stop.

         THE BEARINGS ARE FIXED AT SPAWN AND THERE IS NO HOMING. `ax`/`ay` are
         computed once, here, and `tickSpectre` never recomputes them: "thrown
         at where the quarry is NOW" is the design's own sentence, and a copy
         that steered would be a different ultimate. It is the first thing
         `bloodletting_relic_probe [1]` asserts.

         THREE OF THEM IN A FAN, and both the count and the fan are Rick's. The
         fan is `spread` radians either side of the bearing to the quarry, so
         the middle copy is the one the design describes and the outer two open
         the shape out -- three copies on ONE bearing would be one copy drawn
         three times, and three at random angles would not read as aimed. With
         `n` 1 the spread term is identically zero and this is the one-copy
         ultimate the design priced, which is what makes the two comparable.

         EACH STARTS TURNED TO ITS OWN BEARING (`spin: a`), so the three are
         visibly three objects from the first frame rather than one silhouette
         stamped three times. `dir` IS -1 AND IT IS A CONSTANT: see
         `tickSpectre` for why it is not `f.spinDir`.

         NOT `harrow`, AND THE COLLISION IS ON THIS RELIC'S OWN ROW. Lastlight
         is the SANCTIFIED scythe -- the same weapon -- and `smite` is
         byte-identical to `hemorrhage` apart from its name, so without a
         structural separation these two are one relic in two palettes.
         Harrowing sprays TWELVE small scythes that stick to the BODY, burden
         it and burst once. These stand in the HALL, milling, and while they
         stand the quarry can carry a stack count nothing else in the game can
         put on it.

         AND NOTHING IN THIS GAME HAS EVER OCCUPIED OPEN SPACE. The Thicket's
         vines root to walls, Breach's vents are torn in walls, Deadfall's
         sigils are stamped where a blow landed and the Stasis Field rings its
         own caster. These are the first objects the two balls have to navigate
         around, it is free, and the design calls it the strongest thing in the
         section 1. */
      const dx = foe.x - f.x, dy = foe.y - f.y;
      const a0 = Math.atan2(dy, dx);
      const N  = Math.max(1, u.n || 1);
      f.ultSpectres = [];
      for (let i = 0; i < N; i++){
        const a = a0 + (N === 1 ? 0
                                : ((i / (N - 1)) - 0.5) * 2 * (u.spread || 0));
        f.ultSpectres.push({ x: f.x, y: f.y,
                             ax: Math.cos(a), ay: Math.sin(a),
                             t: 0, flight: u.flight, stand: 0, life: u.life,
                             disc: u.disc, tick: u.tick, cd: 0,
                             spin: a, dir: -1, ticks: 0,
                             landed: false, dead: false, fade: 1 });
      }
      return;
    }

    if (u.kind === "wire"){'''),

# ---- 4. AND THEY ARE TICKED -------------------------------------------------
("tick-dispatch", '''    this.tickDeadfall(dt);''',
 '''    this.tickDeadfall(dt);
    this.tickSpectre(dt);'''),

# ---- 5. THE TICK ITSELF -----------------------------------------------------
("tick-spectre", '''  tickDeadfall(dt){''',
 '''  /* BLOODLETTING -- THE THROW, THE STICK, THE DRIFT, THE MILL, THE CEILING.

     FOUR STATES AND THE LAST ONE IS THE MECHANIC (design 7c): the copies leave
     the weapon; they STOP, which is the frame that tells a viewer they are
     staying and without which the ultimate looks like a missed shot; they mill
     for 4.5 seconds, which is most of the ultimate and the state that has to
     hold up without becoming wallpaper; and while they stand the quarry can
     carry more bleed than anything else in the game can put on it.

     AND THEY NO LONGER STOP DEAD, WHICH IS A CHANGE TO RICK'S OWN SECTION 1.
     It read "flies a short duration and then sticks in place"; he asked for
     "a small amount of movement so they slowly continue to float in the
     direction they were fired." `drift` is 6% of the throw speed, so a copy
     covers about a fifth of its own disc over a whole window -- enough that
     the hall is never quite the same shape twice and far too little to read as
     a second flight. `bloodletting_relic_probe [2]` no longer asserts that the
     position is constant; it asserts that the ONLY movement after landing is
     the drift along the fired bearing plus whatever the closing wall added.

     THE WHOLE THING IS ONE SCALAR AND THE PROBE REPORTS IT. `ticks` is the
     number the design is priced on -- 23 arms give lift = +5.6 + 0.245 x
     spectre damage at r2 0.80 with residuals smaller than the per-arm SE -- so
     TUNE ON TICKS LANDED, NOT ON WIN RATE. It is 30x cheaper and it is what
     the win rate is made of.

     THE COOLDOWN IS A COOLDOWN AND NOT A METRONOME. `cd` counts down and is
     only reset by a tick that LANDS, so a quarry that walks into a disc is
     bitten on the frame it arrives rather than on the next multiple of 0.22s.
     That is the barbed wire ring's rule one relic along -- a place it is
     unsafe to be -- and it is what makes dwell map cleanly onto ticks. EACH
     COPY CARRIES ITS OWN, so a quarry in an overlap is bitten by each. */
  tickSpectre(dt){
    const A = CONFIG.arena, R = CONFIG.physics.ballR, n = this.inset;
    /* THE FREEZE IS READ ONCE, AT THE TOP, AND EVERY COPY SEES THE SAME FRAME.
       Read live inside the loop it is not the same test for each of the three:
       the first copy to tick sets `hitStop` itself, and copies two and three
       then find the hall frozen BY THEIR OWN VOLLEY and skip. Whether a copy
       was paid depended on its index in the array, which is not a rule anybody
       chose -- and it silently capped the overlap the design is now built on.
       `bloodletting_relic_probe [3]` caught it as one owed tick in ten.

       The rule is unchanged and is the design's 6.5: nothing ticks THROUGH a
       freeze. A freeze this frame's own tick created is not one of those; it
       stops the NEXT step, which is where `step()` already returns early. */
    const froze = this.hitStop > 0;

    for (const f of [this.a, this.b]){
      const list = f.ultSpectres;
      if (!list.length) continue;
      const u = f.w.ult, foe = f === this.a ? this.b : this.a;
      let landedNow = 0, closedNow = 0, milling = null;

      for (const S of list){
        /* A DEAD COPY IS A PICTURE AND NOTHING ELSE. It dissolves where it was
           standing, which is why the fade is on the COPY and not on the
           fighter: three of them drift apart, and one per-fighter clock could
           only ever dissolve them all in the same place. */
        if (S.dead){ S.fade = Math.max(0, S.fade - dt / 0.35); continue; }

        /* THE CASTER'S CORPSE ENDS THEM, the way Deadfall's window ends with
           its own caster. NOTHING IS RESTORED HERE -- the ceiling is
           recomputed from scratch at the bottom of this method on every frame,
           so there is no paired write for this branch to forget. That is the
           design's third silent failure mode made unreachable rather than
           checked for. */
        if (!f.alive){ S.dead = true; continue; }

        if (!S.landed){
          S.t += dt;
          S.x += S.ax * u.speed * dt;
          S.y += S.ay * u.speed * dt;
          if (S.t >= S.flight){
            S.landed = true;
            landedNow++;
            f.spectreRings.push({ x: S.x, y: S.y, t: 0, life: 0.44 });
          }
        } else {
          S.stand += dt;
          if (S.stand >= S.life){ S.dead = true; closedNow++; continue; }
          /* THE DRIFT. Rick's, and it is the one line that stops these being
             furniture: a hazard that is very slightly still moving is one the
             other ball has to keep re-reading. Along the FIRED bearing and
             nothing else -- there is no steering here any more than there is
             in the flight. */
          S.x += S.ax * (u.drift || 0) * dt;
          S.y += S.ay * (u.drift || 0) * dt;
          if (milling === null) milling = S;
        }

        /* THEY STAY IN THE HALL, AND IN THE HALL AS IT IS NOW rather than as
           it was when they were thrown. `CONFIG.collapse` walks the inset
           0 -> 140 from t = 21s and the mean fight is 49.5s, so a copy
           anchored early spends much of its life inside a room that is closing
           on it. Design 6.5 asks for a decision and this is it: THE WALL
           SHOVES IT, it does not kill it. The alternative -- letting it die
           when the stone reaches it -- deletes an ultimate silently and late,
           which is the worse of the two failures to watch. Clamped with the
           ball's own margin, the same one `move()` uses. UNMEASURED, and the
           lab did not model the collapse at all. */
        S.x = clamp(S.x, n + R, A.w - n - R);
        S.y = clamp(S.y, n + R, A.h - n - R);

        /* THE SPIN IS THE PICTURE AND NOTHING READS IT -- `drawSpectre` and
           the pool's own pulse, and nothing else in the engine, which is why
           `engine_ab` is the proof that changing it is free.

           RICK'S, off the first sheet: "lets also increase the rotational
           speed by a lot." At the weapon's own 3.2 rad/s a copy that is not
           attached to anybody reads as DRIFTING rather than as milling -- a
           held weapon gets its sense of speed from the ball swinging it, and
           these have no ball. `=== undefined` and not `|| 1` (CLAUDE.md
           4.3).

           AND THE DIRECTION IS A CONSTANT -1, WHICH TOOK THREE GOES AND ONE
           RENDERED STRIP. Rick, twice: "the scythes spin the wrong way."

           Cut one was `+`. Cut two flipped it to `-` and was never rendered,
           because cut three replaced it with the caster's own `f.spinDir` --
           which is `side === 0 ? 1 : -1`, so on side A it is `+1` and the
           "fix" silently restored the direction he had already rejected. That
           is the whole of why he saw the same thing twice.

           `f.spinDir` IS THE WRONG INPUT AND NOT JUST A WRONG SIGN. A scythe
           cuts with the INSIDE of its crescent, so the direction that makes
           the edge lead is a property of THE ARTWORK -- and the artwork is not
           mirrored between sides. Tied to `spinDir` these would lead with the
           edge on side A and with the spine on side B, and a clank would
           reverse three objects in mid-air every time their wielder lost a
           bind.

           SETTLED BY LOOKING, on both arms at once rather than by reasoning
           about canvas handedness a fourth time:
           `05-reference/v59/bloodletting-spin-direction.png` is six frames of
           each. At `+` the crescent's opening trails and the blade leads with
           its spine; at `-` the opening faces into the travel and it scoops.
           `dir` is kept as a field rather than folded into the sign so the
           choice has somewhere to live. */
        S.spin += dt * f.w.spin * S.dir
                * (u.spinMul === undefined ? 1 : u.spinMul);

        /* DOES IT BITE WHILE FLYING? +12.7 against +11.2, inside the noise, so
           it is a picture choice. `=== undefined` and not `|| 1` again: a
           sweep must be able to set this to 0. */
        if (!S.landed && !(u.hitFly === undefined || u.hitFly)) continue;

        /* NO TICK ON A CORPSE, NONE AFTER `m.over`, AND NONE DURING HIT-STOP.
           The sim is frozen during a freeze and so is the hall -- and this
           method is on the normal step path, which `step()` does not reach
           while `hitStop` runs, so the third guard is belt and braces that
           also says what the rule is. The lab does all three and it is NOT
           free: a copy that kept milling through hit-stop would collect extra
           ticks for nothing, and `ticks` is the number the whole design is
           priced on. */
        if (this.over || froze || !foe.alive) continue;

        S.cd -= dt;
        if (S.cd > 0) continue;
        /* ONE TEST, AT THE QUARRY'S CENTRE, AGAINST THIS COPY'S DISC. And it
           reads THE FOE and nothing else: a spectre that milled both balls
           measures -16.5pp at z -6.02, which is BELOW this relic's own
           no-ultimate floor. A scythe has to fight near what it left behind,
           so a shared hazard is a self-inflicted wound for the whole window.
           Six standard errors is not a number to tune against -- it is a
           different relic. */
        const d = Math.hypot(foe.x - S.x, foe.y - S.y);
        if (d > S.disc) continue;
        S.cd = S.tick;
        S.ticks++;
        this.spectreHit(S, f, foe, d);
      }

      /* ONE VOICE AND ONE BEAT PER VOLLEY, NOT PER COPY. Three copies share a
         `flight`, so they land on the same frame: three copies of one sound is
         a click rather than a chord, and three `ult` beats would hand the
         director the same instant three times. `nightfell-arm`'s rule, one
         relic along -- the state change belongs to the VOLLEY. */
      if (landedNow){
        SFX.play("ult", { w: "bloodmirror-stick" });
        this.shake = Math.min(38, this.shake + 10);
        const S0 = list.find(S => S.landed && !S.dead) || list[0];
        /* THE LANDING FILES ITS OWN BEAT and the individual ticks file none --
           the Thicket's `_cineVine` rule, and at fifteen ticks a second across
           three copies filing them would hand the director a fight made of
           three objects standing still. The STICK is the beat because it is
           the event: it is the frame that says the things are staying. */
        this.beat({ kind: "ult", side: f === this.a ? 0 : 1,
                    x: S0.x, y: S0.y, w: f.w.id,
                    foeHpFrac: foe.hp / foe.maxHp });
      }
      if (closedNow) SFX.play("ult", { w: "bloodmirror-close" });

      /* THE MILL, RE-STRUCK, AND ONCE FOR THE WHOLE SET. CLAUDE.md 4.5:
         `_tone` ends on an exponential ramp over its whole length, so A HELD
         NOTE DOES NOT EXIST IN THIS TOOLKIT -- anything that must last is
         re-struck. The Winnowing's rung problem, and the design calls this the
         hard one of the four voices because it has to survive being heard for
         four and a half seconds without becoming a wash. Three of it at once
         would be exactly that wash. */
      if (milling){
        const was = Math.floor((milling.stand - dt) / 0.75);
        if (Math.floor(milling.stand / 0.75) > was)
          SFX.play("ult", { w: "bloodmirror-mill" });
      }

      /* AND A COPY LEAVES ONLY WHEN ITS PICTURE HAS FINISHED. */
      if (list.some(S => S.dead && S.fade <= 0))
        f.ultSpectres = list.filter(S => !S.dead || S.fade > 0);
    }

    /* ---- THE CEILING, RECOMPUTED AND NEVER RESTORED --------------------

       Both fighters, every frame, whether or not anybody has cast anything.
       There is no raise and no matching restore, so none of the design's three
       silent failure modes is reachable: a fighter's cap is a pure function of
       whether the OTHER fighter has a copy STANDING right now, a fresh Match
       starts at the status's own 4 and cannot inherit anything, and a window
       that merely expires puts it back on the same frame the last copy dies.

       RAISED WHILE ONE STANDS AND NOT WHILE THEY FLY. "While it stands" is the
       design's own wording, it is the arm Rick took (+7.9pp at z +4.35, against
       +9.4 for the whole fight), and the flight is 0.55s of a 5.05s object.
       THREE COPIES DO NOT RAISE IT THREE TIMES -- the ceiling is a ceiling and
       the count is not on it, which is the one part of this that three copies
       leave exactly where the design put it. */
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a;
      const live = foe.ultSpectres.some(S => S.landed && !S.dead);
      f.bleedCap = (live && foe.w.ult.cap)
                 ? foe.w.ult.cap : STATUS.hemorrhage.maxStacks;
    }
  }

  /* ONE TICK. Modelled on `jetHit` line for line, because it is the same shape
     of event: a payload that resolves OUTSIDE `resolveHit`, against the quarry
     only, from a thing that is not the caster. */
  spectreHit(S, own, foe, d){
    const u = own.w.ult;
    /* ROUNDED, because every damage number in this engine is an integer and
       this one gets printed over a ball. `dmgTakenMul` is the quarry's own
       Sunder -- nothing this relic applies, but a Cindercleave in the same
       fight can. */
    const dmg = Math.round((u.dmg || 3) * foe.dmgTakenMul());
    if (dmg > 0){
      this.hurt(foe, dmg, own);
      own.dealt += dmg;
      /* `hits` is deliberately NOT incremented: a tick does not go through
         `resolveHit`, and verify's "no pairing resolves on fewer than 6 hits"
         floor is about BLOWS LANDED, which this is not. The same call the
         Deadfall's mines and Breach's jets make. */
      foe.flash = 1; foe.ringFlash = 1;
      this.float(foe.x, foe.y - 40, dmg, AFFINITIES.bloodsworn.glow,
                 26 + dmg * 1.1);
    }
    /* THE BLEED LANDS AFTER THE DAMAGE, so a tick does not amplify itself --
       and it goes through `apply`, which reads the quarry's own `bleedCap`, so
       this is the one place in the game where a status can pass four. */
    const first = !this.taught.hemorrhage
                && !!(STATUS.hemorrhage && STATUS.hemorrhage.tip);
    if (first) this.taught.hemorrhage = true;
    foe.apply("hemorrhage", u.bleed || 2);
    /* AND THE TAG CARRIES THE COUNT WHILE THE CEILING IS UP, which is the only
       evidence on screen that the ceiling moved at all.

       Design 7c: "the stack readout going past four is the only evidence on
       screen that the ceiling moved", and v54 2c is the precedent that cost a
       build -- Deadfall's arming state was invisible at alpha 0.16 and no probe
       in this repo could have said so. A VIEWER CANNOT SEE A CONSTANT. The
       count is printed only while `bleedCap` is above the status default, so
       every other match in the game draws exactly what it drew before, and
       inside this window it is printed for the BLADE'S bleed too -- because the
       blade feeds the raised ceiling, and a number that appeared on some
       applications and not others would be worse than none. */
    this.statusTag(foe.x, foe.y, "hemorrhage", first,
                   foe.bleedCap > STATUS.hemorrhage.maxStacks
                     ? foe.stacks("hemorrhage") : 0);

    /* THE SHOVE, ALONG THIS COPY'S OWN BEARING -- out of its disc. The
       Thicket's rule and Breach's: `resolveHit`'s built-in knock fires away
       from the CASTER, and this hazard is not the caster, so a shove borrowed
       from that function would push the quarry along a line nothing on screen
       is drawn on. WITH THREE COPIES THAT MATTERS MORE, not less: a quarry
       shoved out of one disc is as likely to be shoved into another, and the
       bearing is the only thing that says which one did it.

       AFTER the damage and BEFORE the fatal test, so a killing tick still
       throws the corpse -- `killFlight` is what carries a slain ball into the
       wall it shatters against.

       IT DOES NOT BUY DWELL AND THE DESIGN SAYS SO: ticks fall 11.7 -> 10.9 and
       dwell 26.1% -> 23.1% when the foe is shoved. What the seven points buy is
       somewhere else -- a second thing in the hall interrupting the other
       ball's rhythm. */
    if (foe.alive && (u.knock || 0) > 0){
      const k = d || 1;
      const ax = d > 0.001 ? (foe.x - S.x) / k : S.ax;
      const ay = d > 0.001 ? (foe.y - S.y) / k : S.ay;
      foe.vx += ax * u.knock;
      foe.vy += ay * u.knock;
    }

    const fatal = !foe.alive;
    if (fatal){
      /* A TICK THAT ENDS THE FIGHT CARRIES THE FIGHT'S OWN WEIGHT.
         `resolveHit` swaps its hit-stop for `killStop` and arms `finisher` on a
         fatal blow; anything landing outside that function has to do it itself
         or this ultimate's killing blow is lighter than a swing. */
      this.hitStop = Math.max(this.hitStop, CONFIG.impact.killStop);
      this.finisher = 1.0;
    } else {
      /* SMALL ON PURPOSE, AND SMALLER NOW THAT THERE ARE THREE. A tick every
         0.22s from each of three copies with a full hit-stop each would freeze
         the hall solid for the whole window -- the Deadfall's first build made
         exactly that mistake in reverse. */
      this.hitStop = Math.max(this.hitStop, 0.02);
    }
    this.shake = Math.min(38, this.shake + (fatal ? 20 : 4));
    this.spawnFx(foe.x, foe.y, AFFINITIES.bloodsworn.glow, 10, 200, 0.40, 3);
    SFX.play("ult", { w: "bloodmirror-tick" });
    /* AND THE FATAL ONE FILES A BEAT, WHICH IS THE WHOLE OF v53 section 4.
       `cinema_clip` finds the killing blow with `plan.find(c => c.fatal)` and
       NOTHING on an `ult` beat carries that flag. Measured on Gravemourn before
       that line existed there: 30 of 58 kills were landed by a hand and ALL
       THIRTY rendered a clip with no killing blow. This ultimate deals damage
       and can therefore kill, so it must file one. */
    if (fatal)
      this.beat({ kind: "hit", side: own === this.a ? 0 : 1,
                  x: foe.x, y: foe.y, dmg, crit: false, fatal: true,
                  hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                  selfHpFrac: own.hp / own.maxHp,
                  spd: own.speed, foeSpd: foe.speed,
                  close: Math.hypot(own.vx - foe.vx, own.vy - foe.vy) });
  }

  tickDeadfall(dt){'''),

# ---- 6. THE BLADE'S OWN BLEED TAG CARRIES THE COUNT TOO ---------------------
("resolve-tag", '''      this.statusTag(hx, hy, k, first, k === "curse" ? Math.round(foe.curseSum()) : 0);''',
 '''      /* AND HEMORRHAGE CARRIES ITS COUNT WHILE A BLOODLETTING CEILING IS UP.
         Rick's ruling is that THE BLADE FEEDS THE RAISED CEILING TOO, which is
         what makes the window read as the fighter opening up rather than as an
         object landing -- so the blade's own tag has to be able to say `5`,
         `6`, `7`, `8` exactly as the spectre's does. Zero in every match with
         no standing spectre in it, which is every match this build had before
         this one. */
      this.statusTag(hx, hy, k, first,
                     k === "curse" ? Math.round(foe.curseSum())
                   : (k === "hemorrhage"
                      && foe.bleedCap > STATUS.hemorrhage.maxStacks)
                     ? foe.stacks("hemorrhage") : 0);'''),

# ---- 7. AND THE SHELL DRAWS PAST FOUR ---------------------------------------
("bleed-art", '''  _stBleed(m, f, R, n){
    const c = this.ctx, N = Math.min(4, n) * 2;''',
 '''  /* AND THE DRIP COUNT IS CLAMPED TO THE FIGHTER'S OWN CEILING, NOT TO FOUR.
     It was `Math.min(4, n)`, which was right for every fight ever played on
     this engine and is wrong the moment a Bloodletting spectre stands: eight
     stacks would have drawn exactly what four draws, and design 7c says the
     readout is THE ONLY EVIDENCE ON SCREEN that the ceiling moved. A viewer
     cannot see a constant, and no probe in this repo could have said so --
     which is v54 2c, the precedent that cost a build. */
  _stBleed(m, f, R, n){
    const c = this.ctx, N = Math.min(f.bleedCap || 4, n) * 2;'''),

# ---- 8. THE CAST'S OWN FLASH LIVES THE LENGTH OF THE THROW ------------------
("ultfx-life", '''              ravelbone: 1.5,''',
 '''              ravelbone: 1.5,
              /* THE SPECTRE IS NOT IN HERE. This is the THROW's flash and its
                 particle field only; the copy itself is on `f.ultSpectre` and
                 `f.spectreFade` for v54 section 2a's measured reason, so this
                 number is short on purpose and does not track `ult.life`. */
              bloodmirror: 1.5,'''),

# ---- 9. FOUR VOICES, AND THE THIRD IS THE HARD ONE --------------------------
("sfx", '''        } else if (w === "nightfell-stamp"){''',
 '''        } else if (w === "bloodmirror"){        // the copy leaves the blade
          /* THE THROW, and it is the CAST voice -- `fireUlt` plays
             `{ w: f.w.id }` for every relic, so this is the first of the four
             and nothing extra has to be scheduled for it. A wet tear followed
             by something leaving at speed: the copy coming off the weapon. */
          this._burst(t, { freq: 1100, q: 0.9, gain: 0.20, dur: 0.16, type:"bandpass" });
          this._tone (t, { freq: 260, to: 96, gain: 0.24, dur: 0.34, type:"sawtooth" });
          this._tone (t + 0.05, { freq: 620, to: 210, gain: 0.13, dur: 0.40, type:"triangle" });
        } else if (w === "bloodmirror-stick"){  // and it STOPS
          /* THE FRAME THAT SAYS IT IS STAYING. Design 7c: if the stick does not
             read, the ultimate looks like a missed shot -- so this is the
             LOUDEST of the four and it is the only one with a hard transient.
             A blade going into something and holding. */
          this._burst(t, { freq: 2400, q: 1.2, gain: 0.22, dur: 0.09, type:"bandpass" });
          this._tone (t, { freq: 150, to: 54, gain: 0.26, dur: 0.40, type:"sine" });
          this._burst(t + 0.03, { freq: 300, q: 0.5, gain: 0.17, dur: 0.36, type:"lowpass" });
        } else if (w === "bloodmirror-mill"){   // and it turns, for 4.5s
          /* THE HARD ONE, and the design says so. It has to survive being
             heard for four and a half seconds without becoming a wash, and
             CLAUDE.md 4.5 says a HELD NOTE DOES NOT EXIST IN THIS TOOLKIT --
             `_tone` ends on an exponential ramp over its whole length, so
             anything that must last is RE-STRUCK. `tickSpectre` strikes this
             every 0.75s, which is six strikes over a window.

             It is deliberately DULL and low: the Winnowing's rung problem, and
             the thing that keeps a repeated voice from becoming wallpaper is
             that it is quiet enough to sit under the ticks that ride on it. */
          this._tone (t, { freq: 86, to: 62, gain: 0.13, dur: 0.70, type:"sawtooth" });
          this._burst(t, { freq: 420, q: 0.7, gain: 0.07, dur: 0.55, type:"lowpass" });
        } else if (w === "bloodmirror-tick"){   // and something is inside it
          /* THE PAYMENT. It has to cut through a 0.03s hit-stop and be
             distinguishable from the mill it rides on, because the one thing a
             viewer has to learn from this ultimate is WHEN IT IS BEING PAID.
             Short, bright and wet.

             NO BURST IS LONGER THAN 0.6s. CLAUDE.md 4.5: `_burst` does not loop
             its 0.6s noise buffer, so anything longer plays silence for its
             tail. */
          this._burst(t, { freq: 3000, q: 1.0, gain: 0.14, dur: 0.07, type:"highpass" });
          this._tone (t, { freq: 330, to: 120, gain: 0.15, dur: 0.16, type:"sawtooth" });
        } else if (w === "bloodmirror-close"){  // and it is gone
          /* THE WINDOW CLOSING, and it is the quietest of the four on purpose:
             nothing happens on this frame. It is the mill's own note let go of
             -- same register, falling, with the noise bed taken out from under
             it -- so the absence is what a viewer hears. */
          this._tone (t, { freq: 74, to: 38, gain: 0.15, dur: 0.55, type:"sine" });
          this._tone (t + 0.04, { freq: 220, to: 90, gain: 0.08, dur: 0.44, type:"triangle" });
        } else if (w === "nightfell-stamp"){'''),

# ---- 9b. THE RING IS AGED ON THE PRESENTATION CLOCK -------------------------
# ---- 9b. THE RINGS ARE AGED ON THE PRESENTATION CLOCK -----------------------
("ring-tick", '''    for (const f of [this.a, this.b]){
      if (f.graspCrush){''',
 '''    /* THE COPIES' LANDING RINGS. HERE and not in `tickSpectre` for v54's
       reason, stated one relic along: anything presentation that can share a
       frame with an impact belongs on this clock, because a hit stop runs
       `decayImpactOnly` and a clock on the normal path freezes for exactly the
       frames the viewer is staring hardest at. Deadfall's blast froze on the
       floor 96.2% of the time before that was understood.

       `life` IS IN HALF-SECONDS, like every other presentation clock in this
       engine: this method is called once directly and once through
       `decayImpactOnly`, so it runs at 2x sim time and 0.44 is 0.22 seconds. */
    for (const f of [this.a, this.b]){
      if (f.spectreRings.length){
        for (const G of f.spectreRings) G.t += dt;
        f.spectreRings = f.spectreRings.filter(G => G.t < G.life);
      }
    }
    for (const f of [this.a, this.b]){
      if (f.graspCrush){'''),

# ---- 10. THE COPIES ARE DRAWN, UNDER BOTH FIGHTERS --------------------------
("draw-call", '''    if (__world){
    this.drawShades(m);''',
 '''    if (__world){
    /* UNDER both fighters and under the shades, because hazards the balls
       navigate around have to be things they pass IN FRONT OF -- and over the
       floor, because they are standing on it. IN THE WORLD PASS AND NOT THE
       EMISSIVE ONE: see `drawSpectre`. */
    this.drawSpectre(m);
    this.drawShades(m);'''),

("draw-spectre", '''  drawSigils(m){''',
 '''  /* THE COPIES, STANDING IN THE HALL.

     Design 7b: nothing in this game has ever occupied open space. The Thicket's
     vines root to walls, Breach's vents are torn in walls, Deadfall's sigils
     are stamped where a blow landed and the Stasis Field rings its own caster.
     These are the first objects the two balls have to navigate around, they are
     free, and the design calls it the strongest thing in Rick's section 1.

     THEY ARE THE WEAPON'S OWN SHAPE THROUGH THE WEAPON'S OWN DRAW PATH, so a
     change to `_scBarbed` reaches them for free and the two can never disagree
     -- "the same silhouette, red and ghosted" is the design's line and the
     silhouette is literally the same function.

     DRAWN IN THE WORLD PASS AND NOT THE EMISSIVE ONE. That is where every real
     weapon is drawn and it is deliberate: these are scythes the size of
     scythes, and putting solid blades into the emissive layer is CLAUDE.md
     4.1b's fault -- the art blowing the post chain out -- with bigger objects
     than any of the three relics that have already done it, and now three of
     them at once. If they ever want light, measure the art and the chain
     SEPARATELY first.

     THREE GRADIENTS A FRAME PER CASTER, SIX IN THE WORST CASE. Named because
     the same call in a LOOP is what cost Breach 14x its render time
     (`GRAIN_CACHE`, seventy-two gradient objects a frame); six is not that, and
     the flat-disc substitute is available if it ever becomes so. */
  drawSpectre(m){
    const c = this.ctx;
    for (const f of [m.a, m.b]){
      const u = f.w.ult, pal = f.aff;

      /* THE LANDING RINGS, AND THEY ARE THE FRAME THE DESIGN SAYS HAS TO WORK.
         Rick's, off the first sheet: photographed on a real match the STICK did
         not read at all -- a thin red line arriving in a busy frame, with
         nothing saying it had ARRIVED. Design 7c: "if it does not read, the
         ultimate looks like a missed shot."

         A RING AND NOT A BURST, and that is the distinction rather than a
         preference: a burst says something HIT, and nothing was hit -- the
         copies land on empty floor. A ring expanding to a disc's own edge says
         THIS IS NOW A PLACE, and it draws the boundary of the thing that has
         just been made once, hard, at the moment it appears, instead of asking
         the pool to hold that job for four and a half seconds.

         Drawn OUTSIDE the objects' own loop, because a ring has its own
         position and its own clock and must survive its copy being gone. */
      for (const RG of f.spectreRings){
        const k = clamp(RG.t / RG.life, 0, 1);
        const ease = 1 - Math.pow(1 - k, 3);
        const rr = u.disc * (0.16 + 0.90 * ease);
        c.save();
        c.globalAlpha = (1 - k) * 0.95;
        c.strokeStyle = pal.glow;
        c.lineWidth = 10 * (1 - k) + 1.5;
        c.beginPath(); c.arc(RG.x, RG.y, rr, 0, TAU); c.stroke();
        /* a second, tighter one a beat behind: one ring reads as a bubble and
           two read as something arriving hard */
        c.globalAlpha = (1 - k) * 0.55;
        c.strokeStyle = pal.core;
        c.lineWidth = 4 * (1 - k) + 1;
        c.beginPath(); c.arc(RG.x, RG.y, rr * 0.62, 0, TAU); c.stroke();
        c.restore();
      }

      for (const S of f.ultSpectres){
        const fade = S.dead ? S.fade : 1;
        if (fade < 0.02) continue;
        /* IN THE AIR THEY ARE THROWN OBJECTS AND ON THE GROUND THEY ARE
           PLACES. The floor only reads once one has stopped -- the STICK is the
           frame that tells a viewer it is staying, and a pool that arrived with
           the copy would spend the flight saying it had already landed. */
        if (S.landed || S.dead){
          /* THE GROUND THEY HAVE MADE UNSAFE. Not a dashed ring: `garrote_sheet`
             photographed one of those and it read as a RANGE INDICATOR, which
             is the one thing a hazard must not look like. A pool instead --
             dark in the middle, gone by the rim -- so what is drawn is ground
             rather than a boundary. It breathes at the mill's own rate so the
             floor and the blade are visibly one object.

             RAISED ON RICK'S WORD, off the first sheet: at the alphas this
             shipped with it read in one frame of three and vanished in the
             other two. IT COSTS THE POST CHAIN NOTHING -- this is drawn in the
             WORLD pass, not the emissive one, so none of it reaches the bloom
             and CLAUDE.md 4.1b's "take away AREA, not alpha" does not apply in
             either direction. That is the whole reason it could simply be
             turned up rather than redesigned. */
          const pulse = 1 + 0.05 * Math.sin(S.spin * 2);
          const rr = u.disc * pulse;
          const g = c.createRadialGradient(S.x, S.y, rr * 0.10, S.x, S.y, rr);
          g.addColorStop(0,    pal.core + "8E");
          g.addColorStop(0.42, pal.core + "52");
          g.addColorStop(0.84, pal.core + "24");
          g.addColorStop(1,    pal.core + "00");
          c.save();
          c.globalAlpha = fade;
          c.fillStyle = g;
          c.beginPath(); c.arc(S.x, S.y, rr, 0, TAU); c.fill();
          /* AND A WET RIM, so the extent is a readable edge rather than a
             gradient that could end anywhere. Continuous and soft: a DASHED
             one is what read as a range indicator. */
          c.globalAlpha = fade * 0.55;
          c.strokeStyle = pal.core;
          c.lineWidth = 2.4;
          c.beginPath(); c.arc(S.x, S.y, rr * 0.94, 0, TAU); c.stroke();
          c.restore();
        }

        c.save();
        /* GHOSTED, and it dissolves rather than being cut. The alpha is the
           only thing separating a copy from a real weapon, so it is held high
           enough that the barbs still read: the objects have to be legible
           enough to navigate around. */
        c.globalAlpha = 0.80 * fade;
        /* THEY TURN ABOUT THEIR OWN CENTRES, AND THAT IS RICK'S: "the scythe
           should rotate around its center axis. not the end of its handle."

           They used to be drawn the way a HELD weapon is -- pivot at the ball's
           centre, weapon offset `R - 6` along the radius -- which is right for
           a scythe somebody is swinging and wrong for one nobody is holding:
           the handle end traced a circle and the whole object read as orbiting
           an invisible ball rather than spinning.

           AND "THE CENTRE" TOOK THREE GOES, BECAUSE IT IS THREE DIFFERENT
           POINTS AND ONLY ONE OF THEM IS WHAT A VIEWER MEANS.

           Cut one read the PATH CONSTANTS: x in [0, L*1.03], y in
           [-W*1.32, W*0.30], middle "(L*0.515, -W*0.51)". Rasterised, the INK
           spans x in [-4, 102] -- the crescent's FILL never reaches its own
           nominal control point, and the snath is a STROKE with a round cap
           that runs 4 units BEHIND the origin -- so that was 7.6 units out
           before anything else was decided. v56 learned the same thing on
           Revenant's hand: measure the bounding box of the PARTS, not the
           skeleton's extent.

           Cut two used the ink's BOUNDING-BOX centre, (L*0.4455, -W*0.5435),
           and Rick said it still was not spinning on its centre. He was right
           and the measurement says why: **a crescent's ink is nearly all in
           the blade**, so the bounding box's middle is a point with almost no
           object at it. Three candidates, measured off the drawn pixels:

             bounding-box centre   (L*0.4455, -W*0.5435)   farthest ink 59.0
             1-centre (minimax)    (L*0.4455, -W*0.2622)   farthest ink 54.6
             CENTRE OF MASS        (L*0.6165, -W*0.2996)   farthest ink 73.3

           The centre of MASS is what ships. It is what a thrown blade actually
           turns about, it is the only one of the three with the object's own
           substance at it, and "spins on its center axis" means the visual mass
           stays put rather than orbiting. `rmax` is NOT the check for this --
           the farthest ink is the same distance from ANY pivot under rotation,
           so a constant sweep radius cannot tell a good centre from a bad one,
           and the first version of this check was vacuous.

           AND THAT CHANGES WHAT THE BLADE COVERS. Pivoted at `R - 6` the tip
           swept exactly `R + reach` = the disc, so the drawn sweep and the hit
           box were the same circle for free. Centred on the mass, the sweep is
           `artScale * 0.6664 * L` and only `artScale` 1.88 puts it back on the
           rim.
           `bloodmirror_build` PRINTS both numbers on every run rather than
           letting them drift apart quietly -- a picture that claims a smaller
           hazard than the one that exists is the hardest kind of bug in this
           repo to see, because both halves stay internally consistent. What
           carries the extent when they differ is the POOL and its rim, which is
           drawn at the disc and is why it was worth turning up. */
        const L = f.w.reach + 6, WW = f.w.artW;
        const sc = (u.artScale === undefined ? 1 : u.artScale)
                 * (fade < 1 ? 0.86 + 0.14 * fade : 1);
        c.translate(S.x, S.y);
        c.rotate(S.spin);
        c.scale(sc, sc);
        c.translate(-L * 0.6165, WW * 0.2996);
        if (!litWeapon(c, f.w.shape, L, WW, pal, f.drawK, S.spin)){
          const fn = SHAPES[f.w.shape];
          if (fn) fn(c, L, WW, pal, f.drawK);
        }
        c.restore();
      }
    }
  }

  drawSigils(m){'''),

("ult-block", '''    ult:{ name:"%ULT%", charge:1e9, kind:"effigy", tip:"%TIP1%" },''',
 '''    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"effigy",
          flight:%FLIGHT%, speed:%SPEED%, life:%LIFE%, disc:%DISC%,
          tick:%TICK%, dmg:%DMG_T%, bleed:%BLEED%, cap:%CAP%,
          knock:%KNOCK%, hitFly:%HITFLY%,
          n:%N%, spread:%SPREAD%, drift:%DRIFT%,
          spinMul:%SPINMUL%, artScale:%ARTSCALE%,
          tip:"%TIP%" },'''),

]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=("1", "2", "3b"))
    ap.add_argument("--src", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ult", default=ULT_NAME)
    ap.add_argument("--tip", default=ULT_TIP)
    ap.add_argument("--dmg", type=float, default=None,
                    help="THE BLADE. Not the ultimate's per-tick damage, "
                         "which is --tickdmg.")
    for k, v in ULT.items():
        ap.add_argument(f"--{k}", type=float, default=v)
    A = ap.parse_args()
    if A.dmg is None:
        A.dmg = TUNED_BM if (A.stage == "3b" and TUNED_BM is not None) \
            else BLADE_IN

    src = A.src or {"1": "../02-chain/sc-tipfix.html",
                    "2": "../02-chain/sc-bloodmirror.html",
                    "3b": "../02-chain/sc-bloodletting.html"}[A.stage]
    out = A.out or {"1": "../02-chain/sc-bloodmirror.html",
                    "2": "../02-chain/sc-bloodletting.html",
                    "3b": "../02-chain/sc-bloodletting.html"}[A.stage]
    src_p = (HERE / src).resolve()
    out_p = (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nBLOODMIRROR -- STAGE {A.stage}: "
          + {"1": "the 32nd relic, its ultimate STUBBED",
             "2": "BLOODLETTING -- the throw, the stick, the mill, the ceiling",
             "3b": "THE BLADE"}[A.stage])
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR. Every stage asserts what has to be under it.
    if "cursePool" not in s0:
        raise SystemExit("this source predates the v53 curse rework")
    if "tickNet" not in s0:
        raise SystemExit("this source is not the v61 tip -- `tickNet` is "
                         "absent. Build off `sc-tipfix.html`; the brief's "
                         "Cindercleave tip predates Ravelbone and Gloamwire.")
    if 'tip:"Hits reflect 8% of the damage that cursed, stacks 3 times"' not in s0:
        raise SystemExit(
            "STAGE T IS NOT UNDER THIS BUILD. `tipfix_build.py` is the brief's\n"
            "  stage T and it goes FIRST, because it is the only stage that can\n"
            "  be proven inert -- and proving it inert is worth much less once\n"
            "  a relic has been added on top of it.")

    if A.stage != "3b":
        if len(A.tip) > 72:
            raise SystemExit(f"ULT TIP is {len(A.tip)} characters against "
                             f"verify's 72:\n  {A.tip}")

    if A.stage == "1":
        if f'id:"{RELIC}"' in s0:
            raise SystemExit("this source already has Bloodmirror -- built")

        # THE PHYSICAL STATS ARE THE TYPE'S, ASSERTED AND NOT ASSUMED. Every
        # number in the design was measured on Thornwake's body -- same shape,
        # mass, reach and 5.24s contact gap -- and is only transferable if the
        # five shipped scythes really do agree. If they do not, the design's
        # numbers are not this relic's numbers and that is a finding, not a
        # detail.
        scythes = ["lastlight", "thornwake", "foregone", "vesper",
                   "cindercleave"]
        got = {r: phys(s0, r) for r in scythes}
        keys = ("reach", "width", "artW", "spin", "mass", "mode")
        base = {k: got[scythes[0]].get(k) for k in keys}
        odd = {r: {k: v.get(k) for k in keys if v.get(k) != base[k]}
               for r, v in got.items()}
        odd = {r: d for r, d in odd.items() if d}
        if odd:
            raise SystemExit(
                "the five shipped scythes do NOT agree on the type's own "
                "stats, so the\n  design's numbers -- all measured on one "
                "scythe body -- are not\n  transferable to a sixth:\n  "
                + "\n  ".join(f"{r}: {d}" for r, d in odd.items()))
        print(f"  body  one set across {len(scythes)} scythes -- the TYPE "
              f"owns it")
        print(f"        {base}")
        for k, v in base.items():
            lit = v.strip('"')
            if f"{k}:{lit}" not in S1[0][2].replace('"', "") \
               and f'{k}:"{lit}"' not in S1[0][2]:
                raise SystemExit(
                    f"the entry about to be written does not carry the type's "
                    f"own {k} ({v})")

        # AND THE ART EXISTS. Stage 1 ships a drawn weapon or it ships a relic
        # nobody can see, and `SHAPES.scythe`'s router is the only thing that
        # decides which.
        if 'if (key === "bloodsworn") return SHAPES._scBarbed' not in s0:
            raise SystemExit(
                "`SHAPES.scythe` does not route bloodsworn to `_scBarbed` in "
                "this build.\n  Stage 1 would ship an undrawn relic.")
        if "// and a tip hook" not in s0:
            raise SystemExit(
                "`_scBarbed` has no tip hook to remove in this source.\n"
                "  Either it is already gone -- in which case this build has\n"
                "  been run before -- or the shape has moved. Do not weaken\n"
                "  the anchor; find out which.")
        print("  art   SHAPES.scythe -> _scBarbed, TIP HOOK REMOVED (Rick's,")
        print("        2026-09-01, off a zoom shot before this shipped). The")
        print("        five barbs and their side are untouched and are now a")
        print("        chosen state -- he was shown the sign-flip sheet.")

        edits = S1
        print(f"  ult   {A.ult}  STUBBED at charge 1e9, kind \"effigy\"")
        print(f"  blade {A.dmg:g}   (brief section 5's START, not its answer)")
    elif A.stage == "2":
        if f'id:"{RELIC}"' not in s0:
            raise SystemExit("this source has no Bloodmirror -- run stage 1")
        if "tickSpectre" in s0:
            raise SystemExit("this source already has Bloodletting -- built")

        # THE DISC IS NOT A KNOB AND THE GEOMETRY IS WHY. "A copy of itself"
        # fixes it: the copy pivots at `R - 6` and draws `reach + 6`, so its
        # swept radius is exactly `R + reach`. A `disc` that did not equal that
        # would be a hit box the picture disagrees with -- the hardest bug in
        # this repo to see, because both halves stay internally consistent.
        R = float(re.search(r"ballR:\s*([\d.]+)", s0).group(1))
        reach = float(phys(s0, RELIC)["reach"])
        if abs((R + reach) - A.disc) > 1e-6:
            raise SystemExit(
                f"REFUSING TO WRITE -- disc {A.disc:g} is not the copy's own "
                f"sweep.\n  ballR {R:g} + reach {reach:g} = {R + reach:g}. The "
                f"disc is not a knob:\n  'a copy of itself' is what fixes it, "
                f"and a disc that disagrees with the\n  drawn sweep is a hit "
                f"box the picture lies about.")
        print(f"  disc  {A.disc:g} = ballR {R:g} + reach {reach:g}   "
              f"(NOT a knob -- it is what 'a copy of itself' means)")

        # AND WHAT THE BLADE ACTUALLY COVERS, PRINTED EVERY RUN. Rick's
        # centre-axis rotation means the drawn sweep is no longer the disc for
        # free -- see `drawSpectre`. A picture that claims a smaller hazard than
        # the one that exists is the hardest kind of bug in this repo to see,
        # because both halves stay internally consistent, so the two numbers are
        # put next to each other rather than left to drift apart quietly.
        # 0.6664 IS MEASURED, NOT DERIVED. It is the farthest drawn INK from
        # the drawn ink's own CENTRE OF MASS, rasterised off `SHAPES.scythe`.
        # The path constants give 0.555 about a point 7.6 units away, and the
        # ink's bounding-box centre gives 0.5367 about a point with almost no
        # object at it -- a crescent's mass is nearly all in the blade.
        L = reach + 6.0
        swept = A.artscale * 0.6664 * L
        fill = swept / A.disc
        print(f"  sweep {swept:.1f} at artScale {A.artscale:g} "
              f"({fill:.0%} of the disc)   "
              + ("the blade fills it" if fill > 0.97 else
                 "THE POOL CARRIES THE REST OF THE EXTENT"))
        print(f"        artScale {A.disc / (0.6664 * L):.2f} is the one that "
              f"puts the tip back on the rim")
        print(f"  spin  {A.spinmul:g}x the weapon's own rate   "
              f"(presentation only -- engine_ab is the proof)")

        # AND THE CEILING HAS TO BE ABOVE THE STATUS'S OWN, OR THE WHOLE
        # ULTIMATE IS THE ARM THAT MEASURED -2.5pp AT z -0.93.
        base = float(re.search(r"hemorrhage:\s*\{[^}]*maxStacks:\s*(\d+)",
                               s0).group(1))
        if A.cap <= base:
            raise SystemExit(
                f"REFUSING TO WRITE -- cap {A.cap:g} is not above "
                f"hemorrhage's own {base:g}.\n  Under the ceiling, adding bleed "
                f"to this spectre measures -2.5pp at z -0.93;\n  above it, "
                f"+6.9pp at z +2.67. The ceiling IS the ultimate.")
        print(f"  cap   {base:g} -> {A.cap:g} while it stands, PER FIGHTER "
              f"(design 6.3)")

        edits = S2
        print(f"  ult   {A.ult}  charge {A.charge:g}, kind \"effigy\"")
        print(f"  tip   {len(A.tip)}/72  {A.tip!r}")
        print(f"  copies {A.n:g} in a fan of +/-{A.spread:g} rad, drifting "
              f"{A.drift:g} px/s   (RICK'S -- the design prices ONE)")
        print(f"  throw {A.flight:g}s at {A.speed:g} = "
              f"{A.flight * A.speed:g} units, NO homing")
        print(f"  mill  {A.life:g}s, a tick every {A.tick:g}s -> "
              f"{A.life / A.tick:.1f} ticks a cast at full dwell")
        print(f"  each  {A.tickdmg:g} damage, {A.bleed:g} Hemorrhage, "
              f"knock {A.knock:g}, FOE ONLY")
        print(f"  blade {A.dmg:g}   (unchanged by this stage; 3b bisects it)")
    else:
        # ---- STAGE 3b: THE BLADE, AND NOTHING ELSE ----------------------
        # `dmg` is the ONLY thing this stage writes. It is a one-line rewrite of
        # the shipped entry rather than a re-run of stages 1 and 2, so a retune
        # can never quietly ship a different ultimate alongside a different
        # blade -- v56's failure pointed the other way, and this is the cheap
        # half of never repeating it.
        if TUNED_BM is None and A.dmg == BLADE_IN:
            raise SystemExit(
                "REFUSING TO RUN -- `TUNED_BM` is None and no --dmg was given."
                "\n  The blade is not a guess and it is not a bisection. What"
                "\n  settles one on this roster is a WIDE DIRECT MEASUREMENT at"
                "\n  n >= 1000 a point, on BOTH sides, repeated on a SECOND seed"
                "\n  block:"
                "\n\n    python bloodmirror_sweep.py --only 0"
                "\n    python bloodmirror_sweep.py --only 1 --points a,b,c"
                "\n\n  v48, v56 and v59 each learned separately that a bisection"
                "\n  converges on the noise in its tail; Shroudmaul's returned"
                "\n  19.92 where the answer was 21.00, and its three-point"
                "\n  confirmation was monotonic while being wrong, because it"
                "\n  was drawn on one seed block.")
        if f'id:"{RELIC}"' not in s0 or "tickSpectre" not in s0:
            raise SystemExit("this source is not the stage-2 build")
        e2 = entry(s0, RELIC)
        mm = re.search(r"dmg:\s*([\d.]+),", e2)
        if not mm:
            raise SystemExit("cannot retune: no dmg in Bloodmirror's own entry")
        j2 = s0.index(e2) + mm.start()
        print(f"  blade {float(mm.group(1)):g} -> {A.dmg:g}")
        print("        and NOTHING else -- one line, in this relic's own entry")
        s = s0[:j2] + f"dmg:{A.dmg:g}," + s0[j2 + len(mm.group(0)):]
        edits = []

    subs = {"%ULT%": A.ult, "%TIP1%": ULT_TIP1, "%TIP%": A.tip,
            "%BLURB%": BLURB, "%DMG%": f"{A.dmg:g}",
            "%CHARGE%": f"{A.charge:g}", "%FLIGHT%": f"{A.flight:g}",
            "%SPEED%": f"{A.speed:g}", "%LIFE%": f"{A.life:g}",
            "%DISC%": f"{A.disc:g}", "%TICK%": f"{A.tick:g}",
            "%DMG_T%": f"{A.tickdmg:g}", "%BLEED%": f"{A.bleed:g}",
            "%CAP%": f"{A.cap:g}", "%KNOCK%": f"{A.knock:g}",
            "%HITFLY%": "true" if A.hitfly else "false",
            "%SPINMUL%": f"{A.spinmul:g}", "%ARTSCALE%": f"{A.artscale:g}",
            "%N%": f"{A.n:g}", "%SPREAD%": f"{A.spread:g}",
            "%DRIFT%": f"{A.drift:g}"}
    for label, old, new in edits:
        # BOTH SIDES. Stage 2's `ult` anchor is the block STAGE 1 WROTE, so it
        # carries `Bloodletting` and the stub tip rather than the placeholders
        # this file spells them with. Substituting only the replacement is how
        # a builder ends up unable to find its own previous stage's output.
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)
    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    ult_matches(s, A, A.stage)

    # THE SCHOOL'S OWN CHANNEL, ASSERTED AGAINST WHAT WAS WRITTEN.
    if A.stage == "1":
        mine = body_block(s, RELIC, "onHit")
        others = {r: body_block(s, r, "onHit")
                  for r in ("oathwound", "redflail", "widowmaker",
                            "marrowdraw", "ravelbone")}
        if mine != "{ hemorrhage: 2 }".replace(" ", "").replace("{", "{ ") \
           and mine.replace(" ", "") != "{hemorrhage:2}":
            raise SystemExit(f"onHit written as {mine!r}, not the school's "
                             f"`hemorrhage:2`")
        print(f"  onHit {mine}   (the school's own weight; the others carry "
              f"{sorted(set(others.values()))})")

    # THE PARTICLE FIELD GOES IN BOTH COPIES OR IT GOES IN NEITHER.
    # `src/render/fx.js` is the source and `fx_build.py` inlines it; a spec
    # added only to the page is a spec the next `fx_build` run silently drops,
    # and `ULTFX.sync` returns on a missing spec rather than erroring. That is
    # why `ravelbone` and `gloamwire` have no field today and nothing said so.
    if A.stage == "2":
        fx_p = (HERE / "../src/render/fx.js").resolve()
        if not fx_p.exists():
            raise SystemExit(f"no such file: {fx_p} -- the spec source")
        fx0 = fx_p.read_text(encoding="utf-8")
        grown = FX_ANCHOR.replace(" }\n  };", " }" + FX_SPEC + "\n  };")
        # THE SIGNATURE AND NOT THE NAME. `bloodmirror:` also appears in
        # `ultFx`'s `life` map, which the stage-2 insert above has just
        # written -- so a bare name test reports "already built" on a build
        # this very run created.
        SIG = f"{RELIC}: {{ mode: 'burst'"
        if SIG in s:
            raise SystemExit("the page already carries this spec -- built")
        if FX_ANCHOR not in s:
            raise SystemExit(
                "cannot find the end of the SPECS table in the page.\n"
                "  The spec goes in BOTH copies or in NEITHER: a field added "
                "only to the page\n  is dropped by the next `fx_build` run, "
                "silently, because `ULTFX.sync`\n  returns on a missing spec "
                "rather than erroring.")
        s = one(s, FX_ANCHOR, grown, "fx spec (page)")
        # AND THE SOURCE MAY ALREADY HAVE IT. `src/render/fx.js` is not
        # rewritten by a rebuild of this stage, so a second run finds the spec
        # already there -- which is not an error and must not look like one.
        # The comparison below is the real check either way.
        if SIG in fx0:
            fx1 = fx0
            print("  ok    fx spec (src/render/fx.js)  already present")
        elif FX_ANCHOR in fx0:
            fx1 = fx0.replace(FX_ANCHOR, grown, 1)
            fx_p.write_text(fx1, encoding="utf-8", newline="\n")
            print("  ok    fx spec (src/render/fx.js)  written")
        else:
            raise SystemExit(
                "cannot find the end of the SPECS table in src/render/fx.js, "
                "and it does\n  not already carry this spec. Find out what "
                "moved -- do not write only the\n  page.")
        # AND THE TWO COPIES ARE COMPARED, NOT ASSUMED. `thornshear_build.py`
        # refuses to write unless they are byte-identical; this is the same
        # check, scoped to the table rather than to the whole file, because the
        # page's copy has been through `fx_build`'s inliner.
        i0 = fx1.index("var SPECS = {"); i1 = fx1.index("\n  };", i0)
        j0 = s.index("var SPECS = {");   j1 = s.index("\n  };", j0)
        if fx1[i0:i1] != s[j0:j1]:
            raise SystemExit(
                "REFUSING TO WRITE -- the SPECS table in the page and in "
                "src/render/fx.js\n  are not identical after the insert. A "
                "spec that exists in only one of them\n  is a field the next "
                "`fx_build` run drops or invents.")
        n_fx = fx1[i0:i1].count("mode:")
        print(f"        {n_fx} specs, byte-identical in both copies")
        print("        NOTE: `ravelbone` and `gloamwire` still have NONE, and")
        print("        `ULTFX.sync` returns silently on a missing spec.")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")

    if A.stage == "1":
        print("\n  GATE 1:")
        print(f"    python engine_ab.py --a {src} --b {out} --ids <the 31> --n 8")
        print("      IDENTICAL in every match not containing Bloodmirror.")
        print(f"    python verify.py --game {out} --n 40")
        print("      completes with 32 relics. Bloodmirror will be LOW and")
        print("      that is not a failure -- the design measured its own")
        print("      no-ultimate floor at 48.8% on a 27-relic roster and the")
        print("      brief predicts ~23% at blade 21 on this one. Print it.")
        print("      Do not tune to it.")
        print("      AND THE ART CHANGE IS IN THIS SAME LINK, so this run is")
        print("      also v58's proof that a `SHAPES` edit is render-only.")
        print("    python silhouette_probe.py --game " + out + " \\")
        print("      --types scythe --sheet "
              "../05-reference/v59/scythe-row-notip.png")
        print("      BRIEF OPEN DECISION 6, ANSWERED. The tip hook is off on")
        print("      Rick's word; this is the row it leaves behind, and the")
        print("      number to watch is whether bloodsworn moved TOWARD its")
        print("      nearest sibling -- removing a shape can only lose")
        print("      separation, and he took that trade with the picture in")
        print("      front of him.")

    if A.stage == "2":
        print("\n  GATE 2:")
        print(f"    python bloodletting_relic_probe.py --game {out}")
        print("      13/13, one check per sentence of the design -- and check")
        print("      12 is TICKS A FIGHT, which must be 10.5-11.0. That is the")
        print("      scalar the whole design is priced on and it is the")
        print("      registered prediction this build exists to falsify.")
        print(f"    python engine_ab.py --a {src} --b {out} --ids <the 31> --n 8")
        print("      IDENTICAL on the 31 in any match containing no cast. The")
        print("      `apply` edit touches every relic that applies any status,")
        print("      so this is the check that says `bleedCap` is 4 whenever")
        print("      nothing has raised it.")
        print("    FILM IT. BEFORE YOU TUNE. Brief section 7d and CLAUDE.md")
        print("      4.0: this ultimate is a thing you watch stand there for")
        print("      four and a half seconds. Thirty seconds of clip on")
        print("      placeholder numbers costs four minutes; v43 spent about")
        print("      thirty thousand fights learning that.")
        print("      AND PHOTOGRAPH THE STACK READOUT AT 5, 6, 7 AND 8 off a")
        print("      real match. Design 7c calls it the only evidence on")
        print("      screen that the ceiling moved, and v54 2c is the")
        print("      precedent that cost a build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
