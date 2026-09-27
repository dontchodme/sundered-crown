#!/usr/bin/env python
"""BLOODWICK / GYRE -- the bloodsworn staff, the staff row's sixth. v90.

Built from `06-docs/v90/BLOODWICK-BUILD-BRIEF.md` and `bloodsworn-staff-design-v90.md`
(Cowork, 2026-09-27), the row's `06-docs/v89/STAFF-ROW-v89.md` §1/§6 -- the
input and the only input (CLAUDE.md §3 rule 0). Rick: "build them all".

    stage 1   the relic, its ultimate STUBBED          sc-crozier-fx -> sc-bloodwick
    stage 2   the spell: BLOODSEEKER (the bend)        sc-bloodwick -> sc-seeker
    stage 3   the ultimate's orbit (arm V, no lunge)   sc-seeker -> sc-orbit
    stage 4   the lunge: GYRE whole (arm U)            sc-orbit -> sc-gyre

THE BASE is the staff branch's tip (Culverin, Briarwand, Cipher, Watchlight,
Crozier); several anchors are those builds' own lines.

THE READINGS, where the build has to choose:
  1. THE BEND IS COPIED AT SPAWN (§5: "`spawnShot` copies `home`"), and a
     globule joins the orbit AT SPAWN. The lab did both from `fresh()`, one
     step late, so a globule's first step was straight and an orbiter flew
     one step as a seeker before it joined. Measured at stage 2.
  2. AN ORBITER IS PLACED, NOT MOVED (§5 and brief §1: "in `tickShots`,
     before the move: an orbiter is placed (position + tangential velocity)
     rather than advanced") -- and then meets every other test a shot meets:
     a blade through the ring clanks it (§5: "the counterplay, and it reads"),
     the foe's ball takes its blow, a wall kills it.
  3. THE ORBIT IS EVEN over the CURRENT count (§5: `phase + i*2pi/n`), as the
     lab's placement loop was -- the lab's stored `ph` was never read.
  4. THE WINDOW keeps its 8s on the engine's window clock (Cipher's
     measurement, v94 build §3); the charge is the lab's 16 in the game's
     clock, measured for this fighter.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC, BUILDER = "bloodwick", "bloodwick_build.py"
BLADE = 8.5                    # brief §2 stage 1: "stubbed relic at 8.5"; stage 5 settles it
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.34, speed=300, r=22, life=3.0, grav=0, dmgMul=1.0, home=1.0,
             spell="bloodseeker", tip="Globules bend toward the foe · clankable")
CARD = "Its blood orbits it, then lunges as one when the foe comes close"
ULT_NAME, ULT_KIND = "Gyre", "gyre"
# Design §5, brief §0. `charge` is the lab's 16 in the game's clock, measured.
# `lunge` is stage 3's switch (0: the orbit alone, arm V) and stage 4 sets it.
ULT = {"charge": 14, "dur": 8, "maxOrb": 6, "orbitR": 95, "orbitW": 4.0,
       "lungeR": 230, "lungeV": 520, "lungeHome": 8, "lungeLife": 2.0}
ULT_KEYS = list(ULT)
BLURB = ("A dark rod with a flame guttering in red glass. What it bleeds bends toward "
         "the foe, and for eight seconds it circles the wick and strikes as one.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm A of design §3.1, the bloodsworn
     BOW body at the staff's blade -- which stage 2's globule is measured
     against.
'''
ULT_STUB = f'''    /* GYRE. STUBBED AT `charge:1e9` IN STAGE 1. `kind:"{ULT_KIND}"` is its own;
       the card is Cowork's (design §6), in at stage 1. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''
S1_BLADE_PARA = f'''     `dmg` {fnum(BLADE)} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 8.4 on Chromium 141, and stage 5 settles it wide on 151. */'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* BLOODWICK -- THE BLOODSWORN STAFF, the staff row's sixth relic. Built from
     `06-docs/v90/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Bloodsworn bleeds; the
     bloodsworn bow body is the row's weakest (5.0% at this blade), and this
     is a relic that IS its ultimate (design §4: 20 points between blade 8
     and 9, Bindweed's shape).

{S1_SHOT_PARA}
{S1_BLADE_PARA}
  {{ id:"{RELIC}", name:"Bloodwick", aff:"bloodsworn", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ hemorrhage:2 }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [("Bloodwick joins the roster, its ultimate stubbed",
             '''

];
/* The single source of truth for "which status does this relic teach".''',
             relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".''')]


S2_SHOT_PARA = '''     THE SPELL IS BLOODSEEKER (design §1, §5): a globule of blood every 0.34s
     along the facing, slower than an arrow (300), that BENDS toward the foe
     as it flies -- `home` 1.0 rad/s, the field `tickShots` already turns on
     for Bloodhunt's bolts: a curve, not a hunt. Each that lands hemorrhages
     2. At home 2.2 the same globule won 96 fights in 100 with no ultimate at
     all (§3): the bend was cut, not the blade -- do not "fix" it upward.
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Bloodwick looses the globule",
 f'''  {{ id:"{RELIC}", name:"Bloodwick", aff:"bloodsworn", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Bloodwick", aff:"bloodsworn", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("spawnShot: a globule carries its bend from the barrel",
 '''      if (S.pierce) s.pierce = true;
''',
 '''      if (S.pierce) s.pierce = true;
      /* BLOODWICK'S GLOBULE (v90 §5): `spawnShot` copies `home`, AT SPAWN --
         the lab set it one step late, so a globule's first step was straight.
         `tickShots`' homing turns it at `home` rad/s, rate-limited. */
      if (S.home !== undefined) s.home = S.home;
'''),

("the globule is drawn (first cut)",
 '''      /* CROZIER'S LANCE ON SCREEN (v95 §6.1).''',
 '''      /* BLOODWICK'S GLOBULE -- FIRST CUT, for stage 2's film; the picture is
         stage 6's. "A fat drop of blood, r 22, with a short trailing tail drawn
         from its velocity; it visibly curves" (v90 §6.1) -- the tail is the
         homing code's own ring buffer of real positions where it has one. Off
         the shot's own state; no rng. */
      if (s.spell === "bloodseeker"){
        const pal = s.aff, sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        c.save();
        c.lineCap = "round"; c.lineJoin = "round";
        c.globalAlpha = 0.55; c.strokeStyle = pal.core; c.lineWidth = s.r * 0.7;
        c.beginPath();
        if (s.trail && s.trail.length >= 4){
          c.moveTo(s.trail[0], s.trail[1]);
          for (let j = 2; j < s.trail.length; j += 2) c.lineTo(s.trail[j], s.trail[j + 1]);
          c.lineTo(s.x, s.y);
        } else { c.moveTo(s.x - ux * s.r * 1.6, s.y - uy * s.r * 1.6); c.lineTo(s.x, s.y); }
        c.stroke();
        c.globalAlpha = 1; c.fillStyle = pal.core;
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.72, 0, TAU); c.fill();
        c.fillStyle = pal.glow; c.globalAlpha = 0.8;
        c.beginPath(); c.arc(s.x - s.r * 0.22, s.y - s.r * 0.22, s.r * 0.22, 0, TAU); c.fill();
        c.restore();
        continue;
      }
      /* CROZIER'S LANCE ON SCREEN (v95 §6.1).'''),
    ]


ULT_NOTE = '''    /* GYRE (design §1, §5). For `dur` seconds the globules do not leave: up
       to `maxOrb` of them orbit the ball at `orbitR`, `orbitW` rad/s, evenly
       spaced; when the foe comes within `lungeR` they all lunge at once
       (`lungeV`, homing `lungeHome`, `lungeLife` s) and each that lands
       hemorrhages. At the close whatever is still orbiting is loosed as
       ordinary seekers. THE LUNGE IS THE PAYLOAD (+31); the orbit alone is a
       moat worth +2 to +4 (§3).

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v90/bloodwick-build-v90.md`. */
'''


def s3_edits(U: dict):
    return [
("Gyre is live -- the orbit alone at this stage", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Gyre's orbit",
 '''    this.radianceAge = 0;
''',
 '''    this.radianceAge = 0;
    /* {t, dur, orb, phase} while GYRE's window is open (v90): the orbiters in
       their slots and where the ring has turned to. null otherwise: `tickGyre`
       returns after a two-iteration loop. `gyreTally` is the probe's; nothing
       in the sim reads it. */
    this.ultGyre = null;
    this.gyreTally = null;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "radiance"){
''',
 '''    if (u.kind === "gyre"){
      /* GYRE (v90). NOTHING RESOLVES HERE: `spawnShot` takes the globules into
         orbit, `tickShots` places them, `tickGyre` turns the ring, lunges and
         looses. `m.ultFx` is the cast flash only (open item 25). */
      f.ultGyre = { t: 0, dur: u.dur, orb: [], phase: 0 };
      if (!f.gyreTally) f.gyreTally = { casts: 0, orbited: 0, lunged: 0, loosed: 0, lunges: 0 };
      f.gyreTally.casts++;
      return;
    }
    if (u.kind === "radiance"){
'''),

("spawnShot: a globule loosed in the window takes its slot in the orbit",
 '''      if (S.home !== undefined) s.home = S.home;
''',
 '''      if (S.home !== undefined) s.home = S.home;
      /* GYRE (v90 §5): while the window runs, a globule loosed with fewer than
         `maxOrb` in orbit is taken into it, AT SPAWN (the lab: one step late) --
         `home` 0, and `tickShots` places it from now on. */
      if (f.ultGyre && f.ultGyre.orb.length < f.w.ult.maxOrb){
        s.orb = true; s.home = 0; f.ultGyre.orb.push(s); f.gyreTally.orbited++;
      }
'''),

("tickShots: an orbiter is placed on its lane, not moved",
 '''      /* RADIANCE'S GROWTH (v95 §5): k = min(1, (t - born) / T), r = r0 + (r1 -''',
 '''      /* GYRE'S ORBIT (v90 §5): an orbiter is PLACED -- on the lane at `orbitR`,
         evenly over the current count (`phase + i*2pi/n`), with the tangential
         velocity, its life refreshed -- rather than advanced, and then meets
         every test below as any shot: a blade through the ring clanks it (the
         counterplay), the foe's ball takes its blow, a wall kills it. */
      let placed = false;
      if (s.orb){
        const o = s.own === "a" ? this.a : this.b, G = o.ultGyre;
        const i = G ? G.orb.indexOf(s) : -1;
        if (i >= 0){
          const u = o.w.ult, n = G.orb.length, ang = G.phase + i * TAU / n;
          s.x = o.x + Math.cos(ang) * u.orbitR; s.y = o.y + Math.sin(ang) * u.orbitR;
          s.vx = -Math.sin(ang) * u.orbitR * u.orbitW; s.vy = Math.cos(ang) * u.orbitR * u.orbitW;
          s.a = ang + Math.PI / 2; s.life = s.max;
          placed = true;
        }
      }
      /* RADIANCE'S GROWTH (v95 §5): k = min(1, (t - born) / T), r = r0 + (r1 -'''),

("tickShots: ...and so does not move",
 '''      s.vy += s.grav * dt;
      s.x += s.vx * dt; s.y += s.vy * dt;
      s.life -= dt;''',
 '''      if (!placed){
        s.vy += s.grav * dt;
        s.x += s.vx * dt; s.y += s.vy * dt;
        s.life -= dt;
      }'''),

("the window ticks with the window tickers",
 '''    this.tickRadiance(dt);              // RADIANCE (v95): the lances grow
''',
 '''    this.tickRadiance(dt);              // RADIANCE (v95): the lances grow
    this.tickGyre(dt);                  // GYRE (v90): the blood circles
'''),

("tickGyre: the ring turns, and the close looses it",
 '''  /* ================================================== RADIANCE ========''',
 '''  /* ====================================================== GYRE ========
     v90 §5, and the lab (`overlays/staff_blood.js`) where the prose is silent.
     Each step of the window the ring turns (`phase += orbitW * dt`) and drops
     what is no longer in the hall; `tickShots` places what is left. AT THE
     CLOSE -- the clock, a death or the end -- whatever still orbits is loosed
     toward the foe at the spell's own speed and bend (§5). THE CLOCK is the
     window tickers' and stops through a hit stop; the lab's counted every
     step. */
  tickGyre(dt){
    for (const f of [this.a, this.b]){
      const G = f.ultGyre;
      if (!G) continue;
      const foe = f === this.a ? this.b : this.a;
      const live = new Set(this.shots);
      G.orb = G.orb.filter(s => live.has(s));
      if (!f.alive || !foe.alive || this.over){ this.gyreLoose(f, foe); f.ultGyre = null; continue; }
      G.t += dt;
      G.phase += f.w.ult.orbitW * dt;
      if (G.t >= G.dur){ this.gyreLoose(f, foe); f.ultGyre = null; continue; }
    }
  }

  /* THE CLOSE (v90 §5): "whatever is still orbiting is loosed as ordinary
     seekers" -- at the foe, at the spell's own speed, with its own bend. */
  gyreLoose(f, foe){
    const G = f.ultGyre, S = f.w.shot;
    for (const s of G.orb){
      const ang = Math.atan2(foe.y - s.y, foe.x - s.x);
      s.orb = false; s.home = S.home;
      s.vx = Math.cos(ang) * S.speed; s.vy = Math.sin(ang) * S.speed; s.a = ang;
      f.gyreTally.loosed++;
    }
    G.orb = [];
  }

  /* ================================================== RADIANCE ========'''),

("the orbit's lane is drawn (first cut)",
 '''    this.drawRadiance(m);        // RADIANCE's halo and bead (v95 §6.1)
''',
 '''    this.drawRadiance(m);        // RADIANCE's halo and bead (v95 §6.1)
    /* GYRE's lane -- FIRST CUT, for stage 3's film: "a thin ring at r 95
       (`glow`, alpha 0.35) shows the orbit's lane" (v90 §6.1). */
    for (const f of [m.a, m.b]){
      if (!f.ultGyre || !f.alive) continue;
      const c = this.ctx;
      c.save(); c.globalAlpha = 0.35; c.strokeStyle = f.aff.glow; c.lineWidth = 1.5;
      c.beginPath(); c.arc(f.x, f.y, f.w.ult.orbitR, 0, TAU); c.stroke(); c.restore();
    }
'''),
    ]


def s4_edits():
    return [
("tickGyre: the lunge",
 '''      G.phase += f.w.ult.orbitW * dt;
''',
 '''      G.phase += f.w.ult.orbitW * dt;
      /* THE LUNGE (v90 §5): when the foe comes within `lungeR` of the ball,
         every orbiter is loosed at it at once -- `lungeV`, homing `lungeHome`,
         `lungeLife` s -- and the director is told (rule 3: one `ult` beat at
         the caster). The orbit empties and fills again from the next globule. */
      const u = f.w.ult;
      if (G.orb.length && Math.hypot(foe.x - f.x, foe.y - f.y) < u.lungeR){
        for (const s of G.orb){
          const ang = Math.atan2(foe.y - s.y, foe.x - s.x);
          s.orb = false; s.home = u.lungeHome; s.life = u.lungeLife; s.max = u.lungeLife;
          s.vx = Math.cos(ang) * u.lungeV; s.vy = Math.sin(ang) * u.lungeV; s.a = ang;
          f.gyreTally.lunged++;
        }
        f.gyreTally.lunges++;
        this.beat({ kind: "ult", side: f === this.a ? 0 : 1, w: f.w.id, x: f.x, y: f.y, lunge: G.orb.length });
        G.orb = [];
      }
'''),
    ]


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        return 4 if "gyreTally.lunges++" in code else 3
    return 2 if "home:" in re.search(r"shot:\{([^}]*)\}", ent).group(1) else 1


def all_stages():
    return [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT))), ("4", s4_edits())]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "4"])
    ap.add_argument("--src"); ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nBLOODWICK / GYRE -- the insert audit against {A.audit}")
        return audit(all_stages(), (HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8"); s = s0
    print(f"\nBLOODWICK / GYRE -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"crozier"' not in code or "radianceFade" not in code:
        raise SystemExit("wrong base: no Crozier stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin, Briarwand, Cipher, Watchlight and Crozier in it")
    have = stage_of(code)
    want = {1: 0, 2: 1, 3: 2, 4: 3}[stage]
    if have != want:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built on stage {want}")
    if stage == 1:
        check_bow_body(code); edits = s1_edits()
    elif stage == 2:
        edits = s2_edits(re.search(r"dmg:([\d.]+),", relic_entry(code, RELIC)).group(1))
    elif stage == 3:
        edits = s3_edits(dict(ULT))
    else:
        edits = s4_edits()
    for label, old, new in edits:
        s = one(s, old, new, label)
    out = strip_comments(s)
    shot = SPELL if stage >= 2 else BOW_SHOT
    ent = check_entry(out, RELIC, shot, BLADE, stubbed=(stage <= 2))
    if "onHit:{ hemorrhage:2 }" not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- {RELIC} does not hemorrhage 2 on hit")
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 2 and out.count("if (S.home !== undefined) s.home = S.home;") != 1:
        raise SystemExit("REFUSING TO WRITE -- the bend is not copied at spawn exactly once")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        for need in ("tickGyre(dt){", "this.tickGyre(dt);", 'u.kind === "gyre"', "gyreLoose(f, foe){", "let placed = false;"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS) + ("" if stage >= 4 else "   (the lunge comes at stage 4)"))
    check_no_rng(edits)
    if out.count('shape:"staff"') != 6:
        raise SystemExit("REFUSING TO WRITE -- expected exactly six staves in the roster")
    print(f"  ok    relic  staff, the bow's body, hemorrhage 2, {'the globule' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    six staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
