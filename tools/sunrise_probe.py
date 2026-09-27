#!/usr/bin/env python
"""DAYBREAK'S CIRCLE -- one check per sentence of v99 §4, read INSIDE the hook.

    python sunrise_probe.py --game ../02-chain/sc-sunrise.html
    python sunrise_probe.py --game ... --set r=0            # the brief's control
    python sunrise_probe.py --game ... --set tickDmg=0 smite=0   # the null sun
    python sunrise_probe.py --game ... --rate --seed0 2207 --seeds 20 [--blade 11.2]

Wraps `fireUlt`, `resolveHit` and `tickSunrise` on the Match prototype and
reads each event where it happens. Runs Dawnbringer against every other relic,
both sides, and prints N/N.

`--rate` runs the LAB's fights instead -- Dawnbringer as side A against every
other relic, seeds seed0 + 11i, 160s, exactly `ult_overlay.py`'s arm SHIP loop
-- so the built relic reads against stage 0 on the same fights. `--set k=v`
overrides Dawnbringer's ult block before anything runs (the engine reads it
live); `--blade` its dmg.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD, sentence by sentence:
  [1]  a tick on a foe that was NOT inside r(t) + R of the sun's anchor, with
       r(t) = r * min(1, t / grow) on the sun's own clock
  [2]  two ticks closer than `tick`, or an inside frame with the cooldown
       clear that did not tick (the cadence the lab priced)
  [3]  a tick that did not add `smite` smite (to its cap) and hand `hurt`
       exactly `tickDmg`, once
  [4]  a tick that moved the foe or froze the world (unless it broke a ward:
       the ward's own shatter)
  [5]  a beat filed by a tick that did not kill, or a killing tick with no
       fatal `sunrise` hit beat
  [6]  the caster gaining anything from its sun: hp, shield or a blessing
  [7]  a sun that does not set at `dur` on its own clock, or outlives its
       caster
  [8]  smite applied with a source that is not "a" or "b"
  [9]  any relic but Dawnbringer carrying `ultSunrise`, or the line's state
       (`ultDawn`) on any fighter
  [10] THE BREAK: a landed blow while armed that does not put the sun at the
       blow's own hit point with t = cd = 0, one that is not followed by
       exactly one `ult` beat with `sunrise: true` at that point, a sun that
       comes up without a landed blow, or an anchor that moves while it is up
  [11] THE ARMING: a cast that does not leave the blade armed, or a re-cast
       while a sun is up that disturbs that sun
  [12] the rim's speed off the block is not 100 px/s (r / grow)
STAGE 3 (a link with `sunriseShown`), counted AT THE CALL:
  [13] a tick without exactly one gold number, one shell flash and one tick
       voice on its own frame -- or any of the three on a frame with no tick
       (a foe outside the light gets none of them: the control that fails if
       a tick leaks)
  [14] a hum strike off the arming's quarter-second clock or at the wrong
       step, any hum strike once the sun has broken, or a break without
       exactly one bell on its own frame (the hum STOPS on the break)
  [15] a sunset voice anywhere but a clock sunset with the caster alive, or a
       shimmer strike off the sun's half-second clock
  [16] a voice that does not render audibly ALONE through the shipped chain,
       or the line's step voices still in the synth
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=97001)
ap.add_argument("--set", nargs="*", default=[], help="k=v overrides on Dawnbringer's ult block")
ap.add_argument("--blade", type=float, default=None)
ap.add_argument("--rate", action="store_true", help="the lab's fights, Dawnbringer side A")
ap.add_argument("--secs", type=float, default=160.0)
ap.add_argument("--json", default=None)
a = ap.parse_args()

SET = {}
for kv in a.set:
    k, v = kv.split("=", 1)
    SET[k] = json.loads(v)

SETUP = r"""([set, blade]) => {
  const w = AC.WEAPONS.find(x => x.id === "dawnbringer");
  window.__saved = { ult: Object.assign({}, w.ult), dmg: w.dmg };
  Object.assign(w.ult, set);
  if (blade) w.dmg = blade;
  return { ult: Object.assign({}, w.ult), dmg: w.dmg };
}"""

RATE_JS = r"""([seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "dawnbringer");
  const rows = [];
  for (const fid of foes) for (const sd of seeds){
    const m = new AC.Match("dawnbringer", fid, sd);
    const me = m.a;
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    const T = me.sunriseTally || me.dawnTally || null;
    rows.push({ foe: fid, seed: sd, win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                dur: step * DT, T: T ? Object.assign({}, T) : null });
  }
  return rows;
}"""

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt, R = C.physics.ballR;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oFire = P.fireUlt, oRes = P.resolveHit, oTick = P.tickSunrise;
  const stage3 = typeof P.sunriseShown === "function", oPlay = AC.SFX.play;
  const rec = [];                      /* every SFX call, while a hook listens */
  const listen = () => { rec.length = 0; if (stage3) AC.SFX.play = function(kind, q){
    rec.push({ kind, w: q && q.w, n: q && q.n }); return oPlay.call(this, kind, q); }; };
  const unlisten = () => { if (stage3) delete AC.SFX.play; };
  const castAt = new WeakMap(), shadow = new WeakMap(), lastTick = new WeakMap();
  const waits = [], hitOff = [];
  P.fireUlt = function(f, foe){
    const sr = f.w.ult.kind === "sunrise";
    const S0 = f.ultSunrise;
    const pre = S0 ? { up: S0.up, x: S0.x, y: S0.y, t: S0.t, cd: S0.cd } : null;
    const r = oFire.call(this, f, foe);
    if (sr){
      const S = f.ultSunrise;
      if (!S || !S.armed) fail(11, "a cast that did not arm the blade");
      else inc("armOk");
      if (pre && pre.up){
        if (!(S === S0 && S.up && S.x === pre.x && S.y === pre.y && S.t === pre.t && S.cd === pre.cd))
          fail(11, "a re-cast disturbed the sun that was up");
        else inc("reArmUp");
      }
      castAt.set(f, this.t);            /* the lab: every cast re-arms and restarts the wait */
    }
    return r;
  };
  P.resolveHit = function(self, foe, hx, hy, seg, mul, over){
    const S0 = self.ultSunrise, armed = !!(S0 && S0.armed);
    const up0 = S0 ? { up: S0.up, x: S0.x, y: S0.y } : null;
    const h0 = self.hits, beats = [], oBeat = this.beat;
    const opp = self === this.a ? this.b : this.a;
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    const bx = foe.x, by = foe.y;
    let r;
    listen();
    try { r = oRes.call(this, self, foe, hx, hy, seg, mul, over); }
    finally { delete this.beat; unlisten(); }
    if (stage3){
      const bells = rec.filter(c => c.kind === "ult" && c.w === "dawnbringer-break").length;
      const broke = armed && self.hits > h0;
      if (bells !== (broke ? 1 : 0)) fail(14, `a blow (break ${broke}) rang ${bells} bells`);
      else if (broke) inc("bellOk");
      if (rec.some(c => c.w === "dawnbringer-arm" || c.w === "dawnbringer-up" || c.w === "dawnbringer-set" || c.kind === "sunrise-tick"))
        fail(15, "a sun voice from inside a blow");
    }
    const landed = self.hits > h0;
    const sb = beats.filter(b => b.sunrise && b.kind === "ult");
    const S = self.ultSunrise;
    if (armed && landed){
      if (!(S === S0 && !S.armed && S.up && S.x === hx && S.y === hy && S.t === 0 && S.cd === 0))
        fail(10, `a landed blow while armed: armed ${S && S.armed} up ${S && S.up} at ${S && S.x},${S && S.y} vs ${hx},${hy}`);
      else inc("breaks");
      if (sb.length !== 1 || sb[0].x !== hx || sb[0].y !== hy || sb[0].side !== (self === this.a ? 0 : 1))
        fail(10, `break beats ${sb.length}`);
      else inc("breakBeat");
      if (castAt.has(self)) waits.push(this.t - castAt.get(self));
      shadow.set(self, { x: opp.x, y: opp.y });        /* the lab's anchor: the foe's centre */
      hitOff.push(Math.hypot(hx - bx, hy - by));
    } else {
      if (sb.length) fail(10, "a sunrise beat with no break");
      if (S0 && (S0.armed !== armed || (up0 && (S0.up !== up0.up || S0.x !== up0.x || S0.y !== up0.y)))
          && !(armed && landed))
        fail(10, `the sun changed on a blow that was not a break (armed ${armed}, landed ${landed})`);
    }
    return r;
  };
  P.tickSunrise = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if ("ultDawn" in f || "dawnTally" in f) fail(9, `${f.w.id} carries the line's state`);
      if (f.ultSunrise && f.w.id !== "dawnbringer") fail(9, `${f.w.id} carries ultSunrise`);
      const S = f.ultSunrise;
      if (!S) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, S, up: S.up, armed: S.armed, sx: S.x, sy: S.y,
                 t1: S.t + dt, cd1: S.cd - dt, x: foe.x, y: foe.y, vx: foe.vx, vy: foe.vy,
                 smite: foe.stacks("smite"), hp: f.hp, sh: f.shield, bless: f.stacks("blessing"),
                 fhp: foe.hp, alive: foe.alive, fAlive: f.alive,
                 ticks: f.sunriseTally.ticks });
    }
    const hs0 = this.hitStop, hurts = [], beats = [], oHurt = this.hurt, oBeat = this.beat;
    const floats = [], oFloat = this.float;
    this.float = function(x, y, text, c, size){ floats.push({ x, y, text, c, size });
      return oFloat.call(this, x, y, text, c, size); };
    const pre3 = pre.map(p => ({ w0: p.S.w, hit0: p.f.sunriseHit, t0: p.S.t }));
    listen();
    let shattered = 0;
    this.hurt = function(tgt, dmg, src){ const s0 = tgt.shield; hurts.push([tgt, dmg]);
      const r = oHurt.call(this, tgt, dmg, src); if (s0 > 0 && tgt.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    let r;
    try { r = oTick.call(this, dt); }
    finally { delete this.hurt; delete this.beat; delete this.float; unlisten(); }
    const calls = rec.slice();
    if (stage3) for (let j = 0; j < pre.length; j++){
      const p = pre[j], q = pre3[j], f = p.f, S = p.S, u = f.w.ult;
      const arms = calls.filter(c => c.kind === "ult" && c.w === "dawnbringer-arm");
      const ups = calls.filter(c => c.kind === "ult" && c.w === "dawnbringer-up");
      const sets = calls.filter(c => c.kind === "ult" && c.w === "dawnbringer-set");
      const tv = calls.filter(c => c.kind === "sunrise-tick").length;
      const gold = floats.filter(x => x.c === "#FFD98A" && x.text === u.tickDmg && x.size === 24).length;
      const ticked = f.sunriseTally.ticks - p.ticks;
      /* [13] the tick's three marks, exactly on the tick's frame */
      if (tv !== ticked || gold !== ticked) fail(13, `ticks ${ticked}: voices ${tv}, numbers ${gold}`);
      else if (ticked) inc("marksOk");
      const now = this.t + (this.deathAge || 0);
      if (ticked && f.sunriseHit !== now) fail(13, "a tick with no shell flash");
      if (!ticked && f.sunriseHit !== q.hit0) fail(13, "a shell flash with no tick");
      if (!ticked && p.up && p.fAlive && p.t1 < u.dur) inc("quietFrames");
      /* [14] the hum: a strike on each quarter second of ARMING, at its step */
      if (!p.fAlive){ if (arms.length || sets.length) fail(15, "a voice for a dead caster"); continue; }
      const wantArm = p.armed && Math.floor((q.w0 + dt) / 0.25) > Math.floor(q.w0 / 0.25);
      if (arms.length !== (wantArm ? 1 : 0)) fail(14, `armed ${p.armed}: ${arms.length} hum strikes`);
      else if (wantArm){
        const step = Math.min(2, Math.floor((q.w0 + dt) / 1.5));
        if (arms[0].n !== step) fail(14, `hum step ${arms[0].n}, want ${step}`); else inc("humOk");
      }
      if (!p.armed && arms.length) fail(14, "the hum after the break");
      /* [15] the sunset on a clock set only; the shimmer on its half seconds */
      const setting = p.up && p.t1 >= u.dur;
      if (sets.length !== (setting ? 1 : 0)) fail(15, `setting ${setting}: ${sets.length} sunset voices`);
      else if (setting) inc("sunsetVoice");
      const wantUp = p.up && !setting && Math.floor(p.t1 / 0.5) > Math.floor(q.t0 / 0.5);
      if (ups.length !== (wantUp ? 1 : 0)) fail(15, `${ups.length} shimmer strikes, want ${wantUp ? 1 : 0}`);
      else if (wantUp) inc("upOk");
    }
    for (const p of pre){
      const { f, foe, S } = p, u = f.w.ult;
      const ticked = f.sunriseTally.ticks - p.ticks;
      if (!p.fAlive){
        if (f.ultSunrise) fail(7, "the caster died and its sun stayed"); else inc("deathSet");
        continue;
      }
      if (!p.up){
        if (ticked) fail(1, "a tick with no sun up");
        if (f.ultSunrise !== S || !S.armed) fail(11, "an armed blade lost its sun with no blow");
        continue;
      }
      if (p.t1 >= u.dur){
        const ok = p.armed ? (f.ultSunrise === S && !S.up && S.armed) : f.ultSunrise === null;
        if (!ok) fail(7, "the sun did not set at dur");
        else if (Math.abs(p.t1 - u.dur) <= dt + 1e-9) inc("setOk");
        else fail(7, `set at ${p.t1}`);
        if (ticked) fail(1, "a tick on the setting frame");
        continue;
      }
      if (S.x !== p.sx || S.y !== p.sy) fail(10, "the anchor moved while the sun was up");
      const rad = u.r * Math.min(1, p.t1 / u.grow);
      const inside = p.alive && Math.hypot(p.x - p.sx, p.y - p.sy) < rad + R;
      const sh = shadow.get(f);
      if (sh && p.alive && Math.hypot(p.x - sh.x, p.y - sh.y) < rad + R) inc("litCentre");
      if (ticked > 1) fail(2, `${ticked} ticks in one frame`);
      if (ticked){
        inc("ticks");
        if (!inside) fail(1, `ticked with the foe ${Math.hypot(p.x - p.sx, p.y - p.sy).toFixed(1)} from the anchor, r ${rad.toFixed(1)}`);
        else inc("insideOk");
        const lt = lastTick.get(f);
        if (lt !== undefined && lt.S === S && lt.x === p.sx && lt.y === p.sy && p.t1 - lt.t < u.tick - 1e-9)
          fail(2, `ticks ${(p.t1 - lt.t).toFixed(3)}s apart`);
        lastTick.set(f, { S, x: p.sx, y: p.sy, t: p.t1 });
        if (p.cd1 > 1e-9) fail(2, `ticked with the cooldown at ${p.cd1}`);
        const cap = AC.STATUS.smite.maxStacks;
        const sm = foe.stacks("smite");
        if (sm < Math.min(p.smite + u.smite, cap)) fail(3, `smite ${p.smite} -> ${sm}`);
        if (u.smite > 0){
          const src = foe.status.smite ? foe.status.smite.src : undefined;
          if (src !== (f === this.a ? "a" : "b")) fail(8, `smite src ${typeof src === "object" ? "a Fighter" : JSON.stringify(src)}`);
          else inc("srcOk");
        }
        const hs = hurts.filter(h => h[0] === foe);
        if (hs.length !== 1 || hs[0][1] !== u.tickDmg) fail(3, `hurt calls ${JSON.stringify(hs.map(h => h[1]))}`);
        else inc("dmgOk");
        if (foe.x !== p.x || foe.y !== p.y || foe.vx !== p.vx || foe.vy !== p.vy) fail(4, "a tick moved the foe");
        if (!shattered && this.hitStop !== hs0) fail(4, `hitStop ${hs0} -> ${this.hitStop} without a ward break`);
        if (shattered) inc("wardBreaks", shattered);
        const killed = p.fhp > 0 && foe.hp <= 0;
        const fb = beats.filter(b => b.fatal && b.sunrise && b.kind === "hit");
        if (killed){ if (fb.length !== 1) fail(5, `killing tick filed ${fb.length} fatal beats`); else inc("fatalBeat"); }
        else if (beats.length) fail(5, `a non-killing tick filed ${beats.length} beat(s)`);
      } else {
        if (inside && p.cd1 <= 1e-9) fail(2, "inside with the cooldown clear, and no tick");
        if (beats.length) fail(5, "a frame with no tick filed a beat");
      }
      if (f.stacks("blessing") > p.bless) fail(6, "the caster was blessed");
      if (f.hp > p.hp || f.shield > p.sh) fail(6, "the caster gained hp or shield");
      if (!shattered && f.hp < p.hp) fail(6, "the caster lost hp to its own sun");
      inc("frames"); if (inside) inc("litFrames");
    }
    return r;
  };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "dawnbringer");
  const T = { casts: 0, breaks: 0, ticks: 0, dealt: 0, litFrames: 0, frames: 0 };
  let fights = 0, wins = 0, decided = 0;
  const perFight = [];
  try {
    for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
      const m = side ? new AC.Match(fid, "dawnbringer", sd) : new AC.Match("dawnbringer", fid, sd);
      const me = side ? m.b : m.a;
      let steps = 0;
      while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
      fights++;
      if (m.winner){ decided++; if (m.winner === me) wins++; }
      if (me.sunriseTally){
        for (const k in T) T[k] += me.sunriseTally[k];
        perFight.push(me.sunriseTally.breaks);
      } else perFight.push(0);
    }
  } finally { P.fireUlt = oFire; P.resolveHit = oRes; P.tickSunrise = oTick; }
  return { n, bad, T, fights, win: wins / decided, waits, hitOff, perFight, stage3,
           oldSteps: /dawnbringer-step/.test(AC.SFX.play.toString()),
           rimSpeed: (() => { const u = AC.WEAPONS.find(w => w.id === "dawnbringer").ult; return u.r / u.grow; })() };
}"""


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else float("nan")


