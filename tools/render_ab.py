#!/usr/bin/env python3
"""DOES THIS BUILD DRAW THE SAME PICTURE THE LAST ONE DREW?

    python render_ab.py --a <prev build> --b <this build>
    python render_ab.py --a <prev> --b <this> --frames 0.5,6,12,22,31 --n 6

`engine_ab.py` proves two builds run the same FIGHT. It says nothing at all
about the picture -- `Fighter`, `Match` and `Sfx` contain no reference to a
canvas, which is exactly why a renderer change comes back 2760/2760 whether it
was harmless or a disaster. This repo has been bitten twice by a defect where
wrong and right produce identical numbers, and a renderer refactor is the
purest possible source of that class.

So: same relics, same seed, same frame indices, both builds, and every pixel
compared. It is engine_ab for the picture and it should have existed before
the first renderer change, not after.

WHAT WOULD COUNT AS EVIDENCE AGAINST a "this cannot have changed the picture"
claim: one channel of one pixel differing on any sampled frame.

Runs both builds in ONE Playwright session so the rasteriser is the same for
both -- the comparison is worth nothing across runtimes, and on a machine
where the two Chromiums disagree in the last bit of Math.pow it would not even
be the same fight (docs/RUNTIME-DRIFT.md).
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent

FRAMES_JS = r"""
(cfg) => {
  window.__frozen = true;
  AC.setResolution(cfg.w, cfg.h);
  const cv = document.getElementById('cv');
  const ctx = cv.getContext('2d');
  const dt = AC.CONFIG.physics.dt;
  const out = [];
  for (const pair of cfg.pairs) {
    const m = new AC.Match(pair[0], pair[1], pair[2] >>> 0);
    m.introT = 0;
    AC.__inject(m);
    AC.SFX.play = function () {};
    let cursor = 0;
    for (const at of cfg.frames) {
      while (m.t < at - dt * 0.5 && !m.over) m.step(dt);
      /* The camera shake calls Math.random(), which would make two draws of
         the same frame differ inside ONE build and turn this check into
         noise. Pinned, exactly as hud_cost.py pins it. */
      m.shake = 0;
      if (cfg.roMode !== undefined) AC.renderer.roMode = cfg.roMode;
      AC.__draw(m);
      const d = ctx.getImageData(0, 0, cv.width, cv.height).data;
      /* A hash per frame, not the pixels: shipping 8 MB of RGBA per frame
         across the bridge is what makes a check like this too slow to run,
         and too slow to run is the same as absent. FNV-1a over every byte. */
      let h = 2166136261 >>> 0;
      for (let i = 0; i < d.length; i++) {
        h ^= d[i];
        h = Math.imul(h, 16777619) >>> 0;
      }
      /* and a cheap signature so a mismatch can be described, not just
         reported: mean luma and the count of non-black pixels. */
      let sum = 0, lit = 0;
      for (let i = 0; i < d.length; i += 4 * 17) {
        const l = 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
        sum += l;
        if (l > 8) lit++;
      }
      const n = Math.ceil(d.length / (4 * 17));
      out.push({ a: pair[0], b: pair[1], seed: pair[2], t: +m.t.toFixed(3),
                 hash: h, meanLuma: +(sum / n).toFixed(3),
                 lit: +(100 * lit / n).toFixed(2) });
    }
  }
  return out;
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="control build")
    ap.add_argument("--b", required=True, help="variant build")
    ap.add_argument("--pairs",
                    default="paradox:heartwood:25064,"
                            "ironhail:dawnbringer:4412,"
                            "twinshade:lastlight:991,"
                            "bulwarden:vinesower:70707")
    ap.add_argument("--frames", default="0.5,6,12,22,31,40",
                    help="seconds into the fight")
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--h", type=int, default=960)
    ap.add_argument("--romode", type=int, default=None,
                    help="force renderer.roMode on BOTH builds")
    A = ap.parse_args()

    pa = pathlib.Path(A.a).resolve()
    pb = pathlib.Path(A.b).resolve()
    for p in (pa, pb):
        if not p.exists():
            print(f"! {p} does not exist")
            return 2

    pairs = []
    for spec in A.pairs.split(","):
        x, y, s = spec.split(":")
        pairs.append([x, y, int(s)])
    frames = [float(f) for f in A.frames.split(",")]
    cfg = {"pairs": pairs, "frames": frames, "w": A.w, "h": A.h}
    if A.romode is not None:
        cfg["roMode"] = A.romode

    print(f"\nRENDER A/B  {len(pairs)} pairings x {len(frames)} frames  "
          f"{A.w}x{A.h}"
          + (f"  roMode={A.romode}" if A.romode is not None else ""))
    print(f"  a  {pa.name}")
    print(f"  b  {pb.name}")

    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=["--disable-frame-rate-limit", "--disable-gpu", "--no-sandbox"])
        res = {}
        for tag, path in (("a", pa), ("b", pb)):
            page = browser.new_page(viewport={"width": 620, "height": 1000})
            page.on("pageerror", lambda e, t=tag: errors.append(f"{t}: {e}"))
            page.on("console",
                    lambda mm, t=tag: errors.append(f"{t}: {mm.text}")
                    if mm.type == "error" else None)
            page.goto(path.as_uri())
            page.wait_for_function(
                "window.AC && window.AC.WEAPONS && window.__fontsReady !== false",
                timeout=20000)
            res[tag] = page.evaluate(FRAMES_JS, cfg)
            page.close()
        browser.close()

    if errors:
        print("! page errors:")
        for e in errors[:10]:
            print("   ", e)
        return 1

    ra, rb = res["a"], res["b"]
    if len(ra) != len(rb):
        print(f"! different frame counts: {len(ra)} vs {len(rb)}")
        return 1

    bad = 0
    for x, y in zip(ra, rb):
        if (x["a"], x["b"], x["seed"], x["t"]) != (y["a"], y["b"], y["seed"], y["t"]):
            print(f"  MISALIGNED {x} vs {y}")
            bad += 1
            continue
        if x["hash"] != y["hash"]:
            bad += 1
            print(f"  {x['a']} v {x['b']} seed {x['seed']} t={x['t']:>6.2f}  "
                  f"DIFFERS   luma {x['meanLuma']:.3f} -> {y['meanLuma']:.3f}   "
                  f"lit {x['lit']:.2f}% -> {y['lit']:.2f}%")

    n = len(ra)
    if bad:
        print(f"\nFAIL  {n - bad}/{n} frames identical.")
        print("      The picture moved. If that was intended, this is the")
        print("      receipt for HOW MUCH; if it was not, the change is not")
        print("      the no-op it was described as.")
        return 1
    print(f"\nPASS  {n}/{n} frames pixel-identical.")
    print("      Same relics, same seeds, same frame indices, one runtime.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
