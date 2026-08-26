# SEED — v30, 2026-08-18. EIGHTEEN RELICS, TWO PATCHES MERGED.

`02-chain/sc-health18.html`, sha256 **`b57041681d7ee45b`**, is the chain tip
candidate. Three independent proposals — all three authored against
`sc-cardspin.html` `ec9b8d753235385d`, none of them a chain — composed into one
build, in this order:

```
02-chain/sc-cardspin.html                              ec9b8d753235385d
  shatter_build.py   AXIOM v3: 2-D fracture, 10 pieces 98965a7f49ac32d7  sc-shatter
  lastlight_build.py LASTLIGHT + the Harrowing         445a5241d9dbf0c4  sc-shatter-lastlight
  health_build.py    GAUGE / LIFELINE / STAGES / ULT   b57041681d7ee45b  sc-health18   <-- TIP
```

`01-live/sundered-crown.html` `51c9bf566f9eb679` **untouched.** The tip now
strictly dominates what is live by seven builds.

## WHY THAT ORDER, AND THE ONE THING THAT HAD TO BE BUILT TO MAKE IT COMPOSE

Anchors do not collide: shatter touches only `_gsConjured`; lastlight touches
the roster, two physics lines and the projectile/draw paths; health replaces
`drawHud..drawClock` and the health ring. `drawHud` is at 9301 and `drawSparks`
at 9467, so health's span replacement and lastlight's inserts never overlap.

**But `health_build.py` exits if any relic has no ult sigil** (its rule 9,
enforced not hoped) — so health MUST run last, and the eighteenth relic needed
one. `ULTSIG.lastlight` was written for this merge: twelve little scythes on a
ring, hafts inward, sliding out and brightening as the charge fills, core
emptying as they go. **The count is the count** — `ult.scythes` is 12 and so is
the glyph, so a viewer who counts the sigil and then counts the spray gets the
same number. `ult_sheet.py` shows it at 15% / 62% / 97%.

## Checks on `b57041681d7ee45b`

```
engine_ab --n 18    2448/2448 IDENTICAL vs sc-cardspin on the 17 pre-existing
                    ids.  ALL THREE proposals are provably presentation-only
                    for the existing roster, composed.
verify.py --n 60    13/13 over 153 pairings.  LASTLIGHT 49.3%, dead mid-field.
                    Grudgebearer 59.5.  Spread 12.7pp, mean 37.9s,
                    0/9180 timeouts, no pairing under 6 hits.
harrow_probe        22/22 on the composed tip
introfit_probe      18/18 fit the card, 36/36 bands clean
tip_audit           0 gaps
silhouette_probe    greatsword min IoU 0.330 — matches the shatter patch's
                    own stated number, so the fracture survived composition
twin_identity       _twinConjured 0px, _whConjured 0px, _gsConjured 122473px.
                    Reports NOT IDENTICAL overall and is RIGHT to: the runic
                    greatsword moved and nothing else did.  READ THE ROWS.
health_build        18/18 relics have their own sigil
```

Both incoming builders were first re-run against plain `sc-cardspin.html` and
reproduced their patches' stated hashes EXACTLY — shatter `98965a7f49ac32d7`,
health `d0bb4890b19edc47` — before anything was composed. Every control HTML in
the shatter patch also hash-matches its README.

## glass_probe DOES NOT VERIFY THE SHATTER BUILD, and its README line is wrong

`README-SHATTER-PATCH.md` claims:

```
glass_probe.py --a sc-cardspin.html --b sc-sh-none.html --n 10     5/5
```

That command produces **2 FAILED**, and the reason is structural, not a defect
in either artifact:

* `glass_probe` requires `bind:0.000` **and** `pool:0.000` in the candidate and
  says so at runtime. `sc-sh-none.html` has the first and cannot have the
  second — `shatter_build.py` has no `pool` parameter at all. `pool` is a v2
  (`glass_build.py`) concept. The tool warns "does not look like a --bind 0
  --pool 0 build. Numbers below may be meaningless" and it is right.
* `--dump` shows the candidate's gaps as **negative** (-5.4, -20.4, -18.0 ...).
  glass_probe measures 1-D daylight along the blade axis. **v3 is a 2-D
  fracture**, so pieces overlap when projected onto one axis and the
  instrument's model does not fit the art. [1] sees 10 or 11 runs depending on
  `_t` for the same reason.

