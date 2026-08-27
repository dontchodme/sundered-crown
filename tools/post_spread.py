#!/usr/bin/env python3
"""THE BLOOM SPREAD. One seed, one runtime, four columns, for Rick's eyes.

    python post_spread.py
    python post_spread.py --a paradox --b heartwood --seed 25064 --moments 3

`docs/RENDERER-BRIEF.md` §7 gate 2: every step ships side-by-side filmstrips,
old and new, same seed, same frame indices, one image. And §8.5, which is
CLAUDE.md rule 2: offer a SPREAD, not a guess. v43 landed its sound in one
round trip that way and v42 took four, because a spread of one can never
reveal that the register is wrong.

BOTH STRIPS COME OUT OF ONE RUNTIME, and that is not a detail. Chromium 128
and 151 disagree on the last bit of Math.pow, which is 112 fights in 192
(docs/RUNTIME-DRIFT.md) -- so a sheet whose control was rendered anywhere but
here would be comparing two different fights and calling the difference bloom.
Every tile below is drawn from the same page, the same match object, the same
frame.

WHICH MOMENTS. Not chosen by eye, and not the first thing on screen: the frame
at t=0 has nothing above the lowest threshold in the spread, so a sheet built
from it would show four identical tiles and read as "bloom does nothing". The
scan pass runs the fight at low resolution and measures the emissive mass
inside the arena rect -- how many pixels are bright enough to bloom at all --
then takes the peaks, kept apart so three tiles are not three frames of one
blow.

Writes a PNG to 05-reference/post/ and prints what changed, per column, so the
picture arrives with a number beside it.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-frame.html"
POST_JS = REPO / "src" / "render" / "post.js"
OUTDIR = REPO / "05-reference" / "post"

SCAN_JS = r"""
(cfg) => {
  window.__frozen = true;
  AC.setResolution(cfg.sw, cfg.sh);
  const m = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
  m.introT = 0;
  AC.__inject(m);
  const dt = AC.CONFIG.physics.dt;
  const steps = Math.max(1, Math.round(cfg.every / dt));
  const cv = document.getElementById('cv');
  const g = cv.getContext('2d');
  const R = AC.renderer, k = R.k;
  const x0 = Math.max(0, Math.round(R.pad * k)), y0 = Math.max(0, Math.round(R.arenaTop * k));
  const w = Math.min(cv.width - x0, Math.round(R.aw * k));
  const h = Math.min(cv.height - y0, Math.round(R.ah * k));
  const out = [];
  let guard = 0;
  while (!m.over && guard++ < cfg.maxSamples) {
    for (let i = 0; i < steps; i++) m.step(dt);
    AC.__draw(m);
    const d = g.getImageData(x0, y0, w, h).data;
    let mass = 0;
    for (let i = 0; i < d.length; i += 4) {
      const l = (0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]) / 255;
      if (l > cfg.thresh) mass += l - cfg.thresh;
    }
    out.push({ t: +m.t.toFixed(3), mass: +mass.toFixed(2), cut: !!AC.CINE.cut,
               over: m.over });
    if (m.over) break;
  }
  return { samples: out, dur: +m.t.toFixed(2), over: m.over };
}
"""

SHEET_JS = r"""
(cfg) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const dt = AC.CONFIG.physics.dt;
  const FPS = 60, STEPS_PER_FRAME = Math.round(1 / (FPS * dt));   // 2 at dt=1/120
  const cv = document.getElementById('cv');

  const ov = document.createElement('canvas');
  ov.style.display = 'none';
  document.body.appendChild(ov);
  const post = SWBPost.create(ov);

  /* The readout layer gets its own canvas. The renderer only ever draws to
     #cv, so one of the two passes has to be copied off it before the other
     overwrites it -- the readouts, because they are the cheap one and because
     the world is then what is left on #cv if the chain is switched off. */
  const ro = document.createElement('canvas');
  ro.width = cv.width; ro.height = cv.height;
  const roCtx = ro.getContext('2d');

  const R = AC.renderer;
  const state = () => ({
    enabled: true,
    dt: 1 / FPS,
    rect: { x: R.pad * R.k, y: R.arenaTop * R.k, w: R.aw * R.k, h: R.ah * R.k },
    cine: AC.CINE ? { on: !!AC.CINE.on, cut: !!AC.CINE.cut,
                      tier: AC.CINE.cut ? AC.CINE.cut.tier : null,
                      fatal: AC.CINE.cut ? !!AC.CINE.cut.fatal : false } : null,
  });

  const cols = cfg.cols;
  const TW = cfg.tile, TH = Math.round(TW * 1920 / 1080);
  const PAD = 14, HEAD = 96, ROWH = TH + 40;
  const W = PAD + cols.length * (TW + PAD);
  const H = HEAD + cfg.moments.length * ROWH + PAD;

  const sheet = document.createElement('canvas');
  sheet.width = W; sheet.height = H;
  const s = sheet.getContext('2d');
  s.fillStyle = '#0B0B10'; s.fillRect(0, 0, W, H);
  s.fillStyle = '#E8E4F0';
  s.font = '700 26px sans-serif';
  s.fillText(cfg.title, PAD, 34);
  s.fillStyle = '#8A8296';
  s.font = '400 15px monospace';
  s.fillText(cfg.sub, PAD, 58);
  s.fillText(cfg.runtime, PAD, 78);

  const report = [];
  const baseline = [];

  /* COLUMN-MAJOR, AND FOR A REASON. A trail is history: it needs frames run
     into it before the one being looked at, and a match cannot be rewound. So
     each column gets its OWN match from the same seed -- deterministic, so it
     is the same fight -- stepped to just before each moment and then run
     forward at 60fps with the chain live, which is what fills the buffer.
     A single cold frame would show no trail at all and read as "trails do
     nothing". */
  for (let c = 0; c < cols.length; c++) {
    const key = cols[c];
    let m = null, curPair = -1;

    /* THE CONTROL HAS TO HOLD EVERYTHING ELSE. For a trail spread the
       question is the TAIL, so the control column keeps bloom at the chosen
       default and turns only trails off. A control with bloom off too would
       make every number below the sum of two effects and the sheet would be
       answering a question nobody asked. */
    if (key === 'off' && cfg.effect === 'trails') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(null);
    }
    else if (key === 'off') { post.setBloom(null); post.setTrails(null); }
    else if (key === 'chosen') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
    }
    else if (cfg.effect === 'trails') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(SWBPost.TRAILS[key]);
    } else {
      post.setTrails(null);
      post.setBloom(SWBPost.SPREAD[key]);
    }

    for (let r = 0; r < cfg.moments.length; r++) {
      const row = cfg.moments[r];
      const target = row.t;
      /* A ROW CAN COME FROM A DIFFERENT FIGHT. One sheet can then ask the
         register against two kinds of art at once, which is the only way to
         answer it -- a setting chosen on one relic is a setting chosen on one
         relic. A fresh match per (column, pairing), deterministic from the
         seed, so every column sees the identical fight. */
      if (row.pair !== curPair) {
        const P = cfg.pairs[row.pair];
        m = new AC.Match(P.a, P.b, P.seed >>> 0);
        m.introT = 0;
        AC.__inject(m);
        curPair = row.pair;
      }
      const preTo = Math.max(0, target - cfg.warm / FPS);
      while (m.t < preTo - dt * 0.5) m.step(dt);

      post.resetHistory();
      const chainOn = post.passes.length > 0;
      let drawn = cv;
      for (let f = 0; f < cfg.warm; f++) {
        for (let i2 = 0; i2 < STEPS_PER_FRAME; i2++) m.step(dt);
        if (chainOn) {
          /* TWO PASSES, and the order matters. Readouts first, copied off;
             then the world, which is what the chain is handed. The control
             column takes neither and draws the whole frame at roMode 0, so
             it stays the untouched picture it is supposed to be. */
          R.roMode = 2; AC.__draw(m);
          roCtx.clearRect(0, 0, ro.width, ro.height);
          roCtx.drawImage(cv, 0, 0);
          R.roMode = 1; AC.__draw(m);
          const st = state();
          st.readouts = ro;
          post.render(cv, st);
          drawn = ov;
        } else {
          R.roMode = 0; AC.__draw(m);
          drawn = cv;
        }
      }
      R.roMode = 0;

      const x = PAD + c * (TW + PAD), y = HEAD + r * ROWH;
      s.drawImage(drawn, x, y, TW, TH);
      s.strokeStyle = key === 'off' ? '#C9A227' : '#2A2436';
      s.lineWidth = key === 'off' ? 2 : 1;
      s.strokeRect(x + 0.5, y + 0.5, TW - 1, TH - 1);

      /* The OFF column is drawn first and kept, so every other column is
         measured against the SAME frame of the SAME fight rather than against
         whatever it happens to sit next to. */
      if (key === 'off') {
        /* Read what the control actually PRODUCED -- the raw canvas for a
           bloom spread, the bloom-only composite for a trail one -- and
           record which way up it is so the comparison is like for like. */
        if (chainOn) baseline[r] = { px: post.readPixels(), gl: true };
        else baseline[r] = { px: cv.getContext('2d')
                               .getImageData(0, 0, cv.width, cv.height).data, gl: false };
      }

      let changed = 0, meanAdd = 0;
      if (key !== 'off' && baseline[r]) {
        const px = post.readPixels(), base = baseline[r].px, baseGl = baseline[r].gl;
        const w2 = cv.width, h2 = cv.height;
        let diff = 0, add = 0;
        for (let yy = 0; yy < h2; yy += 3) {
          const gy = h2 - 1 - yy;
          for (let xx = 0; xx < w2; xx += 3) {
            const i3 = (gy * w2 + xx) * 4;
            const j3 = (baseGl ? (gy * w2 + xx) : (yy * w2 + xx)) * 4;
            const dd = Math.abs(px[i3] - base[j3]) + Math.abs(px[i3+1] - base[j3+1])
                     + Math.abs(px[i3+2] - base[j3+2]);
            if (dd) { diff++; add += dd; }
          }
        }
        const n = Math.ceil(h2 / 3) * Math.ceil(w2 / 3);
        changed = +(100 * diff / n).toFixed(1);
        meanAdd = +(add / n).toFixed(2);
      }

      s.fillStyle = key === 'off' ? '#C9A227' : '#E8E4F0';
      s.font = '700 15px sans-serif';
      s.fillText(key === 'off'
                 ? (cfg.effect === 'trails'
                    ? 'TRAILS OFF  (the control -- bloom still on)'
                    : 'OFF  (the control)')
                 : (key === 'chosen' ? 'AS CHOSEN' : key.toUpperCase()),
                 x, y + TH + 18);
      s.fillStyle = '#8A8296';
      s.font = '400 12px monospace';
      const st = state();
      if (key === 'off') {
        const P = cfg.pairs[row.pair];
        s.fillText(P.a + ' v ' + P.b + '  seed ' + P.seed + '   t='
                   + m.t.toFixed(2) + 's' + (st.cine && st.cine.cut ? '  CUT' : ''),
                   x, y + TH + 34);
      } else if (key === 'chosen') {
        s.fillText('bloom ' + SWBPost.SPREAD.DEFAULT + ' + trails '
                   + SWBPost.TRAILS.DEFAULT + '   ' + changed + '% px  +' + meanAdd,
                   x, y + TH + 34);
        report.push({ t: +m.t.toFixed(2), variant: 'chosen', pctChanged: changed,
                      meanAdd: meanAdd, cut: !!(st.cine && st.cine.cut) });
      } else if (cfg.effect === 'trails') {
        const o = SWBPost.TRAILS[key];
        s.fillText(o.seconds + 's tail   ' + changed + '% px  +' + meanAdd,
                   x, y + TH + 34);
        report.push({ t: +m.t.toFixed(2), variant: key, pctChanged: changed,
                      meanAdd: meanAdd, cut: !!(st.cine && st.cine.cut) });
      } else {
        const o = SWBPost.SPREAD[key];
        s.fillText('thr ' + o.threshold + '  int ' + o.intensity
                   + '   ' + changed + '% px  +' + meanAdd, x, y + TH + 34);
        report.push({ t: +m.t.toFixed(2), variant: key, pctChanged: changed,
                      meanAdd: meanAdd, cut: !!(st.cine && st.cine.cut) });
      }
    }
  }
  post.setBloom(null); post.setTrails(null);
  return { png: sheet.toDataURL('image/png').slice(22), w: W, h: H,
           report: report,
           renderer: (() => { const g2 = ov.getContext('webgl2');
             const d = g2.getExtension('WEBGL_debug_renderer_info');
             return d ? g2.getParameter(d.UNMASKED_RENDERER_WEBGL) : g2.getParameter(g2.RENDERER);
           })() };
}
"""


def pick(samples, n, apart):
    """Peaks of emissive mass, kept apart so three tiles are not three frames
    of one blow. Greedy by mass, which is enough here and is at least a
    stated rule rather than a taste."""
    chosen = []
    for s in sorted(samples, key=lambda r: -r["mass"]):
        if s["mass"] <= 0:
            break
        if all(abs(s["t"] - c["t"]) >= apart for c in chosen):
            chosen.append(s)
        if len(chosen) == n:
            break
    return sorted(chosen, key=lambda r: r["t"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--a", default="paradox")
    ap.add_argument("--b", default="heartwood")
    ap.add_argument("--seed", type=int, default=25064)
    ap.add_argument("--pairs", default=None,
                    help="a:b:seed,a:b:seed -- one sheet, several fights, so a "
                         "register can be judged against more than one kind of "
                         "art at once. Overrides --a/--b/--seed.")
    ap.add_argument("--per", type=int, default=None,
                    help="moments taken from each pairing")
    ap.add_argument("--moments", type=int, default=3)
    ap.add_argument("--apart", type=float, default=2.0,
                    help="minimum seconds between chosen moments")
    ap.add_argument("--tile", type=int, default=380)
    ap.add_argument("--wide", type=int, default=620,
                    help="tile width for the two-column `chosen` sheet")
    ap.add_argument("--effect", choices=("bloom", "trails", "chosen"),
                    default="bloom",
                    help="which spread. `trails` holds bloom at the chosen "
                         "default and varies only the tail length.")
    ap.add_argument("--warm", type=int, default=None,
                    help="frames run into the chain before the one captured. "
                         "Trails are history and a cold buffer shows none.")
    ap.add_argument("--every", type=float, default=0.1, help="scan interval")
    ap.add_argument("--out", default=None)
    A = ap.parse_args()

    path = pathlib.Path(A.game).resolve()
    if not path.exists():
        print(f"! {path} does not exist")
        return 2

    post_src = POST_JS.read_text(encoding="utf-8")

    with game(game_path=path) as (page, errors):
        if not page.evaluate("() => !!document.createElement('canvas')"
                             ".getContext('webgl2')"):
            print("! no WebGL2 in this Chromium")
            return 2
        page.add_script_tag(content=post_src)

        if not page.evaluate("() => !!(window.AC && AC.CINE)"):
            print("! this build does not export CINE -- run cineexport_build.py")
            return 2

        if A.pairs:
            pairs = []
            for spec in A.pairs.split(","):
                x, y, sd = spec.split(":")
                pairs.append({"a": x, "b": y, "seed": int(sd)})
        else:
            pairs = [{"a": A.a, "b": A.b, "seed": A.seed}]
        per = A.per if A.per is not None else (
            A.moments if len(pairs) == 1 else 2)

        label = " + ".join(P["a"] + " v " + P["b"] for P in pairs)
        print("")
        print("POST SPREAD  " + label)
        moments = []
        for pi, P in enumerate(pairs):
            print(f"  scanning {P[chr(97)]} v {P[chr(98)]} seed {P[chr(115)+chr(101)+chr(101)+chr(100)]} at {A.every}s...")
            scan = page.evaluate(SCAN_JS, {
                "a": P["a"], "b": P["b"], "seed": P["seed"],
                "every": A.every, "sw": 270, "sh": 480,
                "thresh": 0.62, "maxSamples": 1200,
            })
            chosen = pick(scan["samples"], per, A.apart)
            if not chosen:
                print("! nothing in this pairing clears the threshold; a row")
                print("  from it would be identical tiles.")
                return 1
            for mm in chosen:
                print(f"    t={mm[chr(116)]:>6.2f}s  mass {mm[chr(109)+chr(97)+chr(115)+chr(115)]:>9.1f}")
                moments.append({"pair": pi, "t": mm["t"]})

        if A.effect == "chosen":
            cols = ["off", "chosen"]
            warm = A.warm if A.warm is not None else 20
            title = "AS CHOSEN — " + label
            sub = ("does the register hold on art that is not Paradox's "
                   "lightning? bloom + trails at the chosen settings.")
        elif A.effect == "trails":
            cols = ["off", "short", "mid", "long"]
            warm = A.warm if A.warm is not None else 20
            title = "TRAIL SPREAD — " + label
            sub = ("one variable: tail length in SECONDS. bloom is held at "
                   "the chosen default in every column, the control included.")
        else:
            cols = ["off", "low", "mid", "high"]
            warm = A.warm if A.warm is not None else 1
            title = "BLOOM SPREAD — " + label
            sub = ("same seed, same frame, one runtime. OFF is the untouched "
                   "2D canvas.")
        print(f"  rendering the sheet at 1080x1920, {warm} warm frames…")
        sheet = page.evaluate(SHEET_JS, {
            "pairs": pairs,
            "moments": moments,
            "cols": cols,
            "tile": A.wide if A.effect == "chosen" else A.tile,
            "effect": A.effect, "warm": warm,
            "title": title, "sub": sub,
            "runtime": f"build {path.name}",
        })
        if errors:
            print("! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = pathlib.Path(A.out) if A.out else (
        OUTDIR / (A.effect + "-spread-"
                  + "-".join(P["a"] + "-" + P["b"] + "-" + str(P["seed"])
                             for P in pairs) + ".png"))
    out.write_bytes(base64.b64decode(sheet["png"]))

    print(f"\n  {sheet['renderer']}")
    print(f"\n  {'t':>7} {'variant':>8} {'% px changed':>13} {'mean add':>9}  cut")
    for r in sheet["report"]:
        print(f"  {r['t']:>7.2f} {r['variant']:>8} {r['pctChanged']:>12.1f}% "
              f"{r['meanAdd']:>9.2f}  {'yes' if r['cut'] else ''}")
    print(f"\n  wrote {out}  ({sheet['w']}x{sheet['h']}, "
          f"{out.stat().st_size // 1024} KB)")
    print("\n  THE CHECK IS RICK'S EYES. The numbers say the columns differ;")
    print("  they cannot say which one is right.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
