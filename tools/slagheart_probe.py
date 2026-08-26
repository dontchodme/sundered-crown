#!/usr/bin/env python3
"""Falsify Slagheart and Ironbloom.

    python3 slagheart_probe.py --game sc-slagheart.html

Every check below is aimed at a specific way this relic could be lying, and
several of them exist because the design makes a PROMISE that ordinary
checks cannot see:

  [1] THE BITE DEALS NOTHING. The whole design rests on the connect being a
      latch and not a hit — if it also dealt its 41, Ironbloom would be a
      free enormous swing with a firework attached. Asserted as the foe's hp
      across the bite frame.
  [2] THE HOLD IS A FREEZE, AND IT IS EXACTLY AS LONG AS IT SAYS. Both balls,
      both velocities and the whole shot list must be pixel-identical from
      the first frame of the hold to the last, and the frame count must be
      hold/dt within one frame.
  [3] THE SHAKE RAMPS. Rick asked for it; decayImpactOnly takes 90/s off the
      shake, so "I set it once at the latch" would decay to nothing over
      0.8s. Asserted as monotonic-ish growth across the hold.
  [4] THE BLAST PAYS, AND LAUNCHES. Damage lands, the foe leaves over the
      speed ceiling, and exactly `shards` splinters enter the hall.
  [5] A SPLINTER SUNDERS ONCE, NOT TWICE. The head applies +2 and the shards
      it throws apply +1 — that is the `over.onHit` override, and it is the
      one line most likely to silently fall back to the weapon's own onHit.
  [6] SPLINTERS BOUNCE A BOUNDED NUMBER OF TIMES AND THEN POP. No shard may
      outlive its life, exceed shardBounce wall hits, or ever touch its own
      caster.
  [7] THE LIT HEAD BUYS NO PROTECTION. The Crucible zeroes stun while it
      burns because it promises contact. Ironbloom promises nothing, so a
      hex must still lock it — the opposite assertion to the Crucible's, and
      worth making because copying the forge block would have been easy.
  [8] IT IS DETERMINISTIC. Same seed, same fight, twice, field for field —
      the blast spawns nine objects and must do it off shellHash, not rng,
      or every relic in the game drifts when Slagheart is on the field.
  [9] NO NaN, EVERY MATCH RESOLVES, over a sweep.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from scpage import game

HERE = pathlib.Path(__file__).parent

MECH_JS = r"""() => {
  const dt = AC.CONFIG.physics.dt, out = {};
  const mk = (a, b, seed) => { const m = new AC.Match(a, b, seed);
                               AC.__inject(m); AC.SFX.play = function(){}; return m; };
  const U = AC.WEAPONS.find(w => w.id === "slagheart").ult;
  out.ult = { window: U.window, hold: U.hold, shards: U.shards,
              bounce: U.shardBounce, sunder: U.shardSunder };

  /* ---- [1][2][3][4] one instrumented latch ----------------------------- */
  {
    const m = mk("slagheart", "emberedge", 4242);
    for (let i = 0; i < 120 * 3; i++) m.step(dt);
    m.a.ultHeat = { t: 0, window: 999 };
    let g = 0, hpBefore = null, hpAtBite = null;
    while (!m.latch && g++ < 120 * 60){ hpBefore = m.b.hp; m.step(dt); }
    out.latched = !!m.latch;
    hpAtBite = m.b.hp;
    out.biteDealtDamage = +(hpBefore - hpAtBite).toFixed(4);
    /* the hold: count frames, watch for any motion, watch the shake */
    const snap = () => JSON.stringify([m.a.x, m.a.y, m.a.vx, m.a.vy,
                                       m.b.x, m.b.y, m.b.vx, m.b.vy,
                                       m.b.hp, m.shots.length]);
    const s0 = snap();
    /* the away-axis, fixed at the bite: the blast shoves along it */
    const ax = m.b.x - m.a.x, ay = m.b.y - m.a.y, al = Math.hypot(ax, ay) || 1;
    const ux = ax / al, uy = ay / al;
    const vBeforeProj = m.b.vx * ux + m.b.vy * uy;
    let frames = 0, moved = false, shakes = [];
    while (m.latch && frames < 400){
      m.step(dt); frames++;
      if (m.latch){ if (snap() !== s0) moved = true; shakes.push(m.shake); }
    }
    const vAfterProj = m.b.vx * ux + m.b.vy * uy;
    out.holdFrames = frames;
    out.holdExpect = Math.round(U.hold / dt);
    out.frozeSolid = !moved;
    out.shakeStart = +shakes[0].toFixed(1);
    out.shakeEnd = +shakes[shakes.length - 1].toFixed(1);
    out.shakeRose = shakes[shakes.length - 1] > shakes[0] * 2.5;
    out.shakeDips = shakes.filter((v, i) => i && v < shakes[i-1] - 0.001).length;
    /* the blast happened on the frame the hold ended */
    out.blastDmg = +(hpAtBite - m.b.hp).toFixed(1);
    /* The IMPULSE, not the resulting speed. The first version of this check
       asserted |v| > speedMax and passed or failed on which way the foe
       happened to be travelling when the head bit — on one seed it was flying
       INTO the flail at ~950 and 1800 of launch left it at 856, which is
       correct physics and a failed assertion. What the code promises is the
       shove and the raised ceiling, so that is what is measured. */
    out.launchDV = Math.round(vAfterProj - vBeforeProj);
    out.launchWant = U.launch;
    out.ceilingRaised = m.b.launch > 1.5;
    out.speedMax = AC.CONFIG.physics.speedMax;
    out.shardsSpawned = m.shots.filter(s => s.shard).length;
    /* ---- [5] a splinter sunders ONCE -------------------------------- */
    delete m.b.status.sunder;
    let sunderFromShard = 0, guard = 0;
    /* The caster is stunned for the whole observation window. Without it the
       flail keeps swinging and lands its OWN +2 during the six seconds the
       shards are in the air, and the probe cannot tell the two apart — which
       is how the first version of this check reported "+2 per shard" against
       code that was applying +1 correctly. */
    while (m.shots.length && guard++ < 120 * 6){
      const n0 = m.b.stacks("sunder");
      m.a.stun = 9;
      m.step(dt);
      const d = m.b.stacks("sunder") - n0;
      if (d > 0) sunderFromShard = Math.max(sunderFromShard, d);
    }
    out.sunderPerShard = sunderFromShard;
  }

  /* ---- [6] bounces bounded, nothing outlives its life, no friendly fire */
  {
    const m = mk("slagheart", "aureole", 909);
    for (let i = 0; i < 120 * 3; i++) m.step(dt);
    m.a.ultHeat = { t: 0, window: 999 };
    let g = 0;
    while (!m.shots.some(s => s.shard) && g++ < 120 * 90) m.step(dt);
    let minBounce = 99, aHpStart = m.a.hp, maxLife = 0, guard = 0;
    /* The first version of this check watched m.a.hp while the OPPONENT was
       still swinging, so it failed on damage that had nothing to do with
       shards. Lock the foe out and clear the caster's statuses each frame:
       now the only thing on the field that can hurt the caster is its own
       shrapnel, which is exactly the claim. */
    while (m.shots.length && guard++ < 120 * 8){
      m.b.stun = 9; m.a.status = {};
      m.step(dt);
      for (const s of m.shots) if (s.shard){
        minBounce = Math.min(minBounce, s.bounce);
        maxLife = Math.max(maxLife, s.max - s.life);
      }
    }
    out.shardsCleared = m.shots.length === 0;
    out.minBounceLeft = minBounce === 99 ? null : minBounce;
    out.maxShardAge = +maxLife.toFixed(2);
    out.casterHarmedByOwnShards = m.a.hp < aHpStart;
  }

  /* ---- [7] the lit head buys no protection ---------------------------- */
  {
    const m = mk("slagheart", "spellbreaker", 77);
    for (let i = 0; i < 120 * 3; i++) m.step(dt);
    m.a.ultHeat = { t: 0, window: 999 };
    m.a.stun = 0.5;
    m.step(dt);
    out.stunSurvivesLitHead = m.a.stun > 0.4;
  }

  /* ---- [11] the set-piece outlives what it is explaining --------------- */
  {
    /* ultFx.t runs at ~2x sim time on the normal path (decay() ticks
       presentation twice a frame) and 1x while frozen. Ironbloom shipped its
       first build with life = window + 0.4, so the lit head's glow died 3.3s
       into a 6.0s window and the tell for the state was gone for half of it.
       Measured as screen-life in SIM seconds against the thing it explains. */
    const m = mk("slagheart", "thornwake", 5);
    for (let i = 0; i < 120 * 2; i++) m.step(dt);
    const rate0 = m.t, f0 = (m.ultFx = { w:"probe", kind:"probe", src:"a",
      tgt:"b", x:0, y:0, tx:0, ty:0, hit:true, radius:1, aff:m.a.aff,
      t:0, life:9999 }).t;
    for (let i = 0; i < 240; i++) m.step(dt);
    out.fxRate = +((m.ultFx.t - f0) / (m.t - rate0)).toFixed(2);
    m.ultFx = null;
    const m2 = mk("slagheart", "thornwake", 5);
    for (let i = 0; i < 120 * 2; i++) m2.step(dt);
    m2.a.charge = U.charge;                     // fire it on the next tick
    let g2 = 0;
    while (!m2.a.ultHeat && g2++ < 120 * 5) m2.step(dt);
    out.litLifeScreen = +(m2.ultFx.life / out.fxRate).toFixed(2);
    out.litWindow = U.window;
  }

  /* ---- [8] determinism ------------------------------------------------- */
  {
    const run = () => JSON.stringify(AC.simulate("slagheart", "thornwake", 31337));
    out.deterministic = run() === run();
  }

  /* ---- [9] the sweep --------------------------------------------------- */
  {
    let nan = 0, unresolved = 0, n = 0, latches = 0, casts = 0, blasts = 0;
    let hitS = 0, secS = 0;
    for (const fo of AC.WEAPONS.map(w => w.id)){
      if (fo === "slagheart") continue;
      for (let s = 0; s < 4; s++){
        const m = mk("slagheart", fo, 700 + s * 97);
        let wasH = false, wasL = false;
        const ob = m.blast.bind(m); m.blast = (L) => { blasts++; ob(L); };
        for (let i = 0; i < 120 * 100 && !m.over; i++){
          m.step(dt);
          if (!wasH && m.a.ultHeat) casts++;
          if (!wasL && m.latch) latches++;
          wasH = !!m.a.ultHeat; wasL = !!m.latch;
        }
        n++;
        hitS += m.a.hits; secS += m.t;
        if (!m.over) unresolved++;
        if (![m.a.x, m.a.y, m.b.x, m.b.y, m.a.hp, m.b.hp].every(isFinite)) nan++;
      }
    }
    /* THE BITE RATE, PREDICTED. "39% of casts cool unfired" means nothing on
       its own, and comparing it to the Crucible's 85% is comparing it to an
       ultimate that PULLS — the Crucible manufactures the contact Ironbloom
       has to wait for, which is the designed difference between them.

       The honest check is a model. Ironbloom bites on the first melee connect
       inside `window`, connects arrive at a measured rate, so the rate is a
       Poisson trial: 1 - exp(-window / meanGap). If the observation ever
       drifts off the prediction, something is EATING CASTS — a suppressed
       hit, a window that clears early, a bite that does not register — and
       that is a bug rather than a balance question. The Crucible is still
       measured, as context rather than as a bar. */
    let cCasts = 0, cStrikes = 0;
    for (const fo of AC.WEAPONS.map(w => w.id)){
      if (fo === "grudgebearer") continue;
      for (let s = 0; s < 4; s++){
        const m = mk("grudgebearer", fo, 700 + s * 97);
        let wasF = false;
        for (let i = 0; i < 120 * 100 && !m.over; i++){
          const had = !!m.a.ultForge;
          m.step(dt);
          if (!wasF && m.a.ultForge) cCasts++;
          /* the forge cleared with a strike (not the cap) => it connected */
          if (had && !m.a.ultForge && m.a.ultsFired
              && m.ultFx && m.ultFx.phase === "strike") cStrikes++;
          wasF = !!m.a.ultForge;
        }
      }
    }
    const gap = secS / Math.max(1, hitS);
    const W = AC.WEAPONS.find(w => w.id === "slagheart").ult.window;
    out.sweep = { n, nan, unresolved, casts, latches, blasts,
                  latchRate: +(latches / Math.max(1, casts)).toFixed(3),
                  meanGap: +gap.toFixed(2),
                  predicted: +(1 - Math.exp(-W / gap)).toFixed(3),
                  crucibleCasts: cCasts, crucibleStrikes: cStrikes,
                  crucibleRate: +(cStrikes / Math.max(1, cCasts)).toFixed(2) };
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="sc-slagheart.html")
    a = ap.parse_args()
    fails = 0

    def check(ok, name, detail=""):
        nonlocal fails
        if not ok:
            fails += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))

    with game(game_path=(HERE / a.game).resolve()) as (pg, errs):
        r = pg.evaluate(MECH_JS)
        assert not errs, errs

    U = r["ult"]
    check(r["latched"], "[0] the head bites at all")
    check(abs(r["biteDealtDamage"]) < 0.001,
          "[1] the bite deals no damage of its own",
          f"hp moved {r['biteDealtDamage']} on the bite frame")
    check(abs(r["holdFrames"] - r["holdExpect"]) <= 1,
          "[2] the hold is exactly as long as it says",
          f"{r['holdFrames']} frames vs {r['holdExpect']} ({U['hold']}s at 1/120)")
    check(r["frozeSolid"], "[2] the world is frozen solid through the hold",
          "positions, velocities, hp and the shot list all unchanged")
    check(r["shakeRose"] and r["shakeDips"] == 0,
          "[3] the shake RAMPS across the hold rather than decaying",
          f"{r['shakeStart']} -> {r['shakeEnd']}, {r['shakeDips']} frames of decay")
    check(r["blastDmg"] > 0, "[4] the blast pays", f"{r['blastDmg']} damage")
    check(r["launchDV"] >= r["launchWant"] * 0.95 and r["ceilingRaised"],
          "[4] the blast shoves with its stated launch, over a raised ceiling",
          f"+{r['launchDV']} along the away-axis (states {r['launchWant']}), "
          f"vmax clamp lifted past {r['speedMax']}")
    check(r["shardsSpawned"] == U["shards"],
          "[4] every splinter enters the hall",
          f"{r['shardsSpawned']} of {U['shards']}")
    check(r["sunderPerShard"] == U["sunder"],
          "[5] a splinter sunders ONCE where the head sunders twice",
          f"+{r['sunderPerShard']} per shard (weapon onHit is +2)")
    check(r["shardsCleared"] and r["minBounceLeft"] is not None
          and r["minBounceLeft"] >= 0 and r["maxShardAge"] <= 2.62,
          "[6] splinters bounce a bounded number of times and then pop",
          f"cleared={r['shardsCleared']}, bounces left min {r['minBounceLeft']}, "
          f"oldest {r['maxShardAge']}s of {2.6}")
    check(not r["casterHarmedByOwnShards"],
          "[6] no splinter ever touches its own caster")
    check(r["stunSurvivesLitHead"],
          "[7] the lit head buys no stun immunity — unlike the Crucible",
          "a hex still locks a flail that has promised nothing")
    check(r["litLifeScreen"] >= r["litWindow"],
          "[11] the lit head's glow outlives the window it is explaining",
          f"set-piece life {r['litLifeScreen']}s of screen time at the "
          f"measured {r['fxRate']}x fx clock, window {r['litWindow']}s")
    check(r["deterministic"],
          "[8] deterministic — the blast spawns off shellHash, not rng")
    s = r["sweep"]
    check(s["nan"] == 0 and s["unresolved"] == 0,
          "[9] no NaN, every match resolves",
          f"{s['n']} matches, {s['nan']} NaN, {s['unresolved']} unresolved")
    check(s["blasts"] == s["latches"],
          "[9] every bite reaches its blast",
          f"{s['latches']} bites, {s['blasts']} blasts")
    check(abs(s["latchRate"] - s["predicted"]) < 0.12,
          "[10] the bite rate IS the Poisson prediction — nothing eats casts",
          f"observed {s['latchRate']:.0%} ({s['latches']}/{s['casts']}) vs "
          f"1-exp(-{s['meanGap']:.1f}s gap over a 6.0s window) = "
          f"{s['predicted']:.0%}")
    print(f"\n  For context, not as a bar: the Crucible strikes on "
          f"{s['crucibleRate']:.0%} of its casts "
          f"({s['crucibleStrikes']}/{s['crucibleCasts']}). It PULLS the foe onto\n"
          f"  the hammer; Ironbloom is not given a mechanism for contact, and "
          f"that is the design.")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
