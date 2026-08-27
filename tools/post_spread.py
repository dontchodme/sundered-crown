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
  const m = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
  m.introT = 0;
  AC.__inject(m);
  const dt = AC.CONFIG.physics.dt;
  const cv = document.getElementById('cv');

  const ov = document.createElement('canvas');
  ov.style.display = 'none';
  document.body.appendChild(ov);
  const post = SWBPost.create(ov);

  const R = AC.renderer;
  const state = () => ({
    enabled: true,
    rect: { x: R.pad * R.k, y: R.arenaTop * R.k, w: R.aw * R.k, h: R.ah * R.k },
    cine: AC.CINE ? { on: !!AC.CINE.on, cut: !!AC.CINE.cut,
                      tier: AC.CINE.cut ? AC.CINE.cut.tier : null,
                      fatal: AC.CINE.cut ? !!AC.CINE.cut.fatal : false } : null,
  });

  const cols = cfg.cols;                       // ['off','low','mid','high']
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
  let cursor = 0;

  for (let r = 0; r < cfg.moments.length; r++) {
    const target = cfg.moments[r];
    const need = Math.max(0, Math.round((target - cursor) / dt));
    for (let i = 0; i < need; i++) m.step(dt);
    cursor = m.t;
    AC.__draw(m);

    /* ONE DRAW, FOUR READS. The match is not stepped between columns, so the
       only thing that differs across a row is the chain. */
    const st = state();
    const base = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;

    for (let c = 0; c < cols.length; c++) {
      const key = cols[c];
      const x = PAD + c * (TW + PAD), y = HEAD + r * ROWH;

      let img = cv, changed = 0, meanAdd = 0;
      if (key === 'off') {
        post.setBloom(null);
      } else {
        post.setBloom(SWBPost.SPREAD[key]);
        post.render(cv, st);
        img = ov;
        const px = post.readPixels();
        let diff = 0, add = 0;
        const w2 = cv.width, h2 = cv.height;
        for (let yy = 0; yy < h2; yy += 3) {
          const gy = h2 - 1 - yy;
          for (let xx = 0; xx < w2; xx += 3) {
            const i = (gy * w2 + xx) * 4, j = (yy * w2 + xx) * 4;
            const dd = Math.abs(px[i] - base[j]) + Math.abs(px[i+1] - base[j+1])
                     + Math.abs(px[i+2] - base[j+2]);
            if (dd) { diff++; add += dd; }
          }
        }
        const n = Math.ceil(h2 / 3) * Math.ceil(w2 / 3);
        changed = +(100 * diff / n).toFixed(1);
        meanAdd = +(add / n).toFixed(2);
      }

      s.drawImage(img, x, y, TW, TH);
      s.strokeStyle = key === 'off' ? '#C9A227' : '#2A2436';
      s.lineWidth = key === 'off' ? 2 : 1;
      s.strokeRect(x + 0.5, y + 0.5, TW - 1, TH - 1);

      s.fillStyle = key === 'off' ? '#C9A227' : '#E8E4F0';
      s.font = '700 15px sans-serif';
      const label = key === 'off' ? 'OFF  (the control)' : key.toUpperCase();
      s.fillText(label, x, y + TH + 18);
      s.fillStyle = '#8A8296';
      s.font = '400 12px monospace';
      if (key === 'off') {
        s.fillText('t=' + m.t.toFixed(2) + 's' + (st.cine && st.cine.cut ? '  CUT' : ''),
                   x, y + TH + 34);
      } else {
        const o = SWBPost.SPREAD[key];
        s.fillText('thr ' + o.threshold + '  int ' + o.intensity
                   + '   ' + changed + '% px  +' + meanAdd, x, y + TH + 34);
        report.push({ t: +m.t.toFixed(2), variant: key, pctChanged: changed,
                      meanAdd: meanAdd, cut: !!(st.cine && st.cine.cut) });
      }
    }
  }
  post.setBloom(null);
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
    ap.add_argument("--moments", type=int, default=3)
    ap.add_argument("--apart", type=float, default=2.0,
                    help="minimum seconds between chosen moments")
    ap.add_argument("--tile", type=int, default=380)
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

        print(f"\nPOST SPREAD  {A.a} v {A.b}  seed {A.seed}")
        print(f"  scanning at {A.every}s for emissive mass…")
        scan = page.evaluate(SCAN_JS, {
            "a": A.a, "b": A.b, "seed": A.seed, "every": A.every,
            "sw": 270, "sh": 480, "thresh": 0.62, "maxSamples": 1200,
        })
        got = scan["samples"]
        print(f"  {len(got)} samples, fight {scan['dur']}s, "
              f"over={scan['over']}")

        moments = pick(got, A.moments, A.apart)
        if not moments:
            print("! no frame in this fight has anything above the threshold.")
            print("  A sheet from it would be four identical tiles.")
            return 1
        for mm in moments:
            print(f"    t={mm['t']:>6.2f}s  mass {mm['mass']:>9.1f}"
                  f"{'  CUT' if mm['cut'] else ''}")

        cols = ["off", "low", "mid", "high"]
        print("  rendering the sheet at 1080x1920…")
        sheet = page.evaluate(SHEET_JS, {
            "a": A.a, "b": A.b, "seed": A.seed,
            "moments": [mm["t"] for mm in moments],
            "cols": cols, "tile": A.tile,
            "title": f"BLOOM SPREAD — {A.a} v {A.b}, seed {A.seed}",
            "sub": f"same seed, same frame, one runtime. OFF is the untouched "
                   f"2D canvas.",
            "runtime": f"build {path.name}",
        })
        if errors:
            print("! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = pathlib.Path(A.out) if A.out else (
        OUTDIR / f"bloom-spread-{A.a}-{A.b}-{A.seed}.png")
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
