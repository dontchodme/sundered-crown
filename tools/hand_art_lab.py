#!/usr/bin/env python3
"""FIVE HANDS, RENDERED BEFORE ANYBODY IS ASKED ANYTHING.

    python hand_art_lab.py --game ../02-chain/sc-gravemourn.html

Rick, watching the first-look clip of the new Gravemourn ultimate:

    "the hands dont read as hands. not detailed enough and they need a little
     more flight time."

## WHAT HE IS LOOKING AT, MEASURED FIRST

§4.1: when a person catches something no tool could, the deliverable is a
MEASUREMENT of the thing they saw, not a fix and an apology.

    hand across, soaring     37 px at --w 540      75 px at 1080
    hand across, as a fist   27 px                 54 px
    finger stroke width       3.3 px                6.6 px
    travel per video frame   0.65x its own width -- NOT a motion smear
    on screen                78 frames at 60fps

**IT IS NOT TOO SMALL.** 75px across on a phone frame is a large object, and
it is on screen for over a second. Two things are wrong and neither is size:

    THE SILHOUETTE IS A CIRCLE WITH SPOKES. The shipped hand is a filled disc
    of radius 0.62R with four straight 3.2px strokes radiating from it over
    about 1.2 radians. A disc with spokes is an ASTERISK. A hand's silhouette
    is a broad palm, four fingers SEPARATED BY GAPS, and a thumb opposed at
    roughly a right angle to them -- the thumb is the single feature that
    makes a hand shape a hand rather than a paw, a leaf or a star.

    IT IS DRAWN ENTIRELY UNDER `lighter`. Additive purple over additive purple
    saturates toward white, so every interior edge -- the gaps between the
    fingers, the line of the knuckles, the web of the thumb -- is erased by
    the blend before it can be seen. This is §4.1b's Daybreak lesson on a new
    object: the thing was not lit, it was ERASED. Detail has to be drawn in a
    DARKER ink over a lit body, not in a brighter one.

So every candidate below is a hand in SILHOUETTE and differs in what kind of
hand it is -- which is the register question, and v43's lesson is that being
wrong about the register is what costs and a spread of one can never reveal
it.

    A  ETHEREAL HAND     the literal reading of §1. A soft-edged human hand
                         with a smoke wrist trailing behind it: broad palm,
                         four tapering fingers with a knuckle bend, an opposed
                         thumb, and the whole thing lit from inside with its
                         edges drawn in the school's dark.
    B  GRASPING CLAW     the same anatomy with the fingers splayed much wider
                         and hooked, closing to a fist on the dive. Reads as
                         intent rather than as anatomy, and the SPREAD is what
                         makes it legible at distance.
    C  BONE HAND         a grave-thing. Finger segments as distinct bones with
                         real gaps between them, knuckle joints as beads. The
                         gaps are the point: nothing else in this game is made
                         of separated parts, so it survives a thumbnail.
    D  SOLID SILHOUETTE  the strictest reading of the diagnosis. No interior
                         detail at all -- one dark hand shape with a bright
                         rim light, so the SHAPE does every bit of the work.
                         The one that cannot be erased by the bloom.

## THE POSES ARE THE MECHANIC

Each is drawn at the three moments the flight actually has: OPEN while it
soars, HALF as it turns in, and FIST on the dive. Rick's sentence is a shape
change over time -- "clenches into a fist as it dive bombs" -- so a candidate
that reads as a hand open and as a blob shut has failed at the half of the
job that carries the story.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

HERE = pathlib.Path(__file__).parent


# --------------------------------------------------------------------------
# THE CANDIDATES. Each is (c, R, shut, pal) -> draws a hand centred at the
# origin, pointing along +x, where `shut` is 0 (open) .. 1 (fist).
# THE CANDIDATE ART LIVES IN ITS OWN .js FILE, not in a python string.
# It is 250 lines of canvas drawing and it is going to be iterated on
# with Rick; a builder that has to re-escape it every round is a builder
# that will eventually escape it wrong.
CANDS_JS = (HERE / "hand_art_cands.js").read_text(encoding="utf-8")


SHEET_JS = r"""([order, labels, rOpen, rShut]) => {
  const P = AC.AFFINITIES.umbral;
  const W = 1240, ROW = 250, H = 96 + ROW * order.length;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const c = cv.getContext('2d');
  c.fillStyle = '#0A0810'; c.fillRect(0, 0, W, H);

  c.font = '600 16px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#B49FD0';
  c.fillText('THE HANDS, ROUND 2 — "a bit large... what if the whole hand was bone?"',
             20, 32);
  c.font = '12px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#6E6084';
  c.fillText('each row: OPEN (soaring) · HALF · FIST (diving), at the size '
             + 'they actually fly at (r ' + rOpen.toFixed(0) + ' open, r '
             + rShut.toFixed(0) + ' shut, --w 540), then the same three at 3x.',
             20, 54);
  c.fillText('the shipped hand is 37px across on a 540 frame and 75px on a '
             + 'phone — it is NOT too small. it is a disc with spokes.',
             20, 72);

  order.forEach((key, i) => {
    const y = 96 + ROW * i + ROW * 0.46;
    c.font = '600 15px "Atkinson Hyperlegible Next", system-ui, sans-serif';
    c.fillStyle = key === 'SHIPPED' ? '#6E5A46' : '#E6DAF6';
    c.fillText(labels[i], 18, y - 6);
    c.font = '11px "Atkinson Hyperlegible Next", system-ui, sans-serif';
    c.fillStyle = '#6E6084';
    c.fillText(key === 'SHIPPED' ? 'what shipped' : 'candidate ' + key,
               18, y + 12);
    c.strokeStyle = '#1A1424'; c.lineWidth = 1;
    c.beginPath(); c.moveTo(18, y + ROW * 0.50);
    c.lineTo(W - 18, y + ROW * 0.50); c.stroke();

    /* 1:1, the three poses */
    let x = 250;
    [0, 0.5, 1].forEach((shut, j) => {
      const R = rOpen + (rShut - rOpen) * shut;
      c.save(); c.translate(x, y); window.HAND[key](c, R, shut, P); c.restore();
      c.font = '10px "Atkinson Hyperlegible Next", system-ui, sans-serif';
      c.fillStyle = '#4E4360';
      c.fillText(['open', 'half', 'fist'][j], x - 12, y + 46);
      x += 108;
    });

    /* 3x, REDRAWN rather than upscaled -- an interpolating upscale invents
       edges and the whole question is whether the edges are there. */
    x = 640;
    [0, 0.5, 1].forEach((shut) => {
      const R = (rOpen + (rShut - rOpen) * shut) * 3;
      c.save(); c.translate(x + 90, y); window.HAND[key](c, R, shut, P);
      c.restore();
      x += 190;
    });
  });
  return cv.toDataURL('image/png');
}"""


# --------------------------------------------------------------------------
# AND IN THE HALL, over a real frame, because a shape that reads on black is
# not the same claim as a shape that reads over a lit arena mid-fight.
HALL_JS = r"""([order, labels, rOpen, rShut, seed]) => {
  const P = AC.AFFINITIES.umbral, DT = AC.CONFIG.physics.dt;
  const m = new AC.Match('gravemourn', 'emberedge', seed);
  let step = 0;
  while (!m.over && step < 20 / DT){ m.step(DT); step++; }
  const R0 = AC.renderer;
  R0.draw(m);
  const src = R0.ctx.canvas;
  const CW = Math.round(src.width / 2), CH = Math.round(src.height / 2);
  const W = 40 + (CW + 20) * order.length, H = CH + 96;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const c = cv.getContext('2d');
  c.fillStyle = '#0A0810'; c.fillRect(0, 0, W, H);
  c.font = '600 16px "Atkinson Hyperlegible Next", system-ui, sans-serif';
  c.fillStyle = '#B49FD0';
  c.fillText('THE SAME FIVE, over a real frame, three hands mid-flight each',
             20, 32);
  order.forEach((key, i) => {
    const x = 20 + (CW + 20) * i;
    c.drawImage(src, 0, 0, src.width, src.height, x, 56, CW, CH);
    c.save();
    c.beginPath(); c.rect(x, 56, CW, CH); c.clip();
    /* three hands on the arc they actually fly, at the sizes they fly at */
    [[0.30, 0.62, 0.0], [0.52, 0.40, 0.5], [0.66, 0.30, 1.0]].forEach(p => {
      const R = (rOpen + (rShut - rOpen) * p[2]) * (CW / AC.CONFIG.arena.w);
      c.save();
      c.translate(x + CW * p[0], 56 + CH * p[1]);
      c.rotate(-0.5 + p[2] * 1.3);
      window.HAND[key](c, R * 2, p[2], P);
      c.restore();
    });
    c.restore();
    c.font = '600 13px "Atkinson Hyperlegible Next", system-ui, sans-serif';
    c.fillStyle = key === 'SHIPPED' ? '#6E5A46' : '#E6DAF6';
    c.fillText(labels[i], x, 50);
  });
  return cv.toDataURL('image/png');
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-gravemourn.html")
    ap.add_argument("--out", default="../05-reference/v53")
    A = ap.parse_args()
    path = resolve_game(A.game)
    outdir = (HERE / A.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    order = ["SHIPPED", "A", "B", "C", "D"]
    labels = ["Flame hand, in the build now", "Bone hand, 0.80x",
              "Bone hand, 0.68x", "Bone and ghost, 0.80x",
              "Flame hand at 0.80x (the control)"]

    with game(game_path=path) as (page, errors):
        # the sizes the build actually flies them at: R = 13 + 5 * (1 - shut)
        r_open, r_shut = 18.0, 13.0
        # WRAPPED IN A FUNCTION -- `page.evaluate` of a bare script whose
        # completion value is a function CALLS it with no arguments, and this
        # block ends in an assignment of `window.HAND.D`. kunai_art_lab hit
        # exactly this and its comment is why the wrapper is here.
        page.evaluate("() => {" + CANDS_JS + "}")
        for name, js, args in (
                ("hand-shapes.png", SHEET_JS, [order, labels, r_open, r_shut]),
                ("hand-in-hall.png", HALL_JS,
                 [order, labels, r_open, r_shut, 31337])):
            data = page.evaluate(js, args)
            raw = base64.b64decode(data.split(",", 1)[1])
            (outdir / name).write_bytes(raw)
            print(f"  wrote {outdir / name}  {len(raw) / 1024:.0f} kB")
        if errors:
            print("  ! page errors:", errors[:3])
    return 0


if __name__ == "__main__":
    sys.exit(main())
