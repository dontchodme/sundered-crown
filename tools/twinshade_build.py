#!/usr/bin/env python3
"""TWINSHADE — the umbral twinblade, and THE THREEFOLD.

    python3 twinshade_build.py --src ../02-chain/sc-health18.html \
                               --out ../02-chain/sc-twinshade.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in v37 §1. Everything in this file
is an implementation of those words plus four interview answers:

    copies have NO ULT BAR      -- without it this ultimate is exponential
    expiry is ONE BEAT          -- every survivor goes on the same frame
    a killed copy PAYS NOTHING  -- getting the tempo back is the reward
    the fire is on the CASTER ONLY

WHAT MAKES THIS THE BIGGEST RELIC THIS ENGINE HAS TAKEN

`Match` has exactly two fighters and says so in its own first line
(`if (idA === idB) throw new Error("A relic cannot fight itself")`). Every
per-fighter loop in `step()` is a literal two-element pair. No ult kind in the
game summons anything: the twelve that exist are all projectiles, fields, or
state on a body that already existed.

THE ARCHITECTURE THAT PROTECTS THE BIT-IDENTITY PROOF

Every relic since Lastlight has shipped behind `engine_ab` proving the other
ids play BIT-IDENTICALLY. That proof is what is most at risk here, and it is
kept structurally rather than carefully:

    THE SHADES LIVE IN `m.shades`. THEY ARE NEVER `m.a` OR `m.b`.

Every loop this file adds runs over that list. In every match without this
relic — and in every match with it before the ultimate fires — the list is
empty and each added loop runs zero times. Same class of argument as
Lastlight's zero-burden identity, and like that one the harness asserts it
directly instead of trusting this paragraph.

The three reads that are NOT loops are each an exact identity at rest:

    lifesteal    `self.lifesteal || self.w.lifesteal`   0 || undefined -> falsy
    hit cooldown `cool === false ? 0 : dt`              undefined -> dt
    beat side    `(self.shade ? self.shade.owner : self) === this.a`

WHY RICK'S OWN CONSTRAINT IS WHAT MAKES THIS BUILDABLE

"They cannot hurt or clank with each other or the original" keeps the
interaction graph a STAR, not a mesh. A shade interacts with the foe and with
nothing else, so no N x N pairing exists anywhere in this file. Had the copies
been able to hit each other this would have been a genuine N-body rewrite of
the hot path.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# --------------------------------------------------------------- tuning ----
#
# EVERY NUMBER HERE IS PROVISIONAL AND MOST OF THEM ARE MEASURABLE. The blade
# in particular MUST be swept, not derived: v36 registered a prediction from
# the factored model on this exact cell and it was falsified by 9 points,
# because curse's value depends on WHEN in the fight a hit lands and no
# `mod[school]` term can express that.
#
# The starting blade is the mean of the two shipped twinblades (11.95, 8.81).
# It will be wrong. twinshade_sweep.py is what makes it right.
TUNED_TS = 8.3   # SWEPT, twice: 7.9 before the holds, 8.3 after. The pause
                 # costs the relic ~1.6pp because the caster spends it not
                 # fighting either. See twinshade_sweep.py.

# The ultimate. `dur` is the whole ult; `arrive` is presentation only.
ULT_CHARGE    = 18.0    # the Crucible's 18 is the longest in the game, and
                        # this is a bigger moment than the Crucible
ULT_DUR       = 6.0     # seconds the shades walk
ULT_SHADES    = 2       # "the ball produces 2 coppies of itself"
ULT_HP        = 0.40    # "less life than the original" -> 120 of baseHP 300
ULT_LIFESTEAL = 0.35    # share of damage dealt returned as hp, ALL THREE BALLS
ULT_ARRIVE    = 0.28    # presentation only: the fade-in on a new shade
ULT_HOLD      = 1.00    # THE SPLIT HOLD. Rick: "lets have the fight pause for
                        # a second while the duplicates split off the original
                        # like a cell replicating". The whole hall freezes;
                        # `this.t` keeps running so duration stays honest.
                        # Ironbloom's latch is the same machinery.
ULT_REJOIN    = 0.55    # THE REUNION. Rick: "a reverse of the cell split where
                        # any surviving clones rejoin the original". Half the
                        # split's hold, on purpose: the division is the moment
                        # the relic becomes something and the reunion is the
                        # moment it stops. See the note in tickSplitHold.
ULT_RIBBON    = 0.75    # DRAIN RIBBON THICKNESS, as a factor. Rick: "lets make
                        # the ribbons a little thinner. try 25%". On the ult
                        # data rather than baked into drawDrains, because this
                        # is the third pass over this effect's look and a knob
                        # that has been asked about twice should have a name.
ULT_ARC       = 1.40    # HOW FAR THE RIBBONS BOW OFF THE STRAIGHT LINE, as a
                        # factor on the swirl amplitude. Rick: "lets also give
                        # them a bit wider arc". Scales the ORBIT only — not the
                        # number of turns, which is `swirl`, and not the length.
ULT_SPREAD    = 2.35    # spawn radius in ball-radii, clear of the caster shell

# ---- NAMES ARE PLACEHOLDERS AND RICK HAS NOT CHOSEN EITHER ----------------
# Lastlight's own name came from Rick and only the ULT name was chosen for
# him. Here neither has been, so both are flagged rather than quietly adopted.
# Each is one string.
RELIC_NAME = "Twinshade"          # <-- PLACEHOLDER
ULT_NAME   = "Triplicate"         # Rick, v37 round 2
ULT_TIP    = "Splits into 3 for 6 seconds — each gains lifesteal"
BLURB      = ("Two daggers, and then six. What walks out of it wears your "
              "face and keeps what it takes.")

# ============================================================ relic data ====
RELIC = ('''
  /* TWINSHADE — the umbral twinblade, and THE THREEFOLD.

     The nineteenth relic and the first to put a body on the floor that was not
     there when the match began. Physics are Widowmaker's and Spellbreaker's
     EXACTLY (weapon-matrix decision 1: type owns the physics, school owns
     status and palette) — twinblade_zoom.py photographs all three on the same
     seed and their trajectories are pixel-identical at t=1.10, which is that
     rule showing up as a measurement rather than as a claim.

     curse:1, matching the school's other two, and the reason is the ultimate
     rather than consistency: for six seconds this relic is putting THREE
     twinblades on one foe. The application rate is already tripled by the ult;
     doubling it per hit as well would stack an unbounded permanent drain on
     the earliest-opening type in the game (first Curse at 2.69s against
     Nightfell's 3.95s and Gravemourn's 6.52s — purpledagger_probe [3]).

     `dmg` is the tuned knob (twinshade_build.TUNED_TS) and MUST be swept. */
  { id:"twinshade", name:"%NAME%", aff:"umbral", shape:"twinblade",
    blades:[0,0.5], reach:62, width:8, artW:30, dmg:%DMG%, spin:5.7, mode:"spin", mass:1.1,
    onHit:{ curse:1 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"split", dur:%DUR%,
          shades:%SHADES%, hp:%HP%, lifesteal:%LS%, arrive:%ARRIVE%,
          spread:%SPREAD%, hold:%HOLD%, rejoin:%REJOIN%,
          ribbon:%RIBBON%, arc:%ARC%,
          tip:"%TIP%" },
    blurb:"%BLURB%" },
''')

# Anchored to Axiom's blurb because Axiom is the LAST entry in WEAPONS and the
# insert therefore cannot land between a relic and its own comment.
RELIC_ANCHOR = ('    blurb:"Blade-shards held in formation by nothing at all. '
                'Close the gaps and it is a sword again." },')

# ====================================================== engine: state =======
FSTATE_OLD = ("    this.ultHarrow = null;    "
              "// {t, fuse} while the Harrowing's blades count down")
FSTATE_NEW = FSTATE_OLD + """
    /* THE THREEFOLD. `ultSplit` is on the CASTER and nowhere else; the shades
       themselves carry `shade` and never carry this. */
    this.ultSplit = null;     // {t, dur} while the shades walk
    /* A TIMED share of damage returned as hp. `resolveHit` already implements
       lifesteal and already draws it (the shell knits, a green +N floats) —
       it just reads it off the WEAPON, and a weapon object is shared by every
       match in a sweep, so a timed state cannot live there. The read is
       `self.lifesteal || self.w.lifesteal`, which at 0 and undefined is
       exactly the expression that was there before. */
    this.lifesteal = 0;
    /* Set on a COPY and on nothing else: {owner}. A shade is never a fighter
       of record — never this.a, never this.b, never in `summary()`, never on
       the HUD, never a killFlight target. Reading `f.shade` is how every
       branch in this build asks "is this a real relic or a copy of one". */
    this.shade = null;
    /* Rick's call, and the only one of the four that is load-bearing for
       termination rather than for feel: a copy that "fights the same as the
       original" would charge and cast, and two copies each making two more is
       exponential. Shades are never passed to tickCharge at all, so this is
       belt AND braces — twinshade_probe asserts a shade's charge stays 0. */
    this.noUlt = false;
    this.born = 1;            // presentation only: 0..1 fade-in on a new shade
    /* HOW RECENTLY THIS BALL WAS FED ON. Presentation only, 0..1, set to 1 by
       `drain()` and decayed in tickPresentation. It exists because the motes
       alone are not enough: MEASURED, only 35% of a running ultimate's frames
       had one on screen even after the bursts were lengthened, because hits are
       sparse — three balls at 0.27 hits/s land one about every 1.2 seconds and
       a burst is gone in under one. This decays over ~1.6s, so it bridges the
       gaps between bursts and the tether it drives is lit for most of the
       window without ever being lit when nothing has happened. */
    this.drained = 0;"""

MSTATE_OLD = "    this.shots = [];          // live projectiles, oldest first"
MSTATE_NEW = MSTATE_OLD + """
    /* THE SHADES — live copies, and THE WHOLE BIT-IDENTITY ARGUMENT.

       Empty in every match that does not contain this relic, and empty in one
       that does until the ultimate fires. Every loop this build adds runs over
       this list, so in all of those matches every added loop runs zero times.
       That is why nineteen relics do not re-tune the other eighteen.

       engine_ab.py is what proves it. This comment is not. */
    this.shades = [];
    /* THE SPLIT HOLD — the hall stopped while one ball becomes three. Same
       machinery as Ironbloom's latch: a branch in step() takes over entirely,
       nothing in the simulation advances, and `this.t` runs with it so match
       duration stays honest. Null in every match that does not contain this
       relic. */
    this.splitHold = null;
    /* THE DRAIN — presentation only, and the reason it is a LIST of motes
       rather than a flag on the fighter is that lifesteal has to look like
       something being TAKEN. Each mote is a piece of the foe's own life in the
       foe's own colour, travelling to whoever tore it off. Empty in every
       match without this relic; `tickPresentation` and `drawDrains` both cost
       one length check when it is. */
    this.drains = [];"""

# ============================================ engine: lifesteal is timed ====
#
# Two changes, and the second one is the answer to "why can't I see it".
#
# (1) TIMED, so it is read off the fighter first. `self.lifesteal` is 0 on every
#     fighter in every match without this relic and `w.lifesteal` is declared by
#     no weapon in the game, so `0 || undefined` is falsy and this branch is not
#     entered — byte-for-byte the behaviour that was here.
#
# (2) THE DRAIN FIRES EVEN WHEN THE HEAL IS WORTH NOTHING. Measured on the built
#     relic: of 565 blows landed while lifesteal was on, **194 of them (34%)
#     healed zero** because `hp` is clamped to `maxHp` and the caster was
#     already full. Those frames drew nothing at all, and they are a third of
#     the ultimate.
#
#     Drawing nothing there is not honest either — the life IS being taken, it
#     just has nowhere to go. So a clamped heal now spawns a thinner stream that
#     DIES IN MID-AIR short of the ball, which says "full" in the only place a
#     viewer is already looking. That is information the green +N never carried.
LS_OLD = """    if (self.w.lifesteal){
      const before = self.hp;
      self.hp = Math.min(self.maxHp, self.hp + dmg * self.w.lifesteal);
      const got = Math.round(self.hp - before);
      if (got >= 1){
        self.mend = 1;
        this.float(self.x, self.y - 42, "+" + got, "#8FE3A0", 26 + got * 0.7);
      }
    }"""
LS_NEW = """    const _ls = self.lifesteal || self.w.lifesteal;
    if (_ls){
      const before = self.hp;
      self.hp = Math.min(self.maxHp, self.hp + dmg * _ls);
      const got = Math.round(self.hp - before);
      if (got >= 1){
        self.mend = 1;
        this.float(self.x, self.y - 42, "+" + got, "#8FE3A0", 26 + got * 0.7);
      }
      /* Outside the `got >= 1` guard on purpose — see the note above. A third
         of the blows landed under this ultimate heal nothing, and they were
         drawing nothing. */
      this.drain(foe, self, got, got < 1);
    }"""

# ================================== engine: a shade is not a kill target ====
#
# THE ONLY killFlight ARMING SITE IN THE GAME, and it is reachable by a shade.
# `tgt` is derived as `foe === this.a ? "a" : "b"` — a shade is neither, so it
# resolves to "b" and the Crucible killing a COPY would arm the kill flight on
# the REAL fighter b: checkEnd holds the match open, move() pins b at the first
# wall, and the hall plays a death that did not happen.
#
# Found by reading the arming site, not by watching a match. twinshade_probe
# drives it directly.
KF_OLD = '        this.killFlight = { tgt: foe === this.a ? "a" : "b", t: 0 };'
KF_NEW = """        /* NOT FOR A SHADE. `tgt` is an "a"/"b" key and a copy is
           neither, so this would arm the flight on the real fighter and play
           a death that did not happen. A shade dies where it stands. */
        if (!foe.shade)
          this.killFlight = { tgt: foe === this.a ? "a" : "b", t: 0 };"""

# ============================ engine: the director must not be misinformed ==
BEAT_OLD = """    const _cs = this._cineShot;
    this.beat({ kind: "hit", side: self === this.a ? 0 : 1, x: hx, y: hy,"""
BEAT_NEW = """    const _cs = this._cineShot;
    /* A shade's blow belongs to the relic that cast it. `side` is what the
       director reads to decide which ball a cut is about, and a copy is not
       `this.a`, so untouched this would file every shade hit under side 1 —
       including the ones landed by a shade of side 0. Identity for every
       fighter that is not a shade. */
    const _side = (self.shade ? self.shade.owner : self) === this.a ? 0 : 1;
    this.beat({ kind: "hit", side: _side, x: hx, y: hy,"""

# ============================================== engine: the hit cooldown ====
#
# `tickHits` decrements the ATTACKER's per-blade cooldown by dt at the top. The
# foe now has to be offered the shades as targets as well as the real relic, so
# without this the foe's cooldown would tick three times a frame and its swing
# rate would triple for the duration of the ultimate. `cool === false ? 0 : dt`
# is `dt` at every existing call site, all of which pass three arguments.
COOL_OLD = """  tickHits(self, foe, dt){"""
COOL_NEW = """  /* `cool` is passed FALSE when this fighter's cooldown has already been
     ticked this frame by an earlier call — which is every extra target a
     fighter is offered beyond its first. Undefined at every pre-existing call
     site, and `undefined === false` is false, so `dt` is subtracted exactly as
     before. Without it, a foe facing two shades swings three times as often. */
  tickHits(self, foe, dt, cool){"""

COOL2_OLD = "      self.hitCd[i] = Math.max(0, (self.hitCd[i] || 0) - dt);"
COOL2_NEW = ("      self.hitCd[i] = Math.max(0, (self.hitCd[i] || 0) - "
             "(cool === false ? 0 : dt));")

# ======================================== engine: lifesteal is now VISIBLE ==
#
# Rick: "the lifesteal is also really hard to see. i know we have damage numbers
# that show healing but lets also build an animation for it. im picturing the
# balls as sucking the lifeforce from their enemy. lets show something being
# pysically taken and streamed back to twinshade."
#
# The float was already there and it is not enough: a number over the healer
# says it got better, it does not say WHERE FROM. The travel is the whole
# point, so the drain is spawned at the foe and homes to whoever tore it off.
DRAIN_OLD = """        self.mend = 1;
        this.float(self.x, self.y - 42, "+" + got, "#8FE3A0", 26 + got * 0.7);"""
DRAIN_NEW = """        self.mend = 1;
        this.float(self.x, self.y - 42, "+" + got, "#8FE3A0", 26 + got * 0.7);
        /* and the life itself, physically leaving the thing it came out of.
           Presentation only; `drains` is empty in every match without a
           lifesteal relic in it, which until this build was all of them. */
        this.drain(foe, self, got);"""

# ================================================== engine: the step loop ===
STEP_OLD = """    this.ballCollision();
    this.tickClank(dt);
    this.tickShots(dt);
    this.tickSparks(dt);
    for (const [self, foe] of [[this.a, this.b], [this.b, this.a]])
      this.tickHits(self, foe, dt);"""
STEP_NEW = """    /* THE SHADES MOVE. Deliberately AFTER the real pair and deliberately
       BEFORE ballCollision, which is exactly where the real pair's own move()
       sits — a copy that "fights the same as the original" has to be ticked in
       the same order as one, or it is a different thing that looks similar.

       `tickFire` is absent: a shade of a melee relic has no `shot` to fire and
       a shade of a ranged one would double the relic's fire rate for free.
       `tickCharge` is absent: a shade has no ultimate, which is the interview
       answer that stops this being exponential. */
    this.tickShades(dt);
    this.ballCollision();
    this.tickClank(dt);
    this.tickShots(dt);
    this.tickSparks(dt);
    for (const [self, foe] of [[this.a, this.b], [this.b, this.a]])
      this.tickHits(self, foe, dt);
    /* Both directions, after the real pair and never instead of it: a shade
       swings at the foe, and the foe swings back. Rick: the copies "can be
       killed", and nothing in the engine's own hit loop would ever offer one
       as a target. */
    this.tickShadeHits(dt);"""

# =========================================== engine: collisions and binds ===
BALL_OLD = """  ballCollision(){
    const a = this.a, b = this.b, R = CONFIG.physics.ballR;
    const dx = b.x - a.x, dy = b.y - a.y;"""
BALL_NEW = """  ballCollision(){
    this._ballPair(this.a, this.b);
    /* A shade bounces off the FOE and off nothing else — not off its sibling
       and not off the ball that made it. Zero iterations in every match that
       does not contain this relic, which is the whole identity argument. */
    for (const s of this.shades)
      if (s.alive) this._ballPair(s, this.shadeFoe(s));
  }

  _ballPair(a, b){
    const R = CONFIG.physics.ballR;
    const dx = b.x - a.x, dy = b.y - a.y;"""

CLANK_OLD = """  tickClank(dt){
    if (this.clankCd > 0 || !this.a.alive || !this.b.alive) return;
    const A = this.a, B = this.b;
    if (A.stun > 0 && B.stun > 0) return;"""
CLANK_NEW = """  tickClank(dt){
    /* THE REAL PAIR IS TESTED FIRST, AND THAT ORDER IS THE BALANCE.

       Rick's exclusion is intra-team only, so the shades bind the foe like
       anything else. `clankCd` is a single global cooldown and `_clankPair`
       returns immediately while it is up — so three balls on one foe do NOT
       triple the clank rate, they make a clank likelier to EXIST. That is the
       difference between "the copies fight" and "the copies win the fight",
       and it falls out of the cooldown rather than out of a special case.

       Testing the real pair first also means a bind that both a shade and the
       original could have won is still the original's. */
    this._clankPair(this.a, this.b);
    for (const s of this.shades)
      if (s.alive) this._clankPair(s, this.shadeFoe(s));
  }

  _clankPair(A, B){
    if (this.clankCd > 0 || !A.alive || !B.alive) return;
    if (A.stun > 0 && B.stun > 0) return;"""

# ================================================= engine: the ult clock ====
TICKTOP_OLD = """    if (f.ultHarrow && (!f.alive || !foe.alive || this.over)){
      f.ultHarrow = null;
      this.unstick(foe);
    }
    if (!f.alive || this.over) return;"""
TICKTOP_NEW = """    if (f.ultHarrow && (!f.alive || !foe.alive || this.over)){
      f.ultHarrow = null;
      this.unstick(foe);
    }
    /* ABOVE THE GUARD, for the reason the Harrowing's fuse is above it. A
       fatal blow arms `killFlight` and `checkEnd` deliberately holds the match
       OPEN while the loser flies into the wall; during those frames `over` is
       false and `move()` is still running. Put this below the guard and the
       winner spends its victory flight flanked by two copies of itself that
       nobody is going to dismiss. harrow_probe [10] forced this once already;
       twinshade_probe drives the same window here. */
    if (f.ultSplit && (!f.alive || !foe.alive || this.over)) this.endSplit(f, true);
    if (!f.alive || this.over) return;"""

TICKBODY_OLD = "    if (f.ultRadiant){"
TICKBODY_NEW = """    if (f.ultSplit){
      f.ultSplit.t += dt;
      /* Presentation only, read by drawShadeFire and nothing else.

         `lit` is the ARRIVAL and it is driven by the split hold, not by this
         clock — the fire has to ignite while the cell is dividing, and the
         hold is frozen time in which `ultSplit.t` does not advance. Ramping it
         here instead would leave the whole pause unlit and then snap the flame
         on the frame the hall started moving again.

         What this owns is the GUTTER: the last quarter, so the expiry has a
         warning rather than the copies simply vanishing. */
      const k = f.ultSplit.t / f.ultSplit.dur;
      f.ultSplit.k = (f.ultSplit.lit === undefined ? 1 : f.ultSplit.lit)
                   * Math.min(1, (1 - k) / 0.25 + 0.25);
      if (f.ultSplit.t >= f.ultSplit.dur) this.endSplit(f);
    }
    if (f.ultRadiant){"""

# ============================================ engine: the hall stops ========
#
# Rick: "lets have the fight pause for a second while the duplicates split off
# the original like a cell replicating".
#
# This is Ironbloom's latch machinery and deliberately so: that branch already
# proves the shape works — it takes over step() entirely so nothing in the
# simulation advances, while `this.t` keeps running so match duration stays
# honest and the presentation clock runs with it, which is what lets a
# set-piece play through a frozen world.
#
# Placed AFTER the latch branch and BEFORE hit stop. Before hit stop because
# the cast itself sets hitStop 0.08, and a hold that yielded to it would spend
# its first five frames not running.
HOLD_OLD = """      if (L.t >= L.dur) this.blast(L);
      return;
    }
    if (this.hitStop > 0){"""
HOLD_NEW = """      if (L.t >= L.dur) this.blast(L);
      return;
    }
    /* THE SPLIT. The hall is stopped while one ball becomes three. Nothing in
       the simulation advances — no movement, no swings, no clanks, no charge —
       but the match clock runs, so a fight is not silently lengthened by the
       ultimates cast in it. The daughters are already in `this.shades`; what
       this branch does is walk them out of the parent. */
    if (this.splitHold){
      const S = this.splitHold;
      S.t += dt;
      this.t += dt;
      this.hitStop = Math.max(this.hitStop, 0.03);   // the renderer's punch
      this.decayImpactOnly(dt);
      this.tickSplitHold(dt);
      if (S.t >= S.dur) this.releaseSplit();
      return;
    }
    if (this.hitStop > 0){"""

# ===================================================== engine: the cast =====
FIRE_ANCHOR = '    if (u.kind === "detonate"){'
FIRE_NEW = '''    /* THE THREEFOLD RESOLVES NOTHING HERE. It does not damage, it does not
       apply, it does not reach for the foe at all — it puts two more of this
       relic on the floor and turns on lifesteal for all three. Everything that
       follows is done by ordinary hits landed by ordinary fighters, which is
       why the ult has no `dmg` and no `apply` field to tune. */
    if (u.kind === "split"){
      const R = CONFIG.physics.ballR, A = CONFIG.arena, n = this.inset;
      const loX = n + R, hiX = A.w - n - R, loY = n + R, hiY = A.h - n - R;
      f.ultSplit = { t: 0, dur: u.dur, k: 0, lit: 0 };
      f.lifesteal = u.lifesteal;
      /* THE DAUGHTERS ARE BORN INSIDE THE PARENT AND WALK OUT OF IT.
         Rick: "like a cell replicating". So each one is created AT the
         caster's centre with no velocity, carrying an `emerge` record of where
         it is going, and the hold branch in step() lerps it there over a
         second of stopped hall. Nothing about the placement search changed —
         it just runs now to decide the DESTINATION rather than the spawn. */
      const head = Math.atan2(f.vy, f.vx);
      const born = [];
      for (let i = 0; i < u.shades; i++){
        const s = new Fighter(f.w, f.side, this.rng);
        s.shade  = { owner: f };
        s.noUlt  = true;
        s.lifesteal = u.lifesteal;
        s.maxHp  = s.hp = Math.round(CONFIG.combat.baseHP * u.hp);
        s.hpGhost = s.hp;
        s.born   = 0;
        /* PLACED CLEAR OF THE CASTER'S OWN SHELL, AND A CLAMP IS NOT ENOUGH
           TO DO IT. A body left inside `R * 2` resolves a collision on the
           frame the hall restarts and the split fires the pair out like a nova
           — the splinters' trap, one object class along.

           The first cut clamped the ideal position into the hall, which is
           correct only away from a wall: cast with the caster's back to one
           and the clamp drags the daughter straight back into the shell it
           came out of. Every forced cast in the harness happened at frame one
           in open floor and passed; the check only failed once it was shown
           NATURAL casts, which happen wherever the fight happens to be.

           So the angle is SEARCHED. Twelve candidates off the ideal,
           alternating either side so the pair still comes out abreast where
           there is room, and the first that fits the hall untouched wins.
           Deterministic — no rng, because a relic not in a match must not
           perturb the draw order of one that is. */
        const want = head + TAU * (i + 1) / (u.shades + 1);
        let a = want, px = 0, py = 0, placed = false;
        for (let t = 0; t < 12 && !placed; t++){
          const off = (t === 0) ? 0
                    : (TAU / 12) * Math.ceil(t / 2) * (t % 2 ? 1 : -1);
          a = want + off;
          px = f.x + Math.cos(a) * R * u.spread;
          py = f.y + Math.sin(a) * R * u.spread;
          placed = px >= loX && px <= hiX && py >= loY && py <= hiY;
        }
        s.x = f.x; s.y = f.y;
        s.vx = 0;  s.vy = 0;
        s.emerge = { x0: f.x, y0: f.y,
                     x1: placed ? px : clamp(px, loX, hiX),
                     y1: placed ? py : clamp(py, loY, hiY), a };
        /* Out of phase with the parent and with each other, or three balls
           spin as one object and the hall reads as a rendering error. */
        s.theta   = f.theta + TAU * (i + 1) / (u.shades + 1);
        s.spinDir = f.spinDir;
        this._initChain(s);
        this.shades.push(s);
        born.push(s);
      }
      this.splitHold = { src: f === this.a ? "a" : "b", t: 0,
                         dur: u.hold === undefined ? 1.0 : u.hold };
      this.ring(f.x, f.y, f.aff.core, 6, R * 4.4, 0.7, 8);
      this.shake = Math.max(this.shake, 22);
      /* NO SFX.play HERE. `fireUlt` already fired one above the kind
         dispatch with `w: f.w.id`, so the sound is keyed on the RELIC ID and
         a second call here would play two. See the SFX branch. */
      return;
    }
'''

# ============================================ engine: the shades themselves =
SHADE_ANCHOR = "  checkEnd(){"
SHADE = '''  /* ------------------------------------------------------- THE SHADES --
     Everything below runs over `this.shades`, which is empty in every match
     that does not contain this relic. `checkEnd` is deliberately NOT touched:
     it reads `this.a` and `this.b` and nothing else, so a shade dying cannot
     end a match and no guard had to be written to stop it. That is the payoff
     for keeping copies out of `a`/`b` rather than making them fighters of
     record and then defending against it everywhere. */

  /* A shade fights the FOE. Never its sibling, never the ball that made it —
     Rick's exclusion, and the reason no N x N pairing exists in this build. */
  shadeFoe(s){ return s.shade.owner === this.a ? this.b : this.a; }

  /* THE HALL IS STOPPED AND THE CELL IS DIVIDING.
     Called only from the splitHold branch, so nothing here has to guard
     against the ordinary tick running at the same time. */
  tickSplitHold(dt){
    const S = this.splitHold, f = this[S.src];
    const k = Math.min(1, S.t / S.dur);
    if (S.rejoin){
      /* THE REVERSE. Rick: "something like a reverse of the cell split where
         any surviving clones rejoin the original".

         SHORTER than the split, and the reason is dramatic rather than
         technical: the division is the moment this relic becomes something and
         the reunion is the moment it stops being it. Two equal pauses would
         give the ending the same weight as the transformation, and the hall is
         already stopped twice per cast. `ult.rejoin` is the knob. */
      const e2 = k * k * (3 - 2 * k);
      for (const s of this.shades){
        const E = s.emerge;
        if (!E || s.shade.owner !== f) continue;
        s.x = E.x0 + (E.x1 - E.x0) * e2;
        s.y = E.y0 + (E.y1 - E.y0) * e2;
        s.born = 1 - k;
        s.theta += s.w.spin * 0.55 * dt * s.spinDir;
      }
      /* the fire goes out as they come home, so the last thing on screen is
         one ball with no flame on it */
      if (f.ultSplit) f.ultSplit.k = f.ultSplit.lit = Math.pow(1 - k, 1.1);
      this.shake = Math.max(this.shake, 4 + 22 * Math.pow(k, 2.6));
      return;
    }
    /* smoothstep, then a small overshoot on the last fifth: a cell does not
       glide apart, it strains and then lets go */
    const e = k * k * (3 - 2 * k);
    const pop = k > 0.80 ? Math.sin((k - 0.80) / 0.20 * Math.PI) * 0.06 : 0;
    for (const s of this.shades){
      const E = s.emerge;
      if (!E || s.shade.owner !== f) continue;
      s.x = E.x0 + (E.x1 - E.x0) * (e + pop);
      s.y = E.y0 + (E.y1 - E.y0) * (e + pop);
      s.born = k;
      /* the daughters turn while they separate, so the pair is visibly two
         objects and not one shape being stretched */
      s.theta += s.w.spin * 0.55 * dt * s.spinDir;
    }
    /* THE FIRE IGNITES ON THE DIVISION, not after it. `ultSplit.t` does not
       advance in frozen time, so if the arrival ramp lived on that clock the
       whole pause would be unlit and the flame would snap on the frame the
       hall restarted. */
    if (f.ultSplit) f.ultSplit.k = f.ultSplit.lit = Math.pow(k, 1.3);
    /* a tremor that builds and then breaks, so the ear and the screen agree
       about where the separation is */
    this.shake = Math.max(this.shake,
                          k < 0.82 ? 6 + 26 * Math.pow(k, 2.4) : 34 * (1 - (k - 0.82) / 0.18));
  }

  releaseSplit(){
    const S = this.splitHold, f = this[S.src];
    this.splitHold = null;
    if (S.rejoin){ this.dropSplit(f, true); return; }
    if (f && f.ultSplit) f.ultSplit.lit = 1;
    const R = CONFIG.physics.ballR;
    for (const s of this.shades){
      const E = s.emerge;
      if (!E) continue;
      s.x = E.x1; s.y = E.y1;
      s.vx = Math.cos(E.a) * CONFIG.physics.cruise;
      s.vy = Math.sin(E.a) * CONFIG.physics.cruise;
      s.born = 1;
      s.emerge = null;
      this.ring(s.x, s.y, s.aff.glow, 4, R * 3.0, 0.5, 6);
      this.spawnFx(s.x, s.y, s.aff.core, 20, 260, 0.55, 4);
    }
    if (f) this.ring(f.x, f.y, f.aff.core, 6, R * 4.4, 0.6, 8);
    this.shake = Math.max(this.shake, 30);
  }

  /* THE DRAIN. Rick: "im picturing the balls as sucking the lifeforce from
     their enemy. lets show something being pysically taken and streamed back".

     Presentation only and it never touches the simulation — but it is a LIST
     of motes rather than a flag, because "taken" needs travel: a glow on the
     healer says it got better, a stream from the foe says where it came from.

     Each mote leaves in the FOE'S OWN affinity colour and arrives in the heal
     green, crossfading on the way. That is the whole idea in one property:
     their life, becoming somebody else's.

     `tgt` holds the FIGHTER and not a point, so the stream follows a ball that
     is still moving. Deterministic: every stagger, bow and radius is a
     function of the mote's index, never rng — a presentation object must not
     perturb the draw order of a match. */
  drain(from, to, amount, wasted){
    /* ARCHING LIGHT TRAILS THAT SWIRL AND TRICKLE BACK. Rick, on two previous
       cuts of this: *"I was more picturing arching light trails that swirl and
       trickle back to twinshade. lit up with glow effects and arc then trickle
       off and fade as they trickle back."*

       Both earlier versions were the wrong IDIOM, not the wrong size. v1 was
       small dots on a bowed path; v2 made them fewer and bigger on the theory
       that a thing being taken is a chunk. Neither is a trail — a dot with a
       stub behind it is a projectile, and a projectile is a thing being
       thrown, which is the opposite of what this is.

       A strand is a PATH now, drawn along its own recent history, swirling
       about the axis between the two balls. Three things follow from the word
       "trickle" and each of them reverses a decision from v2:

         MANY and THIN, not few and fat — a trickle is a lot of small flow
         LONG-LIVED and WIDELY STAGGERED — 22 strands leaving over 1.1s and
           living 0.9s each is one heal trickling for over two seconds, which
           is longer than the gap to the next heal
         GLOWING — three additive passes per strand, wide and dim to narrow
           and white. That is what "lit up with glow effects" costs. */
    const n = wasted ? 7
            : Math.max(11, Math.min(22, Math.round(9 + amount * 1.2)));
    /* `ribbon` scales the strand thickness and nothing else — not the count,
       not the length, not the swirl. Read off the HEALER's own ult data, which
       a shade shares with the ball that made it. */
    const rw = (to.w.ult && to.w.ult.ribbon) || 1;
    const ak = (to.w.ult && to.w.ult.arc) || 1;
    for (let i = 0; i < n; i++){
      this.drains.push({
        x0: from.x, y0: from.y, tgt: to, t: 0,
        delay: i * 0.052,
        life: 0.80 + (i % 5) * 0.075,
        /* how far round the axis it turns over the whole flight, and which
           way. Alternating hands make the bundle read as a braid rather than
           as one corkscrew. */
        swirl: ((i % 2) ? 1 : -1) * (2.2 + 2.3 * (((i * 3) % 4) / 3)),
        phase: i * 2.3999632,                       // golden angle, fixed
        /* orbit radius as a fraction of the gap. Opens early, closes into the
           shell — the swirl has to TIGHTEN as it arrives or it reads as
           circling rather than as being drawn in. */
        amp: (0.13 + 0.21 * (((i * 5) % 4) / 3)) * ak,
        w: (3.2 + 1.9 * ((i % 3) / 2)) * rw,
        c0: from.aff.core,
        /* how far along it survives. A wasted strand never arrives. */
        cut: wasted ? 0.45 + ((i % 3) * 0.06) : 1,
      });
    }
    from.drained = 1;
    this.ring(from.x, from.y, wasted ? "#B8C9BC" : "#8FE3A0",
              CONFIG.physics.ballR * 1.15, CONFIG.physics.ballR * 0.35,
              0.34, wasted ? 2 : 4);
    if (this.drains.length > 420)
      this.drains.splice(0, this.drains.length - 420);
  }

  tickShades(dt){
    for (let i = this.shades.length - 1; i >= 0; i--){
      const s = this.shades[i];
      if (!s.alive){ this.killShade(i); continue; }
      const foe = this.shadeFoe(s);
      s.born = Math.min(1, s.born + dt / (s.shade.owner.w.ult.arrive || 0.28));
      this.tickStatus(s, dt);
      this.move(s, foe, dt);
      this.tickWeapon(s, foe, dt);
    }
  }

  /* BOTH DIRECTIONS, and the second one is the half the engine would never
     have offered: the real pair's hit loop is `[[a,b],[b,a]]`, so without this
     the foe could not touch a shade and "the copies can be killed" would be a
     sentence with no code under it.

     `cool` is false on the foe's pass because the foe's per-blade cooldown was
     already ticked by the real loop this frame. Tick it again per shade and a
     foe facing two copies swings three times as often — which is a buff to the
     thing this ultimate is supposed to be attacking.

     Hits are RESOLVED on the shade and CREDITED to the caster. `resolveHit`
     increments `self.hits`, and verify.py's contact floor reads
     `r.hits.a + r.hits.b` — leave the count on the shade and a third of this
     relic's contact silently does not exist to the one check that would catch
     a relic that ends fights without landing blows. */
  tickShadeHits(dt){
    for (const s of this.shades){
      if (!s.alive) continue;
      const foe = this.shadeFoe(s), own = s.shade.owner;
      const h0 = s.hits, d0 = s.dealt, c0 = s.crits;
      this.tickHits(s, foe, dt);
      own.hits  += s.hits  - h0;
      own.dealt += s.dealt - d0;
      own.crits += s.crits - c0;
      if (s.alive) this.tickHits(foe, s, dt, false);
    }
  }

  /* ONE BEAT — the interview answer, and the reunion does not change it.
     Every survivor still goes on a single frame; what changed is WHICH frame,
     because they now walk home first. `hard` is the path for the cases where
     there is nothing to walk home to — a dead caster, a dead foe, a finished
     match — and it drops them where they stand. */
  endSplit(f, hard){
    if (!f.ultSplit) return;
    const mine = this.shades.filter(s => s.shade.owner === f);
    if (hard || !mine.length || this.over || this.splitHold){
      this.dropSplit(f, false);
      return;
    }
    for (const s of mine)
      s.emerge = { x0: s.x, y0: s.y, x1: f.x, y1: f.y, a: 0, rejoin: true };
    this.splitHold = { src: f === this.a ? "a" : "b", t: 0, rejoin: true,
                       dur: f.w.ult.rejoin === undefined ? 0.55 : f.w.ult.rejoin };
    SFX.play("ult", { w: "twinshade-rejoin" });
  }

  /* The removal itself. `merged` is the reunion: the burst is on the PARENT
     and not on wherever each copy happened to be, because what the viewer has
     just watched is three things becoming one, and three separate puffs would
     say the opposite. */
  dropSplit(f, merged){
    if (!f) return;
    f.ultSplit = null;
    f.lifesteal = 0;
    const R = CONFIG.physics.ballR;
    for (let i = this.shades.length - 1; i >= 0; i--){
      const s = this.shades[i];
      if (s.shade.owner !== f) continue;
      if (!merged){
        this.spawnFx(s.x, s.y, s.aff.core, 26, 300, 0.7, 5);
        this.ring(s.x, s.y, s.aff.glow, 6, R * 2.6, 0.5, 5);
      }
      s.emerge = null;
      this.shades.splice(i, 1);
    }
    if (merged){
      this.spawnFx(f.x, f.y, f.aff.core, 46, 330, 0.8, 5);
      /* an INWARD ring — r0 > r1, so it closes on the ball instead of
         expanding off it. Every other ring in this game opens. */
      this.ring(f.x, f.y, f.aff.core, R * 1.5, R * 0.2, 0.38, 4);
      this.shake = Math.max(this.shake, 20);
    }
  }

  /* A KILLED SHADE IS JUST GONE. Rick's call, and it is the answer that keeps
     the foe's incentive simple: kill the copies or eat three attackers. It
     pays the foe nothing and returns the caster nothing.

     It still bursts, because a ball that dies in this game shatters and a copy
     that merely blinked out would read as the ultimate having expired early. */
  killShade(i){
    const s = this.shades[i];
    this.spawnFx(s.x, s.y, s.aff.core, 54, 430, 1.0, 6);
    this.ring(s.x, s.y, s.aff.glow, 6, CONFIG.physics.ballR * 4, 0.7, 7);
    this.shake = Math.max(this.shake, 22);
    this.shades.splice(i, 1);
  }

'''

# ============================================================ renderer ======
DRAW_OLD = """    this.drawUltUnder(m);
    this.drawFx(m);
    this.drawFighter(m, m.b);
    this.drawFighter(m, m.a);"""
DRAW_NEW = """    this.drawUltUnder(m);
    this.drawFx(m);
    /* Fire first (it is an aura and belongs under everything), then the copies,
       then the real pair — so the two balls that own the health bars are on
       top of the two that do not. */
    this.drawShadeFire(m);
    this.drawSplitHold(m);
    this.drawShades(m);
    this.drawFighter(m, m.b);
    this.drawFighter(m, m.a);
    /* over the fighters: the last thing a mote does is go INTO a shell */
    this.drawDrains(m);"""

ART_ANCHOR = "  drawSparks(m){"
ART = '''  /* THE COPIES. `drawFighter` is already per-fighter and already handles
     everything a shade has, so this is a transform and a call rather than a
     second renderer — a copy that drew through its own path would drift away
     from the thing it is a copy of on the first art revision.

     The arrival is a SCALE, not a fade. `drawFighter` sets `globalAlpha` inside
     its own save/restore blocks for the trail and the swing ribbons, so an
     alpha set out here is overwritten before it reaches the shell; and scaling
     up out of the caster reads as "stepping out of" in a way a cross-fade does
     not. 0.55 -> 1.0 over `ult.arrive`. */
  drawShades(m){
    if (!m.shades.length) return;
    const c = this.ctx;
    for (const s of m.shades){
      if (!s.alive) continue;
      /* An emerging daughter starts almost at nothing, because it is coming
         OUT of the parent; one merely fading in from 55% reads as a ball that
         was always there. A copy in ordinary flight uses the gentler floor. */
      const b = s.born === undefined ? 1 : s.born;
      const k = s.emerge ? (0.10 + 0.90 * b) : (0.55 + 0.45 * b);
      c.save();
      c.translate(s.x, s.y); c.scale(k, k); c.translate(-s.x, -s.y);
      this.drawFighter(m, s);
      c.restore();
    }
  }

  /* THE CELL DIVIDING. Rick: "lets have the fight pause for a second while
     the duplicates split off the original like a cell replicating".

     The daughters are ordinary Fighters walking out of the parent, drawn by
     `drawShades` like any other copy — so what THIS draws is the only part
     that is not a ball: the MEMBRANE still joining them, and the strain on the
     parent. Without the neck the pause is two balls sliding out from behind a
     third; with it, it is one thing coming apart, which is the note. */
  drawSplitHold(m){
    const S = m.splitHold;
    if (!S) return;
    const f = m[S.src];
    if (!f || !f.alive) return;
    const c = this.ctx, R = CONFIG.physics.ballR;
    const k = Math.min(1, S.t / S.dur);
    /* on the reunion the neck runs the other way: thin when they are far and
       thickening as they arrive, so the merge reads as absorption */
    const pinch = S.rejoin ? Math.pow(k, 1.4) : Math.pow(1 - k, 1.5);
    c.save();
    c.globalCompositeOperation = "lighter";
    for (const s of m.shades){
      if (!s.emerge || s.shade.owner !== f) continue;
      const dx = s.x - f.x, dy = s.y - f.y;
      const L = Math.hypot(dx, dy);
      /* A NECK, NOT A SHEET. Drawn only while the daughter is still close
         enough for the two shells to be plausibly one body — beyond that a
         filled band between two distant balls is a triangular wing, which is
         what the first cut of the reunion looked like. */
      if (L < 2 || L > R * 3.4) continue;
      const nx = -dy / L, ny = dx / L;
      const w = R * 0.95 * pinch;
      if (w < 0.5) continue;
      const mxp = f.x + dx * 0.5, myp = f.y + dy * 0.5;
      const edge = (sgn) => {
        c.beginPath();
        c.moveTo(f.x + nx * R * 0.78 * sgn, f.y + ny * R * 0.78 * sgn);
        c.quadraticCurveTo(mxp + nx * w * sgn, myp + ny * w * sgn,
                           s.x + nx * R * 0.62 * sgn, s.y + ny * R * 0.62 * sgn);
      };
      const fade = 1 - Math.min(1, L / (R * 3.4));
      c.globalAlpha = 0.42 * (0.35 + 0.65 * fade);
      c.fillStyle = f.aff.core;
      c.beginPath();
      c.moveTo(f.x + nx * R * 0.78, f.y + ny * R * 0.78);
      c.quadraticCurveTo(mxp + nx * w, myp + ny * w,
                         s.x + nx * R * 0.62, s.y + ny * R * 0.62);
      c.lineTo(s.x - nx * R * 0.62, s.y - ny * R * 0.62);
      c.quadraticCurveTo(mxp - nx * w, myp - ny * w,
                         f.x - nx * R * 0.78, f.y - ny * R * 0.78);
      c.closePath(); c.fill();
      /* the surface of it. A filled band with no edge is a smear; the two
         bright rims are what make it a membrane under tension. */
      c.globalAlpha = 0.70 * (0.30 + 0.70 * fade);
      c.strokeStyle = f.aff.glow;
      c.lineWidth = 1.5 + 2.2 * pinch;
      edge(1); c.stroke();
      edge(-1); c.stroke();
    }
    /* the parent strains and then relaxes. On the reunion it swells as the
       daughters land in it instead. */
    const swell = S.rejoin
      ? 0.26 * Math.pow(k, 2.2)
      : Math.sin(Math.min(1, k / 0.72) * Math.PI) * 0.26;
    if (swell > 0.005){
      c.globalAlpha = 0.30;
      c.fillStyle = f.aff.core;
      c.beginPath(); c.arc(f.x, f.y, R * (1 + swell), 0, TAU); c.fill();
    }
    c.restore();
  }

  /* THE DRAIN. Rick: "im picturing the balls as sucking the lifeforce from
     their enemy. lets show something being pysically taken and streamed back."

     The green +N was already there and it is not enough — a number over the
     healer says it got better, it does not say where from. TRAVEL is the whole
     content of the note, so each mote is drawn on a bowed path from the foe to
     the thing that tore it off, and it CHANGES COLOUR on the way: it leaves in
     the foe's own affinity and arrives in the heal green. Two overlaid draws
     under `lighter` crossfade cleanly and cost no colour arithmetic.

     Drawn OVER both fighters, because the last thing that happens is the mote
     going into a shell and it has to be seen to arrive. */
  drawDrains(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    /* THE WOUND. The thing being fed on looks fed on — a rim and a set of
       wisps sitting just OUTSIDE the shell.

       The first cut filled the shell with green under `lighter` at half alpha,
       and `lighter` cannot darken anything: on a bright foe it summed to a
       white disc, which reads as a ball exploding rather than one being drained.
       Nothing that is losing should get brighter. */
    for (const src of [m.a, m.b]){
      const lvl = src.drained || 0;
      if (lvl <= 0.02 || !src.alive) continue;
      c.save();
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = 0.28 * lvl;
      c.strokeStyle = "#8FE3A0";
      c.lineWidth = 1.4 + 2.2 * lvl;
      c.beginPath(); c.arc(src.x, src.y, R * 1.06, 0, TAU); c.stroke();
      for (let i = 0; i < 7; i++){
        const ph = i * 2.3999632;
        const a2 = m.t * 0.9 + ph;
        const rise = 0.5 + 0.5 * Math.sin(m.t * 5.5 + ph * 2.3);
        const r0 = R * 1.02, r1 = R * (1.10 + 0.34 * rise * lvl);
        c.globalAlpha = 0.30 * lvl * rise;
        c.strokeStyle = "#CFFFDC";
        c.lineWidth = 1.0 + 1.6 * rise;
        c.beginPath();
        c.moveTo(src.x + Math.cos(a2) * r0, src.y + Math.sin(a2) * r0);
        c.lineTo(src.x + Math.cos(a2 + 0.16) * r1, src.y + Math.sin(a2 + 0.16) * r1);
        c.stroke();
      }
      c.restore();
    }

    if (!m.drains.length) return;
    c.save();
    c.globalCompositeOperation = "lighter";
    c.lineCap = "round";
    c.lineJoin = "round";
    const SEG = 13, TAIL = 0.40;
    for (const d of m.drains){
      const u = (d.t - d.delay) / d.life;
      if (u <= 0 || u > 1) continue;
      const T = d.tgt;
      const dx = T.x - d.x0, dy = T.y - d.y0;
      const L = Math.hypot(dx, dy) || 1;
      const nx = -dy / L, ny = dx / L;
      /* a wasted strand thins out and vanishes short of the ball rather than
         being switched off */
      let a = 1;
      if (d.cut < 1){
        a = 1 - Math.max(0, (u - (d.cut - 0.22)) / 0.22);
        if (a <= 0) continue;
      }
      /* THE STRAND'S POSITION AT PARAMETER q — eased advance along the axis
         plus a swirl about it. `lag` displaces along the axis on the far half
         of each turn, which is what makes a 2D sine read as going AROUND
         something rather than waving side to side. */
      const P = (q) => {
        const e = q * q * (3 - 2 * q);
        const rad = d.amp * L * Math.sin(Math.PI * Math.min(1, q * 1.06))
                  * (1 - q * 0.45);
        const ang = d.phase + d.swirl * q;
        const off = Math.cos(ang) * rad;
        const e2 = Math.max(0, Math.min(1, e + Math.sin(ang) * rad * 0.30 / L));
        return [d.x0 + dx * e2 + nx * off, d.y0 + dy * e2 + ny * off];
      };
      const pts = [];
      for (let i = 0; i <= SEG; i++){
        const q = u - TAIL * (1 - i / SEG);
        if (q < 0) continue;
        pts.push(P(q));
      }
      if (pts.length < 2) continue;
      /* IT FADES AS IT ARRIVES, AND THAT IS THE WHOLE BACK HALF OF THE NOTE:
         "arc then trickle off and fade as they trickle back to twinshade."

         The first cut of the trail did the opposite — brightest and widest at
         the head, because that is how a projectile is drawn and a projectile
         was still the model. A thing being absorbed gets DIMMER as it lands.
         So the strand peaks in the middle of its arc and thins out over the
         second half, and by the time it reaches the shell there is almost
         nothing left of it to stop. */
      const fade = d.cut >= 1
        ? (u > 0.42 ? Math.max(0, 1 - 0.80 * Math.pow((u - 0.42) / 0.58, 1.30)) : 1)
        : 1;
      /* THREE PASSES = the glow. Wide and dim in the foe's own colour, the
         body in heal green, a white core. Per SEGMENT rather than as one
         polyline, so the strand tapers from nothing at the tail to full at the
         head — a constant-width trail is a tube, and a tube does not trickle. */
      /* Alphas and widths are both up hard on the first cut of this, and the
         reason is `lighter` plus the taper compounding: at 0.11 / 0.26 / 0.55
         under a k-SQUARED ramp, five sixths of every strand was below the
         threshold at which anything is visible against a lit hall, and what
         survived was a faint hook near the head. The taper is k^1.2 now, so
         the trail reads along its whole length instead of only where it is
         thickest. */
      /* THE THREE PASSES ARE NOW SPATIAL, NOT STACKED, and that fixes both
         remaining faults at once.

         COLOUR. The wide pass is the FOE'S OWN colour, and against a pale foe
         like Lightkeeper that is near-white — laid over the whole strand it
         summed with the white core and the hall got silver ropes, with the
         green that actually says "life" buried underneath. So the foe's colour
         is drawn on the TAIL ONLY, where the strand just left them; the green
         owns the body; white is a highlight on the leading edge alone. Which
         is the same idea the crossfade was reaching for, expressed along the
         strand instead of over time — and it survives arriving at a ball of
         any colour, which a timed crossfade did not.

         BEADING. Drawing each segment as its own stroke put a round cap at
         every joint, and under `lighter` twenty-six overlapping caps per
         strand read as a dotted line. Each run is ONE path now, and the taper
         comes from three overlapping runs of decreasing length and increasing
         width — the same trick the flame tongues use. Nine strokes a strand
         instead of thirty-nine, and no joints to pile up. */
      const run = (from, wid, al, col) => {
        if (pts.length - from < 2 || al <= 0.004) return;
        c.globalAlpha = al;
        c.strokeStyle = col;
        c.lineWidth = Math.max(0.4, wid);
        c.beginPath();
        c.moveTo(pts[from][0], pts[from][1]);
        for (let i = from + 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]);
        c.stroke();
      };
      const tailRun = (to, wid, al, col) => {
        if (to < 2 || al <= 0.004) return;
        c.globalAlpha = al;
        c.strokeStyle = col;
        c.lineWidth = Math.max(0.4, wid);
        c.beginPath();
        c.moveTo(pts[0][0], pts[0][1]);
        for (let i = 1; i <= to; i++) c.lineTo(pts[i][0], pts[i][1]);
        c.stroke();
      };
      const N2 = pts.length - 1;
      const base = d.w * (1 - 0.42 * u), A2 = a * fade;
      /* where it came from — the tail, in the foe's own colour */
      tailRun(Math.floor(N2 * 0.60), base * 5.2, 0.085 * A2, d.c0);
      tailRun(Math.floor(N2 * 0.40), base * 2.6, 0.135 * A2, d.c0);
      /* what it is — the body, in heal green, three runs deep */
      run(0,                        base * 4.4, 0.16 * A2, "#8FE3A0");
      run(Math.floor(N2 * 0.35),    base * 2.4, 0.44 * A2, "#8FE3A0");
      run(Math.floor(N2 * 0.62),    base * 1.5, 0.62 * A2, "#B6F5C6");
      /* the leading edge only */
      run(Math.floor(N2 * 0.80),    base * 0.75, 0.55 * A2, "#EAFFF0");
      const h = pts[pts.length - 1];
      /* A SMALL head, not a ball on a string. The first cut put a white disc
         1.3x the strand width at the tip with a 2.9x halo round it, and
         twenty-two of those is a handful of glowing marbles being thrown —
         which is the projectile reading again, and the exact opposite of a
         trickle. */
      c.globalAlpha = 0.55 * a * fade;
      c.fillStyle = "#DFFFE9";
      c.beginPath(); c.arc(h[0], h[1], d.w * 0.52, 0, TAU); c.fill();
      c.globalAlpha = 0.20 * a * fade;
      c.fillStyle = "#8FE3A0";
      c.beginPath(); c.arc(h[0], h[1], d.w * 1.35, 0, TAU); c.fill();
      /* IT LANDS. The strand is deliberately at its dimmest by the time it
         reaches the shell — "fade as they trickle back" — and a thing that
         only fades never visibly ARRIVES. So the last twelfth of the flight
         puts a small absorption flare on the ball itself: the fade says it is
         being taken in, this says it got there. */
      if (u > 0.88 && d.cut >= 1){
        const q = (u - 0.88) / 0.12;
        c.globalAlpha = 0.50 * (1 - q) * a;
        c.fillStyle = "#B6F5C6";
        c.beginPath();
        c.arc(T.x, T.y, R * (0.55 + 0.55 * q), 0, TAU);
        c.fill();
      }
    }
    c.restore();
  }

  /* THE PURPLE FIRE. Rick: "it glows with purple fire (take going super sayan
     from dragonball as inspiration for this animation)".

     Two decisions are what make that reference read rather than a generic halo.

     THE FLAME GOES UP, always, whichever way the ball is travelling. A corona
     that trails the motion is a comet, and a comet is a fast object; this has
     to be a transformed one. Standing fire on a moving ball is exactly the
     Dragon Ball cue.

     IT IS LICKED, NOT SMOOTH. Eleven tongues on their own phases and their own
     lengths, so the silhouette changes every frame. A steady ring around a ball
     is an aura and reads as a status; a flickering upward tongue reads as a
     character doing something.

     ON THE CASTER ONLY — Rick's call, and also the one thing on screen that
     says which of three identical purple balls carries the health bar. v37 §8.2
     makes this the v28 same-affinity smudge at its worst and this is the answer
     to it.

     EVERY PHASE IS A FUNCTION OF `m.t` AND A FIXED PER-TONGUE OFFSET. Never
     Math.random(): the shake offset in draw() is the last place this project
     feeds it into a frame and it is a standing open decision because it blocks
     any frame-exact regression test. Nothing new should add to that debt. */
  drawShadeFire(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.a, m.b]){
      const S = f.ultSplit;
      if (!S || !f.alive) continue;
      const k = S.k === undefined ? 1 : S.k;
      if (k <= 0.001) continue;
      c.save();
      c.globalCompositeOperation = "lighter";
      c.lineCap = "round";

      /* THE ENVELOPE. Second revision, and the correction is the same one
         the mini-scythes needed: the first cut drew tongues only across the
         TOP of the shell and leaned them all toward vertical, which is a
         searchlight standing next to a ball, not a ball that is on fire.

         Fire wraps the thing it is burning. So a tongue leaves EVERY point of
         the rim, and its LENGTH is a function of how far up the rim it starts
         — long licks off the crown, stubs off the underside. That envelope is
         the Dragon Ball silhouette: tight to the body, tallest above it. */
      /* THE ENVELOPE. Third revision, and each correction is recorded because
         each one was a different way of not being fire.

         (1) Tongues only across the TOP, all leaning to one point: a party hat.
         (2) Tongues all round but drawn as STROKES with round caps: noodles.
             A flame lick is wide where it leaves the surface and comes to a
             POINT — the taper is most of what makes it read, and no stroke has
             one. They are filled tapered paths now.
         (3) Every tongue the same length: a crown. Each carries a fixed
             per-tongue length factor as well as its own oscillator, so the
             silhouette is ragged at any instant AND changes shape over time.

         Fire wraps the thing it is burning, so a tongue leaves EVERY point of
         the rim and its length is a function of how far up the rim it starts —
         long licks off the crown, stubs off the underside. That envelope is the
         Dragon Ball silhouette: tight to the body, tallest above it. */
      const N = 24, H = R * (0.95 + 1.65 * k);
      for (let i = 0; i < N; i++){
        const ph = i * 2.3999632;                       // golden angle, fixed
        /* independent rates, one per tongue: a shared rate makes the whole
           envelope pulse as one object, which reads as a balloon inflating */
        const fl   = 0.5 + 0.5 * Math.sin(m.t * (8.5 + (i % 5)) + ph * 3.1);
        const wob  = Math.sin(m.t * (4.1 + (i % 3) * 1.7) + ph);
        const vary = 0.50 + 0.50 * (((i * 5) % 7) / 6);   // fixed, per tongue
        /* the base angles are jittered off even spacing, because sixteen
           evenly-spaced anything reads as a mechanism */
        const base = (i / N) * TAU + Math.sin(ph) * 0.09;
        const up   = 0.5 - 0.5 * Math.sin(base);   // 1 at the crown (+y is down)
        const len  = H * (0.18 + 0.82 * up) * vary * (0.45 + 0.55 * fl);
        const bx = f.x + Math.cos(base) * R * 0.94;
        const by = f.y + Math.sin(base) * R * 0.94;
        /* it rises, and drifts along its own outward normal — a tongue that
           only rises is a stripe, and sixteen stripes are a barcode */
        const tx = bx + Math.cos(base) * len * 0.26 + wob * R * 0.24;
        const ty = by - len;
        const mx = bx + Math.cos(base) * len * 0.34 + wob * R * 0.30;
        const my = by - len * 0.52;
        /* the base is spread along the TANGENT at its own footing, so the
           tongue sits on the shell instead of poking out of it */
        const w  = R * (0.27 + 0.17 * fl) * (0.35 + 0.65 * up);
        const nx = -Math.sin(base), ny = Math.cos(base);
        /* `lk` shortens the tongue as well as narrowing it, which is what
           lets the three passes STACK INTO A GRADIENT instead of averaging to
           white. Under `lighter` a white core laid the full length of a red
           one does not read as a hot heart, it reads as a pale tongue — which
           is exactly what the first pass at Rick's note produced. */
        const tongue = (wk, lk) => {
          const ex = bx + (tx - bx) * lk, ey = by + (ty - by) * lk;
          const cx2 = bx + (mx - bx) * lk, cy2 = by + (my - by) * lk;
          c.beginPath();
          c.moveTo(bx + nx * w * wk, by + ny * w * wk);
          c.quadraticCurveTo(cx2 + nx * w * wk * 0.45, cy2 + ny * w * wk * 0.45,
                             ex, ey);
          c.quadraticCurveTo(cx2 - nx * w * wk * 0.45, cy2 - ny * w * wk * 0.45,
                             bx - nx * w * wk, by - ny * w * wk);
          c.closePath(); c.fill();
        };
        /* TWO PASSES, AND THE SECOND IS WHY THIS IS VISIBLE AT ALL. Umbral is
           core #A45CF0 / glow #DDB8FF and the shell it burns on is the same
           purple; purple on purple under `lighter` is a slightly brighter
           purple ball and no fire. The contrast has to be in VALUE, not hue —
           a wide pass in the school's own colour carries the identity, a
           narrow near-WHITE one inside it carries the heat, and the heart is
           brightest where the licks are longest. That is how fire is lit. */
        /* THREE PASSES, AND THE MIDDLE ONE IS RICK'S NOTE.
           v1 was purple-on-purple under `lighter`, which is a slightly
           brighter purple ball and no fire; the near-white heart fixed the
           VALUE but left it monochrome. Rick: "mix some red into the colors to
           make it really pop." Red is the one hue that is not already on this
           ball, on the vessel, or in the umbral palette — so it is the only
           thing that can separate flame from shell by HUE as well as value.

           Outside in: the school's purple carries the identity, a hot red
           carries the heat, a near-white heart carries the temperature. Real
           flame is layered the same way and in the same order. */
        /* THREE PASSES, LAYERED THE WAY A FLAME IS: white at the base, red
           through the body, the school's purple carrying the tips.

           v1 was purple-on-purple under `lighter` — a slightly brighter purple
           ball and no fire. v2 added a near-white heart, which fixed the VALUE
           and left it monochrome; Rick: "mix some red into the colors to make
           it really pop." v3 put red in and ran it the FULL LENGTH under a
           full-length white core, and `lighter` averaged the two back to pale
           pink. Red is the one hue that is not already on this ball, on the
           vessel or in the umbral palette, so it is the only thing that can
           separate flame from shell by hue as well as by value — and it only
           does that if nothing brighter is laid over the whole of it.

           So each pass is SHORTER than the one under it. The stack is a
           gradient up the tongue rather than three coincident shapes. */
        c.globalAlpha = (0.17 + 0.20 * fl) * k;
        c.fillStyle = f.aff.core;
        tongue(1.00, 1.00);
        c.globalAlpha = (0.26 + 0.34 * fl) * k * (0.40 + 0.60 * up);
        c.fillStyle = "#FF2E4D";
        tongue(0.82, 0.70);
        c.globalAlpha = (0.20 + 0.26 * fl) * k * (0.30 + 0.70 * up);
        c.fillStyle = "#FFB07A";
        tongue(0.52, 0.38);
        c.globalAlpha = (0.16 + 0.24 * fl) * k * (0.30 + 0.70 * up);
        c.fillStyle = "#FFF2E4";
        tongue(0.30, 0.17);
      }

      /* The seat. A DONUT and not a disc — transparent at the centre — so it
         lights the rim the fire comes off without washing the shell it is
         standing on. Lastlight's contact sheet made the same correction on the
         mini-scythes: "the glow was bigger than the blade... the blade is the
         object; the glow only says it is made of light." */
      const g = c.createRadialGradient(f.x, f.y, R * 0.55, f.x, f.y, R * 1.35);
      g.addColorStop(0, "rgba(0,0,0,0)");
      g.addColorStop(0.60, f.aff.core);
      g.addColorStop(1, "rgba(0,0,0,0)");
      c.globalAlpha = 0.34 * k;
      c.fillStyle = g;
      c.beginPath(); c.arc(f.x, f.y, R * 1.45, 0, TAU); c.fill();
      c.restore();
    }
  }

'''

# The interpolator. A shade not in these two lists strobes: `draw` is called at
# display rate and the sim steps at CONFIG.physics.dt, so an object outside the
# snapshot is drawn at whatever the last stepped position was while everything
# around it moves smoothly.
SNAP_OLD = """  for (const f of [m.a, m.b])
    this.snapObj(f, LERP_FIELDS.fighter, LERP_FIELDS.fighterAng, S);"""
SNAP_NEW = """  for (const f of [m.a, m.b])
    this.snapObj(f, LERP_FIELDS.fighter, LERP_FIELDS.fighterAng, S);
  /* Shades interpolate on the same fields as any other fighter. Left out they
     would strobe against a smoothly-moving hall — the one artefact a viewer
     reads as "the game is broken" rather than as a style. */
  for (const s of m.shades)
    this.snapObj(s, LERP_FIELDS.fighter, LERP_FIELDS.fighterAng, S);"""

LERP_OLD = "  for (const f of [m.a, m.b]) apply(f);"
LERP_NEW = """  for (const f of [m.a, m.b]) apply(f);
  for (const s of m.shades) apply(s);"""

# ================================== engine: the two gaps found by tracing ====
#
# Neither of these was found by watching a match. Both were found by following
# the control flow of a thing that had not been written yet, which is the only
# way either could have been found before it shipped.

# (a) THE MATCH ENDS AND THE SHADES DO NOT.
#
#     `step()` opens `if (this.over){ this.decay(dt); return; }`, so once the
#     match is over neither `tickShades` nor `tickCharge` is ever called again.
#     The kill itself lands in `tickHits`/`tickShadeHits`, which run AFTER
#     `tickCharge` in the same step — so the above-the-guard drop cannot catch
#     the frame the foe dies on, and two copies would freeze mid-air and keep
#     drawing through the entire verdict beat.
#
#     `decay` is the one method called on every path INCLUDING the over path,
#     which is why the drop goes here and not in `checkEnd`.
#
#     The killFlight window is NOT this case and is still handled above the
#     guard: there `checkEnd` returns early, `over` stays false, and
#     `tickCharge` does run.
DECAY_OLD = """  decay(dt){
    this.decayImpactOnly(dt);"""
DECAY_NEW = """  decay(dt){
    /* The ultimate cannot outlive the match. Zero-cost when the list is empty,
       which is every match without this relic and every frame of one with it
       up to the kill. */
    if (this.over && (this.shades.length || this.splitHold)){
      this.splitHold = null;
      for (const s of this.shades)
        this.spawnFx(s.x, s.y, s.aff.core, 20, 260, 0.6, 4);
      this.shades.length = 0;
      if (this.a.ultSplit) this.a.ultSplit = null;
      if (this.b.ultSplit) this.b.ultSplit = null;
      this.a.lifesteal = 0; this.b.lifesteal = 0;
    }
    this.decayImpactOnly(dt);"""

# (b) A SHADE'S HEALTH GHOST NEVER TICKS.
#
#     `hpGhost` is the draining tail behind the health reading, and on the
#     liquid build it is what the glass vessel's LEVEL is drawn from. Left out
#     of this loop a shade's vessel would sit at its spawn level for its whole
#     life — three balls on the floor and only two of them showing damage,
#     which reads as the copies being invulnerable.
GHOST_OLD = """    for (const f of [this.a, this.b]){
      if (f.hpGhost == null) f.hpGhost = f.hp;
      f.ringFlash = Math.max(0, (f.ringFlash || 0) - dt * 2.6);"""
GHOST_NEW = """    for (const f of [this.a, this.b, ...this.shades]){
      if (f.hpGhost == null) f.hpGhost = f.hp;
      f.ringFlash = Math.max(0, (f.ringFlash || 0) - dt * 2.6);
      f.drained   = Math.max(0, (f.drained   || 0) - dt * 0.62);"""

# (c) THE DRAIN TICKS ON THE PRESENTATION CLOCK, ABOVE THE HEALTH GHOST.
#
#     `tickPresentation` runs on every path INCLUDING hit stop — and every
#     lifesteal heal is caused by a hit, which begins with a hit stop. Tick it
#     on the normal path only and the stream would freeze for exactly the
#     frames the viewer is staring hardest at, which is the note already
#     written above this method about status tags and the ultimate clock.
#
#     IT SITS ABOVE THE HEALTH-GHOST LOOP AND THAT POSITION IS LOAD-BEARING.
#     `liquid_build.py` does this:
#
#         replace_span(s, "      if (f.hp >= f.hpGhost) f.hpGhost = f.hp;",
#                         "  }\n\n  decayImpactOnly(dt){", SLOSH_HOOK + ...)
#
#     — it replaces the ENTIRE TAIL of `tickPresentation`, from the health
#     ghost to the end of the method, with its own slosh hook. Anything a
#     relic builder inserted in that span is silently discarded, with no
#     failure and no warning: the relic build was correct, the build of record
#     was not, and the effect never rendered in the file anyone watched.
#
#     Anchored on the status-tag loop instead, which is above the span.
#     chain_audit.py is what stops this recurring for the next relic.
DRAINTICK_OLD = """      if (this.tags[i].life <= 0) this.tags.splice(i, 1);
    }"""
DRAINTICK_NEW = """      if (this.tags[i].life <= 0) this.tags.splice(i, 1);
    }
    for (let i = this.drains.length - 1; i >= 0; i--){
      const d = this.drains[i];
      d.t += dt;
      if (d.t >= d.delay + d.life) this.drains.splice(i, 1);
    }"""

# ================================================================== sfx =====
#
# Rick: "how about a new sound effect for the split? ive heard that same sound
# effect reused for several ults now."
#
# He is right, and it is worse than he thinks: an ultimate with no branch of its
# own falls through to the `else` at the end of the chain — the generic
# rune-crack — and that is what FOUR of the nineteen relics play.
#
# Keyed on the relic ID rather than on a name of its own, because `fireUlt`
# already fires `SFX.play("ult", { w: f.w.id })` above the kind dispatch; a
# second call in the split branch would play two sounds over each other.
SFX_ANCHOR = ('        } else if (w === "gravemourn"){                 '
              '// a drop into the grave')
SFX_NEW = '''        } else if (w === "twinshade"){                  // one becomes three
          /* THE ONLY ULTIMATE IN THE GAME WITH A WHOLE SECOND OF FROZEN HALL
             TO FILL, so it is the only one that can afford a sound in three
             movements — and it is built to the picture rather than under it:

               swell   0.00-0.45   the shell straining, pitch climbing
               pinch   0.44-0.62   the neck closing. Wet, and it FALLS, because
                                   a rising pinch reads as something opening
               chord   0.62-1.30   one voice arriving as three

             The chord is the whole ultimate stated in the one thing the ear
             does better than the eye. Three triangles a few cents apart beat
             against each other, which is what makes them read as COPIES rather
             than as a chord — an interval would be harmony, a detune is
             duplication. */
          this._tone (t,        { freq: 58,  to: 156, gain: 0.34, dur: 0.60, type:"sine" });
          this._burst(t,        { freq: 360, q: 0.7,  gain: 0.20, dur: 0.58, type:"lowpass" });
          this._burst(t + 0.44, { freq: 1900, q: 3.4, gain: 0.22, dur: 0.16, type:"bandpass" });
          this._tone (t + 0.46, { freq: 900, to: 210, gain: 0.15, dur: 0.20, type:"triangle" });
          [0, 0.028, 0.056].forEach((d, i) => {
            const det = 1 + i * 0.0075;
            this._tone(t + 0.62 + d, { freq: 196 * det, to: 392 * det,
                                       gain: 0.17, dur: 0.68, type:"triangle" });
          });
          this._burst(t + 0.62, { freq: 5200, q: 0.9, gain: 0.13, dur: 0.30, type:"highpass" });
        } else if (w === "twinshade-rejoin"){           // and three become one
          /* The reverse, and audibly so: the chord arrives FIRST and collapses
             into a single voice, the pitch falls where the split's rose, and
             there is no pinch because nothing is being torn — the last event
             is a soft landing rather than a snap. */
          [0, 0.024, 0.048].forEach((d, i) => {
            const det = 1 + i * 0.0075;
            this._tone(t + d, { freq: 330 * det, to: 196, gain: 0.13, dur: 0.42, type:"triangle" });
          });
          this._tone (t + 0.30, { freq: 150, to: 66, gain: 0.26, dur: 0.44, type:"sine" });
          this._burst(t + 0.30, { freq: 520, q: 0.6, gain: 0.16, dur: 0.40, type:"lowpass" });
          this._burst(t + 0.34, { freq: 3200, q: 1.1, gain: 0.07, dur: 0.22, type:"highpass" });
'''

# ============================================== the director: the crowd =====
#
# Rick: "the director currently seems to go off the majority of the time
# triplicate is active. probably because it does lead to big exchanges like its
# supposed to look for. but its too much and a little distracting. can we build
# an exception for it? it can still trigger during a big exchange but it needs
# to know to only look for big exchanges compared to the average triplicate."
#
# MEASURED BEFORE ANY CODE WAS WRITTEN, 50 matches over five foes:
#
#     28% of the fight is inside a Triplicate window
#     64% of every cut lands there
#     4.78 cuts a minute inside against 1.04 outside -> 4.59x
#
# THE FIRST FIX WAS WRONG AND THE MEASUREMENT SAID SO. The obvious reading of
# "big exchanges compared to the average triplicate" is a SCORE bar: hold
# crowded beats to a percentile of their own window. Built, and it moved the
# rate by nothing at all — 4.59x to the digit, twice, which is louder than a
# change that moves the wrong thing. Asked why:
#
#     crowded  n=673  mean 0.45  p95 1.56  >= floor 2.2%
#     ordinary n=637  mean 0.48  p95 1.59  >= floor 2.2%
#
# THE CROWD DOES NOT SCORE HIGHER. The distributions are the same to two
# decimal places and the qualifying rate is identical. There are simply 2.7x
# as many beats per second. No level can thin a population that differs only
# in rate — any bar that halves the crowd halves ordinary play with it.
#
# So where do the cuts come from? Not hits: only 0.3 single hits a fight clear
# the bar. They come from `cineVolleys`, which groups consecutive contacts —
# and with 2.7x the density a run of three forms constantly:
#
#     volleys inside   91, median 5 blows, sizes 3:22 4:20 5:11 ... 15:2
#     volleys outside  37, median 3 blows, sizes 3:21 4:13 5:1 6:2
#
# Outside, an exchange IS three blows — that is what the minimum was tuned to
# mean. Inside, three blows is a lull. So the exception is not a score at all,
# it is the definition of "exchange": inside a crowded window it takes more
# contacts to be one. Which is Rick's sentence, mechanically.
CROWD_BEAT_OLD = """  beat(o){
    o.t = this.t;
    this.beats.push(o);"""
CROWD_BEAT_NEW = """  beat(o){
    o.t = this.t;
    /* CROWDED — more bodies on the floor than the two this director was tuned
       for. Tagged on EVERY beat rather than at each call site, so a kind added
       later cannot forget to carry it. False in every match without a summon
       in it, which until this relic was all of them. */
    o.crowd = this.shades.length > 0;
    this.beats.push(o);"""

CROWD_CFG_OLD = "  bindsQualify: false,"
CROWD_CFG_NEW = """  bindsQualify: false,
  /* THE CROWD EXCEPTION — how many contacts make an EXCHANGE when there are
     more than two bodies on the floor.

     `volleyMin` is 3 because outside a summon that is what a traded run looks
     like: measured, 21 of 37 volleys in ordinary play are exactly 3 and 34 of
     37 are 3 or 4. Inside a Triplicate window the median run is 5 and they
     reach 15 — three blows there is a lull, and filming it promises an
     exchange the viewer is not seeing.

     A SCORE BAR WAS TRIED FIRST AND MEASURED NOTHING: crowded beats score
     identically to ordinary ones (mean 0.45 vs 0.48, qualifying 2.2% vs 2.2%)
     and are merely 2.7x more frequent. A population that differs only in rate
     cannot be thinned by a level.

     SWEPT, 50 matches, on the number the exception can actually move — the
     kill is exempt by design and 18 of the in-window cuts are kills, because
     this ultimate is often what finishes the fight:

         crowdVolleyMin   3(off)    6      7      8      9
         preference        3.07x  2.43x  2.01x  1.69x  1.59x

     8 taken. The in-window median run is 5, so 8 is genuinely "big for a
     Triplicate" rather than a tax on all of them; 9 buys 0.10x for a
     noticeably quieter window, which is the wrong trade against "it can still
     trigger during a big exchange".

     1.69x is not 1.00x and should not be: the ultimate does put more real
     spectacle on the floor. What it no longer does is out-bid the rest of the
     fight three to one.

     Set equal to volleyMin to disable. */
  crowdVolleyMin: 8,"""

CROWD_SIG_OLD = "function cineVolleys(scored, gap, min){"
CROWD_SIG_NEW = "function cineVolleys(scored, gap, min, crowdMin){"

CROWD_FLUSH_OLD = "    if (run.length >= min){"
CROWD_FLUSH_NEW = """    /* A run that happened with extra bodies on the floor has to be LONGER to
       count as an exchange. Judged on the run, not on the match: a fight that
       contains a summon is ordinary either side of the window and is scored
       that way. */
    const need = (crowdMin && run.some(b => b.crowd)) ? crowdMin : min;
    if (run.length >= need){"""

CROWD_CALL_OLD = "cineVolleys(scored, CINE.volleyGap, CINE.volleyMin)"
CROWD_CALL_NEW = ("cineVolleys(scored, CINE.volleyGap, CINE.volleyMin,\n"
                  "                              CINE.crowdVolleyMin)")

CROWD_VOLLEY_OLD = '''          kind: "volley", t: run[0].t, x: run[0].x, y: run[0].y,'''
CROWD_VOLLEY_NEW = """          kind: "volley", t: run[0].t, x: run[0].x, y: run[0].y,
          crowd: run.some(b => b.crowd),"""

# ================================================================= edit ======
def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly once, or refuse.

    A build that silently applied zero or two of its patches and then reported
    a hash is the failure mode this whole file is arranged around. Every edit
    goes through here.
    """
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor — find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def preflight():
    if (HERE / PROTECTED).exists():
        raise SystemExit(
            f"{PROTECTED} is in the tools directory. 01-live is never a build "
            f"target; move it out before running this.")


def build(src_path: pathlib.Path, out_path: pathlib.Path, blade: float) -> str:
    if out_path.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    s = src_path.read_text()
    before = len(s)

    relic = (RELIC
             .replace("%NAME%", RELIC_NAME).replace("%ULT%", ULT_NAME)
             .replace("%DMG%", f"{blade}")
             .replace("%CHARGE%", f"{ULT_CHARGE:g}")
             .replace("%DUR%", f"{ULT_DUR:g}")
             .replace("%SHADES%", f"{ULT_SHADES}")
             .replace("%HP%", f"{ULT_HP:g}")
             .replace("%LS%", f"{ULT_LIFESTEAL:g}")
             .replace("%ARRIVE%", f"{ULT_ARRIVE:g}")
             .replace("%SPREAD%", f"{ULT_SPREAD:g}")
             .replace("%HOLD%", f"{ULT_HOLD:g}")
             .replace("%REJOIN%", f"{ULT_REJOIN:g}")
             .replace("%RIBBON%", f"{ULT_RIBBON:g}")
             .replace("%ARC%", f"{ULT_ARC:g}")
             .replace("%TIP%", ULT_TIP).replace("%BLURB%", BLURB))

    print("\n  --- data ---")
    s = one(s, RELIC_ANCHOR, RELIC_ANCHOR + "\n" + relic, "relic")

    print("  --- state ---")
    s = one(s, FSTATE_OLD, FSTATE_NEW, "Fighter state")
    s = one(s, MSTATE_OLD, MSTATE_NEW, "Match.shades")

    print("  --- identities (each is a no-op at rest) ---")
    s = one(s, LS_OLD,   LS_NEW,   "lifesteal is timed")
    s = one(s, COOL_OLD, COOL_NEW, "tickHits(cool)")
    s = one(s, COOL2_OLD, COOL2_NEW, "tickHits cooldown")
    s = one(s, BEAT_OLD, BEAT_NEW, "beat side")
    s = one(s, KF_OLD,   KF_NEW,   "a shade is not a kill target")

    print("  --- the hot path ---")
    s = one(s, STEP_OLD,  STEP_NEW,  "step")
    s = one(s, BALL_OLD,  BALL_NEW,  "ballCollision -> _ballPair")
    s = one(s, CLANK_OLD, CLANK_NEW, "tickClank -> _clankPair")

    print("  --- the ultimate ---")
    s = one(s, TICKTOP_OLD,  TICKTOP_NEW,  "split clock, above the guard")
    s = one(s, TICKBODY_OLD, TICKBODY_NEW, "split clock")
    s = one(s, HOLD_OLD, HOLD_NEW, "the hall stops")
    s = one(s, FIRE_ANCHOR,  FIRE_NEW + FIRE_ANCHOR, "fireUlt: split")
    s = one(s, SHADE_ANCHOR, SHADE + SHADE_ANCHOR, "the shade methods")

    print("  --- the two gaps found by tracing ---")
    s = one(s, DECAY_OLD, DECAY_NEW, "shades do not outlive the match")
    s = one(s, GHOST_OLD, GHOST_NEW, "shade health ghost")
    s = one(s, DRAINTICK_OLD, DRAINTICK_NEW, "drain tick")

    print("  --- the director ---")
    s = one(s, CROWD_BEAT_OLD,   CROWD_BEAT_NEW,   "beats carry `crowd`")
    s = one(s, CROWD_CFG_OLD,    CROWD_CFG_NEW,    "CINE.crowdVolleyMin")
    s = one(s, CROWD_VOLLEY_OLD, CROWD_VOLLEY_NEW, "volleys inherit it")
    s = one(s, CROWD_SIG_OLD,    CROWD_SIG_NEW,    "cineVolleys takes crowdMin")
    s = one(s, CROWD_FLUSH_OLD,  CROWD_FLUSH_NEW,  "an exchange is longer in a crowd")
    s = one(s, CROWD_CALL_OLD,   CROWD_CALL_NEW,   "cinePlan passes it")

    print("  --- sfx ---")
    s = one(s, SFX_ANCHOR, SFX_NEW + SFX_ANCHOR, "twinshade has its own sound")

    print("  --- art ---")
    s = one(s, DRAW_OLD,  DRAW_NEW,  "draw order")
    s = one(s, ART_ANCHOR, ART + ART_ANCHOR, "drawShades + drawShadeFire")
    s = one(s, SNAP_OLD,  SNAP_NEW,  "CINE.snap")
    s = one(s, LERP_OLD,  LERP_NEW,  "CINE.drawLerped")

    out_path.write_text(s)
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"\n  -> {out_path.name}  {h}  ({len(s):,} chars, "
          f"{len(s)-before:+,})")
    print(f"     blade {blade}  ·  charge {ULT_CHARGE:g}s  ·  {ULT_SHADES} shades "
          f"at {ULT_HP:g}x hp for {ULT_DUR:g}s  ·  lifesteal {ULT_LIFESTEAL:g}")
    print(f"     NAMES ARE PLACEHOLDERS: relic {RELIC_NAME!r}, ult {ULT_NAME!r}")
    return h


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="../02-chain/sc-health18.html")
    ap.add_argument("--out", default="../02-chain/sc-twinshade.html")
    ap.add_argument("--blade", type=float, default=TUNED_TS,
                    help="the tuned knob. MUST be swept, never derived — see "
                         "the note on TUNED_TS.")
    A = ap.parse_args()
    preflight()
    src = (HERE / A.src).resolve()
    out = (HERE / A.out).resolve()
    if not src.exists():
        raise SystemExit(f"no such source: {src}")
    print(f"src   {src.name}  "
          f"{hashlib.sha256(src.read_bytes()).hexdigest()[:16]}")
    build(src, out, A.blade)
    return 0


if __name__ == "__main__":
    sys.exit(main())
