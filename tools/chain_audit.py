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

# A MARKER MAY NOT SURVIVE ITS OWN BUILDER. Builders template their inserts --
# `tip:"%TIP%"`, `maxStacks:%MAXSTACKS%` -- and the text substituted at build
# time is not the text in the source, so a marker chosen from a templated line
# is guaranteed to be absent from every build and reports as unresolved. The
# report says so honestly ("the marker is wrong, not the chain"), but an
# unresolved marker is an insert nobody is watching. Skip those lines and pick
# the longest line the builder writes VERBATIM.
TEMPLATED = re.compile(r"%[A-Z_0-9]+%")

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
                 and not l.strip("{}(); ") == ""
                 and not TEMPLATED.search(l)]
        if cands:
            out.append((name, max(cands, key=len)))

    # SOURCE-READING MISSES AN INSERT THAT IS NOT A LITERAL. A builder may
    # COMPUTE its insert, or import it from the builder that owns the art so
    # there is only one copy of it -- daybreak_annulus_build.py does exactly
    # that, and this tool answered "no *_NEW inserts found", which reads as a
    # missing builder rather than as a form it cannot see. Second time the
    # discovery has been too narrow; the raw-string note above was the first.
    #
    # So: fall back to IMPORTING the builder and reading its module-level
    # *_NEW strings. Import, not exec -- a builder does its work in main(),
    # and every one of them is import-safe behind `if __name__ == "__main__"`.
    if not out:
        import importlib.util
        spec = importlib.util.spec_from_file_location(builder.stem, builder)
        try:
            mod = importlib.util.module_from_spec(spec)
            sys.modules.setdefault(builder.stem, mod)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"  (could not import {builder.name} to look for computed "
                  f"inserts: {e})")
            return out
        for name in dir(mod):
            if not name.endswith("_NEW"):
                continue
            body = getattr(mod, name)
            if not isinstance(body, str):
                continue
            cands = [l.strip() for l in body.splitlines()]
            cands = [l for l in cands
                     if len(l) > 18 and not l.startswith(("/*", "*", "//"))
                     and not l.strip("{}(); ") == ""
                     and not TEMPLATED.search(l)]
            if cands:
                out.append((name, max(cands, key=len)))
        if out:
            print(f"  ({len(out)} insert(s) found by importing {builder.name} "
                  f"-- computed or imported, not source literals)")

    # AND A BUILDER MAY NOT HAVE `*_NEW` CONSTANTS AT ALL. THIRD TIME this
    # discovery has been too narrow -- the raw-string note was the first, the
    # computed-insert note the second, and both say so above. `curse_build.py`
    # keeps its edits in one table of `(label, old, new)` tuples, which is a
    # perfectly ordinary shape and one this tool answered "nothing to audit"
    # for. That message is technically true and reads as "clean".
    #
    # So the LAST fallback is any module-level sequence of tuples whose final
    # element is a multi-line string: that is an insert table by any name. The
    # label comes from the tuple's own first element when it is a string, so
    # the report still says WHICH edit went missing rather than an index.
    #
    # AND IT IS NOT A FALLBACK ANY MORE, WHICH IS THE FOURTH TIME THIS
    # DISCOVERY HAS BEEN TOO NARROW. It used to run only `if not out`, so a
    # builder carrying BOTH shapes -- one `*_NEW` constant for its fx spec and
    # eighteen edits in `(label, old, new)` tables -- had the constant found,
    # `out` come back non-empty, and the eighteen never looked at.
    # `cindercleave_build.py` is exactly that shape and this tool reported
    # "ALL 1 INSERTS SURVIVE", which is open item 31 in a better costume: a
    # GREEN chain_audit that audited nothing is the failure mode this tool was
    # written for. Both passes run now and the results are merged.
    if True:
        import importlib.util
        spec = importlib.util.spec_from_file_location(builder.stem, builder)
        try:
            mod = importlib.util.module_from_spec(spec)
            sys.modules.setdefault(builder.stem, mod)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"  (could not import {builder.name} to look for insert "
                  f"tables: {e})")
            return out
        n0 = len(out)
        seen = {line for _, line in out}
        for tname in dir(mod):
            if tname.startswith("_"):
                continue
            table = getattr(mod, tname)
            if not isinstance(table, (list, tuple)) or not table:
                continue
            for i, row in enumerate(table):
                if not isinstance(row, (list, tuple)) or len(row) < 2:
                    continue
                body = row[-1]
                if not isinstance(body, str) or "\n" not in body:
                    continue
                label = row[0] if isinstance(row[0], str) else f"{tname}[{i}]"
                cands = [l.strip() for l in body.splitlines()]
                cands = [l for l in cands
                         if len(l) > 18 and not l.startswith(("/*", "*", "//"))
                         and not l.strip("{}(); ") == ""
                         and not TEMPLATED.search(l)]
                if cands:
                    row2 = (f"{tname}:{label}", max(cands, key=len))
                    if row2[1] not in seen:
                        seen.add(row2[1]); out.append(row2)
        if len(out) > n0:
            print(f"  ({len(out) - n0} insert(s) found in {builder.name}'s "
                  f"insert table(s) -- tuples, not *_NEW constants)")
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
