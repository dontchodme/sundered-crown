#!/usr/bin/env python
"""THE BATCH'S BALANCE PASS (v117) -- one link at the batch line's tip that moves blades and nothing else.

    python balance_build.py --src ../02-chain/<tip>.html --out ../02-chain/sc-balance.html

Rick, 2026-09-29: "you pick the blades. do whatevers best for balance." Each batch relic's blade goes
to the measured point nearest 50% BOTH SIDES on the roster the game will carry (the batch tip with
yert's staves carried onto it), measured by `balance_sweep.py` (relic_rate, two seed blocks, pooled).
The numbers live HERE and nowhere else: BLADES maps a relic id to (the blade the tip carries, the
blade this link writes, the measurement it came from). Every other relic's row is untouched.

  - each relic's row is found by `{ id:"<id>",`; its FIRST `dmg:` must read the table's old value
    exactly, or the builder refuses (a tip that moved under the table);
  - that one number is replaced, with a comment saying where it came from;
  - nothing else in the page may change (checked line by line), the page must parse, and a link is
    written once.
"""
from __future__ import annotations
import argparse, difflib, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from staffkit import syntax_check

# id: (the tip's blade, this link's blade, the measurement) -- filled from the v117 sweep, §2 of the doc
BLADES: dict[str, tuple[float, float, str]] = {
    "axiom": (7.42, 9.0, "50.5% both sides on the 49-relic roster, round 2 (was 37.7% at 7.42)"),
    "morningstar": (24.03, 25.75, "49.7% both sides on the 49-relic roster, round 2 (was 46.0% at 24.03)"),
    "bindweed": (18.0, 19.0, "50.7% both sides on the 49-relic roster, round 2 (was 46.0% at 18)"),
    "ironhail": (16.23, 14.75, "50.2% both sides on the 49-relic roster, round 2 (was 59.1% at 16.23)"),
    "lodestone": (20.5, 20.25, "51.0% both sides on the 49-relic roster, round 2 (was 52.2% at 20.5)"),
    "widowmaker": (10.75, 11.25, "50.5% both sides on the 49-relic roster, round 2 (was 45.8% at 10.75)"),
    "censer": (25.5, 26.0, "50.4% both sides on the 49-relic roster, round 2 (was 47.4% at 25.5)"),
    "aureole": (12.5, 12.0, "49.5% both sides on the 49-relic roster, round 2 (was 53.5% at 12.5)"),
    "spellbreaker": (7.5, 7.25, "50.8% both sides on the 49-relic roster, round 2 (was 53.1% at 7.5)"),
    "heartwood": (11.0, 10.5, "50.2% both sides on the 49-relic roster, round 2 (was 53.6% at 11)"),
    "oathwound": (10.25, 9.75, "48.8% both sides on the 49-relic roster, round 2 (was 52.6% at 10.25)"),
}


def fmt(x: float) -> str:
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    src, out = (HERE / A.src).resolve(), (HERE / A.out).resolve()
    if not out.name.startswith("sc-balance"):
        raise SystemExit(f"refusing {out.name}: this builder's links are sc-balance*")
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out.name} -- a link is written once")
    if not BLADES:
        raise SystemExit("BLADES is empty -- nothing to write")
    s0 = src.read_text(encoding="utf-8")
    s = s0
    print(f"\nTHE BALANCE PASS (v117) -- src {src.name} {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    for rid, (old, new, why) in BLADES.items():
        m = re.search(r'\{ id:"' + re.escape(rid) + r'",', s)
        if not m or len(re.findall(r'\{ id:"' + re.escape(rid) + r'",', s)) != 1:
            raise SystemExit(f"{rid}: not exactly one row in the source")
        d = re.compile(r"\bdmg:([0-9.]+)").search(s, m.end())
        nxt = s.find('{ id:"', m.end())
        if not d or (nxt != -1 and d.start() > nxt):
            raise SystemExit(f"{rid}: no dmg in its own row")
        if float(d.group(1)) != old:
            raise SystemExit(f"{rid}: the tip's blade is {d.group(1)}, the table says {old} -- the tip moved")
        rep = f"dmg:{fmt(new)} /* v117 balance, was {fmt(old)}: {why} */"
        s = s[:d.start()] + rep + s[d.end():]
        print(f"  {rid:<13} {fmt(old):>7} -> {fmt(new):<7}  {why}")
    gone, came = [], []
    for op in difflib.unified_diff(s0.split("\n"), s.split("\n"), n=0, lineterm=""):
        if op.startswith(("---", "+++", "@@")):
            continue
        (gone if op[0] == "-" else came).append(op[1:])
    if len(gone) != len(BLADES) or len(came) != len(BLADES) or any("dmg:" not in l for l in gone + came):
        raise SystemExit("REFUSING TO WRITE -- something other than the blades' lines moved")
    syntax_check(s, out.name)
    out.write_text(s, encoding="utf-8", newline="\n")
    print(f"  out {out.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}  ({len(BLADES)} blades)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