Pointed at the build it was written for, it is clean:

```
glass_probe.py --a sc-cardspin.html --b sc-glass-nb.html --n 6     ALL PASS
```

(`--n` describes the CANDIDATE, and the v2 control has 6 shards, not 10.)

**Nothing is wrong with either artifact.** What is wrong is one check line in
the README, which points a v2 1-D instrument at the v3 control with the wrong
shard count. v3's coverage is `silhouette_probe --footprint` (0.330),
`twin_identity`, `engine_ab` and `verify` — all green above. A 2-D fracture
still has no instrument of its own; that is the real gap.

## v3 SHATTER WAS COMPOSED, v2 GLASS WAS NOT — this was a choice

The shatter patch offers two ALTERNATIVE proposals for Axiom and says "pick
one". v3 (`sc-shatter.html`) was composed because the zip, the README title and
the entire check list lead with it. **v2 is not discarded** —
`sc-glass.html`, `sc-glass30.html`, `sc-glass-nb.html` and `sc-glass-np.html`
are all still here with their hashes intact, and swapping is one rebuild:

```
python3 glass_build.py     --src ../02-chain/sc-cardspin.html --out ../02-chain/sc-glass.html --open -0.15
python3 lastlight_build.py --src ../02-chain/sc-glass.html    --out sc-glass-lastlight.html
python3 health_build.py    --src ../02-chain/sc-glass-lastlight.html --out ../02-chain/sc-health18.html
```

## Carried into this merge

* **`scpage.py` is the health patch's modified version** and must stay. The
  artifact embeds Atkinson as base64 WOFF2 and Canvas draws the FALLBACK face,
  with the fallback's metrics, for any text measured before those faces parse.
  The page withholds `window.AC` until `document.fonts.ready` and `game()`
  waits on it. Every capture in the repo goes through that one function.
* **massRef stays 2.680.** Eighteen relics want 2.6645 — the roster falls 0.29%
  slow, inside noise — and re-deriving it re-tunes all seventeen existing
  relics and destroys the bit-identity proof above.
* **HUD cost is a ratio in a GPU-less box** (+2.2% mean, `hud_cost.py`), and
  the shatter art costs ~2.5x the shipped weapon to draw by micro-benchmark.
  Neither has been measured on real hardware. The 165 Hz budget is still owed.
* **The free-cell count in the v26 section below is stale.** It is 24 now
  (42 - 18): twinblade 5, warhammer 5, scythe 5, flail 5, bow 4.

Write-ups: `06-docs/LASTLIGHT-NOTES.md`, `06-docs/README-SHATTER-PATCH.md`,
`06-docs/health/APPLY-ME.md`, and `06-docs/MERGE-v30.md` for this composition.

---

# SEED — v26, 2026-08-15. TWO PATCHES MERGED. The chain was REBASED.

`02-chain/sc-ember.html`, sha256 **`6e73c5776cdee56a`**, is the chain tip and
it now carries everything: the Crucible, Daybreak **with the spark grace**,
the fight card v3, Slagheart/Ironbloom, Slagburst, and massRef 2.680.

**01-live has MOVED for the first time since v21.** The TWO TOWERS patch was
dropped over it as its notes instruct:

```
01-live/sundered-crown.html   51c9bf566f9eb679   (was v21's ba423d8e…)
01-live/sc-playable.html      710b5fd95d877e61
```

**THE CHAIN TIP NOW STRICTLY DOMINATES WHAT IS LIVE.** The shipped file is
the two towers and nothing else; the tip is that plus three more builds. One
more `cp 02-chain/sc-ember.html 01-live/sundered-crown.html` (+ `share_build`)
ships the lot, on Rick's word.

## THE REBASE, and why it was not optional

The TWO TOWERS patch was authored against v21, so it looked older than the
chain. It is not: its **Daybreak is strictly better than the chain's**. 59
differing lines, and they are not a re-tune — they add the **spark grace**
(`sparkGrace:0.7`, an arm chirp, `justArmed`), which fixes a measured defect
the chain's version still had: *"95% of sparks died within 0.4s"* in the
scrum. It also answers the open density question — 6 sparks x 5 damage
against the chain's 3 x 8 — and repays the blade to 10.4 rather than 9.6.

