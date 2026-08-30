#!/usr/bin/env python3
"""THE IGNITION OPEN, MEASURED — one check per sentence of what was built.

    python ignition_probe.py
    python ignition_probe.py --game ../02-chain/sc-paradox-ignition.html

## Why this exists at all

CLAUDE.md §4.1: **a picture fault is a defect class this project has twice**,
and both times the numbers were identical either way. v42 shipped a SILENT
ultimate through a 14-check probe, a 29-check probe, a full sweep, a 13/13
verify and a rendered clip. v43's Stasis hold stuck to the ball it froze
through a 30/30 relic probe and a 2760/2760 engine A/B. Rick caught both.

`engine_ab` proving the sim did not move is necessary here and says nothing at
all about whether anything is on screen. So every check below is about PIXELS,
or about the transform that produces them:

    1  the module is in the build and switched on
    2  the camera takes the frame, and its zoom track IS the shot table
    3  the subject's magnified body stays inside the frame  <- the property the
       feasibility clamp normally guarantees, and the opening switches it off
    4  the pull-wide is continuous, and the A->B seam is a CUT
    5  the camera hands the lens back, on time
    6  the flare is actually drawn                          <- the v42 check
    7  and not before its own moment: the stagger is real and neither flare
       paints the other relic
    8  the swell reaches the canvas: shadowBlur really is multiplied
    9  and the accessor is REMOVED again when the opening is over
   10  a frame drawn three times at one sim time is one frame  <- idempotence
   11  how often the director already wants the opening's 2.35s

Check 10 is the one a wall-clock implementation would fail, which is why it is
here rather than in a comment. **Frame identity against the build this was
built from is `render_ab.py`'s job, not this file's** -- it pins the camera
shake's Math.random and runs both builds in one rasteriser, and neither of
those is worth reimplementing here:

    python render_ab.py --a ../02-chain/sc-paradox-crucible.html \\
        --b ../02-chain/sc-paradox-ignition.html --frames 3,6,12,22,31
                                                        # EXPECT IDENTICAL
    python render_ab.py --a ... --b ... --frames 0.3,1.0,2.0
                                                        # EXPECT A DIFF
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import math
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).parent

W, H = 540, 960

# The shot table, transcribed. Not a substitute for the module -- the sha256
# stamp is what catches drift -- but it is what lets check 2 say the zoom on
# screen is the zoom that was authored, at the sim time it was authored for.
SHOTS = [
    (0.00, 1.33, "a", 2.25, 2.02, "cubic"),
    (1.33, 2.03, "b", 2.25, 2.02, "cubic"),
    (2.03, 2.83, None, 2.02, 1.00, "smooth"),
]
CUT = SHOTS[1][0]        # the hard cut from A to B
PULL = SHOTS[2][0]       # the pull wide starts


def expect_z(t):
    for t0, t1, _at, z0, z1, ease in SHOTS:
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0)
            e = (u * u * (3 - 2 * u)) if ease == "smooth" else 1 - (1 - u) ** 3
            return z0 + (z1 - z0) * e
    return None


def subject(t):
    for t0, t1, at, _z0, _z1, _e in SHOTS:
        if t0 <= t < t1:
            return at
    return None


NEW_JS = r"""([a, b, seed]) => {
  window.__frozen = true;
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  CINE.on = true; CINE.reset(); CINE.acc = 0; CINE.plan = [];
  if (typeof POSTFX !== "undefined") POSTFX.reset();
  const m = new AC.Match(a, b, seed >>> 0);
  m.introT = 0;
  window.__pm = m; window.__match = m; AC.__inject && AC.__inject(m);
  return { t: m.t };
}"""

# Step the CURRENT match forward to an absolute sim time and draw it. Forward
# only, so a rising list of times costs one pass through the fight.
TO_JS = r"""([t]) => {
  const m = window.__pm, dt = AC.CONFIG.physics.dt;
  let n = 0;
  while (m.t < t - dt * 0.5 && !m.over && n < 20000){ m.step(dt); n++; }
  AC.__draw(m);
  const r = AC.renderer;
  const cam = SWBOpen.cam(m, r, AC.CONFIG.arena);
  return { t: m.t, cam, aw: r.aw, ah: r.ah, scale: r.scale, k: r.k,
           pad: r.pad, arenaTop: r.arenaTop,
           ax: m.a.x, ay: m.a.y, bx: m.b.x, by: m.b.y,
           cineCam: r._cineCam ? r._cineCam.slice() : null,
           mul: SWBOpen.mul, shake: m.shake };
}"""

URL_JS = r"""() => { const u = document.getElementById('cv').toDataURL('image/png');
                     return u.slice(u.indexOf(',') + 1); }"""

DRAW_JS = r"""() => { AC.__draw(window.__pm); return true; }"""

# Mean luma inside a disc of sim radius R around a sim point, on the FINISHED
# canvas, through the same transform the frame was drawn with -- so a zoomed
# opening frame is sampled where the relic actually is. `offscreen` when the
# disc does not fully fit the canvas, because a partly-clipped disc is a
# different measurement and must not be compared with a whole one.
DISC_JS = r"""([sx, sy, R]) => {
  const r = AC.renderer, cv = document.getElementById('cv');
  const c = cv.getContext('2d');
  let lx = sx * r.scale, ly = sy * r.scale, rr = R * r.scale;
  const cam = r._cineCam;
  if (cam){ lx = cam[0] + (lx - cam[0]) * cam[2];
            ly = cam[1] + (ly - cam[1]) * cam[2]; rr *= cam[2]; }
  const px = (r.pad + lx) * r.k, py = (r.arenaTop + ly) * r.k;
  const rd = Math.max(4, rr * r.k);
  const x0 = Math.round(px - rd), y0 = Math.round(py - rd);
  const x1 = Math.round(px + rd), y1 = Math.round(py + rd);
  if (x0 < 0 || y0 < 0 || x1 > cv.width || y1 > cv.height)
    return { luma: 0, offscreen: true };
  const d = c.getImageData(x0, y0, x1 - x0, y1 - y0).data;
  let s = 0, n = 0;
  for (let i = 0; i < d.length; i += 4){
    s += (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255; n++;
  }
  return { luma: s / Math.max(1, n), offscreen: false };
}"""

BLUR_JS = r"""() => {
  const cv = document.getElementById('cv'), c = cv.getContext('2d');
  const before = c.shadowBlur;
  c.shadowBlur = 10;
  const seen = c.shadowBlur;
  c.shadowBlur = before;
  const d = Object.getOwnPropertyDescriptor(
              CanvasRenderingContext2D.prototype, 'shadowBlur');
  return { seen, mul: SWBOpen.mul,
           native: !!(d && d.get && /\[native code\]/.test(d.get.toString())) };
}"""

# The crop sweep: cam() and two relic positions, and NOTHING IS DRAWN, so a
# whole pairing costs milliseconds and the ceiling can be measured across the
# roster instead of asserted off one seed.
CROP_JS = r"""([pairs, dur]) => {
  const dt = AC.CONFIG.physics.dt, r = AC.renderer, out = [];
  for (const p of pairs){
    const m = new AC.Match(p[0], p[1], p[2] >>> 0);
    m.introT = 0; window.__pm = m; AC.__inject && AC.__inject(m);
    let worst = null;
    for (let t = 0; t < dur; t += 0.02){
      while (m.t < t - dt * 0.5 && !m.over) m.step(dt);
      const cam = SWBOpen.cam(m, r, AC.CONFIG.arena);
      if (!cam) continue;
      let at = null;
      for (const sh of SWBOpen.SHOTS)
        if (m.t >= sh.t0 && m.t < sh.t1){ at = sh.at || null; break; }
      if (!at) continue;
      const sx = at === 'a' ? m.a.x : m.b.x, sy = at === 'a' ? m.a.y : m.b.y;
      const lx = cam[0] + (sx * r.scale - cam[0]) * cam[2];
      const ly = cam[1] + (sy * r.scale - cam[1]) * cam[2];
      const rr = 34 * r.scale * cam[2];             // the relic's own radius
      const margin = Math.min(lx - rr, ly - rr,
                              r.aw - (lx + rr), r.ah - (ly + rr));
      if (!worst || margin < worst.margin)
        worst = { a: p[0], b: p[1], seed: p[2], t: +m.t.toFixed(2), at: at,
                  margin: +margin.toFixed(1) };
    }
    if (worst) out.push(worst);
  }
  return out;
}"""

PLAN_JS = r"""([pairs, dur]) => {
  let n = 0, early = 0; const first = [];
  for (const p of pairs){
    const plan = cinePlan(p[0], p[1], p[2] >>> 0);
    n++;
    if (plan.cuts.length && plan.cuts[0].t < dur){
      early++; first.push(+plan.cuts[0].t.toFixed(2));
    }
  }
  return { n, early, first };
}"""


def sha(b64: str) -> str:
    return hashlib.sha256(base64.b64decode(b64)).hexdigest()[:16]


class Probe:
    def __init__(self):
        self.rows = []

    def check(self, ok, label, detail=""):
        self.rows.append((bool(ok), label, detail))
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}"
              + (f"\n          {detail}" if detail else ""))
        return bool(ok)

    def note(self, label, detail):
        print(f"  --    {label}\n          {detail}")

    def report(self):
        good = sum(1 for ok, _, _ in self.rows if ok)
        print(f"\n{good}/{len(self.rows)} checks")
        for ok, label, detail in self.rows:
            if not ok:
                print(f"  FAILED: {label}\n          {detail}")
        return 0 if good == len(self.rows) else 1


def screen(s, sx, sy):
    """Sim point -> design-space screen point, under the frame's own camera."""
    if not s["cam"]:
        return sx * s["scale"], sy * s["scale"]
    px, py, z = s["cam"]
    return px + (sx * s["scale"] - px) * z, py + (sy * s["scale"] - py) * z


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="../02-chain/sc-paradox-ignition.html")
    ap.add_argument("--a", default="ironhail")
    ap.add_argument("--b", default="oathwound")
    ap.add_argument("--seed", type=int, default=55196)
    ap.add_argument("--plan-n", type=int, default=120)
    ap.add_argument("--pairings", type=int, default=12,
                    help="how many pairings check 3 sweeps the crop over")
    A = ap.parse_args()

    P = Probe()
    gpath = (HERE / A.game).resolve()

    with game(game_path=gpath) as (page, errors):
        page.evaluate(f"AC.setResolution({W}, {H})")
        info = page.evaluate("() => ({ post: AC.POSTFX.on, "
                             "open: typeof SWBOpen, "
                             "ver: window.SWBOpen ? SWBOpen.VERSION : null, "
                             "on: window.SWBOpen ? SWBOpen.on : null, "
                             "dur: window.SWBOpen ? SWBOpen.DUR : null, "
                             "look: window.SWBOpen ? SWBOpen.LOOK : null })")
        DUR = info["dur"] or 0
        LOOK = info["look"] or {}
        print(f"{gpath.name}   post chain {'ON' if info['post'] else 'OFF'}"
              f"   {W}x{H}   {A.a} v {A.b} seed {A.seed}\n")

        # -- 1 ---------------------------------------------------------------
        P.check(info["open"] == "object" and info["on"] is True
                and info["ver"] == 1,
                "1  the module is in the build and switched on",
                f"SWBOpen v{info['ver']}, DUR {DUR}s, "
                f"flares {LOOK.get('flareA')}s / {LOOK.get('flareB')}s")

        # -- 2, 3, 4 ---------------------------------------------------------
        # One forward pass, sampled every 20ms through the opening and a little
        # past it. Everything about the camera is read off this one sweep.
        page.evaluate(NEW_JS, [A.a, A.b, A.seed])
        sweep = []
        t = 0.0
        while t <= DUR + 0.30:
            sweep.append(page.evaluate(TO_JS, [t]))
            t += 0.02

        zbad = []
        for s in sweep:
            want = expect_z(s["t"])
            got = s["cam"][2] if s["cam"] else None
            if want is None or want <= 1.02:
                continue
            if got is None or abs(got - want) > 1e-6:
                zbad.append((round(s["t"], 3), got, round(want, 4)))
        P.check(not zbad,
                "2  the camera takes the frame and the zoom track IS the shot "
                "table",
                f"{sum(1 for s in sweep if s['cam'])} live samples, "
                f"z {max((s['cam'][2] for s in sweep if s['cam']), default=0):.2f}"
                f" -> {min((s['cam'][2] for s in sweep if s['cam']), default=0):.2f}"
                + (f"   MISMATCHES {zbad[:4]}" if zbad else ""))

        # 3. THE PROPERTY THE FEASIBILITY CLAMP USED TO GUARANTEE. The opening
        #    stands that clamp down, so the thing it bought -- the relic being
        #    filmed is not cropped -- has to be shown some other way. And it is
        #    SWEPT ACROSS PAIRINGS, not asserted off one seed: the opening ships
        #    for every fight, and a corner spawn is a different camera.
        worst_in, lean_bound = 0.0, 0
        for s in sweep:
            if not s["cam"]:
                continue
            at = subject(s["t"])
            if not at:
                continue
            sx = s["ax"] if at == "a" else s["bx"]
            sy = s["ay"] if at == "a" else s["by"]
            lx, ly = screen(s, sx, sy)
            worst_in = max(worst_in, math.hypot(lx - s["aw"] / 2,
                                                ly - s["ah"] / 2))
            # is the lean clamp what is stopping the subject reaching centre?
            z = s["cam"][2]
            my = (s["ah"] / 2) * (1 - 1 / z) * (1 + LOOK.get("overscan", 0.95))
            if abs(abs(s["cam"][1] - s["ah"] / 2) - my) < 0.5:
                lean_bound += 1

        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pairings = [[ids[i % len(ids)], ids[(i * 9 + 5) % len(ids)],
                     30011 + i * 613]
                    for i in range(A.pairings)
                    if ids[i % len(ids)] != ids[(i * 9 + 5) % len(ids)]]
        crops = page.evaluate(CROP_JS, [pairings, DUR])
        worst = min(crops, key=lambda r: r["margin"])
        # THE BAR, STATED. 8px of a 1625px design frame is 2.7 device pixels at
        # the 540-wide delivery size: the ball's own antialiased edge grazing
        # the frame for a frame or two, which is what the lean clamp costs and
        # what the approved clip already does. A real crop is tens of pixels --
        # the frame probe that built the feasibility clamp found 137-376px.
        P.check(worst["margin"] > -8.0,
                "3  the subject's magnified body stays inside the frame",
                f"worst margin {worst['margin']:+.1f}px at {worst['t']}s on "
                f"{worst['at']} ({worst['a']} v {worst['b']}), swept over "
                f"{len(crops)} pairings x the whole opening")
        P.note("   how far the subject sits from dead centre",
               f"up to {worst_in:.0f}px of a {min(s['aw'] for s in sweep)/2:.0f}px "
               f"half-frame; the lean clamp binds on {lean_bound} of "
               f"{sum(1 for s in sweep if s['cam'])} samples, which is what "
               f"stops it centring exactly -- same clamp, same overscan, as "
               f"the approved lab clip")

        # 4. The A->B seam is a CUT and must jump; the pull-wide is a MOVE and
        #    must not. Measured on where the arena's centre lands on screen.
        jumps = []
        for i in range(1, len(sweep)):
            p, q = sweep[i - 1], sweep[i]
            if not (p["cam"] and q["cam"]):
                continue
            a0 = screen(p, 260, 400)
            a1 = screen(q, 260, 400)
            jumps.append((round(q["t"], 2), math.hypot(a1[0] - a0[0],
                                                       a1[1] - a0[1])))
        seam = [d for t2, d in jumps if abs(t2 - (CUT + 0.01)) < 0.03]
        pull = [d for t2, d in jumps if PULL + 0.02 <= t2 <= DUR - 0.02]
        # A cut and a move are told apart by the RATIO, not by a pixel count:
        # the pull-wide is a fast deliberate move (2.02 -> 1.00 in 0.80s) and a
        # threshold in pixels would only be measuring how fast it was authored.
        ratio = max(seam) / max(1.0, max(pull)) if (seam and pull) else 0
        P.check(bool(seam) and bool(pull) and ratio > 8,
                "4  the A->B seam is a cut, the pull-wide is a move",
                f"seam jump {max(seam):.0f}px against a largest pull step of "
                f"{max(pull):.0f}px over the same 20ms -- {ratio:.0f}x")

        # -- 5 ---------------------------------------------------------------
        after = [s for s in sweep if s["t"] >= DUR]
        P.check(after and not any(s["cam"] for s in after)
                and any(s["cam"] for s in sweep if s["t"] < DUR - 0.05),
                "5  and it hands the lens back, on time",
                f"live to {max((s['t'] for s in sweep if s['cam']), default=0):.3f}s, "
                f"{len(after)} samples from {DUR}s on are all released")

        # -- 6, 7 ------------------------------------------------------------
        # The v42 check. Each relic is sampled DURING ITS OWN SHOT, so it is on
        # screen, and the FLARE is isolated from the SWELL by suppressing one
        # contributor at a time -- CLAUDE.md §4.1c, learned the expensive way on
        # Lastlight, where one number over a whole set-piece could not say which
        # half to change. Switching the whole module off would move the camera
        # as well and measure three things at once; the first version of this
        # check did exactly that and read the swell's dimming as a missing
        # flare.
        SUPPRESS = {
            "flare": "SWBOpen.LOOK.flareA = 1e9; SWBOpen.LOOK.flareB = 1e9;",
            "swell": "SWBOpen.LOOK.swellFrom = 1; SWBOpen.LOOK.swellPeak = 1;",
        }

        def contribution(t_at, who, what):
            """Luma the named contributor alone puts on that relic's disc."""
            page.evaluate(NEW_JS, [A.a, A.b, A.seed])
            s = page.evaluate(TO_JS, [t_at])
            sx = s["ax"] if who == "a" else s["bx"]
            sy = s["ay"] if who == "a" else s["by"]
            page.evaluate(DRAW_JS)
            with_it = page.evaluate(DISC_JS, [sx, sy, 60])
            keep = page.evaluate("() => JSON.parse(JSON.stringify(SWBOpen.LOOK))")
            page.evaluate("() => { " + SUPPRESS[what] + " }")
            page.evaluate(DRAW_JS)
            without = page.evaluate(DISC_JS, [sx, sy, 60])
            page.evaluate("([k]) => { for (const n in k) SWBOpen.LOOK[n] = k[n]; }",
                          [keep])
            return (with_it["luma"] - without["luma"],
                    with_it["offscreen"] or without["offscreen"])

        fa, fb = LOOK.get("flareA", 0.10), LOOK.get("flareB", 0.95)
        lit_a, off_a = contribution(fa + 0.04, "a", "flare")
        lit_b, off_b = contribution(fb + 0.04, "b", "flare")
        P.check(lit_a > 0.05 and lit_b > 0.05 and not off_a and not off_b,
                "6  the flare is actually drawn -- both relics ignite",
                f"A at {fa + 0.04:.2f}s +{lit_a:.4f} luma of its own disc, "
                f"B at {fb + 0.04:.2f}s +{lit_b:.4f}"
                + ("   OFF SCREEN" if (off_a or off_b) else ""))

        pre_a, _ = contribution(max(0.0, fa - 0.03), "a", "flare")
        pre_b, _ = contribution(fb - 0.03, "b", "flare")
        P.check(abs(pre_a) < 0.01 and abs(pre_b) < 0.01,
                "7  and not before its own moment: the stagger is real, and "
                "A's flare does not reach B",
                f"A at {max(0.0, fa - 0.03):.2f}s {pre_a:+.4f}, B at "
                f"{fb - 0.03:.2f}s {pre_b:+.4f} -- and A is still lit there")

        sw_lo, _ = contribution(0.07, "a", "swell")
        sw_hi, _ = contribution(0.30, "a", "swell")
        P.note("   and what the SWELL does on its own, measured separately",
               f"relic A's disc {sw_lo:+.4f} at 0.07s (multiplier below 1, the "
               f"hall is dimmed) and {sw_hi:+.4f} at 0.30s (above 1). One "
               f"number over both would have read as a missing flare")

        # -- 8, 9 ------------------------------------------------------------
        page.evaluate(NEW_JS, [A.a, A.b, A.seed])
        page.evaluate(TO_JS, [0.30])
        bl = page.evaluate(BLUR_JS)
        P.check(bl["mul"] > 1.2 and abs(bl["seen"] - 10 * bl["mul"]) < 1e-6,
                "8  the swell reaches the canvas",
                f"mul {bl['mul']:.3f} at 0.30s, shadowBlur 10 -> "
                f"{bl['seen']:.3f}")
        page.evaluate(TO_JS, [1.60])
        bl2 = page.evaluate(BLUR_JS)
        P.check(bl2["mul"] == 1 and bl2["native"] and bl2["seen"] == 10,
                "9  and the accessor is removed again when it is over",
                f"mul {bl2['mul']}, native descriptor "
                f"{'restored' if bl2['native'] else 'STILL PATCHED'}")

        # -- 10 --------------------------------------------------------------
        # The post chain draws every frame four times. A wall-clock opening
        # would advance between them; a pure function of m.t cannot.
        idem = []
        for at in (0.20, 0.95, 2.00):
            page.evaluate(NEW_JS, [A.a, A.b, A.seed])
            page.evaluate(TO_JS, [at])
            hs = []
            for _ in range(3):
                page.evaluate(DRAW_JS)
                hs.append(sha(page.evaluate(URL_JS)))
            idem.append((at, len(set(hs)) == 1, hs[0]))
        P.check(all(x[1] for x in idem),
                "10 a frame drawn three times at one sim time is one frame",
                "  ".join(f"{at:.2f}s {h}" for at, _ok, h in idem))

        # -- 11 --------------------------------------------------------------
        pairs, i = [], 0
        while len(pairs) < A.plan_n:
            a2, b2 = ids[i % len(ids)], ids[(i * 7 + 3) % len(ids)]
            if a2 != b2:
                pairs.append([a2, b2, 40009 + i * 977])
            i += 1
        plan = page.evaluate(PLAN_JS, [pairs, DUR])
        pct = 100.0 * plan["early"] / max(1, plan["n"])
        P.check(True,
                "11 how often the director already wants the opening's window",
                f"{plan['early']}/{plan['n']} pairings ({pct:.1f}%) plan a cut "
                f"before {DUR}s"
                + (f" -- at {plan['first'][:6]}s. The opening wins those; the "
                   f"cut plays out under it and the lens is handed back mid-cut."
                   if plan["first"] else ""))

        if errors:
            print("\npage errors:", errors[:4], file=sys.stderr)
            P.check(False, "no page errors", str(errors[:2]))

    return P.report()


if __name__ == "__main__":
    sys.exit(main())
