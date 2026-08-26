"""Where does the shading actually sit, in world space?

Renders the same weapon from two builds and reports, for the pixels that
differ, the mean world-y offset from the weapon's own centroid. Negative means
the change landed ABOVE the weapon's middle, positive BELOW. A world-lit facet
must stay on the same side at every facing.
"""
import pathlib, sys
sys.path.insert(0, "/home/claude/work")
from scpage import game
import numpy as np

JS = r"""(a) => {
  const [school, deg] = a;
  AC.setResolution(1080,1920);
  const c = document.getElementById('cv').getContext('2d');
  const p = AC.AFFINITIES[school];
  c.setTransform(1,0,0,1,0,0);
  c.fillStyle="#000000"; c.fillRect(0,0,400,400);
  c.save(); c.translate(200,200); c.rotate(deg*Math.PI/180);
  c.globalAlpha=1; c.shadowBlur=0;
  AC.SHAPES.greatsword(c,100,44,p,0.5,school);
  c.restore();
  return Array.from(c.getImageData(0,0,400,400).data);
}"""

def frame(path, school, deg):
    with game(game_path=pathlib.Path(path).resolve()) as (pg, errs):
        d = pg.evaluate(JS, [school, deg])
    return np.array(d, dtype=np.int16).reshape(400, 400, 4)

school = "umbral"
print(f"{'build':16} {'facing':>6} {'shaded-side offset':>19}")
base = "sc-sil.html"
for build in ["sc-tint.html", "sc-world.html"]:
    for deg in (0, 90, 180, 270):
        A, B = frame(base, school, deg), frame(build, school, deg)
        la = (0.2126*A[:,:,0] + 0.7152*A[:,:,1] + 0.0722*A[:,:,2])
        lb = (0.2126*B[:,:,0] + 0.7152*B[:,:,1] + 0.0722*B[:,:,2])
        ink = (A[:,:,:3].sum(2) > 24) | (B[:,:,:3].sum(2) > 24)
        ys, xs = np.nonzero(ink)
        cy = ys.mean()
        darker = (lb - la) < -8            # where the new build removed light
        yd = np.nonzero(darker)[0]
        off = (yd.mean() - cy) if len(yd) else float("nan")
        print(f"{build:16} {deg:>6} {off:>+19.1f}   ({len(yd)} px darkened)")
