#!/usr/bin/env python3
"""RED RAZOR POINTS ON THE BLOODSWORN FLAIL -- CANDIDATES, BEFORE ANY BUILD.

    python3 barb_probe.py --game ../02-chain/sc-twinshade-scrunch.html

Rick: "the tips of the flail are red dots. can we change those to red razor
sharp points? fits the bloody theme better imo"

WHAT IS THERE NOW, and it is worse than "a dot":

    c.fillStyle = p.core;
    c.arc(cos(a)*r*1.86, sin(a)*r*1.86, r*0.13, 0, TAU);

**The barb ALREADY comes to a true vertex.** Its outer edge runs to
`P1 = dir(a+0.86)*r*1.94` and the inner edge leaves from the same point, so the
path terminates in a single point. The dot is a filled circle of radius 0.13r
centred 0.08r INSIDE that vertex -- so it spans 1.73r to 1.99r and caps the
point off. **The red dot is not decorating the tip, it is blunting a tip that
was already sharp.** Removing it is most of the fix.

WHAT REPLACES IT, and the reasoning is v37 §8.3 verbatim -- "a flame lick is
wide where it leaves the surface and comes to a POINT; the taper is most of
what makes it read, and no stroke has one":

  * a FILLED path, never a stroke -- a stroke has a cap, and a cap is a blunt
    end no matter how thin the line
  * edges CONCAVE, not straight. Convex reads as a thorn, straight reads as a
    triangle, concave reads as honed. One parameter, `conc`.
  * the point continues the barb's OWN TANGENT at the vertex -- `P1 - C1` for a
    quadratic -- so it grows out of the hook instead of being glued on
    radially. That tangent is 1.07 rad off radial: these barbs hook hard, and a
    point that ignored it would read as a spike on a hook rather than a hook
    that has been sharpened.
  * a second needle sharing the apex, in `p.glow`, as the light on the edge.
    Candidate E is the control that says whether it earns its place.

Every candidate is injected at runtime over `SHAPES._fhBarbed` and the page is
thrown away. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "05-reference" / "v38"

# One code path, parameterised, so the candidates differ only in their numbers
# and a difference on the sheet cannot be an accident of two separate rewrites.
# `tip` selects the treatment: "dot" is the shipped behaviour, kept as the
# baseline column so the comparison is against the real thing and not against
# a re-typed version of it.
MAKE_JS = r"""(cfg) => {
  const TAU = Math.PI * 2;
  const S = AC.SHAPES;
  S._fhBarbed = function(c, D, p, spin){
    const r = D * 0.34;
    c.save();
    c.rotate(spin);
    c.fillStyle = S._shade(p.steel, 0.58, 0.42);
    c.strokeStyle = S._shade(p.steel, 0.20, 0.52);
    c.lineWidth = Math.max(1, D*0.018);
    for (let i = 0; i < 7; i++){
      const a = (i / 7) * TAU;
      c.beginPath();
      c.moveTo(Math.cos(a - 0.22) * r * 0.92, Math.sin(a - 0.22) * r * 0.92);
      c.quadraticCurveTo(Math.cos(a + 0.34) * r * 1.70,
                         Math.sin(a + 0.34) * r * 1.70,
                         Math.cos(a + 0.86) * r * 1.94,
                         Math.sin(a + 0.86) * r * 1.94);
      c.quadraticCurveTo(Math.cos(a + 0.34) * r * 1.24,
                         Math.sin(a + 0.34) * r * 1.24,
                         Math.cos(a + 0.24) * r * 0.92,
                         Math.sin(a + 0.24) * r * 0.92);
      c.closePath(); c.fill(); c.stroke();
    }
    S._fhBall(c, D, p);

    if (cfg.tip === "dot"){
      c.fillStyle = p.core;
      for (let i = 0; i < 7; i++){
        const a = (i / 7) * TAU + 0.86;
        c.beginPath();
        c.arc(Math.cos(a) * r * 1.86, Math.sin(a) * r * 1.86, r * 0.13, 0, TAU);
        c.fill();
      }
      c.restore(); return;
    }

    const d = (ang, k) => [Math.cos(ang) * r * k, Math.sin(ang) * r * k];
    const q = (A, C, B, t) => { const u = 1 - t;
      return [u*u*A[0] + 2*u*t*C[0] + t*t*B[0],
              u*u*A[1] + 2*u*t*C[1] + t*t*B[1]]; };
    const lp = (u, v, t) => [u[0] + (v[0]-u[0])*t, u[1] + (v[1]-u[1])*t];

    for (let i = 0; i < 7; i++){
      const a = (i / 7) * TAU;
      /* The barb's own control net, restated. If these drift from the loop
         above the point detaches from the barb, which is the one way this can
         fail while still looking like something. */
      const P0 = d(a - 0.22, 0.92), C1 = d(a + 0.34, 1.70),
            P1 = d(a + 0.86, 1.94), C2 = d(a + 0.34, 1.24), P2 = d(a + 0.24, 0.92);
      const B1 = q(P0, C1, P1, cfg.back);     // base, leading edge
      const B2 = q(P1, C2, P2, cfg.front);    // base, trailing edge
      let tx = P1[0] - C1[0], ty = P1[1] - C1[1];       // tangent at the vertex
      const tl = Math.hypot(tx, ty) || 1; tx /= tl; ty /= tl;
      const AP = [P1[0] + tx * r * cfg.len, P1[1] + ty * r * cfg.len];

      const k1 = lp(lp(B1, AP, 0.5), B2, cfg.conc);
      const k2 = lp(lp(AP, B2, 0.5), B1, cfg.conc);
      c.fillStyle = p.core;
      c.beginPath();
      c.moveTo(B1[0], B1[1]);
      c.quadraticCurveTo(k1[0], k1[1], AP[0], AP[1]);
      c.quadraticCurveTo(k2[0], k2[1], B2[0], B2[1]);
      c.closePath(); c.fill();

      if (cfg.glow > 0){
        /* The light ON the edge. Same apex -- two filled paths that share a
           vertex are still one point; an outline stroked round the whole thing
           would round it off exactly the way the dot did. */
        const G2 = lp(B1, B2, cfg.glowW);
        const g1 = lp(lp(B1, AP, 0.5), G2, cfg.conc);
        const g2 = lp(lp(AP, G2, 0.5), B1, cfg.conc);
        c.globalAlpha = cfg.glow;
        c.fillStyle = p.glow;
        c.beginPath();
        c.moveTo(B1[0], B1[1]);
        c.quadraticCurveTo(g1[0], g1[1], AP[0], AP[1]);
        c.quadraticCurveTo(g2[0], g2[1], G2[0], G2[1]);
        c.closePath(); c.fill();
        c.globalAlpha = 1;
      }
    }
    c.restore();
  };
  return "installed " + cfg.name;
}"""

HEAD_JS = """([D, zoom]) => {
  const cv = document.createElement("canvas");
  const S = Math.round(D * 2.9);
  cv.width = S * zoom; cv.height = S * zoom;
  const c = cv.getContext("2d");
  c.scale(zoom, zoom);
  c.fillStyle = "#0B0912"; c.fillRect(0, 0, S, S);
  c.translate(S/2, S/2);
  AC.SHAPES.flailHead(c, D, AC.AFFINITIES.bloodsworn, 0.7);
  return cv.toDataURL("image/png");
}"""

ARENA_JS = """([a, b, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = 0;
  for (let i = 0; i < Math.round(secs / DT); i++) m.step(DT);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

# THE LENGTH LADDER. Rick, having seen the five above: "flail head looks good
# but lets shorten those spikes a bit." Everything except `len` is held at
# candidate B, so this ladder is one variable and the eye is not being asked to
# trade two things off at once.
LADDER = [dict(name=f"{L:.2f}" + ("  <- B, shown before" if abs(L-0.42) < 1e-9 else ""),
               tip="razor", len=L, conc=0.18, back=0.72, front=0.30,
               glow=0.85, glowW=0.34)
          for L in (0.42, 0.36, 0.30, 0.24, 0.18)]

CANDIDATES = [
    dict(name="A  SHIPPED  red dots", tip="dot"),
    dict(name="B  needle       L .42", tip="razor", len=0.42, conc=0.18,
         back=0.72, front=0.30, glow=0.85, glowW=0.34),
    dict(name="C  long claw    L .62", tip="razor", len=0.62, conc=0.26,
         back=0.66, front=0.34, glow=0.85, glowW=0.34),
    dict(name="D  short fang   L .30", tip="razor", len=0.30, conc=0.10,
         back=0.76, front=0.26, glow=0.85, glowW=0.34),
    dict(name="E  needle, NO edge light", tip="razor", len=0.42, conc=0.18,
         back=0.72, front=0.30, glow=0.0, glowW=0.34),
]


def png(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def sheet(imgs, labels, out, scale, title):
    tw, th = int(imgs[0].width * scale), int(imgs[0].height * scale)
    PAD, LBL = 14, 30
    sh = Image.new("RGB", (len(imgs) * (tw + PAD) + PAD, th + PAD * 2 + LBL), (11, 9, 18))
    dr = ImageDraw.Draw(sh)
    dr.text((PAD, 7), title, fill=(224, 58, 78))
    for i, (im, lab) in enumerate(zip(imgs, labels)):
        x = PAD + i * (tw + PAD)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, PAD + LBL))
        dr.text((x + 2, PAD + LBL - 14), lab, fill=(214, 200, 170))
    sh.save(out)
    print(f"  {out.name}  ({sh.width}x{sh.height})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--only", default=None, help="comma-separated candidate letters")
    ap.add_argument("--ladder", action="store_true", help="sweep point length only")
    ap.add_argument("--built", action="store_true",
                    help="draw the FILE'S OWN _fhBarbed -- no injection. "
                         "this is what verifies a build rather than a candidate.")
    A = ap.parse_args()
    gp = (HERE / A.game).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    cands = LADDER if A.ladder else CANDIDATES
    if A.only and not A.ladder:
        keep = set(A.only.upper().split(","))
        cands = [c for c in CANDIDATES if c["name"][0] in keep]

    print(f"\nBARB PROBE -- red razor points, {len(cands)} candidates")
    print(f"  build {gp.name}   NOTHING IS WRITTEN\n")

    with game(game_path=gp) as (page, errors):
        # The relic has to exist for the arena shot; same runtime overwrite the
        # look-first probe used, and just as thrown away.
        page.evaluate("""(r) => { const w = AC.WEAPONS.find(x => x.id === r.id);
          for (const k of Object.keys(w)) delete w[k]; Object.assign(w, r); }""",
          {"id": "axiom", "name": "Provisional", "aff": "bloodsworn", "shape": "flail",
           "blades": [0], "reach": 96, "width": 22, "artW": 52, "dmg": 43.3,
           "spin": 2.2, "mode": "chain", "mass": 3.6, "onHit": {"hemorrhage": 2},
           "ult": {"name": "Placeholder", "charge": 16, "kind": "nova", "radius": 240,
                   "dmg": 12, "apply": {"hemorrhage": 3}, "knock": 200,
                   "tip": "PLACEHOLDER -- nova: 12 damage, 3 Hemorrhage, knockback"},
           "blurb": "Provisional. Injected at runtime; nothing is built."})

        if A.built:
            # No injection at all. The point of this mode is to photograph what
            # the FILE draws, so anything installed over the top would make the
            # check pass on a build that shipped the dot.
            src = page.evaluate("() => AC.SHAPES._fhBarbed.toString()")
            has_needle = page.evaluate("() => typeof AC.SHAPES._needle === 'function'")
            print(f"   _needle present: {has_needle}")
            print(f"   _fhBarbed still draws a circle: {'arc(' in src}")
            if not has_needle or "arc(" in src or "_needle" not in src:
                raise SystemExit("  FAIL: this build does not carry the razor tips")
            cands = [dict(name="AS BUILT")]

        big, small, halls, labels = [], [], [], []
        for cfg in cands:
            if not A.built:
                print("   " + page.evaluate(MAKE_JS, cfg))
            big.append(png(page.evaluate(HEAD_JS, [52, 6])))
            small.append(png(page.evaluate(HEAD_JS, [52, 1])))
            halls.append(png(page.evaluate(ARENA_JS, ["axiom", "slagheart", 337, 4.33])))
            labels.append(cfg["name"])

        sheet(big, labels, OUT / ("barb-built-6x.png" if A.built else "barb-len-6x.png" if A.ladder else "barb-tips-6x.png"), 1.0,
              ("POINT LENGTH LADDER -- 6x. everything but `len` held at candidate B"
               if A.ladder else
               "RED RAZOR POINTS -- 6x, drawn through SHAPES.flailHead at D=52"))
        # 1:1 is the one that decides it. The head is 52px across in the game and
        # every candidate below looks fine at 6x.
        sheet(small, labels, OUT / ("barb-built-1to1.png" if A.built else "barb-len-1to1.png" if A.ladder else "barb-tips-1to1.png"), 5.0,
              "THE SAME FIVE AT 1:1 (52px), nearest-neighbour blown up 5x -- "
              "THIS is what a viewer sees")
        sheet(halls, labels, OUT / ("barb-built-hall.png" if A.built else "barb-len-hall.png" if A.ladder else "barb-tips-hall.png"), 0.26,
              "IN THE HALL, t=4.3s, vs Slagheart")
        if errors:
            print("  PAGE ERRORS:", errors[:3])
    print(f"\n  sheets in {OUT}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
