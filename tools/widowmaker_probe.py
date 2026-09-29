#!/usr/bin/env python
"""EXSANGUINATE'S PROBE (v106) -- one check per sentence of v76 §1 / §2 / §3 /
§4 / §5 / §6.3, read INSIDE the hooks.

    python widowmaker_probe.py --game ../02-chain/sc-widowmaker-drain.html
    python widowmaker_probe.py --game <a link at another blade> --blade 11

Wraps `step`, `fireUlt`, `tickStatus`, `tickDrain`, `tickCharge`,
`tickWeapon`, `bladeSegments`, `tickHits`, `resolveHit` and `resolveClank` on
the Match prototype, and puts a setter on Widowmaker's `hp`, and reads each
event where it happens. Runs Widowmaker against every other relic, both sides,
and prints N/N. The same probe gates every stage from 2 on (the drain, the
blade).

THE BUILD'S NUMBERS ARE PINNED, never read from the row under test (review 3):
the window (`dur` 8) and the charge (14) come from the builder's ULT, the
twinblade's profile (reach, width, spin, mass, blades, mode, onHit) from the
builder's SHIP_HEAD, and the blade from the shipped 11.95 or the builder's
TUNED (or --blade). A link whose row says anything else fails the check that
owns the number.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD:
  [1] "For a duration", 8 s ON THE WINDOW TICKERS' CLOCK (reading 1; the
      standing ruling: every window cadence runs on the clock that stops in a
      hit stop):
      - the row's `dur` anything but the build's 8;
      - a FROZEN step (hitStop > 0, the latch or the split, read on entry)
        that moves the window at all: another object, opened or closed, or
        its clock `t` changed;
      - a LIVE step with the window open whose clock does not move by exactly
        dt (closing it or not; the cast's own step is [6]'s and [8]'s);
      - a clock close after any number of window steps but exactly the ones
        whose dt sum first reaches 8;
      - a death that `tickDrain` sees and does not close on;
      - a window unaccounted for: every cast is a clock close, a death close,
        or a window still set when the match ends (a kill landed after
        `tickDrain` in the last step -- `step` runs no ticker after `over` --
        or the timeout); those are counted, not failed;
      - any relic but Widowmaker carrying `ultDrain`
  [2] "Every tick of Hemorrhage on the enemy heals her by the same amount": a
      hemorrhage tick on her opponent, inside her window, with both alive and
      her short of the cap by more than the tick, whose heal is not exactly d,
      where d = dps x stacks x dt x dmgTakenMul is REBUILT from the engine's
      own loop (the status keys in order, each expiry, every dps tick before
      it, the blessing, and the dmgTakenMul each tick actually read: the heal
      must pay back the tick as dealt)
  [3] "capped at `maxHp`" (v76 §2: the drain "heals `hp` by it, capped at
      `maxHp`"; §4: `min(src.maxHp, ...)`): a drain tick that would carry her
      past maxHp leaving her anywhere but exactly maxHp, or her maxHp moving
      in a status tick
  [4] outside her window nothing drains: any change to her hp in a status
      tick of her foe's with the window shut, in a shade's status tick, or on
      a tick of a fighter already dead -- and the foe's own tick changed (the
      foe's hp rebuilt exactly in every status tick, each dps tick at Sunder's
      DEFINITION, 1 + taken x stacks, not the engine's dmgTakenMul)
  [5] "Her blades are unchanged" -- THE WHOLE BLADE, in the window and out of
      it, every factor REBUILT FROM ITS DEFINITION (the shipped row as pinned,
      the act, desperation, Sunder, Entangle, the page's own segDist and
      clamp), never read back from the engine's methods:
      - the row: reach 62, width 8, spin 5.7, mass 1.1, blades [0, 0.5],
        mode "spin", onHit hemorrhage 2, no knockMul, the blade the pinned one;
      - THE TURN: every live step turns her blade once (no frozen step turns
        it): theta advances by exactly spin x spinMul x dt x spinDir, spinMul
        = max(0.15, act spin x (1 + Entangle's spin x stacks) x desperation's
        1.30 at or under 25%), or not at all while she is stunned;
      - THE SEGMENTS: every `bladeSegments` of hers is the two blades at theta
        + off x TAU, from ballR - 4 to ballR + reach x act reach;
      - THE HIT TEST AND THE COOLDOWN: every `tickHits` of hers lands exactly
        the blows the segments and the width (ballR + width / 2) give, and
        leaves each blade's cooldown at combat.hitCd or the old one less dt;
        no blow of hers lands anywhere else;
      - THE BLOW: its damage (blade x dmgMul x jitter x dmgTaken, rounded,
        crit included, from the captured draws); its onHit where the bleed
        ceiling cannot bind (+2; where it binds, the stacks are [9]'s); its
        KNOCK (combat.knock x 1.5 on a crit, away from her); the foe's HITSTUN
        (impact's stun off the damage, with its diminishing return; none on a
        kill); the STOP (impact's, x critStopMul, killStop on a kill, the ward
        shatter's 0.10 where one breaks);
      - THE CLANK: her spin reversal, stun and velocity in every bind, from
        the two rows' masses (hers 1.1) and the streak.
      A blow on a cursed foe or into Bulwarden's wall is rebuilt with the
      foe's own rule on top (curse's echo from its definition, the wall's
      bite read off the wall, and the wall's 0.05 stop): no blow is exempt.
  [6] "No damage change, no knock, no stun" at the cast, and "no new object"
      (§4): the cast changing ANY field of either fighter (every own number,
      flag and string, and every status) but her window (`ultDrain`), her
      tally (`drainTally`) and the engine's cast count (`ultsFired`) -- her
      Blessing and her lifesteal excepted, which [10] owns at every step, the
      cast's included; the cast drawing the RNG; the cast adding to any array
      of the match but the common ult beat (exactly one) and the note; a stop
      other than the common 0.08; a window that is not {t 0, the row's dur}
  [7] "the drain files none", hp and nothing else: a status tick in which she
      drained that files any beat but the engine's own fatal-tick beat (at
      most one, and only when the foe's hp crossed 0 in that tick), stops the
      world, floats a number, or gives her any status (Blessing is not used)
  [8] THE CHARGE, 14 on her live clock (the lab's 16 converted; Rick's batch
      ruling): the row's charge anything but the build's 14; a cast after any
      number of her live steps (steps on which `tickCharge` runs with her
      standing) but exactly the ones whose dt sum first reaches 14, counted
      from the match's start or her last cast; a fight ending owed a cast; a
      cast while her window is open
  [9] §6.3, "left out": the drain does NOT also lift "her own cap
      (Bloodletting's 8)" -- the hemorrhage STACK ceiling, the bleeding
      fighter's `bleedCap`. Rebuilt from its definition: her foe's ceiling is
      `STATUS.hemorrhage.maxStacks` (4) unless a Bloodletting spectre of HERS
      stands, and none can. Evidence: the foe's `bleedCap` anything else after
      any step or at any blow of hers, window open or shut; or a blow where the
      ceiling binds (stacks before + 2 > 4) leaving the foe anywhere but 4 (or
      where it was, at or above 4)
  [10] THE DRAIN IS HER ONLY HEAL. v76 §3: "Lifesteal is Triplicate's (umbral)
      and is not taken" (arm D, rejected); §4: "Blessing is NOT used (this is
      hp, not a status)". Evidence: her hp rising anywhere but inside another
      fighter's status tick (where [2]-[4] hold every change of it exactly) --
      read by a setter on her `hp`, so no route is missed: her own blows, her
      own status tick, any ticker (the one exempt write is `checkEnd`'s clamp
      of a dead loser's hp up to 0, counted); Blessing on her after any step;
      lifesteal
      (her field or her row) after any step or at any blow of hers

STAGE 6 (the design's stage 3: picture and voice), each check run only where
the link carries it -- the voices detected by the drip arm's own presence in
`AC.SFX.play.toString()`, the picture by `tickSiphon` on the Match -- so the
same probe still gates stages 2 and 5 at 10/10. Once a fight is over the probe
runs 2 s more of the verdict (the step's `over` path, the presentation clock
only) for these two checks alone; checks [1]-[10] read none of those steps.
  [11] THE VOICES fire exactly on their events and nowhere else. v76 §4:
      "cast -- a low inhale, 0.4s"; "the drain -- the bleed's own drip voice
      reversed and pitched by the foe's stack count, quiet"; the close plays
      nothing. Read through `AC.SFX.play` (a no-op headless: the call is
      recorded before its first line returns). Evidence: her cast playing
      anything but exactly one inhale (`ult`, w "widowmaker"); a drain tick
      (her foe's status tick, her window open) playing anything but exactly
      one drip (w "widowmaker-drain") when her drained total crossed a whole
      hp in it and none when it did not; a drip whose n is not the bleeding
      foe's hemorrhage stacks; either voice anywhere else -- another relic's
      cast, her own or a shade's status tick, a shut window, a blow, the
      picture, a close (by the clock OR ON A DEATH) or the verdict. Only her two
      `ult` arms are read: the ward's shatter plays its own crit HIT voice
      inside hurt(), and the drain never goes through hurt().
  [12] THE PICTURE'S HOOK WRITES NOTHING OF THE SIMULATION'S. `tickSiphon`
      (tickPresentation, the one picture call on the step path) is wrapped:
      evidence is any change across it to either fighter (every own number,
      flag and string but her `siphon*` fields, every status, the window, the
      tally, the blade cooldowns, the shared weapon row's own fields) or to
      the match (every own number, flag and string, every array's length but
      `floats`), or an RNG draw. And the picture as declared (readings 12-15):
      a "+n" float other than exactly one per whole hp her drained total
      crosses, "+" the hp crossed, filed there (the running total floated
      equals floor(drained) at the fight's end); the flush's clock not reset
      on the call that sees a cast; the thread up (`siphonFade` > 0) with the
      window shut, a fighter down or `over` set, or not reaching while the
      window is open and the foe bleeds; the thread going down without a
      snap, or a snap filed with no thread up
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
import widowmaker_build as WB

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=101001)
ap.add_argument("--blade", type=float, default=None,
                help="the blade this link must carry (default: the shipped 11.95 or the builder's TUNED)")
ap.add_argument("--json", default=None)
a = ap.parse_args()

# THE PINS: the build's numbers from the builder, the one place they live.
_m = re.search(r'blades:\[([^\]]*)\], reach:([\d.]+), width:([\d.]+), artW:[\d.]+, dmg:([\d.]+), '
               r'spin:([\d.]+), mode:"(\w+)", mass:([\d.]+),\s*onHit:\{ hemorrhage:(\d+) \}', WB.SHIP_HEAD)
assert _m, "the builder's SHIP_HEAD no longer parses"
assert "knockMul" not in WB.SHIP_HEAD and "lifesteal" not in WB.SHIP_HEAD
PIN = {"dur": WB.ULT["dur"], "charge": WB.ULT["charge"],
       "blades": [float(x) for x in _m.group(1).split(",")], "reach": float(_m.group(2)),
       "width": float(_m.group(3)), "spin": float(_m.group(5)), "mode": _m.group(6),
       "mass": float(_m.group(7)), "onHit": int(_m.group(8)),
       "bladeDmg": [a.blade] if a.blade is not None else [float(_m.group(4)), WB.TUNED["dmg"]]}

JS = r"""([seeds, PIN]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, ST = AC.STATUS;
  const critMul = C.chaos.critMul, jitK = C.chaos.dmgJitter, critCh = C.chaos.critChance, FP = Object.getPrototypeOf(new AC.Match("widowmaker", "axiom", 1).a);
  const oDTM = FP.dmgTakenMul;
  /* the constants every multiplier, ceiling and impulse is rebuilt from, read once before any fight */
  const ACTS = C.acts, DESP = C.desperation, SUNT = ST.sunder.taken, HB = ST.hemorrhage.maxStacks, ENT = ST.entangle.spin;
  const IMP = C.impact, CLK = C.clank, KNOCK = C.combat.knock, HITCD = C.combat.hitCd, RB = C.physics.ballR;
  const TAU = Math.PI * 2;
  const clampD = (v, a, b) => v < a ? a : v > b ? b : v;                 // the page's clamp, as defined
  const segDistD = (ax, ay, bx, by, px, py) => {                         // the page's segDist, as defined
    const dx = bx - ax, dy = by - ay, len2 = dx*dx + dy*dy;
    let t = len2 === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / len2;
    t = clampD(t, 0, 1);
    const cx = ax + dx * t, cy = ay + dy * t;
    return { d: Math.hypot(px - cx, py - cy), x: cx, y: cy };
  };
  const ROW = AC.WEAPONS.find(w => w.id === "widowmaker"), U = ROW.ult;
  const MASSES = {}; for (const w of AC.WEAPONS) MASSES[w.id] = w.mass;
  /* THE PINS (the builder's numbers), never the row under test */
  const DUR = PIN.dur, CHARGE = PIN.charge, SPIN = PIN.spin, REACH = PIN.reach, WIDTH = PIN.width,
        MASS = PIN.mass, BLADES = PIN.blades, ONHIT = PIN.onHit, BLADE = ROW.dmg;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  /* THE ROW AGAINST THE PINS: each number is failed by the check that owns it */
  if (U.dur !== DUR) fail(1, `the row's window is ${U.dur}, the build's ${DUR}`);
  if (U.charge !== CHARGE) fail(8, `the row's charge is ${U.charge}, the build's ${CHARGE}`);
  { const got = { reach: ROW.reach, width: ROW.width, spin: ROW.spin, mass: ROW.mass, mode: ROW.mode,
                  blades: JSON.stringify(ROW.blades), onHit: JSON.stringify(ROW.onHit), knockMul: ROW.knockMul };
    const want = { reach: REACH, width: WIDTH, spin: SPIN, mass: MASS, mode: PIN.mode,
                   blades: JSON.stringify(BLADES), onHit: JSON.stringify({ hemorrhage: ONHIT }), knockMul: undefined };
    for (const k in want) if (got[k] !== want[k]) fail(5, `the row's ${k} is ${got[k]}, the shipped twinblade's ${want[k]}`);
    if (!PIN.bladeDmg.includes(BLADE)) fail(5, `the row's blade is ${BLADE}, want ${PIN.bladeDmg.join(" or ")}`); }
  if (ROW.lifesteal) fail(10, `her row carries lifesteal ${ROW.lifesteal}`);

  const oStep = P.step, oFire = P.fireUlt, oStat = P.tickStatus, oDrain = P.tickDrain, oResolve = P.resolveHit;
  const oCharge = P.tickCharge, oWeap = P.tickWeapon, oSegs = P.bladeSegments, oHits = P.tickHits, oClank = P.resolveClank, oEnd = P.checkEnd;
  const isW = f => f && f.w && f.w.id === "widowmaker";
  const isMe = f => isW(f) && !f.shade;
  /* STAGE 6, DETECTED BY ITS OWN PRESENCE: the drip's arm in the synth [11],
     `tickSiphon` on the match [12]. A link without them runs [1]-[10] only. */
  const S6V = /widowmaker-drain/.test(AC.SFX.play.toString()), S6P = typeof P.tickSiphon === "function";
  const oPlay = AC.SFX.play, ownPlay = Object.prototype.hasOwnProperty.call(AC.SFX, "play"), oSiphon = P.tickSiphon;
  let vctx = null, vplace = "a step", vInhale = 0, vDrip = [], vOurs = 0, tail = false;
  if (S6V) AC.SFX.play = function(kind, q){
    if (kind === "ult" && q && (q.w === "widowmaker" || q.w === "widowmaker-drain")){
      vOurs++;
      if (q.w === "widowmaker"){ if (vctx === "cast") vInhale++; else fail(11, `the inhale played in ${vplace}`); }
      else if (vctx === "drain") vDrip.push(q.n);
      else fail(11, `a drip (n ${q.n}) played in ${vplace}`);
    }
    return oPlay.call(this, kind, q);
  };
  /* [12] the simulation's state, as one array in a fixed key order: both
     fighters' own numbers, flags and strings (their `siphon*` fields aside),
     statuses, window, tally, cooldowns and weapon row; the match's own
     numbers, flags and strings and every array's length (`floats` aside) */
  const simSnap = m => {
    const o = [];
    for (const f of [m.a, m.b]){
      for (const k of Object.keys(f)){
        if (k.charCodeAt(0) === 115 && k.startsWith("siphon")) continue;
        const v = f[k];
        if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
        else if (Array.isArray(v)) o.push(k, v.length);
      }
      for (const k in f.status){ const s = f.status[k]; o.push(k, s.stacks, s.t, s.src); }
      o.push(f.ultDrain ? f.ultDrain.t : "-", f.ultDrain ? f.ultDrain.dur : "-");
      const T = f.drainTally;
      if (T) o.push(T.casts, T.frames, T.foeStk, T.ticks, T.drained); else o.push("-");
      if (f.hitCd) o.push(...f.hitCd);
      for (const k of Object.keys(f.w)){ const v = f.w[k]; if (v === null || typeof v !== "object") o.push(k, v); }
    }
    for (const k of Object.keys(m)){
      if (k === "floats") continue;
      const v = m[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o.push(k, v);
      else if (Array.isArray(v)) o.push(k, v.length);
    }
    return o;
  };
  let nClock = 0; { let t = 0; while (t < DUR){ t += DT; nClock++; } }
  let nCharge = 0; { let t = 0; while (t < CHARGE){ t += DT; nCharge++; } }
  const live = new WeakMap();       // window -> tickDrain increments (the window clock)
  const mt = new WeakMap();         // window -> steps of match time
  let per = null, castStep = 0, weapN = 0, chargeLive = 0, otherTick = 0, hitLog = null, phase = "a step", inEnd = false;

  /* the twinblade's two segments, from their definition */
  const segsDef = (m, f) => {
    const reach = REACH * ACTS[m.act].reach * 1, out = [];
    for (const off of BLADES){
      const a = f.theta + off * TAU, ca = Math.cos(a), sa = Math.sin(a);
      out.push({ ax: f.x + ca * (RB - 4), ay: f.y + sa * (RB - 4), bx: f.x + ca * (RB + reach), by: f.y + sa * (RB + reach), a });
    }
    return out;
  };
  /* [10] her hp, read on every write */
  const trapHp = f => {
    let v = f.hp;
    Object.defineProperty(f, "hp", { configurable: true, enumerable: true,
      get(){ return v; },
      set(x){
        if (x > v){
          if (otherTick > 0) inc("riseInTick");
          else if (inEnd && v <= 0 && x === 0) inc("corpseClamp");     // checkEnd's `loser.hp = max(0, hp)`: a corpse, not a heal
          else fail(10, `her hp rose ${v} -> ${x} in ${phase} (her window ${f.ultDrain ? "open" : "shut"}), outside any status tick of another fighter's`);
        }
        v = x;
      } });
  };

  P.step = function(dt){
    /* THE VERDICT (stage 6 only): the steps after `over`, read by [11]-[12] alone */
    if (tail){ vplace = "the verdict (a step after `over`)"; return oStep.call(this, dt); }
    vplace = "a step";
    for (const f of [this.a, this.b]) if (f.ultDrain && !isW(f)) fail(1, `${f.w.id} carries ultDrain`);
    const W = isW(this.a) ? this.a : isW(this.b) ? this.b : null;
    if (!W) return oStep.call(this, dt);
    const foe = W === this.a ? this.b : this.a;
    /* [1] THE WINDOW TICKERS' CLOCK: the step's path, and the window and its
       clock as they stood, read on entry (step() takes the latch, the split
       and the hit stop in that order, each returning before any ticker). */
    const frozen = !this.over && (this.hitStop > 0 || !!this.latch || !!this.splitHold);
    const liveStep = !this.over && !frozen;
    const z0 = W.ultDrain, zt0 = z0 ? z0.t : null;
    if (z0 && !this.over){ inc("winSteps"); mt.set(z0, (mt.get(z0) || 0) + 1); if (frozen) inc("winFrozen"); }
    castStep = 0; weapN = 0; phase = "a step";
    const th0 = W.theta;
    const r = oStep.call(this, dt);
    if (frozen){
      /* a frozen step leaves the window exactly as it was: the same object,
         the clock not moved, nothing opened or closed */
      if (W.ultDrain !== z0 || (z0 && z0.t !== zt0))
        fail(1, `a frozen step moved the window: t ${zt0} -> ${W.ultDrain ? W.ultDrain.t : null}${W.ultDrain !== z0 ? " (opened/closed)" : ""}`);
      else if (z0) inc("winHeldFrozen");
      /* [5] and no frozen step turns her blade */
      if (weapN !== 0 || W.theta !== th0) fail(5, `her blade moved on a frozen step: ${th0} -> ${W.theta}`);
      else inc("turnFrozenOk");
    } else if (liveStep){
      if (z0 && !castStep){
        /* a live step with the window open moves its clock by exactly dt */
        if (z0.t !== zt0 + dt) fail(1, `a live step moved the window's clock by ${z0.t - zt0}, want ${dt}`);
        else if (W.ultDrain === z0) inc("winLiveAdv");
        else if (W.ultDrain === null) inc("winLiveClose");
        else fail(1, "a live step replaced an open window");
      }
      /* [5] every live step turns her blade exactly once */
      if (weapN !== 1) fail(5, `her blade turned ${weapN} times on a live step`);
    }
    /* [9] THE FOE'S BLEED CEILING, after every step: hemorrhage's own, which
       only a standing spectre of hers could raise, and she has none */
    if (foe.bleedCap !== HB) fail(9, `the foe's bleed ceiling is ${foe.bleedCap} after a step (her window ${W.ultDrain ? "open" : "shut"}), want hemorrhage's ${HB}`);
    else inc(W.ultDrain ? "ceilStepIn" : "ceilStepOut");
    /* [10] no Blessing and no lifesteal on her, after every step */
    if (W.status.blessing) fail(10, `she carries Blessing x${W.status.blessing.stacks} after a step (her window ${W.ultDrain ? "open" : "shut"})`);
    else if (W.lifesteal || W.w.lifesteal) fail(10, `she carries lifesteal ${W.lifesteal || W.w.lifesteal} after a step (her window ${W.ultDrain ? "open" : "shut"})`);
    else inc(W.ultDrain ? "noBlessLsIn" : "noBlessLsOut");
    return r;
  };

  /* [10] the loser's clamp to 0 is the one write that may raise a corpse's hp */
  P.checkEnd = function(){ inEnd = true; try { return oEnd.call(this); } finally { inEnd = false; } };

  /* [8] HER LIVE CLOCK: the steps on which the charge runs with her standing */
  P.tickCharge = function(f, foe, dt){
    if (isMe(f) && f.hp > 0 && !this.over) chargeLive++;
    return oCharge.call(this, f, foe, dt);
  };

  /* [6] every own number, flag and string of a fighter, and every status */
  const snapF = (x, mine) => {
    const o = {};
    for (const k of Object.keys(x)){
      if (mine && (k === "ultDrain" || k === "drainTally" || k === "ultsFired" || k === "lifesteal")) continue;
      const v = x[k];
      if (v === null || (typeof v !== "object" && typeof v !== "function")) o[k] = v;
    }
    o["status"] = JSON.stringify(Object.entries(x.status).filter(([k]) => !(mine && k === "blessing"))
                                   .map(([k, s]) => [k, s.stacks, s.t, s.src]));
    return o;
  };
  const same = (p, q) => p === q || (Number.isNaN(p) && Number.isNaN(q));

  P.fireUlt = function(f, foe){
    if (!isW(f)){
      const vp0 = vplace; vplace = `${f.w.id}'s cast`;
      try { return oFire.call(this, f, foe); } finally { vplace = vp0; }
    }
    castStep++; if (per) per.casts++;
    if (f.ultDrain) fail(8, `a cast with the window at ${f.ultDrain.t.toFixed(3)} of ${f.ultDrain.dur}`); else inc("castOk");
    if (chargeLive !== nCharge) fail(8, `a cast after ${chargeLive} steps of her live clock, want ${nCharge} (charge ${CHARGE})`);
    else inc("cadenceOk");
    chargeLive = 0;
    const s0 = snapF(foe, false), m0 = snapF(f, true), hs0 = this.hitStop, len0 = {};
    for (const k of Object.keys(this)) if (Array.isArray(this[k])) len0[k] = this[k].length;
    let draws = 0; const oRng = this.rng;
    this.rng = () => { draws++; return oRng(); };
    const vc0 = vctx, vp0 = vplace; vctx = "cast"; vplace = "her cast"; vInhale = 0;
    let r;
    try { r = oFire.call(this, f, foe); } finally { this.rng = oRng; vctx = vc0; vplace = vp0; }
    /* [11] her cast plays exactly one inhale (a drip here failed in the synth's wrapper) */
    if (S6V){ if (vInhale !== 1) fail(11, `her cast played ${vInhale} inhales, want 1`); else inc("inhaleOk"); }
    const s1 = snapF(foe, false), m1 = snapF(f, true);
    let clean = true;
    for (const k of new Set([...Object.keys(s0), ...Object.keys(s1)]))
      if (!same(s0[k], s1[k])){ clean = false; fail(6, `the cast moved the foe's ${k}: ${s0[k]} -> ${s1[k]}`); }
    for (const k of new Set([...Object.keys(m0), ...Object.keys(m1)]))
      if (!same(m0[k], m1[k])){ clean = false; fail(6, `the cast moved her ${k}: ${m0[k]} -> ${m1[k]}`); }
    if (draws){ clean = false; fail(6, `the cast drew the RNG ${draws} times`); }
    for (const k in len0){
      const d = this[k].length - len0[k];
      if (k === "beats"){ if (d !== 1 || this.beats[this.beats.length - 1].kind !== "ult"){ clean = false; fail(6, `the cast filed ${d} beats (want the common ult beat)`); } }
      else if (k === "events") continue;          // the cast's note, the common head's
      else if (d){ clean = false; fail(6, `the cast added ${d} to ${k}`); }
    }
    if (this.hitStop !== Math.max(hs0, 0.08)){ clean = false; fail(6, `hitStop ${hs0} -> ${this.hitStop}`); }
    if (!f.ultDrain || f.ultDrain.t !== 0 || f.ultDrain.dur !== U.dur){ clean = false; fail(6, "the cast did not open {t 0, dur}"); }
    if (clean) inc("castClean");
    if (f.ultDrain) live.set(f.ultDrain, 0);
    return r;
  };

  P.tickDrain = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]) if (f.ultDrain){
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, Z: f.ultDrain, t1: f.ultDrain.t + dt, fa: f.alive, oa: foe.alive });
    }
    const vp0 = vplace, o0 = vOurs; vplace = "a close (tickDrain)";
    let r;
    try { r = oDrain.call(this, dt); } finally { vplace = vp0; }
    for (const p of pre){
      const k = (live.get(p.Z) || 0) + 1; live.set(p.Z, k);
      const clock = p.t1 >= p.Z.dur, death = !p.fa || !p.oa;
      if (clock || death){
        if (p.f.ultDrain){ fail(1, "the window did not close"); continue; }
        inc("closes"); if (per) per.closes++;
        /* [11] the close plays nothing, on the clock or on a death (a voice here failed in the synth's wrapper) */
        if (S6V && vOurs === o0) inc(death ? "closeQuietDeath" : "closeQuietClock");
        if (!death){ if (k !== nClock) fail(1, `a clock close after ${k} window steps, want ${nClock} (${DUR}s)`); else { inc("clockOk"); inc("clockMatchSteps", mt.get(p.Z) || 0); } }
        else inc("deathClose");
        if (per) per.winLen.push(k);
      } else {
        if (p.f.ultDrain !== p.Z){ fail(1, `closed at ${p.t1.toFixed(3)} of ${p.Z.dur} with both alive`); continue; }
        if (p.Z.t !== p.t1) fail(1, "the window clock is not t + dt");
        inc("winFrames");
      }
    }
    return r;
  };

  P.tickStatus = function(f, dt){
    const me = f === this.a ? this.b : f === this.b ? this.a : null;       // the drainer, if any
    const W = isW(this.a) ? this.a : isW(this.b) ? this.b : null;
    if (!W) return oStat.call(this, f, dt);
    const keys = Object.keys(f.status), snap = {};
    for (const k of keys) snap[k] = { stacks: f.status[k].stacks, t: f.status[k].t, src: f.status[k].src };
    const hasBleed = !!f.status.hemorrhage;
    const f0 = f.hp, W0 = W.hp, Wmax0 = W.maxHp, Wst0 = Object.keys(W.status).join(","), Wbless0 = W.status.blessing ? W.status.blessing.stacks : 0;
    const open = !!(me && me === W && W.ultDrain), Walive = W.hp > 0, hs0 = this.hitStop;
    const muls = [], defs = [], beats = [], floats = [], oBeat = this.beat, oFloat = this.float;
    /* each read of dmgTakenMul: the engine's value (the tick as dealt, which
       the drain must pay back) and Sunder's definition at the same instant
       (the tick as it must be: the foe's own hp is rebuilt from this one) */
    f.dmgTakenMul = function(){ const v = oDTM.call(this); muls.push(v);
      defs.push(1 + SUNT * (this.status.sunder ? this.status.sunder.stacks : 0)); return v; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    this.float = function(...x){ floats.push(x); return oFloat.apply(this, x); };
    /* [10] another fighter's tick is where her hp may rise ([2]-[4] hold it there) */
    const other = f !== W, ph0 = phase;
    if (other) otherTick++; else phase = "her own status tick";
    /* [11] a drain tick is the one place the drip may play */
    const drainCall = !!(me === W && open), vc0 = vctx, vp0 = vplace, D0 = W.drainTally ? W.drainTally.drained : 0;
    vctx = drainCall ? "drain" : null;
    vplace = drainCall ? "a drain tick" : me === W ? "her foe's status tick, her window shut" : f === W ? "her own status tick" : "a shade's status tick";
    const drips = vDrip = [];
    let r;
    try { r = oStat.call(this, f, dt); }
    finally { delete f.dmgTakenMul; delete this.beat; delete this.float; if (other) otherTick--; phase = ph0; vctx = vc0; vplace = vp0; }
    if (S6V){
      const D1 = W.drainTally ? W.drainTally.drained : 0, want = drainCall && Math.floor(D1) > Math.floor(D0) ? 1 : 0;
      if (drips.length !== want) fail(11, `a drain tick played ${drips.length} drips, want ${want} (her drained total ${D0} -> ${D1})`);
      else if (want){
        const s = snap.hemorrhage ? snap.hemorrhage.stacks : 0;
        if (drips[0] !== s) fail(11, `a drip pitched by n ${drips[0]}, the bleeding foe's hemorrhage stacks ${s}`);
        else { inc("dripOk"); inc("dripN" + s); }
      } else if (drainCall && D1 > D0) inc("dripQuietOk");
    }
    /* THE ENGINE'S LOOP, REBUILT: the keys in order, each expiry, every dps
       tick and the blessing. The foe's hp at Sunder's definition; the drain
       at the dmgTakenMul each dps tick actually read (the tick as dealt). */
    let hp = f0, hpD = f0, wh = W0, mi = 0, drains = 0, capped = 0, killBeat = false;
    for (const k of keys){
      const s = snap[k], def = ST[k];
      let t = s.t; if (!(k === "ward" && f.ultDraw)) t -= dt;
      if (t <= 0) continue;
      if (def.dps && k !== "blessing"){
        const hpD0 = hpD, d = def.dps * s.stacks * dt * muls[mi], dDef = def.dps * s.stacks * dt * defs[mi];
        mi++;
        hp -= dDef; hpD -= d;
        if (hpD0 > 0 && hpD <= 0) killBeat = true;
        if (k === "hemorrhage"){
          if (open && Walive && hpD0 > 0 && (!s.src || s.src === (W === this.a ? "a" : "b"))){
            if (wh + d > Wmax0){ capped++; wh = Wmax0; } else wh = wh + d;
            drains++;
          }
        }
      }
      if (k === "blessing"){ hp = Math.min(f.maxHp, hp + def.hps * s.stacks * dt); hpD = Math.min(f.maxHp, hpD + def.hps * s.stacks * dt); }
    }
    hp = Math.min(hp, f.maxHp);
    /* the engine's own fatal-tick beat is filed when the tick it dealt took the
       foe across 0 -- as rebuilt, or as it actually happened (a wrong tick is
       [4]'s, not a beat of the drain's) */
    if (f0 > 0 && f.hp <= 0) killBeat = true;
    if (W.maxHp !== Wmax0) fail(3, `her maxHp ${Wmax0} -> ${W.maxHp} in a status tick (the heal is capped at maxHp; nothing lifts it)`);
    if (mi !== muls.length) fail(4, `rebuilt ${mi} dps ticks, the engine read dmgTakenMul ${muls.length} times`);
    if (f.hp !== hp) fail(4, `the foe's tick: hp ${f0} -> ${f.hp}, rebuilt ${hp}`);
    else if (hasBleed) inc("footTickOk");
    if (drains){
      inc("drainTicks", drains); inc("drainCalls");
      if (capped){
        inc("cappedTicks", capped);
        if (W.hp !== Wmax0) fail(3, `a capped drain: her hp ${W0} -> ${W.hp}, maxHp ${Wmax0}`); else { inc("capOk"); inc("drained", W.hp - W0); }
      } else if (W.hp !== wh) fail(2, `drain: her hp ${W0} -> ${W.hp}, rebuilt ${wh}`); else { inc("drainOk"); inc("drained", W.hp - W0); }
      const others = beats.filter(b => !(b.fatal && b.tick && b.status));
      if (others.length) fail(7, `a drain tick filed ${others.length} beat(s)`);
      if (beats.length > 1) fail(7, `${beats.length} beats in one status tick`);
      if (beats.length && !killBeat) fail(7, "a beat with no killing tick");
      if (this.hitStop !== hs0) fail(7, `hitStop ${hs0} -> ${this.hitStop}`);
      if (floats.length) fail(7, `${floats.length} float(s) in a drain tick`);
      if (Object.keys(W.status).join(",") !== Wst0 || (W.status.blessing ? W.status.blessing.stacks : 0) !== Wbless0) fail(7, "her statuses changed in a drain tick");
      else inc("nothingElseOk");
    } else if (W !== f && W.hp !== W0){
      /* she was not drained on this call, so her hp must not move */
      fail(4, `her hp ${W0} -> ${W.hp} in ${me === W ? (open ? "an open window on a tick that owes nothing" : "a shut window") : "a shade's tick"}`);
    } else if (hasBleed && W !== f){
      if (me !== W) inc("shadeBleedOk"); else if (!open) inc("shutBleedOk"); else if (!(f0 > 0)) inc("deadBleedOk"); else inc("openNoTick");
    }
    return r;
  };

  /* [5] THE TURN: once a live step, by the twinblade's spin from its definition */
  P.tickWeapon = function(f, foe, dt){
    if (!isMe(f)) return oWeap.call(this, f, foe, dt);
    weapN++;
    const th0 = f.theta, dir = f.spinDir, stun0 = f.stun, open = !!f.ultDrain;
    const ent = f.status.entangle ? f.status.entangle.stacks : 0;
    let sm = ACTS[this.act].spin * (1 + ENT * ent);
    if (f.hp > 0 && f.hp / f.maxHp <= DESP.at) sm *= DESP.spin;
    sm = Math.max(0.15, sm);
    const spin = SPIN * sm * 1;
    const want = stun0 > 0 ? th0 : th0 + spin * dt * dir;
    const r = oWeap.call(this, f, foe, dt);
    if (f.theta !== want) fail(5, `${open ? "IN" : "out of"} the window: her blade turned ${f.theta - th0}, want ${want - th0} (spin ${SPIN} x ${sm}${stun0 > 0 ? ", stunned" : ""})`);
    else inc(stun0 > 0 ? "turnStunOk" : open ? "turnIn" : "turnOut");
    return r;
  };

  /* [5] THE SEGMENTS: every one of hers, wherever it is asked for */
  P.bladeSegments = function(f){
    const r = oSegs.call(this, f);
    if (!isMe(f)) return r;
    const e = segsDef(this, f);
    if (r.length !== e.length || r.some((s, i) => s.ax !== e[i].ax || s.ay !== e[i].ay || s.bx !== e[i].bx || s.by !== e[i].by || s.a !== e[i].a))
      fail(5, `${f.ultDrain ? "IN" : "out of"} the window: her blade segments are not the twinblade's (reach ${REACH} x act ${ACTS[this.act].reach}, blades ${BLADES})`);
    else inc(f.ultDrain ? "segIn" : "segOut");
    return r;
  };

  /* [5] THE HIT TEST AND THE COOLDOWN, rebuilt from the width and hitCd */
  P.tickHits = function(self, foe, dt, cool){
    if (!isMe(self)) return oHits.call(this, self, foe, dt, cool);
    const open = !!self.ultDrain;
    const early = (this.killFlight && self.hp <= 0) || !(self.hp > 0) || !(foe.hp > 0);
    const cd0 = BLADES.map((_, i) => self.hitCd[i]);
    const exp = { cd: [], hits: [] };
    if (!early){
      const segs = segsDef(this, self);
      for (let i = 0; i < segs.length; i++){
        let cd = Math.max(0, (cd0[i] || 0) - (cool === false ? 0 : dt));
        if (!(cd > 0 || self.stun > 0)){
          const s = segs[i], h = segDistD(s.ax, s.ay, s.bx, s.by, foe.x, foe.y);
          if (h.d < RB + WIDTH * 0.5){ cd = HITCD; exp.hits.push(s.a); }
        }
        exp.cd.push(cd);
      }
    }
    const outer = hitLog; hitLog = [];
    let r, log;
    try { r = oHits.call(this, self, foe, dt, cool); } finally { log = hitLog; hitLog = outer; }
    const got = BLADES.map((_, i) => self.hitCd[i]);
    if (early){
      if (log.length || got.some((v, i) => v !== cd0[i])) fail(5, `her tickHits struck ${log.length} or moved a cooldown with her or the foe down`);
      else inc("hitSkipOk");
    } else if (got.some((v, i) => v !== exp.cd[i])) fail(5, `${open ? "IN" : "out of"} the window: her blade cooldowns ${got}, want ${exp.cd} (hitCd ${HITCD})`);
    else if (log.length !== exp.hits.length || log.some((x, i) => x !== exp.hits[i]))
      fail(5, `${open ? "IN" : "out of"} the window: her blade landed ${log.length} blows, the hit test (reach ${REACH}, width ${WIDTH}) wants ${exp.hits.length}`);
    else inc(open ? "hitTestIn" : "hitTestOut");
    return r;
  };

  /* [5] THE CLANK: her side of every bind, from the two rows' masses */
  P.resolveClank = function(A, B, hx, hy){
    const meA = isMe(A), meB = isMe(B);
    if (!meA && !meB) return oClank.call(this, A, B, hx, hy);
    const me = meA ? A : B, open = !!me.ultDrain;
    const s0 = { dir: me.spinDir, stun: me.stun, vx: me.vx, vy: me.vy };
    const st = Math.min(CLK.maxStreak, this.clankStreak + 1);
    const knockMul = 1 + CLK.knockGrowth * st, stunMul = 1 / (1 + CLK.stunFalloff * st);
    /* the engine's clank mass is the row's times `massMul` (1 on every fighter but a Coldiron inside
       its Temper, v103 -- carried onto the batch line after this probe was written). Hers is 1. */
    if ((me.massMul ?? 1) !== 1) fail(5, `her clank mass multiplier is ${me.massMul}, not 1`);
    const mA = (meA ? MASS : MASSES[A.w.id]) * (A.massMul ?? 1), mB = (meB ? MASS : MASSES[B.w.id]) * (B.massMul ?? 1);
    const wA = Math.pow(mA, 1.7), wB = Math.pow(mB, 1.7), tot = wA + wB;
    const shareA = wB / tot, shareB = wA / tot;
    const decisive = Math.abs(shareA - shareB) > 0.16, aWins = shareA < shareB;
    /* her spin lock: none (she has no ultSpin and no ultWire) */
    const flip = meA ? (!decisive || !aWins) : (!decisive || aWins);
    const share = meA ? shareA : shareB;
    const dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy) || 1, nx = dx / d, ny = dy / d;
    const want = { dir: flip ? s0.dir * -1 : s0.dir, stun: Math.max(s0.stun, CLK.stun * share * 2 * stunMul),
                   vx: meA ? s0.vx - nx * CLK.knock * shareA * 2 * knockMul : s0.vx + nx * CLK.knock * shareB * 2 * knockMul,
                   vy: meA ? s0.vy - ny * CLK.knock * shareA * 2 * knockMul : s0.vy + ny * CLK.knock * shareB * 2 * knockMul };
    const r = oClank.call(this, A, B, hx, hy);
    const got = { dir: me.spinDir, stun: me.stun, vx: me.vx, vy: me.vy };
    const off = Object.keys(want).filter(k => got[k] !== want[k]);
    if (off.length) fail(5, `a clank ${open ? "IN" : "out of"} the window: her ${off.map(k => `${k} ${s0[k]} -> ${got[k]} (want ${want[k]})`).join(", ")}`);
    else inc(open ? "clankIn" : "clankOut");
    return r;
  };

  P.resolveHit = function(self, foe, hx, hy, seg_, mul, over){
    if (!isMe(self) || mul !== undefined) return oResolve.call(this, self, foe, hx, hy, seg_, mul, over);
    const open = !!self.ultDrain, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    if (hitLog) hitLog.push(seg_ ? seg_.a : NaN); else fail(5, "a blow of hers landed outside her tickHits");
    if (self.lifesteal || self.w.lifesteal) fail(10, `a blow of hers ${open ? "IN" : "out of"} the window carries lifesteal ${self.lifesteal || self.w.lifesteal}`);
    /* THE MULTIPLIERS FROM THEIR DEFINITIONS, never from the engine's own
       methods (a change routed through `dmgMul`, `dmgTakenMul`, `desperate`
       or `actMods` would otherwise be read back as the truth): the act's dmg,
       desperation (alive and at or under `desperation.at` of her maxHp), and
       Sunder's `taken` per stack on the foe -- the constants read once, before
       any fight. */
    const desp = self.hp > 0 && self.hp / self.maxHp <= DESP.at;
    const pre = { dm: ACTS[this.act].dmg * (desp ? DESP.dmg : 1),
                  dt: 1 + SUNT * (foe.status.sunder ? foe.status.sunder.stacks : 0),
                  /* the foe's own two damage rules, read as they stand: curse's echo
                     (its definition: the pool's sum x STATUS.curse.echo, rounded) and
                     Bulwarden's wall (what it ate, read off the wall after) */
                  echo: Math.round((foe.cursePool || []).reduce((x, v) => x + v, 0) * ST.curse.echo),
                  wall: foe.ultAegis || null, ate: foe.ultAegis ? foe.ultAegis.ate : 0,
                  bl: foe.stacks("hemorrhage"), ceil: foe.bleedCap,
                  vx: foe.vx, vy: foe.vy, kx: foe.x - self.x, ky: foe.y - self.y,
                  stun: foe.stun, sdr: foe.stunDR, hs: this.hitStop, sh: foe.shield, me: self.hp };
    const draws = [], oRng = this.rng;
    this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    /* the blow's damage exactly as handed to hurt() (after an aegis, which can
       leave a fraction): the number the engine's hitstun and stop are priced
       off. `dealt`'s difference can lose the last bit of a fraction. */
    let hurtD = null; const oHurt = this.hurt;
    this.hurt = function(t, d, s){ if (t === foe && hurtD === null) hurtD = d; return oHurt.call(this, t, d, s); };
    const ph0 = phase, vp0 = vplace; phase = "a blow of hers"; vplace = "a blow of hers";
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg_, mul, over); }
    finally { this.rng = oRng; delete this.hurt; phase = ph0; vplace = vp0; }
    if (self.hits - h0 !== 1) return r;
    if (per) { if (open) per.in++; else per.out++; }
    /* [10] her hp never rises across her own blow */
    if (self.hp > pre.me) fail(10, `her hp rose ${pre.me} -> ${self.hp} across her own blow ${open ? "IN" : "out of"} the window`);
    else inc("blowNoHeal");
    const D = self.dealt - d0, crit = draws[0] < critCh;       // the crit from its draw, not the engine's count
    if (crit !== (self.crits > c0)) fail(5, `${open ? "IN" : "out of"} the window: the crit draw ${draws[0]} says ${crit}, the engine counted ${self.crits > c0}`);
    const fatal = foe.hp <= 0, Dh = hurtD === null ? D : hurtD;
    if (hurtD === null) fail(5, `${open ? "IN" : "out of"} the window: her blow never reached hurt()`);
    const raw = BLADE * pre.dm * (1 + (draws[1] - 0.5) * jitK) * pre.dt;
    const want = Math.round(crit ? raw * critMul : raw);
    /* the blow as it reaches hurt(): the blade's own, plus the foe's curse echo, less what the foe's wall ate */
    const eaten = pre.wall ? pre.wall.ate - pre.ate : 0;
    const wantD = want + pre.echo - eaten;
    if (Math.abs(Dh - wantD) > 1e-6 || Math.abs(D - Dh) > 1e-6) fail(5, `${open ? "IN" : "out of"} the window: dealt ${D} (to hurt ${Dh}), want ${wantD} (blade ${want}${pre.echo ? `, echo +${pre.echo}` : ""}${eaten ? `, wall -${eaten}` : ""})`);
    else inc(pre.echo || eaten ? "blowFoeRuleOk" : open ? "blowInOk" : "blowOutOk");
    /* THE KNOCK: combat.knock x 1.5 on a crit (her row has no knockMul), away from her */
    const kl = Math.hypot(pre.kx, pre.ky) || 1, power = KNOCK * 1 * (crit ? 1.5 : 1) * 1;
    const wvx = pre.vx + (pre.kx / kl) * power, wvy = pre.vy + (pre.ky / kl) * power;
    if (foe.vx !== wvx || foe.vy !== wvy) fail(5, `${open ? "IN" : "out of"} the window: her blow's knock moved the foe's velocity ${foe.vx - pre.vx}, ${foe.vy - pre.vy}; want ${wvx - pre.vx}, ${wvy - pre.vy}`);
    else inc("knockOk");
    /* THE FOE'S HITSTUN: impact's, off the damage dealt, with its diminishing return; none on a kill */
    let wStun = pre.stun, wDR = pre.sdr;
    if (!fatal){
      const sraw = Math.min(IMP.stunMax, IMP.stunBase + Dh * IMP.stunPerDmg);
      wStun = Math.max(pre.stun, sraw / (1 + IMP.stunDR * pre.sdr)); wDR = pre.sdr + 1;
    }
    if (foe.stun !== wStun || foe.stunDR !== wDR) fail(5, `${open ? "IN" : "out of"} the window: her blow left the foe's stun ${foe.stun} (DR ${foe.stunDR}), want ${wStun} (DR ${wDR})`);
    else inc("stunOk");
    /* THE STOP: impact's off the damage, x critStopMul, killStop on a kill; the ward shatter's 0.10 */
    let stop = Math.min(IMP.stopMax, IMP.stopBase + Dh * IMP.stopPerDmg);
    if (crit) stop *= IMP.critStopMul;
    if (fatal) stop = IMP.killStop;
    const shattered = pre.sh > 0 && Dh > 0 && pre.sh - Math.min(pre.sh, Dh) <= 0;
    const wHs = Math.max(pre.hs, eaten > 0 ? 0.05 : -Infinity, shattered ? 0.10 : -Infinity, stop);
    if (this.hitStop !== wHs) fail(5, `${open ? "IN" : "out of"} the window: her blow's stop ${this.hitStop}, want ${wHs}`);
    else inc("stopOk");
    if (!foe.shade){
      if (pre.ceil !== HB) fail(9, `her blow ${open ? "IN" : "out of"} the window: the foe's bleed ceiling ${pre.ceil}, want hemorrhage's ${HB}`);
      const bl = foe.stacks("hemorrhage");
      if (pre.bl + ONHIT <= HB){
        /* [5] the ceiling cannot bind: exactly the row's onHit */
        if (bl !== pre.bl + ONHIT) fail(5, `onHit: hemorrhage ${pre.bl} -> ${bl}, want +${ONHIT}`); else inc("onHitOk");
      } else {
        /* [9] the ceiling binds: hemorrhage's own, which the drain does not lift */
        const wantBl = pre.bl < HB ? HB : pre.bl;
        if (bl !== wantBl) fail(9, `onHit at the ceiling ${open ? "IN" : "out of"} the window: hemorrhage ${pre.bl} -> ${bl}, want ${wantBl}`);
        else inc(open ? "ceilBindIn" : "ceilBindOut");
      }
    }
    return r;
  };

  /* [12] THE PICTURE'S HOOK: `tickSiphon`, on the presentation clock inside the step */
  if (S6P) P.tickSiphon = function(dt){
    inc("siphonCalls");
    const F = [this.a, this.b];
    const pre = F.map(f => ({ fade: f.siphonFade, snap: f.siphonSnap, hp: f.siphonHp, seen: f.siphonSeen }));
    const s0 = simSnap(this), filed = [], oFl = this.float;
    let draws = 0; const oRng = this.rng;
    this.rng = () => { draws++; return oRng(); };
    this.float = function(...x){ filed.push(x); return oFl.apply(this, x); };
    const vp0 = vplace; vplace = "the picture (tickSiphon)";
    let r;
    try { r = oSiphon.call(this, dt); } finally { this.rng = oRng; delete this.float; vplace = vp0; }
    const s1 = simSnap(this);
    let clean = s0.length === s1.length;
    if (!clean) fail(12, `the picture changed the simulation's shape: ${s0.length} -> ${s1.length} fields`);
    else for (let i = 0; i < s0.length; i++) if (!same(s0[i], s1[i])){
      clean = false;
      fail(12, `the picture wrote the simulation: ${typeof s0[i - 1] === "string" ? s0[i - 1] : "field " + i} ${s0[i]} -> ${s1[i]}${this.over ? " (after over)" : ""}`);
      break;
    }
    if (draws){ clean = false; fail(12, `the picture drew the RNG ${draws} times`); }
    if (clean) inc("siphonClean");
    const want = [];
    for (let i = 0; i < 2; i++){
      const f = F[i], foe = F[1 - i], p = pre[i], T = f.drainTally;
      if (!T){
        if (f.siphonFade !== 0 || f.siphonSnap !== null || f.siphonHp !== 0) fail(12, `${f.w.id}, who never cast, carries the thread`);
        continue;
      }
      /* the flush: its clock reset on the call that sees a cast */
      if (T.casts !== p.seen){
        if (f.siphonSeen !== T.casts || f.siphonAge !== 0) fail(12, `a cast seen (${p.seen} -> ${T.casts}) without the flush's clock at 0 (${f.siphonAge})`);
        else inc("flush");
      } else if (f.siphonSeen !== T.casts) fail(12, "the flush's cast count moved with no cast");
      /* the "+n": one per whole hp her drained total crosses, "+" the hp crossed */
      const w = Math.floor(T.drained);
      if (f.siphonHp !== w) fail(12, `floated ${f.siphonHp} whole hp, drained ${T.drained}`);
      if (w > p.hp) want.push("+" + (w - p.hp));
      /* the thread: up only in an open window with both standing and no verdict; reaching while the foe bleeds */
      const open = !!f.ultDrain && !this.over && f.alive && foe.alive;
      if (f.siphonFade > 0 && !open)
        fail(12, `the thread is up (${f.siphonFade}) with ${this.over ? "`over` set" : !f.ultDrain ? "the window shut" : "a fighter down"}`);
      else if (open && foe.stacks("hemorrhage") > 0 && !(f.siphonFade > p.fade || f.siphonFade === 1))
        fail(12, `the thread did not reach (${p.fade} -> ${f.siphonFade}) while the foe bleeds in the window`);
      else if (f.siphonFade > 0) inc("threadUp");
      /* the snap: exactly when an up thread's window stops being open */
      if (p.fade > 0 && !open){
        if (!f.siphonSnap || f.siphonSnap === p.snap || f.siphonFade !== 0) fail(12, "the thread went down without a snap");
        else inc(this.over ? "snapOver" : "snapClock");
      } else if (f.siphonSnap && f.siphonSnap !== p.snap) fail(12, "a snap filed with no thread up to snap");
    }
    const got = filed.map(x => x[2]);
    if (got.length !== want.length || got.some((x, i) => x !== want[i]))
      fail(12, `the picture floated [${got}], want [${want}] (one "+n" per whole hp drained)`);
    else inc("floatOk", got.length);
    return r;
  };

  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "widowmaker");
  const T = { casts: 0, frames: 0, foeStk: 0, ticks: 0, drained: 0 };
  let fights = 0, wins = 0, decided = 0, bin = 0, bout = 0; const lens = [];
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "widowmaker", sd) : new AC.Match("widowmaker", fid, sd);
    const me = side ? m.b : m.a;
    trapHp(me);
    per = { in: 0, out: 0, winLen: [], casts: 0, closes: 0 };
    chargeLive = 0; otherTick = 0; hitLog = null;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++; bin += per.in; bout += per.out; lens.push(...per.winLen);
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.drainTally) for (const k in T) T[k] += me.drainTally[k];
    /* [1] EVERY WINDOW ACCOUNTED FOR: a clock close, a death close, or still set at the end */
    const still = me.ultDrain ? 1 : 0;
    if (per.casts !== per.closes + still) fail(1, `${per.casts} casts, ${per.closes} closes, ${still} still open at the end`);
    else inc("acctOk");
    if (still){
      if (m.over && m.reason === "slain") inc("openAtKill");
      else if (m.over) inc("openAtTimeout");
      else inc("openAtCap");
    }
    /* [8] no cast owed at the end */
    if (chargeLive >= nCharge) fail(8, `the fight ended ${chargeLive} live steps after her last cast (a cast is due at ${nCharge})`);
    else inc("owedOk");
    /* [11]-[12] THE VERDICT: 2 s of the step's `over` path (the presentation clock only) */
    if ((S6V || S6P) && m.over){
      const o0 = vOurs;
      tail = true;
      try { for (let i = 0; i < 2 / DT; i++) m.step(DT); } finally { tail = false; }
      if (S6V && still && vOurs === o0) inc("verdictQuiet");
    }
    if (S6P){
      const Tm = me.drainTally;
      if (Tm && me.siphonHp !== Math.floor(Tm.drained)) fail(12, `the fight floated ${me.siphonHp} whole hp, she drained ${Tm.drained}`);
      else if (Tm && me.siphonSeen !== Tm.casts) fail(12, `the picture saw ${me.siphonSeen} casts of ${Tm.casts}`);
      else if (m.over && me.siphonFade !== 0) fail(12, `the thread is still up (${me.siphonFade}) after the verdict`);
      else inc("fightEndOk");
    }
  }
  P.step = oStep; P.fireUlt = oFire; P.tickStatus = oStat; P.tickDrain = oDrain; P.resolveHit = oResolve;
  P.tickCharge = oCharge; P.tickWeapon = oWeap; P.bladeSegments = oSegs; P.tickHits = oHits; P.resolveClank = oClank; P.checkEnd = oEnd;
  if (S6P) P.tickSiphon = oSiphon;
  if (S6V){ if (ownPlay) AC.SFX.play = oPlay; else delete AC.SFX.play; }
  return { n, bad, T, fights, win: wins / decided, blowsIn: bin / fights, blowsOut: bout / fights, nClock, nCharge, HB, ONHIT,
           u: { charge: U.charge, dur: U.dur, kind: U.kind }, blade: ROW.dmg, pin: PIN, s6v: S6V, s6p: S6P };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickDrain === 'function'"):
        raise SystemExit("no tickDrain in this build -- not an Exsanguinate link (stage 2+)")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, PIN])
    assert not errors, errors

