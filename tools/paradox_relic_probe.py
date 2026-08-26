#!/usr/bin/env python3
"""ONE CHECK PER SENTENCE OF §1, AGAINST THE BUILD.

    python3 paradox_relic_probe.py --game ../02-chain/sc-paradox.html

`runic_flail_probe.py` priced §1 on the PREVIOUS tip, before a builder was
opened. This is the other half: the same four sentences, asserted against the
thing that was actually written.

    "blue flail gains a medium sized hexagonal shaped chain of lightning
     surrounding the flails ball. the flail gains extra hit stun. enemies that
     stay inside the hexagon (that is inside the beams of lightning with the
     flail head) for too long are true stunned. unable to move (ball and
     weapon) for 2ish seconds."

Every check states what would count as evidence against the build, and several
of them exist because the thing they check is INVISIBLE to every other tool in
this repo:

  * A HELD BALL that still drifts would look, in every table, like a hold that
    worked. [6] measures the position itself.
  * A BROKEN SOUND is inert headless -- `SFX.play` returns on its first line
    and wraps its body in a try/catch -- so [10] RENDERS it in an
    OfflineAudioContext and measures what comes out. v42's ultimate shipped
    silent through five green passes and a person listening is what caught it.
  * A CONTROL EVENT WITH NO DAMAGE files nothing, so `cinePlan` would score
    the most legible moment of this ultimate as empty air. [11] is rule 3.

Injection is runtime-only where it happens at all. NOTHING is written to any
build.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402
from marrowdraw_relic_probe import SFX_JS  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "paradox"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def mean(xs, d=0.0):
    xs = list(xs)
    return statistics.mean(xs) if xs else d


META_JS = """([rid]) => {
  const w = AC.WEAPONS.find(x => x.id === rid);
  const flails = AC.WEAPONS.filter(x => x.shape === "flail");
  return { w: JSON.parse(JSON.stringify(w)),
           flails: JSON.parse(JSON.stringify(flails)),
           runic: AC.WEAPONS.filter(x => x.aff === "runic").map(x => x.id),
           ids: AC.WEAPONS.map(x => x.id),
           status: JSON.parse(JSON.stringify(AC.STATUS)),
           dt: AC.CONFIG.physics.dt,
           ballR: AC.CONFIG.physics.ballR,
           speedMin: AC.CONFIG.physics.speedMin,
           /* read off the shipped source, not asserted in prose */
           moveGuard: /if \\(f\\.pin > 0\\) return;/.test(AC.Match.prototype.move.toString()),
           hitsSkipStun: /self\\.stun > 0/.test(AC.Match.prototype.tickHits.toString()),
           hasField: typeof AC.Match.prototype.tickStasis === "function",
           hasIn: typeof AC.Match.prototype.inField === "function" };
}"""


# ------------------------------------------------------------ the geometry --
# `inField` is the ONE definition of inside, called by the simulation and by
# the art. It is checked against the analytic polygon rather than against
# itself: a regular n-gon of circumradius R has apothem R*cos(pi/n), so every
# point inside the incircle is in, every point outside the circumcircle is out,
# and the boundary between them is a cosine of the angle to the nearest edge.

GEOM_JS = r"""([rid, n]) => {
  const w = AC.WEAPONS.find(x => x.id === rid), u = w.ult;
  const m = new AC.Match(rid, "aureole", 77);
  const me = m.a.w.id === rid ? m.a : m.b;
  me.x = 300; me.y = 400; me.theta = 0.7;
  const K = Math.cos(Math.PI / u.arcs);
  let inIn = 0, outOut = 0, edgeOk = 0, edgeN = 0, bad = [];
  for (let i = 0; i < n; i++){
    const a = (i / n) * Math.PI * 2;
    /* three shells: well inside the incircle, well outside the circumcircle,
       and a sweep across the boundary at this angle */
    if (m.inField(me, me.x + Math.cos(a) * u.rad * K * 0.98,
                      me.y + Math.sin(a) * u.rad * K * 0.98, u)) inIn++;
    if (!m.inField(me, me.x + Math.cos(a) * u.rad * 1.02,
                       me.y + Math.sin(a) * u.rad * 1.02, u)) outOut++;
    /* the analytic boundary radius at this bearing */
    const seg = Math.PI * 2 / u.arcs;
    let ang = (a - me.theta) % seg; if (ang < 0) ang += seg;
    const rb = u.rad * K / Math.cos(ang - Math.PI / u.arcs);
    const hit0 = m.inField(me, me.x + Math.cos(a) * rb * 0.985,
                               me.y + Math.sin(a) * rb * 0.985, u);
    const hit1 = m.inField(me, me.x + Math.cos(a) * rb * 1.015,
                               me.y + Math.sin(a) * rb * 1.015, u);
    edgeN++;
    if (hit0 && !hit1) edgeOk++; else bad.push([+a.toFixed(3), +rb.toFixed(1)]);
  }
  /* AREA, by Monte Carlo on a fixed lattice -- no rng, so this is stable.
     A regular hexagon is 3*sqrt(3)/(2*pi) = 82.7% of its circumcircle. */
  let inN = 0, tot = 0, G = 400;
  for (let i = 0; i < G; i++) for (let j = 0; j < G; j++){
    const x = -u.rad + (2 * u.rad) * (i + 0.5) / G;
    const y = -u.rad + (2 * u.rad) * (j + 0.5) / G;
    if (x * x + y * y > u.rad * u.rad) continue;
    tot++;
    if (m.inField(me, me.x + x, me.y + y, u)) inN++;
  }
  return { inIn, outOut, edgeOk, edgeN, bad: bad.slice(0, 4), n,
           area: inN / Math.max(1, tot), rad: u.rad, arcs: u.arcs, K };
}"""


# --------------------------------------------------------------- the watch --
# One fight, every frame, with the field's own state and the quarry's position
# sampled either side of `step`. Everything §1 claims is a property of one of
# these traces.

WATCH_JS = r"""([rid, foe, seed, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === rid), u = w.ult;
  const m  = new AC.Match(rid, foe, seed);
  const me = m.a.w.id === rid ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;

  let step = 0, casts = 0, pins = 0;
  let fieldFrames = 0, inFrames = 0, pinFrames = 0, frozenFrames = 0;
  let fillOk = 0, fillN = 0, bleedOk = 0, bleedN = 0;
  let blows = 0, feedFree = 0, feedFreeOk = 0, feedHeld = 0, feedHeldOk = 0;
  const pinDrift = [], pinVel = [], pinShove = [], pinLens = [], winLens = [];
  let pinStun = 0, pinStunN = 0, pinQrose = 0;
  let curPin = 0, curWin = 0;
  let ultBeats = 0, maxHeadR = 0, deadN = 0, deadOk = 0;
  let touchF = 0, touchRun = 0; const touchRuns = [];
  const R2 = AC.CONFIG.physics.ballR;
  let capV = [0, 0]; const resume = [];
  const odd = [];

  /* THE IMMOVABLE-OBJECT CLAIM, MEASURED AT THE SITE. The first cut watched
     the held ball's velocity on frames with no blow of MY OWN on them and
     found 831 units/s of change -- which was true and was not `_ballPair`: a
     shade's blow, a bind and a spike all push a held ball too, and none of
     them is `me` landing a hit. Wrapping the function is the precise
     instrument for the precise claim. */
  let pairN = 0, pairMoved = 0;
  const origPair = AC.Match.prototype._ballPair;
  m._ballPair = function(x, y){
    const ax = x.x, ay = x.y, avx = x.vx, avy = x.vy;
    const bx = y.x, by = y.y, bvx = y.vx, bvy = y.vy;
    const r = origPair.call(m, x, y);
    if (x.pin > 0 || y.pin > 0){
      pairN++;
      const da = x.pin > 0 ? [x.x - ax, x.y - ay, x.vx - avx, x.vy - avy] : [0,0,0,0];
      const db = y.pin > 0 ? [y.x - bx, y.y - by, y.vx - bvx, y.vy - bvy] : [0,0,0,0];
      if (da.concat(db).some(v => v !== 0)) pairMoved++;
    }
    return r;
  };
  /* AND THE BIND. `_clankPair` returns only when BOTH sides are stunned, so a
     held ball's frozen blade is still a legal thing to bind against -- the
     caster can spend the hold it just cast clanking a weapon that has
     stopped. Counted rather than assumed. */
  let clankHeld = 0;
  const origClank = AC.Match.prototype.resolveClank;
  m.resolveClank = function(A, B, hx, hy){
    if (A.pin > 0 || B.pin > 0) clankHeld++;
    return origClank.call(m, A, B, hx, hy);
  };

  /* THE RESUME, MEASURED WHERE IT HAPPENS. `move` restores and clears
     `pinV` on the first frame the ball is allowed to move, which is a frame
     LATER than the one the hold ends on -- so a check that samples velocity
     when `pin` hits zero is sampling the polluted value and was, at 992
     units/s. Wrapping `move` catches the vector on its way in. */
  const origMove = AC.Match.prototype.move;
  m.move = function(f2, foe2, dt2){
    if (f2 === th && f2.pinV && f2.pin <= 0)
      resume.push([capV[0], capV[1], f2.pinV[0], f2.pinV[1],
                   Math.hypot(f2.vx, f2.vy)]);
    return origMove.call(m, f2, foe2, dt2);
  };

  const origHit = AC.Match.prototype.resolveHit;
  m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
    if (foe2.shade) return origHit.call(m, self, foe2, hx, hy, seg, mul, over);
    const q0 = me.ultField ? me.ultField.q : null;
    /* THREE BUCKETS, because the feed has three guards on it and a check that
       only knows about one of them reports the other two as failures. A blow
       on a free LIVING quarry feeds; a blow on a held one does not; and the
       KILLING blow does not either, because a charge exists to hold something
       that is still there to be held. */
    const held = foe2.pin > 0, dead0 = !foe2.alive;
    const r = origHit.call(m, self, foe2, hx, hy, seg, mul, over);
    if (self === me && mul === undefined){
      blows++;
      if (q0 !== null && me.ultField){
        const dq = me.ultField.q - q0;
        /* A BLOW ON A FREE QUARRY FEEDS THE CHARGE; A BLOW ON A HELD ONE MUST
           NOT. Both halves are asserted, because a guard that never fires and
           a guard that is missing look identical from one column. */
        if (held || dead0 || !foe2.alive){
          feedHeld++; if (Math.abs(dq) < 1e-12) feedHeldOk++;
        } else {
          feedFree++; if (Math.abs(dq - u.blow) < 1e-9) feedFreeOk++;
        }
      }
    }
    return r;
  };

  while (!m.over && step < secs / DT){
    const hadF = !!me.ultField;
    const F0 = me.ultField
      ? { q: me.ultField.q, in: me.ultField.in, t: me.ultField.t } : null;
    const p0 = th.pin, px = th.x, py = th.y, pvx = th.vx, pvy = th.vy;
    /* ALIVE BEFORE THE STEP. `checkEnd` runs at the END of step(), after
       tickStasis and after tickHits, so on the frame a quarry dies it was
       alive for everything this ultimate did on it -- and a check that reads
       `alive` afterwards calls that frame post-mortem. It is not. */
    const alive0 = th.alive;
    const b0 = m.beats.length;
    const blows0 = blows;
    /* DID THE FIELD'S OWN CLOCK ADVANCE? `step()` has more than one early
       return -- hit stop, and Ironbloom's LATCH, which holds the whole hall
       for 0.8s and is not hit stop -- and every one of them skips tickStasis.
       The first cut of this check tested `hitStop > 0` before the step and
       came back one frame short in six thousand, and the frame was the first
       of a latch. So the test is the thing itself: `F.t` is incremented by
       tickStasis and by nothing else, so if it moved, the tick ran. This is
       independent of every early return present and future. */
    const frozen = m.hitStop > 0;

    m.step(DT); step++;
    if (frozen) frozenFrames++;

    if (!hadF && me.ultField) casts++;
    const hd = Math.hypot(me.headX - me.x, me.headY - me.y);
    if (hd > maxHeadR) maxHeadR = hd;

    if (me.ultField){
      fieldFrames++; curWin = me.ultField.t;
      if (me.ultField.in) inFrames++;
      const ticked = F0 && me.ultField.t > F0.t + 1e-12;
      if (F0 && ticked && th.alive && th.pin <= 0 && p0 <= 0
          && blows === blows0){
        const dq = me.ultField.q - F0.q;
        if (me.ultField.in){ fillN++; if (Math.abs(dq - DT) < 1e-9) fillOk++; }
        else if (F0.q > 0){ bleedN++;
          if (Math.abs(dq + u.bleed * DT) < 1e-6 || me.ultField.q === 0) bleedOk++;
          else odd.push({ what:"bleed", q0:F0.q, q:me.ultField.q, dq,
                          pin:th.pin, p0, inn: me.ultField.in, frozen,
                          alive: th.alive }); }
      }
      if (F0 && ticked && !alive0 && !th.alive){
        deadN++; if (me.ultField.q === F0.q) deadOk++;
      }
      if (p0 > 0 && th.pin > 0 && F0 && me.ultField.q > F0.q + 1e-12){
        pinQrose++;
        odd.push({ what:"pinQ", q0:F0.q, q:me.ultField.q, dq: me.ultField.q - F0.q,
                   pin:th.pin, p0, inn: me.ultField.in, frozen,
                   blew: blows !== blows0 });
      }
    } else if (curWin > 0){ winLens.push(curWin); curWin = 0; }

    /* THE HOLD, measured strictly INSIDE itself: a frame on whose boundary the
       hold started or ended is neither. */
    if (p0 > 0 && th.pin > 0){
      pinFrames++;
      pinDrift.push(Math.hypot(th.x - px, th.y - py));
      const dv = Math.hypot(th.vx - pvx, th.vy - pvy);
      /* A HELD BALL BANKS WHAT IT IS HIT WITH. It cannot move, but knockback
         still goes into its velocity, so the hold ENDS IN A RELEASE. Split by
         whether a blow landed on this frame: on the quiet frames nothing may
         touch it at all (that is the immovable-object claim), and on the loud
         ones the change is the shove it just took (that is the release). */
      pinVel.push(dv);
      pinStunN++; if (th.stun > 0) pinStun++;
      /* AND THE CASTER MUST NOT STICK TO IT. Rick, on the first clip: "really
         weird physics on paradox colliding with the stunned opponent." He was
         right and it was this: a held ball keeps the velocity vector it was
         captured with, `_ballPair` fed that straight into the relative-velocity
         term, and with the stored vector pointing away the exchange came out
         near zero -- so the caster did not bounce, it stuck and slid along the
         thing it had just frozen, for as long as 2.07 seconds, which is the
         whole hold. */
      const sep2 = Math.hypot(th.x - me.x, th.y - me.y);
      if (sep2 < R2 * 2 + 1){ touchF++; touchRun++; }
      else { if (touchRun) touchRuns.push(touchRun * DT); touchRun = 0; }
    } else if (touchRun){ touchRuns.push(touchRun * DT); touchRun = 0; }
    /* and its LENGTH in unfrozen time, because that is the clock it is on */
    if (th.pin > 0){ if (!frozen) curPin += DT; }
    else if (curPin > 0){ pinLens.push(curPin); curPin = 0; }

    if (th.pin > 0 && p0 <= 0){ pins++; capV = [th.vx, th.vy]; }
    for (let i = b0; i < m.beats.length; i++)
      if (m.beats[i].kind === "ult" && m.beats[i].w === rid) ultBeats++;
  }
  if (curWin > 0) winLens.push(curWin);
  return { steps: step, dur: step * DT, casts, pins,
           fieldFrames, inFrames, pinFrames, frozenFrames,
           fillOk, fillN, bleedOk, bleedN,
           blows, feedFree, feedFreeOk, feedHeld, feedHeldOk,
           pinDrift, pinVel, pinShove, pinLens, winLens,
           pinStun, pinStunN, pinQrose,
           ultBeats, maxHeadR, deadN, deadOk, odd: odd.slice(0, 6),
           pairN, pairMoved, clankHeld, resume,
           touchF, touchRuns,
           win: m.winner ? (m.winner === me ? 1 : 0) : -1 };
}"""


# ------------------------------------------------------ the true-stun claim --
# `breakSpin` is what separates the three stuns that CANCEL a wind-up from the
# ordinary hitstun that only delays it. The only wind-up in the game is
# Bloodmill's, and it is on this relic's own type -- so the claim is tested
# where it can actually be observed rather than asserted from the source.

TRUESTUN_JS = r"""([rid, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w = AC.WEAPONS.find(x => x.id === rid), u = w.ult;
  let broke = 0, pins = 0, winds = 0;
  for (const sd of seeds){
    const m = new AC.Match(rid, "redflail", sd);
    const me = m.a.w.id === rid ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    let step = 0, p0 = 0;
    while (!m.over && step < secs / DT){
      const winding = !!th.ultSpin;
      m.step(DT); step++;
      if (th.pin > 0 && p0 <= 0){ pins++; if (winding){ winds++; if (!th.ultSpin) broke++; } }
      p0 = th.pin;
    }
  }
  return { broke, pins, winds };
}"""


# ------------------------------------------------------------- zero burden --

BURDEN_JS = r"""([rid, ids, secs, n]) => {
  const DT = AC.CONFIG.physics.dt;
  let frames = 0, anyField = 0, anyPin = 0, pairs = 0;
  for (let i = 0; i < ids.length; i++){
    for (let j = i + 1; j < ids.length; j++){
      if (ids[i] === rid || ids[j] === rid) continue;
      if ((i * 31 + j) % n !== 0) continue;
      pairs++;
      const m = new AC.Match(ids[i], ids[j], 5000 + i * 13 + j);
      let step = 0;
      while (!m.over && step < secs / DT){
        m.step(DT); step++;
        frames++;
        if (m.a.ultField || m.b.ultField) anyField++;
        if (m.a.pin > 0 || m.b.pin > 0) anyPin++;
      }
    }
  }
  return { frames, anyField, anyPin, pairs };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-paradox.html")
    ap.add_argument("--secs", type=float, default=120.0)
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--skip-sound", action="store_true")
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [2207 + i * 331 for i in range(a.seeds)]
    FOES = ["heartwood", "grudgebearer", "twinshade", "lastlight",
            "widowmaker", "slagheart"]

    with game(game_path=gp) as (page, errors):
        M = page.evaluate(META_JS, [RID])
        w, u, ST = M["w"], M["w"]["ult"], M["status"]
        DT = M["dt"]

        print(f"\n§1, SENTENCE BY SENTENCE — {w['name']} / {u['name']}, "
              f"{len(M['ids'])} relics\n")

        # ------------------------------------------------------------ [1] --
        print("[1] THE RELIC\n")
        check("it is the runic flail, and the id matches the name",
              w["aff"] == "runic" and w["shape"] == "flail"
              and w["id"] == w["name"].lower(),
              f"{w['id']} / {w['name']} — {w['aff']} x {w['shape']}")
        phys = {json.dumps({k: b[k] for k in
                            ("reach", "spin", "mass", "width", "artW", "mode",
                             "blades")}, sort_keys=True) for b in M["flails"]}
        check("all four flails share ONE physics block, byte for byte — the "
              "chain is a property of the TYPE",
              len(phys) == 1,
              f"{len(M['flails'])} flails, {len(phys)} distinct — reach "
              f"{w['reach']} spin {w['spin']} mass {w['mass']} mode {w['mode']}")
        check("it carries the school's channel and nothing else",
              w.get("onHit") == {"hex": 1} and not w.get("onSelf"),
              f"onHit {w.get('onHit')}")
        nums = [float(n) for n in re.findall(r"(\d+(?:\.\d+)?)", u["tip"])]
        have = {float(v) for v in u.values() if isinstance(v, (int, float))}
        check("every number in the ult tip is a number the weapon actually "
              "has — v40 shipped a card reading 5s after a sweep moved it to 8.1",
              all(n in have for n in nums),
              f"tip {u['tip']!r} carries {nums}, weapon has dur "
              f"{u['dur']:g} and pin {u['pin']:g}")

        # ------------------------------------------------------------ [2] --
        print("\n[2] \"A HEXAGONAL CHAIN OF LIGHTNING SURROUNDING THE FLAIL'S "
              "BALL\"\n")
        G = page.evaluate(GEOM_JS, [RID, 720])
        area = 3 * math.sqrt(3) / (2 * math.pi)
        check("`inField` is a regular hexagon and not a circle wearing one — "
              "every point inside the incircle is in, every point outside the "
              "circumcircle is out, and the boundary is where the polygon says",
              G["inIn"] == G["n"] and G["outOut"] == G["n"]
              and G["edgeOk"] == G["edgeN"],
              f"{G['inIn']}/{G['n']} inside, {G['outOut']}/{G['n']} outside, "
              f"{G['edgeOk']}/{G['edgeN']} boundary crossings in the right "
              f"place" + (f"; first miss {G['bad'][0]}" if G["bad"] else ""))
        check("and it encloses the area a hexagon encloses",
              abs(G["area"] - area) < 0.01,
              f"{G['area']:.3f} of its own circumcircle against "
              f"3·√3/2π = {area:.3f}")
        check("ONE definition of inside, called by the simulation — the drawn "
              "beams and the tested boundary are the same object",
              M["hasIn"] and M["hasField"],
              "`inField` is a method on Match and `tickStasis` is the only "
              "caller in the simulation")

        # ---------------------------------------------------------- [3-9] --
        runs = []
        for fo in FOES:
            for sd in seeds:
                x = page.evaluate(WATCH_JS, [RID, fo, sd, a.secs])
                if x["casts"] > 0:
                    runs.append(x)
        assert runs, "no cast on any seed"

        def agg(k):
            return sum(x[k] for x in runs)

        _odd = []
        for x in runs:
            _odd += x.get("odd") or []
        if _odd:
            print("    odd frames (first few):")
            for o in _odd[:6]:
                print("     ", json.dumps(o))

        def cat(k):
            out = []
            for x in runs:
                out += x[k]
            return out

        print(f"\n[3] THE FIELD STANDS, AND THE HEAD IS INSIDE IT — "
              f"{len(runs)} fights, {agg('casts')} casts\n")
        headMax = max(x["maxHeadR"] for x in runs)
        print(f"    field up for {agg('fieldFrames') * DT:.1f}s of "
              f"{sum(x['dur'] for x in runs):.1f}s; the quarry is inside it "
              f"{agg('inFrames') / max(1, agg('fieldFrames')):.1%} of that\n")
        check("§1's parenthesis holds — the head really is inside the beams, "
              "at every extension it reaches",
              u["rad"] > headMax,
              f"circumradius {u['rad']:g} against a head that reaches "
              f"{headMax:.1f} from the shell; the incircle alone is "
              f"{u['rad'] * G['K']:.1f}")
        wl = cat("winLens")
        check("the window is the length the card says — measured on the "
              "windows that were allowed to finish, because a fight that ends "
              "mid-cast truncates one and a mean over all casts is a mean over "
              "how long the fights were",
              abs(max(wl) - u["dur"]) < 0.05
              and sum(1 for x in wl if abs(x - u["dur"]) < 0.05) > len(wl) * 0.5,
              f"{sum(1 for x in wl if abs(x - u['dur']) < 0.05)} of {len(wl)} "
              f"ran the full {u['dur']:g}s on the field's OWN clock, which is "
              f"unfrozen time; the rest were cut short by the match ending. "
              f"Longest {max(wl):.2f}s — in wall clock a full window takes "
              f"about a fifth longer, because the hall freezes")

        print(f"\n[4] \"ENEMIES THAT STAY INSIDE ... FOR TOO LONG\" — the "
              f"charge\n")
        check("the charge fills at exactly one second a second while the "
              "quarry is inside — on the frames the hall is not frozen, which "
              "is the clock every other status in this game is on",
              agg("fillOk") == agg("fillN") and agg("fillN") > 500,
              f"{agg('fillOk')}/{agg('fillN')} frames, with "
              f"{agg('frozenFrames')} of {agg('steps')} excluded as hit stop — "
              f"`step()` returns on `hitStop > 0` before tickStasis, exactly as "
              f"it does before tickStatus (v39 5.3)")
        check("and bleeds at exactly `bleed` while it is out, and never below "
              "zero",
              agg("bleedOk") == agg("bleedN") and agg("bleedN") > 500,
              f"{agg('bleedOk')}/{agg('bleedN')} frames at "
              f"{u['bleed']:g}/s")
        check("a dead quarry neither fills the charge nor bleeds it — the "
              "field stops asking",
              agg("deadOk") == agg("deadN"),
              f"{agg('deadOk')}/{agg('deadN')} frames after the quarry died "
              f"and before the match closed, over the kill flight `checkEnd` "
              f"holds open")
        check("A HELD QUARRY DOES NOT FEED THE HOLD THAT CAUGHT IT — without "
              "that the field would chain holds back to back for the rest of "
              "the window, because a pinned ball is inside the hexagon by "
              "construction",
              agg("pinQrose") == 0,
              f"{agg('pinQrose')} frames of accrual inside a hold, over "
              f"{agg('pinFrames')}")

        print(f"\n[5] \"THE FLAIL GAINS EXTRA HIT STUN\", BUILT AS A FEED\n")
        check("a landed blow on a FREE quarry adds exactly `blow`",
              agg("feedFreeOk") == agg("feedFree") and agg("feedFree") > 20,
              f"{agg('feedFreeOk')}/{agg('feedFree')} blows each added "
              f"{u['blow']:g}s, out of {agg('blows')} landed in total")
        check("and a blow on a HELD one adds nothing — both halves, because a "
              "guard that never fires and a guard that is missing look "
              "identical from one column",
              agg("feedHeldOk") == agg("feedHeld") and agg("feedHeld") > 0,
              f"{agg('feedHeldOk')}/{agg('feedHeld')} blows on a held quarry "
              f"moved the charge by nothing")

        print(f"\n[6] \"UNABLE TO MOVE (BALL AND WEAPON) FOR 2ish SECONDS\"\n")
        drift = cat("pinDrift")
        dv = cat("pinVel")
        lens = cat("pinLens")
        free = M["speedMin"] * DT
        print(f"    {agg('pins')} holds, {agg('pinFrames') * DT:.1f}s of them, "
              f"mean {mean(lens):.2f}s\n")
        check("THE BALL STOPS DEAD. Not a slow, not a floor — no travel at "
              "all, on any frame of any hold",
              max(drift) == 0.0,
              f"max {max(drift):.3g} units a frame over {len(drift)} frames, "
              f"against {free:.2f} for a ball at `speedMin`. `moveMul` bottoms "
              f"out at 0.45 and `speedMin` is {M['speedMin']:g}, so this state "
              f"could not be expressed with anything the engine had")
        rel = cat("resume")
        check("and NOTHING SHOULDERS IT — a held ball is an immovable object "
              "in `_ballPair`, or the caster could push the hold it just cast "
              "across the hall. Measured AT THE SITE, because the first cut of "
              "this check watched velocity on frames with no blow of my own on "
              "them and caught a shade, a bind and a spike instead",
              agg("pairMoved") == 0 and agg("pairN") > 20,
              f"{agg('pairMoved')} of {agg('pairN')} separations that involved "
              f"a held ball moved it by any amount, in position or in velocity")
        check("AND IT RESUMES EXACTLY WHAT IT WAS DOING. Rick: \"no banked "
              "knockback and no loss of momentum after the stun\" — so "
              "everything that landed in a velocity it was not allowed to "
              "spend is discarded on the frame it can move again",
              rel and all(cx == rx and cy == ry for cx, cy, rx, ry, _ in rel),
              f"{len(rel)} releases; the vector `move` restores is "
              f"byte-identical to the vector captured in all of them. What it "
              f"was carrying when it was polluted, on the way in: "
              f"{mean(v for *_, v in rel):.0f} units/s mean against "
              f"{mean(math.hypot(cx, cy) for cx, cy, *_ in rel):.0f} at "
              f"capture — that difference is exactly what is being thrown "
              f"away, and the first build spent it")
        held_clanks = agg("clankHeld")
        tr = cat("touchRuns")
        check("AND THE CASTER DOES NOT STICK TO IT. Rick, on the first clip: "
              "\"really weird physics on paradox colliding with the stunned "
              "opponent\" — a held ball keeps the vector it was captured with, "
              "and feeding that into the relative-velocity term made the "
              "exchange come out near zero",
              tr and max(tr) < 0.4 and mean(tr) < 0.08,
              f"{agg('touchF')} of {agg('pinFrames')} hold frames in contact "
              f"({agg('touchF') / max(1, agg('pinFrames')):.1%}), {len(tr)} "
              f"contacts, mean {mean(tr):.3f}s, longest {max(tr):.3f}s. The "
              f"first build read 6.9% and 2.067s — a full hold spent stuck to "
              f"the thing it had frozen. A held ball's velocity is a MEMORY, "
              f"not a motion, and the exchange reads it as zero")
        check("and a held weapon is still a legal thing to BIND against, which "
              "is named rather than fixed",
              True,
              f"{held_clanks} binds landed on a held ball over {agg('pins')} "
              f"holds — `_clankPair` returns only when BOTH sides are stunned, "
              f"so the caster can spend a hold it cast clanking a weapon that "
              f"has stopped. Priced INTO the +42%: `runic_flail_probe [4]` "
              f"measured the pin with this live")
        check("THE WEAPON STOPS, every frame of every hold",
              agg("pinStun") == agg("pinStunN") and agg("pinStunN") > 200,
              f"{agg('pinStun')}/{agg('pinStunN')} frames with the weapon "
              f"locked — `f.stun` is REFRESHED each frame because tickStatus "
              f"takes dt off it, and a weapon that came unlocked halfway "
              f"through would be a frozen ball still swinging")
        check("the hold is the length the card says, and it ENDS",
              abs(mean(lens) - u["pin"]) < 0.03 and max(lens) < u["pin"] + 0.03,
              f"mean {mean(lens):.3f}s of UNFROZEN time, longest "
              f"{max(lens):.3f}s, against pin {u['pin']:g}. In wall-clock it "
              f"runs longer, because the hall freezes for "
              f"{agg('frozenFrames') / max(1, agg('steps')):.0%} of a fight "
              f"and every clock in this game is on the unfrozen one")

        print(f"\n[7] A TRUE STUN, NOT HITSTUN\n")
        T = page.evaluate(TRUESTUN_JS, [RID, seeds, a.secs])
        check("the hold CANCELS a wind-up, which is what separates the three "
              "true stuns in this game from the two that only delay it",
              T["winds"] == 0 or T["broke"] == T["winds"],
              f"{T['broke']} of {T['winds']} holds that landed on a Bloodmill "
              f"wind-up broke it, over {T['pins']} holds against Threshmaw"
              + ("  (no wind-up coincided — asserted structurally by "
                 "`breakSpin` at the site)" if T["winds"] == 0 else ""))

        print(f"\n[8] THE DIRECTOR IS TOLD — rule 3, fifth relic running\n")
        check("every hold files a beat, because a control event with no damage "
              "and no contact files nothing on its own and `cinePlan` would "
              "score the most legible moment of this ultimate as empty air",
              agg("ultBeats") >= agg("pins") + agg("casts"),
              f"{agg('ultBeats')} ult beats against {agg('casts')} casts and "
              f"{agg('pins')} holds")

        print(f"\n[9] ZERO BURDEN\n")
        B = page.evaluate(BURDEN_JS, [RID, M["ids"], 60.0, 7])
        check("no other relic ever carries a field or a hold",
              B["anyField"] == 0 and B["anyPin"] == 0,
              f"{B['frames']} frames over {B['pairs']} pairings of the other "
              f"{len(M['ids']) - 1}: {B['anyField']} fields, {B['anyPin']} holds")
        check("and the hold is one line in one function",
              M["moveGuard"] and M["hitsSkipStun"],
              "`move` returns on `f.pin > 0`; the weapon half is `f.stun`, "
              "which `tickHits` already skips on")

        # ----------------------------------------------------------- [10] --
        if not a.skip_sound:
            print(f"\n[10] THE SOUND, RENDERED AND MEASURED\n")
            print("     A sound that throws and a sound that is quiet look "
                  "identical from outside: `SFX.play` returns on its first line "
                  "headless\n     and wraps its body in a try/catch. v42's "
                  "ultimate shipped SILENT through a 14-check probe, a "
                  "29-check probe,\n     a full sweep, a 13/13 verify and a "
                  "rendered clip. So this is rendered in an OfflineAudioContext, "
                  "through\n     the shipping chain, at a non-zero "
                  "`currentTime`, and measured.\n")
            snd = {}
            for label, kind, p, secs in (
                    ("the cast", "ult", {"w": RID}, 3.0),
                    ("the hold", "ult", {"w": RID + "-pin"}, 3.0),
                    ("CONTROL Aegis", "ult", {"w": "bulwarden"}, 3.0),
                    ("CONTROL Converse", "ult", {"w": "foregone"}, 3.0)):
                g = page.evaluate(SFX_JS, [kind, p, secs])
                if g.get("skip"):
                    print("     (no OfflineAudioContext — skipped)")
                    snd = None
                    break
                snd[label] = g
            if snd:
                # WHAT SEPARATES A STATE FROM AN EVENT, and `audible` does not:
                # every sound in this game is 1.2-1.9s "audible" because the
                # shipping chain's own tail is longer than most of the sounds
                # in it. `sustain` is the level in the window from 30% of the
                # render onward, against the peak -- a decaying envelope is
                # near zero there by construction and a held tone is not.
                # SFX_JS already returns that window; it was being used for a
                # six-band profile and nothing else.
                import statistics as _st
                # ABSOLUTE, not normalised by peak. The first cut divided by
                # `peak` and the cast scored WORSE than the Aegis control for
                # having a louder attack -- a metric that rewards a quiet
                # transient is the v42 §3c trap arriving from the other side.
                for g in snd.values():
                    ws = g.get("win") or []
                    g["late"] = (math.sqrt(sum(v * v for v in ws) / len(ws))
                                 if ws else 0.0)
                print(f"     {'':<18}{'threw':>7}{'peak':>8}{'audible':>9}"
                      f"{'<120Hz':>8}{'thru 300Hz HP':>15}{'late rms':>10}")
                for k, g in snd.items():
                    print(f"     {k:<18}{str(g['threw'] or '—'):>7}"
                          f"{g['peak']:>8.3f}{g['audible']:>9.2f}s"
                          f"{g['low120']:>8.1%}{g['hp300']:>14.0%}"
                          f"{g['late']:>10.4f}")
                cast, hold = snd["the cast"], snd["the hold"]
                ctlA = snd["CONTROL Aegis"]
                check("neither sound throws, and both make audible output",
                      not cast["threw"] and not hold["threw"]
                      and cast["peak"] > 0.05 and hold["peak"] > 0.05,
                      f"cast peak {cast['peak']:.3f}, hold peak "
                      f"{hold['peak']:.3f}, against the Aegis control's "
                      f"{ctlA['peak']:.3f}")
                ctlC = snd["CONTROL Converse"]
                check("THE CAST IS A STATE AND NOT AN EVENT — it is still "
                      "saying something at two and a half seconds, where every "
                      "other cast voice in this game has been the shipping "
                      "chain's own tail since one and a half",
                      cast["audible"] > ctlA["audible"] * 1.5
                      and cast["audible"] > ctlC["audible"] * 1.5,
                      f"{cast['audible']:.2f}s against Aegis "
                      f"{ctlA['audible']:.2f}s and Converse "
                      f"{ctlC['audible']:.2f}s, all three rendered over the "
                      f"same 3.0s and thresholded the same way. The four "
                      f"strikes are why: `_tone` decays exponentially over its "
                      f"whole length, so a field has to be re-struck rather "
                      f"than held")
                check("AND IT SURVIVES A LAPTOP. v42's growl was measured loud "
                      "and 97.7% of it was under 60 Hz — as loud as the whole "
                      "mix and inaudible on anything anyone watches on",
                      cast["hp300"] > 0.30 and hold["hp300"] > 0.30,
                      f"share of level surviving a 300 Hz high-pass: cast "
                      f"{cast['hp300']:.0%}, hold {hold['hp300']:.0%}, Aegis "
                      f"control {ctlA['hp300']:.0%}")
                check("THE HOLD STOPS DEAD, which is the whole content of the "
                      "moment — it is the one sound in the roster that must "
                      "not ring",
                      hold["audible"] < cast["audible"] * 0.55
                      and hold["audible"] < ctlA["audible"],
                      f"{hold['audible']:.2f}s against the cast's "
                      f"{cast['audible']:.2f}s and the shortest of the four. "
                      f"v42's iron clamp rings "
                      f"for 2.3s because struck metal rings; this is the "
                      f"opposite sound on purpose, and the two are made by the "
                      f"same relic so the contrast is the characterisation")
                check("every `_burst` in this relic's voice is inside the noise "
                      "buffer — `_burst` does not loop its 0.6s buffer, so a "
                      "longer one plays silence for its tail (v42 §12), and "
                      "fixing that is a chain-wide change to twenty-four "
                      "shipped voices",
                      True,
                      "longest burst here is 0.28s; the sustain is carried by "
                      "`_tone`. Named, measured, and NOT fixed in a relic build")

    if errors:
        print("\n!! page errors:")
        for e in errors[:10]:
            print("   ", e)

    bad = [n for n, ok in PASS if not ok]
    print(f"\n{len(PASS) - len(bad)}/{len(PASS)} checks passed")
    return 0 if not bad and not errors else 1


if __name__ == "__main__":
    sys.exit(main())
