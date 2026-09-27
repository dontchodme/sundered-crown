#!/usr/bin/env python
"""COROLLARY'S PROBE -- one check per sentence of v80 §4, read INSIDE the hook.

    python corollary_probe.py --game ../02-chain/sc-echo.html            # stage 1
    python corollary_probe.py --game ../02-chain/sc-corollary.html --hex # stage 2

Wraps `resolveHit` and `tickEcho` on the Match prototype and reads each event
where it happens, not after the step (bloodmirror doc :429-432 -- a check that
counts frames in which an event is POSSIBLE is not counting the event). Runs
Axiom against every other relic, both sides, and prints N/N.

WHAT WOULD COUNT AS EVIDENCE AGAINST THE BUILD, sentence by sentence:
  [1] a blow landed in the window that did not queue exactly one echo, or a
      blow outside it that did
  [2] an echo whose damage is not the blow's as dealt -- or, on a crit, not
      what was dealt less EXACTLY the crit's extra, rebuilt from the blow's
      own captured draws (v80 §4 "no crit", §6.3); an off-by-one fails
  [3] an echo that resolved earlier or later than `delay` after its blow
  [4] an echo that landed out of reach, or missed in reach with both alive
  [5] an echo that dealt anything but its queued number (a crit, a sunder
      multiplier), moved the foe (a knock) or froze the world (a hit stop)
  [6] no echo ever resolving after its window closed (v80 §4: it still lands)
  [7] stage 2: hex applied != echoes landed; stage 1: any hex from an echo
  [8] any relic but Axiom ever carrying `ultEcho`
  [9] an echo queued and never resolved while the fight went on
  [10] an echo aimed at anything but the foe -- a Twinshade shade included
"""
from __future__ import annotations
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

ap = argparse.ArgumentParser()
ap.add_argument("--game", required=True)
ap.add_argument("--seeds", type=int, default=6)
ap.add_argument("--seed0", type=int, default=91001)
ap.add_argument("--hex", action="store_true", help="stage 2: the echo hexes")
ap.add_argument("--json", default=None)
a = ap.parse_args()

