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
  2. Here:        python3 shell_identity.py

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default=str(APP_JSON),
                    help="the json the app wrote")
    ap.add_argument("--game", default=None,
                    help="build to compare against; defaults to the one the "
                         "app recorded, so the two cannot silently differ")
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
    print(f"[identity] headless Chromium {m.group(1) if m else '?'}")

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
        print(f"\nFAIL  {n - bad}/{n} identical — the shell is not the same engine.")
        return 1
    print(f"\nPASS  {n}/{n} identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
