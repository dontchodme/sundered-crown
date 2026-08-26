#!/usr/bin/env python3
"""LASTLIGHT — the sanctified scythe, and THE HARROWING. Eighteenth relic.

    python3 lastlight_build.py --src sc-cardspin.html --out sc-lastlight.html

Rick's interview, 2026-08-17. The cell first:

    "lets start on our next fighter. im thinking the white scythe."

Sanctified is the only white school in the game (`steel:#FFFFFF`,
`glow:#FFFFFF`), so the white scythe is the SANCTIFIED SCYTHE — one of the
free cells the seed has been carrying since v22, and the cheapest of them:
`SHAPES.scythe` already dispatches `p.key === "sanctified"` to `_scRadiant`,
a halo arc standing off the back of the crescent, drawn and approved with no
relic wearing it. `whitescythe_probe.py` confirmed the branch fires and the
cell fights before a line of this was written.

Then the ultimate, in Rick's words:

    "when white scythes ult goes off it begins spraying mini scythes out in
     every direction as projectiles. when those projectiles hit an enemy they
     latch on, weighing it down and impeding its movement a bit. then after a
     duration the mini scythes explode dealing damage and leaving behind
     sparks (same sparks as dawnbringer)"

    "mini scythes should rotate around in a circle to give them a better
     visual sense of movement"

    "lets make sure mini scythes deal damage when they land and when they
     explode. a double payoff"

    "lets also make sure the explosion causes some big hitstun and knockback.
     probably scale it with the amount of projectiles that latched. lots of
     latches should have a big impact"

And three answers to the design interview:

    miss case   "bounce twice then expire"
    the fuse    ONE bloom, everything at once, not a rolling crackle
    name        Lastlight

WHY THIS CELL IS WORTH BUILDING, AND IT IS NOT THE ART
------------------------------------------------------
**Nothing in this game spends Smite, and Smite has no mechanical identity.**
In `STATUS` it is byte-identical to Hemorrhage — `maxStacks:4, dur:3.2,
dps:1.5`, the same three numbers — and all four sanctified surfaces
(Dawnbringer, Aureole, Censer on hit, Consecration on cast) are appliers.
The school is four taps and no drain.

Dwarven is the counter-example that works, and it is why that column reads as
a school rather than as a colour: Slagheart BUILDS Sunder two at a time, the
Crucible SPENDS it, and Slagburst detonates it. Sanctified has no equivalent
and Lastlight does not become one either — the Harrowing spends BLADES, not
Smite. That is deliberate and it is the honest limitation of this build: it
gives sanctified a second verb, not the missing one. The Smite spender is
still owed, and the note is here so nobody reads this relic as having paid
that debt.

WHAT IS FIXED BY THE TYPE, AND WHAT IS NOT
------------------------------------------
Every physics number is Thornwake's, exactly — `reach 104, width 11, artW 46,
spin 3.2, mode "spin", mass 2.4`. Weapon-matrix decision 1: the TYPE owns the
physics and the school owns status and palette. A new scythe that moved reach
or mass would not be a new school cell, it would be a new type wearing a
scythe's name, and the 3x3 block established that the type axis has to be held
rigid or the grid measures the wrong thing.

`dmg` is a PLACEHOLDER at Thornwake's 31.35 and it will be wrong. It is not an
estimate: the Harrowing is a large, unmeasured damage add on top of a blade
that was tuned under a freeze-and-root ultimate, so the correct blade cannot
be derived, only measured. `--blade` is the knob; `harrow_probe.py` and
`verify.py` are what move it.

THE DOUBLE PAYOFF, AND WHERE EACH HALF IS PRICED
------------------------------------------------
Rick asked for damage on landing AND on the burst, and the two are paid in two
different places on purpose:

  the landing   `resolveHit`, exactly like any other projectile — crit, damage
                jitter, the Sunder multiplier, hit stop, diminishing-returns
                hitstun, `self.hits++` for verify.py's six-hit floor, and the
                relic's own `onHit: {smite:1}`. A landing scythe is a HIT in
                every sense the rest of the game already understands.
  the burst     `harrow()`, once, on the caster's fuse. This is the half that
                SCALES: damage, knock, stun, hit stop, shake and the number of
                sparks left behind are all functions of `n`.

Nothing about the landing scales and nothing about the burst is per-scythe
random. So "that one was big" and "six of them stuck" are the same sentence.

THE BURDEN IS PHYSICS, NOT A STATUS, AND THAT IS A RULE NOT A PREFERENCE
------------------------------------------------------------------------
"Weighing it down and impeding its movement" is Entangle's effect, and
Entangle belongs to verdant. `roster-expansion.md` §5.8: *a relic that wants a
status its school does not have is either in the wrong school or the taxonomy
is wrong.* Lastlight is sanctified, so the burden is carried as what it
actually is — mass and drag on the ball:

    moveMul()   -burdenMove per stuck scythe, under the existing 0.45 floor
    move()      the fall term reads `w.mass + burden * burdenMass`

It is also strictly better than a status would have been: it is COUNTABLE on
screen (the blades are drawn where they went in), it stacks past any
`maxStacks`, and it cannot be cleansed by anything that clears statuses.

**`tickClank` is deliberately NOT touched.** Clank share is `mass^1.7` read
off `w.mass`, and a ball with scythes stuck in it should fall harder — not
start winning binds it was losing a second ago. Making the burden count for
clank would hand the QUARRY a buff for being hit.

BIT-IDENTITY, AND WHY THE TWO PHYSICS EDITS ARE SAFE
-----------------------------------------------------
Both edits are exact arithmetic identities when `burden` is 0, which it is on
every fighter in every match that does not contain Lastlight:

    (1 + e) - 0 * 0   ===   1 + e          IEEE754 exact
    mass + 0 * 0      ===   mass           IEEE754 exact

That is what lets `engine_ab.py` prove the relic inert across the other
seventeen ids. If either edit ever stops being an identity at zero, engine_ab
is the check that says so — it is not decoration on this build, it is the
whole argument that eighteen relics did not silently re-tune seventeen.

THE DUD, MEASURED RATHER THAN DESIGNED AROUND
---------------------------------------------
A radial spray in a 520x800 hall will often stick nothing, and Slagburst's
lesson is that a payoff which fizzles one cast in four is a coin flip with a
set-piece attached. Slagburst's fix was to manufacture its own fuel. This one
does NOT do that, because the spray is the spectacle and guaranteeing a latch
would mean homing — and there is no steering, no homing and no correction in
flight anywhere in this engine, by design.

So the dud is kept, made VISIBLE (`phase:"cold"`, its own sound, its own log
line), and the rate is MEASURED by `harrow_probe.py` rather than assumed. If
it comes back high, the knobs are `scythes`, `life`, `bounce` and `speed` — all
of them things the viewer can see — and not a hidden floor.

massRef
-------
Unchanged at 2.680, deliberately. `mean(sqrt(mass))^2` over eighteen relics is
2.6645, so the roster falls 0.29% slow against neutral — inside the noise of
anything this project can measure, and re-deriving it would re-tune all
seventeen existing relics and destroy the bit-identity proof above. Stated
here so it is a decision on the record rather than an oversight. Re-derive it
in a tuner run, with `slagheart_build.py --massref`, never in this build.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# --------------------------------------------------------------- tuning ----
# A GENERATED FILE IS NOT A PLACE TO STORE A NUMBER. Every knob the Harrowing
# has is here, and the HTML is an artifact of this table.

# TUNED, not guessed, and the placeholder it replaces is on the record.
# Thornwake's 31.35 put Lastlight at 71.0% in `verify.py --n 60` — 21pp clear
# of a field whose standard error is 1.7pp, so the direction was unambiguous
# even from the tool the seed warns cannot rank a flat field. `lastlight_sweep.py`
# narrowed it against all seventeen foes on pinned seeds:
#
#     31.35  71.5%      24.00  64.0%      19.00  53.4%
#     17.50  49.3%      16.00  48.0%      14.50  42.5%
#
# 17.5 is the LOWEST blade in the game by a distance (Axiom is 7.42 but swings
# a greatsword arc; this spins at 3.2 with reach 104). That is the honest price
# of an ultimate that fires every 15s and pays twice — the sweep shows Lastlight
# casting ~28 Harrowings per 26-match column, and the blade is what funds them.
TUNED_LL = 17.5

DATA = dict(
    charge=15,            # Thornwake's, and the sanctified median

    # --- the throw ---
    scythes=12,           # blades per cast, evenly spaced off the weapon's facing
    speed=430,            # px/s, jittered +-14% deterministically per index
    r=14,                 # projectile radius; hit test is ballR + r
    life=2.2,             # SHORTER than the fuse on purpose — see FUSE below
    bounce=2,             # Rick: "bounce twice then expire"
    arm=0.10,             # cannot bite until it has left the shell
    spinRate=15.0,        # rad/s of visible turn in flight (presentation only)

    # --- the fuse ---
    # 2.4 > life 2.2, so NOTHING of a cast is still in the air when the bloom
    # comes. That is what makes "all at once" a complete statement rather than
    # a race: every blade has either stuck or expired by the time the clock
    # runs out, and there is no third case to reason about.
    fuse=2.4,

    # --- the landing (does not scale) ---
    landDmg=4.5,          # priced through resolveHit as landDmg / w.dmg

    # --- the burst (scales on n, the count that stuck) ---
    dmgBase=5.0,
    dmgPer=8.0,           # 1 blade 13 · 3 blades 29 · 6 blades 53
    knockBase=120.0,
    knockPer=130.0,       # 1 -> 250 · 3 -> 510 · 6 -> 900
    stunBase=0.10,
    stunPer=0.075,        # a FLOOR under the ordinary DR hitstun, not a replacement
    stopBase=0.05,
    stopPer=0.014,        # whole-sim freeze: 1 -> 0.064s · 6 -> 0.134s

    # --- the burden, per stuck scythe ---
    burdenMove=0.05,      # -5% move each, under moveMul's existing 0.45 floor
    burdenMass=0.45,      # added to the FALL mass only. Never to clank.

    # --- the light left behind: Daybreak's own numbers, so spawnSpark and
    #     tickSparks behave identically for both relics ---
    sparksPer=2,
    sparkDmg=5,
    sparkKnock=260,
    sparkLife=8.0,
    sparkGrace=0.7,
)

ULT_NAME = "Harrowing"
# <= 72 (verify.py enforces). A harrow is the implement that goes through
# ground scattering blades; the Harrowing is the descent that breaks something
# open and lets the light out. Both halves of the mechanic in one word.
ULT_TIP = "Sprays scythes that stick and bite, then burst — 8 each, plus sparks"

BLURB = ("A reaping tool that throws its own blades. What sticks, waits — "
         "and what it leaves behind is light.")

# ------------------------------------------------------------ relic data ----

RELIC = ('''
  /* LASTLIGHT — the sanctified scythe, and the first relic in the game whose
     ultimate is a FIELD OF OBJECTS rather than an event. Physics are
     Thornwake's exactly (the type owns them); the school owns Smite and the
     white. `dmg` is a placeholder — lastlight_build.TUNED_LL. */
  {{ id:"lastlight", name:"Lastlight", aff:"sanctified", shape:"scythe",
    blades:[0], reach:104, width:11, artW:46, dmg:{blade}, spin:3.2, mode:"spin", mass:2.4,
    onHit:{{ smite:1 }},
    ult:{{ name:"{name}", charge:{charge}, kind:"harrow",
          scythes:{scythes}, speed:{speed}, r:{r}, life:{life}, bounce:{bounce},
          arm:{arm}, spinRate:{spinRate}, fuse:{fuse}, landDmg:{landDmg},
          dmgBase:{dmgBase}, dmgPer:{dmgPer},
          knockBase:{knockBase}, knockPer:{knockPer},
          stunBase:{stunBase}, stunPer:{stunPer},
          stopBase:{stopBase}, stopPer:{stopPer},
          burdenMove:{burdenMove}, burdenMass:{burdenMass},
          sparksPer:{sparksPer}, sparkDmg:{sparkDmg}, sparkKnock:{sparkKnock},
          sparkLife:{sparkLife}, sparkGrace:{sparkGrace},
          tip:"{tip}" }},
    blurb:"{blurb}" }},''')

RELIC_ANCHOR = ('blurb:"Longest true reach. Roots its quarry until the swing '
                'can barely come around." },')

# ------------------------------------------------------ engine: state ----

STATE_OLD = ('    this.ultSlag = null;      // {t, fuse, split} while a '
             'Slagburst fuse burns')
STATE_NEW = STATE_OLD + """
    this.ultHarrow = null;    // {t, fuse} while the Harrowing's blades count down
    /* THE BURDEN — what is stuck in THIS ball and what it costs. Zero on every
       fighter in every match that does not contain Lastlight, and BOTH sites
       that read it are exact identities at zero: `(1+e) - 0*0` in moveMul and
       `mass + 0*0` in move(). That is the whole argument that an eighteenth
       relic did not re-tune the other seventeen, and engine_ab.py is what
       proves it rather than this comment. */
    this.stuck = [];          // [{ang, own, tilt, r}] blades buried in the shell
    this.burden = 0;          // how many
    this.burdenMove = 0;      // move penalty per blade, copied from the caster
    this.burdenMass = 0;      // added FALL mass per blade. Never clank mass.
    this.burdenK = 0;         // presentation only: the caster's fuse, 0..1"""

