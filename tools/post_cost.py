#!/usr/bin/env python3
"""WHAT DOES THE POST CHAIN COST PER FRAME?

    python post_cost.py                 on the real GPU, through Electron
    python post_cost.py --headless      through Playwright, i.e. SwiftShader

`docs/RENDERER-BRIEF.md` §7 gate 3: frame cost measured, not felt. "A post
chain that adds 8 ms is not free at 120 fps -- it is the whole budget."

WHICH RUNTIME, AND WHY IT MATTERS MORE HERE THAN ANYWHERE ELSE IN THIS REPO.
Everywhere else the two Chromiums are interchangeable because they agree to
the last bit (docs/RUNTIME-DRIFT.md). Not for this. Playwright launches with
--disable-gpu, so its WebGL is SwiftShader: a software rasteriser, and a
number off it is a measurement of SwiftShader. Electron uses the machine's own
GPU, which is what Rick watches on. So this defaults to Electron and always
prints the renderer it measured.

WHAT TRANSFERS is the RATIO between rows measured back to back in one session
-- hud_cost.py's point, and the only question the chain has to answer: did it
make the frame materially more expensive than the 2D draw already was?

The median of `--reps` repetitions is reported, not the mean: one scheduling
hiccup in a run of five should not become the answer.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-hold-clamp.html"
POST_JS = REPO / "src" / "render" / "post.js"
COST_JS = HERE / "postcost.js"
EL_JS = HERE / "postcost_electron.js"
EL_BIN = [REPO / "app" / "node_modules" / ".bin" / n
          for n in ("electron.cmd", "electron")]


def run_electron(game: pathlib.Path, cfg: dict) -> dict | None:
    exe = next((p for p in EL_BIN if p.exists()), None)
    if exe is None:
        print("! no Electron in app/node_modules -- run `npm install` in app/,")
        print("  or pass --headless and read the caveat in the header.")
        return None
    out = subprocess.run(
        [str(exe), str(EL_JS), "--game", str(game), "--cfg", json.dumps(cfg)],
        capture_output=True, text=True)
    if out.returncode != 0 or "{" not in out.stdout:
        print("! electron run failed")
        print((out.stderr or out.stdout)[-1200:])
        return None
    return json.loads(out.stdout[out.stdout.index("{"):])


def run_headless(game: pathlib.Path, cfg: dict) -> dict | None:
    from scpage import game as page_ctx
    with page_ctx(game_path=game) as (page, errors):
        page.add_script_tag(content=POST_JS.read_text(encoding="utf-8"))
        page.evaluate("() => { window.__frozen = true; }")
        out = page.evaluate("(" + COST_JS.read_text(encoding="utf-8") + ")", cfg)
        if errors:
            print("! page errors:")
            for e in errors[:6]:
                print("   ", e)
            return None
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--headless", action="store_true",
                    help="Playwright instead of Electron. SOFTWARE rasteriser.")
    ap.add_argument("--a", default="paradox")
    ap.add_argument("--b", default="heartwood")
    ap.add_argument("--seed", type=int, default=25064)
    ap.add_argument("--at", type=float, default=22.0,
                    help="seconds of fight before measuring -- seals up, "
                         "statuses live, cracks grown")
    ap.add_argument("--n", type=int, default=60, help="draws per repetition")
    ap.add_argument("--warm", type=int, default=12)
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--json", metavar="PATH")
    A = ap.parse_args()

    game = pathlib.Path(A.game).resolve()
    if not game.exists():
        print(f"! {game} does not exist")
        return 2
    for f in (POST_JS, COST_JS):
        if not f.exists():
            print(f"! {f} does not exist")
            return 2

    cfg = {"a": A.a, "b": A.b, "seed": A.seed, "at": A.at, "n": A.n,
           "warm": A.warm, "reps": A.reps, "w": A.w, "h": A.h}

    print(f"\nPOST COST  {A.a} v {A.b} seed {A.seed} at t={A.at}s  "
          f"{A.w}x{A.h}  {A.n} draws x {A.reps} reps")
    out = (run_headless(game, cfg) if A.headless else run_electron(game, cfg))
    if out is None:
        return 1

    soft = any(s in out["renderer"] for s in ("SwiftShader", "llvmpipe", "Software"))
    print(f"  {out['renderer']}")
    if soft:
        print("  ^ SOFTWARE RASTERISER. These are not Rick's numbers and not a")
        print("    phone's. Read the RATIO column and ignore the milliseconds.")

    by = {}
    order = []
    for r in out["rows"]:
        if r["name"] not in by:
            by[r["name"]] = []
            order.append(r["name"])
        by[r["name"]].append(r["ms"])

    base = statistics.median(by[order[0]])
    print(f"\n  {'configuration':<24} {'ms/frame':>9} {'vs 2D':>8} "
          f"{'added':>9}  spread")
    for name in order:
        v = sorted(by[name])
        med = statistics.median(v)
        print(f"  {name:<24} {med:>9.3f} {med / base:>7.2f}x "
              f"{med - base:>+8.3f}  {v[0]:.2f}..{v[-1]:.2f}")

    chain = statistics.median(by[order[1]]) - base
    both = statistics.median(by[order[-1]]) - base
    print(f"\n  the chain with nothing on costs {chain:+.3f} ms -- that is the"
          f" upload,\n  two copies and the readback, and it is the floor.")
    print(f"  the whole chosen chain costs {both:+.3f} ms.")
    budget60, budget120 = 16.67, 8.33
    print(f"\n  a frame has {budget60:.2f} ms at 60fps and {budget120:.2f} at 120.")
    print(f"  total as chosen: {statistics.median(by[order[-1]]):.2f} ms "
          f"= {100 * statistics.median(by[order[-1]]) / budget60:.0f}% of the 60fps"
          f" budget, {100 * statistics.median(by[order[-1]]) / budget120:.0f}% of 120.")
    if soft:
        print("  (on a software rasteriser, so those percentages are of a"
              " budget\n   this machine was never going to meet. The ratio is"
              " the finding.)")

    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1))
        print(f"\n  wrote {A.json}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
