#!/usr/bin/env python3
"""FOUR KUNAI, RENDERED BEFORE ANYBODY IS ASKED ANYTHING.

    python kunai_art_lab.py --game ../02-chain/sc-thornshear.html

Rick, watching the first-look clip of the Winnowing:

    "the blades dont look like kunai. lets improve their visuals"
    "kunai first, leaf second"

He is right and the second line is the brief. The shipped shape is a LEAF with
a point on it -- a pointed ellipse, a midrib, no tang and no ring -- so the
verdant flavour is carrying the silhouette and the weapon is carrying nothing.
A kunai is recognisable by three things in this order:

    THE TANG      the object is longer than the blade, and the back half of it
                  is dark and narrow. A blade with no handle is a leaf.
    THE RING      the one feature nothing else in this game has. At the sizes
                  these fly at (37px fresh, 72px fully grown, at --w 540) a
                  ring is four pixels across and it still reads, because it is
                  a HOLE and nothing else on screen is one.
    THE SHOULDER  a kunai's blade widens abruptly and then tapers dead
                  straight. A leaf's widest point is halfway and its edges are
                  convex. That single difference is most of "leaf" against
                  "blade".

So all four candidates below are kunai in silhouette and differ in HOW the
leaf gets in -- which is the order Rick asked for. §3 rule 2: offer a spread,
not a guess, and v43's lesson is that being wrong about the REGISTER is what
costs, and a spread of one can never reveal it.

    A  STEEL KUNAI, LEAF TRAIL   the plant is what it came FROM, not what it
                                 is. Grey blade, dark tang, ring, and two
                                 small leaves streaming off the ring.
    B  LEAF-BLADED KUNAI         kunai furniture, and the blade is a leaf --
                                 convex edges, a bright midrib, green steel.
    C  GROWN KUNAI               the whole object is plant. The tang is a
                                 woody stem, the ring is a curled tendril, the
                                 blade's edge is a leaf margin. This is the
                                 one that matches SHAPES._tbGrown, so the
                                 thrown thing is the weapon in miniature --
                                 the rule the flail's spike already follows.
    D  HARD KUNAI                the strictest reading: a real kunai, dark
                                 steel, no green in the shape at all, and the
                                 school arrives only as the glow around it.

TWO SHEETS, because the question has two halves:

    kunai-shapes.png   the four at 1:1 at every rung, and at 3x. Is it a
                       kunai, and does the GROWTH read?
    kunai-in-hall.png  fourteen of them at once over the real arena, at the
                       real scale, at the angles they actually fly at. Rick
                       watched a hall with forty in it; a silhouette that
                       reads alone and turns to soup in a crowd is the wrong
                       answer, and the first sheet cannot see that.

RUNTIME ONLY. Nothing is written to any build. The chosen branch is pasted
into `thornshear_build.py`'s KUNAI_ART_NEW by hand.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent


# --------------------------------------------------------------- the four ---
# Each candidate is a function of (c, r, rung, P) drawing at the origin along
# +x, exactly as `drawShots` would after its translate/rotate. Written here in
# the form they would be pasted into the build, so what Rick picks is what
# ships rather than a mock-up of it.
CANDS_JS = r"""
window.KUNAI = {};

/* Shared: the halo every candidate carries, so the comparison is of
   SILHOUETTE and not of glow. Lifted from the shipped branch unchanged. */
window.KUNAI._halo = function(c, x, y, r, rung, P){
  const hot = Math.min(1, rung / 3);
  const R = r * (1.6 + 0.9 * hot);
  c.globalCompositeOperation = 'lighter';
  const g = c.createRadialGradient(x, y, 1, x, y, R);
  g.addColorStop(0, P.glow + (rung ? 'AA' : '77'));
  g.addColorStop(1, P.glow + '00');
  c.globalAlpha = 0.45 + 0.35 * hot;
  c.fillStyle = g;
  c.beginPath(); c.arc(x, y, R, 0, Math.PI * 2); c.fill();
  c.globalCompositeOperation = 'source-over';
  c.globalAlpha = 1;
};

/* THE KUNAI SKELETON, shared by all four. One set of proportions, so the
   candidates differ in treatment rather than in size -- otherwise the sheet
   compares two things at once and cannot answer either.

   L is the HALF-length. A kunai is ~3.7r long overall, blade 55%, tang 45%,
   and the ring hangs off the butt. */
