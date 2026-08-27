#!/usr/bin/env python3
"""SLAGBURST — Emberedge's ultimate, redesigned. Third of the big ults.

    python3 ultember_build.py --src sc-daybreak.html --out sc-ember.html

Rick's interview, 2026-08-15, three answers:

    fantasy   "The Detonation — set off Sunder"
    budget    "Strictly sideways — same power, new spectacle"
    Sunder    "Detonator — consume stacks for burst"

He picked the detonation over my flagged objection that it is the Crucible's
move pointed outward. Fair — so differentiating it is this builder's problem,
and the answer is below under WHY THIS IS NOT THE CRUCIBLE.

WHY THIS RELIC, WHY THIS SHAPE
------------------------------
Emberedge is NOT weak. Measured at 48.9% across two disjoint seed sets
(0.2pp swing, the most stable relic in the game) — dead mid-field. The v23
note's floor (Farwarden ~46) was noise from `verify.py --n 60`; see
`sundered-crown-weakest-probe.md`. So this redesign buys spectacle, not
winrate, and the blade repays whatever the new ult turns out to be worth.

Old Forgefall was `kind:"nova"` — 17 damage, 4 Sunder, knock 180 — one of
FIVE novas in a sixteen-relic roster, and worth +5.4pp, fourth-weakest ult
in the game. Retiring it kills the most repetition available anywhere.

THE MEASUREMENT THAT SHAPED THE DESIGN
--------------------------------------
`sunder_probe.py` instrumented fireUlt across the whole field, 1893 Emberedge
casts. Sunder on the foe at cast:

    0 stacks 26.3%   1: 17.4%   2: 13.2%   3: 10.9%
    4: 10.9%   5: 6.6%   6: 14.7%        mean 2.42, median 2

**A quarter of all casts happen at zero stacks.** A literal "detonate what is
on the foe" ultimate is a dud one time in four — which is not "bigger and
flashier", it is a coin flip with a set-piece attached. (Grudgebearer is worse
still at 42.2% zero, but the Crucible survives it: its Sunder is a crit
MULTIPLIER on a strike that lands regardless. A detonation has no such floor.)

The fix was already written in the relic's own blurb:

    "Quenched once and never since. It does not cut so much as split."

So the cast SPLITS THE SHELL FIRST. It drives `split` Sunder into the foe as
its opening move, and then ignites everything — banked and fresh together.
The floor becomes 3, the ceiling stays 9, and the ultimate can never fizzle
for want of fuel. The stacks the wielder banked by fighting still pay: the
detonation counts `banked + split` UNCAPPED, so six banked stacks is a nine
stack burst even though the status bar caps at six.

WHY THIS IS NOT THE CRUCIBLE
----------------------------
Same resource, opposite direction, and every axis inverted:

    Crucible    18s · a PROMISE · needs a melee connect · converts stacks to
                crit chance and crit multiplier on ONE strike · rewards
                patience · a whiff keeps the stacks and wastes the cast
    Slagburst   14s · a COMMITMENT · needs no connect at all · manufactures
                its own fuel then spends it instantly for flat burst and
                knockback · rewards pressure · a whiff is impossible but the
                fuse can be cut short by dying

Grudgebearer hoards Sunder and spends it on a promise. Emberedge makes Sunder
and spends it on the spot. Two dwarves, one currency, no overlap in play.

ENGINE SHAPE
------------
`kind:"detonate"`, a THIRD state shape — not the forge's gated promise and not
Daybreak's window, but a fuse:

  cast        in range only (radius, the nova's own rule kept). Applies
              `split` Sunder, lights `f.ultSlag = {t, fuse, ...}`, resolves
              NO damage. The name banners on the TARGET — the thing that is
              about to go off is the foe, not the wielder.
  fuse        `fuse` seconds. The foe keeps moving and keeps fighting; the
              cracks travel with it because the art is drawn on the LIVE
              target, not on a position stamped at cast. Nothing is stunned:
              the Crucible owns freeze, and a second stun-lock ultimate would
              make two of sixteen relics the same relic.
  detonation  reads `n = banked + split`, CLEARS Sunder, then prices the
              damage. Clearing first is deliberate — a detonation whose
              damage is also multiplied by the stacks it just ate would be
              paying itself twice and the curve would go exponential at 9.

  dropped     foe dead, wielder dead, or match over during the fuse -> the
              state clears and nothing resolves. The wielder can be killed
              off its own detonation; that risk is what the guaranteed floor
              is bought with.

The charge is owed from the CAST, not the detonation — the fuse is 0.55s and
gating it would quietly make the cooldown 14.55s while the card said 14.

WHAT THE VIEWER LEARNS BY WATCHING
----------------------------------
The burst throws ONE SHARD PER CONSUMED STACK. The spectacle is not decorated
with the mechanic, it IS the mechanic: a 3-stack Slagburst throws three
shards and a 9-stack throws nine, and the shake, the ring and the flash all
scale on the same n. Nobody has to be told that banking stacks matters.

Zero simulation rng is added anywhere. Shard directions, tumble and scatter
are `shellHash` of (n, i) — the same pure hash the shell fracture uses — so
`engine_ab` over the other fifteen relics is bit-identical and the offline
render matches the live page frame for frame.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# ---------------------------------------------------------------- data ----

TIP = "Splits the shell for 3 Sunder, then blows every stack at once"

# Every Slagburst number lives here. A generated file is not a place to store
# a number — the law, unchanged.
DATA = dict(
    charge=14,      # unchanged from Forgefall: the cadence was never the problem
    radius=230,     # Forgefall's 220, opened slightly — the payoff now has to
                    # survive a 0.55s fuse, so the entry price moved a little
    split=3,        # the floor. 26.3% of casts see zero banked stacks.
    fuse=0.55,      # long enough to read as a tell, short enough that the foe
                    # cannot reliably kill the wielder to cancel it
    dmgBase=6,      # what a 0-banked cast is worth beyond its own split
    dmgPer=5.5,     # per consumed stack, n = banked + split, range 3..9
    knockBase=110,
    knockPer=34,    # 3 stacks -> 212, 9 stacks -> 416: the throw IS the read
)

# THE BLADE IS NOT REPAID, AND THAT IS THE MEASUREMENT, NOT AN OMISSION.
#
# Rick chose STRICTLY SIDEWAYS: measure the new ult and give back exactly the
# difference. Measured — 260 shared seeds x Emberedge's 15 pairings = 3900
# games, the SAME seed list the old build was measured on, so this is a paired
# test and not two independent estimates:
#
#     Forgefall  48.46%      Slagburst  48.08%      delta -0.38pp
#     discordant 519 lost / 504 won      McNemar z = -0.47
#
# Sideways to within half a point of noise at the blade it already had. The
# per-opponent texture moved a lot (Goreshard -6.9pp, Farwarden +4.6pp) while
# the aggregate did not, which is the good version of this outcome: the relic
# plays differently against different foes without moving the field.
#
# Repaying a blade to correct a -0.38pp drift would be tuning against noise.
TUNED_EM = 12.32     # unchanged from Forgefall — measured, not assumed

ULT_OLD = ('ult:{ name:"Forgefall", charge:14, kind:"nova", radius:220, '
           'dmg:17, apply:{sunder:4}, knock:180, '
           'tip:"Nova: 17 damage, 4 Sunder, short knockback" },')

ULT_NEW = (
    'ult:{{ name:"Slagburst", charge:{charge}, kind:"detonate", '
    'radius:{radius},\n'
    '           split:{split}, fuse:{fuse}, dmgBase:{dmgBase}, '
    'dmgPer:{dmgPer},\n'
    '           knockBase:{knockBase}, knockPer:{knockPer},\n'
    '           tip:"{tip}" }},'
).format(tip=TIP, **DATA)

BLURB_OLD = ('blurb:"Quenched once and never since. It does not cut so much '
             'as split." }')
BLURB_NEW = ('blurb:"Quenched once and never since. It does not cut so much '
             'as split — and what it splits, it lights." }')

# ------------------------------------------------------ engine: state ----

STATE_OLD = """    this.ultRadiant = null;   // {t, dur} while Daybreak burns"""
STATE_NEW = """    this.ultRadiant = null;   // {t, dur} while Daybreak burns
    this.ultSlag = null;      // {t, fuse, split} while a Slagburst fuse burns"""