Shipping the chain over it would have REGRESSED a measured fix. So the chain
was rebased onto the patch's game file and every builder re-applied:

```
02-chain/sc-daybreak2.html   51c9bf566f9eb679   <-- TWO TOWERS, the new base
  introfit_build             465bde798a39e4eb   sc-introfit
  slagheart_build            5c690961c489f8f5   sc-slagheart
    (--no-massref variant)   b7b816003fbcbc23   sc-slagheart-norm
  ultember_build             6e73c5776cdee56a   sc-ember   <-- TIP
```

Every anchor in all three builders hit exactly once on the new base. The
pre-rebase artifacts are gone; `sc-daybreak.html` `c25a90cc0ca82f68` is kept
as the SUPERSEDED Daybreak (3 sparks x 8, no grace) and nothing should be
built from it again.

Superseded hashes, for anyone holding them: sc-introfit `71c0a0c0c1ea6996`,
sc-slagheart `f4d8aa660fe0ee0f`.

The card-v3 build, `02-chain/sc-introfit.html`, sha256 **`465bde798a39e4eb`**:
both new ults — Grudgebearer's Crucible and Dawnbringer's Daybreak — plus the
fight card's legibility pass (Rick, 08-15: hard to read on mobile, scrunched
at the bottom, status and ult indistinguishable; doc
`sundered-crown-introfit.md`). `01-live/sundered-crown.html` is still v21's
`ba423d8e…`; **ship = cp the chain tip over it, update this table.**

## The chain. Build from `sc-base.html`, NEVER from `sundered-crown.html`.

```
02-chain/sc-base.html                                     95d34e6caf4f4b57  <-- ROOT
  roster15_build   12 relics, massRef 2.509, TUNED       4ef1db465d3a2f05   sc-c1
  cinema_build     the director, patch v2                093c91b45fcfa3f5   sc-c2
  wallglow_build   --mode buf --down 4                   f3c8e16e0d4103e7   sc-all
  introcard_build  fight card v2 + every tip             36065bdacd779595   sc-everything
  roster_gs_build  +4 greatswords, TUNED_GS              2e9089d9a1ce70fc   sc-gs7
  ultart_build     set-pieces for the 4 new              3dfa6a77288fa9f3   sc-gs7-ults
  ultart2_build    set-pieces for the last 6             ba423d8e6453592d   sc-ults-all
                                                                            = SHIPPED (v21)
  ultforge_build   THE CRUCIBLE                          bd28056762e1fe34   sc-crucible
  ultdawn_build    DAYBREAK                              c25a90cc0ca82f68   sc-daybreak
  introfit_build   THE FIGHT CARD v3, legibility         71c0a0c0c1ea6996   sc-introfit
  slagheart_build  SLAGHEART + IRONBLOOM + massRef        f4d8aa660fe0ee0f   sc-slagheart
```

**THE ABOVE IS THE PRE-REBASE CHAIN AND IS SUPERSEDED.** The live chain now
runs from `sc-daybreak2.html` — see the rebase table at the top. The rows up
to `ultdawn_build` are unchanged history; everything after it was rebuilt.

```
02-chain/sc-daybreak2.html  = TWO TOWERS patch     51c9bf566f9eb679  <-- BASE
  introfit_build   THE FIGHT CARD v3               465bde798a39e4eb   sc-introfit
  slagheart_build  SLAGHEART + IRONBLOOM + massRef 5c690961c489f8f5   sc-slagheart
                   (--no-massref variant)          b7b816003fbcbc23   sc-slagheart-norm
  ultember_build   SLAGBURST (Emberedge)           6e73c5776cdee56a   sc-ember  <-- TIP
```

## THE ROSTER IS A GRID, AND IT IS 17/42

`05-reference/roster-grid.png` is the menu: 6 shapes x 7 schools, and every
shape but the bow already has all seven school variants written (`_scBarbed`,
`_fhBuilt`, `_whGrown`...), dispatched on `p.key`. Greatsword is the only
complete row. **21 free cells remain** — warhammer 4, twinblade 4, scythe 5,
flail 5, and the three unbuilt bow cells need art. School decides the status
(dwarven->sunder, verdant->entangle, vigil->ward, ...); shape decides the
archetype numbers. The design work per cell is the ultimate and the tuning.

