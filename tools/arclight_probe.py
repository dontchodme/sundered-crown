#!/usr/bin/env python
"""STATIC, ASSERTED AGAINST THE BUILD -- the census gates 2 and 3 ask for.

    python arclight_probe.py --game ../02-chain/sc-storm.html      # stage 2
    python arclight_probe.py --game ../02-chain/sc-static.html     # stage 3

IT READS WHICH STAGE IT IS LOOKING AT OFF THE PAGE rather than being told.
Stage 2 is "the storm exists. No ward, no damage", so its damage checks are
checks that NOTHING happened; stage 3 is the ward and the detonation, and the
same instrument read the other way round is the gate. A flag would let the two
drift -- a probe run against the wrong build would report the wrong thing and
pass.

THE MEASUREMENT IS TAKEN AROUND `tickStatic`'S OWN CALL, NOT AROUND THE FRAME
IT RAN ON. A frame carries the blade's hits as well, and a blade hit
legitimately moves the quarry's hp, banks the caster's ward, files a beat and
raises hit stop -- so a frame-level check would report the BLADE as a defect in
the storm. That is CLAUDE.md's most repeated probe fault (five false defects in
one file in v60, five more in v59, three in v61): **a check that counts frames
in which an event is possible is not counting the event.** Wrapping the ticker
puts the before/after either side of the storm and nothing else, and the frame
that ENDS a cast is accounted separately from the frames that run it -- because
at stage 3 those two frames are allowed opposite things.

AND `Math.random` IS STUBBED TO COUNT ITSELF. Brief section 3 trap 1 -- a
`Math.random` anywhere in the storm breaks `engine_ab`, and it breaks it
silently: the page runs, the fight looks right, and two runs of one seed
differ. A grep of the builder's own inserts can only see the builder; this sees
the shipped page.
"""
from __future__ import annotations
import argparse, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scpage import game  # noqa: E402

