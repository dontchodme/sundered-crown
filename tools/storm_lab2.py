#!/usr/bin/env python3
"""storm_lab, second pass: what makes the swarm GROW. Same overlay, same tracks,
same controls (asserted in run_cast). Adds the time-averaged swarm size."""
import sys, json, statistics
sys.argv = [sys.argv[0]] + sys.argv[1:]
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("sl", pathlib.Path(__file__).parent / "storm_lab.py")
# reuse storm_lab's machinery without running its sweep: exec up to the sweep
src = (pathlib.Path(__file__).parent / "storm_lab.py").read_text().split("t0 = time.time()")[0]
ns = {}; exec(compile(src, "storm_lab.py", "exec"), ns)
run_arm, BASE, TR = ns["run_arm"], ns["BASE"], ns["TR"]

def arm(label, **kw):
    P = dict(BASE); P.update(kw)
    r = run_arm(P, label)
    # time-averaged alive bolts over the cast, from the series
    return r

def show(rs):
    print(f"  {'arm':<40}{'hits':>5}{'spawn':>7}{'fork':>7}{'peak':>6}{'eaten':>7}{'walls':>7}{'alive':>7}{'in rx':>7}{'any':>6}{'ward':>7}")
    for r in rs:
        print(f"  {r['label']:<40}{r['hits']:>5.1f}{r['spawned']:>7.1f}{r['forked']:>7.1f}{r['peak']:>6.1f}"
              f"{r['consumed']:>7.1f}{r['died']:>7.1f}{r['at_det']:>7.1f}{r['in_rx']:>7.2f}{r['p_any']:>6.0%}{r['ward']:>7.1f}")

out = []
print("GROWTH — what it takes for the swarm to outrun the caster eating it\n")
rs = [arm("BASE (fork +1, ric 4, rb 8)"),
      arm("fork +2 ('two MORE')", fork_net=2),
      arm("no wall death (ric 99)", ric=99),
      arm("fork +2, ric 99", fork_net=2, ric=99),
      arm("thick bolts rb 16", rb=16),
      arm("thick rb 16, fork +2, ric 99", rb=16, fork_net=2, ric=99),
      arm("rb 16, fork +2, ric 99, k8", rb=16, fork_net=2, ric=99, per_hit=8),
      arm("rb 16, fork +2, ric 99, k8, slow 350", rb=16, fork_net=2, ric=99, per_hit=8, speed=350),
      arm("rb 16, fork +2, ric 99, k8, cap 30", rb=16, fork_net=2, ric=99, per_hit=8, cap=30),
      arm("rb 16, fork +2, ric 99, k8, w6 det6", rb=16, fork_net=2, ric=99, per_hit=8, det=6),
      arm("rb 16, fork +2, ric 99, k8, w8 det8", rb=16, fork_net=2, ric=99, per_hit=8, window=8, det=8),
      arm("rb 16, fork +2, ric 99, k8, w8 det8 rx100", rb=16, fork_net=2, ric=99, per_hit=8, window=8, det=8, rx=100),
      ]
show(rs); out += rs
print("\nCASTER AS SINK — what if the caster did NOT eat bolts (bolts pass through it)")
# emulate by making the caster contact impossible: bank stays 0 and consumption off via huge negative? simplest: rb tiny for caster isn't separable; use a flag
rs = [arm("BASE, caster eats", eat=True),
      arm("BASE, caster does not eat", eat=False),
      arm("fork +2 ric 99 rb16 k8, no eat", rb=16, fork_net=2, ric=99, per_hit=8, eat=False)]
show(rs); out += rs
json.dump(out, open("storm_lab2.json", "w"), indent=1)
