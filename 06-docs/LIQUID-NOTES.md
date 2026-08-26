# THE RELIC IS A VESSEL — glass spheres, liquid health, v31

**2026-08-19.** Built off `02-chain/sc-health18.html` `b57041681d7ee45b`.
Result **`02-chain/sc-liquid.html`**. `01-live/sundered-crown.html`
`51c9bf566f9eb679` **untouched**.

Rick: *"I want to rethink the health bars that are attached to the balls ...
animated as if they are glass spheres filled with liquid ... i would like the
liquid inside the ball to represent its health. Meaning as it looses health the
liquid drains out."*

```
cd tools
python3 liquid_build.py --src ../02-chain/sc-health18.html --out ../02-chain/sc-liquid.html
python3 liquid_probe.py --src ../02-chain/sc-liquid.html            # 14/14
python3 liquid_probe.py --src ../02-chain/sc-liquid.html --selftest # the checks have teeth
python3 verify.py       --game ../02-chain/sc-liquid.html --n 12    # 13/13
python3 engine_ab.py    --a ../02-chain/sc-health18.html --b ../02-chain/sc-liquid.html --ids <all 18>
```

---

# 1. WHAT REPLACED WHAT

Six statements of one number in six weak channels became one statement of it in
the strongest channel there is.

| gone | why |
|---|---|
| the 4-chunk arc gauge | v5's finding — a COUNT beats a proportion — survives as the graduations. But the arc was still an **angle**, the third-ranked visual encoding. A liquid level is **position along a common scale**, the first. |
| the ash husk | said "hurt" by closing in from the rim. The waterline says it by falling. Two statements of one number in the same pixels. |
| the ember + drain tail | features OF the arc. The tail became a tide mark on the glass — the same information in the language of the object. |
| the stone fracture | *"the balls look like stone cracking, id like that to change to glass cracking"*. Rebuilt, then switched off (§3). |
| the grain sprite | existed to stop a smooth sphere reading as glass. The sphere is now glass on purpose. |
| `shellCracks` / `SHELL_CACHE` / `corePath` | **deleted, not left dead.** Recoverable from `sc-health18.html`. |

**The lifeline panel above the hall is untouched, by choice.** It answers "who
is winning", which is a different question from "how badly is this relic hurt",
and it is the one instrument in the frame that can compare two relics at a
fixed seat.

## The one physical lie, stated

A ball in free flight is in free fall, so a truly physical liquid inside it
would be **weightless** between bounces — it would leave the floor of the
sphere, ball up in the middle, and have no level at all. That is real and it is
unreadable, because the health encoding depends on the surface being a level.

So the liquid is given the hall's down permanently, and only the
**non-gravitational** part of the ball's acceleration drives it. Everything a
viewer can actually see — wall bounce, floor slam, knockback, clank, a Crucible
launch — is exactly that part. Free flight is calm, contact is violent, which
is also the rhythm the fight actually has.

## Per school, from the affinity table that already existed

`SLOSH.mat` gives each school a natural frequency, a damping ratio, a drive
gain, a tilt scale, and a bubble population. Sanctified light rings like a
struck glass; dwarven amber heaves once and stops. Measured, not asserted —
`liquid_probe` check [10] requires sanctified to out-slosh dwarven and reports
the whole ordering: **sanc 0.56 · runi 0.55 · vigi 0.39 · verd 0.29 · umbr 0.24
· bloo 0.22 · dwar 0.14** rad peak tilt.

---

# 2. THE DETERMINISM CONTRACT — the whole risk of this build

Every health visual before this one deliberately held **no state** and drew
**no rng**. This one carries ten numbers per relic and integrates them on the
simulation tick. The contract is kept in four parts, and each is *proved*:

1. **The state is write-only.** No simulation code reads a slosh field.
   `liquid_probe` [1] runs the same 54 matches with the integrator on and off
   and requires identical summaries. `--selftest` couples the liquid back into
   `move()` by **1e-6** and the check breaks 35 of 36 matches — so it has teeth.
2. **No rng is drawn.** [2] instruments `m.rng` and requires the call count to
   be identical with the integrator on and off. 462,152 either way.
