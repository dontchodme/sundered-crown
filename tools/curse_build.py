#!/usr/bin/env python3
"""THE CURSE REWORK -- Curse stops eating maximum life and starts REMEMBERING.

    python curse_build.py --src ../02-chain/sc-vesper.html \
                          --out ../02-chain/sc-curse.html

STAGE 1 of three (`06-docs/v51/umbral-build-brief-v51.md` §0). It changes a
STATUS, which is to say it changes every fight in the game that contains one of
the three umbral relics -- and nothing at all in the other twenty-four.

## THE DESIGN IS RICK'S, OFF PATH OF EXILE'S IMPALE

    a Curse stack remembers the damage of the hit that applied it; every later
    hit deals a share of everything remembered; stacks cap at 3-6 and a new
    stack displaces the weakest.

Priced before a builder was opened -- `06-docs/v49/curse-rework-v49.md`,
`tools/echo_probe2.py`. K=3 and echo 8%; permanent; displacement kept; and the
echo is priced ON THE TARGET, so any blow from any source pays it.

## WHAT LEAVES, AND IT IS THE WHOLE OF THE OLD MECHANIC

`maxHpLoss` is DELETED, not zeroed (brief §2.1). With it go both readers that
existed only to draw it: the frosted dead cap in `drawGlassRelic` and the
graduation-mark suppression beside it. A reader left in place against a
constant is worse than no reader -- it teaches the next person that the picture
still shows something it cannot show. `tickStatus`'s closing
`f.hp = Math.min(f.hp, f.maxHp)` STAYS: it is generic, and something else could
still lower a ceiling.

## THE STACK COUNT IS DERIVED FROM THE POOL, AND THAT IS DELIBERATE

Brief §2.2 asks that `stacks("curse")` and `cursePool.length` always agree, and
a convention that two call sites must both fire is not agreement, it is a
promise. So `apply()` DERIVES curse's stack count from the pool. A caller that
applies curse without handing it a memory refreshes the clock and adds nothing
-- the memory IS the stack. `curse_check [3]` asserts it anyway, because the
derivation is the thing that could be edited away.

## THE MEMORY IS `dmgBase` AND NEVER `dmg`

Brief §2.4. If a stack remembered the blow's total INCLUDING the echo that blow
just paid, curse compounds and goes exponential inside one fight. Slagburst's
rule -- consumed then priced -- one line, and the reason is in the code beside
it rather than only here.

## THE ECHO IS FOLDED INTO THE HIT, NOT DEALT BESIDE IT

`dmg += echo` lands BEFORE the Aegis block, so a wall eats the echo, a ward
absorbs it, hit-stop scales with it and knockback carries it. Every number in
`06-docs/v51/hands-v51.md` is therefore a FLOOR -- the lab paid the echo as a
separate `hurt()` after the blow and could not do any of that. Re-bisect
against the build; do not argue with the doc.

It is ROUNDED. Every damage number in this engine is an integer -- crits,
jitter and `Math.round` upstream all say so, and `float()` prints it on screen.
An unrounded echo would put `96.32` over a ball.

## WHAT THIS BUILDER DOES *NOT* DO

Dirge and Eclipse lose `apply:{curse:3}` and their tips lose the clause, and
that is ALL that happens to the two ultimates here. Rebuilding them is stages 2
and 3 and they are separate commits against separate files, for the reason the
brief gives: a stage-2 failure diagnosed against a stage-1 regression costs
more than the stage did.

STAGE 1b IS ALSO HERE, and it is one blade rather than three: `umbral_sweep.py`
re-swept all three and only Gravemourn's answer landed outside the
measurement's own precision. See TUNED_GM below -- the reasoning matters more
than the number, because "the other two did not move" is a finding and not an
omission.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# --- the tuned numbers, and they are the doc's ------------------------------
MAX_STACKS = 3      # v49 §1: Gravemourn lands 5.6 blows a fight and cannot
                    # fill more. A small cap is also what narrows the gap
                    # between the two archetypes the mechanic serves (v49 §4).
ECHO = 0.08         # share of the remembered pool added to every later hit

# RICK'S WORDING, 2026-08-30. He asked for "Applies curse on hit, enemies are
# reflected a portion of cursed damage when they are hit again" and picked this
# trim off a measured spread once the budget was on the table.
#
# HIS FIRST CLAUSE IS NOT HERE BECAUSE THE CARD ALREADY SAYS IT. `_scrunchFacts`
# prints the tag `ON HIT` and the name `+1 CURSE` directly above this line, so
# "applies curse on hit" would be the third time the panel said it. The whole
# budget goes to the half the card cannot say for itself.
#
# THE 8% STAYS AND IS NOT NEGOTIABLE COPY. `tip_audit`'s entire job is finding
# effect fields the tip never mentions; "a portion" has no number in it and
# `echo` would be flagged. A number-free line needs a JUSTIFIED entry in
# tip_audit saying why, and there is no reason to write one here.
CURSE_TIP = "Hits reflect 8% of the damage that cursed"    # 41 ch, 471 px

# THE LIMIT IS 48, NOT 40, AND THE REAL LIMIT IS PIXELS.
#
# The v51 brief says 40 twice and this builder copied it; `verify.py` says 40 in
# a COMMENT and enforces 48 in the line under it. 48 is what actually runs, and
# every shipped status tip is under 40 today, so nothing has ever tested the
# gap -- which is how a folklore number survives.
#
# And characters are the wrong unit anyway. The panel budget is 536px on one
# line at 25px, and "Each hit reflects 8% of remembered cursed damage" is 48
# characters and 583px: it passes verify and overflows the card. `tip_audit` is
# the gate that measures pixels and it is in the gate list for that reason.
# MEASURE A NEW TIP THERE, do not count its letters.
TIP_MAX = 48
PANEL_PX = 536      # what tip_audit checks; this builder cannot measure it

# Dirge and Eclipse: same ultimates, one field lighter. PLACEHOLDER TIPS --
# the copy is Rick's (brief open decision 3) and neither name is settled.
DIRGE_TIP = "Pulls target in, dealing 14 damage"
ECLIPSE_TIP = "Nova: deals 11 damage — knocks back"

# --- STAGE 1b. THE BLADES, RE-SWEPT UNDER THE NEW CURSE ---------------------
# `umbral_sweep.py`, 7566 fights: a wide curve, an escalating bisection inside
# the bracket it measures, and a wide confirmation either side of the answer.
#
# ONLY ONE OF THE THREE MOVED, and that is a finding rather than a shortcut.
#
#   gravemourn   44.10 -> 39.79   the sweep's answer, and verify agrees: the
#                                 relic read 61.1% at 44.10 and was the
#                                 strongest in the game. It was paid TWICE by
#                                 this rework -- it gained the echo AND lost a
#                                 payload `ult_price` measured at -3.2.
#   nightfell    15.83   UNCHANGED. The sweep answered 15.90.
#   twinshade     8.30   UNCHANGED. The sweep answered 8.38.
#
# THE OTHER TWO ARE NOT APPLIED BECAUSE THE ANSWERS ARE INSIDE THE
# MEASUREMENT'S OWN PRECISION. +0.07 and +0.08 are a quarter of one percent on
# a quantity this sweep can locate to about a damage point: two Nightfell
# measurements 0.06 apart, both at n=364, differ by 5.7 points of win rate.
# Writing 15.90 would claim two digits nothing here can see. And `verify --n
# 40` -- 1040 fights a relic, the widest instrument in the repo -- independently
# put the two at 50.0% and 49.0% at the numbers they already ship.
#
# A CHANGE SMALLER THAN THE ERROR BAR IS NOT A TUNE, IT IS CHURN THAT LOOKS
# LIKE ONE. If a later measurement resolves them, move them then.
TUNED_GM = 39.79


EDITS = [

# ---------------------------------------------------------------- 1. the data
("STATUS.curse", '''  curse:      { name:"Curse",      maxStacks:8, dur:99,  maxHpLoss:13,
                tip:"Permanently takes 13 max hp per stack" },''',
 '''  /* CURSE — a MEMORY, and the only status here that is not a rate.
     A stack remembers the damage of the blow that applied it; every later blow
     against the cursed fighter, FROM ANY SOURCE, is enlarged by `echo` of
     everything remembered. A new stack displaces the weakest, so the pool
     converges on the wielder's BIGGEST blows rather than its most recent ones
     — Rick's rule, and the only term in the design that scales with hit size.

     `maxStacks` is 3 because Gravemourn lands 5.6 blows a fight and cannot
     fill more (v49 §1), and because a small cap is what narrows the gap
     between the 5.6-blow flail and the 25.7-blow twinblade the mechanic also
     serves. `dur` 99 is unchanged and still means "for the fight".

     THE STACK COUNT IS THE POOL LENGTH. See `apply` and `pushCurse`. */
  curse:      { name:"Curse",      maxStacks:%MAXSTACKS%, dur:99,  echo:%ECHO%,
                tip:"%CURSETIP%" },'''),

# --------------------------------------------------------- 2. the pool's home
("Fighter.cursePool", '''    this.status = {};
    this.hexClock = 0;''',
 '''    this.status = {};
    /* CURSE'S POOL. Descending, length <= STATUS.curse.maxStacks, and it IS
       curse's stack count — see `apply`. Emptied when the status expires. */
    this.cursePool = [];
    this.hexClock = 0;'''),

# ------------------------------------------------------------- 3. the methods
("Fighter.pushCurse", '''  stacks(key){ return this.status[key] ? this.status[key].stacks : 0; }
''',
 '''  stacks(key){ return this.status[key] ? this.status[key].stacks : 0; }

  /* CURSE — three reads and one write, and they are the whole mechanic.

     `pushCurse` takes the damage of the blow that is applying the stack and
     pushes `n` copies of it, then sorts DESCENDING and trims to the cap. The
     trim is the displacement rule: what falls off the end is the weakest
     memory in the pool, so the pool converges on the biggest blows this
     wielder has landed. That is the only term in the design that scales with
     hit size, and it is why the cap can be as small as 3.

     THE VALUE HANDED IN IS `dmgBase` AND NEVER `dmg`. See resolveHit. */
  pushCurse(v, n){
    for (let i = 0; i < n; i++) this.cursePool.push(v);
    this.cursePool.sort((a, b) => b - a);
    if (this.cursePool.length > STATUS.curse.maxStacks)
      this.cursePool.length = STATUS.curse.maxStacks;
  }
  curseSum(){ let s = 0; for (const v of this.cursePool) s += v; return s; }
  /* What a blow landing on this fighter is enlarged by. Rounded at the call
     site, not here — the raw sum is what both umbral ultimates read. */
  curseEcho(){ return this.curseSum() * STATUS.curse.echo; }
'''),

# ------------------------------- 4. apply(): the ceiling goes, the pool leads
("Fighter.apply", '''    cur.stacks = Math.min(def.maxStacks, cur.stacks + n);
    cur.t = def.dur;
    this.status[key] = cur;
    if (key === "curse") this.maxHp = Math.max(60, this.maxHp - def.maxHpLoss * n);
  }''',
 '''    cur.stacks = Math.min(def.maxStacks, cur.stacks + n);
    cur.t = def.dur;
    /* CURSE'S STACK COUNT IS DERIVED FROM ITS POOL, and that is structural
       rather than conventional. The brief asks that `stacks("curse")` and
       `cursePool.length` always agree; two call sites that must both fire is a
       promise, not an agreement. So the memory IS the stack: a caller that
       applies curse without handing `pushCurse` a memory refreshes the clock
       and adds nothing. Deliberate — an ultimate that "applies 3 Curse stacks"
       out of nowhere is exactly the dead clause v49 measured at +0.0. */
    if (key === "curse") cur.stacks = Math.min(def.maxStacks, this.cursePool.length);
    this.status[key] = cur;
  }'''),

# -------------------------------------------- 5. the three edits in resolveHit
("resolveHit.echo", '''    dmg = Math.round(dmg);
''',
 '''    dmg = Math.round(dmg);

    /* ---- CURSE. THE ECHO IS READ OFF THE TARGET, AND THE MEMORY IS TAKEN
       BEFORE IT IS PAID.

       (b) THE ECHO IS THE STACKS THAT ALREADY EXIST. Read before this blow's
       own onHit runs, so a fresh stack does not pay out on the blow that
       applied it — PoE's own rule, and it comes free from the order
       `resolveHit` was already written in.

       (c) `dmgBase` IS THE MEMORY. Post-crit, post-jitter, post-sunder,
       PRE-echo. IT IS NEVER `dmg`. If a stack remembered the total including
       the echo that blow just paid, every memory would grow by (1 + echo)
       each time the pool was refreshed and curse would go exponential inside
       one fight. Slagburst's rule — consumed, then priced.

       (d) FOLDED IN, NOT DEALT BESIDE. The echo is added to `dmg` here,
       ABOVE the Aegis block, so a directional wall eats it, a ward absorbs
       it, hit-stop scales with it and knockback carries it. An echo paid as a
       separate hurt() would be none of those things.

       ROUNDED, because every damage number in this engine is an integer and
       `float()` prints this one over a ball.

       PRICED ON THE TARGET AND NOT ON AN ASSUMED ATTACKER. There is no
       `self === owner` guard and there must never be one: Twinshade's shades
       are real Fighters carrying `onHit:{curse:1}`, and a guard on the caster
       would make 9.3 blows a fight invisible. It is also PoE's rule — hit by
       any source. */
    const curseEcho = Math.round(foe.curseEcho());
    const dmgBase = dmg;
    dmg += curseEcho;
'''),

# --------------------------------------------- 6. the onHit loop remembers it
("resolveHit.onHit", '''    for (const [k, n] of Object.entries(
           (over && over.onHit) || self.w.onHit || {})){
      foe.apply(k, n);
      const first = !this.taught[k] && !!(STATUS[k] && STATUS[k].tip);
      if (first) this.taught[k] = true;
      this.statusTag(hx, hy, k, first);
    }''',
 '''    for (const [k, n] of Object.entries(
           (over && over.onHit) || self.w.onHit || {})){
      /* THE MEMORY GOES IN BEFORE THE CLOCK IS SET, because `apply` derives
         curse's stack count from the pool and cannot see a push that has not
         happened yet. `dmgBase` and not `dmg`. */
      if (k === "curse") foe.pushCurse(dmgBase, n);
      foe.apply(k, n);
      const first = !this.taught[k] && !!(STATUS[k] && STATUS[k].tip);
      if (first) this.taught[k] = true;
      /* THE TAG PRINTS THE REMEMBERED TOTAL, NOT THE PENDING ECHO. The echo
         peaks at 5-8 across the whole school and is not a number worth
         watching; the pool holds 42-60, peaks above 100, fills in three blows
         and is what BOTH umbral ultimates read. `CURSE 96` at the impact and
         then a detonation for 96 is a story a viewer can follow. */
      this.statusTag(hx, hy, k, first, k === "curse" ? Math.round(foe.curseSum()) : 0);
    }'''),

# ----------------------------------------- 7. the tag carries a number now
("statusTag", '''  statusTag(x, y, key, first){
    const def = STATUS[key]; if (!def) return;
    const aff = Object.values(AFFINITIES).find(a => a.status === key);
    this.tags.push({ x, y, key, name: def.name, tip: first ? def.tip : "", first,''',
 '''  /* `val` is OPTIONAL and is printed after the name when it is non-zero.
     Curse is the only status with a number worth reading at the point of
     contact — every other one here is a rate, and its stack count is already
     drawn on the ball. Undefined at every other call site, so those are
     byte-identical in behaviour. */
  statusTag(x, y, key, first, val){
    const def = STATUS[key]; if (!def) return;
    const aff = Object.values(AFFINITIES).find(a => a.status === key);
    this.tags.push({ x, y, key, name: def.name, tip: first ? def.tip : "", first,
                     val: val || 0,'''),

("tag.quick", '''    const label = g.name.toUpperCase();''',
 '''    const label = g.name.toUpperCase() + (g.val ? " " + g.val : "");'''),

# --------------------------------- 8. the pool dies with the status, not before
("tickStatus.expire", '''        if (key === "ward"){ f.shield = 0; f.shieldMax = 0; f.wardFade = 1; }
        delete f.status[key]; continue;''',
 '''        if (key === "ward"){ f.shield = 0; f.shieldMax = 0; f.wardFade = 1; }
        /* THE POOL IS THE STACKS, so it has to go when they do. `dur` 99
           against a 120s timeout means this is reachable — rare, but a pool
           that outlived its status would leave `stacks("curse")` at 0 while
           every blow still paid an echo. */
        if (key === "curse") f.cursePool.length = 0;
        delete f.status[key]; continue;'''),

# --------------------------------- 9. STAGE 1b, and it is one blade, not three
("blade.gravemourn", '''    blades:[0], reach:96, width:22, artW:52, dmg:44.1, spin:2.2, mode:"chain", mass:3.6,''',
 '''    /* dmg 44.10 -> %TUNEDGM% (`umbral_sweep.py`, stage 1b). The rework paid
       this relic twice — it gained the echo and lost a Dirge payload worth
       -3.2 — and it read 61.1% at 44.10, the strongest relic in the game.
       Nightfell's and Twinshade's re-swept answers came back inside the
       measurement's own precision of what they already ship, so this is the
       only blade that moves. The reasoning is in curse_build.TUNED_GM. */
    blades:[0], reach:96, width:22, artW:52, dmg:%TUNEDGM%, spin:2.2, mode:"chain", mass:3.6,'''),

# ------------------------------------------------- 10. Dirge and Eclipse
("ult.dirge", '''    ult:{ name:"Dirge", charge:16, kind:"pull", radius:320, dmg:14, apply:{curse:3}, tip:"Pulls target in, dealing 14 damage and applying 3 Curse stacks" },''',
 '''    /* `apply:{curse:3}` is GONE. Measured at -3.2 points against a field
       median of +20.4 (`ult_price.py`) — an ultimate whose payload was worth
       LESS than nothing, because a curse stack applied by an ultimate carries
       no memory to remember. Stage 2 replaces the payload; this stage only
       takes the dead one out. Name and tip are PLACEHOLDERS and are Rick's. */
    ult:{ name:"Dirge", charge:16, kind:"pull", radius:320, dmg:14, tip:"%DIRGETIP%" },'''),

("ult.eclipse", '''    ult:{ name:"Eclipse", charge:15, kind:"nova", radius:250, dmg:11, apply:{curse:3},
          knock:150, tip:"Nova: deals 11 damage and applies 3 Curse stacks — knocks back" },''',
 '''    /* `apply:{curse:3}` is GONE, same reason as Dirge's and worth +7.2
       against a field median of +20.4. Stage 3 replaces the payload. Name and
       tip are PLACEHOLDERS and are Rick's. */
    ult:{ name:"Eclipse", charge:15, kind:"nova", radius:250, dmg:11,
          knock:150, tip:"%ECLIPSETIP%" },'''),
]


# --- the span replacements, done by head/tail so a forty-line art block does
#     not have to be transcribed into this file to be replaced ----------------

SPANS = [
 ("glass.deadcap",
  "  /* 4a. CURSE'S DEAD CAP.",
  "  /* 4b. THE GRADUATIONS.",
  '''  /* 4a. CURSE'S DEAD CAP IS GONE, and so is the frost that drew it.

     Curse no longer eats maximum life — it REMEMBERS — so `f.maxHp` is
     `CONFIG.combat.baseHP` for every fighter of every relic for the whole of
     every fight, and `maxFrac` above is 1 forever. What stood here drew a
     frosted band down to `maxFrac` and could only ever draw nothing.

     IT IS DELETED RATHER THAN LEFT AGAINST A CONSTANT. A reader that cannot
     fire still tells the next person the picture shows something, and this
     project has two dead knobs in its open items for exactly that reason. The
     status now says itself on the ball, in `_stCurse`. */

'''),

 ("glass.marks",
  "      if (fr > maxFrac + 0.001) continue;             // eaten by Curse; no mark\n",
  None,
  ""),

 ("_stCurse",
  "  /* CURSE — it is gone for good. Motes leave the relic and keep going; they",
  "  /* HEX — the weapon is jammed",
  '''  /* CURSE — NOTHING LEAVES. One mote per remembered blow, drawn IN.

     The shipped art was built for a mechanic that no longer exists: motes
     escaped the shell and never came back, which said `maximum life, gone for
     good`. Nothing is taken any more, so an escaping mote is now a lie about
     what the viewer is watching — and a picture fault is a defect class in
     this project precisely because "wrong" and "right" produce identical
     numbers (§4.1).

     What is drawn instead is the pool itself. ONE MOTE PER ENTRY, sized by
     that entry's share of the total, so the biggest remembered blow is the
     biggest mote and the displacement rule is visible: a bigger blow lands,
     the smallest mote is replaced by a large one. THE COUNT IS THE STACK
     COUNT, capped at 3 and countable at phone size.

     THE MOTION IS THE OLD ONE REVERSED. Each mote runs its cycle from far out
     to close in and repeats, so the shell is perpetually drawing things
     toward it rather than losing them, and the wisp trails OUTWARD behind the
     mote instead of downward after it. Arrival without per-mote state: every
     position stays a pure function of (side, index, m.t) through shellHash,
     never `this.rng()`, because the renderer may not consume the sim's
     randomness. */
  _stCurse(m, f, R, n){
    const c = this.ctx;
    const pool = f.cursePool, sum = f.curseSum();
    if (!pool.length || sum <= 0) return;
    c.save();
    c.globalCompositeOperation = "lighter";
    for (let i = 0; i < pool.length; i++){
      /* share of the pool, normalised against an even split so a single
         remembered blow is not drawn at three times the size of one of three */
      const share = (pool[i] / sum) * pool.length;
      const ph = (m.t * 0.30 + shellHash(1103 + f.side, i)) % 1;
      /* IN, not out: 1.85R at the start of the cycle down to 1.02R at its end */
      const rad = R * (1.85 - 0.83 * (1 - (1 - ph) * (1 - ph)));
      const a = shellHash(1117 + f.side, i) * TAU + i * TAU / pool.length
              + m.t * 0.55;
      const px = f.x + Math.cos(a) * rad;
      const py = f.y + Math.sin(a) * rad * 0.92;
      /* fades UP as it arrives, and holds — nothing here dims to nothing */
      c.globalAlpha = (0.30 + 0.65 * ph) * 0.95;
      const rr = (2.4 + 3.4 * Math.min(1.6, share)) * (0.72 + 0.28 * ph);
      c.fillStyle = ph > 0.72 ? "#E4CCFF" : "#A45CF0";
      c.beginPath(); c.arc(px, py, rr, 0, TAU); c.fill();
      /* the wisp trails BEHIND it, along the way it came */
      c.globalAlpha *= 0.5;
      c.strokeStyle = "#A45CF0"; c.lineWidth = 1.6;
      c.beginPath(); c.moveTo(px, py);
      c.lineTo(f.x + Math.cos(a) * (rad + 11), f.y + Math.sin(a) * (rad + 11) * 0.92);
      c.stroke();
    }
    c.restore();
  }

'''),

 ("status.prose",
  "     slowed; motes escape and do not come back because Curse eats maximum life\n     for good; and Hex clamps",
  None,
  "     slowed; motes are drawn IN and never leave because Curse takes nothing\n     and remembers everything; and Hex clamps"),
]


def one(src: str, old: str, new: str, label: str) -> str:
    # A BUILDER THAT WRITES BROKEN JAVASCRIPT SHOULD SAY SO -- v43 shipped an
    # unbalanced `*/` once and the only signal was a twenty-second Playwright
    # timeout. These inserts are mostly prose; counting delimiters is the
    # cheapest thing that catches it.
    if new.count("/*") != new.count("*/"):
        raise SystemExit(f"BLOCK {label}: {new.count('/*')} '/*' against "
                         f"{new.count('*/')} '*/'. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def span(src: str, head: str, tail, new: str, label: str) -> str:
    """Replace head..tail (tail exclusive), or just `head` when tail is None.

    Used where the old text is a forty-line art block: transcribing it into
    this file in order to replace it is one more place for it to be wrong.
    """
    if new.count("/*") != new.count("*/"):
        raise SystemExit(f"BLOCK {label}: unbalanced comment delimiters.")
    if src.count(head) != 1:
        raise SystemExit(f"ANCHOR {label}: head occurs {src.count(head)} times, "
                         f"expected 1.\n  {head.splitlines()[0][:90]!r}")
    i = src.index(head)
    if tail is None:
        j = i + len(head)
    else:
        if src.count(tail) != 1:
            raise SystemExit(f"ANCHOR {label}: tail occurs {src.count(tail)} "
                             f"times, expected 1.")
        j = src.index(tail, i)
        if j <= i:
            raise SystemExit(f"ANCHOR {label}: tail lands before head.")
    print(f"  ok    {label}  ({j - i} bytes out, {len(new)} in)")
    return src[:i] + new + src[j:]


def main() -> int:
    ap = argparse.ArgumentParser()
    # THE CHAIN IS LINEAR AND THE TIP IS VESPER. The build brief was written
    # against sc-thornshear.html, which was the build of record when it was
    # written and is the link BEFORE the current one -- building off it would
    # silently un-ship the twenty-seventh relic. Every measurement behind this
    # stage was taken on 26 relics; the twenty-seventh is vigil, carries no
    # curse and touches nothing here, so the design survives the move. What
    # moves with it is one number in every gate: `engine_ab` must be identical
    # on TWENTY-FOUR non-umbral relics, not twenty-three.
    ap.add_argument("--src", default="../02-chain/sc-vesper.html")
    ap.add_argument("--out", default="../02-chain/sc-curse.html")
    ap.add_argument("--max-stacks", type=int, default=MAX_STACKS)
    ap.add_argument("--echo", type=float, default=ECHO)
    ap.add_argument("--tip", default=CURSE_TIP)
    ap.add_argument("--gm-dmg", type=float, default=TUNED_GM,
                    help="Gravemourn's blade, stage 1b")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print("\nTHE CURSE REWORK -- a memory, not a ceiling")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if "maxHpLoss" not in s0:
        raise SystemExit("this source has no maxHpLoss -- already reworked, or "
                         "not a build of this chain")
    if "cursePool" in s0:
        raise SystemExit("this source already has a cursePool -- already built")
    if '"sentinel"' not in s0:
        raise SystemExit(
            "this source has no sentinel -- the tip is sc-vesper.html and the "
            "chain is linear. Building off an older link un-ships a relic.")

    # A STATUS TIP HAS A HARD LIMIT AND verify.py IS WHERE IT IS ENFORCED,
    # which is 12000 fights too late to find out.
    if len(A.tip) > TIP_MAX:
        raise SystemExit(f"STATUS TIP is {len(A.tip)} characters against "
                         f"verify.py's enforced limit of {TIP_MAX}:\n  {A.tip}")
    for t, who in ((DIRGE_TIP, "Dirge"), (ECLIPSE_TIP, "Eclipse")):
        if len(t) > 72:
            raise SystemExit(f"{who} tip is {len(t)}/72")
    # THE TIP MUST STATE THE NUMBER THE BUILD ACTUALLY CARRIES. A tip saying
    # 8% over an echo of 0.10 is a lie tip_audit cannot see.
    pct = f"{A.echo * 100:g}%"
    if pct not in A.tip:
        raise SystemExit(f"the status tip does not name the echo it ships "
                         f"({pct}):\n  {A.tip}")
    print(f"  set maxStacks {A.max_stacks}   echo {A.echo:g}   "
          f"tip {len(A.tip)}/{TIP_MAX}  {A.tip!r}")
    print(f"      the PIXEL budget is {PANEL_PX} and this builder cannot see "
          f"it — tip_audit is that gate")

    subs = {"%MAXSTACKS%": str(A.max_stacks), "%ECHO%": f"{A.echo:g}",
            "%CURSETIP%": A.tip, "%DIRGETIP%": DIRGE_TIP,
            "%ECLIPSETIP%": ECLIPSE_TIP, "%TUNEDGM%": f"{A.gm_dmg:g}"}
    print(f"  1b  gravemourn blade 44.1 -> {A.gm_dmg:g}   "
          f"(nightfell and twinshade deliberately unchanged — see TUNED_GM)")

    for label, old, new in EDITS:
        for k, v in subs.items():
            old = old.replace(k, v)
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for label, head, tail, new in SPANS:
        s = span(s, head, tail, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    # THE OLD CHANNEL IS GONE AND NOTHING MAY QUIETLY RE-OPEN IT. This is
    # curse_check [7] asserted statically, and it is free.
    if "maxHpLoss" in s:
        raise SystemExit("maxHpLoss survives somewhere in the output")
    # NOT a plain substring test: the inserts above QUOTE the field they
    # delete, in backticks, and a guard that cannot tell code from the comment
    # explaining it fires on its own explanation.
    if re.search(r"(?<!`)apply:\{curse:", s):
        raise SystemExit("an ultimate still applies curse with no memory")
    if s.count("f.hp = Math.min(f.hp, f.maxHp)") != \
       s0.count("f.hp = Math.min(f.hp, f.maxHp)"):
        raise SystemExit("tickStatus's generic hp clamp was disturbed -- §2.5 "
                         "says it STAYS")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print("\n  NEXT (brief §0, and a red gate stops the next stage):")
    print(f"    python curse_check.py --game {A.out}")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 10   # the 24")
    print(f"    python verify.py --game {A.out} --n 40")
    print(f"    python chain_audit.py --builder curse_build.py --tip {A.out}")
    print(f"    python umbral_sweep.py --game {A.out}                # stage 1b")
    return 0


if __name__ == "__main__":
    sys.exit(main())
