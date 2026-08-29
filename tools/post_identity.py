#!/usr/bin/env python3
"""With no effect passes, does the post chain change a single pixel?

`docs/RENDERER-BRIEF.md` §8.2 says get one pass working end to end -- source
canvas, framebuffer, a trivial shader, screen -- with the A/B toggle, BEFORE
any effect exists, because the plumbing is where this goes wrong and not the
maths. This is the assertion that step is worth anything at all.

The chain uploads the finished 2D canvas, copies it into a framebuffer, and
copies that to the screen. Every one of those hops is a place a picture can
pick up a bit of gamma, a premultiply, a resample or a flip -- none of which
looks like a bug. It looks like a slightly different render, which is this
project's own worst defect class: wrong and right producing numbers that
look right.

WHAT WOULD COUNT AS EVIDENCE AGAINST: one channel of one pixel differing
between the composited frame and the 2D canvas it was handed.

  python post_identity.py                      one frame of the default fight
  python post_identity.py --a paradox --b heartwood --seed 25064 --at 6.0

Exits non-zero on any difference. See docs/RENDER-LAYERS.md for what the
chain will eventually be allowed to touch, and what it must not.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
POST_JS = REPO / "src" / "render" / "post.js"
BUILD = REPO / "02-chain" / "sc-paradox-arc.html"

# Deliberately runs selfTest against the LIVE canvas rather than a synthetic
# test pattern. A gradient would exercise the copy; only the real frame
# exercises it on the colours the art actually uses, including the additive
# pile-ups in drawUltOver where a premultiply mistake would show first.
CHECK_JS = """
() => {
  const src = document.getElementById('cv');
  const ov = document.createElement('canvas');
  ov.style.display = 'none';
  document.body.appendChild(ov);
  let post;
  try { post = SWBPost.create(ov); }
  catch (e) { return { err: String(e.message || e) }; }
  const r = post.selfTest(src, { enabled: true });
  const gl = ov.getContext('webgl2');
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  return {
    w: src.width, h: src.height, version: post.version,
    total: r.total, differing: r.differing, maxDelta: r.maxDelta,
    sample: r.sample, passes: r.passes,
    renderer: dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)
                  : gl.getParameter(gl.RENDERER),
  };
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--a", default=None, help="relic id, left")
    ap.add_argument("--b", default=None, help="relic id, right")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--at", type=float, default=0.0,
                    help="seconds of fight to run before the frame is checked")
    ap.add_argument("--json", metavar="PATH", help="write the result")
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2
    if not POST_JS.exists():
        print(f"! {POST_JS} does not exist")
        return 2

    with game(game_path=path) as (page, errors):
        if not page.evaluate("() => !!document.createElement('canvas')"
                             ".getContext('webgl2')"):
            print("! no WebGL2 in this Chromium -- cannot check the chain")
            return 2

        if args.a and args.b:
            page.evaluate("([a, b, s]) => AC.newMatch(a, b, s === null "
                          "? undefined : s >>> 0)",
                          [args.a, args.b, args.seed])

        # Let the engine actually draw. Two rAFs so the frame being measured is
        # a finished one and not the one still being composited.
        page.evaluate("(sec) => new Promise(r => setTimeout(r, sec * 1000))",
                      max(0.0, args.at))
        page.evaluate("() => new Promise(r => requestAnimationFrame("
                      "() => requestAnimationFrame(r)))")

        page.add_script_tag(content=POST_JS.read_text(encoding="utf-8"))
        out = page.evaluate(CHECK_JS)

        if errors:
            print("! page errors:")
            for e in errors[:10]:
                print("   ", e)
            return 1

    if out.get("err"):
        print(f"! the chain would not start: {out['err']}")
        return 1

    print(f"[post] {out['version']}  {out['w']}x{out['h']}  "
          f"{out['passes']} effect passes")
    print(f"[post] {out['renderer']}")

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(out, indent=1))

    if out["passes"] > 0:
        print("\n! effect passes are registered, so a difference is EXPECTED "
              "and this check\n  cannot say anything about the plumbing. Run "
              "it with the chain empty.")
        return 2

    if out["differing"] == 0:
        print(f"\nPASS  {out['total']:,} px identical, max delta 0.")
        print("      The chain is invisible with nothing switched on, which is")
        print("      what makes the A/B toggle a control rather than a second")
        print("      unknown.")
        return 0

    s = out["sample"]
    print(f"\nFAIL  {out['differing']:,} of {out['total']:,} px differ, "
          f"max delta {out['maxDelta']}.")
    if s:
        print(f"      first at {s['x']},{s['y']}  "
              f"got {s['got']}  want {s['want']}")
    print("      A passthrough that is not a passthrough. Look at the context")
    print("      attributes and the UNPACK_* pixelStorei calls before the")
    print("      shader: premultiplied alpha and colourspace conversion are")
    print("      the two that produce a picture that still looks right.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
