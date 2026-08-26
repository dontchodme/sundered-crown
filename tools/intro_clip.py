#!/usr/bin/env python3
"""The intro at true frame rate, because a 12.5fps GIF cannot testify about
smoothness. Renders the card plus the first second of the fight at 30fps and
encodes an mp4 (silent — the clank and the bell still need the live page).

    python3 intro_clip.py --game sc-intro.html --a gravemourn --b thornwake

Every frame is a pure function of introT, so this is deterministic and the
motion on screen is exactly the motion the live page computes — the only
thing a video cannot carry is the display's own refresh.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import subprocess
import tempfile

from PIL import Image
from scpage import game

HERE = pathlib.Path(__file__).parent

FRAME_JS = """([a, b, seed, e]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  if (!window.__clipM || window.__clipM.seed !== seed ||
      window.__clipM.a.w.id !== a){
    window.__clipM = new AC.Match(a, b, seed);
    AC.__inject(window.__clipM);
  }
  const m = window.__clipM;
  if (e !== null){ m.introT = Math.max(0.0001, AC.CONFIG.intro.dur - e); }
  else {
    m.introT = 0;
    for (let s = 0; s < 4; s++) m.step(AC.CONFIG.physics.dt);
  }
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png').slice(22);
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="sc-intro.html")
    ap.add_argument("--a", default="gravemourn")
    ap.add_argument("--b", default="thornwake")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--tail", type=float, default=1.2, help="seconds of fight")
    ap.add_argument("--out", default="intro-preview.mp4")
    args = ap.parse_args()

    frames = []
    with game(game_path=(HERE / args.game).resolve()) as (pg, errs):
        dur = pg.evaluate("() => AC.CONFIG.intro.dur")
        n_intro = int(dur * args.fps)
        for i in range(n_intro):
            frames.append(pg.evaluate(
                FRAME_JS, [args.a, args.b, args.seed, i / args.fps]))
        for _ in range(int(args.tail * args.fps)):
            frames.append(pg.evaluate(FRAME_JS, [args.a, args.b, args.seed, None]))
        assert not errs, errs

    with tempfile.TemporaryDirectory() as td:
        for i, f in enumerate(frames):
            im = Image.open(io.BytesIO(base64.b64decode(f))).convert("RGB")
            im.resize((540, 960)).save(f"{td}/f{i:04d}.png")
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(args.fps),
             "-i", f"{td}/f%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-crf", "22", str(HERE / args.out)],
            check=True)
    print(f"{args.out}  {len(frames)} frames @ {args.fps}fps "
          f"({args.a} vs {args.b}, seed {args.seed})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
