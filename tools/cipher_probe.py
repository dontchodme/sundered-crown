#!/usr/bin/env python
"""CIPHER, ASSERTED AGAINST THE BUILD -- the brief's gates as checks. v94.

    python cipher_probe.py --game ../02-chain/sc-converge.html [--seeds 2]
    python cipher_probe.py --game ../02-chain/sc-converge.html --lab [--set ult.charge=15]

Counts EVENTS, both sides, every foe. `--lab` is side A on the lab's seeds and
field (the 33 the row was priced against), printing the design's table.

STAGE 2 -- GLYPH:
  [1] every glyph leaves with the spell's numbers and ONE bounce
  [2] the cadence is 0.34 exactly
  [3] every glyph a wall stops becomes a sigil: vx = vy = 0, life 4.0, hex 2
  [4] a sigil never moves while it is one
  [5] sigils are touched and clanked, over the run
  [6] blows a fight, the brief's ~31
STAGE 3 -- CONVERGENCE:
  [7] the sigils hanging at the cast leave in LAID order, 0.25s apart
  [8] a sigil laid in the window leaves 0.5s after it is laid
  [9] launched a cast (~5.4), blows a window (~5.7), the foe's hex on a
      window frame (~2.6)
  [10] no flown rune ever becomes a sigil again
  [11] every cast files an ult beat; the state never outlives dur + the last fuse
  [P]  the render path is CALLED: bolt, sigil, flown rune
"""
from __future__ import annotations
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

