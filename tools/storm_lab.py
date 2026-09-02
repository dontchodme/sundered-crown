#!/usr/bin/env python3
"""THE SWARM, PRICED BY OVERLAY — v64, the vigil twinblade.

Rick's §1 (2026-09-02): for a window, every blade hit spawns several lightning
bolts at the foe; bolts ricochet off the walls N times then vanish; a bolt that
touches the FOE forks into two and refreshes its ricochets; a bolt that touches
the CASTER is consumed and banks ward; a second timer from the cast detonates
every bolt in a small radius for damage.

Nothing in the window deals damage, so the swarm can be run OFFLINE over real
recorded fights (storm_tracks.py) without touching the simulation. What that
buys: the swarm's size, its growth, who eats it, how much ward it pays, and
the one number the whole cast is priced by -- how many bolts are inside the
small radius of the foe at the instant the timer ends.

DECLARED LIMITS. (1) The ward the swarm banks would change the fight it is
overlaid on; not modelled, second order. (2) The foe does not react to bolts
because bolts do nothing to it until the detonation -- which is exactly true
of §1 as written. (3) Bolts are points of radius `rb` moving in straight lines
between wall bounces; the game's own projectile engine (Winnowing: speed 420,
r 10, bounce 3) is the reference for what a bolt can be.

CONTROLS THAT CAN FAIL. Bookkeeping: spawned + forked == consumed + died on
walls + alive at detonation, per cast, exactly. Fork-off arm: with forking
disabled the fork count must be 0 and the swarm must never exceed spawns.
Both are asserted, not printed.
"""
from __future__ import annotations
import argparse, json, math, pathlib, statistics, sys, time
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--tracks", default="/tmp/storm_tracks.json")
ap.add_argument("--out", default="/tmp/storm_lab.json")
ap.add_argument("--charge", type=float, default=15.0, help="cast metronome, s")
a = ap.parse_args()

T = json.loads(pathlib.Path(a.tracks).read_text())
W, H, R = T["arena"]["w"], T["arena"]["h"], T["ballR"]
DT = T["sample"]
TR = T["tracks"]

BASE = dict(window=6.0, per_hit=4, speed=600.0, rb=8.0, ric=4, fork=True,
            fork_net=1, grace=0.30, cap=60, det=8.0, rx=50.0, bank=4.0,
            cap_ward=90.0)


def run_cast(tr, t0, P, rng):
    """One cast at time t0 over track tr. Returns a dict of counts."""
    mx, my, fx, fy, hit, sh = (np.array(tr[k]) for k in ("mx", "my", "fx", "fy", "hit", "sh"))
    n = len(mx)
    i0 = int(round(t0 / DT))
    i_end = int(round((t0 + P["det"]) / DT))
    if i_end >= n:
        return None                      # fight ended inside the cast
    i_win = int(round((t0 + P["window"]) / DT))
    # bolt arrays
    bx = np.zeros(0); by = np.zeros(0); bvx = np.zeros(0); bvy = np.zeros(0)
    bric = np.zeros(0, dtype=int); bgr = np.zeros(0)      # grace until (time)
    spawned = forked = consumed = died = 0
    ward = 0.0; ward_capped = 0.0
    peak = 0; series = []
    contact = R + P["rb"]
    consumed_fast = 0
    btime = np.zeros(0)

    def add(x, y, k, t, refresh=None):
        nonlocal bx, by, bvx, bvy, bric, bgr, btime
        ang = rng.uniform(0, 2 * math.pi, k)
        bx = np.concatenate([bx, np.full(k, x, float)])
        by = np.concatenate([by, np.full(k, y, float)])
        bvx = np.concatenate([bvx, P["speed"] * np.cos(ang)])
        bvy = np.concatenate([bvy, P["speed"] * np.sin(ang)])
        bric = np.concatenate([bric, np.full(k, P["ric"], int)])
        bgr = np.concatenate([bgr, np.full(k, t + P["grace"])])
        btime = np.concatenate([btime, np.full(k, t)])

    for i in range(i0, i_end + 1):
        t = i * DT
        # spawn on the caster's blade hits, inside the window
        if i < i_win and hit[i] > 0:
            k = int(hit[i]) * P["per_hit"]
            k = min(k, max(0, P["cap"] - len(bx)))
            if k:
                add(fx[i], fy[i], k, t); spawned += k
        if len(bx):
            # move
            bx = bx + bvx * DT; by = by + bvy * DT
            # walls: reflect or die
            rb = P["rb"]
            alive = np.ones(len(bx), bool)
            for arr, v, lo, hi in ((bx, bvx, rb, W - rb), (by, bvy, rb, H - rb)):
                out = (arr < lo) | (arr > hi)
                if out.any():
                    dead = out & (bric <= 0)
                    alive &= ~dead
                    refl = out & ~dead
                    arr[refl] = np.where(arr[refl] < lo, 2 * lo - arr[refl], 2 * hi - arr[refl])
                    v[refl] *= -1
                    bric[refl] -= 1
            died += int((~alive).sum())
            # caster eats
            dc = np.hypot(bx - mx[i], by - my[i])
            eat = alive & (dc < contact) & P.get("eat", True)
            ne = int(eat.sum())
            if ne:
                consumed += ne
                consumed_fast += int((t - btime[eat] < 0.5).sum())
                w = ne * P["bank"]
                ward += w
                ward_capped += max(0.0, min(P["cap_ward"], sh[i] + w) - sh[i])
                alive &= ~eat
            # foe forks
            if P["fork"]:
                df = np.hypot(bx - fx[i], by - fy[i])
                fk = alive & (df < contact) & (bgr <= t)
                nf = int(fk.sum())
                if nf:
                    room = max(0, P["cap"] - int(alive.sum()))
                    bric[fk] = P["ric"]; bgr[fk] = t + P["grace"]
                    kk = min(nf * P["fork_net"], room)
                    forked += kk
                    idx = np.flatnonzero(fk)[:kk] if P["fork_net"] == 1 else None
                    if kk:
                        # new bolts leave from the foe in fresh directions
                        add(fx[i], fy[i], kk, t)
                        alive = np.concatenate([alive, np.ones(kk, bool)])
            keep = alive
            bx, by, bvx, bvy, bric, bgr, btime = (arr[keep] for arr in (bx, by, bvx, bvy, bric, bgr, btime))
        peak = max(peak, len(bx))
        if i % 6 == 0:
            series.append(len(bx))
    # detonation
    at_det = len(bx)
    if at_det:
        df = np.hypot(bx - fx[i_end], by - fy[i_end])
        in_rx = int((df < R + P["rx"]).sum())
        dc = np.hypot(bx - mx[i_end], by - my[i_end])
        self_rx = int((dc < R + P["rx"]).sum())
    else:
        in_rx = self_rx = 0
    assert spawned + forked == consumed + died + at_det, (spawned, forked, consumed, died, at_det)
    if not P["fork"]:
        assert forked == 0 and peak <= spawned
    hits_in_win = int(hit[i0:i_win].sum())
    return dict(spawned=spawned, forked=forked, consumed=consumed, died=died,
                at_det=at_det, in_rx=in_rx, self_rx=self_rx, peak=peak,
                ward=ward, ward_capped=ward_capped, hits=hits_in_win,
                consumed_fast=consumed_fast, series=series)


