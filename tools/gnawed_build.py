#!/usr/bin/env python3
"""THE UMBRAL WARHAMMER, REDRAWN. `_whEaten` OUT, `_whGnawed` IN.

    python gnawed_build.py --src ../02-chain/sc-grasp.html \
                           --out ../02-chain/sc-gnawed.html

`06-docs/v58/umbral-hammer-v58.md`. Rick, on the shipped silhouette:

    "umbral hammers silhouette looks pretty bad. can we take another stab at
     its design? the hammer with blocks attached to it idea just isnt working
     for me"

and on the first cut of the replacement:

    "upclose the spikes just look like triangles layered behind the hammer.
     can we make them look truly attached?"

## THIS IS ART ONLY, AND THAT IS THE CHEAPEST PROOF THIS PROJECT HAS

`SHAPES` is render-only. Nothing in `Fighter`, `Match` or `Sfx` reads it, so
`engine_ab` must come back BIT-IDENTICAL on all 28 relics -- and if a single
bit moves, THAT is the finding and it stops the stage. It is the same argument
stage 1 of v56 made for a name, one layer down.

## WHY THE OLD ONE FAILED, AND IT IS THE GRAMMAR AND NOT THE FUNCTION

`_whEaten` was purely SUBTRACTIVE: call `_whBase`, then punch two blobs and a
haft slot out of it with `destination-out`. **Subtracting from a shape that is
already rectilinear does not produce an absence, it produces smaller
rectangles** -- the haft came apart into two bars with a gap, the head into
lumps, and the two wisps drawn afterwards read as detached shards. A stick, a
gap, a stick and some blocks, which is precisely what Rick saw.

Every other grammar on this row ADDS a contour -- a halo, thorns, hooks, a
burl, plates, langets, a floating cluster. Umbral was the only one that removed
one, and **removal is the weakest silhouette operation there is**: it takes
area without giving the outline a new event, and at phone size the holes close
under the bloom and the mask reverts toward the base hammer.

## AND THE NUMBER NEVER SAW ANY OF IT

`_whEaten` scores 0.382 IoU against its nearest sibling -- inside the band the
silhouette doc calls "distinct, and still recognisably one weapon type". **By
the metric it was fine. It was not fine.** The replacement is a LATERAL move on
that metric (worst case 0.382 -> 0.335, mean 0.505 -> 0.569) and is justified by
the sheet and by Rick. A number that is easy to compute is not thereby the
number you want.

## THE ONE RULE THAT MADE IT WORK

    A grammar that adds a limb to a type must add it to the type's OUTLINE,
    not behind it.

Head, spikes, beak and spur are ONE CLOSED PATH -- one fill, one stroke, no
internal edges. A spike that shares the head's outline cannot come apart from
it at any zoom. This builder ASSERTS it: `path(` must be called exactly three
times (fill, clip, stroke) and there must be no second `stroke()`.

## THE FUNCTION IS READ FROM `06-docs/v58/sc_wh_gnawed.js`, NOT PASTED HERE

One copy, the way `fx_build.py` inlines `src/render/fx.js`. A shape that exists
in two places is a shape that drifts, and this row has six siblings to drift
against.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

SRC_JS = HERE.parent / "06-docs" / "v58" / "sc_wh_gnawed.js"

DISPATCH_OLD = '    if (key === "umbral")     return SHAPES._whEaten(c, L, W, p);'
DISPATCH_NEW = '    if (key === "umbral")     return SHAPES._whGnawed(c, L, W, p);'

# ---- THE EXCISION. `_whEaten` and the comment that introduces it come out
# WHOLE, in the same commit, and not behind a flag: git has it, and a second
# umbral hammer left in the file is how a dispatcher gets repointed by accident
# later. Bounded, and it refuses on anything it does not recognise -- the same
# promise `one()` makes, which is what `nightfell_build`'s Eclipse cut
# established.
# The banner is matched by its ENDING, not by a dash count -- the four
# `UMBRAL --` banners in SHAPES are not all the same width and a
# hardcoded rule is a thing that breaks on a reflow.
CUT_HEAD = "UMBRAL --"
CUT_TAIL = "  _whRadiant(c, L, W, p){"

# ---- THE CLAIM THAT SENT v56 THE WRONG WAY -------------------------------
# `SHROUDMAUL-BUILD-BRIEF.md` §3.2 said "`_whEaten` ALREADY EXISTS ... THE
# SILHOUETTE IS NOT NEW WORK", the build write-up repeated it, and the shipped
# relic carries it as a comment. The v58 doc's first line is that this is now
# the wrong call, so the paragraph is CORRECTED rather than merely repointed --
# and the correction carries WHY, because the 78.6% is the part that made it
# sound settled.
EATEN_CLAIM_OLD = '''     already routes `umbral` to `_whEaten`, so the silhouette is not new work:
     it exists, it is 78.6% distinct from its nearest sibling and it was the
     3rd most distinct of the fifteen open cells.'''
EATEN_CLAIM_NEW = '''     routes `umbral` to `_whGnawed` — a near-black head carrying three bone
     spikes above and three below, a beak forward and a spur back, ALL ON ONE
     CLOSED PATH.

     AND THE SILHOUETTE WAS CALLED FREE, WHICH WAS WRONG. This relic shipped on
     the eaten hammer because the brief said the shape already existed and was
     "78.6% distinct from its nearest sibling". Rick: "umbral hammers silhouette looks
     pretty bad ... the hammer with blocks attached to it idea just isnt
     working for me." The number was fine and the shape was not — the old cell
     also scores 0.382 IoU against its nearest sibling, inside the band the
     silhouette doc calls distinct. A NUMBER THAT IS EASY TO COMPUTE IS NOT
     THEREBY THE NUMBER YOU WANT, and the replacement is a LATERAL move on that
     metric (worst case 0.382 -> 0.335, mean 0.505 -> 0.569). It is justified
     by the sheet and by Rick. See `06-docs/v58/`.'''

# ---- AND `_scEaten` POINTED AT IT FOR THE SHARED TECHNIQUE ---------------
# The note is still true and still worth having; it just cannot name a function
# that is gone. `_gsEaten` and `_tbEaten` are the surviving users.
SCEATEN_OLD = '''    /* shared path — see _whEaten: destination-out removes the glow too, so an
       un-rimmed bite is a hard black hole in the picture. */'''
SCEATEN_NEW = '''    /* shared path — see `_gsEaten` and `_tbEaten`, which do the same thing:
       destination-out removes the GLOW as well as the metal, so an un-rimmed
       bite is a hard black hole in the picture.

       THE WARHAMMER USED TO BE ONE OF THESE AND IS NOT ANY MORE. Rick rejected
       it (`06-docs/v58/`) and `_whGnawed` ADDS a contour rather than removing
       one — and the reason the hammer left applies to all of them:
       subtracting from a shape that is already rectilinear produces smaller
       rectangles rather than an absence. Nobody has complained about these.

       AND THE BITES ERASE WHATEVER IS BEHIND THEM, WHICH IS LATENT AND NOT
       LIVE. Measured: painted onto an OPAQUE background these punch 4877,
       4132 and 560 pixels straight through it. The shipped path is safe only
       because `litWeapon` bakes every weapon onto its own TRANSPARENT scratch
       first, where `destination-out` can reach nothing but the weapon. The one
       path that skips that buffer — `litWeapon` declining, which it does for
       21 of 126 shape x school combinations — is the FLAIL, every time, and no
       flail school is eaten. That is an accident of which shapes need a
       buffer, not a design. */'''


def one(src: str, old: str, new: str, label: str) -> str:
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def cut_eaten(s: str) -> tuple[str, int]:
    """Take `_whEaten` and its header comment out, and refuse if unsure."""
    tail = s.index(CUT_TAIL)
    # the LAST umbral header before _whRadiant -- there are several `UMBRAL --`
    # banners in SHAPES, one per type, so the index is taken backwards from the
    # thing that follows rather than forwards from the file.
    at = s.rindex(CUT_HEAD, 0, tail)
    head = s.rindex("  /* ", 0, at)
    span = s[head:tail]
    # 6758 on the build this was written against: `_whEaten` is 81 lines
    # and most of them are its header. The bound is a sanity rail, and
    # the content assertions below it are the real refusal.
    if not (1200 < len(span) < 9000):
        raise SystemExit(f"THE CUT is {len(span)} characters and nothing that "
                         f"size is the block this removes. Refusing.")
    for must in ("_whEaten(c, L, W, p){", "destination-out", "bitePath",
                 "SHAPES._whBase(c, L, W, p);"):
        if must not in span:
            raise SystemExit(f"THE CUT does not contain {must!r}. Refusing.")
    if "_whRadiant" in span or "_whPlated" in span:
        raise SystemExit("THE CUT reaches into a sibling grammar. Refusing.")
    if span.count("/*") != span.count("*/"):
        raise SystemExit("THE CUT's comments are unbalanced, so it would take "
                         "a `*/` the rest of the file needs.")
    return s[:head] + s[tail:], len(span)


def check_shape(raw: str) -> None:
    """§2.1 and §3 of the v58 doc, asserted on the text rather than trusted.

    COMMENTS ARE STRIPPED FIRST, AS A BLOCK. This function's own header says
    "there is no `destination-out` in this function at all", so the first cut
    of this check refused to write on the sentence promising the thing it was
    checking for. That is CLAUDE.md's "a check that cannot tell code from the
    comment explaining it fires on its own explanation" -- `curse_check` and
    `curse_build` each did it once, and this repo's line-by-line strippers are
    not enough because a block comment's INTERIOR is plain indented prose.
    """
    js = re.sub(r"/\*[\s\S]*?\*/", "", raw)
    js = re.sub(r"//[^\n]*", "", js)
    if "destination-out" in js:
        raise SystemExit(
            "`_whGnawed` contains `destination-out`. The whole point of the "
            "replacement is\n  that the grammar ADDS a contour instead of "
            "removing one -- and the old bites\n  punch through an opaque "
            "background (1378px, measured). Refusing.")
    if "_whBase" in js:
        raise SystemExit(
            "`_whGnawed` calls `_whBase`. It is a whole shape, not a "
            "decoration on one:\n  drawing the base first is what put an "
            "outline behind the spikes.")
    # THE ONE RULE. Head, spikes, beak and spur are ONE closed path: one fill,
    # one clip, one stroke, and no second `stroke()` anywhere. Rick rejected
    # the first cut precisely because each spike carried its own outline.
    if js.count("path(c)") != 3:
        raise SystemExit(
            f"`_whGnawed` calls `path(c)` {js.count('path(c)')} times and it "
            f"must be exactly 3\n  (fill, clip, stroke). One closed path is "
            f"the rule that made this work:\n  a spike that shares the head's "
            f"outline cannot come apart from it at any zoom.")
    if js.count("c.stroke()") != 1:
        raise SystemExit(
            f"`_whGnawed` strokes {js.count('c.stroke()')} times. ONE stroke, "
            f"on the one path --\n  Rick, on the first cut: \"upclose the "
            f"spikes just look like triangles layered\n  behind the hammer.\"")
    # §3: NOTHING IS DRAWN PAST `x = L`, or the weapon lies about `reach`.
    if "lineTo(L, 0)" not in js:
        raise SystemExit("`_whGnawed`'s beak does not land on `L`.")
    print("  rule  one closed path, one stroke, no destination-out, "
          "nothing past x = L")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-grasp.html")
    ap.add_argument("--out", default="../02-chain/sc-gnawed.html")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    if not SRC_JS.exists():
        raise SystemExit(f"no shape at {SRC_JS} -- this builder does not carry "
                         f"its own copy on purpose")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    js = SRC_JS.read_text(encoding="utf-8").rstrip("\n")
    print("\nTHE UMBRAL WARHAMMER — `_whEaten` out, `_whGnawed` in")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    print(f"  fn  {SRC_JS.relative_to(HERE.parent)}  "
          f"{len(js.splitlines())} lines  "
          f"{hashlib.sha256(js.encode()).hexdigest()[:16]}")

    if "_whGnawed" in s0:
        raise SystemExit("this source already has _whGnawed -- already built")
    if "_whEaten" not in s0:
        raise SystemExit("this source has no _whEaten to replace")

    check_shape(js)

    # THE DISPATCH FIRST, so a failure here leaves the old shape in place and
    # reachable rather than orphaning it.
    s = one(s, DISPATCH_OLD, DISPATCH_NEW, "warhammer dispatch")

    # THE CUT COMES BEFORE THE INSERT, and the order is load-bearing. Both
    # blocks open with an `UMBRAL --` banner and both sit immediately before
    # `_whRadiant`, so inserting first makes the excision's backwards search
    # find the NEW function's header and try to remove the shape it has just
    # added. It refused, correctly, on a content assertion -- which is what
    # those are for, and it is why the bound alone would not have saved it.
    # ---- AND THE TWO SENTENCES THAT NAME IT MOVE IN THE SAME COMMIT ------
    # Same rule as v56's Revenant rename: a comment defining a thing against
    # something that no longer exists is worse than no comment in a codebase
    # that teaches through them. One of these is worse than dangling — it is
    # the paragraph that told the last build the silhouette was free.
    s = one(s, EATEN_CLAIM_OLD, EATEN_CLAIM_NEW, "the free-silhouette claim")
    s = one(s, SCEATEN_OLD, SCEATEN_NEW, "_scEaten's shared-path note")

    s, n = cut_eaten(s)

    # THE NEW SHAPE, exactly where the old one stood -- immediately before
    # `_whRadiant`, so the file keeps the row's reading order.
    s = one(s, CUT_TAIL, js.rstrip() + "\n\n" + CUT_TAIL, "_whGnawed")
    print(f"  cut   `_whEaten` and its header, {n} characters "
          f"({s0.count(chr(10)) - s.count(chr(10)) + len(js.splitlines()) + 1} "
          f"lines net)")

    # AND IT IS GONE, not merely unreachable. A second umbral hammer left in
    # the file is how a dispatcher gets repointed by accident later.
    # THE ONE PLACE THAT MAY STILL SAY IT IS THE FUNCTION THAT REPLACED IT,
    # and it is excised by IDENTITY rather than pattern-matched around.
    # `_whGnawed`'s own header opens "Replaces `_whEaten`, on Rick's rejection
    # of it" and then spends a paragraph on why the grammar failed -- which is
    # the most valuable comment in the block and exactly what this scan would
    # otherwise delete. `revenant_rename.py` hit the same wall and took the
    # same way out; CLAUDE.md has now recorded this failure four times.
    scan = s.replace(js.rstrip(), "", 1)
    if "_whEaten" in scan:
        where = [i for i, ln in enumerate(scan.splitlines(), 1)
                 if "_whEaten" in ln]
        raise SystemExit(
            f"`_whEaten` survives at line(s) {where[:8]} outside the function "
            f"that replaced it.\n  It is dead code on this row and the doc "
            f"asks for it to go in the same commit.")
    print("  rule  no `_whEaten` survives anywhere in the output")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} bytes)")
    print("\n  NEXT, and the first one is the whole argument that this is art:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 8   # ALL 28")
    print(f"    python silhouette_probe.py --sheet --game {A.out}")
    print(f"    python cinema_clip.py --game {A.out} --a shroudmaul "
          f"--b emberedge --seed 12345 --full   # FILM IT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