JS = r"""([rid, pairs, secs, sets, labTag]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;
  const w = AC.WEAPONS.find(x => x.id === rid), S = w.shot;
  const undo = [];
  for (const [path, v] of sets){ const ks = path.split('.'); let o = w;
    for (let i = 0; i < ks.length - 1; i++) o = o[ks[i]]; const k = ks[ks.length - 1];
    if (!(k in o)) return { err: 'no field ' + path }; undo.push([o, k, o[k]]); o[k] = v; }
  const U = w.ult, live = U.charge < 1e8;
  /* THE LAB'S TAGGING (`--labtag`): `overlays/staff_runic.js` set `bounce 1`
     from `fresh()`, AFTER the step a bolt was loosed on -- and `tickFire` runs
     before `tickShots`, so a bolt loosed INTO a wall met it untagged and died.
     Declared §5 tags at spawn, and so does the build. Untag at spawn, re-tag
     after the step, and the build is the lab again. */
  const oSpawn = AC.Match.prototype.spawnShot;
  if (labTag) AC.Match.prototype.spawnShot = function(f, angle, quiet){
    const r = oSpawn.call(this, f, angle, quiet), s = this.shots[this.shots.length - 1];
    if (s && s.glyph){ delete s.bounce; s.glyph = false; s.untagged = true; }
    return r;
  };
  const T = { fights: 0, wins: 0, dur: 0, looses: 0, badCad: [], glyphs: 0, badGlyph: [],
              sigils: 0, badSigil: [], moved: 0, sigilHits: 0, clanked: 0, blows: 0,
              casts: 0, ultBeats: 0, atCast: 0, badOrder: [], inWin: 0, badFuse: [], launched: 0,
              winBlows: 0, winFrames: 0, foeStk: 0, reformed: 0, overStay: 0, labCasts: 0, born: 0,
              tallyCasts: 0, castOnLive: 0 };
  try {
    for (const [a, b, sd] of pairs){
      const m = new AC.Match(a, b, sd); m.slLive = false;
      const me = m.a.w.id === rid ? m.a : m.b, foe = me === m.a ? m.b : m.a, own = me === m.a ? 'a' : 'b';
      const landed = new Set(), flownSet = new WeakSet(), pos = new Map();
      const oRH = m.resolveHit;
      m.resolveHit = function(self, tgt, x, y, seg, mul, over){
        const cs = this._cineShot;
        if (self === me && cs && cs.spell === 'glyph'){ landed.add(cs); if (cs.sigil) T.sigilHits++; }
        return oRH.call(this, self, tgt, x, y, seg, mul, over);
      };
      if (m.tickConverge){
        const oTC = m.tickConverge;
        m.tickConverge = function(dt){
          const C0 = me.ultConverge, cast = C0 && C0.cast;
          const pre = new Map(); for (const s of this.shots) if (s.own === own && s.sigil) pre.set(s, s.fuse);
          const r = oTC.call(this, dt);
          const C = me.ultConverge;
          if (cast && C){
            const fused = [...pre.keys()].filter(s => pre.get(s) === undefined && s.fuse !== undefined && s.fuse <= U.gap * 200);
            // hanging at the cast: those with fuse = gap*k -- check the order by `laid`
            const atc = [...pre.keys()].filter(s => pre.get(s) === undefined).sort((p, q) => p.laid - q.laid);
            T.atCast += atc.length;
            atc.forEach((s, k) => { const want = U.gap * k;
              const got = s.flown ? 0 : s.fuse;               // k = 0 launched on this very step
              if (!(s.flown && k === 0) && Math.abs(got - want) > 1e-9 && T.badOrder.length < 5) T.badOrder.push({ k, got, want }); });
          } else if (C && C.t < C.dur){
            for (const s of this.shots) if (s.own === own && s.sigil && pre.has(s) && pre.get(s) === undefined && s.fuse !== undefined){
              T.inWin++;
              if (Math.abs(s.fuse - (C.t + U.fuse)) > 1e-9 && T.badFuse.length < 5) T.badFuse.push({ fuse: s.fuse, want: C.t + U.fuse });
            }
          }
          if (C0 && !C && me.alive && foe.alive && !this.over && C0.t > C0.dur + U.gap * 64 + U.fuse + 1e-9) T.overStay++;
          return r;
        };
      }
      const oB = m.beat; m.beat = function(o){ if (o && o.kind === 'ult' && o.w === rid) T.ultBeats++; return oB.call(this, o); };
      /* A CAST NEVER LANDS ON A LIVE WINDOW: the charge and the window's
         clock run in lockstep, and a waiting sigil dies of its own 4s life,
         so the state is gone ~5.5s before the next cast is due. Asserted. */
      const oF = m.fireUlt; m.fireUlt = function(f, foe){ if (f === me && me.ultConverge) T.castOnLive++; return oF.call(this, f, foe); };
      let step = 0, lastL = me.convergeTally ? me.convergeTally.launched : 0;
      while (!m.over && step < secs / DT){
        const mine = new Map(); for (const s of m.shots) if (s.own === own) mine.set(s, { sigil: !!s.sigil, x: s.x, y: s.y });
        const fc0 = me.fireCd, f0 = me.shotsFired, open0 = !!me.ultConverge, h0 = me.hits;
        m.step(DT); step++;
        if (me.shotsFired > f0){
          T.looses++;
          if (Math.abs((me.fireCd - fc0) - (S.cadence - DT)) > 1e-9 && T.badCad.length < 5) T.badCad.push(me.fireCd - fc0);
        }
        for (const s of m.shots){
          if (s.own !== own) continue;
          const was = mine.get(s);
          if (!was){
            if (s.spell === 'glyph' && !s.sigil && !s.flown && !labTag){
              T.glyphs++;
              const ok = s.r === S.r && s.bounce === 1 && s.glyph === true && s.dmgMul === S.dmgMul && s.life === S.life - DT;
              if (!ok && T.badGlyph.length < 5) T.badGlyph.push({ r: s.r, bounce: s.bounce, life: s.life });
            } else if (s.sigil || s.flown){ T.sigils++; T.born++; }   // loosed into a wall: a sigil on its first step
            continue;
          }
          if (s.sigil && !was.sigil){
            T.sigils++;
            const ok = s.vx === 0 && s.vy === 0 && s.life === S.sigilLife && s.over && s.over.onHit && s.over.onHit.hex === S.sigilHex && s.laid !== undefined;
            if (!ok && T.badSigil.length < 5) T.badSigil.push({ vx: s.vx, vy: s.vy, life: s.life });
            if (flownSet.has(s)) T.reformed++;
          } else if (s.sigil && was.sigil){
            if (s.x !== was.x || s.y !== was.y) T.moved++;
          }
          if (s.flown) flownSet.add(s);
        }
        const alive = new Set(m.shots);
        for (const [s, was] of mine){
          if (alive.has(s) || !was.sigil || landed.has(s)) continue;
          if (s.life > 1e-9) T.clanked++;
        }
        if (labTag) for (const s of m.shots) if (s.own === own && s.untagged){ s.untagged = false; s.bounce = 1; s.glyph = true; }
        const C = me.ultConverge;
        if (C && C.t <= C.dur){
          if (!open0) T.casts++;
          T.winFrames++; T.foeStk += foe.stacks('hex'); T.winBlows += me.hits - h0;
        }
      }
      if (me.convergeTally){ T.launched += me.convergeTally.launched; T.tallyCasts += me.convergeTally.casts; }
      T.fights++; T.dur += m.t; T.blows += me.hits; if (m.winner === me) T.wins++;
      T.labCasts += Math.floor(step * DT / 16 + 1e-9);     // the lab's schedule: a cast every 16s of steps
    }
  } finally { for (const [o, k, v] of undo.reverse()) o[k] = v; AC.Match.prototype.spawnShot = oSpawn; }
  T.live = live;
  return T;
}"""

DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement('canvas'); cv.width = 540; cv.height = 960;
  const ctx = cv.getContext('2d'); const R = AC.renderer, saved = R.ctx;
  const seen = { bolt: 0, sigil: 0, flown: 0 }; let threw = null, frames = 0;
  try {
    for (const foe of ['emberedge', 'axiom', 'farwarden']){
      const m = new AC.Match(rid, foe, seed); const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const g = m.shots.filter(s => s.spell === 'glyph');
        if (!(step % 7 === 0 || g.some(s => s.flown))) continue;
        R.ctx = ctx; R.drawShots(m); R.drawWeapon(m, me); R.ctx = saved; frames++;
        if (g.some(s => !s.sigil && !s.flown)) seen.bolt++;
        if (g.some(s => s.sigil)) seen.sigil++;
        if (g.some(s => s.flown)) seen.flown++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--relic", default="cipher")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed0", type=int, default=7001)
    ap.add_argument("--lab", action="store_true")
    ap.add_argument("--labseed0", type=int, default=2207)
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--secs", type=float, default=200.0)
    ap.add_argument("--json", default="")
    ap.add_argument("--labtag", action="store_true", help="the lab's tagging: a bolt loosed into a wall dies (the reproduction arm)")
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
        T = page.evaluate(JS, [a.relic, pairs, a.secs, sets, a.labtag])
        D = None if a.lab else page.evaluate(DRAW_JS, [a.relic, 7331, a.secs])
        assert not errors, errors
    if "err" in T:
        raise SystemExit(T["err"])
    F = T["fights"]; casts = T["casts"]
    row = dict(win=T["wins"] / F, castsF=casts / F, sig16=T["sigils"] / (T["dur"] / 16.0),
               launchC=T["launched"] / casts if casts else 0, winBlows=T["winBlows"] / casts if casts else 0,
               stk=T["foeStk"] / T["winFrames"] if T["winFrames"] else 0, atCast=T["atCast"] / casts if casts else 0,
               blowsF=T["blows"] / F, dur=T["dur"] / F,
               sigLab=T["sigils"] / T["labCasts"] if T["labCasts"] else 0, born16=T["born"] / (T["dur"] / 16.0))
    tag = ("--lab (side A, the lab's seeds and field)" if a.lab else "every foe, both sides") + ("  --labtag" if a.labtag else "")
    print(f"CIPHER PROBE -- {a.game}   {F} fights, {tag}" + (f"   set {' '.join(a.set)}" if a.set else "") + f"   {time.time()-t0:.0f}s")
    print(f"  win {row['win']:.1%}   casts {row['castsF']:.2f}   sigils {row['sig16']:.1f} a cast-equivalent   "
          f"hanging at a cast {row['atCast']:.2f}   launched {row['launchC']:.2f} a cast   blows {row['winBlows']:.2f} a window   "
          f"foe hex {row['stk']:.2f}   blows {row['blowsF']:.1f} a fight   mean {row['dur']:.1f}s")
    print(f"  sigils {row['sigLab']:.2f} a lab cast (the lab's normalization)   of them born on the step they were loosed "
          f"{row['born16']:.1f} a cast-equivalent")
    if a.lab:
        print("  against stage 0 on 151 (block 2207): arm S 30.5%, 25.50 sigils a lab cast;"
              " arm Y 51.5%, 1.91 hanging, 5.44 launched, 5.77 blows, hex 2.63, 26.00 sigils")
        if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row), indent=1))
        return 0
    res = []
    def check(ok, name, detail):
        res.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}  -- {detail}")
    check(T["glyphs"] > 20 * F and not T["badGlyph"], "[1] every glyph leaves with the spell's numbers and one bounce",
          f"{T['glyphs']} glyphs" + (f"  BAD {T['badGlyph']}" if T["badGlyph"] else ""))
    check(not T["badCad"] and T["looses"] > 0, "[2] the cadence is exact", f"{T['looses']} looses" + (f"  BAD {T['badCad']}" if T["badCad"] else ""))
    check(T["sigils"] > 0 and not T["badSigil"], "[3] every glyph a wall stops is a sigil: still, life 4.0, hex 2",
          f"{T['sigils']} sigils" + (f"  BAD {T['badSigil']}" if T["badSigil"] else ""))
    check(T["moved"] == 0, "[4] a sigil never moves while it is one", f"{T['moved']} sigil-steps moved")
    check(T["sigilHits"] > 0 and T["clanked"] > 0, "[5] sigils are touched and clanked",
          f"touched {T['sigilHits']}, clanked/expired-early {T['clanked']}")
    check(1.3 * 21.9 <= row["blowsF"] <= 60,
          "[6] the spell adds blows: over 1.3x the bow body's 21.9 a fight (stage 1), under 60 (the lab's ~31 is --labtag's)",
          f"{row['blowsF']:.1f}")
    if T["live"]:
        check(T["atCast"] > 0 and not T["badOrder"], "[7] the hanging sigils leave in laid order, 0.25s apart",
              f"{T['atCast']} at {casts} casts" + (f"  BAD {T['badOrder']}" if T["badOrder"] else ""))
        check(T["inWin"] > 0 and not T["badFuse"], "[8] a sigil laid in the window leaves 0.5s after it is laid",
              f"{T['inWin']}" + (f"  BAD {T['badFuse']}" if T["badFuse"] else ""))
        check(4 <= row["launchC"] <= 14 and 4 <= row["winBlows"] <= 14 and 1.8 <= row["stk"] <= 4.0,
              "[9] launched, blows a window, the foe's hex (the lab's 5.4/5.7/2.6 are --labtag's; the build tags at spawn)",
              f"launched {row['launchC']:.2f}, blows {row['winBlows']:.2f}, hex {row['stk']:.2f}")
        check(T["reformed"] == 0, "[10] no flown rune ever becomes a sigil again", f"{T['reformed']} re-formed")
        check(T["ultBeats"] == T["tallyCasts"] and T["overStay"] == 0 and T["castOnLive"] == 0,
              "[11] an ult beat a cast; no cast lands on a live window; the state never outlives its last fuse",
              f"{T['ultBeats']} beats for {T['tallyCasts']} casts ({casts} seen open after their step); "
              f"{T['castOnLive']} casts on a live window; {T['overStay']} over-stays")
    check(D["threw"] is None and D["seen"]["bolt"] > 0 and D["seen"]["sigil"] > 0 and (not T["live"] or D["seen"]["flown"] > 0),
          "[P] the render path is CALLED", (D["threw"] or "") + f"  {D['frames']} frames  {D['seen']}")
    print(f"\n  {sum(res)}/{len(res)}")
    if a.json: pathlib.Path(a.json).write_text(json.dumps(dict(T=T, row=row, D=D), indent=1))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
