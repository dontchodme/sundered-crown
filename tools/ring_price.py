#!/usr/bin/env python3
"""THE RING, THE STAR AND THE SHOWER, PRICED LIVE — v66, the vigil twinblade.

Rick's §1 (2026-09-03) run INSIDE `m.step` against every relic in the build,
storm_price's shape: an overlay that reads the engine's own positions each
frame and pays real damage through the engine's own gates. Nothing is written
to any build.

THE RING is Saturn's: a tilted elliptical band around the caster's ball,
outer semi-axes (A, B), `wd` wide along the major axis, fixed tilt. A foe is
"in the ring" when its disc overlaps the band (centre or any of 12 rim
points). While in it the foe takes `tickDmg` `tickRate` times a second; on
each ENTRY it is left with `burnPer` stacks of a burn (cap `burnCap`,
`burnDps` a stack, `burnDur` s, refreshed on entry) — the "burn that deals
more damage over time for a few seconds".
THE STAR sits on the caster's body. The first body-to-body contact of the
window pops it: `nStars` small stars leave the caster at random angles at
`sSpeed`, radius `sR`, and bounce off the hall's CURRENT inset walls forever.
A SMALL STAR the foe touches detonates: `mineBurn` burn stacks, `mineDmg`
instant, `mineKnock` along the star's travel. THE LEFTOVERS go off when the
window closes, one every `chainGap` s from the top of the hall to the bottom;
a detonation within `blastR` of the foe pays as a touched one does.

DECLARED. Ring ticks and mine damage go through `m.hurt` (the foe's ward
absorbs first, no crit/sunder/jitter, no beat). The burn ticks `hp` directly
like every `dps` status in STATUS (bleed and smite skip the shield). With
`--feed 1` a ring tick also banks `0.55 x dmg` of ward on the caster, which is
what a tick routed through resolveHit would do. Bookkeeping asserted per cast:
spawned = touched + chained + alive.

Arms, paired on (foe, seed):
  A  no ultimate            the body as cell_ults_on prices it
  B  ring only              ticks + burn on entry; the star never pops
  C  shower only            the star pops, mines and chain pay; the ring pays nothing
  D  the whole §1

CONTROL THAT CAN FAIL: arm A must reproduce sash_tracks' win rate on the same
seeds and foes (same seed0, same blade) — it is the identical fight.
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
ap.add_argument("--blade", type=float, default=None)
ap.add_argument("--charge", type=float, default=15.0)
ap.add_argument("--dur", type=float, default=6.0)
# the ring
ap.add_argument("--A", type=float, default=120.0)
ap.add_argument("--B", type=float, default=42.0)
ap.add_argument("--wd", type=float, default=24.0)
ap.add_argument("--tilt", type=float, default=0.45)
ap.add_argument("--tick-rate", type=float, default=10.0)
ap.add_argument("--tick-dmg", type=float, default=1.0)
ap.add_argument("--burn-per", type=int, default=1)
ap.add_argument("--burn-cap", type=int, default=4)
ap.add_argument("--burn-dps", type=float, default=3.0)
ap.add_argument("--burn-dur", type=float, default=3.0)
ap.add_argument("--feed", type=float, default=0.0, help="ward banked per ring tick as a share of tickDmg (0.55 = resolveHit)")
ap.add_argument("--feed-burn", type=float, default=0.0, help="ward banked from BURN damage, as a share (0.55 = the blade's rate)")
ap.add_argument("--tick-stacks", type=int, default=0, help="burn stacks added by every ring tick (dwell feeds the burn)")
# the star and the shower
ap.add_argument("--n-stars", type=int, default=10)
ap.add_argument("--s-speed", type=float, default=380.0)
ap.add_argument("--s-r", type=float, default=12.0)
ap.add_argument("--mine-burn", type=int, default=2)
ap.add_argument("--mine-dmg", type=float, default=0.0)
ap.add_argument("--mine-knock", type=float, default=300.0)
ap.add_argument("--blast-r", type=float, default=80.0)
ap.add_argument("--chain-gap", type=float, default=0.07)
ap.add_argument("--arms", default="A,B,C,D")
ap.add_argument("--control", type=float, default=None, help="arm A must land within 0.5pp of this")
ap.add_argument("--out", default="/tmp/ring_price.json")
a = ap.parse_args()

JS = r"""([donor, foes, seeds, secs, P, arms]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const W = AC.CONFIG.arena.w, H = AC.CONFIG.arena.h;
  const w = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff, dmg: w.dmg,
    onHit: w.onHit ? JSON.parse(JSON.stringify(w.onHit)) : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null,
    charge: w.ult ? w.ult.charge : null };
  w.aff = "vigil"; delete w.onHit; w.onSelf = { ward: 1 };
  if (P.blade) w.dmg = P.blade;
  if (w.ult) w.ult.charge = 1e9;
  function rng(seed){ let s = seed >>> 0; return () => { s += 0x6D2B79F5; let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const ca = Math.cos(P.tilt), sa = Math.sin(P.tilt), kin = (P.A - P.wd) / P.A;
  const inRing = (dx, dy) => {
    const u = dx*ca + dy*sa, v = -dx*sa + dy*ca;
    for (let k = 0; k <= 12; k++){
      const ang = k * Math.PI / 6, rr = k === 12 ? 0 : R;
      const rho = Math.hypot((u + rr*Math.cos(ang)) / P.A, (v + rr*Math.sin(ang)) / P.B);
      if (rho <= 1 && rho >= kin) return true;
    }
    return false;
  };
  const rows = [];
  for (const arm of arms) for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    const foe = (me === m.a) ? m.b : m.a;
    const rnd = rng(sd * 7919 + 31);
    const ringOn = (arm === "B" || arm === "D"), showerOn = (arm === "C" || arm === "D");
    const ultOn = arm !== "A";
    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, popped = false, inb = false, tickAcc = 0;
    let stars = [], chain = [];            // chain: [{star, at}]
    let burn = { st: 0, t: 0 };
    const S = { casts: 0, pops: 0, ticks: 0, entries: 0, burnApplied: 0, spawned: 0, touched: 0, chained: 0,
                chainHit: 0, dmgRing: 0, dmgBurn: 0, dmgMine: 0, ward: 0, ringFrames: 0, burnFrames: 0, lateChain: 0, peak: 0 };
    const pay = (dmg, k) => { if (dmg > 0 && foe.alive && me.alive){ const hp0 = foe.hp + foe.shield; m.hurt(foe, dmg, me); S[k] += hp0 - (foe.hp + foe.shield); } };
    const applyBurn = (n) => { if (!foe.alive) return; burn.st = Math.min(P.burnCap, burn.st + n); burn.t = P.burnDur; S.burnApplied += n; S.peak = Math.max(S.peak || 0, burn.st); };
    const detonate = (s, k) => {
      const dx = foe.x - s.x, dy = foe.y - s.y, d = Math.hypot(dx, dy) || 1;
      if (k === "touched" || d < R + P.blastR){
        applyBurn(P.mineBurn); pay(P.mineDmg, "dmgMine");
        const vl = Math.hypot(s.vx, s.vy) || 1;
        // touched: along the star's travel (a kunai's rule); chained: away from the blast
        const kx = k === "touched" ? s.vx / vl : dx / d, ky = k === "touched" ? s.vy / vl : dy / d;
        if (foe.alive && foe.pin <= 0){ foe.vx += kx * P.mineKnock; foe.vy += ky * P.mineKnock; }
        if (k === "chained") S.chainHit++;
      }
      S[k]++;
    };
    while (!m.over && step < secs / DT){
      m.step(DT); step++; t += DT;
      if (!ultOn) continue;
      // the burn ticks whether or not a window is open
      if (burn.st > 0 && foe.alive){
        burn.t -= DT;
        const d = P.burnDps * burn.st * DT * foe.dmgTakenMul();
        foe.hp -= d; S.dmgBurn += d; S.burnFrames++;
        if (P.feedBurn > 0 && me.alive){ const Wd = AC.STATUS.ward; const b0 = me.shield;
          me.shield = Math.min(Wd.cap, me.shield + d * P.feedBurn); me.shieldMax = Math.max(me.shieldMax, me.shield);
          if (me.shield > b0){ me.apply("ward", 1); S.ward += me.shield - b0; } }
        if (burn.t <= 0) burn.st = 0;
      }
      if (castEnd < 0 && t >= nextCast && chain.length === 0){
        castEnd = t + P.dur; nextCast += P.charge; S.casts++; popped = false; inb = false; tickAcc = 0;
      }
      const open = castEnd >= 0 && t < castEnd;
      const dx = foe.x - me.x, dy = foe.y - me.y, d = Math.hypot(dx, dy);
      if (open){
        // the ring
        const now = foe.alive && inRing(dx, dy);
        if (now){
          S.ringFrames++;
          if (!inb){ S.entries++; if (ringOn) applyBurn(P.burnPer); }
          tickAcc += DT * P.tickRate;
          while (tickAcc >= 1){ tickAcc -= 1; S.ticks++;
            if (ringOn){ pay(P.tickDmg, "dmgRing"); if (P.tickStacks) applyBurn(P.tickStacks);
              if (P.feed > 0 && me.alive){ const Wd = AC.STATUS.ward; const b0 = me.shield;
                me.shield = Math.min(Wd.cap, me.shield + P.tickDmg * P.feed); me.shieldMax = Math.max(me.shieldMax, me.shield);
                me.apply("ward", 1); S.ward += me.shield - b0; } } }
        } else tickAcc = 0;
        inb = now;
        // the star
        if (!popped && d < 2*R + 2 && foe.alive){
          popped = true; S.pops++;
          if (showerOn) for (let i = 0; i < P.nStars; i++){
            const ang = rnd() * Math.PI * 2;
            stars.push({ x: me.x, y: me.y, vx: P.sSpeed*Math.cos(ang), vy: P.sSpeed*Math.sin(ang), born: t });
            S.spawned++; }
        }
      }
      // small stars fly whether the window is open or not, until the chain takes them
      if (stars.length){
        const n = m.inset, lo = n + P.sR, hiX = W - n - P.sR, hiY = H - n - P.sR;
        const keep = [];
        for (const s of stars){
          s.x += s.vx * DT; s.y += s.vy * DT;
          if (s.x < lo){ s.x = 2*lo - s.x; s.vx = -s.vx; } else if (s.x > hiX){ s.x = 2*hiX - s.x; s.vx = -s.vx; }
          if (s.y < lo){ s.y = 2*lo - s.y; s.vy = -s.vy; } else if (s.y > hiY){ s.y = 2*hiY - s.y; s.vy = -s.vy; }
          if (foe.alive && t - s.born > 0.15 && Math.hypot(foe.x - s.x, foe.y - s.y) < R + P.sR){ detonate(s, "touched"); continue; }
          keep.push(s);
        }
        stars = keep;
      }
      if (castEnd >= 0 && t >= castEnd){
        // the window closes: queue the leftovers top to bottom
        stars.sort((p, q) => p.y - q.y);
        chain = stars.map((s, i) => ({ s, at: t + i * P.chainGap }));
        stars = []; castEnd = -1;
      }
      if (chain.length){
        while (chain.length && chain[0].at <= t){ const c = chain.shift(); detonate(c.s, "chained"); }
      }
    }
    S.leftover = stars.length + chain.length;
    rows.push({ arm, foe: f, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1, dur: step * DT, ...S });
  }
  w.aff = saved.aff; w.dmg = saved.dmg; delete w.onHit; delete w.onSelf;
  if (saved.onHit) w.onHit = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  if (w.ult) w.ult.charge = saved.charge;
  return rows;
}"""

P = dict(blade=a.blade, charge=a.charge, dur=a.dur, A=a.A, B=a.B, wd=a.wd, tilt=a.tilt,
         tickRate=a.tick_rate, tickDmg=a.tick_dmg, burnPer=a.burn_per, burnCap=a.burn_cap,
         burnDps=a.burn_dps, burnDur=a.burn_dur, feed=a.feed, feedBurn=a.feed_burn, tickStacks=a.tick_stacks, nStars=a.n_stars, sSpeed=a.s_speed,
         sR=a.s_r, mineBurn=a.mine_burn, mineDmg=a.mine_dmg, mineKnock=a.mine_knock, blastR=a.blast_r,
         chainGap=a.chain_gap)
arms = a.arms.split(",")
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    foes = [i for i in ids if i != "widowmaker"]
    seeds = [a.seed0 + 17 * i for i in range(a.seeds)]
    t0 = time.time()
    rows = page.evaluate(JS, ["widowmaker", foes, seeds, a.secs, P, arms])
    assert not errors, errors[:3]
    print(f"{len(ids)} relics · {len(rows)} fights in {time.time()-t0:.0f}s · blade {a.blade or 'donor 11.95'} · cast every {a.charge}s, window {a.dur}s")
    print(f"ring {a.A}x{a.B} band {a.wd} · {a.tick_rate}/s x {a.tick_dmg} · burn +{a.burn_per} on entry, cap {a.burn_cap}, {a.burn_dps}/s a stack for {a.burn_dur}s · tick feed {a.feed} · burn feeds ward {a.feed_burn} · +{a.tick_stacks} stack a tick")
    print(f"star: {a.n_stars} stars at {a.s_speed}, r {a.s_r} · mine: +{a.mine_burn} burn, {a.mine_dmg} dmg, knock {a.mine_knock} · chain blast {a.blast_r} every {a.chain_gap}s\n")
    hdr = f"  {'arm':<18}{'win':>7}{'casts':>6}{'pops':>6}{'ring s':>7}{'entr':>6}{'burn+':>6}{'mines':>6}{'chain':>6}{'chHit':>6}{'ring':>7}{'burn':>7}{'mine':>7}{'ward':>6}{'total':>7}{'peak':>6}"
    print(hdr)
    out = {}
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm]
        d = [r for r in rs if r["win"] >= 0]
        win = sum(r["win"] for r in d) / len(d)
        casts = sum(r["casts"] for r in rs)
        pc = lambda k: sum(r[k] for r in rs) / max(1, casts)
        name = {"A": "A no ultimate", "B": "B ring only", "C": "C shower only", "D": "D the whole §1"}[arm]
        tot = pc("dmgRing") + pc("dmgBurn") + pc("dmgMine")
        print(f"  {name:<18}{win:>7.1%}{casts/len(rs):>6.2f}{pc('pops'):>6.2f}{pc('ringFrames')/120:>7.2f}{pc('entries'):>6.2f}{pc('burnApplied'):>6.2f}"
              f"{pc('touched'):>6.2f}{pc('chained'):>6.2f}{pc('chainHit'):>6.2f}{pc('dmgRing'):>7.1f}{pc('dmgBurn'):>7.1f}{pc('dmgMine'):>7.1f}{pc('ward'):>6.1f}{tot:>7.1f}{statistics.mean(r['peak'] for r in rs):>6.1f}")
        bad = [r for r in rs if r["spawned"] != r["touched"] + r["chained"] + r["leftover"]]
        assert not bad, f"bookkeeping: {bad[:2]}"
        out[arm] = dict(win=win, n=len(d), casts=casts, **{k: pc(k) for k in
                        ("pops", "ringFrames", "entries", "burnApplied", "touched", "chained", "chainHit", "dmgRing", "dmgBurn", "dmgMine", "ward")})
    if "A" in out:
        for arm in arms:
            if arm != "A": print(f"  {arm} - A = {100*(out[arm]['win']-out['A']['win']):+.1f}pp")
        if a.control is not None:
            ok = abs(out["A"]["win"] - a.control) < 0.005
            print(f"\n  CONTROL: arm A {out['A']['win']:.1%} against {a.control:.1%} — {'PASS' if ok else 'FAIL — the overlay is not inert when it should be'}")
    out["P"] = P; out["errors"] = errors
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