n, bad, T, U = R["n"], R["bad"], R["T"], R["u"]
g = lambda k: n.get(k, 0)
casts = T["casts"] or 1
frames = max(1, T["frames"])
frozen = g("winFrozen") / max(1, g("winSteps"))
print(f"\nEXSANGUINATE PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Widowmaker both sides x every foe x {a.seeds} seeds, seed0 {a.seed0})   ult {U}  blade {R['blade']}")
print(f"  pinned from the builder: window {PIN['dur']}s, charge {PIN['charge']}, the twinblade reach {PIN['reach']:g} "
      f"width {PIN['width']:g} spin {PIN['spin']:g} mass {PIN['mass']:g} blades {PIN['blades']} onHit +{PIN['onHit']}, "
      f"blade {' or '.join(f'{x:g}' for x in PIN['bladeDmg'])}")
print(f"  casts/fight {T['casts']/R['fights']:.2f}   blows a fight: in windows {R['blowsIn']:.2f}, outside {R['blowsOut']:.2f}   "
      f"Widowmaker win {R['win']:.1%}")
print(f"  per cast: drained {T['drained']/casts:.2f} hp (the tally; hp deltas {g('drained')/casts:.2f})   "
      f"drain ticks {T['ticks']/casts:.0f}   foe stacks on a window frame {T['foeStk']/frames:.2f}   "
      f"ticks at the cap {100*g('cappedTicks')/max(1,g('drainTicks')):.1f}%")