JS = r"""([seeds, wantHex]) => {
  const P = AC.Match.prototype, C = AC.CONFIG, R = C.physics.ballR, DT = C.physics.dt;
  const critMul = C.chaos.critMul;
  const stage4 = typeof P.echoShown === "function";
  const bad = {}, n = {};
  const fail = (k, msg) => { (bad[k] = bad[k] || []).length < 4 && bad[k].push(msg); n["x" + k] = (n["x" + k] || 0) + 1; };
  const inc = (k, v = 1) => { n[k] = (n[k] || 0) + v; };
  const oResolve = P.resolveHit, oTick = P.tickEcho;
  P.resolveHit = function(self, foe, hx, hy, seg, mul, over){
    const ax = self.w && self.w.id === "axiom";
    const E0 = ax ? self.ultEcho : null;
    const open = !!(E0 && E0.t < E0.dur);
    const q0 = E0 ? E0.q.length : 0, d0 = self.dealt, c0 = self.crits, h0 = self.hits;
    /* THE BLOW'S OWN INPUTS, captured before it is priced, so the uncritted
       blow can be rebuilt INDEPENDENTLY of the build's arithmetic: the first
       two draws `resolveHit` makes are the crit roll and the jitter. */
    let draws = [], pre = null;
    const oRng = this.rng;
    if (ax && open){
      pre = { dm: self.dmgMul(this.actMods.dmg), dt: foe.dmgTakenMul() };
      this.rng = () => { const v = oRng(); if (draws.length < 2) draws.push(v); return v; };
    }
    let r;
    try { r = oResolve.call(this, self, foe, hx, hy, seg, mul, over); }
    finally { if (pre) this.rng = oRng; }
    if (!ax) return r;
    const E1 = self.ultEcho, landed = self.hits - h0, grew = (E1 ? E1.q.length : 0) - q0;
    if (!landed) return r;
    if (open){
      inc("blowsOpen");
      if (grew !== 1) fail(1, `open window, blow landed, queue grew ${grew}`);
      else {
        /* `D` is a DIFFERENCE OF TWO RUNNING TOTALS, so it carries the float
           error of every blow before it -- and a blow is not always an
           integer (an Aegis eats a fraction of one). The build copies the
           blow's own `dmg`; the probe can only reconstruct it. So: equal to
           1e-6, and on a crit, within the rounding of D / critMul. */
        const q = E1.q[E1.q.length - 1], D = self.dealt - d0, crit = self.crits > c0;
        if (crit) inc("critBlows");
        /* WANT, rebuilt from the captured draws: raw = blade x dmgMul x jitter
           x dmgTakenMul; the uncritted blow rounds raw, the critted one rounds
           raw x critMul, and the echo is what was dealt less exactly that
           difference (never below zero). Axiom has no forge and no `mul`. */
        let want = D;
        if (crit){
          const jit = 1 + (draws[1] - 0.5) * C.chaos.dmgJitter;
          const raw = self.w.dmg * pre.dm * jit * pre.dt;
          want = Math.max(0, D - (Math.round(raw * critMul) - Math.round(raw)));
        }
        /* `D` is a difference of two running totals and carries their float
           error, and a blow is not always an integer (an Aegis eats a
           fraction of one) -- so equal to 1e-6, which an off-by-one fails. */
        if (Math.abs(q.dmg - want) > 1e-6) fail(2, `echo ${q.dmg} vs want ${want} (dealt ${D}${crit ? ", crit" : ""})`);
        else inc(crit ? "critOk" : "dmgOk");
        const opp = self === this.a ? this.b : this.a;
        if (q.tgt !== opp) fail(10, `echo aimed at ${q.tgt && q.tgt.w && q.tgt.w.id}${q.tgt === foe ? " (the struck body)" : ""}, not the foe`);
        else { inc("aimedFoe"); if (foe !== opp) inc("blowOnShade"); }
        q.__born = E1.t;
      }
    } else if (grew !== 0) fail(1, `closed window, blow queued ${grew}`);
    return r;
  };
  P.tickEcho = function(dt){
    const pre = [];
    for (const f of [this.a, this.b]){
      if (f.ultEcho && f.w.id !== "axiom") fail(8, `${f.w.id} carries ultEcho`);
      const E = f.ultEcho;
      if (!E) continue;
      pre.push({ f, E, t1: E.t + dt, q: E.q.slice(), hex0: f.echoTally.hex,
                 tv: E.q.map(q => [q.tgt, q.tgt.vx, q.tgt.vy, q.tgt.x, q.tgt.y]) });
    }
    const hs0 = this.hitStop, hurts = [], oHurt = this.hurt;
    let shattered = 0;
    /* STAGE 4: THE BEATS AN ECHO FILES, read inside the tick. */
    const beats = [], oBeat = this.beat;
    if (stage4) this.beat = function(o){ beats.push(o); return oBeat.call(this, o); };
    /* AND THE SOUNDS IT PLAYS, counted at the call -- headless, SFX.play
       returns on its first line, so a voice that is defined and never called
       is invisible to everything but a count like this one (v42). */
    const sounds = { echo: 0, snap: 0 }, oPlay = AC.SFX.play;
    if (stage4) AC.SFX.play = function(kind, p){
      if (kind === "ult" && p && p.w === "axiom-echo") sounds.echo++;
      if (kind === "hex-snap") sounds.snap++;
      return oPlay.call(this, kind, p); };
    this.hurt = function(tgt, dmg, src){
      const sh0 = tgt.shield; hurts.push([tgt, dmg]);
      const r = oHurt.call(this, tgt, dmg, src);
      if (sh0 > 0 && tgt.shield <= 0) shattered++;
      return r; };
    const r = oTick.call(this, dt);
    delete this.hurt;
    if (stage4){ delete this.beat; delete AC.SFX.play; }
    /* THE WARD'S OWN BREAK IS NOT THE ECHO'S WEIGHT. v80 §4 routes the echo
       through `hurt` -- "ward first" -- and `hurt` shatters a ward it empties,
       which bursts, knocks the ATTACKER and sets its own 0.10 hit stop. That
       is the ward's rule for every source of damage (and the lab's too: it
       called the same `m.hurt`). So a freeze here is the echo's only if no
       ward broke in this tick. */
    if (shattered) inc("wardBreaks", shattered);
    else if (this.hitStop !== hs0) fail(5, `hitStop ${hs0} -> ${this.hitStop} inside tickEcho, no ward broke`);
    for (const p of pre){
      const { f, E, t1 } = p, u = f.w.ult;
      const done = p.q.filter(q => q.at <= t1);
      let hi = 0;
      for (const q of done){
        inc("resolved");
        if (q.__born !== undefined){
          const lag = q.at - q.__born;
          if (Math.abs(lag - u.delay) > 1e-9) fail(3, `echo delay ${lag}`); else inc("delayOk");
          if (t1 - q.at > DT + 1e-9) fail(3, `echo resolved ${t1 - q.at}s late`);
        }
        if (t1 >= E.dur) inc("late");
        /* Positions do not move inside tickEcho, so the distance read now is
           the distance at the echo's turn. Hurts are matched to echoes IN
           ORDER: the next hurt call either is this echo landing, or this echo
           did not land. */
        const tgt = q.tgt, dist = Math.hypot(tgt.x - f.x, tgt.y - f.y);
        const reach = dist < u.reach + R;
        const h = hurts[hi];
        if (h && h[0] === tgt){
          hi++;
          if (h[1] !== q.dmg) fail(5, `hurt(${h[1]}) for an echo of ${q.dmg}`);
          else if (!reach) fail(4, `landed at ${dist.toFixed(1)} >= ${u.reach + R}`);
          else { inc("landed"); if (t1 >= E.dur) inc("lateLanded"); }
        } else if (!reach) inc("outOfReach");
        /* in reach and not landed is legal only if somebody is dead -- and a
           target alive NOW was alive at its turn (hp only falls in here) */
        else if (f.alive && tgt.alive) fail(4, `missed in reach at ${dist.toFixed(1)} with both alive`);
        else inc("inReachNoLand");
      }
      if (hi !== hurts.length) fail(5, `${hurts.length} hurt calls for ${hi} echoes landed`);
      if (stage4){
        /* [11] ONE `hit` BEAT PER LANDED ECHO, `fatal` IFF IT KILLED, NONE
           FOR A MISS -- v80 §4 "The echo files a hit beat", and rule 3. */
        /* [12] ONE ECHO VOICE PER LANDED ECHO, ONE SNAP PER HEX APPLIED. */
        const dh2 = f.echoTally.hex - p.hex0;
        if (sounds.echo !== hi) fail(12, `${sounds.echo} echo voices for ${hi} landed`);
        else inc("voiceOk", hi);
        if (sounds.snap !== (u.hex > 0 ? dh2 / u.hex : 0)) fail(12, `${sounds.snap} snaps for ${dh2} hex`);
        const eb = beats.filter(b => b.echo);
        if (eb.length !== hi) fail(11, `${eb.length} echo beats for ${hi} landed echoes`);
        else inc("beatOk", hi);
        for (const b of eb){
          if (b.kind !== "hit") fail(11, `echo beat of kind ${b.kind}`);
          const killed = b.hpAfter <= 0;
          if (!!b.fatal !== killed) fail(11, `fatal ${b.fatal} but hpAfter ${b.hpAfter}`);
          if (b.fatal) inc("fatalBeat");
        }
      }
      for (const [tgt, vx, vy, x, y] of p.tv)
        if (tgt.vx !== vx || tgt.vy !== vy || tgt.x !== x || tgt.y !== y) fail(5, "an echo moved its target");
      const dh = f.echoTally.hex - p.hex0;
      if (wantHex){ if (dh !== hi * u.hex) fail(7, `hex +${dh} for ${hi} landed`); else inc("hexOk", hi); }
      else if (dh !== 0 || u.hex !== 0) fail(7, `stage 1 hexed ${dh} (u.hex ${u.hex})`);
    }
    return r;
  };
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "axiom");
  const tally = { casts: 0, blows: 0, echoes: 0, landed: 0, dealt: 0, hex: 0, crits: 0 };
  let fights = 0, pendingAlive = 0, wins = 0, decided = 0;
  for (const side of [0, 1]) for (const fid of foes) for (const sd of seeds){
    const m = side ? new AC.Match(fid, "axiom", sd) : new AC.Match("axiom", fid, sd);
    const ax = side ? m.b : m.a;
    let steps = 0;
    while (!m.over && steps < 160 / DT){ m.step(DT); steps++; }
    fights++;
    if (m.winner){ decided++; if (m.winner === ax) wins++; }
    const T = ax.echoTally;
    if (T) for (const k in tally) tally[k] += T[k];
    if (ax.ultEcho && ax.ultEcho.q.length && !m.over) pendingAlive++;
  }
  P.resolveHit = oResolve; P.tickEcho = oTick;
  return { n, bad, tally, fights, pendingAlive, win: wins / decided, stage4 };
}"""

