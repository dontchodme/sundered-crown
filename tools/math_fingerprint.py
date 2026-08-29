#!/usr/bin/env python3
"""Do the app's Chromium and the video pipeline's Chromium do the SAME MATHS?

`CLAUDE.md` §1: "(build, relic A, relic B, seed) -> the same fight, always."
There is an unwritten clause on that sentence — *on the same V8* — and this is
the tool that reads it out loud.

V8 implements the transcendental functions in `ieee754.cc`. Nothing in the
language specifies their last bit and that file changes between Chromium
releases. The sim integrates gravity through `Math.pow` for every fighter on
every one of ~4,800 steps, so a one-ULP difference is not a rounding curiosity:
it is a different fight, roughly three times in five.

WHAT WOULD COUNT AS EVIDENCE AGAINST a shared-runtime claim: any one of these
functions returning a different bit pattern in the two runtimes.

  python math_fingerprint.py              app's Electron vs Playwright's headless
  python math_fingerprint.py --save x.json    record one runtime for later

Exits non-zero on any difference. See docs/RUNTIME-DRIFT.md.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
FP_JS = HERE / "mathfp.js"
EL_JS = HERE / "mathfp_electron.js"
# Windows has electron.cmd, everything else has a plain file. Named explicitly
# rather than shelled through npx so a missing install fails as a missing
# install and not as a network timeout.
EL_BIN = [REPO / "app" / "node_modules" / ".bin" / n
          for n in ("electron.cmd", "electron")]


def chrome_of(ua: str) -> str:
    m = re.search(r"Chrome/([\d.]+)", ua or "")
    return m.group(1) if m else "?"


def headless_fp() -> dict:
    """Playwright's bundled Chromium — the one every mp4 is rendered on."""
    with game(game_path=REPO / "02-chain" / "sc-paradox-arc.html") as (page, _):
        return page.evaluate(FP_JS.read_text())


def electron_fp(exe: str | None = None) -> dict | None:
    """The app's Chromium - the one Rick actually watches.

    `exe` names a different Electron install, which is how a candidate
    version gets fingerprinted before anything in app/ is touched.
    """
    exe = (pathlib.Path(exe) if exe else
           next((q for q in EL_BIN if q.exists()), None))
    if exe is None:
        return None
    out = subprocess.run([str(exe), str(EL_JS)], capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout.strip():
        print("! electron fingerprint failed")
        print((out.stderr or out.stdout)[-800:])
        return None
    return json.loads(out.stdout[out.stdout.index("{"):])


def compare(a: dict, b: dict, na: str, nb: str) -> int:
    keys = [k for k in a if k != "ua"]
    diff = [k for k in keys if a.get(k) != b.get(k)]
    same = [k for k in keys if k not in diff]

    print(f"[mathfp] {na:<9} Chromium {chrome_of(a.get('ua'))}")
    print(f"[mathfp] {nb:<9} Chromium {chrome_of(b.get('ua'))}")
    print(f"\n  identical : {' '.join(same) or '(none)'}")
    print(f"  DIFFERENT : {' '.join(diff) or '(none)'}")

    for k in diff:
        for i, (x, y) in enumerate(zip(a[k].split(","), b[k].split(","))):
            if x != y:
                print(f"    Math.{k}  sample {i}:  {na}={x}  {nb}={y}")
                break

    if not diff:
        print(f"\nPASS  the two runtimes agree to the last bit.")
        return 0
    print(f"\nFAIL  {len(diff)} of {len(keys)} functions differ.")
    print("      The seed does not name the same fight in both runtimes.")
    print("      This is not a bug in the shell or in the engine - it is two")
    print("      different Chromium builds. See docs/RUNTIME-DRIFT.md.")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", metavar="PATH",
                    help="write the headless fingerprint and stop")
    ap.add_argument("--electron", metavar="PATH",
                    help="fingerprint this Electron binary instead of app/'s")
    ap.add_argument("--against", metavar="PATH",
                    help="compare headless against a recorded fingerprint "
                         "instead of against the app's Electron")
    args = ap.parse_args()

    head = headless_fp()
    if args.save:
        pathlib.Path(args.save).write_text(json.dumps(head, indent=1))
        print(f"wrote {args.save}  (Chromium {chrome_of(head['ua'])})")
        return 0

    if args.against:
        other = json.loads(pathlib.Path(args.against).read_text())
        return compare(other, head, "recorded", "headless")

    el = electron_fp(args.electron)
    if el is None:
        print("! no Electron found - run `npm install` in app/, or pass --against")
        return 2
    return compare(el, head, "electron", "headless")


if __name__ == "__main__":
    sys.exit(main())
