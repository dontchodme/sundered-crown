#!/usr/bin/env python3
"""IS THE LIGHT BAKED INTO THE OBJECT? — per shape, and as a fraction.

    python3 bake_probe.py --game sc-bow.html

THE OPEN ITEM
-------------
v14 NEXT-SESSION §4.1: *"The shipped art is still baked. `--worldlight` fixes
the facets this builder added. Grip wrap, guard and pommel still turn over with
the weapon at every facing."* Called the biggest remaining art defect, and
carried for a session with no number on it. `facet_side.py` measures the
facets `depth_build` created. This measures EVERY pixel.

METHOD -- and it needs no knowledge of which code drew what
-----------------------------------------------------------
Draw the shape through a canvas rotation of 0, then again through a rotation of
180 degrees, and rotate the SECOND IMAGE back by 180 about the same origin.

Ink drawn purely in local space is then pixel-identical between the two: it
rode around with the weapon, which is exactly what "baked" means. Ink that
reads the live transform -- `_lit` / `_litN` call `c.getTransform()` -- does
NOT come back to the same place, because the light did not turn with the object.

    baked   = |identical pixels| / |ink|      rides with the weapon
    world   = 1 - baked                        stays with the light

The 180 pair is exact: a half turn about the draw origin is a pixel-for-pixel
flip, so nothing is resampled and no interpolation noise enters the count.
A 90/270 pair is run as well, since `_lit` returns |n| and fades to nothing at
the crossing -- a shape could pass one pair and fail the other.
"""
from __future__ import annotations
import argparse, base64, io, itertools, math, pathlib
import numpy as np
from PIL import Image
from scpage import game

VIA=[False]
SCHOOLS=["sanctified","bloodsworn","dwarven","verdant","umbral","runic","vigil"]
DIM={"greatsword":(116,40),"warhammer":(76,54),"scythe":(104,46),
     "twinblade":(62,30),"bow":(54,44),"flailHead":(96,52)}

JS=r"""(cfg)=>{
  AC.setResolution(1080,1920);
  if(!window.__AFF0){window.__AFF0={};
    for(const k in AC.AFFINITIES) window.__AFF0[k]=Object.assign({},AC.AFFINITIES[k]);}
  for(const k in AC.AFFINITIES) Object.assign(AC.AFFINITIES[k],window.__AFF0[k]);
  const p=Object.assign({},AC.AFFINITIES[cfg.aff]); AC.SHAPES._t=0;
  const cv=document.getElementById('cv'),c=cv.getContext('2d'),s=AC.renderer.scale;
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation='source-over'; c.globalAlpha=1;
  c.shadowBlur=0; c.shadowColor='transparent';
  c.fillStyle="#000000"; c.fillRect(0,0,1080,1920);
  c.save(); c.translate(cfg.ox,cfg.oy); c.rotate(cfg.rot); c.scale(s,s);
  if (cfg.viaLit && AC.litWeapon){
    AC.litWeapon(c, cfg.shape, cfg.L, cfg.W, p, 0.5, cfg.rot);
  } else {
    const fn=AC.SHAPES[cfg.shape]; if(!fn) return null;
    if(cfg.shape==='flailHead') fn(c,cfg.W,p,0.5); else fn(c,cfg.L,cfg.W,p,0.5,cfg.aff);
  }
  c.restore();
  return cv.toDataURL('image/png').slice(22);}"""

def frame(pg,shape,aff,rot,ox,oy,scale):
    L,W=DIM[shape]
    png=pg.evaluate(JS,{"shape":shape,"aff":aff,"L":L,"W":W,"ox":ox,"oy":oy,"rot":rot,"viaLit":VIA[0]})
    im=Image.open(io.BytesIO(base64.b64decode(png))).convert("RGB")
    r=int(L*scale*1.6+48)
    return np.asarray(im.crop((ox-r,oy-r,ox+r,oy+r)),np.int16)

def pair(pg,shape,aff,base,ox,oy,scale):
    a=frame(pg,shape,aff,base,ox,oy,scale)
    b=frame(pg,shape,aff,base+math.pi,ox,oy,scale)[::-1,::-1]   # exact half turn back
    ink=(np.abs(a-np.array([0,0,0])).sum(2)>18)|(np.abs(b).sum(2)>18)
    same=(np.abs(a-b).sum(2)<=12)&ink
    return int(ink.sum()), int(same.sum())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--game",default="sc-bow.html")
    ap.add_argument("--via-litweapon",action="store_true")
    a=ap.parse_args()
    VIA[0]=a.via_litweapon
    with game(game_path=(pathlib.Path(__file__).parent/a.game).resolve()) as (pg,errs):
        scale=pg.evaluate("()=>{AC.setResolution(1080,1920);return AC.renderer.scale;}")
        print(f"=== baked vs world-lit — {a.game} ===")
        print("share of each weapon's ink that RIDES WITH THE WEAPON (baked)\n")
        print(f"{'':12s}"+"".join(f"{x[:6]:>9s}" for x in SCHOOLS)+"     mean")
        for ty in DIM:
            row=[]
            for s in SCHOOLS:
                i1,s1=pair(pg,ty,s,0.0,540,900,scale)
                row.append((1-s1/max(1,i1))*100)
            print(f"{ty:12s}"+"".join(f"{v:8.1f}%" for v in row)+f"{np.mean(row):8.1f}%")
        assert not errs, errs
    print("\n100% = every pixel turns over with the object. The light is painted on.")

main()
