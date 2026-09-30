#!/usr/bin/env python
"""IRONHAIL / QUARRELSTORM, REDESIGNED -- iron hail falls on the foe. v108.

Built from `06-docs/v83/ironhail-quarrelstorm-redesign-v83.md` (Cowork,
2026-09-26), its §5 build brief and its runs (`06-docs/v83/runs/hail_*`,
`tools/overlays/hail.js`), which are the input and the only input. CLAUDE.md
§3 rule 0: nothing here is a design decision. A REDESIGN: the relic ships in
the base; its ultimate is replaced.

    stage 1   the new ultimate stubbed (1e9); the nova out
                                          <tip> -> sc-ironhail-stub.html  (= arm A)
    stage 2   the hail, no sunder         -> sc-ironhail-hail.html        (arm B, brief stage 1)
    stage 3   the sunder                  -> sc-ironhail-sunder.html      (arm C, brief stage 2)
                                                                          THE FINAL LINK
    stage 5   the blade HOLDS at 16.23, the shipped rate (brief stage 3): nothing to write;
              `--stage 5 --alt50` writes Rick's other choice, 50%, blade 14
                                          -> sc-ironhail-b14.html         (not the carry)
    stage 6   picture, voice (brief stage 4) -> sc-ironhail-sunder-fx.html
              (on the final; the nova's field spec leaves BOTH copies of fx.js
              by the orchestrator's sync_fx_remove, not here: reading 20)

THE CARRY is stages 1, 2, 3 and 6. Stage 3's link is the final mechanism: the
brief's target is the shipped rate, and on 151 the redesign reads it at the
shipped blade (below, stage 5). Stage 6 (the picture and the voice) goes on it.

§1: "For a duration iron falls. Every third of a second a bolt drops from the
top of the hall onto where the enemy is, and lands a moment later; an enemy
still standing there when it lands is struck and sundered. The bow keeps
firing."

Declared (§4, the lab `overlays/hail.js` at the taken point `--P fallT=0.3
hitR=60 dropDmg=4`):
  THE HAIL    for the window a bolt drops every `dropCd` (0.4s) at the foe's
              position (x, y) at that frame -- the first on the cast frame --
              and lands `fallT` (0.3s) later.
  A LANDING   the foe's centre within hitR + R (60 + R) of the spot:
              hurt(foe, dropDmg, f) -- 4, ward first, and nothing else (no
              crit, no jitter, no sunder multiplier, no act multiplier, no
              knock, no hit stop but a ward's own shatter inside hurt) -- then
              foe.apply("sunder", 1) (stage 3). A miss does nothing.
  Drops in the air when the window closes still land. No rng.
  The bow keeps firing: tickWeapon, tickFire and resolveHit are untouched.

THE CHARGE. The design names none. Every run it was priced on
(`hail_*.json`: "charge": 16.0) cast every 16 seconds of the LAB's step
clock, the harness's default, which counts hit-stop freezes. Rick,
2026-09-27, for the whole batch: "use the game's equivalent". Measured for
this fighter on the lab's arm C at the taken point (v108 §0): 14. (The shipped
Quarrelstorm was 15 on the engine's clock.)

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE CADENCE IS 0.4s. §1's prose says "every third of a second"; the
     clause line under it ("a drop every 0.4s"), §4 ("A drop every 0.4s of
     the window") and the lab (`dropCd ?? 0.4`, every hail_* run) say 0.4,
     and 0.4 is what was priced. Flagged for Rick.
  2. THE WINDOW IS 8s: §1 says "for a duration"; every run used the
     harness's dur 8.
  3. THE CHARGE is the lab's 16 converted (above).
  4. THE HIT TEST is the foe's centre strictly within hitR + R of the spot on
     the landing frame (§4 "within 60 + R"; the lab's `<`).
  5. THE LANDING IS FLAT: hurt(foe, dropDmg, f) and nothing else -- the lab's
     H.hurt. `f.hits` and `f.dealt` are the bow's and are not touched.
  6. THE SUNDER lands on every landing, after the hurt, a killing one
     included (the lab's; the brief's gate "sunder = landings").
  7. `apply`'s SOURCE IS A SIDE LETTER (the engine's contract; §4 and the lab
     pass the Fighter, and sunder has no reader of it). `hurt`'s source is the
     caster Fighter (its contract: a ward's shatter bursts at it).
  8. A LANDING THAT KILLS files its own fatal hit beat (Rick's standing rule
     for a side-channel kill); no other landing, drop or miss files one.
  9. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`),
     and the hail never falls on the caster (§6.3, the design's default: "it
     does not -- the sky knows its master").
 10. DROPS IN THE AIR STILL LAND however the window closed (§4): a landing
     needs a live foe (the lab's), not a live caster.
 11. THE WINDOW CLOSES on its clock or EITHER death (the lab's); nothing drops
     after the close.
 12. NO CAST WAITS. The design asks none, and a cast cannot find its window
     open: the charge is pure unfrozen time, 14 against a window of 8. Bolts
     still falling from the last window are the match's (`m.hail`), not the
     window's.
 13. THE CARD is the design's own 68-character alternate; its first line is 74,
     over verify's 72-character cap. Measured in pixels (§4 "measure in
     pixels"; v108 §0): 539px on one line, two lines in the ult bar's 390px
     (nothing dropped) and 21px in two lines on the scrunch panel.
 14. NOVA OUT (brief stage 1): `kind:"volley"` was Ironhail's alone, so its
     cast branch in `fireUlt` is retired. `spawnShot` stays: every bow fires
     through it. The nova's PICTURE (the release flash and floor dust keyed on
     `ultFx.w === "ironhail"`, the charge rune's eight heads), its cast voice
     and its field spec (`SPECS.ironhail`) are the brief's stage 4 (stage 6
     here) and still play at the cast until then; nothing in the simulation
     reads any of them.

STAGE 6'S READINGS -- the labs', where the words leave the build a choice (art
and sound are Code's picks under "you pick i overrule"; v108 §5):
 15. THE CAST VOICE is the cast's own `SFX.play("ult", {w: "ironhail"})` in
     fireUlt's generic head, which fell through to rune-crack: an arm is ADDED
     before that shared fallback (the bellows huff) and the fallback line is
     re-emitted unchanged for the relics that still fall through.
 16. THE LANDING VOICE plays once per landed bolt, in tickHail after its hurt
     and its sunder, pitched by the count the foe then carries (the number its
     tag shows, 1-6); a killing landing thuds too, under the death voice.
 17. THE MISS VOICE plays once per missed bolt, on its landing frame, on the
     miss line's own test read first (the anchor guards it: if that line
     changes, the row stops applying).
 18. THE CLOSE HAS NO VOICE (v83 §4: "close -- nothing").
 19. THE PICTURE is drawn from the match's bolts (`m.hail`, read) and the
     fighter's own `quarrel*` fields (never `m.ultFx`, open item 25); a bolt
     that resolves is found by `hailTally` rising, so tickHail makes no call
     for the picture. The limbs read `ultHail && !over` and cool at the
     verdict; a bolt the kill leaves in the air fades on `quarrelEnd`. ONE
     SUNDER TAG ON THE FOE AT A TIME (Tendril's and Temper's rule): a landing
     with a tag already up sets its count in place; a killing landing tags
     nothing (the shatter owns that frame).
 20. "FIELD: IRON-SPARK MOTES ON LANDINGS, BOTH COPIES" IS DRAWN, not an fx.js
     field: a SPECS field fires once, at the cast edge, on the one ultFx slot,
     which Ironhail holds for a median 0.62s of its 8s window; 15 of 417
     landings came while it was still Ironhail's, a median 254 units from the
     field's spawn point. So four motes rise off every landing, drawn. The
     NOVA's field spec (`SPECS.ironhail`, a beam of 1300) is the brief's
     "nova's field spec out": it leaves both copies by the orchestrator's
     sync_fx_remove (fx.js is shared), and this builder never edits either.
 21. THE NOVA'S ART IS RETIRED with the nova: drawUltUnder's floor dust and
     drawUltOver's release flash (keyed on the ultFx slot's "ironhail"), the
     charge rune's eight heads (now three bolts onto a crossed rune) and the
     banner's fan (the letters now fall).

THE CLOCK. The window, the drop cadence and every bolt's fall run on the
window tickers' clock, which stops through a hit stop (Corollary's, Daybreak's,
Zenith's, Canopy's, Onslaught's and Tendril's convention). The lab ran all
three through freezes; v108 §2 measures what that is worth here.

THE BASE is asserted BY CONTENT, never by which relic is last: Ironhail's row
with the shipped Quarrelstorm, the nova's branch used by no other relic, and
every anchor below exactly once. Every insert goes AFTER or BEFORE a stable
line, so the builder re-applies on a later tip that carries other new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "ironhail"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v83 §3-§5.
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v108 §0)
    "dur": 8,         # "for a duration" -- the harness's 8, every hail_* run
    "dropCd": 0.4,    # §4 "a drop every 0.4s of the window"
    "fallT": 0.3,     # §3/§4 "landing at +0.3s" (the taken point; the lab defaults 0.55)
    "hitR": 60,       # §4 "within 60 + R" (the lab defaults 40)
    "dropDmg": 4,     # §3 "(taken)" 4 damage (the lab defaults 5)
    "sunder": 1,      # §4 `foe.apply("sunder", 1, f)` -- stage 3
}
TIP = "Iron hail falls on the foe from above; every bolt that lands sunders"
SHIPPED_ULT = '''    ult:{ name:"Quarrelstorm", charge:15, kind:"volley", shots:14, spread:6.283, dmg:0,
          tip:"Fires a nova of arrows" },
'''
SHIPPED_DMG = "16.23"


def ult_block(charge, sunder) -> str:
    return (f'''    ult:{{ name:"Quarrelstorm", charge:{charge}, kind:"hail", dur:{ULT["dur"]},
          dropCd:{ULT["dropCd"]}, fallT:{ULT["fallT"]}, hitR:{ULT["hitR"]}, dropDmg:{ULT["dropDmg"]},
          sunder:{sunder},          // v83: the sunder (stage 3)
          tip:"{TIP}" }},
''')


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
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH to check the page")
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
# THE NEW ULTIMATE, STUBBED at charge 1e9 (the clock can never reach it, and
# `fireUlt` never runs for this relic), AND THE NOVA OUT. The row keeps every
# physical stat, the bow's shot, the school's channel and the blurb; only the
# ult block changes. Nothing else reads the ult block's fields, so this link
# must be the lab's arm A (the relic with no ultimate) fight for fight.
S1 = [

("Quarrelstorm becomes the hail, stubbed",
 SHIPPED_ULT,
 '''    /* QUARRELSTORM, REDESIGNED (v83; built v108): IRON HAIL. The nova of
       arrows is retired. For the window a bolt drops every `dropCd` onto the
       foe's spot and lands `fallT` later: a foe still within hitR + R takes
       `dropDmg` and is sundered. See `tickHail`. */
''' + ult_block("1e9", 0)),

("the nova is retired: kind \"volley\" was Ironhail's alone",
 '''    if (u.kind === "volley" && f.w.shot){
      const N = u.shots || 12, span = u.spread || TAU;
      for (let i = 0; i < N; i++)
        this.spawnShot(f, f.theta + (i / N) * span - (span >= TAU ? 0 : span/2));
    }
''',
 '''    /* QUARRELSTORM'S NOVA IS RETIRED (v83 §5 stage 1, "nova out"; built
       v108). `kind:"volley"` fired `u.shots` arrows round the bow and was
       Ironhail's alone; its ultimate is now the hail (`kind:"hail"`, above).
       `spawnShot` stays -- every bow fires through it. */
'''),

]

# ---------------------------------------------------------------- stage 2 --
# THE HAIL (brief stage 1: "nova out, `m.hail[]` in"), the sunder written but
# inert at 0, and the charge on the game's clock.
S2 = [

("the hail has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Quarrelstorm", charge:1e9, kind:"hail", dur:8,
''',
 f'''    ult:{{ name:"Quarrelstorm", charge:{ULT["charge"]}, kind:"hail", dur:{ULT["dur"]},   // v83 stage 2: the hail falls
'''),

("the fighter carries the hail's window",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, cd} while IRONHAIL's hail falls (v83). null on every other
       relic and on this one outside its window: `tickHail`'s window loop is
       two iterations that do nothing. The bolts in the air are the MATCH's
       (`m.hail`), because they outlive the window. `hailTally` is the probe's
       count, cumulative over the fight; nothing in the simulation reads it. */
    this.ultHail = null;
    this.hailTally = null;
'''),

("the match carries the bolts in the air",
 '''    this.shots = [];          // live projectiles, oldest first
''',
 '''    this.shots = [];          // live projectiles, oldest first
    /* QUARRELSTORM'S HAIL (v83 §5, `m.hail[]`): the bolts in the air, per-match
       state on the match. Not in `shots` (its `maxLive` ceiling shifts the
       oldest out, and a bolt is not a projectile: it has no path, only a spot
       and a fall), and not on the window, because "drops in the air when the
       window closes still land". Each is {x, y, t, side}: the foe's spot when
       it dropped, its fall so far on the window clock, the caster's side. */
    this.hail = [];
'''),

("the cast opens the hail and resolves nothing",
 '''    if (u.kind === "echo"){
''',
 '''    if (u.kind === "hail"){
      /* QUARRELSTORM (v83). NOTHING RESOLVES HERE: the cast opens the window
         for `u.dur` seconds and `tickHail` drops every bolt and lands it. `cd`
         starts at zero, so the first bolt drops on the cast frame (the lab's).
         The nova is retired: no arrow leaves the bow here. */
      f.ultHail = { t: 0, dur: u.dur, cd: 0 };
      if (!f.hailTally)
        f.hailTally = { casts: 0, frames: 0, drops: 0, landed: 0, missed: 0,
                        dealt: 0, sunder: 0, late: 0 };
      f.hailTally.casts++;
      return;
    }
    if (u.kind === "echo"){
'''),

("the hail ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickHail(dt);                  // QUARRELSTORM (v83)
'''),

("tickHail drops and lands",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================== THE HAIL ========
     v83 §1 / §4 / §5. Two halves, on the window tickers' clock, so all of it
     freezes through a hit stop:
       THE BOLTS IN THE AIR (`m.hail`) fall first. Each adds `dt` to its fall
         and lands on the frame the fall reaches `fallT`: a live foe (the
         caster's opponent, never a shade) whose centre is within hitR + R of
         the spot takes hurt(foe, dropDmg, caster) -- ward first and NOTHING
         ELSE: no crit, no jitter, no multiplier, no knock, no stop but a
         ward's own shatter -- and then sunder, by side letter. A landing that
         kills files its own fatal hit beat; no other landing or miss files
         one. A bolt lands whether or not its window is still open and
         whether or not its caster is still standing.
       THE WINDOWS drop new bolts: the window closes on its clock or either
         death; while it is open a bolt drops at the foe's (x, y) every
         `dropCd`, the cooldown running through the whole window.
     A bolt dropped this frame first falls next frame, so it lands `fallT`
     of window clock after it dropped. No rng. */
  tickHail(dt){
    const R = CONFIG.physics.ballR;
    for (let i = 0; i < this.hail.length; ){
      const d = this.hail[i];
      d.t += dt;
      const f = this[d.side], u = f.w.ult;
      if (d.t < u.fallT){ i++; continue; }
      this.hail.splice(i, 1);
      const foe = f === this.a ? this.b : this.a, T = f.hailTally;
      if (!f.ultHail) T.late++;
      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R)){ T.missed++; continue; }
      T.landed++;
      const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
      this.hurt(foe, u.dropDmg, f);
      T.dealt += before - (foe.hp + foe.shield);
      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }
      if (wasUp && foe.hp <= 0)
        this.beat({ kind: "hit", side: d.side === "a" ? 0 : 1,
                    x: foe.x, y: foe.y, dmg: u.dropDmg, crit: false,
                    fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                    selfHpFrac: Math.max(0, f.hp) / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                    close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                    ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                    shotSpd0: 0, hail: true });
    }
    for (const f of [this.a, this.b]){
      const Z = f.ultHail;
      if (!Z) continue;
      const u = f.w.ult, T = f.hailTally;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHail = null; continue; }
      T.frames++;
      Z.cd -= dt;
      if (Z.cd <= 0){
        Z.cd = u.dropCd;
        this.hail.push({ x: foe.x, y: foe.y, t: 0, side: f === this.a ? "a" : "b" });
        T.drops++;
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the sunder",
 '''          sunder:0,          // v83: the sunder (stage 3)
''',
 f'''          sunder:{ULT["sunder"]},          // v83: the sunder (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE HOLDS THE SHIPPED WIN RATE, AND ON 151 THAT IS THE SHIPPED BLADE.
# The design's target: §5 stage 3 "the blade, wide on 151 at 15 / 15.5 / 16 to
# the shipped rate"; §3 prices the blade back to SHIP ("61.5 against a shipped
# 55.8: the blade from 16.23 to about 15.3 (the bow row 9.5-16.2)"); the v87
# handoff's redesign row reads SHIP -> new. §6.2 ("The blade target") leaves it
# to Rick and names no other target, so rule 0 takes the design's own default,
# THE SHIPPED RATE (as lightkeeper_build.py and widowmaker_build.py do).
# The shipped rate is read on 151: Ironhail as shipped (the nova, 16.23) on the
# base, relic_rate both sides, two blocks (seed0 2207 / 2317, every other relic
# a foe, 10 seeds a foe a side, 1480 fights): 62.0%.
# Both sides, two blocks, 1480 fights a point, relic_rate on sc-ironhail-sunder
# (--set dmg; 16.23 is the link itself):
#   the brief's grid   15 -> 52.6   15.5 -> 56.5   16 -> 59.4   (all under 62.0)
#   16.23 (the shipped blade) -> 61.4   16.5 -> 62.5   (the shipped relic: 62.0)
#   and, under the grid, 12 -> 32.4   13 -> 42.6   14 -> 49.5   14.5 -> 54.1
# The design's gap (61.5 against a shipped 55.8, priced on 141) is not there on
# 151 against the engine: the redesign at the shipped blade already reads the
# shipped rate. IN WINS OF 1480: shipped 917 (61.96%); 16.23 909 (61.42%, -8);
# 16.5 925 (62.50%, +8). The two measured points nearest the shipped rate are
# an EXACT TIE (8 wins either side, each well inside one standard error, ~18
# wins / 1.26 points). The tie goes to 16.23: the blade does not move, it is
# the top of the bow row the design names (§3 "the bow row 9.5-16.2", whose top
# IS Ironhail's own blade; 16.5 would lift it above the row), and it is the
# nearer of the two to the brief's own grid (15 / 15.5 / 16). SO THE BLADE DOES
# NOT MOVE, and stage 3's link is the final. The design names no knob to move
# before the blade, and none moved.
# RICK'S OTHER CHOICE UNDER §6.2, 50% (the batch's standard for a new relic, not
# this design's default): blade 14, 49.5% both sides, the measured point nearest
# the 50% line (which crosses in 14-15 within noise: the 12 and 15 points split
# 5.3 and 6.6 points between blocks). `--stage 5 --alt50` writes it
# (sc-ironhail-b14), measured and gated as this build's first draft (v108 §4, §6).
BLADE = SHIPPED_DMG
ALT50_BLADE = "14"


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v83 §4, brief stage 4), picked on measurements
# under Rick's "you pick i overrule" by `ironhail_voice_lab.py` and the
# picture lab (v108 §5). Presentation only: engine_ab over all 38 relics,
# Ironhail included, is the proof. The rows are byte-exact to the labs' own
# files (voice 3, picture 12; no two share an anchor, so none is merged); the
# picture rows alone reproduce the picture lab's stamp (f03b657a1d99d86c) on
# sc-ironhail-sunder. Voice first, then picture; the other order writes the
# same bytes.
#   THE VOICE: the cast (fireUlt's own `ult`/ironhail call, which fell
#   through to rune-crack: the bellows huff), a landing (in tickHail, after
#   its hurt and its sunder, pitched by the foe's count) and a miss (in
#   tickHail, before the miss line, on that line's own test). The close has
#   none (v83 §4). Plain SFX.play; nothing is read back.
#   THE PICTURE: `tickQuarrel` in tickPresentation reads `ultHail && !over`,
#   `hailTally` rising and the bolts in `m.hail`, and writes only its own
#   `quarrel*` fields, a tag's count, `tags` (statusTag) and `taught`. The
#   limbs glow forge-orange for the window and cool 0.5s after it; each bolt
#   is a rune on its spot with a ring closing on it and a streak falling
#   from the top of the live hall; a landing splashes, dusts, throws six
#   sparks and four iron-spark motes and ticks the sunder tag; a miss
#   splashes in dust. The nova's art (the release flash and floor dust on
#   the ultFx slot, the charge rune's eight heads, the banner's fan) is
#   retired. No beat, no stop, no fx.js edit: the design's field is drawn
#   (reading 20), and the nova's field spec leaves BOTH copies by the
#   orchestrator's sync_fx_remove, not here (fx.js is shared).
#   NAMES: the labs'. `drawQuarrel` is a prefix of `drawQuarrelGlow`, so
#   every stage-6 name check below is on identifier boundaries.
S6 = [

("Sfx: Ironhail's cast, landing and miss arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "ironhail"){                   // the bellows huff
          /* IRONHAIL'S CAST, THE BELLOWS -- v83 §4: "cast -- a forge-bellows
             huff, 0.4s". WHOOMPH, of 9, picked on the numbers by
             `ironhail_voice_lab.py` under Rick's "you pick i overrule" (v108).
             Ironhail had no arm and fell through to rune-crack, which 11 other
             relics on its stage-5 link still used, so this ADDS arms before
             that fallback and leaves it alone.

             The bellows' chamber pushed: a swell of lowpassed air (its cutoff
             150 -> 300 Hz) and, on its top, the huff (400 -> 150 Hz). The
             swell has the longest attack a `_sweep` allows and the huff peaks
             on its top and outlasts it -- the one way two sweeps make one
             hump, since one `_sweep` cannot outlast the noise buffer
             (CLAUDE.md 4.5): it swells to its top (the last 10 -> 90% in 67
             ms), never dips on the way up and never grows again after its top;
             its power centres at 203-272 Hz on every noise draw (a bellows,
             not a quench's hiss), and no peak stands more than 2.5 dB over its
             neighbours (air, not a note). Audible 350 ms; its loudest 50 ms
             -2.8 dB re Ironhail's blow. Register at most 0.77 against
             rune-crack, the dwarven and bow casts, the tornado's woosh, the
             bowstring, the blow and the death voice. */
          const g = 0.6967;
          this._sweep(t, { f0: 150, f1: 300, q: 0.7, gain: g, dur: 0.58, atk: 0.34, type:"lowpass" });
          this._sweep(t + 0.32, { f0: 400, f1: 150, q: 0.7, gain: g, dur: 0.58, atk: 0.02, type:"lowpass" });
        } else if (w === "ironhail-land"){              // a bolt lands
          /* A BOLT LANDS -- "a landing -- a short iron thud (<=0.15s), pitched
             by sunder count" (v83 §4). RINGING, of 9
             (`ironhail_voice_lab.py`). `tickHail` plays it once per landed
             bolt, after its hurt and its sunder, with n = the foe's sunder
             count (the tag's number, 1-6).

             A sine body under a falling punch (its octave down to it, 30 ms),
             an iron bar struck -- its first mode (a triangle at 2.76x) as loud
             as the body and ringing 0.8 of its decay, its second (a sine at
             5.40x) at 0.35 -- and a 12 ms 2.5 kHz contact click (the bolt
             meeting the foe). The note steps up with the count, 110 / 117 /
             123 / 131 / 139 / 147 Hz at 1-6 (measured within 0 cents). Rise
             under 1 ms; gone by 125 ms at every count and draw; 0.72 of its
             power under 400 Hz at the worst; its iron partial 144 cents off
             every harmonic; its loudest 50 ms -2.6 to -2.3 dB re the blow. On
             a phone (nothing under 200 Hz) the count is its iron, 304 / 322 /
             341 / 361 / 383 / 405 Hz, +13.3 dB or more over the score's p90.
             Register at most 0.74 against the blow, the clank, the bowstring,
             the death voice, rune-crack and the cast. */
          const n = clamp(Math.round(p.n || 1), 1, 6), f = 110 * Math.pow(2, (n - 1) / 12), g = 0.1271, D = 0.213;
          this._tone(t, { freq: f * 2, to: f, gain: g * 0.6, dur: 0.03, type:"sine" });
          this._tone(t, { freq: f, gain: g, dur: D, type:"sine" }).frequency.value = f;
          this._tone(t, { freq: f * 2.76, gain: g, dur: D * 0.8, type:"triangle" }).frequency.value = f * 2.76;
          this._tone(t, { freq: f * 5.4, gain: g * 0.35, dur: D * 0.35, type:"sine" }).frequency.value = f * 5.4;
          this._burst(t, { freq: 2500, q: 1.2, gain: g * 0.4, dur: 0.012, type:"bandpass" });
        } else if (w === "ironhail-miss"){              // a bolt falls short
          /* A BOLT MISSES -- "a miss -- a quieter thud" (v83 §4). SAME, of 4
             (`ironhail_voice_lab.py`): the landing's own thud, at count 0's
             note (103.8 Hz, one step under a first landing -- a miss sunders
             nothing). -5.9 dB under the quietest landing on its loudest draw,
             gone by 130 ms, 0.96 of its power under 400 Hz, +10.5 dB over the
             score in its loudest third-octave over 200 Hz (where a phone hears
             it); register at most 0.76 against the blow, the clank, the
             bowstring, the death voice, rune-crack and the cast. `tickHail`
             plays it once per missed bolt. The close plays nothing (v83 §4). */
          const f = 103.83, g = 0.05227, D = 0.213;
          this._tone(t, { freq: f * 2, to: f, gain: g * 0.6, dur: 0.03, type:"sine" });
          this._tone(t, { freq: f, gain: g, dur: D, type:"sine" }).frequency.value = f;
          this._tone(t, { freq: f * 2.76, gain: g, dur: D * 0.8, type:"triangle" }).frequency.value = f * 2.76;
          this._tone(t, { freq: f * 5.4, gain: g * 0.35, dur: D * 0.35, type:"sine" }).frequency.value = f * 5.4;
          this._burst(t, { freq: 2500, q: 1.2, gain: g * 0.4, dur: 0.012, type:"bandpass" });
        } else {                                        // rune-crack'''),

('tickHail: the landing voice, once per landed bolt, after its hurt and its sunder',
 '''      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }''',
 '''      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }
      /* QUARRELSTORM'S LANDING (v83 §4: "a landing -- a short iron thud
         (<=0.15s), pitched by sunder count"): one thud per landed bolt,
         after its hurt and its sunder, pitched by the count the foe now
         carries -- the number its tag shows, 1-6. A killing landing thuds
         too, under the death voice. Presentation only: SFX.play draws
         nothing, is a no-op headless, and nothing here is read back
         (ironhail_voice_lab: fights identical). */
      SFX.play("ult", { w: "ironhail-land", n: foe.stacks("sunder") });'''),

('tickHail: the miss voice, once per missed bolt, before the miss line',
 '''      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R)){ T.missed++; continue; }''',
 '''      /* QUARRELSTORM'S MISS (v83 §4: "a miss -- a quieter thud"): the next
         line's own test, read here first -- a read of foe.alive and two
         positions, and the anchor guards it (if that line changes, this row
         stops applying) -- so a bolt the sim counts as missed thuds once,
         on its landing frame, a bolt falling on the step its foe died
         included. Presentation only; nothing here is read back. */
      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R))
        SFX.play("ult", { w: "ironhail-miss" });
      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R)){ T.missed++; continue; }'''),

('quarrelstorm picture: fighter fields',
 '''    this.ultHail = null;
    this.hailTally = null;
''',
 '''    this.ultHail = null;
    this.hailTally = null;
    /* QUARRELSTORM'S PICTURE (v83 section 4), and none of it is the sim's:
       the limbs cool after `ultHail` is gone, and a landing's puff outlives
       its bolt (`tickHail` splices it), so the picture keeps its own state.
       On the FIGHTER and never on `m.ultFx` (one slot, and the opponent's
       cast takes it: open item 25). Driven in `tickPresentation`
       (`tickQuarrel`); nothing in the simulation reads any of it.
         quarrelFade -- 1 while the hail falls; eased to 0 over the cool
         quarrelAge  -- the presentation clock since the cast (the ignition)
         quarrelOut  -- the presentation clock since the close (the cool)
         quarrelEnd  -- the presentation clock since the match ended: a bolt
                        the kill leaves in the air fades on it
         quarrelSeen -- `hailTally`'s landed and missed, as last seen
         quarrelAir  -- this side's bolts in the air, as last seen: the
                        MATCH's own records, read and never written
         quarrelFx   -- a landing's or a miss's puff (records) */
    this.quarrelFade = 0;
    this.quarrelAge = 0;
    this.quarrelOut = 0;
    this.quarrelEnd = 0;
    this.quarrelSeen = [0, 0];
    this.quarrelAir = [];
    this.quarrelFx = [];
'''),

('quarrelstorm picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickQuarrel(dt);               // QUARRELSTORM'S PICTURE (v83 section 4)
'''),

('quarrelstorm picture: tickQuarrel',
 '''  tickWinnow(dt){
''',
 '''  /* --------------------------------------------- QUARRELSTORM'S PICTURE ---
     v83 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step): 0.3 is the
     limbs' 0.15s ignition, 1.0 their 0.5s cool, 0.8 a landing's 0.4s
     puff, 0.6 a miss's 0.3s, 2.0 the motes' 1s. A BOLT THAT RESOLVES IS
     FOUND BY WATCHING `hailTally` RISE, so `tickHail` makes no call for the
     picture: the bolt that left `m.hail` is the one this side had in the air
     last step, and whether it landed is the tally's word, not a guess (one
     bolt of a side is in the air at a time, dropCd > fallT on one clock;
     two at once are read off `tickHail`'s own test). THE LIMBS ARE READ OFF
     `ultHail && !over`: `tickHail` never runs again once `over` is set, so
     they cool at the verdict, and a bolt the kill leaves in the air fades
     rather than hanging through the panel. Writes presentation fields,
     `tags` and `taught` only, and draws no rng (shellHash). */
  tickQuarrel(dt){
    for (const f of [this.a, this.b]){
      const T = f.hailTally;
      if (!T && !(f.quarrelFade > 0)) continue;                // <- zero burden
      const side = f === this.a ? "a" : "b", foe = f === this.a ? this.b : this.a;
      const Rb = CONFIG.physics.ballR;
      for (let i = f.quarrelFx.length - 1; i >= 0; i--){
        const q = f.quarrelFx[i];
        q.t += dt;
        if (q.t >= q.life) f.quarrelFx.splice(i, 1);
      }
      const Z = (this.over || !f.alive) ? null : f.ultHail;
      if (Z){
        if (!(f.quarrelFade > 0) || f.quarrelOut > 0){ f.quarrelAge = 0; f.quarrelOut = 0; }   // a cast
        f.quarrelFade = 1;
        f.quarrelAge += dt;
      } else if (f.quarrelFade > 0){
        f.quarrelOut += dt;
        f.quarrelFade = Math.max(0, 1 - f.quarrelOut / 1.0);
      }
      if (this.over) f.quarrelEnd += dt;
      if (!T) continue;
      const nl = T.landed - f.quarrelSeen[0], nm = T.missed - f.quarrelSeen[1];
      if (nl > 0 || nm > 0){
        const u = f.w.ult, gone = f.quarrelAir.filter(d => this.hail.indexOf(d) < 0);
        for (let j = 0; j < gone.length; j++){
          const d = gone[j];
          const hit = gone.length === 1 ? nl > 0
                    : foe.alive && Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + Rb;
          const n = f.quarrelSeen[0] + f.quarrelSeen[1] + j + 1;
          f.quarrelFx.push({ x: d.x, y: d.y, r: u.hitR, t: 0, hit, n, s: side === "a" ? 0 : 1,
                             puff: hit ? 0.8 : 0.6, life: hit ? Math.max(0.8, 2.0) : 0.6 });
          /* THE SUNDER TAG ON THE FOE TICKS UP, with its count, on the foe's
             rim toward the spot. ONE SUNDER TAG ON THE FOE AT A TIME
             (Tendril's and Temper's rule): a tag already up there -- the
             bow's own, or the last bolt's -- takes the new count in place
             instead of a second printing over it. A killing landing tags
             nothing: the shatter owns that frame. */
          if (hit && foe.alive && foe.hp > 0){
            const k = foe.stacks("sunder"), a = Math.atan2(d.y - foe.y, d.x - foe.x);
            const g = this.tags.find(g2 => g2.key === "sunder" && !g2.first && g2.life > 0.3
                                           && Math.hypot(g2.x - foe.x, g2.y - foe.y) < Rb * 3);
            if (g) g.val = k;
            else {
              const first = !this.taught.sunder && !!STATUS.sunder.tip;
              if (first) this.taught.sunder = true;
              this.statusTag(foe.x + Math.cos(a) * Rb, foe.y + Math.sin(a) * Rb, "sunder", first, k);
            }
          }
        }
        if (f.quarrelFx.length > 12) f.quarrelFx.splice(0, f.quarrelFx.length - 12);
      }
      f.quarrelSeen[0] = T.landed; f.quarrelSeen[1] = T.missed;
      f.quarrelAir.length = 0;
      for (const d of this.hail) if (d.side === side) f.quarrelAir.push(d);
    }
  }

  tickWinnow(dt){
'''),

('quarrelstorm picture: the ground call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* QUARRELSTORM'S GROUND (v83 section 4): each bolt's rune on the spot it
       will land on, the ring closing on it as it falls, a landing's splash
       and dust. The WORLD pass and under both balls -- the rune is on the
       floor (the sigils' rule: a figure drawn over the ball standing in it
       says the opposite), and nothing of it reaches the bloom. */
    if (__world) this.drawQuarrel(m);
'''),

('quarrelstorm picture: the emissive call (over both fighters)',
 '''    this.drawSunTop(m);
''',
 '''    this.drawSunTop(m);
    /* QUARRELSTORM'S BOLTS, SPARKS AND MOTES, OVER BOTH FIGHTERS: a bolt falls
       in front of everything in the hall and a landing throws its sparks up
       off whatever it hit. Light, so this pass -- the bow's own shots are
       drawn here too, and a falling bolt is one of them. */
    this.drawQuarrelGlow(m);
'''),

("quarrelstorm picture: the limbs' hook in drawWeapon",
 '''        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }
''',
 '''        if (fn) fn(c, reach + 6, f.w.artW, pal, f.drawK);
      }
      /* QUARRELSTORM (v83 section 4): the bow's limbs glow forge-orange for
         the window and cool after it, drawn over the shape in the frame the
         shape was drawn in. `quarrelFade` is 0 on every other relic, so this
         is one comparison on a field nothing else writes. */
      if (f.quarrelFade > 0 && f.w.shape === "bow")
        this._quarrelLimbs(c, reach + 6, f.w.artW, f);
'''),

('quarrelstorm picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------------ QUARRELSTORM'S PICTURE ---
     v83 section 4, drawn off the MATCH's bolts (`m.hail`, each {x, y, t,
     side}: the sim's own records, read and never written) and the fighter's
     `quarrel*` fields -- never `m.ultFx`, one slot the opponent's cast takes
     (open item 25). A bolt in the air is drawn from its own fall, `t /
     fallT` on the window's clock, so it hangs where the sim holds it through
     a hit stop; nothing here keeps state per bolt and nothing draws from the
     rng (shellHash on the landing's count). One method a component, so each
     can be measured alone.
       drawQuarrel      WORLD, under both balls: a landing's splash ring
                        (out to the bolt's reach) and dust; each bolt's rune
                        and the ring closing on it from that reach.
       drawQuarrelGlow  EMISSIVE, over both fighters: each bolt falling from
                        the top of the live hall (the bow's own shot, streak
                        and dart, pointing down); a landing's six sparks and
                        its iron-spark motes (the design's field, drawn). */
  drawQuarrel(m){
    const FA = m.a.quarrelFx, FB = m.b.quarrelFx;
    if (!m.hail.length && !FA.length && !FB.length) return;
    const c = this.ctx, D = AFFINITIES.dwarven;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const q of FA) this._quarrelSplash(c, q, D);
    for (const q of FB) this._quarrelSplash(c, q, D);
    for (const q of FA) this._quarrelDust(c, q);
    for (const q of FB) this._quarrelDust(c, q);
    for (const d of m.hail){
      const f = m[d.side], u = f.w.ult;
      const al = m.over ? 1 - clamp(f.quarrelEnd / 0.5, 0, 1) : 1;
      if (!(al > 0)) continue;
      const p = clamp(d.t / u.fallT, 0, 1);
      this._quarrelRing(c, d, p, u.hitR, al, D);
      this._quarrelRune(c, d, al, D);
    }
    c.restore();
  }
  /* THE SPLASH: a ring out to the bolt's reach, `hitR` -- a foe whose shell
     touches it was struck, which is `tickHail`'s own test drawn. Struck in
     the school's glow; a miss in dust. */
  _quarrelSplash(c, q, D){
    const k = q.t / q.puff;
    if (k >= 1) return;
    const e = 1 - Math.pow(1 - clamp(k / 0.4, 0, 1), 3);
    c.globalAlpha = (1 - k) * (q.hit ? 0.75 : 0.45);
    c.strokeStyle = q.hit ? D.glow : "#8A6A3A";
    c.lineWidth = (q.hit ? 3.4 : 2.4) * (1 - 0.6 * k);
    c.beginPath(); c.arc(q.x, q.y, 14 + (q.r - 14) * e, 0, TAU); c.stroke();
  }
  /* THE DUST: five soft blobs kicked out and up off the spot. */
  _quarrelDust(c, q){
    const k = q.t / q.puff;
    if (k >= 1) return;
    const e = 1 - Math.pow(1 - clamp(k / 0.4, 0, 1), 3);
    c.fillStyle = "#6E5434";
    c.globalAlpha = (1 - k) * (1 - k) * (q.hit ? 0.5 : 0.32);
    for (let j = 0; j < 5; j++){
      const h = shellHash(9931 + q.s, q.n * 8 + j);
      const a = j * TAU / 5 + h * 0.9, dd = (8 + 30 * e) * (0.7 + 0.5 * h);
      c.beginPath();
      c.arc(q.x + Math.cos(a) * dd, q.y + Math.sin(a) * dd * 0.7 - 14 * e,
            4 + 7 * e * (0.6 + 0.4 * h), 0, TAU);
      c.fill();
    }
  }
  /* THE RING CLOSING ON THE RUNE, from the bolt's reach in to the rune as
     the bolt falls: where it will land, and how soon. */
  _quarrelRing(c, d, p, hitR, al, D){
    c.globalAlpha = al * (0.35 + 0.45 * p);
    c.strokeStyle = D.glow; c.lineWidth = 1.6 + 1.6 * p;
    c.beginPath(); c.arc(d.x, d.y, 14 + (hitR - 14) * (1 - p), 0, TAU); c.stroke();
  }
  /* THE RUNE: dwarven dark, r 14, ringed and crossed in the school's core. */
  _quarrelRune(c, d, al, D){
    c.globalAlpha = al * 0.92;
    c.fillStyle = D.dark;
    c.beginPath(); c.arc(d.x, d.y, 14, 0, TAU); c.fill();
    c.strokeStyle = D.core; c.lineWidth = 2.4;
    c.beginPath(); c.arc(d.x, d.y, 14, 0, TAU); c.stroke();
    c.lineWidth = 2;
    c.beginPath();
    for (let i = 0; i < 4; i++){
      const a = i * TAU / 4 + TAU / 8;
      c.moveTo(d.x + Math.cos(a) * 14 * 0.3, d.y + Math.sin(a) * 14 * 0.3);
      c.lineTo(d.x + Math.cos(a) * 14 * 0.78, d.y + Math.sin(a) * 14 * 0.78);
    }
    c.stroke();
  }
  drawQuarrelGlow(m){
    const FA = m.a.quarrelFx, FB = m.b.quarrelFx;
    if (!m.hail.length && !FA.length && !FB.length) return;
    const c = this.ctx, D = AFFINITIES.dwarven;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round"; c.lineJoin = "round";
    for (const d of m.hail){
      const f = m[d.side], u = f.w.ult;
      const al = m.over ? 1 - clamp(f.quarrelEnd / 0.5, 0, 1) : 1;
      if (!(al > 0)) continue;
      const p = clamp(d.t / u.fallT, 0, 1);
      /* FROM THE TOP OF THE LIVE HALL (the seals walk `inset` in) to the
         spot, gathering speed: a third of the way in the first half. */
      const top = Math.min((m.inset || 0) + 12, d.y);
      const hy = top + (d.y - top) * (p * p * 0.35 + p * 0.65);
      const r = (f.w.shot && f.w.shot.r) || 24;
      this._quarrelStreak(c, d.x, top, hy, r, al, D);
      this._quarrelDart(c, d.x, hy, r, al);
    }
    for (const q of FA){ this._quarrelSparks(c, q, D); this._quarrelMotes(c, q, D); }
    for (const q of FB){ this._quarrelSparks(c, q, D); this._quarrelMotes(c, q, D); }
    c.restore();
  }
  /* THE STREAK: the bow's own shot's gradient (dark to core to glow), stood
     on end, never above the ceiling it fell from. */
  _quarrelStreak(c, x, top, hy, r, al, D){
    const tl = Math.min(110, hy - top + 8);
    if (!(tl > 1)) return;
    const g = c.createLinearGradient(x, hy - tl, x, hy);
    g.addColorStop(0, D.dark + "00");
    g.addColorStop(0.55, D.core + "88");
    g.addColorStop(1, D.glow);
    c.globalAlpha = al;
    c.strokeStyle = g; c.lineWidth = r * 0.30;
    c.beginPath(); c.moveTo(x, hy - tl); c.lineTo(x, hy); c.stroke();
  }
  /* THE DART: the bow's own shot's head, pointing down. */
  _quarrelDart(c, x, hy, r, al){
    c.globalAlpha = al;
    c.fillStyle = "#FFF4D0";
    c.beginPath();
    c.moveTo(x, hy + r * 1.05);
    c.lineTo(x + r * 0.42, hy - r * 0.55);
    c.lineTo(x, hy - r * 0.20);
    c.lineTo(x - r * 0.42, hy - r * 0.55);
    c.closePath(); c.fill();
  }
  /* SIX SPARKS off a landing, fanned up out of the spot and falling back,
     each a short streak along its own path. Turned by the landing's count. */
  _quarrelSparks(c, q, D){
    if (!q.hit) return;
    const k = q.t / q.puff;
    if (k >= 1) return;
    c.lineWidth = 2.2 * (1 - 0.5 * k);
    for (let j = 0; j < 6; j++){
      const h1 = shellHash(9941 + q.s, q.n * 8 + j), h2 = shellHash(9947 + q.s, q.n * 8 + j);
      const a = -Math.PI / 2 + ((j + 0.5) / 6 - 0.5) * 2.6 + (h1 - 0.5) * 0.35;
      const v = 150 + 110 * h2, t = q.t;
      const vx = Math.cos(a) * v, vy = Math.sin(a) * v + 520 * t;
      const x = q.x + Math.cos(a) * v * t, y = q.y + Math.sin(a) * v * t + 260 * t * t;
      c.globalAlpha = 1 - k;
      c.strokeStyle = j % 2 ? D.glow : "#FFD9A0";
      c.beginPath(); c.moveTo(x, y); c.lineTo(x - vx * 0.045, y - vy * 0.045); c.stroke();
    }
  }
  /* IRON-SPARK MOTES off a landing (the design's field, drawn: a particle
     field fires once, at the cast, on the one ultFx slot, and these are on
     every landing for the whole window): 4 embers rising off the spot. */
  _quarrelMotes(c, q, D){
    if (!q.hit) return;
    const k = q.t / 2.0;
    if (k >= 1) return;
    c.fillStyle = D.glow;
    for (let j = 0; j < 4; j++){
      const h1 = shellHash(9953 + q.s, q.n * 8 + j), h2 = shellHash(9959 + q.s, q.n * 8 + j);
      const t = q.t;
      c.globalAlpha = Math.sin(Math.PI * k) * 0.85;
      c.beginPath();
      c.arc(q.x + (h1 - 0.5) * 44 + Math.sin(t * 3 + j * 1.7) * 5,
            q.y - 6 - t * (20 + 16 * h2), 1.3 + 1.1 * h2, 0, TAU);
      c.fill();
    }
  }
  /* THE LIMBS IN THE FORGE: SHAPES.bow's own limb path, verbatim, stroked
     over the shape at a forge's dull red, a forge-orange edge and, while it
     is hot, a pale heart; the rivets redrawn on top so the plate still
     reads. Up over the ignition, down over the cool. */
  _quarrelLimbs(c, L, W, f){
    const h = clamp(f.quarrelAge / 0.3, 0, 1) * f.quarrelFade;
    if (!(h > 0.004)) return;
    const lh = W * 0.95, rx = L * 0.13, a0 = c.globalAlpha;
    const limb = (wd, col) => {
      c.strokeStyle = col; c.lineWidth = Math.max(1, wd);
      c.beginPath();
      c.moveTo(rx - L*0.06, -lh);
      c.quadraticCurveTo(rx + L*0.34, -lh*0.44, rx + L*0.17, 0);
      c.quadraticCurveTo(rx + L*0.34,  lh*0.44, rx - L*0.06,  lh);
      c.stroke();
    };
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    c.globalAlpha = a0 * h;
    limb(W * 0.13, "#8A2C0A");
    limb(W * 0.065, "#F08A30");
    c.globalAlpha = a0 * h * h;
    limb(W * 0.024, "#FFE2A8");
    c.globalAlpha = a0;
    for (const sg of [-1, 1]){
      for (let i = 0; i < 3; i++){
        const u = 0.22 + i * 0.29, it = 1 - u;
        const qx = it*it*(rx - L*0.06) + 2*it*u*(rx + L*0.34) + u*u*(rx + L*0.17);
        const qy = it*it*(sg * lh) + 2*it*u*(sg * lh * 0.44);
        c.fillStyle = SHAPES._ink(f.aff.dark, 9.71);
        c.beginPath(); c.arc(qx, qy, W*0.075, 0, TAU); c.fill();
        c.fillStyle = f.aff.steel;
        c.beginPath(); c.arc(qx, qy, W*0.042, 0, TAU); c.fill();
      }
    }
    c.restore();
  }

  drawMotes(m){
'''),

("quarrelstorm picture: the nova's floor dust retired",
 '''    /* ---- Quarrelstorm: the dust the release blows off the floor ------------ */
    else if (u.w === "ironhail"){
      const ex = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - 0.35) / 0.8, 0, 1);
      const R = 210 * (1 - Math.pow(1 - ex, 2.6));
      c.globalAlpha = 0.5 * fade * (1 - ex * 0.5);
      c.strokeStyle = "#8A6A3A"; c.lineWidth = 9 * (1 - ex * 0.6);
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.stroke();
    }
''',
 '''    /* ---- Quarrelstorm's floor dust was the NOVA's; retired with it (v83,
       v108 stage 6). The hail's picture is `drawQuarrel`, off the fighter
       and the match's bolts, where the one ultFx slot cannot erase it. */
'''),

("quarrelstorm picture: the nova's release flash retired",
 '''    /* ---- Quarrelstorm: the RELEASE. Not arrows — drawShots draws those ----- */
    else if (u.w === "ironhail"){
      const flash = 1 - clamp(u.t / 0.22, 0, 1);
      const fade  = 1 - clamp((u.t - 0.2) / 0.7, 0, 1);
      const N = 14;                                 // == u.shots
      if (flash > 0){
        c.save();
        c.globalCompositeOperation = "lighter";
        for (let i = 0; i < N; i++){
          const a = (i / N) * TAU;
          const l = 26 + 66 * flash;
          c.globalAlpha = flash * 0.95;
          c.strokeStyle = "#E8A34E"; c.lineWidth = 3.4 * flash + 1;
          c.shadowColor = "#E8A34E"; c.shadowBlur = 14;
          c.beginPath();
          c.moveTo(u.x + Math.cos(a) * 22, u.y + Math.sin(a) * 22);
          c.lineTo(u.x + Math.cos(a) * (22 + l), u.y + Math.sin(a) * (22 + l));
          c.stroke();
        }
        c.shadowBlur = 0;
        c.restore();
      }
      /* the mount kicks: a hard ring thrown back off the release */
      const ex = clamp(u.t / 0.26, 0, 1);
      c.globalAlpha = fade * (1 - ex) * 0.9;
      c.strokeStyle = "#FFD9A0"; c.lineWidth = 4 * (1 - ex) + 1;
      c.beginPath(); c.arc(u.x, u.y, 20 + 120 * ex, 0, TAU); c.stroke();
    }
''',
 '''    /* ---- Quarrelstorm's release was the NOVA's (fourteen arrow streaks and
       the mount's kick ring); retired with it (v83, v108 stage 6). The cast
       is the limbs igniting and the first bolt's rune (`drawQuarrel`). */
'''),

('quarrelstorm picture: the charge rune',
 '''  /* QUARRELSTORM -- eight heads going out. The nova of arrows, counted. */
  ironhail(c, t, cf, P){
    for (let i = 0; i < 8; i++){
      const a = i * TAU / 8 + t * 0.3, d = 0.3 + cf * 0.56;
      c.save(); c.translate(Math.cos(a) * d, Math.sin(a) * d); c.rotate(a + Math.PI / 2);
      SG.poly(c, [[0, -0.24], [0.15, 0.1], [0, 0.02], [-0.15, 0.1]], P.core, 0.5 + cf * 0.5);
      c.restore();
    }
    SG.ring(c, 0, 0, 0.2, P.glow, 0.07, 0.6);
  },
''',
 '''  /* QUARRELSTORM -- iron falling on a mark. The nova's eight heads went out
     with the nova (v83): three bolts drop onto a crossed rune, lower as the
     charge fills, and are on it at the moment it goes off. */
  ironhail(c, t, cf, P){
    SG.ring(c, 0, 0.52, 0.24, P.glow, 0.07, 0.4 + cf * 0.55);
    SG.path(c, [[-0.1, 0.42], [0.1, 0.62]], P.glow, 0.05, 0.3 + cf * 0.5);
    SG.path(c, [[0.1, 0.42], [-0.1, 0.62]], P.glow, 0.05, 0.3 + cf * 0.5);
    for (let i = 0; i < 3; i++){
      const x = (i - 1) * 0.44, lag = i === 1 ? 0 : 0.14;
      const y = -0.78 + Math.max(0, cf - lag) / (1 - lag) * 0.95 - (i === 1 ? 0 : 0.1);
      SG.path(c, [[x, y - 0.42], [x, y]], P.core, 0.075, 0.45 + cf * 0.5);
      SG.poly(c, [[x, y + 0.2], [x + 0.13, y - 0.02], [x - 0.13, y - 0.02]], P.core, 0.55 + cf * 0.45);
    }
  },
'''),

("quarrelstorm picture: the banner's spread",
 '''                     ironhail: 46, farwarden: 118 }[b.w];
''',
 '''                     farwarden: 118 }[b.w];   // Quarrelstorm's letters fall: no spread (v108)
'''),

("quarrelstorm picture: the banner's letters fall",
 '''    else if (b.w === "ironhail"){
      /* Each letter on its own bearing, converging. `i * TAU / N` reads as
         a circle even when the letters land in a line, because the eye
         reconstructs the fan from the streaks. */
      fn = (i, N) => {
        const s = 1 - ease(clamp((age - i * 0.008) / 0.17, 0, 1));
        const a = (i / N) * TAU + 0.55;
        return { dx: Math.cos(a) * s * 300 * k,
                 dy: Math.sin(a) * s * 210 * k,
                 rot: s * (H(89, i) - 0.5) * 1.5 };
      };
      if (age < 0.30){
        const s = 1 - ease(age / 0.30);
        c.save();
        c.globalCompositeOperation = "lighter";
        c.shadowBlur = 0;
        c.globalAlpha = s * 0.75;
        c.strokeStyle = glow; c.lineCap = "round";
        const N2 = b.text.length;
        for (let i = 0; i < N2; i++){
          const a = (i / N2) * TAU + 0.55;
          const lx = cx + Math.cos(a) * s * 300 * k;
          const ly = y  + Math.sin(a) * s * 210 * k;
          c.lineWidth = (1.5 + 3.5 * s) * k;
          c.beginPath();
          c.moveTo(lx + Math.cos(a) * 70 * k, ly + Math.sin(a) * 50 * k);
          c.lineTo(lx, ly);
          c.stroke();
        }
        c.restore();
      }
    }
''',
 '''    else if (b.w === "ironhail"){
      /* THE LETTERS FALL, each on its own bolt: Quarrelstorm is iron hail
         now (v83), so the name drops out of the ceiling letter by letter, a
         streak over each, and lands on the line. The fan of fourteen arrows
         the letters used to converge from went out with the nova. */
      const fall = (i) => 1 - ease(clamp((age - i * 0.022) / 0.16, 0, 1));
      fn = (i) => { const s = fall(i); return { dy: -s * 300 * k, a: 1 - s * 0.35 }; };
      if (age < 0.5){
        c.save();
        c.globalCompositeOperation = "lighter";
        c.shadowBlur = 0;
        c.strokeStyle = glow; c.lineCap = "round";
        c.font = `700 ${size}px 'Atkinson Hyperlegible Next',sans-serif`;
        const ws = [];
        let tot = -track;
        for (const ch of b.text){ const w = c.measureText(ch).width; ws.push(w); tot += w + track; }
        let lx = cx - tot / 2;
        for (let i = 0; i < b.text.length; i++){
          const s = fall(i), mx = lx + ws[i] / 2;
          lx += ws[i] + track;
          if (s < 0.01) continue;
          const ly = y - size * 0.78 - s * 300 * k;
          c.globalAlpha = s * 0.7;
          c.lineWidth = (1.5 + 2.5 * s) * k;
          c.beginPath(); c.moveTo(mx, ly - (40 + 90 * s) * k); c.lineTo(mx, ly); c.stroke();
        }
        c.restore();
      }
    }
'''),

]

# The names stage 6 adds, free on the base -- checked on identifier boundaries
# (`drawQuarrel` is a prefix of `drawQuarrelGlow`; the base's own renderer
# reads `u.w === "ironhail"` and `b.w === "ironhail"`, so the cast arm is found
# by its whole `} else if (w === "ironhail"){` line, never by the comparison).
S6_NAMES = ("tickQuarrel", "drawQuarrel", "drawQuarrelGlow", "_quarrelLimbs", "_quarrelSplash",
            "quarrelFade", "quarrelFx", "quarrelSeen", "quarrelAir", '"ironhail-land"',
            '"ironhail-miss"')
S6_CAST_ARM = '} else if (w === "ironhail"){'
# What stage 6's ADDED code may write: its own quarrel* fields (and their
# arrays' length), the canvas, a tag's count, a puff record's own clock,
# `taught`, and an oscillator's pitch. Arrays it may push to or splice: its
# own quarrel* arrays and the banner's local width list.
S6_WRITE_OK = (lambda obj, prop: prop.startswith("quarrel") or obj.startswith("quarrel")
               or obj == "c" or (obj, prop) in {("g", "val"), ("q", "t"), ("taught", "sunder"),
                                                ("frequency", "value")})
S6_ARRAY_OK = (lambda obj: obj.startswith("quarrel") or obj == "ws")


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (the nova's field spec is the orchestrator's to take out of
    both copies)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


STAGE_OUT = {"1": "sc-ironhail-stub", "2": "sc-ironhail-hail", "3": "sc-ironhail-sunder",
             "5 --alt50": "sc-ironhail-b14", "6": "sc-ironhail-sunder-fx"}


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


def s5_edits(blade: str) -> list:
    return [
        ("the blade: Rick's other choice, 50%",
         f'''  {{ id:"ironhail", name:"Ironhail", aff:"dwarven", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:{SHIPPED_DMG},''',
         f'''  {{ id:"ironhail", name:"Ironhail", aff:"dwarven", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:{blade},'''),
    ]


# NO MODULE-LEVEL STAGE-5 TABLE: the final link (stage 3's) carries no blade
# edit, and chain_audit reads every module-level insert table as an insert the
# final must hold. The 50% alternative's table is built in main() when asked.


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--alt50", action="store_true",
                    help="stage 5 only: write Rick's other choice under v83 §6.2, "
                         f"50%% (blade {ALT50_BLADE}); NOT the carry")
    A = ap.parse_args()
    if A.alt50 and A.stage != "5":
        raise SystemExit("--alt50 is stage 5's")
    if A.stage == "5" and not A.alt50:
        if BLADE == SHIPPED_DMG:
            raise SystemExit(
                f"stage 5: THE BLADE HOLDS at the shipped {SHIPPED_DMG} -- the design's "
                "target is the shipped rate, and on 151 the redesign reads it there "
                "(v108 §4). Stage 3's link is the final; there is nothing to write. "
                f"(`--stage 5 --alt50` writes Rick's other choice, 50%: blade {ALT50_BLADE}.)")
        raise SystemExit("stage 5: BLADE moved off the shipped blade with no table for it")

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-ironhail"):
        raise SystemExit(f"refusing {out_p.name}: this builder's links are sc-ironhail*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: 02-chain already has a link of that name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    # READ AS BYTES: read_text() turns CRLF into LF, so this refusal could never fire (found by
    # thornwake_build.py, v113; for an LF source the two reads are the same text, so no link moves).
    s0 = src_p.read_bytes().decode("utf-8")
    if "\r" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nIRONHAIL / QUARRELSTORM (REDESIGN) -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The relic this builder redesigns, with its shipped
    # body; the engine's gates the hail pays through; the window clock.
    row = relic_row(code, RELIC)
    for need, why in (('shape:"bow"', "Ironhail is not a bow"),
                      ('mode:"ranged"', "Ironhail is not ranged"),
                      ("onHit:{ sunder:1 }", "Ironhail does not carry the dwarven channel"),
                      ("shot:{ cadence:0.34,", "Ironhail's shot has moved")):
        if need not in row:
            raise SystemExit(f"wrong base: {why}")
    for need, why in (("hurt(foe, dmg, src){", "no hurt(foe, dmg, src) gate"),
                      ("apply(key, n, src){", "no Fighter.apply(key, n, src)"),
                      ("get alive(){ return this.hp > 0; }", "no Fighter.alive"),
                      ("beat(o){", "no beat(o)"),
                      ("fireUlt(f, foe){", "no fireUlt"),
                      ("spawnShot(", "no spawnShot (the bow's fire)")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'\n  sunder:\s+\{ name:"Sunder",', code):
        raise SystemExit("wrong base: no STATUS.sunder")
    # THE WINDOW CLOCK: a hit stop returns from step() before the window tickers.
    st = code[code.find("  step(dt){"):]
    hs = st.find("if (this.hitStop > 0){")
    tt = st.find("this.tickTendril(dt);")
    if tt < 0:
        raise SystemExit("wrong base: no `this.tickTendril(dt);` in step() -- the hail's ticker "
                         "goes after Tendril's (v68), so this is not the Tendril lineage")
    if hs < 0 or not hs < st.find("return;", hs) < tt:
        raise SystemExit("wrong base: the window tickers do not stop in a hit stop")
    # THE NAMES THIS BUILD ADDS ARE FREE ON THE BASE.
    if A.stage == "1":
        for name in ("ultHail", "hailTally", "tickHail", 'kind:"hail"', '"hail"'):
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
        if re.search(r"\bthis\.hail\b|\bm\.hail\b", code):
            raise SystemExit("'this.hail' is already in the base")
        if s0.count(SHIPPED_ULT) != 1:
            raise SystemExit("wrong base: Ironhail does not carry the shipped Quarrelstorm")
        if len(re.findall(r'kind:"volley"', code)) != 1:
            raise SystemExit("wrong base: kind \"volley\" is not Ironhail's alone -- "
                             "the nova cannot be retired")
        if f"dmg:{SHIPPED_DMG}," not in row:
            raise SystemExit("wrong base: Ironhail is not at its shipped blade")
    print("  base  Ironhail's shipped body (bow, ranged, sunder 1); hurt / apply / beat / "
          "STATUS.sunder; the window tickers stop in a hit stop")

    blade = None
    S5 = s5_edits(ALT50_BLADE) if A.alt50 else []
    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if 'kind:"hail"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "tickHail" in code or "charge:1e9" not in row:
                raise SystemExit("stage 2 goes on stage 1, once")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "tickHail" not in code or "sunder:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["sunder"])
        elif A.stage == "6":
            # STAGE 6 GOES ON THE FINAL, ONCE: Ironhail's ult block is stage 3's
            # to the character, its blade the shipped one (not the 50% link);
            # none of stage 6's names is in the source yet (on identifier
            # boundaries) and the Sfx has no Ironhail arm.
            want = ult_block(ULT["charge"], ULT["sunder"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{SHIPPED_DMG}," not in row):
                raise SystemExit("stage 6 goes on the final (stage 3's link, blade "
                                 f"{SHIPPED_DMG}): Ironhail's ult block or blade is not the final's")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if S6_CAST_ARM in code:
                raise SystemExit("the Sfx already has an Ironhail arm -- stage 6 goes on once")
            edits = S6
        else:
            if f'sunder:{ULT["sunder"]},' not in row or f"dmg:{SHIPPED_DMG}," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            blade = ALT50_BLADE
            edits, want = S5, ult_block(ULT["charge"], ULT["sunder"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Ironhail's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if f"dmg:{blade if blade is not None else BLADE}," not in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the blade is not the one this stage writes")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    # aside) draws no RNG, never takes the one ultFx slot (open item 25),
    # calls nothing that hurts, applies, resolves or shatters, writes only
    # what S6_WRITE_OK names and mutates only its own arrays. It READS the
    # window, the tally, the bolts and the foe's count; the probe's [10]-[11]
    # and engine_ab are the dynamic proof.
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|"
                     r"tickHail|spawnShot)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
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
    if A.stage == "6":
        if inlined_fx(s) != inlined_fx(s0):
            raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                             "(the nova's field spec is the orchestrator's sync_fx_remove)")
        if re.search(r'\bu\.w === "ironhail"', out_code):
            raise SystemExit("REFUSING TO WRITE -- the nova's art on the ultFx slot is still drawn")
        for need, n in (('SFX.play("ult", { w: "ironhail-land", n: foe.stacks("sunder") });', 1),
                        ('SFX.play("ult", { w: "ironhail-miss" });', 1),
                        (S6_CAST_ARM, 1), ("this.tickQuarrel(dt);", 1)):
            if out_code.count(need) != n:
                raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly {n}x")
        print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, "
              "writes its own fields); the inlined fx.js untouched; the nova's art out; "
              "three voices wired once each")
    for label, _old, new in S1 + S2 + S3 + S5 + S6:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades)\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
    if len(re.findall(r'kind:"hail"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one hail ultimate")
    if 'kind:"volley"' in out_code or 'u.kind === "volley"' in out_code:
        raise SystemExit("REFUSING TO WRITE -- the nova is still here")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one hail ultimate, Ironhail's; the nova out; no insert draws the RNG "
          f"or writes the shared weapon; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