MOVEMUL_OLD = ('  moveMul(){ return Math.max(0.45, 1 + STATUS.entangle.move * '
               'this.stacks("entangle")); }')
MOVEMUL_NEW = """  /* THE BURDEN IS SUBTRACTED HERE RATHER THAN ROUTED THROUGH A STATUS.
     "Weighing it down and impeding its movement" is Entangle's effect, and
     Entangle belongs to VERDANT — a relic that wants a status its school does
     not have is either in the wrong school or the taxonomy is wrong
     (roster-expansion §5.8). Lastlight is sanctified, so what it does is nail
     four inches of blade into you, and that is mass and drag, not a spell.

     Strictly better than a status would have been, for three reasons that are
     not aesthetic: it is COUNTABLE on screen (the blades are drawn where they
     went in), it stacks past any maxStacks, and nothing that clears statuses
     can clear it. Same 0.45 floor as before, so the two cannot combine into a
     ball that has stopped. */
  moveMul(){
    return Math.max(0.45, 1 + STATUS.entangle.move * this.stacks("entangle")
                            - this.burden * this.burdenMove);
  }"""

GRAV_OLD = ('    f.vy += P.gravity * Math.pow(f.w.mass / P.massRef, '
            'P.massWeight) * dt;')
GRAV_NEW = """    /* The blades ride along. EFFECTIVE mass, and only here: `tickClank`
       reads `w.mass` directly and is deliberately left alone. A ball with
       scythes stuck in it should fall harder — it should not start winning
       binds it was losing a second ago, which is what counting the burden for
       clank share would hand the QUARRY as a reward for being hit. */
    f.vy += P.gravity * Math.pow((f.w.mass + f.burden * f.burdenMass)
                                 / P.massRef, P.massWeight) * dt;"""