print(f"  window: {R['nClock']} steps of the window clock ({R['nClock']/120:.3f}s); match time a window "
      f"{g('clockMatchSteps')/max(1,g('clockOk'))/120:.2f}s (a clock close)   "
      f"FREEZE CENSUS {100*frozen:.1f}% of window steps frozen")
print(f"  the window clock: held on {g('winHeldFrozen')} frozen steps, moved by dt on "
      f"{g('winLiveAdv') + g('winLiveClose')} live steps ({g('winLiveClose')} of them closing)")
print(f"  {T['casts']} windows: {g('clockOk')} closed by the clock, {g('deathClose')} on a death tickDrain saw, "
      f"{g('openAtKill')} still set at `over` (a kill after tickDrain in the last step), "
      f"{g('openAtTimeout')} at the timeout, {g('openAtCap')} at the probe's cap")
print(f"  the charge: {g('cadenceOk')} casts each exactly {R['nCharge']} steps of her live clock after the last "
      f"({R['nCharge']/120:.3f}s); {g('owedOk')} fights ended owing none")
print(f"  bleed ticks that drained nothing: {g('shutBleedOk')} window shut, {g('shadeBleedOk')} a shade's, "
      f"{g('deadBleedOk')} a dead foe's   blows on a cursed foe or Bulwarden's wall, rebuilt with their rules {g('blowFoeRuleOk')}")