window.KUNAI._geom = function(r){
  const L = r * 1.85;
  return { L: L, nose: L, shoulder: L * 0.30, hilt: -L * 0.06,
           butt: -L * 0.74, ring: -L * 0.86, ringR: L * 0.13,
           w: r * 0.52, tw: r * 0.17 };
};

/* A — STEEL KUNAI, LEAF TRAIL. The plant is what it came from. */
window.KUNAI.A = function(c, r, rung, P){
  const G = window.KUNAI._geom(r), hot = Math.min(1, rung / 3);
  /* the two leaves, off the ring and behind it, drawn first so the blade
     sits on top of them */
  c.fillStyle = P.core; c.globalAlpha = 0.85;
  for (const s of [-1, 1]){
    c.beginPath();
    c.moveTo(G.ring, 0);
    c.quadraticCurveTo(G.ring - G.L * 0.30, s * r * 0.30,
                       G.ring - G.L * 0.62, s * r * 0.52);
    c.quadraticCurveTo(G.ring - G.L * 0.30, s * r * 0.08, G.ring, 0);
    c.fill();
  }
  c.globalAlpha = 1;
  /* the tang and the ring, dark */
  c.strokeStyle = '#2A2E28'; c.lineWidth = G.tw * 2;
  c.beginPath(); c.moveTo(G.hilt, 0); c.lineTo(G.butt, 0); c.stroke();
  c.lineWidth = Math.max(1, r * 0.13);
  c.beginPath(); c.arc(G.ring, 0, G.ringR, 0, Math.PI * 2); c.stroke();
  /* the blade: hard shoulder, dead-straight taper */
  c.beginPath();
  c.moveTo(G.nose, 0);
  c.lineTo(G.shoulder, -G.w); c.lineTo(G.hilt, -G.w * 0.34);
  c.lineTo(G.hilt, G.w * 0.34); c.lineTo(G.shoulder, G.w);
  c.closePath();
  c.fillStyle = '#C9D3C6'; c.fill();
  c.strokeStyle = '#EFF6EC'; c.lineWidth = Math.max(0.7, r * 0.07);
  c.beginPath(); c.moveTo(G.nose, 0); c.lineTo(G.shoulder, -G.w); c.stroke();
  if (hot){
    c.globalAlpha = 0.4 + 0.6 * hot;
    c.strokeStyle = P.glow; c.lineWidth = Math.max(0.7, r * 0.08);
    c.beginPath(); c.moveTo(G.nose, 0); c.lineTo(G.shoulder, G.w); c.stroke();
    c.globalAlpha = 1;
  }
};

/* B — LEAF-BLADED KUNAI. Kunai furniture, and the blade is a leaf. */
window.KUNAI.B = function(c, r, rung, P){
  const G = window.KUNAI._geom(r), hot = Math.min(1, rung / 3);
  c.strokeStyle = '#20301F'; c.lineWidth = G.tw * 2;
  c.beginPath(); c.moveTo(G.hilt, 0); c.lineTo(G.butt, 0); c.stroke();
  c.lineWidth = Math.max(1, r * 0.13);
  c.beginPath(); c.arc(G.ring, 0, G.ringR, 0, Math.PI * 2); c.stroke();
  /* the blade: a kunai's shoulder, a leaf's convex edges between shoulder
     and nose */
  const leaf = (k) => {
    c.beginPath();
    c.moveTo(G.nose * k, 0);
    c.quadraticCurveTo(G.shoulder * k, -G.w * 1.30 * k, G.hilt * k, -G.w * 0.36 * k);
    c.lineTo(G.hilt * k, G.w * 0.36 * k);
    c.quadraticCurveTo(G.shoulder * k, G.w * 1.30 * k, G.nose * k, 0);
    c.closePath();
  };
  c.fillStyle = '#0D3A1A'; leaf(1.10); c.fill();
  c.fillStyle = P.core;    leaf(1.00); c.fill();
  /* the midrib, and a pair of veins -- the only leaf detail that survives to
     37 pixels */
  c.strokeStyle = rung ? '#FFFFFF' : P.glow;
  c.lineWidth = Math.max(0.8, r * (0.10 + 0.06 * hot));
  c.beginPath(); c.moveTo(G.hilt, 0); c.lineTo(G.nose * 0.92, 0); c.stroke();
  c.lineWidth = Math.max(0.6, r * 0.05); c.globalAlpha = 0.6;
  for (const s of [-1, 1]){
    c.beginPath(); c.moveTo(G.shoulder * 0.2, 0);
    c.lineTo(G.shoulder * 1.15, s * G.w * 0.70); c.stroke();
  }
  c.globalAlpha = 1;
};

