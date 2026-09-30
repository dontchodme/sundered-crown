#!/usr/bin/env python
"""THORNWAKE / BRAMBLESNARE, REDESIGNED -- every blow leaves a bramble where it landed. v113.

Built from `06-docs/v84/thornwake-bramblesnare-redesign-v84.md` (Cowork,
2026-09-26), its §5 build brief and its runs (`06-docs/v84/runs/bramble_base*`,
`tools/overlays/bramble.js`), which are the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision. A REDESIGN: the relic
ships in the base; its ultimate, the 1.6s root (kind "freeze"), is replaced.

    stage 1   the new ultimate stubbed (1e9); the freeze out of the row
                                          <tip> -> sc-thornwake-stub.html     (= arm A)
    stage 2   the brambles: entangle + bite inside; the design's charge on the
              game's clock; the snare wired at rootFor 0
                                          -> sc-thornwake-bramble.html  (arm B; brief stage 1)
    stage 3   the snare on entry, rootFor 0 -> 0.6
                                          -> sc-thornwake-snare.html    (arm C; brief stage 2)
    stage 5   the blade (brief stage 3), 31.35 -> BLADE: the measured point
              whose win rate BOTH SIDES is nearest 50% -- RICK'S RULING,
              2026-09-29, after the design was written: "you pick the blades.
              do whatevers best for balance." It replaces the design's own
              target ("to the shipped rate", §5), which v113 §4 measures beside
              it.                         -> sc-thornwake-b<BLADE>.html THE FINAL LINK
    stage 6   the picture and the voice (brief stage 4), on stage 5's link,
              picked on the numbers under Rick's "you pick i overrule"
                                          -> sc-thornwake-b<BLADE>-fx.html

There is no stage 4: the brief has two mechanism stages, and the batch numbers
the blade 5 and the picture 6. THE CARRY is stages 1, 2, 3, 5 and 6.

§1: "For a duration every blow the scythe lands leaves a bramble on the floor
where it landed. An enemy that steps into a bramble is snared -- rooted for a
moment -- and while it stays in one it is entangled and bitten by the thorns."

Declared (§1, §4, the lab `overlays/bramble.js` at its defaults, which ARE the
settled numbers: patchR 80, patchLife 6, tickCd 0.5, tickDmg 2, rootFor 0.6):
  THE WINDOW   `dur` 8 on the window tickers' clock.
  A BRAMBLE    {x, y, t0, side} on the match (`m.brambles`, §5's
               "`m.brambles[]` in"), planted by every blow Thornwake lands
               while its window is open, at the struck ball's position; it
               lives `patchLife` (6s) of the window tickers' clock, outlives
               the window, and nothing else removes it ("the hall's close does
               not clip it").
  INSIDE       the foe alive and its centre within patchR + R of any of the
               caster's brambles (§4, the lab's `inside`).
  THE SNARE    on ENTRY -- inside now, not inside on the last tested frame --
               pin `rootFor` (0.6): Grasp's write, ball and weapon. Stage 3.
  THE FEED     inside with the thorns' cooldown clear: entangle +`tickEnt` (1)
               and hurt(foe, `tickDmg` (2), Thornwake), the cooldown `tickCd`
               (0.5). No knock, no hit stop, no beat (§4, Scour's rule).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE CHARGE is the design's on the game's clock (Rick's batch ruling: "use
     the game's equivalent"). The design names no charge in prose; its lab
     cast every 16s of its own step clock (`P.charge`, the harness default,
     `"charge": 16.0` in bramble_base.json), which counts hit-stop freezes.
     Measured for this fighter on the lab's arm C by counting frozen lab steps
     (v113 §0; 660 fights a block): 10.72% / 10.74% of the lab's steps are
     frozen (12.1% inside windows), so 16 x (1 - 0.1073) = 14.28 -> 14 (arm B:
     14.24). The shipped 15 was the freeze's engine charge and goes with it.
  2. THE WINDOW IS 8s (the lab's `P.dur`; §4: "a patch planted at 7.9s lives
     to 13.9s").
  3. THE LANDING POINT is the struck ball's centre at the hit (§1: "where it
     landed"; §4: "at the FOE's position on a landed blow"), taken in
     `resolveHit` beside `self.hits++` -- the count the lab watched (`me.hits`
     rising). The lab read the opponent after the step, the same point for
     every blow on the opponent (nothing moves a ball between `tickHits` and
     the step's end). A blow on one of Twinshade's shades plants at the
     shade, where it landed (Consecration's reading, v109); the lab planted at
     Twinshade. Two blows on one step (a shade and Twinshade) plant two
     brambles; the lab planted one. Only Twinshade's fights can differ.
  4. BRAMBLES OUTLIVE THE WINDOW AND ACT FOR THEIR WHOLE LIFE (§4, explicit,
     and the lab: its tests run while the window is open OR any patch
     lives). A bramble still alive at the next cast acts in that window too.
  5. BRAMBLES OUTLIVE THEIR PLANTER: the lab tests the foe against the
     patches with no check on the caster, so in a kill flight (the caster
     slain, the match held open while it flies) the brambles still bite. The
     prose does not say otherwise.
  6. ENTRY is the transition on the TESTED frames (the lab's `wasIn`): a
     frame is tested while the window is open or any of the caster's brambles
     lives, and `brambleIn` keeps the last tested frame's answer. A bramble
     planted under a foe that was in none on the last tested frame is an
     entry: the blow that plants it snares on the next frame the thorns are
     tested (the lab's reading; §4's "not inside last frame, inside now").
  7. THE SNARE is Grasp's write, the lab's `H.pin` to the letter: `pinV`
     captured iff the hold standing is not longer than `rootFor`; `pin` and
     `pinMax` max'd; `pinFree` NOT touched, so `tickStasis` locks the weapon
     ("ball and weapon", §4).
  8. THE THORNS' CADENCE is the lab's: one cooldown per caster, 0 at every
     cast, run down on every tested frame, inside or not; a tick on the first
     inside frame it is clear. Entangle first, then the bite (the lab's
     order). `apply`'s SOURCE IS A SIDE LETTER (Rick's ruling 4; the lab passed
     the Fighter; entangle has no reader of its source); `hurt`'s source stays
     the Fighter (a ward's shatter reads it).
  9. A TICK THAT KILLS files its own fatal hit beat (Rick's standing rule for
     a side-channel kill; §4's "no beat" is Scour's rule, whose fatal tick
     does file). No other tick files one, and nothing here sets a hit stop
     (a ward the bite breaks shatters inside `hurt`, as every ward does).
 10. THE WINDOW CLOSES on its clock or either death (the lab's). The
     brambles stay.
 11. NO CAST WAITS. The design asks none; the charge is unfrozen time and the
     window 8 on the same clock, so a cast cannot find a window open (the
     probe asserts it). Old brambles never hold a cast (the lab's).
 12. THE TARGET IS THE OPPONENT, never a Twinshade shade: the thorns test,
     snare and bite the opponent only (the lab's `foe`).
 13. NOTHING ELSE: the scythe swings as ever; the blow is the scythe's own.
 14. THE CARD is the design's own, 66 characters; the names are kept (§4).
 15. THE FREEZE IS OUT (brief stage 1 "freeze out"): Thornwake's row loses
     radius 260, dmg 10, apply entangle 3 and freeze 1.6. `kind:"freeze"` has
     no code of its own (no `u.kind === "freeze"` anywhere): the root was
     fireUlt's generic tail (`u.radius`, `u.dmg`, `u.apply`, `u.freeze`), and
     that tail STAYS -- Heartwood's Rootfast still casts through it on this
     base (it is being redesigned too, v112, and either may be carried first),
     and its damage and `apply` clauses serve other ult blocks. So nothing in
     the simulation is retired but the row.
 16. WHAT STAYED FOR STAGE 6 (the brief's stage 4), all presentation and read
     by nothing in the simulation: drawUltUnder's floor roots and drawUltOver's
     thorns keyed `u.w === "thornwake"` (the freeze's picture, which played at
     the cast through stage 5), `ULTSIG.thornwake` (the charge sigil), the
     `ultFx` life entry (2.4), fireUlt's `onTarget` entry (the banner on the
     quarry), the cast voice (`"thornwake"`, "creak and cinch") and
     `SPECS.thornwake` in both copies of fx.js. Stage 6 retires the first
     four's freeze-only parts (reading 20) and replaces the voice (reading 18);
     the charge sigil and the banner's letters keyed on the id stay (they are
     the relic's and its name's, not the freeze's); SPECS.thornwake is the
     orchestrator's `fx_remove` at the carry, never this builder (reading 21).

STAGE 6, THE PICTURE AND THE VOICE (v84 §4's picture and sound; §5's brief
stage 4, "picture, voice, carry"). Rows by the picture lab (scratch
`stage6-picture/tw_rows.py`, 12 rows) and `thornwake_voice_lab.py` (4 rows),
byte-exact to their files (the S6 table's header); v113 §5 carries every
number they were picked on.
 17. PRESENTATION ONLY. Nothing stage 6 adds is read by the simulation; the
     proof is engine_ab over every relic (Thornwake included) and the probe's
     [9]-[10], which read the voices and the picture's hook inside the fight.
 18. THE VOICE: four sounds, v84 §4's four ("cast -- a rustle-and-creak, 0.4s;
     a bramble opening -- a dry crackle; the snare -- a short creak and crack
     (Tendril's root voice, reused); a bite -- a soft snap"). The synth's arm
     keyed on this relic (the freeze's "creak and cinch", four lines) is
     REPLACED by four arms; the shared rune-crack fallback is not touched. The
     cast is fireUlt's own prologue voice (`w: f.w.id`), unchanged, so it
     sounds once a cast. The other three are one `SFX.play` each, after a
     count stage 2 already wrote: the crackle after `planted++` in
     plantBramble (once a bramble, on the landing blow's step); the snare
     after `T.snares++` (the step the pin is written; none at rootFor 0); the
     bite after the cooldown's re-arm (every bite, a killing one too, ahead of
     its entangle and hurt on the same step; the anchor is the re-arm and not
     `T.ticks++`, which a smite ticker repeats on the batch line's newer tips).
     THERE IS NO CLOSE VOICE (v84 names none; the brambles outlive the window)
     and none when a bramble expires. A ward the bite breaks plays its own
     crit hit voice inside hurt(), as every ward break does.
 19. THE SNARE'S VOICE IS TENDRIL'S ROOT, TRANSCRIBED: Tendril's root
     (`ult/bindweed-root`) is not on this base (it landed one link later, on
     sc-tendril-fx), so a reuse by id would fall through to rune-crack here.
     The arm `thornwake-snare` carries Tendril's arm body unchanged (the voice
     lab renders it equal to Tendril's own to 1.5e-07, and to the page's own
     `bindweed-root` on a tip that carries it). It does not follow a later
     re-voicing of Tendril's root.
 20. THE PICTURE is on the FIGHTER (`brier*`, never `bramble*`, the
     simulation's), never on `m.ultFx` (one slot the opponent's cast takes:
     open item 25), and driven in tickPresentation (`tickBrier`), which reads
     the simulation's own brambles (`m.brambles`) and watches the tally's
     snares and ticks rise: the blade greens for the window (drawWeapon); each
     bramble is a tangle of thorned canes on the floor (the world pass, under
     both balls, source-over: nothing the bloom sees) that grows out of the
     hit point over 0.3 s, browns over its last second and goes the step the
     simulation removes it; leaves lift off it; the snare's shoots rise out of
     the bramble and clench the held ball's rim for the pin (Tendril's root
     picture); a bite flashes four thorns on the foe's rim; the ENTANGLE tag
     counts (Tendril's rule). Paradox's hexagon is kept off a ball the snare
     holds (a return inserted before _drawField's guard: `brierHeld` is 1
     exactly while the snare's pin holds). The freeze's art is retired:
     drawUltUnder's floor roots, drawUltOver's thorns on the quarry, the
     cast record's life entry (2.4 -> the map's 1.5) and the banner's seat on
     the quarry (the cast is the caster's now).
 21. NO FIELD (fx_spec NONE). The redesign's picture has no particle field of
     its own: a SPECS field fires once, at the cast, where Thornwake stood,
     and no bramble exists then (the leaves lifting off each bramble are the
     design's field, drawn). `SPECS.thornwake` -- the FREEZE's frost ("A
     FREEZE HOLDS, so its frost settles slowly") -- is retired by the
     orchestrator's `fx_remove` at the carry, in both copies, never by this
     builder: stage 6 refuses if its edits touched the inlined fx.js.
 22. THE SCAN FOR STAGE 6 (`s6_static_checks`, `s6_output_checks`): no RNG,
     no ultFx, no call into the simulation, no write to the shared weapon row
     or a module table (seven exact reads), writes only `brier*` fields, the
     canvas and -- in tickBrier alone -- five bound things by exact line (a
     picture record's clock, a bite flash's clock, the seen counts, the
     ENTANGLE tag's count, the teaching flag); `SFX` only in the three voice
     rows, each whole; the synth only in the Sfx arms; the tags only in
     tickBrier; the retired rows nothing but comments; in the page, the old
     arm gone, the four arms before the rune-crack fallback, the three voice
     lines each once where it belongs, every call and method once, the
     inlined fx.js untouched and the Math.random count unmoved.

THE CLOCK. The window, the brambles' lives and the thorns' cooldown run on the
window tickers' clock, which stops through a hit stop (every batch build's
convention). The lab ran all three through freezes; v113 §2 measures what that
is worth here. The snare's own 0.6s is the engine's `tickStasis` clock, which
the lab shared.

THE ORDER. `tickBramble` runs with the window tickers, after `tickTendril`:
after every ball has moved this frame, before `tickHits`. A bramble planted by
a blow in `tickHits` is tested from the next live frame on (the lab tested it
after the step it was planted on, before the blow's hit stop).

THE SCAN (reading 13, made whole after the Spellbreaker review): every
insert's ADDED code (its re-emitted anchor taken out) draws no RNG, takes no
ultFx slot, writes no shared weapon and no pinFree, sets no hit stop, stuns
nothing, calls no simulation or presentation verb but the design's three (the
entangle, the bite, a killing tick's beat), deletes nothing, and writes only
WRITE_OK: the window, the thorns' two fields, the tally, the match's brambles
and their clock, and Grasp's three fields on the foe.

THE BASE is asserted BY CONTENT, never by which relic is last: Thornwake's row
with its shipped Bramblesnare, the engine gates the brambles pay through, and
every anchor below exactly once. Every insert goes AFTER or BEFORE a stable
line and re-emits it, so the builder re-applies on a later tip that carries
other new relics or other redesigns.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "thornwake"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9). v84 §1, §4, §5.
ULT = {
    "charge": 14,       # the lab's 16 on the game's clock (Rick's batch ruling; measured, v113 §0) -- reading 1
    "dur": 8,           # the lab's window, P.dur 8 -- reading 2
    "patchR": 80,       # §1/§4 "a patch r 80 at the hit point"
    "patchLife": 6,     # §4 "life 6s"
    "tickCd": 0.5,      # §4 "every 0.5s"
    "tickEnt": 1,       # §4 "entangle +1"
    "tickDmg": 2,       # §4 "hurt 2"
    "rootFor": 0.6,     # §4 "pin 0.6" -- stage 3
}
TIP = "Blows leave brambles: a foe in one is rooted, entangled and bitten"
SHIPPED_ULT = ('''    ult:{ name:"Bramblesnare", charge:15, kind:"freeze", radius:260, dmg:10, apply:{entangle:3}, freeze:1.6, tip:"Roots for 1.6 seconds, deals 10 damage and applies 3 Entangle stacks" },
''')
SHIPPED_DMG = "31.35"
ROW_HEAD = '''  { id:"thornwake", name:"Thornwake", aff:"verdant", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:'''
ROW_TAIL = ''', spin:3.2, mode:"spin", mass:2.4,
    onHit:{ entangle:2 },
'''


def ult_block(charge, root_for) -> str:
    return (f'''    ult:{{ name:"Bramblesnare", charge:{charge}, kind:"bramble", dur:{ULT["dur"]},
          patchR:{ULT["patchR"]}, patchLife:{ULT["patchLife"]}, tickCd:{ULT["tickCd"]}, tickEnt:{ULT["tickEnt"]}, tickDmg:{ULT["tickDmg"]},
          rootFor:{root_for},          // v84: the snare on entry (stage 3)
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
# `fireUlt` never runs for this relic), AND THE FREEZE OUT OF THE ROW. The row
# keeps every physical stat, the school's channel and the blurb; only the ult
# block changes. Nothing else reads the ult block's fields, so this link must
# be the lab's arm A (the relic with no ultimate) fight for fight.
S1 = [

("Bramblesnare becomes the brambles, stubbed; the freeze out of the row",
 SHIPPED_ULT,
 '''    /* BRAMBLESNARE, REDESIGNED (v84; built v113): EVERY BLOW LEAVES A
       BRAMBLE. The 1.6s root (radius 260, 10 damage, 3 entangle) is out of
       this row. For the window every blow the scythe lands plants a bramble
       where it landed (`plantBramble`); a foe that steps into one is snared
       `rootFor` seconds, and while it stays in one it is entangled and
       bitten (`tickBramble`). */
''' + ult_block("1e9", 0)),

]

# ---------------------------------------------------------------- stage 2 --
# THE BRAMBLES (brief stage 1: "freeze out, `m.brambles[]` in, the tests,
# entangle + bite"), the snare written but inert at rootFor 0, and the design's
# charge on the game's clock.
S2 = [

("the brambles have a charge: the lab's 16 on the game's clock",
 '''    ult:{ name:"Bramblesnare", charge:1e9, kind:"bramble", dur:8,
''',
 f'''    ult:{{ name:"Bramblesnare", charge:{ULT["charge"]}, kind:"bramble", dur:{ULT["dur"]},   // v84 stage 2: the brambles
'''),

("the fighter carries the window and the thorns",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur} while THORNWAKE's Bramblesnare window is open (v84). null on
       every other relic and on this one outside its window: `resolveHit`
       reads it once, beside `self.hits++`. `brambleCd` is the thorns'
       cooldown and `brambleIn` whether the foe was inside one of this
       fighter's brambles on the last frame the thorns were tested (the
       snare fires on ENTRY); both outlive the window, as the brambles do.
       `brambleTally` is the probe's count, cumulative over the fight;
       nothing in the simulation reads it. The brambles themselves are the
       match's (`m.brambles`). */
    this.ultBramble = null;
    this.brambleCd = 0;
    this.brambleIn = false;
    this.brambleTally = null;
'''),

("the match carries the brambles and their clock",
 '''    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed
''',
 '''    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed
    /* BRAMBLESNARE'S BRAMBLES (v84): SIM objects, {x, y, t0, side}, one a blow
       Thornwake lands in its window, at the struck ball. `brambleT` is their
       own clock, the window tickers' (advanced in `tickBramble`, so it stops
       in a hit stop); a bramble goes when `brambleT - t0` reaches its
       caster's `patchLife`, and nothing else removes one -- not the window's
       close, not the hall's. Empty in every match without Thornwake. */
    this.brambles = [];
    this.brambleT = 0;
'''),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "echo"){
''',
 '''    if (u.kind === "bramble"){
      /* BRAMBLESNARE (v84). NOTHING RESOLVES HERE: the cast opens the window
         for `u.dur` seconds; every blow the scythe lands inside it plants a
         bramble (`plantBramble`, from `resolveHit`), and `tickBramble` tests
         the foe against them. The thorns' cooldown starts clear, so a foe
         already standing in a bramble from the last window is bitten on the
         first frame. The freeze's one-shot -- the generic tail's damage,
         entangle and stun -- is out of this relic's row, and this branch
         returns before that tail. */
      f.ultBramble = { t: 0, dur: u.dur };
      f.brambleCd = 0;
      if (!f.brambleTally)
        f.brambleTally = { casts: 0, frames: 0, planted: 0, tested: 0, after: 0, foeIn: 0,
                           entries: 0, snares: 0, ticks: 0, dealt: 0, ent: 0, kills: 0 };
      f.brambleTally.casts++;
      return;
    }
    if (u.kind === "echo"){
'''),

("a blow inside the window plants a bramble where it landed",
 '''    self.hits++; self.dealt += dmg;
''',
 '''    self.hits++; self.dealt += dmg;
    /* BRAMBLESNARE (v84 §1, §4): "every blow the scythe lands leaves a bramble
       on the floor where it landed" -- at the struck ball, beside
       `self.hits++`, the count the lab watched. `ultBramble` is null on every
       other relic and outside the window, so this is one null test. */
    if (self.ultBramble && (self === this.a || self === this.b)) this.plantBramble(self, foe);
'''),

("the brambles tick with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickBramble(dt);               // BRAMBLESNARE (v84)
'''),

("tickBramble ages the brambles, snares on entry and bites inside; plantBramble plants",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================ BRAMBLESNARE =======
     v84 §1 / §4 / §5. On the window tickers' clock, so all of it freezes
     through a hit stop:
       THE CLOCK    `brambleT` advances; a bramble goes when it has lived its
                    caster's `patchLife`. Nothing else removes one.
       THE WINDOW   `dur` from the cast; closes on its clock or either death.
                    The brambles stay.
       THE TESTS    while the caster's window is open OR any of its brambles
                    lives: the thorns' cooldown runs down, and the foe is
                    INSIDE when alive with its centre within patchR + R of
                    one of them.
       THE SNARE    inside now and not on the last tested frame: pin
                    `rootFor` -- Grasp's write, `pinFree` untouched, so
                    `tickStasis` locks the weapon. Stage 3.
       THE FEED     inside with the cooldown clear: entangle +`tickEnt` (side
                    letter), then hurt(foe, `tickDmg`, the caster), the
                    cooldown `tickCd`. No knock, no hit stop, no beat -- but a
                    tick that kills files its own fatal hit beat.
     The target is the OPPONENT only. */
  tickBramble(dt){
    this.brambleT += dt;
    const G = this.brambles;
    for (let i = G.length - 1; i >= 0; i--){
      const b = G[i], o = b.side === "a" ? this.a : this.b;
      if (this.brambleT - b.t0 >= o.w.ult.patchLife) G.splice(i, 1);
    }
    for (const f of [this.a, this.b]){
      const foe = f === this.a ? this.b : this.a, side = f === this.a ? "a" : "b";
      const Z = f.ultBramble;
      if (Z){
        Z.t += dt;
        if (Z.t >= Z.dur || !f.alive || !foe.alive) f.ultBramble = null;
        else f.brambleTally.frames++;
      }
      let live = !!f.ultBramble;
      if (!live) for (const b of G) if (b.side === side){ live = true; break; }
      if (!live) continue;
      const u = f.w.ult, T = f.brambleTally, R = CONFIG.physics.ballR;
      T.tested++;
      if (!f.ultBramble) T.after++;
      f.brambleCd -= dt;
      let inside = false;
      if (foe.alive)
        for (const b of G)
          if (b.side === side && Math.hypot(foe.x - b.x, foe.y - b.y) < u.patchR + R){ inside = true; break; }
      if (inside){
        T.foeIn++;
        if (!f.brambleIn){
          T.entries++;
          if (u.rootFor > 0){
            if (!(foe.pin > u.rootFor)) foe.pinV = [foe.vx, foe.vy];
            foe.pin = Math.max(foe.pin, u.rootFor);
            foe.pinMax = Math.max(foe.pinMax, u.rootFor);
            T.snares++;
          }
        }
        if (f.brambleCd <= 0){
          f.brambleCd = u.tickCd;
          foe.apply("entangle", u.tickEnt, side);
          T.ent += u.tickEnt;
          const wasUp = foe.hp > 0, before = foe.hp + foe.shield;
          this.hurt(foe, u.tickDmg, f);
          T.ticks++;
          T.dealt += before - (foe.hp + foe.shield);
          if (wasUp && foe.hp <= 0){
            T.kills++;
            this.beat({ kind: "hit", side: f === this.a ? 0 : 1,
                        x: foe.x, y: foe.y, dmg: u.tickDmg, crit: false,
                        fatal: true, hpAfter: 0, hpFrac: 0, maxHp: foe.maxHp,
                        selfHpFrac: f.hp / f.maxHp, spd: f.speed, foeSpd: foe.speed,
                        close: Math.hypot(f.vx - foe.vx, f.vy - foe.vy),
                        ranged: false, range: 0, loosT: 0, lx: 0, ly: 0,
                        shotSpd0: 0, bramble: true });
          }
        }
      }
      f.brambleIn = inside;
    }
  }

  /* A BLOW LANDED INSIDE THE WINDOW, called from `resolveHit` beside
     `self.hits++`: a bramble at the struck ball's centre (a blow on one of
     Twinshade's shades plants at the shade, where it landed), stamped on
     the brambles' own clock, carrying its caster's side. */
  plantBramble(f, q){
    this.brambles.push({ x: q.x, y: q.y, t0: this.brambleT, side: f === this.a ? "a" : "b" });
    f.brambleTally.planted++;
  }

  tickWinnow(dt){
'''),

]

# ---------------------------------------------------------------- stage 3 --
S3 = [
("the snare on entry",
 '''          rootFor:0,          // v84: the snare on entry (stage 3)
''',
 f'''          rootFor:{ULT["rootFor"]},          // v84: the snare on entry (stage 3)
'''),
]

# ---------------------------------------------------------------- stage 5 --
# THE BLADE: THE MEASURED POINT NEAREST 50% BOTH SIDES (Rick, 2026-09-29: "you
# pick the blades. do whatevers best for balance."). The design's brief stage
# 3 was "the blade, wide on 151 at 28 / 29 / 30 to the shipped rate"; the
# ruling settles it at 50 for every redesign. The design gives the build no
# knob to move before the blade (§6.3's bramble life is a design line, Rick's),
# so none moved. Both sides (relic_rate: every other relic a foe, 10 seeds a
# foe a side, 740 fights a block), seed0 2207 + 2317, 1480 fights a point,
# charge 14, on stage 3's link with `--set dmg=` (v113 §4), a fixed grid read
# after, no bisection:
#   24 -> 42.2   24.5 -> 43.9   25 -> 45.5   25.5 -> 47.5   26 -> 48.6
#   26.5 -> 50.9   27 -> 52.3   27.5 -> 52.9   28 -> 55.3   29 -> 57.9
#   30 -> 60.8
#   31.35 -> 63.4 (stage 3's link itself, the shipped blade)
# 26.5 is the measured point nearest 50% (753 of 1480, +13 wins from half; 26
# is -20). The crossing is ~26.3 -- under the brief's "28 / 29 / 30", which
# was aimed at the shipped rate from a 59.7 priced on Chromium 141 (arm C reads
# 63.8 on 151). The design names no knob to move first, and 26.5 is inside the
# scythe row (9.5-31.35, §3). The design's own target, the shipped rate (the
# freeze on this base: 47.8%, 708 of 1480), is nearest at 25.5 (47.5%, -5
# wins); v113 §4 prints it beside the final.
BLADE = "26.5"


def s5_edits(blade: str) -> list:
    return [
        ("the blade: the measured point nearest 50% both sides (Rick's ruling)",
         ROW_HEAD + SHIPPED_DMG + ",",
         ROW_HEAD + blade + ","),
    ]


# THE CARRY'S BLADE AS A MODULE-LEVEL TABLE, so `tools/chain_audit.py` (which
# reads module-level `(label, old, new)` tables) watches the blade like every
# other insert.
S5 = s5_edits(BLADE) if BLADE else []


# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v84 §4's picture and sound; its §5 brief stage 4,
# "picture, voice"), picked on measurements under Rick's "you pick i overrule"
# by the picture lab (scratch, `tw_rows.py`) and `thornwake_voice_lab.py` (v113
# §5). PRESENTATION ONLY: engine_ab over all 38 relics, Thornwake included, is
# the proof, and the probe's [9]-[10] read the voices and the picture's hook
# inside the fight. The rows are byte-exact to the labs' own files (voice
# a539532139eb01b7, 4 rows; picture f80fbfe244abacde, 12 rows); the picture rows
# alone reproduce the picture lab's stamp (65a84cedda239548), the voice rows
# alone the voice lab's end-to-end page (8f8d06e90d66fc3f), and the two sets
# give the same bytes in either order (d306822d6914c08c). No two rows share an
# anchor line, so none is merged.
#   THE VOICE: the synth's arm keyed on this relic, the freeze's "creak and
#   cinch", REPLACED by four arms -- the cast (NEEDLES), a bramble opening
#   (KNOTS), the snare (Tendril's root, transcribed) and a bite (STEM); the
#   shared rune-crack fallback is not touched. Three lines on the sim path,
#   each one SFX.play after a count stage 2 already wrote: the crackle after
#   `planted++` in plantBramble, the snare after `T.snares++` and the bite after
#   the cooldown's re-arm in tickBramble. The cast is fireUlt's own prologue
#   voice (`w: f.w.id`), unchanged. There is no close voice.
#   THE PICTURE: `tickBrier` in tickPresentation (the blade's green, a picture
#   record a bramble, the snare's shoots on the held ball, the bite flashes and
#   the ENTANGLE tag); the brambles in the world pass under both balls; the
#   clench and the bite flash over both fighters; the blade greening in
#   drawWeapon; the hexagon kept off a snared ball in _drawField; the freeze's
#   art retired (drawUltUnder's roots, drawUltOver's thorns, the life entry
#   2.4 and the banner's seat on the quarry).
# COMPOSITION: eleven anchors are re-emitted and five replaced: the synth's own
# arm (four lines), the freeze's two drawUlt branches, and the narrowest
# tokens of the life map (`thornwake: 2.4, `) and the onTarget map
# (`thornwake:1, `), which leave the other entries on those lines to their
# own builds. The rows ride on four of stage 2's own lines (the fighter's
# fields, plantBramble's count, the snare's count, the cooldown's re-arm) and
# on shared lines other stage 6s use as `after` / `before` anchors
# (tickPresentation's first call, the world pass's drawTree and drawTreeTop,
# drawWeapon's ultDraw, _drawField's guard, drawMotes, tickWinnow).
S6 = [

("Sfx: Bramblesnare's cast, crackle, snare and bite arms, replacing the freeze's creak and cinch",
 '''        } else if (w === "thornwake"){                  // creak and cinch
          this._burst(t, { freq: 700, q: 3.0, gain: 0.24, dur: 0.6 });
          this._tone (t, { freq: 150, to: 420, gain: 0.16, dur: 0.55, type:"triangle" });
          this._tone (t + 0.34, { freq: 300, to: 120, gain: 0.14, dur: 0.3, type:"square" });''',
 '''        } else if (w === "thornwake"){                  // the thorns wake
          /* BRAMBLESNARE'S CAST -- v84 s4: "cast -- a rustle-and-creak, 0.4s".
             NEEDLES, of 8, picked on the numbers by `thornwake_voice_lab.py`
             under Rick's "you pick i overrule" (v113). It REPLACES the
             freeze's "creak and cinch" -- the three lines that were this arm
             -- which the redesign retires with the freeze (v84 s5); nothing
             else in the synth moved.

             Needles: narrow bandpass grains (Q 8) ~60 a second, 30 ms each,
             their centres wandering 2310-3900 Hz, swelling to the middle and
             falling away; under them a 330 Hz timber (a sine and its 2.76 mode
             at 0.4) pulsed slowing 45 -> 28 a second, each interval x (1 +
             0.12 sin 2.4k) -- a bough bending (a held note does not exist in
             this toolkit, and a creak is stick-slip). The rustle is noise (no
             peak over 7.0 dB), centred at 3215-3752 Hz on every noise draw and
             not struck (its loudest millisecond 117 ms in); the creak is
             stick-slip, 37 pulses a second (PULSED 0.74), -2.9 dB re the
             rustle, and each owns a third-octave (the rustle +37 dB, the creak
             +40 dB over the other). Audible 395 ms; its loudest 50 ms -3.1 dB
             re Thornwake's blow. Register at most 0.77 (Scour's woosh) against
             rune-crack, the verdant and scythe casts (Tendril's among them),
             the house's voices, the blow, the death voice and the snare. */
          const g = 2.768, kc = 0.07398;
          for (let s = 0, k = 0; s < 0.39; k++){
            const u = s / 0.42, a = g * (0.3 + 0.7 * Math.sin(Math.PI * Math.min(1, u / 0.9)));
            this._burst(t + s, { freq: 3000 * Math.pow(1.3, Math.sin(k * 1.7)), q: 8, gain: a, dur: 0.03, type:"bandpass" });
            s += 0.016 * (1 + 0.4 * Math.sin(k * 2.4));
          }
          for (let s = 0.02, k = 0; s < 0.39; k++){
            const u = s / 0.42, a = g * kc * (0.6 + 0.4 * Math.sin(Math.PI * u));
            this._tone(t + s, { freq: 330, gain: a, dur: 0.03, type:"sine" });
            this._tone(t + s, { freq: 911, gain: a * 0.4, dur: 0.02, type:"sine" });
            s += 0.022 * Math.pow(1.6, u) * (1 + 0.12 * Math.sin(k * 2.4));
          }
        } else if (w === "thornwake-crackle"){          // a bramble opens
          /* A BRAMBLE OPENS -- "a bramble opening -- a dry crackle" (v84 s4).
             KNOTS, of 6 (`thornwake_voice_lab.py`). `plantBramble` plays it
             once per bramble, on the landing blow's frame.

             8 ms narrow bandpass clicks (Q 6) ~33 a second at centres
             wandering 1185-2160 Hz -- knots in dry wood -- each interval x (1
             + 0.45 sin 2.4k), thinning as it goes. 10 clicks or more at
             irregular intervals (their spacing varies 0.30 of its mean), 21 dB
             deep; dry -- 0.022 of its power below 500 Hz and no ring (no peak
             over 2.3 dB). Audible 280 ms, the bramble's 0.3 s growth; its
             loudest 50 ms -11.1 dB re the blow it lands with, heard +17.6 dB
             over the score after the blow's body. Register at most 0.73
             (Scour's tick) against the blow, the wall tick, rune-crack, fork,
             hex-snap, the vine's plant, the spark's burn, Scour's tick,
             Tendril's bite and wither, the cast, the bite and the snare. */
          const g = 4.348;
          for (let s = 0, k = 0; s < 0.295; k++){
            const u = s / 0.295, a = g * (1 - 0.4 * u);
            this._burst(t + s, { freq: 1600 * Math.pow(1.35, Math.sin(k * 1.9)), q: 6, gain: a, dur: 0.008, type:"bandpass" });
            s += 0.03 * (1 + 0.45 * Math.sin(k * 2.4));
          }
        } else if (w === "thornwake-snare"){            // and the foe is snared
          /* THE SNARE -- "the snare -- a short creak and crack (Tendril's root
             voice, reused)" (v84 s4). Tendril's root (`ult/bindweed-root`,
             v101 DEEP) is not on the link this was built on, so this arm is
             made here: its body is that arm's nine lines, transcribed
             unchanged (`thornwake_voice_lab.py` renders it equal to Tendril's
             own to 1e-07). `tickBramble` plays it on the frame the pin is
             written.

             Canopy's timber an octave and a half down (a 260 Hz sine and its
             2.76 mode at 0.4) pulsed for 0.2 s, then a highpass crack over a
             sine falling 60 -> 30 Hz: audible 370 ms, its loudest 50 ms -2.5
             dB re Thornwake's blow, 0.50 of its power below 120 Hz. */
          const g = 0.5179, kc = 0.2683, kt = 0.3464;
          for (let s = 0, k = 0; s < 0.188; k++){
            const u = s / 0.2, a = g * kc * (0.45 + 0.55 * u);
            this._tone(t + s, { freq: 260, gain: a, dur: 0.03, type:"sine" });
            this._tone(t + s, { freq: 718, gain: a * 0.4, dur: 0.02, type:"sine" });
            s += 0.03 * Math.pow(0.6, u) * (1 + 0.12 * Math.sin(k * 2.4));
          }
          this._burst(t + 0.2, { freq: 2600, q: 0.8, gain: g * 0.8, dur: 0.035, type:"highpass" });
          this._tone (t + 0.2, { freq: 60, to: 30, gain: g * kt, dur: 0.3, type:"sine" });
        } else if (w === "thornwake-bite"){             // and bitten
          /* A BITE -- "a bite -- a soft snap" (v84 s4). STEM, of 4
             (`thornwake_voice_lab.py`). `tickBramble` plays it once per bite
             (every 0.5 s of unfrozen time in a bramble), a killing bite too.

             A 10 ms bandpass snap at 1.1 kHz over a sine falling 620 -> 420
             Hz. Struck (rise 1 ms, one snap), audible 65 ms; soft -- its
             loudest 50 ms -11.0 dB re the blow and +11.0 dB re the wall tick,
             the snap's first 10 ms centred at 678 Hz at most. Register at most
             0.39 (fork) against the blow, the wall, fork, hex-snap, the vine's
             plant, Tendril's bite, rune-crack, the cast and the snare. */
          const g = 0.1462, D = 0.1056;
          this._burst(t, { freq: 1100, q: 1.2, gain: g, dur: 0.01, type:"bandpass" });
          this._tone(t, { freq: 620, to: 420, gain: g * 0.6, dur: D, type:"sine" });'''),

('plantBramble: the crackle, once per bramble planted, after the count',
 '''    f.brambleTally.planted++;''',
 '''    f.brambleTally.planted++;
    /* BRAMBLESNARE'S CRACKLE (v84 s4 SOUND: "a bramble opening -- a dry
       crackle"): once per bramble planted, on the landing blow's own frame,
       after the count. Presentation only: SFX.play draws nothing, is a no-op
       headless, and nothing here is read back (thornwake_voice_lab: fights
       identical). */
    SFX.play("ult", { w: "thornwake-crackle" });'''),

("tickBramble: the snare's voice (Tendril's root), on the frame the pin is written",
 '''            T.snares++;''',
 '''            T.snares++;
            /* BRAMBLESNARE'S SNARE (v84 s4 SOUND: "the snare -- a short creak
               and crack (Tendril's root voice, reused)"): on the frame the pin
               is written -- the foe stepping into a bramble -- after the count.
               Plain SFX.play; nothing is read back. */
            SFX.play("ult", { w: "thornwake-snare" });'''),

("tickBramble: the bite's soft snap, once per bite, as the thorns' cooldown is re-armed",
 '''          f.brambleCd = u.tickCd;''',
 '''          f.brambleCd = u.tickCd;
          /* BRAMBLESNARE'S BITE (v84 s4 SOUND: "a bite -- a soft snap"): one
             snap per bite, on the bite's own step, as the thorns' cooldown is
             re-armed -- the line every bite starts with -- ahead of its
             entangle and its hurt on the same step. A killing bite snaps too
             (the number of snaps is the number of bites); its fatal beat is
             the sim's, below. Presentation only: SFX.play draws nothing, is a
             no-op headless, and nothing here is read back
             (thornwake_voice_lab: fights identical). */
          SFX.play("ult", { w: "thornwake-bite" });'''),

('brier picture: fighter fields',
 '''    this.ultBramble = null;
    this.brambleCd = 0;
    this.brambleIn = false;
    this.brambleTally = null;
''',
 '''    this.ultBramble = null;
    this.brambleCd = 0;
    this.brambleIn = false;
    this.brambleTally = null;
    /* BRAMBLESNARE'S PICTURE (v84 section 4), and none of it is the window:
       the blade's green fades 0.3s past `ultBramble`, a bramble outlives the
       window and grows on a clock that runs through the hit stop of the blow
       that planted it, and the snare's shoots outlive the pin, so the picture
       keeps its own state. On the FIGHTER and never on `m.ultFx` (one slot,
       and the opponent's cast takes it: open item 25). Driven in
       `tickPresentation` (`tickBrier`); nothing in the simulation reads any
       of it. `brier`, not `bramble` (the simulation's own names).
         brierGreen -- the blade's green: 1 while the window is open; eased
                       to 0 over the close
         brierAge   -- the presentation clock since the cast (the greening)
         brierOut   -- the presentation clock since the close
         brierEnd   -- the presentation clock since the verdict (they go)
         brierPic   -- this caster's brambles as the picture knows them:
                       {b, age, g}, `b` the simulation's own bramble (read,
                       never written), `age` the presentation clock since it
                       was planted, `g` its canes (placed once, by shellHash)
         brierSeen  -- `brambleTally`'s snares and ticks as last seen
         brierTagN, brierTagT -- the count the bramble's ENTANGLE tag last
                       printed, and how long that tag is still up
         brierBite  -- the bite flashes on the foe's rim {a, t}
       and ON THE HELD BALL, the snare's quarry:
         brierHeld  -- 1 exactly while a Bramblesnare snare's pin holds this
                       ball. Its one reader outside this picture is
                       `_drawField`, which leaves Paradox's hexagon off it
                       (the shoots are its picture); `pinFree` is not
                       touched, so the weapon stays locked
         brierRootFade, brierHeldAge, brierHeldOut -- the shoots' own fade,
                       the clock since the snare, and since the hold let go */
    this.brierGreen = 0;
    this.brierAge = 0;
    this.brierOut = 0;
    this.brierEnd = 0;
    this.brierPic = [];
    this.brierSeen = [0, 0];
    this.brierTagN = 0;
    this.brierTagT = 0;
    this.brierBite = [];
    this.brierHeld = 0;
    this.brierRootFade = 0;
    this.brierHeldAge = 0;
    this.brierHeldOut = 0;
'''),

('brier picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickBrier(dt);                 // BRAMBLESNARE'S PICTURE (v84 section 4)
'''),

('brier picture: tickBrier and the canes',
 '''  tickWinnow(dt){
''',
 '''  /* ------------------------------------------- BRAMBLESNARE'S PICTURE ---
     v84 section 4, on the presentation clock. HALF-SECONDS, like every `life`
     in `tickPresentation` (it runs twice a normal step): 0.5 is the blade's
     0.25s greening at the cast, 0.6 its 0.3s fade at the close, 0.6 a
     bramble's 0.3s growth, 0.6 the brambles' 0.3s fade after the kill, 0.24 + 0.2
     the snare's shoots growing and clenching (0.12s + 0.1s), 0.4 their wilt
     after the hold (0.2s), 0.24 a bite's thorn flash (0.12s). The window is
     `ultBramble`, and not once the caster falls or the match ends:
     `tickBramble` never runs again once `over` is set, so a window open at
     the kill would otherwise stay green through the verdict. THE BRAMBLES are
     the simulation's own (`m.brambles`, read, never written): each gets a
     picture record the frame it exists -- its canes placed once, by
     shellHash on its own planting step and position -- and loses it the
     frame the simulation removes it. THE SNARE, THE BITES AND THE TAG are
     found by watching `brambleTally.snares` and `.ticks` rise, so
     `tickBramble` makes no call for the picture. THE TAG RULE (Tendril's): a
     bite whose count is not the one last printed tags ENTANGLE and the count
     on the foe, one tag up at a time, none while the count sits at its cap;
     and one ENTANGLE tag on the foe at a time -- a tag already up there (the
     scythe's own blow tags it) takes the count instead. Writes presentation
     fields, `tags` and `taught` only, and draws no rng. */
  tickBrier(dt){
    const G = this.brambles, R = CONFIG.physics.ballR;
    for (const f of [this.a, this.b]){
      /* THE HELD BALL (this fighter as a snare's quarry): `brierHeld` is 1
         exactly while the snare's pin holds -- frozen with it through the
         verdict -- and `brierRootFade` is the shoots' own tail. */
      if (f.brierHeld && !(f.pin > 0 && f.alive)) f.brierHeld = 0;
      if (f.brierRootFade > 0){
        if (!f.alive) f.brierRootFade = 0;
        else if (f.brierHeld && !this.over) f.brierHeldAge += dt;
        else {
          f.brierHeldOut += dt;
          f.brierRootFade = Math.max(0, 1 - f.brierHeldOut / 0.4);
        }
      }
      const T = f.brambleTally;
      if (!T && !(f.brierGreen > 0) && !f.brierPic.length) continue;   // <- zero burden
      const foe = f === this.a ? this.b : this.a, side = f === this.a ? "a" : "b";
      const Z = (this.over || !f.alive) ? null : f.ultBramble;
      if (Z){
        if (!(f.brierGreen > 0) || f.brierOut > 0){ f.brierAge = 0; f.brierOut = 0; }   // a cast
        f.brierGreen = 1;
        f.brierAge += dt;
      } else if (f.brierGreen > 0){
        f.brierOut += dt;
        f.brierGreen = Math.max(0, 1 - f.brierOut / 0.6);
      }
      const P = f.brierPic;
      for (let i = P.length - 1; i >= 0; i--) if (G.indexOf(P[i].b) < 0) P.splice(i, 1);
      for (const b of G)
        if (b.side === side && !P.some(p => p.b === b)) P.push({ b, age: 0, g: this._brierCanes(f, b) });
      for (const p of P) p.age += dt;
      if (this.over) f.brierEnd += dt;
      for (let i = f.brierBite.length - 1; i >= 0; i--){
        f.brierBite[i].t += dt;
        if (f.brierBite[i].t >= 0.24) f.brierBite.splice(i, 1);
      }
      if (f.brierTagT > 0) f.brierTagT -= dt;
      if (!T) continue;
      const S = f.brierSeen, dS = T.snares - S[0], dK = T.ticks - S[1];
      S[0] = T.snares; S[1] = T.ticks;
      /* THE SNARE: the thorns' test pinned the foe this step, and the
         tally's count is how this knows. */
      if (dS > 0 && foe.alive && foe.pin > 0 && !foe.pinFree){
        if (!foe.brierHeld) foe.brierHeldAge = 0;
        foe.brierHeld = 1; foe.brierRootFade = 1; foe.brierHeldOut = 0;
      }
      if (!(dK > 0) || !foe.alive) continue;
      /* THE BITE: four thorns flash out of the foe's rim on the side of the
         bramble it stands in (underneath when it stands on the centre) */
      let q = null, qd = 1e9;
      for (const b of G){
        if (b.side !== side) continue;
        const d = Math.hypot(b.x - foe.x, b.y - foe.y);
        if (d < qd){ qd = d; q = b; }
      }
      f.brierBite.push({ a: q && qd > 4 ? Math.atan2(q.y - foe.y, q.x - foe.x) : Math.PI / 2, t: 0 });
      if (!(foe.hp > 0)) continue;
      const n = foe.stacks("entangle");
      const g = this.tags.find(g2 => g2.key === "entangle" && g2.life > 0.3
                                     && Math.hypot(g2.x - foe.x, g2.y - foe.y) < R * 3);
      if (g){ if (!g.first) g.val = n; }
      else if (n !== f.brierTagN && !(f.brierTagT > 0)){
        f.brierTagN = n; f.brierTagT = 1.8;
        const first = !this.taught.entangle && !!STATUS.entangle.tip;
        if (first) this.taught.entangle = true;
        this.statusTag(foe.x, foe.y, "entangle", first, n);
      }
    }
  }
  /* ONE BRAMBLE'S CANES, placed once when it first exists: 7 long canes
     arching through it -- each starts within half its radius of the hit
     point, sets off outward and bends, one way or the other, until it
     reaches the edge -- and a short offshoot off each, with thorns along
     them all: canes that cross each other, a tangle and not a wheel. By
     shellHash on the bramble's own planting step and position, so a
     bramble is the same tangle for its whole life and no rng is drawn.
     Points are relative to its centre. */
  _brierCanes(f, b){
    const Rp = f.w.ult.patchR, sd = 7300 + ((Math.round(b.t0 * 120) * 13
               + Math.round(b.x) * 7 + Math.round(b.y) * 3) % 4093 + 4093) % 4093;
    const H = (i, j) => shellHash(sd + j, i);
    const canes = [], thorns = [], lim = Rp * 0.97;
    const grow = (x, y, h, turn, n, st, id) => {
      const pts = [[x, y]];
      for (let j = 0; j < n; j++){
        h += turn * (0.7 + 0.6 * H(id * 16 + j, 9));
        const nx = x + Math.cos(h) * st, ny = y + Math.sin(h) * st;
        if (Math.hypot(nx, ny) > lim) break;
        x = nx; y = ny; pts.push([x, y]);
        if (j % 2 === 1){
          const tx = Math.cos(h), ty = Math.sin(h), sg = (j >> 1) % 2 ? 1 : -1;
          thorns.push([x, y, tx, ty, sg]);
        }
      }
      if (pts.length > 1) canes.push(pts);
      return pts;
    };
    for (let i = 0; i < 7; i++){
      const a = TAU * (i + H(i, 0)) / 7, r0 = Rp * 0.5 * Math.sqrt(H(i, 1));
      const x0 = Math.cos(a) * r0, y0 = Math.sin(a) * r0;
      const h0 = a + (H(i, 2) - 0.5) * 2.2, turn = (H(i, 3) < 0.5 ? -1 : 1) * (0.07 + 0.1 * H(i, 4));
      const pts = grow(x0, y0, h0, turn, 16, Rp * 0.085, i);
      if (pts.length > 5){
        const q = pts[2 + Math.floor(H(i, 5) * (pts.length - 4))];
        grow(q[0], q[1], h0 + (H(i, 6) < 0.5 ? -1.1 : 1.1), -turn * 1.3, 6, Rp * 0.07, i + 40);
      }
    }
    return { canes, thorns, sd };
  }

  tickWinnow(dt){
'''),

('brier picture: the floor call (world, under both balls)',
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* BRAMBLESNARE'S BRAMBLES (v84 section 4): the thorn tangles on the floor,
       the leaves lifting off them, and the snare's stalks rising out of the
       bramble under a held ball. FLOOR: the WORLD pass, under both balls,
       source-over -- nothing of it reaches the bloom (CLAUDE.md 4.1c) and no
       ball's disc can be painted over (4.1b). */
    if (__world) this.drawBrier(m);
'''),

('brier picture: over both fighters (world)',
 '''    this.drawTreeTop(m);
''',
 '''    this.drawTreeTop(m);
    /* BRAMBLESNARE OVER BOTH FIGHTERS: the snare's shoots clenched round the
       held ball's rim and a bite's thorn flash on the foe's rim. World pass,
       source-over (Tendril's picture), so no shell is lit away. */
    this.drawBrierTop(m);
'''),

('brier picture: the blade greens (drawWeapon)',
 '''      if (f.ultDraw){
''',
 '''      /* BRAMBLESNARE (v84 section 4): "the scythe's blade greens for the
         window" -- drawn here, in the blade's own frame, so it rides the
         blade and the foe's shell clips it as it clips the blade.
         `brierGreen` is 0 on every other relic. */
      if (f.brierGreen > 0 && f.w.shape === "scythe") this._brierBlade(c, f, reach + 6, dim * wk);
      if (f.ultDraw){
'''),

('brier picture: the hexagon off a snared ball',
 '''    if (f.pin > 0 && !f.pinFree''',
 '''    /* AND NOT ON A BALL BRAMBLESNARE'S SNARE HOLDS (v84 section 4: its
       picture is "four thorn shoots up the foe's rim for the pin's length",
       `_brierRoot`). `brierHeld` is presentation state, 1 exactly while the
       snare's pin holds; `pinFree` stays 0, so the weapon is locked. The
       hexagon is this method's last block, so this returns past it alone. */
    if (f.brierHeld > 0 && f.pin > 0 && !f.pinFree) return;
    if (f.pin > 0 && !f.pinFree'''),

('brier picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ------------------------------------------- BRAMBLESNARE'S PICTURE ---
     v84 section 4, drawn off the fighter's `brier*` fields and the
     simulation's own brambles (`m.brambles`, read) -- never `m.ultFx`, one
     slot the opponent's cast takes (open item 25). A BRAMBLE IS FLOOR: a
     tangle of thorned canes in the school's `dark` with `core` seams and
     thorns, at 0.5 (the design's), inside the sim's own radius (`patchR`, read off
     the caster, so the edge is where the test is).
     It grows out of the hit point over 0.3s (the presentation clock) and
     browns over the last second of its life (the sim's), and it is drawn
     for its whole life: it works for its whole life. WORLD pass, under both
     balls, source-over: nothing under `lighter` and nothing the bloom can
     see. One method a component, so each can be measured alone; nothing
     here keeps state or draws from the rng.
       drawBrier      the floor pass: clipped to the live hall
       _brierGeom     one bramble this frame: centre, growth, browning, alpha
       _brierTangle   its canes, seams and thorns
       _brierMotes    leaves lifting off every bramble (the design's field, drawn)
       _brierRoot     the snare: stalks out of the bramble (part 0, under the
                      ball) and the shoots clenched round its rim (part 1, over)
       drawBrierTop   over both fighters: the clench and a bite's thorn flash
       _brierBite     a bite: four thorns out of the foe's rim
       _brierBlade    the blade greening (from `drawWeapon`, in its frame) */
  drawBrier(m){
    const a = m.a, b = m.b;
    if (!a.brierPic.length && !b.brierPic.length
        && !(a.brierRootFade > 0) && !(b.brierRootFade > 0)) return;       // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      if (f.brierPic.length){
        const end = m.over ? Math.max(0, 1 - f.brierEnd / 0.6) : 1;
        if (end > 0.004){
          for (const p of f.brierPic){
            const g = this._brierGeom(m, f, p, end);
            if (!g) continue;
            this._brierTangle(c, g);
          }
          this._brierMotes(c, m, f, end);
        }
      }
      if (f.brierRootFade > 0) this._brierRoot(m, f, 0);
    }
    c.globalAlpha = 1;
    c.restore();
  }
  /* the growth on the presentation clock (it plays through the planting
     blow's hit stop); the browning and the fade on the bramble's sim age, so
     it reaches 0 on the step the simulation removes it */
  _brierGeom(m, f, p, end){
    const b = p.b, u = f.w.ult, P = AFFINITIES.verdant;
    const s = Math.min(1, p.age / 0.6), k = 1 - (1 - s) * (1 - s);
    const left = u.patchLife - (m.brambleT - b.t0);
    const br = clamp(1 - left / 1.0, 0, 1), fl = clamp(left / 0.25, 0, 1);
    const A = end * fl * Math.min(1, s * 4);
    if (!(A > 0.004)) return null;
    return { x: b.x, y: b.y, R: u.patchR, k, A, g: p.g,
             dk: br > 0 ? mix(P.dark, "#2A2012", br) : P.dark,
             sm: br > 0 ? mix(P.core, "#6E5B2E", br) : P.core };
  }
  /* THE TANGLE: all of it, clipped to how far out of the hit point it has
     grown (no clip once grown): one path for the dark strokes, one for the
     seams, one for the thorns */
  _brierTangle(c, g){
    const x0 = g.x, y0 = g.y;
    const clip = g.k < 0.999;
    if (clip){ c.save(); c.beginPath(); c.arc(x0, y0, Math.max(0.5, g.R * g.k), 0, TAU); c.clip(); }
    c.globalAlpha = g.A * 0.5;
    c.beginPath();
    for (const pts of g.g.canes){
      c.moveTo(x0 + pts[0][0], y0 + pts[0][1]);
      for (let j = 1; j < pts.length; j++) c.lineTo(x0 + pts[j][0], y0 + pts[j][1]);
    }
    c.strokeStyle = g.dk; c.lineWidth = 4.2; c.stroke();
    c.strokeStyle = g.sm; c.lineWidth = 1.4; c.stroke();
    c.fillStyle = g.sm;
    c.beginPath();
    for (const [px, py, tx, ty, sg] of g.g.thorns){
      const nx = -ty * sg, ny = tx * sg, x = x0 + px, y = y0 + py;
      c.moveTo(x + nx * 1.6 - tx * 2.2, y + ny * 1.6 - ty * 2.2);
      c.lineTo(x + nx * 6.5 + tx * 1.4, y + ny * 6.5 + ty * 1.4);
      c.lineTo(x + nx * 1.6 + tx * 2.4, y + ny * 1.6 + ty * 2.4);
      c.closePath();
    }
    c.fill();
    if (clip) c.restore();
  }
  /* LEAVES LIFTING OFF EVERY BRAMBLE (the design's field, drawn: a SPECS
     field fires once, at the cast, where Thornwake stood, and no bramble
     exists then). 4 a bramble, born inside it, lifting 30 units, turning
     and fading; placed by shellHash on the bramble's own seed and the match
     clock (the death clock after the kill), so they keep moving through a
     hit stop. */
  _brierMotes(c, m, f, end){
    const T = m.t + (m.deathAge || 0);
    for (const p of f.brierPic){
      const g = this._brierGeom(m, f, p, end);
      if (!g) continue;
      const sd = g.g.sd + 500;
      c.fillStyle = g.sm;
      for (let i = 0; i < 4; i++){
        const ph = (T * (0.55 + 0.25 * shellHash(sd, i)) + shellHash(sd + 1, i)) % 1;
        const q = TAU * shellHash(sd + 2, i), rr = g.R * g.k * Math.sqrt(shellHash(sd + 3, i)) * 0.85;
        const x = g.x + Math.cos(q) * rr + Math.sin(T * 1.6 + i * 2.3) * 5;
        const y = g.y + Math.sin(q) * rr - ph * 30;
        const ang = T * (1.4 + shellHash(sd + 4, i)) + i * 1.7, ca = Math.cos(ang), sa = Math.sin(ang);
        c.globalAlpha = 0.8 * g.A * Math.sin(ph * Math.PI);
        c.beginPath();
        c.moveTo(x - ca * 4.2, y - sa * 4.2);
        c.quadraticCurveTo(x - sa * 2.2, y + ca * 2.2, x + ca * 4.2, y + sa * 4.2);
        c.quadraticCurveTo(x + sa * 2.2, y - ca * 2.2, x - ca * 4.2, y - sa * 4.2);
        c.fill();
      }
    }
  }
  /* THE SNARE (Tendril's root picture, reused): `part` 0 the stalks out of
     the bramble (under both balls), 1 the clench round the rim (over them).
     The shoots grow up in 0.12s, close round the rim in 0.1s more, hold for
     the pin, dry through its last 30%, and fade 0.2s after it lets go.
     `dark` strands, a `core` seam, `core` tips: the caster's school, verdant
     on whatever ball it holds. The stalks rise out of the bramble the ball
     is caught in, from 1.55 R under its centre -- not the hall's floor, which
     is Tendril's (its root comes out of the ground). */
  _brierRoot(m, f, part){
    const c = this.ctx, R = CONFIG.physics.ballR, P = AFFINITIES.verdant;
    const grow = Math.min(1, f.brierHeldAge / 0.24);
    const cl = clamp((f.brierHeldAge - 0.24) / 0.2, 0, 1), ce = 1 - (1 - cl) * (1 - cl);
    const left = f.brierHeld ? clamp(f.pin / Math.max(0.01, f.pinMax || 1), 0, 1) : 0;
    const wilt = clamp((0.3 - left) / 0.3, 0, 1);
    const dk = mix(P.dark, "#2A2012", wilt), sm = mix(P.core, "#6E5B2E", wilt);
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    c.globalAlpha = f.brierRootFade;
    for (let i = 0; i < 4; i++){
      const sd = i < 2 ? -1 : 1, o = i % 2;
      const qa = sd < 0 ? Math.PI - (o ? 0.62 : 0.16) : (o ? 0.62 : 0.16);    // where it meets the rim
      const cx = f.x + Math.cos(qa) * (R + 1.5), cy = f.y + Math.sin(qa) * (R + 1.5);
      if (part === 0){
        /* up out of the bramble, then climbing onto the rim along it, so the
           clench carries on the way the stalk was already going */
        const fx = f.x + sd * R * (o ? 0.45 : 1.25), fy = f.y + R * 1.55, h = fy - cy;
        const ta = qa - sd * Math.PI / 2, x1 = fx, y1 = fy - h * 0.45;
        const x2 = cx - Math.cos(ta) * R * 0.8, y2 = cy - Math.sin(ta) * R * 0.8;
        const pts = [];
        for (let j = 0; j <= 16; j++){
          const t = grow * j / 16, u = 1 - t;
          pts.push([u * u * u * fx + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t * t * t * cx,
                    u * u * u * fy + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t * t * t * cy]);
        }
        for (const [col, w] of [[dk, 5.4], [sm, 2.0]]){
          c.strokeStyle = col; c.lineWidth = w;
          c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
          for (let j = 1; j < pts.length; j++) c.lineTo(pts[j][0], pts[j][1]);
          c.stroke();
        }
        c.fillStyle = sm;                              // thorns up the stalk
        c.beginPath();
        for (let j = 3; j < pts.length - 1; j += 3){
          const p = pts[j], q = pts[j + 1], dx = q[0] - p[0], dy = q[1] - p[1], dl = Math.hypot(dx, dy) || 1;
          const s2 = (j / 3) % 2 ? 1 : -1, nx = -dy / dl * s2, ny = dx / dl * s2;
          c.moveTo(p[0] + nx * 2.2, p[1] + ny * 2.2);
          c.lineTo(p[0] + nx * 7 + dx / dl * 2, p[1] + ny * 7 + dy / dl * 2);
          c.lineTo(p[0] + nx * 2.2 + dx / dl * 3.4, p[1] + ny * 2.2 + dy / dl * 3.4);
          c.closePath();
        }
        c.fill();
      } else if (grow >= 1 && ce > 0){
        const span = (1.05 - 0.55 * wilt) * ce, a1 = qa - sd * span;
        for (const [col, w] of [[dk, 5.4], [sm, 2.0]]){
          c.strokeStyle = col; c.lineWidth = w;
          c.beginPath(); c.arc(f.x, f.y, R + 1.5, qa, a1, sd > 0); c.stroke();
        }
        const tx = f.x + Math.cos(a1) * (R + 1.5), ty = f.y + Math.sin(a1) * (R + 1.5);
        const da = a1 - sd * Math.PI / 2, nx = -Math.sin(da), ny = Math.cos(da);
        c.fillStyle = wilt > 0.5 ? sm : P.core;
        c.beginPath();
        c.moveTo(tx + nx * 3, ty + ny * 3);
        c.lineTo(tx + Math.cos(da) * 8, ty + Math.sin(da) * 8);
        c.lineTo(tx - nx * 3, ty - ny * 3);
        c.closePath(); c.fill();
      }
    }
    c.restore();
  }
  drawBrierTop(m){
    const a = m.a, b = m.b;
    if (!(a.brierRootFade > 0) && !(b.brierRootFade > 0)
        && !a.brierBite.length && !b.brierBite.length) return;           // <- zero burden
    const c = this.ctx, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, CONFIG.arena.w - 2 * n, CONFIG.arena.h - 2 * n); c.clip();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const f of [a, b]){
      const foe = f === a ? b : a;
      if (f.brierBite.length && foe.alive) this._brierBite(c, f, foe);
      if (f.brierRootFade > 0) this._brierRoot(m, f, 1);
    }
    c.globalAlpha = 1;
    c.restore();
  }
  /* A BITE: four thorns flash out of the foe's rim on the side of the bramble
     it stands in, glow over a dark edge, 0.12s. No freeze (Tendril's flash). */
  _brierBite(c, f, foe){
    const R = CONFIG.physics.ballR, P = AFFINITIES.verdant;
    for (const F of f.brierBite){
      const k = F.t / 0.24, bx = foe.x + Math.cos(F.a) * (R - 2), by = foe.y + Math.sin(F.a) * (R - 2);
      c.globalAlpha = 1 - k * k;
      c.beginPath();
      for (const o of [-0.7, -0.3, 0.3, 0.7]){
        const q = F.a + o, L = 20 * (Math.abs(o) > 0.5 ? 0.7 : 1) * (1 + 0.3 * (1 - k));
        const cq = Math.cos(q), sq = Math.sin(q);
        c.moveTo(bx - sq * 3.4, by + cq * 3.4);
        c.lineTo(bx + cq * L, by + sq * L);
        c.lineTo(bx + sq * 3.4, by - cq * 3.4);
        c.closePath();
      }
      c.fillStyle = P.glow; c.fill();
      c.strokeStyle = P.dark; c.lineWidth = 1.6; c.stroke();
      c.beginPath(); c.arc(bx, by, 4.2 * (1 - 0.5 * k), 0, TAU); c.fill(); c.stroke();
    }
  }
  /* THE BLADE GREENS (v84: "the scythe's blade greens for the window"): the
     verdant scythe's crescent (`SHAPES._scCrescent`, the blade `_scGrown`
     fills pale) filled green over its steel -- `core` at the edge to `dark`
     at the heel -- and its edge and inner thorns relit in `core`. In
     `drawWeapon`'s blade frame (L the drawn reach, W the art width). Greens
     over 0.25s, fades over 0.3s; `al` carries the stunned weapon's dimming. */
  _brierBlade(c, f, L, al){
    const s = Math.min(1, f.brierAge / 0.5), k = Math.min(1 - (1 - s) * (1 - s), f.brierGreen);
    if (!(k > 0.004)) return;
    const W = f.w.artW, P = AFFINITIES.verdant;
    c.save();
    SHAPES._scCrescent(c, L, W);
    const g = c.createLinearGradient(L * 0.55, -W, L * 0.95, W * 0.2);
    g.addColorStop(0, P.core); g.addColorStop(0.55, "#2E8A45"); g.addColorStop(1, P.dark);
    c.globalAlpha = al * k * 0.85;
    c.fillStyle = g; c.fill();
    c.fillStyle = P.core;
    for (let i = 1; i <= 6; i++){
      const q = SHAPES._scOuter(L, W, i / 7);
      c.beginPath();
      c.moveTo(q.x - q.nx * W * 0.04, q.y - q.ny * W * 0.04);
      c.lineTo(q.x - q.nx * W * 0.19 + Math.cos(q.a) * W * 0.11,
               q.y - q.ny * W * 0.19 + Math.sin(q.a) * W * 0.11);
      c.lineTo(q.x - q.nx * W * 0.05 + Math.cos(q.a) * W * 0.13,
               q.y - q.ny * W * 0.05 + Math.sin(q.a) * W * 0.13);
      c.closePath(); c.fill();
    }
    c.globalAlpha = al * k;
    c.strokeStyle = P.core; c.lineWidth = Math.max(1, W * 0.05);
    c.lineCap = "round";
    c.beginPath();
    c.moveTo(L * 0.70, W * 0.20);
    c.bezierCurveTo(L * 1.02, -W * 0.20, L * 0.98, -W * 0.95, L * 0.56, -W * 1.32);
    c.stroke();
    c.restore();
  }

  drawMotes(m){
'''),

("brier picture: the freeze's floor roots retired",
 '''    else if (u.w === "thornwake"){
      /* roots running along the floor from caster to quarry */
      const grow = clamp(u.t / 0.30, 0, 1);
      const fade = 1 - clamp((u.t - u.life * 0.72) / (u.life * 0.28), 0, 1);
      c.globalAlpha = 0.85 * fade;
      for (let i = 0; i < 4; i++){
        c.strokeStyle = i % 2 ? "#0D3A1A" : "#2E6B2C";
        c.lineWidth = 5 - i * 0.7;
        this._jag(c, u.x, u.y, tgt.x, tgt.y, 9, 26 + i * 9, 300 + i, grow);
      }
    }
''',
 '''    /* ---- Bramblesnare's floor roots, caster to quarry, were the FREEZE's
       (v84 retired the 1.6s root; v113 stage 6). The brambles are
       `drawBrier`, off the fighter and the simulation's own brambles, where
       the one ultFx slot cannot erase them; the cast's record now carries the
       CAST only and nothing draws from it. */
'''),

("brier picture: the freeze's thorns on the quarry retired",
 '''    /* ---- Bramblesnare: they are pinned, and you can see the thorns */
    else if (u.w === "thornwake"){
      const grow  = clamp((u.t - 0.12) / 0.30, 0, 1);
      const hold  = clamp((u.t - u.life * 0.70) / (u.life * 0.30), 0, 1);
      const alive = 1 - hold;
      const R = CONFIG.physics.ballR;
      const N = 9;
      for (let i = 0; i < N; i++){
        const a0 = (i / N) * TAU + shellHash(11, i) * 0.5;
        const side = shellHash(21, i) > 0.5 ? 1 : -1;
        const len = (R * 2.5 + shellHash(31, i) * R * 1.4) * grow;
        const bx = tgt.x + Math.cos(a0) * (R + 16), by = tgt.y + Math.sin(a0) * (R + 16);
        const ex2 = tgt.x + Math.cos(a0 + side * 1.5) * (R * 0.25);
        const ey2 = tgt.y + Math.sin(a0 + side * 1.5) * (R * 0.25);
        const cx2 = tgt.x + Math.cos(a0 + side * 0.5) * (R + len * 0.7);
        const cy2 = tgt.y + Math.sin(a0 + side * 0.5) * (R + len * 0.7);
        c.globalAlpha = alive;
        c.strokeStyle = "#16401F"; c.lineWidth = 8.5 * grow;
        c.beginPath(); c.moveTo(bx, by); c.quadraticCurveTo(cx2, cy2, ex2, ey2); c.stroke();
        c.strokeStyle = "#4FD06B"; c.lineWidth = 3.4 * grow;
        c.shadowColor = "#4FD06B"; c.shadowBlur = 10;
        c.beginPath(); c.moveTo(bx, by); c.quadraticCurveTo(cx2, cy2, ex2, ey2); c.stroke();
        c.shadowBlur = 0;
        /* thorns, because a smooth vine is a rope and a rope is not a threat */
        c.fillStyle = "#BCF7C7";
        for (let j = 1; j <= 4; j++){
          const t2 = j / 5, uu = 1 - t2;
          const px = uu*uu*bx + 2*uu*t2*cx2 + t2*t2*ex2;
          const py = uu*uu*by + 2*uu*t2*cy2 + t2*t2*ey2;
          const dxq = 2*uu*(cx2-bx) + 2*t2*(ex2-cx2);
          const dyq = 2*uu*(cy2-by) + 2*t2*(ey2-cy2);
          const dl = Math.hypot(dxq, dyq) || 1;
          const nx = -dyq/dl * side, ny = dxq/dl * side;
          const th = 7.5 * grow;
          c.globalAlpha = alive * 0.95;
          c.beginPath();
          c.moveTo(px + nx*1.6, py + ny*1.6);
          c.lineTo(px + nx*1.6 + dxq/dl*4.4, py + ny*1.6 + dyq/dl*4.4);
          c.lineTo(px + nx*th, py + ny*th);
          c.closePath(); c.fill();
        }
      }
      /* the snare cinching shut */
      c.globalAlpha = alive * 0.6;
      c.strokeStyle = "#4FD06B"; c.lineWidth = 2.4;
      c.beginPath();
      c.arc(tgt.x, tgt.y, (R + 20) * (1.25 - 0.25 * grow), 0, TAU); c.stroke();
    }
''',
 '''    /* ---- Bramblesnare's thorns on the pinned quarry were the FREEZE's;
       retired with it (v84, v113 stage 6). The snare's shoots are
       `_brierRoot`, the cast is the blade greening (`_brierBlade`). */
'''),

("brier picture: the cast record's life",
 '''thornwake: 2.4, ''',
 ''''''),

('brier picture: the banner on the caster',
 '''thornwake:1, ''',
 ''''''),

]


# ------------------------------------------------------- the insert scan --
# WHAT STAGES 1-5's ADDED CODE MAY WRITE (reading 13): the window record, the
# thorns' two fields and the tally on the fighter (and the tally's counters),
# the window's clock, the match's brambles and their clock, and the three
# fields of Grasp's write on the foe. The statuses are the design's one
# entangle line; the one hurt is the design's bite; the one beat is a killing
# tick's.
WRITE_OK = {("this", "ultBramble"), ("this", "brambleCd"), ("this", "brambleIn"), ("this", "brambleTally"),
            ("this", "brambles"), ("this", "brambleT"),
            ("f", "ultBramble"), ("f", "brambleCd"), ("f", "brambleIn"), ("f", "brambleTally"),
            ("brambleTally", "casts"), ("brambleTally", "frames"), ("brambleTally", "planted"), ("Z", "t"),
            ("T", "tested"), ("T", "after"), ("T", "foeIn"), ("T", "entries"), ("T", "snares"),
            ("T", "ticks"), ("T", "dealt"), ("T", "ent"), ("T", "kills"),
            ("foe", "pinV"), ("foe", "pin"), ("foe", "pinMax")}
APPLY_LINE = '.apply("entangle", u.tickEnt, side)'
HURT_LINE = ".hurt(foe, u.tickDmg, f)"
CALLS_OK = {"apply", "hurt", "beat", "push", "splice", "hypot", "max", "plantBramble", "tickBramble"}

# ------------------------------------------------------- the stage-6 scan --
# STAGE 6'S NAMES, free on the base on identifier boundaries (the picture's
# `brier*`, never the simulation's `bramble*`), and what its inserts may do
# (readings 17-22). Everything else is the simulation's.
S6_NAMES = ("tickBrier", "drawBrier", "drawBrierTop", "_brierCanes", "_brierGeom", "_brierTangle",
            "_brierMotes", "_brierRoot", "_brierBite", "_brierBlade", "brierGreen", "brierAge", "brierOut",
            "brierEnd", "brierPic", "brierSeen", "brierTagN", "brierTagT", "brierBite", "brierHeld",
            "brierRootFade", "brierHeldAge", "brierHeldOut", "thornwake-crackle", "thornwake-snare",
            "thornwake-bite")
S6_SFX_ROW = "Sfx: Bramblesnare's cast"
S6_TICK_ROW = "brier picture: tickBrier"
S6_DRAW_ROW = "brier picture: the drawing methods"
S6_FIELDS_ROW = "brier picture: fighter fields"
# THE THREE LINES ON THE SIM PATH, whole (reading 18): each row's added code,
# comments stripped, line for line -- one SFX.play and nothing else.
S6_SIM_LINES = {
    "plantBramble: the crackle": ['SFX.play("ult", { w: "thornwake-crackle" });'],
    "tickBramble: the snare's voice": ['SFX.play("ult", { w: "thornwake-snare" });'],
    "tickBramble: the bite's soft snap": ['SFX.play("ult", { w: "thornwake-bite" });'],
}
# THE ONE-LINE ROWS, whole: the picture's calls and its two lines in the
# renderer's own methods (the blade in drawWeapon, the hexagon's return in
# _drawField).
S6_ONE_LINE = {
    "brier picture: the presentation call": ["this.tickBrier(dt);"],
    "brier picture: the floor call": ["if (__world) this.drawBrier(m);"],
    "brier picture: over both fighters": ["this.drawBrierTop(m);"],
    "brier picture: the blade greens": ['if (f.brierGreen > 0 && f.w.shape === "scythe") '
                                        'this._brierBlade(c, f, reach + 6, dim * wk);'],
    "brier picture: the hexagon off": ["if (f.brierHeld > 0 && f.pin > 0 && !f.pinFree) return;"],
}
# THE RETIRED ART: rows that replace the freeze's picture (and its two map
# entries) with nothing but a comment.
S6_RETIRED = ("brier picture: the freeze's floor roots retired",
              "brier picture: the freeze's thorns on the quarry retired",
              "brier picture: the cast record's life", "brier picture: the banner on the caster")
# THE SHARED MODULE TABLES STAGE 6 MAY READ, by exact path, and no other
# reference to one (no write: a table written holds for every later match).
S6_TABLE_READS = ("CONFIG.physics.ballR", "CONFIG.arena.w", "CONFIG.arena.h", "AFFINITIES.verdant",
                  "STATUS.entangle.tip", "SHAPES._scCrescent", "SHAPES._scOuter")
# IN tickBrier ALONE, the writes that are not a `brier*` field, each by its
# receiver and bound where it is declared: a picture record's clock, a bite
# flash's clock, the seen counts, the ENTANGLE tag's count and the teaching
# flag (Tendril's tag rule).
S6_TICK_WRITES = {("p", "age"): "for (const p of P) p.age += dt;",
                  ("f.brierBite[i]", "t"): "f.brierBite[i].t += dt;",
                  ("g", "val"): "if (g){ if (!g.first) g.val = n; }",
                  ("this.taught", "entangle"): "if (first) this.taught.entangle = true;"}
S6_TICK_INDEX = "S[0] = T.snares; S[1] = T.ticks;"
S6_TICK_BINDS = {"P": "const P = f.brierPic;",
                 "S": "const S = f.brierSeen, dS = T.snares - S[0], dK = T.ticks - S[1];",
                 "g": 'const g = this.tags.find(g2 => g2.key === "entangle" && g2.life > 0.3'}
S6_ARMS = ('} else if (w === "thornwake"){', '} else if (w === "thornwake-crackle"){',
           '} else if (w === "thornwake-snare"){', '} else if (w === "thornwake-bite"){')
OLD_ARM = '        } else if (w === "thornwake"){                  // creak and cinch\n'
RUNE_CRACK = "        } else {                                        // rune-crack"
S6_WRITE = r"\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)"
S6_RECV = r"(?<![\w$.])((?:this|[A-Za-z_$][\w$]*)(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*)"


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone -- SPECS.thornwake goes by the orchestrator's fx_remove at
    the carry, never by this builder (reading 21)."""
    head = re.search(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. "
                     r"sha256:([0-9a-f]{64}) ---- \*/\n", s)
    if not head:
        raise SystemExit("no inlined fx.js header in this build")
    tm = re.compile(r"/\* -+ THE ULT FIELDS -+").search(s, head.end())
    return s[head.start():tm.start()]


