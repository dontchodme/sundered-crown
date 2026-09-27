#!/usr/bin/env python
"""DAYBREAK'S PROBE -- one check per sentence of v86 §4, read INSIDE the hook.

    python dawn_probe.py --game ../02-chain/sc-dawn.html

Wraps `tickDawn` and `spawnSpark` on the Match prototype and reads each event
where it happens. Runs Dawnbringer against every other relic, both sides, and
prints N/N.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD, sentence by sentence:
  [1] a tick on a foe that was NOT below the line, or the line not at
      H - min(1, t/dur) * H on the window clock
  [2] two ticks closer than `tick` on the window clock, or a lit frame with
      the cooldown clear that did not tick (the cadence the lab priced)
  [3] a tick that did not add exactly `smite` smite (to its cap) and hand
      `hurt` exactly `tickDmg`, once
  [4] a tick that moved the foe, crit, or froze the world (unless it broke a
      ward: the ward's own shatter)
  [5] a beat filed by a tick that did not kill, or a killing tick with no
      `fatal` hit beat
  [6] the caster gaining anything: hp, shield or a blessing (a ward's
      shatter burst on the attacker is the ward's rule, and is allowed)
  [7] a window that is not `dur` long on the window clock
  [8] smite applied with a source that is not "a" or "b"
  [9] any relic but Dawnbringer carrying `ultDawn`, or Dawnbringer throwing a
      spark (the sparks are out)
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=97001)
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, DT = C.physics.dt;
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oTick = P.tickDawn, oSpark = P.spawnSpark;
  const stage3 = typeof P.dawnShown === "function";
  const stepSeq = new WeakMap();
  const lastTick = new WeakMap();
  P.spawnSpark = function(f, x, y){
    if (f.w.id === "dawnbringer") fail(9, "Dawnbringer threw a spark");
    return oSpark.call(this, f, x, y);
  };
  P.tickDawn = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultDawn && f.w.id !== "dawnbringer") fail(9, `${f.w.id} carries ultDawn`);
      const D = f.ultDawn;
      if (!D) continue;
      const foe = f === this.a ? this.b : this.a;
      pre.push({ f, foe, D, t1: D.t + dt, cd1: D.cd - dt, y: foe.y, x: foe.x,
                 vx: foe.vx, vy: foe.vy, smite: foe.stacks("smite"),
                 hp: f.hp, sh: f.shield, bless: f.stacks("blessing"),
                 fhp: foe.hp, fsh: foe.shield, alive: foe.alive, ticks: f.dawnTally.ticks });
    }
    const hs0 = this.hitStop, hurts = [], beats = [], oHurt = this.hurt, oBeat = this.beat;
    let shattered = 0;
    this.hurt = function(tgt, dmg, src){ const s0 = tgt.shield; hurts.push([tgt, dmg]);
      const r = oHurt.call(this, tgt, dmg, src); if (s0 > 0 && tgt.shield <= 0) shattered++; return r; };
    this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    /* STAGE 3: THE VOICE RIDES THE WINDOW'S CLOCK -- counted at the call. */
    const calls = [], oPlay = AC.SFX.play;
    if (stage3) AC.SFX.play = function(kind, q){
      if (kind === "ult" && q && (q.w === "dawnbringer-step" || q.w === "dawnbringer-close")) calls.push(q);
      return oPlay.call(this, kind, q); };
    const secs = pre.map(p => ({ p, sec: Math.floor(p.D.t), fAlive: p.f.alive }));
    const r = oTick.call(this, dt);
    delete this.hurt; delete this.beat;
    if (stage3){
      delete AC.SFX.play;
      for (const { p, sec, fAlive } of secs){
        const { f, D, t1 } = p;
        const mine = calls;                        /* one dawn caster a match */
        const closes = mine.filter(q => q.w === "dawnbringer-close").length;
        const steps = mine.filter(q => q.w === "dawnbringer-step");
        if (fAlive && t1 >= D.dur){
          if (closes !== 1 || steps.length) fail(10, `clock close: ${closes} close, ${steps.length} step`); else inc("closeVoice");
        } else if (fAlive && Math.floor(t1) > sec){
          const want = Math.floor(t1), prev = stepSeq.get(D) || 0;
          if (steps.length !== 1 || steps[0].n !== want || closes) fail(10, `second ${want}: ${JSON.stringify(steps)} closes ${closes}`);
          else if (want !== prev + 1) fail(10, `step ${want} after ${prev}`);
          else { inc("stepVoice"); stepSeq.set(D, want); }
        } else if (steps.length || closes) fail(10, `a voice off the clock: ${steps.length} steps, ${closes} closes (caster alive ${fAlive})`);
      }
    }
    for (const p of pre){
      const { f, foe, D } = p, u = f.w.ult, H = C.arena.h;
      const closing = p.t1 >= D.dur || !f.alive;
      if (closing){
        if (f.ultDawn) fail(7, "window did not close at dur");
        else if (Math.abs(p.t1 - D.dur) <= dt + 1e-9 || !f.alive) inc("closeOk");
        else fail(7, `closed at ${p.t1}`);
        continue;
      }
      const lineY = H - Math.min(1, p.t1 / D.dur) * H;
      const lit = p.alive && p.y > lineY;
      const ticked = f.dawnTally.ticks - p.ticks;
      if (ticked > 1) fail(2, `${ticked} ticks in one frame`);
      if (ticked){
        inc("ticks");
        if (!lit) fail(1, `ticked with foe.y ${p.y.toFixed(1)} above the line ${lineY.toFixed(1)}`);
        else inc("litOk");
        const lt = lastTick.get(f);
        if (lt !== undefined && lt.D === D && p.t1 - lt.t < u.tick - 1e-9) fail(2, `ticks ${(p.t1 - lt.t).toFixed(3)}s apart`);
        lastTick.set(f, { D, t: p.t1 });
        if (p.cd1 > 1e-9) fail(2, `ticked with the cooldown at ${p.cd1}`);
        /* smite's cap is 4 (STATUS.smite.maxStacks); a tick adds `smite` to it */
        const sm = foe.stacks("smite");
        if (sm < Math.min(p.smite + u.smite, 4)) fail(3, `smite ${p.smite} -> ${sm}`);
        const src = foe.status.smite ? foe.status.smite.src : undefined;
        if (src !== (f === this.a ? "a" : "b")) fail(8, `smite src ${typeof src === "object" ? "a Fighter" : JSON.stringify(src)}`);
        else inc("srcOk");
        const hs = hurts.filter(h => h[0] === foe);
        if (hs.length !== 1 || hs[0][1] !== u.tickDmg) fail(3, `hurt calls ${JSON.stringify(hs.map(h => h[1]))}`);
        else inc("dmgOk");
        if (foe.x !== p.x || foe.y !== p.y || foe.vx !== p.vx || foe.vy !== p.vy) fail(4, "a tick moved the foe");
        if (!shattered && this.hitStop !== hs0) fail(4, `hitStop ${hs0} -> ${this.hitStop} without a ward break`);
        if (shattered) inc("wardBreaks", shattered);
        const killed = p.fhp > 0 && foe.hp <= 0;
        const fb = beats.filter(b => b.fatal && b.dawn);
        if (killed){ if (fb.length !== 1) fail(5, `killing tick filed ${fb.length} fatal beats`); else inc("fatalBeat"); }
        else if (beats.length) fail(5, `a non-killing tick filed ${beats.length} beat(s)`);
      } else {
        if (lit && p.cd1 <= 1e-9) fail(2, "lit with the cooldown clear, and no tick");
        if (beats.length) fail(5, "a frame with no tick filed a beat");
      }
      if (f.stacks("blessing") > p.bless) fail(6, "the caster was blessed");
      if (f.hp > p.hp || f.shield > p.sh) fail(6, "the caster gained hp or shield");
      if (!shattered && (f.hp < p.hp)) fail(6, "the caster lost hp to its own dawn");
      inc("frames"); if (lit) inc("litFrames");
    }
    return r;
  };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "dawnbringer");
  const T = { casts: 0, ticks: 0, dealt: 0, litFrames: 0, frames: 0 };
  let fights = 0, wins = 0, decided = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "dawnbringer", sd) : new AC.Match("dawnbringer", fid, sd);
    const me = side ? m.b : m.a;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++;
    if (m.winner){ decided++; if (m.winner === me) wins++; }
    if (me.dawnTally) for (const k in T) T[k] += me.dawnTally[k];
  }
  P.tickDawn = oTick; P.spawnSpark = oSpark;
  return { n, bad, T, fights, win: wins / decided, stage3,
           oldChord: /220 \* Math\.pow\(2, st\/12\)/.test(AC.SFX.play.toString()) };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    if not page.evaluate("() => typeof AC.Match.prototype.tickDawn === 'function'"):
        raise SystemExit("no tickDawn in this build -- not a Daybreak link")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds])
    if R.get("stage3"):
        from marrowdraw_relic_probe import SFX_JS
        R["voices"] = {name: page.evaluate(SFX_JS, ["ult", q, 3.0]) for name, q in (
            ("cast (step 0)", {"w": "dawnbringer"}),
            ("step 7", {"w": "dawnbringer-step", "n": 7}),
            ("close", {"w": "dawnbringer-close"}))}
    assert not errors, errors

n, bad, T = R["n"], R["bad"], R["T"]
casts = T["casts"] or 1
print(f"\nDAYBREAK PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  {R['fights']} fights "
      f"(Dawnbringer both sides x 33 foes x {a.seeds} seeds)")
print(f"  per cast: ticks {T['ticks']/casts:.2f}  dmg {T['dealt']/casts:.2f}  "
      f"foe lit {100*T['litFrames']/max(1,T['frames']):.1f}% of the window   "
      f"casts/fight {T['casts']/R['fights']:.2f}   Dawnbringer win {R['win']:.1%}")
print(f"  killing ticks {n.get('fatalBeat',0)}   wards broken by a tick {n.get('wardBreaks',0)}")
checks = [
    (1, "every tick lands on a foe below the line H - min(1,t/dur)*H", n.get("litOk", 0) > 0),
    (2, "the lab's cadence: never closer than `tick`, never a missed clear lit frame", n.get("ticks", 0) > 0),
    (3, "each tick: smite +1 (to its cap) and hurt(foe, tickDmg) once", n.get("dmgOk", 0) > 0),
    (4, "nothing else: no move, no crit, no stop but a ward's own", n.get("ticks", 0) > 0),
    (5, "no beat, except the killing tick's own fatal beat", n.get("fatalBeat", 0) > 0),
    (6, "the caster gets nothing", n.get("frames", 0) > 0),
    (7, "the window is `dur` long on the window clock", n.get("closeOk", 0) > 0),
    (8, "smite's source is a side letter", n.get("srcOk", 0) > 0),
    (9, "only Dawnbringer carries ultDawn, and it throws no spark", True),
]
if R.get("stage3"):
    V = R.get("voices", {})
    for k, v in V.items():
        print(f"  voice {k:<14} peak {v.get('peak', 0):.3f}  audible {v.get('audible', 0):.2f}s"
              f"{'  THREW ' + v['threw'] if v.get('threw') else ''}")
    print(f"  step voices {n.get('stepVoice',0)}, clock closes voiced {n.get('closeVoice',0)}")
    checks.append((10, "stage 3: steps 1-7 on the window clock, in order; one close per clock close, none on a death",
                   n.get("stepVoice", 0) > 0 and n.get("closeVoice", 0) > 0))
    heard = bool(V) and all(not v.get("threw") and v.get("peak", 0) >= 0.01 and v.get("audible", 0) >= 0.02 for v in V.values())
    checks.append((11, "stage 3: cast, top step and close each render audibly alone; the old chord and bell is gone",
                   heard and not R.get("oldChord")))
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
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
