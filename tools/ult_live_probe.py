#!/usr/bin/env python3
"""THE ULTIMATES A FROZEN MATCH CANNOT SHOW — measured by stepping a real one.

    python ult_live_probe.py --ids paradox,marrowdraw,twinshade,redflail,foregone
    python ult_live_probe.py                      # all 25

WHY A THIRD PROBE
-----------------
ult_bloom_probe freezes a match and writes `m.ultFx`. That reaches any
set-piece drawn by drawUltUnder/drawUltOver, and ult_fx_capture made it honest
by supplying blocks the ENGINE built rather than blocks a session invented.

Five ultimates are still invisible to it, and not because of `phase`:

    paradox   stasis     twinshade  split      foregone  retrace
    marrowdraw ballista  redflail   spinstorm

THEY DO NOT DRAW FROM `ultFx` AT ALL. Their picture lives in MATCH STATE.
`drawSplitHold(m)` reads `m.splitHold` and is called from draw() BESIDE
drawUltOver, not from it — and it has a dozen siblings: drawShots, drawStuck,
drawSparks, drawDrains, drawRings, drawFx. No block you can assign reaches
them. Only a match that has actually been played into that state does.

So this one plays it. The ult is fired the way step() fires it (`f.charge` set
to the relic's own `ult.charge`), then the match is STEPPED and drawn frame by
frame across the window, and every frame is measured. It is the slowest of the
three probes and the only one that can see these five.

WHAT IT COSTS. One fight per relic, drawn at `--fps` and measured twice per
sampled frame (chain on, chain off). ~10s of match at 20fps is 200 samples,
400 draws. That is a few seconds a relic, not a sweep — CLAUDE.md 6 is about
SIMULATED matches and this is one match with a lot of drawing.

DETERMINISM. The sim has its own mulberry32 and never touches `Math.random`;
`Math.random` appears in the DRAW path only (the camera shake, and Unmaking's
flicker). It is pinned around each draw and restored, and `m.shake` is zeroed
for the draw and put back, so the chain-on and chain-off frames differ in one
variable and two runs agree. Neither touches a number the simulation reads.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
FOE, ALT_FOE = "grudgebearer", "dawnbringer"

JS = """([id, foe, seed, window, fps]) => {
  window0 = null;
  const W = window;
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.setResolution(1080, 1920);
  const w = AC.WEAPONS.find(x => x.id === id);
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const dt = AC.CONFIG.physics.dt;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.26; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.74; m.b.y = A.h * 0.68;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.a.charge = w.ult.charge;

  const r = AC.renderer, cv = document.getElementById('cv'), ctx = cv.getContext('2d');
  const realRandom = Math.random;
  const pin = () => { let sd = 0x5EEDF00D;
    Math.random = function(){ sd|=0; sd=(sd+0x6D2B79F5)|0;
      let x=Math.imul(sd^(sd>>>15),1|sd); x=(x+Math.imul(x^(x>>>7),61|x))^x;
      return ((x^(x>>>14))>>>0)/4294967296; }; };

  function arena(){
    const d = ctx.getImageData(Math.round(r.pad*r.k), Math.round(r.arenaTop*r.k),
                               Math.round(r.aw*r.k), Math.round(r.ah*r.k)).data;
    let s=0, c=0; const N = d.length/4;
    for (let i=0;i<d.length;i+=4){
      const L=(0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2])/255; s+=L; if(L>0.98)c++; }
    return { mean:s/N, clip:c/N };
  }
  function emissive(){
    const keep=r.roMode|0; r.roMode=3; r.draw(m); r.roMode=keep;
    const d=ctx.getImageData(0,0,cv.width,cv.height).data;
    let lit=0; for(let i=3;i<d.length;i+=4) if(d[i]>8) lit++;
    return lit;
  }

  const every = Math.max(1, Math.round(1/(fps*dt)));
  const steps = Math.ceil(W/dt);
  let best = null, baseEmis = null, i = 0, fired = false;
  const wasOn = AC.POSTFX.on;
  while (i < steps){
    m.step(dt); i++;
    if (m.ultFx || m.a.ultRadiant || m.a.ultHarrow || m.splitHold) fired = true;
    if (i % every) continue;
    const sh = m.shake; m.shake = 0;
    pin(); AC.POSTFX.on = false; AC.__draw(m); const off = arena();
    pin(); AC.POSTFX.on = true;  AC.__draw(m); const on  = arena();
    pin(); AC.POSTFX.on = false; const em = emissive();
    m.shake = sh;
    if (baseEmis === null) baseEmis = em;
    const rec = { t: i*dt, on: on, off: off, emis: em };
    if (best === null || on.mean > best.on.mean) best = rec;
    if (m.over) break;
  }
  AC.POSTFX.on = wasOn; Math.random = realRandom;
  return { best: best, fired: fired, baseEmis: baseEmis, frames: Math.floor(i/every) };
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-paradox-fx.html")
    ap.add_argument("--ids", default="paradox,marrowdraw,twinshade,redflail,foregone")
    ap.add_argument("--seed", type=int, default=31337)
    ap.add_argument("--window", type=float, default=12.0, help="seconds of match to play")
    ap.add_argument("--fps", type=float, default=20.0, help="frames measured per second")
    ap.add_argument("--json", default="")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    ids = [i.strip() for i in A.ids.split(",") if i.strip()]
    rows = []
    with game(game_path=g) as (page, errors):
        for rid in ids:
            foe = ALT_FOE if rid == FOE else FOE
            r = page.evaluate(JS, [rid, foe, A.seed, A.window, A.fps])
            b = r["best"]
            rows.append({"id": rid, "fired": r["fired"], "frames": r["frames"],
                         "t": b["t"], "arena": b["on"]["mean"],
                         "lift": b["on"]["mean"] - b["off"]["mean"],
                         "clip": b["on"]["clip"], "emis": b["emis"]})
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    rows.sort(key=lambda x: -x["lift"])
    print(f"  ULT, PLAYED NOT FROZEN -- {g.name}, {A.window}s at {A.fps}fps, worst frame")
    print(f"  {'relic':<13}{'fired':>6}{'t':>7}{'arena':>8}{'+bloom':>9}{'clip%':>8}{'emis px':>10}")
    for x in rows:
        print(f"  {x['id']:<13}{('yes' if x['fired'] else 'NO'):>6}{x['t']:>7.2f}"
              f"{x['arena']:>8.4f}{x['lift']:>+9.4f}{100*x['clip']:>8.2f}{x['emis']:>10,}")
    if any(not x["fired"] for x in rows):
        print("\n  ! a relic marked NO never entered its ultimate in the window.")
        print("    Its row is a measurement of an ordinary fight, not of an ult.")
    if A.json:
        pathlib.Path(A.json).write_text(json.dumps(rows, indent=2), encoding="utf8")


if __name__ == "__main__":
    main()
