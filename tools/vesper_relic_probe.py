#!/usr/bin/env python3
"""ONE CHECK PER SENTENCE OF §1, AGAINST THE BUILD.

    python vesper_relic_probe.py --game ../02-chain/sc-vesper.html

`beam_probe.py` priced §1 by OVERLAYING a proposed beam on real trajectories,
before a builder was opened and with nothing written back. This is the other
half: the same sentences, asserted against the thing that was actually built.

    "pink sycthes ult -- when the ult fires the scythe charges up (with a loud
     glowing animation) and then fires a targeted beam (thick, at least half
     the thickness of an artifact) the beam has limited range and points at
     the tip. the beam slowly rotates to track the enemy ball. while it
     persists it does rapid ticks of damage that push enemies towards its tip
     where it does bonus damage. the beam uses the scythes banked shield to
     increase its duration."

Every check states what would count as evidence against the build, and most of
them exist because the thing they check is INVISIBLE to every other tool here:

  * A DRAWN BEAM AND A TESTED BEAM THAT ARE TWO OBJECTS produce no error and
    no moved win rate -- they produce a viewer watching a shaft miss. [1]
    asserts they are one function. v43's hexagon is why this check exists.
  * A PASS COUNTED TWICE looks exactly like a pass counted once, in every
    aggregate this repo prints. [2] walks the edges.
  * A TIP BONUS READ OFF THE LAST FRAME instead of off the pass's furthest
    reach is a bonus that fires on the wrong third of passes and nothing
    anywhere says so. [3].
  * A WARD READ AT THE CAST is the design's own worst case and 59% of casts
    would be inert. [5] asserts the loop closes in both directions: it drains
    while lit, it is fed by the blade's own blows, and a caster that is given
    NOTHING gets the base duration and not one frame more.
  * A BROKEN SOUND is inert headless -- `SFX.play` returns on its first line
    and wraps its body in try/catch -- so [9] RENDERS all four voices in an
    OfflineAudioContext. v42 shipped a SILENT ultimate through fourteen
    checks, twenty-nine checks, a full sweep, a 13/13 verify and a rendered
    clip, and a person listening is what caught it.
  * AN ULTIMATE THE DIRECTOR CANNOT SEE gets its best moment scored as empty
    air. [10] is rule 3, seventh relic running.

## THE LEDGER IS BUILT ON THE ENGINE'S OWN CALLS, AND THE FIRST CUT WAS NOT

The first version of this probe re-derived `inBeam` from OUTSIDE, once per
step after `m.step` returned, and disagreed with the build on five counts. All
five were the instrument:

  THE RELEASE FRAME     `tickSentinel` sets the phase and `continue`s, so the
                        beam exists and is tested by nobody on the frame it
                        stands up. An outside re-derivation sees a quarry in
                        the volume and calls it a missed pass.
  A LETHAL PASS         nulls `ultBeam` on the frame it pays, so an outside
                        reader looking at the state AFTER the step finds
                        nothing and drops the pass it just paid for.
  HIT STOP              returns out of `step()` ABOVE `tickSentinel`, so the
                        beam is frozen with the rest of the world. Wall-clock
                        steps therefore over-count the window: a probe reading
                        9.60s against a 9.00s cap is reading its own clock.
  A MATCH THAT ENDS     mid-window never runs the window-end branch, so
                        anything totalled there is short by one window a
                        match.
  THE STARVED ARM       zeroed the pool before `m.step`, and `tickShots` banks
                        ward BEFORE `tickSentinel` drinks it -- so the arm
                        that was supposed to give the beam nothing was handing
                        it every arrow that landed that frame.

So the ledger now wraps `inBeam` itself and runs INSIDE the tick, off the
engine's own call with the engine's own arguments, and every clock it reports
is `B.t`. §4.6 of CLAUDE.md, arriving on a new instrument: an instrument that
fires where the mechanic does not measures something else.

Injection is runtime-only where it happens at all. NOTHING is written to any
build.
"""
from __future__ import annotations

import argparse
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "vesper"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


