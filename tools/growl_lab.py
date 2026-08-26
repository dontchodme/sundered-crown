#!/usr/bin/env python3
"""FIT THE GROWL TO A REFERENCE RECORDING, BY MEASUREMENT.

    python3 growl_lab.py

The cast voice took four cuts. The first three were each an adjective
translated into synthesis parameters and each was wrong in a different way --
"a fart", then inaudible sub-bass, then "rolling thunder" -- and none of them
could be argued about, because the only instrument was somebody listening.

Rick supplied a recording. This measured four separate growls in it and turned
the brief into numbers: six band shares and a modulation rate. Then it sweeps
`_growl`'s parameters THROUGH THE SHIPPING CHAIN and reports the total band
error against that target. 65.9 points on the first fit, 6.4 on the last.

TWO THINGS IT HAD TO LEARN THE HARD WAY, both of which invalidated a fit:

  * MEASURE THROUGH `buildChain`. Rendering to `destination` measures a signal
    path nobody hears; the chain's EQ and limiter move the profile 30 points.
  * DO NOT RENDER AT TIME ZERO. An AudioParam whose first automation event is
    at t > 0 holds its constructor default until then, so a growl fitted at
    t=0 measures a case a live match cannot produce -- 19/49/25 on the bench
    against 12/68/15 in the game, same code.

Reads nothing from the repo but the build. Writes nothing.
"""
import pathlib, sys, json, itertools
sys.path.insert(0,'/root/sc/sc/sc/tools')
from scpage import game
import numpy as np
REF=np.array([17.9,49.5,25.7,5.4,0.7,0.2]); BANDS=[(20,60),(60,120),(120,300),(300,700),(700,1500),(1500,20000)]
JS = r"""async ([P, secs]) => {
  const OC = window.OfflineAudioContext, S = AC.SFX, sr = 48000;
  const sv={on:S.on,ok:S.ok,ctx:S.ctx,bus:S.bus,noise:S.noise};
  const off=new OC(1, Math.round(sr*secs), sr);
  S.ctx=off; S.ok=true; S.on=true;
  S.bus=S.constructor.buildChain(off, off.destination);
  S.noise=S._noiseBuffer();
  S._growl(0, P);
  const buf=await off.startRendering();
  S.on=sv.on;S.ok=sv.ok;S.ctx=sv.ctx;S.bus=sv.bus;S.noise=sv.noise;
  return Array.from(buf.getChannelData(0));
}"""
def meas(d, sr=48000):
    c=int(len(d)*0.30); seg=d[c:c+65536]
    S=np.abs(np.fft.rfft(seg*np.hanning(len(seg))))**2
    f=np.fft.rfftfreq(len(seg),1/sr); tot=S.sum()
    return np.array([100*S[(f>=lo)&(f<hi)].sum()/tot for lo,hi in BANDS]), np.abs(d).max()
base=dict(dur=4.6,gain=0.26,depth=0.56,rough=7.5,swell=0.8,f0=78,f0b=80.5,sub=39,
          subG=0.65,lp=330,lpQ=0.8,lp2=140,hp=34,sag=0.92,breath=1.5,breathF=400,rasp=0.12)
grid=[]
for subG in (0.65,1.1,1.6):
    for lp2 in (140,210,300):
        for hp in (34,26):
            grid.append(dict(subG=subG,lp2=lp2,hp=hp))
print("  "+" "*30+"20-60 60-120 120-300 300-700  700+ 1500+   peak   ERR")
print(f"  {'TARGET':30}"+" ".join(f"{v:5.1f}" for v in REF))
best=(1e9,None,None)
with game(game_path=pathlib.Path('/root/sc/sc/sc/02-chain/sc-marrowdraw.html')) as (page,errs):
    for over in grid:
        P=dict(base); P.update(over)
        d=np.array(page.evaluate(JS,[P,6.0]),dtype=np.float32)
        sh,pk=meas(d); e=np.abs(sh-REF).sum()
        nm=f"subG{over['subG']} lp2={over['lp2']} hp={over['hp']}"
        print(f"  {nm:30}"+" ".join(f"{v:5.1f}" for v in sh)+f"  {pk:5.2f}  {e:5.1f}")
        if e<best[0]: best=(e,nm,P)
print(f"\n  best: {best[1]}  ERR {best[0]:.1f}")
pathlib.Path('/tmp/g9.json').write_text(json.dumps(best[2]))