## The Crucible, in one paragraph

`kind:"forge"` — a state ultimate on the bow's pattern. Cast: no damage, no
banner; the ball ignites deep orange, the hammer spins up 6.8x into a wheel,
an event horizon forms. The pull: inward acceleration 260→2600 plus a capture
term that bends the foe's velocity onto the infall line — both ramping over
1.6s. The strike: first melee connect after a 1.05s floor, 2x damage, crit
9%+15%/stack at 2.1+0.4x/stack, consumes ALL Sunder (counting its own
landing), freezes 0.16+0.06s per stack consumed, launches the foe over the
speed ceiling into wall-rattling bounces. Fatal strikes hold the match open
while the ball flies and it shatters against the wall it meets. Whiff = 4s
cap, fizzle, stacks kept, 18s charge rebuilds from the resolution. Full
design + every tuning decision: `claude/sundered-crown-crucible.md` in the
project; the builder docstring carries the same.

## Slagburst, in one paragraph

Emberedge's Forgefall (one of five novas) retired for `kind:"detonate"` — a
third state shape, a FUSE. Cast in range splits the shell for 3 Sunder,
resolves no damage, and lights a 0.55s fuse on fighter time; the detonation
reads `banked + split` UNCAPPED (3..9), clears every stack, and prices
`6 + 5.5n` damage, `110 + 34n` knock, and one shard per stack. It came with
the measurement that shaped it: **a quarter of Emberedge's casts find zero
Sunder**, so a literal detonation is a dud one time in four — the split is
the fix, and the relic's blurb had already written it. Sideways by design:
-0.38pp over 3900 paired games, blade unchanged at 12.32. Full notes:
`06-docs/SLAGBURST-PATCH.md`.

## Slagheart, in one paragraph