print(f"  her blade: turned by the definition on {g('turnIn')} live steps in windows and {g('turnOut')} outside "
      f"({g('turnStunOk')} stunned, held); held on {g('turnFrozenOk')} frozen steps; segments rebuilt {g('segIn')} in / "
      f"{g('segOut')} out")
print(f"             hit test and cooldowns rebuilt on {g('hitTestIn')} tickHits in windows and {g('hitTestOut')} outside "
      f"({g('hitSkipOk')} skipped with one down); knock {g('knockOk')}, foe hitstun {g('stunOk')}, stop {g('stopOk')} "
      f"of her blows; clanks {g('clankIn')} in / {g('clankOut')} out")
print(f"  the foe's bleed ceiling (hemorrhage's {R['HB']}): held after {g('ceilStepIn')} steps in windows and "
      f"{g('ceilStepOut')} outside; blows where it bound {g('ceilBindIn')} in windows, "
      f"{g('ceilBindOut')} outside; onHit +{R['ONHIT']} where it could not bind {g('onHitOk')}")
print(f"  her only heal: {g('riseInTick')} hp rises, all inside another fighter's status tick; no Blessing or lifesteal "
      f"after {g('noBlessLsIn')} steps in windows and {g('noBlessLsOut')} outside; {g('blowNoHeal')} blows of hers healed nothing; "
      f"{g('corpseClamp')} of her deaths clamped to 0 by checkEnd")