TICK_OLD = """      f.ultRadiant.t += dt;
      if (f.ultRadiant.t >= f.ultRadiant.dur) f.ultRadiant = null;
    }"""
TICK_NEW = """      f.ultRadiant.t += dt;
      if (f.ultRadiant.t >= f.ultRadiant.dur) f.ultRadiant = null;
    }
    if (f.ultSlag){
      /* THE FUSE. Everything the split lit is now burning down on the foe,
         and the foe is still moving and still swinging — nothing here stuns
         it. The Crucible owns freeze; a second hold would make two of the
         sixteen the same relic.

         The wielder is NOT protected either. Die during these 0.55 seconds
         and the detonation never comes: `checkEnd` sets over, this drops the
         state, and the cast is spent. That is the price of a payoff that can
         never fizzle for want of stacks. */
      const S = f.ultSlag;
      S.t += dt;
      if (!foe.alive || !f.alive || this.over){ f.ultSlag = null; }
      else if (S.t >= S.fuse){
        f.ultSlag = null;
        this.detonate(f, foe, S.over);
      }
    }"""

# ----------------------------------------------------- engine: resolve ----

BANNER_OLD = """    const onTarget = { thornwake:1, spellbreaker:1 }[f.w.id];"""
BANNER_NEW = """    const onTarget = { thornwake:1, spellbreaker:1, emberedge:1 }[f.w.id];"""

