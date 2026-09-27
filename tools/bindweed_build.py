#!/usr/bin/env python
"""BINDWEED / TENDRIL -- the verdant flail, a NEW relic. v101.

Built from `06-docs/v68/BINDWEED-BUILD-BRIEF.md` and
`verdant-flail-design-v68.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-bindweed.html
    stage 2   the seek and the growth     -> sc-vine.html     (the seek+growth arm)
    stage 3   the bites                   -> sc-bites.html    (arm C)
    stage 4   the root and the wither     -> sc-tendril.html  (arm D)
    stage 5   the turn, the blade         -> sc-tendril-t3.html (turn 4 -> 3, dmg 19 -> 18)
    stage 6   picture, voice, field       (not written yet)

§1 (the brief's §0): "For a duration the whole chain becomes a living thorned
vine. It turns toward the enemy and grows until it reaches them, and it draws
back in when they come closer, so the head -- still a flail head, still hitting
like one -- is always where the enemy is. Anywhere the vine touches them it
bites: a small hit that leaves entangle, over and over while it stays on them.
When the duration ends the vine withers, and the thorns it left take root: the
enemy is held where it stands, ball and weapon, for a moment for every
entangle stack it carries."

Declared (design §4-§7, brief §0-§1):
  THE SEEK    for the window the facing turns toward the foe at `turn` rad/s
              the shortest way round, instead of advancing by spin; the chain's
              spin is 0, so its drive is 0 (the spring, sag, damping and
              extension are the engine's own).
  THE GROWTH  reachMul moves at `grow` a second toward (d - R) / (reach x
              mods.reach), both directions, clamped [1, growCap].
  A BITE      the foe's centre within R + vineW of the pivot -> head segment,
              once per `biteCd`: hurt(foe, biteDmg, f) -- ward first, nothing
              else -- and entangle +bitePer. No knock, no stop, no beat, no
              resolveHit.
  THE ROOT    at the window's clock close with both alive: pin rootPer x the
              foe's entangle stacks, ball and weapon (Grasp's write, no pinFree).
  THE WITHER  0.4s; the next cast waits for it.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm D (v101 §0).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE CHAIN'S SPIN IS 0 FOR THE WINDOW, not only its drive. The lab zeroed
     the weapon's spin, which zeroes the drive AND leaves the extension's
     normaliser at its 0.5 floor, so a small sway throws the head out; the
     brief's "drive = 0" and "the extension untouched" are both that. The build
     zeroes `spin` in tickWeapon for this fighter, and never writes the shared
     weapon (the mirror match shares it).
  2. THE VINE KEEPS TURNING WHILE STUNNED (the brief leaves it to the build;
     the lab turned it, and that is what was priced).
  3. REACH RETURNS TO 1 AT THE CLOSE (design §7 and the lab). The brief's
     "eased back over the wither" is the wither's picture, not the hit box.
  4. NO PER-BITE REACH KICK. The lab's arms add 0.05 of reach a bite; the
     prose has none. v101 §2 prices the difference.
  5. EITHER DEATH ENDS THE WINDOW AND ROOTS NOBODY (the brief); the lab closed
     only on its clock.
  6. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract; the lab and the
     brief wrote the Fighter, and entangle has no reader of it).
  7. A BITE THAT KILLS files its own fatal hit beat (Rick's standing rule for
     a side-channel kill); no other bite files one.
  8. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).

THE CLOCK. The window, the turn, the growth, the bite's cooldown and the
wither run on the window tickers' clock, which stops through a hit stop
(Corollary's, Daybreak's, Zenith's, Canopy's and Onslaught's convention). The
lab ran all of them through freezes; v99 §4 and v100 §2 measured what that is
worth on the two builds before this one.

THE BASE is the chain tip, named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "bindweed"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v101 §0)
    "dur": 8,         # "the window 8s"
    "turn": 4,        # "facing turns toward the foe at 4 rad/s"
    "grow": 0.3,      # "reachMul eased at 0.3/s"
    "growCap": 3.0,   # "clamped [1, 3.0]"
    "vineW": 8,       # "within R + 8 of the pivot -> head segment"
    "biteDmg": 2,     # "2 damage (ward absorbs first)" -- stage 3
    "bitePer": 1,     # "+ 1 entangle" -- stage 3
    "biteCd": 0.3,    # "every 0.30s while touching"
    "rootPer": 0.3,   # "pin 0.30s x entangle stacks" -- stage 4
    "wither": 0.4,    # "the next cast waits for the wither to finish (0.4s)"
}
TIP = "The chain becomes a vine that hunts the foe. Bites entangle, then root"
# Gravemourn's flail profile, the lab's donor (vine_price.py), and the lab's
# blade, 19 ("a placeholder -- stage 5 owns it").
PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:19, spin:2.2, '
        'mode:"chain", mass:3.6')
DONOR_PHYS = ('blades:[0], reach:96, width:22, artW:52, dmg:24.03, spin:2.2, '
              'mode:"chain", mass:3.6')
VERDANT = ("thornwake", "heartwood", "vinesower", "thornshear", "ironwood")
BLURB = ("A flail whose chain becomes a living vine: it hunts the foe, bites it "
         "with thorns, and roots it where it stands.")


def ult_block(charge, bite_dmg, bite_per, root_per) -> str:
    return (f'''    ult:{{ name:"Tendril", charge:{charge}, kind:"tendril", dur:{ULT["dur"]},
          turn:{ULT["turn"]}, grow:{ULT["grow"]}, growCap:{ULT["growCap"]}, vineW:{ULT["vineW"]},
          biteDmg:{bite_dmg}, bitePer:{bite_per},          // v68: the bites (stage 3)
          biteCd:{ULT["biteCd"]},
          rootPer:{root_per},          // v68: the root (stage 4)
          wither:{ULT["wither"]},
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
# THE RELIC, APPENDED AFTER PORTCULLIS, ITS ULTIMATE STUBBED at charge 1e9
# (the clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. Every other table keyed by relic id falls back, and SHAPES.flailHead
# already routes verdant to `_fhGrown`, which no shipped relic has drawn.
ROW_ANCHOR = ('''    blurb:"A flail whose ball becomes the weapon: it charges, every slam hits for the shield it carries, and every slam banks more." },

];''')

S1 = [

("bindweed joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 ROW_ANCHOR[:-4] + f'''
  /* BINDWEED / TENDRIL (v68; built v101) -- THE VERDANT FLAIL, the 38th relic
     built. Gravemourn's flail profile (the lab's donor) at the lab's blade,
     19 (stage 5 settles it), and the school's channel, onHit entangle 2.
     Stage 1 stubs the ultimate at charge 1e9; stages 2-4 give it its seek and
     growth, its bites, then its root. */
  {{ id:"bindweed", name:"Bindweed", aff:"verdant", shape:"flail",
    {PHYS},
    onHit:{{ entangle:2 }},
{ult_block("1e9", 0, 0, 0)}
    blurb:"{BLURB}" }},

];'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the vine has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Tendril", charge:1e9, kind:"tendril", dur:8,
''',
 f'''    ult:{{ name:"Tendril", charge:{ULT["charge"]}, kind:"tendril", dur:{ULT["dur"]},   // v68 stage 2: the vine seeks and grows
'''),

("the fighter carries the vine",
 '''    this.ultRam = null;
    this.ramTally = null;
''',
 '''    this.ultRam = null;
    this.ramTally = null;
    /* {t, dur, cd} while TENDRIL's vine hunts (v68). null on every other relic
       and on this one outside its window: `tickTendril` returns after a
       two-iteration loop that does nothing, and tickWeapon's chain branch
       reads it once. `vineWither` is the seconds left of the wither, which the
       next cast waits for. `vineTally` is the probe's count, cumulative over
       the fight; nothing in the simulation reads it. */
    this.ultVine = null;
    this.vineWither = 0;
    this.vineTally = null;
'''),

("the vine does not spin",
 '''    const spin = f.w.spin * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge || f.ultWire ? (f.w.ult.spinMul || 1)
                 : f.ultSpin ? this.ultSpinMul(f) : 1);
''',
 '''    /* TENDRIL (v68): THE VINE DOES NOT SPIN. `spin` is 0 for the whole
       window, as the lab priced it (it zeroed the weapon's spin; the build
       must never write the shared weapon), so the chain's drive is 0 and the
       extension's normaliser below sits at its 0.5 floor -- a small sway
       throws the head out, and that sway is the picture. `ultVine` is null on
       every other relic, so theirs is the same product. */
    const spin = (f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)
              * (f.ultDraw || f.ultForge || f.ultWire ? (f.w.ult.spinMul || 1)
                 : f.ultSpin ? this.ultSpinMul(f) : 1);
'''),

("the vine turns toward the foe",
 '''      if (f.stun <= 0) f.theta += spin * dt * f.spinDir;
      const drive = f.stun > 0 ? 0 : spin * f.spinDir;
''',
 '''      /* TENDRIL'S SEEK (v68 §5): for the window the facing turns toward the
         foe at `turn` rad/s the shortest way round -- stunned or not, as the
         lab turned it -- instead of advancing by spin. */
      if (f.ultVine){
        if (foe.alive){
          const want = Math.atan2(foe.y - f.y, foe.x - f.x);
          const dl = Math.atan2(Math.sin(want - f.theta), Math.cos(want - f.theta));
          const k = f.w.ult.turn * dt;
          f.theta += clamp(dl, -k, k);
        }
      } else if (f.stun <= 0) f.theta += spin * dt * f.spinDir;
      const drive = f.stun > 0 ? 0 : spin * f.spinDir;
'''),

("the cast opens the vine and resolves nothing",
 '''    if (u.kind === "ram"){
''',
 '''    if (u.kind === "tendril"){
      /* TENDRIL (v68). NOTHING RESOLVES HERE: the cast turns the chain into a
         vine for `u.dur` seconds, and tickWeapon (the seek) and `tickTendril`
         (the growth, the bites, the root) do everything the window does. `cd`
         starts at zero, so a foe already touching is bitten on the first
         frame. */
      f.ultVine = { t: 0, dur: u.dur, cd: 0 };
      if (!f.vineTally)
        f.vineTally = { casts: 0, frames: 0, touchFrames: 0, bites: 0, dealt: 0,
                        stacks: 0, foeStk: 0, peak: 1, roots: 0, rootSec: 0 };
      f.vineTally.casts++;
      return;
    }
    if (u.kind === "ram"){
'''),

("the vine ticks with the window tickers",
 '''    this.tickRam(dt);                   // ONSLAUGHT (v72)
''',
 '''    this.tickRam(dt);                   // ONSLAUGHT (v72)
    this.tickTendril(dt);               // TENDRIL (v68)
'''),

("a cast waits for the last vine's wither",
 '''    if (f.charge >= f.w.ult.charge && !f.ultCorona && !f.ultTree && !f.treeWither){
''',
 '''    if (f.charge >= f.w.ult.charge && !f.ultCorona && !f.ultTree && !f.treeWither
        && !f.ultVine && !f.vineWither){       // TENDRIL (v68): one vine at a time
'''),

("tickTendril grows, bites and roots",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================ THE TENDRIL ========
     v68 §4-§7, brief §0-§1. While the window runs (tickWeapon turns the vine
     toward the foe; this does the rest):
       THE GROWTH  reachMul moves at `grow` a second toward the foe's rim in
                   units of the type's reach, (d - R) / (reach x mods.reach),
                   both directions, clamped [1, growCap]. Every reach read
                   carries it, so the drawn vine and the hit segment grow
                   together; tickWeapon uses it next frame, as the lab did.
       A BITE      the foe's centre within R + vineW of the pivot -> head
                   segment and the cooldown clear: hurt(foe, biteDmg, f) --
                   ward first and NOTHING ELSE: no knock, no stop, no stagger,
                   no resolveHit -- then entangle +bitePer. The cooldown runs
                   through the whole window, touching or not. A bite that
                   kills files its own fatal hit beat; no other bite files one.
       THE CLOSE   by the clock, or EITHER death: reach back to 1 and `wither`
                   seconds that the next cast waits for. Only a clock close
                   with both alive roots: pin rootPer x the foe's entangle
                   stacks, ball and weapon -- Grasp's write, no pinFree, so
                   `tickStasis` locks the weapon.
     The target is the OPPONENT only. On the window tickers' clock, so all of
     it freezes through a hit stop. `apply`'s source is a side letter. */
  tickTendril(dt){
    for (const f of [this.a, this.b]){
      if (f.vineWither > 0) f.vineWither = Math.max(0, f.vineWither - dt);
      const Z = f.ultVine;
      if (!Z) continue;
      const u = f.w.ult, T = f.vineTally;
      const foe = f === this.a ? this.b : this.a;
      const R = CONFIG.physics.ballR;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){
        f.ultVine = null;
        f.reachMul = 1;
        f.vineWither = u.wither;
        if (Z.t >= Z.dur && f.alive && foe.alive && u.rootPer > 0){
          const n = foe.stacks("entangle");
          if (n > 0){
            const hold = u.rootPer * n;
            foe.pin = Math.max(foe.pin, hold);
            foe.pinMax = Math.max(foe.pinMax, hold);
            if (!(foe.pin > hold)) foe.pinV = [foe.vx, foe.vy];
            T.roots++;
            T.rootSec += hold;
          }
        }
        continue;
      }
      T.frames++;
      const dd = Math.hypot(foe.x - f.x, foe.y - f.y);
      const want = clamp((dd - R) / (f.w.reach * this.actMods.reach), 1, u.growCap);
      if (f.reachMul < want) f.reachMul = Math.min(want, f.reachMul + u.grow * dt);
      else if (f.reachMul > want) f.reachMul = Math.max(want, f.reachMul - u.grow * dt);
      if (f.reachMul > T.peak) T.peak = f.reachMul;
      Z.cd -= dt;
      if (segDist(f.pivX, f.pivY, f.headX, f.headY, foe.x, foe.y).d < R + u.vineW){
        T.touchFrames++;
        if ((u.biteDmg > 0 || u.bitePer > 0) && Z.cd <= 0){
          Z.cd = u.biteCd;
          T.bites++;
          const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
          if (u.biteDmg > 0) this.hurt(foe, u.biteDmg, f);
          T.dealt += before - (foe.hp + foe.shield);
          if (u.bitePer > 0){ foe.apply("entangle", u.bitePer, f === this.a ? "a" : "b"); T.stacks += u.bitePer; }
          if (wasUp && foe.hp <= 0)
            this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                        x: foe.x, y: foe.y, dmg: u.biteDmg, crit: false,
                        fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                        selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                        close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                        ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                        shotSpd0: 0, tendril: true });
        }
      }
      T.foeStk += foe.stacks("entangle");
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the bites",
 '''          biteDmg:0, bitePer:0,          // v68: the bites (stage 3)
''',
 f'''          biteDmg:{ULT["biteDmg"]}, bitePer:{ULT["bitePer"]},          // v68: the bites (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 4 --
S4 = [
("the root",
 '''          rootPer:0,          // v68: the root (stage 4)
''',
 f'''          rootPer:{ULT["rootPer"]},          // v68: the root (stage 4)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE TURN AND THE BLADE (brief §2 stage 5: "If the band does not land inside
# 17-19.5, move `turn` inside 3-5 FIRST and say so"). Both sides, two blocks,
# ~1480 fights a point (relic_rate): at the designed turn 4, blade 17 reads
# 54.7, so the crossing is ~15.5 -- outside the band. At turn 3: 17 -> 45.7,
# 18 -> 48.6, 19 -> 55.6, the crossing ~18.2, inside the brief's "expect
# 17.5-18.5"; at 3.5 it would fall just under 17. Why the built relic reads over
# the lab at 4: the engine's window is ~9.6s of match time where the lab's was 8
# (v101 §2, measured with the lab at dur 9.6).
TUNED = {"turn": 3, "dmg": 18}

S5 = [
("the turn: the build's knob, inside 3-5",
 f'''          turn:{ULT["turn"]}, grow:{ULT["grow"]}, growCap:{ULT["growCap"]}, vineW:{ULT["vineW"]},
''',
 f'''          turn:{TUNED["turn"]}, grow:{ULT["grow"]}, growCap:{ULT["growCap"]}, vineW:{ULT["vineW"]},   // v68 stage 5: turn {ULT["turn"]} -> {TUNED["turn"]}, the build's knob
'''),
("the blade: at the crossing",
 '''  { id:"bindweed", name:"Bindweed", aff:"verdant", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:19,''',
 f'''  {{ id:"bindweed", name:"Bindweed", aff:"verdant", shape:"flail",
    blades:[0], reach:96, width:22, artW:52, dmg:{TUNED["dmg"]},'''),
]

STAGE_OUT = {"1": "sc-bindweed", "2": "sc-vine", "3": "sc-bites", "4": "sc-tendril",
             "5": "sc-tendril-t3"}


def relic_row(code: str, rid: str) -> str:
    i = code.find(f'{{ id:"{rid}"')
    if i < 0:
        raise SystemExit(f"no {rid} in this source")
    return code[i:code.find("blurb:", i)]


def relic_ult(code: str) -> str:
    row = relic_row(code, RELIC)
    j = row.find("ult:{")
    k = row.find("},", j)
    return row[j:k + 2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "4", "5"], required=True)
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
    print(f"\nBINDWEED / TENDRIL -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Onslaught
    # through its stage 5.
    if "tickRam(dt){" not in code or "bank:8," not in code:
        raise SystemExit("wrong base: no Onslaught stage 3 -- not the chain tip")
    if "dmg:23," not in relic_row(code, "portcullis"):
        raise SystemExit("wrong base: Portcullis is not at its stage-5 blade")
    # AND THE DONOR'S FLAIL PROFILE IS STILL WHAT THIS BUILDER COPIES; THE
    # SCHOOL'S CHANNEL AND THE VERDANT FLAIL HEAD ARE WHERE THEY WERE.
    if DONOR_PHYS not in " ".join(relic_row(code, "gravemourn").split()):
        raise SystemExit("Gravemourn's flail profile has moved -- the donor is "
                         "not what this builder copies")
    for v in VERDANT:
        if "onHit:{ entangle:2 }" not in relic_row(code, v):
            raise SystemExit(f"{v} does not carry the school's channel, entangle 2")
    if not re.search(r'if \(key === "verdant"\)\s+return SHAPES\._fhGrown\(', code):
        raise SystemExit("SHAPES.flailHead no longer routes verdant to _fhGrown")
    # THE NAMES THIS RELIC ADDS ARE FREE ON THE BASE ("vine" is the Thicket's
    # SFX kind and `tickVines` its ticker, so neither is used here).
    if A.stage == "1":
        for name in ("ultVine", "vineTally", "vineWither", "tickTendril", 'kind:"tendril"'):
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
    print("  base  the chain tip (Onslaught stage 5); the donor's flail profile, the "
          "verdant channel and the verdant head hold")

    if A.stage == "1":
        if f'id:"{RELIC}"' in code:
            raise SystemExit("this source already carries Bindweed -- built")
        edits, want = S1, ult_block("1e9", 0, 0, 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultVine" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 0, 0, 0)
        elif A.stage == "3":
            if "ultVine" not in code or "biteDmg:0, bitePer:0," not in code:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"], 0)
        elif A.stage == "5":
            if f'rootPer:{ULT["rootPer"]},' not in code or f'turn:{ULT["turn"]},' not in code:
                raise SystemExit("stage 5 goes on stage 4, once")
            edits = S5
            want = ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"], ULT["rootPer"]).replace(
                f'turn:{ULT["turn"]},', f'turn:{TUNED["turn"]},')
        else:
            if f'biteDmg:{ULT["biteDmg"]},' not in code or "rootPer:0," not in code:
                raise SystemExit("stage 4 goes on stage 3, once")
            edits, want = S4, ult_block(ULT["charge"], ULT["biteDmg"], ULT["bitePer"],
                                        ULT["rootPer"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Bindweed's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:96]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S4 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        if "pinFree" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' touches "
                             "pinFree (the root is Grasp's write)")
    if len(re.findall(r'kind:"tendril"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one tendril ultimate")
    # THE REACH THE VINE GROWS IS READ WHERE IT MATTERS (scoped, as Canopy's).
    if A.stage != "1":
        if not re.search(r'if \(f\.w\.mode === "chain"\)\{[\s\S]*?const reach = f\.w\.reach \* mods\.reach \* f\.reachMul;', out_code):
            raise SystemExit("REFUSING TO WRITE -- the chain's reach does not carry reachMul")
        print("  ok    reachMul at the chain (site 2)")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one tendril ultimate, Bindweed's; no insert draws the RNG, "
          f"writes the shared weapon or touches pinFree; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
