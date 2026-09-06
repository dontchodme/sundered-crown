#!/usr/bin/env python3
"""THE RING'S EVENT RATE — v66, before anything is designed around it.

Rick's ring is SATURN'S ("a sash that floats off the body and extends
beyond"): a tilted elliptical band around the caster's ball, outer semi-axes
(a, b), `wd` wide along the major axis. "An enemy enters the ring" is the
foe's disc overlapping that band. v43 §4 is the standing rule: measure the
condition's event rate before designing a payoff on it (the hexagon's "stays
inside too long" read 0.0 events a minute). This does that for the vigil
twinblade body against the whole field, OBSERVING ONLY — nothing is injected,
the fight is the fight. (First cut modelled a body-worn bandolier as a capsule;
Rick corrected the picture to Saturn's rings and the band replaced it.)

Per window (cast every `charge` s, open `dur` s):
  contacts     ball-to-ball contact EVENTS (d < 2R+2, debounced 0.15s)
  touchFrames  frames at d < 2R+2                       -> seconds in contact
  nearFrames   frames at d < 2R+`near`                  -> seconds within `near`
  sashFrames   frames the foe's disc (centre or any of 12 rim points) lies in
               the band                                 -> seconds "in the ring"
  entries      transitions into the band                 -> crossings
  auraFrames   frames within (a + R) of the centre       -> a disc of the ring's reach
  firstTouch   seconds from the cast to the first body contact (the star)

Runs on the caster's body as cell_ults_on builds it: widowmaker's twinblade,
aff vigil, onSelf ward 1, its own ultimate suppressed, everyone else's LIVE.
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=3)
ap.add_argument("--seed0", type=int, default=4401)
ap.add_argument("--secs", type=float, default=156.0)
ap.add_argument("--charge", type=float, default=15.0)
ap.add_argument("--dur", type=float, default=6.0)
ap.add_argument("--a", type=float, default=120.0, help="ring OUTER semi-major axis (how far past the body it reaches)")
ap.add_argument("--b", type=float, default=42.0, help="ring OUTER semi-minor axis (the tilt seen edge-on)")
ap.add_argument("--wd", type=float, default=24.0, help="band width along the major axis")
ap.add_argument("--tilt", type=float, default=0.45, help="ring tilt, radians")
ap.add_argument("--near", type=float, default=30.0)
ap.add_argument("--blade", type=float, default=None, help="override the donor blade dmg")
ap.add_argument("--out", default="/tmp/sash_tracks.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, P]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg,
    onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
    charge: w.ult ? w.ult.charge : null };
  w.aff = "vigil"; delete w.onHit; w.onSelf = { ward: 1 };
  if (P.blade) w.dmg = P.blade;
  if (w.ult) w.ult.charge = 1e9;
  const ca = Math.cos(P.tilt), sa = Math.sin(P.tilt);
  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    let t = 0, step = 0, nextCast = P.charge, winEnd = -1, lastTouch = -9;
    let win = null; const wins = [];
    let hitsAll = 0, h0 = me.hits;
    while (!m.over && step < secs / DT){
      m.step(DT); step++; t += DT;
      if (winEnd < 0 && t >= nextCast){
        win = { t0: t, contacts: 0, touch: 0, near: 0, sash: 0, aura: 0, first: -1, hits: 0, foeHits: 0,
                meStun: 0, sep: 0, n: 0, entries: 0, inb: false };
        winEnd = t + P.dur; nextCast += P.charge; h0 = me.hits; win.fh0 = foe.hits;
      }
      if (win){
        const dx = foe.x - me.x, dy = foe.y - me.y, d = Math.hypot(dx, dy);
        win.n++; win.sep += d;
        if (d < 2*R + 2){ win.touch++; if (t - lastTouch > 0.15) { win.contacts++; if (win.first < 0) win.first = t - win.t0; } lastTouch = t; }
        if (d < 2*R + P.near) win.near++;
        // Saturn ring: elliptical annulus, outer (A,B), inner scaled by (A-wd)/A, tilted.
        // The foe DISC overlaps the band if its centre or any of 12 rim points lies in the band.
        const u = dx*ca + dy*sa, v = -dx*sa + dy*ca;
        const kin = (P.a - P.wd) / P.a;
        let inBand = false;
        for (let k = 0; k <= 12 && !inBand; k++){
          const ang = k * Math.PI / 6, rr = k === 12 ? 0 : R;
          const uu = u + rr*Math.cos(ang), vv = v + rr*Math.sin(ang);
          const rho = Math.hypot(uu / P.a, vv / P.b);
          if (rho <= 1 && rho >= kin) inBand = true;
        }
        if (inBand){ win.sash++; if (!win.inb) { win.entries = (win.entries||0) + 1; } }
        win.inb = inBand;
        if (d < P.a + R) win.aura++;
        if (me.stun > 0) win.meStun++;
        if (t >= winEnd){
          win.hits = me.hits - h0; win.foeHits = foe.hits - win.fh0;
          wins.push(win); win = null; winEnd = -1;
        }
      }
    }
    rows.push({ foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1, dur: step * DT, wins });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  if (w.ult) w.ult.charge = saved.charge;
  return { rows, DT };
}"""