# ------------------------------------------------------ engine: the fuse ----

TICKTOP_OLD = """  tickCharge(f, foe, dt){
    if (!f.alive || this.over) return;"""
TICKTOP_NEW = """  tickCharge(f, foe, dt){
    /* THE FUSE HAS TO BE CLEANED UP ABOVE THE GUARD, NOT BELOW IT.
       Everything else in this method needs a live wielder, so the early
       return is right for all of it — but a Harrowing fuse must be dropped
       EXACTLY when a fighter is not alive, and there is a window where that
       matters: a fatal blow arms `killFlight` and `checkEnd` deliberately
       holds the match open while the loser flies into the wall. During those
       frames `over` is still false and `move()` is still running. Put the
       drop below the guard and the winner spends its entire victory flight
       burdened by blades nobody is going to detonate.

       harrow_probe.py [10] is what forced this up here; the first version sat
       under the guard and could not be reached by the case it claimed to
       handle. */
    if (f.ultHarrow && (!f.alive || !foe.alive || this.over)){
      f.ultHarrow = null;
      this.unstick(foe);
    }
    if (!f.alive || this.over) return;"""

TICK_ANCHOR = """    if (f.ultHeat){
      /* The head is lit and the window is burning."""
TICK_NEW = """    if (f.ultHarrow){
      /* THE FUSE. Everything that stuck is counting down TOGETHER — Rick
         chose one bloom over a rolling crackle, so there is exactly one clock
         and it lives on the CASTER, not on the blades. Per-blade fuses would
         have given the director no single peak to cut on, which is the one
         thing `cineScore` has never managed to film on an ultimate.

         The drop-on-death cases are handled at the top of this method, above
         the guard that would otherwise hide them. What is left here is the
         clock and the payoff.

         `life` (2.2) is under `fuse` (2.4) by construction, so nothing of
         this cast is still in the air when the clock runs out. Every blade
         has either stuck or expired, and there is no third case — which is
         what makes "all at once" a complete statement rather than a race. */
      const S = f.ultHarrow;
      S.t += dt;
      foe.burdenK = clamp(S.t / S.fuse, 0, 1);   // presentation: the tell
      if (S.t >= S.fuse){
        f.ultHarrow = null;
        this.harrow(f, foe);
      }
    }
""" + TICK_ANCHOR

# ----------------------------------------------------- engine: fireUlt ----

