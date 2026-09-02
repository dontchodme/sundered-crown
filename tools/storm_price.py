#!/usr/bin/env python3
"""THE STORM, PRICED LIVE — v64. The swarm run INSIDE the fight, not over it.

storm_lab.py priced the swarm's shape by overlay and declared that the ward it
banks would change the fight it was overlaid on. This closes that: the same
swarm runs in JS alongside `m.step`, the eaten bolts bank REAL ward on the
caster (through the same shield/clock the engine uses), and the detonation
deals REAL damage through `m.hurt` -- the engine's one gate for direct damage,
so the foe's own ward absorbs it first exactly as it would a blade.

Four arms per fight, paired on (foe, seed), the v59 budget_probe shape:
  A  no ultimate                 the cell as cell_ults_on prices it
  B  ward only                   eaten bolts bank ward; the detonation is OFF
  C  detonation only             bolts bank nothing; the detonation is ON
  D  the whole §1
B - A and C - A say what the relic is MADE OF, on v59's feed axis.

DECLARED: the detonation goes through m.hurt(foe, dmg, me), which bypasses
`resolveHit`'s multipliers (sunder's dmgTakenMul, crits, jitter) and files no
cinema beat. A build routes it properly; this prices the mean. Bolts are the
overlay's bolts: radius rb, straight lines, wall reflection, a spawn grace so a
bolt born on the foe does not fork on the foe it was born on.

CONTROL THAT CAN FAIL: arm A must reproduce storm_tracks' 60.2% on the same
seeds (4401 + 17i) and the same foes -- it is the identical fight with a swarm
that does nothing bolted on. Bookkeeping asserted per cast as in storm_lab.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=3)
ap.add_argument("--seed0", type=int, default=4401)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--charge", type=float, default=15.0)
ap.add_argument("--window", type=float, default=8.0)
ap.add_argument("--per-hit", type=int, default=8)
ap.add_argument("--speed", type=float, default=600.0)
ap.add_argument("--rb", type=float, default=16.0)
ap.add_argument("--ric", type=int, default=99)
ap.add_argument("--fork-net", type=int, default=2)
ap.add_argument("--grace", type=float, default=0.30)
ap.add_argument("--cap", type=int, default=60)
ap.add_argument("--rx", type=float, default=80.0)
ap.add_argument("--bank", type=float, default=2.0)
ap.add_argument("--dmg", type=float, default=15.0)
ap.add_argument("--arms", default="A,B,C,D")
ap.add_argument("--out", default="/tmp/storm_price.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, P, arms]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const W = AC.CONFIG.arena.w, H = AC.CONFIG.arena.h;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff,
    onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
    charge: w.ult ? w.ult.charge : null };
  w.aff = "vigil"; delete w.onHit; w.onSelf = { ward: 1 };
  if (w.ult) w.ult.charge = 1e9;
  function rng(seed){ let s = seed >>> 0; return () => { s += 0x6D2B79F5; let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const rows = [];
  for (const arm of arms) for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    const rnd = rng(sd * 7919 + 17);
    const wardOn = (arm === "B" || arm === "D"), detOn = (arm === "C" || arm === "D");
    const swarmOn = arm !== "A";
    let bolts = [], t = 0, step = 0, nextCast = P.charge, castEnd = -1, winEnd = -1;
    let h0 = me.hits, stats = { casts: 0, spawned: 0, forked: 0, eaten: 0, walls: 0, det: 0, inRx: 0, dmg: 0, ward: 0 };
    const contact = R + P.rb;
    const spawn = (x, y, k) => { for (let i = 0; i < k; i++){ if (bolts.length >= P.cap) break;
      const ang = rnd() * Math.PI * 2;
      bolts.push({ x, y, vx: P.speed * Math.cos(ang), vy: P.speed * Math.sin(ang), ric: P.ric, gr: t + P.grace }); } };
    while (!m.over && step < secs / DT){
      m.step(DT); step++; t += DT;
      if (!swarmOn) continue;
      if (castEnd < 0 && t >= nextCast){ castEnd = t + P.window; winEnd = castEnd; nextCast += P.charge; stats.casts++; }
      const hits = me.hits - h0; h0 = me.hits;
      if (castEnd >= 0){
        if (hits > 0 && t < winEnd){ const before = bolts.length; spawn(foe.x, foe.y, hits * P.perHit); stats.spawned += bolts.length - before; }
        const keep = [];
        for (const b of bolts){
          b.x += b.vx * DT; b.y += b.vy * DT;
          let dead = false;
          if (b.x < P.rb || b.x > W - P.rb){ if (b.ric <= 0) dead = true; else { b.x = b.x < P.rb ? 2*P.rb - b.x : 2*(W-P.rb) - b.x; b.vx = -b.vx; b.ric--; } }
          if (!dead && (b.y < P.rb || b.y > H - P.rb)){ if (b.ric <= 0) dead = true; else { b.y = b.y < P.rb ? 2*P.rb - b.y : 2*(H-P.rb) - b.y; b.vy = -b.vy; b.ric--; } }
          if (dead){ stats.walls++; continue; }
          if (Math.hypot(b.x - me.x, b.y - me.y) < contact){
            stats.eaten++;
            if (wardOn && me.alive){
              const Wd = AC.STATUS ? AC.STATUS.ward : null;
              const cap = Wd ? Wd.cap : 90;
              const before = me.shield;
              me.shield = Math.min(cap, me.shield + P.bank);
              me.shieldMax = Math.max(me.shieldMax, me.shield);
              me.apply("ward", 1);
              stats.ward += me.shield - before;
            }
            continue;
          }
          keep.push(b);
        }
        bolts = keep;
        // forks
        const nb = bolts.length;
        for (let i = 0; i < nb; i++){ const b = bolts[i];
          if (b.gr <= t && Math.hypot(b.x - foe.x, b.y - foe.y) < contact){
            b.ric = P.ric; b.gr = t + P.grace;
            const before = bolts.length; spawn(foe.x, foe.y, P.forkNet); stats.forked += bolts.length - before; } }
        if (t >= castEnd){
          let n = 0;
          for (const b of bolts) if (Math.hypot(b.x - foe.x, b.y - foe.y) < R + P.rx) n++;
          stats.det += bolts.length; stats.inRx += n;
          if (detOn && n > 0 && foe.alive && me.alive){ m.hurt(foe, n * P.dmg, me); stats.dmg += n * P.dmg; }
          bolts = []; castEnd = -1;
        }
      }
    }
    rows.push({ arm, foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1, dur: step * DT, ...stats });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  if (w.ult) w.ult.charge = saved.charge;
  return rows;
}"""

