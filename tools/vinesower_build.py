#!/usr/bin/env python3
"""VINESOWER and THE THICKET. The verdant bow, and the twenty-second relic.

    python3 vinesower_build.py --src ../02-chain/sc-foregone.html \
                              --out ../02-chain/sc-vinesower.html

THE DESIGN IS RICK'S AND IS QUOTED IN FULL in the v40 design document:

    "for a duration the bow fires out seeds instead of arrows. the seeds deal
     normal damage if they hit another ball. or disappear if clanked. however
     if they stick to the wall they take root. after a short time the bloom
     into a flowering plant with a vine whip that reaches out and strikes at
     the enemy if they come close enough. vine whips should have good but
     limited range so several can swipe at the enemy at the same time. the
     vines cannot be damaged or removed by the enemy. the vines stay for a
     duration and then wither and die. the vines should have knockback. the
     vines should have their own unique whipping sound effect."

## WHY THIS IS THE ANSWER TO WHAT THE SURVEY MEASURED

`bow_survey.py` found that **82% of every arrow this game has ever fired ends
on a wall**, that the wall is worth ten times what any status is on this type,
and that nothing in twenty-one relics addresses it. This ultimate does not
mitigate that number. It SPENDS it. The arrows that miss are the ones that do
the work.

At `cadence 0.34` a five-second window fires ~14.7 seeds and roots ~12 of
them, which is why "several can swipe at the same time" is reachable at all
and why `maxVines` is a requirement rather than a nicety.

## What is FREE, and it is two of the seven sentences

A seed is a `shot`. "Disappear if clanked" is what the parry already does to
any projectile; "normal damage if they hit another ball" is what the hit
branch already does through `resolveHit`. No code was written for either.

"The vines cannot be damaged or removed by the enemy" is free in the strongest
sense available: a vine is not in `a` or `b`, so `tickHits`, `tickClank` and
`tickShots` cannot see one. There is nothing to exempt.

## The zero-burden argument, kept structurally

    ALL STATE LIVES IN `m.vines` AND `f.ultBloom`, WHICH ARE EMPTY AND null
    ON EVERY OTHER RELIC.

`tickVines` returns on its first line when the list is empty, and the branch
in `spawnShot` is one `!!f.ultBloom`. `engine_ab` over the twenty-one
pre-existing ids is the proof, not this paragraph.

## The one thing that had to be invented

**A VINE IS A WALL AND A POSITION ALONG IT, NOT AN (x, y).**
`CONFIG.collapse` walks `m.inset` from 0 to 140 over a fight, so a plant
rooted at 10s is outside the hall by 40s -- buried in the closing wall and
lashing from off-screen. Storing `{wall, u}` and recomputing the perpendicular
coordinate from the CURRENT inset every frame costs two lines and turns the
collapse into part of the mechanic: `bow_survey` §3b measured separation
halving 252 -> 148 as the walls come in, so the garden closes on the fight
exactly as the fight compresses.

## Every number below is a PLACEHOLDER and is marked as one

`dmg`, `dur`, `sprout`, `vineLife`, `reach`, `whipDmg`, `whipCd`, `whipKnock`
and `maxVines` are unset in the design and cannot be guessed. The economy is
worse than the Converse's: the plant count is linear in `dur`, the number that
can reach one point at once grows with `reach`, and the damage is the product
of both against a cooldown. `vinesower_sweep.py` is the instrument and it is
the next thing after the probe.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

RELIC_ID = "vinesower"
# VINESOWER. Rick's, offered against four of mine and better than all of them
# for one reason none of mine had: it is the only candidate that names BOTH
# halves of the relic. The bow SOWS -- that is the ultimate, and it is the
# thing no other relic in the game does -- and what grows is a VINE, which is
# the part that fights. Quickthorn, Coppice and Briarcast each named the
# planting or the plant; this names the act and its consequence in one word,
# and it lands in the -er agent register the roster already runs on
# (Widowmaker, Grudgebearer, Lightkeeper, Farwarden).
#
# THE ID MATCHES THE NAME, and that is deliberate. Two relics in this roster
# already carry drift -- `oathwound` displays as Goreshard, `redflail` as
# Threshmaw -- and both are traps that have cost a reader time. A third was
# not worth the twenty minutes it took to avoid.
RELIC_NAME = "Vinesower"
ULT_NAME = "Thicket"

# ---------------------------------------------------------------------------
# EVERY ONE OF THESE IS A PLACEHOLDER. None is swept. See the module docstring.
TUNED_QS = 16.23        # Ironhail's, because the type owns the profile
ULT = {
    "charge":    15,    # the roster's standard
    # RICK'S SECOND NOTE, and it is a better design than the one it replaces:
    # "instead of firing for a duration it loads up a fixed number of seeds and
    # fires them until they deplete." A duration is a number the viewer cannot
    # see; a magazine is one they can COUNT, and it makes the garden's size a
    # property of the ultimate rather than a consequence of how often the bow
    # happened to be stunned while the clock ran.
    "seeds":     12,    # the magazine. Fires at the bow's own cadence.
    "sprout":    1.0,   # "after a short time" -- seed on the wall before bloom
    "vineLife":  7.0,   # "stay for a duration and then wither and die"
    # RICK'S THIRD NOTE: "with less vines i think we can afford to make them
    # longer". Swept from here, not chosen here.
    "reach":     132,   # "good but limited range" -- from the plant's own base
    # RICK'S FIRST NOTE: "the vines should have motion and tracking. currently
    # they look stationary and damage the enemy ball when it happens to run
    # into them. i was picturing living vines that reach out and slash."
    "turn":      5.2,   # rad/s the head tracks its quarry at
    "awareMul":  1.7,   # x reach: how far out it starts watching and leaning
    "windup":    0.20,  # it COILS, then it slashes. And it can be dodged.
    "whipDmg":   6,     # priced through resolveHit as a mul on w.dmg
    "whipCd":    1.2,   # per plant, not global
    "whipKnock": 260,   # "the vines should have knockback", vine -> foe
    "maxVines":  14,    # a ceiling on the magazine, not a target
    "lash":      0.30,  # how long one slash is on screen
}
# ---------------------------------------------------------------------------


RELIC_NEW = '''    blurb:"Shards that remember the room. What it has already done to you, it can do again, backwards." },

  /* VINESOWER -- the verdant bow, and the twenty-second relic. Physics are
     Ironhail's, Farwarden's and Aureole's exactly: all three bows share one
     `shot` block byte for byte and the TYPE owns it (bow_survey §1). The
     school owns Entangle and the green, and `SHAPES.bow`'s verdant branch has
     drawn this relic since before it existed -- a bent living branch that
     leafs along its length with a vine for a string, the only school for
     which "a bow" is not a stretch.

     THE CELL'S PROBLEM, measured before the design existed (bow_survey v40,
     verdant_bow_probe v40):

       A bow lands 7.7% of what it fires and 82% of every arrow ends on a
       WALL. Entangle is worth +3 hp in a twenty-second window against the
       same weapon with the channel deleted -- inside the error bar, i.e.
       nothing -- and no setting of it helps: doubling the per-hit value, the
       cap, the duration and BOTH slows at once buys +20, and tripling the
       move slow alone costs 11.

     So the channel cannot carry this relic and neither can the parry: a
     PERMANENT root, more than any ultimate could buy, moves the landed rate
     8.2% -> 10.8%. Suppressing the parry is worth a tenth of what suppressing
     the wall would be.

     THE THICKET SPENDS THE WALL INSTEAD OF FIGHTING IT. The 82% stops being
     a loss and becomes a rate.

     `dmg` and every number under `ult` are PLACEHOLDERS -- vinesower_build's
     TUNED_QS and ULT -- and MUST be swept. */
  { id:"%ID%", name:"%NAME%", aff:"verdant", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:%DMG%, spin:2.8, mode:"ranged", mass:1.6,
    shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
           tip:"Fires along its facing · shots can be clanked" },
    onHit:{ entangle:2 },
    ult:{ name:"%ULT%", charge:%CHARGE%, kind:"seedfall",
          seeds:%SEEDS%, sprout:%SPROUT%, vineLife:%VINELIFE%,
          reach:%REACH%, turn:%TURN%, awareMul:%AWAREMUL%, windup:%WINDUP%,
          whipDmg:%WHIPDMG%, whipCd:%WHIPCD%,
          whipKnock:%WHIPKNOCK%, maxVines:%MAXVINES%, lash:%LASH%,
          /* THE NUMBER IN THE TIP IS SUBSTITUTED, not typed. The first build
             said "5s" and the sweep moved `dur` to 8.1 -- a card telling the
             viewer a number the weapon does not have, which nothing in
             verify.py would ever have caught because it only asks that a tip
             EXISTS. `vinesower_probe` asserts the two agree now. */
          tip:"Looses %SEEDTIP% seeds; those that reach a wall root and lash out" },
    blurb:"A branch bent living and never let go. What it misses with takes root where it lands." },

];'''

MATCH_STATE_NEW = '''    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed
    /* THE THICKET. Plants rooted on the walls, in the same family as
       `sparks`, `shades` and `drains`: SIM objects that only one relic can
       ever create, so every loop over them runs zero times in any match
       without it. `tickVines` returns on its first line when this is empty,
       which is the whole zero-burden argument and is what engine_ab is
       asserting over the other twenty-one ids.

       A VINE IS A WALL AND A POSITION ALONG IT. `m.inset` walks 0 -> 140 as
       the hall collapses, so an absolute (x, y) planted early is outside the
       room later -- buried in the wall, lashing from off-screen. Storing
       {wall, u} and recomputing the perpendicular coordinate each frame is
       two lines and makes the collapse part of the mechanic. */
    this.vines = [];
    this.vineSeq = 0;         // deterministic per-plant art variation'''

FIGHTER_STATE_NEW = '''    this.ultRadiant = null;   // {t, dur} while Daybreak burns
    /* {t, dur} while the Thicket sows. Exactly `ultRadiant`'s shape and for
       exactly its reason: Daybreak already established "for a duration this
       weapon's HITS are different", and this is "for a duration this weapon's
       SHOTS are different" -- one field, and one `!!f.ultBloom` in spawnShot. */
    this.ultBloom = null;'''

SEED_FLAG_NEW = '''      dmgMul: S.dmgMul === undefined ? 1 : S.dmgMul,
      /* THE SEED. One flag, read in three places: the wall branch of
         tickShots plants it, drawShots draws it, and nothing else in the
         engine knows it exists. False on every shot any other relic fires,
         including this one outside its own window.

         AND THIS IS WHERE THE MAGAZINE EMPTIES. Decremented at the barrel, so
         a seed that is loaded is a seed that LEFT -- not one a clock ran out
         from under. */
      seed: f.ultBloom ? (f.ultBloom.left--, true) : false,
      aff: f.aff, a,
    });'''

WALL_STICK_NEW = '''      /* --- THE SEED TAKES ROOT. Rick: "however if they stick to the wall
         they take root." Deliberately placed AFTER the parry and both hit
         branches and BEFORE `spent`, which is the order the three sentences
         of the design are in: clanked seeds disappear, seeds that find a ball
         deal normal damage, and only what is left reaches a wall.

         The test is the WALL half of the spent predicate and not the whole
         of it. A seed that ran out of life in mid-air has not stuck to
         anything and must not sprout in the middle of the room -- it cannot
         happen today (bow_survey §4: a shot travels 1292 units in its life
         and the longest wall is 800, so `life` has never once expired in this
         game) and the branch does not rely on that staying true. */
      if (!dead && s.seed && (s.x < n + s.r || s.x > A.w - n - s.r
                              || s.y < n + s.r || s.y > A.h - n - s.r)){
        this.plantVine(s);
        dead = true;
      }

      /* --- spent. No bounce: a ricocheting arrow is chaos the viewer cannot
         attribute to anything, and a miss ending visibly on the wall is what
         makes the miss cost something. */'''

TICK_VINES_NEW = '''  /* ------------------------------------------------------------- THICKET --
     Rick's design is quoted in full in the v40 design doc, and his note on the
     first render is what this method's shape is:

       "the vines should have motion and tracking. currently they look
        stationary and damage the enemy ball when it happens to run into them.
        i was picturing living vines that reach out and slash"

     He was right and the mechanic was the reason, not the art. A vine used to
     resolve the instant the quarry crossed `reach` -- so the strike had no
     duration, nothing on screen ever REACHED, and the only honest reading of
     the picture was a hazard you walked into. A plant that watches, coils and
     then slashes has three states the eye can tell apart and a wind-up the
     quarry can leave. */

  /* WHICH WALL, AND WHERE ALONG IT. Resolved once, at planting, from the same
     predicate tickShots used to decide the seed had arrived -- so the plant is
     always on the wall the viewer just watched the seed hit, and never on a
     corner's other face. `u` is the fraction along that wall in ARENA space,
     which is what survives the collapse. */
  plantVine(s){
    /* The seed's OWNER is the caster, by construction: `seed` is set from
       `f.ultBloom` in spawnShot and nothing else in the engine sets it. So
       the ult block comes off the owner and never off a search of the
       roster -- which is what stops this being wrong the day a second relic
       sows something. */
    const u = this[s.own].w.ult;
    const A = CONFIG.arena, n = this.inset;
    const dW = s.x - (n + s.r), dE = (A.w - n - s.r) - s.x;
    const dN = s.y - (n + s.r), dS = (A.h - n - s.r) - s.y;
    const mn = Math.min(dW, dE, dN, dS);
    const wall = mn === dW ? "W" : mn === dE ? "E" : mn === dN ? "N" : "S";
    /* THE CAP DROPS THE OLDEST, not the newest. A cast that is still sowing
       should always be able to plant, and the plant that has already had the
       most of its life is the one with the least left to lose. Same rule
       `shots` and `sparks` follow. */
    if (this.vines.length >= (u.maxVines || 14)) this.vines.shift();
    /* Deterministic per-plant variation, from `shellHash` and NOT `this.rng()`
       -- the house rule since Ironbloom's splinters: a relic that is not in
       the match must not be able to perturb the draw order of one that is,
       and a probe that pins a seed must get the same garden twice. */
    const idx = this.vineSeq = (this.vineSeq || 0) + 1;
    const nx = wall === "W" ? 1 : wall === "E" ? -1 : 0;
    const ny = wall === "N" ? 1 : wall === "S" ? -1 : 0;
    this.vines.push({
      own: s.own, wall,
      u: wall === "N" || wall === "S"
         ? clamp((s.x - n) / Math.max(1, A.w - 2 * n), 0.02, 0.98)
         : clamp((s.y - n) / Math.max(1, A.h - 2 * n), 0.02, 0.98),
      x: s.x, y: s.y, t: 0, cd: 0,
      /* THE THREE STATES. `aim` is where the head is looking and is the only
         state on a vine that is not derived from `t`; it starts pointing
         straight into the room. `lean` is how far it has committed toward the
         quarry. `wind` is the coil, `lash` is the slash. */
      aim: Math.atan2(ny, nx), lean: 0, wind: 0,
      lash: 0, lashMax: u.lash || 0.30, lashA: 0, hit: false,
      lx: 0, ly: 0, whips: 0, lands: 0,
      sprout: u.sprout || 1.0, life: u.vineLife || 7.0,
      ph: shellHash(9311, idx) * TAU,
      bend: (shellHash(9319, idx) - 0.5) * 0.8,
      leaves: 3 + ((shellHash(9323, idx) * 3) | 0),
    });
    this.spawnFx(s.x, s.y, s.aff.core, 5, 90, 0.3, 2.4);
    SFX.play("vine", { plant: true });
  }

  tickVines(dt){
    if (!this.vines.length) return;          // <- the zero-burden guard
    const A = CONFIG.arena, R = CONFIG.physics.ballR, n = this.inset;
    for (let i = this.vines.length - 1; i >= 0; i--){
      const v = this.vines[i];
      v.t += dt;
      if (v.lash > 0) v.lash -= dt;
      if (v.t >= v.life + v.sprout){ this.vines.splice(i, 1); continue; }

      /* THE PLANT RIDES THE WALL IN. Recomputed every frame from the CURRENT
         inset, which is the whole reason a vine is stored as {wall, u}. */
      if (v.wall === "N" || v.wall === "S"){
        v.x = n + v.u * Math.max(1, A.w - 2 * n);
        v.y = v.wall === "N" ? n + 6 : A.h - n - 6;
      } else {
        v.x = v.wall === "W" ? n + 6 : A.w - n - 6;
        v.y = n + v.u * Math.max(1, A.h - 2 * n);
      }

      if (v.t < v.sprout) continue;          // still a seed on the wall

      const src = this[v.own];
      const foe = v.own === "a" ? this.b : this.a;
      const u = src.w.ult;
      /* A vine will not strike a corpse, and it does not care whether the
         relic that sowed it is still standing -- it withers on its own clock.
         v40 design §3.3, and it is a decision, not an oversight. */
      const live = foe.alive && !this.over;
      const dx = foe.x - v.x, dy = foe.y - v.y;
      const d = Math.hypot(dx, dy);
      const reach = u.reach || 132;
      const aware = reach * (u.awareMul || 1.7);

      /* --- TRACKING. The head turns toward the quarry from well outside
         striking distance, at a rate a plant could plausibly turn at, and
         leans back when it leaves. This is what makes the thing look alive
         between strikes -- the strike itself was never the problem. */
      if (live && d < aware + R){
        const want = Math.atan2(dy, dx);
        let e = want - v.aim;
        while (e >  Math.PI) e -= TAU;
        while (e < -Math.PI) e += TAU;
        v.aim += e * Math.min(1, dt * (u.turn || 5.2));
        v.lean = Math.min(1, v.lean + dt * 2.4);
      } else {
        v.lean = Math.max(0, v.lean - dt * 1.5);
      }

      /* --- THE COIL, AND THEN THE SLASH. The wind-up is what turns a hazard
         into an attack: the plant commits, the quarry has 0.2s to leave, and
         the vine slashes at where its head is pointing WHEN IT RELEASES
         rather than where the quarry was when it decided to. A slash that
         connects with nothing still draws, because a vine that whiffs is the
         only thing that makes one that lands read as aimed. */
      if (v.wind > 0){
        v.wind -= dt;
        if (v.wind > 0) continue;
        v.wind = 0;
        v.lash = v.lashMax;
        v.lashA = v.aim;
        v.whips++;
        const fd = Math.hypot(foe.x - v.x, foe.y - v.y);
        v.hit = live && fd <= reach + R;
        const ux = Math.cos(v.aim), uy = Math.sin(v.aim);
        if (!v.hit){
          v.lx = v.x + ux * reach; v.ly = v.y + uy * reach;
          this.spawnFx(v.lx, v.ly, src.aff.core, 3, 90, 0.22, 1.8);
          SFX.play("vine", { miss: true });
          continue;
        }
        v.lands++;
        const hx = foe.x - ux * R, hy = foe.y - uy * R;
        v.lx = hx; v.ly = hy;
        const seg = { ax: v.x, ay: v.y, bx: hx, by: hy, a: v.aim };
        /* THE STRIKE. Routed through `resolveHit` so a lash is a hit in every
           sense the rest of the game already understands -- crit, jitter, the
           Sunder multiplier, hit stop, diminishing-returns hitstun, the damage
           float, `self.hits++` for verify.py's floor, and the wielder's own
           Entangle. `mul` prices it against the bow's own blow without handing
           tune.py a second knob, which is the same call shape the splinter pop
           uses.

           CINEMA (demo). Rick: "the vines shouldnt trigger the director at
           all". `_cineVine` suppresses the BEAT and nothing else. */
        this._cineVine = v;
        this.resolveHit(src, foe, hx, hy, seg,
                        (u.whipDmg || 6) / Math.max(0.01, src.w.dmg));
        this._cineVine = null;
        /* THE VINE'S OWN KNOCK, along vine -> foe, which is off the wall and
           into the hall. resolveHit's built-in knock still fires away from the
           CASTER -- exactly as it does for every arrow this game has ever
           resolved -- so this is the second of two and it is the readable one. */
        if (foe.alive){
          foe.vx += ux * (u.whipKnock || 260);
          foe.vy += uy * (u.whipKnock || 260);
        }
        this.spawnFx(hx, hy, src.aff.glow, 6, 170, 0.28, 2.6);
        SFX.play("vine", { n: v.lands });
        continue;
      }

      v.cd -= dt;
      if (v.cd > 0 || !live) continue;
      if (d > reach + R) continue;
      v.wind = u.windup || 0.20;
      v.cd = (u.whipCd || 1.2) + v.wind;
      SFX.play("vine", { coil: true });
    }
  }

  tickSparks(dt){'''

TICK_CALL_NEW = '''    this.tickSparks(dt);
    /* AFTER tickShots, so a seed that reached a wall this frame is a plant
       before anything asks it to lash -- and it cannot lash on the frame it
       landed anyway, because `sprout` is a floor it has to clear first. */
    this.tickVines(dt);'''

FIRE_ULT_NEW = '''    /* THE THICKET RESOLVES NOTHING HERE. It sows.

       Everything below this point is skipped for the reason the aimed shot,
       the Crucible, Ironbloom and the Converse skip it: an ultimate that had
       already paid out before the seeds landed would make the seeds
       decorative, and the seeds are the entire ultimate.

       There is no banner either. The name goes nowhere yet, because the thing
       this ultimate does has not happened -- it happens on a wall, up to a
       second and a half later, in as many places as the bow can reach. */
    if (u.kind === "seedfall"){
      /* A MAGAZINE, NOT A CLOCK. Rick: "instead of firing for a duration it
         loads up a fixed number of seeds and fires them until they deplete."
         `left` is decremented in spawnShot and the window closes when it hits
         zero, so a bow that spends the window stunned still gets every seed it
         was loaded with -- under the clock it simply lost them, which was a
         number nobody could see going missing. */
      f.ultBloom = { t: 0, left: u.seeds || 12, loaded: u.seeds || 12 };
      /* The set-piece\'s life is an ESTIMATE and is the one place a duration
         survives: the magazine empties at cadence unless the bow is stunned,
         and the art has to be told how long to stay up before that is known. */
      const est = (u.seeds || 12) * (f.w.shot ? f.w.shot.cadence : 0.34);
      this.ultFx = { w: f.w.id, kind: "seedfall",
                     src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                     x: f.x, y: f.y, tx: foe.x, ty: foe.y, hit: true,
                     radius: 300, aff: f.aff, t: 0, life: est + 0.6 };
      return;
    }
    if (u.kind === "radiant"){'''

WINDOW_NEW = '''    if (f.ultBloom){
      /* The clock is kept for the ART ONLY. What CLOSES the window is the
         magazine running out, in spawnShot, and the cap here exists so a bow
         that is locked down for the rest of the match cannot hold an open
         window forever. */
      f.ultBloom.t += dt;
      if (f.ultBloom.left <= 0 || f.ultBloom.t > 30) f.ultBloom = null;
    }
    if (f.ultRadiant){'''


DRAW_VINES_NEW = '''  /* THE GARDEN, DRAWN. Two passes and they are not the same picture: the
     PLANT is a thing standing on the wall and belongs behind the balls that
     own the health bars; the SLASH is a strike and belongs over them, for the
     same reason a blade's sparks do.

     Everything here is derived from `v.t`, `v.lash` and `v.lean`, never
     accumulated, so it steps with the 120Hz sim and does not strobe against
     the frame interpolator -- the rule the splinter's tumble and the
     Harrowing's turn both follow.

     THE FIRST CUT OF THIS DREW A PLANT THAT NEVER MOVED. Rick, off the first
     render: "currently they look stationary and damage the enemy ball when it
     happens to run into them." The stem leans toward its quarry now, coils
     against the lean while it winds up, and throws the whole vine through the
     slash -- three states with three silhouettes, so which one a plant is in
     is readable from across the hall at phone size. */
  drawVines(m, over){
    if (!m.vines || !m.vines.length) return;
    const c = this.ctx;
    c.save();
    c.lineCap = "round"; c.lineJoin = "round";
    for (const v of m.vines){
      const src = m[v.own];
      const p = src.aff;
      const grow   = clamp(v.t / Math.max(0.01, v.sprout), 0, 1);
      const age    = clamp((v.t - v.sprout) / Math.max(0.01, v.life), 0, 1);
      const wither = clamp((age - 0.80) / 0.20, 0, 1);
      const nx = v.wall === "W" ? 1 : v.wall === "E" ? -1 : 0;
      const ny = v.wall === "N" ? 1 : v.wall === "S" ? -1 : 0;
      const tx = -ny, ty = nx;                       // along the wall
      /* the aim, in the wall's own basis: `an` is how much of it points into
         the room, `at` how much of it runs along the wall */
      const ax = Math.cos(v.aim), ay = Math.sin(v.aim);
      const an = ax * nx + ay * ny, at = ax * tx + ay * ty;
      const K  = v.lash > 0 ? clamp(v.lash / Math.max(0.01, v.lashMax), 0, 1) : 0;
      const W  = v.wind > 0 ? 1 : 0;

      if (over){
        /* ---- THE SLASH. The vine goes OUT along the bearing it released on,
           bows hard to one side, and comes back -- so the stroke has a
           direction the eye can follow instead of being a line that appeared.
           `K` runs 1 -> 0, so `e` is 0 -> 1 -> 0 and the tip travels out and
           returns. A miss draws the same stroke to empty air and that is the
           point: it is what makes the ones that land read as aimed. */
        if (v.lash <= 0) continue;
        const e = Math.sin(Math.PI * (1 - K));
        const L = Math.hypot(v.lx - v.x, v.ly - v.y) || 1;
        const bx = Math.cos(v.lashA), by = Math.sin(v.lashA);
        const px = -by, py = bx;
        const sweep = (1 - 2 * (1 - K)) * L * 0.40 * (v.bend >= 0 ? 1 : -1);
        const tipD = L * (0.25 + 0.75 * e);
        const TX = v.x + bx * tipD, TY = v.y + by * tipD;
        const CX = v.x + bx * tipD * 0.55 + px * sweep;
        const CY = v.y + by * tipD * 0.55 + py * sweep;
        c.globalCompositeOperation = "lighter";
        const draw = (wd, col, al) => {
          c.globalAlpha = al; c.strokeStyle = col; c.lineWidth = wd;
          c.beginPath();
          c.moveTo(v.x + nx * 12, v.y + ny * 12);
          c.quadraticCurveTo(CX, CY, TX, TY);
          c.stroke();
        };
        c.shadowColor = p.core; c.shadowBlur = 12 * e;
        draw(2 + 6 * e, p.glow, 0.85 * e);
        c.shadowBlur = 0;
        draw(1 + 2.4 * e, "#EAFBE4", 0.95 * e);
        /* the tip: a leaf on a miss, a burst of them on a connect */
        c.globalAlpha = e * (v.hit ? 1 : 0.55);
        c.fillStyle = v.hit ? "#EAFBE4" : p.core;
        c.save();
        c.translate(TX, TY);
        c.rotate(Math.atan2(TY - CY, TX - CX));
        const LL = (v.hit ? 13 : 9) * e;
        c.beginPath();
        c.moveTo(0, 0);
        c.quadraticCurveTo(LL * 0.5, -LL * 0.34, LL, 0);
        c.quadraticCurveTo(LL * 0.5,  LL * 0.34, 0, 0);
        c.closePath(); c.fill();
        c.restore();
        c.globalAlpha = 1;
        continue;
      }

      /* ---- THE PLANT.
         `nk` is how far it stands out of the wall and `tk` how far it leans
         along it. Three states drive them:
           watching  -- leans toward the quarry by `lean`
           coiling   -- pulls BACK against that lean and shortens
           slashing  -- the plant itself is thrown out along the stroke
         The first cut had neither of the last two and no `lean` at all. */
      c.globalCompositeOperation = "source-over";
      const dead = wither;
      const H0 = (16 + 46 * grow) * (1 - wither * 0.30);
      const coil = W ? 1 : 0;
      const H = H0 * (1 - 0.26 * coil + 0.30 * (K > 0 ? Math.sin(Math.PI * (1 - K)) : 0));
      const droop = wither * 1.0;
      const bx2 = v.x, by2 = v.y;
      const sway = Math.sin(m.t * 1.9 + v.ph) * 3.4 * grow * (1 - wither * 0.6)
                 * (1 - v.lean * 0.7);
      /* the lean, and the coil that pulls against it */
      const leanT = at * v.lean * 0.85 * (1 - 2.0 * coil);
      const leanN = 1 + an * v.lean * 0.30;
      const B = v.bend * (1 - v.lean * 0.6);
      const P = (uu) => {
        const it = 1 - uu;
        const p1n = 0.34 * leanN, p1t = -B * 0.42 + leanT * 0.18;
        const p2n = 0.74 * leanN, p2t =  B * 0.66 + leanT * 0.62;
        const p3n = 1.00 * leanN, p3t =  B * 0.34 + leanT + droop * 0.55;
        const kn = 3*it*it*uu*p1n + 3*it*uu*uu*p2n + uu*uu*uu*p3n;
        const kt = 3*it*it*uu*p1t + 3*it*uu*uu*p2t + uu*uu*uu*p3t;
        const dn = 3*it*it*(p1n) + 6*it*uu*(p2n-p1n) + 3*uu*uu*(p3n-p2n);
        const dt2= 3*it*it*(p1t) + 6*it*uu*(p2t-p1t) + 3*uu*uu*(p3t-p2t);
        return { x: bx2 + nx*kn*H + tx*(kt*H + sway*uu),
                 y: by2 + ny*kn*H + ty*(kt*H + sway*uu),
                 a: Math.atan2(ny*dn + ty*dt2, nx*dn + tx*dt2) };
      };
      const HD = P(1);

      const stemCol = dead > 0.5 ? "#6E5C3C" : p.core;
      const stroke = (wd, col) => {
        c.strokeStyle = col; c.lineWidth = wd;
        c.beginPath();
        c.moveTo(bx2, by2);
        for (let i = 1; i <= 10; i++){ const q = P(i / 10); c.lineTo(q.x, q.y); }
        c.stroke();
      };
      stroke(6.2, SHAPES._ink(p.dark, 9.71));
      stroke(3.0, stemCol);
      stroke(1.1, dead > 0.5 ? "#8A7550" : p.glow);

      /* ALTERNATING leaves, broad, with a midrib. `sg` flips with the index
         rather than running both ways at once, which is the whole difference
         between a plant and fletching. They fold back along the stem as the
         thing coils, which is most of what makes the wind-up read. */
      for (let i = 0; i < v.leaves; i++){
        const uu = 0.30 + i * (0.56 / Math.max(1, v.leaves - 1));
        const q = P(uu);
        const sg = (i % 2) ? 1 : -1;
        c.save();
        c.translate(q.x, q.y);
        c.rotate(q.a + sg * (1.02 - 0.30 * uu) * (1 - 0.55 * coil)
                 + droop * sg * 0.55);
        const L = (13 - 3 * uu) * grow * (1 - wither * 0.42);
        const Wd = L * 0.52;
        c.strokeStyle = SHAPES._ink(p.dark, 9.71); c.lineWidth = 1.3;
        c.fillStyle = dead > 0.5 ? "#8A7550" : p.core;
        c.globalAlpha = 1 - wither * 0.5;
        c.beginPath();
        c.moveTo(0, 0);
        c.quadraticCurveTo(L * 0.45, -Wd, L, 0);
        c.quadraticCurveTo(L * 0.45,  Wd, 0, 0);
        c.closePath(); c.fill(); c.stroke();
        c.strokeStyle = dead > 0.5 ? "#6E5C3C" : p.glow;
        c.lineWidth = 0.9;
        c.beginPath(); c.moveTo(L * 0.06, 0); c.lineTo(L * 0.88, 0); c.stroke();
        c.restore();
      }
      c.globalAlpha = 1;

      if (grow >= 1){
        /* THE FLOWER IS THE TELL. Shut while the seed is sprouting, open once
           the plant can strike, and it BRIGHTENS through the coil -- so the
           0.2s a quarry has to leave is a thing on screen and not a number in
           a config block. */
        const open = clamp((v.t - v.sprout) / 0.35, 0, 1) * (1 - wither * 0.8);
        const hot = coil ? 1 - (v.wind / Math.max(0.01, src.w.ult.windup || 0.2)) : 0;
        c.save();
        c.translate(HD.x, HD.y);
        c.rotate(HD.a + v.ph * 0.2);
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = (0.5 + 0.5 * hot) * open;
        const g = c.createRadialGradient(0, 0, 1, 0, 0, 22 + 14 * hot);
        g.addColorStop(0, p.glow + "99"); g.addColorStop(1, p.glow + "00");
        c.fillStyle = g;
        c.beginPath(); c.arc(0, 0, 22 + 14 * hot, 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        c.globalAlpha = open;
        const PR = 13 * open * (1 + 0.25 * hot);
        for (let i = 0; i < 5; i++){
          c.save();
          c.rotate(i * TAU / 5);
          c.fillStyle = dead > 0.4 ? "#9A8A5E" : (hot > 0.5 ? "#EAFBE4" : p.glow);
          c.strokeStyle = SHAPES._ink(p.dark, 9.71); c.lineWidth = 1.1;
          c.beginPath();
          c.moveTo(0, 0);
          c.quadraticCurveTo(PR * 0.55, -PR * 0.46, PR, 0);
          c.quadraticCurveTo(PR * 0.55,  PR * 0.46, 0, 0);
          c.closePath(); c.fill(); c.stroke();
          c.restore();
        }
        c.fillStyle = "#F6F2C8";
        c.beginPath(); c.arc(0, 0, (3.4 + 1.6 * hot) * open, 0, TAU); c.fill();
        c.globalAlpha = 1;
        c.restore();
      } else {
        /* still a seed: a husk on the wall with a crack of light in it */
        c.globalAlpha = 1;
        c.fillStyle = SHAPES._ink(p.dark, 9.71);
        c.beginPath(); c.arc(bx2 + nx * 5, by2 + ny * 5, 5.4, 0, TAU); c.fill();
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = 0.35 + 0.45 * Math.sin(m.t * 7 + v.ph) * grow;
        c.fillStyle = p.glow;
        c.beginPath(); c.arc(bx2 + nx * 5, by2 + ny * 5, 2.2 * grow + 0.8, 0, TAU); c.fill();
        c.globalAlpha = 1;
      }
    }
    c.restore();
  }

  drawSparks(m){'''

DRAW_CALL_UNDER_NEW = '''    this.drawDrips(m);
    /* the garden is ON the wall and the balls are in front of it */
    this.drawVines(m, false);'''

DRAW_CALL_OVER_NEW = '''    this.drawSparks(m);
    /* and a lash is a strike, so it goes over the thing it struck */
    this.drawVines(m, true);'''

SEED_ART_NEW = '''      /* A SEED OF THE THICKET. Not an arrow: an arrow reads by its 9:1 aspect
         ratio and a seed borrowing it would say "this is still archery",
         which is the one thing this window is not. A short husk with a tuft
         behind it, tumbling on a DERIVED angle off its own spawn heading so
         it steps with the sim rather than strobing against the interpolator.
         Same construction rule as the splinter and the Harrowing's blades. */
      if (s.seed){
        const ang = s.a + (s.max - s.life) * 9.0;
        const rr = s.r * 0.42;
        c.globalCompositeOperation = "lighter";
        const gh = c.createRadialGradient(s.x, s.y, 1, s.x, s.y, s.r * 1.5);
        gh.addColorStop(0, s.aff.glow + "88");
        gh.addColorStop(1, s.aff.glow + "00");
        c.globalAlpha = 0.6; c.fillStyle = gh;
        c.beginPath(); c.arc(s.x, s.y, s.r * 1.5, 0, TAU); c.fill();
        c.globalCompositeOperation = "source-over";
        c.save();
        c.translate(s.x, s.y);
        c.rotate(ang);
        /* the tuft, trailing */
        c.globalAlpha = 0.85;
        c.strokeStyle = s.aff.glow; c.lineWidth = 1.5; c.lineCap = "round";
        for (let i = -1; i <= 1; i++){
          c.beginPath();
          c.moveTo(-rr * 0.6, 0);
          c.quadraticCurveTo(-rr * 2.2, i * rr * 0.8, -rr * 3.6, i * rr * 1.9);
          c.stroke();
        }
        c.globalAlpha = 1;
        c.fillStyle = SHAPES._ink(s.aff.dark, 9.71);
        c.beginPath(); c.ellipse(0, 0, rr * 1.35, rr * 0.86, 0, 0, TAU); c.fill();
        c.fillStyle = s.aff.core;
        c.beginPath(); c.ellipse(0, 0, rr * 1.0, rr * 0.58, 0, 0, TAU); c.fill();
        c.fillStyle = "#EAFBE4";
        c.beginPath(); c.arc(rr * 0.42, -rr * 0.14, rr * 0.24, 0, TAU); c.fill();
        c.restore();
        c.lineCap = "butt";
        continue;
      }
      if (s.spike){'''

SFX_VINE_NEW = '''      else if (kind === "vine"){
        /* A WHIP, and it is the one sound in this game built out of MOTION
           rather than impact. Three parts, and the order is the whole trick:
           a fast bandpass sweep UP is the vine travelling, a hard short crack
           on top is the tip going supersonic (which is what a real whip crack
           is), and a low woody thump under it is the stem taking the load.
           The crack is what makes it a whip; without it this is a swish.

           `plant` is a different, much quieter event -- a seed finding a wall
           and taking -- and it fires up to a dozen times in five seconds, so
           it is soft, short and low, and deliberately nothing like the lash. */
        if (p && p.plant){
          this._burst(t, { freq: 620, q: 1.6, gain: 0.055, dur: 0.05, type:"bandpass" });
          this._tone (t, { freq: 150, to: 84, gain: 0.055, dur: 0.10, type:"sine" });
        } else if (p && p.coil){
          /* THE WIND-UP HAS A SOUND because it has counterplay. A rising
             creak, quiet, and it is the only warning the quarry gets. */
          this._tone (t, { freq: 120, to: 260, gain: 0.05, dur: 0.19, type:"triangle" });
          this._burst(t, { freq: 480, q: 2.4, gain: 0.035, dur: 0.18, type:"bandpass" });
        } else if (p && p.miss){
          /* a whiff: the swish with the crack taken off it, which is exactly
             what a whip that hits nothing is */
          this._burst(t,        { freq: 900,  q: 1.0, gain: 0.07, dur: 0.055, type:"bandpass" });
          this._burst(t + 0.03, { freq: 2200, q: 1.1, gain: 0.07, dur: 0.06,  type:"bandpass" });
        } else {
          const n = Math.min(6, (p && p.n) || 1);
          this._burst(t,        { freq: 900,  q: 1.0, gain: 0.10, dur: 0.055, type:"bandpass" });
          this._burst(t + 0.03, { freq: 2400, q: 1.1, gain: 0.13, dur: 0.05,  type:"bandpass" });
          this._burst(t + 0.06, { freq: 5200 + n * 120, q: 1.5, gain: 0.16, dur: 0.035, type:"highpass" });
          this._tone (t + 0.05, { freq: 340, to: 92, gain: 0.11, dur: 0.13, type:"triangle" });
          this._tone (t + 0.06, { freq: 1900, to: 520, gain: 0.05, dur: 0.09, type:"sawtooth" });
        }
      }
      else if (kind === "wall"){'''

SFX_ULT_VOICE_NEW = '''        } else if (w === "vinesower"){         // a bowstring, then a field of it
          /* The cast is not a blast, so it does not sound like one. A woody
             string release, then a rising breath of noise that keeps going --
             the window opening rather than a thing landing. It has to still
             be recognisable UNDER a dozen `vine` plants firing on top of it. */
          this._burst(t, { freq: 420, q: 1.2, gain: 0.16, dur: 0.07, type:"bandpass" });
          this._tone (t, { freq: 196, to: 392, gain: 0.16, dur: 0.55, type:"triangle" });
          this._tone (t + 0.06, { freq: 294, to: 588, gain: 0.10, dur: 0.60, type:"triangle" });
          this._burst(t + 0.10, { freq: 700, q: 0.7, gain: 0.13, dur: 1.10, type:"lowpass" });
          this._burst(t + 0.50, { freq: 2600, q: 0.9, gain: 0.06, dur: 0.70, type:"highpass" });
        } else if (w === "gravemourn"){                 // a drop into the grave'''

ULTFX_LIFE_NEW = '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,
              /* THE THICKET is set from `ult.dur` at the cast site, not here:
                 it is the only ultimate in the game whose set-piece has to
                 stay up for a window whose length is a tuned number. The map
                 entry is the fallback if that is ever missed. */
              vinesower: 5.4,'''

BEAT_GUARD_NEW = """    const _side = (self.shade ? self.shade.owner : self) === this.a ? 0 : 1;
    /* A LASH IS NOT A BEAT. Rick: "the vines shouldnt trigger the director at
       all". `beats` is read by nothing in the simulation and everything in the
       director, so this is the one place a mechanic can be made invisible to
       the CAMERA without being made invisible to the game. `_cineVine` is set
       only around the Thicket's own strike and cleared immediately.

       THE FATAL ONE IS KEPT, and that is a deviation from the sentence rather
       than an oversight. A fight ending on a lash would otherwise carry no
       KILL cut at all and the clip would simply stop; "do not let fifteen
       small hits drive the camera" is a different claim from "do not film the
       finish". How often a lash lands the killing blow is measured in
       vinesower_probe [19] rather than assumed here. */
    if (!this._cineVine || fatal)
    this.beat({ kind: "hit", side: _side, x: hx, y: hy,"""

ULT_SETPIECE_NEW = '''    /* ---- THE THICKET, under --------------------------------------------
       Deliberately SMALL, and for the same reason the Harrowing's is: every
       thing a viewer needs in order to read this ultimate is already a
       simulation object -- seeds leaving instead of arrows, husks on the
       walls, flowers opening, vines lashing. A set-piece competing with a
       dozen plants would be light drawn on top of light.

       What is here is the one thing the sim cannot say by itself: THE WINDOW
       IS OPEN. A ring of green riding the walls, brightest at the start and
       guttering out as the sowing ends, so a viewer can see that the seeds
       are still coming without being told. */
    if (u.w === "%ID%"){
      const dur = Math.max(0.01, u.life - 0.4);
      const k2 = clamp(u.t / dur, 0, 1);
      const n = CONFIG.arena, ins = m.inset;
      c.globalCompositeOperation = "lighter";
      c.globalAlpha = (1 - k2) * 0.30 + 0.06;
      c.strokeStyle = u.aff.glow;
      c.lineWidth = 3 + 5 * (1 - k2);
      c.shadowColor = u.aff.core; c.shadowBlur = 16;
      c.strokeRect(ins + 3, ins + 3, n.w - 2 * ins - 6, n.h - 2 * ins - 6);
      c.shadowBlur = 0;
      /* and the caster wearing it for the first half-second of the window */
      const ex = clamp(u.t / 0.5, 0, 1);
      if (ex < 1){
        c.globalAlpha = (1 - ex) * 0.55;
        c.strokeStyle = u.aff.glow; c.lineWidth = 6 * (1 - ex) + 1;
        c.beginPath();
        c.arc(src.x, src.y, 34 + 170 * (1 - Math.pow(1 - ex, 2.2)), 0, TAU);
        c.stroke();
      }
      c.globalAlpha = 1;
      c.globalCompositeOperation = "source-over";
    }

    /* ---- THE HARROWING, under ------------------------------------------'''


EDITS = [
    ("the relic",
     '''    blurb:"Shards that remember the room. What it has already done to you, it can do again, backwards." },

];''',
     RELIC_NEW),

    ("the match's plant list",
     '''    this.sparks = [];         // Daybreak's drift: SIM objects, they burn and they feed''',
     MATCH_STATE_NEW),

    ("the fighter's sowing window",
     '''    this.ultRadiant = null;   // {t, dur} while Daybreak burns''',
     FIGHTER_STATE_NEW),

    ("spawnShot — a seed is a shot with one flag",
     '''      dmgMul: S.dmgMul === undefined ? 1 : S.dmgMul,
      aff: f.aff, a,
    });''',
     SEED_FLAG_NEW),

    ("tickShots — the seed takes root",
     '''      /* --- spent. No bounce: a ricocheting arrow is chaos the viewer cannot
         attribute to anything, and a miss ending visibly on the wall is what
         makes the miss cost something. */''',
     WALL_STICK_NEW),

    ("plantVine and tickVines",
     '''  tickSparks(dt){''',
     TICK_VINES_NEW),

    ("the tick call",
     '''    this.tickSparks(dt);''',
     TICK_CALL_NEW),

    ("fireUlt — the Thicket sows and resolves nothing",
     '''    if (u.kind === "radiant"){''',
     FIRE_ULT_NEW),

    ("the sowing window burns down",
     '''    if (f.ultRadiant){''',
     WINDOW_NEW),

    ("drawVines",
     '''  drawSparks(m){''',
     DRAW_VINES_NEW),

    ("the plants, drawn under the fighters",
     '''    this.drawDrips(m);''',
     DRAW_CALL_UNDER_NEW),

    ("the lashes, drawn over them",
     '''    this.drawSparks(m);
    this.drawUltName(m);''',
     DRAW_CALL_OVER_NEW + '''
    this.drawUltName(m);'''),

    ("the seed, drawn",
     '''      if (s.spike){''',
     SEED_ART_NEW),

    ("the whip's own voice",
     '''      else if (kind === "wall"){''',
     SFX_VINE_NEW),

    ("the cast's voice",
     '''        } else if (w === "gravemourn"){                 // a drop into the grave''',
     SFX_ULT_VOICE_NEW),

    ("the set-piece's life",
     '''              ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,''',
     ULTFX_LIFE_NEW),

    ("a lash is not a beat",
     '''    const _side = (self.shade ? self.shade.owner : self) === this.a ? 0 : 1;
    this.beat({ kind: "hit", side: _side, x: hx, y: hy,''',
     BEAT_GUARD_NEW),

    ("the set-piece",
     '''    /* ---- THE HARROWING, under ------------------------------------------''',
     ULT_SETPIECE_NEW),
]


def one(src: str, old: str, new: str, label: str) -> str:
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-foregone.html")
    ap.add_argument("--out", default="../02-chain/sc-vinesower.html")
    ap.add_argument("--dmg", type=float, default=TUNED_QS)
    for k, v in ULT.items():
        ap.add_argument(f"--{k.lower()}", type=float, default=v)
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nVINESOWER BUILD -- the verdant bow and the Thicket")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if '"retrace"' not in s0:
        raise SystemExit("this source has no retrace -- build off sc-foregone or later")
    if '"seedfall"' in s0:
        raise SystemExit("this source already has a seedfall -- already built")

    subs = {"%ID%": RELIC_ID, "%NAME%": RELIC_NAME, "%ULT%": ULT_NAME,
            "%DMG%": f"{A.dmg:g}"}
    for k in ULT:
        subs["%" + k.upper() + "%"] = f"{getattr(A, k.lower()):g}"
    subs["%SEEDTIP%"] = f"{A.seeds:g}"

    for label, old, new in EDITS:
        for k, v in subs.items():
            new = new.replace(k, v)
        s = one(s, old, new, label)

    for k in subs:
        if k in s:
            raise SystemExit(f"unsubstituted placeholder left in the build: {k}")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print(f"\n  NEXT, and none of it is optional:")
    print(f"    python3 vinesower_probe.py --game {A.out}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --n 10")
    print(f"    python3 verify.py --game {A.out} --n 40")
    print(f"    python3 frame_build.py --src {A.out} --out ../02-chain/sc-vinesower-frame.html")
    print(f"    python3 chain_audit.py --relic {A.out} --tip ../02-chain/sc-vinesower-frame.html\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
