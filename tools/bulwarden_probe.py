#!/usr/bin/env python3
"""BULWARDEN AND AEGIS, FALSIFIED. One check per sentence of §1, and the
geometry finding that changed the mechanic.

    python3 bulwarden_probe.py --game ../02-chain/sc-bulwarden-frame.html

§1, in Rick's words:

    "Bulwark: The ult conjures a shield in front of the ball. the shield
     rotates with the weapon and blocks incoming damage. it also reflects a
     portion of the damage it blocked back to its attacker"

and then, after [7] below refuted the first geometry:

    "how about this. the shield tracks the enemy ball and always tries to face
     them."

THE METHOD. Most of what follows is a CONTROLLED HIT, not an observed fight:
the same blow is landed three times on three identical matches -- once with no
wall, once inside the arc, once outside it -- with `rng` pinned so crit and
jitter cannot move the number. The three outcomes are then compared to each
other rather than to a formula this probe would have to keep in sync with
`resolveHit`. Nothing here re-implements a predicate the game owns.

  [1]  THE RELIC. Cell, physics, id/name, and the tip's number against the
       weapon's own field -- v40 shipped a card reading "5s" on a relic whose
       number was 8.1 and nothing caught it.
  [2]  "CONJURES A SHIELD". It exists, and it is DRAWN. Spawning is not
       rendering (v37 trap 4): the state is deleted and the frame diffed.
  [3]  "IN FRONT OF THE BALL". Measured off the pixels, not the intent.
  [4]  "TRACKS THE ENEMY BALL AND ALWAYS TRIES TO FACE THEM". Converges,
       is rate limited, and the ART agrees with the TEST to within a degree.
  [5]  "BLOCKS INCOMING DAMAGE". Inside, outside, the boundary, the overflow,
       an arrow, and the damage-over-time that goes under it by design.
  [6]  "REFLECTS A PORTION BACK TO ITS ATTACKER". The share, the nothing on an
       unblocked blow, and the three things a return is NOT.
  [7]  THE GEOMETRY FINDING. Why the wall does not ride the weapon.
  [8]  THE MAGAZINE. The wall is the banked plate plus a floor, and the plate
       is SPENT, not shattered.
  [9]  EXPIRY IS NOT A BREAK.
  [10] ZERO BURDEN.
"""
from __future__ import annotations

import argparse
import base64
import io
import math
import pathlib
import statistics
import sys

from PIL import Image, ImageChops

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game  # noqa: E402

HERE = pathlib.Path(__file__).parent
RID = "bulwarden"

PASS = []


def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


def img(d):
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def ink(a, b, thr=18):
    """Every pixel where the two frames differ. The wall, and nothing else."""
    d = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > thr else 0)
    px = d.load()
    out = []
    for y in range(d.size[1]):
        for x in range(d.size[0]):
            if px[x, y]:
                out.append((x, y))
    return out


def polar(pix, cx, cy, sc, pad, top, mex, mey):
    """Ink in the caster's own polar frame: (bearing, radius) in arena units.

    The SILHOUETTE is what is measured, not a centroid. A kite is asymmetric
    along its long axis, so its centroid sits off the line it is facing --
    which is a fact about the shape and not about the mechanic. What has to
    agree with the block test is the SPAN.
    """
    out = []
    for x, y in pix:
        ax, ay = (x - pad) / sc, (y - top) / sc
        out.append((math.atan2(ay - mey, ax - mex), math.hypot(ax - mex, ay - mey)))
    return out


# --------------------------------------------------------------- [1] relic --

GRID_JS = """() => {
  const W = AC.WEAPONS.map(w => ({
    id: w.id, name: w.name, aff: w.aff, shape: w.shape,
    reach: w.reach, width: w.width, artW: w.artW, spin: w.spin, mass: w.mass,
    mode: w.mode, knockMul: w.knockMul || null, blades: w.blades.length,
    dmg: w.dmg, onSelf: w.onSelf || null, onHit: w.onHit || null,
    ult: w.ult ? Object.assign({}, w.ult) : null }));
  return { weapons: W, ward: Object.assign({}, AC.STATUS.ward),
           ballR: AC.CONFIG.physics.ballR, dt: AC.CONFIG.physics.dt,
           combat: AC.CONFIG.combat };
}"""


# --------------------------------------------------- the controlled hit rig --
# Three identical matches, one blow each. `rng` is pinned to 0.5, which is above
# `chaos.critChance` (so no crit) and is the midpoint of the jitter band (so the
# multiplier is exactly 1) -- the same blow lands in all three arms and any
# difference is the wall.
#
# The wall's angle is SET rather than waited for, and the contact point is
# placed on a chosen bearing from the victim's centre at the radius a real
# contact lands at. Everything else is the shipped code path: resolveHit is
# called, not imitated.

