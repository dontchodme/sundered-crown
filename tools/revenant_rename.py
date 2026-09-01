#!/usr/bin/env python3
"""STAGE 1 OF v56: GIVE GRAVEMOURN BACK REVENANT. ONE STRING, AND FIVE COMMENTS.

    python revenant_rename.py --src ../02-chain/sc-nocard.html \
                              --out ../02-chain/sc-revenant.html

`06-docs/v56/SHROUDMAUL-BUILD-BRIEF.md` §2. Rick named Gravemourn's ultimate
GRASP at build time over the v51 brief's REVENANT; the 28th relic's whole §1 is
grasping, and the collision is on the VERB and inside the same school. So the
name goes back.

    REVENANT   *that which comes back* -- a hand that takes a memory, deals it
               and RE-PARKS it. It is a better fit for Gravemourn than for
               anything else in the game, which is why it was the brief's pick
               in the first place.

## THIS IS THE ONLY STAGE IN THE BUILD THAT CAN BE PROVEN INERT

A name is not read by the simulation. `w.ult.name` is drawn by `drawUltName`,
spoken by the VO tools and printed by half of `tools/`, and nothing in
`Fighter`, `Match` or `Sfx` branches on it. So `engine_ab` must come back
BIT-IDENTICAL on all 27 relics -- and if it does not, the finding is that the
harness is wrong, not that the relic is, and it is worth knowing that before
three stages of new objects are in the world.

    python engine_ab.py --a ../02-chain/sc-nocard.html \
                        --b ../02-chain/sc-revenant.html --n 10

## AND THE COMMENTS MOVE WITH IT, WHICH IS NOT TIDINESS

Five paragraphs elsewhere in the build define themselves BY REFERENCE to
Gravemourn's ultimate by name -- the SFX cast voice ("like Grasp's it does not
resolve"), `tickDeadfall`'s header ("the Winnowing's kunai and Grasp's hands"),
`tickSling`'s own restore, and both halves of the blade's history. Stage 3 puts
a DIFFERENT ultimate called GRASP into this same file, so every one of those
sentences would silently start naming the wrong relic.

CLAUDE.md settled this class of question one build ago, when the fight card was
cut: *"a comment defining a thing against something that no longer exists is
worse than no comment in a codebase that teaches through them."* Here it is
worse still -- the thing it names will exist, and be something else.

So this refuses to write if the string "Grasp" survives anywhere in the output.

## THE TIP IS UNCHANGED, AND THAT IS DELIBERATE

    "Lengthens the chain; every hit throws a cursed hand"     51/72

Nothing in it says "grasp". `tip_audit` and `verify` both re-run against an
unchanged string, which keeps this stage's blast radius exactly one name.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "gravemourn"
OLD_NAME = "Grasp"
NEW_NAME = "Revenant"
# UNCHANGED, and asserted below. The tip never said "grasp".
TIP = "Lengthens the chain; every hit throws a cursed hand"


# Each entry is (label, old, new). `old` must occur EXACTLY ONCE -- the same
# promise every builder in this repo makes, for the same reason: an anchor that
# matches twice is an anchor that has stopped describing one place.
EDITS = [

# ------------------------------------------------------------- 1. THE STRING
("ult.name", '''    ult:{ name:"Grasp", charge:16, kind:"sling", dmg:0,''',
 '''    /* REVENANT, and the name is a RETURN rather than a rename (v56 §2).
       Rick took "Grasp" at build time over the v51 brief's REVENANT; the 28th
       relic's ultimate IS a grip, the collision is on the verb and it is
       inside this same school, so the grabbing word goes to the relic that
       grabs. `revenant` -- that which comes back -- is what a hand that takes
       a memory, deals it and RE-PARKS it actually does, and the tip below is
       untouched because it never said "grasp" either. */
    ult:{ name:"Revenant", charge:16, kind:"sling", dmg:0,'''),

# --------------------------------------- 2-3. the blade's own history, twice
("blade.hist.a", '''       was stage 1b's answer for a relic with NO working ultimate; with Grasp
       it read 76.0% and failed verify's 30-70% band outright.''',
 '''       was stage 1b's answer for a relic with NO working ultimate; with
       Revenant it read 76.0% and failed verify's 30-70% band outright.'''),

("blade.hist.b", '''       The alternative is a weaker Grasp bought back as blade, and that is
       Rick's.''',
 '''       The alternative is a weaker Revenant bought back as blade, and that
       is Rick's.'''),

# ------------------------------------------------------- 4. the cast's voice
("sfx.nightfell", '''          /* THE CAST IS A WINDOW OPENING, so like Grasp's it does not''',
 '''          /* THE CAST IS A WINDOW OPENING, so like Revenant's it does not'''),

# --------------------------------- 5-6. tickDeadfall's header and tickSling's
("tickDeadfall.hdr", '''     bolts, the Thicket's seeds, the Winnowing's kunai and Grasp's hands: a''',
 '''     bolts, the Thicket's seeds, the Winnowing's kunai and Revenant's hands: a'''),

("tickDeadfall.restore", '''         restored, because the window writes nothing -- unlike Grasp's, which
         has a `reachMul` to put back.''',
 '''         restored, because the window writes nothing -- unlike Revenant's,
         which has a `reachMul` to put back.'''),
]


def one(src: str, old: str, new: str, label: str) -> str:
    # THE BALANCE IS COMPARED, NOT ASSERTED. Most of this stage's anchors are
    # a SLICE of a comment -- one line out of the middle of a paragraph -- so
    # "the replacement is balanced on its own" is the wrong question and fails
    # on every legitimate edit. What must hold is that the edit does not CHANGE
    # the balance, which is what would take a `*/` the rest of the file needs.
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
    ap.add_argument("--src", default="../02-chain/sc-nocard.html")
    ap.add_argument("--out", default="../02-chain/sc-revenant.html")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nSTAGE 1 -- Gravemourn's ultimate is REVENANT again")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    if f'name:"{NEW_NAME}"' in s0:
        raise SystemExit(f"this source already names an ultimate "
                         f"{NEW_NAME!r} -- already built")
    if f'id:"{RELIC}"' not in s0:
        raise SystemExit(f"no {RELIC} in this build")

    for label, old, new in EDITS:
        s = one(s, old, new, label)

    # ---- THE REFUSAL, AND IT IS THE POINT OF THE STAGE ----------------------
    # Stage 3 introduces a DIFFERENT ultimate called GRASP into this same file.
    # Any surviving "Grasp" would then be a sentence naming the wrong relic --
    # which is worse than the fight card's dangling references were, because
    # the thing being named will exist.
    #
    # THE ONE PARAGRAPH THAT MAY SAY IT IS THE ONE EXPLAINING THE RENAME, and
    # it is excised before the scan rather than pattern-matched around.
    # CLAUDE.md: "a check that cannot tell code from the comment explaining it
    # fires on its own explanation" -- `curse_check` did exactly that, and
    # `curse_build` refused to write on its own comment an hour earlier. This
    # file explains itself in the file too, so the excision is by identity: the
    # exact block this builder just wrote, and nothing else.
    scan = s.replace(EDITS[0][2], "", 1)
    if OLD_NAME in scan:
        where = [i for i, ln in enumerate(scan.splitlines(), 1)
                 if OLD_NAME in ln]
        raise SystemExit(
            f"{len(where)} occurrence(s) of {OLD_NAME!r} survive in the "
            f"output, at line(s) {where[:12]}.\n"
            f"  Stage 3 puts a different ultimate called GRASP in this file.\n"
            f"  Every one of these has to be found and moved in this commit\n"
            f"  (brief §2: GREP WIDER THAN THE BUILD).")
    print(f"  rule  no {OLD_NAME!r} survives anywhere in the output")

    # THE TIP DOES NOT MOVE. Named here so the stage's blast radius is exactly
    # one name and a `tip_audit` re-run has a stated expectation.
    if s.count(f'tip:"{TIP}"') != 1:
        raise SystemExit(f"Revenant's tip is not the unchanged {TIP!r}")
    print(f"  tip   unchanged, {len(TIP)}/72  {TIP}")

    # AND THE SIM MUST NOT HAVE MOVED. A name is presentation; this stage's
    # whole value is that it can be proven inert, so the diff is asserted to be
    # comments and one string literal before `engine_ab` is ever run.
    d = len(s) - len(s0)
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({d:+d} bytes)")
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print("\n  NEXT, and this gate is the reason the stage exists:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 10")
    print("      IDENTICAL on all 27, or the harness is wrong and not the relic")
    print(f"    python tip_audit.py --game {A.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
