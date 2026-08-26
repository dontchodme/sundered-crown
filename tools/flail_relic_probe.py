#!/usr/bin/env python3
"""THE BLOODSWORN FLAIL AND THE SPIKE STORM -- does any of it happen?

    python3 flail_relic_probe.py --game ../02-chain/sc-redflail.html

Lastlight is why this file is long. The Harrowing's latch branch was
UNREACHABLE and the build compiled, drew, and looked right while the ultimate
was silently twelve small arrows. This ultimate has FOUR ways to be silently
nothing and each gets its own question:

  [1] does the relic exist and fight
  [2] does the WIND-UP ever complete -- the release condition is a physical
      state, and a physical state that is never reached is an ultimate that
      never fires
  [3] are the SPIKES real -- spawned, moving, landing, and spent on walls
  [4] can it be BROKEN, and ONLY by the right things. This is the check Rick's
      clarification is about and it is the one that can actually fail:
      hex and ult-freeze must cancel the cast, and ORDINARY HITSTUN MUST NOT.
      The negative control is the point of the block; without it a build where
      everything cancels the cast passes every positive check.

Every measurement steps `CONFIG.physics.dt`, not 1/60. v37 caught six
instruments getting that wrong and this one is not going to be the seventh.

Writes nothing.
"""
from __future__ import annotations

import argparse, pathlib, statistics, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
RID  = "redflail"
FOES = ["thornwake", "censer", "ironhail", "heartwood", "lightkeeper",
        "spellbreaker", "dawnbringer", "grudgebearer", "gravemourn", "aureole"]

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))

ROSTER_JS = """() => AC.WEAPONS.map(w => ({id:w.id, name:w.name, aff:w.aff,
  shape:w.shape, mode:w.mode, kind:w.ult.kind, dmg:w.dmg}))"""

BRANCH_JS = """(id) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const names = ["_fhBarbed","_fhBase","_fhBall","_needle"];
  const fired = [], orig = {};
  for (const n of names){ orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this,a); }; }
  const cv = document.createElement("canvas"); cv.width = cv.height = 400;
  const c = cv.getContext("2d"); c.translate(200,200);
  AC.SHAPES.flailHead(c, w.artW, AC.AFFINITIES[w.aff], 0.7);
  for (const n of Object.keys(orig)) AC.SHAPES[n] = orig[n];
  return fired;
}"""

# [2][3] The field measurement. Forces nothing: casts happen when the bar
# fills, which is the only regime the reported rates mean anything in.
FIELD_JS = """([id, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  const rows = [];
  for (const f of foes){
    for (const sd of seeds){
      const m = new AC.Match(id, f, sd);
      const me = m.a.w.id === id ? m.a : m.b;
      const th = me === m.a ? m.b : m.a;
      /* Casts and breaks are COUNTED at their source, not inferred from the
         state going null -- a storm ENDING also sets it null and the two must
         never be confused. */
      let casts = 0, breaks = 0, released = 0;
      const winds = [];
      const origFire = AC.Match.prototype.fireUlt;
      const origBreak = AC.Match.prototype.breakSpin;
      AC.Match.prototype.fireUlt = function(a, b){
        if (a === me && a.w.ult.kind === "spinstorm") casts++;
        return origFire.call(this, a, b); };
      AC.Match.prototype.breakSpin = function(a, r){
        if (a === me && a.ultSpin) breaks++;
        return origBreak.call(this, a, r); };
      let steps = 0, spikes = 0, maxLive = 0, wasStorm = false;
      let prevShots = 0, spikeHits = 0, prevHits = 0, prevN = 0;
      while (!m.over && steps < 120 / DT){
        m.step(DT); steps++;
        const S = me.ultSpin;
        if (S && S.phase === "storm" && !wasStorm){
          wasStorm = true; released++; winds.push(S.wind);
        }
        if (!S) wasStorm = false;
        if (S && S.n > prevN){ spikes += S.n - prevN; }
        prevN = S ? S.n : 0;
        maxLive = Math.max(maxLive, m.shots.length);
      }
      AC.Match.prototype.fireUlt = origFire;
      AC.Match.prototype.breakSpin = origBreak;
      rows.push({ foe: f, seed: sd, dur: steps * DT, casts, breaks, released,
                  winds, spikes, maxLive, hits: me.hits, shotHits: m.shotHits,
                  foeHp: Math.round(th.hp),
                  won: !!(m.winner && m.winner.w.id === id) });
    }
  }
  return rows;
}"""