with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    kind = page.evaluate("() => AC.WEAPONS.find(w => w.id === 'dawnbringer').ult.kind")
    if kind != "sunrise" and not a.rate:
        raise SystemExit(f"Dawnbringer's ultimate is {kind!r} here -- not a circle link")
    setup = page.evaluate(SETUP, [SET, a.blade])
    if a.rate:
        seeds = [a.seed0 + 11 * i for i in range(a.seeds)]
        rows = page.evaluate(RATE_JS, [seeds, a.secs])
        assert not errors, errors
        d = [r for r in rows if r["win"] >= 0]
        W = sum(r["win"] for r in d) / len(d)
        Ts = [r["T"] for r in rows if r["T"]]
        tot = {k: sum(t.get(k, 0) for t in Ts) for k in ("casts", "breaks", "ticks", "dealt", "litFrames", "frames")}
        casts = tot["casts"] or 1
        print(f"\nDAYBREAK RATE  {pathlib.Path(a.game).name}  Chromium {ver}  kind {kind}  "
              f"blade {setup['dmg']}  set {SET or '-'}")
        print(f"  {len(rows)} fights (Dawnbringer side A x {len(rows)//len(seeds)} foes x {len(seeds)} seeds, "
              f"seed0 {a.seed0}, the lab's arm-SHIP loop)")
        print(f"  WIN {W:.1%}   casts/fight {tot['casts']/len(rows):.2f}   breaks/fight "
              f"{tot['breaks']/len(rows):.2f}   ticks/cast {tot['ticks']/casts:.2f}   dmg/cast "
              f"{tot['dealt']/casts:.2f}   foe inside {100*tot['litFrames']/max(1,tot['frames']):.1f}%")
        out = dict(game=a.game, chromium=ver, set=SET, blade=setup["dmg"], seed0=a.seed0,
                   seeds=a.seeds, n=len(rows), win=W, tot=tot,
                   byFoe={f: sum(r["win"] for r in d if r["foe"] == f) / max(1, len([r for r in d if r["foe"] == f]))
                          for f in sorted({r["foe"] for r in d})})
        if a.json:
            pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        sys.exit(0)
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    if R.get("stage3"):
        from marrowdraw_relic_probe import SFX_JS
        R["voices"] = {name: page.evaluate(SFX_JS, [kind, q, 3.0]) for name, kind, q in (
            ("cast (the root)", "ult", {"w": "dawnbringer"}),
            ("hum, step 2", "ult", {"w": "dawnbringer-arm", "n": 2}),
            ("the bell", "ult", {"w": "dawnbringer-break"}),
            ("the shimmer", "ult", {"w": "dawnbringer-up"}),
            ("the sunset", "ult", {"w": "dawnbringer-set"}),
            ("the tick", "sunrise-tick", {}))}
    assert not errors, errors

