#!/usr/bin/env python3
"""BREACH, ASSERTED AGAINST THE BUILD — one check per sentence. Brief §5b.

    python breach_relic_probe.py --game ../02-chain/sc-breach.html

  [1]  THE LICENCE ENDS ON THE FIFTH TEAR, counted off events rather than
       recomputed, and never on the sixth
  [2]  THE CAP ENDS FEWER THAN 1 WINDOW IN 50. If it ends more, `n` is not
       reachable and the DESIGN changes rather than the number
  [3]  HOLES OUTLIVE THE LICENCE — a hole is still firing after `f.ultBreach`
       is null
  [4]  A JET RESOLVES ONCE PER FIRING, and on the frame the FRONT reaches the
       quarry rather than the frame it opens
  [5]  A QUARRY THAT LEAVES IN TIME IS MISSED — constructed, both ways
  [6]  FOE ONLY, and no shade is ever caught (design §4.8, and this build
       takes the OTHER answer from the placeholder — see `jetHit`)
  [7]  EVERY JET HIT APPLIES EXACTLY ONE SUNDER, and the stack count moves
  [8]  NOTHING FIRES AFTER `m.over` OR ON A CORPSE, and nothing ticks while
       `m.hitStop > 0`
  [9]  PER-MATCH STATE — six other-relic matches run AFTER a Cindercleave one
       are bit-identical to the same six run before it
  [10] THE CAST FILES A BEAT AND EACH TEAR FILES ITS OWN; THE FIRINGS DO NOT
       — and a jet that KILLS files a FATAL one
  [11] THE TELEMETRY. Holes a cast, jets fired, jet hits landed, and the mean
       Sunder on the quarry — because Breach is TWO scalars and one number
       will not tune it
  [12] EVERY VOICE RENDERS TO SOMETHING AUDIBLE in an OfflineAudioContext
  [P]  THE RENDER PATH IS CALLED against a real 2D context

## [P] IS NOT OPTIONAL AND v48 IS WHY

Two picture faults shipped through every headless check in the repo and died
on the first rendered frame: `_drawBeam` reached for a MATCH method from the
RENDERER, and `drawUltUnder` handed NaN to `createRadialGradient`. Both were
green across 27 probe checks, a 280-match `engine_ab`, `chain_audit` and
`post_identity` — and the probe's own check passed on the first one because it
was REGEXING the source for a call, and a string does not resolve a reference.
So this one CALLS `drawVents` on both passes against a live context.

## [6] IS A DECISION AND NOT A DEFAULT

Design §4.8 offered "a jet catches shades like any other body" as its
placeholder. This build takes the other answer, because the roster precedent
is quarry-only (the Deadfall's mines have never been set off by a copy) and
because `spent` is one payment per firing, so sweeping three bodies is either
a shield or a damage multiplier and nobody priced either. The check asserts
whatever the code does, so the day that changes the check moves with it.

## AND THE CHECKS RECONSTRUCT THE ENGINE'S RULE RATHER THAN ASSUMING THEIR OWN

`gravemourn_relic_probe` reported three defects that were not there, all
because the probe had written down its own model of a rule and the engine
legitimately did something else. So `n`, `cap`, `period`, `warm`, `speed`,
`half`, `taperTo` and `jetDmg` are read off `w.ult` here and never typed in,
and [1] counts tears off the engine's own `tearVent` rather than off a
recomputation of when it should have fired.

Runtime only. NOTHING is written to any build.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "cindercleave"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}"
          + (f"\n        {detail}" if detail else ""))


# ------------------------------------------------------------- the main run --
# ONE instrumented match per (foe, seed). Every hook forwards with `arguments`
# -- v44's warning, and it is that a wrapper with a FIXED ARITY silently
# measures the OLD build the moment the build grows a parameter.
RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const M = AC.Match.prototype;
  const A = {
    fights: 0, casts: 0, tears: 0, overN: 0, overWithVents: 0,
    fired: 0, hits: 0, hitOnOpenFrame: 0, hitOutsideSweep: 0,
    doublePay: 0,
    afterLicence: 0, afterLicenceFires: 0,
    corpseFire: 0, overFire: 0, frozenTick: 0, frozenChecks: 0,
    sunderBad: 0, sunderMoves: 0, stackSum: 0, stackN: 0,
    shadeHits: 0, shadeFrames: 0, shadeInPath: 0, selfHit: 0,
    castBeats: 0, tearBeats: 0, jetUltBeats: 0, jetFatalBeats: 0,
    jetKills: 0, maxLive: 0, dmgSum: 0,
  };
  const origTear = M.tearVent, origJet = M.jetHit, origBeat = M.beat;
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      A.fights++;
      const me = m.a;                       // the relic is always side A here
      let step = 0, inTear = false, inJet = false;

      m.tearVent = function (f, P) {
        const before = f.ultBreach ? f.ultBreach.tears : -1;
        inTear = true;
        try { origTear.call(m, f, P); } finally { inTear = false; }
        const after = f.ultBreach ? f.ultBreach.tears : -1;
        if (after > before) A.tears++;
      };
      m.jetHit = function (v, own, foe) {
        A.hits++;
        /* [4] THE FRONT HAS TO HAVE MOVED. A firing sets `front = 0` and
           `continue`s, so a hit on the opening frame would mean the whole line
           resolved at once -- which is the +4.2pp version Rick already
           rejected on a different relic. */
        if (!(v.front > 0)) A.hitOnOpenFrame++;
        /* and the quarry has to be inside the interval the front just swept */
        const px = foe.x - v.x, py = foe.y - v.y;
        const proj = px * v.ax + py * v.ay;
        if (proj > v.front + 1e-6) A.hitOutsideSweep++;
        if (v.__paid === v.fired) A.doublePay++;
        v.__paid = v.fired;
        /* [6] the caster is never the target, and neither is a copy */
        if (own === foe) A.selfHit++;
        if (foe !== m.a && foe !== m.b) A.shadeHits++;
        /* [7] EXACTLY ONE SUNDER, measured either side of the call */
        const b4 = foe.stacks("sunder"), hp4 = foe.hp;
        inJet = true;
        try { origJet.call(m, v, own, foe); } finally { inJet = false; }
        const af = foe.stacks("sunder");
        const want = Math.min(AC.STATUS.sunder.maxStacks,
                              b4 + (U.sunderN || 1));
        if (af !== want) A.sunderBad++;
        if (af > b4) A.sunderMoves++;
        A.dmgSum += (hp4 - foe.hp);
        if (!foe.alive) A.jetKills++;
      };
      /* [10] EVERY BEAT IS ATTRIBUTED TO THE THING THAT FILED IT, rather than
         counted and divided afterward. The cast, each tear and a fatal jet are
         three different claims and a total cannot separate them. */
      m.beat = function (o) {
        if (o && o.kind === "ult" && o.w === rid){
          if (inTear) A.tearBeats++;
          else if (inJet) A.jetUltBeats++;
          else A.castBeats++;
        }
        if (o && o.fatal && inJet) A.jetFatalBeats++;
        origBeat.call(m, o);
      };

      let lastVentN = 0;
      while (!m.over && step < secs / DT){
        lastVentN = m.vents.length;
        /* [8] NOTHING TICKS THROUGH A HIT STOP. Sampled where the engine's own
           freeze already is -- `step()` returns through `decayImpactOnly` for
           as long as `hitStop` runs and this tick sits below that return, so
           this is a check on the STRUCTURE and not on a guard. */
        const frozen = m.hitStop > 0 && m.vents.length > 0;
        const beforeT = frozen ? m.vents.map(v => v.t + "|" + v.next) : null;

        const firedBefore = m.vents.map(v => v.fired);

        m.step(DT); step++;

        if (frozen){
          const afterT = m.vents.slice(0, beforeT.length)
                          .map(v => v.t + "|" + v.next);
          A.frozenChecks++;
          for (let i = 0; i < afterT.length; i++)
            if (afterT[i] !== beforeT[i]){ A.frozenTick++; break; }
        }
        /* [3] A HOLE FIRING WITH NO LICENCE ANYWHERE */
        if (!m.a.ultBreach && !m.b.ultBreach && m.vents.length){
          A.afterLicence++;
          for (let i = 0; i < m.vents.length; i++)
            if (i < firedBefore.length && m.vents[i].fired > firedBefore[i])
              A.afterLicenceFires++;
        }
        let fires = 0;
        for (let i = 0; i < m.vents.length && i < firedBefore.length; i++)
          if (m.vents[i].fired > firedBefore[i]) fires++;
        A.fired += fires;
        A.maxLive = Math.max(A.maxLive, m.vents.length);
        /* [6] A JET CROSSING A HALL WITH THREE BODIES IN IT, and the check has
           to be able to FAIL: the same predicate `tickBreach` uses, applied to
           every copy, so "no shade is ever caught" is a statement about a
           situation that actually arises rather than one that never comes up.
           `shadeInPath` is the opportunity count. */
        if (m.shades && m.shades.length && m.vents.length){
          A.shadeFrames++;
          const L2 = Math.hypot(AC.CONFIG.arena.w, AC.CONFIG.arena.h);
          const R2 = AC.CONFIG.physics.ballR;
          for (const v of m.vents){
            if (v.front === null || v.front === undefined) continue;
            for (const s of m.shades){
              const px = s.x - v.x, py = s.y - v.y;
              const proj = px * v.ax + py * v.ay;
              const wid = v.half * (0.25 + 0.75
                        * Math.min(1, Math.max(0, proj / (L2 * (U.taperTo || 0.55)))));
              if (proj >= 0 && proj <= v.front
                  && Math.abs(px * v.ay - py * v.ax) <= wid + R2)
                A.shadeInPath++;
            }
          }
        }
        /* [7] the stack the design is built on */
        if (m.vents.length){ A.stackSum += m.b.stacks("sunder"); A.stackN++; }
        /* [8] a corpse is not a target */
        if (!m.b.alive && m.vents.length){
          for (let i = 0; i < m.vents.length && i < firedBefore.length; i++)
            if (m.vents[i].fired > firedBefore[i]) A.corpseFire++;
        }
      }
      /* [8] AND THE HALL STOPS VENTING WHEN THE MATCH DOES. `lastVentN` is the
         count on the frame BEFORE the one that ended it, so the check knows
         whether there was anything to clear -- a "0 vents alive" that was
         always going to be zero is not a measurement. */
      if (m.over){
        A.overN++;
        if (lastVentN > 0) A.overWithVents++;
        for (let i = 0; i < 240; i++) m.step(DT);
        A.overFire += m.vents.length;
      }
      A.casts += me.ultsFired;
      m.tearVent = origTear; m.jetHit = origJet; m.beat = origBeat;
    }
  }
  return A;
}"""


