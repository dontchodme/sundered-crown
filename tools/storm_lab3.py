#!/usr/bin/env python3
"""storm_lab, third pass: the LOUD arm's own ladders — ricochet count, blast radius, ward per bolt."""
import sys, json, pathlib, statistics
src = (pathlib.Path(__file__).parent / "storm_lab.py").read_text().split("t0 = time.time()")[0]
ns = {}; exec(compile(src, "storm_lab.py", "exec"), ns)
run_arm, BASE = ns["run_arm"], ns["BASE"]
LOUD = dict(BASE, rb=16, fork_net=2, per_hit=8, window=8, det=8, ric=99)
def arm(label, base=LOUD, **kw):
    P = dict(base); P.update(kw); return run_arm(P, label)
def show(rs, extra=()):
    print(f"  {'arm':<34}{'spawn':>7}{'fork':>7}{'peak':>6}{'eaten':>7}{'walls':>7}{'alive':>7}{'in rx':>7}{'zero':>6}{'ward':>7}{'w.cap':>7}")
    for r in rs:
        print(f"  {r['label']:<34}{r['spawned']:>7.1f}{r['forked']:>7.1f}{r['peak']:>6.1f}"
              f"{r['consumed']:>7.1f}{r['died']:>7.1f}{r['at_det']:>7.1f}{r['in_rx']:>7.2f}{1-r['p_any']:>6.0%}{r['ward']:>7.1f}{r['ward_capped']:>7.1f}")
out = []
print("LOUD arm = fork +2, 8 bolts a hit, thick (r16), window 8 = detonation 8, speed 600\n")
print("RICOCHETS before a bolt dies"); rs = [arm(f"ric {r}", ric=r) for r in (3, 6, 9, 12, 99)]; show(rs); out += rs
print("\nBLAST RADIUS"); rs = [arm(f"rx {r}", rx=r) for r in (40, 60, 80, 100, 130)]; show(rs); out += rs
print("\nWARD PER EATEN BOLT"); rs = [arm(f"bank {b}", bank=b) for b in (1, 2, 3, 4)]; show(rs); out += rs
print("\nBOLTS PER HIT on the loud arm"); rs = [arm(f"per hit {k}", per_hit=k) for k in (4, 6, 8, 10)]; show(rs); out += rs
print("\nSPEED on the loud arm"); rs = [arm(f"speed {v}", speed=v) for v in (350, 500, 600, 800)]; show(rs); out += rs
print("\nONE TIMER OR TWO on the loud arm"); rs = [arm("w8 det8 (one moment)"), arm("w6 det8 (2s of flight after)", window=6), arm("w8 det10", det=10), arm("w5 det5", window=5, det=5)]; show(rs); out += rs
# distribution of in_rx for the loud arm at rx 80
P = dict(LOUD, rx=80)
import numpy as np
rng = np.random.default_rng(7); vals = []
for tr in ns["TR"]:
    t0 = 15.0
    while True:
        c = ns["run_cast"](tr, t0, P, rng)
        if c is None: break
        vals.append(c["in_rx"]); t0 += 15.0
vals = np.array(vals)
print(f"\nin-blast count at rx 80, {len(vals)} casts: mean {vals.mean():.2f}  median {np.median(vals):.0f}  "
      f"p25 {np.percentile(vals,25):.0f}  p75 {np.percentile(vals,75):.0f}  p90 {np.percentile(vals,90):.0f}  zero {np.mean(vals==0):.0%}")
json.dump(out, open("storm_lab3.json", "w"), indent=1)
