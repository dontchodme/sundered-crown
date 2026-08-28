#!/usr/bin/env python3
"""WHY THE HARROWING FOGS THE ARENA -- decomposed, and swept across the count.

    python harrow_bloom_probe.py
    python harrow_bloom_probe.py --ns 1,6,12 --frames 7

THE MEASUREMENT THAT CAME BEFORE THIS ONE WAS THE WRONG SHAPE. ult_bloom_probe
ranks on the CASTER'S DISC, which is right for a white ball being erased by art
drawn over it -- Daybreak, Benediction. The Harrowing does not do that: the
ball stays legible at every frame and the scythes stay countable. What goes
wrong is that the WHOLE ARENA turns milky from t/life 0.09 onward. A disc
metric cannot see a full-frame wash, and three candidates built off it moved
19.5% -> 19.5%.

So this measures the arena, and it separates the two things that could be
feeding it:

  ring     one stroke, white, lineWidth ~7.5, shadowBlur 18, radius
           (66 + n*22) -- 330px at the cap
  scythes  up to twelve white sprites in `lighter`

by rendering arms with each SUPPRESSED and differencing. A single number over
the whole set-piece cannot tell you which one to change.

N IS THE VARIABLE AND THE LIBRARY HOLDS ONE SAMPLE OF IT. ult_fx_capture
caught this block with n=2; `scythes:12` is the cap, and the ring's radius is
a function of n as well. Anything that judges this ult on the captured count
is judging it on a light night. Swept here, always.

THE THREE COLUMNS
  arena     mean luma over the arena rect, chain ON. The fog itself.
  +bloom    arena mean ON minus OFF. How much of the fog the post chain made,
            as against what the art put there. This is the number that decides
            whether the fix is art or bloom, and it is the one the disc metric
            got right by accident: the Harrowing has the largest +bloom in the
            game.
  clip%     share of the arena past 0.98.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
SCRATCH = pathlib.Path(
    r"C:\Users\cathy\AppData\Local\Temp\claude\C--dev-sundered-crown"
    r"\befe3e34-b8fe-4997-82cb-efca947b8356\scratchpad")

ARMS = [("full  (ships)", None),
        ("ring only",     "sc-harrow-d-noscythe.html"),
        ("scythes only",  "sc-harrow-d-noring.html"),
        ("neither",       "sc-harrow-d-none.html")]

JS = """([t, life, block]) => {
  window.__frozen = true; AC.setResolution(1080,1920);
  AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  const m = new AC.Match("lastlight","grudgebearer",31337); m.introT=0;
  /* m.shake drives Math.random() in the draw path and would put the on/off
     arms at two different camera offsets. */
  m.shake=0;
  const A = AC.CONFIG.arena;
  m.a.x=A.w*0.26; m.a.y=A.h*0.30; m.b.x=A.w*0.74; m.b.y=A.h*0.68;
  m.a.vx=m.a.vy=m.b.vx=m.b.vy=0;
  m.ultFx = Object.assign({}, block, { src:"a", tgt:"b",
    x:m.a.x, y:m.a.y, tx:m.b.x, ty:m.b.y, aff:m.a.aff, t:t, life:life });

  const rr=Math.random;
  const pin=()=>{ let sd=0x5EEDF00D;
    Math.random=function(){sd|=0;sd=(sd+0x6D2B79F5)|0;let x=Math.imul(sd^(sd>>>15),1|sd);
      x=(x+Math.imul(x^(x>>>7),61|x))^x;return ((x^(x>>>14))>>>0)/4294967296;};};
  const r=AC.renderer,cv=document.getElementById('cv'),ctx=cv.getContext('2d');
  function arena(){
    const d=ctx.getImageData(Math.round(r.pad*r.k), Math.round(r.arenaTop*r.k),
                             Math.round(r.aw*r.k), Math.round(r.ah*r.k)).data;
    let s=0,c=0; const N=d.length/4;
    for(let i=0;i<d.length;i+=4){const L=(0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2])/255;
      s+=L; if(L>0.98)c++;}
    return {mean:s/N, clip:c/N};
  }
  const was=AC.POSTFX.on;
  pin(); AC.POSTFX.on=true;  AC.__draw(m); const on=arena();
  pin(); AC.POSTFX.on=false; AC.__draw(m); const off=arena();
  AC.POSTFX.on=was; Math.random=rr;
  return {on:on, off:off};
}"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-paradox-frame.html")
    ap.add_argument("--fx", default="../05-reference/post/ultfx-library.json")
    ap.add_argument("--ns", default="1,2,4,8,12")
    ap.add_argument("--frames", type=int, default=7)
    A = ap.parse_args()

    lib = json.loads((HERE / A.fx).resolve().read_text(encoding="utf8"))
    base = dict(lib["lastlight"]["blocks"]["bloom"])
    life = base.get("life", 1.7)
    ns = [int(x) for x in A.ns.split(",")]
    fr = [round(0.03 + 0.55 * (i / max(1, A.frames - 1)) ** 1.2, 3)
          for i in range(A.frames)]

    print(f"  THE HARROWING, bloom phase. arena rect, worst of {A.frames} frames.")
    print(f"  captured n was {base.get('n')}; the cap is 12.\n")
    rows = {}
    for lab, fname in ARMS:
        g = (HERE / A.game).resolve() if fname is None else (SCRATCH / fname)
        if not g.exists():
            sys.exit(f"! missing arm build: {g}")
        with game(game_path=g) as (page, errors):
            for n in ns:
                blk = dict(base); blk["n"] = n
                worst = None
                for f in fr:
                    s = page.evaluate(JS, [f * life, life, blk])
                    if worst is None or s["on"]["mean"] > worst["on"]["mean"]:
                        worst = s
                rows[(lab, n)] = worst
            if errors:
                sys.exit(f"{lab}: page errors {errors[:2]}")

    print(f"  {'arm':<15}" + "".join(f"{('n=' + str(n)):>19}" for n in ns))
    print(f"  {'':<15}" + "".join(f"{'arena  +bloom  clip':>19}" for n in ns))
    for lab, _ in ARMS:
        line = f"  {lab:<15}"
        for n in ns:
            w = rows[(lab, n)]
            lift = w["on"]["mean"] - w["off"]["mean"]
            line += f"{w['on']['mean']:>7.4f}{lift:>+8.4f}{100*w['on']['clip']:>5.1f}"
        print(line)

    print()
    for n in ns:
        full = rows[("full  (ships)", n)]["on"]["mean"]
        none = rows[("neither", n)]["on"]["mean"]
        ring = rows[("ring only", n)]["on"]["mean"] - none
        scy = rows[("scythes only", n)]["on"]["mean"] - none
        tot = full - none
        if tot <= 0:
            continue
        print(f"  n={n:<3} the set-piece adds {tot:+.4f} arena mean over the bare "
              f"arena -- ring {100*ring/tot:4.0f}%, scythes {100*scy/tot:4.0f}%")


if __name__ == "__main__":
    main()