# [3b] A spike must be SPENT on a wall, not bounce off it. Driven directly:
# one spike, aimed at a wall, stepped until it is gone, with its own position
# recorded so "it died" cannot be confused with "it bounced out of the array".
WALL_JS = """([id]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, "censer", 4242);
  const me = m.a.w.id === id ? m.a : m.b;
  m.shots.length = 0;
  me.headX = 60; me.headY = 400; me.headAng = Math.PI;   // pointed at the wall
  m.spawnSpike(me);
  const s0 = m.shots[0];
  if (!s0) return { spawned: false };
  const rec = { spawned: true, bounce: s0.bounce, x0: s0.x, live: 1, frames: 0 };
  for (let i = 0; i < 240 && m.shots.length; i++){ m.tickShots(DT); rec.frames++; }
  rec.live = m.shots.length;
  return rec;
}"""

# [4] THE BREAK, DRIVEN -- and the negative control is the whole point.
BREAK_JS = """([id, mode]) => {
  const DT = AC.CONFIG.physics.dt;
  const foe = mode === "freeze" ? "thornwake" : "censer";
  const m = new AC.Match(id, foe, 909);
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  /* Force the cast, then step PAST the hit stop fireUlt sets -- v37 caught
     three checks measuring a frozen frame and reporting FAIL on a correct
     build. */
  me.charge = me.w.ult.charge;
  for (let i = 0; i < 30 && !me.ultSpin; i++) m.step(DT);
  if (!me.ultSpin) return { started: false };
  const startPhase = me.ultSpin.phase;
  if (mode === "hitstun"){
    /* The NEGATIVE CONTROL. Ordinary hitstun, applied hard and repeatedly --
       far more than a fight would ever deliver -- and the cast must SURVIVE. */
    for (let i = 0; i < 140; i++){ me.takeHitstun(40); m.step(DT); }
  } else if (mode === "hex"){
    me.apply("hex", 5); me.hexClock = AC.STATUS.hex.stunEvery - 0.01;
    for (let i = 0; i < 30 && me.ultSpin; i++) m.step(DT);
  } else if (mode === "clank"){
    /* Also a control: the clank stun is combat, not an ability. */
    for (let i = 0; i < 140; i++){
      me.stun = Math.max(me.stun, 0.2); m.step(DT); }
  } else if (mode === "freeze"){
    /* Bramblesnare is `kind:"freeze"` with `radius: 260`, and the FIRST cut of
       this check ignored that: it forced the cast and reported FAIL while the
       two balls happened to be 300-odd pixels apart, so `inRange` was false and
       the freeze never applied. The build was correct and the instrument was
       not -- v37 section 5 all over again. The foe is placed inside its own
       radius here, which is what the check was always claiming to test. */
    th.x = me.x + 70; th.y = me.y;
    th.vx = 0; th.vy = 0;
    th.charge = th.w.ult.charge;                 // Bramblesnare, for real
    for (let i = 0; i < 20 && me.ultSpin; i++) m.step(DT);
  }
  return { started: true, startPhase, alive: !!me.ultSpin,
           phase: me.ultSpin ? me.ultSpin.phase : null,
           broke: me.ultBroke > 0 };
}"""

