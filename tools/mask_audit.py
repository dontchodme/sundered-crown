#!/usr/bin/env python3
"""IS THE SILHOUETTE PROBE MEASURING THE WHOLE WEAPON?

`silhouette_probe.py` builds its mask by flattening every PALETTE FIELD to
white and thresholding the greyscale at 40. Ink drawn with a hardcoded near-
black literal is not a palette field, so it is not flattened -- and at
luminance < 40 it does not clear the threshold either. Such ink is INVISIBLE
TO THE MASK.

NEXT-SESSION.md §4.3 already records this failure mode for one site
(`_twinConjured`'s `#040814` shards register as EMPTY). This asks the general
question: for every shape and school, how much of the weapon's real footprint
is the probe blind to, and do the published IoU numbers move once it can see?

METHOD -- two masks per cell:
  std   exactly what silhouette_probe.py does today
  hard  every fillStyle/strokeStyle/shadowColor/gradient stop forced to white,
        ALPHA PRESERVED, so the mask is the true footprint regardless of what
        colour the shape asked for

  blind = 1 - |std| / |hard|      the share of the weapon the probe cannot see
"""
from __future__ import annotations
import argparse, base64, io, itertools, pathlib, sys
import numpy as np
from PIL import Image
from scpage import game

SCHOOLS = ["sanctified","bloodsworn","dwarven","verdant","umbral","runic","vigil"]
DIM = {"greatsword":(116,40),"warhammer":(76,54),"scythe":(104,46),
       "twinblade":(62,30),"bow":(54,44),"flailHead":(96,52)}

JS = r"""(cfg) => {
  AC.setResolution(1080, 1920);
  if (!window.__AFF0){ window.__AFF0 = {};
    for (const k in AC.AFFINITIES) window.__AFF0[k] = Object.assign({}, AC.AFFINITIES[k]); }
  for (const k in AC.AFFINITIES) Object.assign(AC.AFFINITIES[k], window.__AFF0[k]);
  const p = Object.assign({}, AC.AFFINITIES[cfg.aff]);
  p.core = p.glow = p.steel = p.dark = "#FFFFFF";
  AC.SHAPES._t = 0;
  const cv = document.getElementById('cv');
  const c  = cv.getContext('2d');
  const s  = AC.renderer.scale;

  let undo = [];
  c.setTransform(1,0,0,1,0,0);
  c.globalCompositeOperation='source-over'; c.globalAlpha=1;
  c.shadowBlur=0; c.shadowColor='transparent';
  c.fillStyle="#000000"; c.fillRect(0,0,1080,1920);
  /* HARD MODE: force every colour the shape asks for to white, keeping alpha.
     Alpha is kept because destination-out sites take their strength from the
     source alpha (depth_build --erase), and flattening it would change the
     footprint rather than just reveal it. */
  if (cfg.hard){
    const proto = Object.getPrototypeOf(c);
    const wh = (v) => {
      if (typeof v !== 'string') return v;
      if (v[0] === '#'){
        if (v.length === 9) return '#FFFFFF' + v.slice(7);
        if (v.length === 5) return '#FFFF' + v[4] + v[4];
        return '#FFFFFF';
      }
      const m = v.match(/^rgba?\(([^)]*)\)/);
      if (m){ const q = m[1].split(',').map(x=>x.trim());
              return 'rgba(255,255,255,' + (q.length>3 ? q[3] : '1') + ')'; }
      return '#FFFFFF';
    };
    for (const k of ['fillStyle','strokeStyle','shadowColor']){
      const d = Object.getOwnPropertyDescriptor(proto, k);
      Object.defineProperty(c, k, { configurable:true,
        get(){ return d.get.call(c); }, set(v){ d.set.call(c, wh(v)); } });
      undo.push(k);
    }
    for (const g of ['createLinearGradient','createRadialGradient']){
      const orig = proto[g];
      c[g] = function(){ const gr = orig.apply(c, arguments);
        const acs = gr.addColorStop.bind(gr);
        gr.addColorStop = (o, col) => acs(o, wh(col));
        return gr; };
    }
  }

  c.save(); c.translate(cfg.ox, cfg.oy); c.scale(s,s);
  const fn = AC.SHAPES[cfg.shape];
  if (!fn) return null;
  if (cfg.shape === 'flailHead') fn(c, cfg.W, p, 0.5);
  else fn(c, cfg.L, cfg.W, p, 0.5, cfg.aff);
  c.restore();
  const out = cv.toDataURL('image/png').slice(22);
  if (cfg.hard){
    for (const k of undo) delete c[k];
    delete c.createLinearGradient; delete c.createRadialGradient;
  }
  return out;
}"""