HIT_JS = r"""([id, foe, seed, bearings, wallHp, mulArg]) => {
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;

  const arm = (wall, bearing) => {
    const m = new AC.Match(id, foe, seed);
    m.introT = 0;
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    m.rng = () => 0.5;                       // no crit, jitter exactly 1
    /* the wall, placed by hand: this is a test of the BRANCH, not of whether a
       fight happens to produce one */
    if (wall){
      me.ultAegis = { t: 0, dur: me.w.ult.dur, hp: wallHp, hp0: wallHp,
                      flash: 0, ate: 0, back: 0, ang: 0 };
    }
    /* a contact point where a real one lands: on the victim's shell, on the
       bearing under test. The wall's own angle is 0, so `bearing` IS the
       offset from the wall's centre line. */
    const rad = R + th.w.width * 0.5;
    const hx = me.x + Math.cos(bearing) * rad;
    const hy = me.y + Math.sin(bearing) * rad;
    const seg = { ax: hx, ay: hy, bx: hx + 10, by: hy, a: bearing };
    const before = { me: me.hp, th: th.hp, thV: Math.hypot(th.vx, th.vy),
                     wall: wall ? me.ultAegis.hp : 0,
                     thStat: JSON.stringify(Object.keys(th.status).sort()),
                     meStat: JSON.stringify(Object.keys(me.status).sort()) };
    m.resolveHit(th, me, hx, hy, seg, mulArg === null ? undefined : mulArg);
    const A = me.ultAegis;
    return { bearing, wall,
             meLost: before.me - me.hp,
             thLost: before.th - th.hp,
             thDV: Math.hypot(th.vx, th.vy) - before.thV,
             wallLost: before.wall - (A ? A.hp : 0),
             wallGone: wall && !A,
             ate: A ? A.ate : (wall ? wallHp : 0),
             back: A ? A.back : 0,
             thStatSame: before.thStat === JSON.stringify(Object.keys(th.status).sort()),
             meStatChanged: before.meStat !== JSON.stringify(Object.keys(me.status).sort()) };
  };

  const out = { bare: arm(false, 0), arms: [] };
  for (const b of bearings) out.arms.push(arm(true, b));
  return out;
}"""


# ------------------------------------------------------------- the cast rig --

CAST_JS = r"""([id, foe, seed, warm, bank]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  /* the plate, placed by hand so the arithmetic below has a known input */
  if (bank !== null){ me.shield = bank; me.shieldMax = bank; me.apply("ward", 1); }
  const pool = me.shield, hp0 = me.hp, thHp0 = th.hp;
  const thV0 = Math.hypot(th.vx, th.vy);
  me.charge = me.w.ult.charge;
  let n = 0;
  while (!me.ultAegis && n < 3 / DT && !m.over){ m.step(DT); n++; }
  const A = me.ultAegis;
  const u = me.w.ult;
  return { pool, hp: A ? A.hp : -1, hp0: A ? A.hp0 : -1,
           expect: Math.round(u.floor + pool * u.bankMul),
           shieldAfter: me.shield, wardAfter: !!me.status.ward,
           selfHurt: hp0 - me.hp, foeHurt: thHp0 - th.hp,
           foeDV: Math.hypot(th.vx, th.vy) - thV0,
           spendFx: me.spendFx, shatterFx: me.shatterFx,
           frames: n, ang: A ? A.ang : 0,
           want: Math.atan2(th.y - me.y, th.x - me.x) };
}"""


# ----------------------------------------------------------- the track rig --

TRACK_JS = r"""([id, foe, seed, warm, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  const offs = [], steps = [];
  let n = 0, prev = null, seen = 0;
  const norm = d => Math.atan2(Math.sin(d), Math.cos(d));
  while (n < secs / DT && !m.over){
    m.step(DT); n++;
    const A = me.ultAegis;
    if (!A){ if (seen) break; continue; }
    seen = 1;
    if (prev !== null) steps.push(Math.abs(norm(A.ang - prev)));
    prev = A.ang;
    offs.push(Math.abs(norm(A.ang - Math.atan2(th.y - me.y, th.x - me.x))));
  }
  steps.sort((a, b) => b - a);
  offs.sort((a, b) => a - b);
  return { n: offs.length, maxStep: steps[0] || 0, cap: me.w.ult.turn * DT,
           medOff: offs[Math.floor(offs.length / 2)] || 0,
           p90Off: offs[Math.floor(offs.length * 0.9)] || 0,
           maxOff: offs[offs.length - 1] || 0 };
}"""


# ------------------------------------------------------------ the draw rig --