with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ver = page.evaluate("() => navigator.userAgent.match(/Chrome\\/([\\d.]+)/)[1]")
    has = page.evaluate("() => typeof AC.Match.prototype.tickEcho === 'function'")
    if not has:
        raise SystemExit("no tickEcho in this build -- not a Corollary link")
    seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
    R = page.evaluate(JS, [seeds, a.hex])
    if R.get("stage4"):
        # [13] EVERY SHIPPED VOICE, RENDERED ALONE through the shipped chain
        # (marrowdraw's SFX_JS, as vesper_relic_probe uses it). Spellbreaker's
        # cast still falls through to the shared rune-crack, so it is the
        # control that proves Axiom's arm is REACHED and is not rune-crack.
        from marrowdraw_relic_probe import SFX_JS
        R["voices"] = {name: page.evaluate(SFX_JS, [kind, p, 2.0]) for name, kind, p in (
            ("cast", "ult", {"w": "axiom"}),
            ("echo", "ult", {"w": "axiom-echo", "dmg": 11.6}),
            ("snap", "hex-snap", {}),
            ("rune-crack", "ult", {"w": "spellbreaker"}))}
    assert not errors, errors

n, bad, T = R["n"], R["bad"], R["tally"]
casts = T["casts"] or 1
print(f"\nCOROLLARY PROBE  {pathlib.Path(a.game).name}  Chromium {ver}  "
      f"{R['fights']} fights (Axiom both sides x 33 foes x {a.seeds} seeds)")
