#!/usr/bin/env python
"""CULVERIN / IRONFALL -- the dwarven staff, and the staff TYPE with it. v96.

Built from `06-docs/v96/CULVERIN-BUILD-BRIEF.md` and
`dwarven-staff-design-v96.md` (Cowork, 2026-09-27), the row's
`06-docs/v89/STAFF-ROW-v89.md` §1/§6, and the art's `staff-art-v89.md` with
`staff_spec.js` beside it. Those are the input and the only input. CLAUDE.md
§3 rule 0: nothing here is a design decision. Rick, 2026-09-27, on yert:
"staff is in the repo. lets build it" -- the row accepted whole.

    stage 1   the relic, its ultimate STUBBED, shape "staff"   sc-leaf -> sc-culverin
    stage 2   the spell: SLUG                                  sc-culverin -> sc-slug
    stage 3   the ultimate: IRONFALL                           sc-slug -> sc-ironfall
    stage 5   the blade, wide on 151: 13 -> 13.5               sc-ironfall -> sc-ironfall-blade
    stage 6   picture, voice, drawn embers                     sc-ironfall-blade -> sc-ironfall-fx

THE TYPE IS THIS BUILD'S TOO. v89's handoff: "`shape:"staff"` is seven heads on
one rod, and the rod is the first build's." So stage 1 pastes Cowork's concept
spec as `SHAPES.staff` -- all three candidate heads a school, because Rick's
seven letters are still owed and they swap in by editing `STAFF.pick` -- and
sizes `weaponGlow`'s sprite for a weapon 1.7 sim reaches long.

THE BASE is `sc-leaf.html`, the build of record and exactly what the row was
priced on. The design batch is building a second line off the same link on
DESKTOP-DERRAFT (sc-leaf -> ... -> sc-dawn); every anchor here is chosen to
hold on that line too, so the two meet by re-running this builder with
`--src` on its tip. The builder accepts either line and says which it is on.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent
PROTECTED = "sundered-crown.html"
SPEC = REPO / "06-docs" / "v89" / "staff_spec.js"

RELIC = "culverin"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9).
# The bow's physics, which v89 §1 makes the staff's exactly. Asserted against
# Ironhail in the source before anything is written.
BODY = dict(blades="[0]", reach=54, width=9, artW=44, spin=2.8, mode='"ranged"', mass=1.6)
# Brief §2, stage 1: "stubbed relic at 13". A bracket; stage 5 settles it.
BLADE = 13
# STAGE 5 -- THE BLADE, MEASURED WIDE ON 151 (brief §2 stage 5), on
# sc-ironfall at charge 14: both sides of every pairing, two seed blocks
# (2207, 5003), 2040 fights a point, all 34 foes, no bisection (v48/v56/v66):
#     13.0 45.7% (44.8 / 46.7)     13.5  49.4% (48.6 / 50.1)
#     13.25 47.9% (47.7 / 48.0)    13.75 51.3% (53.2 / 49.3)
# 13.5 is the measured row nearest 50% whose blocks agree; 13.75's came back
# 3.9 points apart, a swing larger than the difference being decided. The
# honest precision is the interval 13.5-13.75. PROVISIONAL BY DESIGN: v89 §8.2
# re-prices the row against all seven staves before any blade is settled.
TUNED_BLADE = 13.5
# Stage 1 fires the BOW's arrow -- arm A, the dwarven bow body at the staff's
# blade. Copied off Ironhail and asserted.
BOW_SHOT = dict(cadence=0.34, speed=380, r=24, life=3.4, grav=0, dmgMul=1.0,
                tip="Fires along its facing · shots can be clanked")
# Design §6. Cowork's, accepted with the row.
CARD = "Lobs shells that fall on where the foe will be, bursting and sundering"
ULT_NAME = "Ironfall"
ULT_KIND = "ironfall"
BLURB = ("An iron staff that throws its weight. Every slug it lobs comes down, "
         "and for eight seconds so do the shells.")
# Stage 2 -- THE SPELL, design §1 and §5 and brief §0. Every field is one
# `spawnShot` already copies; no new engine. The tip is design §6's.
SLUG = dict(cadence=0.55, speed=470, r=28, life=3.0, grav=700, dmgMul=1.6,
            tip="Lobs a heavy slug that falls · clankable")


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse."""
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def strip_comments(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will (CLAUDE.md 4.11)."""
    import shutil, subprocess, tempfile
    node = shutil.which("node")
    if not node:
        raise SystemExit("no `node` on PATH -- refusing to write an unchecked build")
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not "
                                 "parse.\n  "
                                 + "\n  ".join((r.stderr or "").strip()
                                               .splitlines()[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


def relic_entry(code: str, rid: str) -> str:
    """The WEAPONS entry for `rid`, comments stripped, up to its blurb."""
    m = re.search(r'\{ id:"' + rid + r'"[\s\S]*?blurb:"[^"]*" \}', code)
    if not m:
        raise SystemExit(f"no WEAPONS entry for {rid!r}")
    return m.group(0)


def fnum(v) -> str:
    return repr(v) if isinstance(v, float) else str(v)


def shot_js(S: dict) -> str:
    keys = [k for k in S if k != "tip"]
    return ("shot:{ " + ", ".join(f"{k}:{fnum(S[k])}" for k in keys)
            + f',\n           tip:"{S["tip"]}" }},')


# ------------------------------------------------------------------ the art --

def staff_code() -> tuple[str, str]:
    """Cowork's spec from `const STAFF = {` to its close, byte for byte, and
    its sha. The spec's own file header describes CUT 2 (the pole through the
    ball) and is not pasted; the build carries its own, below."""
    txt = SPEC.read_text(encoding="utf-8")
    i = txt.index("const STAFF = {")
    body = txt[i:].rstrip() + "\n"
    if not body.rstrip().endswith("};"):
        raise SystemExit("staff_spec.js does not end on the STAFF object's close")
    for k in ("bloodsworn", "umbral", "vigil", "verdant", "runic", "sanctified", "dwarven"):
        if f"{k}(c, L, W, p, v)" not in body:
            raise SystemExit(f"staff_spec.js has no head for {k}")
    return body, hashlib.sha256(txt.encode()).hexdigest()[:16]


STAFF_HEADER = '''/* ------------------------------------------------------------------ STAFF --
   THE STAFF ROW'S ART (v89), pasted from Cowork's concept spec
   `06-docs/v89/staff_spec.js` (sha256 %SPEC_SHA%) by culverin_build.py. Cut 3,
   from Rick's references: a LONG staff out ONE side of the ball -- the pole
   from the ball's edge to 1.2 sim reaches, the head at 1.6-1.9 -- a thin
   gnarled pole, and a big head that HOLDS the school's light, which is where
   the spell leaves from. What separates it from a sceptre and a wand (Rick
   expects both to become types) is written once in `staff-art-v89.md`.

   THREE CANDIDATE HEADS A SCHOOL ARE STILL IN HERE, AND THAT IS DELIBERATE.
   Rick picks one letter a school; until he has, `pick` is the spec's own
   default and the losers are NOT deleted, so his letters land by editing
   `pick` and nothing else. All of it is render code: `drawWeapon`,
   `litWeapon`, `weaponGlow` and the scrunch card call it and nothing in the
   simulation reads a pixel of it -- `engine_ab` is the proof on every link
   that carries it.

   EVERYTHING FROM `const STAFF` TO ITS CLOSE IS THE SPEC, BYTE FOR BYTE, so
   the paint gate -- the build's own `SHAPES.staff` against the spec injected
   over the same page, pixel for pixel -- is a gate on the paste and not on
   anybody's taste. */
'''

# ---------------------------------------------------------------- stage 1 --

def relic_block() -> str:
    b = BODY
    return f'''

  /* CULVERIN -- THE DWARVEN STAFF, and the staff row's first relic. Built from
     `06-docs/v96/` (Cowork's design; the row accepted by Rick on 2026-09-27).

     A STAFF IS A BOW THAT CASTS (v89 §1). Every physical stat is the bow's,
     copied off Ironhail -- `blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]},
     spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]}` -- so the ONE thing the staff row changes
     is the projectile, and `culverin_build` asserts the copy against the
     shipped bow before it writes rather than trusting this comment.
     `mode:"ranged"` already looses `f.w.shot` along the facing on its
     cadence; nothing about how a shot is spawned, moved or landed changes.
     What a staff changes is what the shot IS, and on a staff that is the
     SCHOOL's: seven shot blocks where the bow row shares one.

     STAGE 1 LOOSES THE BOW'S ARROW. That is arm A of design §3.1 -- the
     dwarven BOW body at the staff's blade -- and it is what stage 2's slug is
     measured against when it replaces it.

     `dmg` {BLADE} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET, NOT A TUNE. The
     design crosses near 13.2 on Chromium 141; stage 5 settles it wide on
     151, both sides, two blocks, never by bisection (v48/v56/v66).

     THE PICTURE IS LONGER THAN THE HIT BOX, AND THAT IS OPEN, NOT DECIDED.
     `SHAPES.staff` draws the head at 1.6-1.9 sim reaches and the melee
     segment the engine tests is the bow's 54. Whether the type's reach should
     grow to meet the picture is Rick's (`staff-art-v89.md` open item 2; it
     re-prices all seven), and this is built at the 54 the row was priced
     at. */
  {{ id:"{RELIC}", name:"Culverin", aff:"dwarven", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{BLADE}, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}
    onHit:{{ sunder:1 }},
    /* IRONFALL. STUBBED AT `charge:1e9` IN STAGE 1 -- the "OFF" every stubbed
       relic since v55b has used: the clock never reaches it, `fireUlt` never
       runs, and the relic is measured as a blade, a shot and a channel.
       `kind:"{ULT_KIND}"` is its own (v89 §6: seven kinds, one a staff). The
       card is Cowork's (design §6) and in at stage 1, so `tip_audit` measures
       the real line. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},
    blurb:"{BLURB}" }},'''


def s1_edits(spec_body: str, spec_sha: str):
    return [

("the STAFF object, before SHAPES",
 '''const SHAPES = {
''',
 STAFF_HEADER.replace("%SPEC_SHA%", spec_sha) + spec_body + '''
const SHAPES = {
'''),

("SHAPES.staff dispatches to it",
 '''      c.globalAlpha = 1;
    }
  },

  greatsword(c, L, W, p, k, aff){
''',
 '''      c.globalAlpha = 1;
    }
  },

  /* THE STAFF (v89). The whole of it is `STAFF`, above SHAPES, because it is
     Cowork's spec pasted whole: its own helpers (the pole, the orb, the claw)
     and three candidate heads a school. `k` is the bow's DRAW and a staff has
     no string, so it is accepted and not read. */
  staff(c, L, W, p, k){ return STAFF.staff(c, L, W, p, k); },

  greatsword(c, L, W, p, k, aff){
'''),

("weaponGlow sizes its sprite for the shape's own length",
 '''const _glowCache = new Map();
function weaponGlow(shape, L, W, pal, k, blur){
''',
 '''/* HOW FAR A SHAPE DRAWS PAST ITS OWN L, where that is not the 1.15 this
   sprite has always assumed. The staff (v89) puts its head at 1.6-1.9 L --
   `staff_art_lab` reads each candidate off the alpha channel -- so a sprite
   sized at 1.15 L cut the staff's glow off in a straight line across the
   head. The concept sheet could not show it: the lab draws through
   `litWeapon` alone, and this glow is `drawWeapon`'s. 2.0 clears the longest
   candidate (1.86) and the blur's own pad covers the rest. Every other shape
   reads the 1.15 it always has, so its sprite is byte-identical. */
const GLOW_EXT = { staff: 2.0 };
const _glowCache = new Map();
function weaponGlow(shape, L, W, pal, k, blur){
'''),

("  ...and reads it",
 '''  const w = Math.ceil(L * 1.15) + PAD * 2, h = Math.ceil(W * 3) + PAD * 2;
''',
 '''  const ext = GLOW_EXT[shape] === undefined ? 1.15 : GLOW_EXT[shape];
  const w = Math.ceil(L * ext) + PAD * 2, h = Math.ceil(W * 3) + PAD * 2;
'''),

("Culverin joins the roster, its ultimate stubbed",
 '''

];
/* The single source of truth for "which status does this relic teach".''',
 relic_block() + '''

];
/* The single source of truth for "which status does this relic teach".'''),

    ]


# ---------------------------------------------------------------- stage 2 --

S1_SHOT_PARA = '''     STAGE 1 LOOSES THE BOW'S ARROW. That is arm A of design §3.1 -- the
     dwarven BOW body at the staff's blade -- and it is what stage 2's slug is
     measured against when it replaces it.
'''

S2_SHOT_PARA = '''     THE SPELL IS SLUG (design §1, §5): an iron slug lobbed along the facing
     every 0.55s -- fast off the staff at 470 but heavy, so it FALLS at 700
     px/s/s -- big (r 28), and it hits for 1.6 of a blow. EVERY FIELD IS ONE
     `spawnShot` ALREADY COPIES AND `tickShots` ALREADY READS: `grav` is
     integrated as `s.vy += s.grav * dt` on every live shot, `dmgMul` rides
     into `resolveHit`. So the only basic attack in the game with gravity
     needed no engine at all (v89 §6: "five of the seven spells are these
     fields set at spawn"). A slug loosed downward meets the floor and is
     spent; one loosed upward arcs. Clankable, as every shot is.

     THE SLUG IS THE BOW'S EQUAL AND THAT IS THE DESIGN (§3): about 14 blows
     a fight at 1.6 where the arrow lands 17 at 1.0 -- the same relic,
     heavier and rarer, and every landing a blow the viewer feels. The lab
     swapped the shot block in after the Match was made, which moves
     nothing it measured: it ran the relic as side A, whose `fireCd` starts
     at 0 whatever the cadence. As side B the first slug comes half a
     cadence in, 0.275s, where the lab's arrow would have come at 0.17.
'''


def s2_edits():
    b = BODY
    return [

("the relic's note says what it looses now",
 S1_SHOT_PARA, S2_SHOT_PARA),

("Culverin looses the slug",
 f'''  {{ id:"{RELIC}", name:"Culverin", aff:"dwarven", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:%DMG%, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(BOW_SHOT)}''',
 f'''  {{ id:"{RELIC}", name:"Culverin", aff:"dwarven", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:%DMG%, spin:{b["spin"]}, mode:"ranged", mass:{b["mass"]},
    {shot_js(SLUG)}'''),

    ]


# ---------------------------------------------------------------- stage 3 --

# IRONFALL -- design §1, §5 and brief §0. `charge` is the one number that is
# not the design's as written: the lab's 16 on its own step clock, which counts
# hit-stop freezes, converted to the engine's clock, which does not (the design
# batch's ruling, Rick 2026-09-27: "use the game's equivalent"; the staff row
# was priced on the same harness). Measured for this fighter in the build doc.
ULT = {"charge": 14, "dur": 8, "every": 1.0, "T": 0.85, "g": 1000,
       "shellR": 26, "shellMul": 1.3, "popDmg": 8, "popR": 90}
ULT_KEYS = ["charge", "dur", "every", "T", "g", "shellR", "shellMul", "popDmg", "popR"]


def ult_live(U: dict) -> str:
    return (f'''    ult:{{ name:"{ULT_NAME}", charge:{fnum(U["charge"])}, kind:"{ULT_KIND}", dur:{fnum(U["dur"])}, every:{fnum(U["every"])},
          T:{fnum(U["T"])}, g:{fnum(U["g"])}, shellR:{fnum(U["shellR"])}, shellMul:{fnum(U["shellMul"])}, popDmg:{fnum(U["popDmg"])}, popR:{fnum(U["popR"])},
          tip:"{CARD}" }},''')


ULT_STUB = f'''    /* IRONFALL. STUBBED AT `charge:1e9` IN STAGE 1 -- the "OFF" every stubbed
       relic since v55b has used: the clock never reaches it, `fireUlt` never
       runs, and the relic is measured as a blade, a shot and a channel.
       `kind:"{ULT_KIND}"` is its own (v89 §6: seven kinds, one a staff). The
       card is Cowork's (design §6) and in at stage 1, so `tip_audit` measures
       the real line. */
    ult:{{ name:"{ULT_NAME}", charge:1e9, kind:"{ULT_KIND}",
          tip:"{CARD}" }},'''

ULT_NOTE = '''    /* IRONFALL (design §1, §5). For `dur` seconds the staff also looses a
       SHELL every `every` seconds, lobbed high to come down where the foe will
       be `T` seconds later: `target = foe + v_foe*T`, `v = (target -
       caster)/T - (0, g*T/2)`, from the caster's centre, falling at `g`. A
       shell that strikes the foe in flight hits for `shellMul` of a blow; one
       that reaches its mark BURSTS -- the engine's own shard pop, Ironbloom's
       path unchanged: `popDmg` absolute to anything inside `popR`, through
       `resolveHit`, sundering. Clankable, and a wall kills it.

       THE LEAD IS KEPT BECAUSE IT IS WORSE. Aimed at where the foe IS, the
       same relic reads 89% (design §3); a shell every 0.7s reads 72% at blade
       14. Brief §3: do not "fix" either. And the burst prices at +0 -- a shell
       that reaches its mark has usually missed -- and is kept for the picture:
       the shell comes down and bursts on the stone.

       CHARGE %CHARGE% IS THE LAB'S 16 IN THE GAME'S CLOCK. The design priced 16
       seconds of the lab's step clock, which counts hit-stop freezes; the
       engine charges only in unfrozen time. The design batch's ruling (Rick,
       2026-09-27: "use the game's equivalent"), measured for this fighter in
       `06-docs/v96/culverin-build-v96.md`. Nothing waits: the charge rebuilds
       through the window, as the lab's did. */
'''


def s3_edits(U: dict):
    return [

("Ironfall is live",
 ULT_STUB,
 ULT_NOTE.replace("%CHARGE%", fnum(U["charge"])) + ult_live(U)),

("the slug says which spell it is",
 f'''dmgMul:{fnum(SLUG["dmgMul"])},
           tip:"{SLUG["tip"]}" }},''',
 f'''dmgMul:{fnum(SLUG["dmgMul"])}, spell:"slug",
           tip:"{SLUG["tip"]}" }},'''),

("spawnShot carries the spell's name onto the shot",
 '''      seed: f.ultBloom ? (f.ultBloom.left--, true) : false,
      aff: f.aff, a,
    });
''',
 '''      seed: f.ultBloom ? (f.ultBloom.left--, true) : false,
      aff: f.aff, a,
    });
    /* A STAFF'S SPELL NAMES ITSELF (v89). On a staff the shot block is the
       SCHOOL's and seven of them look nothing alike, so `drawShots` needs to
       know which spell a shot is -- and a shot carries no handle on its
       relic. Set only when the block names one, so every shot any other
       relic looses is the same object it always was. Read by the renderer
       and nothing else. */
    if (S.spell) this.shots[this.shots.length - 1].spell = S.spell;
'''),

("the fighter carries Ironfall's window",
 '''    this.deadfallFade = 0;
''',
 '''    this.deadfallFade = 0;
    /* {t, dur, next} while IRONFALL's window is open (v96). null on every
       other relic and on this one outside its window, which is the
       zero-burden argument: `tickIronfall` returns after a two-iteration loop
       that does nothing. `ironTally` is the probe's count, cumulative over the
       fight; nothing in the simulation reads it. */
    this.ultIronfall = null;
    this.ironTally = null;
'''),

("the cast opens the window and resolves nothing",
 '''    /* An aimed shot does not resolve in this frame -- it starts a DRAW, and''',
 '''    if (u.kind === "ironfall"){
      /* IRONFALL (v96). NOTHING RESOLVES HERE: the cast opens the window and
         `tickIronfall` looses the shells. `next` starts at zero, so the first
         shell leaves on the cast's own step, as the lab's left on its cast
         frame. `m.ultFx` carries the cast's flash and field and nothing else
         (the life map's fallback): it is ONE SLOT, and the opponent casting
         anything erases it (open item 25). Nothing in this window needs it --
         the shells and their rings are SIM OBJECTS in `m.shots`. */
      f.ultIronfall = { t: 0, dur: u.dur, next: 0 };
      if (!f.ironTally) f.ironTally = { casts: 0, shells: 0, declined: 0 };
      f.ironTally.casts++;
      return;
    }

    /* An aimed shot does not resolve in this frame -- it starts a DRAW, and'''),

("Ironfall ticks with the window tickers",
 '''    this.tickWinnow(dt);
''',
 '''    this.tickWinnow(dt);
    /* IRONFALL (v96). With the window tickers and AFTER `tickShots`, so a
       shell loosed this step first moves on the next -- as the lab's did,
       pushed after its step. Its clock stops through a hit stop, as theirs do. */
    this.tickIronfall(dt);
'''),

("tickIronfall looses the shells",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== IRONFALL ========
     v96 §5, and the lab (`overlays/staff_dwarf.js`) where the prose is silent.
     Every `every` seconds of the window, while both are alive: a shell from
     the caster's CENTRE with the velocity that puts it on the foe's LEAD
     point `T` seconds out under `g`, carrying `life T` -- so the engine's own
     shard pop bursts it exactly at the mark, on the step its life runs out.
     Everything that happens to a shell after it leaves is `tickShots`, as for
     every other projectile: the parry, the hit at `shellMul`, the pop, the
     wall.

     DECLINED AT THE CEILING, NEVER SHIFTED. `spawnShot` makes room by shifting
     the oldest shot out; this path must not (the fork's reason: a shell is
     not worth somebody's arrow in flight). The lab tested `m.shots.length <
     maxLive` and did not advance `next`, so a declined shell leaves on the
     first step there is room -- built the same way.

     `tx, ty` IS THE MARK, kept on the shell for the probe, which asserts the
     velocity is the solved one. The renderer does not read it: the landing
     ring is a pure function of where the shell is, how fast it is going and
     how long it has left, so it follows the shell that is actually flying.

     THE CLOCK is the window tickers' and stops through a hit stop. The lab's
     counted every step, freezes included -- the same difference the charge
     carries, and the reason it is converted. */
  tickIronfall(dt){
    for (const f of [this.a, this.b]){
      const I = f.ultIronfall;
      if (!I) continue;
      const foe = f === this.a ? this.b : this.a;
      if (!f.alive || !foe.alive || this.over){ f.ultIronfall = null; continue; }
      I.t += dt;
      if (I.t >= I.dur){ f.ultIronfall = null; continue; }
      if (I.t < I.next) continue;
      if (this.shots.length >= CONFIG.shot.maxLive){ f.ironTally.declined++; continue; }
      const u = f.w.ult, T = u.T, g = u.g;
      I.next += u.every;
      const tx = foe.x + foe.vx * T, ty = foe.y + foe.vy * T;
      const vx = (tx - f.x) / T, vy = (ty - f.y) / T - 0.5 * g * T;
      this.shots.push({
        own: f === this.a ? "a" : "b",
        x: f.x, y: f.y, x0: f.x, y0: f.y, spd0: 0, t0: this.t,   // CINEMA (demo)
        vx, vy, r: u.shellR, life: T, max: T, grav: g, dmgMul: u.shellMul,
        seed: false, aff: f.aff, a: Math.atan2(vy, vx),
        shard: true, pop: u.popDmg, popR: u.popR,
        shell: true, tx, ty,
      });
      f.ironTally.shells++;
    }
  }

  tickWinnow(dt){
'''),

("the slug and the shell are drawn as what they are",
 '''      if (s.shard){
        const sp2 = Math.hypot(s.vx, s.vy) || 1;''',
 '''      /* CULVERIN'S SLUG AND SHELL (v96 §6.1) -- FIRST CUTS, for stage 3's
         film; the picture is stage 6's and Rick's (rule 2). They are the two
         projectiles in this game that FALL, so neither may borrow the arrow's
         streak, which says "straight line", and the shell must not reach the
         splinter's branch below: it carries `shard` so the engine's own pop
         bursts it, and without this it would draw as Ironbloom's shrapnel.
         Everything is DERIVED from the shot's own state -- no stored trail,
         no spawned mote, no `rng()` -- so it steps with the sim. */
      if (s.spell === "slug"){
        /* A dull iron ball: the size IS the hit box (r 28), the body is dark
           iron with one lit edge from above, and the only heat is a faint
           shimmer behind it. No trail -- it is heavy, not fast. */
        const sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        c.globalAlpha = 0.16;
        c.fillStyle = s.aff.glow;
        c.beginPath();
        c.ellipse(s.x - ux * s.r * 0.9, s.y - uy * s.r * 0.9, s.r * 1.15, s.r * 0.75,
                  Math.atan2(uy, ux), 0, TAU);
        c.fill();
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 1;
        const gi = c.createRadialGradient(s.x - s.r * 0.35, s.y - s.r * 0.4, s.r * 0.1,
                                          s.x, s.y, s.r);
        gi.addColorStop(0, "#6E6A66"); gi.addColorStop(0.55, "#34302C");
        gi.addColorStop(1, "#141210");
        c.fillStyle = gi;
        c.beginPath(); c.arc(s.x, s.y, s.r, 0, TAU); c.fill();
        c.strokeStyle = s.aff.core + "AA"; c.lineWidth = Math.max(1, s.r * 0.08);
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.96, -2.6, -0.5); c.stroke();
        c.globalCompositeOperation = "lighter";
        continue;
      }
      if (s.shell){
        /* THE MARK FIRST: where the shell will come down, for as long as it
           is in the air -- v75's rune, the viewer sees the landing before it
           lands. A PURE FUNCTION of the shell's state (ballistic, no drag),
           drawn at the burst's own radius, so the ring IS the hazard. */
        const L = Math.max(0, s.life);
        const mx = s.x + s.vx * L, my = s.y + s.vy * L + 0.5 * s.grav * L * L;
        const kk = 1 - clamp(s.life / s.max, 0, 1);
        c.globalAlpha = 0.25;
        c.strokeStyle = s.aff.glow; c.lineWidth = 3;
        c.beginPath(); c.arc(mx, my, s.popR, 0, TAU); c.stroke();
        c.globalAlpha = 0.10 + 0.25 * kk;
        c.beginPath(); c.arc(mx, my, s.popR * (1 - 0.75 * kk), 0, TAU); c.stroke();
        /* THE EMBER TRAIL: five sparks laid back along the velocity, derived
           from the shell's own position and speed, fading with distance. */
        const sp = Math.hypot(s.vx, s.vy) || 1, ux = s.vx / sp, uy = s.vy / sp;
        for (let i = 1; i <= 5; i++){
          c.globalAlpha = 0.55 * (1 - i / 6);
          c.fillStyle = i < 3 ? "#FFD27A" : s.aff.glow;
          c.beginPath();
          c.arc(s.x - ux * s.r * 0.75 * i, s.y - uy * s.r * 0.75 * i, s.r * (0.34 - 0.04 * i), 0, TAU);
          c.fill();
        }
        /* THE SHELL: iron, a hot seam, and a glow that swells as it falls. */
        const gh = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * 2.2);
        gh.addColorStop(0, s.aff.glow + "88"); gh.addColorStop(1, s.aff.glow + "00");
        c.globalAlpha = 0.5 + 0.4 * kk; c.fillStyle = gh;
        c.beginPath(); c.arc(s.x, s.y, s.r * 2.2, 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 1;
        const gi = c.createRadialGradient(s.x - s.r * 0.35, s.y - s.r * 0.4, s.r * 0.1,
                                          s.x, s.y, s.r);
        gi.addColorStop(0, "#5C5652"); gi.addColorStop(1, "#16120E");
        c.fillStyle = gi;
        c.beginPath(); c.arc(s.x, s.y, s.r, 0, TAU); c.fill();
        c.strokeStyle = "#FFB347"; c.lineWidth = Math.max(1, s.r * 0.12);
        c.beginPath(); c.arc(s.x, s.y, s.r * 0.62, 0, TAU); c.stroke();
        c.globalCompositeOperation = "lighter";
        continue;
      }
      if (s.shard){
        const sp2 = Math.hypot(s.vx, s.vy) || 1;'''),

    ]


# ---------------------------------------------------------------- stage 5 --

S1_BLADE_PARA = f'''     `dmg` {BLADE} IS THE BRIEF'S STAGE-1 NUMBER AND A BRACKET, NOT A TUNE. The
     design crosses near 13.2 on Chromium 141; stage 5 settles it wide on
     151, both sides, two blocks, never by bisection (v48/v56/v66).
'''

S5_BLADE_PARA = f'''     `dmg` {fnum(TUNED_BLADE)} IS MEASURED WIDE ON 151 (brief stage 5): both sides of
     every pairing, two seed blocks, 2040 fights a point, no bisection --
     13.0 reads 45.7%, 13.25 47.9%, 13.5 49.4%, 13.75 51.3%. 13.5 is the
     measured row nearest 50% whose two blocks agree (48.6 / 50.1); 13.75's
     came back 3.9 points apart. The honest precision is 13.5-13.75, and it
     is PROVISIONAL: v89 §8.2 re-prices the row against all seven staves
     before any blade is called settled. The numbers live in
     `culverin_build.TUNED_BLADE`, never here (CLAUDE.md §4.9).
'''


def s5_edits():
    b = BODY
    return [

("the relic's note says the blade is measured",
 S1_BLADE_PARA, S5_BLADE_PARA),

("Culverin's blade is the measured one",
 f'''  {{ id:"{RELIC}", name:"Culverin", aff:"dwarven", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(BLADE)}, spin:''',
 f'''  {{ id:"{RELIC}", name:"Culverin", aff:"dwarven", shape:"staff",
    blades:{b["blades"]}, reach:{b["reach"]}, width:{b["width"]}, artW:{b["artW"]}, dmg:{fnum(TUNED_BLADE)}, spin:'''),

    ]


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §6.1-6.2), picked on measurements under
# Rick's "you pick i overrule" (2026-09-27). PRESENTATION ONLY: every line
# below is a `SFX.play` (a no-op headless that reads nothing back), a
# `this.ring` (a presentation list), a render-only field on a shot or a
# fighter, or drawing code -- no rng, no spawnFx, no Math.random. `engine_ab`
# over all 35 relics, Culverin included, is the proof.
#
# THE VOICES are `culverin_voice_lab.py`'s picks, pasted verbatim (its
# `--shipped` check renders the built arms against these bodies sample for
# sample). The lab took four rounds and the rounds are in
# `06-docs/v96/runs/build/stage6_voice_lab_round*.txt`: level-matching, a
# crack that opens bright, the PHONE band (the deliverable is watched on phones,
# and the first thud picked was 57 dB down there), and a cast whose ratchet is
# audible by itself. `S.` in the lab is `this.` in the engine.
VOICES = {
 "thud": """
  S._burst(t, { freq: 300, q: 0.8, gain: 0.1126, dur: 0.12, type:"lowpass" });
  S._tone (t, { freq: 118, to: 58, gain: 0.08046, dur: 0.12, type:"triangle" });""",
 "crack": """
  S._burst(t, { freq: 2600, q: 0.8, gain: 0.06586, dur: 0.035, type:"highpass" });
  S._burst(t, { freq: 900, q: 1.2, gain: 0.03952, dur: 0.06, type:"bandpass" });
  S._tone (t + 0.012, { freq: 120, to: 60, gain: 0.03293, dur: 0.09, type:"sine" });""",
 "cast": """
  for (let i = 0; i < 7; i++){
    const d = i * 0.035, f = 1800 + i * 130;
    S._burst(t + d, { freq: f, q: 3.0, gain: 0.09691, dur: 0.012, type:"bandpass" });
    S._tone (t + d, { freq: f * 0.39, gain: 0.03173, dur: 0.020, type:"triangle" });
  }
  S._burst(t + 0.26, { freq: 700, q: 1.0, gain: 0.04407, dur: 0.06, type:"bandpass" });
  S._tone (t + 0.26, { freq: 58, to: 28, gain: 0.1763, dur: 0.38, type:"sine" });
  S._burst(t + 0.26, { freq: 220, q: 0.6, gain: 0.1058, dur: 0.28, type:"lowpass" });""",
 "shell": """
  S._burst(t, { freq: 200.23, q: 0.8, gain: 0.161, dur: 0.15, type:"lowpass" });
  S._tone (t, { freq: 78.76, to: 38.71, gain: 0.1151, dur: 0.15, type:"triangle" });""",
 "whistle": """
  const D = Math.max(0.12, Math.min(0.9, p.dur || 0.42));
  S._tone(t, { freq: 1900, to: 720, gain: 0.01991, dur: D, type:"sine" });""",
 "burst": """
  S._tone (t, { freq: 100, to: 36, gain: 0.20, dur: 0.90, type:"sine" });
  S._burst(t, { freq: 500, q: 0.8, gain: 0.18, dur: 0.45, type:"bandpass" });
  [0.07, 0.14, 0.22, 0.31, 0.40, 0.48, 0.55].forEach((d, i) =>
    S._burst(t + d, { freq: 1800, q: 3.0, gain: 0.050 - i * 0.005, dur: 0.040, type:"bandpass" }));""",
 "close": """
  const K = [[0.0, 1721.9], [0.035, 1635.2], [0.07, 1548.4], [0.105, 1461.6], [0.14, 1374.9], [0.175, 1288.1], [0.21, 1201.4]];
  for (const [d, f] of K){
    S._burst(t + d, { freq: f, q: 3.0, gain: 0.06784, dur: 0.012, type:"bandpass" });
    S._tone (t + d, { freq: f * 0.39, gain: 0.02221, dur: 0.020, type:"triangle" });
  }""",
}
VOICE_PICKS = {"thud": "CHUFF", "crack": "SPLIT2", "cast": "CRANK2", "shell": "FIFTH",
               "whistle": "SINE", "burst": "SHOT2", "close": "BACK"}


def arm(key: str, indent: str) -> str:
    """A picked body as engine code: `S.` -> `this.`, re-indented."""
    body = VOICES[key].strip("\n").replace("S._", "this._")
    return "\n".join(indent + l[2:] if l.startswith("  ") else indent + l for l in body.splitlines())


def s6_edits():
    return [

("the slug's release: its own voice in `loose`",
 '''        } else {
          this._burst(t, { freq: 380, q: 1.1, gain: 0.055, dur: 0.055, type:"bandpass" });
        }
''',
 '''        } else if (p.spell === "slug"){
          /* CULVERIN'S SLUG LEAVING -- design §6.2: "a deep short thud on
             leaving (a cannon at a distance) ... the heaviest basic-attack
             voice in the game, on purpose (it fires half as often as an
             arrow)." CHUFF, of three (`culverin_voice_lab.py`, Rick's "you
             pick i overrule"): a low noise body and a falling triangle, 75 ms,
             12 dB under the slug's own blow -- a shot leaving must still read
             quieter than one landing (the comment above) -- and 7 dB over the
             bow's release ON A PHONE, where the deeper two all but vanished. */
''' + arm("thud", "          ") + '''
        } else {
          this._burst(t, { freq: 380, q: 1.1, gain: 0.055, dur: 0.055, type:"bandpass" });
        }
'''),

("the slug's landing: `slug-land`, a stone crack",
 '''      else if (kind === "wall"){
''',
 '''      else if (kind === "slug-land"){
        /* CULVERIN'S SLUG ON STONE -- design §6.2: "a stone crack on landing".
           SPLIT2, of six over two rounds (`culverin_voice_lab.py`): a bright
           split first and the knock of the stone 12 ms behind it, 75 ms, 16 dB
           under the blow -- it plays about sixty times a fight. Round 1's three
           let the knock or a bare tick own the first 20 ms. */
''' + arm("crack", "        ") + '''
      }
      else if (kind === "wall"){
'''),

("Sfx: Ironfall's cast, shell, whistle, burst and close, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack
''',
 '''        } else if (w === "culverin"){                   // the ratchet, then the boom
          /* IRONFALL'S CAST -- design §6.2: "a mechanical ratchet into a low
             boom, 0.4s." CRANK2 (`culverin_voice_lab.py`, round 4): seven
             pawl clicks climbing 1.8-2.6 kHz, 35 ms apart, and the boom at 260
             ms with a 700 Hz report on it -- 465 ms, level with the blow, the
             ratchet ALONE within 12 dB of a hit on a phone. Culverin had no arm
             and fell through to rune-crack; this goes before that fallback and
             leaves it alone. */
''' + arm("cast", "          ") + '''
        } else if (w === "culverin-shell"){             // a shell leaves
          /* "The thud pitched down" -- the slug's own CHUFF a fifth down and
             1.25x as long, 8 dB under the blow: a bigger launch than a slug's.
             Played by tickIronfall for every shell loosed. */
''' + arm("shell", "          ") + '''
        } else if (w === "culverin-whistle"){           // and comes down
          /* "A whistle on the way down": a sine falling 1900 -> 720 Hz over
             `p.dur`, the flight the shell has LEFT when its vy turns down --
             tickIronfall passes it -- so the whistle ends where the shell
             lands. 18 dB under the blow. */
''' + arm("whistle", "          ") + '''
        } else if (w === "culverin-burst"){             // and bursts
          /* "The burst (a bass hit with a stone rattle)": SHOT2 (round 2 of
             the burst): a falling bass and a band of noise with a rattle of
             seven chips over half a second, 505 ms, 2 dB over the blow -- the
             rarest sound this relic makes (about one shell in fifteen reaches
             its mark), and neither Ironbloom's blast nor the nova by register.
             The shard pop was SILENT until now: Ironbloom's splinters never
             had a voice, and they still do not -- the pop plays this only for
             a `shell`. */
''' + arm("burst", "          ") + '''
        } else if (w === "culverin-close"){             // and the ratchet runs back
          /* CLOSE -- "the ratchet reversed": the cast's own seven clicks run
             last-first and a fifth down, at 0.7 of the cast's click level, no
             boom. Played when the window runs out by its clock, never on a
             death. */
''' + arm("close", "          ") + '''
        } else {                                        // rune-crack
'''),

("spawnShot: the slug's release names its spell to the voice",
 '''    SFX.play("loose", { bal: !!f.ultBal });
''',
 '''    /* `spell` picks a staff's own release voice (Culverin's thud). Undefined
       on every bow, which falls through to the string exactly as before. */
    SFX.play("loose", { bal: !!f.ultBal, spell: S.spell });
'''),

("spawnShot: a staff's shot remembers where it left, for its puff",
 '''    if (S.spell) this.shots[this.shots.length - 1].spell = S.spell;
''',
 '''    /* AND WHERE IT LEFT (`sx, sy`), for the puff `drawShots` draws there for
       a fifth of a second (design §6.1: "the slug leaves from the mouth with a
       puff of 6 dark motes"). Render-only, like `spell`. */
    if (S.spell){
      const s = this.shots[this.shots.length - 1];
      s.spell = S.spell; s.sx = s.x; s.sy = s.y;
    }
'''),

("tickShots: a slug on stone cracks and leaves a ring of dust",
 '''          this.spawnFx(s.x, s.y, s.aff.core, 4, 110, 0.26, 2.2);
        dead = true;
      }
''',
 '''          this.spawnFx(s.x, s.y, s.aff.core, 4, 110, 0.26, 2.2);
        /* CULVERIN'S SLUG ON STONE (design §6.1-6.2: "it hits stone with a
           heavy spawnFx and no bounce" and "a stone crack on landing"). The
           heavy part is a RING, not more motes: `spawnFx` draws the match rng,
           so a heavier spray would move every Culverin fight and void the
           blade. `life > 0` is the wall, not the (unreached) end of its life. */
        if (s.spell === "slug" && s.life > 0){
          SFX.play("slug-land");
          this.ring(s.x, s.y, "#8C7B66", 8, 46, 0.34, 5);
        }
        dead = true;
      }
'''),

("tickShots: a shell that reaches its mark bursts aloud",
 '''        this.shake = Math.min(38, this.shake + 5);
        dead = true;
      }
''',
 '''        this.shake = Math.min(38, this.shake + 5);
        /* IRONFALL'S BURST (design §6.2). Only a `shell`: Ironbloom's
           splinters pop through this same branch and have never had a voice. */
        if (s.shell) SFX.play("ult", { w: "culverin-burst" });
        dead = true;
      }
'''),

("the fighter carries Ironfall's fade",
 '''    this.ultIronfall = null;
    this.ironTally = null;
''',
 '''    this.ultIronfall = null;
    this.ironTally = null;
    /* AND ITS PICTURE'S CLOCK: 1 while the window is open, down over 0.4s
       after (design §6.1: "the mouth glows ... Close: the mouth dims"). On the
       FIGHTER, never on `m.ultFx` (one slot: open item 25). Driven in
       `tickIronfall`, drawn by `drawIronfall`, read by nothing in the sim. */
    this.ironfallFade = 0;
'''),

("tickIronfall: the whistle, on the step a shell turns down",
 '''  tickIronfall(dt){
    for (const f of [this.a, this.b]){
''',
 '''  tickIronfall(dt){
    /* THE WHISTLE (design §6.2: "a whistle on the way down"), once per shell,
       on the step its vy turns downward, lasting the flight it has left.
       Guarded on a Culverin having cast at all, so no other fight walks the
       shots. `whistled` is render-only. */
    if (this.a.ironTally || this.b.ironTally)
      for (const s of this.shots)
        if (s.shell && !s.whistled && s.vy >= 0){
          s.whistled = true;
          SFX.play("ult", { w: "culverin-whistle", dur: s.life });
        }
    for (const f of [this.a, this.b]){
'''),

("tickIronfall: the close, when the window runs out by its clock",
 '''      if (I.t >= I.dur){ f.ultIronfall = null; continue; }
''',
 '''      /* THE CLOSE (design §6.2: "the ratchet reversed"): by the clock only --
         the death and the end of the match were handled above. */
      if (I.t >= I.dur){ SFX.play("ult", { w: "culverin-close" }); f.ultIronfall = null; continue; }
'''),

("tickIronfall: each shell's launch, and the picture's clock",
 '''      f.ironTally.shells++;
    }
  }
''',
 '''      f.ironTally.shells++;
      SFX.play("ult", { w: "culverin-shell" });   // "the thud pitched down"
    }
    /* THE PICTURE'S CLOCK. Up instantly, down over 0.4s (Deadfall's shape).
       On the window tickers' path, so it holds through a hit stop. */
    for (const f of [this.a, this.b])
      f.ironfallFade = f.ultIronfall ? 1 : Math.max(0, f.ironfallFade - dt / 0.4);
  }
'''),

("drawShots: the slug's puff as it leaves",
 '''        c.beginPath(); c.arc(s.x, s.y, s.r * 0.96, -2.6, -0.5); c.stroke();
        c.globalCompositeOperation = "lighter";
        continue;
      }
      if (s.shell){
''',
 '''        c.beginPath(); c.arc(s.x, s.y, s.r * 0.96, -2.6, -0.5); c.stroke();
        /* THE PUFF (design §6.1: "the slug leaves from the mouth with a puff of
           6 dark motes"): six motes of smoke thrown out around where it left,
           over a fifth of a second of its own life, derived and not spawned. */
        const age = s.max - s.life;
        if (age < 0.22 && s.sx !== undefined){
          const k = age / 0.22;
          for (let i = 0; i < 6; i++){
            const a2 = s.a + (i - 2.5) * 0.62;
            const rr = 8 + 46 * k * (0.7 + 0.3 * shellHash(9601, i));
            c.globalAlpha = 0.55 * (1 - k);
            c.fillStyle = "#3A322B";
            c.beginPath();
            c.arc(s.sx + Math.cos(a2) * rr, s.sy + Math.sin(a2) * rr, 7 * (1 - 0.5 * k), 0, TAU);
            c.fill();
          }
          c.globalAlpha = 1;
        }
        c.globalCompositeOperation = "lighter";
        continue;
      }
      if (s.shell){
'''),

("drawShots: the shell's bigger puff at the launch",
 '''        c.beginPath(); c.arc(s.x, s.y, s.r * 0.62, 0, TAU); c.stroke();
        c.globalCompositeOperation = "lighter";
        continue;
      }
''',
 '''        c.beginPath(); c.arc(s.x, s.y, s.r * 0.62, 0, TAU); c.stroke();
        /* THE LAUNCH (design §6.1: "every shell leaves with a bigger puff"):
           ten motes of smoke and a flash where it left the caster, over 0.3s
           of its own life. Derived, not spawned. */
        const age = s.max - s.life;
        if (age < 0.3){
          const k = age / 0.3;
          c.globalAlpha = 0.6 * (1 - k);
          for (let i = 0; i < 10; i++){
            const a2 = i * TAU / 10 + shellHash(9611, i) * 0.5;
            const rr = 14 + 70 * k * (0.6 + 0.4 * shellHash(9613, i));
            c.fillStyle = "#3A322B";
            c.beginPath();
            c.arc(s.x0 + Math.cos(a2) * rr, s.y0 + Math.sin(a2) * rr, 11 * (1 - 0.5 * k), 0, TAU);
            c.fill();
          }
          c.globalAlpha = 1;
        }
        c.globalCompositeOperation = "lighter";
        if (age < 0.12){
          c.globalAlpha = 0.7 * (1 - age / 0.12);
          c.fillStyle = "#FFD27A";
          c.beginPath(); c.arc(s.x0, s.y0, 22 + 90 * age, 0, TAU); c.fill();
          c.globalAlpha = 1;
        }
        continue;
      }
'''),

("drawIronfall: the head glows and sheds embers while the window runs",
 '''  drawShots(m){
''',
 '''  /* IRONFALL ON THE STAFF (design §6.1): "Cast: the mouth glows ...
     Close: the mouth dims" and "Field: ember motes falling". DRAWN, not an
     fx.js field: the one `m.ultFx` slot is erased by the opponent's cast (open
     item 25), and `src/render/fx.js` is shared by both lines of the chain.
     Off the fighter's own fade, so it survives anything the opponent casts.

     THE HEAD is where Cowork's spec puts the dwarven light: the sphere in the
     jaws at 0.82 of the staff's drawn length (1.7x the sim's L), out from
     the ball's edge. Rick's pick for the head is still his to overrule; all
     three dwarven candidates hold their light within 0.77-0.82 of that
     length, so the glow sits on the light whichever he keeps.

     PRESENTATION ONLY: no rng, no spawnFx -- the embers are `shellHash` and
     the match clock, Zenith's construction (v98). */
  drawIronfall(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      const k = f.ironfallFade;
      if (!(k > 0.01) || !f.alive) continue;
      const reach = f.w.reach * m.actMods.reach * f.reachMul;
      const hd = R - 6 + (reach + 6) * 1.7 * 0.82;
      const hx = f.x + Math.cos(f.theta) * hd, hy = f.y + Math.sin(f.theta) * hd;
      const T = m.t;
      c.save();
      c.globalCompositeOperation = "lighter";
      const fl = 0.85 + 0.15 * Math.sin(T * 23) * Math.sin(T * 7.1);
      const g = c.createRadialGradient(hx, hy, 2, hx, hy, 34);
      g.addColorStop(0, f.aff.glow + "CC"); g.addColorStop(0.4, f.aff.core + "77");
      g.addColorStop(1, f.aff.core + "00");
      c.globalAlpha = 0.75 * k * fl;
      c.fillStyle = g;
      c.beginPath(); c.arc(hx, hy, 34, 0, TAU); c.fill();
      /* THE EMBERS: fourteen, shed off the head and FALLING (they are iron
         sparks, not Zenith's rising motes), cooling from gold to red. Drawn
         as SHORT STREAKS with a hot head: the first cut drew 2 px dots and
         the video's encoder smeared every one of them away -- a falling spark
         reads by its streak, and the streak lengthens as it falls. */
      c.lineCap = "round";
      for (let i = 0; i < 14; i++){
        const ph = (T * (0.9 + 0.5 * shellHash(9621, i)) + shellHash(9623, i)) % 1;
        const ox = (shellHash(9625, i) - 0.5) * 18, sway = Math.sin(T * 2.3 + i * 1.7) * 4;
        const ex = hx + ox + sway * ph + (shellHash(9627, i) - 0.5) * 22 * ph;
        const ey = hy + (shellHash(9629, i) - 0.5) * 10 + ph * ph * 84;
        const col = ph < 0.3 ? "#FFE3A0" : (ph < 0.65 ? "#FFA640" : "#C9551C");
        c.globalAlpha = 0.9 * k * (1 - ph);
        c.strokeStyle = col; c.lineWidth = 2.6 * (1 - 0.4 * ph);
        c.beginPath(); c.moveTo(ex, ey - 4 - 14 * ph); c.lineTo(ex, ey); c.stroke();
        c.fillStyle = col;
        c.beginPath(); c.arc(ex, ey, 3.2 * (1 - 0.45 * ph), 0, TAU); c.fill();
      }
      c.restore();
    }
  }

  drawShots(m){
'''),

("drawIronfall is drawn with the shots",
 '''    this.drawShots(m);
''',
 '''    this.drawShots(m);
    this.drawIronfall(m);        // IRONFALL on the staff (v96 §6.1)
'''),

("the staff's dwarven head: Code's pick under Rick's overrule",
 '''anybody's taste. */
const STAFF = {
''',
 '''anybody's taste. */
/* THE DWARVEN HEAD IS "A" -- Code's pick for Culverin under Rick's "you pick i
   overrule" (2026-09-27): the brass jaws holding a dark iron sphere with an
   ember in it, because the staff whose spell is an iron slug then holds one in
   its head. B and C stay until he has seen it; the other six schools are the
   spec's defaults until their own builds pick. */
const STAFF = {
'''),

    ]


def check_bow_body(code: str) -> None:
    """v89 §1: the staff's physics are the bow's EXACTLY. Read them off the
    shipped bow rather than trusting the table above."""
    ih = relic_entry(code, "ironhail")
    for k, v in BODY.items():
        pat = rf"\b{k}:\s*{re.escape(str(v))}(?=[,\s}}])"
        if not re.search(pat, ih):
            raise SystemExit(f"REFUSING TO WRITE -- Ironhail's {k} is not {v}; "
                             "the bow's physics moved under this builder")
    m = re.search(r"shot:\{([^}]*)\}", ih)
    shot = m.group(1)
    for k in ("cadence", "speed", "r", "life", "grav", "dmgMul"):
        v = BOW_SHOT[k]
        if not re.search(rf"\b{k}:{re.escape(fnum(v))}(?=[,\s])", shot):
            raise SystemExit(f"REFUSING TO WRITE -- the bow's shot {k} is not {v}")
    if f'tip:"{BOW_SHOT["tip"]}"' not in shot:
        raise SystemExit("REFUSING TO WRITE -- the bow's shot tip moved")
    print("  ok    body  the bow's physics and arrow, read off Ironhail")


def stage_of(code: str) -> int:
    """Which stage this source already carries, read off the relic itself."""
    if f'id:"{RELIC}"' not in code:
        return 0
    ent = relic_entry(code, RELIC)
    if "charge:1e9" not in ent:
        if "drawIronfall(m){" in code:
            return 6
        return 5 if f"dmg:{fnum(TUNED_BLADE)}," in ent else 3
    if f"grav:{SLUG['grav']}" in ent:
        return 2
    return 1


def audit(tip_p: pathlib.Path) -> int:
    """DID EVERY EDIT SURVIVE? `chain_audit.py`'s question, asked of this
    builder directly: its discovery reads module-level `*_NEW` constants and
    tuple tables, and this builder makes its tables in functions (they are
    templated on the spec, the stage's numbers and the voices), so
    chain_audit reports "no inserts found" -- open item 31's fifth costume.
    Every stage's edits are replayed here and every line of CODE each edit
    ADDS (block comments stripped, as chain_audit strips them) must be in the
    tip, verbatim."""
    raw = tip_p.read_text(encoding="utf-8")
    tip = strip_comments(raw)
    spec_body, spec_sha = staff_code()
    stages = [("1", s1_edits(spec_body, spec_sha)),
              ("2", [(l, o.replace("%DMG%", fnum(BLADE)), n.replace("%DMG%", fnum(BLADE)))
                     for l, o, n in s2_edits()]),
              ("3", s3_edits(dict(ULT))), ("5", s5_edits()), ("6", s6_edits())]
    # A LINE A LATER STAGE OF THIS BUILDER REPLACES IS SUPERSEDED, NOT LOST:
    # it is in that stage's anchor. And the relic's NOTE edits rewrite comment
    # prose, so they are checked against the tip with its comments kept.
    flat = [(i, st, e) for i, (st, edits) in enumerate(stages) for e in edits]
    total = lost = superseded = 0
    for i, st, (label, old, new) in flat:
        prose = label.startswith("the relic's note")
        strip = (lambda x: x) if prose else strip_comments
        later = set()
        for j, _st, (_l, o2, _n) in flat:
            if j > i:
                later |= set(strip(o2).splitlines())
        olds = set(strip(old).splitlines())
        added = [l for l in strip(new).splitlines()
                 if l not in olds and len(l.strip()) > 6 and l.strip() not in ("}", "});", "},")]
        body = raw if prose else tip
        miss = [l for l in added if l not in body and l not in later]
        sup = [l for l in added if l not in body and l in later]
        total += 1
        if sup:
            superseded += 1
            print(f"  ok    stage {st}  {label}: {len(sup)} line(s) replaced by a later stage, by design")
        if miss:
            lost += 1
            print(f"  LOST  stage {st}  {label}: {len(miss)} of {len(added)} lines, first {miss[0].strip()[:70]!r}")
    print(f"\n  {total - lost}/{total} inserts survive in {tip_p.name}"
          f" ({superseded} carry lines a later stage replaced on purpose)"
          + ("" if not lost else "  <-- A DOWNSTREAM EDIT ATE SOMETHING"))
    return 0 if not lost else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"])
    ap.add_argument("--src")
    ap.add_argument("--out")
    ap.add_argument("--audit", default=None, metavar="TIP",
                    help="replay every stage's edits and check each added line is in TIP")
    ap.add_argument("--charge", type=float, default=None,
                    help="stage 3: a charge other than the shipped one, for a "
                         "MEASUREMENT link written to scratch -- never a link of record")
    A = ap.parse_args()
    if A.audit:
        print(f"\nCULVERIN / IRONFALL -- the insert audit against {A.audit}")
        return audit((HERE / A.audit).resolve())
    if not (A.stage and A.src and A.out):
        raise SystemExit("--stage, --src and --out are required to build")
    stage = int(A.stage)
    U = dict(ULT)
    if A.charge is not None:
        U["charge"] = int(A.charge) if A.charge == int(A.charge) else A.charge
        if (HERE / A.out).resolve().parent == (HERE / "../02-chain").resolve():
            raise SystemExit("--charge writes a measurement link; it may not go in 02-chain")

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nCULVERIN / IRONFALL -- stage {stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    code = strip_comments(s0)
    # THE BASE: sc-leaf or later -- the Winnowing's rung stop is the link Rick
    # passed at gate 4 (v67). Either line is accepted, and named.
    if "s.over.stop = 0.02 * s.rung;" not in code:
        raise SystemExit("wrong base: no Winnowing rung stop -- older than sc-leaf")
    line = ("the design batch's line (carries Corollary)" if "echoShown" in code
            else "sc-leaf's line")
    print(f"  base  {line}")
    have = stage_of(code)
    prev = {1: 0, 2: 1, 3: 2, 5: 3, 6: 5}[stage]
    if have != prev:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built "
                         f"on stage {prev}")
    if stage == 1 and ("SHAPES.staff" in code or "const STAFF" in code):
        raise SystemExit("this source already carries a staff -- built")

    edits = []
    if stage == 1:
        check_bow_body(code)
        spec_body, spec_sha = staff_code()
        print(f"  spec  06-docs/v89/staff_spec.js  {spec_sha}")
        edits = s1_edits(spec_body, spec_sha)
    elif stage == 2:
        dmg = re.search(r"dmg:([\d.]+),", relic_entry(code, RELIC)).group(1)
        edits = [(l, o.replace("%DMG%", dmg), n.replace("%DMG%", dmg))
                 for l, o, n in s2_edits()]
    elif stage == 3:
        edits = s3_edits(U)
    elif stage == 5:
        edits = s5_edits()
    elif stage == 6:
        edits = s6_edits()
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    ent = relic_entry(out_code, RELIC)
    shot = SLUG if stage >= 2 else BOW_SHOT
    if len(CARD) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(CARD)} chars")
    # 46 is `verify`'s shot-tip cap (its own comment says why it is not 40).
    if len(shot["tip"]) > 46:
        raise SystemExit("REFUSING TO WRITE -- the shot tip is over verify's 46")
    for k, v in BODY.items():
        if not re.search(rf"\b{k}:\s*{re.escape(str(v))}(?=[,\s}}])", ent):
            raise SystemExit(f"REFUSING TO WRITE -- Culverin's {k} is not {v}")
    m = re.search(r"shot:\{([^}]*)\}", ent).group(1)
    for k in ("cadence", "speed", "r", "life", "grav", "dmgMul"):
        if not re.search(rf"\b{k}:{re.escape(fnum(shot[k]))}(?=[,\s])", m):
            raise SystemExit(f"REFUSING TO WRITE -- Culverin's shot {k} is not {shot[k]}")
    if f'tip:"{shot["tip"]}"' not in m:
        raise SystemExit("REFUSING TO WRITE -- Culverin's shot tip is not this run's")
    want_dmg = TUNED_BLADE if stage >= 5 else BLADE
    if f"dmg:{fnum(want_dmg)}," not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- Culverin's blade is not {want_dmg}")
    if 'shape:"staff"' not in ent:
        raise SystemExit("REFUSING TO WRITE -- Culverin is not a staff")
    if stage <= 2 and "charge:1e9" not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- stage {stage} must stub the ultimate")
    if stage >= 3:
        # v56's failure, verbatim: a stage that LOGS numbers it does not ship.
        blk = re.search(r"ult:\{[\s\S]*?tip:\"[^\"]*\" \},", ent).group(0)
        want = strip_comments(ult_live(U)).strip()
        if blk.strip() != want:
            raise SystemExit(f"REFUSING TO WRITE -- the shipped ult block is not "
                             f"what this run printed:\n  {blk}\n  want {want}")
        for need, why in (('spell:"slug"', "the slug does not name its spell"),
                          ("tickIronfall(dt){", "no tickIronfall"),
                          ('u.kind === "ironfall"', "no cast branch")):
            if need not in out_code:
                raise SystemExit(f"REFUSING TO WRITE -- {why}")
        if out_code.count('kind:"ironfall"') != 1:
            raise SystemExit("REFUSING TO WRITE -- expected exactly one Ironfall")
        if out_code.count("this.tickIronfall(dt);") != 1:
            raise SystemExit("REFUSING TO WRITE -- tickIronfall must be called once")
        print("  ok    ult   " + ", ".join(f"{k} {U[k]}" for k in ULT_KEYS))
    if stage >= 6:
        for w in ("culverin", "culverin-shell", "culverin-whistle", "culverin-burst", "culverin-close"):
            if out_code.count(f'w === "{w}"') != 1:
                raise SystemExit(f"REFUSING TO WRITE -- the {w} voice arm is not there exactly once")
        for need in ('p.spell === "slug"', 'kind === "slug-land"', "this.drawIronfall(m);", "drawIronfall(m){"):
            if out_code.count(need) != 1:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not there exactly once")
        for key, body in VOICES.items():
            eng = strip_comments(arm(key, "")).split()
            if " ".join(eng) not in " ".join(out_code.split()):
                raise SystemExit(f"REFUSING TO WRITE -- the {key} voice shipped is not the picked body")
        print("  ok    voices  " + ", ".join(f"{k} {VOICE_PICKS[k]}" for k in VOICES)
              + "  -- every arm the picked body, verbatim")
    what = "the slug" if stage >= 2 else "the bow's arrow"
    if A.charge is not None:
        print(f"  NOTE  --charge {U['charge']}: a MEASUREMENT link, not the link of record")
    print(f"  ok    relic  shape staff, the bow's body, {what}, "
          f"{'ultimate stubbed' if 'charge:1e9' in ent else 'ultimate live'}")
    print(f"  ok    shot  " + ", ".join(f"{k} {shot[k]}" for k in shot if k != "tip")
          + f"   tip {len(shot['tip'])} chars")
    print(f"  ok    card  {len(CARD)} chars  {CARD!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, old, new in edits:
        # only the lines this insert ADDS: an anchor may carry an existing call
        # (the spent branch's own spawnFx) that the insert leaves alone
        added = [l for l in new.splitlines() if l not in old.splitlines()]
        ins = strip_comments("\n".join(added))
        if "rng()" in ins or "spawnFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws "
                             "the match RNG")
    if out_code.count('shape:"staff"') != 1:
        raise SystemExit("REFUSING TO WRITE -- expected exactly one staff in the roster")
    print("  ok    one staff in the roster; no insert draws the RNG")

    stamp = (f"<!-- GENERATED by culverin_build.py --stage {stage} "
             f"--src {src_p.name} -->\n")
    s = stamp + s
    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    print("\n  GATE -- in this order, and each can fail:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --ids <the 34> --n 10")
    if stage == 1:
        print(f"    python staff_paint_gate.py --game {A.out}")
    else:
        print(f"    python culverin_probe.py --game {A.out}")
    print(f"    python verify.py --game {A.out} --n 40")
    print(f"    python tip_audit.py --game {A.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
