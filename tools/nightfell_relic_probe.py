#!/usr/bin/env python3
"""DEADFALL, ASSERTED AGAINST THE BUILD -- one check per sentence.

    python nightfell_relic_probe.py --game ../02-chain/sc-nightfell.html

Layer 2 of the v51/52 build brief (§8.4). Ten checks, and the tenth is not
here because no tool in this repo can run it.

  [1]  ONE FIGURE PER BLOW inside the window, `points` charges, on a ring of
       the stated radius -- measured off POSITIONS, not recomputed from config
  [2]  a charge does not exist before its arming time, and the foe can stand
       on a crackling one without setting it off
  [3]  NO CHARGE EVER FIRES ON THE CASTER, in any match, at any separation --
       and the caster is measured standing inside its own figures while it
       does not happen
  [4]  NOTHING EXPIRES. planted = walked-into + still-standing, with nothing
       lost between them
  [5]  the curse pool is UNCHANGED by the whole ultimate
  [6]  the stamp is the pool sum AT THE BLOW, not at the detonation
  [7]  THE CHAIN SPANS FRAMES -- no two charges ever fall in the same step
  [8]  every voice renders to something audible in an OfflineAudioContext
  [9]  the ult files a BEAT, and a charge that KILLS files a FATAL one
  [P]  the render path is CALLED against a real 2D context

## [7] IS THE ONE THIS PROBE EXISTS FOR

If the detonation handler looped over every charge in range, a figure would
come apart in a single frame and **every number in `06-docs/v52/echoes-v52.md`
would still be right**. The damage, the win rate, the chain counters and the
beats are all identical either way, and there would be no chain to see. That
is CLAUDE.md §4.1's defect class -- v42's silent ultimate, v43's sticking hold
-- and it is the reason this check counts charges lost PER STEP rather than
per second.

## [3] IS THE ONE THAT WOULD TUNE STRAIGHT OUT

A self-triggering figure eats 48% of its own charges (v52 §3c) and the cost
disappears into the blade: blade 15.83 with self-triggering lands on exactly
the same win rate as blade 13 without it. So no sweep, no `verify` and no
win-rate check anywhere in this repo can see it. [3] measures the caster
STANDING INSIDE its own armed figures -- which it does constantly, because
they are planted where its own blows land -- and asserts nothing happens.

## AND THE CHECKS RECONSTRUCT THE ENGINE'S RULE RATHER THAN ASSUMING THEIR OWN

Three checks in `gravemourn_relic_probe` reported defects that were not there,
all three because the probe had written down its own model of a rule and the
engine legitimately did something else. So: `points`, `ring`, `rad`, `arm` and
`stampMul` are all read off `w.ult` here, never typed in; [1] compares figures
against the ENGINE'S OWN blow counter as well as against an independent one,
and prints both when they disagree instead of failing on the difference.
"""
from __future__ import annotations

import argparse
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "nightfell"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


META_JS = r"""([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const P = AC.Match.prototype;
  const strip = f => f.toString().replace(/\/\*[\s\S]*?\*\//g, "")
                                 .replace(/\/\/.*/g, "");
  const td = strip(P.tickDeadfall), rh = strip(P.resolveHit);
  return {
    u: JSON.parse(JSON.stringify(w.ult)),
    dmg: w.dmg,
    src: {
      /* THE CAST RESOLVES NOTHING. Eclipse was a 250-radius nova for 11. */
      castIsEmpty: w.ult.dmg === 0,
      kindIsSigil: w.ult.kind === "sigil",
      /* §8.3b: the figure READS the pool. Comments are stripped first, because
         this file explains itself in the file -- `curse_check` fired on its own
         explanation once and `curse_build` refused to write on its. */
      readOnly: !/pushCurse|apply\("curse"|cursePool/.test(td),
      /* `apply` stays deleted -- v52 §3e measured re-application at +0.0% */
      noApply: !w.ult.apply,
      /* per-match state, not `w` and not `shots` (whose maxLive SHIFTS) */
      ownList: /this\.sigils/.test(rh) && /this\.sigils/.test(td),
      /* nothing expires: no lifetime, no splice on a clock */
      noExpiry: !/life|expire/i.test(td),
      /* and a charge files a beat */
      filesBeat: /this\.beat\(/.test(td),
      fatalBeat: /fatal: true/.test(td),
    },
  };
}"""