FIRE_ANCHOR = '    if (u.kind === "detonate"){'
FIRE_NEW = '''    /* THE HARROWING RESOLVES NOTHING HERE. It throws.

       Every piece of this ultimate is an object this engine already had. The
       blades are `shots` — clankable, bouncing, missable, drawn by the same
       loop. The burden is the fall term and moveMul. The fuse is Slagburst's.
       The sparks are DAYBREAK'S OWN: `spawnSpark` reads `sparkGrace` and
       `sparkLife` off `f.w.ult`, so what this leaves behind is the same field
       Dawnbringer leaves, and a fix to one is a fix to both. Nothing here is
       a second implementation of anything.

       The angles come off `f.theta` — the weapon's own facing — with
       deterministic jitter from `shellHash`, NOT from `this.rng()`. Same rule
       Ironbloom's splinters follow: a relic that is not in the match must not
       be able to perturb the draw order of one that is. */
    if (u.kind === "harrow"){
      const R = CONFIG.physics.ballR;
      const N = u.scythes || 12;
      for (let i = 0; i < N; i++){
        const a = f.theta + (i / N) * TAU + (shellHash(7717, i) - 0.5) * 0.28;
        const spd = u.speed * (0.86 + shellHash(7723, i) * 0.28);
        if (this.shots.length >= CONFIG.shot.maxLive) this.shots.shift();
        this.shots.push({
          own: f === this.a ? "a" : "b",
          /* Clear of the shell AND armed. The trap the splinters hit and
             wrote down: a projectile spawned inside `R + s.r` resolves on the
             frame it is born, which would turn the spray into a nova. */
          x: f.x + Math.cos(a) * (R + (u.r || 14) + 10),
          y: f.y + Math.sin(a) * (R + (u.r || 14) + 10),
          arm: u.arm || 0.10,
          x0: f.x, y0: f.y, spd0: f.speed, t0: this.t,        // CINEMA (demo)
          vx: Math.cos(a) * spd, vy: Math.sin(a) * spd,
          r: u.r || 14, life: u.life || 2.2, max: u.life || 2.2, grav: 0,
          /* The landing, priced as a multiplier so it flows through
             resolveHit exactly like every other hit on this relic — one
             damage number, sized by the existing rule. */
          dmgMul: (u.landDmg || 4.5) / Math.max(0.01, f.w.dmg),
          bounce: u.bounce === undefined ? 2 : u.bounce,
          sc: true, spin: (i % 2 ? 1 : -1) * (u.spinRate || 15),
          aff: f.aff, a,
        });
      }
      f.ultHarrow = { t: 0, fuse: u.fuse };
      this.ultFx.phase = "cast";
      this.ultFx.n = N;
      /* THE FX CLOCK RUNS AT ~2x SIM TIME on the normal path — every `life`
         in this engine is in half-seconds. The cast's tell has to still be on
         screen when the fuse blows, so 2x the fuse plus margin. */
      this.ultFx.life = u.fuse * 2 + 0.5;
      /* No banner. The name goes on the BLOOM, where the thing happens — the
         aimed shot, the Crucible and Ironbloom all place it the same way. You
         do not caption a promise. */
      this.banner = null;
      SFX.play("ult", { w: "lastlight-throw" });
      return;
    }

''' + FIRE_ANCHOR

# ------------------------------------------------- engine: latch + bloom ----

# ORDER IS THE WHOLE CHECK HERE, and the first build got it wrong. The latch
# must be tested BEFORE the ordinary hit branch, not before the wall branch:
# `tickShots` runs parry -> hit -> wall -> pop -> spent, each guarded by
# `!dead`, so a latch inserted after the hit branch never fires — the ordinary
# branch resolves the blade and deletes it, and the ultimate silently becomes
# twelve small arrows. It looked fine, it drew fine, and harrow_probe.py [4]
# caught it: 72 casts, 0 blades stuck, 100% duds.
LATCH_ANCHOR = ("      /* --- the hit. Routed through resolveHit so a shot is "
                "a hit in every")
LATCH_NEW = '''      /* --- THE LATCH. A blade of the Harrowing that reaches the foe LANDS
         like any other projectile — resolveHit prices it with crit, damage
         jitter, the Sunder multiplier, hit stop, diminishing-returns hitstun
         and its own Smite — and then it STAYS, buried in the shell, until the
         caster's fuse blows. That is the first half of Rick's double payoff;
         `harrow()` pays the second, and only the second one scales.

         It is deliberately NOT exempt from the parry above. A spinning weapon
         that bats one out of the air is the counterplay, and an ultimate that
         cheated the rules its own weapon lives under would teach the viewer
         that the rules are decorative. */
      if (!dead && s.sc && foe.alive && src.alive && !(s.arm > 0)
          && Math.hypot(s.x - foe.x, s.y - foe.y) < R + s.r){
        const bl = Math.hypot(s.vx, s.vy) || 1;
        const seg = { ax: s.x - s.vx/bl*10, ay: s.y - s.vy/bl*10,
                      bx: s.x + s.vx/bl*10, by: s.y + s.vy/bl*10, a: s.a };
        this.shotHits++;
        this._cineShot = s;
        this.resolveHit(src, foe, s.x, s.y, seg, s.dmgMul, s.over);
        this._cineShot = null;
        /* Planted at the angle it ARRIVED on, measured from the shell centre,
           so where each blade sits is something the viewer watched happen
           rather than a number chosen here. resolveHit can kill — a blade
           does not stick into a corpse. */
        if (foe.alive){
          const U = src.w.ult;
          foe.stuck.push({ ang: Math.atan2(s.y - foe.y, s.x - foe.x),
                           own: s.own, tilt: s.a, r: s.r });
          /* INVARIANT: a relic cannot fight itself and there is exactly one
             harrow relic in the roster, so every entry in `stuck` has the
             same owner and the count is the length. harrow() still filters by
             owner rather than trusting that — the day a second harrow relic
             exists, this must not silently double-count. */
          foe.burden = foe.stuck.length;
          /* The per-blade weights are copied ONTO the quarry rather than
             looked up from the caster: moveMul() and move() run on a fighter
             that has no handle on who stuck what into it, and a global lookup
             would be a second source of truth for a tuned number. */
          foe.burdenMove = U.burdenMove || 0;
          foe.burdenMass = U.burdenMass || 0;
          SFX.play("ult", { w: "lastlight-stick", n: foe.burden });
        }
        dead = true;
      }

''' + LATCH_ANCHOR

