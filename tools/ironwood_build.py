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
    stage 6   picture, voice              -> sc-canopy-fx.html (no field: drawn leaves, v99 §6)

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

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v69 §7.1-7.2), picked on measurements under
# Rick's "you pick i overrule" by `ironwood_voice_lab.py` and the picture lab
# (v99 §6). Presentation only: engine_ab over all 36 relics, Ironwood
# included, is the proof. The rows are byte-exact to the labs' own files.
S6 = [

('Sfx: the bough blow -- a branch in front of the hit arm, taken only with `bough`',
 '''      if (kind === "hit"){''',
 '''      if (kind === "hit" && p.bough){
        /* CANOPY'S BOUGH BLOW -- v69 §7.2: "the hammer's own strike voice,
           pitched down a fourth and quieter (peak <= 0.6 of the hammer's) -- a
           lighter head on a longer arm". PITCH, of 4, picked on the numbers by
           `ironwood_voice_lab.py` under Rick's "you pick i overrule" (v99).
           `resolveHit` adds `bough` (the tree's damage scale, 0.38) only while
           Ironwood's tree stands, so every other call takes the old arm below,
           byte for byte.

           The HAMMER'S strike, not the light one: `dmg / bough` is the blow
           the hammer would have struck, so the weight, the jitter and the
           crits are the hammer's -- the plain hit at the bough's 9 would be
           pitched UP (+286 cents). Every frequency x 0.75: measured -486 cents
           on the noise crack and -501 cents on the body's start; peak 0.44 of
           the hammer's on the same draw (0.55 at the worst draw, jitter or
           crit), loudest 50 ms +15.5 dB over the wall tick. Envelope
           correlation 1.00 with the hammer's own strike. */
        const w = clamp((p.dmg || 10) / p.bough / 45, 0.12, 1), k = 0.75, v = 0.3246;
        this._burst(t, { freq: (2600 - 1500*w) * k, q: 1.1, gain: (0.16 + 0.20*w) * v, dur: (0.06 + 0.06*w) });
        this._tone (t, { freq: (190 - 90*w) * k, to: 46 * k, gain: (0.22 + 0.26*w) * v, dur: (0.11 + 0.13*w), type:"sine" });
        if (p.crit) this._tone(t, { freq: 1500 * k, to: 520 * k, gain: 0.16 * v, dur: 0.16, type:"triangle" });
      }
      else if (kind === "hit"){'''),

("Sfx: Ironwood's cast, sprout and wither arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "ironwood"){                   // the hammer takes root
          /* IRONWOOD'S CAST, THE ROOTING -- v69 §7.2: "a deep creak and a
             ground-thud, 0.5s, share below 120 Hz >= 0.5 -- the heaviest thing
             in the hall is putting down roots". BEAM, of 5, picked on the
             numbers by `ironwood_voice_lab.py` under Rick's "you pick i
             overrule" (v99). Ironwood had no arm and fell through to
             rune-crack, which Censer, Lastlight and Aureole still use, so this
             ADDS arms before that fallback and leaves it alone.

             The thud lands on the cast frame, where the ball stops dead: a
             sine falling 72 -> 28 Hz and a 140 Hz lowpass burst. The creak is
             a timber ringing (a 520 Hz sine and its 2.76 mode at 0.4) pulsed
             slowing from 50 to 25 a second over 0.45 s -- a held note does not
             exist in this toolkit (CLAUDE.md 4.5), and a creak is stick-slip,
             so it is a train of pulses; each interval x (1 + 0.12 sin 2.4k)
             keeps it irregular with no random number. 0.60 of its power below
             120 Hz at the worst noise draw; audible 475 ms; its loudest 50 ms
             -2.9 dB re Ironwood's blow. Register 0.30 against rune-crack, at
             most 0.67 against the warhammer row's casts, 0.35 against the
             death voice. */
          const g = 0.1235, kc = 0.7584;
          this._tone (t, { freq: 72, to: 28, gain: g, dur: 0.4, type:"sine" });
          this._burst(t, { freq: 140, q: 0.7, gain: g * 0.6, dur: 0.18, type:"lowpass" });
          for (let s = 0.03, k = 0; s < 0.48; k++){
            const u = (s - 0.03) / 0.45, a = g * kc * (0.55 + 0.45 * Math.sin(Math.PI * u));
            this._tone(t + s, { freq: 520, gain: a, dur: 0.03, type:"sine" });
            this._tone(t + s, { freq: 1435, gain: a * 0.4, dur: 0.02, type:"sine" });
            s += 0.02 * Math.pow(2, u) * (1 + 0.12 * Math.sin(k * 2.4));
          }
        } else if (w === "ironwood-sprout"){            // two boughs break out
          /* THE SPROUT -- "two quick woody cracks, 80ms each, a fifth apart"
             (v69 §7.2). BLOCK, of 4 (`ironwood_voice_lab.py`). `tickTree`
             plays it on the frame the blade set appears, when the two new
             boughs are live. A then E (the score's i and v), rising, the
             second crack 90 ms after the first: pitches 880-1320 Hz, each
             crack audible 80/75 ms, loudest 50 ms -9.4 dB re the blow and
             +12.2 dB re the wall tick; register at most 0.44 against the blow,
             the bough, the cast and rune-crack. */
          const g = 0.1054, D = 0.133;
          for (const [s, f] of [[0, 880], [0.09, 880 * 1.5]]){
            this._tone(t + s, { freq: f, gain: g, dur: D, type:"triangle" });
            this._tone(t + s, { freq: f * 2.76, gain: g * 0.3, dur: D * 0.5, type:"sine" });
            this._burst(t + s, { freq: f * 3, q: 1.5, gain: g * 0.8, dur: 0.008, type:"bandpass" });
          }
        } else if (w === "ironwood-wither"){            // and the tree lets go
          /* THE WITHER -- "a dry creak falling in pitch, 0.4s, quiet" (v69
             §7.2). BEAM, of 4 (`ironwood_voice_lab.py`): a pulse train slowing
             from 55 to 24 a second, its pitch falling -861 cents, audible 360
             ms, 0.06 of its power below 120 Hz (dry, where the cast is deep),
             -9.0 dB under the cast's top. `tickTree` plays it only when the
             window closes by its clock with the caster alive, never on a
             death. */
          const g = 0.0902;
          for (let s = 0, k = 0; s < 0.37; k++){
            const u = s / 0.4, f = 780 * Math.pow(360 / 780, u), a = g * (1 - 0.6 * u);
            this._tone(t + s, { freq: f, gain: a, dur: 0.02, type:"sine" });
            this._tone(t + s, { freq: f * 2.76, gain: a * 0.4, dur: 0.014, type:"sine" });
            s += 0.018 * Math.pow(2.3333, u) * (1 + 0.12 * Math.sin(k * 2.4));
          }
        } else {                                        // rune-crack'''),

('tickTree: the sprout voice, on the frame the blade set appears',
 '''        T.sprouts++;''',
 '''        T.sprouts++;
        /* CANOPY'S SPROUT (v69 §7.2: "two quick woody cracks, 80ms each, a
           fifth apart"): on the frame the two new boughs exist and are live.
           Presentation only: SFX.play draws nothing, is a no-op headless, and
           nothing here is read back (ironwood_voice_lab: fights identical). */
        SFX.play("ult", { w: "ironwood-sprout" });'''),

('tickTree: the wither voice, when the window closes by its clock with the caster alive',
 '''        f.treeWither = u.wither;''',
 '''        f.treeWither = u.wither;
        /* CANOPY'S WITHER (v69 §7.2: "a dry creak falling in pitch, 0.4s,
           quiet"): only when the window runs out BY ITS CLOCK with the caster
           alive. A caster's death ends the fight on this frame, and a foe's
           death ends it before any close (step() stops calling this), so both
           endings are left to the death voice, as Zenith's and Daybreak's
           closes are. Plain SFX.play; nothing is read back. */
        if (f.alive && Z.t >= Z.dur) SFX.play("ult", { w: "ironwood-wither" });'''),

('resolveHit: the hit voice carries `bough` while the tree stands',
 '''    SFX.play("hit", { dmg, crit });''',
 '''    /* CANOPY'S BOUGH BLOW (v69 §7.2): while Ironwood stands as a tree the
       blow's voice is the hammer's strike pitched down a fourth and quieter.
       ONE plain number more, `bough` (the tree's damage scale), so the hit
       arm can rebuild the hammer's weight from the damage dealt; `dmg` stays
       what was dealt. `ultTree` is null on every other relic and outside the
       window, so every other call is the old one. Presentation only
       (ironwood_voice_lab: fights identical). */
    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });'''),

('canopy picture: fighter fields',
 '''    this.treeWither = 0;
    this.treeTally = null;
''',
 '''    this.treeWither = 0;
    this.treeTally = null;
    /* CANOPY'S PICTURE (v69 section 7.1), and none of it is the window: the
       tree outlives `ultTree` by the 0.4s it takes to wither, so the picture
       keeps its own state. On the FIGHTER and never on `m.ultFx` (one slot,
       and the opponent's cast takes it: open item 25). Driven in
       `tickPresentation`; nothing in the simulation reads any of it.
         treeFade -- 1 while the tree stands; eased to 0 over the wither
           after the close, the caster's fall or the match's end
         treeAge -- the presentation clock since the cast (the bark's climb)
         treeOut -- the presentation clock since the close (the wither)
         treeGrow -- each bough's drawn share of its length: the trunk 1, a
           sprouting bough 0 -> 1 over the sprout, or 1 the frame it strikes
           or clanks (it was live all along)
         treeSnap -- the boughs that have struck or clanked while sprouting
         treeCd -- the last `hitCd` seen per bough (a rise is a blow)
         treeClk -- the last clank count seen
         treeL -- each bough's drawn length at the last standing frame, so
           the wither draws back from where the tree stood
         treeSeen -- canopy applications already shown (`treeTally.stacks`)
         treeTagged -- this stretch under the canopy has had its ENTANGLE tag
         treeDead -- the window ended on the caster's death: no bark falls
           (the shatter owns the ball)
         treeLeaves -- leaf motes shed off the bough tips (records)
         treeBits -- bark falling off the shell in the wither (records)
         treeLeafN, treeLeafAcc -- the motes' count and spawn accumulator */
    this.treeFade = 0;
    this.treeAge = 0;
    this.treeOut = 0;
    this.treeGrow = [1, 0, 0];
    this.treeSnap = [1, 0, 0];
    this.treeCd = [0, 0, 0];
    this.treeClk = 0;
    this.treeL = [0, 0, 0];
    this.treeSeen = 0;
    this.treeTagged = false;
    this.treeDead = false;
    this.treeLeaves = [];
    this.treeBits = [];
    this.treeLeafN = 0;
    this.treeLeafAcc = 0;
'''),

('canopy picture: the presentation clock',
 '''                             : Math.max(0, f.sunLitFade - dt / 0.5);
      }
''',
 '''                             : Math.max(0, f.sunLitFade - dt / 0.5);
      }
      /* AND THE TREE'S (v69 section 7.1). HALF-SECONDS, like every `life`
         in this method (it runs twice a normal step): 0.8 is the bark's 0.4s
         climb and 0.8 the wither's 0.4s. The growth, the sprout and the canopy
         are read off the window itself, so they hold still through a hit stop
         exactly as the hit box does; the bark, the leaves and the wither keep
         playing on this clock. Not after the match, and not once the caster
         falls: `tickTree` never runs again once `over` is set, so a tree
         standing at the kill would otherwise stand through the verdict. */
      { const Z = (this.over || !f.alive) ? null : f.ultTree;
        const foe = f === this.a ? this.b : this.a, Rb = CONFIG.physics.ballR;
        if (Z){
          if (!(f.treeFade > 0) || f.treeOut > 0){  // a new tree
            f.treeAge = 0; f.treeOut = 0; f.treeDead = false; f.treeTagged = false;
            f.treeSnap = [1, 0, 0]; f.treeCd = [0, 0, 0]; f.treeClk = f.clanks;
            f.treeBits.length = 0;
          }
          f.treeFade = 1;
          f.treeAge += dt;
          const reach = f.w.reach * this.actMods.reach * f.reachMul;
          const S = f.bladeSet || f.w.blades;
          /* A BOUGH THAT CONNECTS IS DRAWN WHOLE. The two new boughs are live
             at full reach from the frame they exist and are drawn growing over
             0.5s of the window; a blow (its `hitCd` rises) or a clank against
             one while it is drawn short snaps it to full length on that frame,
             so no contact is ever made by wood the viewer cannot see. */
          const sp = Z.sprouted > 0 ? Math.min(1, (Z.t - Z.sprouted) / 0.5) : 0;
          if (f.bladeSet){
            for (let i = 1; i < S.length && i < 3; i++){
              const cd = f.hitCd[i] || 0;
              if (cd > f.treeCd[i] + 1e-9) f.treeSnap[i] = 1;
              f.treeCd[i] = cd;
            }
            if (f.clanks !== f.treeClk && sp < 1 && foe.alive){
              const segs = this.bladeSegments(foe);
              const touch = (f.w.width + foe.w.width) * 0.5 + CONFIG.clank.pad;
              for (let i = 1; i < S.length && i < 3; i++){
                const q = f.theta + S[i] * TAU, cq = Math.cos(q), sq = Math.sin(q);
                for (const g of segs)
                  if (segSegDist(f.x + cq * (Rb - 4), f.y + sq * (Rb - 4),
                                 f.x + cq * (Rb + reach), f.y + sq * (Rb + reach),
                                 g.ax, g.ay, g.bx, g.by).d < touch) f.treeSnap[i] = 1;
              }
            }
          }
          f.treeClk = f.clanks;
          const e = 1 - (1 - sp) * (1 - sp) * (1 - sp);
          for (let i = 0; i < 3; i++){
            f.treeGrow[i] = i === 0 ? 1 : (!f.bladeSet || i >= S.length ? 0
                          : (f.treeSnap[i] ? 1 : e));
            f.treeL[i] = (reach + 6) * f.treeGrow[i];
          }
          /* THE CANOPY'S TAG, once a stretch (Corona's, Daybreak's and
             Zenith's rule): the first application while the foe is under the
             canopy tags ENTANGLE and its count on the foe; the flag re-arms the
             first frame it is out. `treeTally.stacks` counts the applications,
             so this reads the one `tickTree` made rather than guessing it. */
          const T = f.treeTally;
          const inside = foe.alive && Math.hypot(foe.x - f.x, foe.y - f.y) < reach + Rb;
          if (!inside) f.treeTagged = false;
          if (T && T.stacks !== f.treeSeen){
            f.treeSeen = T.stacks;
            if (!f.treeTagged && foe.hp > 0){
              f.treeTagged = true;
              const first = !this.taught.entangle && !!STATUS.entangle.tip;
              if (first) this.taught.entangle = true;
              this.statusTag(foe.x, foe.y, "entangle", first, foe.stacks("entangle"));
            }
          }
          /* LEAF MOTES off the burl of every bough that has grown out. Placed
             by shellHash on their count: no rng. */
          f.treeLeafAcc += dt * 2.0;
          while (f.treeLeafAcc >= 1){
            f.treeLeafAcc -= 1;
            for (let i = 0; i < S.length && i < 3; i++){
              if (!(f.treeGrow[i] > 0.5)) continue;
              const q = f.theta + S[i] * TAU, rr = Rb - 6 + f.treeL[i] - f.w.artW * 0.3;
              f.treeLeaves.push({ x: f.x + Math.cos(q) * rr, y: f.y + Math.sin(q) * rr,
                                  t: 0, n: f.treeLeafN++ });
            }
          }
          if (f.treeLeaves.length > 60) f.treeLeaves.splice(0, f.treeLeaves.length - 60);
        } else if (f.treeFade > 0){
          const o0 = f.treeOut;
          if (!(o0 > 0)) f.treeDead = !f.alive;
          f.treeFade = Math.max(0, f.treeFade - dt / 0.8);
          f.treeOut += dt;
          /* THE BARK CRACKS AND FALLS: each plate lets go at its own moment
             in the first half of the wither and drops as drawn debris, from
             where the shell is now. Not on a death (the shatter owns it). */
          if (!f.treeDead && f.alive){
            const B = treeBark(f.side);
            for (const pl of B.plates){
              if (!(pl.drop > o0 && pl.drop <= f.treeOut)) continue;
              const px = f.x + pl.cx * Rb, py = f.y + pl.cy * Rb;
              const dl = Math.hypot(pl.cx, pl.cy) || 1;
              f.treeBits.push({ x: px, y: py, vx: pl.cx / dl * pl.kick, vy: pl.cy / dl * pl.kick - 40,
                                t: 0, life: 1.1, j: pl.j });
            }
          }
        }
        for (let i = f.treeLeaves.length - 1; i >= 0; i--){
          f.treeLeaves[i].t += dt;
          if (f.treeLeaves[i].t >= 2.6) f.treeLeaves.splice(i, 1);
        }
        for (let i = f.treeBits.length - 1; i >= 0; i--){
          const d = f.treeBits[i];
          d.t += dt;
          if (d.t >= d.life) f.treeBits.splice(i, 1);
        }
      }
'''),

('canopy picture: the bark plates',
 '''const _glowCache = new Map();
''',
 '''/* CANOPY'S BARK (v69 section 7.1): the plates that grow up Ironwood's shell,
   in the unit disc. Vertical fissures (shared, wavy, so neighbouring plates
   meet on one seam) cut by staggered cross-breaks: bark, not a grid. Each
   plate carries the moment it lets go in the wither and the kick it leaves
   with. A pure function of the side through shellHash -- no rng -- built
   once per side and read by the Match (the falling bits) and the renderer. */
const _barkCache = {};
function treeBark(side){
  if (_barkCache[side]) return _barkCache[side];
  const plates = [], NC = 7, x0 = -1.22, cw = 2.44 / NC;
  /* the fissures: shared by the two plates either side, and wavy */
  const fx = (ci, y) => x0 + ci * cw + (ci === 0 || ci === NC ? 0
    : 0.075 * Math.sin(y * 4.3 + ci * 1.9 + side * 0.9) + 0.035 * Math.sin(y * 9.7 + ci * 2.3));
  let j = 0;
  for (let ci = 0; ci < NC; ci++){
    let y = -1.3 - 0.5 * shellHash(9501 + side, ci), sl = 0;
    while (y < 1.2){
      const y2 = y + 0.62 + 0.40 * shellHash(9503 + side, ci * 8 + j);
      const s2 = (shellHash(9505 + side, j) - 0.5) * 0.30;  // the cross-break slants
      const pts = [];
      for (let k = 0; k <= 2; k++){ const yy = (y + sl) + ((y2 + s2) - (y + sl)) * k / 2; pts.push([fx(ci, yy), yy]); }
      for (let k = 2; k >= 0; k--){ const yy = (y - sl) + ((y2 - s2) - (y - sl)) * k / 2; pts.push([fx(ci + 1, yy), yy]); }
      let cx = 0, cy = 0;
      for (const q of pts){ cx += q[0] / pts.length; cy += q[1] / pts.length; }
      if (Math.hypot(cx, cy) < 1.10)
        plates.push({ pts, cx, cy, j, drop: 0.06 + 0.42 * shellHash(9507 + side, j),
                      kick: 50 + 70 * shellHash(9509 + side, j), spin: (shellHash(9511, j) - 0.5) * 9 });
      y = y2; sl = s2; j++;
    }
  }
  return (_barkCache[side] = { plates });
}

const _glowCache = new Map();
'''),

('canopy picture: the verdant hammer (silhouette + grown tree)',
 '''  _whGrown(c, L, W, p){
    const hh = W * 0.50;
    const wood = SHAPES._shade(p.dark, 1.30, 0.22);
    c.lineCap = "round"; c.lineJoin = "round";

    c.strokeStyle = wood; c.lineWidth = W*0.15;                // the branch
    c.beginPath();
    c.moveTo(0, W*0.04);
    c.quadraticCurveTo(L*0.34, -W*0.13, L*0.62, W*0.02);
    c.stroke();
    c.lineWidth = W*0.075;                                     // the fork
    c.beginPath();
    c.moveTo(L*0.40, -W*0.055);
    c.quadraticCurveTo(L*0.56, -W*0.30, L*0.70, -hh*0.52);
    c.stroke();
    c.beginPath();
    c.moveTo(L*0.44, W*0.05);
    c.quadraticCurveTo(L*0.60, W*0.30, L*0.72, hh*0.50);
    c.stroke();

    for (const [tx, ty, r] of [[0.22,-1,1], [0.33,1,-1]]){      // leaves, out
      c.save();
      c.translate(L*tx, ty * W*0.10);
      c.rotate(ty * 0.85);
      c.fillStyle = p.core;
      c.beginPath();
      c.moveTo(0, 0);
      c.quadraticCurveTo(L*0.10, -W*0.14*r, L*0.22, 0);
      c.quadraticCurveTo(L*0.10,  W*0.14*r, 0, 0);
      c.closePath(); c.fill();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W*0.022);
      c.beginPath(); c.moveTo(0,0); c.lineTo(L*0.21, 0); c.stroke();
      c.restore();
    }

    c.beginPath();                                              // the burl
    c.moveTo(L*0.62, -hh*0.30);
    c.bezierCurveTo(L*0.68, -hh*1.16, L*0.96, -hh*1.02, L*1.00, -hh*0.34);
    c.bezierCurveTo(L*1.04,  hh*0.28, L*0.92,  hh*1.12, L*0.74,  hh*0.94);
    c.bezierCurveTo(L*0.64,  hh*0.84, L*0.60,  hh*0.30, L*0.62, -hh*0.30);
    c.closePath();
    const g = c.createLinearGradient(0, -hh, 0, hh);
    g.addColorStop(0, p.steel);
    g.addColorStop(0.5, SHAPES._shade(p.steel, 0.60, 0.45));
    g.addColorStop(1,   SHAPES._shade(p.steel, 0.32, 0.45));
    c.fillStyle = g; c.fill();
    c.strokeStyle = SHAPES._shade(p.dark, 1.0, 0.10);
    c.lineWidth = Math.max(1, W*0.05); c.stroke();

    c.strokeStyle = p.core + "99";                              // grain rings
    c.lineWidth = Math.max(1, W*0.030);
    for (const rr of [0.30, 0.52]){
      c.beginPath(); c.ellipse(L*0.82, 0, hh*rr*0.72, hh*rr, 0, 0, TAU); c.stroke();
    }

    c.fillStyle = p.glow;                                       // three thorns
    for (const ty of [-0.58, 0, 0.58]){
      c.beginPath();
      c.moveTo(L*0.98, hh*ty - hh*0.13);
      c.lineTo(L*1.16, hh*ty * 1.22);
      c.lineTo(L*0.98, hh*ty + hh*0.13);
      c.closePath(); c.fill();
    }
  },

''',
 '''  _whGrown(c, L, W, p, k, g, hs){
    /* v69 section 7.1, THE SILHOUETTE -- "a knotted burl head on a barked
       haft" -- and the first time this route is ever drawn (Ironwood is the
       school's first warhammer). Two changes to the first cut, measured at
       the app's 453x805:
         THE HEAD IS SIZED OFF THE WIDTH, NOT THE LENGTH. Every number here
         scaled by L, so Canopy's growth (reach x2.5) drew the burl 2.5x long:
         an egg on a stick. The haft now runs to wherever L puts the hit
         segment's tip and the burl stays a burl at its end.
         KNOTTED, NOT RINGED. Concentric rings on a smooth oval read as a
         target; the outline is lumped, the grain crowds round one whorl,
         and the haft carries two fissures and a lit ridge.
       `g` (0..1) thickens the haft into a trunk and `hs` scales the head;
       both are Canopy's (`drawTreeWeapon`) and undefined on every other call,
       so the resting hammer, its glow sprite and its lit scratch are g 0,
       hs 1. */
    g = g || 0; hs = hs === undefined ? 1 : hs;
    const hh = W * 0.50 * hs, HL = W * 0.62 * hs;  // head half-height, head length
    const xf = L, xb = L - HL, xc = L - HL * 0.5;  // face, back, centre
    const wood = SHAPES._shade(p.dark, 1.30, 0.22);
    const hw = W * (0.15 + 0.22 * g);  // the haft, to a trunk
    const xe = xb + HL * 0.18, bend = -W * (0.13 + 0.06 * g);
    c.lineCap = "round"; c.lineJoin = "round";
    const haft = (dy) => { c.beginPath(); c.moveTo(0, W * 0.04 + dy);
      c.quadraticCurveTo(xe * 0.55, bend + dy, xe, W * 0.02 + dy); };
    c.strokeStyle = wood; c.lineWidth = hw; haft(0); c.stroke();  // the branch
    c.strokeStyle = SHAPES._shade(p.dark, 0.55, 0.10);  // two fissures
    c.lineWidth = Math.max(1, hw * 0.13);
    haft(-hw * 0.18); c.stroke(); haft(hw * 0.22); c.stroke();
    c.strokeStyle = SHAPES._shade(p.dark, 2.6, 0.30);  // the lit ridge
    c.lineWidth = Math.max(0.8, hw * 0.09);
    haft(-hw * 0.36); c.stroke();
    c.strokeStyle = wood; c.lineWidth = hw * 0.5;  // the fork grips the burl
    c.beginPath(); c.moveTo(xb - HL * 0.75, -W * 0.05);
    c.quadraticCurveTo(xb - HL * 0.25, -hh * 0.62, xb + HL * 0.20, -hh * 0.62); c.stroke();
    c.beginPath(); c.moveTo(xb - HL * 0.65, W * 0.05);
    c.quadraticCurveTo(xb - HL * 0.20, hh * 0.60, xb + HL * 0.26, hh * 0.58); c.stroke();

    const lw = W * 0.33;  // leaves, out
    for (let j = 0, x = W * 0.33; x < xb - HL * 0.55; j++, x += 12 + 22 * g){
      const ty = j % 2 ? 1 : -1;
      c.save();
      c.translate(x, ty * Math.max(W * 0.10, hw * 0.45));
      c.rotate(ty * 0.85);
      c.fillStyle = p.core;
      c.beginPath(); c.moveTo(0, 0);
      c.quadraticCurveTo(lw * 0.45, -W * 0.14, lw, 0);
      c.quadraticCurveTo(lw * 0.45, W * 0.14, 0, 0);
      c.closePath(); c.fill();
      c.strokeStyle = p.glow; c.lineWidth = Math.max(1, W * 0.022);
      c.beginPath(); c.moveTo(0, 0); c.lineTo(lw * 0.95, 0); c.stroke();
      c.restore();
    }

    const B = [1.00, 0.88, 1.08, 0.92, 1.05, 0.93, 1.09, 0.89, 1.04, 0.95];
    c.beginPath();  // the burl, knotted
    const pt = (j) => { const q = (j % 10) * TAU / 10, b = B[j % 10];
      return [Math.min(xf, xc + Math.cos(q) * HL * 0.56 * b), Math.sin(q) * hh * 1.06 * b]; };
    const md = (j) => { const u = pt(j), v = pt(j + 1); return [(u[0] + v[0]) / 2, (u[1] + v[1]) / 2]; };
    const m0 = md(9); c.moveTo(m0[0], m0[1]);
    for (let j = 0; j < 10; j++){ const u = pt(j), v = md(j); c.quadraticCurveTo(u[0], u[1], v[0], v[1]); }
    c.closePath();
    const gr = c.createLinearGradient(0, -hh, 0, hh);
    gr.addColorStop(0, p.steel);
    gr.addColorStop(0.5, SHAPES._shade(p.steel, 0.60, 0.45));
    gr.addColorStop(1, SHAPES._shade(p.steel, 0.32, 0.45));
    c.fillStyle = gr; c.fill();
    c.strokeStyle = SHAPES._shade(p.dark, 1.0, 0.10);
    c.lineWidth = Math.max(1, W * 0.05 * Math.max(0.6, hs)); c.stroke();

    /* THE KNOTTING IS IN THE GRAIN, NOT IN HOLES: contorted grain lines
       crowding round one whorl, in the burl's own darker tone. Dark ovals in
       a pale head (the first cut's rings, then two knots) read as a face. */
    c.strokeStyle = SHAPES._shade(p.steel, 0.38, 0.45);
    c.lineWidth = Math.max(1, W * 0.026 * hs);
    const wx = xb + HL * 0.40, wy = -hh * 0.22;  // the whorl
    c.beginPath();
    c.ellipse(wx, wy, HL * 0.10, hh * 0.08, 0.6, 0, TAU);
    c.moveTo(wx - HL * 0.30, wy + hh * 0.30);
    c.bezierCurveTo(wx - HL * 0.12, wy - hh * 0.30, wx + HL * 0.22, wy - hh * 0.26, wx + HL * 0.40, wy + hh * 0.02);
    c.moveTo(xb + HL * 0.10, hh * 0.46);
    c.bezierCurveTo(wx - HL * 0.05, hh * 0.10, wx + HL * 0.28, hh * 0.20, xf - HL * 0.08, hh * 0.50);
    c.moveTo(xb + HL * 0.16, -hh * 0.70);
    c.quadraticCurveTo(wx + HL * 0.05, -hh * 0.62, xf - HL * 0.14, -hh * 0.66);
    c.stroke();

    c.fillStyle = p.glow;  // three thorns
    for (const ty of [-0.58, 0, 0.58]){
      c.beginPath();
      c.moveTo(xf - HL * 0.05, hh * ty - hh * 0.13);
      c.lineTo(xf + HL * 0.42, hh * ty * 1.22);
      c.lineTo(xf - HL * 0.05, hh * ty + hh * 0.13);
      c.closePath(); c.fill();
    }
  },

'''),

('canopy picture: the ground call',
 '''    if (__world) this.drawSun(m);
''',
 '''    if (__world) this.drawSun(m);
    /* CANOPY'S GROUND (v69 section 7.1): the canopy's disc and its leaf edge,
       the roots, the falling leaves. The WORLD pass and under both balls --
       the disc lies under the caster's shell and the foe's (CLAUDE.md
       section 4.1b), and nothing of it reaches the bloom (section 4.1c). */
    if (__world) this.drawTree(m);
'''),

('canopy picture: the falling bark call',
 '''    this.drawEchoGhost(m);
''',
 '''    this.drawEchoGhost(m);
    /* CANOPY'S BARK FALLING OFF THE SHELL, over both fighters: it leaves the
       shell, so it is in front of it. World pass, like the ghost blade. */
    this.drawTreeTop(m);
'''),

('canopy picture: the bark on the glass',
 '''    drawGlassRelic(c, m, f, R, { base: CONFIG.combat.baseHP });
''',
 '''    drawGlassRelic(c, m, f, R, { base: CONFIG.combat.baseHP });
    this._drawBark(m, f, c);  // CANOPY'S BARK, on the glass (v69 section 7.1)
'''),

("canopy picture: drawWeapon's hook",
 '''    /* The tree's boughs (v69), exactly the set `bladeSegments` tests -- the
''',
 '''    /* CANOPY'S TREE (v69 section 7.1): while it stands and while it withers
       the tree draws itself (`drawTreeWeapon`), off the same blade set, reach
       and angles `bladeSegments` tests. `treeFade` is 0 and `ultTree` null on
       every other relic, so this is two comparisons on fields nothing else
       writes. */
    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;

    /* The tree's boughs (v69), exactly the set `bladeSegments` tests -- the
'''),

('canopy picture: drawTree / drawTreeTop / _drawBark / drawTreeWeapon',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------------------ THE TREE ---
     CANOPY (v69 section 7.1). THE CAST: the ball stops dead and bark climbs
     its shell from the floor side over 0.4s -- dark plates, living seams --
     and three roots grow down and grip the floor (`_drawBark`, `drawTree`).
     IN MID-AIR THE ROOTS STILL GO TO THE FLOOR: aerial roots, a banyan's,
     dropped from the shell to the live floor however far it is -- the ball
     cannot fall because it is standing on them, and that is the self-root
     read in one picture (measured over 347 casts: the shell's underside is a
     median 135 units off the floor, and within 40 of a floor or a wall on
     only 36% of them).
     THE GROWTH IS THE ANIMATION: every bough runs from the shell to the tip
     of the segment `bladeSegments` tests, the haft thickening into a trunk
     as `reachMul` climbs, the head a burl of fixed size at its end
     (`SHAPES._whGrown` with `g` and `hs`). AT 1.5s the two new boughs sprout,
     drawn growing over 0.5s to a lighter burl -- and snapped whole the frame
     one strikes or clanks, because they are live at full reach from the
     frame they exist. THE CANOPY is a faint disc at the boughs' reach (glow
     at 0.06) edged in leaves, where `tickTree` tests. THE WITHER: the boughs
     draw back as dead wood over 0.4s while the live hammer, already at its
     rest reach, is drawn over them; the bark cracks and falls; the roots let
     go and shrink back to the shell.

     IT HANGS OFF THE FIGHTER (`treeFade`, `treeAge`, `treeOut`, `treeGrow`,
     `treeL`, the leaf and bark records), never `m.ultFx` (open item 25).
     PRESENTATION ONLY: no rng, no spawnFx, no Math.random -- shellHash and
     the clocks -- and nothing here writes a field the simulation reads. */
  drawTree(m){
    const a = m.a, b = m.b;
    if (!(a.treeFade > 0) && !(b.treeFade > 0)
        && !a.treeLeaves.length && !b.treeLeaves.length) return;  // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR, A = CONFIG.arena;
    const n = m.inset || 0, yF = A.h - n;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      const fade = f.treeFade, P = f.aff;
      if (fade > 0){
        const s = Math.min(1, f.treeAge / 0.8), kc = 1 - (1 - s) * (1 - s);
        const stand = !m.over && !!f.ultTree && f.alive;
        const L0 = f.w.reach * m.actMods.reach;
        const e = stand ? 1 : Math.pow(fade, 1.5);  // the wither, the ghost's curve
        const reach = stand ? L0 * f.reachMul
                            : L0 + Math.max(0, f.treeL[0] - 6 - L0) * e;
        const on = Math.min(1, s * 3) * e;
        {
          /* THE CANOPY: glow at 0.06 out to reach + R -- the test's own radius */
          const rc = R + reach;
          c.globalAlpha = 0.06 * on;
          c.fillStyle = P.glow;
          c.beginPath(); c.arc(f.x, f.y, rc, 0, TAU); c.fill();
          {
            /* ITS EDGE, IN LEAVES: the range read. One leaf every ~10
               units, two tones, tilted alternately, drifting slowly round. */
            const N = Math.max(12, Math.round(rc * TAU / 10)), q0 = m.t * 0.10;
            for (let tone = 0; tone < 2; tone++){
              c.globalAlpha = 0.55 * on * (tone ? 0.75 : 1);
              c.fillStyle = tone ? P.glow : P.core;
              c.beginPath();
              for (let j = tone; j < N; j += 2){
                const q = q0 + j * TAU / N, h = shellHash(9601 + f.side, j);
                const rr = rc - 2 + (h - 0.5) * 5, cx = f.x + Math.cos(q) * rr, cy = f.y + Math.sin(q) * rr;
                const d = q + Math.PI / 2 + (j % 4 < 2 ? 0.55 : -0.55), ux = Math.cos(d), uy = Math.sin(d);
                const ll = 4.2 + 1.6 * h, ww = 1.9;
                c.moveTo(cx - ux * ll, cy - uy * ll);
                c.quadraticCurveTo(cx - uy * ww * 2, cy + ux * ww * 2, cx + ux * ll, cy + uy * ll);
                c.quadraticCurveTo(cx + uy * ww * 2, cy - ux * ww * 2, cx - ux * ll, cy - uy * ll);
              }
              c.fill();
            }
          }
        }
        {
          /* THE ROOTS: three, off the underside of the shell to the floor --
             in mid-air, aerial roots dropped to it. They grow down with the
             bark, thick at the shell and tapering, with a side rootlet each
             and a grip splayed on the floor; in the wither they let go of the
             floor and shrink back into the shell. The school's vine grammar
             (a dark strand with a living seam, `_stEntangle`). */
          const kr = stand ? kc : kc * e;
          if (kr > 0.01 && !f.treeDead){
            const y0 = f.y + R * 0.70, gap = Math.max(0, yF - (f.y + R)), flat = gap < 10;
            const seam = mix(P.core, P.dark, 0.35);
            c.globalAlpha = 0.95 * Math.min(1, fade * 1.5);
            const strand = (pts, w0, w1, upto) => {
              const NS = pts.length - 1;
              for (let si = 1; si <= NS; si++){
                if ((si - 1) / NS >= upto) break;
                const u = Math.min(1, (upto - (si - 1) / NS) * NS);
                const p0 = pts[si - 1], q1 = pts[si];
                const p1 = [p0[0] + (q1[0] - p0[0]) * u, p0[1] + (q1[1] - p0[1]) * u];
                const w = w0 + (w1 - w0) * si / NS;
                c.strokeStyle = P.dark; c.lineWidth = w;
                c.beginPath(); c.moveTo(p0[0], p0[1]); c.lineTo(p1[0], p1[1]); c.stroke();
                c.strokeStyle = seam; c.lineWidth = Math.max(0.9, w * 0.22);
                c.beginPath(); c.moveTo(p0[0] - w * 0.15, p0[1]); c.lineTo(p1[0] - w * 0.15, p1[1]); c.stroke();
              }
            };
            for (let i = -1; i <= 1; i++){
              const h = shellHash(9611 + f.side, i + 1);
              const sx = f.x + i * R * 0.42;
              const ex = f.x + i * (R * (flat ? 1.7 : 0.9) + gap * 0.18) + (h - 0.5) * R * 0.5;
              const mx = f.x + i * R * 0.95, my = flat ? yF - 3 : f.y + R + gap * 0.45;
              const amp = flat ? 0 : Math.min(8, 2 + gap * 0.03);
              const pts = [];
              for (let si = 0; si <= 16; si++){
                const t = si / 16, v = 1 - t;
                pts.push([v * v * sx + 2 * v * t * mx + t * t * ex
                            + Math.sin(t * (7 + 4 * h) + h * 6.28) * amp * Math.sin(Math.PI * t),
                          v * v * y0 + 2 * v * t * my + t * t * (yF - 1)]);
              }
              strand(pts, 7.5, 2.6, kr);
              const t0 = 0.40 + 0.25 * h;  // a rootlet off its side
              if (!flat && kr > t0 + 0.05){
                const b0 = pts[Math.round(t0 * 16)], dir = i === 0 ? (h > 0.5 ? 1 : -1) : i;
                const ln = Math.min(22, 8 + gap * 0.06);
                const rl = [b0, [b0[0] + dir * ln * 0.45, b0[1] + ln * 0.35], [b0[0] + dir * ln, b0[1] + ln * 0.9]];
                strand(rl, 3.2, 1.4, Math.min(1, (kr - t0) * 6));
              }
              if (kr > 0.97){  // the grip on the floor
                const e0 = pts[16];
                for (let r2 = -1; r2 <= 1; r2++){
                  const lx = e0[0] + (r2 * 9 + i * 5), ly = yF - 1 - (r2 === 0 ? 0 : 2.5);
                  strand([[e0[0], e0[1] - 2], [e0[0] + (lx - e0[0]) * 0.5, yF - 1], [lx, ly]], 3, 1.4, 1);
                }
              }
            }
          }
        }
      }
      {
        /* THE LEAF MOTES: shed off the burls, tumbling down, gone in ~1.3s */
        const Lv = f.treeLeaves;
        if (Lv.length){
          for (let tone = 0; tone < 3; tone++){
            c.fillStyle = tone === 0 ? P.core : (tone === 1 ? P.glow : SHAPES._shade(P.core, 0.62, 0.1));
            for (const q of Lv){
              if (q.n % 3 !== tone) continue;
              const h = shellHash(9701 + f.side, q.n), h2 = shellHash(9703 + f.side, q.n), s2 = q.t * 0.5;
              const x = q.x + Math.sin(s2 * 3.3 + h * 6.28) * 5 + (h2 - 0.5) * 22 * s2;
              const y = q.y + s2 * (22 + 20 * h) + 26 * s2 * s2;
              const k2 = q.t / 2.6;
              c.globalAlpha = Math.min(1, q.t * 5) * (1 - k2 * k2) * 0.9;
              const d = h * 6.28 + s2 * (2.5 + 3 * h2) * (h > 0.5 ? 1 : -1), ux = Math.cos(d), uy = Math.sin(d);
              const ll = 3.4 + 1.4 * h2, ww = 1.5;
              c.beginPath();
              c.moveTo(x - ux * ll, y - uy * ll);
              c.quadraticCurveTo(x - uy * ww * 2, y + ux * ww * 2, x + ux * ll, y + uy * ll);
              c.quadraticCurveTo(x + uy * ww * 2, y - ux * ww * 2, x - ux * ll, y - uy * ll);
              c.fill();
            }
          }
        }
      }
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* ...and the bark that falls off the shell in the wither, over both
     fighters (see `drawTree`): each plate tumbles from where it let go. */
  drawTreeTop(m){
    const a = m.a, b = m.b;
    if (!a.treeBits.length && !b.treeBits.length) return;  // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR;
    c.save();
    c.lineJoin = "round";
    for (const f of [a, b]){
      if (!f.treeBits.length) continue;
      const B = treeBark(f.side).plates, P = f.aff;
      for (const d of f.treeBits){
        const pl = B.find(q => q.j === d.j); if (!pl) continue;
        const s2 = d.t * 0.5, k2 = d.t / d.life;
        c.save();
        c.translate(d.x + d.vx * s2, d.y + d.vy * s2 + 450 * s2 * s2);
        c.rotate(pl.spin * s2);
        c.scale(R * 0.92, R * 0.92);
        c.globalAlpha = (1 - k2 * k2) * 0.95;
        c.beginPath();
        for (const q of pl.pts) c.lineTo(q[0] - pl.cx, q[1] - pl.cy);
        c.closePath();
        c.fillStyle = P.dark; c.fill();
        c.strokeStyle = "#1A140C"; c.lineWidth = 2.2 / R; c.stroke();
        c.restore();
      }
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* THE BARK ON THE SHELL, drawn INTO the ball's own buffer after the glass
     (so the statuses, the stun ring and the hit flash still land over it).
     It climbs from the floor side over 0.4s with a living edge, then stands:
     dark plates at 0.86 over the glass -- the liquid, which is the health,
     still reads through them -- with seams of the school's core. In the
     wither the seams dry to cracks and the plates let go one by one
     (`treeBits`). */
  _drawBark(m, f, c){
    if (!(f.treeFade > 0)) return;
    {
      const R = CONFIG.physics.ballR, P = f.aff, B = treeBark(f.side).plates;
      const s = Math.min(1, f.treeAge / 0.8), kc = 1 - (1 - s) * (1 - s);
      const out = f.treeOut, lvl = R - 2.1 * R * kc;
      const dry = Math.min(1, out / 0.3);
      c.save();
      c.translate(f.x, f.y);
      c.beginPath(); c.arc(0, 0, R * 0.985, 0, TAU); c.clip();
      if (kc < 1){ c.beginPath(); c.rect(-R * 1.3, lvl, R * 2.6, R * 2.6); c.clip(); }
      const plate = (pl) => { c.beginPath();
        for (const q of pl.pts) c.lineTo(q[0] * R, q[1] * R); c.closePath(); };
      /* THE HEALTH STILL READS THROUGH IT: the plates over the liquid are
         thinner (0.5) than over the headspace (0.86), so the level is a step
         in the bark -- sap glowing through it -- and not hidden under it. The
         glass's own paths, at the glass's own level. */
      const lv = lvlOf(Math.max(0, Math.min(1, f.hp / CONFIG.combat.baseHP)));
      c.fillStyle = P.dark;
      for (const [zone, al] of [[headPoly(f, R, lv), 0.86], [liquidPoly(f, R, lv), 0.5]]){
        c.save(); c.clip(zone); c.globalAlpha = al;
        for (const pl of B){ if (out > 0 && out >= pl.drop) continue; plate(pl); c.fill(); }
        c.restore();
      }
      c.globalAlpha = 0.9;
      c.strokeStyle = dry > 0 ? mix(P.core, "#2A2012", dry) : P.core;
      c.lineWidth = 1.7;
      for (const pl of B){ if (out > 0 && out >= pl.drop) continue; plate(pl); c.stroke(); }
      if (kc < 1){  // the living edge, climbing
        c.globalAlpha = 0.9 * (1 - kc * kc);
        c.strokeStyle = P.glow; c.lineWidth = 2.2;
        c.beginPath(); c.moveTo(-R, lvl); c.lineTo(R, lvl); c.stroke();
      }
      c.restore();
      c.globalAlpha = 1;
    }
  }

  /* THE TREE ITSELF, from `drawWeapon`. Returns true when it has drawn the
     weapon whole. */
  drawTreeWeapon(m, f, reach, dim){
    {
      const c = this.ctx, R = CONFIG.physics.ballR, W = f.w.artW, P = f.aff;
      const L0 = f.w.reach * m.actMods.reach + 6;  // the hammer at rest
      if (!m.over && f.ultTree){
        /* STANDING: a bough per offset in the tested set, from the shell to
           its segment's tip. THE HALO IS DRAWN, not blitted: the resting
           hammer's glow sprite is baked per whole unit of length and its lit
           scratch is sized to the length, so a tree growing on three boughs
           re-baked every other frame. Measured on Electron 44 / RTX 3070 at
           453x805, interleaved on one loaded machine: the base path drew the
           caster's weapon in 13.9-18.7 ms a frame while three boughs grew and
           baked 107-112 glow sprites a window; this draws it in 1.4-1.8 ms
           and bakes none. */
        const S = f.bladeSet || f.w.blades, Lf = reach + 6, G = f.treeGrow;
        const g = clamp((f.reachMul - 1) / (f.w.ult.reachCap - 1), 0, 1);
        c.save();
        for (let i = 0; i < S.length; i++){
          const gi = i === 0 ? 1 : (G[i] || 0);
          if (!(gi > 0.002)) continue;
          const Li = Lf * gi;
          const hs = Math.min(i === 0 ? 1 : 0.72 * (0.35 + 0.65 * gi), Li * 0.8 / (W * 0.62));
          c.save();
          c.translate(f.x, f.y); c.rotate(f.theta + S[i] * TAU); c.translate(R - 6, 0);
          c.globalAlpha = dim * 0.14;
          c.strokeStyle = P.core; c.fillStyle = P.core; c.lineCap = "round";
          c.lineWidth = W * (0.15 + 0.22 * g * gi) + 12;
          c.beginPath(); c.moveTo(0, 0); c.lineTo(Math.max(0, Li - W * 0.31 * hs), 0); c.stroke();
          c.beginPath(); c.arc(Li - W * 0.31 * hs, 0, W * 0.62 * hs, 0, TAU); c.fill();
          c.globalAlpha = dim;
          SHAPES._whGrown(c, Li, W, P, 0, g * gi, hs);
          c.restore();
        }
        c.restore();
        return true;
      }
      /* WITHERING: the boughs as they stood draw back as dead wood -- the
         trunk to the haft's length, the sprouts into the shell -- and fade.
         The live hammer is already at its rest reach (the close restored it)
         and `drawWeapon` draws it over them, so the one thing drawn at full
         strength is the thing that can hit. */
      const k = f.treeFade;
      if (k > 0){
        const e = Math.pow(k, 1.5), n = Math.max(1, f.w.ult.boughs | 0);  // the offsets `tickTree` set
        c.save();
        c.lineCap = "round";
        for (let i = 0; i < n && i < 3; i++){
          const Li = f.treeL[i];
          if (!(Li > 0)) continue;
          const Ld = i === 0 ? L0 + (Li - L0) * e : Li * e;
          if (Ld < 4) continue;
          c.save();
          c.translate(f.x, f.y); c.rotate(f.theta + (i / n) * TAU); c.translate(R - 6, 0);
          c.globalAlpha = dim * 0.9 * k * k;
          c.strokeStyle = "#716449"; c.lineWidth = W * (0.15 + 0.22 * e);
          c.beginPath(); c.moveTo(0, 0); c.lineTo(Ld, 0); c.stroke();
          c.strokeStyle = "#2A2418"; c.lineWidth = Math.max(1, W * 0.035);
          c.beginPath(); c.moveTo(0, -W * 0.03); c.lineTo(Ld * 0.96, -W * 0.02); c.stroke();
          c.restore();
        }
        c.restore();
      }
      if (f.ultTree && m.over){
        /* THE MATCH ENDED UNDER THE TREE: `tickTree` will not run again, so
           the window's reach and blade set are frozen at their last values.
           The hammer is drawn at rest, once, through the verdict. */
        c.save();
        c.globalAlpha = dim;
        c.translate(f.x, f.y); c.rotate(f.theta); c.translate(R - 6, 0);
        const _g = weaponGlow(f.w.shape, L0, W, P, f.drawK, 20);
        c.drawImage(_g.cv, _g.ox, _g.oy);
        if (!litWeapon(c, f.w.shape, L0, W, P, f.drawK, f.theta)){
          const fn = SHAPES[f.w.shape];
          if (fn) fn(c, L0, W, P, f.drawK);
        }
        c.restore();
        return true;
      }
    }
    return false;
  }

  drawMotes(m){
'''),

]

STAGE_OUT = {"1": "sc-ironwood", "2": "sc-rooted", "3": "sc-boughs", "4": "sc-canopy",
             "5": "sc-canopy-w38", "6": "sc-canopy-fx"}


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
    ap.add_argument("--stage", choices=["1", "2", "3", "4", "5", "6"], required=True)
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
        elif A.stage == "6":
            if f'winDmg:{TUNED["winDmg"]},' not in code or "drawTreeWeapon" in code:
                raise SystemExit("stage 6 goes on stage 5, once")
            edits, want = S6, ult_block(ULT["charge"], ULT["boughs"], TUNED["winDmg"],
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
    for label, _old, new in S1 + S2 + S3 + S4 + S5 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the RNG")
    for label, _old, new in S6:
        if "ultFx" in strip_comments(new):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' uses the one "
                             "ultFx slot (open item 25)")
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
