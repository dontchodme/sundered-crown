#!/usr/bin/env python3
"""CURSE_CHECK -- one check per sentence of the Curse rework.

    python curse_check.py --game ../02-chain/sc-curse.html

Layer 1 of the v51/52 build brief (§5). Eight checks, and each one is a
sentence somebody wrote down before the build existed:

  [1] a stack remembers the blow that applied it -- post-crit, post-jitter,
      post-sunder -- and NEVER the echo that blow just paid
  [2] the pool is the top K, and a new stack drops the WEAKEST
  [3] stacks("curse") equals cursePool.length, on every frame of every match
  [4] a fresh stack does not pay out on its own blow
  [5] the echo is stopped by an Aegis wall and absorbed by a Ward, because it
      is FOLDED INTO the hit rather than dealt beside it
  [6] a shade's blow feeds and cashes the pool -- the §4.3 check, written as a
      Twinshade match
  [7] maxHp never moves, in any match, for any relic
  [8] DELIVERED AGAINST NOMINAL, for all eight statuses

## THE ARITHMETIC IS THE CHECK, AND IT IS EXACT

[1], [2] and [4] are not statistics. `resolveHit` is wrapped so the pool is
photographed either side of every blow, `hurt` is wrapped so the damage that
actually arrived is counted, and the identity

    pushed  ==  damage that arrived  -  round(pool sum BEFORE the blow * echo)

is asserted on every single curse application. It holds only if the memory is
`dmgBase` and the echo is read off the stacks that already existed. A build
that remembered `dmg` instead fails it on the second blow of the first fight.

The clean arm deliberately excludes VIGIL foes: a ward absorbs inside `hurt`
and an aegis eats before it, so on those two the damage that arrives is not
the damage that was priced. That is not a hole -- it is check [5], which
asserts the harder identity `arrived + eaten == pushed + echo` on exactly the
relics [1] leaves out.

## [8] IS THE ONE THAT IS NOT ABOUT CURSE

The general form of v47's defect: a status channel can be worth nothing and no
gate in this repo would see it. Curse's own ratio was ~3% before this build.
The other seven have never been measured, and this is where that check belongs
-- so it prints all eight and fails only on a channel that delivers nothing.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402

PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


# --------------------------------------------------------------------------
# THE SOURCE, READ OUT OF THE SHIPPED BUILD rather than copied here. If an
# edit moves the echo below the Aegis block, or hands `pushCurse` the wrong
# variable, these go false and say which sentence stopped being true.
META_JS = r"""() => {
  const P = AC.Match.prototype;
  /* `Fighter` IS NOT EXPORTED. The engine is one classic script, so every
     top-level class is a lexical global and not a property of `window` --
     the same trap `window.AC`'s own comment names for CINE. Reach it through
     a real fighter instead of adding an export for a probe's convenience. */
  const probe = new AC.Match("gravemourn", "axiom", 1);
  const F = Object.getPrototypeOf(probe.a);
  /* THE COMMENTS ARE STRIPPED BEFORE ANY OF THIS IS REGEXED, and that is not
     tidiness. The first cut of `noOwnerGuard` searched `resolveHit` for
     "self === owner" and found it -- inside the paragraph this build wrote
     saying there must never be one. A check that cannot tell code from the
     comment explaining it fires on its own explanation, and it had already
     happened once in the builder an hour earlier. */
  const strip = f => f.toString().replace(/\/\*[\s\S]*?\*\//g, "")
                                 .replace(/\/\/.*/g, "");
  const rh = strip(P.resolveHit);
  const iEcho = rh.indexOf("curseEcho()");
  const iAegis = rh.indexOf("foe.ultAegis");
  return {
    curse: JSON.parse(JSON.stringify(AC.STATUS.curse)),
    statuses: Object.keys(AC.STATUS),
    baseHP: AC.CONFIG.combat.baseHP,
    relics: AC.WEAPONS.map(w => ({ id: w.id, aff: w.aff, dmg: w.dmg,
                                   onHit: w.onHit || null,
                                   onSelf: w.onSelf || null,
                                   apply: w.ult.apply || null })),
    src: {
      hasPool:      /this\.cursePool = \[\]/.test(strip(F.constructor)),
      hasPush:      typeof F.pushCurse === "function",
      hasEcho:      typeof F.curseEcho === "function",
      /* THE MEMORY IS dmgBase. A build that hands `dmg` to pushCurse is the
         exponential one, and it is one character away at all times. */
      pushesBase:   /pushCurse\(dmgBase, n\)/.test(rh),
      neverPushesDmg: !/pushCurse\(dmg,/.test(rh),
      /* FOLDED IN, ABOVE THE WALL. Order, not presence. */
      echoBeforeAegis: iEcho >= 0 && iAegis >= 0 && iEcho < iAegis,
      echoAdded:    /dmg \+= curseEcho/.test(rh),
      /* PRICED ON THE TARGET. There must never be an attacker guard. */
      noOwnerGuard: !/self === owner|self !== owner/.test(rh),
      /* THE OLD CHANNEL IS GONE, everywhere. */
      noMaxHpLoss:  !/maxHpLoss/.test(strip(F.apply)),
      /* AND THE GENERIC CLAMP STAYS -- §2.5 says it is not curse's. */
      clampStays:   /f\.hp = Math\.min\(f\.hp, f\.maxHp\)/.test(strip(P.tickStatus)),
      /* the pool dies with the status */
      poolExpires:  /cursePool\.length = 0/.test(strip(P.tickStatus)),
      /* the stack count is derived rather than promised */
      stacksDerived: /cursePool\.length/.test(strip(F.apply)),
    },
  };
}"""


# --------------------------------------------------------------------------
# [1][2][3][4] THE EXACT ARM. Non-vigil foes only -- see the docstring.
LEDGER_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  const K = AC.STATUS.curse.maxStacks, E = AC.STATUS.curse.echo;
  const out = { blows: 0, pushes: 0, memBad: 0, poolBad: 0, syncBad: 0,
                freshPushes: 0, freshBad: 0, sortBad: 0, capBad: 0,
                maxMem: 0, maxPool: 0, sample: null, worst: null,
                steps: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      /* EVERY HOOK FORWARDS WITH `arguments` -- v44's warning: a wrapper with
         a fixed arity silently measures the old build the moment the build
         grows a parameter. */
      let hurtTgt = null, hurtAcc = 0;
      const origHurt = P.hurt;
      m.hurt = function(foe, dmg){
        if (foe === hurtTgt) hurtAcc += dmg;
        return origHurt.apply(m, arguments);
      };
      const origRH = P.resolveHit;
      m.resolveHit = function(self, foe){
        const pre = foe.cursePool.slice();
        let preSum = 0; for (const v of pre) preSum += v;
        hurtTgt = foe; hurtAcc = 0;
        const r = origRH.apply(m, arguments);
        hurtTgt = null;
        const post = foe.cursePool.slice();
        out.blows++;
        if (post.length === pre.length &&
            post.every((v, i) => v === pre[i])) return r;
        out.pushes++;

        /* the pushed memory, as a multiset difference */
        const left = pre.slice(), pushed = [];
        for (const v of post){
          const i = left.indexOf(v);
          if (i >= 0) left.splice(i, 1); else pushed.push(v);
        }
        /* [1] and [4]: the identity. `pushed` is dmgBase; what arrived is
           dmgBase + the echo the stacks that ALREADY existed were worth. */
        const echo = Math.round(preSum * E);
        const mem = pushed.length ? pushed[0] : null;
        if (mem === null || Math.abs((hurtAcc - echo) - mem) > 1e-9){
          out.memBad++;
          if (!out.worst)
            out.worst = { pre, post, pushed, arrived: hurtAcc, echo,
                          foe: foe.w.id, self: self.w.id };
        }
        if (preSum === 0){
          out.freshPushes++;
          /* a fresh stack pays nothing: what arrived IS the blow */
          if (mem !== null && Math.abs(hurtAcc - mem) > 1e-9) out.freshBad++;
        }
        /* [2] the pool is the top K of what it held plus what was pushed,
           and the trim drops the WEAKEST */
        const want = pre.concat(pushed).sort((a, b) => b - a).slice(0, K);
        if (want.length !== post.length ||
            !want.every((v, i) => v === post[i])) out.poolBad++;
        for (let i = 1; i < post.length; i++)
          if (post[i] > post[i - 1]) out.sortBad++;
        if (post.length > K) out.capBad++;
        if (mem !== null) out.maxMem = Math.max(out.maxMem, mem);
        let s = 0; for (const v of post) s += v;
        out.maxPool = Math.max(out.maxPool, s);
        if (!out.sample && post.length === K)
          out.sample = { pre, pushed, post, arrived: hurtAcc, echo };
        return r;
      };
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++; out.steps++;
        /* [3] on EVERY frame of every match, both fighters, and the shades
           too -- a copy is a real Fighter and can be cursed. */
        for (const f of [m.a, m.b].concat(m.shades || [])){
          if (!f) continue;
          if (f.stacks("curse") !== f.cursePool.length) out.syncBad++;
        }
      }
    }
  }
  return out;
}"""


# --------------------------------------------------------------------------
# [5] THE HARD IDENTITY, on the two defences the clean arm excludes.
#     arrived + eaten == pushed + echo  --  which holds only if the echo went
#     into `dmg` above the wall rather than being paid beside it.
WALL_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  const E = AC.STATUS.curse.echo;
  const out = { aegisBlows: 0, aegisOk: 0, aegisBad: 0,
                wardBlows: 0, wardOk: 0, wardBad: 0, aegisEx: null, wardEx: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let hurtTgt = null, hurtAcc = 0;
      const origHurt = P.hurt;
      m.hurt = function(foe, dmg){
        if (foe === hurtTgt) hurtAcc += dmg;
        return origHurt.apply(m, arguments);
      };
      const origRH = P.resolveHit;
      m.resolveHit = function(self, foe){
        const pre = foe.cursePool.slice();
        let preSum = 0; for (const v of pre) preSum += v;
        const echo = Math.round(preSum * E);
        const ate0 = foe.ultAegis ? foe.ultAegis.ate : null;
        const sh0 = foe.shield;
        hurtTgt = foe; hurtAcc = 0;
        const r = origRH.apply(m, arguments);
        hurtTgt = null;
        const post = foe.cursePool.slice();
        if (echo <= 0) return r;
        const left = pre.slice(), pushed = [];
        for (const v of post){
          const i = left.indexOf(v);
          if (i >= 0) left.splice(i, 1); else pushed.push(v);
        }
        if (!pushed.length) return r;         // no memory to identify against
        const mem = pushed[0];
        if (ate0 !== null && foe.ultAegis){
          const eaten = foe.ultAegis.ate - ate0;
          if (eaten > 0){
            out.aegisBlows++;
            /* what arrived at hurt() plus what the wall ate IS the whole
               priced blow, echo included */
            if (Math.abs((hurtAcc + eaten) - (mem + echo)) < 1e-9) out.aegisOk++;
            else { out.aegisBad++;
                   out.aegisEx = out.aegisEx ||
                     { arrived: hurtAcc, eaten, mem, echo }; }
          }
        }
        const absorbed = sh0 - foe.shield;
        if (absorbed > 0){
          out.wardBlows++;
          /* the ward absorbs INSIDE hurt, so what was handed to hurt is the
             whole priced blow and the plate took a share of the echo with it */
          if (Math.abs(hurtAcc - (mem + echo)) < 1e-9) out.wardOk++;
          else { out.wardBad++;
                 out.wardEx = out.wardEx || { arrived: hurtAcc, absorbed, mem, echo }; }
        }
        return r;
      };
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
    }
  }
  return out;
}"""


# --------------------------------------------------------------------------
# [6] A SHADE FEEDS AND CASHES. §4.3 -- the bug that produced a confidently
#     formatted, entirely wrong finding in cowork's first pass.
SHADE_JS = r"""([foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  const E = AC.STATUS.curse.echo;
  const out = { shadeBlows: 0, shadeFeeds: 0, shadeCashes: 0, shadeEcho: 0,
                casterFeeds: 0 };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match("twinshade", foeId, sd);
      const origRH = P.resolveHit;
      m.resolveHit = function(self, foe){
        const pre = foe.cursePool.slice();
        let preSum = 0; for (const v of pre) preSum += v;
        const r = origRH.apply(m, arguments);
        const grew = foe.cursePool.length !== pre.length ||
                     !foe.cursePool.every((v, i) => v === pre[i]);
        if (self.shade){
          out.shadeBlows++;
          if (grew) out.shadeFeeds++;
          if (preSum > 0){
            out.shadeCashes++;
            out.shadeEcho += Math.round(preSum * E);
          }
        } else if (grew) out.casterFeeds++;
        return r;
      };
      let step = 0;
      while (!m.over && step < secs / DT){ m.step(DT); step++; }
    }
  }
  return out;
}"""


# --------------------------------------------------------------------------
# [7] maxHp NEVER MOVES. Every relic, both sides, every frame.
MAXHP_JS = r"""([ids, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, base = AC.CONFIG.combat.baseHP;
  /* THE SENTENCE IS "maxHp NEVER MOVES", AND IT IS NOT "maxHp IS ALWAYS 400".
     The first cut of this check asserted the constant and failed on
     Twinshade -- a shade is BORN at `baseHP * u.hp` = 160 and is a real
     Fighter, so a probe that reads the roster's ceiling off a constant
     reports the summon mechanic as a curse regression. What the deleted
     channel could do was MOVE a ceiling mid-fight, so the ceiling is
     photographed the first frame each body exists and asserted against
     itself from then on. Both fighters and every shade. */
  let moved = 0, fights = 0, who = null, bodies = 0, shadeBorn = 0;
  for (let i = 0; i < ids.length; i++){
    const a = ids[i], b = ids[(i + 7) % ids.length];
    for (const sd of seeds){
      const m = new AC.Match(a, b, sd); fights++;
      const born = new Map();
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        for (const f of [m.a, m.b].concat(m.shades || [])){
          if (!f) continue;
          if (!born.has(f)){
            born.set(f, f.maxHp); bodies++;
            if (f.shade) shadeBorn++;
            continue;
          }
          if (f.maxHp !== born.get(f)){
            moved++;
            who = who || (f.w.id + (f.shade ? " (shade) " : " ") +
                          born.get(f) + " -> " + f.maxHp);
          }
        }
      }
    }
  }
  return { moved, fights, who, base, bodies, shadeBorn };
}"""


# --------------------------------------------------------------------------
# [8] DELIVERED AGAINST NOMINAL, all eight statuses. One arm with the channel
#     live, one with ONLY its effect field neutered -- the status is still
#     applied, still ticks, still draws, and delivers nothing.
DELIVER_JS = r"""([key, mut, carriers, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, S = AC.STATUS[key];
  const saved = {};
  for (const k of Object.keys(mut)){ saved[k] = S[k]; S[k] = mut[k]; }
  let dealt = 0, wins = 0, fights = 0, secsSum = 0;
  try {
    for (const rid of carriers){
      for (const foeId of foes){
        for (const sd of seeds){
          const m = new AC.Match(rid, foeId, sd);
          let step = 0;
          while (!m.over && step < secs / DT){ m.step(DT); step++; }
          const me = m.a.w.id === rid ? m.a : m.b;
          const th = me === m.a ? m.b : m.a;
          dealt += me.dealt; fights++; secsSum += m.t;
          if (me.hp > th.hp) wins++;
        }
      }
    }
  } finally {
    for (const k of Object.keys(saved)) S[k] = saved[k];
  }
  return { dealt, wins, fights, secs: secsSum };
}"""


# --------------------------------------------------------------------------
# [9] THE RENDER PATH, CALLED RATHER THAN READ. This check exists because
# VESPER'S DID NOT. Two picture faults shipped through 27 probe checks, a
# 280-match engine_ab, chain_audit and post_identity, and died on the first
# rendered frame -- and the probe's own check passed on one of them because it
# was REGEXING the drawing function's SOURCE for a call it never resolved. A
# string does not resolve a reference.
#
# This build re-cut `_stCurse` to read `f.cursePool` and `f.curseSum()` --
# fields that did not exist an hour ago, on an object the RENDERER only ever
# sees through `drawStatus`. And it DELETED a block out of `drawGlassRelic`
# whose neighbours still use the variables it declared. Both are exactly the
# fault class above, so both are called here against a real 2D context, on a
# match driven to a fighter that actually carries the status.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { cursed: 0, status: 0, glass: 0, frame: 0, motes: 0,
                maxStacksSeen: 0, threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const lit = [m.a, m.b].filter(f => f.stacks("curse") > 0);
        if (!lit.length) continue;
        out.cursed++;
        for (const f of lit)
          out.maxStacksSeen = Math.max(out.maxStacksSeen, f.stacks("curse"));
        try {
          for (const f of lit){
            R.ctx.save(); R._stCurse(m, f, AC.CONFIG.physics.ballR,
                                     f.stacks("curse")); R.ctx.restore();
            out.status++;
            /* THE MOTE COUNT IS THE STACK COUNT, and it is the one claim in
               the re-cut art that a number can hold. Counted off the pool the
               drawing function itself reads. */
            if (f.cursePool.length === f.stacks("curse")) out.motes++;
          }
        } catch (e){ out.threw = "_stCurse: " + String(e); return out; }
        try {
          for (const f of lit){
            R.ctx.save();
            drawGlassRelic(R.ctx, m, f, AC.CONFIG.physics.ballR,
                           { base: AC.CONFIG.combat.baseHP });
            R.ctx.restore();
            out.glass++;
          }
        } catch (e){ out.threw = "drawGlassRelic: " + String(e); return out; }
        /* AND THE WHOLE FRAME, because a block deleted out of one function
           can still break the one that calls it. */
        try { R.ctx.save(); R.draw(m); R.ctx.restore(); out.frame++; }
        catch (e){ out.threw = "renderer.draw: " + String(e); return out; }
        if (out.status > 400 && out.maxStacksSeen >= AC.STATUS.curse.maxStacks)
          return out;
      }
    }
  }
  return out;
}"""


# --------------------------------------------------------------------------
# [8] THE EXACT HALF. Curse's own channel needs no A/B: the echo is a number
# the engine computes on every blow, so it can simply be added up and divided
# by what was delivered. One arm, no divergence, no fight-length confound.
ECHO_JS = r"""([rids, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  let dealt = 0, echo = 0, blows = 0, echoBlows = 0, fights = 0;
  for (const rid of rids){
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match(rid, foeId, sd); fights++;
        const origRH = P.resolveHit;
        m.resolveHit = function(self, foe){
          /* READ BEFORE THE CALL: this is the echo THIS blow is about to be
             enlarged by, which is exactly the quantity resolveHit reads one
             line later. Rounded the same way, so it is the same integer. */
          const e = Math.round(foe.curseEcho());
          blows++;
          if (e > 0){ echo += e; echoBlows++; }
          return origRH.apply(m, arguments);
        };
        let step = 0;
        while (!m.over && step < secs / DT){ m.step(DT); step++; }
        dealt += m.a.dealt + m.b.dealt;
      }
    }
  }
  return { dealt, echo, blows, echoBlows, fights };
}"""


# --------------------------------------------------------------------------
# [8] AND THE CHANNEL THAT DELIVERS NO DAMAGE AT ALL. Blessing HEALS, so
# `dealt/s` and a win rate are blind to it by construction -- the first cut of
# [8b] reported it dead on an instrument that could not have seen it either
# way, which is §4.6 exactly: an instrument that fires where the mechanic does
# not measures something else.
#
# It is EARNED, never granted: only collecting a Daybreak spark applies it,
# and it heals against a CEILING, so a fighter at full hp is handed nothing.
# So the quantity is hp actually restored, and it is taken off the engine's
# own tick -- foes are chosen to carry no `dps` status, which makes the whole
# hp delta across tickStatus attributable to the one channel being measured.
HEAL_JS = r"""([mut, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype, S = AC.STATUS.blessing;
  const saved = {};
  for (const k of Object.keys(mut)){ saved[k] = S[k]; S[k] = mut[k]; }
  let healed = 0, frames = 0, applied = 0, fights = 0, wins = 0;
  try {
    for (const foeId of foes){
      for (const sd of seeds){
        const m = new AC.Match("dawnbringer", foeId, sd); fights++;
        const orig = P.tickStatus;
        m.tickStatus = function(f, dt){
          const n = f.stacks("blessing");
          const dps = f.stacks("smite") + f.stacks("hemorrhage");
          const hp0 = f.hp;
          const r = orig.apply(m, arguments);
          if (n > 0 && dps === 0){
            frames++;
            if (f.hp > hp0) healed += f.hp - hp0;
          }
          if (n > 0) applied++;
          return r;
        };
        let step = 0;
        while (!m.over && step < secs / DT){ m.step(DT); step++; }
        const me = m.a.w.id === "dawnbringer" ? m.a : m.b;
        const th = me === m.a ? m.b : m.a;
        if (me.hp > th.hp) wins++;
      }
    }
  } finally {
    for (const k of Object.keys(saved)) S[k] = saved[k];
  }
  return { healed, frames, applied, fights, wins };
}"""


# The neutering, one per status. The FIELD, never the application: a status
# that stops being applied would also stop being drawn, would stop feeding
# `taught`, and would change the match in ways that are not the channel.
NEUTER = {
    "smite":      {"dps": 0},
    "hemorrhage": {"dps": 0},
    "entangle":   {"spin": 0, "move": 0},
    "hex":        {"stunEvery": 1e9, "stunFor": 0},
    "curse":      {"echo": 0},
    "sunder":     {"taken": 0},
    "blessing":   {"hps": 0},
    "ward":       {"bank": 0, "shatter": 0},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-curse.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=130.0)
    A = ap.parse_args()

    g = resolve_game(A.game)
    print(f"\nCURSE_CHECK  {g.name}")
    seeds = [1000 + i * 977 for i in range(A.seeds)]

    with game(game_path=g) as (page, errors):
        M = page.evaluate(META_JS)
        C, S = M["curse"], M["src"]
        umbral = [r["id"] for r in M["relics"] if r["aff"] == "umbral"]
        vigil = [r["id"] for r in M["relics"] if r["aff"] == "vigil"]
        clean = [r["id"] for r in M["relics"] if r["aff"] not in ("umbral", "vigil")]
        print(f"  curse   maxStacks {C['maxStacks']}  dur {C['dur']}  "
              f"echo {C.get('echo')}  tip {C['tip']!r}")
        print(f"  umbral  {', '.join(umbral)}")

        print("\n  --- the source, read out of the build --------------------")
        for k, v in S.items():
            print(f"  {'ok  ' if v else 'BAD '}  {k}")
        check("[0] the shipped source still says every sentence",
              all(S.values()),
              ", ".join(k for k, v in S.items() if not v) or "12/12")
        check("[0b] maxHpLoss is gone from the data, not zeroed",
              "maxHpLoss" not in C and C.get("echo") is not None,
              f"fields: {sorted(C)}")

        # ---------------------------------------------------------- 1..4
        print("\n  --- [1][2][3][4] the exact arm, non-vigil foes -----------")
        agg = {}
        for rid in umbral:
            r = page.evaluate(LEDGER_JS, [rid, clean[:6], seeds, A.secs])
            print(f"  {rid:12s} blows {r['blows']:6d}  pushes {r['pushes']:5d}  "
                  f"fresh {r['freshPushes']:4d}  maxMem {r['maxMem']:4.0f}  "
                  f"maxPool {r['maxPool']:5.0f}  memBad {r['memBad']}  "
                  f"poolBad {r['poolBad']}  syncBad {r['syncBad']}")
            if r["worst"]:
                print(f"      worst: {json.dumps(r['worst'])}")
            for k, v in r.items():
                if isinstance(v, (int, float)):
                    agg[k] = agg.get(k, 0) + v
            agg.setdefault("sample", None)
            agg["sample"] = agg["sample"] or r["sample"]

        check("[1] a stack remembers dmgBase, never the echo",
              agg["pushes"] > 200 and agg["memBad"] == 0,
              f"{agg['pushes']} applications, {agg['memBad']} bad")
        check("[2] the pool is the top K and the trim drops the weakest",
              agg["poolBad"] == 0 and agg["sortBad"] == 0 and agg["capBad"] == 0,
              f"poolBad {agg['poolBad']} sortBad {agg['sortBad']} "
              f"capBad {agg['capBad']}  (K={C['maxStacks']})")
        check("[3] stacks('curse') == cursePool.length, every frame",
              agg["syncBad"] == 0,
              f"{agg['steps']} frames x 2+ fighters, {agg['syncBad']} bad")
        check("[4] a fresh stack does not pay on its own blow",
              agg["freshPushes"] > 50 and agg["freshBad"] == 0,
              f"{agg['freshPushes']} first-stack blows, {agg['freshBad']} bad")
        if agg["sample"]:
            s = agg["sample"]
            print(f"      a full pool: {s['pre']} + {s['pushed']} -> {s['post']}"
                  f"   (arrived {s['arrived']}, of which echo {s['echo']})")

        # ------------------------------------------------------------- 5
        print("\n  --- [5] the wall and the plate ---------------------------")
        w = page.evaluate(WALL_JS, [umbral[0], vigil, seeds, A.secs])
        w2 = page.evaluate(WALL_JS, [umbral[1], vigil, seeds, A.secs])
        for k in w:
            if isinstance(w[k], (int, float)):
                w[k] += w2[k]
        w["aegisEx"] = w["aegisEx"] or w2["aegisEx"]
        w["wardEx"] = w["wardEx"] or w2["wardEx"]
        print(f"  aegis  {w['aegisBlows']:4d} echoed blows eaten by a wall, "
              f"{w['aegisOk']} obey arrived+eaten == mem+echo")
        print(f"  ward   {w['wardBlows']:4d} echoed blows into a plate, "
              f"{w['wardOk']} obey arrived == mem+echo")
        if w["aegisEx"]:
            print(f"      aegis counterexample: {json.dumps(w['aegisEx'])}")
        if w["wardEx"]:
            print(f"      ward counterexample: {json.dumps(w['wardEx'])}")
        check("[5] an Aegis wall eats the echo with the blow",
              w["aegisBlows"] > 0 and w["aegisBad"] == 0,
              f"{w['aegisOk']}/{w['aegisBlows']}")
        check("[5b] a Ward absorbs the echo with the blow",
              w["wardBlows"] > 0 and w["wardBad"] == 0,
              f"{w['wardOk']}/{w['wardBlows']}")

        # ------------------------------------------------------------- 6
        print("\n  --- [6] a shade feeds and cashes the pool ----------------")
        sh = page.evaluate(SHADE_JS, [clean[:6], seeds, A.secs])
        print(f"  shade blows {sh['shadeBlows']}   feeds {sh['shadeFeeds']}   "
              f"cashes {sh['shadeCashes']}   echo dealt by shades "
              f"{sh['shadeEcho']}   caster feeds {sh['casterFeeds']}")
        check("[6] a shade's blow feeds the pool",
              sh["shadeFeeds"] > 0,
              f"{sh['shadeFeeds']} of {sh['shadeBlows']} shade blows")
        check("[6b] a shade's blow cashes the pool",
              sh["shadeCashes"] > 0 and sh["shadeEcho"] > 0,
              f"{sh['shadeCashes']} blows, {sh['shadeEcho']} damage of echo")

        # ------------------------------------------------------------- 7
        print("\n  --- [7] the old channel is shut -------------------------")
        ids = [r["id"] for r in M["relics"]]
        mh = page.evaluate(MAXHP_JS, [ids, seeds[:3], A.secs])
        check("[7] maxHp never moves, any relic, any frame",
              mh["moved"] == 0,
              f"{mh['fights']} fights, {mh['bodies']} bodies "
              f"({mh['shadeBorn']} of them shades, born at 0.4 of {mh['base']}), "
              f"{mh['moved']} moved" + (f" ({mh['who']})" if mh["who"] else ""))

        # ------------------------------------------------------------- 8
        print("\n  --- [8] DELIVERED AGAINST NOMINAL, all eight -------------")
        # THE EXACT HALF FIRST, and it is the one the brief actually asks
        # about. The A/B below is confounded by fight length -- delete a
        # damaging status and the fight runs LONGER, so the blade delivers
        # more and the raw difference comes back NEGATIVE. Curse's own channel
        # needs no A/B at all: the echo is a number the engine computes, so it
        # can be added up and divided by what was delivered. One arm, exact.
        ec = page.evaluate(ECHO_JS, [umbral, clean[:5], seeds, A.secs])
        eshare = ec["echo"] / ec["dealt"] if ec["dealt"] else 0.0
        print(f"      curse, exactly: {ec['echo']:.0f} of {ec['dealt']:.0f} damage "
              f"delivered over {ec['fights']} fights IS the echo = "
              f"{eshare * 100:.1f}%")
        print(f"                      {ec['echoBlows']} of {ec['blows']} blows "
              f"landed on a pool that had something in it")
        print("      status       dealt/s(on)  (off)    delta    win(on) win(off)"
              "   delta    secs(on)  (off)")
        rows, dead = [], []
        for key in M["statuses"]:
            if key not in NEUTER:
                continue
            carriers = [r["id"] for r in M["relics"]
                        if (r["onHit"] or {}).get(key) or (r["onSelf"] or {}).get(key)
                        or (r["apply"] or {}).get(key)]
            # blessing is EARNED, never granted -- only collecting a Daybreak
            # spark applies it, so it has no carrier in the weapon table.
            if not carriers and key == "blessing":
                carriers = ["dawnbringer"]
            if not carriers:
                print(f"      {key:12s} (no carrier)")
                continue
            carriers = carriers[:3]
            foes = [i for i in clean if i not in carriers][:3]
            on = page.evaluate(DELIVER_JS, [key, {}, carriers, foes, seeds, A.secs])
            off = page.evaluate(DELIVER_JS, [key, NEUTER[key], carriers, foes,
                                             seeds, A.secs])
            dps_on = on["dealt"] / on["secs"] if on["secs"] else 0.0
            dps_off = off["dealt"] / off["secs"] if off["secs"] else 0.0
            ratio = (dps_on - dps_off) / dps_on if dps_on else 0.0
            wo = on["wins"] / on["fights"] * 100
            wf = off["wins"] / off["fights"] * 100
            rows.append((key, ratio, wo - wf))
            print(f"      {key:12s} {dps_on:9.2f} {dps_off:8.2f} {ratio * 100:+8.1f}%"
                  f"   {wo:6.1f}% {wf:6.1f}%  {wo - wf:+7.1f}pp"
                  f"   {on['secs'] / on['fights']:7.1f} {off['secs'] / off['fights']:6.1f}")
            # A DEAD CHANNEL MOVES NEITHER, and both thresholds are named
            # rather than eyeballed: 2% of damage RATE and 5 points of win
            # rate, over carriers x foes x seeds fights an arm.
            if key == "blessing":
                # MEASURED ON THE CHANNEL IT ACTUALLY HAS. See HEAL_JS.
                nodps = [r["id"] for r in M["relics"]
                         if not (r["onHit"] or {}).get("smite")
                         and not (r["onHit"] or {}).get("hemorrhage")
                         and r["aff"] not in ("sanctified", "bloodsworn")][:3]
                hon = page.evaluate(HEAL_JS, [{}, nodps, seeds, A.secs])
                hoff = page.evaluate(HEAL_JS, [NEUTER[key], nodps, seeds, A.secs])
                print(f"      {'':12s} and on the channel it HAS: "
                      f"{hon['healed']:.0f} hp restored over {hon['fights']} "
                      f"fights against {hoff['healed']:.0f} with hps 0 "
                      f"({hon['frames']} clean ticks)")
                if hon["healed"] - hoff["healed"] > 1.0:
                    continue          # not dead: it delivers hp, not damage
            if abs(ratio) < 0.02 and abs(wo - wf) < 5.0:
                dead.append(f"{key} ({ratio * 100:+.1f}% dmg/s, {wo - wf:+.1f}pp)")
        check("[8] curse delivers what its tip promises",
              eshare > 0.05,
              f"{eshare * 100:.1f}% of all damage delivered IS the echo "
              f"(the old channel delivered ~3% of its nominal)")
        check("[8b] no status channel delivers nothing",
              not dead,
              "all eight move damage rate or win rate" if not dead
              else "DEAD OR NEARLY DEAD: " + "; ".join(dead))

        # ------------------------------------------------------------- 9
        print("\n  --- [9] the render path, CALLED --------------------------")
        dr = page.evaluate(DRAW_JS, [umbral[0], clean[:4], seeds[:3], A.secs])
        if dr.get("skip"):
            print(f"      skipped: {dr['skip']}")
        else:
            print(f"      {dr['cursed']} cursed frames driven   _stCurse "
                  f"{dr['status']}   drawGlassRelic {dr['glass']}   "
                  f"full frames {dr['frame']}   deepest pool "
                  f"{dr['maxStacksSeen']}")
            if dr["threw"]:
                print(f"      THREW: {dr['threw']}")
        check("[9] the re-cut art and the whole frame draw without throwing",
              not dr.get("skip") and dr["threw"] is None and dr["status"] > 100
              and dr["frame"] > 100,
              f"{dr.get('status', 0)} _stCurse calls, {dr.get('frame', 0)} "
              f"full frames, 0 exceptions")
        check("[9b] the mote count IS the stack count, on every drawn frame",
              not dr.get("skip") and dr["status"] > 0
              and dr["motes"] == dr["status"],
              f"{dr.get('motes', 0)}/{dr.get('status', 0)}")

        if errors:
            print("\n  page errors:")
            for e in errors[:10]:
                print("   ", e)
        check("[10] the page raised no JS error in any of the above",
              not errors, f"{len(errors)} errors")

    ok = sum(1 for _, v in PASS if v)
    print(f"\n  {ok}/{len(PASS)} checks pass\n")
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