n, bad, T = R["n"], R["bad"], R["T"]
casts, breaks = T["casts"] or 1, T["breaks"] or 1
waits, off = R["waits"], R["hitOff"]
print(f"\nDAYBREAK'S CIRCLE -- PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  "
      f"{R['fights']} fights (Dawnbringer both sides x {R['fights'] // (2 * a.seeds)} foes x {a.seeds} seeds)"
      + (f"   SET {SET}" if SET else ""))
print(f"  casts/fight {T['casts']/R['fights']:.2f}   suns/fight {T['breaks']/R['fights']:.2f}   "
      f"breaks/cast {T['breaks']/casts:.3f}   Dawnbringer win {R['win']:.1%}")
print(f"  per cast: ticks {T['ticks']/casts:.2f}  dmg {T['dealt']/casts:.2f}    per sun: ticks "
      f"{T['ticks']/breaks:.2f}  dmg {T['dealt']/breaks:.2f}")
lit_hp = 100 * n.get("litFrames", 0) / max(1, n.get("frames", 0))
lit_c = 100 * n.get("litCentre", 0) / max(1, n.get("frames", 0))
print(f"  foe inside the sun: {lit_hp:.1f}% anchored at the HIT POINT (built)   "
      f"{lit_c:.1f}% anchored at the foe's CENTRE (the lab's)   design: 56% (centre)")