3. **It runs on the SIM tick, in `tickPresentation`** — 120 Hz in the live page
   and 120 Hz in the offline render, so the two agree frame for frame. It also
   runs on the *frozen* path, so the fluid keeps moving through a hit stop,
   which is exactly when the viewer is staring at the ball.
4. **Every position is a pure function of `(side, index, m.t)` through
   `shellHash`** — bubbles, vapour, frost, leak — exactly as the fractures and
   statuses already are.

`engine_ab.py` over all eighteen relics: **918/918 identical field for field.**

### The freeze test, which is not obvious

Hit stop, the Harrowing's latch and the end of the match all stop calling
`move()`, so no gravity was applied on those ticks — and subtracting it anyway
injects a phantom impulse every frozen frame and tips the liquid over during
the exact beats the viewer is watching hardest. **The ball not having moved IS
the frozen tick**, exactly, and it costs two compares and no new coupling.

---

# 3. THE THREE MEASUREMENTS THAT CHANGED THE BUILD

## 3.1 A bounce is an impulse, not a force — and the first cut was invisible

The readable version fed the measured acceleration into the oscillator as a
forcing term. Physically the right shape; **a floor bounce moved the surface by
0.0017 of a radius**, a third of a pixel. A bounce is one tick of a very large
number, so `force * dt` is the entire budget and it is nothing. What a bounce
delivers is a step change in velocity, and the liquid's response is a step
change in the oscillator's **velocity**. Kick that directly and the same bounce
moves the surface half a radius.

`slHeave` was also never wired into `surf()` at all. Both were invisible in the
code and obvious the moment a filmstrip was rendered.

## 3.2 A headless sweep must not integrate a picture — 40% of the whole sim

Measured on a 612-match sweep: **17.5s → 24.9s**, and stubbing the integrator
recovered every bit of it. 215 ns a call in isolation does not explain 6.4 s
across the sweep — the cost is the extra work on the hot tick, not the
arithmetic in it. Two rewrites (allocation-free, then fields declared in the
`Fighter` constructor) each bought back about a second and neither was the
answer.

The answer is `Match.slLive`, default **true**, set **false** on the one line
in `simulate()` that is by definition headless. `verify.py` and `tune.py` call
`simulate()` thousands of times and draw none of them; a balance run should
never pay for a visual feature. **17.75s → 18.48s, +4%, noise.**

Frame cost at 1080×1920, GPU-less box: **median 55.6 → 56.3 ms, +1.3%.** The
glass costs about what the stone shell, the grain sprite and the five-pass
fracture cost together. *This is not a phone number and nobody has measured one
yet — see §6.*

## 3.3 The reading budget, derived — and my first two derivations were wrong

A health readout that wobbles is a health readout that lies. Full scale is
1.64 R for 300 HP, so **0.01 R of surface is 1.8 HP**.

**Attempt one** clamped heave only, reasoning that tilt and both cosine modes
integrate to zero. The probe returned 0.19 R of drift — **35 HP**. The error:
what a viewer reads is not the surface at the centre, it is the boundary
averaged across the *width*, and the width of a sphere is a chord. Under a
chord weight the cosines do **not** vanish; the nth mode contributes
`J1(nπ)/(nπ/2)` of its amplitude — **0.181** for mode 2, **0.068** for mode 3.

**Attempt two** added a pointwise bound and the probe returned 0.60 R against a
claimed 0.274, because the tilt term is `u·tan(θ)` and at the rim near the 0.92
clamp that is 1.3 R by itself. Not a defect: a tilted surface pivots about the
centre, the ends go where the ends go, and the chord is zero out there anyway.

**The budget that shipped**, with the clamps set *from* it rather than the
other way round:

```
reading error  <=  heave + 0.181*A2 + 0.068*A3
               =   0.060 + 0.0199  + 0.0068   =  0.0867 R  ~=  15.9 HP
observed worst                                    0.0748 R  =  13.7 HP
peak tilt in real play  0.50 rad (29 deg)   against a 0.92 rad (53 deg) clamp
```

---

# 4. WHAT RICK CUT MID-BUILD, AND WHAT IT COST

Both were called on sight of a contact sheet, and both were right.