FIRE_OLD = """    if (u.kind === "radiant"){"""
FIRE_NEW = """    /* SLAGBURST RESOLVES NOTHING HERE. It splits, and then it waits.

       The split is the whole reason this ultimate works: measured over 1893
       casts, 26.3% of them find ZERO Sunder on the foe, so a detonation of
       "whatever is there" is a dud one time in four. The cast drives its own
       `split` stacks into the shell first, which makes 3 the floor and keeps
       9 the ceiling for a wielder who has been fighting. */
    if (u.kind === "detonate"){
      if (!inRange){
        /* Out of range: the nova's own rule, kept. Nothing splits, nothing
           lights, and the set-piece says so rather than playing a burst that
           did not happen. */
        this.ultFx.phase = "cold";
        this.ultFx.life = 0.55;
        return;
      }
      /* THE OVERFLOW, and why it lives on the fuse state and not on the foe.
         `apply` caps at maxStacks 6, so a foe already sitting on five banked
         stacks would silently lose two of the three the split drives in, and
         a wielder who had been fighting hardest would be punished for it.
         The remainder is carried on the state object the fuse already owns —
         which means a fuse that gets dropped (either fighter dies) takes its
         bookkeeping with it. A counter parked on the foe would survive the
         drop and inflate the NEXT Slagburst by a stale amount. */
      const before = foe.stacks("sunder");
      foe.apply("sunder", u.split);
      const over = before + u.split - foe.stacks("sunder");
      const firstTeach = !this.taught.sunder && !!(STATUS.sunder && STATUS.sunder.tip);
      if (firstTeach) this.taught.sunder = true;
      this.statusTag(foe.x, foe.y, "sunder", firstTeach);
      f.ultSlag = { t: 0, fuse: u.fuse, split: u.split, over };
      this.ultFx.phase = "fuse";
      /* THE FX CLOCK RUNS AT 2x SIM TIME. Measured, after the filmstrip
         showed a dead frame at 0.58s — no ring, no cracks, and the burst
         still to come. `ultFx.t` is advanced by BOTH decay paths, so a
         `life` of 0.9 is 0.45 seconds of match time, not 0.9. Every `life`
         number in this engine is in half-seconds and always has been; the
         1.3-2.6 table above reads as 0.65-1.3s on screen.

         So the tell needs (fuse + the cast's own hit-stop) x 2 = 1.26 to
         reach its own detonation, plus margin. Nothing else in this file
         needs converting: the burst's art constants were authored against
         the filmstrip, which means they were authored in fx units already. */
      this.ultFx.life = u.fuse * 2 + 0.45;
      /* The fuse draws the TRUE count, not the capped one, so the cracks the
         viewer counts during the tell equal the shards the burst throws. */
      this.ultFx.n = foe.stacks("sunder") + over;
      return;
    }

    if (u.kind === "radiant"){"""

