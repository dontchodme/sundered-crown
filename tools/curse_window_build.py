#!/usr/bin/env python
"""CURSE KEEPS THE LAST 3 HITS INSTEAD OF THE 3 BIGGEST. RICK'S RULING.

    python curse_window_build.py

`06-docs/v63/curse-window-v63.md` (Cowork, 2026-09-02) is the design and this
builder is nothing but its §1, applied. Rick proposed the change on 2026-09-01,
it was measured twice, and he ruled it in knowing what it costs Duskreave:
**"last-3 goes in; Scour lands at ~+40."**

THE WHOLE CHANGE IS ONE FUNCTION:

    push n copies, then DROP THE OLDEST until the length is 3
    -- instead of --
    push n copies, sort descending, truncate to 3

`curseSum`, `curseEcho`, `apply` (which derives the stack count from the pool's
length), the echo fold at `resolveHit`, the status tag that prints `curseSum()`,
Revenant's `cursePool.length = 0` and Deadfall's read-only `curseSum()` all keep
working untouched. **Rick's tooltip -- "Hits reflect 8% of the damage that
cursed, stacks 3 times" -- is still true under the window** and does not change.

ITS TIMING CONDITION IS MET. The design says "NOT UNTIL GLOAMWIRE IS IN A LINK",
and Gloamwire is in `sc-nova.html`, the build of record.

AND IT IS COWORK'S CLAIM, NOT THIS SESSION'S. `CLAIMS.md` has it as DESIGNED,
NOT TO LAND YET, gated on re-pricing the four built umbral relics. Rick asked
for it to land now so Duskreave's blade can be balanced against the rule the
game will actually have rather than against one that is on its way out. **The
re-pricing that gate asks for is still owed** and is printed at the end of every
run of this file.

WHAT IT IS NOT: a balance change dressed as a rule change. It is measured at
-2.6 / -4.6 / -4.0 / +0.0 on the four built umbral relics (v62 §13a-b) and at
roughly a quarter of Duskreave's damage, because `shift()` drops the OLDEST and
not the smallest -- so every tornado tick that applies curse trades one of the
scythe's 35-damage memories for a 5.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

OLD = """  pushCurse(v, n){
    for (let i = 0; i < n; i++) this.cursePool.push(v);
    this.cursePool.sort((a, b) => b - a);
    if (this.cursePool.length > STATUS.curse.maxStacks)
      this.cursePool.length = STATUS.curse.maxStacks;
  }"""

NEW = """  /* THE LAST THREE, NOT THE THREE BIGGEST. Rick's ruling, 2026-09-02;
     `06-docs/v63/curse-window-v63.md` is the design and this is the whole of
     it.

     The pool used to converge on the three biggest blows ever landed on this
     fighter and keep them for the whole fight (`dur` 99) -- so a curse pool
     was a fighter's WORST MOMENTS, permanently. It is now the three most
     recent blows whatever their size, which makes the echo a description of
     what is happening NOW rather than of what once happened.

     `shift()` DROPS THE OLDEST AND NOT THE SMALLEST, and that is the whole
     cost: every small application trades away a large memory. Measured, it
     takes about a quarter of Duskreave's damage -- each tornado tick that
     applies curse swaps one of the scythe's 35-damage memories for a 5 -- and
     Scour goes from +59.2pp to +40.5pp. Rick was shown that and ruled it in.

     NOTHING ELSE MOVES. `curseSum`, `curseEcho`, `apply` (which derives the
     stack count from this pool's length), the echo fold in `resolveHit`, the
     tag that prints `curseSum()`, Revenant's `cursePool.length = 0` and
     Deadfall's read-only `curseSum()` are all untouched, and Rick's tooltip --
     "stacks 3 times" -- is still true. */
  pushCurse(v, n){
    for (let i = 0; i < n; i++) this.cursePool.push(v);
    while (this.cursePool.length > STATUS.curse.maxStacks)
      this.cursePool.shift();
  }"""


def syntax_check(html: str, label: str) -> None:
    node = shutil.which("node")
    if not node:
        print("  WARN  no `node` on PATH -- output NOT syntax checked")
        return
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not "
                                 f"parse.\n  " + (r.stderr or "").strip())
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-scourvoice.html")
    ap.add_argument("--out", default="../02-chain/sc-lastthree.html")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    s0 = src_p.read_text(encoding="utf-8")

    print("\nCURSE -- THE LAST 3, NOT THE 3 BIGGEST  (Rick's ruling, v63)")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    # THE TIMING CONDITION IS PART OF THE RULING, so it is checked rather than
    # remembered: "NOT UNTIL GLOAMWIRE IS IN A LINK."
    if 'id:"gloamwire"' not in s0:
        raise SystemExit(
            "the design's timing condition is not met -- Gloamwire is not in\n"
            "  this link, and the ruling says the window lands after it ships.")
    if "cursePool.shift()" in s0:
        raise SystemExit("this source already has the window -- built")
    if s0.count(OLD) != 1:
        raise SystemExit(
            "`pushCurse` is not the shipped three-biggest rule in this "
            "source.\n  Do not weaken the anchor -- find out what changed, "
            "because this\n  function is read by five relics and by the whole "
            "curse school.")

    s = s0.replace(OLD, NEW, 1)

    # AND THE REST OF THE SCHOOL IS UNTOUCHED, ASSERTED. The design's own list
    # of what must keep working, checked against the file rather than trusted.
    for must in ("curseSum(){", "curseEcho(){", "foe.pushCurse(dmgBase",
                 "cursePool.length = 0"):
        if must not in s:
            raise SystemExit(f"`{must}` is gone after the edit -- the change "
                             f"was supposed to be one function")
    if s.count("cursePool.sort(") != 0:
        raise SystemExit("a `cursePool.sort` survives -- the pool is still "
                         "being ordered by size somewhere")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8")
    print(f"  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"  ({len(s) - len(s0):+d} bytes)")

    print("\n  THE GATE, and the first one is not optional:")
    print("    python engine_ab.py --a %s \\" % A.src)
    print("      --b %s --ids <the NON-CURSE relics> --n 8" % A.out)
    print("      IDENTICAL. No relic that never applies curse can move --")
    print("      `pushCurse` is only ever called from an `onHit:{curse:n}` or")
    print("      from Revenant's hands, so a diff outside umbral means this")
    print("      touched something it was not supposed to.")
    print("    AND NOT identical on the umbral pairings. That is the POINT --")
    print("      an A/B that came back green there would mean the rule did")
    print("      not land.")
    print("\n  STILL OWED, and it is the gate `CLAIMS.md` put on this change:")
    print("    RE-PRICE THE FOUR BUILT UMBRAL RELICS. Measured at")
    print("    -2.6 / -4.6 / -4.0 / +0.0 (Gravemourn, Nightfell, Twinshade,")
    print("    Shroudmaul) on 320-350 fights an arm -- which is well under the")
    print("    n~700 floor this roster needs, so those four numbers are a")
    print("    direction and not a measurement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