checks = [
    (1, "the window is the build's 8 s on the window tickers' clock: held on every frozen step, dt on every live one; "
        "closes on a death tickDrain sees; every window accounted for; only Widowmaker carries ultDrain",
        g("clockOk") > 0 and g("deathClose") > 0 and g("winHeldFrozen") > 0
        and g("winLiveAdv") > 0 and g("winLiveClose") > 0 and g("acctOk") == R["fights"]),
    (2, "every hemorrhage tick on her live foe in the window heals her by exactly d, rebuilt from the engine's loop",
        g("drainOk") > 0 and g("drainTicks") > 0),
    (3, "capped at maxHp (§2): a tick that would carry her past it leaves her exactly at maxHp; maxHp never moves",
        g("capOk") > 0 and g("cappedTicks") > 0),
    (4, "nothing drains with the window shut, from a shade or a corpse; the foe's own tick untouched",
        g("shutBleedOk") > 0 and g("footTickOk") > 0),
    (5, "her blades unchanged, the whole blade from its definition, in the window and out: the row, the turn, "
        "the segments, the hit test and cooldown, the blow (damage, onHit +2, knock, hitstun, stop), the clank",
        all(g(k) > 0 for k in ("blowInOk", "blowOutOk", "onHitOk", "turnIn", "turnOut", "turnFrozenOk", "segIn",
                               "segOut", "hitTestIn", "hitTestOut", "knockOk", "stunOk", "stopOk", "clankIn", "clankOut"))),
    (6, "the cast moves nothing on either fighter but her window: no damage, knock, stun or status, no RNG, "
        "no new object, the common 0.08 stop and ult beat only; a window {t 0, dur}",
        g("castClean") > 0),
    (7, "a drain tick: no beat but the fatal tick's own, no stop, no float, no status on her",
        g("nothingElseOk") > 0),
    (8, "the build's charge 14 on her live clock: every cast exactly then, none owed at the end, "
        "none while her window is open",
        g("castOk") > 0 and g("cadenceOk") > 0 and g("owedOk") == R["fights"]),
    (9, "the drain lifts no cap (§6.3): the foe's bleed ceiling is hemorrhage's own 4 after every step and at every blow, "
        "and a blow at the ceiling stops there",
        g("ceilStepIn") > 0 and g("ceilStepOut") > 0 and g("ceilBindIn") > 0),
    (10, "the drain is her only heal (§3 no lifesteal, §4 no Blessing): her hp rises only in another fighter's "
         "status tick; no Blessing or lifesteal on her after any step or at any blow",
        g("riseInTick") > 0 and g("noBlessLsIn") > 0 and g("noBlessLsOut") > 0 and g("blowNoHeal") > 0),
]
if R["s6v"]:
    dn = sorted((int(k[5:]), v) for k, v in n.items() if k.startswith("dripN"))
    print(f"  stage 6 voices: {g('inhaleOk')} casts each one inhale; {g('dripOk')} drain ticks crossing a whole hp each one drip "
          f"(n = the foe's stacks: {', '.join(f'{s}: {v}' for s, v in dn)}), {g('dripQuietOk')} paying less than a whole hp none; "
          f"closes silent: {g('closeQuietClock')} by the clock, {g('closeQuietDeath')} on a death; "
          f"{g('verdictQuiet')} windows set at `over` silent through 2 s of the verdict")
    checks.append((11, "stage 6 voices: one inhale a cast, one drip per whole hp drained (n = the foe's stacks), "
                       "none anywhere else -- no voice on a close, a death or the verdict",
                   g("inhaleOk") == T["casts"] and g("inhaleOk") > 0 and g("dripOk") > 0 and g("dripQuietOk") > 0
                   and g("closeQuietClock") > 0 and g("closeQuietDeath") > 0 and g("verdictQuiet") > 0))
