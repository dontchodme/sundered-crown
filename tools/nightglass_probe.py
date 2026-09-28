#!/usr/bin/env python
"""NIGHTGLASS, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v91.

    python nightglass_probe.py --game ../02-chain/sc-backlash.html [--seeds 2]
    python nightglass_probe.py --game ../02-chain/sc-backlash.html --lab [--labtag] [--set ult.charge=15]

Counts EVENTS, both sides, every foe. `--lab` is side A on the lab's seeds and
field (the 33 the row was priced against), printing the design's table;
`--labtag` gives a bolt its bounces one step late, as the lab's `fresh()` did.

STAGE 2 -- SHADEBOLT:
  [1] every bolt leaves with the spell's numbers and its two bounces
  [2] the cadence is 0.34 exactly
  [3] bounces a cast-equivalent (the brief's ~43)
  [4] blows a fight (the brief's ~37)
STAGE 3 -- BACKLASH:
  [5] EVERY blow that lands on the shrouded caster is thrown back at
      round(0.5 x what landed) -- read from OUTSIDE, by a wrapper on `hurt()`
      that measures the landing and the reflection separately
  [6] nothing is thrown back outside a window, or once either is down
  [7] a reflected blow never reflects again -- including in MIRROR matches,
      where both can be shrouded at once
  [8] the foe's curse on a window frame (the brief's ~3.0)
  [9] a reflected blow of 4+ files a hit beat (ranged:false); a fatal one always
  [10] an ult beat a cast
  [P] the render path is CALLED: bolt, shroud
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets, labTag, mirror]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const undo = [];
  for (const [path, v] of sets){ const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++) o = o[ks[i]]; const k = ks[ks.length - 1];
    if (!(k in o)) return { err: 'no field ' + path }; undo.push([o, k, o[k]]); o[k] = v; }
  const U = w.ult, live = U.charge < 1e8;
  const oSpawn = AC.Match.prototype.spawnShot;
  if (labTag) AC.Match.prototype.spawnShot = function(f, angle, quiet){
    const r = oSpawn.call(this, f, angle, quiet), s = this.shots[this.shots.length - 1];
    if (s && s.spell === 'shadebolt'){ delete s.bounce; s.untagged = true; }
    return r;
  };
  const T = { fights: 0, wins: 0, dur: 0, looses: 0, badCad: [], bolts: 0, badBolt: [], bounces: 0, blows: 0,
              blowsTaken: 0, reflected: 0, badBack: [], outside: 0, nested: 0, mirrorFights: 0, mirrorRefl: 0,
              winFrames: 0, foeStk: 0, bigBack: 0, bigBeat: 0, fatalBack: 0, fatalBeat: 0, casts: 0, ultBeats: 0, tally: 0 };
  try {
    for (const [a, b, sd, synth] of pairs){
      /* THE ENGINE REFUSES A MIRROR ("A relic cannot fight itself"), so the
         design's both-shrouded case is STAGED: in a `synth` fight the foe is
         shrouded too whenever Nightglass is, reflecting at 0.5. */
      const m = new AC.Match(a, b, sd); m.slLive = false;
      const isMirror = !!synth;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a, own = me === m.a ? 'a' : 'b';
      /* THE REFLECTION, FROM OUTSIDE: every hurt() on a shrouded fighter by the
         other side is a landing; the nested hurt() it makes (with
         `_reflecting` held) is the reflection. */
      const oHurt = m.hurt; let depth = 0, pending = null;
      /* EVERY WRAPPER PASSES ITS REST ON: stage 6 hands hurt() and shroudBack
         the point of contact, and a fixed-arity wrapper silently measures the
         old build -- here it threw, on `src.x` (CLAUDE.md, `breakSpin`). */
      m.hurt = function(v, dmg, src, ...rest){
        if (this._reflecting){
          if (depth > 1) T.nested++;
          if (pending && v !== pending.victim){ pending.back = dmg; }
          if (!(v.ultShroud || (pending && pending.victim.ultShroud))) T.outside++;
          /* what the VICTIM loses during its own reflection (the foe's ward
             shattering back at it: `shatter()` writes hp directly) is not what
             landed on it */
          const pv = pending ? pending.victim.hp + pending.victim.shield : 0;
          depth++; const r = oHurt.call(this, v, dmg, src, ...rest); depth--;
          if (pending) pending.side += pv - (pending.victim.hp + pending.victim.shield);
          return r;
        }
        const shrouded = v.ultShroud && src && src !== v;
        if (!shrouded){ depth++; const r = oHurt.call(this, v, dmg, src, ...rest); depth--; return r; }
        const p0 = v.hp + v.shield, opp = v === this.a ? this.b : this.a, o0 = opp.alive;
        const prev = pending; pending = { victim: v, back: 0, side: 0 };
        depth++; const r = oHurt.call(this, v, dmg, src, ...rest); depth--;
        const taken = p0 - (v.hp + v.shield) - pending.side, want = Math.round(taken * v.w.ult.refl);
        /* nothing is owed once either is down: the victim after the landing,
           or the foe -- which can die INSIDE the landing, when the blow empties
           the victim's ward and the shatter bursts back at it */
        const oppUp = o0 && (pending.back > 0 || opp.alive);
        const expect = ((v.hp + pending.side) > 0 && oppUp && want > 0) ? want : 0;
        if (v === me || isMirror){
          T.blowsTaken++;
          if (pending.back > 0) T.reflected++;
          if (pending.back !== expect && T.badBack.length < 5) T.badBack.push({ taken, want: expect, got: pending.back });
          if (isMirror && pending.back > 0) T.mirrorRefl++;
        }
        pending = prev;
        return r;
      };
      const oB = m.beat; m.beat = function(o){
        if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++;
        if (o && o.kind === 'hit' && o.ranged === false && this._reflecting === false && o.side === (me === this.a ? 0 : 1) && o.x === foe.x && o.y === foe.y && o.dmg !== undefined){ /* counted below */ }
        return oB.call(this, o);
      };
      /* beats filed by shroudBack: count them against its own tally */
      const oSB = m.shroudBack;
      if (oSB) m.shroudBack = function(f, taken, ...rest){
        const b0 = m.events ? 0 : 0, beats0 = T.beatsSeen || 0;
        const back = Math.round(taken * f.w.ult.refl), opp = f === this.a ? this.b : this.a;
        const willBack = back > 0 && f.alive && opp.alive;
        let filed = 0; const ob = this.beat; this.beat = function(o){ if (o && o.kind === 'hit' && o.ranged === false) filed++; return ob.call(this, o); };
        const r = oSB.call(this, f, taken, ...rest); this.beat = ob;
        if (f === me && willBack){
          if (back >= 4){ T.bigBack++; if (filed) T.bigBeat++; }
          if (opp.hp <= 0){ T.fatalBack++; if (filed) T.fatalBeat++; }
        }
        return r;
      };
      const fw = foe.w.ult, fRefl = fw ? fw.refl : undefined;
      if (isMirror && fw) fw.refl = 0.5;
      let step = 0;
      while (!m.over && step < secs / DT){
        if (isMirror){
          if (me.ultShroud && !foe.ultShroud){ foe.ultShroud = { t: 0, dur: 1e9 }; if (!foe.shroudTally) foe.shroudTally = { casts: 0, taken: 0, back: 0, count: 0 }; }
          if (!me.ultShroud && foe.ultShroud) foe.ultShroud = null;
        }
        const before = new Map(); for (const s of m.shots) if (s.own === own && s.spell === 'shadebolt') before.set(s, s.bounce);
        const fc0 = me.fireCd, f0 = me.shotsFired, W0 = me.ultShroud;
        m.step(DT); step++;
        if (labTag) for (const s of m.shots) if (s.own === own && s.untagged){ s.untagged = false; s.bounce = S.bounce; }
        if (me.ultShroud && !W0) T.casts++;
        if (me.shotsFired > f0){
          T.looses++;
          if (Math.abs((me.fireCd - fc0) - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push(me.fireCd - fc0);
        }
        for (const s of m.shots){
          if (s.own !== own || s.spell !== 'shadebolt') continue;
          if (!before.has(s)){
            T.bolts++;
            const ok = s.r === S.r && (labTag || s.bounce === S.bounce || s.bounce === S.bounce - 1) && Math.abs(s.life - (S.life - DT)) < 1e-9;
            if (!ok && T.badBolt.length < 5) T.badBolt.push({ r: s.r, bounce: s.bounce, life: s.life });
            if (!labTag && s.bounce < S.bounce) T.bounces += S.bounce - s.bounce;
          } else if (s.bounce < before.get(s)) T.bounces += before.get(s) - s.bounce;
        }
        if (me.ultShroud){ T.winFrames++; T.foeStk += foe.stacks('curse'); }
      }
      if (isMirror && fw){ if (fRefl === undefined) delete fw.refl; else fw.refl = fRefl; foe.ultShroud = null; }
      if (me.shroudTally) T.tally += me.shroudTally.casts;
      if (isMirror) T.mirrorFights++;
      else { T.fights++; T.dur += m.t; T.blows += me.hits; if (m.winner === me) T.wins++; }
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; AC.Match.prototype.spawnShot = oSpawn; }
  T.live = live;
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d'); const R = AC.renderer, saved = R.ctx;
  const seen = { bolt: 0, shroud: 0 }; let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed); const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        if (!(step % 7 === 0 || me.ultShroud)) continue;
        R.ctx = ctx; R.drawShots(m); R.drawWeapon(m, me); if (R.drawShroud) R.drawShroud(m); R.ctx = saved; frames++;
        if (m.shots.some(s => s.spell === 'shadebolt')) seen.bolt++;
        if (me.ultShroud) seen.shroud++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="nightglass")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true")
    ap.add_argument("--labtag", action="store_true", help="the lab's tagging: the bounces one step late")
    ap.add_argument("--labseed0", type=int, default=2207)
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--secs", type=float, default=200.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    sets = [(kv.split("=", 1)[0], json.loads(kv.split("=", 1)[1])) for kv in a.set]
    t0 = time.time()
    STAVES = ("ironhail", "culverin", "briarwand", "cipher", "watchlight", "crozier", "bloodwick", "nightglass")
    with game(game_path=(HERE / a.game).resolve()) as (page, errors):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = [i for i in ids if i != a.relic]
        if a.lab:
            lab_foes = [f for f in foes if f not in STAVES]
            pairs = [[a.relic, f, a.labseed0 + 11 * i] for f in lab_foes for i in range(20)]
        else:
            seeds = [a.seed0 + 13 * i for i in range(a.seeds)]
            pairs = [p for f in foes for s in seeds for p in ([a.relic, f, s], [f, a.relic, s])]
            pairs += [[a.relic, f, 9001 + 7 * i, True] for i, f in enumerate(foes[:12])]   # the staged mirror
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets, a.labtag, True])
        D = None if a.lab else page.evaluate(DRAW_JS, [a.relic, 7331, a.secs])
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]; casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F, bounce16=T["bounces"] / (T["dur"] / 16.0), blowsF=T["blows"] / F,
               stk=T["foeStk"] / T["winFrames"] if T["winFrames"] else 0, reflC=T["reflected"] / casts if casts else 0,
               takenC=T["blowsTaken"] / casts if casts else 0, dur=T["dur"] / F)
    tag = ("--lab (side A, the lab's seeds and field)" if a.lab else "every foe, both sides") + ("  --labtag" if a.labtag else "")
    print(f"NIGHTGLASS PROBE -- {a.game}   {F} fights, {tag}" + (f"   set {' '.join(a.set)}" if a.set else "") + f"   {time.time()-t0:.0f}s")
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f}   bounces {row['bounce16']:.1f} a cast-equivalent   blows {row['blowsF']:.1f} a fight   "
          f"blows taken in a window {row['takenC']:.1f} a cast, thrown back {row['reflC']:.1f}   foe curse {row['stk']:.2f}   mean {row['dur']:.1f}s")
    if a.lab:
        print("  against stage 0 on 151 (runs/build/stage0_*.txt)")
        if a.json: pathlib.Path(a.json).write_bytes(json.dumps(dict(T=T, row=row), indent=1).encode("utf-8"))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["bolts"] > 20 * F and not T["badBolt"], "[1] every bolt leaves with the spell's numbers and its two bounces",
          f"{T['bolts']} bolts" + (f"  BAD {T['badBolt']}" if T["badBolt"] else ""))
    check(not T["badCad"] and T["looses"] > 0, "[2] the cadence is exact", f"{T['looses']} looses" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(25 <= row["bounce16"] <= 70, "[3] bounces a cast-equivalent (the brief's ~43)", f"{row['bounce16']:.1f}")
    check(25 <= row["blowsF"] <= 60, "[4] blows a fight (the brief's ~37)", f"{row['blowsF']:.1f}")
    if T["live"]:
        check(T["blowsTaken"] > 0 and not T["badBack"], "[5] every blow landing on the shroud is thrown back at round(0.5 x what landed)",
              f"{T['blowsTaken']} landings, {T['reflected']} thrown back" + (f"  BAD {T['badBack']}" if T["badBack"] else ""))
        check(T["outside"] == 0, "[6] nothing is thrown back outside a window", f"{T['outside']}")
        check(T["nested"] == 0 and T["mirrorFights"] > 0 and T["mirrorRefl"] > 0, "[7] a reflected blow never reflects again, mirror matches included",
              f"{T['nested']} nested; {T['mirrorFights']} staged mirror fights (the engine refuses a real one), {T['mirrorRefl']} reflections in them")
        check(2.0 <= row["stk"] <= 3.0, "[8] the foe's curse on a window frame (the brief's ~3.0)", f"{row['stk']:.2f}")
        check(T["bigBack"] > 0 and T["bigBeat"] == T["bigBack"] and T["fatalBeat"] == T["fatalBack"],
              "[9] a reflected blow of 4+ files a hit beat; a fatal one always", f"{T['bigBeat']} of {T['bigBack']}; fatal {T['fatalBeat']} of {T['fatalBack']}")
        check(T["ultBeats"] >= T["tally"] and T["tally"] > 0, "[10] an ult beat a cast", f"{T['ultBeats']} beats for {T['tally']} casts (mirrors included)")
    check(D["threw"] is None and D["seen"]["bolt"] > 0 and (not T["live"] or D["seen"]["shroud"] > 0),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json: pathlib.Path(a.json).write_bytes(json.dumps(dict(T=T, row=row, D=D), indent=1).encode("utf-8"))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
