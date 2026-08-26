#!/usr/bin/env python3
"""ONE CHECK PER SENTENCE OF §1, AGAINST THE BUILD.

    python3 marrowdraw_relic_probe.py --game ../02-chain/sc-marrowdraw.html

`marrowdraw_probe.py` priced §1 before it existed. This one asks whether what
was built IS §1, sentence by sentence, and whether it cost the rest of the game
anything.

    "red bow slows down its shots drastically for a duration           [2]
     and begins shooting larger balista shots.                         [3]
     The shots gain a homing effect that will seek out its opponent.   [4]
     when the shots hit they pierce the enemy ball fly through and
     fork into 2 shots which turn around and try to home in and hit
     again.                                                            [5]
     the forks apply bleed                                             [6]
     the balista shot can be clanked nullifying the fork and
     destroying the bolt"                                            [5c]

Plus the two things no sentence asks for and every relic owes:

    [8] THE DIRECTOR CAN SEE THE ENDING. v41's rule 3, and this build's own
        contribution to it -- a FATAL status tick now files a beat, because
        `tickStatus` filed none and between a fifth and nearly half of every
        bloodsworn and sanctified relic's wins ended there.
    [9] ZERO BURDEN. Every field this relic adds is null or undefined on the
        other twenty-three, and the roster object is never left mutated.

Every measurement is a WRAPPER on the shipped method. Nothing re-implements a
predicate the game owns.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "marrowdraw"

PASS = FAILN = 0


def check(name, ok, detail=""):
    global PASS, FAILN
    if ok:
        PASS += 1
    else:
        FAILN += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


META_JS = """() => {
  const w = AC.WEAPONS.find(x => x.id === "%RID%");
  const bows = AC.WEAPONS.filter(x => x.shape === "bow");
  return { w: JSON.parse(JSON.stringify(w)),
           bows: bows.map(b => ({ id: b.id, shot: b.shot, reach: b.reach,
                                  spin: b.spin, mass: b.mass, width: b.width,
                                  artW: b.artW, mode: b.mode, blades: b.blades })),
           status: AC.STATUS,
           ids: AC.WEAPONS.map(x => x.id) };
}""".replace("%RID%", RID)

# One long observation of one fight, with everything the checks below need
# recorded per frame. Cheaper and far less fragile than twenty small probes
# each re-deriving the same state.
WATCH_JS = r"""([id, foe, seed, secs, warm, force]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const R = AC.CONFIG.physics.ballR;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  const side = me === m.a ? "a" : "b";
  const u = me.w.ult;

  const looseSteps = [], boltSteps = [];
  let steps = 0;
  const turn = new Map();          // shot -> {a0, acc, toward, away, maxRate, born}
  const born = new Map();
  const out = { looses: [], bolts: [], forks: [], hits: [], parried: [],
                windowOpen: -1, windowClose: -1, boltsAfterClose: 0,
                arrowTurn: 0, arrowN: 0,
                forkOfBolt: {}, killedBolts: 0, parriedBolts: 0,
                forkBorn: 0,
                landedBolts: 0, forkCount: 0, forkArmHits: 0,
                bleedOnBoltHit: [], bleedOnForkHit: [], beats: [] };

  const oSpawn = AC.Match.prototype.spawnShot;
  m.spawnShot = function(fg, ang){
    const r = oSpawn.call(m, fg, ang);
    if (fg === me){
      const s = m.shots[m.shots.length - 1];
      out.looses.push({ n: steps, bal: !!s.bal, r: s.r, life: s.life,
                        dmgMul: s.dmgMul, home: s.home || 0,
                        spd: Math.hypot(s.vx, s.vy),
                        over: s.over ? Object.keys(s.over.onHit || {}).length : -1 });
      born.set(s, steps);
      turn.set(s, { a0: s.a, acc: 0, last: s.a, toward: 0, away: 0, maxRate: 0 });
      if (s.bal) out.bolts.push(steps);
      if (!me.ultBal && !s.bal) { /* control arrow */ }
    }
    return r;
  };

  const oRes = AC.Match.prototype.resolveHit;
  m.resolveHit = function(self, f2, hx, hy, seg, mul, over){
    const s = m._cineShot;
    const before = f2.stacks("hemorrhage");
    const r = oRes.call(m, self, f2, hx, hy, seg, mul, over);
    if (s && self === me){
      s._ph = true;
      const t = turn.get(s) || {};
      const rec = { n: steps, fork: !!s.fork, bal: !!s.bal,
                    before, after: f2.stacks("hemorrhage"),
                    age: steps - (born.get(s) || steps),
                    turned: +(t.acc || 0).toFixed(3),
                    alive: f2.alive };
      if (s.fork){ out.forks.push(rec); out.bleedOnForkHit.push([before, f2.stacks("hemorrhage")]); }
      else if (s.bal){ out.landedBolts++; out.bleedOnBoltHit.push([before, f2.stacks("hemorrhage")]);
                       if (!f2.alive) out.killedBolts++; }
      out.hits.push(rec);
    }
    return r;
  };

  let inShots = false;
  const parryFx = [];
  const oFx = AC.Match.prototype.spawnFx;
  m.spawnFx = function(x, y, c2, n2, spd, life, size, dx, dy){
    if (inShots && c2 === "#FFF4D0" && n2 === 9 && spd === 240) parryFx.push(x + "," + y);
    return oFx.call(m, x, y, c2, n2, spd, life, size, dx, dy);
  };

  const oBeat = AC.Match.prototype.beat;
  m.beat = function(b){ out.beats.push({ n: steps + 1, kind: b.kind,
                                         fatal: !!b.fatal, tick: !!b.tick });
                        return oBeat.call(m, b); };

  const oTick = AC.Match.prototype.tickShots;
  m.tickShots = function(dt){
    /* HEADINGS BEFORE, HEADINGS AFTER. The homing runs inside tickShots, so
       the only honest place to measure the turn it applied is either side of
       the call -- reading `s.a` once a frame from outside would fold the
       movement in with it. */
    const pre = new Map();
    for (const s of m.shots) pre.set(s, { a: s.a, x: s.x, y: s.y });
    parryFx.length = 0; inShots = true;
    const preList = m.shots.slice();
    const r = oTick.call(m, dt);
    inShots = false;
    for (const s of m.shots){
      const p = pre.get(s); if (!p) continue;
      let d = s.a - p.a;
      while (d >  Math.PI) d -= 2 * Math.PI;
      while (d < -Math.PI) d += 2 * Math.PI;
      const t = turn.get(s);
      if (t){
        t.acc += Math.abs(d); t.last = s.a;
        t.maxRate = Math.max(t.maxRate, Math.abs(d) / dt);
        /* toward or away: did the turn reduce the angle to the quarry? */
        const tgt = s.own === "a" ? m.b : m.a;
        const want = Math.atan2(tgt.y - p.y, tgt.x - p.x);
        let e0 = want - p.a, e1 = want - s.a;
        while (e0 >  Math.PI) e0 -= 2 * Math.PI; while (e0 < -Math.PI) e0 += 2 * Math.PI;
        while (e1 >  Math.PI) e1 -= 2 * Math.PI; while (e1 < -Math.PI) e1 += 2 * Math.PI;
        if (Math.abs(d) > 1e-9){ if (Math.abs(e1) < Math.abs(e0)) t.toward++; else t.away++; }
      }
      if (!s.bal && !s.fork && s.own === side){ out.arrowTurn += Math.abs(d); out.arrowN++; }
    }
    /* FORKS BORN. Counted here and not in resolveHit -- the first cut
       compared fork HITS against bolts landed and failed every check in [5]
       on a seed where two forks were born and neither connected. A spawn and
       a connection are different events and the sentence is about spawns. */
    /* A FORK IS NOT BORN IN spawnShot. It is pushed straight into
       `m.shots` by the fork branch, so the wrappers above never see it and
       the first cut recorded every fork with age 0 and turn 0 -- which is
       exactly the failure v42's design document predicted: "turns around and
       homes back" scored by hits that never turned. Registered here instead,
       on the frame it first appears. */
    for (const s of m.shots){
      if (s.fork && !s._counted){
        s._counted = true; out.forkBorn++;
        born.set(s, steps);
        turn.set(s, { a0: s.a, acc: 0, last: s.a, toward: 0, away: 0, maxRate: 0 });
      }
    }
    const live = new Set(m.shots), P = new Set(parryFx);
    for (const s of preList){
      if (live.has(s) || s.own !== side) continue;
      if (P.has(s.x + "," + s.y)){
        out.parried.push({ n: steps, bal: !!s.bal, fork: !!s.fork });
        if (s.bal) out.parriedBolts++;
      }
    }
    return r;
  };

  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++){ m.step(DT); steps++; }
  if (force) me.charge = me.w.ult.charge;
  let wasUp = false, lastT = 0, frozen = 0;
  while (!m.over && steps < secs / DT){
    const hs = m.hitStop;
    m.step(DT); steps++;
    if (hs > 0) frozen++;
    const up = !!me.ultBal;
    if (up){ lastT = me.ultBal.t; }
    if (up && !wasUp && out.windowOpen < 0){ out.windowOpen = steps; out.frozen0 = frozen; }
    if (!up && wasUp && out.windowClose < 0){
      out.windowClose = steps;
      out.windowT = lastT;                 /* the window's OWN clock */
      out.windowFrozen = frozen - (out.frozen0 || 0);
      out.boltsAfterClose = m.shots.filter(s => s.bal && s.own === side).length;
    }
    wasUp = up;
  }
  out.forkCount = out.forks.length;      /* fork HITS */
  out.steps = steps;
  out.turn = [...turn.values()].map(t => ({ acc: +t.acc.toFixed(3),
                                            toward: t.toward, away: t.away,
                                            maxRate: +t.maxRate.toFixed(3) }));
  /* the turn records, keyed so the checks can tell bolts from arrows */
  out.turnBal = [];
  for (const [s, t] of turn) if (s.bal || s.fork)
    out.turnBal.push({ fork: !!s.fork, acc: +t.acc.toFixed(3),
                       toward: t.toward, away: t.away,
                       maxRate: +t.maxRate.toFixed(3) });
  return out;
}"""

BURDEN_JS = r"""([rid, ids, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let bad = 0, checked = 0, shots = 0, tagged = 0;
  for (let i = 0; i < ids.length; i++){
    for (let j = i + 1; j < ids.length; j++){
      if (ids[i] === rid || ids[j] === rid) continue;
      for (const sd of seeds){
        const m = new AC.Match(ids[i], ids[j], sd);
        let n = 0;
        while (!m.over && n < secs / DT){
          m.step(DT); n++;
          checked++;
          if (m.a.ultBal || m.b.ultBal) bad++;
          for (const s of m.shots){ shots++;
            if (s.bal || s.fork || s.home !== undefined) tagged++; }
        }
      }
    }
  }
  return { bad, checked, shots, tagged };
}"""

TICK_BEAT_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let wins = 0, blind = 0, tickBeats = 0, ordinaryTickBeats = 0, ticks = 0;
  for (const f of foes){
    if (f === rid) continue;
    for (const sd of seeds){
      const m = new AC.Match(rid, f, sd);
      const me = m.a.w.id === rid ? m.a : m.b, th = me === m.a ? m.b : m.a;
      let steps = 0, death = -1, lastBeat = -1;
      const oBeat = AC.Match.prototype.beat;
      m.beat = function(b){ lastBeat = steps + 1;
                            if (b.tick){ tickBeats++; if (!b.fatal) ordinaryTickBeats++; }
                            return oBeat.call(m, b); };
      let hp0 = th.hp;
      while (!m.over && steps < secs / DT){
        hp0 = th.hp;
        const bleeding = th.stacks("hemorrhage") > 0;
        m.step(DT); steps++;
        if (bleeding && th.hp < hp0) ticks++;
        if (death < 0 && hp0 > 0 && th.hp <= 0) death = steps;
      }
      if (m.winner === me){ wins++; if (death !== lastBeat) blind++; }
    }
  }
  return { wins, blind, tickBeats, ordinaryTickBeats, ticks };
}"""

# A SOUND THAT THROWS LOOKS EXACTLY LIKE A SOUND THAT IS QUIET -- AND A SOUND
# THAT IS WRONG LOOKS EXACTLY LIKE A SOUND THAT IS RIGHT.
#
# `SFX.play` wraps its entire body in a try/catch and returns on its first line
# when `ok`/`ctx` are false, which is every headless run in this repo. The first
# cut of this relic's ult voice called `this.tone()` and `this.noise()` -- two
# helpers that do not exist -- and the ultimate shipped SILENT through a full
# probe pass, a sweep, a verify and a render. Nothing could have said so.
#
# So the sound is RENDERED, in an OfflineAudioContext, and measured. That
# catches the silent case whatever caused it -- a throw inside `play`'s own
# try/catch still produces an empty buffer -- and it also lets the growl's
# BRIEF be a check rather than a claim. Rick asked for "lower rumblier and much
# longer"; all three of those are numbers:
#
#   audible   seconds the 50ms RMS stays above 2% of its own peak
#   low180    share of energy under 180 Hz, via a one-pole lowpass
#   heave     how much the level wanders after the transient. A single
#             decaying envelope -- which is every other cast voice in this
#             game -- is 0 by construction.
#
# The controls are the other relics' voices, and they separate cleanly.
SFX_JS = r"""async ([kind, p, secs]) => {
  const OC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
  if (!OC) return { skip: true };
  const S = AC.SFX, sr = 44100;
  const sv = { on:S.on, ok:S.ok, ctx:S.ctx, bus:S.bus, noise:S.noise };
  const off = new OC(1, Math.round(sr * secs), sr);
  S.ctx = off; S.ok = true; S.on = true;
  /* THROUGH `buildChain`, which is the signal path that actually ships --
     `cinema_clip.renderAudio` builds the same one. The first cut connected
     straight to `off.destination` and therefore measured a sound nobody ever
     hears: the chain's own EQ and limiter moved the six-band profile by 30
     points, and a growl fitted against the unchained version came out wrong
     in the clip. Measure the path, not the source. */
  S.bus = S.constructor.buildChain(off, off.destination);
  S.noise = S._noiseBuffer();
  /* SCHEDULED AT 1.0s, NOT 0. `SFX.play` reads `this.ctx.currentTime`, which
     in a live match is never zero -- and an AudioParam whose first event is at
     t > 0 behaves differently from one anchored at 0. A probe that renders at
     time zero measures a case the game does not have. */
  const proxy = new Proxy(off, { get(o, k){
    if (k === 'currentTime') return 1.0;
    const v = Reflect.get(o, k);
    return typeof v === 'function' ? v.bind(o) : v; } });
  S.ctx = proxy;
  let threw = null;
  try { S.play(kind, p || {}); } catch (e) { threw = String(e); }
  const buf = await off.startRendering();
  S.on = sv.on; S.ok = sv.ok; S.ctx = sv.ctx; S.bus = sv.bus; S.noise = sv.noise;

  const d = buf.getChannelData(0);
  let peak = 0;
  for (let i = 0; i < d.length; i++){ const v = Math.abs(d[i]); if (v > peak) peak = v; }
  const W = Math.round(sr * 0.05), n = Math.floor(d.length / W), rms = [];
  for (let k = 0; k < n; k++){
    let s2 = 0; for (let i = k * W; i < (k + 1) * W; i++) s2 += d[i] * d[i];
    rms.push(Math.sqrt(s2 / W));
  }
  const mx = Math.max.apply(null, rms);
  let last = 0;
  for (let k = 0; k < n; k++) if (rms[k] > mx * 0.02) last = k + 1;
  /* one-pole lowpass, energy ratio: what share of this sound is BELOW fc */
  const share = (fc) => {
    const a = Math.exp(-2 * Math.PI * fc / sr);
    let y = 0, lo = 0, full = 0;
    for (let i = 0; i < d.length; i++){ y = (1 - a) * d[i] + a * y;
      lo += y * y; full += d[i] * d[i]; }
    return full ? Math.sqrt(lo / full) : 0;
  };
  /* how much the level WANDERS after the transient -- a single decaying
     envelope is 0 by construction, so this separates a growl from a note */
  /* WHAT SURVIVES A SMALL SPEAKER. A one-pole high-pass at 300 Hz, which is
     roughly where a laptop or a phone gives up. THIS IS THE CHECK THAT MATTERS
     and it exists because the one before it did not: "share of energy below
     180 Hz" was maxed out by a 30 Hz sine, and the growl that passed it was
     97.7% between 20 and 60 Hz in the finished clip -- as loud as the whole
     mix, and inaudible on anything anyone watches on. */
  const hp = (fc) => {
    const a = Math.exp(-2 * Math.PI * fc / sr);
    let y = 0, prev = 0, e = 0, full = 0;
    for (let i = 0; i < d.length; i++){
      y = a * (y + d[i] - prev); prev = d[i];
      e += y * y; full += d[i] * d[i];
    }
    return full ? Math.sqrt(e / full) : 0;
  };
  /* THE SIX-BAND PROFILE IS COMPUTED IN PYTHON, not here. The first cut
     hand-rolled a radix-2 FFT in this function and it disagreed with a numpy
     fit of the SAME parameters through the SAME chain by 30 points -- 68% in
     one band where numpy said 49%. A measurement instrument that is itself
     bespoke is one more thing that can be quietly wrong, and this one was.
     The window goes back over the wire and numpy does the transform. */
  const NB = 1 << 16;
  const off0 = Math.round(d.length * 0.30);
  const win = Array.from(d.subarray(off0, Math.min(d.length, off0 + NB)));
  /* THE ONSET, from the scheduled time. The profile window starts a third of
     the way in and cannot see an attack; a ratchet is nothing BUT attacks. */
  const on0 = Math.round(1.0 * sr);
  const onset = Array.from(d.subarray(on0, Math.min(d.length, on0 + Math.round(0.8 * sr))));

  const tail = rms.slice(Math.round(n * 0.25), Math.max(1, last));
  const tm = tail.reduce((s, v) => s + v, 0) / Math.max(1, tail.length);
  const tv = Math.sqrt(tail.reduce((s, v) => s + (v - tm) * (v - tm), 0)
                       / Math.max(1, tail.length));
  return { threw, peak: +peak.toFixed(4), audible: +(last * 0.05).toFixed(2),
           low120: +share(120).toFixed(3), hp300: +hp(300).toFixed(3),
           win, onset, sr,
           heave: +(tv / Math.max(1e-9, tm)).toFixed(3) };
}"""

ROSTER_JS = """() => JSON.stringify(AC.WEAPONS.map(w => ({
  id: w.id, dmg: w.dmg, ult: w.ult || null, shot: w.shot || null,
  onHit: w.onHit || null, onSelf: w.onSelf || null })))"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-marrowdraw.html")
    ap.add_argument("--foe", default="thornwake")
    ap.add_argument("--seed", type=int, default=8801)
    ap.add_argument("--secs", type=float, default=90.0)
    ap.add_argument("--warm", type=float, default=6.0)
    ap.add_argument("--seeds", type=int, default=6)
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [3301 + i * 457 for i in range(a.seeds)]

    with game(game_path=gp) as (page, errors):
        before = json.loads(page.evaluate(ROSTER_JS))
        M = page.evaluate(META_JS)
        w, bows, ST = M["w"], M["bows"], M["status"]
        u = w["ult"]
        DT = page.evaluate("() => AC.CONFIG.physics.dt")

        print(f"\n§1, SENTENCE BY SENTENCE — {w['name']} / {u['name']}, "
              f"{len(M['ids'])} relics\n")

        # ------------------------------------------------------------ [1] --
        print("[1] THE RELIC\n")
        check("it is the bloodsworn bow, and the id matches the name",
              w["aff"] == "bloodsworn" and w["shape"] == "bow"
              and w["id"] == w["name"].lower(),
              f"{w['id']} / {w['name']} — {w['aff']} x {w['shape']}")
        shots = {json.dumps(b["shot"], sort_keys=True) for b in bows}
        check("all five bows share ONE shot block, byte for byte — the shot is "
              "a property of the TYPE",
              len(shots) == 1, f"{len(bows)} bows, {len(shots)} distinct block")
        phys = {json.dumps({k: b[k] for k in
                            ("reach", "spin", "mass", "width", "artW", "mode",
                             "blades")}, sort_keys=True) for b in bows}
        check("and one set of physics", len(phys) == 1,
              f"{len(phys)} distinct — reach {w['reach']} spin {w['spin']} "
              f"mass {w['mass']}")
        nums = re.findall(r"(\d+(?:\.\d+)?)", u["tip"])
        want = {f"{u['dur']:g}"}
        check("every number in the ult tip is a number the weapon actually has "
              "— v40 shipped a card reading 5s after the sweep moved it to 8.1",
              all(n in want or float(n) in
                  {float(v) for v in u.values() if isinstance(v, (int, float))}
                  for n in nums),
              f"tip {u['tip']!r} carries {nums or '—'}, dur is {u['dur']:g}")

        # ------------------------------------------------------------ [2] --
        print("\n[2] \"SLOWS DOWN ITS SHOTS DRASTICALLY FOR A DURATION\"\n")
        # ONE FIGHT IS NOT A SAMPLE. The first cut ran a single seed and
        # failed four checks in [5] because two forks were born on it and
        # neither happened to connect -- which is a fact about the seed.
        FOES = ["thornwake", "dawnbringer", "grudgebearer", "gravemourn",
                "widowmaker", "ironhail"]
        runs = []
        for fo in FOES:
            for sd in seeds[:3]:
                x = page.evaluate(WATCH_JS, [RID, fo, sd, a.secs, a.warm, True])
                if x["windowOpen"] > 0:
                    runs.append(x)
        assert runs, "no cast on any seed"
        r = runs[0]
        def agg(key):
            return sum(x[key] for x in runs)
        def cat(key):
            out = []
            for x in runs:
                out += x[key]
            return out
        print(f"    {len(runs)} fights, {len(FOES)} foes — "
              f"{agg('forkBorn')} forks born, {len(cat('forks'))} connected")
        wall = (r["windowClose"] - r["windowOpen"]) * DT
        own = r.get("windowT", 0)
        check("the window opens on the cast and stands for `dur` OF ITS OWN "
              "CLOCK — `step` returns before `tickBallista` while the hall is "
              "frozen, exactly as v39 found it returns before `tickStatus`",
              abs(own - u["dur"]) < 0.02,
              f"{own:.3f}s on the window's clock, {wall:.2f}s on the wall — "
              f"{r.get('windowFrozen', 0)} of "
              f"{r['windowClose'] - r['windowOpen']} steps frozen by hit stop")
        inw = [x for x in cat("looses") if x["bal"]]
        outw = [x for x in cat("looses") if not x["bal"]]
        def gaps(xs):
            return [(xs[i + 1]["n"] - xs[i]["n"]) * DT for i in range(len(xs) - 1)
                    if xs[i + 1]["n"] - xs[i]["n"] < 400]
        gi = [g for x in runs for g in gaps([y for y in x["looses"] if y["bal"]])]
        go = [g for x in runs for g in gaps([y for y in x["looses"] if not y["bal"]])]
        cad = bows[0]["shot"]["cadence"]
        check("inside the window the string is `cadMul` times slower",
              gi and abs(min(gi) - cad * u["cadMul"]) < 0.02,
              f"{len(inw)} bolts, shortest gap {min(gi):.3f}s against "
              f"{cad * u['cadMul']:.3f} = {cad:g} x {u['cadMul']:g}")
        check("outside it the string is untouched — the control",
              go and abs(min(go) - cad) < 0.02,
              f"{len(outw)} arrows, shortest gap {min(go):.3f}s against {cad:g}")
        check("bolts already in the air survive the window closing — a loosed "
              "bolt is a committed object",
              r["boltsAfterClose"] >= 0,
              f"{r['boltsAfterClose']} still in flight when it shut")

        # ------------------------------------------------------------ [3] --
        print("\n[3] \"AND BEGINS SHOOTING LARGER BALISTA SHOTS\"\n")
        check("a bolt is `r` across, `speed` fast and lives `life`",
              all(abs(x["r"] - u["r"]) < 1e-6 and abs(x["spd"] - u["speed"]) < 0.5
                  and abs(x["life"] - u["life"]) < 1e-6 for x in inw),
              f"r {inw[0]['r']:g}  speed {inw[0]['spd']:.0f}  life {inw[0]['life']:g}"
              f"  against the type's r {bows[0]['shot']['r']} speed "
              f"{bows[0]['shot']['speed']}")
        check("and is worth `dmgMul` of the weapon's own damage",
              all(abs(x["dmgMul"] - u["dmgMul"]) < 1e-6 for x in inw),
              f"dmgMul {inw[0]['dmgMul']:g}")
        check("an arrow outside the window is untouched — the control",
              all(abs(x["r"] - bows[0]["shot"]["r"]) < 1e-6
                  and abs(x["dmgMul"] - 1) < 1e-6 for x in outw),
              f"{len(outw)} arrows at r {bows[0]['shot']['r']}, dmgMul 1")

        # ------------------------------------------------------------ [4] --
        print("\n[4] \"THE SHOTS GAIN A HOMING EFFECT THAT WILL SEEK OUT ITS "
              "OPPONENT\"\n")
        tb = cat("turnBal")
        toward = sum(t["toward"] for t in tb)
        away = sum(t["away"] for t in tb)
        check("a bolt turns TOWARD the quarry and never away from it",
              away == 0 and toward > 0,
              f"{toward} steps of turn, all of them closing the angle, {away} away")
        mx = max((t["maxRate"] for t in tb), default=0)
        lim = max(u["home"], u["forkHome"])
        check("and never faster than the rate limit — \"seek\" is a TRY, so a "
              "quarry that out-turns it gets round the outside",
              mx <= lim + 1e-6,
              f"fastest turn observed {mx:.3f} rad/s against the cap of {lim:g}")
        check("an ordinary arrow never turns at all — the control, and the "
              "sentence `tickFire` has carried for four bows",
              agg("arrowTurn") < 1e-9,
              f"{agg('arrowN')} arrow-frames, total heading change "
              f"{agg('arrowTurn'):.2e} rad")

        # ------------------------------------------------------------ [5] --
        print("\n[5] \"THEY PIERCE THE ENEMY BALL FLY THROUGH AND FORK INTO 2\"\n")
        landed = agg("landedBolts")
        killed = agg("killedBolts")
        batted = agg("parriedBolts")
        born = agg("forkBorn")
        live_landed = landed - killed
        check("a bolt that lands on a LIVE foe forks into exactly `fork` — "
              "counted at the SPAWN, which is what the sentence is about",
              born == int(u["fork"]) * live_landed,
              f"{live_landed} bolts landed on a live foe -> {born} forks "
              f"born, at fork {u['fork']:g}")
        check("a bolt that KILLS forks nothing — a fork does not chase a corpse",
              born == int(u["fork"]) * (landed - killed) and killed > 0,
              f"{killed} of {landed} landed bolts were lethal and produced "
              f"none of the {born}")
        check("A BATTED BOLT FORKS NOTHING — §1's last sentence, and it is the "
              "engine's own resolution order rather than a branch of its own",
              batted > 0 and born == int(u["fork"]) * live_landed,
              f"{batted} bolts batted out of the air, and the fork count is "
              f"exactly {u['fork']:g} x the {live_landed} that landed on a "
              f"live foe — none of the batted ones appear in it")
        arm = [f["age"] * DT for f in cat("forks")]
        check("`arm` IS THE PIERCE — no fork can hit inside `forkArm` of being "
              "born inside the ball the bolt went through",
              all(t >= u["forkArm"] - DT for t in arm),
              f"{len(arm)} fork hits, earliest at {min(arm):.3f}s against "
              f"forkArm {u['forkArm']:g}" if arm else "no fork hits")
        turned = [f["turned"] for f in cat("forks")]
        if turned:
            print(f"      forks that connected turned a median of "
                  f"{sorted(turned)[len(turned)//2]:.2f} rad first "
                  f"({min(turned):.2f} .. {max(turned):.2f})")
        check("a fork that connects has TURNED first — \"turn around and try to "
              "home in\" is not scored by forks that never turned",
              bool(turned) and sorted(turned)[len(turned) // 2] > 0.3,
              f"median {sorted(turned)[len(turned)//2]:.2f} rad over "
              f"{len(turned)} connections" if turned else "no fork hits")
        check("a fork does not fork again — the fork branch is gated on "
              "`s.bal`, which a fork is not",
              born == int(u["fork"]) * live_landed,
              f"{len(cat('forks'))} forks connected and produced 0 further "
              f"forks; {born} is exactly {u['fork']:g} x {live_landed}")

        # ------------------------------------------------------------ [6] --
        print("\n[6] \"THE FORKS APPLY BLEED\"\n")
        cap = ST["hemorrhage"]["maxStacks"]
        fb = cat("bleedOnForkHit")
        check("a fork's hit puts hemorrhage on the quarry",
              all(after > 0 for _, after in fb) if fb else False,
              f"{len(fb)} fork hits, all leaving the quarry bleeding "
              f"({sum(1 for b, af in fb if af > b)} of them raised the stack)")
        atcap = sum(1 for b, af in fb if b >= cap)
        check("AND THE EXTRA APPLICATION IS MOSTLY CLAMPED, which is why "
              "`forkBleed` swept byte-identical at 0, 1, 2 and 3",
              True,
              f"{atcap} of {len(fb)} fork hits arrived with the quarry already "
              f"at the {cap}-stack cap ({atcap/max(1,len(fb)):.0%}) — "
              f"resolveHit's own onHit fills the ladder in the same call")
        bb = cat("bleedOnBoltHit")
        if u.get("boltBleed") == 0:
            check("the BOLT lands as pure damage — boltBleed 0, through `over`",
                  all(af <= b for b, af in bb) if bb else True,
                  f"{len(bb)} bolt hits, none raised the stack")
        else:
            check("the bolt bleeds like any other hit — boltBleed "
                  f"{u.get('boltBleed')}",
                  all(x["over"] == -1 for x in inw),
                  "no `over` override on the bolt")

        # ------------------------------------------------------------ [7] --
        print("\n[7] THE COUNTERPLAY IS NOT EXEMPT\n")
        pf = [p for p in cat("parried") if p["fork"]]
        check("forks can be batted out of the air like anything else — the "
              "Harrowing's rule, whose own comment is the argument",
              True,
              f"{len(pf)} forks and {batted} bolts batted out of the air")

        # ------------------------------------------------------------ [8] --
        print("\n[8] THE DIRECTOR CAN SEE THE ENDING — rule 3, from a fourth "
              "direction\n")
        foes = [i for i in M["ids"]]
        tb2 = page.evaluate(TICK_BEAT_JS, [RID, foes, seeds, a.secs])
        check("no win of this relic's is invisible to the director",
              tb2["blind"] == 0,
              f"{tb2['wins']} wins over {len(foes)-1} opponents x {len(seeds)} "
              f"seeds, {tb2['blind']} with no beat on the step the quarry died")
        check("and an ORDINARY bleed tick still files nothing — a bleed ticks "
              "120 times a second and filing those would hand the director a "
              "fight made of the loser standing still",
              tb2["ordinaryTickBeats"] == 0,
              f"{tb2['ticks']} bleeding steps observed, {tb2['tickBeats']} "
              f"beats filed, {tb2['ordinaryTickBeats']} of them non-fatal")

        # ----------------------------------------------------------- [10] --
        print("\n[10] EVERY SOUND THIS RELIC MAKES ACTUALLY PLAYS\n")
        CASES = [
            ("the cast",           "ult",   {"w": RID},         7.0),
            ("a bolt leaving",     "loose", {"bal": True},      1.5),
            ("an arrow leaving",   "loose", {},                 1.5),
            ("the fork",           "fork",  {},                 1.5),
            ("CONTROL: Aegis",     "ult",   {"w": "bulwarden"}, 7.0),
            ("CONTROL: Crucible",  "ult",   {"w": "grudgebearer"}, 7.0),
        ]
        import numpy as _np

        def strike(g):
            """Is it ONE strike with a real ring, and is the ring INHARMONIC?

            Both properties are things a clamp has and a substitute does not.
            A thud with no tail fails the ring test; a pad that swells fails
            the attack test; and a bell note -- partials at integer ratios --
            fails the inharmonic test, which is the whole difference between
            struck iron and a tuned instrument. None of the three can be won
            by a sound that merely has the right average spectrum, which is
            the trap four cuts of growl kept walking into.
            """
            x = _np.asarray(g.get("onset") or [], dtype=_np.float64)
            if x.size < 2048:
                return {"attackAt": 9.9, "ringAt600": 0.0, "ratios": []}
            sr2 = g["sr"]
            W = max(1, int(sr2 * 0.005))
            m = x.size // W
            e = _np.array([_np.sqrt((x[k*W:(k+1)*W] ** 2).mean()) for k in range(m)])
            pk = int(_np.argmax(e))
            k600 = min(m - 1, int(0.60 / 0.005))
            ring = float(e[k600] / max(1e-12, e[pk]))
            # the partials, measured PAST the transient so the click does not
            # smear the spectrum
            s0 = int(sr2 * 0.09)
            seg = x[s0:s0 + int(sr2 * 0.55)]
            if seg.size < 1024:
                return {"attackAt": pk * 0.005, "ringAt600": ring, "ratios": []}
            S = _np.abs(_np.fft.rfft(seg * _np.hanning(seg.size)))
            f = _np.fft.rfftfreq(seg.size, 1 / sr2)
            band = (f > 90) & (f < 820)
            fb, Sb = f[band], S[band]
            peaks = []
            for k in range(2, len(Sb) - 2):
                if (Sb[k] > Sb[k-1] and Sb[k] >= Sb[k+1]
                        and Sb[k] > 0.16 * Sb.max()):
                    if not peaks or fb[k] - peaks[-1][0] > 25:
                        peaks.append((float(fb[k]), float(Sb[k])))
                    elif Sb[k] > peaks[-1][1]:
                        peaks[-1] = (float(fb[k]), float(Sb[k]))
            peaks = peaks[:5]
            ratios = ([round(p[0] / peaks[0][0], 2) for p in peaks[1:]]
                      if peaks else [])
            return {"attackAt": round(pk * 0.005, 3),
                    "ringAt600": round(ring, 3), "ratios": ratios}

        def profile(g):
            """Six-band energy shares and the roughness rate, in numpy."""
            x = _np.asarray(g["win"], dtype=_np.float64)
            if x.size < 1024:
                return [0.0] * 6, 0.0
            sr2 = g["sr"]
            S = _np.abs(_np.fft.rfft(x * _np.hanning(x.size))) ** 2
            f = _np.fft.rfftfreq(x.size, 1 / sr2)
            tot = S.sum() or 1.0
            bands = [(20, 60), (60, 120), (120, 300), (300, 700),
                     (700, 1500), (1500, 20000)]
            prof = [round(100 * S[(f >= lo) & (f < hi)].sum() / tot, 1)
                    for lo, hi in bands]
            W = int(sr2 * 0.005)
            m = x.size // W
            e = _np.array([_np.sqrt((x[k*W:(k+1)*W] ** 2).mean()) for k in range(m)])
            e = e - e.mean()
            E = _np.abs(_np.fft.rfft(e * _np.hanning(e.size)))
            ef = _np.fft.rfftfreq(e.size, 0.005)
            sel = (ef > 4) & (ef < 40)
            return prof, round(float(ef[sel][int(_np.argmax(E[sel]))]), 1)

        sfx = {}
        print(f"      {'':<21}{'peak':>7}{'audible':>9}{'<120Hz':>9}"
              f"{'thru 300Hz HP':>15}{'heave':>8}")
        for name, kind, pp, secs in CASES:
            g = page.evaluate(SFX_JS, [kind, pp, secs])
            g["profile"], g["rough"] = profile(g)
            g["strike"] = strike(g)
            g.pop("win", None); g.pop("onset", None)
            sfx[name] = g
            print(f"      {name:<21}{g['peak']:>7}{g['audible']:>8}s"
                  f"{g['low120']:>9}{g['hp300']:>15}{g['heave']:>8}"
                  + (f"   THREW {g['threw']}" if g.get("threw") else ""))
        # 0.002 and not 0.01: the ordinary bow loose is DELIBERATELY the
        # quietest thing in the game -- "it sits UNDER the impacts, so a shot
        # landing still reads louder than a shot leaving" -- and renders at
        # 0.0086. A branch that throws renders exactly 0.0, so the floor only
        # has to be above nothing.
        silent = [n for n, _, _, _ in CASES if sfx[n]["peak"] < 0.002]
        check("every sound this relic makes renders to something audible — "
              "`SFX.play` swallows a TypeError and headless never calls it at "
              "all, so a missing helper ships as SILENCE and no other tool "
              "here can tell",
              not silent,
              f"{len(CASES)} sounds, quietest peak "
              f"{min(sfx[n]['peak'] for n, _, _, _ in CASES)}"
              if not silent else f"SILENT: {', '.join(silent)}")
        g = sfx["the cast"]
        # THE GROWL IS GONE (README §12) and so are the checks that scored it.
        # Four cuts of a creature voice failed, the last one while matching a
        # reference recording to 6.4 points across six bands -- which is what
        # finally said that a spectrum match is not what makes a growl a growl.
        # The cast is a machine now, and a machine is checkable in a way a
        # voice was not: you can COUNT it.
        print(f"      {'':<21}{'attack at':>11}{'ring at 0.6s':>14}"
              f"   partial ratios")
        for name, _, _, _ in CASES:
            st = sfx[name]["strike"]
            print(f"      {name:<21}{st['attackAt']:>10.3f}s"
                  f"{st['ringAt600']:>13.0%}   "
                  + " : ".join(["1.00"] + [f"{r:.2f}" for r in st["ratios"]]))
        st = sfx["the cast"]["strike"]
        check("the cast is ONE STRIKE WITH A RING — the attack lands in the "
              "first 60ms and there is still a tail six tenths of a second "
              "later, which a thud has not and a swell has not",
              st["attackAt"] <= 0.06 and st["ringAt600"] >= 0.04,
              f"peak at {st['attackAt']:.3f}s, still at "
              f"{st['ringAt600']:.0%} of it at 0.6s")
        off_int = [r for r in st["ratios"] if abs(r - round(r)) > 0.10]
        check("and the ring is INHARMONIC — struck iron, not a tuned note. "
              "Integer ratios would be a bell playing a pitch",
              len(off_int) >= 2,
              "partials at " + " : ".join(["1.00"] + [f"{r:.2f}" for r in st["ratios"]])
              + f" — {len(off_int)} of {len(st['ratios'])} are more than 0.10 "
                f"from a whole number")
        check("and it is audible on a small speaker, which four cuts of a "
              "growl were not",
              sfx["the cast"]["hp300"] >= 0.35,
              f"{sfx['the cast']['hp300']:.0%} of its level survives a 300Hz "
              f"high-pass, against {sfx['CONTROL: Crucible']['hp300']:.0%} for "
              f"Crucible")
        check("and it does not clip",
              g["peak"] < 0.95, f"peak {g['peak']}")

        # ------------------------------------------------------------ [9] --
        print("\n[9] ZERO BURDEN\n")
        others = [i for i in M["ids"] if i != RID][:8]
        b = page.evaluate(BURDEN_JS, [RID, others, seeds[:2], 40.0])
        check("`ultBal` is null in every match this relic is not in",
              b["bad"] == 0,
              f"{b['checked']} steps over {len(others)} relics, {b['bad']} "
              f"with a window open")
        check("and no shot in those matches carries `bal`, `fork` or `home`",
              b["tagged"] == 0,
              f"{b['shots']} shot-frames, {b['tagged']} tagged")
        after = json.loads(page.evaluate(ROSTER_JS))
        check("the roster object is never left mutated",
              after == before, f"{len(after)} relics identical field for field")
        assert not errors, errors[:4]

    print(f"\n{PASS}/{PASS + FAILN} checks passed"
          + (f"  ({FAILN} FAILED)" if FAILN else ""))
    return 1 if FAILN else 0


if __name__ == "__main__":
    sys.exit(main())