def run_arm(P, label, seed=7):
    rng = np.random.default_rng(seed)
    casts = []; truncated = 0
    for tr in TR:
        t0 = a.charge
        while True:
            c = run_cast(tr, t0, P, rng)
            if c is None:
                truncated += 1; break
            casts.append(c); t0 += a.charge
    n = len(casts)
    def m(k): return statistics.mean(c[k] for c in casts)
    def med(k): return statistics.median(c[k] for c in casts)
    empty = sum(1 for c in casts if c["hits"] == 0) / n
    r = dict(label=label, P=P, casts=n, truncated=truncated, empty=empty,
             hits=m("hits"), spawned=m("spawned"), forked=m("forked"),
             consumed=m("consumed"), died=m("died"), at_det=m("at_det"),
             peak=m("peak"), peak_med=med("peak"),
             in_rx=m("in_rx"), in_rx_med=med("in_rx"),
             p_any=sum(1 for c in casts if c["in_rx"] > 0) / n,
             self_rx=m("self_rx"), ward=m("ward"), ward_capped=m("ward_capped"),
             fast=(sum(c["consumed_fast"] for c in casts) / max(1, sum(c["consumed"] for c in casts))))
    return r


def row(r):
    return (f"  {r['label']:<30}{r['hits']:>5.1f}{r['spawned']:>7.1f}{r['forked']:>7.1f}"
            f"{r['peak']:>6.1f}{r['consumed']:>7.1f}{r['died']:>7.1f}{r['at_det']:>7.1f}"
            f"{r['in_rx']:>7.2f}{r['p_any']:>7.0%}{r['ward']:>7.1f}{r['ward_capped']:>7.1f}")


HDR = (f"  {'arm':<30}{'hits':>5}{'spawn':>7}{'fork':>7}{'peak':>6}{'eaten':>7}{'walls':>7}"
       f"{'alive':>7}{'in rx':>7}{'any':>7}{'ward':>7}{'w.cap':>7}")

t0 = time.time()
print(f"STORM LAB — {len(TR)} fights, {T['relics']} relics, cast every {a.charge}s, "
      f"tracks at {DT*1000:.1f}ms\n{T['ua'].split(') ')[-1]}\n")
print("columns are MEANS PER CAST. 'in rx' = bolts inside the foe's blast radius at the detonation;"
      "\n'any' = share of casts where at least one is. 'ward' = banked by eaten bolts; 'w.cap' = after the 90 cap.\n")
out = []
def arm(label, **kw):
    P = dict(BASE); P.update(kw)
    r = run_arm(P, label); out.append(r); print(row(r), flush=True); return r

print("BASE and its controls"); print(HDR)
base = arm("BASE  w6 k4 v600 ric4 det8 rx50")
arm("  fork OFF (control)", fork=False)
arm("  no cap", cap=100000)
print(f"\n  empty casts (no blade hit in the window): {base['empty']:.0%}   "
      f"eaten within 0.5s of birth: {base['fast']:.0%}   truncated by fight end: {base['truncated']}")

print("\nWINDOW and DETONATION TIMER (det >= window)"); print(HDR)
for w, d in ((4, 4), (4, 6), (6, 6), (6, 8), (6, 10), (8, 8), (8, 11)):
    arm(f"  window {w}  det {d}", window=w, det=d)

print("\nBOLT SPEED"); print(HDR)
for v in (300, 450, 600, 800):
    arm(f"  speed {v}", speed=v)

print("\nRICOCHETS before a bolt dies"); print(HDR)
for rc in (2, 4, 6, 99):
    arm(f"  ric {rc}", ric=rc)

print("\nBOLTS PER HIT"); print(HDR)
for k in (2, 4, 6, 8):
    arm(f"  per hit {k}", per_hit=k)

print("\nBLAST RADIUS at the detonation"); print(HDR)
for rx in (30, 50, 80, 120):
    arm(f"  rx {rx}", rx=rx)

print("\nSWARM CAP"); print(HDR)
for c in (30, 60, 120):
    arm(f"  cap {c}", cap=c)

print(f"\n{len(out)} arms in {time.time()-t0:.0f}s")
json.dump(out, open(a.out, "w"), indent=1)