# [5] Nothing but this relic ever carries the state.
BURDEN_JS = """([ids, seeds]) => {
  const DT = AC.CONFIG.physics.dt;
  let bad = 0, checked = 0;
  for (let i = 0; i < ids.length; i++){
    for (const sd of seeds){
      const j = (i + 3) % ids.length;
      if (ids[i] === ids[j]) continue;
      const m = new AC.Match(ids[i], ids[j], sd);
      let steps = 0;
      while (!m.over && steps < 60 / DT){
        m.step(DT); steps++;
        if (m.a.ultSpin || m.b.ultSpin) bad++;
      }
      checked++;
    }
  }
  return { bad, checked };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-redflail.html")
    ap.add_argument("--seeds", type=int, default=8)
    A = ap.parse_args()
    g = (HERE / A.game).resolve()
    seeds = [3301 + i * 4409 for i in range(A.seeds)]

    print(f"\nFLAIL RELIC PROBE -- {g.name}\n")
    with game(game_path=g) as (page, errors):
        roster = page.evaluate(ROSTER_JS)
        mine = [w for w in roster if w["id"] == RID]

        print("[1] THE RELIC")
        check("it is in the roster", len(mine) == 1, f"{len(roster)} relics")
        if not mine:
            sys.exit("no relic, nothing else can be asked")
        w = mine[0]
        print(f"     {w['name']}  {w['aff']} {w['shape']} {w['mode']} "
              f"ult {w['kind']} dmg {w['dmg']}")
        check("it is the bloodsworn flail on the chain profile",
              w["aff"] == "bloodsworn" and w["shape"] == "flail" and w["mode"] == "chain")
        fired = page.evaluate(BRANCH_JS, RID)
        print(f"     draw branches fired: {fired}")
        check("renders through _fhBarbed, not the _fhBase fallback",
              "_fhBarbed" in fired and "_fhBase" not in fired)
        check("and through the razor-point _needle", "_needle" in fired)

        print("\n[2] THE WIND-UP, and [3] THE SPIKES -- natural casts, no forcing")
        rows = page.evaluate(FIELD_JS, [RID, FOES, seeds])
        casts = sum(r["casts"] for r in rows)
        rel   = sum(r["released"] for r in rows)
        brk   = sum(r["breaks"] for r in rows)
        winds = [x for r in rows for x in r["winds"]]
        spikes = sum(r["spikes"] for r in rows)
        print(f"     {len(rows)} matches, mean {statistics.mean(r['dur'] for r in rows):.1f}s")
        print(f"     casts {casts}   released {rel} ({100*rel/max(1,casts):.0f}%)   "
              f"broken {brk} ({100*brk/max(1,casts):.0f}%)")
        if winds:
            winds.sort()
            print(f"     wind-up seconds: median {statistics.median(winds):.2f}   "
                  f"min {winds[0]:.2f}   max {winds[-1]:.2f}")
        check("the wind-up completes at least sometimes", rel > 0,
              f"{rel} of {casts}")
        check("spikes are spawned", spikes > 0, f"{spikes} over {rel} storms")
        if rel:
            print(f"     {spikes/rel:.0f} spikes a storm")
        live = max(r["maxLive"] for r in rows)
        print(f"     peak shots live in any match: {live}  (CONFIG.shot.maxLive is 64)")
        check("the maxLive cap is never reached", live < 64, f"peak {live}")
        print(f"     shot hits landed: {sum(r['shotHits'] for r in rows)} over {len(rows)} matches")
        check("spikes land on the foe", sum(r["shotHits"] for r in rows) > 0)

        print("\n[3b] A SPIKE IS SPENT ON THE WALL, NOT BOUNCED")
        wl = page.evaluate(WALL_JS, [RID])
        print(f"     {wl}")
        check("spawnSpike produces a shot", wl.get("spawned"))
        check("it carries no bounce", not wl.get("bounce"))
        check("and it is gone within 2 seconds", wl.get("live") == 0)

        print("\n[4] WHAT BREAKS IT -- and what must NOT")
        for mode, want_alive, label in [
            ("hitstun", True,  "NEGATIVE CONTROL: ordinary hitstun does NOT break it"),
            ("clank",   True,  "NEGATIVE CONTROL: a clank stun does NOT break it"),
            ("hex",     False, "hex breaks it"),
            ("freeze",  False, "an ult freeze breaks it"),
        ]:
            r = page.evaluate(BREAK_JS, [RID, mode])
            if not r.get("started"):
                check(label, False, "the cast never started -- check is worthless")
                continue
            print(f"     {mode:8} -> alive={r['alive']} phase={r['phase']} broke={r['broke']}")
            check(label, r["alive"] == want_alive,
                  f"alive={r['alive']}, wanted {want_alive}")

        print("\n[5] ZERO BURDEN")
        ids = [x["id"] for x in roster if x["id"] != RID]
        b = page.evaluate(BURDEN_JS, [ids, seeds[:3]])
        print(f"     {b['checked']} matches among the other {len(ids)} relics")
        check("no other relic ever carries ultSpin", b["bad"] == 0,
              f"{b['bad']} frames")

        check("no page errors", not errors, "; ".join(errors[:3]))

    ok = sum(1 for _, v in PASS if v)
    print(f"\n  {ok}/{len(PASS)} checks pass\n")
    return 0 if ok == len(PASS) else 1


if __name__ == "__main__":
    sys.exit(main())