# ---------------------------------------------------------------- the run ---
# ONE instrumented match per (foe, seed). Every hook forwards with `arguments`
# -- v44's warning, which is that a wrapper with a FIXED ARITY silently
# measures the old build the moment the build grows a parameter.
RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const A = { fights: 0, blows: 0, engBlows: 0, figures: 0, engFigures: 0,
              refused: 0, countBad: 0, ringBad: 0, spaceBad: 0,
              planted: 0, sprung: 0, standing: 0,
              preArmFired: 0, preArmFrames: 0,
              selfHurt: 0, casterInside: 0,
              poolMoved: 0, poolFrames: 0,
              stampBad: 0, stampFrozen: 0,
              multiFrame: 0, chained: 0, longest: 0,
              ultBeats: 0, chargeKills: 0, fatalBeats: 0,
              dmgBad: 0, maxLive: 0, casts: 0, bombDmg: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      A.fights++;

      /* ---- the hooks. All three forward with `arguments`. ---- */
      let inTick = false;
      const oTick = m.tickDeadfall.bind(m);
      m.tickDeadfall = function(){
        inTick = true;
        /* [5]. MEASURED ACROSS `tickDeadfall` AND NOTHING ELSE. The first cut
           compared the pool across a whole `m.step` and reported 2 moves in
           336 -- both of them a BLADE BLOW landing on the same frame as a
           detonation, which is the pool doing exactly what it is for. A check
           that photographs a wider span than the claim it is making measures
           the rest of the engine and calls it a defect; three checks in
           `gravemourn_relic_probe` did the same thing in one session. */
        const before = th.cursePool.join(",") + "|" + me.cursePool.join(",");
        const wasAlive = th.alive && me.alive;
        try { return oTick.apply(m, arguments); }
        finally {
          inTick = false;
          /* the fatal frame is excluded: death runs the status-clearing path,
             which is the engine tidying a corpse rather than this ultimate
             writing to a pool */
          if (wasAlive && th.alive && me.alive){
            A.poolFrames++;
            if (th.cursePool.join(",") + "|" + me.cursePool.join(",") !== before)
              A.poolMoved++;
          }
        }
      };
      const oHurt = m.hurt.bind(m);
      m.hurt = function(f){
        /* [3]. A charge hurting its own caster is the 48% self-eat, and it is
           invisible to every win rate because it tunes out of the blade. */
        if (inTick && f === me) A.selfHurt++;
        return oHurt.apply(m, arguments);
      };
      const oBeat = m.beat.bind(m);
      m.beat = function(b){
        if (inTick && b && b.kind === "ult") A.ultBeats++;
        if (inTick && b && b.fatal) A.fatalBeats++;
        return oBeat.apply(m, arguments);
      };
      const oRes = m.resolveHit.bind(m);
      m.resolveHit = function(self, foe2, hx, hy){
        const n0 = m.sigils.length;
        /* the window, read BEFORE the call: `resolveHit` can close nothing,
           but the blow can kill, and a dead foe is the engine's own reason
           not to stamp */
        const open = self === me && !!me.ultDeadfall && !m.over;
        const r = oRes.apply(m, arguments);
        if (!open) return r;
        const alive = foe2.alive && !foe2.shade && foe2 === th;
        if (alive) A.blows++;                     // the independent count
        const n1 = m.sigils.length;
        if (n1 > n0){
          const g = m.sigils[n1 - 1];
          A.figures++;
          A.planted += g.ch.length;
          /* [1]. MEASURED OFF POSITIONS. `points` and `ring` are read from
             `w.ult`, never typed in -- a probe that hardcodes a number fails
             on every legitimate change to it. */
          if (g.ch.length !== U.points) A.countBad++;
          const angs = [];
          for (const c of g.ch){
            if (Math.abs(Math.hypot(c.x - g.x, c.y - g.y) - U.ring) > 1e-6)
              A.ringBad++;
            angs.push(Math.atan2(c.y - g.y, c.x - g.x));
          }
          angs.sort((p, q) => p - q);
          const want = 2 * Math.PI / g.ch.length;
          for (let i = 1; i < angs.length; i++)
            if (Math.abs((angs[i] - angs[i - 1]) - want) > 1e-6) A.spaceBad++;
          /* [6]. The stamp is what Curse remembers AT THIS INSTANT -- which
             is after this blow's own memory went in, because the block sits
             after the `onHit` loop on purpose. */
          if (Math.abs(g.stamp - foe2.curseSum() * U.stampMul) > 1e-6)
            A.stampBad++;
          for (const c of g.ch)
            if (Math.abs(c.mem - g.stamp / g.ch.length) > 1e-9) A.stampBad++;
        }
        return r;
      };

      let step = 0, lastBoom = -99, run_ = 0;
      while (!m.over && step < secs / DT){
        /* the whole floor, photographed before and after the step */
        const pre = m.sigils.map(g => ({ g, live: g.ch.filter(c => !c.dead),
                                         t: g.t }));
        const preLive = pre.reduce((s, p) => s + p.live.length, 0);
        if (preLive > A.maxLive) A.maxLive = preLive;
        const hpPre = th.hp;
        /* [2] and [3] are only worth anything if they were EXERCISED. Count
           the frames in which the thing that must not happen was available. */
        for (const p of pre){
          const armed = p.t >= p.g.arm;
          for (const c of p.live){
            const dth = Math.hypot(th.x - c.x, th.y - c.y);
            const dme = Math.hypot(me.x - c.x, me.y - c.y);
            if (!armed && dth <= p.g.rad) A.preArmFrames++;
            if (armed && dme <= p.g.rad) A.casterInside++;
          }
        }
        const nf0 = m.sigils.length;
        const alivePre = th.alive;
        m.step(DT); step++;
        if (m.sigils.length > nf0) A.figures += 0;   // counted in resolveHit

        /* what fell this step, and whether it was allowed to */
        let fell = 0;
        for (const p of pre){
          for (const c of p.live) if (c.dead){
            fell++;
            /* [2]. `p.t` is the age BEFORE the step: a charge that fell while
               its own figure had not finished arming is a live mine wearing a
               crackle. */
            if (p.t + DT < p.g.arm) A.preArmFired++;
          }
        }
        if (fell > 1) A.multiFrame++;
        if (fell > 0){
          A.sprung += fell;
          A.bombDmg += Math.max(0, hpPre - th.hp);
          if (m.t - lastBoom <= 0.45){ A.chained += fell; run_ += fell; }
          else run_ = fell;
          if (run_ > A.longest) A.longest = run_;
          lastBoom = m.t;
          if (alivePre && !th.alive) A.chargeKills++;
          /* [9]. A charge that ends the fight has to file a FATAL beat --
             `cinema_clip` finds the killing blow with `plan.find(c => c.fatal)`
             and an `ult` beat carries no such flag. 30 of Gravemourn's 58
             kills rendered a clip with no killing blow before the same line
             existed there. */
        }
      }
      A.casts += me.ultsFired;
      /* [4]. planted = walked-into + still-standing, and nothing in between. */
      for (const g of m.sigils)
        for (const c of g.ch) if (!c.dead) A.standing++;
      /* the engine's OWN counters, for [1]'s second opinion. The last window
         is still open if the fight ended inside it. */
      if (me.ultDeadfall){ A.engBlows += me.ultDeadfall.blows;
                           A.engFigures += me.ultDeadfall.figures;
                           A.refused += me.ultDeadfall.refused; }
    }
  }
  return A;
}"""


# THE RENDER PATH, CALLED. §4.0/§4.1 and the Vesper lesson: two picture faults
# shipped through 27 probe checks, a 280-match engine_ab, chain_audit and
# post_identity, and DIED ON THE FIRST RENDERED FRAME -- because the probe was
# REGEXING a draw function's source for a call, and a string does not resolve a
# reference. This calls the three entry points this relic touches against a
# real 2D context.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { arming: 0, armed: 0, crackle: 0, under: 0, over: 0,
                threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        if (m.sigils.length){
          let anyArming = false, anyArmed = false;
          for (const g of m.sigils) (g.t >= g.arm ? anyArmed = true
                                                  : anyArming = true);
          try { R.ctx.save(); R.drawSigils(m); R.ctx.restore();
                if (anyArming) out.arming++; if (anyArmed) out.armed++; }
          catch (e){ out.threw = "drawSigils: " + String(e); return out; }
        }
        /* BOTH HALVES OF THE CRACKLE, and it is drawn off the FIGHTER rather
           than off `m.ultFx` -- see `drawCrackle`. A window whose art hangs on
           the match's single fx slot is erased by the opponent's next cast,
           which is why this one does not. */
        if (m.a.deadfallFade > 0 || m.b.deadfallFade > 0){
          try { R.ctx.save(); R.drawCrackle(m, false);
                R.drawCrackle(m, true); R.ctx.restore(); out.crackle++; }
          catch (e){ out.threw = "drawCrackle: " + String(e); return out; }
        }
        if (!m.ultFx) continue;
        try { R.ctx.save(); R.drawUltUnder(m); R.ctx.restore(); out.under++; }
        catch (e){ out.threw = "drawUltUnder: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltOver(m); R.ctx.restore(); out.over++; }
        catch (e){ out.threw = "drawUltOver: " + String(e); return out; }
      }
      if (out.arming > 200 && out.armed > 400 && out.under > 400) return out;
    }
  }
  return out;
}"""