RUN_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, A = AC.CONFIG.arena;

  /* THE RANDOMNESS TRAP, CLOSED ON THE SHIPPED PAGE. Nothing in this engine is
     allowed to call `Math.random` -- every draw goes through the match's own
     mulberry32 -- so a counter that ends at anything but zero is a determinism
     bug that `engine_ab` would find later and more expensively. */
  const W = window.__arc = { rand: 0 };
  if (!window.__arcRandStubbed){
    Math.random = function(){ W.rand++; return 0.5; };
    window.__arcRandStubbed = 1;
  }

  const DETONATES = typeof AC.Match.prototype.stormBlow === "function";

  if (!AC.Match.prototype.__arcWrapped){
    const orig = AC.Match.prototype.tickStatic;
    AC.Match.prototype.tickStatic = function(dt){
      const S = this.storm;
      if (!S) return orig.call(this, dt);
      const src = S.src === "a" ? this.a : this.b;
      const foe = S.src === "a" ? this.b : this.a;
      const b = { hp: foe.hp, sh: src.shield || 0, shM: src.shieldMax || 0,
                  fsh: foe.shield || 0, alive: foe.alive,
                  beats: this.beats.length, stop: this.hitStop,
                  stun: foe.stun, vx: foe.vx, vy: foe.vy };
      const r = orig.call(this, dt);
      const O = window.__arcOut;
      const ended = !this.storm;
      const d = { hp: b.hp - foe.hp,
                  ward: (src.shield || 0) - b.sh,
                  fward: (foe.shield || 0) - b.fsh,
                  beats: this.beats.length - b.beats,
                  stop: this.hitStop > b.stop,
                  stun: foe.stun > b.stun,
                  knock: foe.vx !== b.vx || foe.vy !== b.vy };

      if (!ended){
        /* THE WINDOW'S OWN FRAMES. Nothing here is allowed to deal damage in
           either stage -- the only damage in this ultimate is the detonation --
           and at stage 2 the ward is not allowed to move either. */
        O.winFrames++;
        if (d.hp !== 0) O.winHp++;
        if (d.ward !== 0) O.winWard++;
        if (d.fward !== 0) O.winFoeWard++;
        if (d.beats !== 0) O.winBeat++;
        if (d.stop) O.winStop++;
        if (d.stun) O.winStun++;
        if (d.knock) O.winKnock++;
        if (src.shield > (AC.STATUS ? AC.STATUS.ward.cap : 90)) O.overCap++;
        const n = this.inset, r0 = src.w.ult.r;
        for (const x of this.storm.bolts){
          if (x.x < n + r0 - 0.6 || x.x > A.w - n - r0 + 0.6
              || x.y < n + r0 - 0.6 || x.y > A.h - n - r0 + 0.6){
            O.outOfHall++; break;
          }
        }
        if (this.storm.bolts.length > O.peakSeen)
          O.peakSeen = this.storm.bolts.length;
        return r;
      }

      /* THE CENSUS, TAKEN ON THE STEP THAT ENDS THE CAST. `S` is the object the
         ticker just nulled; reading `this.storm` after the step sees nothing at
         all, which is the sampling fault Bloodmirror's probe filed 24 defects
         with. */
      O.casts++;
      O.rows.push({ t: +S.t.toFixed(3), blows: S.blows, spawned: S.spawned,
                    forked: S.forked, eaten: S.eaten, died: S.died,
                    walls: S.walls, refused: S.refused, peak: S.peak,
                    alive: S.bolts.length,
                    /* THE HALL IS SMALLER LATE, AND THAT IS THE ONE THING THE
                       DESIGN'S OVERLAY DID NOT MODEL: `storm_price` bounces its
                       bolts off the ARENA, this build bounces them off
                       `m.inset`, and the seals walk it 0 -> 140. A swarm in a
                       smaller room comes back to the quarry more often.
                       Recorded per cast so the claim is measurable rather than
                       argued. */
                    ins: +this.inset.toFixed(1),
                    mt: +this.t.toFixed(1),
                    /* THE DETONATION, ATTRIBUTED TO ITS OWN FRAME. */
                    inBlast: S.inBlast || 0, hits: S.hits || 0,
                    dealt: +(S.dealt || 0).toFixed(1),
                    banked: +(S.banked || 0).toFixed(1),
                    dHp: +d.hp.toFixed(1), dWard: +d.ward.toFixed(1),
                    dBeats: d.beats, dStop: d.stop ? 1 : 0,
                    dStun: d.stun ? 1 : 0, dKnock: d.knock ? 1 : 0,
                    killed: b.alive && !foe.alive ? 1 : 0,
                    foeWasAlive: b.alive ? 1 : 0,
                    hp: +foe.hp.toFixed(1) });
      return r;
    };
    AC.Match.prototype.__arcWrapped = 1;
  }

  const O = window.__arcOut = { casts: 0, rows: [], winFrames: 0,
                                winHp: 0, winWard: 0, winFoeWard: 0,
                                winBeat: 0, winStop: 0, winStun: 0,
                                winKnock: 0, overCap: 0,
                                movedFrozen: 0, frozenSteps: 0,
                                outOfHall: 0, peakSeen: 0, alive: 0,
                                fights: 0, det: DETONATES, err: null };
  try {
    for (const foe of foes){
      for (const sd of seeds){
        const m = new AC.Match(rid, foe, sd);
        let step = 0;
        while (!m.over && step < secs / DT){
          /* THE FREEZE IS SAMPLED AT THE TOP OF THE STEP, which is the only
             place it means what it says. Read INSIDE the ticker it means
             "something earlier in this step raised a hit stop" -- `tickShots`
             and six window tickers run before this one -- and that step is
             still a LIVE step whose bolts are supposed to move. Sampled here it
             means "this step returns through `decayImpactOnly`", and a bolt
             that moved across it would be a bolt on the wrong clock. The first
             cut of this check read it inside and reported 148 defects that were
             the engine working. */
          const frozen = m.hitStop > 0 && m.storm && m.storm.bolts.length > 0;
          const was = frozen ? m.storm.bolts.map(x => [x.x, x.y]) : null;
          m.step(DT); step++;
          if (frozen){
            O.frozenSteps++;
            const now = m.storm ? m.storm.bolts : [];
            for (let i = 0; i < Math.min(was.length, now.length); i++)
              if (now[i].x !== was[i][0] || now[i].y !== was[i][1]){
                O.movedFrozen++; break;
              }
          }
        }
        O.fights++;
        if (m.storm) O.alive++;
      }
    }
  } catch (e){ O.err = String(e && e.stack || e); }
  O.rand = W.rand;
  return O;
}"""


# AND THE RENDER PATH IS CALLED, NOT GREPPED. v48 shipped two picture faults
# through 27 green probe checks, a 280-match `engine_ab`, `chain_audit` and
# `post_identity`: `_drawBeam` reached for a MATCH method from the RENDERER, and
# `drawUltUnder` handed a NaN to `createRadialGradient`. The probe's own check
# passed on the first one because it was REGEXING the source for a call --
# **a string does not resolve a reference.**
#
# So this drives a real match to a standing storm and calls the renderer's own
# functions against a real 2D context. `drawStorm` is new code that no headless
# check in this repo would otherwise ever execute, and `ULTSIG.arclight` is a
# brand-new sigil that is drawn only when a HUD is on screen.
DRAW_JS = r"""([rid, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const R = AC.renderer;
  if (!R || !R.ctx) return { skip: "no renderer/context" };
  const out = { storm: 0, under: 0, over: 0, sig: 0, bolts: 0, threw: null };
  for (const foeId of foes){
    for (const sd of seeds){
      const m = new AC.Match(rid, foeId, sd);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        if (!m.storm) continue;
        try {
          R.ctx.save(); R.drawStorm(m); R.ctx.restore();
          out.storm++;
          out.bolts = Math.max(out.bolts, m.storm.bolts.length);
        } catch (e){ out.threw = "drawStorm: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltUnder(m); R.ctx.restore(); out.under++; }
        catch (e){ out.threw = "drawUltUnder: " + String(e); return out; }
        try { R.ctx.save(); R.drawUltOver(m); R.ctx.restore(); out.over++; }
        catch (e){ out.threw = "drawUltOver: " + String(e); return out; }
        /* THE SIGIL, WITH ITS OWN ARGUMENTS. `ULTSIG[w.id]` is called from the
           HUD with the match clock and the charge fraction, and a new entry is
           the one piece of this relic that a headless run can never reach. */
        if (out.sig < 60){
          try {
            R.ctx.save();
            AC.ULTSIG.arclight(R.ctx, m.t, out.sig / 60,
                               AC.AFFINITIES.vigil);
            R.ctx.restore();
            out.sig++;
          } catch (e){ out.threw = "ULTSIG.arclight: " + String(e); return out; }
        }
      }
      if (out.storm > 600 && out.sig >= 60) return out;
    }
  }
  return out;
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-static.html")
    ap.add_argument("--relic", default="arclight")
    ap.add_argument("--foes", default="")
    ap.add_argument("--seeds", default="")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--secs", type=float, default=120.0)
    A = ap.parse_args()
    seeds = ([int(x) for x in A.seeds.split(",")] if A.seeds
             else [11961 + i * 977 for i in range(A.n)])

    with game(game_path=(HERE / A.game).resolve()) as (pg, errs):
        ids = pg.evaluate("() => AC.WEAPONS.map(w => w.id)")
        foes = (A.foes.split(",") if A.foes
                else [i for i in ids if i != A.relic])
        r = pg.evaluate(RUN_JS, [A.relic, foes, seeds, A.secs])
        dr = pg.evaluate(DRAW_JS, [A.relic, foes[:6], seeds[:2], A.secs])

    if r["err"]:
        print("THREW:\n" + r["err"])
        return 1
    rows = r["rows"]
    n_f = r["fights"]
    det = r["det"]
    print(f"\nSTATIC -- stage {'3 (the ward and the detonation)' if det else '2 (the storm, and nothing else)'}"
          f", {n_f} fights ({len(foes)} foes x {len(seeds)} seeds), "
          f"{r['casts']} casts\n")
    checks = []

    def chk(ok, label, detail):
        checks.append(bool(ok))
        print(f"  {'PASS' if ok else 'FAIL'}  {label}\n        {detail}")

    def mean(k, pop=None):
        p = rows if pop is None else pop
        return sum(x[k] for x in p) / len(p) if p else 0.0

    chk(r["casts"] > 0, "the ultimate casts at all",
        f"{r['casts']} casts over {n_f} fights "
        f"({r['casts']/max(1,n_f):.2f} a fight; charge 15 predicts ~2-3)")

    # THE DESIGN'S OWN INVARIANT, and it is the one `storm_lab` asserted per
    # cast before any of this was built: nothing appears and nothing vanishes
    # except through the four doors.
    bad = [x for x in rows
           if x["spawned"] + x["forked"] != x["eaten"] + x["died"] + x["alive"]]
    chk(not bad, "the books balance -- spawned + forked = eaten + died + alive",
        f"{len(rows) - len(bad)} of {len(rows)} casts balance"
        + ("" if not bad else f"; first bad {bad[0]}"))

    bad = [x for x in rows if x["spawned"] != x["blows"] * 8 and not x["refused"]]
    chk(not bad, "eight bolts a blade hit, and none from anywhere else",
        f"{sum(x['blows'] for x in rows)} blows -> "
        f"{sum(x['spawned'] for x in rows)} spawned"
        + ("" if not bad else f"; first bad {bad[0]}"))

    # GATE 2's NUMBERS, MEASURED ON THE POPULATION THE MODEL DESCRIBES, WHICH IS
    # THE OPEN HALL. `storm_price.py` bounces its bolts off the ARENA (`x <
    # P.rb`, `x > W - P.rb`); this build bounces them off `m.inset`, which the
    # seals walk 0 -> 140 across a fight. Those are the same room only while the
    # hall is open, and pooling the two populations compares a build against a
    # model of a different arena. The closed-hall rows are a FINDING rather than
    # a failure -- see the table at the foot of this run.
    OPEN = 40
    op = [x for x in rows if x["ins"] < OPEN]
    want = {"spawned": (17, 20), "forked": (30, 30), "eaten": (21, 21),
            "alive": (24, 24), "peak": (30, 30)}
    got = {k: mean(k, op) for k in want}
    off = {k: (round(got[k], 1), v) for k, v in want.items()
           if not (v[0] * 0.75 <= got[k] <= v[1] * 1.25)}
    chk(op and not off,
        "IN THE OPEN HALL the swarm is the one the design priced (within 25%)",
        f"{len(op)} of {len(rows)} casts opened at inset < {OPEN}:  "
        + "  ".join(f"{k} {got[k]:.1f} (want {v[0]}-{v[1]})"
                    for k, v in want.items())
        + ("" if not off else f"\n        OUT OF BAND: {off}"))

    zero = sum(1 for x in rows if x["blows"] == 0)
    chk(rows and zero / len(rows) <= 0.30,
        "a storm needs a spark -- casts that grow nothing are the minority",
        f"{zero} of {len(rows)} casts landed no blade hit inside the window "
        f"({100*zero/max(1,len(rows)):.0f}%; the model says 8-12%, and the "
        f"brief FORBIDS a fallback spawn)")

    # AND THIS ONE IS EXPECTED TO FAIL ON THE SHIPPED NUMBERS, WHICH IS WHY IT
    # IS LEFT IN. Brief section 0: "cap 60 bolts alive -- never binds at these
    # numbers (peak ~30). A safety, not a knob." It never binds in the open hall
    # and it binds hard once the seals have closed, so on the whole population
    # the cap IS a knob. Weakening the check to make the run green would delete
    # the only measurement that says so.
    chk(sum(x["refused"] for x in rows) == 0 and r["peakSeen"] < 60,
        "the cap is a safety and never binds",
        f"peak seen {r['peakSeen']} of a cap of 60, "
        f"{sum(x['refused'] for x in rows)} spawns refused; refused in "
        f"{sum(1 for x in rows if x['refused'])} of {len(rows)} casts and "
        f"{sum(1 for x in op if x['refused'])} of {len(op)} while the hall "
        f"was open")

    chk(sum(x["eaten"] for x in rows) > 0 and sum(x["died"] for x in rows) > 0,
        "both sinks are real -- the caster eats and the walls kill",
        f"{sum(x['eaten'] for x in rows)} eaten, "
        f"{sum(x['died'] for x in rows)} spent on a 7th wall, "
        f"{sum(x['walls'] for x in rows)} ricochets")

    chk(r["outOfHall"] == 0, "no bolt is ever outside the hall",
        f"{r['outOfHall']} ticker calls left a bolt in the stone")

    chk(r["movedFrozen"] == 0 and r["frozenSteps"] > 0,
        "the bolts freeze with everything else",
        f"{r['movedFrozen']} of {r['frozenSteps']} steps that BEGAN frozen "
        f"moved a bolt (must be 0, and the denominator must not be 0 -- a "
        f"check with no chance to fire is not a check)")

    chk(r["winHp"] == 0 and r["winFoeWard"] == 0,
        "the window itself deals nothing -- the only damage is the detonation",
        f"hp moved on {r['winHp']} window frames, the foe's own ward on "
        f"{r['winFoeWard']} (both must be 0 in either stage)")
    chk(r["winBeat"] == 0 and r["winStop"] == 0 and r["winStun"] == 0
        and r["winKnock"] == 0,
        "and the window is silent to the director and to the physics",
        f"beats {r['winBeat']}, hit stops {r['winStop']}, hitstun "
        f"{r['winStun']}, knocks {r['winKnock']}")

    if not det:
        chk(r["winWard"] == 0 and all(x["dWard"] == 0 for x in rows)
            and all(x["dHp"] == 0 for x in rows),
            "STAGE 2: no ward and no detonation",
            f"caster ward moved on {r['winWard']} window frames and on "
            f"{sum(1 for x in rows if x['dWard'])} ending frames; hp moved on "
            f"{sum(1 for x in rows if x['dHp'])} ending frames (all must be 0)")
    else:
        # ---- STAGE 3. THE SAME INSTRUMENT, READ THE OTHER WAY ROUND.
        chk(r["winWard"] > 0, "STAGE 3: the eaten bolts feed the ward",
            f"the caster's pool rose on {r['winWard']} of {r['winFrames']} "
            f"window frames; {mean('banked'):.1f} banked a cast against the "
            f"design's ~35, from {mean('eaten'):.1f} bolts eaten")
        chk(r["overCap"] == 0, "and the 90 cap is never exceeded",
            f"{r['overCap']} frames with a pool over "
            f"{'STATUS.ward.cap'} (the cap is NOT raised for this relic)")

        paid = [x for x in rows if x["foeWasAlive"]]
        blank = [x for x in paid if x["inBlast"] == 0]
        chk(paid and 0.05 <= len(blank) / len(paid) <= 0.35,
            "the finale is a lottery and the radius sets how often it pays",
            f"{len(blank)} of {len(paid)} live casts caught NOTHING "
            f"({100*len(blank)/max(1,len(paid)):.0f}%; the design says 18% at "
            f"blast 80), mean {mean('inBlast', paid):.2f} bolts in the blast "
            f"against the design's ~4")
        chk(mean("dealt", paid) > 0,
            "and it pays in damage through the ordinary path",
            f"{mean('dealt', paid):.1f} damage a cast against the design's ~60 "
            f"(priced through `m.hurt`, which skips crit, jitter, Sunder and "
            f"the quarry's own ward -- the gap is gate 6's to write down)")

        # ONE EVENT, NOT TWENTY-FOUR (brief trap 6). Counted as transitions
        # across the detonation's own frame, so a blade blow on the same frame
        # cannot be mistaken for one of the bolts.
        bad = [x for x in rows if x["dBeats"] > (2 if x["killed"] else 1)]
        chk(not bad, "the detonation files ONE beat, and one more only on a kill",
            f"{sum(x['dBeats'] for x in rows)} beats over {len(rows)} casts, "
            f"{sum(x['killed'] for x in rows)} of them fatal"
            + ("" if not bad else f"; first bad {bad[0]}"))
        bad = [x for x in rows if x["dStun"] or x["dKnock"]]
        chk(not bad, "and it carries no hitstun and no knockback",
            f"{sum(x['dStun'] for x in rows)} casts staggered the quarry, "
            f"{sum(x['dKnock'] for x in rows)} moved it "
            f"(section 1 names neither)")
        dead = [x for x in rows if not x["foeWasAlive"]]
        chk(all(x["dealt"] == 0 and x["hits"] == 0 for x in dead),
            "nothing fires over a corpse",
            f"{len(dead)} casts ended with the quarry already dead and all of "
            f"them paid nothing")

    chk(r["alive"] == 0, "no storm outlives its match",
        f"{r['alive']} matches ended with one standing")

    chk(not dr.get("threw") and not dr.get("skip")
        and dr.get("storm", 0) > 0 and dr.get("sig", 0) > 0,
        "the RENDER PATH runs against a real 2D context",
        f"drawStorm {dr.get('storm',0)} frames (peak {dr.get('bolts',0)} "
        f"bolts), drawUltUnder {dr.get('under',0)}, drawUltOver "
        f"{dr.get('over',0)}, ULTSIG.arclight {dr.get('sig',0)}"
        + (f"\n        THREW: {dr['threw']}" if dr.get("threw") else "")
        + (f"\n        SKIPPED: {dr['skip']}" if dr.get("skip") else "")
        + "\n        (v48 shipped two picture faults through 27 green checks. "
          "A string does not resolve a reference.)")

    chk(r["rand"] == 0, "nothing in the storm calls `Math.random`",
        f"{r['rand']} calls over {r['winFrames']} window frames "
        f"(the stub counts every one; a single call breaks engine_ab)")

    ok = sum(checks)
    print(f"\n  {ok}/{len(checks)} checks pass\n")
    if rows:
        keys = ["blows", "spawned", "forked", "eaten", "died", "alive", "peak",
                "walls"]
        if det:
            keys += ["inBlast", "hits", "dealt", "banked"]
        print("  per cast: " + "  ".join(f"{k} {mean(k):.1f}" for k in keys))
        print(f"  window ran {min(x['t'] for x in rows):.2f}s .. "
              f"{max(x['t'] for x in rows):.2f}s on its own clock")
        # THE HALL CLOSES, AND THE SWARM IS A FUNCTION OF HOW BIG THE ROOM IS.
        # Bucketed rather than averaged, because an average over both
        # populations hides the whole effect.
        print("\n  BY HOW CLOSED THE HALL WAS AT THE CAST:")
        head = f"    {'inset':>10}  {'casts':>5}  {'spawn':>6}  {'fork':>6}  " \
               f"{'eaten':>6}  {'alive':>6}  {'peak':>6}  {'refused':>7}"
        if det:
            head += f"  {'inBlast':>7}  {'dealt':>6}  {'banked':>6}"
        print(head)
        for lo, hi in [(0, 1), (1, 40), (40, 90), (90, 999)]:
            b = [x for x in rows if lo <= x["ins"] < hi]
            if not b:
                continue
            f = lambda k: sum(x[k] for x in b) / len(b)
            line = (f"    {lo:>4}-{hi:<5}  {len(b):>5}  {f('spawned'):>6.1f}  "
                    f"{f('forked'):>6.1f}  {f('eaten'):>6.1f}  "
                    f"{f('alive'):>6.1f}  {f('peak'):>6.1f}  "
                    f"{f('refused'):>7.1f}")
            if det:
                line += (f"  {f('inBlast'):>7.2f}  {f('dealt'):>6.1f}  "
                         f"{f('banked'):>6.1f}")
            print(line)
    return 0 if ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
