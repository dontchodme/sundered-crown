#!/usr/bin/env python3
"""MOVE THE FIGHTER'S BLURS OFF THE FULL CANVAS.

    python3 shadowbuf_build.py --src sc-lit.html --out sc-buf.html

WHY
---
Measured on an Adreno 660 (`sundered-crown-perf-finding.md`): shadow blur is
83% of the frame in the shipped build and still 62% after the world light.
A Canvas2D shadow costs in proportion to the SURFACE it runs on, which is why
`worldlight_build.py` — written for art reasons — turned out to be the biggest
perf win in the project: it moved 4 blurred draws per frame from a 2.07 Mpx
canvas onto a 0.37 Mpx one and cut shadow cost 57.26 ms -> 16.64 ms.

Traced per call site over one frozen frame, the blurs still on the full canvas:

    8x  Renderer.drawFighter     blur 8.0 x4, 18.0 x2, 26.5, 22.7
    2x  Renderer.drawBar         blur 16.0
    1x  Renderer.drawArena       blur 30.0

**drawFighter is 8 of 11.** This applies the same trick to it: the ball section
draws into a buffer sized to the ball, then blits. Nothing about the drawing
changes -- the buffer's transform is set so world coordinates still work, so
every `f.x, f.y` inside the wrapped block lands exactly where it did.

WHAT IS AND IS NOT WRAPPED
--------------------------
Wrapped: everything from the damage constants through `drawStatus` -- the
desperate ring, the core glow, the grain, the fractures, the shell, the health
ring and the status effects. That is every blur drawFighter owns.

NOT wrapped, deliberately:
  * the trail and the swing-arc ribbons, which run BEFORE and are `lighter`
    against the arena
  * the weapon, which `worldlight_build.py` already buffers
  * the name tag, which is sized in screen pixels and sits outside the ball

KNOWN DIFFERENCE
----------------
One `globalCompositeOperation = "lighter"` sits inside the wrapped block: the
bloom on the health ring's head. Inside a buffer it adds against the ball's own
pixels instead of against the arena. Its gradient fades to transparent within
9-17 world units and it sits on the ring, well inside the ball, so the affected
area is small -- but it is a real difference and it is why this build gets
diffed against its source rather than assumed identical.
"""
from __future__ import annotations
import argparse, pathlib, sys

METHOD = r'''  /* THE BALL, ON ITS OWN SURFACE. A Canvas2D shadow costs in proportion to the
     surface it is drawn on, so eight blurred draws per frame on a 2.07 Mpx
     canvas is eight full-canvas blurs. Drawn into a buffer sized to the ball
     they are eight blurs on ~0.1 Mpx. Measured on an Adreno 660, the same move
     on the weapon was worth 40 ms a frame.

     The buffer's transform is the caller's transform translated so the ball
     sits in the middle, which is what lets the wrapped code go on using world
     coordinates unchanged. Nothing inside it knows it moved. */
  _ballBuf(c, m, f, body){
    const R = CONFIG.physics.ballR;
    const t = c.getTransform();
    const k = Math.hypot(t.a, t.b) || 1;
    const rad = R * 2.1 + 38;                 // desperate ring + widest blur + margin
    const S = Math.ceil(rad * 2 * k);
    if (!this._bbuf){ this._bbuf = document.createElement("canvas"); }
    const b = this._bbuf;
    if (b.width < S || b.height < S){ b.width = S; b.height = S; }
    const bx = b.getContext("2d");
    bx.setTransform(1, 0, 0, 1, 0, 0);
    bx.globalCompositeOperation = "source-over";
    bx.globalAlpha = 1;
    bx.shadowBlur = 0; bx.shadowColor = "transparent";
    bx.clearRect(0, 0, b.width, b.height);
    bx.save();
    bx.translate(S / 2, S / 2);
    bx.scale(k, k);
    bx.translate(-f.x, -f.y);                 /* world coords still work inside */
    body(bx);
    bx.restore();
    c.drawImage(b, 0, 0, S, S, f.x - rad, f.y - rad, rad * 2, rad * 2);
  }

'''
METHOD_ANCHOR = "  drawFighter(m, f){"

OPEN_ANCHOR = """    const base   = CONFIG.combat.baseHP;"""
OPEN_NEW = """    this._ballBuf(c, m, f, (c) => {
    const base   = CONFIG.combat.baseHP;"""

CLOSE_ANCHOR = """    this.drawStatus(m, f);
"""
CLOSE_NEW = """    this.drawStatus(m, f);
    });
"""

PROTECTED = "sundered-crown.html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="sc-lit.html")
    ap.add_argument("--out", default="sc-buf.html")
    a = ap.parse_args()
    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    here = pathlib.Path(__file__).parent
    t = (here / a.src).read_text(encoding="utf-8")
    for name, anc in (("method", METHOD_ANCHOR), ("open", OPEN_ANCHOR), ("close", CLOSE_ANCHOR)):
        if t.count(anc) != 1:
            print(f"! anchor {name} appears {t.count(anc)} times, expected 1", file=sys.stderr)
            return 1
    t = t.replace(METHOD_ANCHOR, METHOD + METHOD_ANCHOR, 1)
    t = t.replace(OPEN_ANCHOR, OPEN_NEW, 1)
    t = t.replace(CLOSE_ANCHOR, CLOSE_NEW, 1)
    print("  [shadowbuf] _ballBuf injected")
    print("  [shadowbuf] drawFighter's ball section wrapped (1 site)")
    out = here / a.out
    out.write_text(t, encoding="utf-8")
    print(f"{a.src} -> {a.out}")
    from scpage import game
    with game(game_path=out.resolve()) as (pg, errs):
        pg.evaluate("""()=>{ AC.setResolution(1080,1920);
          AC.newMatch('grudgebearer','spellbreaker');
          const m=AC.match; m.introT=0; const dt=AC.CONFIG.physics.dt;
          for(let i=0;i<900;i++) m.step(dt);
          AC.__draw(m); return 1; }""")
        if errs:
            print("! PAGE ERRORS:\n  " + "\n  ".join(errs[:4]), file=sys.stderr)
            return 1
    print("  check: 900 steps drawn, no page errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