HARROW_ANCHOR = "  checkEnd(){"
HARROW = '''  /* Every blade out of the shell, and every trace of what they weighed. One
     place, because the burden is four fields and a partial clear is a ball
     that stays slow for the rest of the match. */
  unstick(f){
    f.stuck = [];
    f.burden = 0; f.burdenMove = 0; f.burdenMass = 0; f.burdenK = 0;
  }

  /* ---------------------------------------------------------- THE HARROWING --
     The fuse reaches the blades. Called only from tickCharge, only with both
     fighters alive, and it is the ONLY place a harrow ult resolves.

     `n` is what actually stuck, and EVERYTHING here scales on it — damage,
     knock, the raised speed ceiling, the stun floor, the hit stop, the shake,
     and the number of sparks left behind. Rick's rule for this one was "lots
     of latches should have a big impact", and a burst that read the same at
     one blade as at six would make the entire spray decorative. */
  harrow(f, foe){
    const u = f.w.ult;
    const own = f === this.a ? "a" : "b";
    const n = foe.stuck.reduce((k, s) => k + (s.own === own ? 1 : 0), 0);
    const bx = foe.x, by = foe.y;
    this.unstick(foe);

    if (!n){
      /* THE DUD, AND IT IS VISIBLE. Nothing stuck, so nothing bursts, and the
         ultimate SAYS SO rather than playing a bloom that did not happen.
         Slagburst manufactured its own fuel to make this case impossible;
         this one cannot, because guaranteeing a latch would mean homing and
         there is no homing anywhere in this engine. So the dud is kept, made
         legible, and its RATE IS MEASURED — harrow_probe.py — instead of
         being assumed away. */
      this.ultFx = { w: f.w.id, kind: "harrow", phase: "cold",
                     src: own, tgt: own === "a" ? "b" : "a",
                     x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: false,
                     radius: 300, aff: f.aff, t: 0, n: 0, life: 1.1 };
      SFX.play("ult", { w: "lastlight-cold" });
      this.note(`${f.w.name} — nothing held`);
      return;
    }

    const raw = u.dmgBase + u.dmgPer * n;
    const dmg = Math.round(raw * this.actMods.dmg * foe.dmgTakenMul());
    this.hurt(foe, dmg, f);
    foe.flash = 1; foe.ringFlash = 1;
    f.dealt += dmg;
    const fatal = foe.hp <= 0;
    if (fatal) this.finisher = 1.0;
    this.float(bx, by - 40, dmg, "#FFF6E2", 46 + n * 3);

    /* THE IMPACT, four channels on the same n. The knock throws it; `launch`
       raises the speed ceiling so the throw can actually happen and the relax
       term pays it back over the next second and a half; the stun is a FLOOR
       under the ordinary diminishing-returns hitstun rather than a
       replacement for it (the DR exists so a fast relic cannot lock a slow
       one out of the match, and this must not become a way around it); and
       the hit stop is what makes the frame feel heavy. */
    const dx = bx - f.x, dy = by - f.y, dl = Math.hypot(dx, dy) || 1;
    const k = u.knockBase + u.knockPer * n;
    foe.vx += (dx / dl) * k; foe.vy += (dy / dl) * k;
    if (n >= 3) foe.launch = Math.max(foe.launch || 0, 1.4);
    if (!fatal){
      foe.takeHitstun(dmg);
      foe.stun = Math.max(foe.stun, u.stunBase + u.stunPer * n);
    }
    this.hitStop = Math.max(this.hitStop, u.stopBase + u.stopPer * n);
    this.shake = Math.max(this.shake, 24 + n * 4.5);

    /* THE LIGHT LEFT BEHIND. Daybreak's sparks, spawned by Daybreak's own
       function: it reads sparkGrace and sparkLife off `f.w.ult`, so these arm
       with the same pop, drift on the same deterministic phase, heal the
       owner as Blessing and burn the foe for sparkDmg exactly as
       Dawnbringer's do. Rick asked for "the same sparks as dawnbringer" and
       this is that literally, not a copy of it. */
    for (let i = 0; i < (u.sparksPer || 2) * n; i++) this.spawnSpark(f, bx, by);

    this.spawnFx(bx, by, "#FFF6E2", 26 + n * 5, 420 + n * 30, 0.75, 5);
    this.ring(bx, by, "#FFFFFF", 8, 150 + n * 22, 0.5, 8);
    this.banner = { text: u.name, life: 2.1, max: 2.1, color: f.aff.core,
                    glow: f.aff.glow, w: f.w.id, bx, by };
    this.ultFx = { w: f.w.id, kind: "harrow", phase: "bloom",
                   src: own, tgt: own === "a" ? "b" : "a",
                   x: bx, y: by, tx: bx, ty: by, hit: true,
                   radius: u.radius || 300, aff: f.aff, t: 0, n, life: 1.7 };
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: bx, y: by,
                w: f.w.id, foeHpFrac: Math.max(0, foe.hp) / foe.maxHp });
    SFX.play("ult", { w: "lastlight-bloom", n });
    this.note(`${f.w.name} — ${u.name}, ${n} blade${n > 1 ? "s" : ""}`);
  }

''' + HARROW_ANCHOR

# ---------------------------------------------------------------- art ----

MINI = '''  /* THE WHOLE SCYTHE, NOT THE HEAD. First cut drew the crescent alone and
     Rick called it immediately: "the mini scythes only show the head spinning,
     not the whole scythe." A crescent tumbling by itself is a boomerang — the
     L is what says scythe, exactly as `_scConjured`'s docstring worked out for
     the runic cell (the snath is ~60% of a scythe's footprint, and a long pole
     with a hook at the far end IS the type; delete it and what is left is a
     different weapon). That finding was about a silhouette on a contact sheet
     and it transfers here unchanged.

     PROPORTIONS ARE CARICATURED ON ONE AXIS ONLY. The pole and its bow are
     `_scBase`'s exactly — same quadratic, same control point, same collar.
     What is exaggerated is the blade's DEPTH: the real relic runs W/L 0.106,
     which puts a long shallow hook on a long pole and reads as a stick at
     forty pixels. Here W/L is 0.31, so the hook is deep enough to survive
     being thrown across the hall. Nothing else is changed, so the object in
     the air is recognisably the object in the wielder's hand.

     THE PIVOT IS THE OBJECT'S OWN CENTRE, not its grip. A scythe rotating
     about the butt of its handle orbits; one rotating about its middle
     tumbles, which is what a thrown blade does. The translate below is the
     centre of the bounding extent — x runs 0..1.02L, y runs -1.32W..0.30W.

     One shape, three call sites — in flight, buried in a shell, and thrown
     out of the bloom — so all three read as the same object. */
  _miniScythe(c, r){
    const L = 2.40 * r, W = 0.75 * r;
    c.save();
    c.translate(-1.224 * r, 0.383 * r);

    c.lineCap = "round";
    c.lineWidth = Math.max(1, r * 0.17);                    // the snath
    c.beginPath();
    c.moveTo(0, 0);
    c.quadraticCurveTo(L * 0.44, W * 0.30, L * 0.70, W * 0.16);
    c.stroke();

    c.beginPath();                                          // the collar
    c.arc(L * 0.70, W * 0.14, W * 0.17, 0, TAU);
    c.fill();

    c.beginPath();                                          // the crescent
    c.moveTo(L * 0.70, W * 0.20);
    c.bezierCurveTo(L * 1.02, -W * 0.20, L * 0.98, -W * 0.95, L * 0.56, -W * 1.32);
    c.bezierCurveTo(L * 0.88, -W * 0.72, L * 0.86, -W * 0.10, L * 0.66, W * 0.30);
    c.closePath();
    c.fill();

    /* the honed edge, one stroke, on the concave side only — the same
       asymmetry `_scBase` uses to stop the crescent reading as a sticker */
    c.lineWidth = Math.max(1, r * 0.12);
    c.beginPath();
    c.moveTo(L * 0.70, W * 0.20);
    c.bezierCurveTo(L * 1.02, -W * 0.20, L * 0.98, -W * 0.95, L * 0.56, -W * 1.32);
    c.stroke();
    c.restore();
  }

'''
MINI_ANCHOR = "  drawSparks(m){"

