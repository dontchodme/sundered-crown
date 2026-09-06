#!/usr/bin/env python3
"""WHAT A BURN LOOKS LIKE -- four vocabularies, off one real frame. v66.

    python corona_burn_sheet.py --game ../02-chain/sc-corona-fx.html

Rick, 2026-09-03, on the third rendered window: *"the burn stacks need a
different animation. they look like worms."*

HE IS DESCRIBING A CONSTANT-WIDTH CURVED STROKE, which is what the first cut
was: a quadratic with a wobbling control point, stroked three times at 5.4 /
3.0 / 1.3 px. Nothing in fire is a line of even thickness that bends, so a
stroked curve reads as something ANIMAL. Every variant below is a FILLED,
TAPERED shape or a discrete mote instead, and the sheet exists because which
one reads is his (rule 2, the ult animations are one of the seven).

SHAPE QUESTIONS GO TO A SHEET. Four vocabularies at TWO stack counts, because
this status is the only one in the game with no ceiling -- what has to work is
not one picture but the range from a single crossing to a quarry standing in
the shower, and `_stBleed` shipped a bug for exactly that reason (it drew
`min(4, n)` drips, so eight stacks looked like four).

  A  TONGUES   tapered filled flames, wide at the root, pointed at the tip
  B  EMBERS    no licks at all: a hot rim and discrete motes lifting off it
  C  CROWN     ONE closed jagged silhouette around the shell, not N marks
  D  CHAR      the shell blackens and cracks, and the cracks glow

Every one is deterministic -- a function of the match clock and the mark's
index, never `this.rng()`, because a renderer that draws from the sim's stream
moves every fight it is drawn over.
"""
from __future__ import annotations

import argparse
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "starwarden"