/* C — GROWN KUNAI. The whole object is plant, and it is the weapon in
   miniature: SHAPES._tbGrown's own grammar at a fifth of the size. */
window.KUNAI.C = function(c, r, rung, P){
  const G = window.KUNAI._geom(r), hot = Math.min(1, rung / 3);
  /* the stem: woody, slightly crooked, with two knots */
  c.strokeStyle = '#3A2C18'; c.lineWidth = G.tw * 2.2; c.lineCap = 'round';
  c.beginPath();
  c.moveTo(G.hilt, 0);
  c.quadraticCurveTo((G.hilt + G.butt) / 2, r * 0.10, G.butt, 0);
  c.stroke();
  /* the ring is a CURLED TENDRIL, not a forged loop -- open, so it reads as
     grown rather than made */
  c.strokeStyle = '#4A5A2A'; c.lineWidth = Math.max(1, r * 0.12);
  c.beginPath(); c.arc(G.ring, 0, G.ringR, -2.2, 2.9); c.stroke();
  /* the blade, with a leaf margin: a straight taper cut into three teeth a
     side, which is a serration a viewer reads at size and a leaf edge close up */
  const teeth = (k, s) => {
    c.lineTo(G.shoulder * 0.72 * k, s * G.w * 0.92 * k);
    c.lineTo(G.shoulder * 0.50 * k, s * G.w * 0.58 * k);
    c.lineTo(G.shoulder * 0.28 * k, s * G.w * 0.78 * k);
    c.lineTo(G.hilt * k, s * G.w * 0.34 * k);
  };
  const blade = (k) => {
    c.beginPath();
    c.moveTo(G.nose * k, 0);
    c.lineTo(G.shoulder * k, -G.w * 1.06 * k);
    teeth(k, -1);
    c.lineTo(G.hilt * k, G.w * 0.34 * k);
    c.lineTo(G.shoulder * 0.28 * k, G.w * 0.78 * k);
    c.lineTo(G.shoulder * 0.50 * k, G.w * 0.58 * k);
    c.lineTo(G.shoulder * 0.72 * k, G.w * 0.92 * k);
    c.lineTo(G.shoulder * k, G.w * 1.06 * k);
    c.closePath();
  };
  c.fillStyle = '#0D3A1A'; blade(1.12); c.fill();
  c.fillStyle = P.core;    blade(1.00); c.fill();
  c.strokeStyle = rung ? '#FFFFFF' : P.glow;
  c.lineWidth = Math.max(0.8, r * (0.09 + 0.06 * hot));
  c.beginPath(); c.moveTo(G.hilt, 0); c.lineTo(G.nose * 0.90, 0); c.stroke();
  c.lineCap = 'butt';
};

/* D — HARD KUNAI. The strictest reading of "kunai first": no green in the
   shape at all. The school arrives as the halo and nothing else. */
window.KUNAI.D = function(c, r, rung, P){
  const G = window.KUNAI._geom(r), hot = Math.min(1, rung / 3);
  c.strokeStyle = '#1C1F1B'; c.lineWidth = G.tw * 2.4;
  c.beginPath(); c.moveTo(G.hilt, 0); c.lineTo(G.butt, 0); c.stroke();
  c.lineWidth = Math.max(1.1, r * 0.15);
  c.beginPath(); c.arc(G.ring, 0, G.ringR, 0, Math.PI * 2); c.stroke();
  /* a heavier blade than A's: the diamond is wider and the shoulder is
     further forward, which is the profile of a real kunai rather than of a
     dart */
  c.beginPath();
  c.moveTo(G.nose, 0);
  c.lineTo(G.shoulder * 1.25, -G.w * 1.15);
  c.lineTo(G.hilt, -G.w * 0.40);
  c.lineTo(G.hilt, G.w * 0.40);
  c.lineTo(G.shoulder * 1.25, G.w * 1.15);
  c.closePath();
  c.fillStyle = '#8A9488'; c.fill();
  /* the bevel: one lit face, one shadowed, which is what makes a grey shape
     read as METAL rather than as a grey shape */
  c.beginPath();
  c.moveTo(G.nose, 0);
  c.lineTo(G.shoulder * 1.25, -G.w * 1.15);
  c.lineTo(G.hilt, -G.w * 0.40);
  c.closePath();
  c.fillStyle = '#D5DED2'; c.fill();
  c.strokeStyle = rung ? '#FFFFFF' : '#EFF6EC';
  c.lineWidth = Math.max(0.7, r * (0.06 + 0.06 * hot));
  c.beginPath(); c.moveTo(G.nose, 0); c.lineTo(G.shoulder * 1.25, G.w * 1.15);
  c.stroke();
};

