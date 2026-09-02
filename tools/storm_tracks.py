#!/usr/bin/env python3
"""RECORD THE TRACKS a vigil twinblade would cast its swarm over — v64.

The v64 ultimate (Rick's §1, 2026-09-02) deals NO damage while its window runs:
bolts spawn on the blade's hits, bounce, fork on the foe and are eaten by the
caster, and only the detonation at the end deals anything. So everything but
the detonation and the ward can be priced by OVERLAY on real fights — the same
non-invasive method beam_probe (v48) and tornado_lab (v62) used — and the
swarm itself is simulated offline in storm_lab.py against these tracks.

What this records, per fight, every SAMPLE seconds: both fighters' positions,
whether the caster landed a blade hit in that sample, and the caster's shield.

The caster is the cell exactly as cell_ults_on builds it: widowmaker's
twinblade profile, aff vigil, onSelf ward 1, its OWN ultimate suppressed.
The field's ultimates are LIVE (the world the game plays in).

DECLARED, NOT MODELLED: the swarm's ward would change the fight it is overlaid
on (a shield absorbs blows). Second order, and the same limit v48 declared.
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=3)
ap.add_argument("--seed0", type=int, default=4401)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--sample", type=float, default=1/60)
ap.add_argument("--foes", default="all")
ap.add_argument("--out", default="/tmp/storm_tracks.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, sample]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff,
    onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
    charge: w.ult ? w.ult.charge : null };
  w.aff = "vigil"; delete w.onHit; w.onSelf = { ward: 1 };
  if (w.ult) w.ult.charge = 1e9;
  const tracks = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    const mx = [], my = [], fx = [], fy = [], hit = [], sh = [];
    let step = 0, acc = 0, h0 = me.hits;
    while (!m.over && step < secs / DT){
      m.step(DT); step++; acc += DT;
      if (acc >= sample - 1e-9){
        acc = 0;
        mx.push(Math.round(me.x)); my.push(Math.round(me.y));
        fx.push(Math.round(foe.x)); fy.push(Math.round(foe.y));
        hit.push(me.hits - h0); h0 = me.hits;
        sh.push(Math.round(me.shield));
      }
    }
    tracks.push({ foe: f, seed: sd, mx, my, fx, fy, hit, sh, dur: step * DT,
                  win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                  hits: me.hits, dealt: Math.round(me.dealt) });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  if (w.ult) w.ult.charge = saved.charge;
  return { tracks, arena: AC.CONFIG.arena, ballR: AC.CONFIG.physics.ballR,
           dt: DT, twin: { dmg: w.dmg, reach: w.reach, spin: w.spin } };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    ver = page.evaluate("() => navigator.userAgent")
    donor = "widowmaker"
    foes = [i for i in ids if i != donor] if a.foes == "all" else a.foes.split(",")
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    t0 = time.time()
    r = page.evaluate(JS, [donor, foes, seeds, a.secs, a.sample])
    assert not errors, errors[:3]
    r["ua"] = ver; r["relics"] = len(ids); r["sample"] = a.sample
    r["game"] = str(pathlib.Path(a.game).resolve())
    n = len(r["tracks"])
    hits = sum(t["hits"] for t in r["tracks"])
    wins = [t["win"] for t in r["tracks"] if t["win"] >= 0]
    print(f"{len(ids)} relics · {n} fights in {time.time()-t0:.0f}s · {a.sample*1000:.1f}ms samples")
    print(f"caster (vigil twinblade, no ult) win {sum(wins)/len(wins):.1%} · "
          f"{hits/n:.1f} blade hits a fight · mean fight {sum(t['dur'] for t in r['tracks'])/n:.1f}s")
    print(f"runtime: {ver}")
    pathlib.Path(a.out).write_text(json.dumps(r))
    print(f"wrote {a.out}  errors: {errors}")
