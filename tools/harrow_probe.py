#!/usr/bin/env python3
"""LASTLIGHT AND THE HARROWING, FALSIFIED. The harness for lastlight_build.py.

    python3 harrow_probe.py --game ../02-chain/sc-lastlight.html

Every check here is written to FAIL if the thing it names is not true, and
several of them did during the build. What it asserts, and why each one earns
its place:

  [1]  structure — the relic exists, wears `_scRadiant`, carries Smite, has no
       `shot` block (a melee relic that `relicShot` thinks is ranged makes the
       fight card and verify.py disagree about what it is)
  [2]  the spray — twelve blades, every one born CLEAR of the shell and armed.
       The trap this guards is written down in the engine: a projectile
       spawned inside `R + s.r` resolves on the frame it is born, which would
       silently turn the spray into a nova
  [3]  the turn is DERIVED, not accumulated — asserted against the source
       text, because an accumulated angle would strobe against the frame
       interpolator and no screenshot would show it reliably
  [4]  the double payoff — a blade that reaches the foe takes hp AND sticks
  [5]  the burden is physics: moveMul falls, the fall term rises, and CLANK IS
       UNTOUCHED. Also the identity at zero burden, which is the entire reason
       engine_ab can prove the other seventeen relics inert
  [6]  one bloom — nothing of the cast is still in the air when it goes
  [7]  it scales — damage, knock, stun and hit stop strictly increasing in n
  [8]  the sparks are Daybreak's: right count, and born in grace
  [9]  THE DUD RATE, measured over a real population rather than assumed
  [10] the fuse drops if either fighter dies, and the blades come out
  [11] a miss bounces at most twice and then expires
  [12] the set-piece draws for every relic in the roster without throwing

`--sheet` additionally writes art samples: the spray in flight, blades in a
shell at three points on the fuse, and the bloom.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent
ID = "lastlight"

# --------------------------------------------------------------------------
# Checks that need the SOURCE TEXT rather than a running page. Both of these
# are claims about how the code is written, not about what it computes, and a
# runtime probe cannot see either one.
# --------------------------------------------------------------------------


def source_checks(path: pathlib.Path):
    t = path.read_text(encoding="utf-8")
    out = []

    # [3] The blade's rotation must be DERIVED from state, not accumulated on
    # the object. `LERP_FIELDS.shot` is ["x","y"] and shotAng is ["a"], so a
    # field like `s.rot += ...` would not be interpolated and the blade would
    # strobe between sim steps. The splinter's tumble solved this the same way
    # and the comment there says so.
    derived = 's.a + (s.max - s.life) * (s.spin || 15)' in t
    no_accum = 's.rot +=' not in t and 's.spinPhase +=' not in t
    lerp_ok = 'shot: ["x", "y"],' in t and 'shotAng: ["a"],' in t
    out.append(("[3] blade turn is derived from (a, life), not accumulated",
                derived and no_accum and lerp_ok,
                f"derived={derived} no-accumulator={no_accum} lerp-fields={lerp_ok}"))

    # [5c] Clank share must still read `w.mass`. If the burden ever reaches
    # tickClank, a ball starts winning binds because it was HIT, which is a
    # reward pointed at the wrong fighter.
    clank_clean = "const mA = A.w.mass, mB = B.w.mass;" in t
    burden_in_clank = "burdenMass" in t.split("tickClank(dt){")[1][:2500] \
        if "tickClank(dt){" in t else True
    out.append(("[5c] clank share still reads w.mass, burden nowhere near it",
                clank_clean and not burden_in_clank,
                f"w.mass-read={clank_clean} burden-in-tickClank={burden_in_clank}"))
    return out


# --------------------------------------------------------------------------
# In-page checks.
# --------------------------------------------------------------------------

STRUCT_JS = """(id) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  if (!w) return { err: "not in WEAPONS" };
  const st = AC.relicStatus(w);
  // Which draw branch fires — wrap the candidates and see.
  const names = ["_scRadiant", "_scBase", "_scGrown", "_scBuilt", "_scPlated",
                 "_scBarbed", "_scEaten", "_scConjured"];
  const fired = [], orig = {};
  for (const n of names){
    orig[n] = AC.SHAPES[n];
    AC.SHAPES[n] = function(...a){ fired.push(n); return orig[n].apply(this, a); };
  }
  const cv = document.createElement("canvas"); cv.width = cv.height = 400;
  const c = cv.getContext("2d"); c.translate(60, 200);
  AC.SHAPES.scythe(c, w.reach, w.width, AC.AFFINITIES[w.aff], undefined, w.aff);
  for (const n of names) AC.SHAPES[n] = orig[n];
  return { name: w.name, aff: w.aff, shape: w.shape, mass: w.mass,
           reach: w.reach, spin: w.spin, mode: w.mode, dmg: w.dmg,
           statusKey: st && st.key, statusTip: st && st.def && st.def.tip,
           shot: AC.relicShot(w), ultKind: w.ult.kind, ultName: w.ult.name,
           ultTip: w.ult.tip, ultTipLen: w.ult.tip.length,
           branch: fired[0], roster: AC.WEAPONS.length };
}"""

# Fire the ult on a pinned match with the foe parked far away, and look at the
# blades on the frame they are born.
SPRAY_JS = """([id, foe, seed]) => {
  const m = new AC.Match(id, foe, seed);
  const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
  // park the quarry in the far corner so nothing can resolve by accident
  th.x = 480; th.y = 760; th.vx = 0; th.vy = 0;
  me.x = 120; me.y = 120; me.vx = 0; me.vy = 0;
  const R = AC.CONFIG.physics.ballR;
  m.fireUlt(me, th);
  const blades = m.shots.filter(s => s.sc);
  const born = blades.map(s => ({
    d: Math.hypot(s.x - me.x, s.y - me.y),
    clear: Math.hypot(s.x - me.x, s.y - me.y) > R + s.r,
    arm: s.arm, bounce: s.bounce, spin: s.spin, r: s.r,
    speed: Math.hypot(s.vx, s.vy) }));
  const hp0 = th.hp;
  for (let i = 0; i < 6; i++) m.step(1/120);      // 0.05s — inside `arm`
  return { n: blades.length, born,
           minClear: Math.min(...born.map(b => b.d - (R + b.r))),
           allArmed: born.every(b => b.arm > 0),
           signs: [...new Set(born.map(b => Math.sign(b.spin)))].sort(),
           hpUnchangedInsideArm: th.hp === hp0,
           fuse: !!me.ultHarrow };
}"""

# Run real fights and watch every Harrowing cast: how many stuck, what the
# landing took, what the bloom took, how many sparks, and whether anything was
# still in the air when it went off.
CASTS_JS = """([id, foes, seeds]) => {
  const out = [];
  for (const foe of foes) for (const seed of seeds){
    const m = new AC.Match(id, foe, seed);
    const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
    let cast = null;
    let steps = 0;
    let prevFuse = false, prevStuck = 0, prevHp = th.hp;
    const casts = [];
    while (!m.over && steps < 60 * 120){
      const hpBefore = th.hp, stuckBefore = th.stuck.length;
      const sparksBefore = m.sparks.length;
      const fuseBefore = !!me.ultHarrow;
      m.step(1/120); steps++;
      // a cast just started
      if (!fuseBefore && me.ultHarrow){
        cast = { t: m.t, land: 0, landDmg: 0, peakStuck: 0,
                 bloomDmg: 0, bloomN: 0, sparks: 0, inAirAtBloom: -1,
                 stunAtBloom: 0 };
      }
      if (cast){
        if (th.stuck.length > stuckBefore){
          cast.land += th.stuck.length - stuckBefore;
          cast.landDmg += hpBefore - th.hp;
        }
        cast.peakStuck = Math.max(cast.peakStuck, th.stuck.length);
        // the bloom: the fuse was running and now it is not, on a live foe
        if (fuseBefore && !me.ultHarrow && th.alive && me.alive && !m.over){
          cast.bloomN = stuckBefore;
          cast.bloomDmg = hpBefore - th.hp;
          cast.sparks = m.sparks.length - sparksBefore;
          cast.inAirAtBloom = m.shots.filter(s => s.sc).length;
          cast.stunAtBloom = th.stun;
          casts.push(cast); cast = null;
        } else if (fuseBefore && !me.ultHarrow){
          cast.dropped = true; casts.push(cast); cast = null;
        }
      }
    }
    out.push({ foe, seed, dur: +(steps/120).toFixed(2), over: m.over,
               winner: m.winner ? m.winner.w.id : null,
               myHits: me.hits, foeHits: th.hits, clanks: m.clankCount,
               stuckLeft: th.stuck.length, burdenLeft: th.burden, casts });
  }
  return out;
}"""

# The burden, isolated. No opponent activity, no rng — just the two arithmetic
# sites, read directly.
BURDEN_JS = """([id, foe]) => {
  const m = new AC.Match(id, foe, 12345);
  const th = m.a.w.id === id ? m.b : m.a;
  const P = AC.CONFIG.physics;
  const base = th.moveMul();
  // the identity at zero: burden 0 must reproduce the pre-build expression
  const preBuild = Math.max(0.45, 1 + AC.STATUS.entangle.move * th.stacks("entangle"));
  const rows = [];
  for (const n of [0, 1, 2, 3, 4, 6]){
    th.burden = n; th.burdenMove = 0.05; th.burdenMass = 0.45;
    const mv = th.moveMul();
    const fall = Math.pow((th.w.mass + n * 0.45) / P.massRef, P.massWeight);
    rows.push({ n, move: +mv.toFixed(6), fall: +fall.toFixed(6) });
  }
  th.burden = 0; th.burdenMove = 0; th.burdenMass = 0;
  // entangle must still compose, and the floor must still hold
  th.apply("entangle", 4); th.burden = 6; th.burdenMove = 0.05;
  const both = th.moveMul();
  return { base, preBuild, identityAtZero: base === preBuild, rows,
           bothFloored: both, floorHeld: both >= 0.45 - 1e-12 };
}"""

# The burst, isolated: synthesise n stuck blades and call harrow() directly.
SCALE_JS = """([id, foe]) => {
  const rows = [];
  for (const n of [1, 2, 3, 4, 5, 6]){
    const m = new AC.Match(id, foe, 777);
    const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
    const own = me === m.a ? "a" : "b";
    me.x = 200; me.y = 400; th.x = 300; th.y = 400;
    th.vx = 0; th.vy = 0; th.stun = 0; th.stunDR = 0;
    for (let i = 0; i < n; i++)
      th.stuck.push({ ang: i, own, tilt: 0, r: 14 });
    th.burden = n; th.burdenMove = 0.05; th.burdenMass = 0.45;
    const hp0 = th.hp, sp0 = m.sparks.length;
    m.hitStop = 0; m.shake = 0;
    m.harrow(me, th);
    rows.push({ n, dmg: Math.round(hp0 - th.hp),
                knock: +Math.hypot(th.vx, th.vy).toFixed(1),
                stun: +th.stun.toFixed(4),
                stop: +m.hitStop.toFixed(4),
                shake: +m.shake.toFixed(1),
                sparks: m.sparks.length - sp0,
                sparksInGrace: m.sparks.every(s => s.arm > 0),
                stuckCleared: th.stuck.length === 0 && th.burden === 0
                              && th.burdenMove === 0 && th.burdenK === 0,
                banner: m.banner && m.banner.text });
  }
  // and the dud: a fuse that finds nothing
  const m0 = new AC.Match(id, foe, 778);
  const me0 = m0.a.w.id === id ? m0.a : m0.b, th0 = me0 === m0.a ? m0.b : m0.a;
  const hp0 = th0.hp;
  m0.harrow(me0, th0);
  return { rows, dud: { dmg: hp0 - th0.hp, phase: m0.ultFx && m0.ultFx.phase,
                        sparks: m0.sparks.length } };
}"""

# POST-MORTEM SAFETY, and the first version of this check was asking the wrong
# question. It killed a fighter and stepped, expecting the fuse to drop — but
# `step()` returns into `decay()` the moment `this.over` is set and
# `tickCharge` returns early on `!f.alive || this.over`, so the branch under
# test was never reached and the check failed against a build that was fine.
#
# What actually has to be true is two separate things:
#   (a) a fuse can never resolve once the match is over — guaranteed by those
#       same early returns, so this asserts the CONSEQUENCE (no damage, no
#       banner) rather than the state;
#   (b) the window where the quarry is dead and the match is still OPEN — the
#       kill flight — must drop the fuse and pull the blades. That path does
#       reach tickCharge, so it is driven directly.
DROP_JS = """([id, foe]) => {
  const res = {};

  // (a) match already over: the fuse must not pay out
  {
    const m = new AC.Match(id, foe, 4242);
    const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
    const own = me === m.a ? "a" : "b";
    m.fireUlt(me, th);
    for (let i = 0; i < 3; i++) th.stuck.push({ ang: i, own, tilt: 0, r: 14 });
    th.burden = 3; th.burdenMove = 0.05; th.burdenMass = 0.45;
    const hp0 = th.hp;
    m.over = true; m.banner = null;
    for (let i = 0; i < 600; i++) m.step(1/120);   // 5s, well past the 2.4 fuse
    res.overNoPayout = { dmg: hp0 - th.hp, banner: m.banner && m.banner.text };
  }

  // (b) quarry dead, match still open (the kill flight): drop and unstick
  {
    const m = new AC.Match(id, foe, 4243);
    const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
    const own = me === m.a ? "a" : "b";
    m.fireUlt(me, th);
    for (let i = 0; i < 3; i++) th.stuck.push({ ang: i, own, tilt: 0, r: 14 });
    th.burden = 3; th.burdenMove = 0.05; th.burdenMass = 0.45;
    th.hp = 0;
    m.tickCharge(me, th, 1/120);
    res.quarryDown = { fuse: !!me.ultHarrow, stuck: th.stuck.length,
                       burden: th.burden, move: +th.moveMul().toFixed(4) };
  }

  // (c) the mirror: caster dead, quarry alive, match still open
  {
    const m = new AC.Match(id, foe, 4244);
    const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
    const own = me === m.a ? "a" : "b";
    m.fireUlt(me, th);
    for (let i = 0; i < 3; i++) th.stuck.push({ ang: i, own, tilt: 0, r: 14 });
    th.burden = 3; th.burdenMove = 0.05; th.burdenMass = 0.45;
    me.hp = 0;
    m.tickCharge(me, th, 1/120);
    res.casterDown = { fuse: !!me.ultHarrow, stuck: th.stuck.length,
                       burden: th.burden, move: +th.moveMul().toFixed(4) };
  }
  return res;
}"""

# A blade that never reaches anyone: how many walls does it touch before it
# goes? Watched per blade, not inferred.
#
# THE CLOCK MATTERS AND THE FIRST VERSION USED THE WRONG ONE. It counted
# `steps/120` and asserted every blade was gone before the 2.4s fuse — and
# measured 2.64s against a build where nothing was wrong. Hit stop freezes the
# world but `this.t` keeps advancing (so match duration stays honest), and
# `s.life` only decrements on frames the sim actually advances. So step count
# and `m.t` are BOTH the wrong clock for this, and the only right one is the
# blade's own `life`. That is what is measured now; whether a blade can
# outlive the fuse is [6]'s job, measured on real fights.
BOUNCE_JS = """([id, foe, seed]) => {
  const m = new AC.Match(id, foe, seed);
  const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
  me.x = 260; me.y = 400; me.vx = 0; me.vy = 0;
  th.hp = 1e9;                       // parked and immortal, out of the way
  th.x = 40; th.y = 40; th.vx = 0; th.vy = 0;
  m.fireUlt(me, th);
  const A = AC.CONFIG.arena, n = m.inset;
  const seen = new Map();
  for (const s of m.shots)
    if (s.sc) seen.set(s, { start: s.bounce, min: s.bounce, lastLife: s.life,
                            zombie: false });
  let steps = 0;
  while (m.shots.some(s => s.sc) && steps < 120 * 8){
    m.step(1/120); steps++;
    for (const s of m.shots) if (s.sc && seen.has(s)){
      const r = seen.get(s);
      r.min = Math.min(r.min, s.bounce);
      r.lastLife = s.life;
      /* THE ACTUAL CLAIM. `tickShots` removes a spent blade on the frame it
         reaches a wall with no bounces left, so a blade observed ALIVE, at a
         wall, holding zero bounces is a third bounce that should not exist.
         The bounce branch clamps to exactly `n + r`, and the spent test is a
         strict inequality, so sitting exactly on the boundary for the frame
         it bounced is correct and is not counted. */
      if (s.bounce <= 0 &&
          (s.x < n + s.r - 0.001 || s.x > A.w - n - s.r + 0.001 ||
           s.y < n + s.r - 0.001 || s.y > A.h - n - s.r + 0.001))
        r.zombie = true;
    }
  }
  const rows = [...seen.values()];
  return { blades: rows.length,
           startAll2: rows.every(r => r.start === 2),
           minSeen: Math.min(...rows.map(r => r.min)),
           everNegative: rows.some(r => r.min < 0),
           reachedZero: rows.filter(r => r.min === 0).length,
           zombies: rows.filter(r => r.zombie).length,
           /* Blades end three legitimate ways — latched, parried out of the
              air, or expired — so a blade removed with life left is NOT a
              defect and the first version of this check wrongly said it was.
              Reported, not asserted. */
           endedEarly: rows.filter(r => r.lastLife > 0.02).length,
           allGone: !m.shots.some(s => s.sc) };
}"""

# Every relic's set-piece, drawn. A relic whose ult art throws takes the whole
# frame down, and the failure would first show up in a render, not here.
DRAWALL_JS = """(id) => {
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const bad = [];
  for (const w of AC.WEAPONS){
    const foe = AC.WEAPONS.find(x => x.id !== w.id).id;
    try {
      const m = new AC.Match(w.id, foe, 31337);
      const me = m.a.w.id === w.id ? m.a : m.b, th = me === m.a ? m.b : m.a;
      m.fireUlt(me, th);
      for (let i = 0; i < 40; i++){ m.step(1/120); AC.__draw(m); }
    } catch (e) { bad.push({ id: w.id, err: String(e) }); }
  }
  // and the Harrowing's own three phases, forced
  for (const phase of ["cast", "bloom", "cold"]){
    try {
      const m = new AC.Match(id, "dawnbringer", 9);
      const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
      m.ultFx = { w: id, kind: "harrow", phase, src: me === m.a ? "a" : "b",
                  tgt: me === m.a ? "b" : "a", x: th.x, y: th.y,
                  tx: th.x, ty: th.y, hit: phase !== "cold", radius: 300,
                  aff: me.aff, t: 0, n: 5, life: 2 };
      for (let i = 0; i < 30; i++){ m.ultFx.t += 0.04; AC.__draw(m); }
    } catch (e) { bad.push({ id: id + ":" + phase, err: String(e) }); }
  }
  return bad;
}"""

SHOT_JS = """([id, foe, seed, plan]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, seed);
  const me = m.a.w.id === id ? m.a : m.b, th = me === m.a ? m.b : m.a;
  m.introT = 0;
  me.x = 180; me.y = 420; me.vx = 0; me.vy = 0;
  th.x = 330; th.y = 470; th.vx = 0; th.vy = 0;
  const own = me === m.a ? "a" : "b";
  if (plan.mode === "spray"){
    m.fireUlt(me, th);
    for (let i = 0; i < plan.steps; i++) m.step(1/120);
  } else if (plan.mode === "stuck"){
    m.fireUlt(me, th);
    for (let i = 0; i < plan.n; i++)
      th.stuck.push({ ang: (i / plan.n) * Math.PI * 2, own, tilt: 0, r: 14 });
    th.burden = plan.n; th.burdenMove = 0.05; th.burdenMass = 0.45;
    th.burdenK = plan.k;
    m.shots = m.shots.filter(s => !s.sc);
  } else if (plan.mode === "bloom"){
    for (let i = 0; i < plan.n; i++)
      th.stuck.push({ ang: (i / plan.n) * Math.PI * 2, own, tilt: 0, r: 14 });
    th.burden = plan.n;
    m.harrow(me, th);
    m.ultFx.t = plan.t;
  }
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""


