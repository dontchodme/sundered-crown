# LASTLIGHT — the sanctified scythe, and THE HARROWING

**2026-08-17/18.** The eighteenth relic, and the first free cell of the
6 x 7 grid to be filled since the four greatswords. Built off
`02-chain/sc-cardspin.html` `ec9b8d753235385d`, one builder, one anchor set.

```
02-chain/sc-lastlight.html      32a1a7bad61659df     <-- NEW CHAIN TIP CANDIDATE
  tools/lastlight_build.py      every tuned number lives here
  tools/harrow_probe.py         22 checks, all green
  tools/lastlight_sweep.py      the blade, narrowed against the field
  tools/whitescythe_probe.py    the look-first probe, written before the build
```

`01-live/sundered-crown.html` `51c9bf566f9eb679` **untouched.**

---

# 0. THE CELL, AND WHY IT WAS THE CHEAPEST ONE ON THE BOARD

Rick: *"lets start on our next fighter. im thinking the white scythe."*

Sanctified is the only white school in the game — `steel:#FFFFFF`,
`glow:#FFFFFF`, `core:#FFF6E2` — so "the white scythe" resolves to exactly one
cell, and that cell already had finished art: `SHAPES.scythe` dispatches
`p.key === "sanctified"` to `_scRadiant`, a halo arc standing off the back of
the crescent with a pierced spine, drawn and approved with no relic wearing it.

`whitescythe_probe.py` was written and run **before any design work**: it
injects a provisional relic at runtime, proves the branch actually fires
(`_scRadiant`, not the `_scBase` fallback), proves the cell fights, and writes
nothing to any build. Two things it caught that would otherwise have been
discovered later:

- **`WEAPON_BY_ID` is not on the `AC` surface.** Pushing onto `AC.WEAPONS`
  gets a relic the roster can see and `new AC.Match()` cannot construct
  ("Unknown relic id"). The reachable runtime injection is to overwrite an
  existing relic OBJECT in place, since the map and the array hold the same
  reference. Worth knowing for every future look-first probe.
- **The same-affinity smudge is real here.** Sanctified already has three
  relics, and against Dawnbringer both balls are the same white sphere with
  the same orange rim. v28 §2 made this a selection rule for shorts; this
  relic makes the sanctified column the worst offender in the game.

---

# 1. THE DESIGN, IN RICK'S WORDS

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

Interview answers: miss case **"bounce twice then expire"** · the fuse **one
bloom, all at once** (not a rolling crackle) · name **Lastlight**.

Two calls made without asking, both flagged at the time: the burden is
**physics, not a status** (§3), and the sparks are **Daybreak's own function**,
not a copy of it. The ultimate's name, **Harrowing**, was chosen and is a
one-string change if Rick wants another.

## Nothing in this game spends Smite — and this relic does not fix that

`STATUS.smite` and `STATUS.hemorrhage` are byte-identical: `maxStacks:4,
dur:3.2, dps:1.5`, the same three numbers. All four sanctified surfaces
(Dawnbringer, Aureole and Censer on hit, Consecration on cast) are appliers.
The school is four taps and no drain, where dwarven has a builder
(Slagheart, +2), a spender (the Crucible) and a detonator (Slagburst) — which
is most of why that column reads as a school rather than as a colour.

**The Harrowing spends BLADES, not Smite.** It gives sanctified a second verb,
not the missing one. Recorded here so nobody later reads this relic as having
paid that debt.

---

# 2. WHAT IT IS, MECHANICALLY

`kind:"harrow"`, and every piece of it is an object the engine already had —
the blades are `shots` (clankable, bouncing, missable, drawn by the same
loop), the fuse is Slagburst's, the sparks are Daybreak's. Nothing here is a
second implementation of anything.

```
cast          12 blades, evenly spaced off the WEAPON'S OWN FACING with
              deterministic shellHash jitter (never this.rng() — a relic not
              in the match must not perturb the draw order of one that is),
              speed 430 +-14%, radius 14, armed 0.10s, bounce 2, life 2.2s.
              No damage. No banner: the name goes on the bloom.
land          resolveHit at 4.5 — a real hit, with crit, damage jitter, the
              Sunder multiplier, hit stop, DR hitstun, self.hits++ and the
              relic's own Smite. THEN it sticks, at the angle it arrived on.
burden        per blade: -5% move (moveMul) and +0.45 fall mass (move()).
              Never clank mass. Countable on screen, uncleansable, unbounded.
fuse          2.4s, ONE clock, on the caster. life 2.2 < fuse 2.4 BY
              CONSTRUCTION, so nothing of a cast is airborne when it blows:
              every blade has stuck or expired and there is no third case.
bloom         n = what stuck. dmg 5 + 8n · knock 120 + 130n · stun floor
              0.10 + 0.075n ON TOP of ordinary DR hitstun · hit stop
              0.05 + 0.014n · shake 24 + 4.5n · launch ceiling raised at n>=3
              · 2 sparks per blade. Banner lands here.
dud           n = 0 bursts for nothing, plays `phase:"cold"`, its own sound
              and its own log line. Kept and made visible, not designed away.
```