/* THE SHIPPED ONE, for the comparison. A leaf with a point on it. */
window.KUNAI.SHIPPED = function(c, r, rung, P){
  const hot = Math.min(1, rung / 3);
  const L = r * 1.85, W = r * 0.80;
  const leaf = (k) => {
    c.beginPath();
    c.moveTo(L * k, 0);
    c.quadraticCurveTo(0, -W * k, -L * 0.62 * k, 0);
    c.quadraticCurveTo(0,  W * k, L * k, 0);
    c.closePath();
  };
  c.fillStyle = '#0D3A1A'; leaf(1.12); c.fill();
  c.fillStyle = P.core;    leaf(1.00); c.fill();
  c.strokeStyle = rung ? '#FFFFFF' : P.glow;
  c.lineWidth = Math.max(0.8, r * (0.10 + 0.06 * hot));
  c.beginPath(); c.moveTo(-L * 0.55, 0); c.lineTo(L * 0.92, 0); c.stroke();
};
"""


SHEET_JS = r"""([order, labels, rgrow, r0]) => {
  const P = AC.AFFINITIES.verdant;
  const W = 1180, ROW = 196, H = 70 + ROW * order.length;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const c = cv.getContext('2d');
  c.fillStyle = '#0A0D0A'; c.fillRect(0, 0, W, H);

  c.font = '600 15px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#9FB39C';
  c.fillText('THE WINNOWING — four kunai, and the leaf second. 1:1 at every '
             + 'rung, then 3x.', 20, 30);
  c.font = '12px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#5E6E5C';
  c.fillText('a fresh kunai is r ' + r0 + ' and a fully grown one is r '
             + (r0 * Math.pow(rgrow, 3)).toFixed(1)
             + ' — the sizes they actually fly at, at --w 540', 20, 50);

  order.forEach((key, i) => {
    const y = 70 + ROW * i + ROW * 0.5;
    c.font = '600 14px "Atkinson Hyperlegible Next", system-ui, sans-serif';
    c.fillStyle = key === 'SHIPPED' ? '#7A6E52' : '#DCEBD8';
    c.fillText(labels[i], 18, y - 4);
    c.font = '11px "Atkinson Hyperlegible Next", system-ui, sans-serif';
    c.fillStyle = '#5E6E5C';
    c.fillText(key === 'SHIPPED' ? 'what shipped' : 'candidate ' + key, 18, y + 14);
    c.strokeStyle = '#18201A'; c.lineWidth = 1;
    c.beginPath(); c.moveTo(18, y + ROW * 0.5 - 8);
    c.lineTo(W - 18, y + ROW * 0.5 - 8); c.stroke();

    /* 1:1, every rung, left to right, so the GROWTH is a row and not a claim */
    let x = 230;
    for (let rung = 0; rung <= 3; rung++){
      const r = r0 * Math.pow(rgrow, rung);
      window.KUNAI._halo(c, x, y, r, rung, P);
      c.save(); c.translate(x, y); c.rotate(0.0);
      window.KUNAI[key](c, r, rung, P);
      c.restore();
      c.font = '10px "Atkinson Hyperlegible Next", system-ui, sans-serif';
      c.fillStyle = '#4A5A48';
      c.fillText('rung ' + rung, x - 18, y + 52);
      x += 44 + r * 3.4;
    }

    /* 3x NEAREST is not available on a canvas draw, so this redraws at 3x
       rather than upscaling: an interpolating upscale invents edges and the
       question is whether the edges are there. twinblade_zoom's rule. */
    let zx = 760;
    for (const rung of [0, 3]){
      const r = r0 * Math.pow(rgrow, rung) * 2.6;
      window.KUNAI._halo(c, zx, y, r, rung, P);
      c.save(); c.translate(zx, y); c.rotate(0.0);
      window.KUNAI[key](c, r, rung, P);
      c.restore();
      zx += 190;
    }
  });
  return cv.toDataURL('image/png');
}"""


HALL_JS = r"""([order, labels, rgrow, r0, seed]) => {
  const P = AC.AFFINITIES.verdant;
  const PW = 286, PH = 430, GAP = 12;
  const cols = order.length;
  const W = GAP + (PW + GAP) * cols, H = 74 + PH + 16;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const c = cv.getContext('2d');
  c.fillStyle = '#0A0D0A'; c.fillRect(0, 0, W, H);
  c.font = '600 15px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#9FB39C';
  c.fillText('THE SAME FOURTEEN KUNAI IN THE HALL — real scale, the rungs in '
             + 'the measured proportion, one seed', 16, 28);
  c.font = '12px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#5E6E5C';
  c.fillText('a silhouette that reads alone and turns to soup in a crowd is '
             + 'the wrong answer, and the shape sheet cannot see that', 16, 48);

  /* ONE deterministic layout, shared by every panel, so the only variable is
     the branch. mulberry32 off a fixed seed -- the same generator the sim
     uses, for the same reason. */
  let s = seed >>> 0;
  const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  /* THE RUNGS IN THE MEASURED PROPORTION, not evenly: the census over 44 real
     casts read 19/47/107/242 at rungs 0..3, so a crowd is mostly GROWN. */
  const mix = [0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2];
  const spots = [];
  for (let i = 0; i < 14; i++)
    spots.push([28 + rnd() * (PW - 56), 30 + rnd() * (PH - 60),
                rnd() * Math.PI * 2, mix[i]]);

  order.forEach((key, i) => {
    const ox = GAP + (PW + GAP) * i, oy = 66;
    /* the hall's own ground, so the contrast is the contrast a viewer sees */
    const g = c.createLinearGradient(ox, oy, ox, oy + PH);
    g.addColorStop(0, '#0E1410'); g.addColorStop(1, '#070A08');
    c.fillStyle = g; c.fillRect(ox, oy, PW, PH);
    c.strokeStyle = '#7A2B23'; c.lineWidth = 2;
    c.strokeRect(ox + 1, oy + 1, PW - 2, PH - 2);
    c.save();
    c.beginPath(); c.rect(ox, oy, PW, PH); c.clip();
    for (const [x, y, a, rung] of spots){
      const r = r0 * Math.pow(rgrow, rung);
      window.KUNAI._halo(c, ox + x, oy + y, r, rung, P);
      c.save(); c.translate(ox + x, oy + y); c.rotate(a);
      window.KUNAI[key](c, r, rung, P);
      c.restore();
    }
    c.restore();
    c.font = '600 13px "Atkinson Hyperlegible Next", system-ui, sans-serif';
    c.fillStyle = key === 'SHIPPED' ? '#7A6E52' : '#DCEBD8';
    c.fillText(labels[i], ox + 4, oy - 8);
  });
  return cv.toDataURL('image/png');
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-thornshear.html")
    ap.add_argument("--out", default="../05-reference/v47")
    A = ap.parse_args()
    path = resolve_game(A.game)
    outdir = (HERE / A.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    order = ["SHIPPED", "A", "B", "C", "D"]
    labels = ["Leaf with a point on it", "Steel kunai, leaf trail",
              "Leaf-bladed kunai", "Grown kunai", "Hard kunai"]

    with game(game_path=path) as (page, errors):
        u = page.evaluate("() => { const w = AC.WEAPONS.find(x => "
                          "x.id === 'thornshear'); return { r: w.ult.r, "
                          "growR: w.ult.growR }; }")
        # WRAPPED IN A FUNCTION, and it is not a style choice: `page.evaluate`
        # of a bare script whose completion value is a FUNCTION calls that
        # function with no arguments. This block ends in an assignment of
        # `window.KUNAI.SHIPPED`, so Playwright called the last candidate with
        # a null context and reported it as an error inside the art.
        page.evaluate("() => {" + CANDS_JS + "}")
        for name, js, args in (
                ("kunai-shapes.png", SHEET_JS,
                 [order, labels, u["growR"], u["r"]]),
                ("kunai-in-hall.png", HALL_JS,
                 [order, labels, u["growR"], u["r"], 90210])):
            data = page.evaluate(js, args)
            raw = base64.b64decode(data.split(",", 1)[1])
            (outdir / name).write_bytes(raw)
            print(f"  wrote {outdir / name}  {len(raw) / 1024:.0f} kB")
        if errors:
            print("  ! page errors:", errors[:3])
    return 0


if __name__ == "__main__":
    sys.exit(main())