def png(d):
    from PIL import Image
    return Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGB")


def contact(imgs, labels, out, scale=0.34, title=""):
    from PIL import Image, ImageDraw
    W, H = 1080, 1920
    tw, th = int(W * scale), int(H * scale)
    PAD, LBL = 14, 32
    sh = Image.new("RGB", (len(imgs) * (tw + PAD) + PAD, th + PAD * 2 + LBL), (12, 10, 18))
    dr = ImageDraw.Draw(sh)
    dr.text((PAD, 8), title, fill=(201, 162, 39))
    for i, (im, lab) in enumerate(zip(imgs, labels)):
        x = PAD + i * (tw + PAD)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, PAD + LBL))
        dr.text((x + 2, PAD + LBL - 14), lab, fill=(214, 200, 170))
    sh.save(out)
    print(f"    {out.name}  ({sh.width}x{sh.height})")
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="../02-chain/sc-lastlight.html")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--sheet", action="store_true")
    A = ap.parse_args()

    g = (HERE / A.game).resolve()
    if not g.exists():
        sys.exit(f"no such build: {g}")

    results = []          # (label, ok, detail)

    def chk(label, ok, detail=""):
        results.append((label, bool(ok), detail))
        print(f"  {'PASS' if ok else 'FAIL'}  {label}"
              + (f"\n          {detail}" if detail else ""))

    print(f"=== harrow_probe — {g.name} ===\n")

    for label, ok, detail in source_checks(g):
        chk(label, ok, detail)

    FOES = ["dawnbringer", "thornwake", "gravemourn", "grudgebearer",
            "spellbreaker", "ironhail"]
    SEEDS = [1000 + i * 7919 for i in range(A.seeds)]

    with game(game_path=g) as (page, errors):
        # ---------------------------------------------------------- [1] ----
        s = page.evaluate(STRUCT_JS, ID)
        if s.get("err"):
            sys.exit(f"[1] {s['err']}")
        chk("[1] structure — sanctified scythe, Smite, melee, _scRadiant",
            s["aff"] == "sanctified" and s["shape"] == "scythe"
            and s["statusKey"] == "smite" and s["shot"] is None
            and s["branch"] == "_scRadiant" and s["ultKind"] == "harrow"
            and s["ultTipLen"] <= 72 and s["roster"] == 18,
            f"{s['name']} · {s['aff']}/{s['shape']} · status {s['statusKey']} · "
            f"shot {s['shot']} · art {s['branch']} · ult {s['ultName']} "
            f"({s['ultKind']}, tip {s['ultTipLen']}/72) · roster {s['roster']}")
        chk("[1b] physics are Thornwake's exactly (the TYPE owns them)",
            (s["reach"], s["spin"], s["mode"], s["mass"]) == (104, 3.2, "spin", 2.4),
            f"reach {s['reach']} spin {s['spin']} mode {s['mode']} mass {s['mass']}")

        # ---------------------------------------------------------- [2] ----
        sp = page.evaluate(SPRAY_JS, [ID, "dawnbringer", 20260817])
        chk("[2] the spray — 12 blades, all clear of the shell, all armed, "
            "nothing resolves inside the arm window",
            sp["n"] == 12 and sp["minClear"] > 0 and sp["allArmed"]
            and sp["hpUnchangedInsideArm"] and sp["fuse"],
            f"n={sp['n']} · closest born {sp['minClear']:.1f}px OUTSIDE the hit "
            f"radius · armed={sp['allArmed']} · foe hp unchanged at 0.05s="
            f"{sp['hpUnchangedInsideArm']} · fuse lit={sp['fuse']}")
        chk("[2b] blades turn both ways (the spray is not 12 copies)",
            sp["signs"] == [-1, 1], f"spin signs {sp['signs']}")

        # ---------------------------------------------------------- [5] ----
        b = page.evaluate(BURDEN_JS, [ID, "dawnbringer"])
        rows = b["rows"]
        mono_move = all(rows[i]["move"] > rows[i + 1]["move"] for i in range(len(rows) - 1))
        mono_fall = all(rows[i]["fall"] < rows[i + 1]["fall"] for i in range(len(rows) - 1))
        chk("[5a] burden 0 reproduces the pre-build moveMul EXACTLY "
            "(this is what lets engine_ab prove the roster inert)",
            b["identityAtZero"], f"{b['base']!r} === {b['preBuild']!r}")
        chk("[5b] burden slows movement and increases fall, monotonically",
            mono_move and mono_fall,
            "  ".join(f"n={r['n']}:move {r['move']:.3f}/fall {r['fall']:.3f}"
                      for r in rows))
        chk("[5d] entangle still composes, and the 0.45 floor still holds",
            b["floorHeld"], f"4 entangle + 6 blades -> moveMul {b['bothFloored']:.4f}")

        # ---------------------------------------------------------- [7] ----
        sc = page.evaluate(SCALE_JS, [ID, "dawnbringer"])
        r = sc["rows"]
        def rising(k):
            return all(r[i][k] < r[i + 1][k] for i in range(len(r) - 1))
        chk("[7] the burst scales on n — damage, knock, stun and hit stop all "
            "strictly increasing",
            rising("dmg") and rising("knock") and rising("stun") and rising("stop"),
            "\n          " + "\n          ".join(
                f"n={x['n']}  dmg {x['dmg']:>3}  knock {x['knock']:>6}  "
                f"stun {x['stun']:.3f}  stop {x['stop']:.3f}  shake {x['shake']:>5}  "
                f"sparks {x['sparks']:>2}" for x in r))
        chk("[7b] the burst clears every burden field it consumed",
            all(x["stuckCleared"] for x in r),
            "a partial clear is a ball that stays slow for the rest of the match")
        chk("[7c] the name lands on the bloom, not on the cast",
            all(x["banner"] == "Harrowing" for x in r))

        # ---------------------------------------------------------- [8] ----
        chk("[8] sparks are Daybreak's — 2 per blade, all born in grace",
            all(x["sparks"] == 2 * x["n"] for x in r)
            and all(x["sparksInGrace"] for x in r),
            "  ".join(f"n={x['n']}->{x['sparks']}" for x in r))
        chk("[8b] a dud bursts for nothing and says so",
            sc["dud"]["dmg"] == 0 and sc["dud"]["phase"] == "cold"
            and sc["dud"]["sparks"] == 0,
            f"dmg {sc['dud']['dmg']} · phase {sc['dud']['phase']} · "
            f"sparks {sc['dud']['sparks']}")

        # --------------------------------------------------------- [10] ----
        d = page.evaluate(DROP_JS, [ID, "dawnbringer"])
        chk("[10a] a fuse cannot pay out after the match is over",
            d["overNoPayout"]["dmg"] == 0 and not d["overNoPayout"]["banner"],
            f"5s stepped past a 2.4s fuse with over=true: "
            f"{d['overNoPayout']['dmg']} damage, banner "
            f"{d['overNoPayout']['banner']!r}")
        for who in ("quarryDown", "casterDown"):
            v = d[who]
            chk(f"[10b] {who}: the fuse drops and the blades come out "
                "(the kill-flight window, where the match is still open)",
                not v["fuse"] and v["stuck"] == 0 and v["burden"] == 0
                and abs(v["move"] - 1.0) < 1e-12, json.dumps(v))

        # --------------------------------------------------------- [11] ----
        bo = page.evaluate(BOUNCE_JS, [ID, "dawnbringer", 555])
        chk("[11] a miss bounces at most twice, then expires — no blade ever "
            "takes a third wall",
            bo["startAll2"] and not bo["everNegative"] and bo["reachedZero"] > 0
            and bo["zombies"] == 0 and bo["allGone"],
            f"{bo['blades']} blades · all start at 2 · min bounce seen "
            f"{bo['minSeen']} · {bo['reachedZero']} spent both bounces · "
            f"third-bounce zombies {bo['zombies']} · all removed="
            f"{bo['allGone']} · {bo['endedEarly']} ended early (latched or "
            f"parried, both legitimate)")

        # ------------------------------------------------ [4][6][9] real ----
        casts = page.evaluate(CASTS_JS, [ID, FOES, SEEDS])
        allc = [c for row in casts for c in row["casts"]]
        blooms = [c for c in allc if not c.get("dropped")]
        n_land = [c["bloomN"] for c in blooms]
        duds = sum(1 for n in n_land if n == 0)
        landed = [c for c in blooms if c["bloomN"] > 0]
        chk("[4] the double payoff — a blade that lands takes hp AND sticks",
            bool(landed) and all(c["landDmg"] > 0 for c in landed),
            (f"{len(landed)} blooms with at least one blade; landing damage "
             f"median {statistics.median([c['landDmg'] for c in landed]):.0f} "
             f"over {sum(c['land'] for c in landed)} landings")
            if landed else
            f"NO BLADE EVER STUCK across {len(blooms)} casts — the latch "
            f"branch is unreachable or the spray cannot connect")
        chk("[6] one bloom — nothing of the cast is still in the air when it goes",
            all(c["inAirAtBloom"] == 0 for c in blooms),
            f"max blades airborne at bloom across {len(blooms)} casts: "
            f"{max([c['inAirAtBloom'] for c in blooms] or [0])}")

        hist = {k: n_land.count(k) for k in sorted(set(n_land))}
        print(f"\n  [9] THE DUD RATE, measured over {len(blooms)} casts "
              f"({len(FOES)} foes x {len(SEEDS)} seeds)\n")
        for k, v in hist.items():
            print(f"        {k} blade{'s' if k != 1 else ' '}   {v:>4}  "
                  f"{v/len(blooms)*100:>5.1f}%  {'#' * int(v/len(blooms)*60)}")
        mean_n = statistics.mean(n_land) if n_land else 0
        print(f"\n        mean {mean_n:.2f} blades · "
              f"DUDS {duds}/{len(blooms)} = {duds/max(1,len(blooms))*100:.1f}%"
              f"   (Slagburst's was 26.3% before its fix)")
        bd = [c["bloomDmg"] for c in landed]
        if bd:
            print(f"        bloom damage: median {statistics.median(bd):.0f}, "
                  f"max {max(bd):.0f}")

        drops = sum(1 for c in allc if c.get("dropped"))
        print(f"        {drops} casts had the fuse dropped by a death mid-fuse")

        stuck_left = sum(row["stuckLeft"] for row in casts)
        print(f"        {stuck_left} blades were still in a shell when a fight "
              f"ended (cosmetic — `decay()` does not call `move()`, so the "
              f"burden is not read after `over`)")

        # --------------------------------------------------------- [12] ----
        bad = page.evaluate(DRAWALL_JS, ID)
        chk("[12] every relic's set-piece draws, and all three Harrowing "
            "phases draw", not bad, json.dumps(bad[:3]) if bad else "18 relics + 3 phases")

        if A.sheet:
            print("\n  art samples")
            imgs, labs = [], []
            for lab, plan in [("spray 0.15s", {"mode": "spray", "steps": 18}),
                              ("spray 0.45s", {"mode": "spray", "steps": 54}),
                              ("3 stuck, fuse 0.2", {"mode": "stuck", "n": 3, "k": 0.2}),
                              ("3 stuck, fuse 0.95", {"mode": "stuck", "n": 3, "k": 0.95}),
                              ("bloom n=5, t=0.15", {"mode": "bloom", "n": 5, "t": 0.15}),
                              ("bloom n=5, t=0.55", {"mode": "bloom", "n": 5, "t": 0.55})]:
                imgs.append(png(page.evaluate(SHOT_JS, [ID, "gravemourn", 4242, plan])))
                labs.append(lab)
            contact(imgs, labs, HERE.parent / "harrow-art.png", 0.30,
                    "THE HARROWING — throw, stick, bloom")

        if errors:
            chk("[0] no page errors", False, str(errors[:3]))
        else:
            chk("[0] no page errors", True)

    ok = sum(1 for _, o, _ in results if o)
    print(f"\n{ok}/{len(results)} checks pass")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