# THE FOUR, AS SOURCE. Injected over `_stBurn` one at a time; the build is not
# touched until Rick picks one.
VARIANTS = r"""
({
  /* A -- TONGUES. The direct answer to "worms": a flame is a TAPERED shape,
     not a line of even width that bends. Each tongue is a filled path -- two
     curves from a wide root to a single point -- so its silhouette narrows as
     it rises and can never read as a body with a constant thickness. */
  A: function(m, f, R, n){
    const c = this.ctx;
    const HOT = "#FFD08A", CORE = "#FF7A1F", EDGE = "#2A0C02";
    const heat = Math.min(1, n / 24), N = Math.min(12, n), t = m.t;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = 0.10 + 0.28 * heat;
    c.fillStyle = CORE;
    c.beginPath(); c.arc(f.x, f.y, R * 0.96, 0, TAU); c.fill();
    c.globalCompositeOperation = "source-over";
    for (let i = 0; i < N; i++){
      const a = i * TAU / N + 0.05 * Math.sin(t * 0.7 + i);
      const wob = 0.5 + 0.5 * Math.sin(t * 8 + i * 2.1);
      const L = (9 + 7 * wob) * (0.7 + 0.5 * heat);
      const w = 5.0 + 2.0 * heat;          // the ROOT is wide
      const ca = Math.cos(a), sa = Math.sin(a);
      const bx = f.x + ca * (R - 1), by = f.y + sa * (R - 1);
      const tx = f.x + ca * (R + L), ty = f.y + sa * (R + L);
      /* the lean is on the TIP only, so the root stays planted and the shape
         tapers -- a flame leans, a worm crawls */
      const lx = -sa * (wob - 0.5) * 7, ly = ca * (wob - 0.5) * 7;
      c.beginPath();
      c.moveTo(bx - sa * w, by + ca * w);
      c.quadraticCurveTo(bx - sa * w * 0.4 + lx * 0.5, by + ca * w * 0.4 + ly * 0.5,
                         tx + lx, ty + ly);
      c.quadraticCurveTo(bx + sa * w * 0.4 + lx * 0.5, by - ca * w * 0.4 + ly * 0.5,
                         bx + sa * w, by - ca * w);
      c.closePath();
      c.lineJoin = "round";
      c.lineWidth = 2.6; c.strokeStyle = EDGE; c.globalAlpha = 0.9; c.stroke();
      c.fillStyle = CORE; c.globalAlpha = 0.95; c.fill();
      c.globalAlpha = 0.30 + 0.45 * wob;
      c.fillStyle = HOT;
      c.beginPath();
      c.moveTo(bx - sa * w * 0.42, by + ca * w * 0.42);
      c.quadraticCurveTo(bx + lx * 0.5, by + ly * 0.5,
                         bx + ca * (L * 0.62) + lx * 0.7,
                         by + sa * (L * 0.62) + ly * 0.7);
      c.quadraticCurveTo(bx + lx * 0.5, by + ly * 0.5,
                         bx + sa * w * 0.42, by - ca * w * 0.42);
      c.closePath(); c.fill();
    }
    c.restore();
  },

  /* B -- EMBERS. No licks at all, which is the cheapest way to be sure nothing
     reads as a worm. The shell carries the heat and the COUNT is carried by
     how many motes are in the air -- and motes have no long axis, so there is
     nothing to wriggle. The rise is a function of the clock and the index, so
     each mote lifts and fades on its own phase with no state. */
  B: function(m, f, R, n){
    const c = this.ctx;
    const HOT = "#FFE3B0", CORE = "#FF7A1F";
    const heat = Math.min(1, n / 24), N = Math.min(22, 4 + n), t = m.t;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.globalAlpha = 0.12 + 0.34 * heat;
    c.fillStyle = CORE;
    c.beginPath(); c.arc(f.x, f.y, R * 0.98, 0, TAU); c.fill();
    /* the rim, brightest where the shell is hottest */
    c.globalAlpha = 0.45 + 0.4 * heat;
    c.lineWidth = 2.6 + 2.4 * heat; c.strokeStyle = CORE;
    c.beginPath(); c.arc(f.x, f.y, R * 0.99, 0, TAU); c.stroke();
    for (let i = 0; i < N; i++){
      const ph = (t * (0.9 + 0.25 * ((i * 37) % 7) / 7) + i * 0.618) % 1;
      const a = i * TAU / N + 0.9 * Math.sin(i * 2.3);
      const rise = ph * (26 + 16 * heat);
      const x = f.x + Math.cos(a) * (R - 2) + Math.sin(i * 1.7) * rise * 0.35;
      const y = f.y + Math.sin(a) * (R - 2) - rise;
      const r = (2.6 - 1.6 * ph) * (0.75 + 0.5 * heat);
      if (r <= 0.2) continue;
      c.globalAlpha = (1 - ph) * (0.55 + 0.4 * heat);
      c.fillStyle = ph < 0.4 ? HOT : CORE;
      c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    }
    c.restore();
  },

  /* C -- CROWN. ONE closed silhouette around the whole shell instead of N
     separate marks, which is `_whGnawed`'s rule applied to a status: a grammar
     that adds a limb to a shape must add it to the shape's OUTLINE, not behind
     it. There are no separate objects to read as animals because there is only
     one object, and the count is carried by how tall and how many its peaks
     are. */
  C: function(m, f, R, n){
    const c = this.ctx;
    const HOT = "#FFD08A", CORE = "#FF7A1F", EDGE = "#2A0C02";
    const heat = Math.min(1, n / 24), t = m.t;
    const P = Math.min(14, 5 + Math.floor(n / 2));
    const path = (amp, rad) => {
      c.beginPath();
      const K = P * 6;
      for (let i = 0; i <= K; i++){
        const a = i * TAU / K;
        const w = 0.5 + 0.5 * Math.cos(a * P - t * 3.2);
        const w2 = 0.5 + 0.5 * Math.sin(a * (P * 2) + t * 5.1);
        const rr = rad + amp * (w * 0.78 + w2 * 0.22);
        const x = f.x + Math.cos(a) * rr, y = f.y + Math.sin(a) * rr;
        if (i === 0) c.moveTo(x, y); else c.lineTo(x, y);
      }
      c.closePath();
    };
    c.save();
    c.globalCompositeOperation = "source-over";
    const amp = (7 + 9 * heat), rad = R + 1;
    path(amp, rad);
    c.lineJoin = "round";
    c.lineWidth = 3.4; c.strokeStyle = EDGE; c.globalAlpha = 0.9; c.stroke();
    c.fillStyle = CORE; c.globalAlpha = 0.92; c.fill();
    c.globalCompositeOperation = "lighter";
    path(amp * 0.52, rad - 1);
    c.fillStyle = HOT; c.globalAlpha = 0.35 + 0.35 * heat; c.fill();
    c.restore();
  },

  /* D -- CHAR. A burn is DAMAGE, so the shell blackens and the cracks in it
     glow. Nothing leaves the silhouette at all, which is the most legible
     option at phone size and the least legible at a glance -- it says "this
     one is hurt" rather than "this one is on fire". Included because the
     status is the relic's whole payload and a quiet picture for it is a real
     choice, not a straw man. */
  D: function(m, f, R, n){
    const c = this.ctx;
    const HOT = "#FFC061", CORE = "#FF6A12";
    const heat = Math.min(1, n / 24), t = m.t;
    const N = Math.min(9, 3 + Math.floor(n / 3));
    c.save();
    c.globalCompositeOperation = "source-over";
    c.globalAlpha = 0.20 + 0.45 * heat;
    c.fillStyle = "#160803";
    c.beginPath(); c.arc(f.x, f.y, R * 0.99, 0, TAU); c.fill();
    c.globalCompositeOperation = "lighter";
    for (let i = 0; i < N; i++){
      const a = i * TAU / N + 0.7 * Math.sin(i * 1.9);
      const pulse = 0.45 + 0.55 * (0.5 + 0.5 * Math.sin(t * 4.4 + i * 1.3));
      const r0 = R * 0.18, r1 = R * (0.62 + 0.3 * Math.sin(i * 2.7));
      c.globalAlpha = pulse * (0.35 + 0.5 * heat);
      c.lineCap = "round";
      c.lineWidth = 3.6; c.strokeStyle = CORE;
      c.beginPath();
      c.moveTo(f.x + Math.cos(a) * r0, f.y + Math.sin(a) * r0);
      c.lineTo(f.x + Math.cos(a + 0.25) * r1, f.y + Math.sin(a + 0.25) * r1);
      c.stroke();
      c.lineWidth = 1.4; c.strokeStyle = HOT; c.globalAlpha = pulse * 0.9;
      c.stroke();
    }
    /* a few motes so it is not entirely static */
    for (let i = 0; i < 6; i++){
      const ph = (t * 0.8 + i * 0.31) % 1;
      const a = i * TAU / 6 + Math.sin(i * 3.1);
      const x = f.x + Math.cos(a) * R * 0.7, y = f.y + Math.sin(a) * R * 0.7 - ph * 22;
      c.globalAlpha = (1 - ph) * 0.5 * (0.4 + heat);
      c.fillStyle = HOT;
      c.beginPath(); c.arc(x, y, 1.9 * (1 - ph * 0.6), 0, TAU); c.fill();
    }
    c.restore();
  }
})
"""