DETONATE = """
  /* ------------------------------------------------------------ SLAGBURST --
     The fuse reaches the powder. Called only from tickCharge, only with both
     fighters alive, and it is the ONLY place a detonate ult resolves. */
  detonate(f, foe, over){
    const u = f.w.ult;
    /* `banked` is what is on the shell right now — the split the cast drove
       in, plus anything the wielder landed during the fuse itself, which is
       a real and deliberate reward for keeping the pressure on while it
       burns. `over` is the part the status cap swallowed. The count runs
       UNCAPPED past the ceiling of six, because the bar capping is a display
       rule and this is an arithmetic one: a wielder who arrived with six
       banked stacks blew a nine-stack charge and the screen owes it nine
       shards. */
    const n = foe.stacks("sunder") + (over || 0);
    /* CONSUMED, then priced. Not the other way round. A detonation whose
       damage is also multiplied by dmgTakenMul's share of the stacks it just
       ate would pay itself twice, and at nine stacks the curve leaves the
       building. The stacks are FUEL here, not a debuff being cashed. */
    delete foe.status.sunder;
    const raw = u.dmgBase + u.dmgPer * n;
    const dmg = Math.round(raw * this.actMods.dmg * foe.dmgTakenMul());
    this.hurt(foe, dmg, f);
    foe.flash = 1;
    foe.ringFlash = 1;
    f.dealt += dmg;
    this.float(foe.x, foe.y - 40, dmg, "#FFD08A", 46 + n * 2);
    this.spawnFx(foe.x, foe.y, "#FFB863", 30 + n * 4, 300 + n * 26, 0.8, 5);
    this.ring(foe.x, foe.y, "#E8761A", 7, 150 + n * 16, 0.5, 5);
    /* The throw scales on the same n as everything else, so "that one was
       big" and "that one threw it into the wall" are the same sentence. */
    const dx = foe.x - f.x, dy = foe.y - f.y, dl = Math.hypot(dx, dy) || 1;
    const k = u.knockBase + u.knockPer * n;
    foe.vx += (dx / dl) * k; foe.vy += (dy / dl) * k;
    this.shake = Math.max(this.shake, 26 + n * 3.4);
    this.hitStop = Math.max(this.hitStop, 0.06 + n * 0.008);
    SFX.play("ult", { w: "emberedge-burst", n });
    /* The burst is its own set-piece, stamped where the shell actually was.
       ONE SHARD PER CONSUMED STACK — the count is the mechanic, on screen. */
    this.ultFx = { w: f.w.id, kind: "detonate", phase: "burst",
                   src: f === this.a ? "a" : "b", tgt: f === this.a ? "b" : "a",
                   x: foe.x, y: foe.y, tx: foe.x, ty: foe.y, hit: true,
                   radius: u.radius || 230, aff: f.aff, t: 0, n,
                   life: 1.45 };
    this.beat({ kind: "ult", side: f === this.a ? 0 : 1, x: foe.x, y: foe.y,
                w: f.w.id, foeHpFrac: foe.hp / foe.maxHp });
  }
"""

DETONATE_ANCHOR = """  checkEnd(){"""

# ------------------------------------------------------------ sfx ----