Dwarven flail, `mode:"chain"`, the second one in the game — picked because
chain had exactly one relic and the question was whether the model
generalises. It does: not one line of the chain model changed. Sunder at +2
a hit against Grudgebearer's +1, so the school now has a Sunder BUILDER and a
Sunder SPENDER. **Ironbloom** (`kind:"latch"`, Rick's design) lights the head
for 6s; the first melee connect bites instead of hitting, the chain snaps
taut and the hall freezes for 0.8s with the shake RAMPING rather than
decaying; then it blasts, shoves the foe at 1800 over a raised ceiling, and
throws nine bouncing splinters that sunder and pop where they die. It never
pulls: 61% of casts bite and the rest cool unfired, which is exactly
`1 - exp(-6.0s window / 6.2s connect gap)` — a Poisson trial on the foe's
position that NO weapon-side knob can move (a spin-up and a chain payout were
both built, measured at +3pp and +2pp, and deleted). Full design + both
deleted mechanics: `claude/sundered-crown-slagheart.md`.

## The fight card v3, in one paragraph

The card was scrunched: v2 bottom-anchored the facts so ~40% of each card was
dead air, and its shrink-to-fit guard had quietly taken the two longest ult
tips to 19px — on a 1080-wide canvas at ~390pt that is a 7pt glyph on the
card's most important line. v3 fills the card top-to-bottom (frame margin
118 -> 104, card 560 -> 574, and the tape's 678..1242 band is untouched),
takes tips to 30px and WRAPS instead of shrinking, moves the cooldown off the
sentence onto a right-aligned chip, and makes the status and the ultimate two
different objects — tinted grounds, accent rails (school colour vs gold), a
lit border on the ultimate, and twice the gap above it. Silhouettes are now
FITTED to a header box by measuring the shape (`_artBox`) rather than sharing
one scale:2.2, which is what let the scythe hang out of the card on the first
cut. Layout is factored (`_introFacts` / `_introLayout`, both on `AC.IC`) so
introfit_probe.py can lay out all 16 relics and assert instead of screenshot.
Full design: `claude/sundered-crown-introfit.md`.

## Checks on the REBASED chain tip (all run at `6e73c5776cdee56a`)

```
verify.py --n 60    13/13 over 136 pairings.  Grudgebearer 62.4 · Dawnbringer
                    54.1 · SLAGHEART 51.4 · field 45.3-50.7.  Both deliberate
                    towers intact; Slagheart still inside Rick's 46-52 with
                    no re-tune needed after the rebase; Emberedge 50.5,
                    sideways as the patch claimed.
engine_ab --n 50    6000/6000 IDENTICAL, sc-slagheart vs sc-ember on the 16
                    non-Emberedge ids.  Slagburst is inert.
ultember_check      23/23
slagheart_probe     17/17
introfit_probe      8/8 — 17/17 relics fit the card, 34/34 bands clean
intro_probe         [1]-[6] PASS.  NOTE the scoping: [1] must be run on the
                    CARD STEP alone (--src sc-daybreak2.html --out
                    sc-introfit.html --pre sc-c2.html).  Run against the tip
                    it fails correctly — the tip's engine differs from the
                    base by a relic, an ult and a physics constant, which is
                    not what [1] is asking about.
tip_audit           0 gaps
massref_probe       mean fall multiplier 1.000 at 2.680
```

## Checks on the pre-rebase tip (all run at `f4d8aa660fe0ee0f`)

```
slagheart_probe   16/16.  The ones worth knowing: the bite deals NO damage;
                  the hold is frozen solid for 97 frames of a stated 96; the
                  shake ramps 18->58 with ZERO frames of decay; a splinter
                  sunders once where the head sunders twice; the lit head
                  buys no stun immunity (the OPPOSITE of the Crucible's
                  assertion); and [10] asserts the bite rate against the
                  Poisson prediction rather than a threshold.
engine_ab         6600/6600 IDENTICAL, sc-introfit vs sc-slagheart-NORM.
                  The relic is inert.  Against the shipped tip (new massRef)
                  it is 4800/4800 DIFFERENT — that is the constant, measured
                  on its own.
verify.py --n 60  13/13 over 136 pairings.  Slagheart 51.5%.  Towers intact:
                  Grudgebearer 62.9, Dawnbringer 55.1.  Field 45.8-51.5,
                  TIGHTER than it was at 16 relics.
massref_probe     mean fall multiplier 1.000, drift +0.0%.  Item 7 closed.
introfit_probe    17/17 fit the card, 34/34 overflow bands clean
intro_probe       [1]-[6] PASS (--pre sc-c2.html)
tip_audit         0 gaps.  Ironbloom's tip is 71 chars of 72.
```

## Checks on the previous tip (all run at `71c0a0c0c1ea6996`)

```
introfit_probe        [A] all 16 relics fit, tips wrap clean, silhouettes
                          inside the header band, no name reaches the art
                      [B] smallest tip face 26px (v2 floor was 20px; v2
                          shrank 8 tips below 25)
                      [C] 32/32 card-overflow bands clean
                      [D] the dead band carries facts: 0.0800 vs v2 0.0000
                      [E] gap above ULTIMATE 28 > above ON HIT 14, 16/16
intro_probe           [1][2][3][4][5][6] all PASS.  NOTE: [3] now takes
                          --pre sc-c2.html — the last build with NO card.
                          Against --src (which now HAS a card) the
                          differential arm cannot fail, and a check that
                          cannot fail is comparing nothing.
engine_ab  --n 55     6600/6600 identical across all 16 ids
verify.py  --n 60     13/13.  Towers intact: Grudgebearer 63.0,
                          Dawnbringer 54.4; floor Farwarden 46.1
tip_audit             0 gaps
```

## Checks on the previous tip (all run at `bd28056762e1fe34`)

```
verify.py --n 60      13/13 at the tip.  TWO deliberate towers now:
                      Grudgebearer 63.0, Dawnbringer 54.4.  Field 46.0-51.8.
                      NOTE: tune.py must not be run blind — it would flatten
                      both towers.
engine_ab             6300/6300 matches bit-identical on the other 15 relics
                      (vs sc-ults-all).  Zero extra rng draws off-relic.
ultforge harness      15 mech asserts + 12 art samples + wallcrack + 15-relic
                      set-piece regression, all PASS.
tip_audit             0 gaps.  intro_probe [1][2][4][5][6] PASS.
```

## The short

`07-shorts/short-4-grudgebearer-v-thornwake.mp4` — seed 1476297217, 31.3s,
kill cut IS a six-stack Crucible (606!) into the wall shatter. Pipeline:
`06-docs/SHORTSHANDOFF.md`, **including a new §8 addendum: the Crucible's
kill SFX breaks the old stage-3c mix (+0.5 dBTP); use the corrected filter
line with `alimiter ... level=false`.** kokoro models are NOT in this seed —
restore per its §1.

## NEVER MEASURED ON THE PHONE

v21's debt in full (cinema director's unretracted 21.85ms regression, wall
glow proxy), **plus the whole Crucible, plus the card v3**. In-container the
card-hold frame is 15.5ms (v2) vs 16.3ms p50 (v3) — inside this box's noise,
so it says "not obviously worse", not "fine". `_artBox` costs 2 x ~1ms ONCE
per page, on the first card frame; that is a real one-frame cost on a slow
phone and nobody has watched for it. Its art is small-stroke by design
(shadowBlur ≤ 18, gradients ≤ 150px, no full-canvas blur) — still a proxy.
`03-bench/` has the paired pages; a fresh bench page off the chain tip is
still owed.