SHEET_JS = r"""([rid, foe, seed, secs, variants, labels, counts, shipped]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer, savedCtx = R.ctx;
  const proto = R.constructor.prototype;
  const orig = proto._stBurn;
  const V = shipped ? { SHIPPED: orig } : eval(variants);
  /* A REAL FRAME, and a real BURNING quarry -- not a posed one. What has to be
     judged is the status against the shell it lands on, the health ring, the
     hall and whatever the bloom does to all of it. */
  const m = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  let step = 0;
  while (!m.over && step < secs / DT){
    m.step(DT); step++;
    if (th.stacks("burn") >= 6) break;
  }
  if (!th.stacks("burn")) { R.ctx = savedCtx; return { ok: false }; }
  /* WITH `--shipped` THE SHEET DRAWS THE BUILD'S OWN `_stBurn` ACROSS A RANGE
     OF STACK COUNTS INSTEAD OF FOUR CANDIDATES ACROSS TWO. That is the check
     the SPREAD cannot make: this status has no ceiling, it peaks near 60, and
     what has to work is the whole range rather than one picture. `_stBleed`
     shipped `Math.min(4, n)` drips and eight stacks looked exactly like four
     for the life of the game. */
  const keys = Object.keys(V);
  const PW = 320, PH = 340, ROWS = counts.length, COLS = keys.length;
  const cv = document.createElement("canvas");
  cv.width = PW * COLS; cv.height = (PH + 30) * ROWS + 8;
  const g = cv.getContext("2d");
  g.fillStyle = "#07050B"; g.fillRect(0, 0, cv.width, cv.height);
  const panel = document.createElement("canvas");
  panel.width = 540; panel.height = 960;
  const pc = panel.getContext("2d");
  const real = th.status.burn;
  for (let r = 0; r < counts.length; r++){
    for (let i = 0; i < keys.length; i++){
      th.status.burn = { stacks: counts[r], t: 3.0, src: "a" };
      proto._stBurn = keys[i] === "SHIPPED" ? orig : V[keys[i]];
      pc.save(); pc.fillStyle = "#0B0710";
      pc.fillRect(0, 0, panel.width, panel.height); pc.restore();
      R.ctx = pc;
      R.drawArena(m);
      R.drawFighter(m, th);
      R.drawStatus(m, th);
      R.ctx = savedCtx;
      const cw = 320, ch = 340;
      const sx = Math.max(0, Math.min(panel.width - cw, th.x - cw / 2));
      const sy = Math.max(0, Math.min(panel.height - ch, th.y - ch / 2));
      const ox = i * PW, oy = r * (PH + 30) + 30;
      g.drawImage(panel, sx, sy, cw, ch, ox, oy, PW, PH);
      g.save();
      g.fillStyle = "#EDE3D0"; g.font = "600 15px monospace";
      g.fillText(labels[i] + "   " + counts[r] + " stacks", ox + 10, oy - 9);
      g.strokeStyle = "#2A2233"; g.lineWidth = 1;
      g.strokeRect(ox + 0.5, oy + 0.5, PW - 1, PH - 1);
      g.restore();
    }
  }
  th.status.burn = real;
  proto._stBurn = orig;
  R.ctx = savedCtx;
  return { ok: true, png: cv.toDataURL("image/png") };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-corona-fx.html")
    ap.add_argument("--a", default=RID)
    ap.add_argument("--b", default="gravemourn")
    ap.add_argument("--seed", type=int, default=33138)
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--shipped", action="store_true",
                    help="draw the BUILD's own _stBurn across the range of "
                         "stack counts, instead of the four candidates")
    ap.add_argument("--out", default="../05-reference/v66/corona-burn-shapes.png")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    labels = ["A TONGUES", "B EMBERS", "C CROWN", "D CHAR"]
    counts = [6, 30]
    if a.shipped:
        # ONE COLUMN, THE BUILD'S OWN, ACROSS THE RANGE THE STATUS ACTUALLY
        # REACHES. 6 is a couple of crossings, 20 a cast that landed, 40 a
        # quarry that walked through the shower, 60 the measured peak.
        labels = ["SHIPPED"]
        counts = [6, 20, 40, 60]
    out = (pathlib.Path(__file__).parent / a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nWHAT A BURN LOOKS LIKE - four vocabularies at {counts} stacks\n")
    with game(game_path=gp) as (page, errors):
        r = page.evaluate(SHEET_JS, [a.a, a.b, a.seed, a.secs, VARIANTS,
                                     labels, counts, a.shipped])
        assert not errors, errors[:3]
        if not r.get("ok"):
            print("  no burning quarry reached -- try another seed")
            return 1
        png = base64.b64decode(r["png"].split(",", 1)[1])
        out.write_bytes(png)
        for lab in labels:
            print(f"    {lab}")
        print(f"\n  wrote {out}  {len(png) / 1e6:.2f} MB")
        print("\n  NOTHING IS IN THE BUILD YET. The pick is Rick's and the "
              "chosen one\n  lands as a builder insert, not as an edit to the "
              "page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