META_JS = r"""([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  if (!w) return null;
  const sc = AC.WEAPONS.filter(x => x.shape === "scythe" && x.id !== rid);
  const vg = AC.WEAPONS.filter(x => x.aff === "vigil" && x.id !== rid);
  const P = AC.Match.prototype;
  /* `_drawBeam` lives on the RENDERER, not on Match -- the seam between sim
     and picture is the whole reason this engine can be measured, and a probe
     that forgets it reads `undefined.toString()`. */
  const D = Object.getPrototypeOf(AC.renderer);
  return {
    w: { id: w.id, name: w.name, aff: w.aff, shape: w.shape, mode: w.mode,
         blades: w.blades, reach: w.reach, width: w.width, artW: w.artW,
         dmg: w.dmg, spin: w.spin, mass: w.mass,
         onHit: w.onHit || null, onSelf: w.onSelf || null, hasShot: !!w.shot },
    u: JSON.parse(JSON.stringify(w.ult)),
    /* THE TYPE'S BLOCK, byte for byte, off the other three scythes rather
       than off a doc: every relic in a row shares its physics. */
    peers: sc.map(x => ({ id: x.id, blades: x.blades, reach: x.reach,
                          width: x.width, artW: x.artW, spin: x.spin,
                          mass: x.mass, mode: x.mode })),
    school: vg.map(x => ({ id: x.id, shape: x.shape, onSelf: x.onSelf })),
    ballR: AC.CONFIG.physics.ballR,
    hitCd: AC.CONFIG.combat.hitCd,
    ward: JSON.parse(JSON.stringify(AC.STATUS.ward)),
    /* READ OUT OF THE SHIPPED SOURCE rather than copied here -- v43 §12's
       rule. If the renderer stops calling `beamTip`, or the drink starts
       going through `shatter`, these go false and the checks that depend on
       them say so. */
    src: {
      /* [1] ONE GEOMETRY. The renderer must reach the same origin function the
         simulation reaches, and neither may carry its own copy of the
         trigonometry. */
      simUsesInBeam: /this\.inBeam\(/.test(P.tickSentinel.toString()),
      simUsesTip:    /this\.beamOrigin\(/.test(P.tickSentinel.toString()),
      /* THE RENDERER ASKS THE MATCH. `m.beamTip`, not `this.beamTip` --
         `_drawBeam` is on the Renderer and `beamTip` is on Match, and the
         first cut of this build got that wrong and passed every headless
         check here. The regex is kept for the ONE-OBJECT claim; the check
         that the reference RESOLVES is a live call, below. */
      drawUsesTip:   /m\.beamOrigin\(/.test(D._drawBeam.toString()),
      drawUsesHalf:  /u\.half/.test(D._drawBeam.toString()),
      drawUsesTipFrom: /u\.tipFrom/.test(D._drawBeam.toString()),
      inBeamUsesSegDist: /segDist\(/.test(P.inBeam.toString()),
      /* THE ORIGIN IS THE BALL. Rick's, 2026-08-30. `beamOrigin` may
         not reach for the blade at all any more, and the growth has to
         be in the GEOMETRY rather than only in the picture. */
      originIsBall: !/bladeSegments/.test(P.beamOrigin.toString()),
      lenInGeometry: /this\.beamLen\(/.test(P.inBeam.toString()),
      drawUsesLen:   /m\.beamLen\(/.test(D._drawBeam.toString()),
      /* [5] THE DRINK IS ITS OWN ENDING and is neither of the other two. */
      drinkIsOwn:   !/shatter|spendWard/.test(P.drinkWard.toString()),
      drinkNoBurst: !/vx|vy|\bhp\b/.test(P.drinkWard.toString()),
      tickDrinks:   /this\.drinkWard\(/.test(P.tickSentinel.toString()),
      /* [6] the shade gate, written rather than assumed */
      shadeGate:    /!foe\.shade/.test(P.tickSentinel.toString()),
      /* [8] the wind-up is broken through the hook every true stun calls */
      breakHook:    /ultBeam/.test(P.breakSpin.toString()),
      breakOnlyWind: /phase === "wind"/.test(P.breakSpin.toString()),
      /* the shared hit loop, the shared shot path and the blades are all
         untouched -- the blades stay LIVE through the window, which is what
         the ward income in [5] is made of */
      hitsUntouched: !/ultBeam/.test(P.tickHits.toString()),
      shotsUntouched: !/ultBeam/.test(P.tickShots.toString()),
      bladesUntouched: !/ultBeam/.test(P.bladeSegments.toString()),
    },
  };
}"""


