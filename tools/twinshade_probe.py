#!/usr/bin/env python3
"""TWINSHADE — 24 checks against the build's own prose.

    python3 twinshade_probe.py --game ../02-chain/sc-twinshade.html

Lastlight's harness is the model and its lesson is the reason this file is
long: the Harrowing's latch branch was UNREACHABLE, and the build compiled,
drew, and looked right while the ultimate was silently twelve small arrows.
Only a probe that asks "did anything actually stick" catches that.

The equivalent question here is asked three ways, because this ultimate has
three ways to be silently nothing:

    do the copies EXIST                     [3]
    do they LAND ANYTHING                   [4]
    can the foe KILL them                   [5]   <- the direction the engine
                                                     would never have offered

Every check that asserts an identity is paired with a NEGATIVE CONTROL or
drives the exact window it claims to cover. A check that cannot fail is worth
less than no check, because it reports PASS.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
ID = "twinshade"

# Instrumentation installed once, before any match is built. Wrapping the
# PROTOTYPE rather than an instance is what lets every check below share one
# ledger of who hit whom — and asking the engine rather than inferring from
# hp deltas is the difference between measuring contact and guessing at it.
SETUP_JS = """() => {
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const P = AC.Match.prototype;
  window.__log = { hits: [], clanks: [], err: [] };
  const tag = (f, m) => f == null ? "null"
            : f.shade ? ("shade:" + f.w.id + ":" + (f.shade.owner === m.a ? "a" : "b"))
            : (f === m.a ? "a:" : "b:") + f.w.id;
  const oh = P.resolveHit;
  P.resolveHit = function(self, foe){
    window.__log.hits.push([tag(self, this), tag(foe, this)]);
    return oh.apply(this, arguments);
  };
  const oc = P.resolveClank;
  P.resolveClank = function(A, B){
    window.__log.clanks.push([tag(A, this), tag(B, this)]);
    return oc.apply(this, arguments);
  };
  return "instrumented";
}"""

RESET_JS = "() => { window.__log = { hits: [], clanks: [], err: [] }; return 1; }"

REACH_JS = """([a, b, seed]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  /* fireUlt now opens a one-second hold in which step() ticks nothing at all.
     A check that forces a cast and then steps once is measuring a held frame,
     which is the hit-stop mistake one object along. Stepped past explicitly so
     the hold is exercised rather than skipped. */
  const past = (mm) => { let g = 0; while (mm.splitHold && g++ < 900){ mm.hitStop = 0; mm.step(DT); } mm.hitStop = 0; };

  /* THE FIRST VERSION OF THIS CHECK WAS WRONG AND FAILED A CORRECT BUILD.
     It placed the shade at the foe's reach and then STEPPED forty frames — but
     `move()` runs every one of those frames, so within three of them the
     geometry it had set up no longer existed and it was measuring a drifting
     hall. The field measurement said 26 blows landed unaided in 5 of 6
     pairings while this reported zero, and the disagreement is what gave it
     away.

     Asked at the right granularity instead. The claim is that
     `tickShadeHits` OFFERS the shade to the foe — the engine's own hit loop is
     `[[a,b],[b,a]]` and never would — so the shade is placed on the far end of
     the foe's own first blade segment, taken from `bladeSegments` rather than
     guessed at, and that one method is called once. Nothing moves. */
  const out = {};
  for (const mode of ["touching", "far"]){
    const m = new AC.Match(a, b, seed);
    m.introT = 0; m.step(DT);
    const me = m.a.w.id === a ? m.a : m.b, foe = me === m.a ? m.b : m.a;
    m.fireUlt(me, foe);
    past(m);
    const s = m.shades[0];
    if (!s) return { error: "no shade spawned - check [3] first" };
    const seg = m.bladeSegments(foe)[0];
    const A = AC.CONFIG.arena;
    if (mode === "touching"){ s.x = seg.bx; s.y = seg.by; }
    else { s.x = A.w - seg.bx; s.y = A.h - seg.by; }
    foe.hitCd = foe.hitCd.map(() => 0);
    foe.stun = 0; s.stun = 0;
    const hp0 = s.hp;
    window.__log.hits.length = 0;
    m.tickShadeHits(DT);
    out[mode] = {
      landed: window.__log.hits.filter(([x, y]) => !x.startsWith("shade") &&
                                                    y.startsWith("shade")).length,
      hpLost: +(hp0 - s.hp).toFixed(1),
      d: +Math.hypot(s.x - seg.bx, s.y - seg.by).toFixed(0) };
  }
  return out;
}"""

# One match, stepped, reporting everything the checks below need. `force`
# fires the ultimate on the first frame rather than waiting out an 18s charge,
# so a check does not silently pass by never reaching the code it tests.
RUN_JS = """([a, b, seed, steps, force]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  /* THE LEDGER IS PER-RUN. It is installed on the PROTOTYPE and therefore
     shared by every match this page ever builds; read without resetting it,
     every count below is cumulative across pairings and rises monotonically —
     which is what it did, and which looks enough like "later foes take more
     hits" to be believed. */
  window.__log = { hits: [], clanks: [], err: [] };
  const m = new AC.Match(a, b, seed);
  m.introT = 0;
  const me = m.a.w.id === a ? m.a : m.b;
  const foe = me === m.a ? m.b : m.a;
  const out = { casts: 0, frames: [], maxShades: 0, spawnDist: [],
                spawnFoeDist: [], chargeSeen: 0, noUlt: true,
                shadeHitsFoe: 0, foeHitsShade: 0, shadeKilled: 0,
                shadeExpired: 0, ownerHits0: 0, endedOver: false,
                lifestealDuring: 0, lifestealOutside: 0, lsLeak: 0,
                twoFires: 0, shadeFire: 0, ultWall: 0, ultStep: 0,
                holds: 0, rejoins: 0, holdFrames: 0, holdLeak: 0,
                tetherFrames: 0, drainedPeak: 0,
                clockStall: 0, drainsSeen: 0, drainTotal: 0,
                dur: 0 };
  if (force){
    m.step(DT);
    m.fireUlt(me, foe);
    out.casts++;
  }
  let lastUltT = 0, prevHold = false, prevRejoin = false;
  let frozen = [m.a.x, m.a.y, m.a.hp, m.a.theta, m.b.x, m.b.y, m.b.hp, m.b.theta];
  let frozenT = m.t;
  let prevShades = m.shades.length, prevSplit = !!me.ultSplit;
  let prevFoeHp = foe.hp, prevMeHp = me.hp;
  let steps_ = 0;
  const drops = [];
  while (!m.over && steps_ < steps){
    const hp0 = m.shades.map(s => s.hp);
    const n0 = m.shades.length;
    const split0 = !!me.ultSplit;
    const meHp0 = me.hp;
    m.step(DT);
    steps_++;
    /* CAST COUNTING ONLY. Spawn distances are measured at RELEASE, below —
       at the cast the daughters are inside the parent by design and any
       clearance measured here is a measurement of the hold, not of the
       placement search. */
    if (me.ultSplit && !prevSplit) out.casts++;
    /* SPAWN DISTANCES ARE MEASURED AT RELEASE, NOT AT CAST. The daughters are
       now born INSIDE the parent and walk out of it over a second of stopped
       hall, so a measurement taken at the cast is a measurement of zero. */
    if (prevHold && !m.splitHold && !prevRejoin){
      for (const s of m.shades){
        out.spawnDist.push(Math.hypot(s.x - me.x, s.y - me.y));
        out.spawnFoeDist.push(Math.hypot(s.x - foe.x, s.y - foe.y));
      }
    }
    /* THE HALL MUST ACTUALLY BE STOPPED. Nothing about the two real fighters
       may change on a held frame — not position, not hp, not facing — while
       `m.t` keeps running so a fight is not silently lengthened by its own
       ultimates. Sampled every frame rather than at the ends, because a hold
       that leaked for three frames in the middle would average out. */
    if (prevHold && m.splitHold){
      if (frozen.some((v, j) => v !== [m.a.x, m.a.y, m.a.hp, m.a.theta,
                                       m.b.x, m.b.y, m.b.hp, m.b.theta][j]))
        out.holdLeak++;
      if (!(m.t > frozenT)) out.clockStall++;
      out.holdFrames++;
    }
    if (m.splitHold && !prevHold) out.holds++;
    if (m.splitHold && m.splitHold.rejoin && !prevRejoin) out.rejoins++;
    prevHold = !!m.splitHold;
    prevRejoin = !!(m.splitHold && m.splitHold.rejoin);
    frozen = [m.a.x, m.a.y, m.a.hp, m.a.theta, m.b.x, m.b.y, m.b.hp, m.b.theta];
    frozenT = m.t;
    out.drainsSeen = Math.max(out.drainsSeen, m.drains.length);
    out.drainTotal += m.drains.length;
    prevSplit = !!me.ultSplit;
    out.maxShades = Math.max(out.maxShades, m.shades.length);
    for (const s of m.shades){
      out.chargeSeen = Math.max(out.chargeSeen, s.charge || 0);
      if (!s.noUlt) out.noUlt = false;
    }
    const n1 = m.shades.length;
    if (n1 < n0){
      /* how many went, and whether the split was still running when they did:
         an expiry drops EVERY survivor on one frame, a kill drops one */
      drops.push({ went: n0 - n1, left: n1, split: split0 && !me.ultSplit,
                   t: +m.t.toFixed(3) });
    }
    /* lifesteal: the caster gaining hp with no other source. There is no
       regen in this game and `hp` only rises through lifesteal and ult.heal,
       neither of which any umbral relic has. */
    { const th2 = me === m.a ? m.b : m.a;
      if ((th2.drained || 0) > 0.02) out.tetherFrames++;
      out.drainedPeak = Math.max(out.drainedPeak, th2.drained || 0); }
    if (me.hp > meHp0 + 0.001){
      if (split0 || me.ultSplit) out.lifestealDuring++;
      else out.lifestealOutside++;
    }
    /* THE ACTUAL INVARIANT, asserted every frame rather than inferred from
       when a heal happened: no fighter carries lifesteal without a split
       running. This is what the first version of [11] was reaching for. */
    for (const f of [m.a, m.b])
      if (!f.ultSplit && f.lifesteal) out.lsLeak++;
    if (m.a.ultSplit && m.b.ultSplit) out.twoFires++;
    for (const s3 of m.shades) if (s3.ultSplit) out.shadeFire++;
    if (me.ultSplit){
      out.ultWall += DT;
      out.ultStep += Math.max(0, me.ultSplit.t - lastUltT);
      lastUltT = me.ultSplit.t;
    } else lastUltT = 0;
    for (const s2 of m.shades)
      if (!s2.shade.owner.ultSplit && s2.lifesteal) out.lsLeak++;
  }
  out.dur = +m.t.toFixed(2);
  out.endedOver = !!m.over;
  out.shadesAtEnd = m.shades.length;
  out.drops = drops;
  out.ownerHits = me.hits;
  out.ownerDealt = me.dealt;
  out.foeHp = Math.round(foe.hp);
  out.winner = m.winner ? m.winner.w.id : null;
  const L = window.__log;
  for (const [s, t] of L.hits){
    if (s.startsWith("shade") && !t.startsWith("shade")) out.shadeHitsFoe++;
    if (!s.startsWith("shade") && t.startsWith("shade")) out.foeHitsShade++;
  }
  out.intraHits = L.hits.filter(([s, t]) =>
      (s.startsWith("shade") && t.startsWith("shade")) ||
      (s.startsWith("shade:" + a) && t === "a:" + a) ||
      (s === "a:" + a && t.startsWith("shade:" + a)));
  out.intraClanks = L.clanks.filter(([s, t]) =>
      (s.startsWith("shade") && t.startsWith("shade")) ||
      (s.startsWith("shade") && !t.startsWith("shade") &&
       (t === "a:" + a || t === "b:" + a)));
  return out;
}"""

# [9] THE ONLY killFlight ARMING SITE IN THE GAME IS REACHABLE BY A SHADE.
#
# `tgt` is an "a"/"b" key derived as `foe === this.a ? "a" : "b"`, and a copy is
# neither — so unguarded, Grudgebearer's Crucible killing a COPY arms the kill
# flight on the REAL fighter b: checkEnd holds the match open and move() pins b
# at the first wall with a wallCrack and shake 54. A death that did not happen.
#
# Driven directly, because arranging it in play means waiting for a Crucible to
# be lit AND past its legibility floor AND to connect with a shade on the frame
# that shade is at 1hp. The NEGATIVE CONTROL is the same blow on the real
# fighter: without it this check passes on a build where killFlight never arms
# at all, which is a different bug wearing the same PASS.
KILLFLIGHT_JS = """([a, seed]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  /* fireUlt now opens a one-second hold in which step() ticks nothing at all.
     A check that forces a cast and then steps once is measuring a held frame,
     which is the hit-stop mistake one object along. Stepped past explicitly so
     the hold is exercised rather than skipped. */
  const past = (mm) => { let g = 0; while (mm.splitHold && g++ < 900){ mm.hitStop = 0; mm.step(DT); } mm.hitStop = 0; };
  const out = {};
  for (const target of ["shade", "real"]){
    const m = new AC.Match(a, "grudgebearer", seed);
    m.introT = 0;
    const me = m.a.w.id === a ? m.a : m.b;
    const g  = me === m.a ? m.b : m.a;
    m.step(DT);
    m.fireUlt(me, g);
    past(m);
    const victim = target === "shade" ? m.shades[0] : me;
    if (!victim) return { error: "no shade spawned — check [3] first" };
    victim.hp = 1;
    g.ultForge = { t: 99, minT: 0, cap: 4 };
    m.killFlight = null;
    m.resolveHit(g, victim, victim.x, victim.y, m.bladeSegments(g)[0]);
    out[target] = { armed: !!m.killFlight,
                    tgt: m.killFlight ? m.killFlight.tgt : null,
                    dead: victim.hp <= 0 };
  }
  return out;
}"""

# [10] THE FOE MUST NOT SWING THREE TIMES AS OFTEN.
#
# `tickHits` decrements the attacker's per-blade cooldown at the top, and the
# foe is now offered the shades as extra targets. Without the `cool` flag its
# cooldown ticks once per target.
#
# The foe is STUNNED for the measured frame: `tickHits` continues past a stunned
# blade AFTER decrementing it, so nothing can land and reset a cooldown and turn
# this into a measurement of something else.
COOL_JS = """([a, b, seed]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  /* fireUlt now opens a one-second hold in which step() ticks nothing at all.
     A check that forces a cast and then steps once is measuring a held frame,
     which is the hit-stop mistake one object along. Stepped past explicitly so
     the hold is exercised rather than skipped. */
  const past = (mm) => { let g = 0; while (mm.splitHold && g++ < 900){ mm.hitStop = 0; mm.step(DT); } mm.hitStop = 0; };
  const m = new AC.Match(a, b, seed);
  m.introT = 0;
  m.step(DT);
  const me = m.a.w.id === a ? m.a : m.b;
  const foe = me === m.a ? m.b : m.a;
  m.fireUlt(me, foe);
  past(m);
  const n = m.shades.length;
  foe.stun = 5;
  foe.hitCd = foe.hitCd.map(() => 0.5);
  const before = foe.hitCd.slice();
  m.step(DT);
  const after = foe.hitCd.slice();
  return { shades: n, dt: DT, blades: before.length,
           drop: before.map((v, i) => +(v - after[i]).toFixed(6)) };
}"""

# [11] LIFESTEAL IS TIMED, AND OFF FOR EVERYONE ELSE.
#
# The identity claim is `self.lifesteal || self.w.lifesteal`, which at 0 and
# undefined is the expression that was there before. The control is a pairing
# with no twinshade in it: if any fighter in it gains hp, the edit is not an
# identity and every one of the eighteen other relics has been changed.
LS_JS = """([a, b, seed, steps]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  const m = new AC.Match(a, b, seed);
  m.introT = 0;
  let gains = 0, gainTotal = 0;
  let s = 0;
  while (!m.over && s < steps){
    const h = [m.a.hp, m.b.hp];
    m.step(DT); s++;
    for (let i = 0; i < 2; i++){
      const f = i === 0 ? m.a : m.b;
      if (f.hp > h[i] + 0.001){ gains++; gainTotal += f.hp - h[i]; }
    }
  }
  return { gains, gainTotal: +gainTotal.toFixed(1), steps: s };
}"""

# [13] THE MATCH ENDS AND SO DO THEY, and [14] the killFlight window.
END_JS = """([a, b, seed]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  /* fireUlt now opens a one-second hold in which step() ticks nothing at all.
     A check that forces a cast and then steps once is measuring a held frame,
     which is the hit-stop mistake one object along. Stepped past explicitly so
     the hold is exercised rather than skipped. */
  const past = (mm) => { let g = 0; while (mm.splitHold && g++ < 900){ mm.hitStop = 0; mm.step(DT); } mm.hitStop = 0; };
  const out = {};
  /* (a) the foe dies: `step` returns into decay() from the next frame, so the
     drop has to be in decay and not in tickCharge */
  {
    const m = new AC.Match(a, b, seed);
    m.introT = 0; m.step(DT);
    const me = m.a.w.id === a ? m.a : m.b, foe = me === m.a ? m.b : m.a;
    m.fireUlt(me, foe); past(m);
    const spawned = m.shades.length;
    foe.hp = 0;
    for (let i = 0; i < 60; i++) m.step(DT);
    out.foeDies = { spawned, over: !!m.over, left: m.shades.length,
                    split: !!me.ultSplit, ls: me.lifesteal };
  }
  /* (b) THE KILLFLIGHT WINDOW — `over` is false, move() is still running, and
     tickCharge IS reached. This is the case Lastlight's harrow_probe [10]
     forced above the guard, driven here directly. */
  {
    const m = new AC.Match(a, b, seed);
    m.introT = 0; m.step(DT);
    const me = m.a.w.id === a ? m.a : m.b, foe = me === m.a ? m.b : m.a;
    m.fireUlt(me, foe); past(m);
    const spawned = m.shades.length;
    foe.hp = 0;
    m.killFlight = { tgt: foe === m.a ? "a" : "b", t: 0 };
    for (let i = 0; i < 60; i++){ m.hitStop = 0; m.step(DT); if (!m.shades.length) break; }
    out.killFlight = { spawned, over: !!m.over, left: m.shades.length,
                       split: !!me.ultSplit, flight: !!m.killFlight };
  }
  /* (c) A DEAD SHADE MUST NOT END THE MATCH. checkEnd reads a and b only, so
     this should be true by construction — and by construction is exactly the
     kind of claim that stops being true when someone edits checkEnd. */
  {
    const m = new AC.Match(a, b, seed);
    m.introT = 0; m.step(DT);
    const me = m.a.w.id === a ? m.a : m.b, foe = me === m.a ? m.b : m.a;
    m.fireUlt(me, foe); past(m);
    for (const s of m.shades) s.hp = 0;
    const n = m.shades.length;
    m.hitStop = 0; m.step(DT); m.hitStop = 0; m.step(DT);
    out.shadeDeath = { killed: n, over: !!m.over, left: m.shades.length,
                       split: !!me.ultSplit, aAlive: m.a.alive, bAlive: m.b.alive };
  }
  return out;
}"""

# [15] EVERY PHASE DRAWS. A set-piece that throws is a black frame, and a
# renderer exception inside requestAnimationFrame does not stop the sim — it
# stops the picture and nothing says so.
# THE TWO HOLDS, WATCHED FRAME BY FRAME. Rick asked for a pause in which the
# copies "split off the original like a cell replicating", and for the expiry
# to be "a reverse of the cell split where any surviving clones rejoin the
# original". Both are claims about a TRAJECTORY, so both are sampled rather
# than checked at the ends: a hold that teleported the daughters on the last
# frame would pass any before/after test and would look nothing like division.
HOLDS_JS = """([a, b, seed]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  const m = new AC.Match(a, b, seed);
  m.introT = 0; m.step(DT);
  const me = m.a.w.id === a ? m.a : m.b, foe = me === m.a ? m.b : m.a;
  m.fireUlt(me, foe);
  const out = { split: [], rejoin: [], leak: 0, clock: 0, sawSplit: !!m.splitHold,
                spawnedDuringHold: m.shades.length, sawRejoin: false };
  const snap = () => [m.a.x, m.a.y, m.a.hp, m.a.theta,
                      m.b.x, m.b.y, m.b.hp, m.b.theta];
  let prev = snap(), prevT = m.t;
  let g = 0;
  while (m.splitHold && g++ < 900){
    m.hitStop = 0; m.step(DT);
    const now = snap();
    if (now.some((v, i) => v !== prev[i])) out.leak++;
    if (!(m.t > prevT)) out.clock++;
    prev = now; prevT = m.t;
    out.split.push({ t: +m.splitHold ? +(m.splitHold.t).toFixed(3) : null,
                     d: +Math.hypot(m.shades[0].x - me.x,
                                    m.shades[0].y - me.y).toFixed(1),
                     born: +m.shades[0].born.toFixed(2),
                     lit: +(me.ultSplit.lit || 0).toFixed(2) });
  }
  out.afterSplit = { d: +Math.hypot(m.shades[0].x - me.x,
                                    m.shades[0].y - me.y).toFixed(1),
                     n: m.shades.length, vx: +m.shades[0].vx.toFixed(0) };
  /* run to the expiry — the reunion has to happen on its own, not be forced */
  let seen = false;
  while (!m.over && g++ < DT_FPS * 90){
    m.step(DT);
    if (m.splitHold && m.splitHold.rejoin){
      seen = true;
      out.rejoin.push({ d: +Math.hypot(m.shades[0].x - me.x,
                                       m.shades[0].y - me.y).toFixed(1),
                        born: +m.shades[0].born.toFixed(2),
                        n: m.shades.length });
    }
    if (seen && !m.splitHold) break;
  }
  out.sawRejoin = seen;
  out.afterRejoin = { n: m.shades.length, split: !!me.ultSplit,
                      ls: me.lifesteal };
  return out;
}"""

# [12e] DOES THE DRAIN ACTUALLY CHANGE THE FRAME?
#
# Every check on this effect asked whether motes were SPAWNED. None asked
# whether they MOVE, or whether removing them changes a single pixel — and for
# four builds the answer to both was no on the build of record, while the probe
# reported 54/54.
#
# The cause was `liquid_build.py` replacing the whole tail of
# `tickPresentation` and silently discarding the drain's clock, so `d.t` never
# advanced, every strand sat at u <= 0 and `drawDrains` skipped all of them.
# The relic build was correct; the file being watched was not.
#
# Two questions, and the second one cannot be satisfied by anything except the
# effect reaching the canvas:
#
#   [a] do strands become LIVE (0 < u <= 1) and then get removed
#   [b] does deleting `m.drains` change the rendered frame — on BOTH the
#       probe's draw path and the path the mp4 is rendered through, which are
#       different code and only one had ever been looked at
#
# THE SHAKE HAS TO BE PINNED FIRST. `draw()` offsets the hall by
# (Math.random()-0.5)*m.shake every call, so two renders of one state differ
# across the whole frame; the first version of [b] measured that and reported a
# million differing pixels. v26 §4's open decision, met as a real obstacle.
LIVE_JS = """([id, foe, seed]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  AC.__inject && AC.__inject(m);
  const me = m.a.w.id === id ? m.a : m.b;
  let g = 0;
  while (g++ < 400000 && !(me.ultSplit && m.drains.length >= 8)) m.step(DT);
  if (!m.drains.length) return { error: "no drain reached in 400k steps" };
  const born = m.drains.length;
  const liveAt = [];
  for (let k = 0; k < Math.round(1.2 / DT); k++){
    m.step(DT);
    liveAt.push(m.drains.filter(d => {
      const u = (d.t - d.delay) / d.life; return u > 0 && u <= 1; }).length);
  }
  const peakLive = Math.max(...liveAt);
  const advanced = m.drains.length ? Math.max(...m.drains.map(d => d.t)) : 0;
  /* find a frame that HAS live strands, then diff it */
  let guard = 0;
  while (guard++ < 60000 && !m.drains.some(d => {
      const u = (d.t - d.delay) / d.life; return u > 0.15 && u < 0.85; })) m.step(DT);
  const cv = document.getElementById('cv');
  m.shake = 0;
  const keep = m.drains.slice();
  const shot = (fn) => { fn(); return cv.toDataURL('image/png'); };
  const plainWith = shot(() => AC.__draw(m));
  m.drains.length = 0;
  const plainWithout = shot(() => AC.__draw(m));
  m.drains.push(...keep);
  let lerpWith = null, lerpWithout = null;
  if (typeof CINE !== "undefined"){
    lerpWith = shot(() => { CINE.snap(m); CINE.drawLerped(AC.renderer, m, 0.5); });
    m.drains.length = 0;
    lerpWithout = shot(() => { CINE.snap(m); CINE.drawLerped(AC.renderer, m, 0.5); });
    m.drains.push(...keep);
  }
  return { born, peakLive, advanced: +advanced.toFixed(3),
           liveNow: m.drains.filter(d => {
             const u = (d.t - d.delay) / d.life; return u > 0 && u <= 1; }).length,
           plainWith, plainWithout, lerpWith, lerpWithout };
}"""

DRAW_JS = """([a, b, seed]) => {
  const DT = AC.CONFIG.physics.dt, DT_FPS = Math.round(1/DT);
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const out = [];
  const phases = ["before", "dividing", "dividing-late", "arriving",
                  "burning", "guttering", "one-dead", "rejoining", "after"];
  for (const p of phases){
    const m = new AC.Match(a, b, seed);
    m.introT = 0; m.step(DT);
    const me = m.a.w.id === a ? m.a : m.b, foe = me === m.a ? m.b : m.a;
    const past = () => { let g = 0; while (m.splitHold && g++ < 900){ m.hitStop = 0; m.step(DT); } m.hitStop = 0; };
    if (p !== "before"){
      m.fireUlt(me, foe);
      if (p === "dividing"){      for (let i = 0; i < 12; i++){ m.hitStop = 0; m.step(DT); } }
      if (p === "dividing-late"){ for (let i = 0; i < 50; i++){ m.hitStop = 0; m.step(DT); } }
      if (p === "arriving"){      past(); for (let i = 0; i < 4;  i++) m.step(DT); }
      if (p === "burning"){       past(); for (let i = 0; i < 90; i++) m.step(DT); }
      if (p === "guttering"){     past(); me.ultSplit.t = me.ultSplit.dur * 0.92; m.step(DT); }
      if (p === "one-dead"){      past(); if (m.shades[0]) m.shades[0].hp = 0; m.step(DT); }
      if (p === "rejoining"){     past(); m.endSplit(me);
                                  for (let i = 0; i < 12; i++){ m.hitStop = 0; m.step(DT); } }
      if (p === "after"){         past(); m.endSplit(me); past(); m.step(DT); }
      /* and a drain in flight, on every phase that has one to draw */
      if (m.drains.length === 0 && m.shades[0]) m.drain(foe, me, 9);
    }
    let err = null;
    try { AC.__draw(m); } catch (e){ err = String(e); }
    /* the interpolated path too: it is what the live page and the clip
       renderer both actually call, and it touches a different set of objects */
    let lerpErr = null;
    try {
      if (typeof CINE !== "undefined"){ CINE.snap(m); CINE.drawLerped(AC.renderer, m, 0.5); }
    } catch (e){ lerpErr = String(e); }
    /* did the snapshot actually take the shades? a shade outside it strobes */
    let snapped = null;
    if (typeof CINE !== "undefined" && CINE._snap)
      snapped = m.shades.filter(s => CINE._snap.has(s)).length;
    out.push({ phase: p, shades: m.shades.length, err, lerpErr, snapped });
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-twinshade-scrunch.html")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--steps", type=int, default=60 * 110)
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")

    FOES = ["widowmaker", "spellbreaker", "thornwake", "emberedge",
            "lightkeeper", "gravemourn"]
    seeds = [A.seed + i * 7919 for i in range(A.seeds)]

    ok, notes = {}, []

    def say(k, good, msg):
        ok[k] = bool(good)
        print(f"    {'PASS' if good else 'FAIL'}  {msg}")

    with game(game_path=g) as (page, errors):
        print(page.evaluate(SETUP_JS), "\n")

        relic = page.evaluate(
            "(id) => { const w = AC.WEAPONS.find(x => x.id === id);"
            "return w ? { name: w.name, dmg: w.dmg, ult: w.ult } : null; }", ID)
        if not relic:
            sys.exit(f"[1] FAIL — no relic {ID!r} in this build")
        u = relic["ult"]
        print(f"[1] THE RELIC IS IN THE BUILD")
        say("relic", True,
            f"{relic['name']}  dmg {relic['dmg']}  ult {u['name']!r} "
            f"kind {u['kind']!r} charge {u['charge']}s")
        say("ultdata", all(k in u for k in ("dur", "shades", "hp", "lifesteal")),
            f"ult carries dur {u.get('dur')} · shades {u.get('shades')} · "
            f"hp {u.get('hp')} · lifesteal {u.get('lifesteal')}")
        say("tip", len(u.get("tip", "")) <= 72,
            f"tip is {len(u.get('tip',''))} chars of 72")

        # ---------------------------------------------------------------- [2]
        print(f"\n[2] IT FIGHTS — {len(FOES)} foes, ult FORCED on frame one so "
              f"no check below can pass by never reaching the ultimate")
        runs = []
        for foe in FOES:
            r = page.evaluate(RUN_JS, [ID, foe, A.seed, A.steps, True])
            runs.append((foe, r))
            print(f"    v {foe:<13} {r['dur']:>6.1f}s  {r['ownerHits']:>3} hits  "
                  f"maxShades {r['maxShades']}  shade->foe {r['shadeHitsFoe']:>3}  "
                  f"foe->shade {r['foeHitsShade']:>3}  "
                  f"winner {str(r['winner'])}")
        say("fights", all(r["endedOver"] for _, r in runs),
            "every pairing resolves")

        # ---------------------------------------------------------------- [3]
        print(f"\n[3] THE COPIES EXIST  — the Harrowing's 'did anything stick'")
        maxs = [r["maxShades"] for _, r in runs]
        say("spawn", all(m == u["shades"] for m in maxs),
            f"every cast put exactly {u['shades']} on the floor "
            f"(observed {sorted(set(maxs))})")
        d0 = [d for _, r in runs for d in r["spawnDist"]]
        say("clear", d0 and min(d0) >= 68.0,
            f"born clear of the caster's shell: closest {min(d0):.1f} of "
            f"2R=68 — inside it and the split fires like a nova on frame one")
        df = [d for _, r in runs for d in r["spawnFoeDist"]]
        say("clearfoe", df and min(df) > 34.0,
            f"and clear of the FOE: closest {min(df):.1f}")

        # ---------------------------------------------------------------- [4]
        print(f"\n[4] THE COPIES LAND SOMETHING  — a shade that spawns and never "
              f"connects is an ultimate that is silently nothing")
        sh = [r["shadeHitsFoe"] for _, r in runs]
        say("shadehits", all(x > 0 for x in sh),
            f"shade -> foe hits per pairing: {sh}")
        say("credit", all(r["ownerHits"] >= r["shadeHitsFoe"] for _, r in runs),
            "shade hits are credited to the caster (verify.py's contact floor "
            "reads hits.a + hits.b and would not otherwise see them)")

        # ---------------------------------------------------------------- [5]
        print(f"\n[5] THE FOE CAN KILL THEM  — the direction the engine's own "
              f"hit loop [[a,b],[b,a]] would never have offered")
        fh = [r["foeHitsShade"] for _, r in runs]
        print(f"    field: foe -> shade hits per pairing {fh}  "
              f"(REPORTED, not asserted — a chain at reach 96 landing nothing "
              f"on a 6s copy is an ordinary outcome, not a defect)")
        rc = page.evaluate(REACH_JS, [ID, "thornwake", A.seed])
        if rc.get("error"):
            say("reach", False, rc["error"]); say("reachctl", False, "-")
        else:
            print(f"    shade ON the foe's blade tip:  "
                  f"{rc['touching']['landed']} hits, "
                  f"{rc['touching']['hpLost']} hp off it  (d={rc['touching']['d']})")
            print(f"    shade across the hall:         "
                  f"{rc['far']['landed']} hits, {rc['far']['hpLost']} hp off it  "
                  f"(d={rc['far']['d']})   <- negative control")
            say("reach", rc["touching"]["landed"] > 0 and rc["touching"]["hpLost"] > 0,
                "the foe's blade REACHES a copy and takes life off it — the "
                "engine's own hit loop is [[a,b],[b,a]] and would never have "
                "offered one as a target")
            say("reachctl", rc["far"]["landed"] == 0,
                "and does not when it is nowhere near one — without this the "
                "check above passes on a build that hits everything")
        say("foehitsfield", sum(fh) > 0,
            f"and across the field the foe lands {sum(fh)} blows on copies "
            f"unaided, in {sum(1 for x in fh if x)}/{len(fh)} pairings")

        # ---------------------------------------------------------------- [6]
        print(f"\n[6] NOTHING INTRA-TEAM  — Rick: they cannot hurt or clank with "
              f"each other or the original")
        ih = [h for _, r in runs for h in r["intraHits"]]
        ic = [c for _, r in runs for c in r["intraClanks"]]
        say("nointra", not ih, f"shade-on-shade / shade-on-caster hits: {len(ih)}"
                               + (f"  {ih[:3]}" if ih else ""))
        say("noclank", not ic, f"shade-on-shade / shade-on-caster clanks: {len(ic)}"
                               + (f"  {ic[:3]}" if ic else ""))

        # ---------------------------------------------------------------- [7]
        print(f"\n[7] NO RECURSION  — the interview answer that stops this being "
              f"exponential")
        say("noult", all(r["noUlt"] for _, r in runs),
            "every shade carries noUlt")
        say("nocharge", all(r["chargeSeen"] == 0 for _, r in runs),
            f"no shade's charge ever left 0 "
            f"(max seen {max(r['chargeSeen'] for _, r in runs)})")

        # ---------------------------------------------------------------- [8]
        print(f"\n[8] ONE BEAT  — Rick chose all-at-once over a rolling expiry")
        exp = [d for _, r in runs for d in r["drops"] if d["split"]]
        bad = [d for d in exp if d["left"] != 0]
        full = [d for d in exp if d["went"] == u["shades"]]
        say("onebeat", exp and not bad,
            f"{len(exp)} expiries, every one left NOTHING behind"
            + (f" — EXCEPT {bad[:3]}" if bad else "")
            + f"  ({len(full)} of them dropped the full {u['shades']}; the "
              f"rest had already lost a copy to the foe, which is the same "
              f"beat with fewer survivors in it)")

        # --------------------------------------------------------------- [8b]
        print(f"\n[8b] THE FIRE IS ON THE CASTER ONLY — Rick's answer, and the "
              f"only thing on screen saying which of three identical purple "
              f"balls has the health bar")
        say("onefire", sum(r["twoFires"] for _, r in runs) == 0,
            f"never two fighters burning at once "
            f"({sum(r['twoFires'] for _, r in runs)} frame-pairs)")
        say("nocopyfire", sum(r["shadeFire"] for _, r in runs) == 0,
            f"and no COPY ever carries ultSplit — drawShadeFire iterates "
            f"[m.a, m.b] and cannot reach one, which is exactly the kind of "
            f"claim that stops being true when someone edits the loop "
            f"({sum(r['shadeFire'] for _, r in runs)} frame-shades)")
        wall = sum(r["ultWall"] for _, r in runs)
        step = sum(r["ultStep"] for _, r in runs)
        casts = sum(r["casts"] for _, r in runs)
        print(f"    HALL-TIME DILATION, over {casts} casts: the ultimate's own "
              f"clock advanced {step:.1f}s\n    while {wall:.1f}s of hall time "
              f"passed — {wall/max(0.01,step):.2f}x. `this.t` runs through hit "
              f"stop but\n    tickCharge does not, so the ult only ages on "
              f"STEPPED frames: THE MORE IT\n    LANDS, THE LONGER IT LASTS. "
              f"Nominal {u['dur']:g}s is really "
              f"{u['dur'] * wall/max(0.01,step):.1f}s of hall.\n"
              f"    REPORTED, not asserted — it is a property of the engine's "
              f"hit-stop convention\n    (Slagburst's fuse and the Harrowing's "
              f"both have it), not a defect. It is\n    larger here because no "
              f"other ultimate puts three attackers on the floor.")

        # ---------------------------------------------------------------- [9]
        print(f"\n[9] A SHADE IS NOT A KILL TARGET  — the only killFlight "
              f"arming site in the game, driven directly, with a control")
        kf = page.evaluate(KILLFLIGHT_JS, [ID, A.seed])
        if kf.get("error"):
            say("killflight", False, kf["error"]); say("kfcontrol", False, "-")
        else:
            print(f"    Crucible kills a SHADE:  armed={kf['shade']['armed']} "
                  f"tgt={kf['shade']['tgt']}  (shade died: {kf['shade']['dead']})")
            print(f"    Crucible kills the REAL: armed={kf['real']['armed']} "
                  f"tgt={kf['real']['tgt']}   <- negative control")
            say("killflight", kf["shade"]["dead"] and not kf["shade"]["armed"],
                "killing a copy does NOT arm the kill flight "
                "(unguarded it arms on the real fighter b and plays a death "
                "that did not happen)")
            say("kfcontrol", kf["real"]["armed"],
                "and killing a real fighter still DOES — without this the "
                "check above passes on a build where nothing ever arms")

        # --------------------------------------------------------------- [10]
        print(f"\n[10] THE FOE DOES NOT SWING THREE TIMES AS OFTEN  — tickHits "
              f"decrements the attacker's cooldown, and the foe now has three "
              f"targets")
        cd = page.evaluate(COOL_JS, [ID, "thornwake", A.seed])
        dt, drops = cd["dt"], cd["drop"]
        want = dt
        worst = max(abs(d - want) for d in drops) if drops else 9
        say("hitcd", cd["shades"] > 0 and worst < 1e-6,
            f"with {cd['shades']} shades alive the foe's per-blade cooldown "
            f"fell by {drops} against dt {dt:.6f} — "
            f"{1 + cd['shades']}x would be {(1+cd['shades'])*dt:.6f}")

        # --------------------------------------------------------------- [11]
        print(f"\n[11] LIFESTEAL IS TIMED, AND IS AN IDENTITY FOR EVERYONE ELSE")
        during = sum(r["lifestealDuring"] for _, r in runs)
        outside = sum(r["lifestealOutside"] for _, r in runs)
        say("lifesteal", during > 0,
            f"the caster gained hp on {during} frames while the split ran")
        say("lsoff", outside == 0,
            f"and on {outside} frames while it did not")
        leaks = sum(r["lsLeak"] for _, r in runs)
        say("lsinvariant", leaks == 0,
            f"and NO fighter, real or copy, ever carried lifesteal with no "
            f"split running — {leaks} frame-fighters over "
            f"{sum(1 for _ in runs)} pairings")
        ctl = page.evaluate(LS_JS, ["widowmaker", "thornwake", A.seed, A.steps])
        say("lsidentity", ctl["gains"] == 0,
            f"CONTROL — a pairing with no twinshade in it: {ctl['gains']} hp "
            f"gains over {ctl['steps']} steps. Any gain means the `self.lifesteal "
            f"|| self.w.lifesteal` edit is not an identity and all eighteen "
            f"other relics have moved.")

        # --------------------------------------------------------------- [12]
        print(f"\n[12] THE ULTIMATE CANNOT OUTLIVE THE MATCH")
        e = page.evaluate(END_JS, [ID, "thornwake", A.seed])
        fd, kfw, sd = e["foeDies"], e["killFlight"], e["shadeDeath"]
        print(f"    foe dies        spawned {fd['spawned']}  over {fd['over']}  "
              f"shades left {fd['left']}  split {fd['split']}  lifesteal {fd['ls']}")
        say("endmatch", fd["over"] and fd["left"] == 0 and not fd["split"]
                        and fd["ls"] == 0,
            "the kill drops every copy, the fire and lifesteal in the same "
            "frame — step() returns into decay() from the next frame, so this "
            "cannot be done in tickCharge")
        print(f"    killFlight win  spawned {kfw['spawned']}  over {kfw['over']}  "
              f"shades left {kfw['left']}  split {kfw['split']}")
        say("kfwindow", not kfw["over"] and kfw["left"] == 0 and not kfw["split"],
            "and the killFlight window — `over` false, move() still running — "
            "drops them too. This is harrow_probe [10]'s case: below the guard "
            "it is unreachable")
        print(f"    shade killed    killed {sd['killed']}  over {sd['over']}  "
              f"left {sd['left']}  split {sd['split']}  a/b alive "
              f"{sd['aAlive']}/{sd['bAlive']}")
        say("shadedeath", not sd["over"] and sd["left"] == 0 and sd["split"]
                          and sd["aAlive"] and sd["bAlive"],
            "killing every copy ends NOTHING — the match runs on and the split "
            "keeps burning. checkEnd reads a and b only, and this is the check "
            "that notices if that stops being true")

        # -------------------------------------------------------------- [12b]
        print(f"\n[12b] THE HALL ACTUALLY STOPS — Rick: \"lets have the fight "
              f"pause for a second while the duplicates split off the "
              f"original\"")
        h = page.evaluate(HOLDS_JS, [ID, "thornwake", A.seed])
        sp, rj = h["split"], h["rejoin"]
        say("holdopens", h["sawSplit"] and h["spawnedDuringHold"] == u["shades"],
            f"the cast opens a hold with {h['spawnedDuringHold']} daughters "
            f"already inside the parent")
        say("holdfreeze", h["leak"] == 0,
            f"over {len(sp)} held frames NOTHING about either real fighter "
            f"moved — position, hp or facing ({h['leak']} leaks). Sampled every "
            f"frame, because a hold that leaked for three frames in the middle "
            f"would pass a before/after test")
        say("holdclock", h["clock"] == 0,
            f"and `m.t` advanced on every one of them, so a fight is not "
            f"silently lengthened by the ultimates cast in it")
        walked = sp and sp[0]["d"] < 12 and sp[-1]["d"] > 60
        span = (sp[-1]["d"] - sp[0]["d"]) if sp else 0
        # the designed overshoot is 6% of the span, taken over the last fifth
        back = max((sp[i-1]["d"] - sp[i]["d"] for i in range(1, len(sp))),
                   default=0)
        half = sp[len(sp)//2]["d"] if sp else 0
        say("holdwalk", walked and back <= span * 0.075 and 0.25 < half/max(1,span) < 0.75,
            f"the daughters WALK out — {sp[0]['d'] if sp else '?'} -> "
            f"{half:.0f} at the halfway frame -> {sp[-1]['d'] if sp else '?'}. "
            f"Largest backward step {back:.1f} of a {span:.0f} span, which is "
            f"the designed overshoot (a cell strains and lets go; it does not "
            f"glide). A hold that teleported them on the last frame would pass "
            f"any before/after test and would look nothing like division")
        say("holdlight", sp and sp[0]["lit"] < 0.15 and sp[-1]["lit"] > 0.85,
            f"and the fire ignites ON the division rather than after it "
            f"(lit {sp[0]['lit'] if sp else '?'} -> {sp[-1]['lit'] if sp else '?'})")
        say("holdrelease", h["afterSplit"]["n"] == u["shades"]
                           and h["afterSplit"]["vx"] != 0,
            f"and they leave the hold at speed, {h['afterSplit']['d']} units out")

        # -------------------------------------------------------------- [12c]
        print(f"\n[12c] AND THEY COME BACK — Rick: \"a reverse of the cell "
              f"split where any surviving clones rejoin the original\"")
        say("rejoinhappens", h["sawRejoin"] and len(rj) > 0,
            f"the expiry opens a reunion hold on its own, unforced "
            f"({len(rj)} held frames)")
        say("rejoinwalk", rj and rj[0]["d"] > rj[-1]["d"] and rj[-1]["d"] < 30,
            f"and the survivors walk HOME — {rj[0]['d'] if rj else '?'} -> "
            f"{rj[-1]['d'] if rj else '?'} units, the split run backwards")
        say("rejoinends", h["afterRejoin"]["n"] == 0
                           and not h["afterRejoin"]["split"]
                           and h["afterRejoin"]["ls"] == 0,
            f"and when they land, all of it ends together — copies, fire and "
            f"lifesteal on one frame")

        # -------------------------------------------------------------- [12d]
        print(f"\n[12d] THE LIFESTEAL IS VISIBLE — Rick: \"show something "
              f"being pysically taken and streamed back\"")
        say("drains", sum(r["drainTotal"] for _, r in runs) > 0,
            f"motes are torn off the foe on a heal — peak {max(r['drainsSeen'] for _, r in runs)} "
            f"in flight at once, {sum(r['drainTotal'] for _, r in runs)} "
            f"frame-motes across the field")
        dctl = page.evaluate(
            "([a,b,seed,steps]) => { const DT = AC.CONFIG.physics.dt;"
            " const m = new AC.Match(a,b,seed); m.introT=0;"
            " let n=0,s=0; while(!m.over && s++<steps){ m.step(DT); n+=m.drains.length; }"
            " return n; }", ["widowmaker", "thornwake", A.seed, A.steps])
        # the 34% of blows that heal NOTHING used to draw nothing at all
        wj = page.evaluate(
            "([id, foe, seed]) => { const DT = AC.CONFIG.physics.dt;"
            " const m = new AC.Match(id, foe, seed);"
            " m.introT = 0; m.step(DT);"
            " const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;"
            " me.lifesteal = 0.35; me.hp = me.maxHp;"          # FULL: nothing to gain
            " const n0 = m.drains.length;"
            " m.resolveHit(me, th, th.x, th.y, m.bladeSegments(me)[0]);"
            " const wasted = m.drains.slice(n0);"
            " me.hp = me.maxHp * 0.5; const n1 = m.drains.length;"
            " m.resolveHit(me, th, th.x, th.y, m.bladeSegments(me)[0]);"
            " const real = m.drains.slice(n1);"
            " return { wasted: wasted.length, wastedCut: wasted.length ? wasted[0].cut : null,"
            "          real: real.length, realCut: real.length ? real[0].cut : null,"
            "          drained: +(th.drained || 0).toFixed(2) }; }",
            [ID, "thornwake", A.seed])
        print(f"    at FULL health: {wj['wasted']} motes, cut {wj['wastedCut']} "
              f"(they die in mid-air)")
        print(f"    at half health: {wj['real']} motes, cut {wj['realCut']} "
              f"(they arrive)")
        say("wasted", wj["wasted"] > 0 and wj["wastedCut"] and wj["wastedCut"] < 1,
            "a blow that heals NOTHING still draws — measured, 34% of blows "
            "landed under this ultimate are clamped at full hp and used to "
            "draw nothing at all, which is a third of the window")
        say("wastedreal", wj["real"] > wj["wasted"] and wj["realCut"] == 1,
            "and a blow that heals MORE draws more of them, and they arrive — "
            "without this the check above passes on a build where nothing ever "
            "reaches the ball")
        tf = sum(r["tetherFrames"] for _, r in runs)
        say("tether", tf > 0 and max(r["drainedPeak"] for _, r in runs) > 0.9,
            f"the foe carries a `drained` level that bridges the gaps between "
            f"bursts — lit on {tf} frames across the field, peak "
            f"{max(r['drainedPeak'] for _, r in runs):.2f}")
        say("drainidentity", dctl == 0,
            f"CONTROL — a pairing with no lifesteal in it spawned {dctl} of "
            f"them. `drains` is a new list on every Match in the game and this "
            f"is what says it costs nothing in the eighteen that never fill it")

        # -------------------------------------------------------------- [12e]
        print(f"\n[12e] AND IT REACHES THE CANVAS — the check whose absence let "
              f"four builds ship an effect that never rendered")
        lv = page.evaluate(LIVE_JS, [ID, "emberedge", 177319])
        if lv.get("error"):
            say("live", False, lv["error"]); say("pixels", False, "-")
            say("pixelscine", False, "-")
        else:
            print(f"    {lv['born']} strands born · clock reached "
                  f"{lv['advanced']}s · peak {lv['peakLive']} live at once")
            say("live", lv["peakLive"] > 0 and lv["advanced"] > 0.1,
                "strands MOVE — `d.t` advances and they pass through the "
                "drawable range. Spawning was all any earlier check asked, and "
                "spawning was never the thing that was broken")
            import base64, io
            from PIL import Image, ImageChops
            def px(a1, b1):
                if not a1 or not b1: return -1
                A = Image.open(io.BytesIO(base64.b64decode(a1.split(",",1)[1]))).convert("RGB")
                B = Image.open(io.BytesIO(base64.b64decode(b1.split(",",1)[1]))).convert("RGB")
                bb = ImageChops.difference(A, B).getbbox()
                return 0 if bb is None else (bb[2]-bb[0]) * (bb[3]-bb[1])
            pa = px(lv["plainWith"], lv["plainWithout"])
            pc = px(lv["lerpWith"], lv["lerpWithout"])
            print(f"    deleting m.drains changes  AC.__draw: {pa} px of bbox   "
                  f"CINE.drawLerped: {pc} px of bbox")
            say("pixels", pa > 2000,
                "removing the drain CHANGES THE RENDERED FRAME on the probe's "
                "own draw path")
            say("pixelscine", pc > 2000,
                "and on CINE.drawLerped, which is the path the mp4 is rendered "
                "through — different code, and until now only one of the two "
                "had ever been looked at")

        # --------------------------------------------------------------- [13]
        print(f"\n[13] EVERY PHASE DRAWS, ON BOTH PATHS")
        for d in page.evaluate(DRAW_JS, [ID, "thornwake", A.seed]):
            bad = d["err"] or d["lerpErr"]
            miss = d["shades"] and d["snapped"] != d["shades"]
            print(f"    {d['phase']:<11} shades {d['shades']}  "
                  f"snapshot {d['snapped']}  "
                  f"{'THREW: ' + str(bad) if bad else 'draw ok'}"
                  f"{'   <-- NOT INTERPOLATED (will strobe)' if miss else ''}")
            ok[f"draw:{d['phase']}"] = not bad and not miss

        # --------------------------------------------------------------- [14]
        print(f"\n[14] THE ULTIMATE FIRES ON ITS OWN — every check above forced "
              f"it, and a charge gate that never opens would pass all of them")
        nat = []
        for s in seeds[:4]:
            r = page.evaluate(RUN_JS, [ID, "thornwake", s, A.steps, False])
            nat.append(r)
            print(f"    seed {s:<10} {r['dur']:>6.1f}s  casts {r['casts']}  "
                  f"maxShades {r['maxShades']}  shade->foe {r['shadeHitsFoe']}")
        say("natural", all(r["casts"] > 0 for r in nat),
            f"the ultimate fires unaided in {sum(1 for r in nat if r['casts'])}"
            f"/{len(nat)} matches")

        if errors:
            print("\nPAGE ERRORS (a silent exception reads as a clean run):")
            for x in errors[:10]:
                print("   ", x)
            ok["clean"] = False
        else:
            ok["clean"] = True

    print("\n" + "=" * 68)
    good = sum(1 for v in ok.values() if v)
    for k, v in ok.items():
        if not v:
            print(f"  FAIL  {k}")
    print(f"  {good}/{len(ok)} checks pass")
    print("=" * 68)
    return 0 if good == len(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