if waits:
    print(f"  arming wait (match time, cast -> break): mean {statistics.mean(waits):.2f}s  "
          f"median {statistics.median(waits):.2f}s  p90 {pct(waits, 0.9):.2f}s  max {max(waits):.2f}s   design: ~3.0s mean")
if off:
    print(f"  hit point from the struck body's centre: median {statistics.median(off):.1f}  "
          f"p10 {pct(off, 0.1):.1f}  p90 {pct(off, 0.9):.1f}  (ballR 34)")
print(f"  killing ticks {n.get('fatalBeat', 0)}   wards broken by a tick {n.get('wardBreaks', 0)}   "
      f"re-casts while a sun was up {n.get('reArmUp', 0)}   suns set by the clock {n.get('setOk', 0)}")
checks = [
    (1, "every tick lands on a foe inside r(t) + R of the anchor", n.get("insideOk", 0) > 0),
    (2, "the lab's cadence: never closer than `tick`, never a missed clear inside frame", n.get("ticks", 0) > 0),
    (3, "each tick: smite +smite (to its cap) and hurt(foe, tickDmg) once, through hurt", n.get("dmgOk", 0) > 0),
    (4, "nothing else: no move, no stop but a ward's own", n.get("ticks", 0) > 0),
    (5, "no beat, except the killing tick's own fatal beat", n.get("fatalBeat", 0) > 0 or T["dealt"] == 0),
    (6, "the caster gets nothing", n.get("frames", 0) > 0),
    (7, "the sun sets at `dur` on its own clock, and with its caster", n.get("setOk", 0) > 0),
    (8, "smite's source is a side letter", n.get("srcOk", 0) > 0 or SET.get("smite") == 0),
    (9, "only Dawnbringer carries ultSunrise; the line's state is gone", n.get("frames", 0) > 0),
    (10, "the break: at the blow's hit point, t = cd = 0, one sunrise beat there; the anchor holds",
     n.get("breaks", 0) > 0 and n.get("breakBeat", 0) == n.get("breaks", 0)),
    (11, "the arming: every cast arms; a re-cast leaves the sun that is up alone", n.get("armOk", 0) > 0),
    (12, "the rim travels 100 px/s off the block (r / grow)", abs(R["rimSpeed"] - 100) < 1e-9 or bool(SET)),
]
if R.get("stage3"):
    V = R.get("voices", {})
    for k, v in V.items():
        print(f"  voice {k:<16} peak {v.get('peak', 0):.3f}  audible {v.get('audible', 0):.2f}s"
              f"{'  THREW ' + v['threw'] if v.get('threw') else ''}")
    print(f"  ticks with their three marks {n.get('marksOk', 0)}   quiet frames {n.get('quietFrames', 0)}   "
          f"hum strikes {n.get('humOk', 0)}   bells {n.get('bellOk', 0)}   shimmer strikes {n.get('upOk', 0)}   "
          f"clock sunsets voiced {n.get('sunsetVoice', 0)}")
    heard = bool(V) and all(not v.get("threw") and v.get("peak", 0) >= 0.01 and v.get("audible", 0) >= 0.02
                            for v in V.values())
    checks += [
        (13, "stage 3: every tick, and only a tick, has its number, its shell flash and its voice",
         n.get("marksOk", 0) > 0 and n.get("quietFrames", 0) > 0),
        (14, "stage 3: the hum on the arming's clock at its step; none after the break; one bell a break",
         n.get("humOk", 0) > 0 and n.get("bellOk", 0) > 0),
        (15, "stage 3: the sunset voice on a clock set only; the shimmer on its half seconds",
         n.get("sunsetVoice", 0) > 0 and n.get("upOk", 0) > 0),
        (16, "stage 3: every voice renders audibly alone; the line's steps are gone from the synth",
         heard and not R.get("oldSteps")),
    ]
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), [])}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    R2 = dict(R); R2.pop("waits"); R2.pop("hitOff")
    R2.update(waitMean=statistics.mean(waits) if waits else None, waitP90=pct(waits, 0.9),
              hitOffMedian=statistics.median(off) if off else None, litHitPoint=lit_hp, litCentre=lit_c)
    pathlib.Path(a.json).write_text(json.dumps(R2, indent=1))
sys.exit(0 if ok == len(checks) else 1)
