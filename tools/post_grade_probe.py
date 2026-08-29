#!/usr/bin/env python3
"""DOES THE VIGNETTE ACTUALLY STACK WITH THE DIRECTOR'S SCRIM?

    python post_grade_probe.py
    python post_grade_probe.py --a twinshade --b lastlight --seed 2027809443

`CINE.wash` is a darkening radial scrim centred on the point of contact,
present only during a cut. A grade's vignette is a frame-centred falloff
that is always on. They are not the same job -- but during a cut, near the
focus, both are darkening the same pixels, and two darkenings stacked read as
a picture that has gone muddy at exactly the moment it should be at its most
legible.

That was ASSERTED in a handover note and then in a comment. This measures it,
which is the difference between a reason and a story.

FOUR CONDITIONS, on the SAME cut frames of the SAME fight:

  A  wash on,  no vignette            what ships today
  B  wash OFF, vignette, no yield     the vignette's own contribution
  C  wash on,  vignette, no yield     THE STACK
  D  wash on,  vignette, full yield   the fix

`CINE.wash` is zeroed for condition B after the pump and before the draw, so
the director still plans and runs the cut -- the zoom, the letterbox and the
timing are all still there -- and only the scrim is suppressed. Nothing in the
build is modified.

Reports mean luma inside the arena rect. If (A - C) is small the yield is not
worth the code and `washYield` should go to 0 with this output as the reason.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-hold-clamp.html"
POST_JS = REPO / "src" / "render" / "post.js"

PROBE_JS = r"""
(cfg) => {
  window.__frozen = true;
  AC.setResolution(cfg.w, cfg.h);
  const FPS = 60, raw = 1 / FPS;
  const cv = document.getElementById('cv');
  const R = AC.renderer;
  const ov = document.createElement('canvas');
  ov.style.display = 'none';
  document.body.appendChild(ov);
  const post = SWBPost.create(ov);

  const VIG = { vignette: 0.38, vignetteFrom: 0.45, grain: 0, contrast: 1.0,
                lift: 0 };

  const rectOf = () => ({ x: R.pad * R.k, y: R.arenaTop * R.k,
                          w: R.aw * R.k, h: R.ah * R.k });

  /* Mean luma inside the arena rect, read off the COMPOSITED pixels. */
  const meanLuma = (px, rect) => {
    const W = cv.width, H = cv.height;
    const x0 = Math.max(0, Math.round(rect.x)), x1 = Math.min(W, Math.round(rect.x + rect.w));
    const y0 = Math.max(0, Math.round(rect.y)), y1 = Math.min(H, Math.round(rect.y + rect.h));
    let sum = 0, n = 0;
    for (let y = y0; y < y1; y += 2) {
      const gy = H - 1 - y;
      for (let x = x0; x < x1; x += 2) {
        const i = (gy * W + x) * 4;
        sum += 0.2126 * px[i] + 0.7152 * px[i + 1] + 0.0722 * px[i + 2];
        n++;
      }
    }
    return n ? sum / n : 0;
  };

  const run = (frames, cond) => {
    CINE.on = true; CINE.interp = true; CINE.reset(); CINE.acc = 0;
    CINE.plan = cinePlan(cfg.a, cfg.b, cfg.seed >>> 0).cuts;
    const m = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
    m.introT = 0; AC.__inject(m);
    AC.SFX.play = function () {}; AC.SFX.resume = function () {};

    post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
    post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
    post.setGrade(cond.vig
      ? Object.assign({}, VIG, { washYield: cond.yield })
      : null);

    const out = [];
    let frame = 0, alpha = 0, wi = 0;
    const want = frames.slice().sort((p, q) => p - q);
    while (wi < want.length && frame < cfg.maxFrames) {
      alpha = CINE.pump(raw, m, 1);
      frame++;
      const near = frame >= want[wi] - cfg.warm;
      if (!near) continue;
      /* Condition B: the director still runs the whole cut, only the scrim is
         suppressed -- after the pump computed it, before the draw reads it. */
      const washNow = CINE.wash || 0;
      if (cond.noWash) CINE.wash = 0;
      m.shake = 0;
      R.roMode = 2;
      if (alpha > 0) CINE.drawLerped(R, m, alpha); else AC.__draw(m);
      const roCtx = (window.__ro = window.__ro || (() => {
        const c = document.createElement('canvas');
        c.width = cv.width; c.height = cv.height; return c;
      })()).getContext('2d');
      roCtx.clearRect(0, 0, cv.width, cv.height);
      roCtx.drawImage(cv, 0, 0);
      R.roMode = 1;
      if (alpha > 0) CINE.drawLerped(R, m, alpha); else AC.__draw(m);
      R.roMode = 0;
      const rect = rectOf();
      post.render(cv, { enabled: true, dt: raw, frame: frame, rect: rect,
                        readouts: window.__ro,
                        cine: { on: true, cut: !!CINE.cut, wash: CINE.wash || 0,
                                tier: CINE.cut ? (CINE.cut.fatal ? 'KILL' : 'T' + CINE.cut.tier) : null } });
      if (cond.noWash) CINE.wash = washNow;
      if (frame === want[wi]) {
        out.push({ frame: frame, luma: +meanLuma(post.readPixels(), rect).toFixed(3),
                   wash: +washNow.toFixed(3),
                   tier: CINE.cut ? (CINE.cut.fatal ? 'KILL' : 'T' + CINE.cut.tier) : null });
        wi++;
      }
    }
    post.setGrade(null); post.setBloom(null); post.setTrails(null);
    return out;
  };

  /* Find cut frames first, cheaply: pump only, no drawing. */
  CINE.on = true; CINE.interp = true; CINE.reset(); CINE.acc = 0;
  CINE.plan = cinePlan(cfg.a, cfg.b, cfg.seed >>> 0).cuts;
  const m0 = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
  m0.introT = 0; AC.__inject(m0);
  AC.SFX.play = function () {}; AC.SFX.resume = function () {};
  const cutFrames = [];
  let f = 0, best = {};
  while (f < cfg.maxFrames && !m0.over) {
    CINE.pump(raw, m0, 1); f++;
    if (CINE.cut && CINE.wash > 0) {
      const key = (CINE.cut.fatal ? 'KILL' : 'T' + CINE.cut.tier) + ':' + Math.round(f / 600);
      if (!best[key] || CINE.wash > best[key].wash) best[key] = { frame: f, wash: CINE.wash };
    }
  }
  for (const k in best) cutFrames.push(best[k].frame);
  cutFrames.sort((p, q) => p - q);
  const frames = cutFrames.slice(0, cfg.moments);
  if (!frames.length) return { err: 'this fight has no cut' };

  return {
    frames: frames,
    A: run(frames, { vig: false, noWash: false }),
    B: run(frames, { vig: true, noWash: true,  yield: 0 }),
    C: run(frames, { vig: true, noWash: false, yield: 0 }),
    D: run(frames, { vig: true, noWash: false, yield: 1 }),
  };
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--a", default="ironhail")
    ap.add_argument("--b", default="dawnbringer")
    ap.add_argument("--seed", type=int, default=922484771)
    ap.add_argument("--moments", type=int, default=3)
    ap.add_argument("--warm", type=int, default=24)
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--h", type=int, default=960)
    ap.add_argument("--json", metavar="PATH")
    A = ap.parse_args()

    path = pathlib.Path(A.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2

    with game(game_path=path) as (page, errors):
        page.add_script_tag(content=POST_JS.read_text(encoding="utf-8"))
        out = page.evaluate(PROBE_JS, {
            "a": A.a, "b": A.b, "seed": A.seed, "moments": A.moments,
            "warm": A.warm, "w": A.w, "h": A.h, "maxFrames": 6000,
        })
        if errors:
            print("! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    if out.get("err"):
        print(f"! {out['err']} -- pick a seed that has one "
              f"(post_spread.py --cuts lists them)")
        return 2

    print(f"\nGRADE STACK  {A.a} v {A.b} seed {A.seed}  {A.w}x{A.h}")
    print("  mean luma inside the arena rect, per condition\n")
    print(f"  {'frame':>6} {'tier':>5} {'wash':>6} "
          f"{'A base':>8} {'B vig':>8} {'C stack':>8} {'D yield':>8}   "
          f"{'A-C':>7} {'A-D':>7}")
    rows = []
    for i in range(len(out["A"])):
        a, b, c, d = out["A"][i], out["B"][i], out["C"][i], out["D"][i]
        rows.append((a, b, c, d))
        print(f"  {a['frame']:>6} {str(a['tier']):>5} {a['wash']:>6.3f} "
              f"{a['luma']:>8.3f} {b['luma']:>8.3f} {c['luma']:>8.3f} "
              f"{d['luma']:>8.3f}   {a['luma'] - c['luma']:>7.3f} "
              f"{a['luma'] - d['luma']:>7.3f}")

    stack = sum(r[0]["luma"] - r[2]["luma"] for r in rows) / len(rows)
    yielded = sum(r[0]["luma"] - r[3]["luma"] for r in rows) / len(rows)
    base = sum(r[0]["luma"] for r in rows) / len(rows)
    print(f"\n  the vignette costs {stack:.3f} of {base:.3f} mean luma on a cut "
          f"frame\n  when it does NOT yield -- {100 * stack / max(base, 1e-6):.1f}% "
          f"darker.")
    print(f"  with the yield it costs {yielded:.3f} "
          f"({100 * yielded / max(base, 1e-6):.1f}%).")
    saved = stack - yielded
    if abs(stack) < 0.6:
        print("\n  THE STACK IS NEGLIGIBLE. The yield is not worth the code, and")
        print("  washYield should go to 0 with this output as the reason.")
    else:
        print(f"\n  The yield recovers {saved:.3f} luma "
              f"({100 * saved / max(stack, 1e-6):.0f}% of the stack), so it")
        print("  earns its place. Neither effect had to be switched off.")

    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(out, indent=1))
        print(f"\n  wrote {A.json}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