SFX_ANCHOR = """        } else if (w === "thornwake"){                  // creak and cinch"""
SFX_NEW = """        } else if (w === "emberedge"){                  // the shell splits open
          /* Dry, high, and SHORT — this is a tell, not an event. It has to
             leave room for the burst 0.55s later or the ear hears one long
             noise instead of a fuse and a bang. */
          this._burst(t, { freq: 2600, q: 1.8, gain: 0.20, dur: 0.10, type:"highpass" });
          this._tone (t, { freq: 90, to: 260, gain: 0.16, dur: 0.52, type:"sawtooth" });
          this._burst(t + 0.14, { freq: 1500, q: 2.4, gain: 0.09, dur: 0.34, type:"bandpass" });
        } else if (w === "emberedge-burst"){            // and it goes
          /* Scaled by stack count like everything else in this ultimate: a
             three-stack burst is a crack, a nine-stack burst is a shell going
             off. `n` arrives on the play options. */
          const n = Math.max(3, Math.min(9, p.n || 3)), g = 0.30 + n * 0.035;
          this._tone (t, { freq: 220 + n * 14, to: 30, gain: g, dur: 0.55 + n * 0.03, type:"sine" });
          this._burst(t, { freq: 300, q: 0.5, gain: g * 0.9, dur: 0.45, type:"lowpass" });
          this._burst(t + 0.02, { freq: 5200, q: 0.7, gain: 0.12 + n * 0.016, dur: 0.22, type:"highpass" });
          this._tone (t + 0.06, { freq: 620, to: 140, gain: 0.12, dur: 0.30, type:"sawtooth" });
        } else if (w === "thornwake"){                  // creak and cinch"""

# ------------------------------------------------------------ art ----

ART_UNDER = r"""    else if (u.w === "emberedge"){
      /* SLAGBURST, on the floor. Two phases and a cold one.

         The fuse draws under the LIVE target because the foe keeps moving
         while it burns — a pool stamped at the cast position would leave the
         thing that is about to explode standing somewhere else. */
      if (u.phase === "fuse"){
        const k = clamp(u.t / Math.max(0.001, u.life), 0, 1);
        const heat = k * k;                       // slow, then all at once
        const R = 30 + 26 * heat;
        c.globalAlpha = 0.5 + 0.35 * heat;
        const g = c.createRadialGradient(tgt.x, tgt.y, 3, tgt.x, tgt.y, R);
        g.addColorStop(0, "#FFD08A" + (heat > 0.6 ? "CC" : "77"));
        g.addColorStop(0.5, "#B4491A55"); g.addColorStop(1, "#8A2E0E00");
        c.fillStyle = g;
        c.beginPath(); c.arc(tgt.x, tgt.y, R, 0, TAU); c.fill();
      }
      else if (u.phase === "burst"){
        /* Slag on the floor where the shell went. It cools from white to
           crust over the whole life — the only thing still moving after the
           first third, which is what says "this was molten a second ago". */
        const ex = clamp(u.t / 0.20, 0, 1);
        const cool = clamp((u.t - 0.18) / 0.8, 0, 1);
        const fade = 1 - clamp((u.t - 0.55) / 0.6, 0, 1);
        const R = (110 + (u.n || 3) * 13) * (1 - Math.pow(1 - ex, 2.5));
        c.globalAlpha = 0.6 * fade;
        const g = c.createRadialGradient(u.x, u.y, 4, u.x, u.y, Math.max(1, R));
        const hot = cool > 0.6 ? "#3A1A08" : (cool > 0.25 ? "#B4491A" : "#FFE7BE");
        g.addColorStop(0, hot + "DD"); g.addColorStop(0.30, "#8A2E0E66");
        g.addColorStop(0.62, "#8A2E0E1A"); g.addColorStop(1, "#8A2E0E00");
        c.fillStyle = g;
        c.beginPath(); c.arc(u.x, u.y, Math.max(1, R), 0, TAU); c.fill();
        /* One crust fissure per consumed stack. Same count as the shards
           above — the floor and the air are telling the viewer the same
           number, which is how a rule gets learned without a caption. */
        for (let i = 0; i < (u.n || 3); i++){
          const a = shellHash(61, i) * TAU;
          c.globalAlpha = 0.6 * fade * cool;
          c.strokeStyle = "#25120A"; c.lineWidth = 3.4;
          this._jag(c, u.x, u.y, u.x + Math.cos(a) * R, u.y + Math.sin(a) * R,
                    6, 12, 610 + i, 1);
        }
      }
      else if (u.phase === "cold"){
        /* Out of range. A puff of heat that dies where the wielder stands —
           the honest picture of an ultimate that found nothing to split. */
        const out = 1 - clamp(u.t / 0.55, 0, 1);
        c.globalAlpha = 0.35 * out;
        const g = c.createRadialGradient(src.x, src.y, 2, src.x, src.y, 60);
        g.addColorStop(0, "#8A2E0E88"); g.addColorStop(1, "#8A2E0E00");
        c.fillStyle = g;
        c.beginPath(); c.arc(src.x, src.y, 60, 0, TAU); c.fill();
      }
    }"""

