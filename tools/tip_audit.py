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

EXTRACT = """() => {
  const c = document.createElement('canvas').getContext('2d');
  // THE PANEL'S OWN FONT STRING, copied from intro_probe [6]. A previous
  // version of this tool used a 400-weight -apple-system stack and measured
  // every tip ~13% narrow, which invented 80px of headroom that did not exist
  // and passed four tips that overflow. If two tools measure the same thing,
  // they have to measure it the same way.
  c.font = "500 25px ui-sans-serif,system-ui,sans-serif";
  const out = [];
  for (const k in AC.STATUS){
    const s = AC.STATUS[k];
    const fields = {};
    for (const f in s) if (f !== 'name' && f !== 'tip') fields[f] = s[f];
    out.push({ key:k, name:s.name, tip:s.tip, fields,
               len:s.tip.length, px:Math.round(c.measureText(s.tip).width) });
  }
  return out;
}"""


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
    ap.add_argument("--panel-px", type=int, default=536,
                    help="the in-arena explainer panel's width — the REAL constraint")
    A = ap.parse_args()

    g = HERE / A.game
    if not g.exists():
        sys.exit(f"no such build: {g}")
    with game(game_path=g.resolve()) as (page, errors):
        rows = page.evaluate(EXTRACT)
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    print(f"STATUS TIPS — {A.game}   panel limit {A.panel_px}px at 25px\n")
    gaps = 0
    for r in rows:
        fit = "" if r["px"] <= A.panel_px else "  <-- OVER PANEL"
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
