#!/usr/bin/env python3
"""One-line contract change for verify.py: ult tips 44 -> 72 chars.

    python3 verify_tip_patch.py            # patches verify.py in place

The v2 fight card renders ult tips on their own 25px line, so the length
budget is the line (~72 chars), not the old tag row (44). Status tips keep
40 — the in-arena first-landing panel still prints those, and intro_probe's
check [6] measures that they fit it.

Anchored exactly, like every patcher here: refuses if the line is not found
exactly once, and says so if the patch is already in.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).parent
TARGET = HERE / "verify.py"

OLD = ("    else if (u.tip.length > 44) bad.push("
       "`${w.name}: ult tip ${u.tip.length} chars (max 44)`);")
NEW = """    // 44 -> 72 with the v2 fight card (2026-08-14): ult tips render on
    // their own 25px line now, so the budget is the line, not the tag row.
    // Status tips keep 40 — the in-arena first-landing panel still prints those.
    else if (u.tip.length > 72) bad.push(`${w.name}: ult tip ${u.tip.length} chars (max 72)`);"""


def main() -> int:
    t = TARGET.read_text(encoding="utf-8")
    if NEW in t:
        print("verify.py already carries the 72-char ult contract — nothing to do")
        return 0
    n = t.count(OLD)
    if n != 1:
        print(f"! anchor appears {n} times, expected 1 — verify.py has moved; "
              f"diff before re-anchoring", file=sys.stderr)
        return 1
    TARGET.write_text(t.replace(OLD, NEW, 1), encoding="utf-8")
    print("verify.py: ult tip contract 44 -> 72 (status tips keep 40)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