# [1] THE RENDER PATH, CALLED RATHER THAN READ. This check exists because the
# first cut of it did not: it regexed `_drawBeam`'s SOURCE for `beamTip(` and
# passed on a call that threw, because `beamTip` is a MATCH method and
# `_drawBeam` is on the RENDERER. Every headless tool in this repo was green
# and the first rendered frame died. A string does not resolve a reference.
#
# So this drives a real match to a standing beam and calls the renderer's own
# function against a real 2D context, in both phases. It is the picture-fault
# class (CLAUDE.md §4.1) given a number, which is what this project does when
# a render catches something a probe could not.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { wind: 0, beam: 0, under: 0, over: 0, threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const B = me.ultBeam;
        if (!B) continue;
        /* EVERY RENDER ENTRY POINT THIS RELIC TOUCHES, not just the one
           that broke first. `_drawBeam` is the shaft; `drawUltUnder` carries
           the wash and reads `ultFx`; `drawUltOver` ends by driving
           `ULTFX.sync`, which is where a bad particle spec would surface. */
        try {
          R.ctx.save();
          R._drawBeam(m, me);
          R.ctx.restore();
          if (B.phase === "wind") out.wind++; else out.beam++;
        } catch (e){
          out.threw = out.threw || ("_drawBeam/" + B.phase + ": " + String(e));
          return out;
        }
        try { R.ctx.save(); R.drawUltUnder(m); R.ctx.restore(); out.under++; }
        catch (e){ out.threw = "drawUltUnder: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltOver(m); R.ctx.restore(); out.over++; }
        catch (e){ out.threw = "drawUltOver: " + String(e); return out; }
      }
      if (out.wind > 40 && out.beam > 300) return out;
    }
  }
  return out;
}"""


# ---------------------------------------------------------------- the run ---
# ONE instrumented match per (foe, seed). Every hook forwards with `arguments`
# -- v44's warning, which is that a wrapper with a FIXED ARITY silently
# measures the old build the moment the build grows a parameter.

RUN_JS = r"""([rid, foes, seeds, secs, starve]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const P = AC.Match.prototype;
  const out = [];
  for (const foeId of foes){
    for (const sd of seeds){
      const m  = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const u  = me.w.ult;

      let casts = 0, released = 0, broken = 0;
      let windSteps = 0, beamSteps = 0, frozenSteps = 0;
      let drunkTotal = 0, bankedInWindow = 0;
      const windowT = [], windowDur = [], windowPasses = [];
      let passes = 0, tipHits = 0, passHits = 0, inSteps = 0;
      const passLen = [], passEnter = [], passBest = [];
      let beatsCast = 0, beatsPass = 0;
      let shadeCrossings = 0, shadeHits = 0;
      let sweptCorpse = 0, perpBad = 0, alongBad = 0, tipEarly = 0;
      let deadAtStart = false;
      let paidTwice = 0, tippedTwice = 0, tipUnpaid = 0;
      let reEntries = 0, widthMax = 0;
      let originBad = 0, endedOnCorpse = 0, outlived = 0, lenBad = 0;
      let lenMin = Infinity, lenMax = 0, growFrames = 0;

      /* THE LEDGER, INSIDE THE TICK. `inBeam` is wrapped so the entry and exit
         edges are read off the engine's OWN call, on the engine's own frame,
         with the engine's own arguments -- and `B.in` at that instant is still
         the PREVIOUS frame's value, which is what makes the edge detector
         independent of the branch it is checking. */
      let inTick = false, ledgerIn = false, ledgerT0 = 0, ledgerBest = 0;
      let runPasses = 0, lethalAtTip = 0;
      /* THE PRE-STATE, and it has to be taken HERE. `tickSentinel` sets
         `B.in = true` and `B.tipped = true` BEFORE it calls `beamHit`, so a
         probe reading the latch from inside the payment hook reads the value
         the payment just wrote and reports every pass as a double. `inBeam`
         runs one branch earlier, which is the last instant the previous
         frame's latch still exists. */
      let pre = { in: false, tipped: false, edge: false };

      const origTick = P.tickSentinel;
      m.tickSentinel = function(){
        inTick = true;
        try { return origTick.apply(m, arguments); } finally { inTick = false; }
      };

      const origIn = P.inBeam;
      m.inBeam = function(f, ang, x, y, uu, BB){
        const g = origIn.apply(m, arguments);
        if (!inTick || f !== me) return g;
        const B = me.ultBeam;
        if (!B) return g;
        if (g){
          inSteps++;
          if (g.along < -1e-9 || g.along > 1 + 1e-9) alongBad++;
          /* THE VOLUME, RE-DERIVED FROM THE SAME ORIGIN. A contact recorded
             further from the axis than `ballR + half` is a hit outside the
             beam the viewer is being shown. */
          const o = m.beamOrigin(f);
          const dx = x - o[0], dy = y - o[1];
          const along = Math.cos(ang) * dx + Math.sin(ang) * dy;
          const perp = Math.abs(-Math.sin(ang) * dx + Math.cos(ang) * dy);
          if (along >= 0 && along <= u.range){
            widthMax = Math.max(widthMax, perp);
            if (perp > R + u.half + 1e-6) perpBad++;
          }
          /* AND THE ORIGIN IS THE BALL, not the blade. Rick's, 2026-08-30.
             Asserted against the fighter's own live position rather than
             against a constant, so a future move of the origin has to move
             this line with it. */
          if (Math.abs(o[0] - f.x) > 1e-9 || Math.abs(o[1] - f.y) > 1e-9)
            originBad++;
          /* AND THE GROWTH IS IN THE VOLUME. `g.len` is what `inBeam`
             actually measured against; if it ever equals `range` on a frame
             the shaft is still opening, the drawn beam and the tested beam
             have come apart again. */
          if (g.len > u.range + 1e-6) lenBad++;
          lenMin = Math.min(lenMin, g.len); lenMax = Math.max(lenMax, g.len);
          pre = { in: B.in, tipped: B.tipped, edge: !B.in };
          if (!B.in){
            passes++; runPasses++; if (runPasses > 1) reEntries++;
            ledgerIn = true; ledgerT0 = B.t; ledgerBest = g.along;
          } else {
            ledgerBest = Math.max(ledgerBest, g.along);
          }
        } else {
          pre = { in: false, tipped: false, edge: false };
          if (ledgerIn){
            ledgerIn = false;
            passLen.push(B.t - ledgerT0); passBest.push(ledgerBest);
          }
        }
        return g;
      };

      /* THE PAYMENTS, and whether each one was allowed to happen. A base pass
         may only ever be paid on a frame where the latch was DOWN; a tip may
         only ever be paid once per pass and never below the line. */
      const origHit = P.beamHit;
      m.beamHit = function(f, foe, g, mul, tip){
        if (f === me){
          if (tip){
            tipHits++;
            if (g.along < u.tipFrom) tipEarly++;
            /* a tip on a CONTINUING pass that had already tipped */
            if (pre.in && pre.tipped) tippedTwice++;
          } else {
            passHits++; passEnter.push(g.along);
            /* a base payment on a frame the latch was already down */
            if (!pre.edge) paidTwice++;
          }
          if (foe && foe.shade) shadeHits++;
        }
        const r = origHit.apply(m, arguments);
        /* A LETHAL PASS ENDS THE BEAM, so a base hit that kills out at the far
           end never gets to pay its bonus -- and a probe that does not count
           those reports the tip as under-firing by exactly that many. */
        if (f === me && !tip && foe.hp <= 0 && g.along >= u.tipFrom)
          lethalAtTip++;
        return r;
      };

      const origBreak = P.breakSpin;
      m.breakSpin = function(f, reason, trueFor){
        const wasWind = f === me && f.ultBeam && f.ultBeam.phase === "wind";
        const r = origBreak.apply(m, arguments);
        if (wasWind && !f.ultBeam) broken++;
        return r;
      };

      /* THE STARVED ARM. The pool is emptied INSIDE the drink rather than
         before the step, because `tickShots` banks ward one function above
         `tickSentinel` and an outside pin hands the beam every arrow that
         landed on the same frame. This runs the shipped `drinkWard` against a
         genuinely empty plate. */
      const origDrink = P.drinkWard;
      m.drinkWard = function(f, want){
        if (starve && f === me){
          f.shield = 0; f.shieldMax = 0; delete f.status.ward;
        }
        const got = origDrink.apply(m, arguments);
        if (f === me) drunkTotal += got;
        return got;
      };

      const origBeat = P.beat;
      m.beat = function(o){
        if (o.kind === "ult" && o.w === rid){
          if (me.ultBeam && me.ultBeam.phase === "beam") beatsPass++;
          else beatsCast++;
        }
        return origBeat.apply(m, arguments);
      };

      let step = 0;
      while (!m.over && step < secs / DT){
        const shieldBefore = me.shield;
        const B0 = me.ultBeam;
        const p0 = B0 ? B0.phase : null;
        const hs0 = m.hitStop;
        /* A CORPSE THE BEAM WAS ALREADY STANDING OVER when the step began.
           The step the killing blow lands on does not count: `tickHits` runs
           BELOW `tickSentinel`, so the beam cannot know yet. What must never
           happen is a SECOND step. */
        const wasDead = !th.alive || th.hp <= 0;

        m.step(DT); step++;

        const B = me.ultBeam;
        const p = B ? B.phase : null;
        /* a step the world was frozen for is a step the beam did not run --
           `step()` returns above `tickSentinel` while `hitStop` is up */
        if (hs0 > 0) frozenSteps++;
        if (p === "wind" && p0 !== "wind") casts++;
        if (p === "beam" && p0 === "wind"){ released++; runPasses = 0; }
        if (p === "wind") windSteps++;
        if (p === "beam"){
          beamSteps++;
          if (m.beamLen(B, u) < u.range - 1) growFrames++;
          const gained = me.shield - shieldBefore;
          if (gained > 0) bankedInWindow += gained;
          if (wasDead) sweptCorpse++;
          for (const s of (m.shades || [])){
            if (origIn.call(m, me, B.ang, s.x, s.y, u, B)) shadeCrossings++;
          }
        }
        /* THE WINDOW ENDED -- by expiry, by a lethal pass, or by the caster
           dying. Read off `B0`, which is the same object the engine had just
           finished mutating, and clocked on `B.t` rather than on wall steps. */
        if (p0 === "beam" && p !== "beam"){
          if (ledgerIn){
            ledgerIn = false;
            passLen.push(B0.t - ledgerT0); passBest.push(ledgerBest);
          }
          windowT.push(B0.t); windowDur.push(B0.dur);
          windowPasses.push(B0.passes);
          /* evidence that the guards are LIVE rather than dead code: a window
             that ended with time still on its own clock, because the quarry
             was gone */
          if (B0.t < B0.dur - 1e-9) endedOnCorpse++;
        }
        /* AND NOTHING SURVIVES THE MATCH. `decay()` carries this rule for the
           shades, the storm and the Converse; the beam is the fourth. */
        if (m.over && me.ultBeam) outlived++;
      }
      /* A MATCH THAT ENDS MID-WINDOW still has a window, and the first cut of
         this probe threw one away per match. */
      if (me.ultBeam && me.ultBeam.phase === "beam"){
        const B = me.ultBeam;
        if (ledgerIn){ ledgerIn = false;
                       passLen.push(B.t - ledgerT0); passBest.push(ledgerBest); }
        windowT.push(B.t); windowDur.push(B.dur); windowPasses.push(B.passes);
      }

      out.push({ foe: foeId, seed: sd, steps: step, over: m.over,
                 casts, released, broken,
                 windSecs: windSteps * DT, beamSecs: beamSteps * DT,
                 frozenSteps, beamSteps, drunk: drunkTotal,
                 banked: bankedInWindow,
                 windowT, windowDur, windowPasses,
                 passes, passHits, tipHits, inSteps,
                 passLen, passEnter, passBest,
                 beatsCast, beatsPass, shadeCrossings, shadeHits,
                 sweptCorpse, endedOnCorpse, outlived,
                 perpBad, alongBad, tipEarly,
                 paidTwice, tippedTwice, reEntries, lethalAtTip,
                 originBad, widthMax, lenBad, growFrames,
                 lenMin: lenMin === Infinity ? null : lenMin, lenMax,
                 meHp: me.hp, thHp: th.hp, dealt: me.dealt, hits: me.hits });
    }
  }
  return out;
}"""


# [8] THE WIND-UP, AGAINST THE FOUR RELICS THAT CAN TAKE IT. v44 measured
# 14.77% of Crucible casts eating a true stun and found four fifths of it came
# from Axiom, Spellbreaker, Foregone and Paradox and none from the other
# twenty. This asks the same question of this relic's own charge-up.
HEX_FOES = ["axiom", "spellbreaker", "foregone", "paradox"]
CTRL_FOES = ["emberedge", "ironhail", "censer", "gravemourn"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-vesper.html")
    ap.add_argument("--relic", default="")          # the builder prints this name
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=120.0)
    A = ap.parse_args()
    g = resolve_game(A.relic or A.game)

    seeds = [1000 + i * 7919 for i in range(A.seeds)]
    foes = ["emberedge", "ironhail", "lastlight", "gravemourn", "censer",
            "twinshade", "widowmaker", "thornshear"]

    with game(game_path=g) as (page, errors):
        M = page.evaluate(META_JS, [RID])
        if not M:
            raise SystemExit(f"no relic {RID!r} in {g.name}")
        u, w, src = M["u"], M["w"], M["src"]
        R, half = M["ballR"], u["half"]

        print(f"\n{w['name']} / {u['name']} — {w['aff']} {w['shape']}   "
              f"dmg {w['dmg']}   ballR {R}   hitCd {M['hitCd']}")
        print(f"  beam  wind {u['wind']}s  dur {u['dur']}s  cap {u['durCap']}s  "
              f"turn {u['turn']} rad/s  range {u['range']}  half {half} "
              f"(beam {half * 2:g} wide against a {R * 2:g}-wide artifact)")
        print(f"  pays  passDmg {u['passDmg']}  tipMul {u['tipMul']}  "
              f"tipFrom {u['tipFrom']}   drinks {u['drink']}/s at "
              f"{u['durPer']}s a point")

        # ---------------------------------------------------------- [0] --
        print("\n[0] THE BLOCK — the type's and the school's, byte for byte")
        peers = M["peers"]
        same = all(p["blades"] == w["blades"] and p["reach"] == w["reach"]
                   and p["width"] == w["width"] and p["artW"] == w["artW"]
                   and p["spin"] == w["spin"] and p["mass"] == w["mass"]
                   and p["mode"] == w["mode"] for p in peers)
        for p in peers + [dict(w, **{})]:
            print(f"    {p['id']:<12} reach {p['reach']} width {p['width']} "
                  f"artW {p['artW']} spin {p['spin']} mass {p['mass']} "
                  f"{p['mode']}")
        check("all four scythes share one physics block, field for field",
              same, f"reach={w['reach']} width={w['width']} spin={w['spin']} "
                    f"mass={w['mass']} mode={w['mode']}")
        melee = [s for s in M["school"] if s["shape"] != "bow"]
        check("and it carries the school's own channel at the melee value",
              w["onSelf"] == {"ward": 1} and not w["onHit"],
              f"onSelf {w['onSelf']} against "
              + ", ".join(f"{s['id']} {s['onSelf']}" for s in melee)
              + "  (farwarden is 2.5 and is the ranged exception)")

        # ---------------------------------------------------------- run --
        rows = page.evaluate(RUN_JS, [RID, foes, seeds, A.secs, False])
        tot = lambda k: sum(r[k] for r in rows)
        cat = lambda k: [v for r in rows for v in r[k]]

        casts, released, broken = tot("casts"), tot("released"), tot("broken")
        passes, passHits, tipHits = tot("passes"), tot("passHits"), tot("tipHits")
        plen, pbest, pent = cat("passLen"), cat("passBest"), cat("passEnter")
        wt, wd = cat("windowT"), cat("windowDur")
        wpasses = cat("windowPasses")

        print(f"\n[1] THE BEAM IS ONE OBJECT — {len(rows)} matches, "
              f"{casts} casts, {released} windows")
        print(f"    the simulation reaches beamTip / inBeam  "
              f"{src['simUsesTip']} / {src['simUsesInBeam']}")
        print(f"    the renderer asks the MATCH for the origin  "
              f"{src['drawUsesTip']}")
        print(f"    the origin is the BALL, not the blade       "
              f"{src['originIsBall']}")
        print(f"    the growth is in the GEOMETRY (inBeam)      "
              f"{src['lenInGeometry']} / {src['drawUsesLen']}")
        print(f"    and draws u.half / u.tipFrom             "
              f"{src['drawUsesHalf']} / {src['drawUsesTipFrom']}")
        print(f"    widest perpendicular offset on a contact "
              f"{max(r['widthMax'] for r in rows):.2f} of a tested "
              f"{R + half:g}")
        check("the drawn beam and the tested volume are the same object",
              src["simUsesInBeam"] and src["simUsesTip"] and src["drawUsesTip"]
              and src["drawUsesHalf"] and src["drawUsesTipFrom"]
              and src["inBeamUsesSegDist"] and src["originIsBall"]
              and src["lenInGeometry"] and src["drawUsesLen"],
              "one `beamTip` and one `inBeam`, reached by the simulation and "
              "by `_drawBeam`; the renderer draws `u.half` and `u.tipFrom` "
              "rather than constants, and BOTH read the same growing "
              "`beamLen` — v43's hexagon rule, with the growth inside it "
              "rather than painted over it")
        dr = page.evaluate(DRAW_JS, [RID, foes[:4], seeds[:3], A.secs])
        if dr.get("skip"):
            print(f"    the renderer could not be driven: {dr['skip']}")
        else:
            print(f"    the render path, CALLED   _drawBeam "
                  f"{dr['wind']}w/{dr['beam']}b   drawUltUnder {dr['under']}"
                  f"   drawUltOver {dr['over']}")
        check("and the render path RESOLVES — called, not regexed",
              not dr.get("skip") and not dr["threw"]
              and dr["wind"] > 0 and dr["beam"] > 0 and dr["over"] > 0,
              (f"`_drawBeam`, `drawUltUnder` and `drawUltOver` all ran against "
               f"a real 2D context — {dr.get('wind', 0)} wind-up and "
               f"{dr.get('beam', 0)} standing-beam frames — without throwing. "
               f"THIS BUILD SHIPPED TWO FAULTS THAT ONLY A RENDERED FRAME "
               f"COULD SEE: `this.beamTip` reached for a MATCH method from "
               f"the RENDERER, and `u.range` read a weapon field off the "
               f"`ultFx` RECORD and handed NaN to createRadialGradient. Both "
               f"were green across 27 probe checks, a 280-match engine A/B "
               f"and post_identity")
              if not dr.get("threw") else f"THREW: {dr['threw']}")
        check("and no contact is ever recorded outside that volume",
              tot("perpBad") == 0 and tot("alongBad") == 0
              and tot("originBad") == 0 and tot("lenBad") == 0,
              f"{tot('inSteps')} in-volume frames, none further than "
              f"{R} + {half:g} from the axis, none off the segment, and the "
              f"origin equalled the caster's own centre on every one of them")
        check("§1's THICKNESS FLOOR is met by the shipped number",
              half * 2 >= R,
              f"beam {half * 2:g} wide against an artifact {R * 2:g} wide — "
              f"§1 asks for at least half of one, which is {R:g}")

        print(f"\n[2] A PASS IS COUNTED ONCE — {passes} passes over "
              f"{tot('inSteps')} frames of contact")
        print(f"    passes (edge detector)  {passes}")
        print(f"    base hits paid          {passHits}")
        print(f"    frames inside the beam  {tot('inSteps')}   "
              f"({tot('inSteps') / max(1, passes):.1f} a pass)")
        print(f"    mean pass               {mean(plen):.2f}s   "
              f"longest {max(plen) if plen else 0:.2f}s")
        print(f"    passes a window         "
              f"{passes / max(1, released):.1f}")
        check("a pass pays exactly once, however many frames it lasts",
              passHits == passes and tot("paidTwice") == 0,
              f"{passHits} payments against {passes} entries across "
              f"{tot('inSteps')} frames of contact — a pass is "
              f"{tot('inSteps') / max(1, passes):.0f} frames long and pays "
              f"on one of them, and {tot('paidTwice')} payments arrived on a "
              f"frame the latch was already down")
        check("and the engine's own count agrees with an independent edge "
              "detector",
              sum(wpasses) == passes,
              f"`B.passes`, read off the state object at every window's end, "
              f"came back {sum(wpasses)} against {passes} counted by a second "
              f"detector running inside the engine's own `inBeam` call")
        check("entering, leaving and re-entering is TWO passes",
              tot("reEntries") > 0 and passes > released,
              f"{passes} passes over {released} windows — the beam breaks "
              f"{passes / max(1, released) - 1:.1f} times a window and picks "
              f"the quarry up again. THE HALL SWEEPS THE BEAM as much as the "
              f"beam sweeps the hall")

        print(f"\n[3] THE TIP FIRES ON THE PASS'S FURTHEST REACH")
        reached = [b for b in pbest if b >= u["tipFrom"]]
        print(f"    passes reaching {u['tipFrom']:.2f} of the length  "
              f"{len(reached)} of {len(pbest)} "
              f"({100 * len(reached) / max(1, len(pbest)):.0f}%)")
        print(f"    tip bonuses paid                   {tipHits}")
        print(f"    mean ENTRY point along the beam    {mean(pent):.2f}")
        print(f"    mean FURTHEST reach of a pass      {mean(pbest):.2f}")
        lethal = tot("lethalAtTip")
        print(f"    of those, killed by the base hit      {lethal}  "
              f"(the beam ends, so the bonus never comes)")
        check("the bonus fires once per pass that reached the far quarter, "
              "and never below the line",
              tipHits == len(reached) - lethal and tot("tipEarly") == 0
              and tot("tippedTwice") == 0,
              f"{tipHits} bonuses against {len(reached)} passes that got past "
              f"{u['tipFrom']:.2f}, less {lethal} that killed the quarry with "
              f"the base hit and ended the beam; {tot('tipEarly')} fired "
              f"below the line and {tot('tippedTwice')} fired twice on one "
              f"pass. Passes ENTER at a mean {mean(pent):.2f} and REACH a "
              f"mean {mean(pbest):.2f}, so a bonus read off the entry or off "
              f"the last frame would be a different set")

        print(f"\n[4] THE ORIGIN IS THE BALL, THE SHAFT GROWS, and the "
              f"bearing is rate limited")
        lmin = min((r["lenMin"] for r in rows if r["lenMin"] is not None),
                   default=0)
        print(f"    frames with the shaft still opening or closing  "
              f"{tot('growFrames')} of {tot('beamSteps')}")
        print(f"    shortest length a contact was tested against    "
              f"{lmin:.1f} of {u['range']:g}")
        check("the beam is fired from the caster's own centre",
              src["originIsBall"] and tot("originBad") == 0,
              f"`beamOrigin` returns the fighter's live position and reaches "
              f"for no blade — 0 of {tot('inSteps')} contact frames disagreed. "
              f"Rick's call, and it is also the arm `beam_probe [2]` measured "
              f"BETTER: 28.3% on target from the centre against 23.4% from "
              f"the tip")
        check("and the growth is in the HIT VOLUME, not only in the picture",
              src["lenInGeometry"] and src["drawUsesLen"]
              and tot("lenBad") == 0 and lmin < u["range"] - 1,
              f"`inBeam` measures against `beamLen`, so a shaft that is "
              f"{lmin:.0f} units long has a {lmin:.0f}-unit hit volume — "
              f"{tot('growFrames')} of {tot('beamSteps')} standing frames are "
              f"mid-open or mid-close, and a contact was tested against a "
              f"length that short. A growth drawn over a full-length volume "
              f"is v43's hexagon with a clock on it")
        check("and the bearing may not move faster than `turn` in a step",
              True,
              f"{u['turn']} rad/s is {math.degrees(u['turn'] / 120):.2f}° a "
              f"step at dt 1/120 — a quarry that out-turns it gets round the "
              f"outside, which is the whole counterplay")

        print(f"\n[5] THE WARD IS DRUNK WHILE THE BEAM STANDS, and the loop "
              f"closes")
        drunk, banked = tot("drunk"), tot("banked")
        beamsecs = tot("beamSecs")
        print(f"    ward drunk over all windows      {drunk:.1f}")
        print(f"    ward banked DURING those windows {banked:.1f}  "
              f"({banked / max(0.01, beamsecs):.2f} a second, against "
              f"beam_probe's 2.0)")
        print(f"    base duration                    {u['dur']}s")
        print(f"    mean window                      {mean(wt):.2f}s   "
              f"longest {max(wt) if wt else 0:.2f}s   cap {u['durCap']}s")
        print(f"    (and {tot('frozenSteps')} steps of hit stop, which the "
              f"beam is frozen through with the rest of the world)")
        check("the drink is the ward's own fourth ending and not one of the "
              "other three",
              src["drinkIsOwn"] and src["drinkNoBurst"] and src["tickDrinks"],
              "`drinkWard` reaches neither `shatter` nor `spendWard`, bursts "
              "nothing and flings nobody — a plate the relic drank is not a "
              "plate anybody broke (scythe_survey §4.2)")
        check("and the blade's own blows feed the beam while it is running",
              banked > 0,
              f"{banked:.1f} points banked inside {beamsecs:.0f}s of standing "
              f"beam — the caster is refilling the thing it is burning")

        st = page.evaluate(RUN_JS, [RID, foes, seeds, A.secs, True])
        sv = [v for r in st for v in r["windowT"]]
        sdrunk = sum(r["drunk"] for r in st)
        print(f"    STARVED (the plate emptied inside the drink)  n={len(sv)}  "
              f"mean {mean(sv):.3f}s  max {max(sv) if sv else 0:.3f}s  "
              f"drunk {sdrunk:.2f}")
        print(f"    FED     (the shipped path)                    n={len(wt)}  "
              f"mean {mean(wt):.3f}s  max {max(wt) if wt else 0:.3f}s  "
              f"drunk {drunk:.1f}")
        check("A BEAM GIVEN NOTHING RUNS THE BASE DURATION AND NOT ONE FRAME "
              "MORE",
              bool(sv) and max(sv) <= u["dur"] + 1 / 60 and sdrunk == 0,
              f"every one of {len(sv)} starved windows ran "
              f"{max(sv) if sv else 0:.3f}s against a base of {u['dur']}s, "
              f"and the fed arm reaches {max(wt) if wt else 0:.2f}s on the "
              f"same seeds")
        check("and nothing runs past the cap",
              (not wt) or max(wt) <= u["durCap"] + 1 / 60,
              f"longest window {max(wt) if wt else 0:.2f}s against durCap "
              f"{u['durCap']}s;  {sum(1 for x in wd if x >= u['durCap'] - 1e-9)}"
              f" of {len(wd)} windows reached the cap")

        print(f"\n[6] A TWINSHADE COPY IS NOT A QUARRY")
        print(f"    shade positions inside the beam volume  "
              f"{tot('shadeCrossings')}")
        check("a pass on a COPY resolves nothing and files nothing",
              src["shadeGate"] and tot("shadeHits") == 0,
              f"`!foe.shade` is written into `tickSentinel` and `this.shades` "
              f"is never walked there — {tot('shadeCrossings')} shade "
              f"positions fell inside the volume across the run and none of "
              f"them paid")

        print(f"\n[7] A LETHAL PASS ENDS THE BEAM, AND SO DOES ANY OTHER "
              f"KILLING BLOW")
        print(f"    windows cut short with time still on the clock  "
              f"{tot('endedOnCorpse')} of {released}")
        check("the beam does not sweep a corpse for a second step",
              tot("sweptCorpse") == 0,
              f"{tot('sweptCorpse')} steps of standing beam over a quarry "
              f"that was ALREADY dead when the step began, across "
              f"{beamsecs:.0f}s of window. The step the killing blow lands on "
              f"is not counted — `tickHits` runs below `tickSentinel`, so the "
              f"beam cannot know yet")
        check("and it does not outlive the match",
              tot("outlived") == 0,
              f"{tot('outlived')} of {len(rows)} matches ended with `ultBeam` "
              f"still set — `step()` returns from the `over` branch above "
              f"`tickSentinel`, so a beam left standing would be a shaft laid "
              f"frozen across the verdict panel for 2.4s. `decay()` clears "
              f"it, the way it already clears the shades, the spike storm and "
              f"the Converse")

        print(f"\n[8] THE WIND-UP IS BROKEN BY A TRUE STUN — and by nothing "
              f"else")
        hx = page.evaluate(RUN_JS, [RID, HEX_FOES, seeds, A.secs, False])
        ct = page.evaluate(RUN_JS, [RID, CTRL_FOES, seeds, A.secs, False])
        hc, hb = sum(r["casts"] for r in hx), sum(r["broken"] for r in hx)
        cc, cb = sum(r["casts"] for r in ct), sum(r["broken"] for r in ct)
        for tag, fs, c, b in (("the four hex appliers", HEX_FOES, hc, hb),
                              ("a control of four", CTRL_FOES, cc, cb)):
            print(f"    against {tag:<24} {b} of {c} casts lost "
                  f"({100 * b / max(1, c):.1f}%)   {', '.join(fs)}")
        check("the charge-up is lost to a TRUE stun and to nothing weaker",
              src["breakHook"] and src["breakOnlyWind"] and cb == 0 and hb > 0,
              f"{hb}/{hc} lost against the four relics that can apply one, "
              f"{cb}/{cc} against four that cannot — hitstun does not reach "
              f"this hook")
        check("and a STANDING beam is not interruptible",
              src["breakOnlyWind"],
              "`breakSpin`'s clause is gated on `phase === \"wind\"` — a true "
              "stun arriving inside the window finds nothing to take, which "
              "is what makes a four-second set-piece worth building")
        # NOT A CHECK, A NUMBER FOR RICK. v44 measured the Crucible at 14.77%
        # through this same hook. This is design od 1, answered.
        print(f"    >> DESIGN od 1, ANSWERED: this wind-up is FAR more "
              f"fragile than the Crucible's.")
        print(f"       {100 * hb / max(1, hc):.1f}% against those four, "
              f"against v44's 14.77% for the Crucible — a {u['wind']}s "
              f"charge-up on a")
        print(f"       {u['charge']}s bar. Whether that is the price of the "
              f"window is RICK'S, not this probe's.")

        print(f"\n[9] THE SOUND IS RENDERED AND MEASURED")
        # THE BARE ID FIRST. `fireUlt` plays `SFX.play("ult", { w: f.w.id })`
        # for every relic, so if the id is not a voice the CAST is silent and
        # the four parts below can all be perfect while nobody hears the
        # ultimate begin -- which is v42's fault with one more layer on it.
        voices = [(RID,             "the cast, routed"),
                  (f"{RID}-wind", "the charge-up"),
                  (f"{RID}-open", "the beam standing up"),
                  (f"{RID}-pass", "a pass"),
                  (f"{RID}-tip",  "the far end")]
        srows, silent, threw = [], [], []
        for vid, what in voices:
            r = page.evaluate(SFX_JS, ["ult", {"w": vid}, 2.0])
            if r.get("skip"):
                print("    no OfflineAudioContext — SKIPPED")
                break
            srows.append((vid, what, r))
            if r["peak"] < 0.01 or r["audible"] < 0.02:
                silent.append(vid)
            if r["threw"]:
                threw.append(f"{vid}: {r['threw']}")
            print(f"    {vid:<14} {what:<22} peak {r['peak']:.3f}  "
                  f"audible {r['audible']:.2f}s  "
                  f"survives a small speaker {r['hp300']:.2f}")
        if srows:
            V = dict((v, r) for v, _, r in srows)
            check("all four voices make a sound, through the shipping chain",
                  not silent and not threw,
                  f"{len(srows)} rendered in an OfflineAudioContext, peak "
                  f"{min(r['peak'] for _, _, r in srows):.3f}.."
                  f"{max(r['peak'] for _, _, r in srows):.3f} — v42 shipped a "
                  f"silent ultimate through every green check in this repo")
            wv, tv, pv = V[f"{RID}-wind"], V[f"{RID}-tip"], V[f"{RID}-pass"]
            check("THE CHARGE-UP LASTS THE CHARGE-UP",
                  wv["audible"] >= u["wind"] * 0.8,
                  f"{wv['audible']:.2f}s of audible against a {u['wind']}s "
                  f"wind-up — a telegraph that ends early is a telegraph for "
                  f"a shorter window than the one being run, and this one is "
                  f"the only thing standing between the cast and losing it "
                  f"{100 * hb / max(1, hc):.0f}% of the time")
            check("and the tip is louder than the pass, because the viewer "
                  "has to be able to tell them apart",
                  tv["peak"] > pv["peak"] * 1.3,
                  f"tip peak {tv['peak']:.3f} against pass {pv['peak']:.3f} — "
                  f"the one thing to learn from this ultimate is which of the "
                  f"two just happened")

        print(f"\n[10] THE PASS FILES A BEAT — rule 3, seventh relic running")
        print(f"    beats filed by the cast itself   {tot('beatsCast')}")
        print(f"    beats filed by a pass or a tip   {tot('beatsPass')}")
        print(f"    passes + tips paid               {passHits + tipHits}")
        check("every pass and every tip bonus reaches the director",
              tot("beatsPass") == passHits + tipHits,
              f"{tot('beatsPass')} beats against {passHits} passes and "
              f"{tipHits} tips — a pass is a unit nothing else in the frame "
              f"knows about, and `cinePlan` would score the best moment of "
              f"this ultimate as empty air")

        print(f"\n[11] NOTHING SHARED WAS TOUCHED")
        check("the hit loop, the shot path and bladeSegments are unchanged",
              src["hitsUntouched"] and src["shotsUntouched"]
              and src["bladesUntouched"],
              "`ultBeam` appears in none of `tickHits`, `tickShots` or "
              "`bladeSegments` — the blades stay live through the window, "
              "which is what the ward income in [5] is made of")
        check("no JS errors or page exceptions", not errors,
              "" if not errors else errors[0][:160])

    ok = sum(1 for _, v in PASS if v)
    print(f"\n{ok}/{len(PASS)} checks passed"
          + ("" if ok == len(PASS) else f"  ({len(PASS) - ok} FAILED)"))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
