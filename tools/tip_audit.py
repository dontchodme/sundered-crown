#!/usr/bin/env python3
"""DOES EACH TIP DESCRIBE WHAT ITS STATUS ACTUALLY DOES?

    python3 tip_audit.py --game sc-gs7-ults.html

Rick misread Hex from its own tip — `Stuns the weapon 0.2s, faster per stack`
and concluded the stun DURATION scaled with stacks. It does not; the frequency
does. He is the person who wrote the wording convention, and if the line misled
him it will mislead a first-time viewer, who gets one line and no source code.

So the tip was the defect, not the reading. This asks the same question of every
other tip mechanically: put each status's REAL data fields next to the line that
is supposed to describe them, and flag every number the code uses that the tip
never mentions.

WHAT IT CANNOT DO
-----------------
It cannot tell you a tip is misleading — only that a tip is INCOMPLETE, by
finding effect fields with no number in the text. Hex's original line would pass
that test: it contains 0.2, and `stunFor` is 0.2. The thing that made it wrong
was an adverb attached to the wrong noun, and no checker catches that. Read the
"reads as" column and argue with it; that is the part that needs a person.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

# What each effect field MEANS, and what a viewer must be told about it.
# `unit` is how the number should appear in a tip if it appears at all.
FIELDS = {
    "dps":       ("damage per second, per stack", "1.5"),
    "spin":      ("swing-speed change, per stack", "13%"),
    "move":      ("MOVEMENT-speed change, per stack", "6%"),
    "taken":     ("damage-taken increase, per stack", "11%"),
    "stunFor":   ("stun DURATION — flat, does not scale", "0.2s"),
    "stunEvery": ("stun INTERVAL — divided by stacks, so more stacks = more often", "1.15s"),
    "maxHpLoss": ("maximum-hp removed, per stack", "13"),
    "bank":      ("share of damage dealt that becomes shield", "55%"),
    "cap":       ("shield ceiling", "90"),
    "shatter":   ("share of the pool released on a break", "40%"),
    "knock":     ("knockback on a break", "210"),
    "dur":       ("how long it lasts", ""),
    "maxStacks": ("stack ceiling", ""),
}
# Fields a tip is not obliged to mention: structural, or already printed
# elsewhere on the card (the stack count is on the ON HIT line).
EXEMPT = {"maxStacks", "dur", "knock", "cap"}

# Fields DELIBERATELY left out of a specific tip, with the reason. These are not
# oversights and putting the number in would make the line WRONG — which is a
# worse failure than leaving it incomplete. Recorded here so the next pass over
# the wording does not "fix" them.
JUSTIFIED = {
    ("hex", "stunEvery"):
        "1.15s is the interval at ONE stack; the clock is advanced by dt*stacks, "
        "so the real interval is 1.15/n. Printing 'every 1.15s' would be true only "
        "for the first stack and wrong for every other. 'more often per stack' "
        "carries the direction without a number that expires.",
    ("ward", "bank"):
        "0.55 is scaled by the relic's own onSelf.ward value — resolveHit does "
        "`dmg * W.bank * n`, and n is 1 on Lightkeeper but 2.5 on Farwarden. "
        "STATUS tips are SHARED across every relic carrying the status, so a "
        "flat '55%' here would be correct for one relic and wrong for the other.",
}

EXTRACT = """async () => {
  // THE FACE THE BOX IS ACTUALLY DRAWN IN, AND IT IS NOT THE PANEL'S.
  // `_tagFirst` -- the pop-up the first time a status lands in a fight -- draws
  // `500 25px 'Atkinson Hyperlegible Next'`, one line, no wrap, no clip and no
  // measurement, so a tip wider than its box just draws out into the hall. This
  // tool used to set "500 25px ui-sans-serif,system-ui,sans-serif", which is
  // right for the PANEL and wrong for the surface that can overflow: the same
  // string measures 475px in the bundled face, 414 in Segoe UI (Rick's PC) and
  // 526 in DejaVu (a Linux container). So the gate had 61px of imaginary
  // headroom on the machine that matters. The bundled face is embedded in the
  // build as a data URI, so measuring in it is machine-independent -- this is
  // not a trade-off, it is strictly better. tip-surface-v59 section 1.2.
  const FACE = "500 25px 'Atkinson Hyperlegible Next'";
  await document.fonts.load(FACE);
  await document.fonts.ready;
  const c = document.createElement('canvas').getContext('2d');
  c.font = FACE;
  // AND THE FALLBACK IS THE FAILURE MODE. If the face did not load, canvas
  // silently measures whatever the browser substitutes and this tool is wrong
  // again in a new way, with every number looking plausible. Report it and let
  // the caller refuse.
  const loaded = document.fonts.check(FACE);
  const out = [];
  for (const k in AC.STATUS){
    const s = AC.STATUS[k];
    const fields = {};
    for (const f in s) if (f !== 'name' && f !== 'tip') fields[f] = s[f];
    out.push({ key:k, name:s.name, tip:s.tip, fields, loaded,
               len:s.tip.length, px:Math.round(c.measureText(s.tip).width) });
  }
  return out;
}"""


TAG_BOX = re.compile(r"_tagFirst[\s\S]{0,4000}?const w = (\d+) \* k")


def tag_budget(src: str) -> tuple[int, int]:
    """The reminder box's width and its TEXT budget, read out of the build.

    Not a literal. The 536 this tool carried was `596 - 2 * 30` written down by
    hand, and stage T of the Bloodmirror brief moves the box to 760 -- a gate
    with the old constant baked in would have gone on reporting overflows that
    had been fixed, or worse, passing a build whose box had been narrowed.
    """
    m = TAG_BOX.search(src)
    if not m:
        raise SystemExit(
            """cannot find `_tagFirst`'s box width in this build.
  This tool measures the ONE-LINE, NO-WRAP, NO-CLIP reminder -- the only
  tip surface that can overflow -- and it reads the box out of the source
  rather than assuming it. Do not fall back to a literal: find out what
  moved.""")
    w = int(m.group(1))
    return w, w - 60          # 30px text inset each side


def mentions(tip: str, key: str, val) -> bool:
    """Is this field's number present in the tip in any plausible rendering?"""
    t = tip.lower()
    cands = set()
    try:
        v = float(val)
    except (TypeError, ValueError):
        return True
    cands.add(f"{v:g}")
    if abs(v) < 1:                     # 0.13 -> "13%"
        cands.add(f"{abs(v) * 100:g}")
    cands.add(f"{abs(v):g}")
    return any(re.search(r"(?<![\d.])" + re.escape(c) + r"(?![\d])", t) for c in cands)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="sc-gs7-ults.html")
    A = ap.parse_args()

    g = HERE / A.game
    if not g.exists():
        sys.exit(f"no such build: {g}")

    # THE BUDGET COMES OUT OF THE BUILD, NOT OUT OF THIS FILE.
    # tip-surface-v59 change 4.
    box, budget = tag_budget(g.read_text(encoding="utf-8"))

    with game(game_path=g.resolve()) as (page, errors):
        rows = page.evaluate(EXTRACT)
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    # AND IF THE FACE DID NOT LOAD, EVERY WIDTH BELOW IS A SUBSTITUTE'S.
    if rows and not rows[0]["loaded"]:
        sys.exit(
            """REFUSING TO REPORT -- 'Atkinson Hyperlegible Next' did not
  load in this page, so every width below belongs to some substitute face
  and this tool is wrong again in a new way. That is the defect change 4
  exists to remove.""")

    print(f"STATUS TIPS -- {A.game}")
    print("  the surface is `_tagFirst`, the first-application reminder: "
          "ONE line, 25px,")
    print(f"  no wrap, no clip, no measurement. Box {box}px, text budget "
          f"{budget}px, in")
    print("  the BUNDLED 'Atkinson Hyperlegible Next'. The scrunch panel "
          "wraps to three")
    print("  lines, shrinks, and is not the gate.")
    print()
    gaps = 0
    for r in rows:
        fit = "" if r["px"] <= budget else "  <-- OVER THE BOX, DRAWS INTO THE HALL"
        print(f"  {r['name']:<11} {r['len']:>3}ch {r['px']:>4}px  \"{r['tip']}\"{fit}")
        for f, v in r["fields"].items():
            if f in EXEMPT:
                continue
            meaning, want = FIELDS.get(f, (f, ""))
            if not mentions(r["tip"], f, v):
                why = JUSTIFIED.get((r["key"], f))
                if why:
                    print(f"      omitted  {f} = {v}   BY DESIGN")
                    for line in __import__("textwrap").wrap(why, 68):
                        print(f"                 {line}")
                    continue
                gaps += 1
                print(f"      MISSING  {f} = {v}   ({meaning})"
                      + (f"   should read ~{want}" if want else ""))
        print()

    print(f"  {gaps} effect fields the tips never mention.\n")
    print("  Remember what this cannot see: Hex's OLD tip contained 0.2 and would")
    print("  have passed clean. 'faster per stack' was a true word attached to the")
    print("  wrong noun. Completeness is checkable; clarity is not.")


if __name__ == "__main__":
    main()