ART_OVER = r"""    /* ---- Slagburst: the shell splits, glows, and goes ---------------------- */
    else if (u.w === "emberedge"){
      if (u.phase === "fuse"){
        /* THE TELL, and it is drawn ON THE FOE. Every other ultimate in the
           game announces itself on the wielder; this one lights up the thing
           it is about to destroy, which is the only honest place for it —
           the damage is already committed and it is committed to that ball.

           An IMPLODING ring, not an expanding one. Five of sixteen relics
           threw an expanding nova ring; running it inward is the cheapest
           possible way to say "this is not one of those". */
        const k = clamp(u.t / Math.max(0.001, u.life), 0, 1);
        const heat = k * k;
        const cracks = Math.max(3, u.n || 3);
        c.save();
        c.globalCompositeOperation = "lighter";
        /* SIZED FOR A PHONE, NOT FOR A PIXEL DIFF. The first version drew
           these at 20-36px with a 1.6px stroke and passed every automated
           check; on the filmstrip at 390px wide they did not exist. The
           ball is 34px in radius, so a crack that is going to read as a
           crack has to be roughly the ball again, not a third of it. */
        c.restore();                       // the dark pass is NOT additive
        for (let i = 0; i < cracks; i++){
          const a = shellHash(77, i) * TAU;
          const len = (34 + shellHash(78, i) * 30) * (0.55 + 0.45 * heat);
          const x1 = tgt.x + Math.cos(a) * len, y1 = tgt.y + Math.sin(a) * len;
          /* underlay first: a lit crack on a lit ball is invisible without
             something dark behind it */
          c.globalAlpha = (0.5 + 0.4 * heat);
          c.strokeStyle = "#1C0C05"; c.lineWidth = 6 + 7 * heat;
          this._jag(c, tgt.x, tgt.y, x1, y1, 4, 6, 770 + i, 1);
        }
        c.save();
        c.globalCompositeOperation = "lighter";
        for (let i = 0; i < cracks; i++){
          const a = shellHash(77, i) * TAU;
          const len = (34 + shellHash(78, i) * 30) * (0.55 + 0.45 * heat);
          const x1 = tgt.x + Math.cos(a) * len, y1 = tgt.y + Math.sin(a) * len;
          c.globalAlpha = 0.45 + 0.55 * heat;
          c.strokeStyle = heat > 0.72 ? "#FFF6E2"
                        : (heat > 0.34 ? "#FFD08A" : "#FF8C3A");
          c.lineWidth = 3 + 5 * heat;
          c.shadowColor = "#FF6A1A"; c.shadowBlur = 10 + 16 * heat;
          this._jag(c, tgt.x, tgt.y, x1, y1, 4, 6, 770 + i, 1);
        }
        c.shadowBlur = 0;
        /* the ring closing in — an IMPLOSION, the one shape no nova makes */
        const rIn = 104 * (1 - heat) + 26;
        c.globalAlpha = 0.40 + 0.5 * heat;
        c.strokeStyle = "#FFB863"; c.lineWidth = 2.6 + 3.6 * heat;
        c.shadowColor = "#E8761A"; c.shadowBlur = 12;
        c.beginPath(); c.arc(tgt.x, tgt.y, rIn, 0, TAU); c.stroke();
        c.shadowBlur = 0;
        c.restore();
      }

      else if (u.phase === "burst"){
        const n = u.n || 3;
        const fade = 1 - clamp((u.t - 0.80) / 0.6, 0, 1);
        c.save();
        c.globalCompositeOperation = "lighter";
        /* The flash was 0.14s at 0.85 alpha over a radius that grew with n,
           which meant the bigger the burst the more completely it erased its
           own shards during the exact frames they were closest together and
           most countable. Shorter and dimmer; the shards are the event. */
        const flash = 1 - clamp(u.t / 0.10, 0, 1);
        if (flash > 0){                              // the shell goes
          c.globalAlpha = flash * 0.55;
          const R = 78 + n * 8;
          const g = c.createRadialGradient(u.x, u.y, 2, u.x, u.y, R);
          g.addColorStop(0, "#FFFFFF"); g.addColorStop(0.22, "#FFE7BE99");
          g.addColorStop(0.55, "#E8761A55"); g.addColorStop(1, "#E8761A00");
          c.fillStyle = g;
          c.beginPath(); c.arc(u.x, u.y, R, 0, TAU); c.fill();
        }
        /* ONE SHARD PER CONSUMED STACK. This is the mechanic, drawn. They
           are born fast and die in about a second — shrapnel, not Daybreak's
           drifting collectible field. Nothing here is a sim object and
           nothing here draws rng: direction, speed and tumble are shellHash
           of (n, i), so the offline render and the live page agree. */
        /* THE SHARDS ARE THE MECHANIC, SO THEY GET A MODEL.
           v1 drew them at 7-14px long and 2.4-4.6px wide, born at 300-560,
           dead by 0.85s. Every assert passed and the filmstrip settled it:
           at 390px wide a nine-stack burst and a three-stack burst were the
           same picture. Same lesson Daybreak's dot-sparks taught, learned
           twice. They are now roughly the ball's own radius long, born
           slower so they stay on screen, carried to 1.25s, and each one is
           drawn dark-first so it has an edge against both the flash behind
           it and the dark hall it flies into. Counting them is the point;
           if they cannot be counted the ultimate does not explain itself. */
        for (let i = 0; i < n; i++){
          const a = (i / n) * TAU + shellHash(81, i) * 0.55;
          const sp = 210 + shellHash(82, i) * 150;
          const q = clamp(u.t / 1.25, 0, 1);
          const d = sp * u.t * (1 - q * 0.5);
          const x = u.x + Math.cos(a) * d, y = u.y + Math.sin(a) * d;
          const rot = a + u.t * (4 + shellHash(83, i) * 5);
          const life = 1 - q;
          if (life <= 0) continue;
          const L = (26 + shellHash(84, i) * 20) * (0.5 + 0.5 * life);
          const W = (7 + shellHash(85, i) * 5) * (0.5 + 0.5 * life);
          if (q < 0.55){                            // the streak it tears
            c.globalAlpha = life * fade * 0.55;
            c.strokeStyle = "#FFD08A"; c.lineWidth = (3 + 3 * life);
            c.beginPath();
            c.moveTo(x, y);
            c.lineTo(x - Math.cos(a) * 44 * life, y - Math.sin(a) * 44 * life);
            c.stroke();
          }
          c.save();
          c.translate(x, y); c.rotate(rot);
          c.beginPath();                            // a splinter, not a dot
          c.moveTo(L, 0); c.lineTo(0, W); c.lineTo(-L * 0.55, 0); c.lineTo(0, -W);
          c.closePath();
          /* dark body, hot core: readable on the flash AND on the hall */
          c.globalAlpha = life * fade;
          c.fillStyle = "#2A1207";
          c.fill();
          c.shadowColor = "#FF6A1A"; c.shadowBlur = 16 * life;
          c.fillStyle = q < 0.30 ? "#FFF6E2" : (q < 0.66 ? "#FFB863" : "#B4491A");
          c.beginPath();
          c.moveTo(L * 0.78, 0); c.lineTo(0, W * 0.55);
          c.lineTo(-L * 0.4, 0); c.lineTo(0, -W * 0.55);
          c.closePath(); c.fill();
          c.shadowBlur = 0;
          c.restore();
        }
        c.restore();
        /* the shockwave, sized on n */
        const ex = clamp(u.t / 0.34, 0, 1);
        c.globalAlpha = fade * (1 - ex) * 0.9;
        c.strokeStyle = "#FFB863"; c.lineWidth = 5 * (1 - ex) + 1;
        c.shadowColor = "#E8761A"; c.shadowBlur = 16;
        c.beginPath();
        c.arc(u.x, u.y, (120 + n * 16) * (1 - Math.pow(1 - ex, 2.5)), 0, TAU);
        c.stroke();
        c.shadowBlur = 0;
      }
    }"""


