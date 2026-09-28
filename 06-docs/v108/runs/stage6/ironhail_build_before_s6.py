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
    stage 6   picture, voice, the nova's field out (brief stage 4; not written yet)

THE CARRY is stages 1, 2 and 3. Stage 3's link is the final: the brief's
target is the shipped rate, and on 151 the redesign reads it at the shipped
blade (below, stage 5).

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

STAGE_OUT = {"1": "sc-ironhail-stub", "2": "sc-ironhail-hail", "3": "sc-ironhail-sunder",
             "5 --alt50": "sc-ironhail-b14"}


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
    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)
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

    s0 = src_p.read_text(encoding="utf-8")
    if "\r\n" in s0:
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
    for label, _old, new in S1 + S2 + S3 + S5:
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
