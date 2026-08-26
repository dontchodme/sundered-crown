"""How many extra getTransform calls does --worldlight cost per frame?

A COUNT, not a timing. bench_build.py's own docstring says a headless container
cannot honestly time a frame -- no GPU, and the three in-container methods
disagreed by three orders of magnitude. So count the calls here and let the
perf build measure the cost on Rick's hardware.
"""
import pathlib, sys
sys.path.insert(0, "/home/claude/work")
from scpage import game

JS = r"""() => {
  AC.setResolution(1080,1920);
  const proto = CanvasRenderingContext2D.prototype;
  const orig = proto.getTransform;
  let n = 0;
  proto.getTransform = function(){ n++; return orig.apply(this, arguments); };
  const m = new AC.Match('grudgebearer', 'thornwake', 1198145675);
  let frames = 0;
  for (let i = 0; i < 600; i++){ m.step(1/60); AC.__draw(m); frames++; }
  proto.getTransform = orig;
  return {calls: n, frames};
}"""

for build in sys.argv[1:]:
    p = pathlib.Path(build).resolve()
    with game(game_path=p) as (pg, errs):
        try:
            r = pg.evaluate(JS)
            print(f"{p.name:16} {r['calls']:>7} calls / {r['frames']} frames "
                  f"= {r['calls']/r['frames']:.2f} per frame")
        except Exception as e:
            print(f"{p.name:16} probe failed: {str(e)[:160]}")
