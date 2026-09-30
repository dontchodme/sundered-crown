#!/usr/bin/env python
"""GORESHARD / BLOODPRICE, REDESIGNED -- the foe pays in blood. v114.

Built from `06-docs/v81/goreshard-bloodprice-redesign-v81.md` (Cowork,
2026-09-26), §5 its build brief, which is the input and the only input.
CLAUDE.md §3 rule 0: nothing here is a design decision. A REDESIGN: the relic
ships in the base (id `oathwound`, name Goreshard -- the roster's id/name
mismatch; read the name from the build); its beam is replaced.

    stage 1   the ultimate stubbed      <tip> -> sc-goreshard-stub.html
              the new ult block at charge 1e9 (the beam unreachable) -- the
              lab's arm A, fight for fight
    stage 2   the price                 -> sc-goreshard-price.html
              the design's stage 1 ("beam out, the multiplier in"), the charge
              on the game's clock (the lab's arm B at perStack 0.30)
    stage 5   the blade                 -> sc-goreshard-b<blade>.html
              the design's stage 2 ("the blade"), settled by Rick's 2026-09-29
              ruling: the measured point nearest 50% both sides (reading 12)
    stage 6   the picture and the voice -> sc-goreshard-b<blade>-fx.html
              the design's stage 3 ("picture, voice, carry; beam's field spec
              out"), on stage 5's link: the labs' rows, byte for byte (S6,
              readings 13-21). No fx.js field (reading 15): the beam's
              `SPECS.oathwound` leaves BOTH fx.js copies at the carry, by the
              orchestrator's fx_remove; stage 6 leaves the inlined copy as it
              is, and refuses if its edits touch it.

§1: "For a duration the enemy's blood is the sword's edge: every blow
Goreshard lands hits harder for every stack of Hemorrhage the enemy is
carrying -- nearly a third more per stack."  One clause: `dmg x (1 + 0.30 x foe
hemorrhage stacks)` on every blow in the window (cap 4 -> up to +120%).

Declared (v81 §1, §4, §5):
  THE CAST     opens a window of `dur` seconds and resolves nothing: the beam's
               16 damage and 3 Hemorrhage are deleted from the row with its
               card ("beam out").
  THE PRICE    in `resolveHit`, for a blow by a caster whose window is open:
               the blade is x(1 + perStack x the struck fighter's Hemorrhage
               stacks), the stacks READ BEFORE this blow's own onHit ("the
               blow pays on the stacks it found, then bleeds"). One line; the
               lab wrote `w.dmg` each frame, the build scales in the hit.
  THE BLADE    otherwise unchanged: the greatsword's blow and its onHit
               hemorrhage 2, to hemorrhage's own ceiling of 4.

THE CHARGE. The design states none; its lab cast every 16s of its own step
clock (`ult_overlay`'s default). Rick, 2026-09-27, for the whole batch: "use
the game's equivalent". Measured for this fighter on the lab's arm B (v114
§0: the census).

THE READINGS, where the build had to choose and the doc or the engine decides:
  1. THE WINDOW IS 8s: the design says "for a duration" and names no number;
     its lab ran `ult_overlay`'s default window, 8, and that is what was priced.
  2. THE STACKS ARE THE STRUCK FIGHTER'S, READ AT THE BLOW, before its own
     onHit (§4, explicit: `foe.stacks("hemorrhage")` in resolveHit, "read
     BEFORE this blow's own application (the blow pays on the stacks it found,
     then bleeds)"). The lab set `w.dmg` from the opponent's stacks at the end
     of the previous step. The two differ only where (a) the foe's bleed
     expires in this step's tickStatus before the blow, or (b) the blow lands
     on a Twinshade shade, which pays on the shade's own stacks (the lab's
     `w.dmg` carried the opponent's). §4's prose is explicit, so it is built.
  3. THE MULTIPLIER SITS INSIDE THE PRODUCT, on the blade itself, ahead of
     the jitter, the crit and the rounding -- where the lab scaled `w.dmg` --
     so a blow is bit-identical to the lab's for the same stack count (the
     tree's line, v99 reading 3). The curse echo and a garrote's consume are
     not scaled (they were not in the lab either).
  4. THE SHARED WEAPON IS NEVER WRITTEN (the lab wrote `w.dmg` every frame;
     `w` is shared by the mirror match). The builder refuses any insert that
     writes it.
  5. THE WINDOW CLOSES BY ITS CLOCK OR ON A DEATH THAT `tickPrice` SEES (the
     lab's close is either death). A kill landed later in the same step (a
     blow in `tickHits`, after the window tickers) ends the match with the
     window still set: `step` runs no ticker after `over`, and nothing in the
     simulation reads `ultPrice` then. A picture drawn off it must stop at
     `over`.
  6. NO WAIT CLAUSE. Charge 14 against a window of 8 on one clock cannot
     overlap (the probe asserts it, and that every cast comes exactly 14 s of
     the caster's live clock after the last; it pins 14 and 8 from ULT below).
  7. THE CARD IS WRITTEN AT STAGE 1: the stub is the new ult block, and the
     beam's card would describe a cast that is gone. 69 characters (§4 prints
     "(69)").
  8. THE BEAM'S PICTURE, VOICE AND FIELD STILL PLAY AT THE CAST in stages 2-5:
     `drawUltUnder`'s pool and `drawUltOver`'s seam (`u.w === "oathwound"`),
     the rune-crack fallback voice (Goreshard has no ult arm of its own),
     `SPECS.oathwound`'s beam field and the charge sigil `ULTSIG.oathwound`
     are keyed on the relic, not the kind. Stage 6 (the design's stage 3:
     "the beam art is retired") retires the pool, the seam and the sigil and
     adds the cast's own voice (readings 13-21); `SPECS.oathwound` goes at the
     carry (reading 15). Nothing in the simulation reads any of them. The
     beam had no `radius`, so fireUlt's record is as it was.
  9. EVERY BLOW OF THE CASTER'S takes the multiplier -- whatever reaches
     resolveHit's damage line with its window open, as every read of the
     lab's `w.dmg` did. Goreshard has no projectile, so these are its melee
     blows (on the opponent, or on a shade).
  10. NOTHING ELSE: no status, no stop, no beat, no float, no knock and no
     heal of the price's own. The scaled blow is an ordinary blow: its knock,
     hitstun and stop are the engine's rules applied to its damage, as they
     were to the lab's scaled `w.dmg`. The cast keeps `fireUlt`'s common
     banner, 0.08 stop and ult beat.
  11. THE PRICE LIFTS NO CAP. §1 prices "cap 4 -> up to +120%"; §6.3 (whether
     Bloodletting's cap of 8 applies too) is "not priced", so the build takes
     §1's cap 4: hemorrhage's own `maxStacks`, untouched. Flagged for Rick.
  12. THE BLADE IS FOR BALANCE (Rick, 2026-09-29, after the design was
     written: "you pick the blades. do whatevers best for balance."): the
     final blade is the measured point whose win rate both sides
     (`tools/relic_rate.py`, two blocks) is nearest 50%. This replaces §5's
     "confirm 9.17" (the design's own target, measured beside it, v114 §4).
     The design names no other knob, and none moved.

STAGE 6 -- THE PICTURE AND THE VOICE (v81 §4: "Picture: the beam art is
retired. Cast: the blade darkens to arterial red for the window; the blade's
glow SCALES with the foe's current stack count (0 -> 4 maps alpha 0.2 -> 0.8),
so 'harder the more you bleed' is on the sword itself; the damage float on a
scaled blow is drawn larger. Field: blood motes off the blade, both copies.
Sound: cast -- a wet drawn-blade hiss, 0.4s; a scaled blow -- the sword's strike
voice pitched DOWN by the stack count (bigger = lower); close -- nothing.").
Every look and sound is Code's pick on measurements under Rick's "you pick i
overrule" (the picture lab, scratch `gs_rows.py`; `goreshard_voice_lab.py`;
v114 §5). The rows are the labs' own, byte for byte (the S6 table below says
how that is proved).
  13. THE PICTURE HANGS OFF THE FIGHTER (`gore*` fields), never `m.ultFx`:
     that slot is one, and the opponent's cast takes it (open item 25). It is
     driven on the presentation clock (`tickGore`, called from
     tickPresentation), which runs through a hit stop and after `over`.
  14. THE WINDOW IS READ OFF `ultPrice && !over`, with both fighters standing
     (reading 5: about one window in seven is still set at `over`), so the
     blade drains at the verdict; THE CAST IS FOUND BY `priceTally.casts`
     RISING, so fireUlt makes no call for the picture.
  15. NO fx.js FIELD. "Field: blood motes off the blade, both copies" is drawn
     as motes shed off the blade's barbs (`_goreShed`, `drawGoreDrops`: world
     pass, under both balls, placed by shellHash, never the RNG), not a SPECS
     field: a field rides the one ultFx slot, which the picture lab measured
     as Goreshard's at 89 of 107 casts and for a median 0.67 s of an 8 s
     window (7.5%), lost to the opponent's cast 18 times; and a field bursts
     where the cast was, a median 220 units from the blade it is to come off.
     The beam's own `SPECS.oathwound` (a beam field) is retired at the carry,
     out of both copies, by the orchestrator's fx_remove; stage 6 does not
     touch the inlined copy (checked, and refused if it does).
  16. THE GLOW is the blade's own glow sprite (weaponGlow's cache, baked once a
     reach, never per frame), in the school's bright `glow`, added at 0.2 +
     0.15 x the foe's Hemorrhage read live through `stacks` (a pure read),
     eased; the design's 0 -> 4 maps 0.2 -> 0.8.
  17. THE FLOAT on a scaled blow is x(1 + 0.1 x priceN), the stacks the blow
     paid on: `priceN` is 0 on every blow the price did not scale (the window
     shut, the struck body not bleeding, every other relic), so every other
     float is the old size exactly. It REPLACES resolveHit's shared float-size
     line with its own text times that factor: one of the two lines stage 6
     puts on the sim path, and it writes only the float (presentation).
  18. THE SCALED BLOW'S VOICE is the plain strike at the damage dealt (its
     weight, level, jitter and crit the blow's own), every frequency down a
     semitone a stack (SEMI, of five; a major third at 4), held at 4's voice
     above Hemorrhage's cap. It plays for a blow priced on n > 0: a window blow
     on a body with no Hemorrhage is x1 and keeps the plain call. The other
     line on the sim path passes `price: priceN` to that call, before the
     hit-voice line, which follows unchanged for every other blow.
  19. THE CAST'S VOICE is its own arm (DRIP, of four: a Q 5 scrape rising
     2.6 -> 8 kHz in two strokes, three drops chirping off the blade),
     ADDED before the shared rune-crack fallback, which eleven other relics
     still use and which is re-emitted unchanged, last. fireUlt already plays
     `ult/oathwound` once a cast. THE CLOSE plays nothing (the design's "close
     -- nothing").
  20. THE BEAM'S ART IS RETIRED: drawUltUnder's pool and drawUltOver's seam
     (`u.w === "oathwound"`) go, and the charge sigil `ULTSIG.oathwound`
     (it drew a beam and the pool under it) is redrawn as a greatsword that
     reddens as the charge fills. The ultFx `life` entry `oathwound: 1.5` is
     KEPT: it equals the map's default 1.5, and a line other relics' rows
     anchor on is not worth a row that changes nothing.
  21. NOTHING OF IT REACHES THE SIMULATION: no RNG, no spawnFx, no ultFx, no
     Math.random, no call into the simulation, no write but its own `gore*`
     fields, its motes, the renderer's canvas and cache and the synth's nodes;
     the voice and the float its only two lines on the sim path, each whole
     and where it belongs. The probe's [11]-[12] and engine_ab (all 38 relics,
     Goreshard included) are the dynamic proof.

WHAT IS RETIRED, and what is not. Goreshard's beam block (dmg 16, apply
hemorrhage 3, its card) is deleted. `kind:"beam"` has no cast branch of its own
-- it resolves in `fireUlt`'s generic tail, which every non-returning kind
shares -- and Aureole's Benediction is still a beam on this base. The builder
reads who else is a beam and never refuses on it (Aureole's redesign takes her
off the beam too, and may be carried first).

THE CLOCK. The window runs on the window tickers' clock, which stops through a
hit stop (Corollary's, Daybreak's, Zenith's, Canopy's, Onslaught's, Tendril's
and Exsanguinate's convention). The lab's window ran 8 step-seconds, frozen
ones included (v114 §2 measures what that is worth).

THE BASE is asserted by content (the features this builder needs), never by
which relic is last, so the links re-apply onto a later tip that carries other
new relics.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
CHAIN = HERE.parent / "02-chain"
PROTECTED = "sundered-crown.html"

RELIC = "oathwound"

# THE NUMBERS, AND THE ONLY PLACE THEY LIVE (CLAUDE.md §4.9).
ULT = {
    "charge": 14,     # the lab's 16 on the game's clock (Rick's batch ruling; measured, v114 §0)
    "dur": 8,         # the lab's window ("for a duration"; reading 1)
    "perStack": 0.3,  # v81 §1: "x (1 + 0.30 x foe hemorrhage stacks)" (the lab's default 0.12 is not it)
}
TIP = "Its blows hit harder the more the foe bleeds: +30% a Hemorrhage stack"   # v81 §4 (69)
# THE SHIPPED ROW, the donor of every number this build keeps.
SHIP_HEAD = ('''  { id:"oathwound", name:"Goreshard", aff:"bloodsworn", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, spin:3.4, mode:"swing", arc:1.5, mass:3.0, dmg:9.17,
    onHit:{ hemorrhage:2 },
''')
SHIP_BLADE = 9.17
SHIP_ULT = ('''    ult:{ name:"Bloodprice", charge:14, kind:"beam", dmg:16, apply:{hemorrhage:3},
          tip:"Deals 16 damage and applies 3 Hemorrhage stacks" },
''')

# ---------------------------------------------------------------- stage 5 --
# THE BLADE, FOR BALANCE (reading 12). Both sides, two blocks, 1480 fights a
# point (relic_rate on stage 2's link, every other relic a foe; v114 §4):
# 9.17 -> 43.2, 9.5 -> 45.8, 9.75 -> 46.7, 10 -> 48.3, 10.25 -> 50.2,
# 10.5 -> 50.7, 10.75 -> 53.6. 10.25 is the measured point nearest 50%
# (Rick, 2026-09-29: "you pick the blades. do whatevers best for balance."),
# inside the greatsword row (7.42-12.65). The design's own target, "confirm
# 9.17", reads 43.2 here; the shipped beam at 9.17 reads 35.3 on the same
# fights. The design names no other knob, and none moved.
TUNED = {"dmg": 10.25}


def ult_block(charge) -> str:
    return (f'''    /* BLOODPRICE, REDESIGNED (v81; built v114): the beam is gone. For
       `dur` seconds every blow Goreshard lands is x(1 + perStack x the struck
       fighter's Hemorrhage stacks, read before the blow's own onHit) --
       resolveHit's damage line. */
    ult:{{ name:"Bloodprice", charge:{charge}, kind:"price", dur:{ULT["dur"]}, perStack:{ULT["perStack"]},
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
# THE BEAM OUT OF THE ROW, THE NEW BLOCK IN, STUBBED at charge 1e9: the clock
# can never reach it and `fireUlt` never runs, so this is the lab's arm A (the
# relic with its ultimate suppressed) and must equal it fight for fight.
S1 = [
("Bloodprice's beam block out, the price's block in, stubbed",
 SHIP_ULT,
 ult_block("1e9")),
]

# ---------------------------------------------------------------- stage 2 --
# The anchors compose with the batch's other builds: the fields go after a
# stable line, the cast before an existing branch, the ticker after Tendril's
# call, the method before `tickWinnow`, and the price is a clause inserted
# after the tree's (the Angelus build on the batch line inserts its own clause
# at the same place: either order reads the same).
PRICE_READ_ANCHOR = '''    const jitter = 1 + (this.rng() - 0.5) * C.dmgJitter;
'''
PRICE_LINE_ANCHOR = '''    let dmg = (self.ultTree ? self.w.dmg * self.w.ult.winDmg : '''
# THE PRICE ITSELF, as a `*_NEW` constant so chain_audit can see it. The clause
# is a partial line (no newline), and chain_audit's table pass skips any insert
# body without one (open item 31's failure: v114's review, 2026-09-30, deleted
# the clause from a copy of the final link and chain_audit still printed "ALL 8
# INSERTS SURVIVE"). Its source pass reads `NAME_NEW = ANCHOR + '''...'''` and marks
# the clause by its own text.
PRICE_CLAUSE_NEW = PRICE_LINE_ANCHOR + '''self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : '''
S2 = [

("the price has a charge: the lab's 16 on the game's clock",
 f'''    ult:{{ name:"Bloodprice", charge:1e9, kind:"price", dur:{ULT["dur"]}, perStack:{ULT["perStack"]},
''',
 f'''    ult:{{ name:"Bloodprice", charge:{ULT["charge"]}, kind:"price", dur:{ULT["dur"]}, perStack:{ULT["perStack"]},   // v81 stage 1: the price
'''),

("the fighter carries the price's window",
 '''    this.vineTally = null;
''',
 '''    this.vineTally = null;
    /* {t, dur} while BLOODPRICE's window is open (v81). null on every other
       relic and on this one outside its window: `tickPrice` returns after a
       two-iteration loop that does nothing, and `resolveHit` reads it once a
       blow. `priceTally` is the probe's count, cumulative over the fight;
       nothing in the simulation reads it. */
    this.ultPrice = null;
    this.priceTally = null;
'''),

("the blow reads the stacks it found, before its own onHit",
 PRICE_READ_ANCHOR,
 PRICE_READ_ANCHOR + '''    /* BLOODPRICE (v81 §4): THE BLOW PAYS ON THE STACKS IT FOUND, THEN BLEEDS.
       The struck fighter's Hemorrhage, read here -- after this blow's two
       draws and before its own onHit below -- and priced into the blade on
       the damage line. 0 whenever the window is shut, and on every other
       relic (`ultPrice` is null), so theirs is the same product. */
    const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;
    if (self.ultPrice){ self.priceTally.blows++; self.priceTally.stk += priceN; }
'''),

("the blade is x(1 + perStack x the stacks it found), inside the product",
 PRICE_LINE_ANCHOR,
 PRICE_CLAUSE_NEW),

("the cast opens the window and resolves nothing",
 '''    if (u.kind === "tendril"){
''',
 '''    if (u.kind === "price"){
      /* BLOODPRICE (v81). NOTHING RESOLVES HERE: no damage, no status -- the
         beam's dmg and apply are gone from the row. The cast opens the window
         for `u.dur` seconds, and `resolveHit` prices every blow in it. */
      f.ultPrice = { t: 0, dur: u.dur };
      if (!f.priceTally)
        f.priceTally = { casts: 0, frames: 0, foeStk: 0, blows: 0, stk: 0 };
      f.priceTally.casts++;
      return;
    }
    if (u.kind === "tendril"){
'''),

("the window ticks with the window tickers",
 '''    this.tickTendril(dt);               // TENDRIL (v68)
''',
 '''    this.tickTendril(dt);               // TENDRIL (v68)
    this.tickPrice(dt);                 // BLOODPRICE (v81)
'''),

("tickPrice keeps the window's clock",
 '''  tickWinnow(dt){
''',
 '''  /* ================================================ BLOODPRICE ========
     v81 §1/§4. The window's clock and nothing else: the price itself is in
     `resolveHit`'s damage line, where the blow is. On the window tickers'
     clock, so it stops through a hit stop. The window closes by its clock or
     on a death this ticker sees. A kill landed later in the same step
     (`tickHits`) ends the match with the window still set: `step` runs no
     ticker after `over`, and nothing in the simulation reads `ultPrice` then
     -- a picture drawn off it must stop at `over`. The probe's window-frame
     counts live here; nothing in the simulation reads them. */
  tickPrice(dt){
    for (const f of [this.a, this.b]){
      const Z = f.ultPrice;
      if (!Z) continue;
      const foe = f === this.a ? this.b : this.a;
      Z.t += dt;
      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultPrice = null; continue; }
      f.priceTally.frames++;
      f.priceTally.foeStk += foe.stacks("hemorrhage");
    }
  }

  tickWinnow(dt){
'''),

]


def s5_edits(blade) -> list:
    """The blade, as a module-level table (chain_audit reads tables, not
    functions): the shipped row's head with the blade Rick's ruling measured."""
    return [
        ("the blade: nearest 50% both sides (Rick's ruling, reading 12)",
         SHIP_HEAD,
         SHIP_HEAD.replace(f"dmg:{SHIP_BLADE},", f"dmg:{blade},")),
    ]


S5 = s5_edits(TUNED["dmg"]) if TUNED["dmg"] is not None else []

# ---------------------------------------------------------------- stage 6 --
# THE PICTURE AND THE VOICE (v81 §4's picture and sound; its §5 brief stage 3,
# "picture, voice, carry; beam's field spec out"), picked on measurements under
# Rick's "you pick i overrule" by the picture lab (scratch, `gs_rows.py`) and
# `goreshard_voice_lab.py` (v114 §5). PRESENTATION ONLY: engine_ab over all 38
# relics, Goreshard included, is the proof, and the probe's [11]-[12] read the
# voices and the picture's hook inside the fight. The rows are byte-exact to the
# labs' own files (voice 780b26fd136cfa59, 3 rows; picture 1b95d5d4e1c71ed6, 10
# rows); the picture rows alone reproduce the picture lab's stamp
# (1f0248fee32086ba), the voice rows alone the voice lab's page
# (8323dc9c2a8302b5), and the two sets give the same bytes in either order
# (f063e05c0f721d54). No two rows share an anchor line, so none is merged.
#   THE VOICE: the scaled blow's branch before the plain hit arm (taken only
#   with `price`), the cast's arm before the shared rune-crack fallback (which
#   is re-emitted unchanged, last), and one line on the sim path, before
#   resolveHit's hit-voice line: a blow priced on n > 0 passes `price: priceN`.
#   THE PICTURE: `tickGore` in tickPresentation (the red's run and drain, the
#   glow's ease toward 0.2 + 0.15 x the foe's Hemorrhage, the motes); the
#   blade in drawWeapon; the motes in the world pass under both balls; the
#   priced blow's float x(1 + 0.1 x priceN); the beam's art retired
#   (drawUltUnder's pool, drawUltOver's seam, the charge rune redrawn).
# COMPOSITION: nine anchors are re-emitted and four replaced: three
# Goreshard's own (the pool, the seam, ULTSIG.oathwound), and resolveHit's
# shared float-size line, replaced by its own text with the price's factor on
# it (x1 exactly wherever `priceN` is 0: every other relic's blow).
# The rows ride on two of stage 2's own lines (the fields, tickPrice's end)
# and on shared lines every stage 6 of the batch uses as `after` / `before`
# anchors (tickPresentation's first call, drawWeapon's tree hook, the world
# pass's drawTree, drawMotes, the rune-crack fallback, the plain hit arm).
S6 = [

('Sfx: the scaled blow -- a branch before the plain hit arm, taken only with `price`',
 '''      else if (kind === "hit"){''',
 '''      else if (kind === "hit" && p.price){
        /* BLOODPRICE'S SCALED BLOW -- v81 s4: "a scaled blow -- the sword's
           strike voice pitched DOWN by the stack count (bigger = lower)".
           SEMI, of 5, picked on the numbers by `goreshard_voice_lab.py` under
           Rick's "you pick i overrule" (v114). `resolveHit` adds `price` (the
           Hemorrhage stacks the blow was priced on, 1-4) only to a scaled
           Goreshard blow, so every other call takes the arms below, byte for
           byte.

           The strike as the plain arm plays this blow -- at the damage dealt,
           so its weight, level, jitter and crits are the blow's -- with every
           frequency x 2^(-100 n / 1200): a semitone a stack, a major third at
           4. Against the plain hit at the same damage it falls 82/200/316/422
           cents on the crack and 102/204/307/409 on the body at 1-4 stacks; at
           2 and 4 (the counts a window has) that is 1.5 and 1.9 x what the
           damage roll moves the plain hit by. Its peak within 0.9 dB of the
           plain hit's; register 0.73 with it at 4 stacks (still that voice),
           0.97 against the death voice. Held at 4's voice above 4
           (Hemorrhage's cap). */
        const w = clamp((p.dmg || 10) / 45, 0.12, 1), n = Math.min(p.price, 4), k = Math.pow(2, -n * 100 / 1200);
        this._burst(t, { freq: (2600 - 1500*w) * k, q: 1.1, gain: 0.16 + 0.20*w, dur: (0.06 + 0.06*w) });
        this._tone (t, { freq: (190 - 90*w) * k, to: 46 * k, gain: 0.22 + 0.26*w, dur: (0.11 + 0.13*w), type:"sine" });
        if (p.crit) this._tone(t, { freq: 1500 * k, to: 520 * k, gain: 0.16, dur: 0.16, type:"triangle" });
      }
      else if (kind === "hit"){'''),

("Sfx: Goreshard's cast arm, before the shared rune-crack fallback",
 '''        } else {                                        // rune-crack''',
 '''        } else if (w === "oathwound"){                  // the blade drawn, wet
          /* GORESHARD'S CAST, BLOODPRICE -- v81 s4: "cast -- a wet drawn-blade
             hiss, 0.4s". DRIP, of 4, picked on the numbers by
             `goreshard_voice_lab.py` under Rick's "you pick i overrule"
             (v114). Goreshard had no arm and fell through to rune-crack, which
             eleven other relics on its stage-5 link still use, so this ADDS an
             arm before that fallback and leaves it alone. The beam it replaces
             had no voice of its own.

             The draw: a scrape (bandpass noise, Q 5) rising 2.6 -> 8 kHz in
             two overlapping strokes -- a single `_sweep` runs to an absolute
             1e-4 and cannot be audible 0.4 s at a blow's level -- climbing
             +997 cents from its first 100 ms to its last and swelling in 194
             ms (drawn, not struck); 0.96 of its power at 2 kHz and up. Under
             it, three drops off the blade as it clears, each a sine chirping
             up 1.5x: 0.03 of the power at 150-1500 Hz, gliding over 804 cents.
             Audible 400 ms; its top -2.8 dB re Goreshard's blow, heard +36.4
             dB over the score. Register at most 0.71 (woosh) against
             rune-crack, the bloodsworn and greatsword casts, the tornado's
             woosh, the blow and the death voice, and Widowmaker's cast, and
             Lightkeeper's cast, and Heartwood's cast. */
          const g = 0.5095, kw = 0.03921;
          this._sweep(t, { f0: 2600, f1: 4600, q: 5, gain: g, dur: 0.36, atk: 0.08, type:"bandpass" });
          this._sweep(t + 0.16, { f0: 4100, f1: 8000, q: 5, gain: g, dur: 0.49, atk: 0.1, type:"bandpass" });
          for (const [s, f] of [[0.17, 760], [0.25, 880], [0.31, 1010]])
            this._tone(t + s, { freq: f, to: f * 1.5, gain: g * kw, dur: 0.08, type:"sine" });
        } else {                                        // rune-crack'''),

("resolveHit: a scaled blow's hit voice carries `price` (priceN > 0), before the hit-voice line",
 '''    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });''',
 '''    /* BLOODPRICE'S SCALED BLOW (v81 s4: "a scaled blow -- the sword's strike
       voice pitched DOWN by the stack count (bigger = lower)"): ONE plain
       number more, `price`, the Hemorrhage stacks this blow was priced on
       (`priceN`, read above, before its own onHit), and only when it is > 0:
       a window blow on a body with no Hemorrhage is x1 and keeps the plain
       call. `priceN` is 0 whenever the window is shut and on every other
       relic, so they take the `else` -- the line below, Canopy's call,
       unchanged. `dmg` stays what was dealt. Reads priceN, dmg and crit;
       writes nothing. Presentation only (goreshard_voice_lab: fights
       identical). */
    if (priceN > 0) SFX.play("hit", { dmg, crit, price: priceN });
    else
    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });'''),

('bloodprice picture: fighter fields',
 '''    this.ultPrice = null;
    this.priceTally = null;
''',
 '''    this.ultPrice = null;
    this.priceTally = null;
    /* BLOODPRICE'S PICTURE (v81 section 4), and none of it is the window:
       the red outlives `ultPrice` by its drain, and a mote by its fall. On
       the FIGHTER and never on `m.ultFx` (one slot, and the opponent's cast
       takes it: open item 25). Driven in `tickPresentation` (`tickGore`);
       nothing in the simulation reads any of it.
         goreFade  -- 1 while the window is open and the match is on; eased
                      to 0 over the drain after the close, the caster's fall
                      or the match's end
         goreAge   -- the presentation clock since the cast (the red's run)
         goreOut   -- the presentation clock since the close (the drain);
                      0 while the window is open
         goreGlow  -- the blade's glow alpha, eased toward 0.2 + 0.15 x the
                      foe's Hemorrhage stacks, read live
         goreSeen  -- `priceTally.casts`, as last seen (a cast is it rising)
         goreAcc, goreDropN -- the motes' emission clock and their count
         goreDrops -- the blood motes in flight, in world space
         goreTh, goreT, goreW -- theta and the match clock at the last look,
                      and the blade's sweep (rad/s) they give */
    this.goreFade = 0;
    this.goreAge = 0;
    this.goreOut = 0;
    this.goreGlow = 1;
    this.goreSeen = 0;
    this.goreAcc = 0;
    this.goreDropN = 0;
    this.goreDrops = [];
    this.goreTh = 0;
    this.goreT = -1;
    this.goreW = 0;
'''),

('bloodprice picture: the presentation call',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
''',
 '''  tickPresentation(dt){
    this.tickNovaFx(dt);
    this.tickGore(dt);                 // BLOODPRICE'S PICTURE (v81 section 4)
'''),

('bloodprice picture: tickGore',
 '''      f.priceTally.foeStk += foe.stacks("hemorrhage");
    }
  }
''',
 '''      f.priceTally.foeStk += foe.stacks("hemorrhage");
    }
  }

  /* ------------------------------------------------ BLOODPRICE'S PICTURE ---
     v81 section 4, on the presentation clock. HALF-SECONDS, like every
     `life` in `tickPresentation` (it runs twice a normal step and once in a
     hit stop): 0.6 is the cast's 0.3s run of red from the guard to the
     point, 0.7 the close's 0.35s drain, 0.16 the glow's ease, 1.3 a
     mote's life. THE WINDOW IS READ OFF `ultPrice && !over`, with both
     fighters standing: `tickPrice` never runs again once `over` is set, and
     about one window in seven is still set when the match ends (the kill
     lands in `tickHits`, after `tickPrice`), so the blade drains at the
     verdict instead of holding red through the panel. THE CAST IS FOUND BY
     WATCHING `priceTally.casts` RISE, so `fireUlt` makes no call for the
     picture. THE GLOW reads the foe's Hemorrhage live (`stacks` is a pure
     read): 0.2 + 0.15 a stack, as v81 maps it. THE MOTES are shed off the
     four back-edge barbs and the point in turn while the window is open,
     jittered by shellHash on their count, carrying a third of the blade's
     sweep, and fall. Writes presentation fields only; no rng. */
  tickGore(dt){
    for (const f of [this.a, this.b]){
      const T = f.priceTally;
      if (!T) continue;                                       // <- zero burden
      const foe = f === this.a ? this.b : this.a;
      /* the blade's sweep, off the match clock (it runs in a hit stop too,
         where theta holds and this reads 0) */
      if (this.t !== f.goreT){
        if (f.goreT >= 0) f.goreW = (f.theta - f.goreTh) / (this.t - f.goreT);
        f.goreTh = f.theta; f.goreT = this.t;
      }
      const open = !!f.ultPrice && !this.over && f.alive && foe.alive;
      if (T.casts !== f.goreSeen){
        f.goreSeen = T.casts;
        if (open){ f.goreAge = 0; f.goreOut = 0; f.goreGlow = 1; }   // a cast
      }
      if (open){
        f.goreFade = 1; f.goreOut = 0;
        f.goreAge += dt;
        const n = Math.min(4, foe.stacks("hemorrhage"));
        f.goreGlow += (0.2 + 0.15 * n - f.goreGlow) * Math.min(1, dt / 0.16);
        f.goreAcc += dt * 5;
        while (f.goreAcc >= 1){
          f.goreAcc -= 1;
          this._goreShed(f);
        }
      } else if (f.goreFade > 0){
        f.goreOut += dt;
        f.goreFade = Math.max(0, 1 - f.goreOut / 0.7);
      }
      for (let i = f.goreDrops.length - 1; i >= 0; i--){
        f.goreDrops[i].t += dt;
        if (f.goreDrops[i].t >= 1.3) f.goreDrops.splice(i, 1);
      }
    }
  }

  /* one mote, off a barb's hooked tip (or the point), where `_gsBarbed`
     draws it this frame: the blade's own frame turned into the hall's */
  _goreShed(f){
    const R = CONFIG.physics.ballR, L = f.w.reach * this.actMods.reach * f.reachMul + 6;
    const bh = f.w.artW * 0.19, n = f.goreDropN++, j = n % 5;
    const h1 = shellHash(8111 + f.side, n), h2 = shellHash(8117 + f.side, n);
    const lx = j < 4 ? L * (0.34 + 0.14 * j) - L * 0.075 + (h1 - 0.5) * L * 0.05 : L * (0.97 + 0.03 * h1);
    const ly = j < 4 ? bh * 2.1 : (h1 - 0.5) * bh;
    const a = f.theta + (f.bladeSet || f.w.blades)[0] * TAU, ca = Math.cos(a), sa = Math.sin(a);
    const rx = R - 6 + lx;
    const x = f.x + ca * rx - sa * ly, y = f.y + sa * rx + ca * ly;
    /* a third of the sweep at that radius, and a little out along the blade */
    const w = clamp(f.goreW, -12, 12) * 0.33, rr = Math.hypot(rx, ly);
    const vx = -sa * w * rr + ca * (10 + 30 * h2), vy = ca * w * rr + sa * (10 + 30 * h2) - 20;
    f.goreDrops.push({ x, y, vx, vy, t: 0, n });
    if (f.goreDrops.length > 40) f.goreDrops.shift();
  }
'''),

("bloodprice picture: drawWeapon's blade hook",
 '''    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;
''',
 '''    if ((f.treeFade > 0 || f.ultTree) && this.drawTreeWeapon(m, f, reach, dim)) return;
    /* BLOODPRICE (v81 section 4): through the window, and the drain after
       it, the blade draws itself (`drawGoreWeapon`) -- arterial red, its glow
       following the foe's Hemorrhage -- off the same blade set, reach and
       angles `bladeSegments` tests. `goreFade` is 0 on every other relic, so
       this is one comparison on a field nothing else writes. `w` is never
       written: it is the mirror match's too. */
    if (f.goreFade > 0 && this.drawGoreWeapon(m, f, reach, dim)) return;
'''),

("bloodprice picture: the motes' call (world, under both balls)",
 '''    if (__world) this.drawTree(m);
''',
 '''    if (__world) this.drawTree(m);
    /* BLOODPRICE'S MOTES (v81 section 4: "blood motes off the blade"): shed
       off the barbs for the window and falling. The WORLD pass and under both
       balls: nothing of it reaches the bloom (CLAUDE.md section 4.1c) and no
       ball's disc is painted over (4.1b). */
    if (__world) this.drawGoreDrops(m);
'''),

('bloodprice picture: the drawing methods',
 '''  drawMotes(m){
''',
 '''  /* ================================================ BLOODPRICE ========
     v81 section 4: "the beam art is retired. Cast: the blade darkens to
     arterial red for the window; the blade's glow SCALES with the foe's
     current stack count (0 -> 4 maps alpha 0.2 -> 0.8), so 'harder the more
     you bleed' is on the sword itself; the damage float on a scaled blow is
     drawn larger. Field: blood motes off the blade."

     THE CAST: the red runs down the blade from the guard to the point in
     0.3s, a bright front crossing it, fastest at the start: it is moving
     inside the cast's own stop. THE WINDOW: the blade is arterial red
     (the school's steel swapped for "#D02A40": the blade, its barbs and its
     swept guard; the honed edge, grip, pommel and the fed notch are the
     school's own, so the barbed silhouette reads as it does at rest), and
     its glow climbs as the foe bleeds and sinks as the bleed runs out: the
     blade's own glow sprite, baked off it at 1.6x its width, in the school's
     bright `glow` instead of its `core`, ADDED (`lighter`, the world pass:
     nothing of it reaches the bloom) at 0.2 + 0.15 a foe stack. Baked once
     by `weaponGlow`'s own cache (one more key a reach), never per frame; the
     alpha is the blit's. Measured (gs_explore): the stacks' 0.2 -> 0.8
     moves three times the pixels, three times as far, as the rest sprite's
     red would (|dL| 0.109 on 8130 px against 0.036 on 2566; 0.076 on 5353
     at the rest sprite's own width). THE CLOSE: the red drains back from the point
     into the guard in 0.35s, and the glow crossfades back to the rest
     pose's. The float is `resolveHit`'s own, larger.

     IT HANGS OFF THE FIGHTER (`goreFade`, `goreAge`, `goreOut`, `goreGlow`,
     `goreDrops`), never `m.ultFx` (open item 25). PRESENTATION ONLY: no rng,
     no spawnFx, no Math.random -- shellHash and the clocks -- and nothing
     here writes a field the simulation reads. */
  drawGoreWeapon(m, f, reach, dim){
    const c = this.ctx, R = CONFIG.physics.ballR, L = reach + 6, W = f.w.artW;
    const run = !(f.goreOut > 0);
    /* the run eases OUT, so the red is already a third of the way down the
       blade inside the cast's own 0.08s stop (this clock runs through it);
       the drain eases in and out */
    const u = run ? clamp(f.goreAge / 0.6, 0, 1) : 1 - clamp(f.goreOut / 0.7, 0, 1);
    const e = run ? 1 - (1 - u) * (1 - u) : u * u * (3 - 2 * u);
    const x1 = L * (0.13 + 0.92 * e);                    // the red's front, from the guard
    const P = this._gorePal(f.aff, 0);
    for (const off of (f.bladeSet || f.w.blades)){
      const a = f.theta + off * TAU;
      c.save();
      c.translate(f.x, f.y);
      c.rotate(a);
      c.translate(R - 6, 0);
      this._goreGlow(c, f, L, W, e, dim);
      c.globalAlpha = dim;
      if (x1 < L * 1.02) this._goreSteel(c, f, L, W, a, f.aff, null);
      if (x1 > L * 0.14) this._goreSteel(c, f, L, W, a, P, x1 < L * 1.02 ? x1 : null);
      if (e > 0.02 && e < 0.98) this._goreFront(c, f, L, W, x1, dim * (run ? 1 - e * 0.5 : 0.5));
      c.restore();
    }
    return true;
  }

  /* the school's palettes for the window, cached per school: 0 the blade
     (its steel arterial), 1 the glow (its `core` -- the colour `weaponGlow`
     bakes -- the school's bright `glow`) */
  _gorePal(aff, k){
    const C = this._gorePals || (this._gorePals = {}), id = aff.key + k;
    return C[id] || (C[id] = Object.assign({}, aff, k ? { core: aff.glow } : { steel: "#D02A40" }));
  }

  /* THE GLOW: the rest pose's own sprite fading out as the red runs in (and
     back as it drains), and the window's, added at the stacks' alpha */
  _goreGlow(c, f, L, W, e, dim){
    if (e < 0.999){
      const g0 = weaponGlow(f.w.shape, L, W, f.aff, f.drawK, 20);
      c.globalAlpha = dim * (1 - e);
      c.drawImage(g0.cv, g0.ox, g0.oy);
    }
    if (e > 0.001){
      const g = weaponGlow(f.w.shape, L, W * 1.6, this._gorePal(f.aff, 1), f.drawK, 18);
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = clamp(dim * e * f.goreGlow, 0, 1);
      c.drawImage(g.cv, g.ox, g.oy);
      c.restore();
    }
  }

  /* THE BLADE in a palette, clipped behind the red's front when it has one */
  _goreSteel(c, f, L, W, a, P, x1){
    if (x1 != null){
      c.save();
      c.beginPath(); c.rect(-L * 0.2, -W * 3, x1 + L * 0.2, W * 6); c.clip();
    }
    if (!litWeapon(c, f.w.shape, L, W, P, f.drawK, a)){
      const fn = SHAPES[f.w.shape];
      if (fn) fn(c, L, W, P, f.drawK);
    }
    if (x1 != null) c.restore();
  }

  /* THE FRONT: a bright seam across the blade where the red has reached */
  _goreFront(c, f, L, W, x1, al){
    const bh = W * 0.19, xs = Math.min(x1, L * 0.995);
    const hh = xs < L * 0.795 ? bh * 1.05 : bh * 0.9 * (L - xs) / (L * 0.205) + 1;
    c.globalAlpha = clamp(al, 0, 1);
    c.strokeStyle = f.aff.glow; c.lineWidth = Math.max(1.5, W * 0.06); c.lineCap = "round";
    c.beginPath(); c.moveTo(xs, -hh); c.lineTo(xs, hh); c.stroke();
  }

  /* THE MOTES: drops of blood off the barbs, falling, each drawn along its
     own velocity with a dark rim, so it reads on a white foe as well as on
     the floor. Clipped to the hall. */
  drawGoreDrops(m){
    const a = m.a, b = m.b;
    if (!a.goreDrops.length && !b.goreDrops.length) return;   // <- zero burden
    const c = this.ctx, A = CONFIG.arena, n = m.inset || 0;
    c.save();
    c.beginPath(); c.rect(n, n, A.w - 2 * n, A.h - 2 * n); c.clip();
    for (const f of [a, b]){
      for (const q of f.goreDrops){
        const s = q.t * 0.5, k = q.t / 1.3;
        const x = q.x + q.vx * s, y = q.y + q.vy * s + 560 * 0.5 * s * s;
        const vx = q.vx, vy = q.vy + 560 * s, sp = Math.hypot(vx, vy) || 1;
        const r = 1.7 + 0.9 * shellHash(8123 + f.side, q.n), st = Math.min(5, sp * 0.012);
        c.save();
        c.translate(x, y); c.rotate(Math.atan2(vy, vx));
        c.globalAlpha = clamp((1 - k) * 1.5, 0, 1) * Math.min(1, k * 10 + 0.2);
        c.fillStyle = "#3A0610";
        c.beginPath(); c.ellipse(-st * 0.5, 0, r + 0.9 + st, r + 0.9, 0, 0, TAU); c.fill();
        c.fillStyle = f.aff.core;
        c.beginPath(); c.ellipse(-st * 0.5, 0, r + st, r, 0, 0, TAU); c.fill();
        c.restore();
      }
    }
    c.restore();
  }

  drawMotes(m){
'''),

("bloodprice picture: the priced blow's float, larger",
 '''    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1);
''',
 '''    /* BLOODPRICE (v81 section 4): "the damage float on a scaled blow is
       drawn larger" -- x(1 + 0.1 x the stacks the blow paid on). `priceN`
       is 0 on every blow the price did not scale (its window shut, the struck
       body not bleeding, every other relic), and x1 is exact, so every other
       float is the old size. Presentation only: `floats` is aged, drawn and
       lerped, and nothing in the simulation reads it. */
    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);
'''),

("bloodprice picture: the beam's pool retired",
 '''    /* ---- Bloodprice: what runs out of the wound, on the floor -------------- */
    else if (u.w === "oathwound"){
      const open = clamp((u.t - 0.12) / 0.26, 0, 1);
      const fade = 1 - clamp((u.t - 0.6) / 0.85, 0, 1);
      c.globalAlpha = 0.8 * fade * open;
      const g = c.createRadialGradient(u.tx, u.ty + 14, 3, u.tx, u.ty + 14, 108 * open);
      g.addColorStop(0, "#5A0A18EE"); g.addColorStop(0.6, "#3A0610AA");
      g.addColorStop(1, "#3A061000");
      c.fillStyle = g;
      c.beginPath(); c.ellipse(u.tx, u.ty + 14, 108 * open, 46 * open, 0, 0, TAU); c.fill();
      /* rivulets: the pool does not stay a circle */
      for (let i = 0; i < 7; i++){
        const a = shellHash(31, i) * TAU;
        const len = 60 * open * (0.5 + shellHash(32, i));
        c.globalAlpha = 0.6 * fade * open;
        c.strokeStyle = "#5A0A18"; c.lineWidth = 4 - shellHash(33, i) * 2;
        this._jag(c, u.tx, u.ty + 14, u.tx + Math.cos(a) * len,
                  u.ty + 14 + Math.sin(a) * len * 0.42, 5, 7, 340 + i, open);
      }
    }
''',
 '''    /* ---- Bloodprice's pool was the BEAM's (the floor under the struck foe,
       and its rivulets, for the record's 1.5); retired with it (v81, v114
       stage 6). The window's picture is the blade itself (`drawGoreWeapon`),
       off the fighter, where the one ultFx slot cannot erase it. */
'''),

("bloodprice picture: the beam's seam retired",
 '''    /* ---- Bloodprice: a seam torn open in the air, and the oath that holds -- */
    else if (u.w === "oathwound"){
      const open = clamp((u.t - 0.08) / 0.22, 0, 1);
      const shut = clamp((u.t - u.life * 0.55) / (u.life * 0.45), 0, 1);
      const fade = 1 - clamp((u.t - 0.5) / 1.0, 0, 1);
      const H = 120, w = 30 * open * (1 - shut);

      /* the wound: a vesica, dark inside, hot at the rim */
      c.save();
      c.translate(u.tx, u.ty);
      c.globalAlpha = Math.max(0, 1 - shut);
      c.beginPath();
      c.moveTo(0, -H);
      c.quadraticCurveTo(w, 0, 0, H);
      c.quadraticCurveTo(-w, 0, 0, -H);
      const wg = c.createLinearGradient(-w, 0, w, 0);
      wg.addColorStop(0, "#3A0610"); wg.addColorStop(0.5, "#120004");
      wg.addColorStop(1, "#3A0610");
      c.fillStyle = wg; c.fill();
      c.strokeStyle = "#FF97A2"; c.lineWidth = 2.6;
      c.shadowColor = "#E03A4E"; c.shadowBlur = 18;
      c.stroke();
      c.shadowBlur = 0;
      c.restore();

      /* it bleeds downward — drops leaving the seam, not thrown outward */
      c.globalCompositeOperation = "source-over";
      for (let i = 0; i < 9; i++){
        const ph = (u.t * 1.3 + shellHash(21, i)) % 1;
        c.globalAlpha = (1 - ph) * fade * 0.9 * open;
        c.fillStyle = "#E03A4E";
        const px = u.tx + (shellHash(22, i) - 0.5) * w * 1.6;
        const py = u.ty - H * 0.3 + ph * (H * 1.5);
        c.beginPath(); c.ellipse(px, py, 2.4, 4.2 + ph * 3, 0, 0, TAU); c.fill();
      }

      /* THE TETHER: a taut thread back to the caster. Straight, not jagged
         — a binding, and the thing Exsanguinate's flung fangs never had.
         (Was "THE OATH" when this relic was Oathwound. The picture did not
         change with the rename; the reason for it did.) */
      c.globalAlpha = 0.75 * fade;
      c.strokeStyle = "#8E1226"; c.lineWidth = 2.4;
      c.shadowColor = "#E03A4E"; c.shadowBlur = 10;
      c.beginPath(); c.moveTo(u.tx, u.ty); c.lineTo(src.x, src.y); c.stroke();
      c.shadowBlur = 0;
      for (let i = 0; i < 3; i++){            // beads running back down it
        const q = (u.t * 0.8 + i / 3) % 1;
        c.globalAlpha = (1 - q) * fade;
        c.fillStyle = "#FF97A2";
        c.beginPath();
        c.arc(lerp(u.tx, src.x, q), lerp(u.ty, src.y, q), 3.2, 0, TAU); c.fill();
      }
    }
''',
 '''    /* ---- Bloodprice's seam was the BEAM's (the wound torn in the air over
       the quarry, its drops and the tether back to the caster); retired with
       it (v81, v114 stage 6). The cast is the red running down the blade. */
'''),

('bloodprice picture: the charge rune',
 '''  /* BLOODPRICE -- a beam, and the toll paid under it. */
  oathwound(c, t, cf, P){
    const g = c.createLinearGradient(-1, 0, 1, 0);
    g.addColorStop(0, P.core + "00"); g.addColorStop(0.55, P.core); g.addColorStop(1, P.glow);
    SG.a(c, 0.35 + cf * 0.6); c.fillStyle = g;
    c.fillRect(-1, -0.16 - cf * 0.06, 2, 0.32 + cf * 0.12); SG.a(c, 1);
    SG.poly(c, [[0, 0.3], [0.24, 0.66], [0, 0.92], [-0.24, 0.66]], P.core, 0.55 + cf * 0.4);
    SG.disc(c, 0.86, 0, 0.11 + cf * 0.06, P.glow, 0.6 + cf * 0.4);
  },
''',
 '''  /* BLOODPRICE -- the sword that is paid in blood. The beam and the pool
     under it went out with the beam (v81): a greatsword laid across the
     rune, reddening from the guard to the point as the charge fills, its
     glow rising with it, and blood running off its edge. */
  oathwound(c, t, cf, P){
    const ux = 0.7071, uy = -0.7071, px = 0.7071, py = 0.7071;
    const gx = -0.40, gy = 0.40, len = 1.50, hw = 0.12;
    const at = (s, d) => [gx + ux * s * len + px * d, gy + uy * s * len + py * d];
    SG.path(c, [at(0.02, 0), at(1, 0)], P.core, 0.46, 0.08 + cf * 0.34);
    SG.path(c, [at(-0.30, 0), at(0, 0)], P.dark, 0.13, 0.9);
    SG.path(c, [at(0, -0.28), at(0, 0.28)], P.core, 0.1, 0.9);
    SG.poly(c, [at(0.03, -hw), at(0.84, -hw * 0.9), at(1, 0), at(0.84, hw * 0.9), at(0.03, hw)], P.steel, 0.9);
    const k = 0.03 + 0.97 * cf;
    if (k > 0.05){
      const e = Math.min(k, 0.84);
      const pts = [at(0.03, -hw), at(e, -hw * (1 - 0.1 * e / 0.84)), at(e, hw * (1 - 0.1 * e / 0.84)), at(0.03, hw)];
      if (k > 0.84) pts.splice(2, 0, at(k, hw * 0.9 * (1 - k) / 0.16), at(k, -hw * 0.9 * (1 - k) / 0.16));
      SG.poly(c, pts, "#D02A40", 0.92);
    }
    for (let i = 0; i < 2; i++){
      const u = (t * 0.7 + i * 0.5) % 1, [x0, y0] = at(0.35 + i * 0.3, hw * 1.2);
      SG.disc(c, x0, y0 + u * 0.55, 0.055, P.core, (1 - u) * (0.25 + cf * 0.7));
    }
  },
'''),

]

# THE STAGE-6 SCANS (readings 13-21). Everything the table's ADDED code may do.
S6_NAMES = ("tickGore", "_goreShed", "drawGoreWeapon", "_gorePal", "_gorePals", "_goreGlow", "_goreSteel",
            "_goreFront", "drawGoreDrops", "goreFade", "goreAge", "goreOut", "goreGlow", "goreSeen", "goreAcc",
            "goreDropN", "goreDrops", "goreTh", "goreT", "goreW")
S6_SFX_ROWS = ("Sfx: the scaled blow", "Sfx: Goreshard's cast arm")
S6_TICK_ROW = "bloodprice picture: tickGore"
S6_DRAW_ROW = "bloodprice picture: the drawing methods"
S6_FIELDS_ROW = "bloodprice picture: fighter fields"     # the Fighter's constructor: `this` is the fighter
# THE TWO LINES ON THE SIM PATH, whole (readings 17 and 18): each row's added
# code, comments stripped, line for line.
S6_SIM_LINES = {
    "resolveHit: a scaled blow's hit voice": ['if (priceN > 0) SFX.play("hit", { dmg, crit, price: priceN });', "else"],
    "bloodprice picture: the priced blow's float": [
        "const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);"],
}
FLOAT_OLD = "    const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1);\n"
HIT_VOICE = '    SFX.play("hit", self.ultTree ? { dmg, crit, bough: self.w.ult.winDmg } : { dmg, crit });\n'
# THE SHARED MODULE TABLES STAGE 6 MAY READ, by exact path, and no other
# reference to one (no write: a table written holds for every later match).
S6_TABLE_READS = ("CONFIG.physics.ballR", "CONFIG.arena", "SHAPES[f.w.shape]")
RUNE_CRACK = "        } else {                                        // rune-crack"
S6_ARM = '} else if (w === "oathwound"){'
PRICED_HIT = 'else if (kind === "hit" && p.price){'
PLAIN_HIT = '      else if (kind === "hit"){\n'
BEAM_GONE = ('u.w === "oathwound"', "BLOODPRICE -- a beam, and the toll paid under it.",
             "Bloodprice: what runs out of the wound", "Bloodprice: a seam torn open in the air")


def inlined_fx(s: str) -> str:
    """The inlined copy of src/render/fx.js, header to THE ULT FIELDS: stage 6
    leaves it alone (reading 15)."""
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


def s6_bound_once(ins: str, name: str, expr: str) -> bool:
    """`name` is bound exactly once in the insert, as `const name = expr` (alone
    or the first of a const list), and bound or assigned nowhere else."""
    decl = "const " + name + " = " + expr
    if len(re.findall(re.escape(decl) + r"[;,]", ins)) != 1:
        return False
    rest = ins.replace(decl, "", 1)
    return not re.search(r"\b(?:const|let|var)\s+" + re.escape(name) + r"\b|[,(]\s*" + re.escape(name)
                         + r"\s*=(?!=)|(?<![\w.$])" + re.escape(name) + r"\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)",
                         rest)


def s6_local_array(ins: str, name: str) -> bool:
    """`name` is the insert's own fresh array: bound once as `const name = [`,
    and bound or assigned nowhere else."""
    return (len(re.findall(r"\bconst " + re.escape(name) + r" = \[", ins)) == 1
            and not re.search(r"\b(?:let|var)\s+" + re.escape(name) + r"\b|(?<![\w.$])" + re.escape(name)
                              + r"\s*(?:=(?!=)|\+=|-=)", ins.replace("const " + name + " = [", "", 1)))


def s6_static_checks() -> None:
    """STAGE 6 IS PRESENTATION (reading 21). Its ADDED code (a row's re-emitted
    anchor aside) draws no RNG, never takes the one ultFx slot (open item 25),
    calls nothing that hurts, applies, resolves, beats, floats or knocks, never
    writes the shared weapon row or a module table (it reads three of them by
    exact path), writes only its own `gore*` fields, its motes' clocks, the
    renderer's canvas and cache and the synth's nodes; mutates only its own
    motes; `SFX` and the float size only in their two sim-path rows, each whole;
    the synth only in the Sfx arms. The probe's [11]-[12] and engine_ab are the
    dynamic proof. Run on every stage: it reads the table."""
    WRITE = r"\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)"
    labels = [lb for lb, _o, _n in S6]
    for want in list(S6_SIM_LINES) + list(S6_SFX_ROWS) + [S6_TICK_ROW, S6_DRAW_ROW, S6_FIELDS_ROW]:
        if sum(1 for lb in labels if lb.startswith(want)) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- the S6 table has no single row '{want}'")
    for label, old, new in S6:
        ins = s6_added(old, new)
        sfx = label.startswith(S6_SFX_ROWS)
        tick = label.startswith(S6_TICK_ROW)
        draw = label.startswith(S6_DRAW_ROW)
        if re.search(r"\brng\b", ins) or "spawnFx" in ins or "ultFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' draws "
                             "the RNG or uses the one ultFx slot")
        if re.search(r"\.(apply|hurt|heal|resolveHit|resolveClank|shatter|fireUlt|knock|beat|float|breakSpin|"
                     r"takeHitstun|tickPrice|tickStatus|tickWeapon|tickHits|tickCharge|spawnShot|spawnSpark|note|"
                     r"checkEnd|statusTag|step|ring|burst)\(", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' calls "
                             "into the simulation")
        if re.search(r"\bw\.[A-Za-z_]\w*(\.\w+)*" + WRITE, ins) or re.search(r"\bw\[", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the "
                             "shared weapon row")
        for mt in re.finditer(r"\b(?:STATUS|CONFIG|AFFINITIES|WEAPONS|SHAPES|ULT_LIFE|ACTS)\b"
                              r"(?:\s*\.\s*[A-Za-z_$][\w$]*|\s*\[[^\]]*\])*", ins):
            if mt.group(0) not in S6_TABLE_READS or re.match(WRITE, ins[mt.end():]):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reaches a shared "
                                 f"module table other than by the reads it may make: {mt.group(0)!r}")
        if re.search(r"\.\s*(beat|beats|hurt|knock|shake|hitStop|pin|stun|stunDR|charge|status|ultPrice|priceTally|"
                     r"hp|alive|over|winner|theta|swingPhase|spinDir|vx|vy|x|y|hitCd|bleedCap|dealt|hits|crits)\b"
                     + WRITE, ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes the window, "
                             "the tally, a status or a body")
        sim = [k for k in S6_SIM_LINES if label.startswith(k)]
        if sim:
            got = [ln.strip() for ln in ins.splitlines() if ln.strip()]
            if got != S6_SIM_LINES[sim[0]]:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6's line on the sim path "
                                 f"('{label}') is not its own text alone:\n{ins}")
        elif re.search(r"\bSFX\b|\bfsz\b|\bfloats\b", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' plays a voice or sizes "
                             "a float outside its two sim-path rows")
        if re.search(r"\b_tone\s*\(|\b_burst\s*\(|\b_sweep\s*\(|\.play\s*\(|\bfrequency\b|"
                     r"\bcreateOscillator\b|\bctx\.destination\b", ins) and not sim and not sfx:
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' strikes the "
                             "synth outside the Sfx arms")
        if re.search(r"\bdelete\s|Object\.(defineProperty|defineProperties|setPrototypeOf)\s*\(", ins) \
                or re.search(r"Object\.assign\s*\((?!\{\}\s*,)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' deletes or "
                             "redefines a property, or assigns into an object it did not make")
        # THE CANVAS: `c` only as the renderer's own context, or a method's first parameter
        for mb in re.finditer(r"\b(?:const|let|var)\s+c\s*=\s*([^,;\n]+)", ins):
            if mb.group(1).strip() != "this.ctx":
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' binds "
                                 f"`c` to {mb.group(1).strip()!r}, not the renderer's context")
        if re.search(r"(?<![\w.$])c\s*=(?!=)", ins.replace("const c =", "")):
            raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' reassigns `c`")
        for mw in re.finditer(r"([\w\]\)]+)\s*\.\s*(\w+)" + WRITE, ins):
            obj, prop = mw.group(1), mw.group(2)
            ok = ((obj == "f" and prop.startswith("gore"))
                  or (obj == "this" and label.startswith(S6_FIELDS_ROW) and prop.startswith("gore"))
                  or (obj == "this" and draw and prop == "_gorePals")
                  or obj == "c"
                  or (tick and obj == "i]" and prop == "t" and "f.goreDrops[i].t += dt;" in ins))
            if not ok:
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes {obj}.{prop}")
        for mw in re.finditer(r"([\w\]\)$.]+)\s*\.\s*(push|splice|pop|shift|unshift|reverse|sort|copyWithin)\s*\(", ins):
            if not ((tick and mw.group(1) == "f.goreDrops") or s6_local_array(ins, mw.group(1))):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' mutates {mw.group(1)}")
        # an index write (a destructuring `const [a, b] = ...` is a declaration, not one): only the
        # renderer's own palette cache, bound once as `const C = this._gorePals || (...)`
        for mi in re.finditer(r"([\w\]\)$]+)\s*\[[^\]]*\]" + WRITE, re.sub(r"\b(?:const|let|var)\s*\[[^\]]*\]", "D", ins)):
            if not (draw and mi.group(1) == "C"
                    and s6_bound_once(ins, "C", "this._gorePals || (this._gorePals = {})")):
                raise SystemExit(f"REFUSING TO WRITE -- stage 6 insert '{label}' writes through an index")


def s6_output_checks(s: str, s0: str, code: str, out_code: str) -> None:
    """What stage 6 leaves in the page (readings 15-21): the inlined fx.js
    untouched; the rune-crack fallback kept once and after Goreshard's arm; the
    priced-blow branch before the plain hit arm, which stays once; the beam's
    art gone; the two sim-path lines each once, where they belong, after the
    price's read; every call, pass and method wired exactly once; no
    Math.random added or taken."""
    if inlined_fx(s) != inlined_fx(s0):
        raise SystemExit("REFUSING TO WRITE -- stage 6 touched the inlined fx.js copy "
                         "(no field: reading 15; SPECS.oathwound goes at the carry)")
    if s.count(RUNE_CRACK) != 1 or not 0 <= s.find(S6_ARM) < s.find(RUNE_CRACK):
        raise SystemExit("REFUSING TO WRITE -- the shared rune-crack fallback is not kept, "
                         "once, after Goreshard's cast arm")
    if s.count(PLAIN_HIT) != 1 or not 0 <= s.find(PRICED_HIT) < s.find(PLAIN_HIT):
        raise SystemExit("REFUSING TO WRITE -- the priced-blow branch is not before the plain hit "
                         "arm, or the plain arm is not there once")
    for gone in BEAM_GONE:
        if gone in s:
            raise SystemExit(f"REFUSING TO WRITE -- the beam's art is still drawn: {gone!r}")
    for need in ("this.tickGore(dt);", "if (__world) this.drawGoreDrops(m);", "  tickGore(dt){",
                 "  _goreShed(f){", "  drawGoreWeapon(m, f, reach, dim){", "  drawGoreDrops(m){",
                 "if (f.goreFade > 0 && this.drawGoreWeapon(m, f, reach, dim)) return;", S6_ARM, PRICED_HIT,
                 "  oathwound(c, t, cf, P){"):
        if out_code.count(need) != 1:
            raise SystemExit(f"REFUSING TO WRITE -- {need!r} is not in the page exactly once")
    for v in S6_SIM_LINES.values():
        for ln in v[:1]:
            if out_code.count(ln) != code.count(ln) + 1:
                raise SystemExit(f"REFUSING TO WRITE -- {ln!r} is not added exactly once")
    if FLOAT_OLD in s:
        raise SystemExit("REFUSING TO WRITE -- resolveHit's old float-size line is still there")
    rh = out_code[out_code.find("  resolveHit(self, foe, hx, hy, seg"):]
    rh = rh[:rh.find("\n  }\n")]
    i_n = rh.find('const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;')
    i_f = rh.find("const fsz = clamp(22 + dmg * 0.62, 22, 62) * (crit ? 1.3 : 1) * (1 + 0.1 * priceN);")
    m_v = re.search(r'if \(priceN > 0\) SFX\.play\("hit", \{ dmg, crit, price: priceN \}\);\s*else\s*'
                    r'SFX\.play\("hit", self\.ultTree \? \{ dmg, crit, bough: self\.w\.ult\.winDmg \} : '
                    r'\{ dmg, crit \}\);', rh)
    if not (0 <= i_n < i_f and m_v and i_f < m_v.start()):
        raise SystemExit("REFUSING TO WRITE -- the float and the priced voice are not in resolveHit, "
                         "after the price's read, the voice just before the hit-voice line")
    if "  tickPresentation(dt){\n    this.tickNovaFx(dt);\n    this.tickGore(dt);" not in s:
        raise SystemExit("REFUSING TO WRITE -- tickGore does not follow tickNovaFx in tickPresentation")
    if out_code.count('SFX.play("ult", { w: f.w.id });') != code.count('SFX.play("ult", { w: f.w.id });'):
        raise SystemExit("REFUSING TO WRITE -- fireUlt's cast voice moved")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- stage 6 moves a Math.random")
    print("  ok    stage 6: presentation only (no RNG, no ultFx, no call into the sim, writes its own gore* "
          "fields, its motes, the canvas and the synth only; the priced voice and the float its two lines on "
          "the sim path, each where it belongs); the inlined fx.js untouched; the rune-crack fallback kept; "
          "the beam's art gone; every call, pass, arm and method once")


STAGE_OUT = {"1": "sc-goreshard-stub", "2": "sc-goreshard-price",
             "5": f"sc-goreshard-b{TUNED['dmg']}", "6": f"sc-goreshard-b{TUNED['dmg']}-fx"}

# ------------------------------------------------------- the insert scan --
# WHAT STAGES 1-5's ADDED CODE MAY WRITE (reading 10): the window record and
# the tally on the fighter, the tally's counters, and the window's clock.
# Nothing else: no status, no stop, no beat, no float, no knock, no heal.
WRITE_OK = {("f", "ultPrice"), ("f", "priceTally"), ("this", "ultPrice"), ("this", "priceTally"),
            ("priceTally", "casts"), ("priceTally", "blows"), ("priceTally", "stk"),
            ("priceTally", "frames"), ("priceTally", "foeStk"), ("Z", "t")}
CALLS_OK = {"stacks", "tickPrice"}   # the only calls the added code makes (reads and the ticker)

NAMES = ("ultPrice", "priceTally", "tickPrice", "priceN", 'kind:"price"', '"price"')


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
    ap.add_argument("--stage", choices=["1", "2", "5", "6"], required=True)
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
    if not out_p.name.startswith("sc-goreshard"):
        raise SystemExit(f"a link of this build is named sc-goreshard*: {out_p.name}")
    if out_p.parent != CHAIN.resolve() and (CHAIN / out_p.name).exists():
        raise SystemExit(f"{out_p.name} is already a link on the chain -- pick "
                         "another name")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    if A.stage == "5" and TUNED["dmg"] is None:
        raise SystemExit("stage 5 has no blade yet: TUNED['dmg'] is set from the measured grid")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nGORESHARD / BLOODPRICE -- stage {A.stage}")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}"
          f"  (LF text)")
    code = strip_comments(s0)
    # THE BASE, BY CONTENT. The features this builder needs, never which relic
    # is last: the shipped Goreshard row (the greatsword, the blade, the
    # channel), STATUS.hemorrhage at its ceiling of 4, resolveHit's two draws
    # and its damage line's prefix, the status reader, and the anchors the
    # inserts compose on.
    head = SHIP_HEAD if A.stage != "6" else SHIP_HEAD.replace(f"dmg:{SHIP_BLADE},", f"dmg:{TUNED['dmg']},")
    if head not in s0:
        raise SystemExit("wrong base: Goreshard's row (greatsword, "
                         f"{SHIP_BLADE if A.stage != '6' else TUNED['dmg']}, hemorrhage 2) has moved")
    if not re.search(r'hemorrhage:\s*\{ name:"Hemorrhage", maxStacks:4, dur:3\.2, dps:1\.5,', code):
        raise SystemExit("wrong base: STATUS.hemorrhage is not maxStacks 4 / dps 1.5")
    if "stacks(key){ return this.status[key] ? this.status[key].stacks : 0; }" not in code:
        raise SystemExit("wrong base: Fighter.stacks is not the status reader this builder reads")
    # (stage 5 reads its own stage 2 here: the price's two lines may stand
    # between the jitter and the damage line, exactly as stage 2 wrote them)
    if not re.search(r"const crit = this\.rng\(\) < \(forge[\s\S]{0,120}?: C\.critChance\);\s*"
                     r"const jitter = 1 \+ \(this\.rng\(\) - 0\.5\) \* C\.dmgJitter;\s*"
                     r"(?:const priceN = self\.ultPrice \? foe\.stacks\(\"hemorrhage\"\) : 0;\s*"
                     r"if \(self\.ultPrice\)\{ self\.priceTally\.blows\+\+; self\.priceTally\.stk \+= priceN; \}\s*)?"
                     r"let dmg = \(self\.ultTree \? self\.w\.dmg \* self\.w\.ult\.winDmg : ", code):
        raise SystemExit("wrong base: resolveHit's crit, jitter and damage line are not the "
                         "sequence this builder reads")
    if not re.search(r"for \(const \[k, n\] of Object\.entries\(\s*\(over && over\.onHit\) \|\| "
                     r"self\.w\.onHit \|\| \{\}\)\)\{", code):
        raise SystemExit("wrong base: resolveHit's onHit loop has moved")
    i_dmg = code.find("let dmg = (self.ultTree ? self.w.dmg * self.w.ult.winDmg : ")
    i_hit = re.search(r"for \(const \[k, n\] of Object\.entries\(\s*\(over && over\.onHit\)", code).start()
    if not (0 <= i_dmg < i_hit):
        raise SystemExit("wrong base: the damage line is not ahead of the onHit loop")
    for anchor in (PRICE_READ_ANCHOR, PRICE_LINE_ANCHOR, '    if (u.kind === "tendril"){\n',
                   '    this.tickTendril(dt);               // TENDRIL (v68)\n',
                   '  tickWinnow(dt){\n', '    this.vineTally = null;\n'):
        if s0.count(anchor) != 1:
            raise SystemExit(f"wrong base: anchor {anchor.strip()!r} is not there "
                             "exactly once")
    # THE BEAM STAYS FOR THE OTHERS (what is retired is Goreshard's row only).
    # The beam has no branch of its own -- it resolves in fireUlt's generic
    # tail -- and this build touches none of that code (the price's branch
    # returns before it). It READS who still is a beam and never refuses on it.
    beams = [bm for bm in re.findall(r'\{ id:"([a-z]+)", name:"', code)
             if bm != RELIC and 'kind:"beam"' in relic_row(code, bm)]
    # THE NAMES THIS RELIC ADDS ARE FREE ON THE BASE (identifier boundaries).
    if A.stage == "1":
        for name in NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")
    print("  base  Goreshard's shipped row, hemorrhage at 4, resolveHit's draws / damage line / "
          "onHit loop and the anchors hold; the beam's generic tail kept, untouched, for "
          + (", ".join(beams) if beams else "no other relic"))

    blade = SHIP_BLADE
    if A.stage == "1":
        if SHIP_ULT not in s0:
            raise SystemExit("this source does not carry the shipped beam -- built?")
        edits, want = S1, ult_block("1e9")
    elif A.stage == "2":
        if 'charge:1e9, kind:"price"' not in code:
            raise SystemExit("stage 2 goes on stage 1")
        if not free_name("ultPrice", code):
            raise SystemExit("this source already carries stage 2 -- built")
        edits, want = S2, ult_block(ULT["charge"])
    elif A.stage == "5":
        if f'charge:{ULT["charge"]}, kind:"price"' not in code or "tickPrice(dt){" not in code:
            raise SystemExit("stage 5 goes on stage 2, once")
        edits, want, blade = S5, ult_block(ULT["charge"]), TUNED["dmg"]
    else:
        # STAGE 6 GOES ON STAGE 5, ONCE: the price at its charge, the tuned
        # blade on Goreshard's row, and none of stage 6's names in the source
        # yet (on identifier boundaries).
        if (f'charge:{ULT["charge"]}, kind:"price"' not in code or "tickPrice(dt){" not in code
                or f"dmg:{TUNED['dmg']}," not in relic_row(code, RELIC)):
            raise SystemExit("stage 6 goes on stage 5 (the price at its charge, the blade at "
                             f"{TUNED['dmg']})")
        for name in S6_NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
        if S6_ARM in code or PRICED_HIT in code:
            raise SystemExit("Goreshard's voices are already in this source -- stage 6 goes on once")
        edits, want, blade = S6, ult_block(ULT["charge"]), TUNED["dmg"]
    for label, old, new in edits:
        s = one(s, old, new, label)

    out_code = strip_comments(s)
    blk = relic_ult(out_code)
    if " ".join(strip_comments(want).split()) != " ".join(blk.split()):
        raise SystemExit(f"REFUSING TO WRITE -- Goreshard's ult block is not "
                         f"what this run printed:\n  {blk}")
    tip = re.search(r'tip:"([^"]*)"', blk).group(1)
    if tip != TIP or len(tip) > 72:
        raise SystemExit(f"REFUSING TO WRITE -- the card is {len(tip)} chars "
                         f"or not the design's: {tip!r}")
    row = relic_row(out_code, RELIC)
    for gone in ("apply:", 'kind:"beam"', "dmg:16"):
        if gone in row:
            raise SystemExit(f"REFUSING TO WRITE -- the beam's {gone} is still on Goreshard's row")
    if f"dmg:{blade}," not in row:
        raise SystemExit("REFUSING TO WRITE -- the blade is not the one this stage writes")
    print(f"  ok    ult   {' '.join(blk.split())[:100]} ...")
    print(f"  ok    card  {len(tip)} chars  {tip!r}")
    print(f"  ok    blade {blade}")
    if out_code.count("Math.random") != code.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    # STAGE 6'S TABLE IS PRESENTATION (reading 21): read on every stage.
    s6_static_checks()
    # WHAT THE ADDED CODE MAY DO, AND NOTHING ELSE (readings 4 and 10). The
    # anchor each row re-emits is taken out first.
    for label, old, new in S1 + S2 + S5:
        ins = strip_comments(new)
        added = strip_comments(new.replace(old, "", 1) if old and old in new else new)
        if "rng()" in added or "spawnFx" in added or "ultFx" in added or "Math.random" in added:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\bw\.(spin|reach|dmg|blades|ult|mass|onHit|arc|width)\s*=[^=]", ins) or \
           re.search(r"\bw\.ult\.\w+\s*=[^=]", ins) or re.search(r"\bw\[", added):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon")
        for bad in ("hitStop", "beat(", "float(", "SFX", "pinFree", "lifesteal", "shake", "banner",
                    "finisher", "taught", "statusTag", "note("):
            if bad in added:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' carries '{bad}': "
                                 "the price is the blade's damage and nothing else (reading 10)")
        for call in re.findall(r"\.(\w+)\(", added):
            if call not in CALLS_OK:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' calls .{call}(): the "
                                 "price reads the stacks and nothing else (reading 10)")
        for mw in re.finditer(r"([\w\]\)]+)\.(\w+)\s*(?:=(?!=)|\+=|-=|\*=|/=|\+\+|--)", added):
            if (mw.group(1), mw.group(2)) not in WRITE_OK:
                raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes "
                                 f"{mw.group(1)}.{mw.group(2)} (reading 10: the window, the tally "
                                 "and the clock only)")
        if re.search(r"\bdelete\b|\[[^\]]*\]\s*(?:=(?!=)|\+=|-=|\+\+|--)", added):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' deletes or writes by index")
        if re.search(r"(?<![\w.])(dmg|stop|crit|jitter)\s*(?:=(?!=)|\+=|-=|\*=|/=)", added):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' rewrites the blow's own "
                             "locals (the price is one factor inside the damage line)")
    if len(re.findall(r'kind:"price"', out_code)) != 1:
        raise SystemExit("REFUSING TO WRITE -- not exactly one price ultimate")
    if A.stage != "1":
        # THE PRICE IS READ ONCE, FROM THE STRUCK FIGHTER, AHEAD OF THE DAMAGE
        # LINE AND THE onHit LOOP, AND PRICED ONCE, INSIDE THE PRODUCT.
        if out_code.count('const priceN = self.ultPrice ? foe.stacks("hemorrhage") : 0;') != 1:
            raise SystemExit("REFUSING TO WRITE -- the stacks are not read exactly once, from the struck fighter")
        if out_code.count("self.ultPrice ? self.w.dmg * (1 + self.w.ult.perStack * priceN) : ") != 1:
            raise SystemExit("REFUSING TO WRITE -- the price is not exactly one clause of the damage line")
        i_n = out_code.find("const priceN")
        i_d = out_code.find("let dmg = (self.ultTree ? self.w.dmg * self.w.ult.winDmg : self.ultPrice ? ")
        i_h = re.search(r"for \(const \[k, n\] of Object\.entries\(\s*\(over && over\.onHit\)", out_code).start()
        if not (0 <= i_n < i_d < i_h):
            raise SystemExit("REFUSING TO WRITE -- the read, the damage line and the onHit loop are "
                             "not in that order")
        if out_code.count("this.tickPrice(dt);") != 1:
            raise SystemExit("REFUSING TO WRITE -- the window's ticker is not called exactly once")
    n_beam = len(re.findall(r'kind:"beam"', out_code))   # read, never a refusal
    n_ids = len(re.findall(r'\{ id:"[a-z]+", name:"', out_code))
    print(f"  ok    one price ultimate, Goreshard's; {n_beam} other beam row(s) left as they "
          f"were; no insert draws the RNG, writes the shared weapon, or stops, beats, floats, "
          f"applies, knocks or heals; {n_ids} relics in the roster")

    if A.stage == "6":
        s6_output_checks(s, s0, code, out_code)
    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