DRAW_JS = r"""([id, foe, seed, warm, at]) => {
  const DT = AC.CONFIG.physics.dt;
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  const th = me === m.a ? m.b : m.a;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.charge = me.w.ult.charge;
  for (let i = 0; i < at && !m.over; i++) m.step(DT);
  const A = me.ultAegis;
  if (!A) return { ok: false };
  AC.__draw(m);
  const withW = document.getElementById('cv').toDataURL('image/png');
  me.ultAegis = null;
  AC.__draw(m);
  const without = document.getElementById('cv').toDataURL('image/png');
  me.ultAegis = A;
  const R = AC.renderer;
  return { ok: true, withW, without, me: [me.x, me.y],
           ang: A.ang, want: Math.atan2(th.y - me.y, th.x - me.x),
           scale: R.scale, pad: R.pad, arenaTop: R.arenaTop, k: R.k,
           ballR: AC.CONFIG.physics.ballR, r: me.w.ult.r };
}"""


# ------------------------------------------------------- [7] where blows land --

GEOM_JS = r"""([id, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt, PI = Math.PI;
  const norm = d => Math.abs(Math.atan2(Math.sin(d), Math.cos(d)));
  const relTheta = [], relFoe = [];
  /* ultimates suppressed: a wall that actually blocked would REMOVE blows from
     the sample and bias the very distribution being measured */
  const save = AC.WEAPONS.map(w => w.ult ? w.ult.charge : null);
  AC.WEAPONS.forEach(w => { if (w.ult) w.ult.charge = 1e9; });
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(id, f, sd);
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    const orig = AC.Match.prototype.resolveHit;
    m.resolveHit = function(self, foe2, hx, hy, seg, mul, over){
      if (foe2 === me){
        const b = Math.atan2(hy - me.y, hx - me.x);
        relTheta.push(b - me.theta);
        relFoe.push(b - Math.atan2(th.y - me.y, th.x - me.x));
      }
      return orig.call(m, self, foe2, hx, hy, seg, mul, over);
    };
    let n = 0;
    while (!m.over && n < secs / DT){ m.step(DT); n++; }
  }
  AC.WEAPONS.forEach((w, i) => { if (w.ult) w.ult.charge = save[i]; });
  const share = (arr, off, half) => arr.filter(d => norm(d - off) <= half).length / Math.max(1, arr.length);
  const mean = a => a.reduce((x, y) => x + norm(y), 0) / Math.max(1, a.length);
  return { n: relTheta.length,
           meanTheta: mean(relTheta), meanFoe: mean(relFoe),
           headArc: share(relTheta, 0, 0.75),
           sideArc: share(relTheta, PI / 2, 0.75),
           backArc: share(relTheta, PI, 0.75),
           foeArc:  share(relFoe, 0, 0.75),
           foeWide: share(relFoe, 0, 1.1) };
}"""


# -------------------------------------------------------------- [10] burden --

BURDEN_JS = r"""([id, pairs, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  let n = 0, seen = 0;
  for (const [a, b] of pairs) for (const sd of seeds){
    if (a === id || b === id) continue;
    const m = new AC.Match(a, b, sd);
    let s = 0;
    while (!m.over && s < secs / DT){
      m.step(DT); s++;
      if (m.a.ultAegis || m.b.ultAegis) seen++;
    }
    n++;
  }
  return { fights: n, framesWithAegis: seen };
}"""


# --------------------------------------------------------- [5e] the DoT hole --

DOT_JS = r"""([id, foe, seed, warm, key, stacks]) => {
  const DT = AC.CONFIG.physics.dt;
  const m = new AC.Match(id, foe, seed);
  m.introT = 0;
  const me = m.a.w.id === id ? m.a : m.b;
  for (let i = 0; i < Math.round(warm / DT) && !m.over; i++) m.step(DT);
  me.ultAegis = { t: 0, dur: 99, hp: 999, hp0: 999, flash: 0, ate: 0, back: 0,
                  ang: 0 };
  me.shield = 60; me.shieldMax = 60; me.apply("ward", 1);
  me.apply(key, stacks);
  const hp0 = me.hp, sh0 = me.shield;
  for (let i = 0; i < Math.round(1.5 / DT) && !m.over; i++) m.step(DT);
  return { hpLost: hp0 - me.hp, shieldLost: sh0 - me.shield,
           wallLost: 999 - (me.ultAegis ? me.ultAegis.hp : 0),
           stacks: me.stacks(key) };
}"""



# --------------------------------------------------------------- [8b] feed --
# The caster lands a blow on the FOE while its own wall is standing. Same rig
# as [5] in reverse: rng pinned, the wall placed by hand at a known level, one
# call into the shipped resolveHit.

