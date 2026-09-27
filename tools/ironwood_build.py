#!/usr/bin/env python
"""IRONWOOD / CANOPY -- the verdant warhammer, a NEW relic. v99.

Built from `06-docs/v69/IRONWOOD-BUILD-BRIEF.md` and
`verdant-warhammer-design-v69.md` (Cowork, 2026-09-26), which are the input and
the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-ironwood.html
    stage 2   the root and the growth     -> sc-rooted.html   (arm C, one bough)
    stage 3   the boughs                  -> sc-boughs.html   (arm C)
    stage 4   the canopy                  -> sc-canopy.html   (arm D)
    stage 5   the bough scale, the blade  -> sc-canopy-w38.html (winDmg 0.38, dmg 24)
    stage 6   picture, voice, field       (not written yet)

§1: "For a duration the hammer takes root: the ball stops where it stands and
grows bark -- it cannot be moved or knocked but it can still swing -- and the
haft grows into a bough, then two more boughs grow from the trunk, so three
lighter heads sweep the hall at up to two and a half times the hammer's reach.
Anyone under the canopy is entangled. When it ends the tree withers back to a
hammer and the roots let go."

Declared (design §6, brief §0-§1):
  THE ROOT     `f.pin` on the caster with `pinFree` 1 and `pinV` [0,0], re-armed
               every frame; released on close to REST (pin, pinMax 0, pinV null,
               pinFree 0, vx = vy = 0). `move`, gravity, `_ballPair` and the
               knock discard already do the rest.
  THE GROWTH   `f.reachMul` += 0.35/s to 2.5, back to 1 on close.
  THE BOUGHS   a per-fighter blade set [0, 1/3, 2/3] from 1.5s into the window
               (`f.bladeSet`, read by `bladeSegments` and `drawWeapon`); `tips`
               sized to it; every blow while the tree stands is the hammer's x
               0.35 (`resolveHit`'s damage line, the ONLY damage change).
  THE CANOPY   entangle 1 every 0.5s on a foe whose centre is within
               reach x mods.reach x reachMul + R of the caster.
  THE WITHER   0.4s; the next cast waits for it.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter (arm D, 660 fights) 13.0% of the lab's steps are frozen, so
the lab's 16 is the engine's ~13.9, and 14.

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE SPROUT IS THE PROSE'S: two boughs grow at 1.5s (the brief, twice).
     The lab gave all three at the cast, so stage 3 may read a little under arm
     C, by 1.5s of two boughs a cast.
  2. THE SHARED WEAPON IS NEVER MUTATED (the brief). `w` is module-level and
     the mirror match shares it; the lab wrote `w.blades` and `w.dmg`.
  3. THE 0.35 GOES ON `w.dmg` INSIDE `resolveHit`'s product, ahead of the
     jitter, the crit and the rounding, so a blow is bit-identical to the
     lab's scaled `w.dmg`. Ironwood's blows all arrive with `mul` undefined.
  4. THE ROOT IS RE-ARMED WITH `pinFree`, not only `pin` (the lab re-arms the
     pin). Ravelbone's wire writes `pinFree = 0` on its quarry at a connect or
     a slip; with the pin re-armed and pinFree not, `tickStasis` would lock the
     weapon for the rest of the window, and the prose says it keeps turning.
  5. THE WINDOW CLOSES ON THE CASTER'S DEATH (the prose), not the foe's (the
     lab). A caster that dies keeps its kill-flight velocity (the engine's
     rule; `tickStasis` already cleared its pin): only a live caster is set
     to rest.
  6. A NEW BOUGH'S COOLDOWN STARTS AT ZERO ("each bough has its own 0.45s
     hitCd"); the lab left the last window's value in the slot.
  7. THE CANOPY'S SOURCE IS A SIDE LETTER (Fighter.apply's contract); the lab
     passed the Fighter. Entangle has no damage tick, so nothing reads it.
  8. THE GROWTH IS LINEAR, as priced ("eased" in the brief; the lab is linear).
  9. THE WITHER IS A PICTURE AFTER A MECHANICAL CLOSE (§6: reach back to 1 and
     the roots released "on close"); the wait it adds to the next cast cannot
     bind at charge 14 against 8 + 0.4.

THE CLOCK. The window, the growth, the sprout, the canopy cooldown and the
wither run on the window tickers' clock, which stops through a hit stop
(Corollary's, Daybreak's and Zenith's convention).

THE BASE is the chain tip, `sc-zenith.html`, named and asserted.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "ironwood"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling)
    "dur": 8,         # "the window 8s"
    "grow": 0.35,     # "reachMul eased at 0.35/s"
    "reachCap": 2.5,  # "to 2.5"
    "sprout": 1.5,    # "the two extra boughs sprout at 1.5s"
    "boughs": 3,      # "w.blades [0, 1/3, 2/3] for the window" -- stage 3
    "winDmg": 0.35,   # "blows at dmg x 0.35 while the tree stands" -- stage 3
    "canopy": 1,      # "entangle 1" -- stage 4
    "canopyCd": 0.5,  # "every 0.5s"
    "wither": 0.4,    # "the wither: 0.4s; the next cast waits for it"
}
TIP = "Takes root and grows three sweeping boughs. Foes beneath them entangle"
# Grudgebearer's hammer profile, the lab's donor (cell_ults_on.TYPE_DONOR) and
# the whole type's (all five shipped hammers carry it); dmg 23.5 is its blade.
DONOR_PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:23.50, spin:1.6, '
              'mode:"spin", mass:5.0, knockMul:2.3')
PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:23.5, spin:1.6, '
        'mode:"spin", mass:5.0, knockMul:2.3')
HAMMERS = ("grudgebearer", "censer", "bulwarden", "shroudmaul", "ravelbone")
VERDANT = ("thornwake", "heartwood", "vinesower", "thornshear")
BLURB = ("A hammer that takes root and grows into a tree: three boughs sweep the "
         "hall, and whoever stands beneath them is entangled.")


def ult_block(charge, boughs, win_dmg, canopy) -> str:
    return (f'''    ult:{{ name:"Canopy", charge:{charge}, kind:"tree", dur:{ULT["dur"]},
          grow:{ULT["grow"]}, reachCap:{ULT["reachCap"]}, sprout:{ULT["sprout"]},
          boughs:{boughs},          // v69: the boughs (stage 3)
          winDmg:{win_dmg},       // v69: a blow while the tree stands (stage 3)
          canopy:{canopy},          // v69: the canopy (stage 4)
          canopyCd:{ULT["canopyCd"]}, wither:{ULT["wither"]},
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
# THE RELIC, APPENDED AFTER MORNINGSTAR, ITS ULTIMATE STUBBED at charge 1e9
# (the clock can never reach it, `fireUlt` never runs) -- Starwarden's stage-1
# pattern. Every other table keyed by relic id falls back.
ROW_ANCHOR = ('''    blurb:"A flail whose head becomes a sun: its light smites and burns, and every burn heals the one swinging it." },

];''')

S1 = [

("ironwood joins the roster, its ultimate stubbed",
 ROW_ANCHOR,
 ROW_ANCHOR[:-4] + f'''
  /* IRONWOOD / CANOPY (v69; built v99) -- THE VERDANT WARHAMMER, the 36th
     relic built. Grudgebearer's hammer profile and its blade, 23.5 (the lab's
     donor and the whole type's), and the school's channel, onHit entangle 2.
     Stage 1 stubs the ultimate at charge 1e9; stages 2-4 give it its root and
     growth, its boughs and its canopy, a few numbers at a time. */
  {{ id:"ironwood", name:"Ironwood", aff:"verdant", shape:"warhammer",
    {PHYS},
    onHit:{{ entangle:2 }},
{ult_block("1e9", 1, 1, 0)}
    blurb:"{BLURB}" }},

];'''),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the tree has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Canopy", charge:1e9, kind:"tree", dur:8,
''',
 f'''    ult:{{ name:"Canopy", charge:{ULT["charge"]}, kind:"tree", dur:{ULT["dur"]},   // v69 stage 2: the tree roots
'''),

("the fighter carries the tree",
 '''    this.ultSun = null;
    this.sunTally = null;
''',
 '''    this.ultSun = null;
    this.sunTally = null;
    /* {t, dur, cd, sprouted} while IRONWOOD stands as a tree (v69). null on
       every other relic and on this one outside its window: `tickTree` returns
       after a two-iteration loop that does nothing. `bladeSet` is the tree's
       own blade offsets once its boughs sprout -- `bladeSegments` and
       `drawWeapon` read it before `w.blades`, because `w` is shared with the
       other side of a mirror match and must never be written. `treeWither` is
       the seconds left of the wither, which the next cast waits for.
       `treeTally` is the probe's count, cumulative over the fight; nothing in
       the simulation reads it. */
    this.ultTree = null;
    this.bladeSet = null;
    this.treeWither = 0;
    this.treeTally = null;
'''),

("the cast roots the tree and resolves nothing",
 '''    if (u.kind === "sun"){
''',
 '''    if (u.kind === "tree"){
      /* CANOPY (v69). NOTHING RESOLVES HERE: the cast roots the hammer for
         `u.dur` seconds and `tickTree` does everything the window does. THE
         ROOT is Garrote's hold on the caster itself -- `pin` with `pinFree`,
         so the ball is held and the weapon keeps turning -- and `pinV` [0,0]
         is the rest it is released to. `cd` starts at zero, so a foe already
         under the canopy is entangled on the first frame. */
      f.ultTree = { t: 0, dur: u.dur, cd: 0, sprouted: 0 };
      f.pinV = [0, 0]; f.pin = u.dur; f.pinMax = u.dur; f.pinFree = 1;
      if (!f.treeTally)
        f.treeTally = { casts: 0, frames: 0, canopyFrames: 0, stacks: 0,
                        peak: 0, sprouts: 0 };
      f.treeTally.casts++;
      return;
    }
    if (u.kind === "sun"){
'''),

("the tree ticks with the window tickers",
 '''    this.tickSun(dt);                   // ZENITH (v71)
''',
 '''    this.tickSun(dt);                   // ZENITH (v71)
    this.tickTree(dt);                  // CANOPY (v69)
'''),

("a cast waits for the last tree's wither",
 '''    if (f.charge >= f.w.ult.charge && !f.ultCorona){
''',
 '''    /* AND FOR THE LAST TREE TO WITHER (v69: "the next cast waits for it").
       Both fields are null / 0 on every other relic. It cannot bind at the
       shipped numbers either: the charge is 14 and a tree and its wither are
       8.4. */
    if (f.charge >= f.w.ult.charge && !f.ultCorona && !f.ultTree && !f.treeWither){
'''),

("the boughs are the tree's own blades: the hit box",
 '''    const out = [];
    for (const off of f.w.blades){
      const a = f.theta + off * TAU;
      const ca = Math.cos(a), sa = Math.sin(a);
''',
 '''    const out = [];
    /* THE TREE'S BOUGHS (v69) are its own blade set, read before the
       weapon's: `bladeSet` is null on every other relic and on this one
       outside its window, and `w.blades` is shared by the mirror match. */
    for (const off of (f.bladeSet || f.w.blades)){
      const a = f.theta + off * TAU;
      const ca = Math.cos(a), sa = Math.sin(a);
'''),

("the boughs are the tree's own blades: the picture",
 '''    for (const off of f.w.blades){
      const a = f.theta + off * TAU;
      c.save();
''',
 '''    /* The tree's boughs (v69), exactly the set `bladeSegments` tests -- the
       picture and the hit box read the same array. */
    for (const off of (f.bladeSet || f.w.blades)){
      const a = f.theta + off * TAU;
      c.save();
'''),

("a blow while the tree stands is the hammer's x winDmg",
 '''    let dmg = self.w.dmg * (mul === undefined ? (forge ? self.w.ult.strikeMul : 1) : mul)
''',
 '''    /* THE TREE'S LIGHTER BLOWS (v69 §6): while Ironwood stands as a tree
       every blow is the hammer's x `winDmg`, applied to the blade itself,
       ahead of the jitter, the crit and the rounding -- where the lab scaled
       `w.dmg`, so a blow is bit-identical to what was priced. `ultTree` is
       null on every other relic, so their blows are the same product. */
    let dmg = (self.ultTree ? self.w.dmg * self.w.ult.winDmg : self.w.dmg)
            * (mul === undefined ? (forge ? self.w.ult.strikeMul : 1) : mul)
'''),

("tickTree roots, grows, sprouts and shades",
 '''  tickWinnow(dt){
''',
 '''  /* =================================================== THE TREE =======
     v69 §1 / §6, brief §0-§1. While the window runs:
       THE ROOT   `pin` re-armed to the window every frame, with `pinFree` --
                  `tickStasis` has just taken dt off it, and Ravelbone's wire
                  can clear `pinFree` on its quarry; the prose's weapon "can
                  still swing" the whole window.
       THE GROWTH `reachMul` += grow x dt, to reachCap. Every reach read site
                  carries it, so the hit box and the drawn haft grow together.
       THE SPROUT at `sprout` seconds the tree's blade set becomes `boughs`
                  evenly spaced offsets; the two new boughs get a ribbon and a
                  cooldown of their own, starting clear.
       THE CANOPY every `canopyCd` while the foe's centre is within reach x
                  mods.reach x reachMul + R of the caster: entangle `canopy`
                  (the real status; no damage, no knock, no beat). The cooldown
                  runs through the whole window, lit or not (the lab's cadence).
     CLOSE, by the clock or the caster's death: the boughs go (the blade set,
     the extra ribbons), reach returns to 1, and the roots let go -- a live
     caster to REST, a dead one keeping its kill flight (`tickStasis` has
     already released it). Then `wither` seconds that the next cast waits for.
     The target is the OPPONENT only. On the window tickers' clock, so all of
     it freezes through a hit stop. `apply`'s source is a side letter. */
  tickTree(dt){
    for (const f of [this.a, this.b]){
      if (f.treeWither > 0) f.treeWither = Math.max(0, f.treeWither - dt);
      const Z = f.ultTree;
      if (!Z) continue;
      const u = f.w.ult, T = f.treeTally;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive){
        f.ultTree = null;
        f.bladeSet = null;
        const n = f.w.blades.length;
        if (f.tips.length > n) f.tips.length = n;
        if (f.hitCd.length > n) f.hitCd.length = n;
        f.reachMul = 1;
        f.pin = 0; f.pinMax = 0; f.pinV = null; f.pinFree = 0;
        if (f.alive){ f.vx = 0; f.vy = 0; }
        f.treeWither = u.wither;
        continue;
      }
      const foe = f === this.a ? this.b : this.a;
      const R = CONFIG.physics.ballR;
      f.pin = Z.dur; f.pinMax = Z.dur; f.pinFree = 1;
      f.reachMul = Math.min(u.reachCap, f.reachMul + u.grow * dt);
      T.frames++;
      if (f.reachMul > T.peak) T.peak = f.reachMul;
      if (!f.bladeSet && u.boughs > 1 && Z.t >= u.sprout){
        f.bladeSet = Array.from({ length: u.boughs }, (_, i) => i / u.boughs);
        while (f.tips.length < u.boughs) f.tips.push([]);
        for (let i = 1; i < u.boughs; i++) f.hitCd[i] = 0;
        Z.sprouted = Z.t;
        T.sprouts++;
      }
      Z.cd -= dt;
      if (u.canopy > 0 && foe.alive){
        const reach = f.w.reach * this.actMods.reach * f.reachMul;
        if (Math.hypot(foe.x - f.x, foe.y - f.y) < reach + R){
          T.canopyFrames++;
          if (Z.cd <= 0){
            Z.cd = u.canopyCd;
            foe.apply("entangle", u.canopy, f === this.a ? "a" : "b");
            T.stacks += u.canopy;
          }
        }
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the boughs",
 '''          boughs:1,          // v69: the boughs (stage 3)
          winDmg:1,       // v69: a blow while the tree stands (stage 3)
''',
 f'''          boughs:{ULT["boughs"]},          // v69: the boughs (stage 3)
          winDmg:{ULT["winDmg"]},       // v69: a blow while the tree stands (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 4 --
S4 = [
("the canopy",
 '''          canopy:0,          // v69: the canopy (stage 4)
''',
 f'''          canopy:{ULT["canopy"]},          // v69: the canopy (stage 4)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BOUGH SCALE AND THE BLADE (brief §2 stage 5: "If out of band move
# `winDmg` inside 0.30-0.40 first and say so"). At the designed 0.35 the
# crossing is blade 25.0, both sides (23.5 -> 44.4, 24.5 -> 46.6, 25 -> 49.9),
# outside the brief's 23.5-24.5. At 0.38 it is 24.0 (23.5 -> 48.9, 24 -> 50.1,
# 24.5 -> 52.9), where design §5 puts it ("the crossing is near 24"). Why the
# built relic reads under the lab at 0.35 is measured in v99 §4: the canopy's
# cadence runs on the window clock, which stops in a hit stop, and the lab's
# ran through them.
TUNED = {"winDmg": 0.38, "dmg": 24}

S5 = [
("the bough scale: the build's knob, inside 0.30-0.40",
 f'''          winDmg:{ULT["winDmg"]},       // v69: a blow while the tree stands (stage 3)
''',
 f'''          winDmg:{TUNED["winDmg"]},       // v69: a blow while the tree stands (stage 3); stage 5: {ULT["winDmg"]} -> {TUNED["winDmg"]}, the build's knob
'''),
("the blade: at the crossing",
 '''  { id:"ironwood", name:"Ironwood", aff:"verdant", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:23.5,''',
 f'''  {{ id:"ironwood", name:"Ironwood", aff:"verdant", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:{TUNED["dmg"]},'''),
]

STAGE_OUT = {"1": "sc-ironwood", "2": "sc-rooted", "3": "sc-boughs", "4": "sc-canopy",
             "5": "sc-canopy-w38"}


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
    print(f"\nIRONWOOD / CANOPY -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS NAMED AND ASSERTED: the chain tip, which carries Morningstar
    # through its stage 4.
    for need, why in (('name:"Zenith", charge:14', "no Zenith at charge 14"),
                      ("tickSun(dt){", "no tickSun -- not the chain tip"),
                      ("bless:1,", "no Zenith stage 4 -- not the chain tip")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    # AND THE TYPE'S HAMMER PROFILE IS STILL WHAT THIS BUILDER COPIES: the
    # donor's exactly, and the same numbers on every shipped hammer.
    if DONOR_PHYS not in relic_row(code, "grudgebearer"):
        raise SystemExit("Grudgebearer's hammer profile has moved -- the donor "
                         "is not what this builder copies")
    for h in HAMMERS:
        row = " ".join(relic_row(code, h).split())
        if not re.search(r'shape:"warhammer",\s*blades:\[0\], reach:76, width:26, '
                         r'artW:54, dmg:[\d.]+, spin:1\.6, mode:"spin", mass:5\.0, '
                         r'knockMul:2\.3', row):
            raise SystemExit(f"{h} is not the type's hammer profile any more")
    for v in VERDANT:
        if "onHit:{ entangle:2 }" not in relic_row(code, v):
            raise SystemExit(f"{v} does not carry the school's channel, entangle 2")
    if not re.search(r'if \(key === "verdant"\)\s+return SHAPES\._whGrown\(', code):
        raise SystemExit("SHAPES.warhammer no longer routes verdant to _whGrown")
    print("  base  the chain tip (Zenith stage 4); the five hammers' profile, the "
          "four verdant channels and the verdant silhouette hold")

    if A.stage == "1":
        if f'id:"{RELIC}"' in code:
            raise SystemExit("this source already carries Ironwood -- built")
        edits, want = S1, ult_block("1e9", 1, 1, 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultTree" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            edits, want = S2, ult_block(ULT["charge"], 1, 1, 0)
        elif A.stage == "3":
            if "ultTree" not in code or "boughs:1," not in code:
                raise SystemExit("stage 3 needs stage 2 under it")
            edits, want = S3, ult_block(ULT["charge"], ULT["boughs"], ULT["winDmg"], 0)
        elif A.stage == "4":
            if f'boughs:{ULT["boughs"]},' not in code:
                raise SystemExit("stage 4 needs stage 3 under it")
            edits, want = S4, ult_block(ULT["charge"], ULT["boughs"], ULT["winDmg"],
                                        ULT["canopy"])
        else:
            if f'canopy:{ULT["canopy"]},' not in code or f'winDmg:{ULT["winDmg"]},' not in code:
                raise SystemExit("stage 5 goes on stage 4, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["boughs"], TUNED["winDmg"],
                                        ULT["canopy"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Ironwood's ult block is not "
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
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the RNG")
        if re.search(r"\bw\.(blades|dmg|reach)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
    if len(re.findall(r'kind:"tree"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one tree ultimate")
    # THE REACH THE TREE GROWS IS READ WHERE IT MATTERS (the brief's refusal,
    # scoped: four shipped reads -- card art, a spectre -- never carried it).
    if A.stage != "1":
        for site, pat in (("bladeSegments", r"bladeSegments\(f\)\{[\s\S]*?const reach = f\.w\.reach \* mods\.reach \* f\.reachMul;"),
                          ("drawWeapon", r"drawWeapon\(m, f\)\{[\s\S]{0,400}?const reach = f\.w\.reach \* m\.actMods\.reach \* f\.reachMul;"),
                          ("the canopy", r"tickTree\(dt\)\{[\s\S]*?const reach = f\.w\.reach \* this\.actMods\.reach \* f\.reachMul;")):
            if not re.search(pat, out_code):
                raise SystemExit(f"REFUSING TO WRITE -- {site}'s reach does not "
                                 "carry reachMul")
        print("  ok    reachMul at the hit box, the drawn weapon and the canopy")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one tree ultimate, Ironwood's; no insert draws the RNG or "
          f"writes the shared weapon; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