P = dict(charge=a.charge, window=a.window, perHit=a.per_hit, speed=a.speed, rb=a.rb, ric=a.ric,
         forkNet=a.fork_net, grace=a.grace, cap=a.cap, rx=a.rx, bank=a.bank, dmg=a.dmg)
arms = a.arms.split(",")
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    has_status = page.evaluate("() => !!AC.STATUS")
    foes = [i for i in ids if i != "widowmaker"]
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    t0 = time.time()
    rows = page.evaluate(JS, ["widowmaker", foes, seeds, a.secs, P, arms])
    assert not errors, errors[:3]
    print(f"{len(ids)} relics · {len(rows)} fights in {time.time()-t0:.0f}s · AC.STATUS exposed: {has_status}")
    print(f"swarm: window {a.window}s = detonation · {a.per_hit} bolts a hit · speed {a.speed} · r {a.rb} · "
          f"fork +{a.fork_net} · ric {a.ric} · cap {a.cap} · blast r {a.rx} · {a.dmg}/bolt · ward {a.bank}/bolt · cast every {a.charge}s\n")
    print(f"  {'arm':<22}{'win':>7}{'casts':>7}{'spawn':>7}{'fork':>7}{'eaten':>7}{'alive':>7}{'in rx':>7}{'dmg/cast':>10}{'ward/cast':>10}")
    out = {}
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm]
        d = [r for r in rs if r["win"] >= 0]
        win = sum(r["win"] for r in d) / len(d)
        casts = sum(r["casts"] for r in rs)
        def pc(k): return sum(r[k] for r in rs) / max(1, casts)
        name = {"A": "A no ultimate", "B": "B ward only", "C": "C detonation only", "D": "D the whole §1"}[arm]
        print(f"  {name:<22}{win:>7.1%}{casts/len(rs):>7.2f}{pc('spawned'):>7.1f}{pc('forked'):>7.1f}{pc('eaten'):>7.1f}"
              f"{pc('det'):>7.1f}{pc('inRx'):>7.2f}{pc('dmg'):>10.1f}{pc('ward'):>10.1f}")
        out[arm] = dict(win=win, n=len(d), casts=casts, spawned=pc("spawned"), forked=pc("forked"),
                        eaten=pc("eaten"), alive=pc("det"), inRx=pc("inRx"), dmg=pc("dmg"), ward=pc("ward"))
    if "A" in out:
        print(f"\n  CONTROL: arm A {out['A']['win']:.1%} against storm_tracks' 60.2% on the same seeds and foes — "
              f"{'PASS' if abs(out['A']['win'] - 0.602) < 0.005 else 'FAIL — the injection is not inert when it should be'}")
        for arm in arms:
            if arm != "A": print(f"  {arm} - A = {100*(out[arm]['win']-out['A']['win']):+.1f}pp")
    out["P"] = P; out["errors"] = errors
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
