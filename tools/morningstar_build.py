#!/usr/bin/env python
"""MORNINGSTAR / ZENITH -- the sanctified flail, a NEW relic. v98.

Built from `06-docs/v71/MORNINGSTAR-BUILD-BRIEF.md` and
`sanctified-flail-design-v71.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-morningstar.html
    stage 2   the light and the smite     -> sc-sun.html      (arm B)
    stage 3   the burn                    -> sc-burn.html     (arm C)
    stage 4   the heal                    -> sc-zenith.html   (arm D)
    stage 5   the blade                   confirm 24.03 wide on 151 (no link unless it moves)
    stage 6   picture, voice, field       (not written yet)

§1 (the brief's §0): "For a duration the flail's head becomes a sun. An enemy
in its light is smitten and burned for as long as it stays there, and every
burn heals the one swinging it. The head still hits like a flail head."

Declared (design §5, brief §0-§1): the light is a disc of radius 100 on the
flail HEAD; the foe is lit when its centre is within 100 + R. A tick every
0.4s while lit: `hurt(foe, 3, f)` (ward first, nothing else), smite +1, then
blessing +1 on the caster. Blessing heals through the existing `tickStatus`
branch. No `resolveHit` change, no stun, no pin, no knock.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter the engine's clock runs 0.897 of the lab's (the lab's 16 =
the engine's ~14.35), so 14.

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE TICK'S ORDER is the prose's: hurt, then smite, then blessing (the lab
     does smite first; no fight can tell).
  2. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract). Smite ticks
     damage, and its fatal DOT beat is attributed by that letter.
  3. THE TICK THAT KILLS files its own fatal hit beat (the engine's rule for a
     side-channel kill); no other tick files one.
  4. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab lights only
     `foe`; Corollary's reading 3).
  5. THE CADENCE is the lab's: a 0.4s cooldown running through the whole
     window, firing on the first lit frame it is clear.
  6. THE BLESSING is per TICK and unconditional on damage dealt (§5 as
     written), so a tick a ward swallows still blesses.

THE CLOCK. The window and the cooldown run on the window tickers' clock, which
stops through a hit stop (Corollary's and Daybreak's convention).

THE BASE is the chain tip, `sc-daybreak-fx.html`, named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "morningstar"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling)
    "dur": 8,         # "the window 8s"
    "r": 100,         # "disc radius 100 on the HEAD"
    "tick": 0.4,      # "every 0.4s while lit"
    "smite": 1,       # "smite +1"
    "tickDmg": 3,     # "hurt 3" -- stage 3
    "bless": 1,       # "then blessing +1 on the caster" -- stage 4
}
TIP = "The head becomes a sun: its light smites foes, and each burn heals it"
# Gravemourn's flail profile, the lab's donor (cell_ults_on.TYPE_DONOR), and
# the type's own blade: "24.03 -- UNCHANGED".
PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:24.03, spin:2.2, '
        'mode:"chain", mass:3.6')
BLURB = ("A flail whose head becomes a sun: its light smites and burns, and "
         "every burn heals the one swinging it.")


def ult_block(charge, tick_dmg: int, bless: int) -> str:
    return (f'''    ult:{{ name:"Zenith", charge:{charge}, kind:"sun", dur:{ULT["dur"]},
          r:{ULT["r"]}, tick:{ULT["tick"]}, smite:{ULT["smite"]},
          tickDmg:{tick_dmg},        // v71: the burn (stage 3)
          bless:{bless},          // v71: the heal (stage 4)
          tip:"{TIP}" }},''')


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
        print("  WARN  no `node` on PATH -- output NOT syntax checked.")
        return
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


# ---------------------------------------------------------------- stage 1 --
# THE RELIC, APPENDED AFTER STARWARDEN, ITS ULTIMATE STUBBED at charge 1e9 (the
# clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. Every other table keyed by relic id falls back.
ROW_ANCHOR = ('''    blurb:"A ring of light worn like a sash, and a star at the heart of it. Whatever touches either one goes on burning." },

];''')

S1 = [

("morningstar joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 ROW_ANCHOR[:-4] + f'''
  /* MORNINGSTAR / ZENITH (v71; built v98) -- THE SANCTIFIED FLAIL, the 35th
     relic built. Gravemourn's flail profile and the type's own blade, 24.03
     (the lab's donor; "UNCHANGED"), and the school's channel, onHit smite.
     Stage 1 stubs the ultimate at charge 1e9; stages 2-4 give it its light,
     its burn and its heal, one number at a time. */
  {{ id:"morningstar", name:"Morningstar", aff:"sanctified", shape:"flail",
    {PHYS},
    onHit:{{ smite:1 }},
{ult_block("1e9", 0, 0)}
    blurb:"{BLURB}" }},

];'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the sun has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Zenith", charge:1e9, kind:"sun", dur:8,
''',
 f'''    ult:{{ name:"Zenith", charge:{ULT["charge"]}, kind:"sun", dur:{ULT["dur"]},   // v71 stage 2: the sun lights
'''),

("the fighter carries the sun's window",
 '''    this.ultDawn = null;
    this.dawnTally = null;
''',
 '''    this.ultDawn = null;
    this.dawnTally = null;
    /* {t, dur, cd} while ZENITH's sun burns on the flail head (v71). null on
       every other relic and on this one outside its window: `tickSun` returns
       after a two-iteration loop that does nothing. `sunTally` is the probe's
       count, cumulative over the fight; nothing in the simulation reads it. */
    this.ultSun = null;
    this.sunTally = null;
'''),

("the cast lights the sun and resolves nothing",
 '''    if (u.kind === "dawn"){
''',
 '''    if (u.kind === "sun"){
      /* ZENITH (v71). NOTHING RESOLVES HERE: the cast turns the flail's head
         into a sun for `u.dur` seconds, and `tickSun` does everything the
         window does. `cd` starts at zero, so a foe already in the light is
         struck on the first frame. */
      f.ultSun = { t: 0, dur: u.dur, cd: 0 };
      if (!f.sunTally)
        f.sunTally = { casts: 0, ticks: 0, dealt: 0, bless: 0,
                       litFrames: 0, frames: 0 };
      f.sunTally.casts++;
      return;
    }
    if (u.kind === "dawn"){
'''),

("the sun ticks with the window tickers",
 '''    this.tickDawn(dt);                  // DAYBREAK (v86)
''',
 '''    this.tickDawn(dt);                  // DAYBREAK (v86)
    this.tickSun(dt);                   // ZENITH (v71)
'''),

("tickSun burns in the light of the head",
 '''  tickWinnow(dt){
''',
 '''  /* =================================================== THE SUN ========
     v71 §5 / brief §0: while the window runs the flail's HEAD is a sun of
     radius `r`. A foe whose centre is within `r` + R of the head is lit, and
     every `tick` seconds while lit: `hurt(foe, tickDmg, f)` -- ward first and
     NOTHING ELSE: no crit, no knock, no hit stop, no hitstun -- then smite
     +`smite`, then blessing +`bless` on the caster (it heals through
     tickStatus). No beat, except the tick that KILLS, which files its own
     (the engine's rule for a side-channel kill).

     The HEAD is `f.headX/Y`, which tickWeapon moved earlier this step, so the
     light is tested where the head is now. The target is the OPPONENT only.
     THE COOLDOWN RUNS THROUGH THE WHOLE WINDOW, lit or not, and a tick fires
     on the first lit frame it is clear (the lab's cadence, and what was
     priced). On the window tickers' clock, so it freezes through a hit stop.
     `apply`'s source is a side letter (Fighter.apply's contract). */
  tickSun(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultSun;
      if (!Z) continue;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive){ f.ultSun = null; continue; }
      const u = f.w.ult, T = f.sunTally;
      const foe = f === this.a ? this.b : this.a;
      const R = CONFIG.physics.ballR;
      Z.cd -= dt;
      T.frames++;
      if (!foe.alive
          || !(Math.hypot(foe.x - f.headX, foe.y - f.headY) < u.r + R)) continue;
      T.litFrames++;
      if (Z.cd > 0) continue;
      Z.cd = u.tick;
      T.ticks++;
      const side = f === this.a ? "a" : "b";
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      this.hurt(foe, u.tickDmg, f);
      T.dealt += before - (foe.hp + foe.shield);
      foe.apply("smite", u.smite, side);
      if (u.bless > 0){ f.apply("blessing", u.bless, side); T.bless += u.bless; }
      if (wasUp && foe.hp <= 0)
        this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                    x: foe.x, y: foe.y, dmg: u.tickDmg, crit: false,
                    fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                    selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                    close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                    ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                    shotSpd0: 0, sun: true });
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the burn",
 '''          tickDmg:0,        // v71: the burn (stage 3)
''',
 f'''          tickDmg:{ULT["tickDmg"]},        // v71: the burn (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 4 --
S4 = [
("the heal",
 '''          bless:0,          // v71: the heal (stage 4)
''',
 f'''          bless:{ULT["bless"]},          // v71: the heal (stage 4)
'''),
]

STAGE_OUT = {"1": "sc-morningstar", "2": "sc-sun", "3": "sc-burn", "4": "sc-zenith"}


def relic_ult(code: str) -> str:
    i = code.find('id:"morningstar"')
    if i < 0:
        raise SystemExit("no Morningstar in this source")
    j = code.find("ult:{", i)
    k = code.find("},", j)
    return code[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "4"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()

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
    print(f"\nMORNINGSTAR / ZENITH -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Corollary
    # at charge 14 and Daybreak through its stage 3.
    for need, why in (('name:"Corollary", charge:14', "no Corollary at charge 14"),
                      ("dawnShown", "no Daybreak stage 3 -- not the chain tip")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    # AND THE DONOR'S FLAIL PROFILE IS STILL WHAT THIS BUILDER COPIES.
    g = code[code.find('id:"gravemourn"'):]
    if PHYS not in g[:400]:
        raise SystemExit("Gravemourn's flail profile has moved -- the donor is "
                         "not what this builder copies")
    print("  base  the chain tip (Corollary c14, Daybreak stage 3); the donor's "
          "flail profile holds")

    if A.stage == "1":
        if 'id:"morningstar"' in code:
            raise SystemExit("this source already carries Morningstar -- built")
        edits, want = S1, ult_block("1e9", 0, 0)
    else:
        if 'id:"morningstar"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultSun" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0, 0)
        elif A.stage == "3":
            if "ultSun" not in code:
                raise SystemExit("stage 3 needs stage 2 under it")
            edits, want = S3, ult_block(ULT["charge"], ULT["tickDmg"], 0)
        else:
            if f'tickDmg:{ULT["tickDmg"]},' not in code:
                raise SystemExit("stage 4 needs stage 3 under it")
            edits, want = S4, ult_block(ULT["charge"], ULT["tickDmg"], ULT["bless"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Morningstar's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S4:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the RNG")
    if len(re.findall(r'kind:"sun"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one sun ultimate")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one sun ultimate, Morningstar's; no insert draws the RNG; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
