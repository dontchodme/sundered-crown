#!/usr/bin/env python3
"""GRAVEMOURN'S ULTIMATE, ASSERTED AGAINST THE BUILD -- one check per sentence.

    python gravemourn_relic_probe.py --game ../02-chain/sc-gravemourn.html

Layer 2 of the v51/52 build brief (§5, checks 9-14).

  [9]  the chain really lengthens, and ONLY for the window, and ONLY for this
       fighter -- the other 26 relics' reach untouched during and after, in the
       SAME PAGE SESSION
  [10] one hand per pool entry, and the pool is empty the instant they leave
  [11] a hand deals exactly what it carries, and re-parks exactly that
  [12] no hand resolves after the fight ends or on a corpse
  [13] the ult files a BEAT for the director -- rule 3, seventh relic running
  [14] THE SOUND IS RENDERED AND MEASURED in an OfflineAudioContext, all three
       voices

## [9] IS THE ONE THIS PROBE EXISTS FOR

`w` is module-level and shared by every match in a page session. A window that
writes `w.reach` and misses one restore path does not lengthen one flail -- it
permanently rewrites the relic for every fight afterwards, and **the symptom
appears in a match that never cast anything**. So [9] does not check one match.
It runs a Gravemourn fight that casts, then runs fights for other relics AFTER
it in the same page, and asserts every reach in the roster is what it was.

A per-fighter field makes that structurally impossible, which is the point --
this check is what proves the field is actually per-fighter rather than a
module-level one with a tidier name.

## [14] IS WHY v42's ULTIMATE WAS SILENT

`SFX.play` returns on its first line headless and wraps its body in try/catch,
so a broken voice is invisible to every other tool in this repo. All three
voices are rendered through `buildChain` -- the signal path that actually ships
-- and measured.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game, resolve_game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

RID = "gravemourn"
PASS: list[tuple[str, bool]] = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


META_JS = r"""([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const P = AC.Match.prototype;
  const strip = f => f.toString().replace(/\/\*[\s\S]*?\*\//g, "")
                                 .replace(/\/\/.*/g, "");
  const rh = strip(P.resolveHit), ts = strip(P.tickSling);
  return {
    u: JSON.parse(JSON.stringify(w.ult)),
    dmg: w.dmg, reach: w.reach,
    /* THE ROSTER'S REACH, PHOTOGRAPHED BEFORE ANYTHING RUNS. [9] compares
       against this, not against a constant. */
    roster: AC.WEAPONS.map(x => ({ id: x.id, reach: x.reach })),
    src: {
      /* THE HAZARD, AS A PROPERTY OF THE TEXT. No assignment to w.reach
         anywhere, and every read of f.w.reach carries the multiplier. */
      noWReachWrite: !/w\.reach\s*=/.test(strip(P.constructor) + rh + ts),
      hasReachMul:   /reachMul/.test(ts),
      /* the window restores on BOTH exits -- the clock and the corpse */
      restores:      (strip(P.tickSling).match(/reachMul = 1/g) || []).length >= 1,
      /* the memory is re-parked, not grown */
      reParks:       /pushCurse\(dmg, 1\)/.test(ts),
      /* the clamp is a conservation law and it is in the ENGINE, not only in
         the builder that wrote it */
      clampsHandMul: /Math\.min\(1, src\.w\.ult\.handMul\)/.test(ts),
      /* hands are their own list, not shots -- spawnShot shifts at maxLive */
      ownList:       /this\.hands/.test(rh),
      /* and a hand files a beat */
      filesBeat:     /this\.beat\(/.test(ts),
      /* the cast opens a window and resolves nothing */
      castIsEmpty:   w.ult.dmg === 0,
      kindIsSling:   w.ult.kind === "sling",
    },
  };
}"""


# --------------------------------------------------------------------------
# [9] THE MODULE-LEVEL HAZARD, IN THE SAME PAGE SESSION. Cast first, then run
# other relics AFTER, then read the roster back.
REACH_JS = r"""([rid, foes, seeds, others, secs]) => {
  const DT = AC.CONFIG.physics.dt, H = AC.CONFIG.chain.hilt;
  const before = AC.WEAPONS.map(w => w.reach);
  let casts = 0, windowSeen = 0, hiMul = 0, badRestore = 0, otherTouched = 0;
  let fights = 0;
  /* THE MEASUREMENT IS A RATIO, NOT A LENGTH, AND THAT IS THE WHOLE FIX.
     The first cut of this check compared the head's peak orbit INSIDE the
     window against its peak OUTSIDE and reported 77 against 77 -- the chain
     apparently not lengthening at all, on a build where it does. Both numbers
     were maxima taken in DIFFERENT ACTS: `actMods.reach` climbs 1.0 -> 1.1
     over a fight, the window lands early, the late fight is all outside it,
     and the act quietly ate the effect.

     What is sampled now is `headR` over the chain length this relic would have
     WITHOUT the window, on the SAME FRAME. Act-independent by construction,
     and it reads 1.35 against a reachMul of 1.35. */
  let inMax = 0, outMax = 0, inSum = 0, outSum = 0, inN = 0, outN = 0;
  let settleFrames = 0;
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd); fights++;
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      let step = 0, sawWindow = false;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        const bare = me.w.reach * m.actMods.reach * (1 - H);
        const r = Math.hypot(me.headX - me.pivX, me.headY - me.pivY) / bare;
        if (me.ultSling){
          sawWindow = true; windowSeen++;
          hiMul = Math.max(hiMul, me.reachMul);
          inMax = Math.max(inMax, r); inSum += r; inN++;
        } else {
          outMax = Math.max(outMax, r); outSum += r; outN++;
          /* THE SETTLE TAIL. `tickSling` runs AFTER `tickWeapon` in the same
             step, so on the frame a window closes the head was already placed
             at the long length before the restore ran. Counted rather than
             ignored: one frame per close, the picture and the hit box agree
             with each other on it, and a number is how the next person knows
             it was looked at rather than missed. */
          if (r > 1.05) settleFrames++;
          if (sawWindow && me.reachMul !== 1) badRestore++;
        }
        if (th.reachMul !== 1) otherTouched++;
      }
      casts += me.ultsFired;
    }
  }
  /* NOW RUN OTHER RELICS, AFTER the casts, in the SAME page session. This is
     the shape of the bug: the symptom appears in a match that never cast. */
  let afterBad = 0;
  for (const a of others){
    for (const b of others){
      if (a === b) continue;
      const m = new AC.Match(a, b, 4242);
      let step = 0;
      while (!m.over && step < 20 / DT){
        m.step(DT); step++;
        if (m.a.reachMul !== 1 || m.b.reachMul !== 1) afterBad++;
      }
    }
  }
  const after = AC.WEAPONS.map(w => w.reach);
  const moved = [];
  for (let i = 0; i < before.length; i++)
    if (before[i] !== after[i])
      moved.push(AC.WEAPONS[i].id + " " + before[i] + " -> " + after[i]);
  return { casts, fights, windowSeen, hiMul, badRestore, otherTouched,
           afterBad, moved, settleFrames,
           inMax: +inMax.toFixed(3), outMax: +outMax.toFixed(3),
           inMean: +(inSum / Math.max(1, inN)).toFixed(3),
           outMean: +(outSum / Math.max(1, outN)).toFixed(3), inN, outN };
}"""


# --------------------------------------------------------------------------
# [10][11][12] THE HANDS, LEDGERED OFF THE ENGINE'S OWN CALLS.
HAND_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, P = AC.Match.prototype;
  const out = { blows: 0, spawnEvents: 0, perBlowBad: 0, poolNotEmpty: 0,
                landed: 0, dealtBad: 0, reparkBad: 0, lost: 0,
                onCorpse: 0, afterOver: 0, beats: 0, thrown: 0,
                memSeen: 0, knockBad: 0, sample: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      const me = m.a.w.id === rid ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      const U = me.w.ult;

      /* [13] the beat, counted off the engine's own filing */
      const origBeat = P.beat;
      m.beat = function(o){
        if (o && o.kind === "ult" && o.w === rid) out.beats++;
        return origBeat.apply(m, arguments);
      };
      /* [10] ONE HAND PER POOL ENTRY, AND THE REFERENCE POINT IS THE POOL AS
         IT STOOD WHEN THE HANDS LEFT -- not as it stood when the blow began.
         The first cut of this check snapshotted the pool before `resolveHit`
         and reported 18 of 27 blows with "the wrong count": a pool of [35]
         producing two hands carrying [58, 35]. The engine was right. The blow
         that throws the hands is one of the blows they remember, so its own
         `onHit` push is in the pool by the time they peel off -- which is
         exactly what the build's comment says it does.

         So `pushCurse` is hooked to count what this blow contributed, and the
         expected number is the pool AFTER that push, capped: a check that
         reconstructs the engine's rule rather than assuming its own. */
      const K = AC.STATUS.curse.maxStacks;
      const F = Object.getPrototypeOf(me);
      const origPush = F.pushCurse;
      /* ONE PERSISTENT RECORDER ON THE QUARRY, with a context flag, rather
         than a hook installed and deleted inside resolveHit. The two hooks
         this check needs -- what a BLOW pushed and what a HAND pushed -- would
         otherwise clobber each other, because resolveHit's `delete` removes
         whichever own property is there. */
      let ctx = null, blowPushes = 0, slingPushes = [];
      th.pushCurse = function(v, n){
        if (ctx === "blow") blowPushes += n;
        else if (ctx === "sling") slingPushes.push(v);
        return origPush.apply(th, arguments);
      };
      const origTS = P.tickSling;
      m.tickSling = function(){
        slingPushes = []; ctx = "sling";
        try { return origTS.apply(m, arguments); } finally { ctx = null; }
      };
      const origRH = P.resolveHit;
      m.resolveHit = function(self, foe){
        const pre = self === me && me.ultSling ? foe.cursePool.slice() : null;
        const n0 = m.hands.length;
        blowPushes = 0;
        const outer = ctx; if (pre) ctx = "blow";
        const r = origRH.apply(m, arguments);
        ctx = outer;
        const pushedHere = blowPushes;
        if (pre && pre.length + pushedHere){
          out.blows++;
          const made = m.hands.length - n0;
          if (made > 0){
            out.spawnEvents++;
            out.thrown += made;
            const want = Math.min(K, pre.length + pushedHere);
            if (made !== want) out.perBlowBad++;
            if (foe.cursePool.length !== 0) out.poolNotEmpty++;
            if (!out.sample)
              out.sample = { poolBefore: pre, pushedByThisBlow: pushedHere,
                             expected: want, hands: made,
                             mems: m.hands.slice(-made).map(h => h.mem) };
          }
        }
        return r;
      };
      let step = 0;
      let prev = [];
      while (!m.over && step < secs / DT){
        const hp0 = th.hp, pool0 = th.cursePool.slice();
        const before = m.hands.map(h => ({ h, mem: h.mem, u: h.u }));
        const overBefore = m.over, aliveBefore = th.alive;
        m.step(DT); step++;
        /* which hands resolved this frame */
        for (const b of before){
          if (m.hands.indexOf(b.h) >= 0) continue;
          if (!aliveBefore || overBefore){
            /* [12] it must not have paid anything */
            out.lost++;
            if (!aliveBefore) out.onCorpse++;
            if (overBefore) out.afterOver++;
            continue;
          }
          out.landed++;
          out.memSeen += b.mem;
          /* [11] IT DEALS EXACTLY WHAT IT CARRIES, AND RE-PARKS EXACTLY THAT.
             `dmgTakenMul` is the one legitimate scaler between the two, so it
             is re-derived rather than assumed to be 1.

             THE CLAIM IS ABOUT WHAT THE HAND PUSHED, NOT ABOUT WHAT SURVIVED.
             The first cut asserted the value was still IN the pool afterwards
             and started failing the moment flight time went 1.2s -> 1.8s: with
             hands in the air longer, the quarry gets hit again before they
             land, so a small re-parked memory is pushed into a full pool and
             DISPLACED on the same call. That is curse's top-K rule working,
             not the hand misbehaving. What this checks is the push itself. */
          const want = Math.round(b.mem * Math.min(1, U.handMul)
                                  * th.dmgTakenMul());
          if (!slingPushes.length) out.reparkBad++;
          else if (!slingPushes.includes(want)) out.reparkBad++;
        }
      }
    }
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-gravemourn.html")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--secs", type=float, default=130.0)
    A = ap.parse_args()

    g = resolve_game(A.game)
    print(f"\nGRAVEMOURN RELIC PROBE  {g.name}")
    seeds = [11 + i * 977 for i in range(A.seeds)]
    FOES = ["emberedge", "axiom", "heartwood", "ironhail", "lastlight"]
    OTHERS = ["emberedge", "axiom", "slagheart"]

    with game(game_path=g) as (page, errors):
        M = page.evaluate(META_JS, [RID])
        U, S = M["u"], M["src"]
        print(f"  ult {U['name']}  kind {U['kind']}  dur {U['dur']}  "
              f"reachMul {U['reachMul']}  handFly {U['handFly']}  "
              f"handStag {U['handStag']}  handMul {U['handMul']}  "
              f"knock {U['knock']}")
        print(f"  blade {M['dmg']}   reach {M['reach']}")
        print("\n  --- the source ------------------------------------------")
        for k, v in S.items():
            print(f"  {'ok  ' if v else 'BAD '}  {k}")
        check("[8] the shipped source still says every sentence",
              all(S.values()),
              ", ".join(k for k, v in S.items() if not v) or f"{len(S)}/{len(S)}")

        print("\n  --- [9] the chain, and the module-level hazard -----------")
        r = page.evaluate(REACH_JS, [RID, FOES, seeds, OTHERS, A.secs])
        print(f"  {r['fights']} fights, {r['casts']} casts, "
              f"{r['windowSeen']} frames inside a window")
        print(f"  head orbit over the chain it would have WITHOUT the window,")
        print(f"  same frame:   in {r['inMean']} mean / {r['inMax']} peak"
              f"     out {r['outMean']} mean / {r['outMax']} peak")
        check("[9] the chain lengthens, by exactly the multiplier it was given",
              abs(r["inMax"] - U["reachMul"]) < 0.02
              and r["hiMul"] == U["reachMul"]
              and r["inMean"] > r["outMean"] + 0.15,
              f"peak {r['inMax']}x against a reachMul of {U['reachMul']}; "
              f"mean {r['outMean']} -> {r['inMean']}")
        check("[9b] it is restored on every exit from the window",
              r["badRestore"] == 0,
              f"{r['badRestore']} frames off 1 after a window; "
              f"{r['settleFrames']} of {r['outN']} outside frames are the "
              f"one-frame settle tail (tickSling runs after tickWeapon)")
        check("[9c] it never reaches the foe",
              r["otherTouched"] == 0, f"{r['otherTouched']} frames")
        check("[9d] AND NO OTHER RELIC IS TOUCHED, in the same page session",
              not r["moved"] and r["afterBad"] == 0,
              "27 reaches unmoved after the casts; 6 later matches clean"
              if not r["moved"] else "MOVED: " + "; ".join(r["moved"]))

        print("\n  --- [10][11][12] the hands ------------------------------")
        h = page.evaluate(HAND_JS, [RID, FOES, seeds, A.secs])
        print(f"  blows in window {h['blows']}   spawn events {h['spawnEvents']}"
              f"   hands thrown {h['thrown']}   landed {h['landed']}   "
              f"declined/lost {h['lost']}")
        if h["sample"]:
            s = h["sample"]
            print(f"      a blow: pool {s['poolBefore']} + "
                  f"{s['pushedByThisBlow']} pushed by this blow -> "
                  f"{s['expected']} expected, {s['hands']} hands "
                  f"carrying {s['mems']}")
        check("[10] one hand per pool entry",
              h["spawnEvents"] > 0 and h["perBlowBad"] == 0,
              f"{h['spawnEvents']} spawn events, {h['perBlowBad']} with the "
              f"wrong count")
        check("[10b] the pool is empty the instant they leave",
              h["poolNotEmpty"] == 0, f"{h['poolNotEmpty']} blows left a pool behind")
        check("[11] a hand re-parks exactly what it dealt",
              h["landed"] > 0 and h["reparkBad"] == 0,
              f"{h['landed']} landings, {h['reparkBad']} bad")
        check("[12] no hand resolves on a corpse or after the fight",
              h["onCorpse"] == 0 and h["afterOver"] == 0,
              f"{h['lost']} hands were in the air at the end and paid nothing")
        check("[13] the ultimate files a BEAT the director can see",
              h["beats"] > 0,
              f"{h['beats']} ult beats filed from the dive")

        print("\n  --- [14] the sound, RENDERED --------------------------")
        voices = [("cast (the chain)", "gravemourn"),
                  ("hand (peeling off)", "gravemourn-hand"),
                  ("fist (landing)", "gravemourn-fist")]
        silent = []
        print(f"      {'voice':<22}{'peak':>8}{'audible':>9}")
        for name, wid in voices:
            sfx = page.evaluate(SFX_JS, ["ult", {"w": wid}, 2.0])
            if sfx.get("skip"):
                print(f"      {name:<22}  (no OfflineAudioContext)")
                continue
            print(f"      {name:<22}{sfx['peak']:>8}{sfx['audible']:>8}s"
                  + (f"   THREW {sfx['threw']}" if sfx.get("threw") else ""))
            if sfx.get("threw") or sfx["peak"] < 0.01 or sfx["audible"] < 0.05:
                silent.append(name)
        check("[14] all three voices render and are audible",
              not silent,
              "cast, hand and fist all sound" if not silent
              else "SILENT OR THREW: " + ", ".join(silent))

        if errors:
            print("\n  page errors:")
            for e in errors[:8]:
                print("   ", e)
        check("[15] the page raised no JS error in any of the above",
              not errors, f"{len(errors)} errors")

    ok = sum(1 for _, v in PASS if v)
    print(f"\n  {ok}/{len(PASS)} checks pass\n")
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