STUCK = '''  /* THE BLADES IN THE SHELL. Drawn over both fighters and under the sparks,
     because they are on the OUTSIDE of the ball and the light coming off them
     belongs on top of everything the ball is doing.

     THEY DO NOT TURN. A stuck blade that kept spinning would read as still
     flying, and the entire point of the latch is that it stopped. What moves
     instead is the heat: `burdenK` is the caster's fuse as 0..1, cubed, so
     almost all of the tell lands in the last third — a linear ramp reads as
     "bright" for two seconds and as no warning at all in the half second that
     matters. The shiver is on the match clock, not on rng, so a paused and
     resumed render replays identically. */
  drawStuck(m){
    const c = this.ctx, R = CONFIG.physics.ballR;
    for (const f of [m.b, m.a]){
      if (!f.stuck || !f.stuck.length) continue;
      const heat = Math.pow(clamp(f.burdenK || 0, 0, 1), 3);
      c.save();
      c.lineCap = "round"; c.lineJoin = "round";
      for (let i = 0; i < f.stuck.length; i++){
        const s = f.stuck[i];
        const jit = Math.sin(m.t * 46 + i * 2.1) * heat * 0.028;
        const a = s.ang + jit;
        /* PLANTED ON THE SHELL EDGE, NOT INSIDE IT. The first cut seated
           them at `R - 0.34r`, which is inside a 34px ball: the blades were
           behind the shell's own light and the contact sheet showed nothing
           at all until the fuse was nearly out. They straddle the rim now —
           buried to the horns, blade standing off it. */
        const px = f.x + Math.cos(a) * (R + s.r * 0.62);
        const py = f.y + Math.sin(a) * (R + s.r * 0.62);
        c.globalCompositeOperation = "lighter";
        const gr = s.r * (1.1 + heat * 2.6);
        const g = c.createRadialGradient(px, py, 1, px, py, gr);
        g.addColorStop(0, "#FFFFFF");
        g.addColorStop(0.42, "#FFF6E2" + (heat > 0.55 ? "AA" : "44"));
        g.addColorStop(1, "#FFF6E200");
        c.globalAlpha = 0.34 + 0.66 * heat; c.fillStyle = g;
        c.beginPath(); c.arc(px, py, gr, 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = 1;
        c.save();
        c.translate(px, py);
        /* BLADE IN, HAFT OUT. The shape's hook is at local +x and its grip at
           local -x, so turning it a half circle past the arrival angle drives
           the crescent into the shell and leaves the snath standing off it —
           which is what a thrown scythe that stuck in something looks like,
           and it is also the half of the object that reads at a glance. */
        c.rotate(a + Math.PI);
        c.fillStyle = "#FFFFFF";
        c.strokeStyle = "#FFF6E2";
        this._miniScythe(c, s.r * 1.05);
        c.restore();
      }
      c.restore();
    }
  }

''' + MINI_ANCHOR

ORDER_OLD = "    this.drawShots(m);\n    this.drawSparks(m);"
ORDER_NEW = "    this.drawShots(m);\n    this.drawStuck(m);\n    this.drawSparks(m);"

SHOTART_ANCHOR = "      if (s.shard){\n        const sp2 = Math.hypot(s.vx, s.vy) || 1;"
SHOTART_NEW = '''      /* A BLADE OF THE HARROWING. Not an arrow — an arrow reads by its 9:1
         aspect ratio and a crescent borrowing it would read as a second
         archer — and not a splinter either. It is the weapon itself in
         miniature, and it TURNS as it flies: Rick asked for the rotation and
         he is right, a crescent travelling on a straight line with a fixed
         angle reads as a decal sliding across the screen.

         The turn is DERIVED, not accumulated: `s.a` plus elapsed life times a
         per-blade rate. `life` is not in LERP_FIELDS.shot, so an accumulated
         angle would strobe against the interpolator; a derived one steps with
         the 120Hz sim, which is the same trick the splinter's tumble uses and
         the same reason. Alternating sign per index so the spray does not
         read as twelve copies of one object. */
      if (s.sc){
        const ang = s.a + (s.max - s.life) * (s.spin || 15);
        const dim = clamp(s.life / 0.4, 0, 1);
        /* NO MOTION STREAK. The arrow has one because an arrow is a rigid
           9:1 dart whose direction is otherwise unreadable. This object has a
           HAFT, and once the whole scythe is drawn a streak is a second stick
           coming off the same point — the zoomed contact sheet showed twelve
           blades each apparently holding a grey pole at the wrong angle. The
           tumble is the motion cue; it does not need a second one. */
        /* THE GLOW IS SMALLER THAN THE BLADE, NOT BIGGER. First cut put a
           2.3r halo at 0.85 alpha around a 1.0r crescent and the contact
           sheet showed twelve white blobs — the shape was inside its own
           bloom. The blade is the object; the glow only has to say it is
           made of light. */
        const gh = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * 1.7);
        gh.addColorStop(0, s.aff.core + "88");
        gh.addColorStop(0.5, s.aff.core + "3A");
        gh.addColorStop(1, "#FFF6E200");
        c.globalAlpha = 0.5 * dim; c.fillStyle = gh;
        c.beginPath(); c.arc(s.x, s.y, s.r * 1.7, 0, TAU); c.fill();
        c.globalAlpha = dim;
        c.save();
        c.translate(s.x, s.y); c.rotate(ang);
        c.fillStyle = "#FFFFFF";
        c.strokeStyle = "#FFF6E2"; c.lineWidth = Math.max(1, s.r * 0.15);
        this._miniScythe(c, s.r * 1.25);
        c.restore();
        c.lineCap = "butt";
        continue;
      }
''' + SHOTART_ANCHOR

