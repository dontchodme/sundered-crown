#!/usr/bin/env python3
"""STAGE T OF THE BLOODMIRROR BRIEF -- THE TIP SURFACE. TWO EDITS, NEITHER READ
BY THE SIM.

    python tipfix_build.py --src ../02-chain/sc-crossweave.html \
                           --out ../02-chain/sc-tipfix.html

**THE DESIGN IS NOT THIS FILE'S.** `06-docs/v59/tip-surface-v59.md` is the
measurement and `06-docs/v59/bloodmirror-build-brief-v59.md` stage T is the
instruction. Change 2's width is RICK'S, picked from a spread of four
photographed at 1080x1920 (720 fits his line by 7px and looks squeezed; 800 was
offered and not taken). This builder implements and refuses; it does not choose.

## THE FOUR CHANGES, AND ONLY TWO OF THEM ARE IN THE BUILD

    1  STATUS.curse.tip      -> "... , stacks 3 times"      HERE
    2  _tagFirst box width   596 * k -> 760 * k             HERE
    3  verify.py status cap  48 -> 72                       a tool, not a build
    4  tip_audit.py EXTRACT  measure the BUNDLED face       a tool, not a build

3 and 4 are edits to `tools/` and are not made by this file -- a builder that
rewrites its own gates is a builder that can pass itself.

## WHY STAGE T IS FIRST

It is the only stage in the Bloodmirror brief that can be proven inert. Neither
edit is read by the sim: `STATUS.curse.tip` is a string the renderer prints and
`_tagFirst` is a method on `Renderer`. So `engine_ab` must come back IDENTICAL
on every relic in every match, and if a single bit moves THAT is the finding and
it stops the stage.

## THE ONE THING THIS CHANGE CAN BREAK, AND IT IS GEOMETRY

`_tagFirst` positions itself with

    const x = clamp(g.x - w / 2, 6, A.w - w - 6);

and `clamp(v,a,b)` is `v < a ? a : v > b ? b : v`, so when `a > b` -- a box
wider than the hall it is drawn in -- it returns `a` and the box runs off the
right edge instead of failing. The box is measured in DEVICE pixels and drawn in
ARENA units, `k = 1 / this.scale` and `this.scale = this.aw / 520`, so its width
in arena units is `760 * 520 / aw` and it grows as the render gets SMALLER.

    aw (arena px)   box at 596      box at 760      A.w - w - 6
    1080                287             366             148
     540                574             732            -218   <-- already broken
                                                              at 596 today

**That is not this change's defect and this change makes it worse.** It is
printed below at both resolutions rather than asserted, because the brief's own
gate for it is to photograph a real pop-up, and a number computed here cannot
see what a person looking at the frame can. See the gate list this prints.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# ---------------------------------------------------------------- the edits --

# CHANGE 1. Rick's own line, and the defect in the old one is not the wording
# convention -- curse remembers THREE blows and the line describes one, so a
# reader guesses the bonus is 8% where a full pool is 24%. The claim that this
# string is "pre-rework wording", carried as an open bug through three
# documents, is false: `curse-build-v53.md` section 2 lists this exact string in
# the table of what the rework SHIPPED.
CURSE_OLD = 'Hits reflect 8% of the damage that cursed'
CURSE_NEW = 'Hits reflect 8% of the damage that cursed, stacks 3 times'

# CHANGE 2. RICK'S, from four widths photographed at 1080x1920. The widening
# applies to all eight statuses, which is why it was his call and not a
# mechanical consequence of change 1 -- the next longest tip is sunder at 472px
# and gains 228px of room it did not ask for (tip-surface-v59 open decision 2).
TAG_OLD = "const w = 596 * k, h = 92 * k;"
TAG_NEW = ("const w = 760 * k, h = 92 * k;   /* 596 -> 760: RICK'S, from a "
           "spread of four\n"
           "                                        photographed at 1080x1920. "
           "His curse line is\n"
           "                                        653px and the text budget "
           "is w - 60, so 596\n"
           "                                        ran 117px into the hall and "
           "720 fit by 7. This\n"
           "                                        box does NOT wrap, does NOT "
           "clip and does NOT\n"
           "                                        measure -- an over-long tip "
           "just draws out of\n"
           "                                        it. tip-surface-v59 section "
           "1. */")

# The measured widths of every shipped tip in the face `_tagFirst` actually
# draws in -- 'Atkinson Hyperlegible Next' at 25px, from tip-surface-v59 1.1.
# Carried here so the refusal below is against MEASURED pixels and not against a
# character count, which is the wrong unit and has been twice.
TIP_PX = {"blessing": 378, "entangle": 431, "smite": 441, "hex": 447,
          "ward": 455, "sunder": 472, "curse": 475}
CURSE_NEW_PX = 653          # measured, tip-surface-v59 section 0


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-crossweave.html")
    ap.add_argument("--out", default="../02-chain/sc-tipfix.html")
    ap.add_argument("--box", type=int, default=760,
                    help="RICK'S 760. He was shown 596/720/760/800.")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nSTAGE T -- THE TIP SURFACE. Two edits, neither read by the sim.")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE CHAIN IS LINEAR AND THIS STAGE ASSERTS WHAT HAS TO BE UNDER IT.
    if "cursePool" not in s0:
        raise SystemExit(
            "this source has no cursePool -- change 1 describes the REWORKED "
            "curse\n  ('stacks 3 times' is the pool's top-K rule) and would be "
            "a lie on a\n  build that still eats maximum life.")
    if "_tagFirst" not in s0:
        raise SystemExit("this source has no `_tagFirst` -- wrong surface")

    # THE BUDGET IS THE BOX MINUS ITS TWO 30px INSETS, AND IT IS MEASURED IN THE
    # FACE THE BOX IS DRAWN IN. Characters are the wrong unit and the wrong
    # typeface is a 27% error either way (tip-surface-v59 1.2).
    budget = A.box - 60
    if CURSE_NEW_PX > budget:
        raise SystemExit(
            f"REFUSING TO WRITE -- the new curse line is {CURSE_NEW_PX}px and "
            f"the box at {A.box}\n  gives {budget}px. That is the exact failure "
            f"this stage exists to fix,\n  reintroduced by a narrower box.")
    over = {k: v for k, v in TIP_PX.items() if v > budget}
    if over:
        raise SystemExit(f"REFUSING TO WRITE -- these tips overflow at "
                         f"box {A.box}: {over}")

    print(f"  box  {A.box}px, text budget {budget}px")
    print(f"  curse {CURSE_NEW_PX}px  slack {budget - CURSE_NEW_PX:+d}"
          f"   (at 596 it was {536 - CURSE_NEW_PX:+d} -- it ran into the hall)")
    worst = max(TIP_PX.items(), key=lambda kv: kv[1])
    print(f"  worst of the other seven: {worst[0]} {worst[1]}px, "
          f"slack {budget - worst[1]:+d}")

    if len(CURSE_NEW) > 72:
        raise SystemExit(f"the new curse tip is {len(CURSE_NEW)} characters "
                         f"against verify's 72 (change 3)")
    print(f"  chars {len(CURSE_NEW)}/72   (change 3 raises verify's cap from "
          f"48; 57 > 48 either way)")

    if f'tip:"{CURSE_NEW}"' in s0 and f"{A.box} * k" in s0:
        raise SystemExit("this source already carries stage T -- built")

    s = one(s, f'tip:"{CURSE_OLD}"', f'tip:"{CURSE_NEW}"', "curse tip")
    s = one(s, TAG_OLD, TAG_NEW.replace("760", str(A.box), 1), "_tagFirst width")

    # THE CLAMP DEGENERATES QUIETLY. Printed, not asserted -- the brief's gate
    # for this is a photograph and the failure is already live at 596.
    print("\n  the box in ARENA units, and the margin the clamp has "
          "(A.w = 520):")
    for aw, lbl in ((1080, "1080-wide render"), (540, "540-wide short"),
                    (453, "the app at phone size")):
        for box in (596, A.box):
            wa = box * 520.0 / aw
            marg = 520 - wa - 6
            flag = "   <-- clamp degenerates, box runs off the right edge" \
                if marg < 6 else ""
            print(f"    {lbl:<22} box {box}: {wa:6.1f}u  margin "
                  f"{marg:7.1f}{flag}")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")

    print("\n  GATE T -- and the first one is the whole point of doing this "
          "stage first:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 8")
    print("      IDENTICAL on all 31, every match. Neither edit is read by")
    print("      the sim. If a bit moves, THAT is the finding and it stops")
    print("      the stage.")
    print(f"    python tip_audit.py --game {A.out}")
    print("      AFTER change 4. Expect tip-surface-v59 1.1 -- curse 475px,")
    print("      sunder 472, blessing 378 -- not what it prints today in the")
    print("      wrong typeface.")
    print(f"    python verify.py --game {A.out} --n 40")
    print("      AFTER change 3. 12/13; the thirteenth is the known one.")
    print("    LOOK AT ONE. Photograph a real first-application pop-up off a")
    print("      real match, at 1080x1920 AND at the app's phone size. The")
    print("      table above says the clamp is already degenerate at 540 and")
    print("      below, at the OLD width -- nobody has ever looked at that,")
    print("      and this change makes the box 28% wider.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
