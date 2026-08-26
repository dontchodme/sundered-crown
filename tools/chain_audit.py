#!/usr/bin/env python3
"""DID EVERY EDIT SURVIVE THE CHAIN?

    python3 chain_audit.py --relic ../02-chain/sc-twinshade.html \
                           --tip   ../02-chain/sc-twinshade-scrunch.html

A relic is built into `sc-health18.html` and then carried up through
`liquid_build.py` and `scrunch_build.py`. THOSE BUILDERS REPLACE SPANS, NOT
LINES, and a span can contain an edit the relic builder made:

    liquid_build.py, "slosh hook":
      replace_span(s, "      if (f.hp >= f.hpGhost) f.hpGhost = f.hp;",
                      "  }\\n\\n  decayImpactOnly(dt){", SLOSH_HOOK + ...)

That replaces the ENTIRE TAIL of `tickPresentation`. Twinshade's drain clock was
inserted in it. The result: the relic build was correct, the build of record was
not, the drain never advanced past u <= 0 so `drawDrains` skipped every strand,
and the effect did not render in the file anyone watched. Nothing failed.
`twinshade_probe` reported 54/54 on the broken build because every check it had
asked whether motes were SPAWNED, and spawning was never what broke.

Four rounds of art revision were spent on an effect that was not on screen.

This is the cheap, general guard: take every marker the relic builder inserts,
and assert it is still present at the tip. It cannot catch an edit that is
present but neutered — [12e] in twinshade_probe is what covers that — but it
catches the whole class of "a downstream builder ate it", in one second, for
every relic from here on.
"""
from __future__ import annotations
import argparse, pathlib, re, sys

HERE = pathlib.Path(__file__).parent

def markers_from_builder(builder: pathlib.Path) -> list[tuple[str, str]]:
    """Pull the anchors a relic builder inserts, straight out of its own source.

    Hand-maintaining a marker list beside a builder means the list rots the
    first time the builder changes and nobody notices — which is the same
    failure mode one level up. The `*_NEW` constants ARE the record of what was
    inserted, so they are what gets read.
    """
    src = builder.read_text(encoding="utf-8")
    out = []
    # `[rRbBfF]*` because a builder is free to write `r'''...'''`, and one did:
    # v43's inserts are raw strings and this tool reported "no *_NEW inserts
    # found" -- which is the right message for the wrong reason, and would have
    # been read as "the audit passed with nothing to say" by anyone in a hurry.
    for m in re.finditer(r'(?m)^([A-Z_0-9]+_NEW)\s*=\s*(?:[A-Z_0-9]+\s*\+\s*)?'
                         r'[rRbBfF]*(?:"""|\'\'\')(.*?)(?:"""|\'\'\')', src, re.S):
        name, body = m.group(1), m.group(2)
        # the most distinctive line the insert adds: longest non-comment,
        # non-blank line that is not pure punctuation
        cands = [l.strip() for l in body.splitlines()]
        cands = [l for l in cands
                 if len(l) > 18 and not l.startswith(("/*", "*", "//"))
                 and not l.strip("{}(); ") == ""]
        if cands:
            out.append((name, max(cands, key=len)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--relic", required=True, help="the relic build")
    ap.add_argument("--tip", required=True, help="the build of record")
    ap.add_argument("--mid", default=None, help="an intermediate, e.g. the liquid build")
    ap.add_argument("--builder", default="twinshade_build.py")
    A = ap.parse_args()

    relic = (HERE / A.relic).resolve()
    tip = (HERE / A.tip).resolve()
    mid = (HERE / A.mid).resolve() if A.mid else None
    marks = markers_from_builder(HERE / A.builder)
    if not marks:
        sys.exit(f"! no *_NEW inserts found in {A.builder} — nothing to audit, "
                 f"which is itself a failure")

    R = relic.read_text(encoding="utf-8")
    M = mid.read_text(encoding="utf-8") if mid else None
    T = tip.read_text(encoding="utf-8")

    print(f"relic  {relic.name}")
    if mid: print(f"mid    {mid.name}")
    print(f"tip    {tip.name}")
    print(f"{len(marks)} inserts read out of {A.builder}\n")

    lost, never = [], []
    for name, line in marks:
        r, t = R.count(line), T.count(line)
        m_ = M.count(line) if M is not None else None
        if r == 0:
            never.append(name)
            print(f"  {'?':>2}  {name:<26} not in the relic build either — the "
                  f"marker is wrong, not the chain")
            continue
        ok = t > 0
        if not ok: lost.append(name)
        mid_s = f"{m_:>3}" if m_ is not None else "  -"
        print(f"  {'ok' if ok else 'LOST':>4}  {name:<26} relic {r:>2}  "
              f"mid {mid_s}  tip {t:>2}"
              + ("" if ok else f"\n        {line[:88]!r}"))

    print()
    if lost:
        print(f"!! {len(lost)} INSERT(S) DID NOT SURVIVE THE CHAIN: "
              f"{', '.join(lost)}")
        print("   The relic build is correct and the build of record is not. "
              "Find the\n   span that swallowed it — liquid_build's `replace_span` "
              "calls are the\n   usual cause — and move the insert outside it.")
        return 1
    print(f"ALL {len(marks) - len(never)} INSERTS SURVIVE to {tip.name}")
    if never:
        print(f"({len(never)} marker(s) unresolved and reported above)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
