#!/usr/bin/env python3
"""CORONA, ASSERTED AGAINST THE BUILD -- one check per sentence of the brief.

    python corona_relic_probe.py --game ../02-chain/sc-ring.html

`06-docs/v66/STARWARDEN-BUILD-BRIEF.md` sections 1 and 2. The checks that
belong to a stage that has not been built yet SKIP rather than fail, and say
so -- a probe that reports a defect for an absent mechanic is a probe nobody
reads by stage 4.

  [1]  THE WINDOW opens on the charge, closes on `dur`, never two at once, and
       never outlives its caster or the match
  [2]  THE RING'S RATE -- dwell, crossings, ticks and stacks a cast, against
       the design's own table. REPORTED EVERY RUN
  [3]  THE BURN IS UNCAPPED. The peak is above every other status's ceiling in
       this game and below `maxStacks`
  [4]  THE BURN TICKS `hp` DIRECTLY and the quarry's shield does not absorb it
  [5]  THE FEED LANDS ON THE APPLIER -- burn applied by A moves A's ward and
       nobody else's, at `STATUS.ward.bank` of the tick, capped at `ward.cap`
  [6]  A STATUS WITH NO SOURCE PAYS NOBODY -- hemorrhage and smite are
       unchanged, which is what makes `apply`'s third argument inert
  [7]  FOE ONLY. The caster is never burned by its own ring and never hurt by
       its own ticks
  [8]  ZERO BURDEN. In a match with no Starwarden in it, `ultCorona` is null on
       every frame and no fighter ever carries a burn
  [9]  DETERMINISM. One seed, twice, bit-identical -- the ring, the burn and
       the feed draw from nothing but the clock
  [10] THE SHOWER -- bookkeeping per fight: spawned = touched + chained + alive
       (stage 3)
  [11] THE CHAIN -- top to bottom, one every `gap`, and no cast opens under a
       running one (stage 4)
  [P]  the render path is CALLED against a real 2D context, in every state

## WHY [5] AND [6] ARE TWO CHECKS AND NOT ONE

CORONA is the first thing in this game whose STATUS TICKS pay somebody. The
plumbing for that is a `src` on the status and one new branch in `tickStatus`,
and both of them sit on the path every bleed and every smite in the game runs
down. So [5] asserts the new behaviour and [6] asserts the ABSENCE of it
everywhere else, in a bloodsworn match with no vigil relic in it -- because the
failure that matters is not "the feed does not work", it is "every bleed in the
game now feeds somebody".

## AND THE COUNTERS ARE READ OFF THE ENGINE, NOT RECOMPUTED

`gravemourn_relic_probe` reported three defects that were not there, all three
because the probe wrote down its own model of a rule the engine legitimately
implements differently. So the ring's geometry is never re-derived here: what
[2] reports is what `tickCorona` itself counted, and [1] asks what the window
DID rather than what it should have done.

A CHECK THAT COUNTS FRAMES IN WHICH AN EVENT IS POSSIBLE IS NOT COUNTING THE
EVENT -- five times in one file in v60, three more in v59. Every count below is
of a transition or of a value the engine wrote.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

RID = "starwarden"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  - {detail}" if detail else ""))


def skip(name, why):
    print(f"  SKIP  {name}  - {why}")


META_JS = r"""([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const P = AC.Match.prototype;
  /* THE BLOCK COMMENT IS REMOVED AS A BLOCK. This codebase teaches in its
     comments and every string below appears in the paragraph explaining it --
     `curse_check` fired on its own explanation once. */
  const strip = f => f.toString().replace(/\/\*[\s\S]*?\*\//g, "")
                                 .replace(/\/\/[^\n]*/g, "");
  const tc = P.tickCorona ? strip(P.tickCorona) : "";
  const ts = strip(P.tickStatus);
  const R = AC.renderer.constructor.prototype;
  return {
    u: JSON.parse(JSON.stringify(w.ult)),
    burn: AC.STATUS.burn ? JSON.parse(JSON.stringify(AC.STATUS.burn)) : null,
    ward: JSON.parse(JSON.stringify(AC.STATUS.ward)),
    dmg: w.dmg, aff: w.aff, shape: w.shape,
    onSelf: JSON.parse(JSON.stringify(w.onSelf || {})),
    relics: AC.WEAPONS.length,
    has: {
      tick: !!P.tickCorona,
      ring: /coronaRing/.test(tc),
      /* THE SHOWER IS DETECTED ON ITS OWN METHODS AND NOT IN `tickCorona`'s
         TEXT. The first cut grepped the ticker for `stars.push`, which lives
         in `coronaPop` -- so it reported "stage 3 is not in this build" on a
         build that has it and SKIPPED the bookkeeping invariant the design
         asks for. A capability check that looks in the wrong place does not
         fail, it goes quiet. */
      star: !!P.coronaPop && !!P.coronaFly,
      chain: /C\.chain\.shift\(\)/.test(tc),
      draw: !!R.drawCorona,
      stBurn: !!R._stBurn,
    },
    src: {
      /* the cast resolves nothing: no damage and no apply on the ult block */
      castIsEmpty: !w.ult.dmg && !w.ult.apply,
      kindIsCorona: w.ult.kind === "corona",
      /* the window is per-FIGHTER, never on the match */
      perFighter: /ultCorona/.test(tc) && !/this\.corona\b/.test(tc),
      /* and the art hangs off the fighter, which is v54 2a / open item 25 */
      artOnFighter: R.drawCorona
        ? /ultCorona|coronaFade/.test(strip(R.drawCorona)) : false,
      /* the feed reads the ward's own share rather than a second copy of it */
      feedIsWardBank: /W\.bank/.test(ts),
      /* nothing in the ultimate draws from the match's stream */
      noRng: !/this\.rng\(\)/.test(tc),
      noRandom: !/Math\.random/.test(tc),
    },
  };
}"""


# ONE INSTRUMENTED MATCH PER (foe, seed). Every hook forwards with `arguments`
# -- v44's warning: a wrapper with a FIXED ARITY silently measures the old
# build the moment the build grows a parameter.
RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.WEAPONS.find(x => x.id === rid), U = W.ult;
  const A = { fights: 0, casts: 0, closed: 0, doubleOpen: 0, deadWindow: 0,
              overWindow: 0, longest: 0,
              ringF: 0, entries: 0, ticks: 0, stacks: 0, dmg: 0,
              pops: 0, spawned: 0, touched: 0, chained: 0, chainHit: 0,
              refused: 0, bookBad: 0, leftover: 0,
              burnDealt: 0, burnBanked: 0, casterBurn: 0, casterHurt: 0,
              casterShatter: 0,
              peak: 0, overCap: 0, capHit: 0, chainGapBad: 0, chainOrderBad: 0,
              castUnderChain: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      A.fights++;
      let step = 0, wasOpen = false, t0 = 0;
      /* [7]'s SECOND HALF, AND IT IS MEASURED ACROSS `tickCorona` AND NOTHING
         ELSE. A blade blow landing on the same step legitimately moves the
         caster's own hp -- three checks in `gravemourn_relic_probe` failed
         exactly that way by photographing a wider span than their own claim. */
      let inTick = false, shattered = 0;
      /* AND THE ONE THING THAT CAN LEGITIMATELY HURT THE CASTER INSIDE ITS OWN
         TICK IS A WARD IT BROKE. `hurt` absorbs into the quarry's plate first
         and calls `shatter` when the pool empties -- and a shatter is a BLAST,
         which catches whoever is standing next to it. This relic is a contact
         hazard, so the caster is standing next to it by construction. The
         first cut of [7] asserted "the caster's hp never moves inside the
         tick" and reported that as a defect; it is `hurt`'s own downstream
         behaviour and not Corona touching its caster. Counted rather than
         assumed. */
      const oShat = m.shatter.bind(m);
      m.shatter = function(){
        if (inTick) shattered++;
        return oShat.apply(m, arguments);
      };
      const oTick = m.tickCorona ? m.tickCorona.bind(m) : null;
      if (oTick) m.tickCorona = function(){
        inTick = true;
        const hp0 = me.hp;
        const sh0 = shattered;
        try { return oTick.apply(m, arguments); }
        finally {
          inTick = false;
          if (me.hp !== hp0){
            if (shattered > sh0) A.casterShatter++; else A.casterHurt++;
          }
          /* [1] IS ASKED HERE AND NOT AFTER `m.step`, AND THE FIRST CUT OF IT
             WAS WRONG THE WAY THIS REPO'S PROBES ARE ALWAYS WRONG. The ticker
             runs BEFORE `tickHits` and `checkEnd`, so a fight that ends on
             this step leaves a window standing on a frame the ticker never saw
             -- and reading it after the step reported 12 "windows that
             outlived the match" that the engine clears on its next call. A
             CHECK THAT COUNTS FRAMES IN WHICH AN EVENT IS POSSIBLE IS NOT
             COUNTING THE EVENT. What the engine promises is that the window
             does not SURVIVE a tick it should have been cleared by. */
          if (me.ultCorona && !me.alive) A.deadWindow++;
          if (me.ultCorona && m.over) A.overWindow++;
        }
      };
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const C = me.ultCorona;
        if (C && !wasOpen){ A.casts++; t0 = C.t; }
        if (C){
          if (th.ultCorona) A.doubleOpen++;
          /* THE DEAD-WINDOW AND OVER-WINDOW COUNTS ARE NOT TAKEN HERE, AND THE
             FIRST CUT OF THIS PROBE TOOK THEM HERE AND REPORTED FOUR DEFECTS
             THAT DO NOT EXIST. `tickCorona` runs before `tickHits` and
             `checkEnd`, so a caster killed later in the same step leaves a
             window standing on a frame the ticker never saw -- and the ticker
             clears it on its very next call. They are counted in the wrapper
             above, where the question is the one the engine actually answers:
             did a window SURVIVE a tick that should have cleared it? Measured
             separately over twelve fights with a standalone trace: ZERO. */
          A.longest = Math.max(A.longest, C.t);
          if (C.chain && C.chain.length && C.t < C.dur) A.castUnderChain++;
        }
        if (!C && wasOpen){
          A.closed++;
        }
        wasOpen = !!C;
        /* THE COUNTERS ARE THE ENGINE'S OWN and they are read on the LAST
           frame the window exists, because the window is nulled from inside
           the tick and a read after that is a read of nothing. */
        if (C) A.last = { ringF: C.ringF, entries: C.entries, ticks: C.ticks,
                          stacks: C.stacks, dmg: C.dmg, pops: C.pops,
                          spawned: C.spawned, touched: C.touched,
                          chained: C.chained, chainHit: C.chainHit,
                          refused: C.refused,
                          live: (C.stars ? C.stars.length : 0)
                              + (C.chain ? C.chain.length : 0) };
        else if (A.last){
          for (const k of ["ringF","entries","ticks","stacks","dmg","pops",
                           "spawned","touched","chained","chainHit","refused"])
            A[k] += A.last[k] || 0;
          A.leftover += A.last.live || 0;
          /* [10]. SPAWNED = TOUCHED + CHAINED + STILL ALIVE, per cast. The
             lab asserts this and so does this -- a star that is neither
             touched, chained nor standing has been dropped somewhere. */
          if ((A.last.spawned || 0) !==
              (A.last.touched || 0) + (A.last.chained || 0) + (A.last.live || 0))
            A.bookBad++;
          A.last = null;
        }
        const bn = th.stacks("burn");
        if (bn > A.peak) A.peak = bn;
        if (AC.STATUS.burn && bn > AC.STATUS.burn.maxStacks) A.overCap++;
        if (AC.STATUS.burn && bn === AC.STATUS.burn.maxStacks) A.capHit++;
        if (me.stacks("burn")) A.casterBurn++;
      }
      A.burnDealt += me.burnDealt || 0;
      A.burnBanked += me.burnBanked || 0;
    }
  }
  return A;
}"""


# [8]. THE ZERO BURDEN, and it is asked of a roster with no Starwarden in it.
IDLE_JS = r"""([rid, pairs, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const A = { fights: 0, frames: 0, windows: 0, burns: 0, fades: 0 };
  for (const [x, y] of pairs) for (const sd of seeds){
    const m = new AC.Match(x, y, sd);
    A.fights++;
    let step = 0;
    while (!m.over && step < secs / DT){
      m.step(DT); step++; A.frames++;
      for (const f of [m.a, m.b]){
        if (f.ultCorona) A.windows++;
        if (f.coronaFade > 0) A.fades++;
        if (f.stacks("burn")) A.burns++;
      }
    }
  }
  return A;
}"""


# [4], [5] AND [6] ARE DIRECTED, because the thing being asserted is a rule and
# not a rate. Three fighters' worth of state is set by hand and one step is
# taken: what a fight would give instead is a number that is usually right.
UNIT_JS = r"""([rid]) => {
  const DT = AC.CONFIG.physics.dt;
  const W = AC.STATUS.ward, B = AC.STATUS.burn;
  const out = {};
  /* [4] THE BURN SKIPS THE SHIELD. `hurt` absorbs into `shield` first; a `dps`
     status does not go through `hurt` at all, and this asserts that on a
     quarry sitting on a full plate rather than trusting the code path. */
  {
    const m = new AC.Match(rid, "emberedge", 991);
    const a = m.a, b = m.b;
    b.shield = 40; b.shieldMax = 40; b.apply("ward", 1);
    b.apply("burn", 10, a === m.a ? "a" : "b");
    const hp0 = b.hp, sh0 = b.shield;
    m.tickStatus(b, DT);
    out.burnHp = hp0 - b.hp;
    out.burnShield = sh0 - b.shield;
  }
  /* [5] THE FEED LANDS ON THE APPLIER, BOTH WAYS ROUND. Applied with src "a"
     it moves a; applied with src "b" it moves b. A build that banked on "the
     other fighter" passes the first of these and fails the second. */
  {
    const m = new AC.Match(rid, "emberedge", 992);
    const a = m.a, b = m.b;
    a.shield = 0; a.shieldMax = 0; b.shield = 0; b.shieldMax = 0;
    b.apply("burn", 8, "a");
    const hp0 = b.hp;
    m.tickStatus(b, DT);
    out.feedA = a.shield; out.feedAOther = b.shield;
    out.feedShare = a.shield / Math.max(1e-9, hp0 - b.hp);
  }
  {
    const m = new AC.Match(rid, "emberedge", 993);
    const a = m.a, b = m.b;
    a.shield = 0; a.shieldMax = 0; b.shield = 0; b.shieldMax = 0;
    a.apply("burn", 8, "b");
    m.tickStatus(a, DT);
    out.feedB = b.shield; out.feedBOther = a.shield;
  }
  /* AND IT IS CAPPED AT THE WARD'S OWN CEILING. */
  {
    const m = new AC.Match(rid, "emberedge", 994);
    const a = m.a, b = m.b;
    a.shield = W.cap - 0.2; a.shieldMax = a.shield;
    b.apply("burn", 60, "a");
    for (let i = 0; i < 60; i++) m.tickStatus(b, DT);
    out.feedCapped = a.shield;
  }
  /* [6] A STATUS WITH NO SOURCE PAYS NOBODY. Hemorrhage and smite are applied
     the way every relic in the game applies them -- two arguments -- and the
     assertion is that nothing anywhere gains a shield. */
  {
    const m = new AC.Match("widowmaker", "dawnbringer", 995);
    const a = m.a, b = m.b;
    a.shield = 0; a.shieldMax = 0; b.shield = 0; b.shieldMax = 0;
    b.apply("hemorrhage", 4); a.apply("smite", 4);
    for (let i = 0; i < 30; i++){ m.tickStatus(a, DT); m.tickStatus(b, DT); }
    out.noSrcShield = a.shield + b.shield;
    out.noSrcHp = (a.maxHp - a.hp) + (b.maxHp - b.hp);
    out.noSrcField = (b.status.hemorrhage && b.status.hemorrhage.src === undefined)
                  && (a.status.smite && a.status.smite.src === undefined);
  }
  /* [3] UNCAPPED IS A NUMBER AND NOT AN ABSENCE. `apply` reads `maxStacks`, so
     the ceiling has to be provably far above anything the relic can reach. */
  {
    const m = new AC.Match(rid, "emberedge", 996);
    const b = m.b;
    for (let i = 0; i < 200; i++) b.apply("burn", 1, "a");
    out.stackCeiling = b.stacks("burn");
  }
  out.burnDef = B ? { maxStacks: B.maxStacks, dur: B.dur, dps: B.dps,
                      feed: !!B.feed, tip: B.tip } : null;
  out.wardBank = W.bank; out.wardCap = W.cap;
  return out;
}"""


# [9]. DETERMINISM, ON THIS BUILD, WITH THE ULTIMATE LIVE. `engine_ab` proves
# the OTHER relics did not move; nothing proves this one is reproducible except
# running it twice. A stray `Math.random` in a new object is invisible to every
# other check in this repo.
DET_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const run = () => {
    const out = [];
    for (const f of foes) for (const sd of seeds){
      const m = new AC.Match(rid, f, sd);
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
      out.push([m.a.hp, m.b.hp, m.a.x, m.a.y, m.b.x, m.b.y, step,
                m.winner ? (m.winner === m.a ? "a" : "b") : "-"].join(","));
    }
    return out.join("|");
  };
  const one = run(), two = run();
  return { same: one === two, n: one.split("|").length };
}"""


# [P]. THE RENDER PATH IS CALLED. v48: two picture faults shipped through every
# headless check in this repo and died on the FIRST RENDERED FRAME -- a
# renderer reaching for a Match method, and a NaN handed to
# `createRadialGradient`. The probe that was meant to catch the first one
# PASSED, because it was REGEXING the source for a name and a string does not
# resolve a reference. So this CALLS the functions against a real 2D context.
DRAW_JS = r"""([rid, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const cv = document.createElement("canvas");
  cv.width = 520; cv.height = 800;
  const ctx = cv.getContext("2d");
  const R = AC.renderer, saved = R.ctx;
  const seen = { open: 0, fade: 0, burn: 0, stars: 0, chain: 0 };
  let threw = null, frames = 0;
  try {
    for (const foe of ["emberedge", "axiom"]){
      const m = new AC.Match(rid, foe, seed);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const C = me.ultCorona;
        const burning = th.stacks("burn") > 0 || me.stacks("burn") > 0;
        if (!C && !(me.coronaFade > 0.01) && !burning) continue;
        if (C) seen.open++; else if (me.coronaFade > 0.01) seen.fade++;
        if (burning) seen.burn++;
        if (C && C.stars && C.stars.length) seen.stars++;
        if (C && C.chain && C.chain.length) seen.chain++;
        R.ctx = ctx;
        if (R.drawCorona){ R.drawCorona(m, false); R.drawCorona(m, true); }
        if (R._stBurn && th.stacks("burn"))
          R._stBurn(m, th, AC.CONFIG.physics.ballR, th.stacks("burn"));
        R.drawStatus(m, th);
        R.ctx = saved;
        frames++;
      }
    }
  } catch (e){ threw = String(e && e.stack || e); }
  R.ctx = saved;
  return { threw, frames, seen };
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-ring.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--foes", type=int, default=11,
                    help="how many of the roster to fight, strided across it")
    ap.add_argument("--secs", type=float, default=156.0)
    ap.add_argument("--json", default="")
    a = ap.parse_args()
    gp = resolve_game(a.game)
    seeds = [4177 + 31 * i for i in range(a.seeds)]

    print(f"\nCORONA - asserted against {gp.name}\n")
    with game(game_path=gp) as (page, errors):
        M = page.evaluate(META_JS, [RID])
        U, H, S = M["u"], M["has"], M["src"]
        B = M["burn"]
        print(f"  relic  {RID}  {M['aff']} x {M['shape']}  dmg {M['dmg']:g}  "
              f"onSelf {M['onSelf']}   roster {M['relics']}")
        print(f"  ult    {U['name']}  charge {U['charge']:g}  kind {U['kind']}  "
              f"dur {U['dur']:g}s")
        print(f"  ring   {U['A']:g} x {U['B']:g}  band {U['wd']:g}  "
              f"tilt {U['tilt']:g}  {U['rate']:g}/s x {U['tickDmg']:g}  "
              f"+{U['entry']:g} on entry, +{U['tickStacks']:g} a tick")
        if B:
            print(f"  burn   maxStacks {B['maxStacks']:g}  dur {B['dur']:g}s  "
                  f"dps {B['dps']:g}  feed {bool(B.get('feed'))}")
        print(f"  built  ring {H['ring']} · star {H['star']} · "
              f"chain {H['chain']} · draw {H['draw']} · burn art {H['stBurn']}")
        print()

        # THE FOES ARE SAMPLED ACROSS THE ROSTER, NOT OFF THE TOP OF IT. This
        # relic is a CONTACT hazard and its dwell is a property of who it is
        # fighting; the first eight ids in `WEAPONS` are five greatswords and a
        # flail, and read 0.61s of dwell where a stride over all 33 reads
        # nearer the design's 0.87. A biased foe list is not a smaller sample,
        # it is a different measurement.
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        pool = [i for i in ids if i != RID]
        k = max(1, len(pool) // a.foes)
        foes = pool[::k][:a.foes]
        print(f"  foes   {len(foes)} of {len(pool)}, stride {k}: "
              + ", ".join(foes) + "\n")

        # ------------------------------------------------------- structure --
        check("[S] the cast resolves nothing and the kind is its own",
              S["castIsEmpty"] and S["kindIsCorona"])
        check("[S] the window is PER-FIGHTER and the art hangs off it "
              "(open item 25)", S["perFighter"] and S["artOnFighter"])
        check("[S] the feed reads STATUS.ward.bank rather than a second copy "
              "of 0.55", S["feedIsWardBank"])
        check("[S] no Math.random and no this.rng() in the ultimate",
              S["noRandom"] and S["noRng"])

        # ------------------------------------------------------ [4] [5] [6] --
        Uu = page.evaluate(UNIT_JS, [RID])
        assert not errors, errors[:3]
        check("[4] the burn ticks hp DIRECTLY and the plate absorbs none of it",
              Uu["burnHp"] > 0 and abs(Uu["burnShield"]) < 1e-9,
              f"hp -{Uu['burnHp']:.4f}, shield moved {Uu['burnShield']:.4f}")
        share = Uu["feedShare"]
        check("[5] the feed lands on the APPLIER, both ways round, at "
              "ward.bank of the tick",
              Uu["feedA"] > 0 and Uu["feedAOther"] == 0
              and Uu["feedB"] > 0 and Uu["feedBOther"] == 0
              and abs(share - Uu["wardBank"]) < 1e-6,
              f"a +{Uu['feedA']:.4f} / b +{Uu['feedB']:.4f}, "
              f"share {share:.3f} against ward.bank {Uu['wardBank']:g}")
        check("[5] and it is capped at STATUS.ward.cap",
              Uu["feedCapped"] <= Uu["wardCap"] + 1e-9,
              f"{Uu['feedCapped']:.2f} of {Uu['wardCap']:g}")
        check("[6] hemorrhage and smite still pay NOBODY and carry no source",
              Uu["noSrcShield"] == 0 and Uu["noSrcHp"] > 0
              and Uu["noSrcField"],
              f"shield {Uu['noSrcShield']:g} after {Uu['noSrcHp']:.1f} "
              "damage of ordinary bleed and smite")
        check("[3] the burn is UNCAPPED in this engine's terms",
              B is not None and Uu["stackCeiling"] == B["maxStacks"]
              and B["maxStacks"] >= 99,
              f"200 applications reach {Uu['stackCeiling']:g}")

        # ------------------------------------------------- the fights [1][2] --
        A = page.evaluate(RUN_JS, [RID, foes, seeds, a.secs])
        assert not errors, errors[:3]
        casts = max(1, A["casts"])
        print(f"\n  {A['fights']} fights, {A['casts']} casts "
              f"({A['casts'] / max(1, A['fights']):.2f} a fight)\n")
        # A WINDOW STILL STANDING WHEN THE FIGHT ENDED IS NOT AN UNCLOSED ONE.
        # At most one per fight can be in that state, which is what the first
        # clause says; anything above that is a window that was dropped.
        check("[1] every window that opened closed, none opened twice at once, "
              "and none survived a tick it should not have",
              A["casts"] - A["closed"] <= A["fights"] and A["doubleOpen"] == 0
              and A["deadWindow"] == 0 and A["overWindow"] == 0,
              f"opened {A['casts']}, closed {A['closed']}, "
              f"{A['casts'] - A['closed']} still open at the bell, "
              f"double {A['doubleOpen']}, dead {A['deadWindow']}, "
              f"over {A['overWindow']}, "
              f"longest {A['longest']:.2f}s of {U['dur']:g}")
        check("[7] FOE ONLY -- the caster is never burned by its own ring, "
              "and nothing in the tick hurts it except a ward it broke",
              A["casterBurn"] == 0 and A["casterHurt"] == 0,
              f"{A['casterShatter']} frames of blast from a plate the ring "
              "popped, which is `hurt`'s own downstream behaviour")
        check("[3] the peak sits above every other status's ceiling and under "
              "maxStacks", A["overCap"] == 0 and A["peak"] > 6,
              f"peak {A['peak']} stacks, cap reached on {A['capHit']} frames")

        # THE COLUMN IT IS READ AGAINST IS THE ARM THAT WAS BUILT. Arm B is
        # the ring alone (stage 2) and arm D is the whole ultimate (stage 4);
        # printing D's numbers next to a stage-2 build would report a relic
        # missing two thirds of its fire as broken.
        whole = H["star"] and H["chain"]
        D = ((0.82, 5.6, 33.9, 5.8, 20.5, 11.2, 49) if whole
             else (0.87, 5.7, 12.0, 6.3, 6.3, 3.4, 20))
        dwell = A["ringF"] / 120 / casts
        print(f"\n  [2] PER CAST -- against the design's own table (section "
              f"10), arm {'D, the whole' if whole else 'B, the ring alone'}")
        print("      (and the burn's dps is the build's own number, so the "
              "damage and\n       shield rows scale with it -- the design's "
              "column is at 0.10)\n")
        print(f"      dwell        {dwell:5.2f}s   design {D[0]}")
        print(f"      crossings    {A['entries'] / casts:5.2f}    design {D[1]}")
        print(f"      ring ticks   {A['ticks'] / casts:5.2f}")
        print(f"      burn stacks  {A['stacks'] / casts:5.2f}    design {D[2]}")
        print(f"      ring damage  {A['dmg'] / casts:5.2f}    design {D[3]}")
        print(f"      burn damage  {A['burnDealt'] / casts:5.2f}    design {D[4]}")
        print(f"      shield       {A['burnBanked'] / casts:5.2f}    design {D[5]}")
        print(f"      peak stacks  {A['peak']:5.0f}      design {D[6]}\n")
        # AND THIS ONE IS A GATE ONLY AT THE FULL ROSTER, because it is the
        # design's table it is being read against and the design's table is on
        # all 33 foes. THE DWELL IS A PROPERTY OF WHO THIS RELIC IS FIGHTING --
        # it is a CONTACT hazard -- so a strided sample does not read the same
        # number: the 8-foe stride gives 0.51s, the 11-foe 0.61s, the design's
        # 33 gives 0.82. The first cut of this gated at any sample size and
        # FAILED on the build of record for no reason but `--foes 8`, on a
        # build byte-identical in every line the check touches (measured: the
        # pre-merge build reads 0.51s on the same sample). A CHECK THAT FIRES
        # ON ITS OWN CONFIGURATION IS NOT A CHECK.
        full = len(foes) >= len(pool)
        if full:
            check("[2] the ring's dwell and crossing rate are the design's, "
                  "within a quarter",
                  0.6 <= dwell <= 1.15 and 4.0 <= A["entries"] / casts <= 7.5,
                  f"{dwell:.2f}s in {A['entries'] / casts:.2f} crossings")
        else:
            skip("[2] the dwell against the design's table",
                 f"{len(foes)} of {len(pool)} foes -- the design's 0.82s is on "
                 f"all of them, and dwell is a property of WHO this relic is "
                 f"fighting. Read {dwell:.2f}s as a shape, not a verdict; "
                 f"re-run with --foes {len(pool)} to gate it")
        check("[5] the shield banked is ward.bank of the burn dealt "
              "(less what the cap clipped)",
              A["burnBanked"] <= A["burnDealt"] * Uu["wardBank"] + 1e-6
              and A["burnBanked"] > 0,
              f"{A['burnBanked']:.1f} of {A['burnDealt'] * Uu['wardBank']:.1f} "
              "possible")

        # ------------------------------------------------------------ [10] --
        if H["star"]:
            check("[10] spawned = touched + chained + still alive, every cast",
                  A["bookBad"] == 0 and A["spawned"] > 0,
                  f"{A['spawned'] / casts:.1f} spawned, "
                  f"{A['touched'] / casts:.1f} touched, "
                  f"{A['chained'] / casts:.1f} chained a cast")
        else:
            skip("[10] the shower", "stage 3 is not in this build")
        if H["chain"]:
            check("[11] no cast opens under a running chain",
                  A["castUnderChain"] == 0)
        else:
            skip("[11] the chain", "stage 4 is not in this build")

        # ------------------------------------------------------------- [8] --
        pairs = [[foes[0], foes[1]], [foes[2], foes[3]], [foes[4], foes[5]]]
        I = page.evaluate(IDLE_JS, [RID, pairs, seeds[:3], a.secs])
        assert not errors, errors[:3]
        check("[8] zero burden: no window, no fade and no burn in a match "
              "without this relic",
              I["windows"] == 0 and I["burns"] == 0 and I["fades"] == 0,
              f"{I['frames']} frames over {I['fights']} fights")

        # ------------------------------------------------------------- [9] --
        D = page.evaluate(DET_JS, [RID, foes[:4], seeds[:3], a.secs])
        assert not errors, errors[:3]
        check("[9] determinism: the same seeds twice, bit-identical",
              D["same"], f"{D['n']} fights")

        # ------------------------------------------------------------- [P] --
        R = page.evaluate(DRAW_JS, [RID, seeds[0], a.secs])
        check("[P] the render path is CALLED against a real 2D context",
              R["threw"] is None and R["frames"] > 0,
              (R["threw"] or "") + f"  {R['frames']} frames  {R['seen']}")
        check("[P] and it is called in every state the build has",
              R["seen"]["open"] > 0 and R["seen"]["fade"] > 0
              and R["seen"]["burn"] > 0
              and (not H["star"] or R["seen"]["stars"] > 0)
              and (not H["chain"] or R["seen"]["chain"] > 0))

        assert not errors, errors[:3]

    ok = sum(1 for _, v in PASS if v)
    print(f"\n  {ok}/{len(PASS)} checks pass\n")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(
            {"meta": M, "run": A, "unit": Uu, "idle": I, "draw": R}, indent=1))
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