# [1] and [2] want the window's OWN record, which is gone by the time the tick
# has nulled it. So this pass copies it out at the instant it ends.
WINDOW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const out = { windows: [], sixth: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const origTear = m.tearVent;
      let step = 0, prev = null, thisStep = 0;
      /* THE TEAR ON THE CLOSING FRAME COUNTS. `prev` is a snapshot taken
         BEFORE the step, and there is one path where a window closes on the
         same frame as its last tear -- the cap arriving with a cut in the
         stone. Read off `prev` alone that window looks like one tear short of
         the count, which is precisely the difference between "the guard rail
         fired" and "the licence was spent". */
      m.tearVent = function (f, P){
        const b = f.ultBreach ? f.ultBreach.tears : -1;
        origTear.call(m, f, P);
        const a2 = f.ultBreach ? f.ultBreach.tears : -1;
        if (f === m.a && a2 > b) thisStep++;
      };
      while (step < secs / DT){
        prev = m.a.ultBreach
             ? { t: m.a.ultBreach.t, n: m.a.ultBreach.n,
                 tears: m.a.ultBreach.tears, cap: m.a.ultBreach.cap } : null;
        const wasOver = m.over;
        thisStep = 0;
        m.step(DT); step++;
        if (prev && !m.a.ultBreach){
          /* WHAT ENDED IT, AND THE THREE ANSWERS ARE NOT THE SAME CLAIM. The
             first cut of this called everything that did not reach the count
             "the cap" and reported 12% against a registered 2% -- when most of
             those windows had ended because their CASTER DIED or because the
             MATCH did, neither of which is a guard rail failing. */
          out.windows.push({
            t: prev.t, n: prev.n, cap: prev.cap,
            tears: prev.tears + thisStep,
            dead: !m.a.alive, over: m.over && !wasOver,
            late: prev.t + DT >= prev.cap });
        }
        if (m.a.ultBreach && m.a.ultBreach.tears > m.a.ultBreach.n) out.sixth++;
        if (m.over) break;
      }
      m.tearVent = origTear;
    }
  }
  return out;
}"""


# [5] CONSTRUCTED, BOTH WAYS. A vent is planted by hand on a known wall with a
# known bearing, the quarry is parked on the axis at a known distance, and the
# only difference between the two arms is whether it is still there when the
# front arrives. A travelling front that cannot be outrun is a tax; one that
# can is a thing to watch, and it is the whole reason the design paid 4.2
# points for it.
LEAVE_JS = r"""([rid, leave]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(rid, "emberedge", 4242);
  const U = AC.WEAPONS.find(w => w.id === rid).ult;
  const A = AC.CONFIG.arena;
  let hits = 0;
  const orig = m.jetHit;
  m.jetHit = function (){ hits++; return orig.apply(m, arguments); };
  /* a hole on the west wall, firing straight across, mid-height */
  const vy = A.h * 0.5;
  m.vents.length = 0;
  m.vents.push({ own: "a", wall: "W", u: 0.5, x: 0, y: vy, nx: 1, ny: 0,
                 ax: 1, ay: 0, k: 1, half: U.half, life: 99,
                 t: 0, next: 0.001, fired: 0, front: null, spent: false,
                 seq: 1 });
  /* THE QUARRY IS HELD ON THE AXIS BY HAND, re-placed every frame, so this
     measures the mechanic and not the physics. The only difference between the
     two arms is whether it is still there when the front arrives -- and in the
     `leave` arm it moves PERPENDICULAR to the bearing, because sliding along
     the axis is not leaving, it is waiting further out. */
  const D = 420;
  m.b.x = D; m.b.y = vy; m.b.vx = 0; m.b.vy = 0;
  m.a.x = A.w * 0.5; m.a.y = 40;
  const arrive = D / U.speed;                 // when the front gets there
  let t = 0;
  for (let i = 0; i < 240; i++){
    const away = leave && t > arrive * 0.55;
    m.b.x = D; m.b.y = away ? vy - 230 : vy; m.b.vx = 0; m.b.vy = 0;
    m.hitStop = 0;
    m.step(DT); t += DT;
    if (m.over) break;
  }
  return { hits, arrive, front: m.vents.length ? m.vents[0].front : null };
}"""


# [9] PER-MATCH STATE. `gravemourn_relic_probe [9d]`'s pattern: the six control
# matches are run, then a Cindercleave match is run in the same page session,
# then the six are run again. Anything this relic left on a prototype, on a `w`
# object or in a module-level list shows up as a moved summary.
LEAK_JS = r"""([rid, pairs, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const run = (a, b, sd) => {
    const m = new AC.Match(a, b, sd);
    let i = 0;
    while (!m.over && i < secs / DT){ m.step(DT); i++; }
    return [m.t.toFixed(6), m.a.hp.toFixed(6), m.b.hp.toFixed(6),
            m.a.dealt.toFixed(6), m.b.dealt.toFixed(6),
            m.a.hits, m.b.hits, m.a.ultsFired, m.b.ultsFired].join("|");
  };
  const before = pairs.map(p => run(p[0], p[1], p[2]));
  for (const sd of [4242, 771, 90210]) run(rid, "emberedge", sd);
  const after = pairs.map(p => run(p[0], p[1], p[2]));
  let bad = 0;
  for (let i = 0; i < before.length; i++) if (before[i] !== after[i]) bad++;
  return { bad, n: before.length };
}"""


# [P] THE RENDER PATH, CALLED. Not regexed -- v48's own lesson, twice over.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { hole: 0, jet: 0, licence: 0, under: 0, over: 0, threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const lic = m.a.breachFade > 0 || m.b.breachFade > 0;
        if (!m.vents.length && !lic) continue;
        if (m.vents.length) out.hole++;
        if (m.vents.some(v => v.front !== null && v.front !== undefined))
          out.jet++;
        if (lic) out.licence++;
        try { R.ctx.save(); R.drawVents(m, false); R.ctx.restore(); }
        catch (e){ out.threw = "drawVents(under): " + String(e); return out; }
        try { R.ctx.save(); R.drawVents(m, true); R.ctx.restore(); }
        catch (e){ out.threw = "drawVents(over): " + String(e); return out; }
        if (!m.ultFx) continue;
        try { R.ctx.save(); R.drawUltUnder(m); R.ctx.restore(); out.under++; }
        catch (e){ out.threw = "drawUltUnder: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltOver(m); R.ctx.restore(); out.over++; }
        catch (e){ out.threw = "drawUltOver: " + String(e); return out; }
      }
      if (out.jet > 500 && out.licence > 800) return out;
    }
  }
  return out;
}"""


# AND THE ONE THING A RENDER CANNOT SEE. `_burst` does not loop its 0.6s noise
# buffer, so a burst asked for a longer tail simply plays silence into it -- and
# the rendered waveform looks like a sound that ended, which is exactly what a
# sound that ended looks like. So this is measured on the SOURCE.
BURSTS_JS = r"""([names]) => {
  const src = AC.SFX.play.toString();
  const out = { n: 0, max: 0, over: [], missing: [] };
  for (const nm of names){
    const i = src.indexOf('w === "' + nm + '"');
    if (i < 0){ out.missing.push(nm); continue; }
    let j = src.indexOf('} else if (', i);
    if (j < 0) j = src.length;
    const body = src.slice(i, j);
    const re = /_burst\(([\s\S]*?)\)\s*;/g;
    let m2;
    while ((m2 = re.exec(body))){
      const d = /dur:\s*([0-9.]+)/.exec(m2[1]);
      if (!d) continue;
      const v = parseFloat(d[1]);
      out.n++;
      if (v > out.max) out.max = v;
      if (v > 0.6) out.over.push(nm + " " + v + "s");
    }
  }
  return out;
}"""


# `SFX_JS` SCHEDULES AT `currentTime = 1.0` INSIDE A `secs`-LONG BUFFER, so the
# window actually rendered is `secs - 1.0` and asking for 1.0 renders NOTHING.
# The first cut of this list did exactly that for the jet and reported peak 0 --
# which is indistinguishable from the silent ultimate v42 shipped, and is the
# reason the check earns its place even when it is the probe that is wrong.
CASES = [
    ("the cast",        "ult", {"w": "cindercleave"},       2.4),
    ("the wall tears",  "ult", {"w": "cindercleave-tear"},  1.9),
    ("a hole spits",    "ult", {"w": "cindercleave-jet"},   1.8),
    ("and it connects", "ult", {"w": "cindercleave-burn"},  2.0),
]


def profile(g):
    return {k: g.get(k) for k in ("peak", "audible", "low120", "hp300")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-breach.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=130.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    gp = resolve_game(a.game)
    seeds = [2207 + 11 * i for i in range(a.seeds)]
    print(f"\nBREACH — one check per sentence — {gp.name}")

    with game(game_path=gp) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if RID not in ids:
            raise SystemExit(f"{RID} is not in this build")
        U = page.evaluate("(r) => JSON.parse(JSON.stringify("
                          "AC.WEAPONS.find(w=>w.id===r).ult))", RID)
        foes = [i for i in ids if i != RID]
        print(f"  {len(foes)} foes x {len(seeds)} seeds = "
              f"{len(foes)*len(seeds)} fights   "
              f"n {U['n']}  cap {U['cap']}  period {U['period']}  "
              f"speed {U['speed']:g}\n")

        A = page.evaluate(RUN_JS, [RID, foes, seeds, a.secs])
        Wd = page.evaluate(WINDOW_JS, [RID, foes, seeds[:3], a.secs])
        stay = page.evaluate(LEAVE_JS, [RID, False])
        gone = page.evaluate(LEAVE_JS, [RID, True])
        pairs = [["dawnbringer", "axiom", 4242], ["ironhail", "paradox", 771],
                 ["vesper", "thornwake", 90210], ["twinshade", "censer", 313],
                 ["bulwarden", "redflail", 1717], ["foregone", "aureole", 55]]
        leak = page.evaluate(LEAK_JS, [RID, pairs, a.secs])
        drawn = page.evaluate(DRAW_JS, [RID, foes[:8], seeds[:3], a.secs])
        bursts = page.evaluate(BURSTS_JS, [[c[2]["w"] for c in CASES]])

        sfx = {}
        print("[12] THE VOICES")
        print(f"      {'':<21}{'peak':>7}{'audible':>8}{'<120Hz':>9}"
              f"{'>300Hz':>15}")
        for name, kind, pp, secs in CASES:
            g = page.evaluate(SFX_JS, [kind, pp, secs])
            sfx[name] = g
            print(f"      {name:<21}{g['peak']:>7}{g['audible']:>8}s"
                  f"{g['low120']:>9}{g['hp300']:>15}"
                  + (f"   THREW {g['threw']}" if g.get("threw") else ""))
        assert not errors, errors

    n_f = A["fights"]
    wins = Wd["windows"]
    # THE FOUR WAYS A WINDOW ENDS, and only one of them is the guard rail.
    closed = [w for w in wins if w["tears"] >= w["n"]]
    rest = [w for w in wins if w["tears"] < w["n"]]
    dead = [w for w in rest if w["dead"]]
    ended = [w for w in rest if not w["dead"] and w["over"]]
    capped = [w for w in rest if not w["dead"] and not w["over"]]

    print(f"\n[1] THE LICENCE ENDS ON THE FIFTH TEAR")
    check(f"no window ever tears more than n={U['n']}",
          Wd["sixth"] == 0 and all(w["tears"] <= w["n"] for w in wins),
          f"{Wd['sixth']} sixth tears over {len(wins)} windows; "
          f"worst {max((w['tears'] for w in wins), default=0)}")
    check("a window that reaches the count ends on that frame",
          all(w["tears"] == w["n"] for w in closed) and len(closed) > 0,
          f"{len(closed)} of {len(wins)} windows spent the licence, mean "
          f"{statistics.mean([w['t'] for w in closed]):.2f}s into a "
          f"{U['cap']:g}s cap" if closed else "none")

    print(f"\n[2] THE CAP IS A GUARD RAIL")
    rate = len(capped) / max(1, len(wins))
    print(f"        {len(wins)} windows: {len(closed)} spent the count, "
          f"{len(dead)} ended with the CASTER, {len(ended)} with the MATCH,\n"
          f"        {len(capped)} on the cap. Only the last is the guard rail "
          f"firing — the first cut of\n        this check called all "
          f"{len(rest)} of them the cap and reported "
          f"{len(rest)/max(1,len(wins)):.1%}.")
    check("the cap ends fewer than 1 window in 50",
          rate < 0.02,
          f"{len(capped)} of {len(wins)} = {rate:.2%}"
          + ("" if rate < 0.02 else "  <- n IS NOT REACHABLE. The DESIGN "
                                     "changes, not the number."))

    print(f"\n[3] THE HOLES OUTLIVE THE LICENCE")
    check("a hole goes on firing with no licence open anywhere",
          A["afterLicenceFires"] > 0,
          f"{A['afterLicenceFires']} firings over {A['afterLicence']} "
          f"licence-free frames with holes on the walls")

    print(f"\n[4] A JET RESOLVES ONCE PER FIRING, WHEN THE FRONT ARRIVES")
    check("no jet is ever paid twice for one firing",
          A["doublePay"] == 0, f"{A['doublePay']} of {A['hits']} hits")
    check("no hit lands on the frame the jet opens — the front has to travel",
          A["hitOnOpenFrame"] == 0, f"{A['hitOnOpenFrame']} of {A['hits']}")
    check("no hit lands beyond the front's own position",
          A["hitOutsideSweep"] == 0, f"{A['hitOutsideSweep']} of {A['hits']}")

    print(f"\n[5] A QUARRY THAT LEAVES IN TIME IS MISSED")
    check("a quarry that stays on the axis is caught",
          stay["hits"] > 0, f"{stay['hits']} hits, front arrives at "
          f"{stay['arrive']:.2f}s")
    check("the same quarry, gone before the front arrives, is not",
          gone["hits"] == 0, f"{gone['hits']} hits")

    print(f"\n[6] FOE ONLY")
    check("the caster is never its own target",
          A["selfHit"] == 0, f"{A['selfHit']} of {A['hits']}")
    check("no shade is ever caught — DECIDED, and it is the other answer from "
          "design §4.8's placeholder (see `jetHit`)",
          A["shadeHits"] == 0 and A["shadeInPath"] > 0,
          f"{A['shadeHits']} caught, over {A['shadeInPath']} frame-samples "
          f"where a copy was geometrically INSIDE a jet's swept path\n"
          f"        ({A['shadeFrames']} frames with copies in the hall and "
          f"holes on the walls). A check that\n"
          f"        cannot fail is not a check — the opportunity count is what "
          f"makes this one real.")

    print(f"\n[7] EVERY HIT APPLIES EXACTLY ONE SUNDER")
    check(f"every jet hit moves the stack to min(6, before + "
          f"{U['sunderN']})",
          A["sunderBad"] == 0, f"{A['sunderBad']} of {A['hits']} disagree")
    # THE RIGHT NUMBER IS THE STACK, NOT THE SHARE OF HITS THAT RAISED IT. At
    # the cap a hit CANNOT raise it, and a scythe pinned at six stacks is this
    # ultimate doing exactly what it is for. `sunder_survey` measured the
    # unhelped scythe at 1.23 stacks when it lands a blow and 42% of its blows
    # at ZERO; anything near that would mean the jets are not landing.
    mstack = A["stackSum"] / max(1, A["stackN"])
    check("the stack the design is built on actually moves — `sunder_survey` "
          "measured this body at 1.23 stacks unhelped, and the ultimate is the "
          "Sunder rather than the damage",
          mstack > 2.5,
          f"mean {mstack:.2f} on the quarry while holes are open, against "
          f"1.23 unhelped.\n"
          f"        {A['sunderMoves']} of {A['hits']} hits raised it; the rest "
          f"landed on a quarry already at the cap.")

    print(f"\n[8] THE HALL STOPS WHEN THE MATCH DOES")
    check("nothing fires at a corpse", A["corpseFire"] == 0,
          f"{A['corpseFire']}")
    check("no hole survives the end of the match",
          A["overFire"] == 0 and A["overWithVents"] > 0,
          f"{A['overFire']} vents alive 2s after `over`, over "
          f"{A['overWithVents']} of {A['overN']} fights that ended WITH holes "
          f"still on the walls")
    check("no vent clock advances through a hit stop",
          A["frozenTick"] == 0,
          f"{A['frozenTick']} of {A['frozenChecks']} frozen frames moved")

    print(f"\n[9] PER-MATCH STATE")
    check("six other-relic matches are bit-identical before and after a "
          "Cindercleave one in the same page session",
          leak["bad"] == 0, f"{leak['bad']} of {leak['n']} moved")

    print(f"\n[10] THE BEATS")
    check("the cast files exactly one beat",
          A["castBeats"] == A["casts"],
          f"{A['castBeats']} cast beats against {A['casts']} casts")
    check("each tear files its own",
          A["tearBeats"] == A["tears"],
          f"{A['tearBeats']} tear beats against {A['tears']} tears")
    check("and the firings file none — the Thicket's `_cineVine` rule, and "
          "sixty a cast would drown every other beat in the fight",
          A["jetUltBeats"] == 0,
          f"{A['jetUltBeats']} over {A['fired']} firings")
    check("a jet that kills files a FATAL beat — v53 §4, and 30 of 58 "
          "Gravemourn kills rendered a clip with no killing blow before the "
          "same line existed there",
          A["jetKills"] > 0 and A["jetFatalBeats"] == A["jetKills"],
          f"{A['jetKills']} jet kills, {A['jetFatalBeats']} fatal beats filed "
          f"from inside `jetHit`"
          + ("   <- NOT EXERCISED: no jet landed a kill in this run"
             if A["jetKills"] == 0 else ""))

    print(f"\n[11] THE TELEMETRY — BREACH IS TWO SCALARS")
    print(f"        holes a cast     {A['tears']/max(1,A['casts']):>7.2f}"
          f"      (n = {U['n']})")
    print(f"        casts a fight    {A['casts']/n_f:>7.2f}")
    print(f"        jets fired       {A['fired']/n_f:>7.2f} a fight")
    print(f"        JET HITS LANDED  {A['hits']/n_f:>7.2f} a fight"
          f"      <- scalar one")
    print(f"        mean Sunder      {A['stackSum']/max(1,A['stackN']):>7.2f}"
          f"      <- scalar two: what a hit is WORTH")
    print(f"        holes at once    {A['maxLive']:>7}      "
          f"(cap {U['maxVents']})")
    print(f"        jet damage       {A['dmgSum']/n_f:>7.1f} a fight")
    print(f"        The design fitted beam hits at r2 0.33, against GRASP's "
          f"0.79 on one\n        scalar. TUNE BOTH COLUMNS — one number will "
          f"not do it.")

    print(f"\n[12] THE VOICES")
    silent = [n for n, _, _, _ in CASES if sfx[n]["peak"] < 0.002]
    check("every voice renders to something audible — `SFX.play` returns on "
          "its first line headless and swallows its exceptions, so a missing "
          "helper ships as SILENCE (v42)",
          not silent,
          f"quietest peak {min(sfx[n]['peak'] for n, _, _, _ in CASES)}"
          if not silent else f"SILENT: {', '.join(silent)}")
    check("the tear and the burn are distinguishable — the one thing a viewer "
          "has to learn is which jets connected",
          abs(sfx["the wall tears"]["low120"]
              - sfx["and it connects"]["low120"]) > 0.05
          or abs(sfx["the wall tears"]["hp300"]
                 - sfx["and it connects"]["hp300"]) > 0.05,
          f"tear <120Hz {sfx['the wall tears']['low120']}, burn "
          f"{sfx['and it connects']['low120']}")
    check("no `_burst` in any of the four is longer than 0.6s — CLAUDE.md "
          "§4.5: it does not loop its 0.6s noise buffer, so a longer one plays "
          "SILENCE for its tail, measured on the SOURCE and not on the render",
          not bursts["over"] and not bursts["missing"] and bursts["n"] > 0,
          f"{bursts['n']} bursts across the four voices, longest "
          f"{bursts['max']}s"
          + (f"   OVER: {bursts['over']}" if bursts["over"] else ""))

    print(f"\n[P] THE RENDER PATH IS CALLED")
    check("drawVents runs on both passes against a real 2D context, over "
          "holes, jets and a live licence",
          not drawn.get("threw") and drawn.get("jet", 0) > 0
          and drawn.get("licence", 0) > 0,
          f"{drawn.get('hole',0)} hole frames, {drawn.get('jet',0)} with a jet "
          f"in flight, {drawn.get('licence',0)} with the licence lit"
          + (f"   THREW {drawn['threw']}" if drawn.get("threw") else ""))

    ok = sum(1 for _, v in PASS if v)
    print(f"\n{ok}/{len(PASS)} checks passed")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"run": A, "windows": len(wins), "capped": len(capped),
             "sfx": {k: profile(v) for k, v in sfx.items()},
             "draw": drawn, "leak": leak}, indent=1))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