# ---------------------------------------------------------------- edit ----

def one(src, old, new, label):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"anchor {label!r} matched {n} times, expected 1")
    return src.replace(old, new, 1)


def replace_block(src, marker, new, which, label):
    """Replace the `which`-th brace-matched block starting at `marker`."""
    starts = [m.start() for m in re.finditer(re.escape(marker), src)]
    if len(starts) != 2:
        raise SystemExit(f"{label}: found {len(starts)} occurrences of the "
                         f"emberedge art marker, expected 2")
    s = starts[which]
    i = src.index("{", s + len(marker) - 1)
    d = 0
    j = i
    while j < len(src):
        if src[j] == "{":
            d += 1
        elif src[j] == "}":
            d -= 1
            if d == 0:
                break
        j += 1
    return src[:s] + new.lstrip("\n") + src[j + 1:]


def build(src_path, out_path, blade):
    src = src_path.read_text(encoding="utf-8")

    ult_new = ULT_NEW
    src = one(src, ULT_OLD, ult_new, "ult data")
    src = one(src, BLURB_OLD, BLURB_NEW, "blurb")
    src = one(src, STATE_OLD, STATE_NEW, "fighter state")
    src = one(src, TICK_OLD, TICK_NEW, "tickCharge")
    src = one(src, BANNER_OLD, BANNER_NEW, "banner onTarget")
    src = one(src, FIRE_OLD, FIRE_NEW, "fireUlt branch")
    src = one(src, DETONATE_ANCHOR, DETONATE.lstrip("\n") + "\n" + DETONATE_ANCHOR,
              "detonate method")
    src = one(src, SFX_ANCHOR, SFX_NEW, "sfx")

    # blade
    dmg_old = ('blades:[0], reach:116, width:14, artW:40, dmg:12.32, spin:3.4, '
               'mode:"swing", arc:1.5, mass:3.0,')
    dmg_new = (f'blades:[0], reach:116, width:14, artW:40, dmg:{blade}, '
               'spin:3.4, mode:"swing", arc:1.5, mass:3.0,')
    src = one(src, dmg_old, dmg_new, "emberedge blade")

    # art: two brace-matched blocks, under first then over
    marker = 'else if (u.w === "emberedge"){'
    src = replace_block(src, marker, ART_UNDER, 0, "drawUltUnder")
    src = replace_block(src, marker, ART_OVER, 1, "drawUltOver")

    # the ultFx life table entry is now overridden per phase; leave it as the
    # fallback for any path that forgets to set one.
    out_path.write_text(src, encoding="utf-8", newline="\n")
    h = hashlib.sha256(src.encode()).hexdigest()[:16]
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="sc-daybreak.html")
    ap.add_argument("--out", default="sc-ember.html")
    ap.add_argument("--blade", type=float, default=TUNED_EM)
    a = ap.parse_args()

    sp = (HERE / a.src) if not pathlib.Path(a.src).is_absolute() else pathlib.Path(a.src)
    if not sp.exists():
        sp = HERE.parent / "02-chain" / a.src
    op = (HERE.parent / "02-chain" / a.out) if "/" not in a.out else pathlib.Path(a.out)
    if op.name == PROTECTED:
        raise SystemExit("refusing to write the shipped file")

    h = build(sp, op, a.blade)
    print(f"{sp.name} -> {op}  sha256 {h}  blade {a.blade}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