def mask(pg, shape, aff, ox, oy, scale, hard, thresh=40):
    L,W = DIM[shape]
    png = pg.evaluate(JS, {"shape":shape,"aff":aff,"L":L,"W":W,"ox":ox,"oy":oy,"hard":hard})
    im = Image.open(io.BytesIO(base64.b64decode(png))).convert("L")
    r = L*scale*1.5 + 40
    im = im.crop((int(ox-r),int(oy-r),int(ox+r),int(oy+r)))
    return np.asarray(im,dtype=np.int16) > thresh

def pad_to(a,b):
    h=max(a.shape[0],b.shape[0]); w=max(a.shape[1],b.shape[1]); out=[]
    for m in (a,b):
        z=np.zeros((h,w),bool); y0,x0=(h-m.shape[0])//2,(w-m.shape[1])//2
        z[y0:y0+m.shape[0], x0:x0+m.shape[1]]=m; out.append(z)
    return out

def iou(a,b):
    if a.shape!=b.shape: a,b = pad_to(a,b)
    u=int((a|b).sum()); return float((a&b).sum())/u if u else 1.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--game", default="sc-world.html")
    ap.add_argument("--sheet")
    a=ap.parse_args()
    with game(game_path=pathlib.Path(a.game)) as (pg,errs):
        scale = pg.evaluate("AC.renderer.scale")
        ox,oy = 540,900
        rows={}
        for ty in DIM:
            std ={s:mask(pg,ty,s,ox,oy,scale,False) for s in SCHOOLS}
            hard={s:mask(pg,ty,s,ox,oy,scale,True ) for s in SCHOOLS}
            rows[ty]=(std,hard)
        assert not errs, errs

    print(f"{a.game}\n")
    print("BLIND INK — share of the true footprint silhouette_probe.py cannot see")
    print(f"{'shape':11s} " + " ".join(f"{s[:5]:>6s}" for s in SCHOOLS) + "   worst")
    for ty,(std,hard) in rows.items():
        b=[1-std[s].sum()/max(1,hard[s].sum()) for s in SCHOOLS]
        print(f"{ty:11s} " + " ".join(f"{x*100:5.1f}%" for x in b) + f"  {max(b)*100:5.1f}%")

    print("\nIoU — published (std masks) vs true footprint (hard masks)")
    print(f"{'shape':11s} {'std min':>8s} {'std mean':>9s} | {'hard min':>9s} {'hard mean':>10s} | {'d min':>7s}")
    for ty,(std,hard) in rows.items():
        ps=list(itertools.combinations(SCHOOLS,2))
        sv=[iou(std[x],std[y]) for x,y in ps]
        hv=[iou(hard[x],hard[y]) for x,y in ps]
        print(f"{ty:11s} {min(sv):8.3f} {np.mean(sv):9.3f} | {min(hv):9.3f} {np.mean(hv):10.3f} | "
              f"{min(hv)-min(sv):+7.3f}")

    if a.sheet:
        cells=[]
        CW=max(m.shape[1] for st,hd in rows.values() for m in list(st.values())+list(hd.values()))
        CH=max(m.shape[0] for st,hd in rows.values() for m in list(st.values())+list(hd.values()))
        sheet=Image.new("RGB",(CW*len(SCHOOLS), CH*len(rows)*2),(8,8,10))
        for r,(ty,(std,hard)) in enumerate(rows.items()):
            for k,src in enumerate((std,hard)):
                for cix,s in enumerate(SCHOOLS):
                    m=src[s]; rgb=np.zeros(m.shape+(3,),np.uint8)
                    rgb[m]= (255,255,255) if k else (150,150,160)
                    if k:  # mark what std missed
                        d=m & ~std[s] if std[s].shape==m.shape else m
                        rgb[d]=(255,60,60)
                    im=Image.fromarray(rgb)
                    sheet.paste(im,(cix*CW+(CW-m.shape[1])//2,(r*2+k)*CH+(CH-m.shape[0])//2))
        sheet.save(a.sheet); print(f"\nsheet -> {a.sheet}  (row pairs: std grey / hard white, RED = ink the probe misses)")

main()