Charge 15s. Blade **17.5** (§4).

---

# 3. THE BURDEN IS PHYSICS, AND THAT IS A RULE NOT A PREFERENCE

"Weighing it down and impeding its movement" is Entangle's effect, and
Entangle belongs to **verdant**. `roster-expansion.md` §5.8: a relic that
wants a status its school does not have is either in the wrong school or the
taxonomy is wrong. Lastlight is sanctified, so what it does is nail four
inches of blade into you — mass and drag on the ball, not a spell on it.

```
moveMul()   Math.max(0.45, 1 + entangle.move * stacks - burden * burdenMove)
move()      f.vy += gravity * ((w.mass + burden*burdenMass)/massRef)^massWeight
```

Strictly better than a status would have been, for three reasons that are not
aesthetic: it is **countable on screen** (the blades are drawn where they went
in), it **stacks past any maxStacks**, and **nothing that clears statuses can
clear it**.

**`tickClank` is deliberately untouched.** Clank share is `mass^1.7` read off
`w.mass`. A ball with scythes stuck in it should fall harder — it must not
start winning binds it was losing a second ago, which is what counting the
burden for clank would hand the QUARRY as a reward for being hit.

## Why the roster did not move

Both edits are exact arithmetic identities at zero burden, which is every
fighter in every match without Lastlight:

    (1 + e) - 0 * 0  ===  1 + e        mass + 0 * 0  ===  mass

`engine_ab` is what proves that rather than the comment: **2448/2448 matches
bit-identical field for field** across the seventeen pre-existing ids (and
3400/3400 on the pre-tune build). `harrow_probe` [5a] asserts the moveMul
identity directly, so if either edit ever stops being an identity at zero the
harness says so before engine_ab has to.

---

# 4. THE BLADE — MEASURED, NOT DERIVED

The placeholder was Thornwake's 31.35, and it was wrong by a mile, exactly as
the builder said it would be: **`verify.py --n 60` put Lastlight at 71.0%**,
21pp clear of a field whose standard error is 1.7pp. `lastlight_sweep.py`
narrowed it against all seventeen foes on **pinned** seeds (the engine's own
`batch()` draws from `Math.random()`, so two candidates would be measured on
two different populations and a 2pp difference would be unreadable):

```
    blade   winrate      blade   winrate
    31.35     71.5%      17.50     49.3%
    24.00     64.0%      16.00     48.0%
    19.00     53.4%      14.50     42.5%
```

**17.5 is the lowest blade in the game by a distance** — Axiom is 7.42 but
swings a greatsword arc; this spins at 3.2 with reach 104. That is the honest
price of an ultimate that fires every fifteen seconds and pays twice.

## verify.py --n 60 on the tuned build — 13/13

```
Grudgebearer 59.5  Dawnbringer 54.0  Aureole 53.2  Slagheart 52.3
Gravemourn 51.6  Heartwood 51.5  Ironhail 50.4  Farwarden 49.8
LASTLIGHT 49.3   Emberedge 48.5  Lightkeeper 47.9  Axiom 47.9
Goreshard 47.7  Widowmaker 47.5  Censer 47.5  Nightfell 47.3
Thornwake 47.2  Spellbreaker 46.8

spread 12.7pp · mean duration 37.9s · mean clanks 14.1 · 0/9180 timeouts
no pairing resolves on fewer than 6 hits · every pairing clanks
```

Lastlight is dead mid-field. Grudgebearer's deliberate tower survives. **Read
that list as a band, not a ranking** — `--n 60` cannot rank a flat field and
does not say so (SEED, `sundered-crown-weakest-probe.md`).

The contact floor is the one worth calling out: a relic that slows the foe by
up to 30% and stuns on every bloom is exactly the shape of thing rule 2 of
`roster-expansion.md` §5 warns about, and *no pairing resolves on fewer than
six hits* is the check that would have caught it.

---

# 5. THE DUD RATE, MEASURED