UNDER_ANCHOR = ('drawUltUnder(m){\n    if (m.wallCrack) this._wallCrack(m);\n'
                '    const s = this._ult(m); if (!s) return;\n'
                '    const { u, src, tgt, k } = s, c = this.ctx, A = CONFIG.arena;\n'
                '    c.save();\n'
                '    c.lineCap = "round"; c.lineJoin = "round";')
UNDER_NEW = UNDER_ANCHOR + '''

    /* ---- THE HARROWING, under ------------------------------------------
       Deliberately SMALL. Everything a viewer needs in order to read this
       ultimate is already a simulation object — twelve turning blades, the
       ones buried in the shell brightening on the fuse, the burst's own float
       and ring, and the spark field afterwards. A set-piece competing with
       that would be light drawn on top of light. What is here is the two
       things the sim cannot say by itself: where the throw came FROM, and how
       hard the bloom hit. */
    if (u.w === "lastlight"){
      c.globalCompositeOperation = "lighter";
      if (u.phase === "cast"){
        const ex = clamp(u.t / 0.55, 0, 1);
        c.globalAlpha = (1 - ex) * 0.5;
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 7 * (1 - ex) + 1;
        c.beginPath();
        c.arc(src.x, src.y, 34 + 210 * (1 - Math.pow(1 - ex, 2.2)), 0, TAU);
        c.stroke();
      } else if (u.phase === "bloom"){
        const n = u.n || 1;
        const ex = clamp(u.t / 0.30, 0, 1);
        const fade = 1 - clamp((u.t - 0.30) / 1.20, 0, 1);
        const rad = (86 + n * 26) * (1 - Math.pow(1 - ex, 2.4));
        const g = c.createRadialGradient(u.x, u.y, 2, u.x, u.y, rad);
        g.addColorStop(0, "#FFFFFF");
        g.addColorStop(0.34, "#FFF6E2AA");
        g.addColorStop(1, "#FFF6E200");
        c.globalAlpha = 0.85 * fade; c.fillStyle = g;
        c.beginPath(); c.arc(u.x, u.y, rad, 0, TAU); c.fill();
      } else if (u.phase === "cold"){
        /* the dud, and it looks like one: the light goes out under the
           caster instead of a burst that never came */
        const ex = clamp(u.t / 0.9, 0, 1);
        c.globalAlpha = (1 - ex) * 0.34;
        c.fillStyle = "#FFF6E2";
        c.beginPath(); c.arc(src.x, src.y, 52 * (1 - ex * 0.5), 0, TAU); c.fill();
      }
      c.globalCompositeOperation = "source-over";
    }
'''

OVER_ANCHOR = ('drawUltOver(m){\n    const s = this._ult(m); if (!s) return;\n'
               '    const { u, src, tgt, k } = s, c = this.ctx, A = CONFIG.arena;\n'
               '    c.save();\n'
               '    c.lineCap = "round"; c.lineJoin = "round";')
OVER_NEW = OVER_ANCHOR + '''

    /* ---- THE HARROWING, over -------------------------------------------
       ONE CRESCENT PER BLADE THAT STUCK, thrown outward from the burst. The
       count is the mechanic, so the count is on screen and countable in the
       frame — the same rule Slagburst's shards follow, and the reason its
       fuse draws the true count rather than the capped one. */
    if (u.w === "lastlight" && u.phase === "bloom"){
      const n = u.n || 1;
      c.globalCompositeOperation = "lighter";
      const ex = clamp(u.t / 0.44, 0, 1);
      const fade = 1 - clamp((u.t - 0.44) / 1.05, 0, 1);
      for (let i = 0; i < n; i++){
        const a2 = (i / n) * TAU + shellHash(8101, i) * 0.8;
        const d = (26 + 160 * (1 - Math.pow(1 - ex, 2.0)))
                * (0.7 + shellHash(8111, i) * 0.6);
        c.globalAlpha = fade * (1 - ex * 0.5);
        c.save();
        c.translate(u.x + Math.cos(a2) * d, u.y + Math.sin(a2) * d);
        c.rotate(a2 + u.t * 7);
        c.fillStyle = "#FFFFFF";
        c.strokeStyle = "#FFF6E2"; c.lineWidth = 1.6;
        this._miniScythe(c, 9.5 * (1 - ex * 0.3));
        c.restore();
      }
      c.globalAlpha = fade * (1 - ex) * 0.95;
      c.strokeStyle = "#FFFFFF"; c.lineWidth = 6 * (1 - ex) + 1.5;
      c.shadowColor = "#FFF6E2"; c.shadowBlur = 18;
      c.beginPath();
      c.arc(u.x, u.y, (66 + n * 22) * (1 - Math.pow(1 - ex, 2.6)), 0, TAU);
      c.stroke();
      c.shadowBlur = 0;
      c.globalCompositeOperation = "source-over";
    }
'''

# ---------------------------------------------------------------- sfx ----