**The graduations.** *"i dont love how the quarter markers are looking and im
starting to think we dont need them."* Four etched marks read as a clock face
painted on a marble. What is lost is the one boundary that is not arbitrary —
`CONFIG.desperation.at`, the frame the simulation changes gear. `MARKS.mode` is
live in the page: `"none"` (shipped) · `"desperation"` (that line alone) ·
`"ticks"` (all four). The vessel does not need a scale the way the arc did: the
glass **is** the scale, both ends are always on screen.

**The fracture. REJECTED, and the decision is closed.** *"i also think the
glass cracking is a bit distracting ... lets add it back later if we feel like
we need it"*, and then after the experiment of §4b was built and rendered:
*"think that settles it. im not interested in the cracking and leaking feature.
lets leave it cut."*

Read §4b before rebuilding any of this. It was built once, properly, judged on
video against the same seed frame for frame, and turned down. The whole pattern
is still live behind `FRACTURE.on` — impact sites with radial arms and scalloped hackle
rings, optics inverted so a crack is the **brightest** thing on the ball rather
than the darkest (a fracture in glass is a mirror; in stone it is a gap).

Turning it off also turns off:
* **the chipped silhouette** — a straight-edged bite with no crack running to
  it reads as a rendering fault, not as damage. Probe [12] enforces it.
* **the leak.** The vents ARE the fracture arms that reach the shell, and
  liquid jetting out of a visibly intact sphere reads as a defect. `--fracture
  off` forces `--leak none` and says so.

`sc-liquid-frac.html` **`ff28ebcf0936776f`** is the same build with both on. It
is kept as the RECORD OF A DECISION, not as a candidate.

**What the decision costs, stated plainly:** with the fracture off, the relic's
damage is carried by the **level and nothing else** on the ball. The vapour and the
halo are restatements of the same number, not independent readings. The v5
legibility work argued for redundancy; this build has one strong channel where
it had six weak ones. That is a defensible trade and it is not a free one.

---

# 4b. THE CRACK-AND-LEAK EXPERIMENT — built to be written off honestly

Rick, after the clean build shipped: *"as an exparament can you build the balls
cracking and leaking? i dont think im gonna want to go in that direction but i
feel like i should see it before i write it off for good."*

A thing built to be rejected still has to be built well, or the rejection is of
the draft rather than of the idea. Two defects were found by exercising code
that had shipped untested, and both would have made the experiment unfair to
itself.

**THE LEAK HAD NEVER EMITTED A SINGLE DROPLET.** Every shot and every clip up
to this point was the fracture-off build, so `tickDrips`, `glassVents` and
`drawDrips` had shipped without ever running. First exercise:

```
side 0:  6 sites,  3 vents reach the shell
side 1:  6 sites,  2 vents reach the shell
first drop at 29.4 s of a 43.7 s fight — 67% through
```

Two thirds of the fight showed cracks and no spill. The cause is geometric: arm
lengths are 0.17–0.51 R from sites at 0.16–0.82 R, so most arms simply never
reach the rim. **The fix is better physics, not a bigger number.** The impact
point is *itself* a hole — a crush zone is pulverised glass, which is to say a
gap — and a stone through a windscreen takes material out AT the impact. Adding
the crush zone as a vent, gated on the site sitting near the rim (a hole in the
middle of the projected disc faces the viewer and the liquid has nowhere to go
this renderer can draw):

```
5–6 vents a side · first drop at 15.8 s · 606 drops over the fight · peak 47 on screen
```

**A HIT DID NOT SPURT.** Emission was a flat rate against the head of pressure,
so the spill looked identical during a clean exchange and at the instant a
warhammer landed — and *hit, crack, spill, level down* is the entire argument
for the feature. `slJolt` is already the contact impulse the slosh runs on, so
the rate and the jet velocity now both ride it. Costs nothing and ties the
spurt to the blow instead of to the clock.

Droplets also went from 1.4–3.6 sim units to 0.7–2.2: at the old size they read
as bubbles leaving the ball rather than as liquid.

**Cost.** `liquid_probe` 14/14 on this build too. Frame cost **+3.0%** median
against the v30 tip, where the clean build measures **−1.0%** — so cracking and
leaking is about four points of a frame more than not.

