#!/usr/bin/env python3
"""DOES THE DRAIN SURVIVE THE PATH THE VIDEO IS RENDERED THROUGH?

Every look at this effect so far has been through `AC.__draw(m)`. The mp4 is
NOT rendered that way — `cinema_clip` drives `window.__clip.frame()`, which
pumps the sim through `CINE.pump` and draws through `CINE.drawLerped`. Those
are different code paths and only one of them has ever been checked.

Decisive and falsifiable: at a frame with drains alive, render twice — once as
is, once with `m.drains` emptied — and count the pixels that differ. If the two
images are identical the effect is not reaching the file, whatever it looks
like in a probe capture.
"""
import base64, io, pathlib, sys
from PIL import Image, ImageChops
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
HERE = pathlib.Path(__file__).parent

JS = """([id, foe, seed]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  AC.__inject && AC.__inject(m);
  const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const cv = document.getElementById('cv');
  let g = 0;
  while (g++ < 400000 && !(me.ultSplit && m.drains.length >= 8)) m.step(DT);
  if (!m.drains.length) return { error: "no drain reached" };
  /* A BURST IS INVISIBLE ON THE FRAME IT SPAWNS. Strand i does not start until
     `i * 0.052`s and `drawDrains` skips anything with u <= 0, so the instant
     `drains.length` first goes up is precisely the instant none of them is
     drawing. Step on into the burst before asking. */
  for (let k = 0; k < Math.round(0.35 / DT); k++) m.step(DT);
  const live = m.drains.filter(d => {
    const u = (d.t - d.delay) / d.life; return u > 0 && u <= 1; }).length;
  /* PIN THE SHAKE. draw() offsets the hall by (Math.random()-0.5)*m.shake on
     every call, so two renders of one state differ across the whole frame and
     a pixel diff measures the jitter rather than the thing under test. This is
     v26 §4's open decision appearing as a real obstacle. */
  m.shake = 0;
  const info = { motes: m.drains.length, live: live,
                 drained: +(th.drained||0).toFixed(2),
                 hasCine: typeof CINE !== "undefined",
                 cineOn: (typeof CINE !== "undefined") && !!CINE.on,
                 hasClip: typeof window.__clip !== "undefined" };
  const shots = {};
  /* (a) the path every probe capture has used */
  AC.__draw(m);
  shots.plain_with = cv.toDataURL('image/png');
  const keep = m.drains.slice();
  m.drains.length = 0;
  AC.__draw(m);
  shots.plain_without = cv.toDataURL('image/png');
  m.drains.push(...keep);
  /* (b) the path the mp4 is rendered through */
  if (typeof CINE !== "undefined"){
    CINE.snap(m);
    CINE.drawLerped(AC.renderer, m, 0.5);
    shots.lerp_with = cv.toDataURL('image/png');
    m.drains.length = 0;
    CINE.snap(m);
    CINE.drawLerped(AC.renderer, m, 0.5);
    shots.lerp_without = cv.toDataURL('image/png');
    m.drains.push(...keep);
  }
  return { info, shots };
}"""

with game(game_path=(HERE / "../02-chain/sc-twinshade-scrunch.html").resolve()) as (p, e):
    r = p.evaluate(JS, ["twinshade", "emberedge", 177319])
    if e: print("PAGE ERRORS:", e[:4])
if r.get("error"): sys.exit(r["error"])
print(" ", r["info"])
S = {k: Image.open(io.BytesIO(base64.b64decode(v.split(",",1)[1]))).convert("RGB")
     for k, v in r["shots"].items()}
def diff(a, b, label):
    d = ImageChops.difference(S[a], S[b])
    bbox = d.getbbox()
    px = sum(1 for p in d.getdata() if p != (0,0,0))
    mx = max(max(p) for p in d.getdata())
    print(f"  {label:<34} differing px {px:>8}   max delta {mx:>3}   bbox {bbox}")
    return px
print()
diff("plain_with", "plain_without", "AC.__draw          (probe path)")
if "lerp_with" in S:
    diff("lerp_with", "lerp_without", "CINE.drawLerped    (VIDEO path)")