# FOUR VOICES, and [8] is why v42's ultimate shipped silent. `SFX.play` returns
# on its first line headless and wraps its body in try/catch, so a missing
# helper is SILENCE and no other tool in this repo can tell.
CASES = [
    ("the cast",       "ult", {"w": "nightfell"},       2.2),
    ("a figure lands", "ult", {"w": "nightfell-stamp"}, 1.2),
    ("it goes live",   "ult", {"w": "nightfell-arm"},   1.2),
    ("something walks in", "ult", {"w": "nightfell-boom"}, 1.4),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--foes", default="emberedge,bulwarden,axiom,ironhail,"
                                      "twinshade,grudgebearer")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    A = ap.parse_args()

    foes = [x.strip() for x in A.foes.split(",") if x.strip()]
    seeds = [3301 + 19 * i for i in range(A.seeds)]
    path = resolve_game(A.game)
    print(f"\nDEADFALL — the build, asserted\n  game {path.name}")
    print(f"  {len(foes)} foes x {len(seeds)} seeds = {len(foes)*len(seeds)} fights")

    with game(game_path=path) as (page, errors):
        M = page.evaluate(META_JS, [RID])
        u, S = M["u"], M["src"]
        print(f"\n  {u['name']}  kind {u['kind']}  dur {u['dur']}  "
              f"points {u['points']}  ring {u['ring']}  rad {u['rad']}  "
              f"arm {u['arm']}  stampMul {u['stampMul']}  push {u['push']}")
        print(f"  blade {M['dmg']}   tip {len(u['tip'])}/72  {u['tip']!r}")

        check("the cast resolves NOTHING — Eclipse was a 250-radius nova for "
              "11 and DEADFALL's cast only opens a window",
              S["castIsEmpty"] and S["kindIsSigil"],
              f"dmg {u['dmg']}, kind {u['kind']!r}")
        check("THE FIGURE IS READ-ONLY ON THE POOL (§8.3b) — Gravemourn MOVES "
              "a memory, this one COPIES one, and a charge that writes back "
              "recreates the +0.0 clause v52 §3e deleted",
              S["readOnly"] and S["noApply"],
              "no pushCurse / apply(\"curse\") / cursePool in tickDeadfall, "
              "and ult.apply is gone")
        check("the charges are per-match state with no lifetime — not on `w`, "
              "not in `shots` (whose maxLive SHIFTS a live one out)",
              S["ownList"] and S["noExpiry"])

        print()
        R = page.evaluate(RUN_JS, [RID, foes, seeds, A.secs])
        print(f"    {R['fights']} fights   {R['casts']} casts   "
              f"{R['figures']} figures   {R['planted']} charges planted   "
              f"{R['sprung']} walked into   {R['standing']} still standing")
        print(f"    most live at once {R['maxLive']}   chained {R['chained']}"
              f"   longest run {R['longest']}   "
              f"{R['bombDmg']} damage off the floor")

        # [1]
        blows, figs = R["blows"], R["figures"]
        check("ONE FIGURE PER BLOW landed inside the window, and it is "
              "`points` charges evenly spaced on a ring of `ring` — measured "
              "off the positions the proximity test actually reads, not "
              "recomputed from the config",
              blows == figs + R["refused"] and not R["countBad"]
              and not R["ringBad"] and not R["spaceBad"],
              f"{blows} blows -> {figs} figures + {R['refused']} refused; "
              f"count/ring/spacing bad: {R['countBad']}/{R['ringBad']}/"
              f"{R['spaceBad']}   (the engine's own counters say "
              f"{R['engBlows']} blows / {R['engFigures']} figures on the "
              f"windows still open at the end)")

        # [2]
        check("A CHARGE DOES NOT EXIST BEFORE ITS ARMING TIME — the foe stands "
              "inside crackling figures and nothing happens",
              R["preArmFired"] == 0 and R["preArmFrames"] > 0,
              f"{R['preArmFrames']} frames spent inside an un-armed charge, "
              f"{R['preArmFired']} of them fired"
              if R["preArmFrames"] else "NEVER EXERCISED — no frame put the "
              "foe inside a crackling charge, so this check proved nothing")

        # [3]
        check("NO CHARGE EVER FIRES ON THE CASTER (§8.3c) — and the caster is "
              "measured standing inside its own armed figures while it does "
              "not, because they are planted where its own blows land",
              R["selfHurt"] == 0 and R["casterInside"] > 0,
              f"{R['casterInside']} frames with the caster inside its own "
              f"armed charge, {R['selfHurt']} of them hurt it"
              if R["casterInside"] else "NEVER EXERCISED")

        # [4]
        check("NOTHING EXPIRES — planted = walked-into + still-standing, with "
              "nothing lost in between",
              R["planted"] == R["sprung"] + R["standing"],
              f"{R['planted']} = {R['sprung']} + {R['standing']}")

        # [5]
        check("the curse pool is UNCHANGED by the whole ultimate — same "
              "entries before and after every detonation",
              R["poolMoved"] == 0 and R["poolFrames"] > 0,
              f"{R['poolFrames']} `tickDeadfall` calls, {R['poolMoved']} of "
              f"them moved a pool")

        # [6]
        check("THE STAMP IS THE POOL SUM AT THE BLOW, not at the detonation, "
              "and each charge carries an equal share of it",
              R["stampBad"] == 0,
              f"{R['figures']} figures, {R['stampBad']} mis-stamped")

        # [7]
        check("THE CHAIN SPANS FRAMES (§8.3a) — no two charges ever fall in "
              "the same step, so the shove that carries the ball into the "
              "next one has landed before the next test runs",
              R["multiFrame"] == 0 and R["sprung"] > 0,
              f"{R['sprung']} detonations, {R['multiFrame']} steps took more "
              f"than one")

        # [9]
        check("a charge files a BEAT, and a charge that KILLS files a FATAL "
              "one — `cinema_clip` finds the killing blow with "
              "`plan.find(c => c.fatal)` and an `ult` beat carries no such flag",
              R["ultBeats"] >= R["sprung"] and R["fatalBeats"] >= R["chargeKills"]
              and S["filesBeat"] and S["fatalBeat"],
              f"{R['sprung']} detonations -> {R['ultBeats']} ult beats; "
              f"{R['chargeKills']} kills by a charge -> {R['fatalBeats']} "
              f"fatal beats"
              + ("   (WEAKLY EXERCISED: a charge deals about a fifth of a "
                 "stamped pool, so it lands the killing blow far less often "
                 "than Grasp's hand does — run more fights before reading "
                 "this as proof)" if R["chargeKills"] < 4 else ""))

        # [P]
        print()
        D = page.evaluate(DRAW_JS, [RID, foes, seeds[:3], A.secs])
        if D.get("skip"):
            check("THE RENDER PATH IS CALLED", False, D["skip"])
        else:
            print(f"    the render path, CALLED   drawSigils "
                  f"{D['arming']} arming / {D['armed']} armed   "
                  f"drawCrackle {D['crackle']}   "
                  f"drawUltUnder {D['under']}   drawUltOver {D['over']}")
            check("`drawSigils`, `drawCrackle`, `drawUltUnder` and "
                  "`drawUltOver` all run "
                  "against a real 2D context, in BOTH sigil states — a "
                  "regex on a draw function's source cannot resolve a "
                  "reference, which is how two picture faults shipped through "
                  "27 green checks in v48",
                  not D["threw"] and D["arming"] > 0 and D["armed"] > 0
                  and D["crackle"] > 0 and D["under"] > 0 and D["over"] > 0,
                  D["threw"] or "nothing threw")

        # [8]
        print()
        try:
            import numpy as _np
        except Exception:
            _np = None

        def profile(g):
            if _np is None or not g.get("win"):
                return None
            x = _np.asarray(g["win"], dtype=float)
            sr2 = 44100
            Sp = _np.abs(_np.fft.rfft(x * _np.hanning(x.size))) ** 2
            f = _np.fft.rfftfreq(x.size, 1 / sr2)
            tot = Sp.sum() or 1.0
            bands = [(20, 60), (60, 120), (120, 300), (300, 700),
                     (700, 1500), (1500, 20000)]
            return [round(100 * Sp[(f >= lo) & (f < hi)].sum() / tot, 1)
                    for lo, hi in bands]

        sfx = {}
        print(f"      {'':<21}{'peak':>7}{'audible':>9}{'<120Hz':>9}"
              f"{'thru 300Hz HP':>15}")
        for name, kind, pp, secs in CASES:
            g = page.evaluate(SFX_JS, [kind, pp, secs])
            g["profile"] = profile(g)
            g.pop("win", None)
            g.pop("onset", None)
            sfx[name] = g
            print(f"      {name:<21}{g['peak']:>7}{g['audible']:>8}s"
                  f"{g['low120']:>9}{g['hp300']:>15}"
                  + (f"   THREW {g['threw']}" if g.get("threw") else ""))
        silent = [n for n, _, _, _ in CASES if sfx[n]["peak"] < 0.002]
        check("every voice this relic makes renders to something audible — "
              "`SFX.play` swallows a TypeError and headless never calls it at "
              "all, so a missing helper ships as SILENCE (v42)",
              not silent,
              f"{len(CASES)} voices, quietest peak "
              f"{min(sfx[n]['peak'] for n, _, _, _ in CASES)}"
              if not silent else f"SILENT: {', '.join(silent)}")
        # THE ARMING SNAP IS THE ONE SOUND WITH A JOB. The armed state is
        # invisible to a viewer watching the balls instead of the floor, so it
        # is the only cue that reaches them either way -- and it has to be
        # nothing like the stamp before it or the detonation after it.
        arm, stamp, boom = (sfx["it goes live"], sfx["a figure lands"],
                            sfx["something walks in"])
        check("the ARMING snap is a different sound from the stamp before it "
              "and the detonation after it — it is the only cue a viewer "
              "watching the balls instead of the floor ever gets",
              arm["hp300"] > stamp["hp300"] + 0.15
              and arm["audible"] < boom["audible"] + 0.35,
              f"through a 300 Hz high-pass: stamp {stamp['hp300']}, "
              f"arm {arm['hp300']}, boom {boom['hp300']}")

        check("no page errors", not errors, "; ".join(errors[:3]))

    bad = [n for n, ok in PASS if not ok]
    print(f"\n  {len(PASS) - len(bad)}/{len(PASS)} checks pass")
    # [10] IS NOT HERE, AND SAYING SO IS THE POINT.
    print("""
  [10] ARMED READS DIFFERENTLY FROM ARMING — NOT CHECKED, AND NOT CHECKABLE
       HERE. §8.4's tenth check is a filmstrip question and nothing in
       `tools/` can answer it: with a fuse the crackle was a COUNTDOWN and the
       tension was time; with a mine it is an ARMING animation and the tension
       is space, and a viewer who cannot tell a live sigil from a crackling
       one cannot see the mechanic at all. The art makes them differ in four
       ways at once (incomplete/complete, flickering/still, dim/lit,
       loose/bound, plus a snap on the transition) and whether any of that
       survives a phone screen is Rick's, off a rendered clip.""")
    if bad:
        print("  FAILED: " + "; ".join(bad[:4]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