**A/B on video, same pairing and same seed, frame for frame:**

```
07-shorts/liquid/liquid-wm-v-axiom.mp4              clean
07-shorts/liquid/liquid-CRACK-LEAK-wm-v-axiom.mp4   cracking + leaking
```

**THE VERDICT: cut.** Rick, on the A/B: *"think that settles it. im not
interested in the cracking and leaking feature."* Written off having been seen
working and fixed twice, which is the only kind of rejection worth recording.
Do not rebuild it to find out — that is what this section is for.

# 5. THE TWO STATUSES THAT STONE MADE SENSE OF AND GLASS DOES NOT

**Curse** ate maximum life and drew an umbral arc at the far end of the health
ring — which read as *health* to anyone who had not read the code. It is now
the part of the glass the liquid can never reach again: a frosted dead cap from
the fill line down to `maxHp`. A dead, empty, frosted band above the fluid
cannot be read as health by anybody. The shroud is gone (it occupied the exact
annulus where fluid now meets glass); the escaping motes stay, and now leave
**from the dead band**, so the thing being taken and the place it is taken from
are the same place on screen.

**Sunder** lifted armour plates off a stone shell — right for stone, impossible
for glass, which has no layers to lift. Glass under repeated impact **spalls**:
a shallow curved flake lets go and leaves a bright scalloped scar. Same
mechanic in the right material, still legible with the colour removed, and
deliberately *not* a fracture — a flake has a smooth conchoidal edge and no
radial arms, so a sundered relic is distinguishable from a cracked one at a
glance.

**Death** is the vessel failing, and it has two halves a stone shell did not.
The glass goes as flat straight-edged slivers, each with one lit face. And the
liquid goes with it: the droplet count scales on `deathHp` — what was still in
the glass when it failed — so a relic finished at 2 HP barely stains the floor
and one taken from a third of its life empties itself across the hall.

---

# 6. STILL OPEN

1. **Nobody has measured a phone.** +1.3% median in a GPU-less box says the
   glass costs what the stone cost, and that number is worth what it is worth.
   The budget is ~6 ms at 165 Hz and it has not been measured against any of
   the last five sessions' work. `bench_build.py`, or `03-bench/` on a handset.
2. **One channel, not six — and now permanently.** §4. The fracture was the
   obvious second channel and it is cut for good (§4b), so if the level ever
   proves insufficient at phone size the answer has to be something new rather
   than something switched back on. Nothing has yet shown that it is
   insufficient; this is a thing to watch, not a thing to fix.
3. **~500 lines of rejected code still ship in the default build.** `glassCracks`,
   `drawGlassFracture`, `glassVents`, `tickDrips`, `drawDrips` and the chip
   branch of `glassPath` are all inert behind `FRACTURE.on = false`, and this
   session deleted `shellCracks`/`corePath` on exactly the argument that
   retired code is a trap for whoever reads it next. That inconsistency is
   deliberate and it is not resolved: **`liquid_build.py` can already
   regenerate every line of it from `--fracture on`**, so the shipped HTML does
   not need to carry it. Teaching the builder to omit the blocks when the flag
   is off is maybe an hour and it touches a verified build, which is why it was
   not done at handoff. `liquid_probe` check [12] toggles `FRACTURE.on` and
   would need rewriting with it.
4. **The lifeline was left alone** and now speaks a different visual language
   from the balls. Two glass tubes holding the same substance at the same level
   is the obvious next move, and it was explicitly deferred.
5. **Shorts have never been shot on this.** The whole week-one pipeline films
   `sc-cardspin`. Widowmaker v Axiom shows the level falling on both sides.
6. **`sc-liquid` vs `sc-cardspin` as tip of record** — four sessions have now
   asked. This build makes it a bigger question, not a smaller one.
7. Carried from v30: `sc-scflip` · 24 free grid cells · `o.dark` · Nightfell
   silhouette · same-type tape ties · `render.py` wall-time audio port · the
   cinema director's unretracted 21.85 ms phone regression · `fireUlt`
   life-table `grudgebearer: 1.7` shadowed by the forge branch · `cineScore`
   still cannot film an ultimate · the HUD spill · **a 2-D fracture has no
   probe** · **nothing spends Smite**.
