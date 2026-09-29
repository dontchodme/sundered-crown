#!/usr/bin/env python3
"""ONE HARNESS FOR PRICING AN ULTIMATE THAT DOES NOT EXIST YET — v69 onward.

vine_price (v68), ring_price (v66) and storm_price (v64) were the same tool
three times: a §1 run INSIDE `m.step` against every relic in the build with
THEIR ultimates live, paired on (foe, seed), paying through the engine's own
gates, nothing written to any build. This is that tool with the mechanic
lifted out into a small JS module so the next fourteen designs do not each
rewrite the harness — and so the harness's control is the same control every
time.

    python ult_overlay.py --game ../02-chain/sc-trunk.html \
        --relic gravemourn --cell verdant:flail --mech overlays/vine.js \
        --arms A,B,C,D --P blade=19 turn=4 --seeds 20 --control 0.015

THE CELL. `--cell aff:type` grafts the school's channel onto the donor
exactly as cell_ults_on does (aff, onHit/onSelf) and suppresses the donor's
own ultimate in every arm. Without `--cell` the relic is taken as shipped
(a REDESIGN): its own ultimate is suppressed in every arm except `SHIP`,
which leaves it live — so `SHIP` is the thing a redesign has to beat and
`A` is the body with nothing.

THE MECHANIC is a JS file evaluating to a factory:

    ({P, AC, m, me, foe, arm, S, rnd, H}) => ({
      onCast(t){},                 // a window opened (the harness schedules casts)
      onFrame(t, dt, open){},      // every step, after m.step; `open` while a window runs
      onClose(t, reason){},        // "clock" | "death" | "over"
      wait(t){ return false; },    // true = the next cast waits (a wither, a chain)
    })

`P` is the parameter bag (`--P k=v ...`, numbers parsed), `arm` the arm
letter (the mechanic reads its features off it), `S` a free stats object
(numbers summed per fight; keys starting `f_` are reported per FIGHT, all
others per CAST), `rnd` a seeded mulberry32 for the mechanic's own draws
(never `m.rng` — that would move the fight), and `H` the helpers:
  H.segDist(px,py,ax,ay,bx,by)  H.hurt(f, dmg, src) -> dealt  H.pin(f, hold)
  H.knock(f, kx, ky, power)     H.angTo(a, b)          H.R, H.DT, H.W, H.Hh

CONTROL THAT CAN FAIL: arm A on the same seeds must reproduce `cell_ults_on`'s
ults-on body for the cell (or `verify`'s no-ult read for a redesign) — pass
`--control` and the run exits 2 if it does not.

`hits in/out` is the head/blade blows landed inside and outside windows, per
fight; `casts` per fight; everything else per cast unless prefixed `f_`.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, 'C:/dev/sundered-crown/tools')
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--relic", required=True, help="donor id (an open cell) or the relic itself (a redesign)")
ap.add_argument("--cell", default=None, help="aff:type for an open cell; omit for a redesign")
ap.add_argument("--mech", required=True, help="path to the mechanic's JS module")
ap.add_argument("--arms", default="A,D")
ap.add_argument("--P", nargs="*", default=[], help="k=v mechanic parameters")
ap.add_argument("--seeds", type=int, default=10)
ap.add_argument("--seed0", type=int, default=2207)
ap.add_argument("--secs", type=float, default=160.0)
ap.add_argument("--foes", default=None)
ap.add_argument("--control", type=float, default=None, help="arm A must land within 0.05pp of this")
ap.add_argument("--label", default="")
ap.add_argument("--out", default="/tmp/ult_overlay.json")
a = ap.parse_args()

CHAN = {"bloodsworn": ("onHit", "hemorrhage", 2), "dwarven": ("onHit", "sunder", 1),
        "runic": ("onHit", "hex", 1), "sanctified": ("onHit", "smite", 1),
        "umbral": ("onHit", "curse", 1), "verdant": ("onHit", "entangle", 2),
        "vigil": ("onSelf", "ward", 1)}

def parse(v):
    try: return json.loads(v)
    except Exception: return v
P = {"charge": 16.0, "dur": 8.0, "blade": None}
for kv in a.P:
    k, v = kv.split("=", 1); P[k] = parse(v)

MECH = pathlib.Path(a.mech).read_text()

JS = r"""([donor, cell, foes, seeds, secs, P, arms, mechSrc]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const W = AC.CONFIG.arena.w, Hh = AC.CONFIG.arena.h;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg, spin: w.spin, reach: w.reach, mass: w.mass,
    onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
    charge: w.ult ? w.ult.charge : null };
  if (cell){
    const [aff, typ] = cell; const [slot, key, per] = P.__chan;
    w.aff = aff; delete w.onHit; delete w.onSelf; const o = {}; o[key] = per; w[slot] = o;
  }
  if (P.blade) w.dmg = P.blade;
  const factory = eval(mechSrc);
  const mk = (seed) => { let s = seed >>> 0; return () => { s += 0x6D2B79F5; let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  const H = { R, DT, W, Hh,
    segDist(px, py, ax, ay, bx, by){ const dx = bx-ax, dy = by-ay, l2 = dx*dx+dy*dy;
      let t = l2 > 0 ? ((px-ax)*dx + (py-ay)*dy)/l2 : 0; t = Math.max(0, Math.min(1, t));
      return Math.hypot(px-(ax+t*dx), py-(ay+t*dy)); },
    angTo(a, b){ let d = b - a; return Math.atan2(Math.sin(d), Math.cos(d)); },
    pin(f, hold){ if (!f.alive || hold <= 0) return; if (!(f.pin > hold)) f.pinV = [f.vx, f.vy];
      f.pin = Math.max(f.pin, hold); f.pinMax = Math.max(f.pinMax, hold); },
    knock(f, kx, ky, power){ if (!f.alive || f.pin > 0) return; const l = Math.hypot(kx, ky) || 1;
      f.vx += kx/l*power; f.vy += ky/l*power; },
  };
  const rows = [];
  for (const arm of arms) for (const fid of foes) for (const sd of seeds){
    const m = new AC.Match(donor, fid, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    H.hurt = (f, dmg, src) => { if (!(dmg > 0) || !f.alive) return 0; const hp0 = f.hp + f.shield; m.hurt(f, dmg, src); return hp0 - (f.hp + f.shield); };
    // the donor's own ultimate: off in every arm but SHIP
    if (w.ult) w.ult.charge = (arm === "SHIP") ? saved.charge : 1e9;
    const overlayOn = arm !== "A" && arm !== "SHIP";
    const S = {};
    const mech = overlayOn ? factory({ P, AC, m, me, foe, arm, S, rnd: mk(sd * 7919 + 31), H }) : null;
    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, casts = 0, hitsIn = 0, hitsOut = 0;
    let cSteps = 0, cFrozen = 0, cWin = 0, cWinFrozen = 0;
    while (!m.over && step < secs / DT){
      const h0 = me.hits;
      { const fz = m.hitStop > 0 || !!m.latch || !!m.splitHold, ow = castEnd >= 0 && t < castEnd;
        cSteps++; if (fz) cFrozen++; if (ow){ cWin++; if (fz) cWinFrozen++; } }
      m.step(DT); step++; t += DT;
      const open = castEnd >= 0 && t < castEnd;
      if (me.hits > h0){ if (open) hitsIn += me.hits - h0; else hitsOut += me.hits - h0; }
      if (!mech) continue;
      if (castEnd >= 0 && (t >= castEnd || !me.alive || !foe.alive || m.over)){
        const reason = m.over ? "over" : (!me.alive || !foe.alive) ? "death" : "clock";
        castEnd = -1; if (mech.onClose) mech.onClose(t, reason);
      }
      if (castEnd < 0 && t >= nextCast && me.alive && foe.alive && !(mech.wait && mech.wait(t))){
        castEnd = t + P.dur; nextCast += P.charge; casts++; if (mech.onCast) mech.onCast(t);
      }
      if (mech.onFrame) mech.onFrame(t, DT, castEnd >= 0 && t < castEnd);
    }
    if (mech && castEnd >= 0 && mech.onClose) mech.onClose(t, "over");
    if (mech && mech.end) mech.end();
    rows.push({ arm, foe: fid, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                dur: step * DT, casts, hitsIn, hitsOut, S, cen: [cSteps, cFrozen, cWin, cWinFrozen] });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; w.spin = saved.spin; w.reach = saved.reach; w.mass = saved.mass;
  delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit; if (saved.onSelf) w.onSelf = saved.onSelf;
  if (w.ult) w.ult.charge = saved.charge;
  return rows;
}"""

def wr(rs):
    d = [r for r in rs if r["win"] >= 0]
    return sum(r["win"] for r in d) / len(d) if d else float("nan")

arms = a.arms.split(",")
seeds = [a.seed0 + 11 * i for i in range(a.seeds)]
cell = a.cell.split(":") if a.cell else None
if cell: P["__chan"] = list(CHAN[cell[0]])
t0 = time.time()
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = a.foes.split(",") if a.foes else [i for i in ids if i != a.relic]
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    print(f"{len(ids)} relics · Chromium {ver} · {a.relic}{' as ' + a.cell if a.cell else ' (redesign)'} · "
          f"{len(foes)} foes x {len(seeds)} seeds = {len(foes)*len(seeds)} fights an arm · {a.label}")
    print("  " + " ".join(f"{k}={v}" for k, v in P.items() if not k.startswith("__")))
    rows = page.evaluate(JS, [a.relic, cell, foes, seeds, a.secs, P, arms, MECH])
    assert not errors, errors

keys = sorted({k for r in rows for k in r["S"]})
out = {"P": {k: v for k, v in P.items() if not k.startswith("__")}, "arms": {}}
base = None
hdr = f"  {'arm':<6}{'win':>7}{'casts':>7}{'hits in/out':>13}" + "".join(f"{k:>9}" for k in keys)
print("\n" + hdr)
for arm in arms:
    rs = [r for r in rows if r["arm"] == arm]
    Wn = wr(rs); n = len(rs)
    casts = sum(r["casts"] for r in rs)
    if arm == "A": base = Wn
    cols = []
    stats = {}
    for k in keys:
        tot = sum(r["S"].get(k, 0) for r in rs)
        v = tot / n if k.startswith("f_") else (tot / casts if casts else 0.0)
        stats[k] = v; cols.append(f"{v:>9.2f}")
    byFoe = {}
    for r in rs:
        if r["win"] >= 0: byFoe.setdefault(r["foe"], []).append(r["win"])
    print(f"  {arm:<6}{Wn:>7.1%}{casts/n:>7.2f}{sum(r['hitsIn'] for r in rs)/n:>6.2f}/{sum(r['hitsOut'] for r in rs)/n:<6.2f}" + "".join(cols))
    out["arms"][arm] = dict(win=Wn, n=n, casts=casts / n, hitsIn=sum(r["hitsIn"] for r in rs) / n,
                            hitsOut=sum(r["hitsOut"] for r in rs) / n, stats=stats,
                            byFoe={k: sum(v) / len(v) for k, v in byFoe.items()})
    _c = [sum(r['cen'][i] for r in rs) for i in range(4)]
    out['arms'][arm]['census'] = dict(steps=_c[0], frozen=_c[1], win=_c[2], winFrozen=_c[3])
    _fs = _c[1] / max(1, _c[0]); _fw = _c[3] / max(1, _c[2]); _fo = (_c[1] - _c[3]) / max(1, _c[0] - _c[2])
    print(f"      census {arm}: frozen {_fs:.4f} of lab steps ({_c[1]} of {_c[0]}), {_fw:.4f} inside windows, {_fo:.4f} outside; "
          f"lab {P['charge']:g} -> engine {P['charge']*(1-_fs):.2f}; window {P['dur']:g} lab-s = {P['dur']*(1-_fw):.2f} engine window-s")
if base is not None:
    print("  lifts over A: " + "  ".join(f"{arm} {100*(out['arms'][arm]['win']-base):+.1f}" for arm in arms if arm != "A"))
if a.control is not None and base is not None:
    ok = abs(base - a.control) < 0.0005
    print(f"  CONTROL arm A {base:.2%} against {a.control:.2%}: {'PASS' if ok else 'FAIL'}")
    if not ok: sys.exit(2)
print(f"  {len(rows)} fights in {time.time()-t0:.0f}s   errors: {errors}")
pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