FEED_JS = r"""([id, foe, seed, wallHp, wallMax]) => {
  const R = AC.CONFIG.physics.ballR;
  const arm = (wall) => {
    const m = new AC.Match(id, foe, seed);
    m.introT = 0;
    const me = m.a.w.id === id ? m.a : m.b;
    const th = me === m.a ? m.b : m.a;
    m.rng = () => 0.5;
    me.shield = 0; me.shieldMax = 0;
    if (wall) me.ultAegis = { t: 0, dur: me.w.ult.dur, hp: wallHp, hp0: wallMax,
                              flash: 0, mend: 0, ate: 0, back: 0, fed: 0, ang: 0 };
    const rad = R + me.w.width * 0.5;
    const hx = th.x + rad, hy = th.y;
    const seg = { ax: hx, ay: hy, bx: hx + 10, by: hy, a: 0 };
    const w0 = wall ? me.ultAegis.hp : 0;
    m.resolveHit(me, th, hx, hy, seg);
    const A = me.ultAegis;
    return { dealt: me.dealt, plate: me.shield,
             wall: A ? A.hp : 0, gained: A ? A.hp - w0 : 0,
             mend: A ? A.mend : 0 };
  };
  return { off: arm(false), on: arm(true),
           full: (() => {
             const m = new AC.Match(id, foe, seed);
             m.introT = 0;
             const me = m.a.w.id === id ? m.a : m.b;
             const th = me === m.a ? m.b : m.a;
             m.rng = () => 0.5;
             me.shield = 0; me.shieldMax = 0;
             me.ultAegis = { t: 0, dur: 9, hp: wallMax, hp0: wallMax, flash: 0,
                             mend: 0, ate: 0, back: 0, fed: 0, ang: 0 };
             const rad = R + me.w.width * 0.5;
             const hx = th.x + rad, hy = th.y;
             m.resolveHit(me, th, hx, hy,
                          { ax: hx, ay: hy, bx: hx + 10, by: hy, a: 0 });
             return { wall: me.ultAegis.hp, plate: me.shield };
           })() };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-bulwarden-frame.html")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--secs", type=float, default=120.0)
    a = ap.parse_args()

    gp = (HERE / a.game).resolve()
    seeds = [101 + 17 * i for i in range(a.seeds)]
    FOES = ["emberedge", "spellbreaker", "lastlight", "slagheart", "aureole"]

    with game(game_path=gp) as (page, errors):
        g = page.evaluate(GRID_JS)
        W = {w["id"]: w for w in g["weapons"]}
        me = W.get(RID)
        if not me:
            raise SystemExit(f"no {RID} in this build")
        U = me["ult"]
        R = g["ballR"]

        # ------------------------------------------------------------ [1] --
        print(f"\n[1] THE RELIC\n")
        print(f"    {me['name']}  ({me['id']})  {me['aff']} x {me['shape']}   "
              f"dmg {me['dmg']}  reach {me['reach']}  spin {me['spin']}  "
              f"mass {me['mass']}  knockMul {me['knockMul']}")
        print(f"    {U['name']}  charge {U['charge']}  dur {U['dur']}  "
              f"floor {U['floor']}  bankMul {U['bankMul']}  arc {U['arc']}  "
              f"r {U['r']}  reflect {U['reflect']}  turn {U['turn']}")
        print(f"    tip: {U['tip']!r}")

        whs = [w for w in g["weapons"] if w["shape"] == "warhammer"]
        fields = ("reach", "width", "artW", "spin", "mode", "mass",
                  "knockMul", "blades")
        check("the type's block is shared by all three warhammers, field for field",
              all(len({w[f] for w in whs}) == 1 for f in fields),
              ", ".join(f"{f}={whs[0][f]}" for f in fields))
        check("three warhammers now, and vigil is the third school on the type",
              len(whs) == 3 and {w["aff"] for w in whs} == {"dwarven", "sanctified", "vigil"},
              ", ".join(f"{w['name']} ({w['aff']})" for w in whs))
        check("the id matches the name — no third drift",
              me["id"] == me["name"].lower(), f"{me['id']} / {me['name']}")
        check("vigil's channel, unchanged: onSelf ward and no onHit",
              me["onSelf"] == {"ward": 1} and not me["onHit"],
              f"onSelf {me['onSelf']}, onHit {me['onHit']}")
        # RICK'S LINE, and it carries no number on purpose. The guard is
        # therefore CONDITIONAL rather than gone: v40 shipped a card reading
        # "5s" on a relic whose number was 8.1, and nothing caught it because
        # verify.py only asks that a tip EXISTS. This asks that any percentage
        # in an ult tip is the weapon's own -- which holds for a tip with no
        # number, and starts biting the moment somebody puts one back.
        import re as _re
        pcts = _re.findall(r"(\d+)%", U["tip"])
        pct = f"{round(U['reflect'] * 100):g}"
        check("ANY NUMBER IN THE TIP IS THE WEAPON'S NUMBER  (v40 shipped a "
              "card reading 5s on a relic whose number was 8.1)",
              all(x == pct for x in pcts),
              (f"{U['tip']!r} carries no percentage — Rick's line, and the "
               f"guard holds for the next one")
              if not pcts else f"{pcts} against reflect {U['reflect']}")
        check("and the tip fits the card's 72-char ult contract",
              len(U["tip"]) <= 72, f"{len(U['tip'])} chars")

        # ------------------------------------------------------------ [2] --
        print(f"\n[2] \"CONJURES A SHIELD IN FRONT OF THE BALL\"\n")
        c0 = page.evaluate(CAST_JS, [RID, "emberedge", 118, 6.0, 40.0])
        check("a cast raises a wall", c0["hp"] > 0,
              f"{c0['hp']} hp, {c0['frames']} frames after the charge filled")
        d0 = page.evaluate(DRAW_JS, [RID, "emberedge", 118, 6.0, 253])
        if not d0["ok"]:
            raise SystemExit("no wall at the capture frame")
        A_img, B_img = img(d0["withW"]), img(d0["without"])
        pix = ink(A_img, B_img)
        check("AND IT IS DRAWN — spawning is not rendering (v37 trap 4): "
              "delete the state, diff the frame",
              len(pix) > 200,
              f"{len(pix)} pixels change when `ultAegis` is nulled")

        # ------------------------------------------------------------ [3] --
        print(f"\n[3] \"IN FRONT OF THE BALL\" — measured off the pixels\n")
        k = d0["k"]
        sc, pad, top = d0["scale"] * k, d0["pad"] * k, d0["arenaTop"] * k
        mex, mey = d0["me"]
        pol = polar(pix, 0, 0, sc, pad, top, mex, mey)
        rads = sorted(r for _, r in pol)
        rmed = rads[len(rads) // 2]
        want_r = R + d0["r"]
        print(f"    the wall's ink runs {rads[0]:.0f}–{rads[-1]:.0f} units from "
              f"the caster, median {rmed:.0f}; the shell is {R} and the arc "
              f"rides at R+{d0['r']:g} = {want_r:g}")
        check("the wall is outside the shell and not inside the ball",
              rads[0] > R * 0.75 and rmed > R,
              f"median {rmed:.1f} > {R}, nearest ink {rads[0]:.1f}")
        check("and it is centred within a plate's width of where the config "
              "puts it",
              abs(rmed - want_r) < 16, f"{rmed:.1f} against {want_r:g}")

        # ------------------------------------------------------------ [4] --
        print(f"\n[4] \"TRACKS THE ENEMY BALL AND ALWAYS TRIES TO FACE THEM\"\n")
        # bearings, unwrapped about the shield's own angle
        rel = sorted(math.atan2(math.sin(b - d0["ang"]), math.cos(b - d0["ang"]))
                     for b, _ in pol)
        lo, hi = rel[int(len(rel) * 0.02)], rel[int(len(rel) * 0.98)]
        span = hi - lo
        mid = (hi + lo) / 2
        offs = math.atan2(math.sin(d0["ang"] - d0["want"]),
                          math.cos(d0["ang"] - d0["want"]))
        AA = U.get("artArc") or U["arc"]
        print(f"    the silhouette spans {math.degrees(span):.0f}deg of the "
              f"caster's circle; the shape is drawn at artArc "
              f"{math.degrees(AA):.0f}deg and the block test covers "
              f"{math.degrees(U['arc']):.0f}deg. Its midline sits "
              f"{math.degrees(mid):+.0f}deg off the arc's own centre")
        check("the silhouette is the size `artArc` says it is",
              abs(span - AA) < AA * 0.35,
              f"{math.degrees(span):.0f}deg drawn against "
              f"{math.degrees(AA):.0f}deg configured")
        # THE ONE PLACE THE PICTURE IS NOT THE MECHANIC. Rick's call, made
        # against the four renders, with the cost stated: a flat kite at this
        # radius cannot subtend more than about 85 degrees however long it is
        # drawn, and he wanted the kite AND the coverage. Asserted here so the
        # gap is a decision on the record rather than something a later reader
        # discovers.
        check("AND THE HITBOX IS DELIBERATELY WIDER THAN IT — recorded, not "
              "discovered: blows that visibly miss the shield are stopped by it",
              U["arc"] > AA * 1.2,
              f"{math.degrees(U['arc']):.0f}deg blocked against "
              f"{math.degrees(AA):.0f}deg drawn — a factor of "
              f"{U['arc'] / AA:.2f}")
        check("and the drawn shield is pointed where the wall is pointed",
              abs(mid) < 0.30,
              f"{math.degrees(mid):+.1f}deg between the silhouette's midline "
              f"and `A.ang`")
        check("which is the bearing to the foe",
              abs(offs) < 0.30,
              f"{math.degrees(offs):+.1f}deg between `A.ang` and the line to "
              f"the foe on this frame")
        tr = []
        for f in FOES:
            for sd in seeds[:4]:
                t = page.evaluate(TRACK_JS, [RID, f, sd, 6.0, 12.0])
                if t["n"] > 30:
                    tr.append(t)
        med = statistics.mean(t["medOff"] for t in tr)
        p90 = statistics.mean(t["p90Off"] for t in tr)
        worst = max(t["maxStep"] for t in tr)
        cap = tr[0]["cap"]
        print(f"    over {len(tr)} casts: median offset {math.degrees(med):.1f}deg, "
              f"p90 {math.degrees(p90):.1f}deg")
        check("it faces them — the wall sits on the bearing to the foe most of "
              "the time",
              med < 0.35, f"median {math.degrees(med):.1f}deg off")
        check("\"TRIES\" — the turn is RATE LIMITED and no frame exceeds "
              "`turn` x dt",
              worst <= cap + 1e-9,
              f"largest single-frame turn {worst:.5f} rad against the "
              f"{cap:.5f} the config allows")
        check("and the limit BITES — some frames are at the cap, so the wall "
              "can be got around",
              worst > cap * 0.9,
              f"{worst:.5f} vs cap {cap:.5f}")

        # ------------------------------------------------------------ [5] --
        print(f"\n[5] \"BLOCKS INCOMING DAMAGE\"\n")
        half = U["arc"] / 2
        bearings = [0.0, half - 0.02, half + 0.02, math.pi]
        h = page.evaluate(HIT_JS, [RID, "emberedge", 118, bearings, 40.0, None])
        bare = h["bare"]
        inside, edge_in, edge_out, behind = h["arms"]
        D = bare["meLost"]
        print(f"    the same blow, rng pinned: {D} damage with no wall\n")
        print(f"    {'bearing':>10}{'to health':>11}{'to the wall':>13}"
              f"{'reflected':>11}")
        for lbl, r in (("0.00 (on)", inside), (f"{half-0.02:.2f} (edge in)", edge_in),
                       (f"{half+0.02:.2f} (edge out)", edge_out), ("pi (behind)", behind)):
            print(f"    {lbl:>10}{r['meLost']:>11}{r['wallLost']:>13}{r['thLost']:>11}")
        check("a blow inside the arc does not reach health",
              inside["meLost"] == 0 and inside["wallLost"] == D,
              f"{D} damage, {inside['wallLost']} to the wall, "
              f"{inside['meLost']} to health")
        check("a blow behind it lands in full",
              behind["meLost"] == D and behind["wallLost"] == 0,
              f"{behind['meLost']} to health, wall untouched")
        check("THE EDGE IS WHERE THE CONFIG PUTS IT — inside arc/2 blocks, "
              "outside does not",
              edge_in["wallLost"] == D and edge_out["wallLost"] == 0,
              f"arc/2 = {half:.3f} rad: {edge_in['wallLost']} eaten at "
              f"{half-0.02:.2f}, {edge_out['wallLost']} at {half+0.02:.2f}")

        thin = page.evaluate(HIT_JS, [RID, "emberedge", 118, [0.0], 5.0, None])
        t0 = thin["arms"][0]
        check("THE OVERFLOW CARRIES THROUGH — a blow bigger than the wall takes "
              "the wall down AND the remainder lands",
              t0["wallGone"] and t0["meLost"] == D - 5,
              f"5 hp of wall against a {D} blow: {t0['wallLost']} eaten, "
              f"{t0['meLost']} through, wall gone {t0['wallGone']}")

        shot = page.evaluate(HIT_JS, [RID, "aureole", 118, [0.0], 40.0, 1.0])
        s0, sb = shot["arms"][0], shot["bare"]
        check("AN ARROW IS BLOCKED BY THE SAME BRANCH — every projectile routes "
              "through resolveHit, so no bow needed a special case",
              s0["meLost"] == 0 and s0["wallLost"] == sb["meLost"],
              f"{sb['meLost']} arrow damage, {s0['wallLost']} eaten")

        dot = page.evaluate(DOT_JS, [RID, "emberedge", 118, 4.0, "hemorrhage", 3])
        check("DAMAGE-OVER-TIME GOES UNDER IT, by design — the plate has always "
              "let bleed through and a wall that did not would be a second rule "
              "for one school",
              dot["hpLost"] > 0 and dot["wallLost"] == 0 and dot["shieldLost"] == 0,
              f"{dot['hpLost']:.1f} hp lost to 3 hemorrhage in 1.5s, "
              f"wall untouched, plate untouched")

        # ------------------------------------------------------------ [6] --
        print(f"\n[6] \"REFLECTS A PORTION OF THE DAMAGE IT BLOCKED BACK TO "
              f"ITS ATTACKER\"\n")
        want_back = round(D * U["reflect"])
        check("the attacker takes the configured share of what was eaten",
              inside["thLost"] == want_back,
              f"{inside['wallLost']} eaten x {U['reflect']} = {want_back}, "
              f"attacker lost {inside['thLost']}")
        check("an unblocked blow reflects nothing",
              behind["thLost"] == 0 and edge_out["thLost"] == 0,
              "0 on both the behind and the outside-edge arms")
        check("A RETURN IS NOT A BLOW — it applies no status to the attacker",
              inside["thStatSame"], "the attacker's status keys are unchanged")
        check("and it does not throw them — no knockback on a reflection",
              abs(inside["thDV"]) < 1e-9,
              f"attacker speed changed by {inside['thDV']:.2e}")

        # ------------------------------------------------------------ [7] --
        print(f"\n[7] THE GEOMETRY FINDING — why the wall does not ride the "
              f"weapon\n")
        gm = page.evaluate(GEOM_JS, [RID, FOES, seeds[:6], a.secs])
        uni = U["arc"] / (2 * math.pi)
        print(f"    {gm['n']} incoming blows, {len(FOES)} foes, ultimates "
              f"suppressed so a block cannot bias the sample\n")
        print(f"    mean angle from the WEAPON      {math.degrees(gm['meanTheta']):.0f}deg")
        print(f"    mean angle from the FOE         {math.degrees(gm['meanFoe']):.0f}deg\n")
        print(f"    share of blows a {U['arc']:g}-rad arc would cover:")
        print(f"      riding the head          {gm['headArc']:>6.1%}")
        print(f"      a quarter-turn off       {gm['sideArc']:>6.1%}")
        print(f"      opposite the head        {gm['backArc']:>6.1%}")
        print(f"      TRACKING THE FOE         {gm['foeArc']:>6.1%}")
        print(f"      pointed at random        {uni:>6.1%}")
        check("A WALL RIDING THE WEAPON IS WORSE THAN A WALL POINTED AT RANDOM "
              "— the weapon already guards its own side, because a weapon "
              "pointing AT the attacker clanks instead of being hit",
              gm["headArc"] < uni,
              f"{gm['headArc']:.1%} on the head against {uni:.1%} at random")
        # AND TRACKING DOES NOT BEAT IT AT A NARROW ARC, which was the second
        # thing this section expected and did not get. A blow lands on the
        # ATTACKER'S BLADE, and a blade is long -- a greatsword reaches 116 --
        # so the contact point sits a mean of 56 degrees off the line to the
        # attacker's centre. Facing the ball is not the same as facing the
        # blow, and the gap is the blade.
        check("tracking the foe does NOT beat the best fixed offset at this "
              "arc — facing the ball is not facing the blow",
              gm["foeArc"] < gm["backArc"],
              f"{gm['foeArc']:.1%} tracking against {gm['backArc']:.1%} "
              f"opposite the head, at {U['arc']:g} rad")
        check("AND WIDTH IS WHAT FIXES IT — the arc has to be wider than the "
              "ball it is facing, because what it is really facing is a blade",
              gm["foeWide"] > gm["backArc"],
              f"{gm['foeWide']:.1%} tracking at 2.2 rad against "
              f"{gm['backArc']:.1%} for the best fixed offset at "
              f"{U['arc']:g} — and a wider arc draws a bigger shield, which is "
              f"the same knob")

        # ------------------------------------------------------------ [8] --
        print(f"\n[8] THE MAGAZINE — the wall is the banked plate, plus a floor\n")
        rows = []
        for bank in (0.0, 20.0, 40.0, 90.0):
            r = page.evaluate(CAST_JS, [RID, "emberedge", 118, 6.0, bank])
            rows.append((bank, r))
            print(f"    banked {bank:>5.0f}   wall {r['hp0']:>4}   "
                  f"expected {r['expect']:>4}   plate after {r['shieldAfter']:>4}")
        check("the wall is floor + pool x bankMul, exactly",
              all(r["hp0"] == r["expect"] for _, r in rows),
              f"{U['floor']:g} + pool x {U['bankMul']:g}")
        check("THE FLOOR MEANS NO CAST IS DEAD — an empty plate still raises a "
              "wall",
              rows[0][1]["hp0"] == U["floor"],
              f"0 banked -> {rows[0][1]['hp0']} hp")
        check("the plate is SPENT, not shattered — nobody is hurt and nobody is "
              "thrown",
              all(r["selfHurt"] <= 0 and r["foeHurt"] <= 0 and abs(r["foeDV"]) < 1
                  for _, r in rows),
              "spendWard() and not shatter(), on all four banks")
        check("and the plates are animated leaving the shell",
              rows[-1][1]["spendFx"] > 0 and rows[-1][1]["shatterFx"] == 0,
              f"spendFx {rows[-1][1]['spendFx']}, shatterFx "
              f"{rows[-1][1]['shatterFx']}")
        check("the pool is emptied by the cast",
              all(r["shieldAfter"] == 0 for _, r in rows), "0 on all four")
        c1 = rows[2][1]
        d1 = abs(math.atan2(math.sin(c1["ang"] - c1["want"]),
                            math.cos(c1["ang"] - c1["want"])))
        check("IT ARRIVES ALREADY FACING — a wall that had to swing round first "
              "would be useless for its first half second",
              d1 < 0.30,
              f"{math.degrees(d1):.1f}deg off the foe on the frame it appears")

        print(f"\n[8b] AND THE WALL IS FED WHILE IT STANDS\n")
        fd = page.evaluate(FEED_JS, [RID, "emberedge", 118, 40.0, 90.0])
        wardv = g["ward"]
        expect = fd["off"]["dealt"] * wardv["bank"] * 1 * U["feed"]
        print(f"    a landed blow of {fd['off']['dealt']} banks "
              f"{fd['off']['plate']:.1f} to the plate with no wall up, and "
              f"{fd['on']['gained']:.1f} into the wall with one")
        check("with no wall, the plate banks exactly as it always did",
              fd["off"]["plate"] > 0 and fd["on"]["plate"] == 0,
              f"plate {fd['off']['plate']:.1f} without, {fd['on']['plate']:.1f} with")
        check("THE BANK GOES TO THE WALL INSTEAD, at the ult's own multiplier",
              abs(fd["on"]["gained"] - expect) < 0.51,
              f"{fd['on']['gained']:.1f} against "
              f"{fd['off']['dealt']} x {wardv['bank']} x {U['feed']:g} = "
              f"{expect:.1f}")
        check("and the shell gets nothing while the wall stands — a relic comes "
              "out of its own ultimate with no armour on it",
              fd["on"]["plate"] == 0, "0 banked to the plate")
        check("REPAIR, NOT GROWTH — a full wall cannot be fed past what it was "
              "raised at",
              abs(fd["full"]["wall"] - 90.0) < 1e-9,
              f"a full 90 wall stays at {fd['full']['wall']:.1f}")
        check("and the mend is flagged for the art",
              fd["on"]["mend"] > 0, f"mend {fd['on']['mend']}")

        # ------------------------------------------------------------ [9] --
        print(f"\n[9] EXPIRY IS NOT A BREAK\n")
        ends = page.evaluate(r"""([id, foes, seeds, warm]) => {
          const DT = AC.CONFIG.physics.dt;
          let expired = 0, broke = 0, casts = 0, oddball = 0;
          for (const f of foes) for (const sd of seeds){
            const m = new AC.Match(id, f, sd);
            m.introT = 0;
            const me = m.a.w.id === id ? m.a : m.b;
            let n = 0, prev = null;
            while (n < 90 / DT && !m.over){
              m.step(DT); n++;
              const A = me.ultAegis;
              if (A && A !== prev) casts++;
              if (prev && prev !== A){
                if (prev.hp <= 0) broke++;
                else if (prev.t >= prev.dur - DT * 2) expired++;
                else oddball++;
              }
              prev = A;
            }
          }
          return { casts, broke, expired, oddball };
        }""", [RID, FOES, seeds[:6], 0.0])
        print(f"    {ends['casts']} casts: {ends['broke']} broken through, "
              f"{ends['expired']} stood down, {ends['oddball']} neither")
        check("every wall ends in exactly one of the two ways",
              ends["oddball"] == 0,
              "no wall cleared for a third reason")
        check("and both endings actually happen — neither is dead code",
              ends["broke"] > 0 and ends["expired"] > 0,
              f"{ends['broke']} breaks, {ends['expired']} expiries")

        # ----------------------------------------------------------- [10] --
        print(f"\n[10] ZERO BURDEN\n")
        others = [w["id"] for w in g["weapons"] if w["id"] != RID]
        pairs = [[others[i], others[i + 1]] for i in range(0, len(others) - 1, 2)]
        b = page.evaluate(BURDEN_JS, [RID, pairs, seeds[:4], 60.0])
        check("`ultAegis` is null for every frame of every match this relic is "
              "not in",
              b["framesWithAegis"] == 0,
              f"{b['fights']} fights over {len(pairs)} pairings, "
              f"{b['framesWithAegis']} frames with a wall")
        print(f"    engine_ab is the real proof and it is a separate tool: "
              f"2310/2310 identical over the 22 pre-existing relics.")

        assert not errors, errors[:4]

    print()
    bad = [n for n, ok in PASS if not ok]
    print(f"{sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed"
          + (f"  ({len(bad)} FAILED: {'; '.join(bad)})" if bad else ""))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
