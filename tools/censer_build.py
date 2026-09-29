#!/usr/bin/env python
"""CENSER / CONSECRATION -- the sanctified warhammer's ultimate, REDESIGNED. v109.

Built from `06-docs/v78/censer-consecration-redesign-v78.md` (Cowork,
2026-09-26; its §5 is the build brief) and its runs (`06-docs/v78/runs/
holyground_*`, `tools/overlays/holyground.js`), which are the input and the
only input. CLAUDE.md §3 rule 0: nothing here is a design decision.

A REDESIGN, NOT A NEW RELIC. Censer ships in the base; its nova
(Consecration, kind "nova": 12 damage and 3 Smite in 300, knock 300) is
replaced by the design's holy ground.

    stage 1   the ultimate stubbed            <tip> -> sc-censer-stub.html          (arm A)
    stage 2   the ground and the smite        -> sc-censer-ground.html              (arm B, tickDmg 0)
    stage 3   the heal, bless 0 -> 1          -> sc-censer-consecration.html        (arm C, tickDmg 0)
    stage 5   the blade, 28.77 -> BLADE       -> sc-censer-consecration-b<BLADE>.html
    stage 6   the picture and the voice  -> sc-censer-consecration-b<BLADE>-fx.html (presentation)
              design §5's "Stage 4 -- picture, voice, carry", on stage 5's link;
              no fx.js field (reading 18). The carry is the orchestrator's:
              stages 1, 2, 3, 5 and 6 on its tip, and `fx_remove.py` for the
              nova's SPECS entry.

The design's §5 stages it as "Stage 1 -- nova out, m.holyGround[] in (discs
with x, y, t0), the tests", "Stage 2 -- the heal", "Stage 3 -- the blade",
"Stage 4 -- picture, voice, carry". This build puts a stub under them (its
stage 1, which must be arm A fight for fight) and numbers the blade 5, as the
batch does (v107's numbering).

§1: "For a duration every blow the hammer lands consecrates the ground where
it landed: a circle of holy ground that lasts. An enemy standing on holy
ground is smitten for as long as it stands there. Censer standing on holy
ground is healed."

Declared (design §1, §3, §4):
  THE GROUND  a disc r `groundR` (90) at each blow's landing point, living
              `groundLife` (8s); it does not move.
  THE SMITE   the foe on the ground: smite +`smite` (1) every `tickCd` (0.5s).
              No damage ("The tick's damage is dropped"), no knock, no beat.
  THE HEAL    Censer on the ground: blessing +`bless` (1) every `blessCd`
              (1.0s). Stage 3.

THE CHARGE. The design names none: its lab cast every 16s of its own step
clock (`P.charge`, the harness default; `P` in runs/holyground_*.json), which
counts hit-stop freezes. Rick, 2026-09-27, for the whole batch: "use the
game's equivalent". Measured for this fighter on the lab's arm C by counting
frozen lab steps (v109 §0). The shipped 15 was the nova's and goes with it.

THE WINDOW. The design's prose says only "for a duration"; its lab priced
every arm at P.dur 8 (seconds), and that is the build's `dur`, kept on the
window tickers' clock (below) like every window in the batch.

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE LANDING POINT is the struck ball's position at the hit (§4: "the
     FOE's position at the hit"; §1: "the ground where it landed"), taken in
     `resolveHit` beside `self.hits++` -- the count the lab watched (`me.hits`
     rising) -- for the hammer's own blows (`mul === undefined`) while the
     window is open. The lab read the foe after the step, which is the same
     point (nothing moves a ball between `tickHits` and the step's end). A
     blow on a Twinshade shade consecrates the shade's ground, where it
     landed; the lab, which never sees a shade, planted at the opponent.
     Only the fights against Twinshade can differ; the probe counts them.
  2. THE GROUND ACTS ONLY WHILE ITS CASTER'S WINDOW IS OPEN (the lab: every
     test sits after `if (!open) return`, and every priced number -- the
     gates' ~4 smite and ~2.6 blessing a cast -- is a window count). A disc
     lives `groundLife` from its blow and does not move; after the window
     closes it stands inert until it expires, and a disc still alive when the
     next window opens acts in it (the lab's list is the fight's, filtered by
     age only; at the lab's 16 against 8 + 8 that could never happen, at the
     engine's 14 it can, and the probe counts it). The prose's other reading
     -- holy ground smites and heals for its whole life, window or not -- is
     put to Rick with its measured size (v109 §6).
  3. THE FOE IS ON THE GROUND when its ball touches a disc: its centre within
     groundR + R (the lab's `on`, H.R). The prose does not say centre for the
     foe ("an enemy standing on holy ground").
  4. THE CASTER IS ON THE GROUND when its CENTRE is within groundR of a disc
     (§4, explicit: "while the caster's centre is within a disc"). The lab
     tested the caster's ball like the foe's (groundR + R); v109 §2 measures
     the difference with a scratch variant on the lab's test.
  5. THE GROUND IS ITS CASTER'S: a disc carries its side, which names its
     caster for the purge (its `groundLife`) and for the probe, and only its
     own caster's window reads it (the lab had one caster). There is no mirror
     match: `Match` refuses a relic against itself, so no test can tell this
     side test from none (the stage-5 review's mutant mx4-side).
  6. THE CADENCES: the smite once per `tickCd`, the blessing once per
     `blessCd`; each cooldown is 0 at the cast and runs down through the
     whole window, on the ground or off (the lab's `cd -= dt` every open
     frame), so a foe that steps on after a gap is smitten on that frame.
  7. `apply`'s SOURCE IS A SIDE LETTER for both (the engine's contract; the
     lab passed the Fighter). Smite reads it: a fatal smite tick's beat is
     attributed by `st.src` (presentation; the director's). Blessing reads
     none.
  8. THE TICK'S DAMAGE IS DROPPED (§3, "taken"): the lab's `tickDmg` defaults
     to the rejected 2, so every lab arm passes tickDmg=0. The ground's only
     writes are smite on the foe and blessing on the caster: no damage, no
     knock, no move, no beat, no hit stop, no rng. Smite's own dps and its
     fatal-tick beat are the status's existing machinery (`tickStatus`).
  9. THE WINDOW CLOSES on its clock or either death (the lab's). No wither and
     no wait: the charge and the window run on one clock and 8 < the charge,
     so a cast cannot come under a standing window.
 10. THE TARGET IS THE OPPONENT, never a Twinshade shade (the lab's `foe`).
 11. THE GROUND IS ON THE MATCH (§5: "`m.holyGround[]` in (discs with x, y,
     t0)"), each disc {x, y, t0, side}; `t0` is read on `m.holyT`, the
     ground's own clock, which is the window tickers' (it stops in a hit
     stop), so a disc's 8s are 8 seconds of the window clock. "The hall's
     close does not clip it": nothing removes a disc but its age.
 12. NOTHING ELSE: the hammer swings as ever.

STAGE 6, THE PICTURE AND THE VOICE (design §4 "Picture" and "Sound"; §5's
"Stage 4 -- picture, voice, carry"). Picked on measurements under Rick's "you
pick i overrule" by the picture lab (scratch) and `censer_voice_lab.py` (v109
§5); the rows are the labs', byte-exact. Declared:
 13. THE PICTURE READS THE WINDOW OFF `ultHoly && alive && !over` and keeps
     its own state on the fighter (`cons*`), never on `m.ultFx` (one slot,
     and the foe's cast takes it: open item 25). `tickConsecration` runs in
     `tickPresentation`, on the presentation clock, which runs through hit
     stops and after `over`. So the head cools over 0.3s at a clock close, a
     death or the verdict (`tickHolyGround` never runs once `over` is set,
     and a window open at the kill would otherwise stay lit), and the ground
     fades out over 0.3s after the kill.
 14. THE DISCS ARE THE SIMULATION'S, READ AND NEVER WRITTEN: a picture record
     {d, age} per disc of `m.holyGround`, made the frame the disc exists and
     dropped the frame the simulation removes it. A disc blooms out of the
     impact point over 0.3s on the PRESENTATION clock (the planting blow's
     hit stop stops `holyT`; v54's lesson) and fades over the last second of
     its SIM life (`holyT - t0` against `groundLife`), reaching 0 the step it
     goes. It is drawn for its whole life: LIVE (fill 0.18) while its
     caster's window is open, INERT (0.07) once it closes -- the ground acts
     only in a window (reading 2) and works again at the next cast.
 15. ON THE GROUND IS `tickHolyGround`'S OWN TEST AS IT RAN, found by watching
     `holyTally` rise: a step the window ticked (`frames` rose) is a foe-on
     step iff `foeOn` rose with it, a Censer-on step iff `selfOn` did; a
     smite tick is `ticks` rising, a blessing `bless` rising. So the ticker
     makes no call for the picture. The tag rule (Corona's, Daybreak's,
     Zenith's, Canopy's, Benediction's): the first smite of each on-ground
     stretch tags SMITE on the foe, the first blessing BLESSING on Censer.
     The picture writes its `cons*` fields, the tags and `taught` only, and
     draws no rng (shellHash and the clocks place the incense).
 16. THE VOICES ON THE SIM PATH ARE TWO `SFX.play` CALLS, each a no-op
     headless that writes nothing the simulation reads: the disc's bell in
     `resolveHit`, once per disc planted, after `holyTally.discs++`, with n
     the caster's discs standing (a block-scoped count that reads
     `m.holyGround`), clamped to 1..5 in the arm; and the heal, the existing
     spark collect, unchanged, once per blessing after `T.bless++`, with the
     blessing Censer now carries (Zenith's call word for word). The cast's
     voice is fireUlt's own `SFX.play("ult", { w: f.w.id })`, which found no
     arm and fell through to rune-crack: the arms are ADDED before that
     shared fallback, which is re-emitted unchanged for the relics that
     still use it. The smite tick has no voice ("nothing new"; no smite voice
     exists in the synth). There is no close voice: the design names none.
 17. A DISC PLANTED BY A KILLING BLOW RINGS ITS BELL on the step the death
     voice plays (the survey: 32 of 716 discs); the bell is the blow's own
     consequence, and the design's "a disc opening" has no exception.
 18. NO fx.js FIELD (design §4: "incense motes rising from each disc (both
     fx.js copies)"). A SPECS field rides the one ultFx slot, fires once, at
     the cast, where Censer stood -- and no disc exists at the cast: the slot
     is Censer's a median 0.68s of the 8s window, and 10 of 163 discs exist
     while it is (the picture lab's fxprobe, 101 windows). The incense is
     drawn instead, off every disc, in the world pass. This builder edits
     neither fx.js copy, and stage 6 refuses if its edits touched the
     inlined one. The nova's `SPECS.censer` burst is the retired ultimate's:
     the orchestrator takes it out of both copies at the carry
     (`fx_remove.py --relic censer`). Rick's to overrule.
 19. THE NOVA'S ART IS RETIRED WITH THE NOVA: drawUltUnder's glyph ring and
     drawUltOver's smoke and incense sparks (both drawn at every cast from the
     ultFx record, out to the 300 fallback radius), and the life map's
     `censer: 1.6` (the cast's record falls to the map's own 1.5, and nothing
     draws from it). The charge rune, ULTSIG.censer, is redrawn: the censer
     swung over a disc of holy ground that fills with the charge. The four
     are replaced, not re-emitted: every other anchor is.

THE CLOCK. The window, both cooldowns and the discs' lives run on the window
tickers' clock, which stops through a hit stop (Corollary's, Daybreak's,
Zenith's, Canopy's, Onslaught's, Tendril's and Bulwark's convention). The lab
ran them all through freezes; v109 §2 measures what that is worth here.

THE ORDER. `tickHolyGround` runs with the window tickers, after
`tickTendril`: after every ball has moved this frame, before `tickHits`. A
disc planted by a blow in `tickHits` is tested from the next live frame on.

WHAT IS RETIRED. The nova's numbers (radius 300, dmg 12, apply smite 3, knock
300) and its card leave Censer's row, and its kind becomes "holyground". THE
NOVA ITSELF STAYS: on this base Widowmaker's Exsanguinate and Lightkeeper's
Bulwark are kind:"nova" and the generic tail of `fireUlt` is theirs (their
own redesigns, v106 and v107, may be carried before or after this one); the
holyground branch returns before it. The builder reads who is still a nova
and never refuses on it: this build touches none of the nova's code.
The nova's presentation keyed on the id -- ULTSIG `censer`, the two
`u.w === "censer"` draw branches (the glyph ring and the smoke), the `life`
map's 1.6, the fx.js SPECS `censer` burst and the rune-crack fallback voice
-- is picture and sound, and design §5 retires it at its stage 4 ("nova's
field spec out"): this build's stage 6 (readings 16, 18, 19), which takes out
the draw branches and the life entry, redraws the sigil and gives Censer arms
of its own before the fallback; the SPECS burst is the orchestrator's to take
out of both fx.js copies at the carry. Nothing in the simulation reads any
of it.

THE BASE is asserted BY CONTENT (the features this builder needs), never by
which relic is last, so it re-applies on a later tip that carries other new
relics or other redesigns. No insert writes the shared weapon row or a shared
module table (STATUS, CONFIG, AFFINITIES, WEAPONS, SHAPES).
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "censer"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). Design §1, §3, §4.
ULT = {
    "charge": 14,       # the lab's 16 on the game's clock (Rick's batch ruling; measured, v109 §0)
    "dur": 8,           # the lab's window ("for a duration"; P.dur 8)
    "groundR": 90,      # "a disc r 90 at each blow's landing point"
    "groundLife": 8,    # "8s life"; "the disc lives 8s and does not move"
    "tickCd": 0.5,      # "foe.apply("smite", 1, f) every 0.5s"
    "smite": 1,         # "+1 every 0.5s on the ground"
    "blessCd": 1.0,     # "f.apply("blessing", 1, f) every 1.0s"
    "bless": 1,         # "blessing +1 a second while Censer stands on it" -- stage 3
}
TIP = "Its blows make holy ground: foes on it are smitten, and it heals there"
# THE SHIPPED ROW, which this builder asserts before it touches it.
PHYS = ('blades:[0], reach:76, width:26, artW:54, dmg:28.77, spin:1.6, '
        'mode:"spin", mass:5.0, knockMul:2.3,')
OLD_ULT = ('''    ult:{ name:"Consecration", charge:15, kind:"nova", radius:300, dmg:12, apply:{smite:3}, knock:300, tip:"Nova: 12 damage, 3 Smite, knockback" },
''')
# THE STATUSES THE LAB PRICED (STATUS.smite and STATUS.blessing as shipped).
STATUSES = ('smite:      { name:"Smite",      maxStacks:4, dur:3.2, dps:1.5,',
            'blessing:   { name:"Blessing",   maxStacks:5, dur:6.0, hps:1.2,')


def ult_block(charge, bless) -> str:
    return (f'''    ult:{{ name:"Consecration", charge:{charge}, kind:"holyground", dur:{ULT["dur"]},
          groundR:{ULT["groundR"]}, groundLife:{ULT["groundLife"]}, tickCd:{ULT["tickCd"]}, smite:{ULT["smite"]}, blessCd:{ULT["blessCd"]},
          bless:{bless},          // v78: the heal (stage 3)
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
        raise SystemExit("REFUSING TO WRITE -- no `node` on PATH, so the output "
                         "cannot be syntax checked")
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
# THE NOVA OUT, THE HOLY GROUND'S BLOCK IN, STUBBED at charge 1e9 (the clock
# can never reach it, `fireUlt` never runs for Censer) -- Starwarden's stage-1
# pattern, on a relic that already ships. Nothing else in the row moves, so
# this link must be the lab's arm A (the relic with no ultimate) to the fight.
S1 = [

("Consecration's nova out, the holy ground's block in, stubbed",
 OLD_ULT,
 '''    /* CONSECRATION, REDESIGNED (v78; built v109): the nova is out and the
       holy ground is in. `kind:"holyground"`. Stage 1 stubs it at charge
       1e9; stages 2-3 give it its ground and smite, then its heal. */
''' + ult_block("1e9", 0)),

]

# ---------------------------------------------------------------- stage 2 --
S2 = [

("the ground has a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Consecration", charge:1e9, kind:"holyground", dur:8,
''',
 f'''    ult:{{ name:"Consecration", charge:{ULT["charge"]}, kind:"holyground", dur:{ULT["dur"]},   // v78 stage 2: the ground is consecrated
'''),

("the fighter carries the window",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur, cd, bcd} while CONSECRATION's window is open (v78): `cd` is
       the smite's cooldown, `bcd` the blessing's. null on every other relic
       and on this one outside its window. `holyTally` is the probe's count,
       cumulative over the fight; nothing in the simulation reads it. The
       ground itself is the match's (`m.holyGround`). */
    this.ultHoly = null;
    this.holyTally = null;
'''),

("the match carries the holy ground and its clock",
 '''    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed
''',
 '''    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed
    /* CONSECRATION'S GROUND (v78): SIM objects, discs {x, y, t0, side}, one
       a blow Censer lands in its window, at the struck ball. `holyT` is the
       ground's own clock, the window tickers' (advanced in `tickHolyGround`,
       so it stops in a hit stop); a disc goes when `holyT - t0` reaches its
       caster's `groundLife`, and nothing else removes one. Empty in every
       match without Censer. */
    this.holyGround = [];
    this.holyT = 0;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "holyground"){
      /* CONSECRATION (v78). NOTHING RESOLVES HERE, and the nova's tail below
         is never reached: the cast opens the window for `u.dur` seconds, the
         hammer's blows consecrate the ground (`resolveHit`) and
         `tickHolyGround` does the rest. Both cooldowns start at zero, so a
         foe already on the ground is smitten on the first frame. */
      f.ultHoly = { t: 0, dur: u.dur, cd: 0, bcd: 0 };
      if (!f.holyTally)
        f.holyTally = { casts: 0, frames: 0, discs: 0, foeOn: 0, ticks: 0,
                        selfOn: 0, bless: 0, foeStk: 0 };
      f.holyTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("a blow in the window consecrates the ground where it landed",
 '''    self.hits++; self.dealt += dmg;
''',
 '''    self.hits++; self.dealt += dmg;
    /* CONSECRATION (v78 §1, §4): "every blow the hammer lands consecrates the
       ground where it landed" -- a disc at the struck ball's position at the
       hit, the hammer's own blows only, while the window is open. Beside
       `self.hits++`, the count the lab watched. `ultHoly` is null on every
       other relic, so this is one null test for them. */
    if (self.ultHoly && mul === undefined){
      this.holyGround.push({ x: foe.x, y: foe.y, t0: this.holyT,
                             side: self === this.a ? "a" : "b" });
      self.holyTally.discs++;
    }
'''),

("the ground ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickHolyGround(dt);            // CONSECRATION (v78)
'''),

("tickHolyGround ages the ground, smites the foe on it and heals the caster",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================ THE HOLY GROUND ====
     v78 §1 / §4. The ground's clock, and while a Censer's window is open:
       THE GROUND  every disc ages on `holyT`, the window tickers' clock, and
                   goes when its caster's `groundLife` is up. It does not move
                   and nothing else removes it. It acts only while its own
                   caster's window is open (the lab's reading), and a disc
                   still alive at the next cast acts in that window too.
       THE SMITE   the foe's ball on any of the caster's discs -- its centre
                   within groundR + R -- and the cooldown clear: smite
                   +`smite` on the foe, the cooldown `tickCd`. No damage, no
                   knock, no beat, no hit stop.
       THE HEAL    the caster's CENTRE within groundR of one of its discs
                   (v78 §4) and its cooldown clear: blessing +`bless` on the
                   caster, the cooldown `blessCd`. Stage 3.
     Both cooldowns run through the whole window, on the ground or off. The
     window closes on its clock or either death. The target is the OPPONENT
     only. `apply`'s source is a side letter. */
  tickHolyGround(dt){
    this.holyT += dt;
    const G = this.holyGround;
    for (let i = G.length - 1; i >= 0; i--){
      const d = G[i], o = d.side === "a" ? this.a : this.b;
      if (this.holyT - d.t0 >= o.w.ult.groundLife) G.splice(i, 1);
    }
    for (const f of [this.a, this.b]){
      const Z = f.ultHoly;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultHoly = null; continue; }
      const u = f.w.ult, T = f.holyTally, R = CONFIG.physics.ballR;
      const side = f === this.a ? "a" : "b";
      T.frames++;
      T.foeStk += foe.stacks("smite");
      Z.cd -= dt;
      Z.bcd -= dt;
      let foeOn = false, selfOn = false;
      for (const d of G){
        if (d.side !== side) continue;
        if (Math.hypot(foe.x - d.x, foe.y - d.y) < u.groundR + R) foeOn = true;
        if (Math.hypot(f.x - d.x, f.y - d.y) < u.groundR) selfOn = true;
      }
      if (foeOn){
        T.foeOn++;
        if (Z.cd <= 0){
          Z.cd = u.tickCd;
          foe.apply("smite", u.smite, side);
          T.ticks++;
        }
      }
      if (selfOn){
        T.selfOn++;
        if (u.bless > 0 && Z.bcd <= 0){
          Z.bcd = u.blessCd;
          f.apply("blessing", u.bless, side);
          T.bless++;
        }
      }
    }
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the heal",
 '''          bless:0,          // v78: the heal (stage 3)
''',
 f'''          bless:{ULT["bless"]},          // v78: the heal (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE (design §5 "Stage 3 -- the blade, wide on 151 at 26 / 26.5 / 27
# to the shipped rate"; §3: "at 57.9% against a shipped 50.3 the blade comes
# from 28.77 to about 26.5"). The design's own target is THE SHIPPED RATE,
# read on 151 (the shipped nova on this base, relic_rate both sides, two
# blocks), never the published 50.3 (the nova on Chromium 141). The design
# gives the build no knob to move first. Rick's other choice, 50%, is
# measured beside it (v109 §4).
# THE SHIPPED RATE ON 151: the nova on this base, relic_rate both sides, two
# blocks (seed0 2207 / 2317), 1480 fights: 49.5 / 50.8 -> 50.1%.
# The brief's three on stage 3 (--set dmg, the same fights): 26 -> 52.6,
# 26.5 -> 53.6, 27 -> 55.0 -- all over the shipped rate. The design names no
# knob, so the grid was widened DOWN inside "the hammer row 20-29" (§3), a
# fixed grid read after the three, no bisection: 25.5 -> 49.6, 25 -> 51.2,
# 24.5 -> 48.6, 24 -> 45.2. The line through the seven crosses the shipped
# rate at 25.26 and 50% at 25.22. BLADE 25.5 IS THE MEASURED POINT NEAREST
# THE SHIPPED RATE (49.6 against 50.1) AND NEAREST 50% as well: on 151 the
# shipped nova reads 50.1, so the design's target and Rick's other choice are
# the same point here. It sits 1.0 under the design's "about 26.5", which was
# priced at 141 on the lab's clock; the built relic reads over the lab by the
# window clock (v109 §2).
BLADE = 25.5

S5 = [] if BLADE is None else [
("the blade: the shipped rate",
 '''  { id:"censer", name:"Censer", aff:"sanctified", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:28.77,''',
 f'''  {{ id:"censer", name:"Censer", aff:"sanctified", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:{BLADE},'''),
]

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (design §4 "Picture" and "Sound"; its §5
# "Stage 4 -- picture, voice, carry"), picked on measurements under Rick's
# "you pick i overrule" by the picture lab (scratch, `ce_rows.py`) and
# `censer_voice_lab.py` (v109 §5). PRESENTATION ONLY: engine_ab over all 38
# relics, Censer included, is the proof, and the probe's [10]-[11] read the
# voices and the picture's hook inside the fight. The rows are byte-exact to
# the labs' own files (voice 63c842fa690c5f02, 3 rows; picture
# 5133d7afb3acb9e9, 10 rows); the picture rows alone reproduce the picture
# lab's stamp (b3f790861677e2bd), the voice rows alone the voice lab's page
# (6af8bc7cac4bf257), and the two sets give the same bytes in either order
# (3d68c7648a9cb3a8). No two rows share an anchor, so none is merged.
#   THE VOICE: two arms -- the cast's thurible swing and the disc's bell --
#   ADDED before the shared rune-crack fallback, which is re-emitted
#   unchanged, last; two calls on the sim path, each after a count this
#   build's stage 2 already keeps (the bell after `holyTally.discs++` in
#   resolveHit, the heal chime after `T.bless++` in tickHolyGround).
#   THE PICTURE: `tickConsecration` in tickPresentation; the floor in the
#   world pass under both balls (the discs, the lattice, the rims, the
#   incense, the foe's rim, Censer's drift); the head's hot core in the
#   emissive pass over both fighters; the nova's art retired (the glyph
#   ring, the smoke, the life entry) and the charge rune redrawn.
# COMPOSITION: nine anchors are re-emitted; four are consumed, all Censer's
# own (the nova's two art branches, ULTSIG.censer, and the life map's
# narrowest token `censer: 1.6,`, which leaves Aureole's entry on the same
# line to its own build). The rows ride on three of stage 2's own lines
# (the fields, the plant's count, the blessing's count) and on shared lines
# every stage 6 of the batch uses as `after` / `before` anchors
# (tickPresentation's first call, tickWinnow, the world and emissive passes,
# drawMotes, the rune-crack fallback).
S6 = [

("Sfx: Censer's cast (the thurible swing) and disc-bell arms, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "censer"){                     // the censer swings
          /* CENSER'S CAST, THE SWING -- v78 s4: "a thurible swing (a
             chain-rattle into a low bell, 0.5s)". JINGLE, of 5, picked on the
             numbers by `censer_voice_lab.py` under Rick's "you pick i
             overrule" (v109). Censer had no arm and fell through to
             rune-crack, which other relics still use, so this ADDS arms before
             that fallback and leaves it alone.

             Nine links of the chain ringing as bands of noise (Q 6, 30 ms,
             3.3-6.1 kHz), rising in level, then a church bell struck on A: hum
             A2, prime A3, tierce, quint and nominal A4, with the clapper's
             knock. The bell struck 206 ms in, after 9 onsets of the rattle
             (5.8 dB under it, centroid 4852 Hz); audible 495 ms; the bell's
             strongest peak 110 Hz, 99% of its power under 500 Hz; loudest 50
             ms -2.9 dB re Censer's own blow. Register at most 0.69 (Ironhail's
             cast, on the batch line) against rune-crack, the school's and the
             warhammers' casts, the seal, the death voice, the clank, the blow
             and the batch line's other voices. */
          const g = 0.1083, kr = 8.734, D = 0.415, S = 0.2, F = 220;
          for (const [s, f, k] of [[0, 4100, 0.45], [0.019, 5300, 0.52], [0.041, 3700, 0.58],
                                   [0.057, 6100, 0.64], [0.082, 4600, 0.71], [0.101, 3300, 0.77],
                                   [0.126, 5700, 0.84], [0.148, 4300, 0.92], [0.171, 5000, 1]]){
            this._burst(t + s, { freq: f, q: 6, gain: g * kr * k, dur: 0.03, type:"bandpass" });
          }
          for (const [r, k, d] of [[0.5, 0.5, 1.5], [1, 0.7, 1], [1.2, 0.55, 0.8], [1.5, 0.3, 0.6], [2, 1, 0.5]])
            this._tone(t + S, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;
          this._burst(t + S, { freq: F * 4, q: 0.9, gain: g * 0.25, dur: 0.012, type:"bandpass" });
        } else if (w === "censer-disc"){                // and the ground is consecrated
          /* A DISC OPENING -- "a soft bell tone, pitch by disc count" (v78
             s4). BOWL, of 5 (`censer_voice_lab.py`). `resolveHit` plays it
             once per disc planted, on the blow's frame, with `n`, the caster's
             discs standing on the ground after the push.

             A struck bowl (two sines on its 1 : 2.71 modes, the upper at 0.3
             and dying half as long): one step of the score's A minor
             pentatonic a disc, C5 D5 E5 G5 A5 (counts clamped to 1..5).
             Audible 400 ms at every count; its loudest 50 ms -11.0 dB re the
             blow and +11.0 dB re the wall tick; over the heaviest blow on its
             frame by +13.0 dB or more in its note's third-octave. Register at
             most 0.66 (Angelus's cast, on the batch line) against the heal
             chime that follows it, Zenith's tick, the wall tick, the runic
             snap, the blow, rune-crack, the cast and the batch line's other
             voices. */
          const n = clamp(Math.round(p.n || 0), 1, 5), g = 0.04177, D = 0.612;
          const F = [523.25, 587.33, 659.26, 783.99, 880][n - 1];
          for (const [r, k, d] of [[1, 1, 1], [2.71, 0.3, 0.55]])
            this._tone(t, { freq: F * r, gain: g * k, dur: D * d, type:"sine" }).frequency.value = F * r;
        } else {                                        // rune-crack'''),

("resolveHit: the disc bell, once per disc planted, with the caster's discs standing",
 '''      self.holyTally.discs++;''',
 '''      self.holyTally.discs++;
      /* CONSECRATION'S DISC (v78 s4: "a disc opening -- a soft bell tone,
         pitch by disc count"): once per disc planted, on the blow's frame,
         `n` the caster's discs standing on the ground now, this one
         included (the purge ran earlier this step, in tickHolyGround). The
         blow keeps its own `hit` voice. A block-scoped count that READS
         the ground and writes nothing; SFX.play is a no-op headless and
         nothing is read back (censer_voice_lab: fights identical). */
      { const sd_ = self === this.a ? "a" : "b";
        let n_ = 0;
        for (const d_ of this.holyGround) if (d_.side === sd_) n_++;
        SFX.play("ult", { w: "censer-disc", n: n_ }); }'''),

('tickHolyGround: the heal chime (spark collect, unchanged), once per blessing, with the count',
 '''          T.bless++;''',
 '''          T.bless++;
          /* CONSECRATION'S HEAL (v78 s4: "the heal -- the `spark collect`
             voice, reused"): the EXISTING heal chime, unchanged, once per
             blessing, after the apply, with the count Censer now carries --
             Zenith's call word for word. Presentation only; nothing is read
             back (censer_voice_lab: fights identical). */
          SFX.play("spark", { collect: true, n: f.stacks("blessing") });'''),

('consecration picture: fighter fields',
 '''    this.ultHoly = null;
    this.holyTally = null;
''',
 '''    this.ultHoly = null;
    this.holyTally = null;
    /* CONSECRATION'S PICTURE (v78 section 4), and none of it is the window:
       the head cools for 0.3s after `ultHoly` is gone, a disc outlives the
       window and blooms on a clock that runs through the hit stop of the blow
       that planted it, and "the foe is on the ground" holds through a hit
       stop, so the picture keeps its own state. On the FIGHTER and never on
       `m.ultFx` (one slot, and the opponent's cast takes it: open item 25).
       Driven in `tickPresentation` (`tickConsecration`); nothing in the
       simulation reads any of it.
         consFade -- the head's light: 1 while the window is open; eased to 0
                     over the close
         consAge  -- the presentation clock since the cast (the ignition)
         consOut  -- the presentation clock since the close
         consEnd  -- the presentation clock since the verdict (the ground goes)
         consPic  -- this caster's discs as the picture knows them: {d, age},
                     `d` the simulation's own disc (read, never written) and
                     `age` the presentation clock since it was planted
         consFoeOn, consSelfOn -- the foe / Censer was on a disc on the last
                     step the window ticked
         consFoeLit, consSelfLit -- the foe's rim and Censer's drift, 0 -> 1
         consPulse -- a smite tick's flash on the disc under the foe, 1 -> 0
         consSeen -- `holyTally`'s frames, foeOn, ticks, selfOn, bless as last
                     seen
         consTagS, consTagB -- this on-ground stretch has had its SMITE / its
                     BLESSING tag */
    this.consFade = 0;
    this.consAge = 0;
    this.consOut = 0;
    this.consEnd = 0;
    this.consPic = [];
    this.consFoeOn = false;
    this.consSelfOn = false;
    this.consFoeLit = 0;
    this.consSelfLit = 0;
    this.consPulse = 0;
    this.consSeen = [0, 0, 0, 0, 0];
    this.consTagS = false;
    this.consTagB = false;
'''),

('consecration picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickConsecration(dt);          // CONSECRATION'S PICTURE (v78 section 4)
'''),

('consecration picture: tickConsecration',
 '''  tickWinnow(dt){
''',
 '''  /* ------------------------------------------- CONSECRATION'S PICTURE ---
     v78 section 4, on the presentation clock. HALF-SECONDS, like every `life`
     in `tickPresentation` (it runs twice a normal step): 0.5 is the head's
     0.25s ignition at the cast, 0.6 its 0.3s cooling at the close, 0.6 a
     disc's 0.3s bloom, 0.6 the ground's 0.3s fade after the kill, 0.2 / 0.5 the
     foe's rim and Censer's drift coming up (0.1s) and going down (0.25s), 0.6
     a smite tick's flash (0.3s). The window is `ultHoly`, and not once the
     caster falls or the match ends: `tickHolyGround` never runs again once
     `over` is set, so a window open at the kill would otherwise stay lit
     through the verdict. THE DISCS are the simulation's own (`m.holyGround`,
     read, never written): each gets a picture record the frame it exists and
     loses it the frame the simulation removes it. ON THE GROUND IS
     `tickHolyGround`'S OWN TEST AS IT RAN: a step the window ticked
     (`holyTally.frames` rose) is a foe-on step iff `foeOn` rose with it, and
     a Censer-on step iff `selfOn` did; through a hit stop nothing ticks and
     the last answer holds, as the ground does. THE TAG RULE (Corona's,
     Daybreak's, Zenith's, Canopy's, Benediction's): the first smite of each
     on-ground stretch tags SMITE and the foe's count on the foe, the first
     blessing tags BLESSING and Censer's on Censer, both re-armed the first
     step off -- found by watching `holyTally.ticks` and `.bless` rise, so
     `tickHolyGround` makes no call for the picture. Writes presentation
     fields, `tags` and `taught` only, and draws no rng. */
  tickConsecration(dt){
    const G = this.holyGround;
    for (const f of [this.a, this.b]){
      const T = f.holyTally;
      if (!T && !(f.consFade > 0) && !f.consPic.length) continue;   // <- zero burden
      const foe = f === this.a ? this.b : this.a, side = f === this.a ? "a" : "b";
      const Z = (this.over || !f.alive) ? null : f.ultHoly;
      if (Z){
        if (!(f.consFade > 0) || f.consOut > 0){                // a cast
          f.consAge = 0; f.consOut = 0; f.consFoeOn = false; f.consSelfOn = false;
          f.consTagS = false; f.consTagB = false;
        }
        f.consFade = 1;
        f.consAge += dt;
      } else if (f.consFade > 0){
        f.consOut += dt;
        f.consFade = Math.max(0, 1 - f.consOut / 0.6);
      }
      const P = f.consPic;
      for (let i = P.length - 1; i >= 0; i--) if (G.indexOf(P[i].d) < 0) P.splice(i, 1);
      for (const d of G)
        if (d.side === side && !P.some(p => p.d === d)) P.push({ d, age: 0 });
      for (const p of P) p.age += dt;
      if (this.over) f.consEnd += dt;
      if (!T) continue;
      const S = f.consSeen;
      const dF = T.frames - S[0], dO = T.foeOn - S[1], dK = T.ticks - S[2],
            dS = T.selfOn - S[3], dB = T.bless - S[4];
      S[0] = T.frames; S[1] = T.foeOn; S[2] = T.ticks; S[3] = T.selfOn; S[4] = T.bless;
      if (!Z){ f.consFoeOn = false; f.consSelfOn = false; }
      else if (dF > 0){ f.consFoeOn = dO > 0; f.consSelfOn = dS > 0; }
      if (!f.consFoeOn) f.consTagS = false;
      if (!f.consSelfOn) f.consTagB = false;
      if (f.consFoeOn || f.consFoeLit > 0)
        f.consFoeLit = f.consFoeOn ? Math.min(1, f.consFoeLit + dt / 0.2)
                                   : Math.max(0, f.consFoeLit - dt / 0.5);
      if (f.consSelfOn || f.consSelfLit > 0)
        f.consSelfLit = f.consSelfOn ? Math.min(1, f.consSelfLit + dt / 0.2)
                                     : Math.max(0, f.consSelfLit - dt / 0.5);
      if (dK > 0) f.consPulse = 1;
      else if (f.consPulse > 0) f.consPulse = Math.max(0, f.consPulse - dt / 0.6);
      if (!Z || !foe.alive || !(foe.hp > 0)) continue;
      if (dK > 0 && !f.consTagS){
        f.consTagS = true;
        const fs = !this.taught.smite && !!STATUS.smite.tip;
        if (fs) this.taught.smite = true;
        this.statusTag(foe.x, foe.y, "smite", fs, foe.stacks("smite"));
      }
      if (dB > 0 && !f.consTagB){
        f.consTagB = true;
        const fb = !this.taught.blessing && !!STATUS.blessing.tip;
        if (fb) this.taught.blessing = true;
        this.statusTag(f.x, f.y, "blessing", fb, f.stacks("blessing"));
      }
    }
  }

  tickWinnow(dt){
'''),

('consecration picture: the floor call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* CONSECRATION'S GROUND (v78 section 4): the discs, their lattice and rim,
       the incense rising off them, the rim on a foe standing on one and the
       up-drift round Censer on one. FLOOR: the WORLD pass, under both balls,
       source-over -- nothing of it reaches the bloom (CLAUDE.md 4.1c) and no
       ball's disc can be painted over (4.1b). */
    if (__world) this.drawConsecration(m);
'''),

("consecration picture: the head's light (emissive, over both fighters)",
 '''    this.drawSunTop(m);
''',
 '''    this.drawSunTop(m);
    /* CONSECRATION'S HEAD (v78 section 4: "the hammer head lights (a hot
       core, not a white one)"): ON the head, so over both fighters; light,
       so this pass (the bloom may glow it: a small area, measured). */
    this.drawConsecrationTop(m);
'''),

('consecration picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------- CONSECRATION'S PICTURE ---
     v78 section 4, drawn off the fighter's `cons*` fields and the
     simulation's own discs (`m.holyGround`, read) -- never `m.ultFx`, one
     slot the opponent's cast takes (open item 25). HOLY GROUND IS FLOOR: a
     disc of pale gold at 0.18 (the censer's incense gold; the school's glow is
     white) at the sim's own radius (`groundR`, read off the caster, so the
     edge is where the test is), a brighter 3-unit rim with the hole cut in the
     path, and a faint lattice of light on the hall's own diagonal grid. It
     blooms out of the impact point over 0.3s, and fades over the last second
     of its life (the sim's), and it is drawn for its whole life: LIVE at 0.18
     while its caster's window is open, INERT at 0.07 once it closes (it acts
     only in a window, and works again if the next cast finds it standing).
     WORLD pass, under both balls, source-over: nothing under `lighter` and
     nothing the bloom can see. The head's light is the one lit thing, and
     it is `drawConsecrationTop`. One method a component, so each can be
     measured alone; nothing here keeps state or draws from the rng.
       drawConsecration  the floor pass: clipped to the live hall
       _consLive         how live the caster's ground is, and the verdict's fade
       _consGeom         one disc this frame: centre, radius, envelope
       _consFill         its fill
       _consHatch        its lattice
       _consEdge         its rim (brighter while it blooms, and on a smite tick
                         while the foe stands on it)
       _consMotes        incense rising off every disc (the design's field, drawn)
       _consRim          a foe on the ground wears a rim of the gold
       _consDrift        Censer on the ground: the soft up-drift round its shell
       drawConsecrationTop  the head's hot core (emissive, over both fighters) */
  drawConsecration(m){
    const a = m.a, b = m.b;
    if (!a.consPic.length && !b.consPic.length && !(a.consFoeLit > 0) && !(b.consFoeLit > 0)
        && !(a.consSelfLit > 0) && !(b.consSelfLit > 0)) return;       // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    for (const f of [a, b]){
      const L = this._consLive(m, f);
      if (!(L.end > 0.004)) continue;
      for (const p of f.consPic){
        const g = this._consGeom(m, f, p, L);
        if (!g) continue;
        this._consFill(c, g);
        this._consHatch(c, g);
        this._consEdge(c, m, f, g);
      }
      this._consMotes(c, m, f, L);
      this._consRim(c, m, f, L);
      this._consDrift(c, m, f, L);
    }
    c.globalAlpha = 1;
    c.restore();
  }
  /* `live`: the caster's window, up with the head's ignition and down with
     its cooling; `end`: 1 until the verdict, then eased out */
  _consLive(m, f){
    const s = Math.min(1, f.consAge / 0.5), kI = 1 - (1 - s) * (1 - s);
    const live = f.consFade > 0 ? Math.min(kI, f.consFade) : 0;
    const end = m.over ? Math.max(0, 1 - f.consEnd / 0.6) : 1;
    return { live, end };
  }
  /* the bloom on the presentation clock (it plays through the planting blow's
     hit stop); the fade on the disc's sim age, so it reaches 0 on the step
     the simulation removes it */
  _consGeom(m, f, p, L){
    const d = p.d, u = f.w.ult;
    const s = Math.min(1, p.age / 0.6), k = 1 - (1 - s) * (1 - s);
    const fl = Math.max(0, Math.min(1, (u.groundLife - (m.holyT - d.t0)) / 1.0));
    const A = L.end * fl * Math.min(1, s * 3);
    if (!(A > 0.004)) return null;
    return { x: d.x, y: d.y, R: u.groundR, r: u.groundR * k, s, A, live: L.live, d };
  }
  _consFill(c, g){
    c.globalAlpha = g.A * (0.07 + (0.18 - 0.07) * g.live);
    c.fillStyle = "#FFE9A8";
    c.beginPath(); c.arc(g.x, g.y, g.r, 0, TAU); c.fill();
  }
  /* THE LATTICE: lines of constant x - y and x + y, 16 units apart, on the
     hall's grid -- two overlapping discs share one lattice -- clipped inside
     the rim */
  _consHatch(c, g){
    const ri = g.r - 3;
    if (!(ri > 4)) return;
    const S = 16 * Math.SQRT2, q = Math.SQRT1_2;
    c.save();
    c.beginPath(); c.arc(g.x, g.y, ri, 0, TAU); c.clip();
    c.globalAlpha = g.A * 0.13 * (0.4 + 0.6 * g.live);
    c.strokeStyle = "#FFF3C4"; c.lineWidth = 1.1;
    c.beginPath();
    for (const sg of [1, -1]){
      const c0 = g.x - sg * g.y;                      // x - y (sg 1) or x + y (sg -1)
      for (let j = Math.ceil((c0 - ri * Math.SQRT2) / S); j * S <= c0 + ri * Math.SQRT2; j++){
        const e = (j * S - c0) * q, h = Math.sqrt(Math.max(0, ri * ri - e * e));
        const fx = g.x + e * q, fy = g.y - sg * e * q;
        c.moveTo(fx - h * q, fy - sg * h * q);
        c.lineTo(fx + h * q, fy + sg * h * q);
      }
    }
    c.stroke();
    c.restore();
  }
  /* THE RIM, the hole cut in the path (4.1b); brighter while the disc blooms
     -- the consecration spreading from the blow -- and, for 0.3s after each
     smite tick, on every disc the foe's centre stands on (the sim's own test) */
  _consEdge(c, m, f, g){
    const foe = f === m.a ? m.b : m.a, R = CONFIG.physics.ballR;
    let al = 0.2 + (0.45 - 0.2) * g.live + 0.35 * (1 - g.s);
    if (f.consPulse > 0 && foe.alive && Math.hypot(foe.x - g.x, foe.y - g.y) < g.R + R)
      al += 0.4 * f.consPulse * g.live;
    const r0 = Math.max(0, g.r - 3);
    c.globalAlpha = Math.min(1, g.A * al);
    c.fillStyle = "#FFD98A";
    c.beginPath();
    c.arc(g.x, g.y, g.r, 0, TAU);
    if (r0 > 0) c.arc(g.x, g.y, r0, TAU, 0, true);         // the hole
    c.fill();
  }
  /* INCENSE RISING OFF EVERY DISC (the design's field, drawn: a SPECS field
     fires once, at the cast, where Censer stood, and no disc exists then).
     5 a disc, born inside it, rising 42 units and fading; placed by
     shellHash on the disc's planting step and the match clock (the death
     clock after the kill), so they keep moving through a hit stop. */
  _consMotes(c, m, f, L){
    const T = m.t + (m.deathAge || 0);
    c.fillStyle = "#FFE9A8";
    for (const p of f.consPic){
      const g = this._consGeom(m, f, p, L);
      if (!g) continue;
      const sd = 9400 + ((Math.round(p.d.t0 * 120) * 7) % 997);
      for (let i = 0; i < 5; i++){
        const ph = (T * (0.3 + 0.2 * shellHash(sd, i)) + shellHash(sd + 1, i)) % 1;
        const q = TAU * shellHash(sd + 2, i), rr = g.r * Math.sqrt(shellHash(sd + 3, i)) * 0.9;
        const x = g.x + Math.cos(q) * rr + Math.sin(T * 1.3 + i * 2.1) * 3;
        const y = g.y + Math.sin(q) * rr - ph * 42;
        c.globalAlpha = 0.6 * g.A * (0.35 + 0.65 * g.live) * Math.sin(ph * Math.PI);
        c.beginPath(); c.arc(x, y, 1.7 * (1 - 0.4 * ph), 0, TAU); c.fill();
      }
    }
  }
  /* A FOE ON THE GROUND WEARS A RIM OF THE GOLD. Drawn here, under its ball,
     from the shell outward with the hole cut AT the shell: it can only ever
     be a rim, whatever the school (Benediction's measured fix). */
  _consRim(c, m, f, L){
    const foe = f === m.a ? m.b : m.a, k = f.consFoeLit * L.end;
    if (!(k > 0.01) || !foe.alive) return;
    const R = CONFIG.physics.ballR, x = foe.x, y = foe.y;
    const h = c.createRadialGradient(x, y, R, x, y, R + 8);
    h.addColorStop(0, hexA("#FFD98A", 0.8 * k)); h.addColorStop(1, hexA("#FFD98A", 0));
    c.globalAlpha = 1;
    c.fillStyle = h;
    c.beginPath(); c.arc(x, y, R + 8, 0, TAU); c.arc(x, y, R, TAU, 0, true); c.fill();
  }
  /* CENSER ON THE GROUND: the design's "soft up-drift of motes", born round
     its shell and rising 46 units, under the ball (so the shell covers
     whatever of them is inside it) */
  _consDrift(c, m, f, L){
    const k = f.consSelfLit * L.end;
    if (!(k > 0.01) || !f.alive) return;
    const T = m.t + (m.deathAge || 0), R = CONFIG.physics.ballR, sd = f.side ? 9480 : 9460;
    c.fillStyle = "#FFE9A8";
    for (let i = 0; i < 10; i++){
      const ph = (T * (0.55 + 0.3 * shellHash(sd, i)) + shellHash(sd + 1, i)) % 1;
      const q = TAU * (i + shellHash(sd + 2, i)) / 10, rr = R + 2 + 7 * shellHash(sd + 3, i);
      const x = f.x + Math.cos(q) * rr + Math.sin(T * 1.7 + i) * 2;
      const y = f.y + Math.sin(q) * rr - ph * 46;
      c.globalAlpha = 0.75 * k * Math.sin(ph * Math.PI);
      c.beginPath(); c.arc(x, y, 1.9 * (1 - 0.35 * ph), 0, TAU); c.fill();
    }
  }
  /* THE HEAD LIGHTS (v78: "a hot core, not a white one"): the censer's coals
     showing through its piercings -- a hot gold core in the central one, the
     four small ones lit -- and the head's radiant halo stroked gold. At the
     head's own place (`drawWeapon`'s transform and `SHAPES._whRadiant`'s
     geometry), dimmed with a stunned weapon. When Censer is `b` the foe's
     shell is cut out of it: `a` is drawn over `b`, so the foe's shell covers
     b's head, and a core floating over it would paint the foe's disc
     (Zenith's measured rule). Ignites over 0.25s, cools over 0.3s. */
  drawConsecrationTop(m){
    const a = m.a, b = m.b;
    if (!(a.consFade > 0) && !(b.consFade > 0)) return;       // <- zero burden
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [a, b]){
      if (!(f.consFade > 0) || !f.alive) continue;
      const s = Math.min(1, f.consAge / 0.5), kI = 1 - (1 - s) * (1 - s);
      const heat = Math.min(kI, f.consFade) * (f.stun > 0 ? 0.42 : 1);
      if (!(heat > 0.004)) continue;
      const Lw = f.w.reach * m.actMods.reach * f.reachMul + 6, hh = f.w.artW * 0.5;
      const ang = f.theta + (f.bladeSet || f.w.blades)[0] * TAU;
      c.save();
      if (f === b && a.alive){
        c.beginPath(); c.rect(f.x - Lw - R - 60, f.y - Lw - R - 60, 2 * (Lw + R + 60), 2 * (Lw + R + 60));
        c.arc(a.x, a.y, R, 0, TAU); c.clip("evenodd");
      }
      c.translate(f.x, f.y); c.rotate(ang); c.translate(R - 6, 0);
      c.globalAlpha = 0.6 * heat;
      c.strokeStyle = "#FFC24A"; c.lineWidth = Math.max(1, f.w.artW * 0.055);
      c.beginPath(); c.arc(Lw * 0.70, 0, hh * 1.34, 0, TAU); c.stroke();
      c.globalAlpha = 1;
      const hx = Lw * 0.755, rc = hh * 0.5;
      const g = c.createRadialGradient(hx, 0, 0, hx, 0, rc);
      g.addColorStop(0, "rgba(255,222,128," + heat.toFixed(3) + ")");
      g.addColorStop(0.45, "rgba(255,190,80," + (0.85 * heat).toFixed(3) + ")");
      g.addColorStop(1, "rgba(240,140,40,0)");
      c.fillStyle = g;
      c.beginPath(); c.arc(hx, 0, rc, 0, TAU); c.fill();
      c.fillStyle = "#FFB547";
      c.globalAlpha = 0.9 * heat;
      for (const [px, py, pr] of [[0.755, -0.62, 0.19], [0.755, 0.62, 0.19], [0.875, -0.36, 0.15], [0.875, 0.36, 0.15]]){
        c.beginPath(); c.arc(Lw * px, hh * py, hh * pr, 0, TAU); c.fill();
      }
      c.restore();
    }
    c.globalAlpha = 1;
  }

  drawMotes(m){
'''),

("consecration picture: the nova's glyph ring retired",
 '''    /* ---- Consecration: glyphs igniting outward across the floor ------------ */
    else if (u.w === "censer"){
      const ex = clamp(u.t / 0.40, 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 0.9, 0, 1);
      const R = u.radius * (1 - Math.pow(1 - ex, 2.2));
      const N = 12;
      for (let i = 0; i < N; i++){
        const a = (i / N) * TAU + u.t * 0.4;
        const rr = R * (0.55 + 0.45 * shellHash(51, i));
        const lit = clamp((R - rr) / 60, 0, 1);
        if (lit <= 0) continue;
        this._glyph(c, u.x + Math.cos(a) * rr, u.y + Math.sin(a) * rr,
                    13, u.t * 1.2 + i, "#C9A227", fade * lit * 0.9);
      }
      c.globalAlpha = 0.35 * fade * (1 - ex * 0.6);
      c.strokeStyle = "#C9A227"; c.lineWidth = 3;
      c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.stroke();
    }
''',
 '''    /* ---- Consecration's glyph ring was the NOVA's (glyphs igniting out to
       r 300 at the cast for the record's 1.6); retired with it (v78, v109
       stage 6). The holy ground is `drawConsecration`, off the fighter and
       the simulation's own discs, where the one ultFx slot cannot erase it;
       the cast's record now carries the CAST only and nothing draws from it. */
'''),

("consecration picture: the nova's smoke retired",
 '''    /* ---- Consecration: the censer swung, and smoke over holy ground -------- */
    else if (u.w === "censer"){
      const ex = clamp(u.t / 0.40, 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 0.9, 0, 1);
      c.save();
      c.globalCompositeOperation = "lighter";
      for (let arm = 0; arm < 4; arm++){
        c.globalAlpha = 0.5 * fade;
        c.strokeStyle = arm % 2 ? "#C9A227" : "#FFF6E2";
        c.lineWidth = 5 - arm * 0.8;
        c.beginPath();
        for (let j = 0; j <= 30; j++){
          const t2 = j / 30;
          /* ribbons of smoke thrown off a swung censer: an outward spiral,
             wide and slow, nothing like the tight vortex Dirge draws */
          const a = arm * TAU / 4 + t2 * 2.4 + u.t * 1.6;
          const r = u.radius * 0.92 * t2 * ex;
          const px = u.x + Math.cos(a) * r;
          const py = u.y + Math.sin(a) * r * 0.86;
          j ? c.lineTo(px, py) : c.moveTo(px, py);
        }
        c.stroke();
      }
      c.restore();
      for (let i = 0; i < 14; i++){               // sparks of incense
        const q = (u.t * 0.7 + shellHash(52, i)) % 1;
        const a = shellHash(53, i) * TAU;
        const r = u.radius * 0.8 * q;
        c.globalAlpha = (1 - q) * fade * 0.9;
        c.fillStyle = "#FFE9A8";
        c.beginPath();
        c.arc(u.x + Math.cos(a) * r, u.y + Math.sin(a) * r - q * 30,
              1.6 + (1 - q) * 2, 0, TAU);
        c.fill();
      }
    }
''',
 '''    /* ---- Consecration's smoke spiral and incense sparks were the NOVA's
       (thrown out to r 300 under `lighter`); retired with it (v78, v109
       stage 6). The cast is the hammer head lighting (`drawConsecrationTop`)
       and the incense rises off each disc (`drawConsecration`). */
'''),

('consecration picture: the charge rune',
 '''  /* CONSECRATION -- the censer swings, and the rings go out from where it is,
     not from the middle. */
  censer(c, t, cf, P){
    const sw = Math.sin(t * 1.7) * (0.16 + cf * 0.2);
    SG.path(c, [[0, -0.95], [Math.sin(sw) * 0.85, -0.95 + Math.cos(sw) * 0.72]], P.steel, 0.045, 0.7);
    const bx = Math.sin(sw) * 0.85, by = -0.95 + Math.cos(sw) * 0.72;
    SG.poly(c, [[bx - 0.26, by], [bx + 0.26, by], [bx + 0.17, by + 0.4], [bx - 0.17, by + 0.4]],
            P.core, 0.9);
    for (let i = 0; i < 3; i++){
      const u = (t * 0.6 + i / 3) % 1;
      SG.ring(c, bx, by + 0.2, 0.12 + u * 0.72, P.glow, 0.05, (1 - u) * (0.25 + cf * 0.6));
    }
  },
''',
 '''  /* CONSECRATION -- the censer swings over holy ground. The nova's rings
     went out with the nova (v78): a disc on the floor under it that fills
     with the charge, a coal in the censer (gold, not white), and incense
     rising off the disc. */
  censer(c, t, cf, P){
    c.save(); c.translate(0, 0.56); c.scale(1, 0.34);
    SG.disc(c, 0, 0, 0.9, "#FFE9A8", 0.12 + cf * 0.38);
    SG.ring(c, 0, 0, 0.9, "#FFD98A", 0.12, 0.3 + cf * 0.6);
    c.restore();
    const sw = Math.sin(t * 1.7) * (0.16 + cf * 0.2);
    const bx = Math.sin(sw) * 0.72, by = -0.95 + Math.cos(sw) * 0.62;
    SG.path(c, [[0, -0.95], [bx, by]], P.steel, 0.045, 0.7);
    SG.poly(c, [[bx - 0.24, by], [bx + 0.24, by], [bx + 0.16, by + 0.36], [bx - 0.16, by + 0.36]],
            P.core, 0.9);
    SG.disc(c, bx, by + 0.17, 0.075, "#FFB547", 0.35 + cf * 0.65);
    for (let i = 0; i < 4; i++){
      const u = (t * 0.5 + i / 4) % 1, x = (i - 1.5) * 0.34 + Math.sin(t * 1.3 + i * 2) * 0.05;
      SG.disc(c, x, 0.52 - u * 0.78, 0.05, "#FFE9A8", Math.sin(u * Math.PI) * (0.25 + cf * 0.6));
    }
  },
'''),

("consecration picture: the cast record's life",
 '''censer: 1.6,''',
 ''''''),

]

# STAGE 6'S NAMES, free on the base on identifier boundaries, and what its
# inserts may write: their own `cons*` fields, a picture record's clock, a
# tag's `taught`, the canvas and the synth's own nodes. Everything else is the
# simulation's.
S6_NAMES = ("tickConsecration", "drawConsecration", "drawConsecrationTop", "_consLive", "_consGeom", "_consFill",
            "_consHatch", "_consEdge", "_consMotes", "_consRim", "_consDrift", "consFade", "consAge", "consOut",
            "consEnd", "consPic", "consFoeOn", "consSelfOn", "consFoeLit", "consSelfLit", "consPulse", "consSeen",
            "consTagS", "consTagB", "censer-disc")
S6_WRITE_OK = (lambda obj, prop: prop.startswith("cons") or obj.startswith("cons") or obj == "c"
               or (obj, prop) in {("p", "age"), ("taught", "smite"), ("taught", "blessing"),
                                  ("frequency", "value")})
# THE TWO CALLS ON THE SIM PATH, whole (reading 16): each row's added code,
# comments stripped, line for line.
S6_SIM_LINES = {
    "resolveHit: the disc bell": ['{ const sd_ = self === this.a ? "a" : "b";', 'let n_ = 0;',
                                  'for (const d_ of this.holyGround) if (d_.side === sd_) n_++;',
                                  'SFX.play("ult", { w: "censer-disc", n: n_ }); }'],
    "tickHolyGround: the heal chime": ['SFX.play("spark", { collect: true, n: f.stacks("blessing") });'],
}
S6_SFX_ROW = "Sfx: Censer's cast"
S6_TICK_ROW = "consecration picture: tickConsecration"
RUNE_CRACK = "        } else {                                        // rune-crack"


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 18)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_array_ok(obj: str, ins: str) -> bool:
    """An array stage 6 may change: its own `cons*` ones, or a name its row
    binds once, as `const X = f.cons...;` (tickConsecration's P and S)."""
    if obj.startswith("cons"):
        return True
    bound = re.findall(r"\bconst " + re.escape(obj) + r" = \w+\.(cons\w+);", ins)
    decls = re.findall(r"\b(?:const|let|var)\s+" + re.escape(obj) + r"\b|[,(]\s*" + re.escape(obj)
                       + r"\s*=(?!=)|(?<![\w.$])" + re.escape(obj) + r"\s*=(?!=)", ins)
    return len(bound) == 1 and len(decls) == 1


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION. Its ADDED code (a row's re-emitted anchor
    aside) draws no RNG, never takes the one ultFx slot (open item 25), calls
    nothing that hurts, applies, resolves, beats, floats, rings or knocks,
    never writes the shared weapon row, writes only what S6_WRITE_OK names and
    mutates only its own arrays. Its two lines on the sim path are the two
    voice calls, whole, each in its own row; the synth's nodes only in the Sfx
    row; the tags and `taught` only in tickConsecration. The probe's [10]-[11]
    and engine_ab are the dynamic proof. Run on every stage: it reads the
    table."""
    for label, old, new in S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|"
                     r"tickHolyGround|tickStatus|tickStasis|tickWeapon|tickHits|spawnShot|note|checkEnd)\(", ins) \
                or re.search(r"(?<!SG)\.ring\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*\s*(=[^=]|\+=|-=|\*=|/=|\+\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        if re.search(r"\b(beat|hurt|knock|shake|hitStop)\b", ins):
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
                             "outside the disc's bell and the heal")
        if ("_tone(" in ins or "_burst(" in ins) and not label.startswith(S6_SFX_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if ("statusTag(" in ins or "taught" in ins) and not label.startswith(S6_TICK_ROW):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' tags or "
                             "teaches outside tickConsecration")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not S6_WRITE_OK(mw.group(1), mw.group(2)):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}.{mw.group(2)}")
        for mw in re.finditer(r"([\w\]\)]+)\.(push|splice|pop|shift|unshift|reverse|sort|copyWithin)\(", ins):
            if not s6_array_ok(mw.group(1), ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"mutates {mw.group(1)}")
        for mw in re.finditer(r"([\w\]\)]+)\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", ins):
            if not s6_array_ok(mw.group(1).split(".")[-1], ins):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' "
                                 f"writes {mw.group(1)}[...]")
        if re.search(r"\bdelete\s", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' deletes a property")


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched, the
    shared rune-crack fallback kept once and after Censer's arms, the nova's
    art gone, and every arm, call and pass wired exactly once."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 18)")
    if s.count(RUNE_CRACK) != 1 or s.find('} else if (w === "censer-disc"){') > s.find(RUNE_CRACK):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Censer's arms")
    for gone in ('u.w === "censer"', "censer: 1.6"):
        if gone in out_code:
            raise SystemExit(f"REFUSING TO WRITE -- the nova's art is still drawn ({gone!r})")
    for need in ["this.tickConsecration(dt);", "if (__world) this.drawConsecration(m);",
                 "this.drawConsecrationTop(m);", "  tickConsecration(dt){", "  drawConsecration(m){",
                 "  drawConsecrationTop(m){", "  censer(c, t, cf, P){",
                 '} else if (w === "censer"){', '} else if (w === "censer-disc"){']:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        ln = [x for x in v if x.startswith("SFX.play(")][0]
        if out_code.count(ln) != code.count(ln) + 1:
            raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    if "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n    this.tickConsecration(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickConsecration is not tickPresentation's second call")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes "
          "its own fields; the disc's bell and the heal chime its two lines on the sim path); "
          "the inlined fx.js untouched; the rune-crack fallback kept; the nova's art gone; every "
          "arm, call and pass once")


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


NEW_NAMES = ("ultHoly", "holyTally", "holyGround", "holyT", "tickHolyGround", 'kind:"holyground"',
             '"holyground"')
STAGE_OUT = {"1": "sc-censer-stub", "2": "sc-censer-ground", "3": "sc-censer-consecration"}

# What an insert may never do (the design's "no damage, no knock, no beat";
# the batch's rules). Checked on every insert with its comments stripped.
TABLES = r"(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES)"


def check_insert(label: str, ins: str) -> None:
    if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
        raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the RNG or uses "
                         "the one ultFx slot")
    if re.search(r"\bw\.(dmg|spin|reach|blades|mass|width|arc|artW|knockMul|ult|onHit|onSelf)"
                 r"\s*(?:[-+*/]?=(?!=)|\+\+|--)", ins) or \
            re.search(r"\bw\.ult\.\w+\s*(?:[-+*/]?=(?!=)|\+\+|--)", ins):
        raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the shared weapon")
    aliases = re.findall(r"\b(\w+)\s*=\s*" + TABLES + r"\b[\w.\[\]\"']*\s*[,;)]", ins)
    for nm in [TABLES] + [re.escape(x) for x in aliases]:
        if re.search(r"\b" + nm + r"\s*[.\[][\w.\[\]\"']*\s*(?:[-+*/%]?=(?!=)|\+\+|--)", ins) or \
                re.search(r"(?:\+\+|--)\s*" + nm + r"\s*[.\[]", ins) or \
                re.search(r"\bdelete\s+" + nm + r"\b", ins) or \
                re.search(r"\bObject\.(?:assign|defineProperty|defineProperties|setPrototypeOf)\(\s*"
                          + nm + r"\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes a shared module "
                             "table (STATUS / CONFIG / AFFINITIES / WEAPONS / SHAPES)")
    if "this.beat(" in ins or "hitStop" in ins or ".hurt(" in ins or "shatter(" in ins \
            or "resolveHit(" in ins or "knock" in ins.replace("knockMul", ""):
        raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' files a beat, a hit stop, "
                         "damage or a knock (the ground does none)")
    if re.search(r"\.(stun|stunDR|pin|pinV|pinMax|pinFree|burden|launch|hp|maxHp|shield|shieldMax"
                 r"|x|y|vx|vy|charge)\s*(?:[-+*/]?=(?!=)|\+\+|--)", ins):
        raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' moves, heals, stuns, pins, "
                         "burdens or charges a fighter directly")
    bad = [k for k in re.findall(r'\.apply\(\s*"(\w+)"', ins) if k not in ("smite", "blessing")]
    if bad or re.search(r"\.apply\(\s*[^\"\s]", ins):
        raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' lays a status other than "
                         f"smite and blessing: {bad}")


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
    if not out_p.name.startswith("sc-censer"):
        raise SystemExit(f"refusing {out_p.name}: this relic's links are named sc-censer*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: a link of that name is already "
                         "on the chain")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nCENSER / CONSECRATION (redesign) -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE IS ASSERTED BY CONTENT: the features this build needs, never
    # which relic is last.
    for need, why in (
            ("tickTendril(dt){", "no tickTendril -- the window tickers' anchor is missing"),
            ("this.tickTendril(dt);", "no tickTendril call to follow"),
            ("  tickWinnow(dt){", "no tickWinnow to precede"),
            ('if (u.kind === "tendril"){', "no tendril cast branch to precede"),
            ("this.vineTally = null;", "no vineTally field to follow"),
            ("this.sparks = [];", "no sparks list on the match to follow"),
            ("self.hits++; self.dealt += dmg;", "resolveHit's blow count has moved"),
            ("f.charge += dt;", "the charge is no longer pure live time"),
            ("if (src) cur.src = src;", "Fighter.apply no longer records its source"),
            ('if (key === "blessing"){', "tickStatus no longer heals by the blessing"),
    ):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    for st in STATUSES:
        if st not in code:
            raise SystemExit(f"wrong base: the status the lab priced has moved: {st!r}")
    # THE ORDER: every ball has moved, then the window tickers, then tickHits.
    i_col, i_tt = code.find("    this.ballCollision();"), code.find("    this.tickTendril(dt);")
    i_hits = code.find("this.tickHits(self, foe, dt);", i_tt)
    if not (0 <= i_col < i_tt < i_hits):
        raise SystemExit("wrong base: tickTendril does not sit between ballCollision "
                         "and tickHits")
    # THE BLOW COUNT IS resolveHit's, AND `mul` IS ITS SIXTH PARAMETER.
    if "resolveHit(self, foe, hx, hy, seg, mul, over){" not in code:
        raise SystemExit("wrong base: resolveHit's signature has moved")
    row = relic_row(code, RELIC)
    # Stage 6 goes on stage 5's link, whose row carries the blade BLADE names
    # in place of the shipped 28.77; the rest of the profile is asserted alike.
    phys = PHYS if A.stage != "6" else PHYS.replace("dmg:28.77,", f"dmg:{BLADE},")
    if phys not in " ".join(row.split()):
        raise SystemExit("Censer's warhammer profile has moved -- not the shipped relic "
                         "this builder redesigns")
    if "onHit:{ smite:1 }," not in row:
        raise SystemExit("Censer no longer carries onHit smite 1")
    # THE NOVA STAYS FOR THE OTHERS (what is retired is Censer's only). This
    # build touches none of the nova's code (the holyground branch returns
    # before the generic tail), so it needs no other relic to be a nova. It
    # READS who still is, and never refuses on it.
    novas = [nv for nv in re.findall(r'\{ id:"([a-z]+)", name:"', code)
             if nv != RELIC and 'kind:"nova"' in relic_row(code, nv)]
    print("  base  the window tickers' anchors, the blow count, the smite and blessing "
          "statuses; Censer's shipped profile; the nova's tail kept, untouched, for "
          + (", ".join(novas) if novas else "no other relic"))

    if A.stage == "1":
        if " ".join(strip_comments(OLD_ULT).split()) not in " ".join(row.split()):
            raise SystemExit("Censer's nova is not in this source -- stage 1 goes on the "
                             "shipped relic, once")
        for name in NEW_NAMES:
            if name in code:
                raise SystemExit(f"'{name}' is already in the base")
        edits, want = S1, ult_block("1e9", 0)
    else:
        if 'kind:"holyground"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if "ultHoly" in code:
                raise SystemExit("this source already carries stage 2 -- built")
            for name in ("holyTally", "holyGround", "holyT", "tickHolyGround"):
                if name in code:
                    raise SystemExit(f"'{name}' is already in the base")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if "ultHoly" not in code or "bless:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["bless"])
        elif A.stage == "5":
            if BLADE is None:
                raise SystemExit("stage 5: BLADE is not set -- the blade is measured first "
                                 "(v109 §4)")
            if f'bless:{ULT["bless"]},' not in row or "dmg:28.77," not in row:
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bless"])
        else:
            # STAGE 6 GOES ON STAGE 5, ONCE: the heal on, the blade BLADE names,
            # none of stage 6's names in the source yet (on identifier
            # boundaries), and what the picture and the voice read there.
            if (BLADE is None or f'bless:{ULT["bless"]},' not in row
                    or f"dmg:{BLADE}," not in row or "tickHolyGround(dt){" not in code):
                raise SystemExit("stage 6 goes on stage 5 (the heal, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if '} else if (w === "censer"){' in code:
                raise SystemExit("Censer's cast voice is already in this source -- stage 6 goes on once")
            for need, why in (("function shellHash(", "no shellHash (the incense's hash, never the RNG)"),
                              ("function hexA(", "no hexA (the foe's rim)"),
                              ("  statusTag(x, y, key, first, val){", "no statusTag (the tags)"),
                              ('SFX.play("ult", { w: f.w.id });', "fireUlt no longer voices the cast by id"),
                              ('SFX.play("spark", { collect: true, n: f.stacks("blessing") });',
                               "no spark collect voice to reuse")):
                if need not in code:
                    raise SystemExit(f"wrong base for stage 6: {why}")
            edits, want = S6, ult_block(ULT["charge"], ULT["bless"])
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Censer's ult block is not what this "
                         f"run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:110]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, old, new in S1 + S2 + S3 + S5 + S6:
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        check_insert(label, ins)
    s6_static_checks()
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    if len(re.findall(r'kind:"holyground"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- more than one holyground ultimate")
    if 'kind:"nova"' in relic_ult(out_code):
        raise SystemExit("REFUSING TO WRITE -- Censer still casts the nova")
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    if n_ids != len(re.findall(r'\{ id:"[a-z]+", name:"', code)):
        raise SystemExit("REFUSING TO WRITE -- the roster changed size (a redesign adds "
                         "no relic)")
    if A.stage != "1":
        # THE ORDER HOLDS ON THE OUTPUT: the ground ticks after every ball has
        # moved and before the hit loop.
        i_tt = out_code.find("    this.tickTendril(dt);")
        i_hg = out_code.find("    this.tickHolyGround(dt);")
        i_hits = out_code.find("this.tickHits(self, foe, dt);", i_tt)
        if not (0 <= i_tt < i_hg < i_hits):
            raise SystemExit("REFUSING TO WRITE -- tickHolyGround is not between the "
                             "window tickers and tickHits")
    print(f"  ok    one holyground ultimate, Censer's; the nova gone from its row; no insert "
          f"draws the RNG, writes the shared weapon or a shared table, beats, stops, hurts, "
          f"knocks, moves, heals directly, stuns, pins or lays a status but smite and "
          f"blessing; {n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
