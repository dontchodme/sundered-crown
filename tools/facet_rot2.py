"""Same question, better instrument.

The first version split the frame at a fixed row, which at diagonal facings
measures WHERE the blade is rather than which of its faces is dark. This one
regresses ink luminance against world y over the weapon's own pixels, so it is
position-independent: slope < 0 means the object gets darker downward at that
facing, which is what a fixed overhead light does.
"""
import pathlib, sys
sys.path.insert(0, "/home/claude/work")
from scpage import game

JS = r"""(school) => {
  AC.setResolution(1080,1920);
  const cv = document.getElementById('cv'), c = cv.getContext('2d');
  const p = AC.AFFINITIES[school], out = [];
  for (let deg = 0; deg < 360; deg += 30){
    c.setTransform(1,0,0,1,0,0);
    c.fillStyle="#000000"; c.fillRect(0,0,400,400);
    c.save(); c.translate(200,200); c.rotate(deg*Math.PI/180);
    c.globalAlpha=1; c.shadowBlur=0;
    AC.SHAPES.greatsword(c,100,44,p,0.5,school);
    c.restore();
    const d = c.getImageData(0,0,400,400).data;
    let n=0, sy=0, sL=0, syy=0, syL=0;
    for (let y=0;y<400;y++) for (let x=0;x<400;x++){
      const i=(y*400+x)*4;
      if (d[i]+d[i+1]+d[i+2] < 24) continue;
      const L=0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2];
      n++; sy+=y; sL+=L; syy+=y*y; syL+=y*L;
    }
    const den = n*syy - sy*sy;
    out.push({deg, n, slope: den ? +(((n*syL - sy*sL)/den)).toFixed(3) : null});
  }
  return out;
}"""

path = pathlib.Path(sys.argv[1]).resolve()
school = sys.argv[2] if len(sys.argv) > 2 else "umbral"
with game(game_path=path) as (pg, errs):
    rows = pg.evaluate(JS, school)
neg = sum(1 for r in rows if r["slope"] is not None and r["slope"] < 0)
print(f"{path.name:16} {school:9} " +
      " ".join(f"{r['slope']:+.2f}" for r in rows if r["slope"] is not None) +
      f"   | darker-downward at {neg}/{len(rows)} facings")