A radial spray in a 520x800 hall often sticks nothing. Slagburst's answer was
to manufacture its own fuel; this one cannot, because guaranteeing a latch
means homing and there is no homing anywhere in this engine. So the dud is
kept, made visible, and **measured** — 87 casts, 6 foes x 12 seeds, on the
tuned build:

```
    0 blades   11.5%   #######          <- the dud
    1 blade    21.8%   #############
    2 blades   23.0%   #############
    3 blades   25.3%   ###############
    4 blades   12.6%   #######
    5 blades    4.6%   ##
    6 blades    1.1%
                                mean 2.24 · bloom damage median 39, max 72
```

**1 cast in 9 sticks nothing** (Slagburst's was 26.3% before its fix). If Rick
wants that lower the knobs are `scythes`, `life`, `bounce` and `speed` — all
things a viewer can see — never a hidden floor.

Note the tuning interaction: on the 31.35 build the dud rate was **2.9%**.
Lowering the blade lengthened fights, which changed the distance distribution
at cast time. The dud rate is a property of the whole build, not of the ult.

---

# 6. THE HARNESS — 22 CHECKS, AND TWO OF THEM FAILED FOR REAL

`harrow_probe.py`. The two that mattered:

**(a) THE LATCH BRANCH WAS UNREACHABLE.** `tickShots` runs parry -> hit ->
wall -> pop -> spent, each guarded by `!dead`. The first build anchored the
latch before the WALL branch — which is after the HIT branch, so the ordinary
projectile path resolved every blade and deleted it. It built, it drew, it
looked right, and the ultimate was silently twelve small arrows: **72 casts,
0 blades stuck, 100% duds.** Nothing but a probe that asks "did anything
stick" catches that. Re-anchored before the hit branch.

**(b) THE DROP-ON-DEATH SAT UNDER A GUARD THAT HID IT.** `tickCharge` opens
with `if (!f.alive || this.over) return;`, so a fuse cleanup placed below it
can never run in the case it claims to handle. It matters because a fatal
blow arms `killFlight` and `checkEnd` deliberately holds the match OPEN while
the loser flies into the wall — during those frames `over` is false and
`move()` is still running, so the winner would spend its entire victory flight
burdened by blades nobody is going to detonate. Moved above the guard.

Three checks were **wrong themselves** and were rewritten rather than
weakened, which is the more useful half of this section:

1. **The post-mortem check asked an unreachable question.** It killed a
   fighter, stepped, and expected the fuse to drop — but `step()` returns into
   `decay()` the moment `over` is set. It was failing against a build that was
   fine. Now it asserts the *consequence* (no damage, no banner, 5s stepped
   past a 2.4s fuse) and drives the kill-flight window directly.
2. **The bounce check used the wrong clock, twice.** It counted `steps/120`
   and asserted every blade was gone before the fuse; measured 2.64s against a
   correct build. Hit stop freezes the world but `this.t` keeps advancing (so
   duration stays honest) while `s.life` only decrements on frames the sim
   advances — so step count *and* `m.t` are both wrong for this. The only
   right clock is the blade's own `life`. It now asserts the real claim:
   **no blade ever takes a third wall**, by watching for a blade alive at a
   boundary holding zero bounces.
3. **It called an early removal a defect.** Blades end three legitimate ways —
   latched, parried out of the air, expired. Reported now, not asserted.

Also asserted, and each earns its place: the blades are born **clear of the
shell and armed** (the splinters' trap — a projectile spawned inside
`R + s.r` resolves on the frame it is born, which would turn the spray into a
nova); the turn is **derived from `(a, life)`, not accumulated**, because
`life` is not in `LERP_FIELDS.shot` and an accumulated angle would strobe
against the interpolator; the burst **clears every burden field it consumed**
(a partial clear is a ball that stays slow for the rest of the match); and
every relic's set-piece plus all three Harrowing phases **draw without
throwing**.

## Gates on `32a1a7bad61659df`

```
harrow_probe        22/22
verify.py --n 60    13/13 over 153 pairings, Lastlight 49.3%
engine_ab --n 18    2448/2448 IDENTICAL on the other 17 ids, re-run after
                    the art revision (3400/3400 at --n 25 pre-tune)
introfit_probe      18/18 relics fit the card, 36/36 bands clean,
                    silhouettes fitted, tips wrapped
tip_audit           0 gaps. Harrowing's tip is 68 chars of 72.
```

---

# 7. THE ART

`_miniScythe` is one shape used three times — in flight, in the shell, and
thrown out of the bloom — so all three read as the same object. It is a
**scaled copy** of `_scCrescent`'s proportions rather than a call into it:
that path is authored in the weapon's own L/W and arrives with a snath, a
collar and a maker's mark, none of which survive being drawn fourteen pixels
wide. What has to survive is the hook.

## The head is not the weapon — Rick's correction

The first two cuts drew the CRESCENT ALONE. Rick, on the finished clip: *"the
mini scythes only show the head spinning, not the whole scythe."* He is right,
and the project had already worked out why in a different context: the runic
scythe's docstring records that the snath is ~60% of a scythe's footprint and
that **a long pole with a hook at the far end IS the type** — delete it and
what is left is a crescent, which is a different weapon. That finding was
about a silhouette on a contact sheet; it transfers to a thrown object
unchanged. A crescent tumbling by itself is a boomerang.

`_miniScythe` now draws the whole thing: `_scBase`'s own snath (same
quadratic, same control point), its collar, then the crescent hooking off the
end. **Proportions are caricatured on exactly one axis** — the real relic runs
`W/L` 0.106, a long shallow hook on a long pole, which reads as a stick at
forty pixels; this uses 0.31 so the hook survives being thrown across the
hall. Nothing else is changed, so the object in the air is recognisably the
object in the wielder's hand. The pivot is the object's own centre of extent,
not its grip: a scythe turning about the butt of its handle orbits, one
turning about its middle tumbles.

