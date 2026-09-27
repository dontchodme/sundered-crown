#!/usr/bin/env python
"""CULVERIN / IRONFALL -- the dwarven staff, and the staff TYPE with it. v96.

Built from `06-docs/v96/CULVERIN-BUILD-BRIEF.md` and
`dwarven-staff-design-v96.md` (Cowork, 2026-09-27), the row's
`06-docs/v89/STAFF-ROW-v89.md` §1/§6, and the art's `staff-art-v89.md` with
`staff_spec.js` beside it. Those are the input and the only input. CLAUDE.md
§3 rule 0: nothing here is a design decision. Rick, 2026-09-27, on yert:
"staff is in the repo. lets build it" -- the row accepted whole.

    stage 1   the relic, its ultimate STUBBED, shape "staff"   sc-leaf -> sc-culverin
    stage 2   the spell: SLUG                                  (not written yet)
    stage 3   the ultimate: IRONFALL                           (not written yet)
    stage 5   the blade, wide on 151                           (a link only if it moves)
    stage 6   picture, voice, field, the carry                 (not written yet)

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
        return 3
    if f"grav:{SLUG['grav']}" in ent:
        return 2
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    stage = int(A.stage)

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
    if have != stage - 1:
        raise SystemExit(f"this source carries stage {have}; stage {stage} is built "
                         f"on stage {stage - 1}")
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
    if stage == 1 and f"dmg:{BLADE}," not in ent:
        raise SystemExit("REFUSING TO WRITE -- Culverin's blade is not this run's")
    if 'shape:"staff"' not in ent:
        raise SystemExit("REFUSING TO WRITE -- Culverin is not a staff")
    if stage <= 2 and "charge:1e9" not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- stage {stage} must stub the ultimate")
    what = "the slug" if stage >= 2 else "the bow's arrow"
    print(f"  ok    relic  shape staff, the bow's body, {what}, "
          f"{'ultimate stubbed' if 'charge:1e9' in ent else 'ultimate live'}")
    print(f"  ok    shot  " + ", ".join(f"{k} {shot[k]}" for k in shot if k != "tip")
          + f"   tip {len(shot['tip'])} chars")
    print(f"  ok    card  {len(CARD)} chars  {CARD!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in edits:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
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
