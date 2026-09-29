#!/usr/bin/env python
"""ANGELUS / ASCENSION -- the sanctified twinblade, a NEW relic. v104.

Built from `06-docs/v74/ANGELUS-BUILD-BRIEF.md` and
`sanctified-twinblade-design-v74.md` (Cowork, 2026-09-26), which are the input
and the only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

    stage 1   the relic, ult stubbed      <tip> -> sc-angelus.html
    stage 2   the rise and the shafts     -> sc-angelus-rise.html   (arm B)
    stage 3   the heal                    -> sc-angelus-heal.html   (arm C)
    stage 5   the blade                   -> sc-angelus-b9.html      (11.95 -> 9)
    stage 6   the picture and the voice   -> sc-angelus-b9-fx.html   (presentation)
              on stage 5's link; no fx.js field (reading 17). The carry is the
              orchestrator's: stages 1, 2, 3, 5 and 6 on its tip.

§1 (the brief's §0): "For a duration the relic rises and hangs in the air. Its
two blades become two shafts of light reaching the floor, sweeping the hall as
they turn; a shaft through the enemy is a light hit, and every hit heals the
one above."

Declared (design §5, brief §0-§1):
  THE RISE    at the cast the caster is pinned (`pin`, `pinFree` 1, `pinV`
              [0,0]) and eased from where it stands to (W/2, hangY) over
              `rise` seconds; it hangs there, re-armed every window frame
              (pin, pinMax and pinFree), and is released to REST on close
              (pin, pinMax 0, pinV null, pinFree 0, vx = vy = 0), so it drops.
              A pinned ball is immovable, takes hits and takes no knock
              (`move`, `_ballPair` and the knock discard do that already).
  THE SHAFTS  when it arrives: `reachMul` = shaft (10) on both blades (every
              reach read carries it; `bladeSegments` is untouched), the spin
              x shaftSpin (0.5) in tickWeapon's product, and every blow x
              winDmg (0.4) in `resolveHit`'s damage line, off `f.ultRise`
              (the Canopy rule: scale in the hit, never on the weapon).
              Everything else about a blade blow -- smite 1, the hit stop,
              the knock, the beat, binds -- is the blade's.
  THE HEAL    `apply("blessing", healPer)` for every shaft hit that lands,
              read off the `hits` delta in `tickRise` (the brief's §1), and
              healed by the existing `tickStatus` blessing path.
  The cast files fireUlt's own `ult` beat; nothing in the window files one.

THE CHARGE. The brief's 16 is the LAB's clock, which counts hit-stop freezes;
Rick, 2026-09-27, for the whole batch: "use the game's equivalent". Measured
for this fighter on the lab's arm C (v104 §0).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE SHAFTS LIGHT WHEN IT ARRIVES (design §5, twice): for the `rise`
     seconds the blades are the twinblade's own (reach 1, full spin, full
     damage, no heal); the lab teleported the caster and lit the whole window.
     The design's open item 5 prices this at "~4%" of the window.
  2. THE EASE IS A SMOOTHSTEP, 3u^2 - 2u^3, from the cast position to the hang
     point on the window clock. The prose says "eases it up over 0.35s" and
     the lab moved it in one frame; the curve is the build's.
  3. THE HANG POINT IS THE LAB'S: (W/2, max(hangY, inset + R + 6)). The clamp
     cannot bind (maxInset 140 + R 34 + 6 = 180 < 300); it is the lab's line.
     After the arrival the hold writes the hang point every window frame, as
     the lab did after every step; nothing in this engine moves a pinned ball,
     so the write is the pin's own result.
  4. THE HOLD IS RE-ARMED EVERY WINDOW FRAME, `pinMax` and `pinFree` as well
     as `pin` (the brief: "pinned there (pinFree 1, re-armed)"; Canopy's
     reading), and the blades must keep turning ("sweeping the hall as they
     turn"). What can clear it is Ravelbone's wire, and only on a caster it
     caught BEFORE the cast (a pinned ball cannot be caught): the wire's slip,
     its window's end and its connect each clear pin / pinMax / pinV / pinFree
     on its quarry, and the next tick puts the hold back. (A connect clears it
     in resolveHit, after the tick, so the caster would ride its knock for one
     frame before the hang write puts it back; the lab re-pinned after the
     step. By reasoning -- never observed.) THE PATH NEVER CAME UP: the probe
     found pinFree cleared 0 times (v104 §3), so it is not left to argument:
     the probe clears the hold itself before every 50th window tick -- inert
     on this build, the fights identical -- and [2] fails a build that does
     not re-arm (mutant m8-pinfree, review r2's r1).
  5. THE WINDOW CLOSES ON THE CASTER'S DEATH (the prose's "for a duration";
     Canopy's reading), and a dead caster keeps its kill flight -- when the
     tick comes round after the death (a kill flight, or a death in the
     fighter loop); see 10 for the kill that ends the match.
  6. EVERY SHAFT HIT HEALS, the last window frame's included: the heal reads
     the `hits` delta at the top of the tick, before the clock can close the
     window. (The lab closed first and dropped the last frame's heal.)
  7. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract; the brief wrote
     `f`). Blessing has no reader of it.
  8. THE SHARED WEAPON IS NEVER WRITTEN. The lab scaled `w.spin` and `w.dmg`;
     both are scaled at their one read site for this relic, in the same order
     of multiplication, so a blow and a turn are bit-identical to the lab's.
  9. NO CAST WAIT. The design has no wither, and a cast cannot come inside a
     window: the charge (14) and the window (8) run on the same unfrozen clock
     and the charge is spent at the cast. The probe asserts it ([10]). A knob
     move that put the charge at or under `dur` WOULD need one (a cast inside
     a window starts a new rise with reachMul still 10 and full damage; review
     r2 measured it at charge 6), and it would go on the charge gate's stable
     prefix, "if (f.charge >= f.w.ult.charge && !f.ultCorona".
 10. THE WINDOW DOES NOT CLOSE ON THE FOE'S DEATH, AND IT STAYS OPEN AT
     `over` -- Canopy's convention (v99), against the lab. The lab released on
     either death (ult_overlay: `!me.alive || !foe.alive` -> ascend.js
     release()), but AFTER its step, with the match already decided, so that
     close moved no fight and leaving it out moves none. In the engine a kill
     ends the match INSIDE the killing step (checkEnd: only Ravelbone's burst
     and Grudgebearer's forge arm a killFlight, and Angelus's blows arm none),
     and step() returns at `over` before any ticker -- so a window open at the
     kill stays open, hung and lit at reach x10, through the verdict, whichever
     ball died (unless Angelus dies to one of those two, whose flight lets
     the tick close it: reading 5). A foe that dies in the fighter loop (to
     Angelus's own smite, a damage-over-time status in tickStatus) is dead for
     one more tick, and that tick leaves the window open too. The probe
     counts both (v104 §3: open at the end of 260 of b9's 456 probe fights).
     THE PICTURE CLOSES IT: stage 6 draws the close (the
     shafts shorten, the halo goes) at `over`, as Canopy's picture reads
     `(this.over || !f.alive) ? null : f.ultTree`; the sim will not.
 11. A SHAFT HIT ON A SHADE HEALS. `tickShadeHits` calls tickHits(Angelus,
     shade), so a blow on Twinshade's copy is an ordinary resolveHit blow: x
     winDmg while lit, and `self.hits++`, which the heal reads. The lab read
     the same `hits` delta, and the prose says "every hit heals".

STAGE 6, THE PICTURE AND THE VOICE (the brief's stage 6; design §6.1 "the
picture" and §6.2 "sound"). Picked on measurements under Rick's "you pick i
overrule" by the picture lab (scratch) and `angelus_voice_lab.py` (v104 §5);
the rows are the labs', byte-exact. Declared:
 12. THE PICTURE READS THE WINDOW OFF `ultRise && !over && alive` (Canopy's
     rule) and keeps its own state on the fighter (`ascend*`), never on
     `m.ultFx` (one slot, and the foe's cast takes it: open item 25).
     `tickAscend` runs in `tickPresentation`, on the presentation clock, which
     runs through hit stops and after `over`. So the picture closes the window
     reading 10 leaves open at the kill -- the shafts shorten to blades over
     0.3s and the halo goes -- and, with `reachMul` still 10 through the
     verdict, `drawWeapon` draws the blades at rest. The sim's ball stays
     where it hung: no presentation-only drop (the picture lab's reading).
 13. THE PICTURE FINDS A SHAFT BLOW BY WATCHING `hits` RISE WHILE LIT (a blow
     on a shade counts, and heals: reading 11) and starts the blow's thread
     at the `hit` beat `resolveHit` filed that step, read and never written;
     it finds a heal by watching `riseTally.bless` rise. So neither tickRise
     nor resolveHit makes a call for the picture. It writes its own `ascend*`
     fields, the tags (the BLESSING tag, one on the caster at a time: a tag
     already up takes the new count) and `taught`, which nothing in the
     simulation reads; it draws no rng (shellHash and the clocks).
 14. THE VOICES ON THE SIM PATH ARE THREE `SFX.play` CALLS, each a no-op
     headless that writes nothing the simulation reads: the shaft-hit tap in
     tickRise's heal, once per shaft hit healed, after its blessing lands (n =
     the caster's blessing stacks, 1-5); the close chord in tickRise's close;
     the landing thud in `move`, on the first floor contact after that close
     with the caster alive. The thud's flag is `riseTally.falling`, on the
     probe's tally, which nothing in the simulation reads. The cast's voice is
     fireUlt's own `SFX.play("ult", { w: "angelus" })`, which found no arm and
     fell through to rune-crack: the arms are ADDED before that shared
     fallback, which is re-emitted unchanged for the relics that still use it.
 15. THE CLOSE CHORD (and so the thud) ONLY ON A CLOSE BY THE CLOCK WITH BOTH
     ALIVE. A caster's death closes the window in a kill flight, and a match
     that ends inside the window never reaches the tick again (reading 10):
     both are the death voice's moment, as for Zenith's, Canopy's and
     Onslaught's closes. A foe killed by its smite earlier in that step is
     not alive (the hp getter), so no chord plays over it.
 16. THE BODY TRAIL IS NOT DRAWN WHILE THE PICTURE IS UP (`ascendFade` > 0):
     `move` feeds the trail and skips a pinned ball, and `tickRise` carries
     the ball away, so for the whole window the trail drew a ghost of the ball
     at the cast point. This row REPLACES "    const tr = f.trail;" and does
     not re-emit it: the second anchor Angelus consumes (no builder in tools/
     contains it on 2026-09-28; the first is reading 8's spin product).
 17. NO fx.js FIELD (the brief's "the field in both copies"). A SPECS field
     rides the one ultFx slot, which Angelus holds a median 0.633s of window
     clock (7.4% of the window; the shafts light at 0.35), and fires once at
     the cast point, a median 226 units from the hang point the shafts turn
     about (the picture lab's fxprobe, 133 windows). The design's motes are
     drawn instead, in the world pass, down each shaft (Zenith's and Canopy's
     precedent). This builder edits neither copy, and stage 6 refuses if its
     edits touched the inlined one. Rick's to overrule.
 18. THE LANDING THUD IS NEW. The design names it (§6.2 "the ball's landing
     thud") and the engine had none: every floor contact plays the wall tick,
     which still plays under it.

THE CLOCK. The window, the rise and the hold run on the window tickers' clock,
which stops through a hit stop (Corollary's, Daybreak's, Zenith's, Canopy's,
Onslaught's and Tendril's convention).

THE BASE is asserted BY CONTENT: the anchors this builder uses, the twinblade
profile it copies, the sanctified channel, the sanctified twinblade's head
route, the blessing heal and the pin's hold. Never by which relic is last, so
it re-applies on a tip that carries other new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC = "angelus"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). The brief's §0.
ULT = {
    "charge": 14,      # the lab's 16 on the game's clock (Rick's batch ruling; measured, v104 §0)
    "dur": 8,          # "the window 8s every 16s"
    "rise": 0.35,      # "the rise to (W/2, 300) over 0.35s"
    "hangY": 300,      # "(W/2, 300)" -- design §3: y 300 of 800, taken
    "shaft": 10,       # "reachMul 10 on both blades"
    "shaftSpin": 0.5,  # "spin x 0.5"
    "winDmg": 0.4,     # "damage x 0.4 in resolveHit off f.ultRise"
    "healPer": 1,      # "apply("blessing", 1, f) per shaft hit landed" -- stage 3
}
TIP = "Rises into the air; its blades become shafts of light. Each hit heals"
# Widowmaker's twinblade profile, the lab's donor and the whole type's (all
# five twinblades carry it), at the lab's blade, 11.95; stage 5 settles it.
# The donor's own blade is NOT asserted: Widowmaker's v106 redesign moves it.
PHYS_OF = lambda dmg: (f'blades:[0,0.5], reach:62, width:8, artW:30, dmg:{dmg}, spin:5.7, '
                       'mode:"spin", mass:1.1')
LAB_BLADE = 11.95
TYPE_RE = (r'shape:"twinblade",\s*blades:\[0,0\.5\], reach:62, width:8, artW:30, '
           r'dmg:[\d.]+, spin:5\.7, mode:"spin", mass:1\.1')
TWINBLADES = ("widowmaker", "spellbreaker", "twinshade", "thornshear", "starwarden")
SANCTIFIED = ("dawnbringer", "lastlight", "aureole", "censer", "morningstar")
BLURB = ("Twin blades that rise into the air and become two shafts of light: "
         "they sweep the hall beneath, and every hit heals the one above.")
# THE BLADE (stage 5; brief §2: "Wide on 151 at 9 / 9.5 / 10. Expect 9-9.5").
# Both sides, two blocks, 1520 fights a point (relic_rate on sc-angelus-heal,
# v104 §4): 8.5 -> 46.3, 9 -> 51.2, 9.5 -> 53.5, 10 -> 57.5. The crossing is
# ~8.9, just under the brief's band; the brief names no knob to move for the
# blade (the hang height is Rick's lever, design §7 item 1, and "do not
# improve the hang height"), so nothing else moves. 9 is the measured point
# nearest 50%, and inside the band.
BLADE = 9
NAMES = ("ultRise", "riseTally", "tickRise", 'kind:"rise"', "shaftSpin", "healPer", "hangY")


def ult_block(charge, heal) -> str:
    return (f'''    ult:{{ name:"Ascension", charge:{charge}, kind:"rise", dur:{ULT["dur"]},
          rise:{ULT["rise"]}, hangY:{ULT["hangY"]}, shaft:{ULT["shaft"]}, shaftSpin:{ULT["shaftSpin"]}, winDmg:{ULT["winDmg"]},
          healPer:{heal},          // v74: the heal (stage 3)
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
# THE RELIC, APPENDED AT THE END OF THE WEAPONS ARRAY, ITS ULTIMATE STUBBED at
# charge 1e9 (the clock can never reach it, `fireUlt` never runs) --
# Starwarden's stage-1 pattern. The anchor is the array's closing and the
# comment under it, which names no relic, so a row another build appends first
# still leaves it in place. SHAPES.twinblade already routes sanctified to
# `_tbRadiant`, which no shipped relic has drawn (the design's "first cut").
ROW_ANCHOR = '\n\n];\n/* The single source of truth for "which status does this relic teach".'

S1 = [

("angelus joins the roster at the end of the array, its ultimate stubbed",
 ROW_ANCHOR,
 f'''

  /* ANGELUS / ASCENSION (v74; built v104) -- THE SANCTIFIED TWINBLADE. A new
     relic. Widowmaker's twinblade profile (the lab's donor and the whole
     type's) at the lab's blade, 11.95 (stage 5 settles it), and the school's
     channel, onHit smite 1. Stage 1 stubs the ultimate at charge 1e9; stages
     2-3 give it its rise and its shafts, then the heal. */
  {{ id:"{RELIC}", name:"Angelus", aff:"sanctified", shape:"twinblade",
    {PHYS_OF(LAB_BLADE)},
    onHit:{{ smite:1 }},
{ult_block("1e9", 0)}
    blurb:"{BLURB}" }},''' + ROW_ANCHOR),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the rise has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Ascension", charge:1e9, kind:"rise", dur:8,
''',
 f'''    ult:{{ name:"Ascension", charge:{ULT["charge"]}, kind:"rise", dur:{ULT["dur"]},   // v74 stage 2: the rise and the shafts
'''),

("the fighter carries the rise",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, x0, y0, lit, hits} while ASCENSION's caster rises and hangs
       (v74). null on every other relic and on this one outside its window:
       `tickRise` returns after a two-iteration loop that does nothing, and
       tickWeapon and `resolveHit` read it once each. `riseTally` is the
       probe's count, cumulative over the fight; nothing in the simulation
       reads it. */
    this.ultRise = null;
    this.riseTally = null;
'''),

("the cast pins the caster and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "rise"){
      /* ASCENSION (v74). NOTHING RESOLVES HERE: the cast pins the caster where
         it stands -- `pin` with `pinFree`, so the ball is held and the blades
         keep turning, and `pinV` [0,0] is the rest it is released to -- and
         `tickRise` eases it up to the hang point, lights the shafts when it
         arrives and heals every shaft hit. `hits` is the ledger the heal
         reads its delta from. */
      f.ultRise = { t: 0, dur: u.dur, x0: f.x, y0: f.y, lit: 0, hits: f.hits };
      f.pinV = [0, 0]; f.pin = u.dur; f.pinMax = u.dur; f.pinFree = 1;
      if (!f.riseTally)
        f.riseTally = { casts: 0, frames: 0, litFrames: 0, arrivals: 0,
                        shaftHits: 0, bless: 0 };
      f.riseTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the rise ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickRise(dt);                  // ASCENSION (v74)
'''),

# COMPOSITION: THE ONE ANCHOR ANGELUS DOES NOT RE-EMIT. The lab's order of
# multiplication puts the shaft scale between the spin and spinMul, so this
# insert consumes "(f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)" (Bindweed's
# line, already carried). A builder carried AFTER Angelus that anchors on that
# exact string will refuse; on 2026-09-28 no builder in tools/ but
# bindweed_build.py (the line's author) contains it (v104 §1).
("the shafts turn at half the blades' spin",
 '''(f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)''',
 '''(f.ultVine ? 0 : f.w.spin)
              /* ASCENSION (v74): THE SHAFTS TURN AT `shaftSpin` x the blades'
                 spin once they are lit, where the lab scaled `w.spin` -- the
                 same product in the same order, and the shared weapon is
                 never written. `ultRise` is null on every other relic, so
                 theirs is x 1, exactly. */
              * (f.ultRise && f.ultRise.lit ? f.w.ult.shaftSpin : 1) * f.spinMul(mods.spin)'''),

("a shaft hit is the blade x winDmg",
 '''self.ultTree ? self.w.dmg * self.w.ult.winDmg : ''',
 '''self.ultTree ? self.w.dmg * self.w.ult.winDmg : self.ultRise && self.ultRise.lit ? self.w.dmg * self.w.ult.winDmg : '''),

("tickRise lifts, lights and heals",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE RISE ========
     v74 §1 / §5, brief §0-§1. While the window runs:
       THE HEAL   first, every shaft hit landed since the last tick (the
                  `hits` delta, read before the clock can close the window):
                  blessing +healPer each, through `tickStatus`'s own heal.
       THE HOLD   `pin`, `pinMax` and `pinFree` re-armed every frame --
                  `tickStasis` has just taken dt off the pin, and Ravelbone's
                  wire can clear `pinFree`; the blades keep turning.
       THE RISE   for `rise` seconds the caster is eased (smoothstep) from
                  where it cast to the hang point, (W/2, max(hangY, inset + R
                  + 6)); the blades are its own until it arrives.
       THE SHAFTS on arrival `reachMul` = shaft and `lit` = 1, which the spin
                  product in tickWeapon and `resolveHit`'s damage line read;
                  the hang point is written every frame after (the lab's
                  hold; nothing moves a pinned ball).
     CLOSE, by the clock or the caster's death: reach back to 1 and the hold
     let go -- a live caster to REST, so it drops; a dead one keeps its kill
     flight (`tickStasis` has already released it). No hurt, no knock, no
     beat and no hit stop here. On the window tickers' clock, so all of it
     freezes through a hit stop. `apply`'s source is a side letter. */
  tickRise(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultRise;
      if (!Z) continue;
      const u = f.w.ult, T = f.riseTally;
      const n = f.hits - Z.hits;
      Z.hits = f.hits;
      if (n > 0 && Z.lit){
        T.shaftHits += n;
        if (u.healPer > 0 && f.alive){
          f.apply("blessing", u.healPer * n, f === this.a ? "a" : "b");
          T.bless += u.healPer * n;
        }
      }
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive){
        f.ultRise = null;
        f.reachMul = 1;
        f.pin = 0; f.pinMax = 0; f.pinV = null; f.pinFree = 0;
        if (f.alive){ f.vx = 0; f.vy = 0; }
        continue;
      }
      T.frames++;
      f.pin = Z.dur; f.pinMax = Z.dur; f.pinFree = 1;
      const tx = CONFIG.arena.w / 2;
      const ty = Math.max(u.hangY, this.inset + CONFIG.physics.ballR + 6);
      if (!Z.lit && Z.t < u.rise){
        const k = Z.t / u.rise, e = k * k * (3 - 2 * k);
        f.x = Z.x0 + (tx - Z.x0) * e;
        f.y = Z.y0 + (ty - Z.y0) * e;
        continue;
      }
      if (!Z.lit){ Z.lit = 1; f.reachMul = u.shaft; T.arrivals++; }
      f.x = tx; f.y = ty;
      T.litFrames++;
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the heal",
 '''          healPer:0,          // v74: the heal (stage 3)
''',
 f'''          healPer:{ULT["healPer"]},          // v74: the heal (stage 3)
'''),
]


# ---------------------------------------------------------------- stage 5 --
def s5_edits() -> list:
    return [
        ("the blade: at the crossing",
         f'''  {{ id:"{RELIC}", name:"Angelus", aff:"sanctified", shape:"twinblade",
    {PHYS_OF(LAB_BLADE)},''',
         f'''  {{ id:"{RELIC}", name:"Angelus", aff:"sanctified", shape:"twinblade",
    {PHYS_OF(BLADE)},'''),
    ]

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (the brief's stage 6; design §6.1 and §6.2),
# picked on measurements under Rick's "you pick i overrule" by the picture
# lab (scratch) and `angelus_voice_lab.py` (v104 §5). PRESENTATION ONLY:
# engine_ab over all 39 relics, Angelus included, is the proof, and the
# probe's [11]-[12] read the voices and the picture's hook inside the fight.
# The rows are byte-exact to the labs' own files (voice 70f47a5acf37e4f7, 4
# rows; picture 324d3654c51b4d04, 8 rows); the picture rows alone reproduce
# the picture lab's stamp (32d61ac685db232f), the voice rows alone the voice
# lab's page (32d55d74179c4335), and the two sets give the same bytes in
# either order. No two rows share an anchor, so none is merged.
#   THE VOICE: four arms -- the cast's chord, the shaft-hit tap, the close,
#   the landing thud -- ADDED before the shared rune-crack fallback, which
#   is re-emitted unchanged, last; three calls on the sim path (the tap and
#   the close in tickRise, the thud in `move`: readings 14, 15 and 18).
#   THE PICTURE: `tickAscend` in tickPresentation (readings 12-13); the
#   world pass under both balls (the column, the halo, the pools); the
#   shafts inside drawWeapon (bodies, motes, the blades at rest); the cores
#   and the threads over both fighters; the body trail hidden while it is
#   up (reading 16).
# COMPOSITION: every anchor is re-emitted but the body trail's,
# "    const tr = f.trail;" (reading 16), which no builder in tools/ contains
# on 2026-09-28. The rows ride on four of stage 2's own lines (the fields,
# the heal, the close) and on shared lines every stage 6 of the batch uses
# as `after` / `before` anchors (tickPresentation, the world and emissive
# passes, drawWeapon's tree hook, drawMotes, tickWinnow, move's bounce).
S6 = [

("Sfx: Angelus's cast, shaft-hit, close and landing arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "angelus"){                    // it rises
          /* ANGELUS'S CAST, THE RISE -- v74 §6.2: "a choir swell (three
             re-struck tones a fifth and octave apart, 0.6s) -- the one voice
             in the game allowed to be a chord". VOWEL, of 5, picked on the
             numbers by `angelus_voice_lab.py` under Rick's "you pick i
             overrule" (v104). Angelus had no arm and fell through to
             rune-crack, which other relics still use, so this ADDS arms before
             that fallback and leaves it alone.

             D4, A4 and D5 (the score's iv: root, fifth, octave) as three
             sines, each strike carrying its 2nd and 3rd partials at 0.3 /
             0.12, each held by re-striking it in phase at its own whole cycles
             every ~11 ms, swelling +11.9 dB to a crest 445 ms in -- where the
             rise arrives and the shafts light -- and released: audible 605 ms,
             its crest -2.8 dB re Angelus's own blow. Register at most 0.61
             (Starwarden's cast) against rune-crack, the seal (the game's other
             stack of fifths), the school's and the twinblades' casts, the
             death voice and the blow. */
          const g = 0.01343, sw = 18.85, D = 0.161, L = 0.455, F = 293.665;
          const lv = (s) => g * Math.pow(10, -sw * (1 - s / L) / 20);
          for (const [r, k, s0, c] of [[1, 1, 0, 0], [1.5, 0.8, 0, 0], [2, 0.6, 0, 0]]){
            const f = F * r * Math.pow(2, c / 1200), dt = Math.max(1, Math.round(f * 0.011)) / f;
            const q = Math.pow(0.0001 / lv(s0), dt / D);
            for (let j = 0; s0 + j * dt < L - 1e-9; j++){
              const s = s0 + j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, 0.6 / (1 - q)));
              this._tone(t + s, { freq: f, gain: a, dur: D, type:"sine" }).frequency.value = f;
              for (const [h, kh] of [[2, 0.3], [3, 0.12]])
                this._tone(t + s, { freq: f * h, gain: a * kh, dur: D, type:"sine" }).frequency.value = f * h;
            }
          }
        } else if (w === "angelus-shaft"){              // a shaft hit healed
          /* A SHAFT HIT -- "a bright glassy tap, 70ms, quiet; blessing count
             in the pitch" (v74 §6.2). SKY, of 7 (`angelus_voice_lab.py`).
             `tickRise` plays it once per shaft hit healed, after the blessing
             lands, with `n`, the caster's blessing count (1-5).

             A thin glass rod (sines on 1 : 2.76), one step of the score's A
             minor pentatonic a count: C8 D8 E8 G8 A8 (counts clamped to 1..5).
             Audible 70-70 ms; its loudest 50 ms -9.3 dB re the shaft's own
             blow and +9.3 dB re the wall tick; centroid 4774 Hz or more.
             Register at most 0.51 (the wall tick) against the heal chime,
             Zenith's tick, the wall tick, the runic snap, the blow and the
             cast. */
          const n = clamp(Math.round(p.n || 0), 1, 5), g = 0.06776, D = 0.106;
          const F = [4186.01, 4698.64, 5274.04, 6271.93, 7040][n - 1];
          for (const [r, k, d] of [[1, 1, 1], [2.76, 0.35, 0.6]])
            this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;
        } else if (w === "angelus-close"){              // the chord resolves down
          /* THE CLOSE -- "the chord resolving down" (v74 §6.2). STEP, of 4
             (`angelus_voice_lab.py`): the cast's own chord and voice moving
             down a fourth to the score's tonic, A3-E4-A4 (iv -> i, the plagal
             cadence), the three voices step down together at 0.15 s; the level
             falls 6 dB across it and the release is the decay. Audible 590 ms,
             its loudest 50 ms -3.0 dB re the cast. Register at most 0.62 (the
             seal) against the seal, the death voice, rune-crack and the blow.
             `tickRise` plays it only when the window closes by its clock with
             both alive. */
          const g = 0.004659, D = 0.256, E = 0.35, F0 = 293.665, F1 = 220;
          const lv = (s) => g * Math.pow(10, -6 * s / E / 20);
          for (const [r, k, c, s1] of [[1, 1, 0, 0.15], [1.5, 0.8, 0, 0.15], [2, 0.6, 0, 0.15]])
            for (const [F, s0, s2] of [[F0, 0, s1], [F1, s1, E]]){
              const f = F * r * Math.pow(2, c / 1200), dt = Math.max(1, Math.round(f * 0.011)) / f;
              const q = Math.pow(0.0001 / lv(s0), dt / D);
              for (let j = 0; s0 + j * dt < s2 - 1e-9; j++){
                const s = s0 + j * dt, a = k * (j ? lv(s) : lv(s) * Math.max(1, 0.6 / (1 - q)));
                this._tone(t + s, { freq: f, gain: a, dur: D, type:"sine" }).frequency.value = f;
                for (const [h, kh] of [[2, 0.3], [3, 0.12]])
                  this._tone(t + s, { freq: f * h, gain: a * kh, dur: D, type:"sine" }).frequency.value = f * h;
              }
            }
        } else if (w === "angelus-land"){               // and the ball lands
          /* THE LANDING -- "and the ball's landing thud" (v74 §6.2). The
             engine plays its wall tick on every floor contact and had no thud,
             so this one is new. DEEP, of 6 (`angelus_voice_lab.py`): BODY
             lower: 95 -> 42 Hz under noise low-passed at 220 Hz. Audible 115
             ms, 100% of its power under 250 Hz, its loudest 50 ms -6.7 dB re
             the blow. Register at most 0.77 (the death voice) against the
             blow, the death voice, the wall tick and the clank. `move` plays
             it on the first floor contact after a clock close, the caster
             alive. */
          const g = 0.0811, D = 0.187;
          this._tone(t, { freq: 95, to: 42, gain: g, dur: D, type:"sine" });
          this._burst(t, { freq: 220, q: 0.7, gain: g * 0.5, dur: D * 0.5, type:"lowpass" });
        } else {                                        // rune-crack'''),

('tickRise: the shaft-hit tap, once per shaft hit healed, after its blessing, carrying the count',
 '''          T.bless += u.healPer * n;''',
 '''          T.bless += u.healPer * n;
          /* ASCENSION'S SHAFT HIT (v74 §6.2: "a bright glassy tap, 70ms,
             quiet; blessing count in the pitch"): once per shaft hit healed,
             after its blessing lands -- the NEXT live step after the blow,
             once the blow's own hit stop has run -- pitched by the count the
             caster now carries (1-5; at the cap the blessing refreshes and it
             taps at 5's note). The blow keeps its own `hit` voice. A shaft
             hit on a Twinshade shade heals too, so it taps too. Presentation
             only: SFX.play draws nothing, is a no-op headless, and nothing
             here is read back (angelus_voice_lab: fights identical). */
          SFX.play("ult", { w: "angelus-shaft", n: f.stacks("blessing") });'''),

('tickRise: the close, when the window closes by its clock with both alive; the drop is marked',
 '''        f.ultRise = null;''',
 '''        f.ultRise = null;
        /* ASCENSION'S CLOSE (v74 §6.2: "the chord resolving down and the
           ball's landing thud"): the chord only when the window runs out BY
           ITS CLOCK with both fighters alive -- a caster's death closes it in
           a kill flight, and a fight that ends with the window open never
           gets here (step() stops calling this), so both are left to the
           death voice, as Zenith's, Canopy's and Onslaught's closes are. The
           ball drops from here; `falling` (on `riseTally`, which nothing in
           the simulation reads) tells `move` that its next floor contact is
           the landing. Plain SFX.play; nothing is read back. */
        if (Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive){
          SFX.play("ult", { w: "angelus-close" });
          T.falling = 1;
        }'''),

('move: the landing thud, on the first floor contact after a clock close, the caster alive',
 '''      this.spawnFx(f.x, f.y, f.aff.core, 3, 90, 0.3, 2);''',
 '''      this.spawnFx(f.x, f.y, f.aff.core, 3, 90, 0.3, 2);
      /* ASCENSION'S LANDING (v74 §6.2: "... and the ball's landing thud"):
         the first floor contact after the window closed by its clock, the
         caster alive -- over the wall tick this contact plays anyway, which
         is not a thud. A drop knocked about on its way down still lands, and
         thuds then. `riseTally` is the probe's tally; nothing in the
         simulation reads it. Presentation only; nothing is read back. */
      if (f.riseTally && f.riseTally.falling && f.alive && f.y >= hiY){
        f.riseTally.falling = 0;
        SFX.play("ult", { w: "angelus-land" });
      }'''),

('ascension picture: fighter fields',
 '''    this.ultRise = null;
    this.riseTally = null;
''',
 '''    this.ultRise = null;
    this.riseTally = null;
    /* ASCENSION'S PICTURE (v74 section 6.1), and none of it is the sim's:
       the shafts shorten and the halo goes AFTER `ultRise` is gone -- by the
       clock, by the caster's death, or at the kill, where `tickRise` never
       runs again and leaves the window open -- so the picture keeps its own
       state. On the FIGHTER and never on `m.ultFx` (one slot, and the
       opponent's cast takes it: open item 25). Driven in `tickPresentation`
       (`tickAscend`); nothing in the simulation reads any of it.
         ascendFade -- 1 while the window is open, the match live and the
                       caster alive; eased to 0 over the close
         ascendAge  -- the presentation clock since the cast
         ascendLit  -- the presentation clock since the shafts lit; -1 before
         ascendOut  -- the presentation clock since the close
         ascendSeen -- `hits` and `riseTally.bless`, as last seen
         ascendHeal -- the presentation clock since a heal landed (the
                       halo's flare)
         ascendFx   -- a shaft blow's thread up the shaft (records) */
    this.ascendFade = 0;
    this.ascendAge = 0;
    this.ascendLit = -1;
    this.ascendOut = 0;
    this.ascendSeen = [0, 0];
    this.ascendHeal = 9;
    this.ascendFx = [];
'''),

('ascension picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickAscend(dt);                // ASCENSION'S PICTURE (v74 section 6.1)
'''),

('ascension picture: tickAscend',
 '''  tickWinnow(dt){
''',
 '''  /* ---------------------------------------------- ASCENSION'S PICTURE ---
     v74 section 6.1, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.6 is the
     close's 0.3s (the shafts shorten to blades, the halo goes), 0.5 a
     thread's 0.25s run up the shaft, 0.6 the halo's 0.3s flare on a
     heal. THE WINDOW IS READ OFF `ultRise && !over
     && alive` (Canopy's rule): `tickRise` never runs again once `over` is
     set, so a window open at the kill -- 57% of fights (v104 reading 10) --
     would otherwise hang its shafts and halo through the whole verdict; here
     they shorten and go on this clock, which keeps running under it.
     A SHAFT BLOW IS FOUND BY WATCHING `hits` RISE while the shafts are lit
     (the blow's own ledger -- a blow on one of Twinshade's shades counts,
     and heals, too: v104 reading 11), and its thread starts where the blow
     landed: the `hit` beat `resolveHit` filed for it this step, read and
     never written. THE HEAL IS FOUND BY WATCHING `riseTally.bless` RISE (it
     lands on the next live step, after the blow's hit stop), so the tick
     makes no call for the picture: the halo flares gold and the BLESSING
     tag goes up on the caster, with its count. ONE BLESSING TAG ON THE
     CASTER AT A TIME (Tendril's and Temper's rule): a tag already up there
     takes the new count in place. Writes presentation fields, `tags` and
     `taught` only, and draws no rng. */
  tickAscend(dt){
    for (const f of [this.a, this.b]){
      const T = f.riseTally;
      if (!T && !(f.ascendFade > 0)) continue;                 // <- zero burden
      for (let i = f.ascendFx.length - 1; i >= 0; i--){
        const q = f.ascendFx[i];
        q.t += dt;
        if (q.t >= 0.5) f.ascendFx.splice(i, 1);
      }
      const Z = (this.over || !f.alive) ? null : f.ultRise;
      if (Z){
        if (!(f.ascendFade > 0) || f.ascendOut > 0){            // a cast
          f.ascendAge = 0; f.ascendOut = 0; f.ascendLit = -1; f.ascendFx.length = 0;
        }
        f.ascendFade = 1;
        f.ascendAge += dt;
        if (Z.lit) f.ascendLit = f.ascendLit < 0 ? 0 : f.ascendLit + dt;
      } else if (f.ascendFade > 0){
        f.ascendOut += dt;
        f.ascendFade = Math.max(0, 1 - f.ascendOut / 0.6);
        f.ascendAge += dt;
        if (f.ascendLit >= 0) f.ascendLit += dt;
      }
      if (!T) continue;
      const side = f === this.a ? 0 : 1, Rb = CONFIG.physics.ballR;
      if (f.ascendHeal < 9) f.ascendHeal += dt;
      const nh = f.hits - f.ascendSeen[0], nb = T.bless - f.ascendSeen[1];
      f.ascendSeen[0] = f.hits; f.ascendSeen[1] = T.bless;
      if (nh > 0 && Z && Z.lit){
        /* THE BLOW'S THREAD: the newest `hit` beats this side filed this
           step (each blow's contact point), each laid on the shaft nearest
           its bearing, at its distance along it. */
        const B = this.beats, S = f.bladeSet || f.w.blades;
        let n = 0;
        for (let j = B.length - 1; j >= 0 && n < nh; j--){
          const b = B[j];
          if (b.t !== this.t) break;
          if (b.kind !== "hit" || b.side !== side) continue;
          n++;
          const dx = b.x - f.x, dy = b.y - f.y, d = Math.hypot(dx, dy);
          if (d < Rb + 8) continue;
          let bi = 0, bc = -2;
          for (let i = 0; i < S.length; i++){
            const q = f.theta + S[i] * TAU, cs = (Math.cos(q) * dx + Math.sin(q) * dy) / d;
            if (cs > bc){ bc = cs; bi = i; }
          }
          f.ascendFx.push({ i: bi, d: d * bc, t: 0 });
        }
        if (f.ascendFx.length > 8) f.ascendFx.splice(0, f.ascendFx.length - 8);
      }
      if (nb > 0 && f.alive && !this.over){
        f.ascendHeal = 0;                                       // the halo flares
        const k = f.stacks("blessing");
        const g = this.tags.find(g2 => g2.key === "blessing" && !g2.first && g2.life > 0.3
                                       && Math.hypot(g2.x - f.x, g2.y - f.y) < Rb * 3);
        if (g) g.val = k;
        else {
          const first = !this.taught.blessing && !!STATUS.blessing.tip;
          if (first) this.taught.blessing = true;
          this.statusTag(f.x, f.y, "blessing", first, k);
        }
      }
    }
  }

  tickWinnow(dt){
'''),

('ascension picture: the world call (under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* ASCENSION'S GROUND (v74 section 6.1): the column the ball rises on,
       the halo it hangs in, the pools where the shafts meet the hall. The
       WORLD pass and under both balls (CLAUDE.md section 4.1b); nothing of
       it reaches the bloom (section 4.1c). */
    if (__world) this.drawAscend(m);
'''),

('ascension picture: the emissive call (over both fighters)',
 '''    this.drawSunTop(m);
''',
 '''    this.drawSunTop(m);
    /* ASCENSION'S SHAFT CORES, over both fighters: the one part of the
       shafts under `lighter` (v74 section 6.1), both shells cut out; and a
       shaft blow's thread over them. */
    this.drawAscendTop(m);
'''),

("ascension picture: the shafts' hook in drawWeapon",
 '''    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;
''',
 '''    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;
    /* ASCENSION'S SHAFTS (v74 section 6.1): while the shafts are lit and
       while they shorten, the blades are drawn at their REST length and the
       light runs on from them to the edge of the live hall
       (`drawAscendWeapon`) -- `reachMul` is 10 and would draw the blade art
       ~680 units long, past every wall, and it stays 10 through the verdict
       when the match ends in the window. `ascendFade` is 0 and `ultRise` null
       on every other relic, so this is two comparisons on fields nothing
       else writes. */
    if ((f.ascendFade > 0 || f.ultRise) && this.drawAscendWeapon(m, f, dim)) return;
'''),

("ascension picture: the body trail's ghost",
 '''    const tr = f.trail;
''',
 '''    /* ASCENSION (v74 section 6.1): the body trail is fed by `move`, which a
       pinned ball skips, and `tickRise` carries the ball away from it -- so
       for the whole window the trail sat where the cast was, a ghost of the
       ball on the floor it left. Not drawn while the picture is up; `move`
       refills it within 0.15s of the release, inside the close.
       `ascendFade` is 0 on every other relic. */
    const tr = f.ascendFade > 0 ? [] : f.trail;
'''),

('ascension picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------------- THE ASCENSION ---
     ANGELUS / ASCENSION (v74 section 6.1). THE RISE: the ball lifts to the
     hang point over 0.35s on a column of light from the floor, which fades
     once it hangs; a halo ring (r 1.1R, the school's glow, source-over, not
     `lighter`) comes up over the rise and marks it hanging. THE SHAFTS: each
     blade is drawn at its REST length and its light runs on from the shell to
     the wall or the floor -- a soft-edged bar 10 wide at 0.55 with a hot
     3-unit core -- CLIPPED AT THE LIVE HALL: the hit segment runs ~654 units,
     past every wall, and the picture stops where the hall does. Each shaft's
     foot throws a small pool of light where it meets the hall, and light
     motes drift down the shafts (the design's field, drawn). A SHAFT HIT: the
     blade's own flash, a gold thread with a bead running up the shaft from
     the blow to the ball (Zenith's "what it burns heals", along the light),
     and when the heal lands the halo flares gold and BLESSING n goes up on
     the caster. THE CLOSE: the shafts shorten to blades over 0.3s and the
     halo goes; the ball drops (the engine's, not drawn). AT THE KILL the
     same, on the presentation clock: `reachMul` stays 10 through the
     verdict, so the blades are drawn at rest here.

     IT HANGS OFF THE FIGHTER (`ascendFade`, `ascendAge`, `ascendLit`,
     `ascendOut`, `ascendHeal`, `ascendFx`), never `m.ultFx` (open item 25).
     THREE PASSES. `drawAscend` is the WORLD pass under both balls (the
     column, the halo, the pools). `drawAscendWeapon` draws the shaft bodies
     and the motes inside `drawWeapon`, in the world pass, the foe's shell
     cut out as it is for every weapon. `drawAscendTop` draws the cores
     under `lighter` and the threads over them, over both fighters with both
     shells cut out.
     PRESENTATION ONLY: no rng, no spawnFx, no Math.random -- shellHash and
     the clocks -- and nothing here writes a field the simulation reads. */
  drawAscend(m){
    const a = m.a, b = m.b;
    if (!(a.ascendFade > 0) && !(b.ascendFade > 0)) return;       // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    for (const f of [a, b]){
      if (!(f.ascendFade > 0) || !f.alive) continue;
      this._ascendColumn(m, f);
      this._ascendHalo(m, f);
      this._ascendPools(m, f);
    }
    c.globalAlpha = 1;
    c.restore();
  }

  /* THE COLUMN: from the ball down to the floor while it rises; it fades
     once the ball hangs. */
  _ascendColumn(m, f){
    const c = this.ctx, R = CONFIG.physics.ballR, yF = CONFIG.arena.h - (m.inset || 0), P = f.aff;
    const kc = f.ascendFade * (f.ascendLit < 0 ? Math.min(1, f.ascendAge / 0.1)
                                               : Math.max(0, 1 - f.ascendLit / 0.8));
    if (!(kc > 0.01) || !(f.y < yF)) return;
    const hw = R * 0.8;
    const g = c.createLinearGradient(f.x - hw, 0, f.x + hw, 0);
    g.addColorStop(0, P.glow + "00"); g.addColorStop(0.5, P.glow); g.addColorStop(1, P.glow + "00");
    c.globalAlpha = 0.24 * kc;
    c.fillStyle = g;
    c.fillRect(f.x - hw, f.y, 2 * hw, yF - f.y);
    c.globalAlpha = 0.45 * kc;
    c.fillStyle = P.core;
    c.fillRect(f.x - 1.5, f.y, 3, yF - f.y);
  }

  /* THE HALO: r 1.1R round the shell, up over the rise, gone with the
     close. Under the ball, so the shell covers its inside. A HEAL LANDED:
     it flares gold and swells a little. */
  _ascendHalo(m, f){
    const c = this.ctx, R = CONFIG.physics.ballR;
    const kh = f.ascendFade * Math.min(1, f.ascendAge / 0.7);
    if (!(kh > 0.01)) return;
    c.globalAlpha = 0.85 * kh;
    c.strokeStyle = f.aff.glow; c.lineWidth = 2.6;
    c.beginPath(); c.arc(f.x, f.y, R * 1.1, 0, TAU); c.stroke();
    if (f.ascendHeal < 0.6){
      const kf = f.ascendHeal / 0.6;
      c.globalAlpha = kh * (1 - kf) * 0.95;
      c.strokeStyle = "#FFC24A"; c.lineWidth = 2.6 + 3.4 * (1 - kf);
      c.beginPath(); c.arc(f.x, f.y, R * 1.1 + 5 * kf, 0, TAU); c.stroke();
    }
  }

  /* THE POOLS: where each lit shaft meets the hall, flattened along the edge
     it meets; they leave the edge with the shaft on the close. */
  _ascendPools(m, f){
    if (f.ascendLit < 0) return;
    const c = this.ctx, R = CONFIG.physics.ballR, fade = f.ascendFade, P = f.aff;
    const Z = f.ultRise, live = !!(Z && Z.lit) && !m.over;
    const e = live ? 1 : fade * fade * (3 - 2 * fade), kp = e * e * e * e;
    if (!(kp > 0.01)) return;
    const S = f.bladeSet || f.w.blades;
    for (let i = 0; i < S.length; i++){
      const q = f.theta + S[i] * TAU, cq = Math.cos(q), sq = Math.sin(q);
      const E = this._ascendEdge(m, f.x, f.y, cq, sq);
      if (E[0] > R + f.w.reach * m.actMods.reach * f.w.ult.shaft) continue;
      c.save();
      c.translate(f.x + cq * E[0], f.y + sq * E[0]);
      if (E[1]) c.scale(0.33, 1); else c.scale(1, 0.33);
      const g = c.createRadialGradient(0, 0, 0, 0, 0, 18);
      g.addColorStop(0, P.glow); g.addColorStop(1, P.glow + "00");
      c.globalAlpha = 0.45 * kp;
      c.fillStyle = g;
      c.beginPath(); c.arc(0, 0, 18, 0, TAU); c.fill();
      c.restore();
    }
  }

  /* The distance from (x, y) along (ux, uy) to the edge of the live hall,
     and whether that edge is a wall (1) or the floor or ceiling (0). */
  _ascendEdge(m, x, y, ux, uy){
    const A = CONFIG.arena, n = m.inset || 0;
    let d = Infinity, w = 0;
    if (ux > 1e-6){ const t = (A.w - n - x) / ux; if (t < d){ d = t; w = 1; } }
    else if (ux < -1e-6){ const t = (n - x) / ux; if (t < d){ d = t; w = 1; } }
    if (uy > 1e-6){ const t = (A.h - n - y) / uy; if (t < d){ d = t; w = 0; } }
    else if (uy < -1e-6){ const t = (n - y) / uy; if (t < d){ d = t; w = 0; } }
    return [Math.max(0, d), w];
  }

  /* A shaft's drawn end, from the ball's centre: the hit segment's end or the
     live hall's edge, whichever is nearer, shortened to the rest blade's tip
     as `e` goes 1 -> 0. */
  _ascendLen(m, f, q, e){
    const R = CONFIG.physics.ballR, rr = f.w.reach * m.actMods.reach;
    const dE = this._ascendEdge(m, f.x, f.y, Math.cos(q), Math.sin(q))[0];
    const Lf = Math.min(dE, R + rr * f.w.ult.shaft), Lt = Math.min(Lf, R + rr);
    return Lt + (Lf - Lt) * e;
  }

  /* THE SHAFTS, inside `drawWeapon`. False during the rise (the ordinary
     blades, `reachMul` 1); true while lit, while they shorten, and through a
     verdict that left the window open. */
  drawAscendWeapon(m, f, dim){
    const Z = f.ultRise, hung = !!(Z && Z.lit), live = hung && !m.over && f.alive;
    if (!hung && !(f.ascendFade > 0 && f.ascendLit >= 0)) return false;
    const c = this.ctx, R = CONFIG.physics.ballR, W = f.w.artW, P = f.aff;
    const S = f.bladeSet || f.w.blades, fade = f.ascendFade;
    const L0 = f.w.reach * m.actMods.reach + 6;                // the blade at rest
    const e = live ? 1 : fade * fade * (3 - 2 * fade);
    if (e > 0.002 && f.ascendLit >= 0){
      const A = CONFIG.arena, n = m.inset || 0;
      const ign = live && f.ascendLit < 0.24 ? 1 + 0.5 * (1 - f.ascendLit / 0.24) : 1;
      const al = dim * Math.min(1, 0.55 * ign) * (live ? 1 : 0.35 + 0.65 * fade);
      c.save();
      c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
      for (let i = 0; i < S.length; i++){
        const q = f.theta + S[i] * TAU, Ld = this._ascendLen(m, f, q, e);
        if (Ld < R + 2) continue;
        c.save();
        c.translate(f.x, f.y); c.rotate(q);
        this._ascendBody(f, Ld, al);
        this._ascendMotes(m, f, i, Ld, al);
        c.restore();
      }
      c.restore();
    }
    /* THE BLADES AT REST, over the light: the ordinary path's own drawing. */
    for (const off of S){
      const a = f.theta + off * TAU;
      c.save();
      c.globalAlpha = dim;
      c.translate(f.x, f.y); c.rotate(a); c.translate(R - 6, 0);
      const _g = weaponGlow(f.w.shape, L0, W, P, f.drawK, 20);
      c.drawImage(_g.cv, _g.ox, _g.oy);
      if (!litWeapon(c, f.w.shape, L0, W, P, f.drawK, a)){
        const fn = SHAPES[f.w.shape];
        if (fn) fn(c, L0, W, P, f.drawK);
      }
      c.restore();
    }
    return true;
  }

  /* THE BODY, in the shaft's own frame: a soft-edged bar, source-over,
     warm at its edge so it reads as light and not as a white rod. */
  _ascendBody(f, Ld, al){
    const c = this.ctx, R = CONFIG.physics.ballR, P = f.aff;
    const g = c.createLinearGradient(0, -7, 0, 7);
    g.addColorStop(0, "#FFD98A" + "00"); g.addColorStop(0.18, "#FFD98A"); g.addColorStop(0.36, P.glow);
    g.addColorStop(0.64, P.glow); g.addColorStop(0.82, "#FFD98A"); g.addColorStop(1, "#FFD98A" + "00");
    c.globalAlpha = al;
    c.fillStyle = g;
    c.fillRect(R + 1, -7, Ld - R - 1, 2 * 7);
  }

  /* THE MOTES, drifting down the shaft just outside its body, where the dark
     floor shows them (shellHash and the clock; the design's field, drawn). */
  _ascendMotes(m, f, i, Ld, al){
    const c = this.ctx, R = CONFIG.physics.ballR, T = m.t + (m.deathAge || 0);
    c.fillStyle = "#FFF1CC";
    for (let j = 0; j < 8; j++){
      const h = shellHash(7401 + i, j), h2 = shellHash(7403 + i, j);
      const d = R + 10 + ((T * 90 * (0.8 + 0.4 * h2) + h * 640) % 640);
      if (d > Ld - 3) continue;
      const k = Math.min(1, (Ld - d) / 40) * Math.min(1, (d - R - 10) / 30);
      const y = (j % 2 ? 1 : -1) * (7 + 1.5 + 3 * h2) + Math.sin(T * 2.1 + j * 1.7 + i) * 1.6;
      c.globalAlpha = Math.min(1, al * 1.6) * k;
      c.beginPath();
      c.arc(d, y, 1.3 + 0.8 * h2, 0, TAU);
      c.fill();
    }
  }

  /* THE THREADS: a blow's gold line up the light and a bead running home to
     the ball, in the shaft's own frame, so they ride it as it turns (drawn by
     `drawAscendTop`, over the core). */
  _ascendThreads(f, i, Ld, dim){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const x of f.ascendFx){
      if (x.i !== i) continue;
      const kt = x.t / 0.5, d0 = Math.min(x.d, Ld);
      if (kt >= 1 || d0 < R + 8) continue;
      const d1 = R + 2, db = d0 + (d1 - d0) * (1 - (1 - kt) * (1 - kt));
      c.globalAlpha = dim * 0.95 * (1 - kt * kt);
      c.lineCap = "round";
      c.strokeStyle = "#E89A1E"; c.lineWidth = 4;
      c.beginPath(); c.moveTo(d0, 0); c.lineTo(Math.max(d1, db), 0); c.stroke();
      c.strokeStyle = "#FFC24A"; c.lineWidth = 1.6; c.stroke();
      c.globalAlpha = dim * Math.min(1, 1.3 * (1 - kt * kt * kt));
      c.fillStyle = "#FFD66B"; c.strokeStyle = "#5A4E30"; c.lineWidth = 1.4;
      c.beginPath(); c.arc(db, 0, 6, 0, TAU); c.fill(); c.stroke();
      c.fillStyle = "#FFF8E6";
      c.beginPath(); c.arc(db, 0, 2.4, 0, TAU); c.fill();
    }
  }

  /* ...and the cores and the threads, over both fighters (see `drawAscend`). */
  drawAscendTop(m){
    const a = m.a, b = m.b;
    if (!(a.ascendFade > 0) && !(b.ascendFade > 0)) return;       // <- zero burden
    const c = this.ctx, A = CONFIG.arena, R = CONFIG.physics.ballR, n = m.inset || 0;
    c.save();
    for (const f of [a, b]){
      const fade = f.ascendFade;
      if (!(fade > 0) || !f.alive || f.ascendLit < 0) continue;
      const Z = f.ultRise, live = !!(Z && Z.lit) && !m.over;
      const e = live ? 1 : fade * fade * (3 - 2 * fade);
      if (e < 0.002) continue;
      const foe = f === a ? b : a, S = f.bladeSet || f.w.blades;
      const dim = f.stun > 0 ? 0.42 : 1;
      const ign = live && f.ascendLit < 0.24 ? 1 + 0.5 * (1 - f.ascendLit / 0.24) : 1;
      c.save();
      c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n);
      c.moveTo(f.x + R, f.y); c.arc(f.x, f.y, R, 0, TAU);
      if (foe.alive){ c.moveTo(foe.x + R * 0.98, foe.y); c.arc(foe.x, foe.y, R * 0.98, 0, TAU); }
      c.clip("evenodd");
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = dim * Math.min(1, 0.8 * ign) * (live ? 1 : 0.35 + 0.65 * fade);
      c.strokeStyle = f.aff.core; c.lineWidth = 3; c.lineCap = "butt";
      for (let i = 0; i < S.length; i++){
        const q = f.theta + S[i] * TAU, Ld = this._ascendLen(m, f, q, e);
        if (Ld < R + 2) continue;
        const cq = Math.cos(q), sq = Math.sin(q);
        c.beginPath(); c.moveTo(f.x + cq * R, f.y + sq * R); c.lineTo(f.x + cq * Ld, f.y + sq * Ld); c.stroke();
      }
      /* THE THREADS, OVER THE CORES and source-over: drawn under them, a
         gold line on a white shaft was washed out by the core. */
      if (f.ascendFx.length){
        c.globalCompositeOperation = "source-over";
        for (let i = 0; i < S.length; i++){
          if (!f.ascendFx.some(x => x.i === i)) continue;
          const q = f.theta + S[i] * TAU, Ld = this._ascendLen(m, f, q, e);
          c.save();
          c.translate(f.x, f.y); c.rotate(q);
          this._ascendThreads(f, i, Ld, dim);
          c.restore();
        }
      }
      c.restore();
    }
    c.restore();
  }

  drawMotes(m){
'''),

]

# STAGE 6'S NAMES, free on the base on identifier boundaries, and what its
# inserts may write: their own `ascend*` fields, a thread record's clock, a
# tag's count, `taught`, the landing flag on the probe's tally, the canvas and
# the synth's own nodes. Everything else is the simulation's.
S6_NAMES = ("tickAscend", "drawAscend", "drawAscendTop", "drawAscendWeapon", "_ascendColumn", "_ascendHalo",
            "_ascendPools", "_ascendEdge", "_ascendLen", "_ascendBody", "_ascendMotes", "_ascendThreads",
            "ascendFade", "ascendAge", "ascendLit", "ascendOut", "ascendSeen", "ascendHeal", "ascendFx",
            "angelus-shaft", "angelus-close", "angelus-land")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("ascend") or obj.startswith("ascend") or obj == "c"
               or (obj, prop) in {("q", "t"), ("g", "val"), ("taught", "blessing"), ("T", "falling"),
                                  ("riseTally", "falling"), ("frequency", "value")})
S6_ARRAY_OK = (lambda obj: obj.startswith("ascend"))
# THE THREE CALLS ON THE SIM PATH, whole (reading 14): each row's added code,
# comments stripped, line for line.
S6_SIM_LINES = {
    "tickRise: the shaft-hit tap": ['SFX.play("ult", { w: "angelus-shaft", n: f.stacks("blessing") });'],
    "tickRise: the close": ["if (Z.t >= Z.dur && f.alive && (f === this.a ? this.b : this.a).alive){",
                            'SFX.play("ult", { w: "angelus-close" });', "T.falling = 1;", "}"],
    "move: the landing thud": ["if (f.riseTally && f.riseTally.falling && f.alive && f.y >= hiY){",
                               "f.riseTally.falling = 0;", 'SFX.play("ult", { w: "angelus-land" });', "}"],
}
S6_SFX_ROW = "Sfx: Angelus's cast"
S6_TICK_ROW = "ascension picture: tickAscend"
RUNE_CRACK = "        } else {                                        // rune-crack"


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 17)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    aside) draws no RNG, never takes the one ultFx slot (open item 25), calls
    nothing that hurts, applies, resolves, beats, floats or knocks, never
    writes the shared weapon row, writes only what S6_WRITE_OK names and
    mutates only its own arrays. Its three lines on the sim path are the three
    voice calls, whole, each in its own row; the synth's nodes only in the Sfx
    row; the tag and `taught` only in tickAscend. The probe's [11]-[12] and
    engine_ab are the dynamic proof. Run on every stage: it reads the table."""
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|"
                     r"tickRise|tickStatus|tickStasis|tickWeapon|spawnShot|note|checkEnd)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*\s*(=[^=]|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\b(beat|hurt|knock|ring|shake|hitStop)\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' hurts, knocks, "
                             "stops or files a beat")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        if sim:
            got = [ln.strip() for ln in ins.splitlines() if ln.strip()]
            if got != S6_SIM_LINES[sim[0]]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"('{label}') is not its voice call alone:\n{ins}")
        elif "SFX" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside the tap, the close and the landing")
        if ("_tone(" in ins or "_burst(" in ins) and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if ("statusTag(" in ins or "taught" in ins) and not label.startswith(S6_TICK_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' tags or "
                             "teaches outside tickAscend")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort)\(", ins):
            if not S6_ARRAY_OK(mw.group(1)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_ARRAY_OK(mw.group(1).split(".")[-1]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")


def s6_output_checks(s: str, s0: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched, the
    shared rune-crack fallback kept once and after Angelus's arms, and every
    arm, call and pass wired exactly once."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 17)")
    if s.count(RUNE_CRACK) != 1 or s.find('} else if (w === "angelus-land"){') > s.find(RUNE_CRACK):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Angelus's arms")
    for need in ["this.tickAscend(dt);", "this.drawAscend(m);", "this.drawAscendTop(m);",
                 "this.drawAscendWeapon(m, f, dim)", "const tr = f.ascendFade > 0 ? [] : f.trail;",
                 '} else if (w === "angelus"){', '} else if (w === "angelus-shaft"){',
                 '} else if (w === "angelus-close"){', '} else if (w === "angelus-land"){'] + \
                [ln for v in S6_SIM_LINES.values() for ln in v if ln.startswith("SFX.play(")]:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes "
          "its own fields; the tap, the close and the landing its three lines on the sim path); "
          "the inlined fx.js untouched; the rune-crack fallback kept; every arm, call and pass once")


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


ANCHORS = (
    (ROW_ANCHOR, "the WEAPONS array's closing and the comment under it"),
    ("    this.vineTally = null;\n", "the vineTally field line"),
    ('    if (u.kind === "tendril"){\n', "the tendril cast branch"),
    ("    this.tickTendril(dt);               // TENDRIL (v68)\n", "the tickTendril call"),
    ("  tickWinnow(dt){\n", "tickWinnow"),
    ("(f.ultVine ? 0 : f.w.spin) * f.spinMul(mods.spin)", "tickWeapon's spin product"),
    ("self.ultTree ? self.w.dmg * self.w.ult.winDmg : ", "resolveHit's damage line"),
)


def assert_base(s0: str, code: str, stage: str) -> None:
    """THE BASE BY CONTENT: every feature this builder reads or anchors on."""
    if stage == "1":
        for a, why in ANCHORS:
            if s0.count(a) != 1:
                raise SystemExit(f"wrong base: {why} is there {s0.count(a)}x, not once")
    # WHAT THE MECHANISM LEANS ON, AS THE ENGINE WRITES IT
    for need, why in (
            ("if (f.pin > 0) return;", "`move` no longer returns for a pinned ball"),
            ("const wa = pa ? 0 : (pb ? 1 : 0.5), wb = pb ? 0 : (pa ? 1 : 0.5);",
             "`_ballPair` no longer treats a held ball as immovable"),
            ("if (!f.pinFree) f.stun = Math.max(f.stun, f.pin);",
             "`tickStasis` no longer leaves a pinFree ball's weapon free"),
            ("const reach = f.w.reach * mods.reach * f.reachMul;", "`bladeSegments` no longer reads reachMul"),
            ("f.hp = Math.min(f.maxHp, f.hp + def.hps * st.stacks * dt);", "tickStatus's blessing heal has moved"),
            ("f.theta += spin * dt * f.spinDir;", "the spin mode no longer turns by `spin`"),
            ("self.hits++; self.dealt += dmg;", "resolveHit's hit ledger has moved"),
            ("f.charge += dt;", "the charge no longer runs on the step")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'blessing:\s*\{ name:"Blessing",\s*maxStacks:5, dur:6\.0, hps:1\.2,', code):
        raise SystemExit("wrong base: STATUS.blessing is not {5 stacks, 6s, 1.2 hp/s a stack}")
    if not re.search(r'if \(key === "sanctified"\) return SHAPES\._tbRadiant\(', code):
        raise SystemExit("wrong base: SHAPES.twinblade no longer routes sanctified to _tbRadiant")
    # THE TYPE'S TWINBLADE PROFILE IS STILL WHAT THIS BUILDER COPIES (every
    # twinblade, the donor's blade aside), AND THE SCHOOL'S CHANNEL IS WHERE IT WAS.
    for tb in TWINBLADES:
        if not re.search(TYPE_RE, " ".join(relic_row(code, tb).split())):
            raise SystemExit(f"{tb} is not the type's twinblade profile any more")
    for sn in SANCTIFIED:
        if "onHit:{ smite:1 }" not in relic_row(code, sn):
            raise SystemExit(f"{sn} does not carry the school's channel, smite 1")
    others = [m for m in re.findall(r'\{ id:"([a-z]+)", name:"[^"]*", aff:"sanctified", shape:"twinblade"', code)
              if m != RELIC]
    if others:
        raise SystemExit(f"a sanctified twinblade is already on the roster: {others}")
    if stage == "1":
        for name in NAMES:
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-angelus"):
        raise SystemExit(f"refusing to write {out_p.name}: this relic's links are sc-angelus*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    if A.stage == "5" and BLADE is None:
        raise SystemExit("stage 5 has no blade yet -- v104 §4 sets it")

    raw = src_p.read_bytes()
    if b"\r\n" in raw:
        raise SystemExit("the source is not LF text")
    s0 = raw.decode("utf-8")
    s = s0
    print(f"\nANGELUS / ASCENSION -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    assert_base(s0, code, A.stage)
    print("  base  by content: the anchors, the five twinblades' profile, the sanctified "
          "channel, the radiant head route, blessing, the pin's hold")

    if A.stage == "1":
        if f'id:"{RELIC}"' in code:
            raise SystemExit("this source already carries Angelus -- built")
        edits, want = S1, ult_block("1e9", 0)
    else:
        if f'id:"{RELIC}"' not in code:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        blk0 = relic_ult(code)
        row0 = relic_row(code, RELIC)
        if A.stage == "2":
            if "ultRise" in code or "charge:1e9," not in blk0:
                raise SystemExit("stage 2 goes on stage 1, once")
            for a, why in ANCHORS[1:]:
                if s0.count(a) != 1:
                    raise SystemExit(f"wrong base: {why} is there {s0.count(a)}x, not once")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "ultRise" not in code or "healPer:0," not in blk0:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["healPer"])
        elif A.stage == "5":
            if (f'healPer:{ULT["healPer"]},' not in blk0
                    or PHYS_OF(LAB_BLADE) not in " ".join(row0.split())):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = s5_edits(), ult_block(ULT["charge"], ULT["healPer"])
        else:
            # STAGE 6 GOES ON STAGE 5, ONCE: the heal on, the blade BLADE names,
            # none of stage 6's names in the source yet (on identifier
            # boundaries), and the picture's hash function there to read.
            if (f'healPer:{ULT["healPer"]},' not in blk0 or "tickRise(dt){" not in code
                    or PHYS_OF(BLADE) not in " ".join(row0.split())):
                raise SystemExit("stage 6 goes on stage 5 (the heal, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if ".falling" in code or 'w === "angelus"' in code:
                raise SystemExit("Angelus's cast voice or its landing flag is already in this "
                                 "source -- stage 6 goes on once")
            if "function shellHash(" not in code:
                raise SystemExit("wrong base: no shellHash (the picture's hash, never the RNG)")
            edits, want = S6, ult_block(ULT["charge"], ULT["healPer"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Angelus's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the brief's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    blade = BLADE if A.stage in ("5", "6") else LAB_BLADE
    if PHYS_OF(blade) not in " ".join(relic_row(out_code, RELIC).split()):
        raise SystemExit(f"REFUSING TO WRITE -- Angelus's row is not the twinblade profile at {blade}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, old, new in S1 + S2 + S3 + (s5_edits() if BLADE is not None else []):
        # WHAT THE INSERT ADDS: an anchor it re-emits is the base's, not the insert's.
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*\s*(=[^=]|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\b(beat|hurt|knock|ring|shake|hitStop)\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' hurts, knocks, "
                             "stops or files a beat")
    s6_static_checks()
    if A.stage == "6":
        s6_output_checks(s, s0, out_code)
    if len(re.findall(r'kind:"rise"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one rise ultimate")
    if A.stage != "1":
        for site, pat in (
                ("tickWeapon's spin", r"const spin = \(f\.ultVine \? 0 : f\.w\.spin\)\s*\* \(f\.ultRise && f\.ultRise\.lit \? f\.w\.ult\.shaftSpin : 1\) \* f\.spinMul\(mods\.spin\)"),
                ("resolveHit's damage", r"let dmg = \(self\.ultTree \? self\.w\.dmg \* self\.w\.ult\.winDmg : self\.ultRise && self\.ultRise\.lit \? self\.w\.dmg \* self\.w\.ult\.winDmg : [^\n]*self\.w\.dmg\)")):
            if not re.search(pat, out_code):
                raise SystemExit(f"REFUSING TO WRITE -- {site} is not where the build put it")
        # THE TICK'S SLOT: once, after tickTendril (after every mover and
        # ballCollision, after tickStasis) and before the hit loops.
        i_tt = out_code.find("this.tickTendril(dt);")
        i_tr = out_code.find("this.tickRise(dt);")
        i_th = out_code.find("this.tickHits(self, foe, dt);")
        if out_code.count("this.tickRise(dt);") != 1 or not (0 <= i_tt < i_tr < i_th):
            raise SystemExit("REFUSING TO WRITE -- tickRise is not called once, after "
                             "tickTendril and before tickHits")
        print("  ok    the spin product, the damage line, and tickRise before tickHits")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one rise ultimate, Angelus's; no insert draws the RNG, takes the "
          f"ultFx slot, writes the shared weapon or files a beat; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
