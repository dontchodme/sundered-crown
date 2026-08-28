#!/usr/bin/env python3
"""ULT SET-PIECES FOR THE LAST SIX BARE RELICS.

    python3 ultart2_build.py --src sc-gs7-ults.html --out sc-ults-all.html

`ultart_build.py` did the four new greatswords. These are the six that were
already in the roster and never got art: the three `roster15_build` relics
(Aureole, Censer, Emberedge) and the two vigil relics (Lightkeeper, Farwarden),
plus Ironhail — whose Quarrelstorm is **fourteen full-damage arrows** and draws
nothing at all. After this, all sixteen have a set-piece.

WHAT EACH ONE HAD TO AVOID
--------------------------
Sanctified and dwarven now carry three relics each, so "distinct from its
school-mate" is a harder constraint here than it was for the greatswords —
Benediction has to differ from BOTH Judgement and Consecration.

  Quarrelstorm  The volley already spawns fourteen real projectiles that
                `drawShots` draws. So the set-piece is deliberately NOT arrows:
                it is the RELEASE — a ring of muzzle flares and the recoil
                blown back off the mount. Drawing arrows here would double
                every one of them.

  Bulwark       vs Mountainfall (earth fissures) and Exsanguinate (fangs) —
                the other two novas. This one is GEOMETRIC: interlocking
                plates of light, tilting as they pass. Vigil banks damage as
                plate; the nova is that plate let go.

  Reprisal      not a strike at all — an `aimedshot` has a DRAW, and the arrow
                is a projectile drawn elsewhere. So this is the wind-up: the
                ward pool spiralling inward and compressing to a point, with
                the aim line steadying as the spin comes round.

  Benediction   vs Judgement (a vertical pillar falling) — a bow does not call
                light down, it sends it out. Horizontal lance along the shot
                line, halo rings opening at the target, and the heal drawn as
                rings closing INTO the caster rather than Dawnbringer's rising
                motes.

  Consecration  vs Judgement and Benediction — neither of those touches the
                floor. A censer is swung, and what it leaves is ground made
                holy: glyphs igniting outward in a ring, smoke ribbons over.

  Forgefall     vs Mountainfall — that one breaks the floor open. This one is
                heat: a molten pool that crusts over as it cools, and embers
                thrown up. Same school, opposite element.

FRAME COST
----------
Same rule as the first batch: every `shadowBlur` is on a small stroke, none
above 20, nothing blurred whose bounding box is the canvas. The wall-glow work
this session priced a single full-canvas blur at 2.07 Mpx and set-pieces are
already the frame's worst moment.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

UNDER = r'''
    /* ---- Quarrelstorm: the dust the release blows off the floor ------------ */
    else if (u.w === "ironhail"){
      const ex = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - 0.35) / 0.8, 0, 1);
      const R = 210 * (1 - Math.pow(1 - ex, 2.6));
      c.globalAlpha = 0.5 * fade * (1 - ex * 0.5);
      c.strokeStyle = "#8A6A3A"; c.lineWidth = 9 * (1 - ex * 0.6);
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.stroke();
    }

    /* ---- Bulwark: the plates' footprint, a tiled ring ---------------------- */
    else if (u.w === "lightkeeper"){
      const ex = clamp(u.t / 0.34, 0, 1);
      const fade = 1 - clamp((u.t - 0.4) / 0.85, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.4));
      const N = 18;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 0.5;
        c.globalAlpha = 0.4 * fade * (1 - ex * 0.4);
        c.strokeStyle = "#F06BB8"; c.lineWidth = 2;
        c.beginPath();
        c.arc(u.x, u.y, Math.max(1, R), a, a + TAU / N * 0.62);
        c.stroke();
      }
    }

    /* ---- Reprisal: the draw ring, tightening as the shot is held ----------- */
    else if (u.w === "farwarden"){
      const p = clamp(u.t / Math.max(0.001, u.life * 0.7), 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.72) / (u.life * 0.28), 0, 1);
      c.globalAlpha = 0.7 * fade;
      c.strokeStyle = "#F06BB8"; c.lineWidth = 2.4;
      c.beginPath(); c.arc(u.x, u.y, 150 * (1 - p * 0.72), 0, TAU); c.stroke();
      c.globalAlpha = 0.35 * fade;
      c.lineWidth = 1.2;
      c.beginPath(); c.arc(u.x, u.y, 150, 0, TAU); c.stroke();
    }

    /* ---- Benediction: the lit ground under the blessing -------------------- */
    else if (u.w === "aureole"){
      const open = clamp((u.t - 0.06) / 0.24, 0, 1);
      const fade = 1 - clamp((u.t - 0.45) / 0.95, 0, 1);
      c.globalAlpha = 0.5 * fade * open;
      const g = c.createRadialGradient(u.tx, u.ty, 3, u.tx, u.ty, 150 * open);
      g.addColorStop(0, "#FFF6E2AA"); g.addColorStop(1, "#FFF6E200");
      c.fillStyle = g;
      c.beginPath(); c.ellipse(u.tx, u.ty, 150 * open, 62 * open, 0, 0, TAU); c.fill();
    }

    /* ---- Consecration: glyphs igniting outward across the floor ------------ */
    else if (u.w === "censer"){
      const ex = clamp(u.t / 0.40, 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 0.9, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.2));
      const N = 12;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 0.4;
        const rr = R * (0.55 + 0.45 * shellHash(51, i));
        const lit = clamp((R - rr) / 60, 0, 1);
        if (lit <= 0) continue;
        this._glyph(c, u.x + Math.cos(a) * rr, u.y + Math.sin(a) * rr,
                    13, u.t * 1.2 + i, "#C9A227", fade * lit * 0.9);
      }
      c.globalAlpha = 0.35 * fade * (1 - ex * 0.6);
      c.strokeStyle = "#C9A227"; c.lineWidth = 3;
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.stroke();
    }

    /* ---- Forgefall: a molten pool, crusting over as it cools --------------- */
    else if (u.w === "emberedge"){
      const ex = clamp(u.t / 0.32, 0, 1);
      const cool = clamp((u.t - 0.35) / 0.9, 0, 1);
      const fade = 1 - clamp((u.t - 0.8) / 0.8, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.5));
      /* ALPHA AND FALLOFF, both cut hard from the first version. At 0.85 with
         a stop at 0.55 this washed the entire arena orange and hid the target
         behind its own light — a radius-220 nova reading bigger than
         Mountainfall at 300. A pool is a thing on the floor with an edge; it
         is not a light source for the hall. */
      c.globalAlpha = 0.55 * fade;
      const g = c.createRadialGradient(u.x, u.y, 4, u.x, u.y, Math.max(1, R));
      /* the pool goes from white-hot to a dark crust; `cool` is the only
         thing moving after the first third, which is what says "quenched" */
      const hot = cool > 0.6 ? "#3A1A08" : (cool > 0.25 ? "#B4491A" : "#FFD08A");
      g.addColorStop(0, hot + "DD"); g.addColorStop(0.30, "#8A2E0E66");
      g.addColorStop(0.62, "#8A2E0E1A"); g.addColorStop(1, "#8A2E0E00");
      c.fillStyle = g;
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.fill();
      for (let i = 0; i < 9; i++){                 // crust lines
        const a = shellHash(61, i) * TAU;
        c.globalAlpha = 0.55 * fade * cool;
        c.strokeStyle = "#25120A"; c.lineWidth = 3.4;
        this._jag(c, u.x, u.y, u.x + Math.cos(a) * R, u.y + Math.sin(a) * R,
                  6, 12, 610 + i, 1);
      }
    }
'''

OVER = r'''
    /* ---- Quarrelstorm: the RELEASE. Not arrows — drawShots draws those ----- */
    else if (u.w === "ironhail"){
      const flash = 1 - clamp(u.t / 0.22, 0, 1);
      const fade  = 1 - clamp((u.t - 0.2) / 0.7, 0, 1);
      const N = 14;                                 // == u.shots
      if (flash > 0){
        c.save();
        c.globalCompositeOperation = "lighter";
        for (let i = 0; i < N; i++){
          const a = (i / N) * TAU;
          const l = 26 + 66 * flash;
          c.globalAlpha = flash * 0.95;
          c.strokeStyle = "#E8A34E"; c.lineWidth = 3.4 * flash + 1;
          c.shadowColor = "#E8A34E"; c.shadowBlur = 14;
          c.beginPath();
          c.moveTo(u.x + Math.cos(a) * 22, u.y + Math.sin(a) * 22);
          c.lineTo(u.x + Math.cos(a) * (22 + l), u.y + Math.sin(a) * (22 + l));
          c.stroke();
        }
        c.shadowBlur = 0;
        c.restore();
      }
      /* the mount kicks: a hard ring thrown back off the release */
      const ex = clamp(u.t / 0.26, 0, 1);
      c.globalAlpha = fade * (1 - ex) * 0.9;
      c.strokeStyle = "#FFD9A0"; c.lineWidth = 4 * (1 - ex) + 1;
      c.beginPath(); c.arc(u.x, u.y, 20 + 120 * ex, 0, TAU); c.stroke();
    }

    /* ---- Bulwark: interlocking plates of light, let go ---------------------- */
    else if (u.w === "lightkeeper"){
      const ex = clamp(u.t / 0.34, 0, 1);
      const fade = 1 - clamp((u.t - 0.4) / 0.85, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.4));
      const N = 18;
      c.save();
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 0.5;
        const w = TAU / N * 0.60;
        const h = 26 * (1 - ex * 0.45);
        c.save();
        c.translate(u.x + Math.cos(a + w / 2) * R, u.y + Math.sin(a + w / 2) * R);
        /* each plate TILTS as it flies — the thing that makes this read as
           armour let go rather than a ring of light expanding */
        c.rotate(a + w / 2 + Math.PI / 2 + ex * 0.5 * (i % 2 ? 1 : -1));
        c.globalAlpha = fade * (1 - ex * 0.5);
        c.fillStyle = "#F06BB833";
        c.strokeStyle = "#FFD1EC"; c.lineWidth = 2;
        c.shadowColor = "#F06BB8"; c.shadowBlur = 12;
        const wpx = R * w;
        c.beginPath();
        c.moveTo(-wpx / 2, -h / 2); c.lineTo(wpx / 2, -h / 2 + 4);
        c.lineTo(wpx / 2, h / 2 - 4); c.lineTo(-wpx / 2, h / 2);
        c.closePath(); c.fill(); c.stroke();
        c.shadowBlur = 0;
        c.restore();
      }
      c.restore();
    }

    /* ---- Reprisal: the ward spent, spiralling into one point ---------------- */
    else if (u.w === "farwarden"){
      const p = clamp(u.t / Math.max(0.001, u.life * 0.7), 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.72) / (u.life * 0.28), 0, 1);
      /* plates drawn IN, not thrown out — the pool becoming the arrow */
      for (let i = 0; i < 10; i++){
        const q = clamp(p * 1.25 - i * 0.045, 0, 1);
        if (q <= 0) continue;
        const a = shellHash(41, i) * TAU + q * 3.2;
        const rr = 150 * (1 - q);
        c.save();
        c.translate(u.x + Math.cos(a) * rr, u.y + Math.sin(a) * rr);
        c.rotate(a + q * 4);
        c.globalAlpha = fade * (1 - q * 0.55);
        c.fillStyle = "#F06BB855";
        c.strokeStyle = "#FFD1EC"; c.lineWidth = 1.8;
        c.beginPath();
        c.moveTo(-13, -7); c.lineTo(13, -4); c.lineTo(13, 4); c.lineTo(-13, 7);
        c.closePath(); c.fill(); c.stroke();
        c.restore();
      }
      /* the aim line steadies as the spin comes round */
      c.globalAlpha = fade * p * 0.8;
      c.strokeStyle = "#FFD1EC"; c.lineWidth = 1.6;
      c.setLineDash([9, 11]);
      c.beginPath(); c.moveTo(u.x, u.y); c.lineTo(tgt.x, tgt.y); c.stroke();
      c.setLineDash([]);
      c.globalAlpha = fade * p;
      c.fillStyle = "#FFFFFF";
      c.shadowColor = "#F06BB8"; c.shadowBlur = 18;
      c.beginPath(); c.arc(u.x, u.y, 5 + 7 * p, 0, TAU); c.fill();
      c.shadowBlur = 0;
    }

    /* ---- Benediction: sent OUT, not called down ---------------------------- */
    else if (u.w === "aureole"){
      const open = clamp((u.t - 0.06) / 0.20, 0, 1);
      const fade = 1 - clamp((u.t - 0.42) / 1.0, 0, 1);
      const dx = u.tx - u.x, dy = u.ty - u.y, L = Math.hypot(dx, dy) || 1;
      c.save();
      c.globalCompositeOperation = "lighter";
      /* the lance, along the shot line. Judgement falls vertically; a bow
         sends its blessing where it was aimed. */
      c.save();
      c.translate(u.x, u.y); c.rotate(Math.atan2(dy, dx));
      const w = 34 * open * (0.4 + 0.6 * fade);
      const g = c.createLinearGradient(0, -w, 0, w);
      g.addColorStop(0, "#FFF6E200"); g.addColorStop(0.5, "#FFFFFFCC");
      g.addColorStop(1, "#FFF6E200");
      c.fillStyle = g; c.globalAlpha = 0.55 * fade;
      /* THE LANCE STARTS AT THE SHELL, NOT AT THE CENTRE. It was drawn from
         (0,0) -- the caster's own middle -- as a `lighter` bar whose centre
         stop is #FFFFFFCC, so its first 34px sat on top of a sanctified body
         already near white. Same fault Daybreak's corona had, different
         shape: measured 0.506 bare -> 0.663 on the disc with 18.7% of it past
         0.98. The bar is otherwise unchanged -- same width, same gradient,
         same alpha, same length to the target. */
      const R0 = CONFIG.physics.ballR * 1.06;
      c.fillRect(R0, -w, Math.max(0, L * open - R0), w * 2);
      c.restore();
      /* halo rings opening at the target */
      for (let i = 0; i < 3; i++){
        const q = clamp(open * 1.2 - i * 0.18, 0, 1);
        if (q <= 0) continue;
        c.globalAlpha = fade * (1 - q * 0.6) * 0.9;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 3 - i * 0.6;
        c.shadowColor = "#FFF6E2"; c.shadowBlur = 16;
        c.beginPath(); c.arc(u.tx, u.ty, 26 + q * (58 + i * 30), 0, TAU); c.stroke();
        c.shadowBlur = 0;
      }
      /* the heal: rings CLOSING into the caster — Dawnbringer's motes rise,
         these contract, so the two sanctified heals do not read alike */
      for (let i = 0; i < 4; i++){
        const q = (u.t * 0.85 + i / 4) % 1;
        c.globalAlpha = (1 - q) * fade * 0.85;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 2.2;
        /* They CONTRACT INTO the caster, and they used to contract THROUGH
           it: r fell to 16 against a ball radius of 34, so the last third of
           every ring was stroked white across the body. Floored at the shell
           -- they now land ON it, which is the read the comment above always
           claimed. The outer radius is held at its old 90 so the gesture is
           the same size it was. */
        const rIn = CONFIG.physics.ballR * 1.06, rOut = 90;
        c.beginPath(); c.arc(src.x, src.y, rIn + (1 - q) * (rOut - rIn), 0, TAU);
        c.stroke();
      }
      c.restore();
    }

    /* ---- Consecration: the censer swung, and smoke over holy ground -------- */
    else if (u.w === "censer"){
      const ex = clamp(u.t / 0.40, 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 0.9, 0, 1);
      c.save();
      c.globalCompositeOperation = "lighter";
      for (let arm = 0; arm < 4; arm++){
        c.globalAlpha = 0.5 * fade;
        c.strokeStyle = arm % 2 ? "#C9A227" : "#FFF6E2";
        c.lineWidth = 5 - arm * 0.8;
        c.beginPath();
        for (let j = 0; j <= 30; j++){
          const t2 = j / 30;
          /* ribbons of smoke thrown off a swung censer: an outward spiral,
             wide and slow, nothing like the tight vortex Dirge draws */
          const a = arm * TAU / 4 + t2 * 2.4 + u.t * 1.6;
          const r = u.radius * 0.92 * t2 * ex;
          const px = u.x + Math.cos(a) * r;
          const py = u.y + Math.sin(a) * r * 0.86;
          j ? c.lineTo(px, py) : c.moveTo(px, py);
        }
        c.stroke();
      }
      c.restore();
      for (let i = 0; i < 14; i++){               // sparks of incense
        const q = (u.t * 0.7 + shellHash(52, i)) % 1;
        const a = shellHash(53, i) * TAU;
        const r = u.radius * 0.8 * q;
        c.globalAlpha = (1 - q) * fade * 0.9;
        c.fillStyle = "#FFE9A8";
        c.beginPath();
        c.arc(u.x + Math.cos(a) * r, u.y + Math.sin(a) * r - q * 30,
              1.6 + (1 - q) * 2, 0, TAU);
        c.fill();
      }
    }

    /* ---- Forgefall: embers thrown up off the quench ------------------------- */
    else if (u.w === "emberedge"){
      const ex = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 0.95, 0, 1);
      c.save();
      c.globalCompositeOperation = "lighter";
      const hit = 1 - clamp(u.t / 0.16, 0, 1);
      if (hit > 0){                                // the blow itself
        c.globalAlpha = hit * 0.75;
        const g = c.createRadialGradient(u.x, u.y, 2, u.x, u.y, 112);
        g.addColorStop(0, "#FFF0C0"); g.addColorStop(0.32, "#E8761A66");
        g.addColorStop(1, "#E8761A00");
        c.fillStyle = g;
        c.beginPath(); c.arc(u.x, u.y, 112, 0, TAU); c.fill();
      }
      for (let i = 0; i < 30; i++){                // embers, rising and dying
        const q = (u.t * 0.62 + shellHash(63, i)) % 1;
        const a = shellHash(64, i) * TAU;
        const r = u.radius * 0.85 * q * (0.4 + shellHash(65, i) * 0.8);
        const rise = q * q * 96;
        c.globalAlpha = (1 - q) * fade;
        /* embers cool as they climb — the colour IS the age of the spark */
        c.fillStyle = q > 0.66 ? "#8A2E0E" : (q > 0.33 ? "#E8761A" : "#FFD08A");
        c.beginPath();
        c.arc(u.x + Math.cos(a) * r, u.y + Math.sin(a) * r * 0.8 - rise,
              1.4 + (1 - q) * 2.6, 0, TAU);
        c.fill();
      }
      c.restore();
      c.globalAlpha = fade * (1 - ex) * 0.85;      // the heat ring
      c.strokeStyle = "#E8761A"; c.lineWidth = 4 * (1 - ex) + 1;
      c.shadowColor = "#E8761A"; c.shadowBlur = 16;
      c.beginPath();
      c.arc(u.x, u.y, u.radius * (1 - Math.pow(1 - ex, 2.5)), 0, TAU); c.stroke();
      c.shadowBlur = 0;
    }
'''

LIFE_OLD = """              oathwound: 1.5, heartwood: 2.2, nightfell: 1.4,
              axiom: 1.5 }[f.w.id] || 1.5,"""
LIFE_NEW = """              oathwound: 1.5, heartwood: 2.2, nightfell: 1.4,
              axiom: 1.5,
              /* The last six. Reprisal is the outlier and it is not a strike:
                 an aimedshot holds a DRAW until the bow's facing comes round,
                 so its art has to still be on screen when the arrow finally
                 leaves. The rest end. */
              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,
              aureole: 1.6, censer: 1.6,
              emberedge: 1.5 }[f.w.id] || 1.5,"""

ANCHOR_UNDER = """    c.restore();
  }

  /* Above the fighters: light, blades, vines, bolts, dust. */
  drawUltOver(m){"""

ANCHOR_OVER = """    c.restore();
  }

  /* ----------------------------------------------------------- fighter --- */"""

CHECK_JS = r"""
(ids) => {
  const out = [];
  for (const id of ids){
    const w = AC.WEAPONS.find(x => x.id === id);
    const foe = id === "dawnbringer" ? "grudgebearer" : "dawnbringer";
    const m = new AC.Match(id, foe, 0x9A11 + 7);
    AC.setResolution(1080, 1920);
    const f = m.a, fo = m.b;
    const rec = []; let threw = null;
    for (const t of [0.05, 0.25, 0.5, 0.9, 1.3]){
      m.ultFx = { w: id, kind: w.ult.kind, src: "a", tgt: "b",
                  x: f.x, y: f.y, tx: fo.x, ty: fo.y, hit: true,
                  radius: w.ult.radius || 300, aff: f.aff, t: t, life: 2.2,
                  shots: w.ult.shots || 0 };
      const cv = document.getElementById('cv'), c = cv.getContext('2d');
      c.setTransform(1,0,0,1,0,0); c.fillStyle = "#000"; c.fillRect(0,0,1080,1920);
      try { AC.__draw(m); } catch (e) { threw = String(e); break; }
      const a = c.getImageData(0,0,1080,1920).data;
      m.ultFx = null;
      c.setTransform(1,0,0,1,0,0); c.fillStyle = "#000"; c.fillRect(0,0,1080,1920);
      AC.__draw(m);
      const b = c.getImageData(0,0,1080,1920).data;
      let diff = 0;
      for (let i = 0; i < a.length; i += 16)
        if (Math.abs(a[i]-b[i]) + Math.abs(a[i+1]-b[i+1]) + Math.abs(a[i+2]-b[i+2]) > 12) diff++;
      rec.push({ t, px: diff });
    }
    out.push({ id, threw, rec, peak: Math.max(...rec.map(r => r.px), 0) });
  }
  return out;
}
"""

IDS = ["ironhail", "lightkeeper", "farwarden", "aureole", "censer", "emberedge"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="sc-gs7-ults.html")
    ap.add_argument("--out", default="sc-ults-all.html")
    ap.add_argument("--no-check", action="store_true")
    A = ap.parse_args()

    if pathlib.Path(A.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    src = HERE / A.src
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr); return 2
    s = src.read_text(encoding="utf-8")

    for name, anc in (("drawUltUnder tail", ANCHOR_UNDER),
                      ("drawUltOver tail", ANCHOR_OVER),
                      ("ultFx life table", LIFE_OLD)):
        n = s.count(anc)
        if n != 1:
            print(f"! anchor {name} appears {n} times, expected 1.", file=sys.stderr)
            return 3

    s = s.replace(ANCHOR_UNDER, UNDER + ANCHOR_UNDER, 1)
    s = s.replace(ANCHOR_OVER, OVER + ANCHOR_OVER, 1)
    s = s.replace(LIFE_OLD, LIFE_NEW, 1)
    print("  [ultart2] drawUltUnder: 6 branches")
    print("  [ultart2] drawUltOver:  6 branches")
    print("  [ultart2] ultFx life table: 6 durations")

    doc = "<!DOCTYPE html>\n"
    i = s.find(doc)
    if i < 0:
        print("! no doctype", file=sys.stderr); return 4
    stamp = (f"<!-- GENERATED by ultart2_build.py --src {A.src} — "
             f"do not hand-edit or tune in place -->")
    s = s[:i + len(doc)] + stamp + "\n" + s[i + len(doc):]

    out = HERE / A.out
    out.write_text(s, encoding="utf-8")
    print(f"{A.src} -> {A.out}   sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}")
    if A.no_check:
        print("  ! checks skipped"); return 0

    sys.path.insert(0, str(HERE))
    from scpage import game
    with game(game_path=out) as (page, errors):
        rows = page.evaluate(CHECK_JS, IDS)
        if errors:
            print(f"! page errors: {errors[:3]}", file=sys.stderr)
            out.unlink(); return 5

    bad = []
    print(f"\n  {'relic':<13}{'t=.05':>8}{'t=.25':>8}{'t=.5':>8}{'t=.9':>8}{'t=1.3':>8}")
    for r in rows:
        if r["threw"]:
            bad.append(f"{r['id']}: threw {r['threw'][:80]}")
            print(f"  {r['id']:<13}  THREW: {r['threw'][:58]}"); continue
        print(f"  {r['id']:<13}" + "".join(f"{x['px']:>8}" for x in r["rec"]))
        if r["peak"] < 200:
            bad.append(f"{r['id']}: peak {r['peak']} — draws (almost) nothing")

    print()
    if bad:
        print("  ULT ART CHECK FAILED:")
        for b in bad: print("   ", b)
        out.unlink(); print(f"\n  {A.out} deleted.")
        return 6
    print("  ult art check PASS — all six draw and none throws")
    print("  ALL SIXTEEN RELICS NOW HAVE A SET-PIECE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