if R["s6p"]:
    print(f"  stage 6 picture: tickSiphon {g('siphonCalls')} calls, {g('siphonClean')} writing nothing of the simulation's "
          f"and drawing no RNG; {g('flush')} flushes for {T['casts']} casts; {g('floatOk')} \"+n\" floats; the thread up on "
          f"{g('threadUp')} calls; snaps {g('snapClock')} at a clock close, {g('snapOver')} at `over`; "
          f"{g('fightEndOk')} fights end with every whole hp floated and the thread down")
    checks.append((12, "stage 6 picture: tickSiphon writes nothing of the simulation's and draws no RNG; one \"+n\" per whole hp "
                       "drained; the flush on every cast; the thread up only in an open window, snapping at its close",
                   g("siphonCalls") > 0 and g("siphonClean") == g("siphonCalls") and g("flush") == T["casts"] > 0
                   and g("floatOk") > 0 and g("threadUp") > 0 and g("snapClock") > 0 and g("snapOver") > 0
                   and g("fightEndOk") == R["fights"]))
if not R["s6v"] and not R["s6p"]:
    print("  stage 6: not on this link (no drip arm in the synth, no tickSiphon) -- [11]-[12] not run")
ok = 0
for k, text, cover in checks:
    fails = g(f"x{k}")
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
