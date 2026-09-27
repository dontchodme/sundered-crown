#!/usr/bin/env python
"""BRIARWAND / BLOOM -- the verdant staff, the staff row's second. v93.

Built from `06-docs/v93/BRIARWAND-BUILD-BRIEF.md` and
`verdant-staff-design-v93.md` (Cowork, 2026-09-27), the row's
`06-docs/v89/STAFF-ROW-v89.md` §1/§6. Those are the input and the only input
(CLAUDE.md §3 rule 0). Rick, 2026-09-27: "go ahead with the rest" / "build
them all".

    stage 1   the relic, its ultimate STUBBED           sc-ironfall-fx -> sc-briarwand
    stage 2   the spell: THORNBURST (the fan)           sc-briarwand -> sc-thornburst
    stage 3   the ultimate: BLOOM (the drifting cloud)  sc-thornburst -> sc-bloom
    stage 5   the blade, wide on 151                    (not written yet)
    stage 6   picture, voices                           (not written yet)

THE BASE is the staff branch's tip, `sc-ironfall-fx.html` (sc-leaf + Culverin
stages 1-6): the STAFF art and `shape:"staff"` are already in it, and several
anchors below are Culverin's own lines, so the two carry together, in order.

TWO NAMES THE BRIEF USES ARE NOT THE ONES BUILT, AND NEITHER IS A DESIGN CHOICE:
  * `f.ultBloom` is the THICKET's (Vinesower's seed window) -- `spawnShot` reads
    it on every shot. Briarwand's cloud lives in `f.ultPollen`, the lab's own
    name for it. `kind:"bloom"` is free (the Thicket is `seedfall`) and is used.
  * The spell's shot block gains `spell:"thornburst"` beside the design's
    numbers, for the renderer (Culverin's `spell` line in `spawnShot`).
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from staffkit import (BODY, HERE, one, strip_comments, relic_entry, fnum, shot_js,
                      check_bow_body, check_entry, check_no_rng, write_link, paths, audit)

RELIC = "briarwand"
BUILDER = "briarwand_build.py"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9).
BLADE = 17                     # brief §2 stage 1: "stubbed relic at 17"; stage 5 settles it
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
SPELL = dict(cadence=0.42, speed=440, r=16, life=1.2, grav=0, dmgMul=0.6, fan=3, spread=0.28,
             spell="thornburst", tip="Throws a fan of three thorns · clankable")
CARD = "A pollen cloud drifts after the foe: inside it, entangle and bites"
ULT_NAME, ULT_KIND = "Bloom", "bloom"
# Design §5 and brief §0. `charge` is the lab's 16 in the game's clock (the
# batch's ruling, "use the game's equivalent"), measured for this fighter.
ULT = {"charge": 14, "dur": 8, "cloudR": 110, "drift": 90, "every": 0.4, "bite": 2.5, "stk": 1}
ULT_KEYS = list(ULT)
BLURB = ("A briar rod that throws its own thorns, three at a time. For eight seconds "
         "its pollen goes looking for you.")


def ult_live(U: dict) -> str:
    kv = ", ".join(f"{k}:{fnum(U[k])}" for k in ULT_KEYS if k != "charge")
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}",
          {kv},
          tip:"{CARD}" }},''')


# ---------------------------------------------------------------- stage 1 --
S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW -- arm A of design §3.1, the verdant BOW
     body at the staff's blade -- which stage 2's fan is measured against.
'''

ULT_STUB = f'''    /* BLOOM. STUBBED AT `charge:1e9` IN STAGE 1 (the "OFF" every stubbed relic
       since v55b has used). `kind:"{ULT_KIND}"` is its own; the card is
       Cowork's (design §6), in at stage 1 so `tip_audit` measures the real
       line. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''


def relic_block() -> str:
    b = BODY
    return f'''

  /* BRIARWAND -- THE VERDANT STAFF, the staff row's second relic. Built from
     `06-docs/v93/` (Cowork's design; the row accepted by Rick, 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1): the bow's physics, asserted off
     Ironhail by the builder; the SHOT is the school's. Verdant's status slows
     (entangle) and is worth most where it is CONTINUOUS -- so the spell lands
     many small hits and the ultimate keeps the foe entangled without having
     to land anything (design, "why this cell").

{S1_SHOT_PARA}
     `dmg` {BLADE} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET: the design
     crosses near 16.5 on Chromium 141, and stage 5 settles it wide on 151. */
  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{BLADE}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ entangle:2 }},
{ULT_STUB}
    blurb:"{BLURB}" }},'''


def s1_edits():
    return [
("Briarwand joins the roster, its ultimate stubbed",
 '''

];
/* The single source of truth for "which status does this relic teach".''',
 relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".'''),
    ]


# ---------------------------------------------------------------- stage 2 --
S2_SHOT_PARA = '''     THE SPELL IS THORNBURST (design §1, §5): every 0.42s not one thorn but a
     FAN of three -- one along the facing and one either side at 0.28 rad --
     fast (440) and short-lived (life 1.2: they reach ~500 and stop), each 0.6
     of a blow, each that lands entangling 2. `fan`/`spread` are the only new
     fields and `tickFire` reads them (the volley loop's shape); `spawnShot`
     is untouched but for a `quiet` flag, so every other caller is the same
     call it always was. The first fan priced (0.45, life 0.8) was WORSE than
     the bow (design §3): this is the second, and it is the bow's equal.
'''


def s2_edits(dmg: str):
    b = BODY
    return [
("the relic's note says what it looses now", S1_SHOT_PARA, S2_SHOT_PARA),

("Briarwand looses the thorns",
 f'''  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Briarwand", aff:"verdant", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{dmg}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SPELL)}'''),

("tickFire looses a staff's fan",
 '''      f.ultNet.fired++;
      if (--f.ultNet.left <= 0) f.ultNet = null;
      return;
    }
    this.spawnShot(f);
  }
''',
 '''      f.ultNet.fired++;
      if (--f.ultNet.left <= 0) f.ultNet = null;
      return;
    }
    /* A STAFF'S FAN (v93, Briarwand's Thornburst): `fan` shots every cadence,
       the middle one along the facing and the rest at -spread, +spread,
       -2 spread ... in that order -- the lab's order (`overlays/staff_verdant.js`
       looses the middle thorn first). ONE loose voice a fan: the side shots are
       `quiet`, because three transients on one frame are one louder click
       (Thornshear's leaf volley found it first). Undefined `fan` on every other
       relic, so this is a comparison against undefined and falls through. */
    if (S.fan > 1){
      this.spawnShot(f);
      for (let k = 1; k < S.fan; k++)
        this.spawnShot(f, f.theta + S.spread * Math.ceil(k / 2) * (k % 2 ? -1 : 1), true);
      return;
    }
    this.spawnShot(f);
  }
'''),

("spawnShot takes a quiet flag",
 '''  spawnShot(f, angle){
''',
 '''  spawnShot(f, angle, quiet){
'''),

("  ...and a quiet shot makes no release sound",
 '''    SFX.play("loose", { bal: !!f.ultBal, spell: S.spell });
''',
 '''    if (!quiet) SFX.play("loose", { bal: !!f.ultBal, spell: S.spell });
'''),
    ]


# ---------------------------------------------------------------- stage 3 --
ULT_NOTE = '''    /* BLOOM (design §1, §5). A cloud of pollen leaves the staff (`cloudR`) and
       drifts after the foe at `drift` px/s for `dur` seconds; a foe inside it
       is bitten for `bite` and entangled +`stk` every `every` seconds. The
       DRIFT IS THE MECHANIC: a cloud that stays where it was cast holds the foe
       28% of the window against 57% and prices at +0 (design §3). The foe at
       ~3.7 of 4 entangle on the average window frame is the payload; the bite
       is the visible part of it.

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK: the lab's charge
       counts hit-stop freezes and the engine's does not (the batch's ruling,
       "use the game's equivalent"), measured for this fighter in
       `06-docs/v93/briarwand-build-v93.md`. Nothing waits. */
'''


def s3_edits(U: dict):
    return [
("Bloom is live", ULT_STUB, ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the fighter carries Bloom's cloud",
 '''    this.ironfallFade = 0;
''',
 '''    this.ironfallFade = 0;
    /* {t, dur, x, y, next, bitten} while BLOOM's cloud is out (v93). NOT
       `ultBloom`, which is the Thicket's. null on every other relic and on this
       one outside its window: `tickPollen` returns after a two-iteration loop
       that does nothing. `pollenTally` is the probe's count; nothing in the
       simulation reads it. */
    this.ultPollen = null;
    this.pollenTally = null;
'''),

("the cast lets the cloud go and resolves nothing",
 '''    if (u.kind === "ironfall"){
''',
 '''    if (u.kind === "bloom"){
      /* BLOOM (v93). NOTHING RESOLVES HERE: the cloud leaves the caster's
         centre and `tickPollen` does the rest. `next` 0 makes the first bite
         free, as the lab's was (`nextTick = t` at its cast). `m.ultFx` carries
         the cast flash only (one slot: open item 25); the cloud is drawn off
         `f.ultPollen`. */
      f.ultPollen = { t: 0, dur: u.dur, x: f.x, y: f.y, next: 0, bitten: false };
      if (!f.pollenTally)
        f.pollenTally = { casts: 0, frames: 0, inFrames: 0, bites: 0, dealt: 0 };
      f.pollenTally.casts++;
      return;
    }
    if (u.kind === "ironfall"){
'''),

("the cloud drifts with the window tickers",
 '''    this.tickIronfall(dt);
''',
 '''    this.tickIronfall(dt);
    this.tickPollen(dt);                // BLOOM (v93): the cloud drifts and bites
'''),

("tickPollen drifts the cloud and bites",
 '''  /* ================================================== IRONFALL ========''',
 '''  /* ===================================================== BLOOM ========
     v93 §5, and the lab (`overlays/staff_verdant.js`) where the prose is
     silent. The cloud starts on the caster's centre and each step moves toward
     the foe by min(distance, drift * dt). It is CLAMPED TO THE INSET (§5:
     "walls do not stop it (it is clamped to the inset)"); the lab needed no
     clamp, because a cloud moving along the line to a foe inside the hall
     stays inside it -- except when the hall closes behind a lagging cloud.

     INSIDE is |foe - cloud| < cloudR + R. Every `every` seconds while the foe
     is inside -- the cooldown runs from the last bite, and the first bite of a
     cast is free -- the foe takes `bite` through `hurt` (ward first; no crit,
     no knock, no hit stop: "the bite is a tick") and `stk` entangle, its
     source a side letter (Fighter.apply's contract).

     BEATS (brief §1, rule 3). `hurt` is invisible to the director, so the
     FIRST bite of each cast files one `hit` beat, and a bite that KILLS files
     its own fatal one -- the engine's rule for every side-channel kill.

     THE CLOCK is the window tickers' and stops through a hit stop; the lab's
     counted every step, freezes included (the difference the charge carries).
     The cloud and its bite timer therefore hold still through a freeze, with
     the rest of the hall. */
  tickPollen(dt){
    for (const f of [this.a, this.b]){
      const P = f.ultPollen;
      if (!P) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultPollen = null; continue; }
      P.t += dt;
      if (P.t >= P.dur){ f.ultPollen = null; continue; }
      const u = f.w.ult, R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset;
      const dx = foe.x - P.x, dy = foe.y - P.y, l = Math.hypot(dx, dy) || 1;
      const st = Math.min(l, u.drift * dt);
      P.x = clamp(P.x + dx / l * st, n, A.w - n);
      P.y = clamp(P.y + dy / l * st, n, A.h - n);
      const T = f.pollenTally;
      T.frames++;
      if (Math.hypot(foe.x - P.x, foe.y - P.y) >= u.cloudR + R) continue;
      T.inFrames++;
      if (P.t < P.next) continue;
      P.next = P.t + u.every;
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      this.hurt(foe, u.bite, f);
      foe.apply("entangle", u.stk, f === this.a ? "a" : "b");
      T.bites++; T.dealt += before - (foe.hp + foe.shield);
      const fatal = wasUp && foe.hp <= 0;
      if (fatal || !P.bitten)
        this.beat({ kind: "hit", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y,
                    dmg: u.bite, crit: false, fatal,
                    hpAfter: Math.max(0, foe.hp), hpFrac: Math.max(0, foe.hp) / foe.maxHp,
                    maxHp: foe.maxHp, selfHpFrac: f.hp / f.maxHp,
                    spd: f.speed, foeSpd: foe.speed,
                    close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy), bloom: true });
      P.bitten = true;
    }
  }

  /* ================================================== IRONFALL ========'''),

("the thorn and the cloud are drawn (first cuts)",
 '''      if (s.spell === "slug"){
''',
 '''      /* BRIARWAND'S THORN (v93 §6.1) -- FIRST CUT, for stage 3's film; the
         picture is stage 6's. "Three slim thorns (r 16, drawn long and narrow)
         fanning from the bud -- the fan IS the picture; at 1.2s they drop and
         fade." A thorn is drawn along its own heading, sinks and fades over its
         last quarter second, and borrows nothing from the arrow's streak.
         Derived from the shot's own state; no rng. */
      if (s.spell === "thornburst"){
        const fade = clamp(s.life / 0.25, 0, 1);
        const drop = (1 - fade) * 10;
        const L = s.r * 1.9, W = s.r * 0.26;
        c.save();
        c.translate(s.x, s.y + drop); c.rotate(s.a);
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = fade;
        c.fillStyle = SHAPES._ink(s.aff.dark, 9.7);
        c.beginPath(); c.moveTo(L * 1.08, 0); c.lineTo(-L * 0.62, -W * 1.35); c.lineTo(-L * 0.62, W * 1.35); c.closePath(); c.fill();
        c.fillStyle = s.aff.core;
        c.beginPath(); c.moveTo(L, 0); c.lineTo(-L * 0.55, -W); c.lineTo(-L * 0.55, W); c.closePath(); c.fill();
        c.strokeStyle = s.aff.glow; c.lineWidth = 1;
        c.beginPath(); c.moveTo(-L * 0.5, 0); c.lineTo(L * 0.85, 0); c.stroke();
        c.restore();
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 1;
        continue;
      }
      if (s.spell === "slug"){
'''),

("drawPollen: the cloud (first cut)",
 '''  drawShots(m){
''',
 '''  /* BLOOM'S CLOUD (v93 §6.1) -- FIRST CUT, for stage 3's film. "A soft disc
     r 110, verdant glow at alpha 0.22 with a brighter drifting inner texture
     (12 slow motes circling inside it), and it visibly leaves the caster and
     goes after the foe." Off `f.ultPollen` (the fighter's, never `m.ultFx`).
     No rng: the motes are `shellHash` and the window's own clock. */
  drawPollen(m){
    const c = this.ctx;
    for (const f of [m.a, m.b]){
      const P = f.ultPollen;
      if (!P) continue;
      const r = f.w.ult.cloudR, pal = f.aff;
      c.save();
      c.globalCompositeOperation = "lighter";
      const g = c.createRadialGradient(P.x, P.y, r * 0.15, P.x, P.y, r);
      g.addColorStop(0, pal.glow + "4D"); g.addColorStop(0.7, pal.core + "33"); g.addColorStop(1, pal.core + "00");
      c.fillStyle = g;
      c.beginPath(); c.arc(P.x, P.y, r, 0, TAU); c.fill();
      for (let i = 0; i < 12; i++){
        const a = TAU * shellHash(9701, i) + P.t * (0.35 + 0.3 * shellHash(9703, i)) * (i % 2 ? 1 : -1);
        const rr = r * (0.25 + 0.6 * shellHash(9705, i));
        c.globalAlpha = 0.55;
        c.fillStyle = i % 3 ? pal.glow : "#FFF7C8";
        c.beginPath(); c.arc(P.x + Math.cos(a) * rr, P.y + Math.sin(a) * rr, 2.6, 0, TAU); c.fill();
      }
      c.restore();
    }
  }

  drawShots(m){
'''),

("drawPollen is drawn with the shots",
 '''    this.drawIronfall(m);        // IRONFALL on the staff (v96 §6.1)
''',
 '''    this.drawIronfall(m);        // IRONFALL on the staff (v96 §6.1)
    this.drawPollen(m);          // BLOOM's cloud (v93 §6.1)
'''),
    ]


def stage_of(code: str) -> int:
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        return 3
    return 2 if "fan:3" in ent else 1


def all_stages():
    return [("1", s1_edits()), ("2", s2_edits(fnum(BLADE))), ("3", s3_edits(dict(ULT)))]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3"])
    ap.add_argument("--src")
    ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP")
    A = ap.parse_args()
    if A.audit:
        print(f"\nBRIARWAND / BLOOM -- the insert audit against {A.audit}")
        return audit(all_stages(), (HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    src_p, out_p = paths(A.src, A.out)
    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nBRIARWAND / BLOOM -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    code = strip_comments(s0)
    if 'id:"culverin"' not in code or "drawIronfall(m){" not in code:
        raise SystemExit("wrong base: no Culverin stage 6 -- build on the staff branch's tip")
    print("  base  the staff branch, Culverin stages 1-6 in it")
    have = stage_of(code)
    if have != stage - 1:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built on stage {stage - 1}")
    if stage == 1:
        check_bow_body(code)
        edits = s1_edits()
    elif stage == 2:
        dmg = re.search(r"dmg:([\d.]+),", relic_entry(code, RELIC)).group(1)
        edits = s2_edits(dmg)
    else:
        edits = s3_edits(dict(ULT))
    for label, old, new in edits:
        s = one(s, old, new, label)
    out = strip_comments(s)
    shot = SPELL if stage >= 2 else BOW_SHOT
    ent = check_entry(out, RELIC, shot, BLADE, stubbed=(stage <= 2))
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    if stage >= 3:
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        if blk.strip() != strip_comments(ult_live(ULT)).strip():
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not this run's:\n  {blk}")
        for need in ("tickPollen(dt){", "this.tickPollen(dt);", 'u.kind === "bloom"', "drawPollen(m){"):
            if out.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        if 'kind:"bloom"' in out and out.count('kind:"bloom"') != 1:
            raise SystemExit("REFUSING TO WRITE -- more than one bloom ultimate")
        if "ultPollen" not in out:
            raise SystemExit("REFUSING TO WRITE -- no ultPollen")
        print("  ok    ult   " + ", ".join(f"{k} {ULT[k]}" for k in ULT_KEYS))
    if stage >= 2 and out.count("if (S.fan > 1){") != 1:
        raise SystemExit("REFUSING TO WRITE -- the fan loop is not there exactly once")
    check_no_rng(edits)
    if out.count('shape:"staff"') != 2:
        raise SystemExit("REFUSING TO WRITE -- expected exactly two staves in the roster")
    print(f"  ok    relic  shape staff, the bow's body, "
          f"{'the thorns' if stage >= 2 else 'the bow arrow'}, "
          f"{'ultimate live' if stage >= 3 else 'ultimate stubbed'}; card {len(CARD)} chars")
    print("  ok    two staves in the roster; no insert draws the RNG")
    write_link(src_p, out_p, s0, s, BUILDER, stage)
    print("\n  GATE -- in this order, and each can fail:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids <the 35> --n 10")
    print(f"    python briarwand_probe.py --game {A.out}")
    print(f"    python verify.py --game {A.out} --n 40")
    return 0


if __name__ == "__main__":
    sys.exit(main())