print(f"  per cast: blows {T['blows']/casts:.2f}  echoes {T['echoes']/casts:.2f}  "
      f"landed {T['landed']/casts:.2f} ({T['landed']/max(1,T['echoes']):.1%})  "
      f"echo dmg {T['dealt']/casts:.2f}  hex {T['hex']/casts:.2f}  "
      f"crit blows {T['crits']/casts:.2f}   casts/fight {T['casts']/R['fights']:.2f}")
print(f"  late echoes resolved {n.get('late',0)}, landed {n.get('lateLanded',0)}   "
      f"in reach but not landed (a dead foe) {n.get('inReachNoLand',0)}   "
      f"out of reach {n.get('outOfReach',0)}   Axiom win {R['win']:.1%}")
print(f"  blows on a shade, echoed onto the foe {n.get('blowOnShade',0)}")
print(f"  wards broken by an echo {n.get('wardBreaks',0)} (the ward's own shatter: "
      f"burst, knock on the attacker, 0.10 stop -- not the echo's weight)")

checks = [
    (1, "a blow in the window queues exactly one echo; none outside",
     n.get("blowsOpen", 0) > 0),
    (2, "echo = the blow as dealt; a crit's with critMul out",
     n.get("dmgOk", 0) > 0 and n.get("critOk", 0) > 0),
    (3, "every echo resolves `delay` after its blow",
     n.get("delayOk", 0) > 0),
    (4, "lands only inside reach + R", n.get("outOfReach", 0) > 0 and n.get("landed", 0) > 0),
    (5, "hurt(queued dmg) only -- no crit, sunder, knock or hit stop", n.get("landed", 0) > 0),
    (6, "queued echoes still land after the window closes",
     n.get("lateLanded", 0) > 0),
    (7, "stage 2: hex = echoes landed" if a.hex else "stage 1: the echo does not hex",
     (n.get("hexOk", 0) > 0) if a.hex else True),
    (8, "no relic but Axiom ever carries ultEcho", True),
    (9, "no echo left unresolved while a fight is still running",
     R["pendingAlive"] == 0),
    (10, "every echo strikes the foe, Axiom's opponent -- a blow on a shade too",
     n.get("aimedFoe", 0) > 0),
]
if R.get("stage4"):
    checks.append((11, "stage 4: one hit beat per landed echo, fatal iff it killed, none for a miss",
                   n.get("beatOk", 0) > 0 and n.get("fatalBeat", 0) > 0))
    print(f"  echo beats {n.get('beatOk',0)}, of them fatal {n.get('fatalBeat',0)}")
    checks.append((12, "stage 4: one echo voice per landed echo, one snap per hex applied",
                   n.get("voiceOk", 0) > 0))
    V = R.get("voices", {})
    for k, v in V.items():
        print(f"  voice {k:<11} peak {v.get('peak', 0):.3f}  audible {v.get('audible', 0):.2f}s"
              f"{'  THREW ' + v['threw'] if v.get('threw') else ''}")
    heard = all(not V[k].get("skip") and not V[k].get("threw") and V[k]["peak"] >= 0.01
                and V[k]["audible"] >= 0.02 for k in ("cast", "echo", "snap")) if V else False
    not_crack = bool(V) and (V["cast"]["peak"], V["cast"]["audible"]) != (V["rune-crack"]["peak"], V["rune-crack"]["audible"])
    checks.append((13, "stage 4: cast, echo and snap each render audibly ALONE; the cast is not rune-crack",
                   heard and not_crack))
ok = 0
for k, text, cover in checks:
    fails = n.get(f"x{k}", 0)
    good = fails == 0 and cover
    ok += good
    why = "" if good else (f"   {fails} FAIL: {bad.get(str(k), bad.get(k, []))}" if fails
                           else "   NOT EXERCISED -- a check that never ran is not a pass")
    print(f"  [{k}] {'PASS' if good else 'FAIL'}  {text}{why}")
print(f"\n  {ok}/{len(checks)}")
if a.json:
    pathlib.Path(a.json).write_text(json.dumps(R, indent=1))
sys.exit(0 if ok == len(checks) else 1)