SFX_ANCHOR = '        } else if (w === "thornwake"){                  // creak and cinch'
SFX_NEW = '''        } else if (w === "lastlight-throw"){            // twelve blades leave
          /* Bright, short, and PLURAL — three staggered slices rather than one
             swell, because what the eye is about to see is a count. */
          this._burst(t,        { freq: 3400, q: 1.6, gain: 0.20, dur: 0.16, type:"highpass" });
          this._burst(t + 0.05, { freq: 4200, q: 1.6, gain: 0.15, dur: 0.14, type:"highpass" });
          this._burst(t + 0.10, { freq: 5000, q: 1.6, gain: 0.11, dur: 0.12, type:"highpass" });
          this._tone (t,        { freq: 300, to: 900, gain: 0.13, dur: 0.34, type:"triangle" });
        } else if (w === "lastlight-stick"){            // one buries itself
          /* Rises with the count, so the ear hears the fuse getting heavier
             without anything on screen having to say so. Deliberately quiet:
             this can fire six times in two seconds. */
          const n = Math.max(1, Math.min(6, p.n || 1));
          this._burst(t, { freq: 1800 + n * 260, q: 4.0, gain: 0.09, dur: 0.13, type:"bandpass" });
          this._tone (t, { freq: 520 + n * 70, to: 180, gain: 0.07, dur: 0.18, type:"sine" });
        } else if (w === "lastlight-bloom"){            // and they all go
          /* Scaled on the same n as every other channel of the burst: one
             blade is a chime, six is the roof coming off. */
          const n = Math.max(1, Math.min(8, p.n || 1)), g = 0.22 + n * 0.055;
          this._tone (t,        { freq: 180 + n * 20, to: 34, gain: g, dur: 0.55 + n * 0.04, type:"sine" });
          this._burst(t,        { freq: 260, q: 0.5, gain: g * 0.8, dur: 0.42, type:"lowpass" });
          this._burst(t + 0.01, { freq: 6200, q: 0.8, gain: 0.10 + n * 0.022, dur: 0.30, type:"highpass" });
          this._tone (t + 0.04, { freq: 1400, to: 620, gain: 0.10 + n * 0.012, dur: 0.42, type:"triangle" });
        } else if (w === "lastlight-cold"){             // nothing held
          this._tone (t, { freq: 420, to: 90, gain: 0.15, dur: 0.6, type:"sine" });
          this._burst(t, { freq: 2400, q: 0.8, gain: 0.07, dur: 0.5, type:"highpass" });
''' + SFX_ANCHOR


# ---------------------------------------------------------------- edit ----

def one(src, old, new, label):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"anchor {label!r} matched {n} times, expected 1")
    return src.replace(old, new, 1)


def preflight():
    """Structural checks that do not need a browser. Cheapest failures first."""
    fails = []
    if len(ULT_TIP) > 72:
        fails.append(f"ult tip is {len(ULT_TIP)} chars, limit 72")
    if DATA["life"] >= DATA["fuse"]:
        fails.append(f"life {DATA['life']} >= fuse {DATA['fuse']} — blades "
                     "would still be in the air at the bloom, which the "
                     "'all at once' design says cannot happen")
    if DATA["arm"] <= 0:
        fails.append("arm must be > 0 or every blade resolves on spawn")
    # The spawn ring has to clear the hit test, or the spray is a nova. Ball
    # radius is 34 in CONFIG.physics; the spawn offset is R + r + 10.
    if 34 + DATA["r"] + 10 <= 34 + DATA["r"]:
        fails.append("spawn offset does not clear R + r")
    if DATA["burdenMove"] * 6 >= 0.55:
        fails.append(f"six blades would cost {DATA['burdenMove']*6:.2f} move, "
                     "past moveMul's 0.45 floor — the floor would be doing the "
                     "tuning instead of the number")
    if fails:
        for f in fails:
            print(f"  PREFLIGHT FAIL — {f}", file=sys.stderr)
        raise SystemExit(1)
    print(f"  preflight ok · ult tip {len(ULT_TIP)}/72 chars · "
          f"life {DATA['life']} < fuse {DATA['fuse']} · "
          f"6 blades = -{DATA['burdenMove']*6:.0%} move, "
          f"+{DATA['burdenMass']*6:.1f} fall mass")


def build(src_path, out_path, blade):
    preflight()
    src = src_path.read_text(encoding="utf-8")

    if 'id:"lastlight"' in src:
        raise SystemExit("source already contains lastlight — build from a "
                         "chain tip that does not")

    relic = RELIC.format(blade=blade, name=ULT_NAME, tip=ULT_TIP,
                         blurb=BLURB, **DATA)

    src = one(src, RELIC_ANCHOR, RELIC_ANCHOR + relic, "relic data")
    src = one(src, STATE_OLD, STATE_NEW, "fighter state")
    src = one(src, MOVEMUL_OLD, MOVEMUL_NEW, "moveMul burden")
    src = one(src, GRAV_OLD, GRAV_NEW, "move() fall mass")
    src = one(src, TICKTOP_OLD, TICKTOP_NEW, "tickCharge drop-on-death")
    src = one(src, TICK_ANCHOR, TICK_NEW, "tickCharge fuse")
    src = one(src, FIRE_ANCHOR, FIRE_NEW, "fireUlt harrow branch")
    src = one(src, LATCH_ANCHOR, LATCH_NEW, "tickShots latch")
    src = one(src, HARROW_ANCHOR, HARROW, "harrow + unstick methods")
    src = one(src, MINI_ANCHOR, MINI + MINI_ANCHOR, "_miniScythe")
    src = one(src, MINI_ANCHOR, STUCK, "drawStuck")
    src = one(src, ORDER_OLD, ORDER_NEW, "draw order")
    src = one(src, SHOTART_ANCHOR, SHOTART_NEW, "drawShots blade art")
    src = one(src, UNDER_ANCHOR, UNDER_NEW, "drawUltUnder set-piece")
    src = one(src, OVER_ANCHOR, OVER_NEW, "drawUltOver set-piece")
    src = one(src, SFX_ANCHOR, SFX_NEW, "sfx")

    out_path.write_text(src, encoding="utf-8")
    return hashlib.sha256(src.encode()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="sc-cardspin.html")
    ap.add_argument("--out", default="sc-lastlight.html")
    ap.add_argument("--blade", type=float, default=TUNED_LL,
                    help=f"Lastlight's damage per hit (default {TUNED_LL}, "
                         "a PLACEHOLDER — see the docstring)")
    a = ap.parse_args()

    sp = pathlib.Path(a.src)
    if not sp.is_absolute():
        sp = HERE / a.src
        if not sp.exists():
            sp = HERE.parent / "02-chain" / a.src
    op = (HERE.parent / "02-chain" / a.out) if "/" not in a.out else pathlib.Path(a.out)
    if op.name == PROTECTED:
        raise SystemExit("refusing to write the shipped file")
    if not sp.exists():
        raise SystemExit(f"no such source: {sp}")

    h = build(sp, op, a.blade)
    print(f"{sp.name} -> {op}  sha256 {h}  blade {a.blade}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