def s6_added(old: str, new: str) -> str:
    """A stage-6 row's ADDED code, comments out: its new text less the anchor it
    re-emits (a replace row adds all of its new text)."""
    return strip_comments(new.replace(old, "", 1) if old in new else new)


def s6_lines(ins: str) -> list:
    return [" ".join(ln.split()) for ln in ins.splitlines() if ln.strip()]


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION (reading 22). Its ADDED code (a row's re-emitted
    anchor aside) draws no RNG, never takes the one ultFx slot (open item 25),
    calls nothing that hurts, applies, plants, ticks, resolves, stuns, beats,
    knocks or moves, never writes the shared weapon row or a module table (it
    reads seven of their entries by exact path), writes only `brier*` fields,
    the canvas and -- in tickBrier alone -- five bound things by exact line,
    and mutates only its own arrays. Its lines on the sim path are the three
    voice rows, whole, each in its own row; `SFX` only there; the synth only in
    the Sfx arms; the tags only in tickBrier; the one-line rows whole; the
    retired rows nothing but comments. The probe's [9]-[10] and engine_ab are
    the dynamic proof. Run on every stage: it reads the table."""
    labels = [lb for lb, _o, _n in S6]
    for key in list(S6_SIM_LINES) + list(S6_ONE_LINE) + list(S6_RETIRED) + [S6_SFX_ROW, S6_TICK_ROW,
                                                                             S6_DRAW_ROW, S6_FIELDS_ROW]:
        if sum(1 for lb in labels if lb.startswith(key)) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's table has not exactly one row '{key}...'")
    for label, old, new in S6:
        ins = s6_added(old, new)
        tick = label.startswith(S6_TICK_ROW)
        draw = label.startswith(S6_DRAW_ROW)
        sfx = label.startswith(S6_SFX_ROW)
        if re.search(r"\brng\b", ins) or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|breakSpin|"
                     r"takeHitstun|tickBramble|plantBramble|tickStatus|tickStasis|tickWeapon|tickHits|tickCharge|"
                     r"move|collide|spawnShot|note|checkEnd|step|decay|decayImpactOnly)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*" + S6_WRITE, ins) or re.search(r"\bult\.\w+" + S6_WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        for mt in re.finditer(r"\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES)\b(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*", ins):
            if mt.group(0) not in S6_TABLE_READS or re.match(S6_WRITE, ins[mt.end():]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reaches a shared "
                                 f"module table other than by the seven reads it may make: {mt.group(0)!r}")
        if re.search(r"\.\s*(?:hp|shield|pin|pinMax|pinV|pinFree|stun|hitStop|shake|x|y|vx|vy|theta|charge|"
                     r"brambles|brambleT|ultBramble|brambleCd|brambleIn|brambleTally|planted|snares|ticks|"
                     r"status|over|winner)(?![\w$])" + S6_WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the simulation "
                             "(a body, a hold, the clock, the brambles, the window or the tally)")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        one = [k for k in S6_ONE_LINE if label.startswith(k)]
        if sim and s6_lines(ins) != S6_SIM_LINES[sim[0]]:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path ('{label}') is "
                             f"not its voice alone:\n{ins}")
        if not sim and re.search(r"\bSFX\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice "
                             "outside the crackle, the snare and the bite")
        if one and s6_lines(ins) != S6_ONE_LINE[one[0]]:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's one-line row ('{label}') is not "
                             f"that line alone:\n{ins}")
        if any(label.startswith(k) for k in S6_RETIRED) and s6_lines(ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6's retiring row ('{label}') adds code:\n{ins}")
        if re.search(r"\b_tone\s*\(|\b_burst\s*\(|\b_sweep\s*\(|\bbuildChain\b|\bfrequency\b|\bctx\.currentTime\b",
                     ins) and not sfx:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if re.search(r"\.play\s*\(", ins) and not sim:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays outside its "
                             "three voice lines")
        if re.search(r"\btags\b|\bstatusTag\b|\btaught\b|\.val\b", ins) and not tick:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' touches the "
                             "tags outside tickBrier")
        if re.search(r"\bdelete\s|Object\.(assign|defineProperty|defineProperties|setPrototypeOf)\s*\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' deletes or "
                             "redefines a property")
        # THE CANVAS: `c` only as the renderer's own context, or a method's first parameter
        for mb in re.finditer(r"\b(?:const|let|var)\s+c\s*=\s*([^,;\n]+)", ins):
            if mb.group(1).strip() != "this.ctx":
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' binds `c` to "
                                 f"{mb.group(1).strip()!r}, not the renderer's context")
        if re.search(r"(?<![\w.$])c\s*=(?!=)", re.sub(r"\bconst c = this\.ctx\b", "", ins)):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reassigns `c`")
        lines = s6_lines(ins)
        if tick:
            for nm, bind in S6_TICK_BINDS.items():
                if sum(ln.startswith(bind) for ln in lines) != 1 or len(re.findall(
                        r"(?<![\w$.])" + re.escape(nm) + r"\s*=(?!=)", ins)) != 1:
                    raise SystemExit(f"REFUSING TO WRITE -- tickBrier does not bind `{nm}` exactly "
                                     f"once, as {bind!r}")
        for mw in re.finditer(S6_RECV + r"\s*\.\s*([A-Za-z_$][\w$]*)" + S6_WRITE, ins):
            recv, prop = re.sub(r"\s+", "", mw.group(1)), mw.group(2)
            ok = ((recv in ("this", "f", "foe") and prop.startswith("brier")
                   and (label.startswith(S6_FIELDS_ROW) if recv == "this" else tick))
                  or (recv == "c" and draw)
                  or (tick and (recv, prop) in S6_TICK_WRITES
                      and lines.count(S6_TICK_WRITES[(recv, prop)]) == 1))
            if not ok:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes {recv}.{prop}")
        for mw in re.finditer(S6_RECV + r"\s*\[([^\]]*)\]" + S6_WRITE, ins):
            recv = re.sub(r"\s+", "", mw.group(1))
            if not (tick and recv == "S" and mw.group(2).strip() in ("0", "1") and lines.count(S6_TICK_INDEX) == 1):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes through an "
                                 f"index: {recv}[{mw.group(2)}]")
        for mw in re.finditer(S6_RECV + r"\s*\.\s*(push|splice|pop|shift|unshift|reverse|sort|copyWithin|fill)\s*\(", ins):
            recv = re.sub(r"\s+", "", mw.group(1))
            local = (re.search(r"\bconst " + re.escape(recv) + r" = \[", ins)
                     or re.search(r"\bconst canes = \[\], thorns = \[\]", ins) and recv in ("canes", "thorns"))
            ok = ((recv == "c" and draw)
                  or (tick and recv in ("P", "f.brierBite"))
                  or ((tick or draw) and recv in ("canes", "thorns", "pts") and local))
            if not ok:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' mutates {recv}")


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page: the inlined fx.js untouched; the old
    arm gone and the four new ones before the shared rune-crack fallback,
    which is kept once; the freeze's art gone; the three voice lines each
    added once, each where it belongs; every arm, call, pass and method wired
    exactly once; the hexagon's return just before its guard; and no
    Math.random added or taken away."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 21)")
    if "// creak and cinch" in s:
        raise SystemExit("REFUSING TO WRITE -- the freeze's voice (creak and cinch) is still here")
    if s.count(RUNE_CRACK) != 1 or any(not 0 <= s.find(a) < s.find(RUNE_CRACK) for a in S6_ARMS):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Bramblesnare's arms")
    if ('u.w === "thornwake"' in out_code or re.search(r"\bthornwake\s*:\s*2\.4\b", out_code)
            or re.search(r"onTarget\s*=\s*\{[^}]*\bthornwake\s*:", out_code)):
        raise SystemExit("REFUSING TO WRITE -- the freeze's art is still drawn or seated "
                         "(its drawUlt branches, its life entry or its banner seat)")
    for need in ("this.tickBrier(dt);", "if (__world) this.drawBrier(m);", "this.drawBrierTop(m);",
                 "  tickBrier(dt){", "  _brierCanes(f, b){", "  drawBrier(m){", "  _brierGeom(m, f, p, end){",
                 "  _brierTangle(c, g){", "  _brierMotes(c, m, f, end){", "  _brierRoot(m, f, part){",
                 "  drawBrierTop(m){", "  _brierBite(c, f, foe){", "  _brierBlade(c, f, L, al){",
                 S6_ONE_LINE["brier picture: the blade greens"][0],
                 S6_ONE_LINE["brier picture: the hexagon off"][0]) + S6_ARMS:
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        for ln in v:
            if out_code.count(ln) != code.count(ln) + 1:
                raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    flat = " ".join(out_code.split())
    for label, pat in (("the crackle", r'plantBramble\(f, q\)\{ this\.brambles\.push\(\{ x: q\.x, y: q\.y, t0: this\.brambleT, '
                        r'side: f === this\.a \? "a" : "b" \}\); f\.brambleTally\.planted\+\+; '
                        r'SFX\.play\("ult", \{ w: "thornwake-crackle" \}\); \}'),
                       ("the snare", r'foe\.pinMax = Math\.max\(foe\.pinMax, u\.rootFor\); T\.snares\+\+; '
                        r'SFX\.play\("ult", \{ w: "thornwake-snare" \}\); \}'),
                       ("the bite", r'if \(f\.brambleCd <= 0\)\{ f\.brambleCd = u\.tickCd; '
                        r'SFX\.play\("ult", \{ w: "thornwake-bite" \}\); foe\.apply\("entangle", u\.tickEnt, side\);')):
        if len(re.findall(pat, flat)) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {label}'s voice is not where it belongs "
                             "(plantBramble after the count; the snare after the pin's count; the bite as "
                             "the cooldown re-arms, before the entangle)")
    if "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n    this.tickBrier(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickBrier does not follow tickNovaFx in tickPresentation")
    # the guard by its own prefix (the row's anchor): Tendril's stage 6 extends that line on later tips
    if not re.search(r"if \(f\.brierHeld > 0 && f\.pin > 0 && !f\.pinFree\) return;\s*if \(f\.pin > 0 && !f\.pinFree\b",
                     out_code):
        raise SystemExit("REFUSING TO WRITE -- the hexagon's return is not just before _drawField's guard")
    if out_code.count('SFX.play("ult", { w: f.w.id });') != code.count('SFX.play("ult", { w: f.w.id });'):
        raise SystemExit("REFUSING TO WRITE -- fireUlt's cast voice moved")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- stage 6 adds or takes away a Math.random")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes its own "
          "`brier*` fields, the canvas and five bound things in tickBrier only; the crackle, snare and bite "
          "voices its three lines on the sim path, each where it belongs); the inlined fx.js untouched; the "
          "rune-crack fallback kept; the freeze's voice and art gone; every arm, call, pass and method once")


# ---------------------------------------------------------------- naming --
NAMES = ("ultBramble", "brambleCd", "brambleIn", "brambleTally", "brambles", "brambleT",
         "tickBramble", "plantBramble", 'kind:"bramble"', '"bramble"')
STAGE_OUT = {"1": "sc-thornwake-stub", "2": "sc-thornwake-bramble", "3": "sc-thornwake-snare",
             "5": f"sc-thornwake-b{BLADE}", "6": f"sc-thornwake-b{BLADE}-fx"}


def free_name(name: str, code: str) -> bool:
    return not re.search(r"(?<![A-Za-z0-9_$])" + re.escape(name) + r"(?![A-Za-z0-9_$])", code)


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
    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    if A.stage != "1" and ULT["charge"] is None:
        raise SystemExit(f"stage {A.stage}: the charge is not measured yet (ULT['charge'])")
    if A.stage == "5" and (BLADE is None or BLADE == SHIPPED_DMG):
        raise SystemExit("stage 5: the blade is not measured yet (BLADE)")

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not out_p.name.startswith("sc-thornwake"):
        raise SystemExit(f"refusing {out_p.name}: this builder's links are sc-thornwake*")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is "
                         "written once. Delete it by hand if this is a rebuild.")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"refusing {out_p.name}: 02-chain already has a link of that name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    # READ AS BYTES: read_text() translates CRLF to LF, so this refusal could never fire
    # (found at stage 6: a CRLF copy of the base built; fixed then, and no link moves).
    s0 = src_p.read_bytes().decode("utf-8")
    if "\r" in s0:
        raise SystemExit("the source is not LF text")
    s = s0
    print(f"\nTHORNWAKE / BRAMBLESNARE (REDESIGN) -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The relic this builder redesigns, with its body;
    # the engine's gates the brambles pay through; the window clock.
    row = relic_row(code, RELIC)
    for need, why in (('shape:"scythe"', "Thornwake is not a scythe"),
                      ('mode:"spin"', "Thornwake does not spin"),
                      ('aff:"verdant"', "Thornwake is not verdant"),
                      ("onHit:{ entangle:2 }", "Thornwake does not carry the verdant channel")):
        if need not in row:
            raise SystemExit(f"wrong base: {why}")
    if " ".join(ROW_HEAD.split()) not in " ".join(row.split()) or \
       " ".join(ROW_TAIL.split()) not in " ".join(row.split()):
        raise SystemExit("wrong base: Thornwake's scythe profile has moved")
    for need, why in (("hurt(foe, dmg, src){", "no hurt(foe, dmg, src) gate"),
                      ("apply(key, n, src){", "no Fighter.apply(key, n, src)"),
                      ("get alive(){ return this.hp > 0; }", "no Fighter.alive"),
                      ("resolveHit(self, foe, hx, hy, seg, mul, over){", "no resolveHit"),
                      ("self.hits++; self.dealt += dmg;", "resolveHit no longer counts the blow"),
                      ("fireUlt(f, foe){", "no fireUlt"),
                      ("beat(", "no beat"),
                      ("tickStasis(dt){", "no tickStasis"),
                      ("if (!f.pinFree) f.stun = Math.max(f.stun, f.pin);",
                       "tickStasis no longer locks the weapon of a hold without pinFree"),
                      ("if (f.pin > 0) return;", "move() no longer holds a pinned ball"),
                      ("f.vy = Math.max(0, f.pinV[1]);", "move() no longer resumes pinV (the Stasis clamp)"),
                      ('if (idA === idB) throw new Error("A relic cannot fight itself");',
                       "Match no longer refuses a mirror")):
        if need not in code:
            raise SystemExit(f"wrong base: {why}")
    if not re.search(r'\n  entangle:\s+\{ name:"Entangle",', code):
        raise SystemExit("wrong base: no STATUS.entangle")
    # THE WINDOW CLOCK: a hit stop returns from step() before the window
    # tickers, and the tickers run before the hit loops.
    st = code[code.find("  step(dt){"):]
    hs = st.find("if (this.hitStop > 0){")
    tt = st.find("this.tickTendril(dt);")
    th = st.find("this.tickHits(self, foe, dt);")
    mv = st.find("this.move(self, foe, dt);")
    if tt < 0:
        raise SystemExit("wrong base: no `this.tickTendril(dt);` in step() -- the brambles' ticker "
                         "goes after Tendril's (v68), so this is not the Tendril lineage")
    if hs < 0 or not hs < st.find("return;", hs) < tt:
        raise SystemExit("wrong base: the window tickers do not stop in a hit stop")
    if not mv < tt < th:
        raise SystemExit("wrong base: the window tickers do not run after the moves and before the hit loops")
    # WHO ELSE CASTS THROUGH THE FREEZE'S GENERIC TAIL (read, never refused on:
    # Heartwood is being redesigned too, and either may be carried first).
    freezers = [rid for rid in re.findall(r'\{ id:"([a-z]+)", name:"', code)
                if 'kind:"freeze"' in relic_row(code, rid)]
    # THE NAMES THIS BUILD ADDS ARE FREE ON THE BASE.
    if A.stage == "1":
        for name in NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")
        if s0.count(SHIPPED_ULT) != 1:
            raise SystemExit("wrong base: Thornwake does not carry the shipped Bramblesnare")
        if f"dmg:{SHIPPED_DMG}," not in row:
            raise SystemExit("wrong base: Thornwake is not at its shipped blade")
    print("  base  Thornwake's shipped body (verdant scythe, spin, entangle 2); hurt / apply / "
          "resolveHit's count / beat / tickStasis's lock / move's hold and resume; no mirror; the "
          "window tickers stop in a hit stop and run after the moves, before the hit loops")
    if A.stage == "1":
        print(f"  note  kind \"freeze\" on this base: {', '.join(freezers) or 'none'} -- its generic tail "
              "stays (reading 15)")

    blade = SHIPPED_DMG                 # stages 1-3 keep the shipped blade; stage 5 writes BLADE
    root_now = 0
    if A.stage == "1":
        edits, want = S1, ult_block("1e9", 0)
    else:
        if 'kind:"bramble"' not in row:
            raise SystemExit(f"stage {A.stage} needs stage 1 under it")
        if A.stage == "2":
            if not free_name("tickBramble", code) or "charge:1e9" not in row:
                raise SystemExit("stage 2 goes on stage 1, once")
            edits, want = S2, ult_block(ULT["charge"], 0)
        elif A.stage == "3":
            if free_name("tickBramble", code) or "rootFor:0," not in row:
                raise SystemExit("stage 3 goes on stage 2, once")
            edits, want = S3, ult_block(ULT["charge"], ULT["rootFor"])
            root_now = ULT["rootFor"]
        elif A.stage == "6":
            # STAGE 6 GOES ON STAGE 5, ONCE: the snare on, the blade BLADE names,
            # the brambles' ticker, none of stage 6's names in the source yet (on
            # identifier boundaries), the freeze's voice still there to replace,
            # and what the picture and the voice read there.
            want = ult_block(ULT["charge"], ULT["rootFor"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{BLADE}," not in row or free_name("tickBramble", code)
                    or free_name("plantBramble", code)):
                raise SystemExit("stage 6 goes on stage 5 (the snare on, at the blade BLADE names)")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            if s0.count(OLD_ARM) != 1:
                raise SystemExit("the freeze's voice (creak and cinch) is not in this source once -- "
                                 "stage 6 goes on stage 5, once")
            for need, why in (("function shellHash(", "no shellHash (the canes' hash, never the RNG)"),
                              ("const clamp = ", "no clamp"),
                              ("function mix(", "no mix (the browning)"),
                              ("const TAU = ", "no TAU"),
                              ("  stacks(key){", "no Fighter.stacks (the tag's count)"),
                              ("  statusTag(x, y, key, first, val){", "no statusTag (the ENTANGLE tag)"),
                              ("this.taught = ", "no taught (the teaching panel's flag)"),
                              ("  _scCrescent(c, L, W){", "no SHAPES._scCrescent (the blade the green fills)"),
                              ("  _scOuter(", "no SHAPES._scOuter (the blade's edge)"),
                              ('  verdant:    { key:"verdant"', "no AFFINITIES.verdant"),
                              ("  drawWeapon(m, f){", "no drawWeapon(m, f)"),
                              ("  _drawField(m, f){", "no _drawField(m, f) (the hexagon a snare must not draw)"),
                              ("  tickPresentation(dt){\n    this.tickNovaFx(dt);", "tickPresentation does not open "
                               "with tickNovaFx"),
                              ('SFX.play("ult", { w: f.w.id });', "fireUlt no longer voices the cast by id"),
                              (RUNE_CRACK, "no shared rune-crack fallback in the synth")):
                if need not in s0:
                    raise SystemExit(f"wrong base for stage 6: {why}")
            blade = BLADE
            edits = S6
            root_now = ULT["rootFor"]
        else:
            want = ult_block(ULT["charge"], ULT["rootFor"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{SHIPPED_DMG}," not in row):
                raise SystemExit("stage 5 goes on stage 3 (the snare on, blade 31.35), once")
            blade = BLADE
            edits = S5
            root_now = ULT["rootFor"]
    s6_static_checks()                  # stage 6's table, read on every stage, before any edit
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Thornwake's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    print(f"  ok    ult   {' '.join(blk.split())[:110]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}   rootFor {root_now}")
    if f"dmg:{blade}," not in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the blade is not the one this stage writes")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    for label, _old, new in S1 + S2 + S3 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades|ult|mass|onHit)\s*=[^=]", ins) or \
           re.search(r"\bw\.ult\.\w+\s*=[^=]", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        if "pinFree" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' touches "
                             "pinFree (the snare is Grasp's write)")
        if re.search(r"hitStop\s*[-+*/]?=(?!=)|\.stun\s*[-+*/]?=(?!=)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' stops the world or stuns "
                             "(reading 13)")
        # WHAT THE ADDED CODE MAY DO, AND NOTHING ELSE (reading 13): the anchor each row
        # re-emits is taken out first.
        added = strip_comments(new.replace(_old, "", 1) if _old and _old in new else new)
        for call in re.findall(r"\.(\w+)\(", added):
            if call not in CALLS_OK:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' calls .{call}(): the "
                                 "brambles plant, snare, entangle and bite, nothing else (reading 13)")
        applies = re.findall(r"\.apply\([^;]*\)", added)
        if applies and applies != [APPLY_LINE]:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' applies {applies}: the only "
                             f"status is the design's entangle, {APPLY_LINE}")
        hurts = re.findall(r"\.hurt\([^;]*\)", added)
        if hurts and hurts != [HURT_LINE]:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' hurts {hurts}: the only "
                             f"damage is the design's bite, {HURT_LINE}")
        beats = re.findall(r"\.beat\(", added)
        if beats and (len(beats) != 1 or "fatal: true" not in added or "if (wasUp && foe.hp <= 0){" not in added):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' files a beat that is not a "
                             "killing tick's (reading 9)")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", added):
            if (mw.group(1), mw.group(2)) not in WRITE_OK:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes "
                                 f"{mw.group(1)}.{mw.group(2)} (reading 13: the window, the thorns, "
                                 "the tally, the brambles and their clock, and Grasp's pin only)")
        if re.search(r"\bdelete\b|\[[^\]]*\]\s*=(?!=)", added):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' deletes or writes by index")
    if len(re.findall(r'kind:"bramble"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one bramble ultimate")
    if 'kind:"freeze"' in relic_row(out_code, RELIC):
        raise SystemExit("REFUSING TO WRITE -- the freeze is still in Thornwake's row")
    if A.stage != "1" and out_code.count("this.plantBramble(self, foe)") != 1:
        raise SystemExit("REFUSING TO WRITE -- the plant is not called exactly once, from resolveHit")
    if A.stage != "1" and out_code.count("this.tickBramble(dt);") != 1:
        raise SystemExit("REFUSING TO WRITE -- the brambles' ticker is not called exactly once")
    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one bramble ultimate, Thornwake's; the freeze out of its row; no insert draws "
          f"the RNG, writes the shared weapon, touches pinFree, stops or stuns; "
          f"{n_ids} relics in the roster")

    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
