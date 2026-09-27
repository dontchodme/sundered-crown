#!/usr/bin/env python
"""WATCHLIGHT, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v92.

    python watchlight_probe.py --game ../02-chain/sc-beacon.html [--seeds 2]
    python watchlight_probe.py --game ../02-chain/sc-beacon.html --lab [--labtag] [--set ult.charge=15]

Counts EVENTS, both sides, every foe. `--lab` is side A on the lab's seeds and
field (the 33 the row was priced against), printing the design's table;
`--labtag` gives the wardbolt its shove one step late, as the lab's `fresh()`
did, which is the reproduction arm.

STAGE 2 -- WARDBOLT:
  [1] every wardbolt leaves with the spell's numbers and its shove (knock 420)
  [2] the cadence is 0.34 exactly
  [3] every landing adds `knock` along the bolt's travel -- 420 for a
      wardbolt, 150 for a lantern shot -- read off the foe's velocity on the
      write that follows `resolveHit` (an accessor on the foe)
  [4] every landing banks ward (unless the plate is full)
  [5] blows a fight, the brief's ~25
STAGE 3 -- BEACON:
  [6] the lantern is set down at the caster's centre, clamped to the inset
  [7] every lantern shot leaves the lantern aimed at the foe, with its numbers
  [8] the lantern fires every 1.2s of the window clock (a refusal delays it)
  [9] lantern shots a cast (6-7), lantern blows a window (~4.5), shield on a
      window frame (~31)
  [10] the lantern never fires outside a window or after a death
  [11] an ult beat a cast; every lantern shot carries x0, y0, t0 (the director)
  [P]  the render path is CALLED: wardbolt, lantern shot, lantern
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets, labTag, exact]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const undo = [];
  for (const [path, v] of sets){ const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++) o = o[ks[i]]; const k = ks[ks.length - 1];
    if (!(k in o)) return { err: 'no field ' + path }; undo.push([o, k, o[k]]); o[k] = v; }
  const U = w.ult, live = U.charge < 1e8;
  const oSpawn = AC.Match.prototype.spawnShot;
  if (labTag) AC.Match.prototype.spawnShot = function(f, angle, quiet){
    const r = oSpawn.call(this, f, angle, quiet), s = this.shots[this.shots.length - 1];
    if (s && s.spell === 'wardbolt'){ delete s.knock; s.untagged = true; }
    return r;
  };
  const T = { fights: 0, wins: 0, dur: 0, looses: 0, badCad: [], bolts: 0, badBolt: [], blows: 0,
              landings: 0, knockChecked: 0, badKnock: [], lampLand: 0, banked: 0, capped: 0, noBank: 0, nodmg: 0, badBank: [], reflected: 0,
              casts: 0, ultBeats: 0, badPlace: [], lampShots: 0, badLamp: [], badGap: [], outside: 0,
              noCine: 0, winFrames: 0, shield: 0, winBlows: 0, refused: 0, labCasts: 0, tally: 0 };
  try {
    for (const [a, b, sd] of pairs){
      const m = new AC.Match(a, b, sd); m.slLive = false;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a, own = me === m.a ? 'a' : 'b';
      let armed = null;
      if (exact){
        /* THE SHOVE, EXACTLY: the hit branch writes foe.vx then foe.vy the
           statement after resolveHit returns. An accessor sees the write. */
        let vx = foe.vx, vy = foe.vy;
        Object.defineProperty(foe, 'vx', { configurable: true, get(){ return vx; }, set(v){
          if (armed && armed.stage === 0){ armed.dvx = v - vx; armed.stage = 1; } vx = v; } });
        Object.defineProperty(foe, 'vy', { configurable: true, get(){ return vy; }, set(v){
          if (armed && armed.stage === 1){ armed.dvy = v - vy; armed.stage = 2;
            const kn = armed.knock, want = [armed.ux * kn, armed.uy * kn];
            T.knockChecked++;
            if ((Math.abs(armed.dvx - want[0]) > 1e-6 || Math.abs(armed.dvy - want[1]) > 1e-6) && T.badKnock.length < 5)
              T.badKnock.push({ got: [armed.dvx, armed.dvy], want });
            armed = null; }
          vy = v; } });
      }
      const oRH = m.resolveHit;
      m.resolveHit = function(self, tgt, x, y, seg, mul, over){
        const cs = this._cineShot;
        const sh0 = me.shield, fh0 = tgt.hp + tgt.shield, mh0 = me.hp;
        const r = oRH.call(this, self, tgt, x, y, seg, mul, over);
        const dealt = fh0 - (tgt.hp + tgt.shield) > 0;
        if (self === me && cs && (cs.spell === 'wardbolt' || cs.lamp)){
          T.landings++; if (cs.lamp) T.lampLand++;
          /* The engine banks dmg * 0.55 * n, capped at 90: a landing that DEALT
             nothing (a wall ate it) banks nothing, by the engine's own rule. */
          if (me.shield > sh0) T.banked++; else if (!dealt) T.nodmg++; else if (me.shield >= 89.999 || !me.alive) T.capped++;
          /* Bulwarden's wall REFLECTS: the blow comes back inside the same call and
             eats the plate just banked, then hp (6 of 6 misses, measured). */
          else if (mh0 - me.hp > 0) T.reflected++; else { T.noBank++; if (T.badBank.length < 6) T.badBank.push({ foe: tgt.w.id, foeAlive: tgt.alive, over: this.over, selfHpLost: mh0 - me.hp, shield0: sh0, dealt: fh0 - (tgt.hp + tgt.shield), shield: me.shield, lamp: !!cs.lamp, t: this.t }); }
          if (exact && cs.knock){ const l = Math.hypot(cs.vx, cs.vy) || 1; armed = { stage: 0, knock: cs.knock, ux: cs.vx / l, uy: cs.vy / l }; }
          if (!(cs.x0 !== undefined && cs.y0 !== undefined && cs.t0 !== undefined)) T.noCine++;
        }
        return r;
      };
      const oB = m.beat; m.beat = function(o){ if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++; return oB.call(this, o); };
      let step = 0, lastLampT = null;
      while (!m.over && step < secs / DT){
        const before = new Set(m.shots);
        const fc0 = me.fireCd, f0 = me.shotsFired, h0 = me.hits, B0 = me.ultBeacon, alive0 = me.alive && foe.alive;
        const lampLand0 = T.lampLand;
        m.step(DT); step++;
        armed = null;
        if (labTag) for (const s of m.shots) if (s.own === own && s.untagged){ s.untagged = false; s.knock = S.knock; }
        if (me.shotsFired > f0){
          T.looses++;
          if (Math.abs((me.fireCd - fc0) - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push(me.fireCd - fc0);
        }
        const B = me.ultBeacon;
        if (B && !B0){
          T.casts++;
          const n = m.inset, want = [Math.min(Math.max(me.x, n), A.w - n), Math.min(Math.max(me.y, n), A.h - n)];
          /* set down on the cast's step, from the centre as it stood then --
             the ball has moved one step since, so compare within a step's travel */
          if ((Math.abs(B.x - want[0]) > 12 || Math.abs(B.y - want[1]) > 12) && T.badPlace.length < 5) T.badPlace.push({ B: [B.x, B.y], me: want });
          lastLampT = null;
        }
        for (const s of m.shots){
          if (s.own !== own || before.has(s)) continue;
          if (s.spell === 'wardbolt'){
            T.bolts++;
            const ok = s.r === S.r && s.dmgMul === S.dmgMul && Math.abs(Math.hypot(s.vx, s.vy) - S.speed) < 1e-9 && (labTag || s.knock === S.knock);
            if (!ok && T.badBolt.length < 5) T.badBolt.push({ r: s.r, knock: s.knock, v: Math.hypot(s.vx, s.vy) });
          } else if (s.lamp){
            T.lampShots++;
            if (!B0 && !B) T.outside++;
            if (!alive0) T.outside++;
            const Bn = B || B0;
            const aim = Math.atan2(foe.y - s.y, foe.x - s.x);
            const ok = Bn && s.x === Bn.x && s.y === Bn.y && Math.abs(Math.hypot(s.vx, s.vy) - U.speed) < 1e-9 && s.r === U.r
                       && s.life === U.life && s.dmgMul === U.dmgMul && s.knock === U.knock && Math.abs(s.a - Math.atan2(s.vy, s.vx)) < 1e-9;
            if (!ok && T.badLamp.length < 5) T.badLamp.push({ x: s.x, y: s.y, r: s.r, life: s.life });
            if (Bn){
              if (lastLampT !== null){ const g = Bn.t - lastLampT;
                if (Math.abs(g - U.every) > DT * 1.01 && g < U.every && T.badGap.length < 5) T.badGap.push(g); }
              lastLampT = Bn.t;
            }
          }
        }
        if (B && B.t < B.dur){ T.winFrames++; T.shield += me.shield; T.winBlows += me.hits - h0; }
      }
      if (me.beaconTally){ T.refused += me.beaconTally.refused; T.tally += me.beaconTally.casts; }
      T.fights++; T.dur += m.t; T.blows += me.hits; if (m.winner === me) T.wins++;
      T.labCasts += Math.floor(step * DT / 16 + 1e-9);
      if (exact){ delete foe.vx; delete foe.vy; }
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; AC.Match.prototype.spawnShot = oSpawn; }
  T.live = live;
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d'); const R = AC.renderer, saved = R.ctx;
  const seen = { bolt: 0, lamp: 0, lantern: 0 }; let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed); const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        if (!(step % 7 === 0 || me.ultBeacon)) continue;
        R.ctx = ctx; R.drawShots(m); R.drawBeacon && R.drawBeacon(m); R.drawWeapon(m, me); R.ctx = saved; frames++;
        if (m.shots.some(s => s.spell === 'wardbolt')) seen.bolt++;
        if (m.shots.some(s => s.lamp)) seen.lamp++;
        if (me.ultBeacon) seen.lantern++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="watchlight")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true")
    ap.add_argument("--labtag", action="store_true", help="the lab's tagging: the shove arrives one step late")
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
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets, a.labtag, not a.lab])
        D = None if a.lab else page.evaluate(DRAW_JS, [a.relic, 7331, a.secs])
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]; casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F, lampC=T["lampShots"] / casts if casts else 0,
               lampBlowC=T["lampLand"] / casts if casts else 0, winBlowsF=T["winBlows"] / F,
               winBlowC=T["winBlows"] / casts if casts else 0,
               shield=T["shield"] / T["winFrames"] if T["winFrames"] else 0, blowsF=T["blows"] / F,
               outF=(T["blows"] - T["winBlows"]) / F, dur=T["dur"] / F)
    tag = ("--lab (side A, the lab's seeds and field)" if a.lab else "every foe, both sides") + ("  --labtag" if a.labtag else "")
    print(f"WATCHLIGHT PROBE -- {a.game}   {F} fights, {tag}" + (f"   set {' '.join(a.set)}" if a.set else "") + f"   {time.time()-t0:.0f}s")
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f}   hits in/out {row['winBlowsF']:.2f}/{row['outF']:.2f}   "
          f"lantern shots {row['lampC']:.2f} a cast   blows {row['winBlowC']:.2f} a window ({row['lampBlowC']:.2f} the lantern's)   shield {row['shield']:.1f} on a window frame   "
          f"blows {row['blowsF']:.1f} a fight   mean {row['dur']:.1f}s   refused {T['refused']}")
    if a.lab:
        print("  against stage 0 on 151 (runs/build/stage0_*.txt)")
        if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row), indent=1))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["bolts"] > 20 * F and not T["badBolt"], "[1] every wardbolt leaves with the spell's numbers and its shove",
          f"{T['bolts']} bolts" + (f"  BAD {T['badBolt']}" if T["badBolt"] else ""))
    check(not T["badCad"] and T["looses"] > 0, "[2] the cadence is exact", f"{T['looses']} looses" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["knockChecked"] > 0 and T["knockChecked"] >= 0.95 * T["landings"] and not T["badKnock"],
          "[3] every landing shoves `knock` along the bolt's travel (420 a wardbolt, 150 a lantern shot)",
          f"{T['knockChecked']} of {T['landings']} landings read exactly" + (f"  BAD {T['badKnock']}" if T["badKnock"] else ""))
    check(T["banked"] > 0 and T["noBank"] == 0, "[4] every landing that deals damage banks ward (unless the plate is full)",
          f"banked {T['banked']}, full {T['capped']}, dealt nothing {T['nodmg']}, reflected {T['reflected']}, missed {T['noBank']}" + (f"  BAD {T['badBank']}" if T["badBank"] else ""))
    check(20 <= row["blowsF"] <= 60, "[5] blows a fight (the brief's ~25 is the spell's; the lantern adds)", f"{row['blowsF']:.1f}")
    if T["live"]:
        check(casts > 0 and not T["badPlace"], "[6] the lantern is set down at the caster's centre, clamped",
              f"{casts} casts" + (f"  BAD {T['badPlace']}" if T["badPlace"] else ""))
        check(T["lampShots"] > 0 and not T["badLamp"], "[7] every lantern shot leaves the lantern with its numbers",
              f"{T['lampShots']}" + (f"  BAD {T['badLamp']}" if T["badLamp"] else ""))
        check(not T["badGap"], "[8] the lantern fires every 1.2s of the window clock", "ok" if not T["badGap"] else f"BAD {T['badGap']}")
        check(5.0 <= row["lampC"] <= 7.2 and 3.0 <= row["winBlowC"] <= 7.0 and 20 <= row["shield"] <= 60,
              "[9] lantern shots 6-7 a cast, blows ~4.5 a window (staff and lantern, the lab's hitsInWin), shield ~31 on a window frame",
              f"{row['lampC']:.2f}, {row['winBlowC']:.2f} ({row['lampBlowC']:.2f} the lantern's), {row['shield']:.1f}")
        check(T["outside"] == 0, "[10] the lantern never fires outside a window or after a death", f"{T['outside']}")
        check(T["ultBeats"] == T["tally"] and T["noCine"] == 0, "[11] an ult beat a cast; every lantern shot carries x0, y0, t0",
              f"{T['ultBeats']} beats for {T['tally']} casts; {T['noCine']} shots without flight data")
    check(D["threw"] is None and D["seen"]["bolt"] > 0 and (not T["live"] or (D["seen"]["lamp"] > 0 and D["seen"]["lantern"] > 0)),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row, D=D), indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