P = dict(charge=a.charge, dur=a.dur, a=a.a, b=a.b, wd=a.wd, tilt=a.tilt, near=a.near, blade=a.blade)
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != "widowmaker"]
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    t0 = time.time()
    res = page.evaluate(JS, ["widowmaker", foes, seeds, a.secs, P])
    assert not errors, errors[:3]
    rows, DT = res["rows"], res["DT"]
    d = [r for r in rows if r["win"] >= 0]
    wr = sum(r["win"] for r in d) / len(d)
    wins = [w for r in rows for w in r["wins"]]
    print(f"{len(ids)} relics · {len(rows)} fights in {time.time()-t0:.0f}s · body wins {wr:.1%} (n={len(d)}) · {len(wins)} windows")
    print(f"window {a.dur}s every {a.charge}s · ring outer {a.a}x{a.b}, band {a.wd}, tilt {a.tilt:.2f} · near={a.near} · blade {a.blade or 'donor'}\n")
    def mean(k): return statistics.mean(w[k] for w in wins)
    def med(k): return statistics.median(w[k] for w in wins)
    fr = lambda k: mean(k) * DT
    print(f"  per window ({a.dur}s):")
    print(f"    body contacts        mean {mean('contacts'):.2f}   median {med('contacts'):.0f}   windows with none {sum(1 for w in wins if w['contacts']==0)/len(wins):.0%}")
    print(f"    seconds touching     {fr('touch'):.3f}")
    print(f"    seconds within {a.near:.0f}    {fr('near'):.3f}")
    print(f"    seconds in the ring  {fr('sash'):.3f}   entries {mean('entries'):.2f}   windows with none {sum(1 for w in wins if w['sash']==0)/len(wins):.0%}")
    print(f"    seconds in the aura  {fr('aura'):.3f}   (a disc of the ring's reach, r={a.a+34:.0f})")
    firsts = [w['first'] for w in wins if w['first'] >= 0]
    print(f"    first contact at     median {statistics.median(firsts) if firsts else float('nan'):.2f}s   (in {len(firsts)/len(wins):.0%} of windows)")
    print(f"    my blade hits        {mean('hits'):.2f}   foe hits {mean('foeHits'):.2f}   mean separation {mean('sep')/mean('n'):.0f}   me stunned {fr('meStun'):.2f}s")
    # by foe type
    types = page.evaluate("() => Object.fromEntries(AC.WEAPONS.map(w => [w.id, w.shape]))")
    print(f"\n  {'type':<12}{'contacts':>10}{'touch s':>10}{'ring s':>10}{'entries':>9}{'aura s':>10}{'hits':>8}{'n win':>7}")
    for ty in sorted(set(types.values())):
        ws = [w for r in rows if types[r['foe']] == ty for w in r['wins']]
        if not ws: continue
        print(f"  {ty:<12}{statistics.mean(w['contacts'] for w in ws):>10.2f}{statistics.mean(w['touch'] for w in ws)*DT:>10.3f}"
              f"{statistics.mean(w['sash'] for w in ws)*DT:>10.3f}{statistics.mean(w['entries'] for w in ws):>9.2f}{statistics.mean(w['aura'] for w in ws)*DT:>10.3f}"
              f"{statistics.mean(w['hits'] for w in ws):>8.2f}{len(ws):>7}")
    pathlib.Path(a.out).write_text(json.dumps(dict(P=P, wr=wr, rows=rows), indent=0))
