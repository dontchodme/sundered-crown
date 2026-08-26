#!/usr/bin/env python3
"""Film a real Ironbloom, at true frame rate. The law is WATCH IT.

    python3 ironbloom_clip.py --game sc-slagheart.html --b thornwake

Two passes over the same deterministic match: the first finds the frame the
head bites, the second replays and captures around it. Nothing is staged —
this is a cast that happened in a fight nobody arranged.
"""
from __future__ import annotations
import argparse, base64, io, pathlib, subprocess, tempfile
from PIL import Image
from scpage import game

HERE = pathlib.Path(__file__).parent

FIND = """([a, b, seed, cine, RES]) => {
  window.__frozen = true; AC.setResolution(RES[0], RES[1]);
  if (typeof CINE !== "undefined") CINE.on = cine;
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const dt = AC.CONFIG.physics.dt;
  const m = new AC.Match(a, b, seed); AC.__inject(m);
  let lit = -1, bite = -1, i = 0;
  for (; i < 120 * 120 && !m.over; i++){
    const hadHeat = !!m.a.ultHeat;
    m.step(dt);
    if (lit < 0 && !hadHeat && m.a.ultHeat) lit = i;
    if (bite < 0 && m.latch){ bite = i; break; }
  }
  return { lit, bite };
}"""

PLAY = """([a, b, seed, from_, n, every, cine, RES]) => {
  window.__frozen = true; AC.setResolution(RES[0], RES[1]);
  if (typeof CINE !== "undefined") CINE.on = cine;
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const dt = AC.CONFIG.physics.dt;
  const m = new AC.Match(a, b, seed); AC.__inject(m);
  for (let i = 0; i < from_; i++) m.step(dt);
  const out = [];
  for (let k = 0; k < n; k++){
    for (let s = 0; s < every; s++) m.step(dt);
    AC.__draw(m);
    out.push(document.getElementById('cv').toDataURL('image/png').slice(22));
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="sc-slagheart.html")
    ap.add_argument("--b", default="thornwake")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--pre", type=float, default=2.2, help="seconds before the bite")
    ap.add_argument("--post", type=float, default=4.2, help="seconds after")
    ap.add_argument("--cine", action="store_true", help="leave the director on")
    ap.add_argument("--out", default="ironbloom.mp4")
    ap.add_argument("--strip", default="ironbloom-strip.png")
    a = ap.parse_args()
    every = max(1, round(120 / a.fps))

    with game(game_path=(HERE / a.game).resolve()) as (pg, errs):
        f = pg.evaluate(FIND, ["slagheart", a.b, a.seed, a.cine, [540, 960]])
        if f["bite"] < 0:
            print(f"no bite in this match (lit at frame {f['lit']}) — try another seed")
            return 1
        start = max(0, f["bite"] - int(a.pre * 120))
        n = int((a.pre + a.post) * a.fps)
        print(f"  bite at frame {f['bite']} ({f['bite']/120:.1f}s), "
              f"head lit at {f['lit']/120:.1f}s — capturing {n} frames")
        pngs = pg.evaluate(PLAY, ["slagheart", a.b, a.seed, start, n, every, a.cine, [540, 960]])
        assert not errs, errs

    ims = [Image.open(io.BytesIO(base64.b64decode(p))).convert("RGB") for p in pngs]
    with tempfile.TemporaryDirectory() as td:
        for i, im in enumerate(ims):
            im.save(f"{td}/f{i:04d}.png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps),
                        "-i", f"{td}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-crf", "21", str(HERE / a.out)], check=True)
    # a strip across the beat, for a still read
    pick = [int(len(ims) * q) for q in (0.06, 0.26, 0.36, 0.40, 0.44, 0.47, 0.52, 0.70)]
    W = 240
    strip = Image.new("RGB", (W * len(pick), W * 960 // 540), (10, 8, 16))
    for i, k in enumerate(pick):
        strip.paste(ims[min(k, len(ims)-1)].resize((W, W*960//540), Image.LANCZOS), (i*W, 0))
    strip.save(HERE / a.strip)
    print(f"  {a.out}  {len(ims)} frames @ {a.fps}fps · {a.strip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