## A generated file is not a place to store a number

Unchanged law. Tuned values live in the builders:

```
roster15_build.py   TUNED       the 12 original relics
roster_gs_build.py  TUNED_GS    the 4 new greatswords
introcard_build.py  tip edits   every status and ultimate line
introfit_build.py   IC          every fight-card metric (margins, panel box,
                                art box, stretch cap, gaps)
slagheart_build.py  TUNED_SH    dmg/blast/shard/window for Slagheart
                    MASSREF     2.680, re-derived for 17 relics
ultforge_build.py   DATA_NEW    every Crucible number (charge, spin, pull,
                                crit scaling, launch, freeze) + the tip
ultdawn_build.py    DATA/TUNED_DB  every Daybreak number (window, sparks,
                                blessing) and Dawnbringer's repaid blade 9.6
```

## Traps recorded this session (full list in the project doc)

* A pull without a capture term slingshots — measured, the strike never came.
* A wind-up the foe can stun-lock breaks its own promise — stun burns off
  while the forge is lit. That call was made without asking; flag it to Rick
  if hex counterplay ever feels missing.
* NaN in one ball infects both through ballCollision in a dozen frames.
* engine_ab with an explicit id list is the cheap bit-identity proof every
  ult redesign should end with.
* ffmpeg alimiter re-normalizes to full scale unless `level=false`.
* **A rate that is a property of the FOE cannot be tuned on the WEAPON.**
  Two mechanics were built and deleted proving it (Ironbloom's spin-up and
  chain payout). Work out what the constraint actually is before buying a
  knob for it.
* **A projectile spawned at `R + 6` is inside `R + s.r`** and resolves on the
  frame it is born. Arm your shrapnel.
* **A probe that watches hp while the other relic is still swinging** is not
  measuring your effect. Isolate the party you are not testing.
* **A report can state a count it never measured** — introfit_probe printed
  "16/16" over a 17-relic roster. Print `len(x)`, never the number you
  expected.
* **THE FX CLOCK RUNS AT ~1.95x SIM TIME on the normal path** and exactly 1x
  while frozen. `decay()` calls `decayImpactOnly()` (which ticks
  presentation) and then ticks presentation AGAIN. Every `life` in the engine
  is therefore in half-seconds. Flagged in SLAGBURST-PATCH.md, verified here,
  and it had already broken Ironbloom: `life = window + 0.4` meant the lit
  head's glow died 3.3s into a 6.0s window. Doubled, and slagheart_probe [11]
  now asserts screen-life against the thing it explains.
* **An incoming patch that looks older may be strictly newer in one place.**
  TWO TOWERS was authored against v21 and its Daybreak was AHEAD of the
  chain's. Diff the substance before assuming a fast-forward.
* **`verify.py --n 60` cannot rank a flat field and does not say so.** SE is
  1.7pp; the field is ~5pp wide. The v23 "floor" (Farwarden ~46) was noise —
  two disjoint seed sets put Farwarden near the TOP. Only Lightkeeper and
  Nightfell are bottom-three in both. See `sundered-crown-weakest-probe.md`
  and `tools/weak_probe.py`. **Read the bar chart as a band, not a ranking.**

## Do NOT rebuild sc-hud.html

`hudglow_build.py` is a measured dead end, unchanged from v21.