**The motion streak came off in the same pass.** The arrow has one because an
arrow is a rigid 9:1 dart whose direction is otherwise unreadable. Once the
haft is drawn, a streak is a second stick coming off the same point — the
zoomed sheet showed twelve blades each apparently holding a grey pole at the
wrong angle. The tumble is the motion cue and does not need a second one.

Stuck blades were re-seated to match: half a turn past the arrival angle, so
the crescent bites into the shell and the snath stands off it.

## Three things the first contact sheet corrected, all of them proportion:

- **the crescent was too thin** — narrow works at reach 104 with a snath under
  it; at 14px in motion it read as a scratch. Horns pulled apart, belly
  deepened.
- **the glow was bigger than the blade** — a 2.3r halo at 0.85 alpha around a
  1.0r crescent gave twelve white tadpoles. The glow is 1.7r at 0.5 now and
  the crescent is drawn at 1.55r. The blade is the object; the glow only says
  it is made of light.
- **the stuck blades were inside the ball** — seated at `R - 0.34r` on a 34px
  shell they were behind the shell's own light and invisible until the fuse
  was nearly out. They straddle the rim now, at `R + 0.34r`.

The fuse tell is `burdenK` **cubed**, so almost all of it lands in the last
third. A linear ramp reads as "bright" for two seconds and as no warning at
all in the half second that matters.

---

# 8. Carried, and not touched

- **massRef stays 2.680.** `mean(sqrt(mass))^2` over eighteen relics is
  2.6645 — the roster falls 0.29% slow against neutral, inside the noise of
  anything this project can measure. Re-deriving it re-tunes all seventeen
  existing relics and destroys the bit-identity proof. Do it in a tuner run
  (`slagheart_build.py --massref`), never in this build.
- **SEED's "21 free cells" is stale.** 42 - 18 = 24 now; it was 25 before this
  build, not 21. Per shape: twinblade 5, warhammer 5, scythe 5, flail 5, bow 4.
- The clip has **no VO hook** — kokoro models are not in the seed (restore per
  `tools/FETCH-KOKORO.md`). Raw mix is -19.9 LUFS.
- `cineScore` still cannot film an ultimate. The Harrowing is the best
  candidate yet — one bloom, one spike, a countable object — and it is still
  not wired.

---

# 9. Open decisions

1. **Is the Harrowing's feel right at 12 blades / 2.4s fuse?** Watch the clip.
   Mean 2.24 stick; the knobs that change that are all visible ones.
2. **Is an 11.5% dud acceptable**, or should the spray get denser/slower?
3. **`Harrowing` as the ult name** — chosen, not asked. One string.
4. **The tape reads 18 damage against Thornwake's 31 and Gravemourn's 44**,
   and the card says nothing about the ult paying twice. Legibility problem or
   honest weakness?
5. **A fourth sanctified relic makes the palette smudge worse** — Lastlight
   and Dawnbringer are the same white ball. Does affinity contrast become a
   hard gate in `pick.py` (v28 open decision 3), now that it matters more?
6. **Promote `sc-lastlight.html` `6469fe83f5f73ae5` to the chain tip of
   record?** It supersedes `sc-cardspin.html`, which was itself still an open
   promotion (v27 open decision 1 / v28 open decision 5).
7. **Ship to 01-live?** The tip now strictly dominates what is live by five
   builds.
