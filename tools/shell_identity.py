#!/usr/bin/env python3
"""Does the Electron shell run the SAME ENGINE headless Chromium runs?

This is Phase 1's actual test, and "the app opened" is not it. The whole
argument for Electron over Tauri is that the app renders on the same Chromium
the video pipeline is validated against — so the app cannot show Rick something
the mp4 will not. That claim is worth exactly as much as this check.

WHAT WOULD COUNT AS EVIDENCE AGAINST: any field of any fight summary differing
between the two runtimes for the same (relic, relic, seed). One differing
digit means the shell has changed the engine, and every clip rendered from a
seed watched in the app is a different fight from the one that was watched.

  1. In the app:  Engine identity -> Run 200 seeds
     (writes out/shell_identity_app.json)
  2. Here:        python shell_identity.py      (python3 on mac/Linux)

Exits non-zero on any mismatch.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
APP_JSON = REPO / "out" / "shell_identity_app.json"

# Run the app's rows through the headless engine, one for one, in order.
# Deliberately re-simulates rather than re-deriving the seeds: if the app and
# this file computed seeds independently and both were wrong the same way, the
# check would pass on two identical mistakes.
SWEEP_JS = r"""
(rows) => rows.map(r => ({ a: r.a, b: r.b, seed: r.seed,
                           r: AC.simulate(r.a, r.b, r.seed) }))
"""


def flatten(prefix, obj, out):
    """Compare every leaf, not a summary of them. A check that compares
    winners only would pass on a build where damage moved and the stronger
    relic still won."""
    if isinstance(obj, dict):
        for k in sorted(obj):
            flatten(f"{prefix}.{k}", obj[k], out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            flatten(f"{prefix}[{i}]", v, out)
    else:
        out[prefix] = obj
    return out


def _when(p: pathlib.Path) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(
        p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=str(APP_JSON),
                    help="the json the app wrote")
    ap.add_argument("--game", default=None,
                    help="build to compare against; defaults to the one the "
                         "app recorded, so the two cannot silently differ")
    ap.add_argument("--stale-ok", action="store_true",
                    help="compare even when the app json predates the build. "
                         "Almost never what you want -- read the guard")
    args = ap.parse_args()

    app_path = pathlib.Path(args.app)
    if not app_path.exists():
        print(f"! {app_path} not found — run the app's identity check first")
        return 2

    app = json.loads(app_path.read_text())
    rows = app["rows"]
    build = args.game or app.get("build")
    if not build:
        print("! the app json names no build and --game was not given")
        return 2

    path = (REPO / build).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2

    # THIS GATE CAN PASS WITHOUT THE APP EVER HAVING RUN, and it did.
    #
    # 2026-08-29: fx_build.py made a new tip and app/main.js was repointed at
    # it. This tool then reported PASS 192/192 -- against a json the app had
    # written THREE DAYS EARLIER, naming the OLD build. It does not launch the
    # app; it diffs an artifact on disk. So the one gate whose entire job is
    # "the app and the video agree" was comparing a stale app against a fresh
    # headless, and a green result meant nothing.
    #
    # That is CLAUDE.md §4.1's defect class in a gate rather than in the art:
    # right and wrong produce the same output. Two guards, and both are loud
    # rather than advisory, because a warning in a passing run is not read.
    stale = path.stat().st_mtime - app_path.stat().st_mtime
    if stale > 0:
        print("\n! THE APP JSON IS OLDER THAN THE BUILD IT NAMES.")
        print(f"    {app_path.name}  {_when(app_path)}")
        print(f"    {path.name}  {_when(path)}   ({stale / 3600:.1f}h newer)")
        print("  The app has not been run against this build, so a PASS here "
              "would be a\n  comparison with a stale artifact. Run the app's "
              "own check first:")
        print("\n    cd app && npm run identity\n")
        if not args.stale_ok:
            return 2
        print("  --stale-ok given; continuing against the old run.\n")

    print(f"[identity] app   Chromium {app.get('chrome','?')}  {len(rows)} fights")
    print(f"[identity] build {build}")

    with game(game_path=path) as (page, errors):
        head = page.evaluate("() => navigator.userAgent")
        got = page.evaluate(SWEEP_JS, [{"a": r["a"], "b": r["b"], "seed": r["seed"]}
                                       for r in rows])
        if errors:
            print("! page errors during the sweep:")
            for e in errors[:10]:
                print("   ", e)
            return 1

    import re
    m = re.search(r"Chrome/([\d.]+)", head)
    head_chrome = m.group(1) if m else "?"
    app_chrome = str(app.get("chrome", "?"))
    print(f"[identity] headless Chromium {head_chrome}")

    bad = 0
    for i, (want, have) in enumerate(zip(rows, got)):
        if (want["a"], want["b"], want["seed"]) != (have["a"], have["b"], have["seed"]):
            print(f"  [{i}] ROW MISALIGNED — app {want['a']}/{want['b']}/{want['seed']}"
                  f" vs headless {have['a']}/{have['b']}/{have['seed']}")
            bad += 1
            continue
        fa = flatten("", want["r"], {})
        fb = flatten("", have["r"], {})
        for k in sorted(set(fa) | set(fb)):
            if fa.get(k) != fb.get(k):
                print(f"  [{i}] {want['a']} v {want['b']} seed {want['seed']}"
                      f"  {k}: app={fa.get(k)!r} headless={fb.get(k)!r}")
                bad += 1
                break

    n = len(rows)
    if bad:
        print(f"\nFAIL  {n - bad}/{n} identical.")
        # ATTRIBUTION MATTERS MORE THAN THE COUNT. This check was written to
        # catch a shell that had changed the engine, and its only failure
        # message said exactly that. It is not the only way to fail it. If the
        # two runtimes are different Chromium builds, the engine is untouched
        # and the maths under it is not: V8 promises no last bit for Math.pow,
        # the sim integrates gravity through it every step, and about three
        # fights in five come out different. Saying "the shell is not the same
        # engine" here sends the next session to read a shell that is innocent.
        if app_chrome != head_chrome and "?" not in (app_chrome, head_chrome):
            print("      The two runtimes are DIFFERENT CHROMIUM BUILDS:")
            print(f"        app      Chromium {app_chrome}")
            print(f"        headless Chromium {head_chrome}")
            print("      Before reading the shell, run:  python math_fingerprint.py")
            print("      It says whether Math itself differs. If it does, this")
            print("      failure is the runtime PAIR, not the shell, and the fix")
            print("      is a pin. See docs/RUNTIME-DRIFT.md.")
        else:
            print(f"      Both runtimes report Chromium {head_chrome}, so this is")
            print("      NOT runtime drift - the shell has changed the engine.")
        return 1
    print(f"\nPASS  {n}/{n} identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
