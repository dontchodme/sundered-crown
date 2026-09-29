# v109 — CENSER / CONSECRATION (REDESIGN), BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-lightkeeper-fxout`, the nova's field spec out of both `fx.js` copies: §7; shell_identity waits for Rick to be off the PC): stage 1 is arm A to the fight; the holy ground is the lab's (probe 9/9 on every stage from 2 on; ten mutants, each changing fights and each caught by its own check alone); the built relic reads over the lab by the window clock and under it by the heal's centre test, both measured with controls; no knob to move (the design names none); **the blade at the design's own target, the shipped rate: 25.5 (49.6% both sides, against the shipped nova's 50.1% on the same fights)**, and on 151 the shipped rate is 50%, so Rick's other choice is the same point. The brief's three blades (26 / 26.5 / 27) all read over the shipped rate, so the grid was widened down inside the hammer row, and it is said here. engine_ab: the 37 others identical. verify --n 40: 10/13, the base's own three reds and no new one (Censer 51.7%). **Stage 6, the picture and the voice, is built (`sc-censer-consecration-b25.5-fx`, §5):** thirteen rows byte-exact to the two labs'; the holy ground drawn as floor under both balls off the simulation's own discs (live at 0.18 in a window, inert at 0.07 outside one), the hammer head's hot gold core, a gold rim on a foe on the ground, the drift round Censer on it, SMITE and BLESSING once a stretch; a thurible swing at the cast, a bowl's bell a disc (one step of A minor pentatonic a disc standing), the spark collect a blessing, the smite tick silent; the nova's art out, and no `fx.js` field (the incense is drawn). engine_ab 4218/4218 with Censer in; the probe 11/11, its two new checks (the voices, the picture's hook, 74 fights drawn) each failed by its own mutants; render_ab 24/24 with a control at 0/6; compose6 0 FAIL up to `sc-lightkeeper-fxout`. The clip is with Rick. The nova's `fx.js` spec is the orchestrator's to take out at the carry. Claude Code has it.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`, the BUILD row under the redesign's).
Input: `06-docs/v78/censer-consecration-redesign-v78.md` (its §5 is the build brief) and its runs
(`06-docs/v78/runs/holyground_*`, `tools/overlays/holyground.js`), and nothing else (rule 0). Builder
`tools/censer_build.py` (0d97b0a19fe72d27; stages 1-5's was 78501578c5773570), probe `tools/censer_probe.py`
(c588b606b1fc7741; stages 1-5's was 5d78670c3787524e), runs in `runs/` (stage 6's are `runs/stage6_*`).
**A REDESIGN, not a new relic:** Censer ships in the base; its nova (Consecration) is replaced by the design's
holy ground, and the roster stays 38.

```
sc-tendril-t3.html                          the base: the chain tip (Bindweed stage 5)                    5a6216e3b629fad4
  -> sc-censer-stub.html                     stage 1  the nova out, the ground's block in, stubbed (1e9)   56626e03654f3daf
  -> sc-censer-ground.html                   stage 2  the ground and the smite; charge 14 (arm B)          9da88c11cb87a3a2
  -> sc-censer-consecration.html             stage 3  the heal, bless 0 -> 1 (arm C)                       2ce681c11f5d4183
  -> sc-censer-consecration-b25.5.html       stage 5  the blade, 28.77 -> 25.5 (the shipped rate)          56c49ad3f0ccb3aa
  -> sc-censer-consecration-b25.5-fx.html    stage 6  the picture and the voice (presentation)             3d68c7648a9cb3a8
```

**Built in scratch** (the batch runs its builds in parallel on one tip); the orchestrator carries the links
onto the chain by rebuilding them with this builder on the tip of the day and proving each carry with
`engine_ab`. Every link above rebuilds byte-identical from the final builder (re-checked on resume, in
`runs/compose2.txt`, and with the stage-6 link in `runs/stage6_builder_checks.txt` and
`runs/stage6_compose6.txt`), and no `sc-censer*` name is on `02-chain/`. **The builder composes** (`runs/compose2.sh`
-> `compose2.txt`, 0 FAIL, 2026-09-29 03:19): with every other in-progress batch builder on this line
(Lightkeeper, Widowmaker, Aureole, Coldiron, Ironhail, Lodestone, Oracle, Angelus, each at its last stage,
Aureole's stage 5 included), both ways and in two stacks (in version order with Censer in its place, and
Censer last on the other eight). And on the line's newer tips on `02-chain` — `sc-tendril-fx`,
`sc-coldiron-temper-fx`, `sc-ironhail-fxout`, `sc-lodestone-b205-fx`, `sc-widowmaker-b1075-fx` and the newest,
`sc-widowmaker-fxout` (04fdd2e2daa17c26): the four stages apply to each, and the change they make there is
line for line the change on `sc-tendril-t3` (the sorted diff lines hash alike, 98dc422a898f5043); and at the
close, on the two tips carried since, `sc-oracle-fx` (15cf62f96f72653a) and `sc-angelus-b9-fx`
(85b8af63055d1108), the same change set again (`runs/compose3.txt`). On the stack
where Lightkeeper and Widowmaker are both off the nova, the builder reports "the nova's tail kept, untouched,
for no other relic" and builds (§0, what is retired). compose2 ran on the stages 1-5 builder (78501578c5773570);
the final one writes the same four links byte for byte, and **compose6** (§5, 0 FAIL) runs stages 1, 2, 3, 5 and
6 with the three builders in progress since (Aureole, Heartwood, Spellbreaker), both ways and in two stacks, and
on the line's four newest tips up to `sc-lightkeeper-fxout` (088189f3517b6f11): stages 1-5 make the change set
98dc422a898f5043 on every one, and stage 6 alone bc494860e7c77ee9 on every one.

## 0. What this build stands on

- **The relic** is Censer as shipped: the sanctified warhammer (reach 76, width 26, artW 54, dmg 28.77,
  spin 1.6, spin, mass 5.0, knockMul 2.3; onHit smite 1) and its nova, Consecration (charge 15, radius
  300, dmg 12, apply smite 3, knock 300). The builder asserts the profile, the channel and the nova block,
  by content, before it touches them. Names kept (design §4): CENSER / CONSECRATION; the card is the
  design's 70 characters, `Its blows make holy ground: foes on it are smitten, and it heals there`.
- **The shipped relic's rate on the base, the reference** (`relic_rate`, both sides, two blocks, 1480
  fights, `runs/ref_shipped_rr_*`): **50.1%** (49.5 / 50.8; side A 50.5, side B 49.7), mean 53.9s. This is
  "the shipped rate" the blade is settled to: the design's 50.3 is the nova on Chromium 141.
- **The charge is 14.** The design names none: its lab priced every arm at the harness default, 16 on the
  lab's clock (`P` in `v78/runs/holyground_*.json`). Rick's batch ruling converts it. Measured for this
  fighter by a census copy of `ult_overlay.py` that counts, before each lab step, the frozen ones
  (`m.hitStop > 0 || m.latch || m.splitHold`; `runs/holy_census.py`; 660 fights, block 2207,
  `runs/s0_census_2207`): **on arm C 11.08% of the lab's steps are frozen (12.54% inside windows, 10.13%
  outside), so the lab's 16 is the engine's 14.23, and 14** (arm B: 10.93%, 14.25). The census copy
  reproduces the lab's own arms B and C to the fight (48.8 / 57.4, the unmodified lab's block 2207). The
  shipped 15 was the nova's and goes with it.
- **The window is 8 seconds.** The prose says only "for a duration"; the lab priced every arm at `P.dur` 8,
  and the build takes it, on the window tickers' clock (the batch's convention; §2 measures what that
  clock makes of it: ~9.2s of match time).
- **The lab is `overlays/holyground.js` through `ult_overlay.py`**, with no `--cell` (a redesign): arm A is
  the relic with its ultimate suppressed, SHIP the nova live, B the ground and the smite, C with the heal.
  **Flagged: the lab's `tickDmg` defaults to 2**, the tick damage the design dropped (§3: "The tick's damage
  is dropped ... (taken)" at 0). Every lab arm here passes `--P tickDmg=0`, the brief's own stage-0
  command. Every other default is the settled number (groundR 90, groundLife 8, tickCd 0.5, blessCd 1.0;
  plantCd is arm D's, not taken).
- **Readings** (in the builder's docstring):
  1. **The landing point is the struck ball at the hit** (§4: "the FOE's position at the hit"; §1: "the
     ground where it landed"), taken in `resolveHit` beside `self.hits++` — the count the lab watched
     (`me.hits` rising) — for the hammer's own blows (`mul === undefined`) while the window is open. The lab
     read the foe after the step, which is the same point (nothing moves a ball between `tickHits` and the
     step's end). A blow on a Twinshade shade consecrates the shade's ground; the lab, which never sees a
     shade, planted at the opponent. The probe counts them: 21 of 2244 discs on the final link, all against
     Twinshade.
  2. **The ground acts only while its caster's window is open** (the lab: every test sits after `if
     (!open) return`, and every priced number — the gates' ~4 smite and ~2.6 blessing a cast — is a window
     count). A disc lives 8s from its blow and does not move; after the window closes it stands inert until
     it expires. **A disc still alive when the next window opens acts in it**: the lab's list is the fight's,
     filtered by age only. At the lab's 16 against 8 + 8 that could never happen; at the engine's 14 it can,
     and does at 21% of casts (the probe: 292 of 1390 casts on the final link open on 336 standing discs of
     their own; 2.9% of window frames have one). **The prose's other reading** — "an enemy standing on holy
     ground is smitten for as long as it stands there" as the ground working for its whole life, window or
     not — is a different relic: the scratch variant `wholelife` reads **71.75** (73.0 / 70.5) on the lab's
     field at 28.77 against the built 60.9 (§2; Rick's, §6).
  3. **The foe is on the ground when its ball touches a disc**: its centre within groundR + R (the lab's
     `on`). The prose says nothing finer for the foe ("an enemy standing on holy ground").
  4. **The caster is on the ground when its CENTRE is within groundR of a disc** (§4, explicit: "while the
     caster's centre is within a disc"). The lab tested the caster's ball like the foe's (groundR + R). The
     explicit prose is taken; the difference is measured (§2): the lab's test reads **62.65** on the lab's
     field against the built 60.9, and 2.67 blessings a cast in the lab against the built 2.45 (the lab's field, both blocks). Rick's (§6).
  5. **The ground is its caster's**: a disc carries its side, which names its caster for the purge (its
     `groundLife`) and for the probe, and only its own caster's window reads it (the lab had one caster).
     There is no mirror match: `Match` refuses a relic against itself, so no test can tell this side test
     from none (the stage-5 review's mutant mx4-side behaves identically in every legal match).
  6. **The cadences**: the smite once per 0.5s, the blessing once per 1.0s; each cooldown is 0 at the cast
     and runs down through the whole window, on the ground or off (the lab's `cd -= dt` every open frame),
     so a foe that steps on after a gap is smitten on that frame.
  7. **`apply`'s source is a side letter** for both (the engine's contract; the lab passed the Fighter).
     Smite reads it: a fatal smite tick's beat is attributed by `st.src` — with the lab's Fighter it would
     have been attributed to side B, the foe itself when Censer is side A. Presentation (the director's);
     no fight moves. Blessing reads none.
  8. **The tick's damage is dropped** (§3, taken). The ground's only writes are smite on the foe and
     blessing on the caster: no damage, no knock, no move, no beat, no hit stop, no rng. Smite's own dps
     and its fatal-tick beat are the status's existing machinery (`tickStatus`), so the ground files no
     beat of its own (a side channel that cannot kill).
  9. **The window closes on its clock or either death** (the lab's). No wither and no wait: the charge and
     the window run on one clock and 8 < 14, so a cast cannot come under a standing window.
  10. **The target is the opponent**, never a Twinshade shade (the lab's `foe`). The probe diffs every shade
      field by field around every window frame.
  11. **The ground is on the match** (§5: "`m.holyGround[]` in (discs with x, y, t0)"), each disc {x, y, t0,
      side}; `t0` is read on `m.holyT`, the ground's own clock, the window tickers' (it stops in a hit stop),
      so a disc's 8s are 8 seconds of the window clock. "The hall's close does not clip it": nothing removes
      a disc but its age.
  12. **Nothing else: the hammer swings as ever.** The builder refuses an insert that draws the rng, takes
      the ultFx slot, writes the shared weapon row or a shared module table (STATUS, CONFIG, AFFINITIES,
      WEAPONS, SHAPES, by name or through an alias), beats, stops, hurts, knocks, moves, heals directly,
      stuns, pins, burdens or lays any status but smite and blessing.
- **Names:** the kind is `"holyground"`, the fields `ultHoly` / `holyTally` on the fighter and `holyGround`
  / `holyT` on the match, the ticker `tickHolyGround`: none is in the base or in any in-progress builder.
- **The clock:** the window, both cooldowns and the discs' lives run on the window tickers' clock, which
  stops in a hit stop. The lab ran them all through freezes (§2).
- **What is retired.** The nova's numbers (radius 300, dmg 12, apply smite 3, knock 300) and its card leave
  Censer's row and its kind becomes `"holyground"`. **The nova itself stays:** on this base Widowmaker's
  Exsanguinate and Lightkeeper's Bulwark are `kind:"nova"` and the generic tail of `fireUlt` is theirs;
  the holyground branch returns before it. Both of their own redesigns (v106, v107) take them off the nova
  too, so once all three are carried no relic casts it; the tail is shared machinery and stays (the builder
  reads who is still a nova and never refuses on it). **The nova's presentation keyed on the id is retired at
  stage 6** (§5), as design §5 asks ("nova's field spec out"): ULTSIG `censer`, the two
  `u.w === "censer"` draw branches (the glyph ring and the smoke, drawn through stage 5 for the cast record's `life` 1.6 at the
  300 fallback radius), the `life` map's 1.6, the fx.js SPECS `censer` burst (§5) and the rune-crack
  fallback voice (Censer's own two arms now stand before it). Nothing in the simulation reads any of it
  (engine_ab, §4 and §5e).

## 1. Stages 1-3

Stage 1 replaces the nova block in Censer's row with the holy ground's, stubbed at charge 1e9 (the old cast
unreachable, the new never reached), so the relic is arm A. Stage 2 adds `ultHoly` / `holyTally` after
`vineTally`, `holyGround` / `holyT` on the match after `sparks`, the `kind === "holyground"` cast branch
before the tendril's (it opens `{t 0, dur 8, cd 0, bcd 0}` and returns), the plant in `resolveHit` after
`self.hits++; self.dealt += dmg;`, `tickHolyGround` after `tickTendril` (after every ball has moved this
frame, before `tickHits`; the method itself sits before `tickWinnow`) and the charge 14, with the heal
written at 0 and inert. Stage 3 is the heal, bless 1. Every anchor is a stable line other builds keep, and
every edit re-emits its anchor, so another relic's insert on the same line applies in either order
(`compose2.txt`).

`tickHolyGround`, each live step: `holyT += dt`; every disc whose age on `holyT` has reached its caster's
`groundLife` goes; then, for a caster whose window is open (the clock, or either death, closes it): both
cooldowns run down by dt; the foe's centre within 90 + R of one of the caster's discs and the smite's
cooldown clear: smite +1 (source the side letter), cooldown 0.5; the caster's centre within 90 of one of its
discs and the blessing's cooldown clear: blessing +1, cooldown 1.0.

## 2. Stage 0 and the stages against it — the window clock and the heal's test, measured

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic censer --mech overlays/holyground.js
--arms A,SHIP,B,C --P tickDmg=0 --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights an arm a block,
Chromium 151.0.7922.34 (`runs/s0_ASBC_*`). The foes are the design's 33 (the 34-relic roster less the donor,
which here is the relic itself). The built links run `--arms SHIP` on the same foes and seeds
(`runs/built_*`).

```
                           published 141 (330)    lab on 151 (1 / 2)    BUILT (1 / 2)             pooled
A    no ultimate           38.5                   38.2 / 39.8           stage 1: 38.2 / 39.8      identical, fight for fight
SHIP the nova              50.3                   50.0 / 49.8           (the base)
B    ground + smite        54.2 (tickDmg 2)       48.8 / 52.0           stage 2: 51.1 / 52.1      51.6 (lab 50.4)
C    + the heal            57.9 (tickDmg 0)       57.4 / 59.7           stage 3: 61.5 / 60.3      60.9 (lab 58.6)
```

**Stage 1 is arm A fight for fight** on both blocks: every foe's rate and every blow count identical
(`runs/stub_vs_A.txt`).

**Published against 151.** On the design's own seeds (330 fights) on `sc-trunk`, 151 reads A 37.9, SHIP 51.5,
B (tickDmg 2) 51.2, C (tickDmg 2) 60.0, C at tickDmg 0 56.4, against the published 38.5 / 50.3 / 54.2 / 65.5 /
57.9 (`runs/repro_trunk_*`). On this base the same arms read A 39.0, SHIP 49.9, B 50.4, C 58.6 (tickDmg 0).
**The brief's stage-1 gate "relic ~54% at 28.77" is arm B WITH the dropped tick damage on 141**; without it,
on 151, the lab itself reads 50.4 and the build 51.6. Its stage-2 gate, "relic ~58%", holds in the lab (58.6)
and reads 60.9 built (below).

**The mechanism on the lab's own fights** (the probe run on the lab's field: the 33 foes, side A, the lab's
seeds, the fights the SHIP arm plays; `runs/probe_labfield_*`; both blocks pooled):

```
                        casts  discs/cast  foe on ground  smites/cast  foe smite stacks  blessings/cast  blows in / out   win
lab B (both blocks)     2.87   1.31        19.66%         3.99         1.90              -               3.99 / 6.00      50.4
built stage 2           2.89   1.54        19.19%         4.26         2.00              -               4.46 / 5.37      51.6
lab C                   2.97   1.32        19.87%         4.04         1.89              2.67            4.17 / 6.17      58.6
built stage 3           2.98   1.55        19.27%         4.25         2.00              2.45            4.61 / 5.50      60.9
```

On those fights the probe's Censer wins exactly what the built links' SHIP arm reads (51.1 / 52.1 and
61.5 / 60.3), and reads 9/9 on each. The charge conversion holds: 2.89 / 2.98 casts a fight against the lab's
2.87 / 2.97. **The designed gates**: "~1.3 discs a cast" — the lab 1.32, the build 1.55; "foe on
ground ~20% of window frames" — 19.9 / 19.3; "~4 smite a cast" — 4.04 / 4.25; "~2.6 blessing a
cast" — 2.67 / 2.45. The build lands about a tenth more blows in a window (the window clock, below), and
plants a disc for every one of them; **the lab plants none for a killing blow** (`ult_overlay` counts it in
"hits in" but closes the window before the overlay's frame, so the lab's discs a fight, 3.94 on arm C, sit
under its 4.17 blows in windows; the built discs are its blows exactly). The window clock and that count are
the build's sixth more discs a cast (1.55 against 1.32); the disc at a kill acts on nothing.

**The gap, attributed.** Stage 2 reads 1.2 over arm B, inside the noise (a pooled rate of 1320 fights has a
standard error of about 1.4; a difference about 1.9). Stage 3 reads 2.3 over arm C. Controls, each a scratch
copy of a built link with one thing changed (`runs/ctl_variant.py`), or the lab with one number changed (both
blocks, the lab's field; `runs/ctl_*`, `runs/lab918*`):

```
                                                                ground + smite (B)     + the heal (C)
the lab                                                         48.8 / 52.0   50.4     57.4 / 59.7   58.6
the build (the window clock; the heal on the caster's centre)   51.1 / 52.1   51.6     61.5 / 60.3   60.9
the build on the lab's clock (the ground ticked through freezes) 47.3 / 48.8  48.0     56.4 / 58.0   57.2
the build with the lab's heal test (the caster's ball)                                 62.7 / 62.6   62.65
the lab at the engine's window (dur 9.18)                       48.6 / 52.9   50.75    62.7 / 64.4   63.55
the lab with every clock of the ground x1.148 (dur, life, cds)  49.8 / 51.2   50.5     61.2 / 63.8   62.5
the build with the ground working its whole life (wholelife)                           73.0 / 70.5   71.75
```

The engine's 8s are 8 seconds of the window clock; 13.0% of window steps are frozen (the probe), so a window
is ~9.2s of match time where the lab's was 8 step-seconds (1 / (1 - 0.129) = 1.148), and the hammer lands
about a tenth more blows in it (4.61 against 4.17 a fight on the lab's field, both blocks), so it lays more ground.
**Two things move stage 3, in opposite directions, and nothing is mis-built:**
1. **The window clock, about +3.5 to +4.** The build put back on the lab's clock reads 57.2 (the lab 58.6).
   The lab given the engine's clock on every number of the ground — the window, the disc's life and both
   cooldowns x1.148 — reads **62.5**, and the build with the lab's heal test (the same relic on the engine's
   clock) reads **62.65** beside it. At stage 2 the same clock measures +0.1 (the lab) to +3.6 (the build),
   inside the noise of a smite that deals nothing on its own.
2. **The heal on the caster's centre (reading 4), about -1.75.** The build with the lab's ball test reads
   62.65 against the built 60.9, and blesses 2.67 times a cast in the lab against the built 2.45 (the lab's field, both blocks).
The net is the +2.3 measured. The engine's convention and every designed number are kept; stage 5 settles
the blade on the built relic.

## 3. The probe (`censer_probe.py`, one check per sentence, read inside the hooks)

It wraps `step`, `tickHolyGround`, `fireUlt`, `tickCharge`, `tickWeapon`, `tickHits`, `resolveHit` and
`tickStatus`, puts an accessor on Censer's `hp` for the length of each fight, plays Censer against every
other relic from both sides (444 fights; `--foes/--sides/--seedstep` give the lab's field), and REBUILDS the
ground on every window frame from the frame's own discs, balls and cooldowns: it ages the discs on the
ground's clock and says which discs are left, whether the foe must be smitten and whether the caster must
be blessed, then compares that with what the ticker did. **The design's numbers are pinned from the
builder's `ULT`** (dur 8, groundR 90, groundLife 8, tickCd 0.5, smite 1, blessCd 1.0, bless 0 or 1, charge
14) and each is checked by its own sentence's check; the per-frame models read the row, so a drifted number
fails once, where it belongs. "A check that never ran is not a pass": every check prints what it read. The
checks:

- [1] **"For a duration" — the window on the window clock**: a live step moves the window's clock by exactly
  dt; a frozen step (hit stop, latch, split hold) leaves the window, the ground and `holyT` exactly as they
  were; the ticker runs exactly once on every live step and never on a frozen one; `holyT` moves by exactly
  dt; the window closes on its clock or either death, never early, and every clock-closed window is the same
  number of live steps (960); no cast under a standing window; only Censer carries `ultHoly` / `holyTally`.
- [2] **"every blow the hammer lands consecrates the ground where it landed"**: a Censer blow (its own blade,
  `mul` undefined) landed with the window open pushes exactly one disc `{x, y, t0, side}` at the struck ball
  as it stood at the hit, `t0` the ground's clock, `side` the caster's (JSON-exact); a blow outside the window
  pushes none; no disc appears anywhere else (the ground's list is reconciled against a model every step).
- [3] **"a circle of holy ground that lasts"** (r 90, 8s, "does not move", "the hall's close does not clip
  it"): the row's groundR / groundLife are the builder's; a disc never moves or changes; exactly the discs
  whose age on `holyT` reached their caster's life go, in the ticker, and nothing else removes one.
- [4] **"An enemy standing on holy ground is smitten"**: on a window frame, the foe's centre within groundR + R
  of one of the caster's live discs and the cooldown clear → smite exactly as `apply("smite", 1, side)` leaves
  it (stacks to the cap, t the status's 3.2, src the side letter), the cooldown 0.5; otherwise no smite, the
  foe's smite untouched and the cooldown run down by exactly dt.
- [5] **"Censer standing on holy ground is healed"**: the caster's centre within groundR of one of its live
  discs and its cooldown clear (bless > 0) → blessing exactly as `apply("blessing", 1, side)` leaves it, the
  cooldown 1.0; none otherwise and none at bless 0. **And the blessing is the heal**: an accessor on Censer's
  hp fails any rise outside its own status tick (bounded there by hps x stacks x dt), except the death clamp
  (`checkEnd`'s `Math.max(0, hp)`); the ticker's own frames are [6]'s.
- [6] **nothing else on a ground frame** ("No damage, no knock, no beat"): no hurt, beat, rng draw or hit stop
  in the ticker; a whole-state diff (the status table split key by key) of both fighters, the match (every
  array by length, identity and content; a Twinshade shade field by field) and the shared tables STATUS,
  CONFIG and AFFINITIES, before and after every window frame; the only changes allowed are the caster's
  `ultHoly`, `holyTally` and blessing, the foe's smite, and the match's `holyGround` / `holyT`. With no window
  open, a compact read of both balls (position, velocity, hp, shield, stun, pin, charge, statuses) and the
  shots. Once a fight, WEAPONS, SHAPES and the three against the run's start.
- [7] **"the nova is out"**: a Censer cast opens exactly `{t 0, dur, cd 0, bcd 0}` and writes nothing else
  after the engine's shared prologue (snapshotted when the prologue assigns `ultFx`, its last statement
  before the kind branches): only the caster's `ultHoly` and a `holyTally` whose casts went up by one.
- [8] **"the hammer swings as ever"**: Censer's turn on every live step (w.spin x spinMul x dt, rebuilt from
  its definition, locked while stunned; reachMul 1), the blade segment and hit test in `tickHits` (the
  cooldown, the stun, R + width / 2, the hit point), and every blow it lands rebuilt from the captured crit
  and jitter draws: the damage (dmgMul rebuilt from its definition, the curse echo added; the damage a blow
  dealt must be a whole number to 1e-6 of float residue, and the rebuilt one), the knock, the foe's
  hitstun, the hit stop (a ward's own shatter allowed), the onHit smite on the foe's statuses — in the window
  and out. Blows into Bulwarden's wall are exempt (counted).
- [9] **the charge** (Rick's batch ruling): Censer's charge moves by exactly dt on each of its charge ticks,
  and a cast comes exactly when it reaches the builder's 14 and spends it.

Results (every relic, both sides, 6 seeds, 444 fights, unless named; `runs/probe_*`):

```
                                         fights checks  casts  discs smites  bless  foe on   stk  blows in/out    win  frozen
                                                       /fight  /cast  /cast  /cast       %              /fight      %   % win
stage 2  sc-censer-ground                   444    9/9   2.92   1.55   4.41   0.00   20.20  2.02   4.53 / 5.39   53.8    12.8
stage 3  sc-censer-consecration             444    9/9   3.03   1.57   4.45   2.44   20.61  2.03   4.77 / 5.57   62.8    13.0
stage 5  sc-censer-consecration-b25.5       444    9/9   3.13   1.61   4.68   2.60   21.29  2.02   5.05 / 5.49   50.5    13.1
stage 2, the lab's field, 2207              660    9/9   2.87   1.56   4.28   0.00   19.24  2.03   4.48 / 5.32   51.1    12.9
stage 2, the lab's field, 2317              660    9/9   2.90   1.53   4.23   0.00   19.14  1.98   4.43 / 5.43   52.1    12.8
stage 3, the lab's field, 2207              660    9/9   2.97   1.57   4.28   2.48   19.36  2.02   4.66 / 5.44   61.5    13.0
stage 3, the lab's field, 2317              660    9/9   2.98   1.53   4.23   2.42   19.18  1.98   4.56 / 5.57   60.3    12.9
```

Every probe number in §0-§4 is from the stages 1-5 probe (`censer_probe.py` 5d78670c3787524e; stage 6's,
c588b606b1fc7741, prints every one of its lines and counters alike on the final link: §5e) but the four
lab-field runs, which were read under the one before it (07fdcdb0ff9fefa9); the only change between the two
cannot move a run in which [3] passes (below), and the final link reads the same under both, json and text
to the byte (`runs/probe_07fd/` keeps the earlier runs).

- **The final link, `sc-censer-consecration-b25.5`: 9/9** (444 fights). 3.13 casts a fight; a cast lays 1.61
  discs, smites 4.68 times and blesses 2.60 times; the foe is on the ground 21.3% of window frames, at 2.02
  smite stacks; Censer wins 50.5% of these fights. Every clock-closed window is the same 960 live steps
  (1149 of them; 70 closed by a death); 13.1% of window steps are frozen, so a window is ~9.21s of match
  time. What each check read, so none passed by not running: 2244 discs planted and 2436 blows outside a
  window planting none; 1545 discs expired, each at its life; 6505 smites and 3619 blessings rebuilt, and
  1.21 million window frames rebuilt with no smite and 1.22 million with no blessing; 1.22 million window
  frames diffed whole; 346,137 frozen steps unchanged; 4613 blows rebuilt (67 into Bulwarden's wall exempt); 2.72 million charge ticks and 1390 casts
  each at 14; 1.05 million of Censer's blessing heal steps bounded. Counted, not checked: 292 of 1390 casts
  open on 336 standing discs of their own (reading 2); 21 discs at a Twinshade shade (reading 1).
- **Stages 2 and 3: 9/9 each** (444 fights). Stage 2 blesses 0 times ([5]: "none at bless 0") and wins 53.8% of its 444 fights;
  stage 3 blesses 2.44 times a cast and wins 62.8%.
- **On the lab's field** (the four `probe_labfield_*` runs, 660 fights each): 9/9 each, and each wins exactly
  what the built link's SHIP arm reads on those fights (51.1 / 52.1, 61.5 / 60.3).
- **Two probe fixes, neither a build change.** The first run on the final link (`runs/probe_b25.5_v1.txt`)
  failed [8] on 2 of 4611 blows: the rebuilt hit stop 6e-17 off, because the probe read a blow's damage as
  the raw float difference of `dealt`; it now reads it as the whole number it is and fails one that is not.
  The first run of mutant m3 (discs purged at 90% of their life) failed [3] and also [4] and [5] (34 and 31
  frames): those two rebuilt the ground from the model's own purge, so a wrong purge leaked into them. They
  now read the ground as the ticker left it, and [3] alone owns the purge; when [3] passes the two are the
  same list, disc for disc.

**Controls: ten scratch mutants of the final link** (`runs/mutants.py`, hashes in `runs/mutants_hashes.txt`;
`runs/probe_mut_<m>.txt` on 3 seeds, 222 fights, against the final link's own 3-seed run, 9/9,
`runs/probe_mut_base_3seeds.txt`; `runs/fightdiff_mut_<m>.txt`, Censer against every relic, both sides, 3
seeds, 222 fights, the final link's Censer winning 111). Each changes fights, and each fails its own check
and only that one:

```
mutant     sha16             breaks                      how                                                                probe (3 seeds)                   fights differ  Censer wins
m1-window  3f76a11106b435e5  [1] "for a duration"        the window 9s, not the builder's 8                                 8/9  [1] fails 678185x            192/222        111 -> 121
m10-clock  a260fb1bb397e97b  [1] the window clock        the ground's ticker also run on hit-stop steps (the lab's clock)   8/9  [1] fails 589381x            211/222        111 -> 99
m2-plant   706535e5016b63ce  [2] "where it landed"       the disc planted under the caster, not the struck ball             8/9  [2] fails 2260x              214/222        111 -> 133
m3-life    40e3b58173e2ce3e  [3] "that lasts" (8s)       a disc goes at 90% of its life                                     8/9  [3] fails 1550x              85/222         111 -> 111
m4-smite   8b8edb51c9464000  [4] "is smitten" (0.5s)     the smite's cooldown 20% short (0.4s)                              8/9  [4] fails 3686x              161/222        111 -> 106
m5-heal    2e698abff28b8333  [5] "Censer ... is healed"  the caster's ball, not its centre (the lab's test)                 8/9  [5] fails 54764x             168/222        111 -> 122
m6-dmg     dd1c25d5439f558b  [6] "no damage"             a smite tick also hurts 2 (the lab's rejected tickDmg)             8/9  [6] fails 6150x              207/222        111 -> 132
m7-nova    a8b7c3fdcc0bf5fa  [7] "the nova is out"       the cast still lays the nova's 3 Smite                             8/9  [7] fails 696x               220/222        111 -> 133
m8-blade   16679c359aa2c29b  [8] "the hammer as ever"    the hammer 10% heavier in the window                               8/9  [8] fails 1093x              221/222        111 -> 118
m9-charge  d7da52d52df12fa3  [9] the charge (14)         the lab's 16, unconverted                                          8/9  [9] fails 1525477x           222/222        111 -> 103
```

- Each mutant is ONE edit of the final link (`runs/mutants.py` holds the before and after of each), and each
  changes fights: between 85 and 222 of the 222 (`fightdiff`). m3's discs gone 0.8s early move 85 fights and
  not the win count; the others move it by 5 to 22 wins.
- Two sentences are covered twice: [1] by a longer window (m1) and by the lab's clock (m10, the ground's ticker
  also run on hit-stop steps: "the ground's ticker ran on a frozen step"), and the heal by the lab's own ball
  test (m5), which fails [5] on the frames where the caster's ball but not its centre is on a disc.
- m1 and m9 are caught by the numbers the probe pins from the builder ("the window's dur 9, the builder's 8";
  "the row's charge is 16, the builder's 14"): a drifted number fails once, in its own sentence's check,
  and the per-frame models, which read the row, stay quiet.
- The unmutated final link reads 9/9 on the same 3 seeds (`runs/probe_mut_base_3seeds.txt`), so each failure
  is the mutant's.

## 4. Stage 5: the blade — 25.5, the shipped rate

Both sides (`relic_rate.py`: each seed from both sides; every other relic a foe, 10 seeds a foe a side,
740 fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`, `runs/stage5_table.txt`):

```
                                       blade   2207   2317  pooled  side A  side B  mean s     n
the shipped nova (the base)            28.77   49.5   50.8   50.14    50.5    49.7    53.9  1480
Consecration, stage 3 --set               24   43.8   46.6   45.20    45.3    45.1    58.3  1480
Consecration, stage 3 --set             24.5   47.0   50.1   48.58    47.7    49.5    57.9  1480
Consecration, stage 3 --set               25   49.9   52.6   51.22    51.8    50.7    57.5  1480
Consecration, stage 3 --set             25.5   49.5   49.7   49.59    50.9    48.2    57.2  1480
Consecration, stage 3 --set               26   52.7   52.6   52.64    54.2    51.1    57.2  1480
Consecration, stage 3 --set             26.5   53.9   53.2   53.58    54.7    52.4    57.0  1480
Consecration, stage 3 --set               27   53.9   56.1   55.00    55.9    54.1    56.7  1480
Consecration, stage 3 as built         28.77   58.9   59.5   59.19    59.6    58.8    55.4  1480
sc-censer-consecration-b25.5, no set    25.5   49.5   49.7   49.59    50.9    48.2    57.2  1480

the line through the seven: -23.50 + 2.92 x blade; the shipped 50.14 at 25.26, 50% at 25.22
the measured point nearest the shipped rate: 25.5 (49.59, -0.54); nearest 50%: 25.5 (49.59)
residuals: 24 -1.25  24.5 +0.67  25 +1.84  25.5 -1.24  26 +0.35  26.5 -0.16  27 -0.20
```

- **The knob: none moved.** The design gives the build no knob to move before the blade.
- **The target is the shipped rate, the design's own** (§3: "at 57.9% against a shipped 50.3 the blade comes
  from 28.77 to about 26.5"; §5: "Stage 3 — the blade, wide on 151 at 26 / 26.5 / 27 to the shipped rate").
  The shipped rate on 151 is the nova's **50.1%** on these same fights.
- **The brief's three read over it**: 26 → 52.6, 26.5 → 53.6, 27 → 55.0. The design names no knob, so the grid
  was **widened down inside "the hammer row 20–29"** (§3's own range for this blade) and said here: 25.5,
  25, 24.5, 24, a fixed grid read after the three, both blocks each, no bisection. **Blade 25.5 is the measured
  point nearest the shipped rate: 49.6% (-0.5 on the unrounded rates, 49.59 against 50.14)**, side A 50.9,
  side B 48.2. The line through the seven puts the shipped rate at 25.26; 25 reads 51.2 (+1.1) and 26 52.6.
  The grid is noisy at 1480 fights a point (25 reads 1.6 over 25.5; residuals within ±1.9 of the line, a
  point's standard error 1.3), and it does not touch the choice: 25.5 is the nearest measured point either
  way.
- **Rick's other choice, 50%, is the same point**: on 151 the shipped nova reads 50.1, so the 50% crossing
  (25.22 on the line) and the shipped rate (25.26) are 0.04 of a blade apart, and 25.5 is the measured point
  nearest both. The design's "about 26.5" was priced at 141 on the lab's clock; the built relic reads over
  the lab by the window clock (§2), so the blade lands a point lower.
- **The built link is the measured relic:** `relic_rate` on `sc-censer-consecration-b25.5` with no knob set
  reproduces the `--set dmg=25.5` runs exactly on both blocks (49.46 / 49.73%, side A and side B, every foe,
  the mean duration to the digit; `runs/cmp_rr_b25.5.txt`).
- **The holy ground lengthens Censer's fights**: 57.2s mean against the nova's 53.9.

**The ladder at 25.5** (40 fights a foe, `runs/ladder_b25.5.txt`), beside the shipped nova on the same
fights: by type greatsword 70% (shipped 65), flail 50 (44), twinblade 48 (50), warhammer 46 (55), scythe 45
(48), bow 35 (39). Worst **Gloamwire 22.5%** (shipped 20), Ironhail 27.5 (35), Aureole and Farwarden 32.5
(32.5); best Axiom 87.5 (72.5), Heartwood 82.5 (77.5), Nightfell and Oathwound 70. The largest gains:
Paradox +22.5, Thornshear +17.5, Axiom +15, Portcullis +12.5, Gravemourn +10; the largest losses: Ironwood
-20, Shroudmaul -17.5, Lastlight, Starwarden and Vinesower -15. Holy ground punishes a foe that stays where
it was hit and heals a hammer that stands its ground; the bows that stand off (Gloamwire, Ironhail, the bow
row at 35%) seldom step on it. **The type spread (35 to 70) is item 12/32, Rick's.**

### 4a. The gates on the final link

- **engine_ab `sc-tendril-t3` → `sc-censer-consecration-b25.5`, the 37 others (every base id but Censer), n=6:
  3996/3996 identical** (`runs/engine_ab37_b25.5.txt`; 37/37 distinct winners, 3996 distinct seeds,
  20.8-111.2s; the ids are `runs/ids37.txt`). The redesign moves no other relic's fight; Censer's own differ by
  design, so its id is not passed.
- **verify --n 40 on the final link (38 relics, 703 pairings, 28120 fights): 10/13** (`runs/verify_b25.5.txt`),
  the same three reds as the base's own run (`06-docs/v101/runs/verify_t3.txt`, 10/13) and on the same
  pairings: "both sides can win every matchup" on Heartwood v Twinshade 0/40 and Heartwood v Bindweed 0/40
  (neither is Censer's), and the two clock bands (pairing means 38.6-100.0s; overall 61.0s against the base's
  60.8), red on every link since the minute pace. **Censer 51.7%** (the shipped nova 50.7% in the base's run;
  verify plays it in place, both sides by pair order). Every relic in 30-70% (Heartwood 30.6 .. Gloamwire
  63.3); no other relic's rate moves more than 0.7 against the base's run.
- **tip_audit**: identical to the base's but for the file name (`runs/tip_audit_{base,b25.5}.txt`; the one
  "MISSING" is Burn's `feed`, the base's own). The ultimate's card is checked by the builder: the design's 70
  characters.
- **chain_audit** `--relic sc-censer-consecration-b25.5 --tip sc-censer-consecration-b25.5 --builder
  censer_build.py`: **ALL 10 INSERTS SURVIVE** (`runs/chain_audit_b25.5.txt`). **Control:** the same relic
  against the base as the tip loses all 10 and exits 1 (`runs/chain_audit_b25.5_ctl_base.txt`).
- **compose** (`runs/compose2.txt`, 0 FAIL): above, under the link table.

## 5. Stage 6: the picture and the voice — `sc-censer-consecration-b25.5-fx`

Design §4 ("Picture", "Sound") and its §5 "Stage 4 — picture, voice, carry", this batch's stage 6. Picked on
measurements under Rick's "you pick i overrule" by two labs run in parallel (the picture lab's scratch,
`ce_rows.py` a31bb4e11181e3c1, and `tools/censer_voice_lab.py` 845c809a8ebae571), and built as
`censer_build.py --stage 6` on the final link (stage 5's b25.5): **thirteen anchored edits (voice 3, picture
10)**, byte-exact to the labs' own row files (voice `rows_final.json` 63c842fa690c5f02, picture
5133d7afb3acb9e9; copied as `runs/stage6_voice_rows.json` and `runs/stage6_picture_rows.json`). The reports the
two labs returned, as the orchestrator relayed them, are the files (their first 4999 and 7000 characters are
the files' own JSON, character for character; a one-character change fails the check:
`runs/stage6_check_inline.txt`).

```
sc-censer-consecration-b25.5.html          stage 5  the blade (the base of stage 6)                     56c49ad3f0ccb3aa
  -> sc-censer-consecration-b25.5-fx.html  stage 6  the picture and the voice (presentation)          3d68c7648a9cb3a8
```

- **The rows, reproduced** (`runs/stage6_gen_s6.txt`; the generator is `runs/stage6_gen_s6.py`, the pattern's:
  rows == files, the stamps, no nested anchor, merge by anchor, a `--stage 6` that refuses to run twice and
  scans S6 for `ultFx`): the picture rows alone give the picture lab's stamp, **b3f790861677e2bd** (its
  `ce-final.html`, byte for byte); the voice rows alone the voice lab's page, **6af8bc7cac4bf257**
  (`sc-censer-voice.html`); both sets, either order, **3d68c7648a9cb3a8**, the picture lab's co-apply and the
  fx link. No two rows share an anchor, so none is merged; no row's anchor sits inside another row's anchor
  or code, and no two anchors' spans overlap. **Nine re-emit their anchor and four replace it**, all four
  Censer's own: the nova's two art branches (the glyph ring, the smoke), `ULTSIG.censer`, and the life map's
  narrowest token `censer: 1.6,` (Aureole's entry on the same line is left to its own build).
- **Composition.** The Sfx row goes BEFORE the shared rune-crack fallback, which it re-emits unchanged, so the
  11 other relics that still fall through keep it and another relic's arms anchored there apply in either
  order; the two voice calls on the sim path ride on stage 2's own counts (`holyTally.discs++`, `T.bless++`);
  the picture's fields follow stage 2's fields; its calls and methods sit beside shared lines
  (`tickPresentation`'s first call, `tickWinnow`, `drawTree`, `drawSunTop`, `drawMotes`) and re-emit them.
  **compose6** (`runs/stage6_compose6.txt`, 0 FAIL): stages 1, 2, 3, 5 and 6 with the three other builders in
  progress (Aureole at its stage 5, Heartwood and Spellbreaker at their stage 3, their last today), both ways
  and in two stacks; and on the line's four newest tips on `02-chain` — `sc-widowmaker-fxout`, `sc-oracle-fx`,
  `sc-angelus-b9-fx` and the newest, `sc-lightkeeper-fxout` (088189f3517b6f11): on every one the change set of
  stages 1-5 is t3's (98dc422a898f5043) and the change set of stage 6 alone is t3's (bc494860e7c77ee9). The
  picture lab also carried its rows with the voice rows onto 17 tips and scratch pictures, every order equal
  (`runs/stage6_picture_order.txt`).
- The picture sheet is `05-reference/v109/censer-picture-sheet.png` (5aa8c219f8239251, 2200x3195); the voice
  lab's wavs are `05-reference/v109/censer-*.wav` (40 files, raw level; gitignored).

### 5a. The picture

Every number here is the picture lab's: headless Chromium 151 at 540x960 with the post chain on (m2: 10
fights, 130 frames, white, dark and ordinary foes), on its shipped-look page (the rows, with the nova's
`SPECS.censer` taken out of the inlined `fx.js` as the carry will: 9eb071b0e42df058).

- **The disc is the simulation's disc** (reading 14): centre `(d.x, d.y)`, radius read live off its caster
  (`groundR`, 90), so the drawn edge is where `tickHolyGround` tests. "Pale gold, sanctified glow at 0.18":
  the school's glow is white, so the fill is the censer's own incense gold, **#FFE9A8 at 0.18** (Rick on
  Daybreak: "sunlight glowing rather than the dull white"); a brighter 3-unit rim (#FFD98A, 0.45) with the
  hole cut in the path (CLAUDE.md 4.1b); "a faint cross-hatch of light" as two sets of diagonals 16 units
  apart (#FFF3C4 at 0.13), laid on the HALL's grid, so two overlapping discs share one lattice. The world
  pass, under both balls, source-over, clipped to the live hall: floor, nothing the bloom sees.
- **It blooms out of the impact point over 0.3s on the presentation clock** (the planting blow's hit stop
  stops `holyT`: a picture on the sim clock would sit at radius 0 through exactly the frames the viewer
  watches, v54's lesson), its rim brighter (+0.35) while it blooms; **it fades over the last second of its
  SIM life** (`holyT - t0` against `groundLife`), reaching 0 the step the simulation removes it.
- **Live and inert** (the stage-5 review's note: "make an inert disc read as inert"): a disc is drawn for its
  whole 8s, but the ground acts only in its caster's window (reading 2), so the picture says which: LIVE at
  0.18 (rim 0.45) while the window is open, INERT at 0.07 (rim 0.2, the lattice at 0.4 of itself) once it
  closes; the switch follows the head, up over 0.25s at a cast (a disc still standing works again) and down
  over 0.3s at the close. **The tell: the fill |dL| live 0.126, inert 0.054.**
- **What the ground does, shown** (reading 15): a foe on a live disc wears a gold rim 8 units outside its
  shell (#FFD98A at 0.8, raised from 0.5 when m1 read it at 0.055 under the ball's own contour art), up over
  0.1s and down over 0.25s, drawn under its ball with the hole cut at the shell, so it can only be a rim
  (Benediction's measured fix); each smite tick flashes the rim of every disc under the foe for 0.3s (+0.4);
  **SMITE n on the first smite of each on-ground stretch, BLESSING n on Censer on the first blessing of
  each** (the tag rule of Corona, Daybreak, Zenith, Canopy and Benediction), both re-armed the first step
  off; Censer on a disc gets the design's "soft up-drift of motes", ten round its shell rising 46 units,
  under the ball.
- **The cast: the hammer head lights, "a hot core, not a white one"** (§4; 4.1b): a hot gold core in the
  head's central piercing (a radial gradient 255,222,128 → 240,140,40), the four small piercings lit like a
  censer's coals (#FFB547), the head's radiant halo stroked gold (#FFC24A), at the head's own place
  (`drawWeapon`'s transform, `SHAPES._whRadiant`'s geometry), in the EMISSIVE pass over both fighters. It
  ignites over 0.25s, stays lit while the window is open (the tell that blows consecrate now), and cools over
  0.3s at the close, a death or the verdict (`tickHolyGround` never runs once `over` is set, so a window open
  at the kill would otherwise stay lit); dimmed to 0.42 with a stunned weapon; when Censer is side `b` the
  foe's shell is cut out of it (Zenith's rule: `a` is drawn over `b`).
- **The field, drawn** (5b): five incense motes a disc rise 42 units off it and fade, placed by `shellHash`
  on the disc's planting step and the match clock (the death clock after the kill): no RNG, and they keep
  moving through a hit stop.
- **After the kill** the ground fades out over 0.3s in the verdict, with the head.
- **The nova's art is retired** (reading 19): `drawUltUnder`'s glyph ring (12 glyphs out to r 300) and
  `drawUltOver`'s smoke spiral and 14 incense sparks under `lighter`, both drawn at every cast off the ultFx
  record; the life map's `censer: 1.6` (the record falls to the map's own 1.5, and nothing draws from it);
  and the charge rune, `ULTSIG.censer`, redrawn: the censer swung over a disc of holy ground that fills with
  the charge, a gold coal in it, incense rising off the disc (the nova's rings gone).
- **The silhouette is left alone**: Censer's resting hammer reads |dL| 0.286, 1st of the 7 warhammers
  (Lodestone 0.252, Ironwood 0.216, Bulwarden 0.214, Ravelbone 0.174, Shroudmaul 0.145, Grudgebearer 0.125;
  `hammer_sil.py` on the lightkeeper-fxout carry, 453x805).
- **The art hangs off the Fighter** (`consFade`, `consAge`, `consOut`, `consEnd`, `consPic`, `consFoeOn`,
  `consSelfOn`, `consFoeLit`, `consSelfLit`, `consPulse`, `consSeen`, `consTagS`, `consTagB`), never off
  `m.ultFx` (open item 25). `tickConsecration`, in `tickPresentation`, finds every event by watching
  `holyTally` rise, so neither `tickHolyGround` nor `resolveHit` makes a call for the picture.
- **Bloom** (the design's gate: a floor disc adds ≤ +0.01 arena-mean lift): the picture's share of the lift
  **max +0.0001** (the batch's gate +0.02); **the floor alone +0.0000** (the design's +0.01); the raw luma it
  adds (chain off) at most +0.0225. No ball's disc pushed past 0.90 by it (the caster 6 frames with / 6
  without; the foe 6 / 8). The art on the balls' discs: the caster -0.0007..+0.0056; the foe
  -0.0081..+0.0208 (the ground beside a squashed white Morningstar in a hit stop, not over it). **Three
  controls, each failing:** every live disc as a white `lighter` disc at 0.35 lifts +0.031 (past 0.02 on
  11/130 frames) and pushes the foe's disc past 0.90 on 16/45; a white-hot glow on the caster pushes its disc
  past 0.90 on 91/100 window frames; the foe's rim as a filled white `lighter` disc, 30/45.
- **Legibility** (median |dL| of each component's own pixels, out of a hit stop / in one): the floor 0.162 /
  0.152; the fill 0.114 (inert 0.063); the lattice 0.053 (inert 0.030); the rim 0.225 / 0.247 (0.323
  blooming, 0.290 on a smite tick, 0.111 inert); the incense 0.140 / 0.148; the foe's rim 0.081 / 0.120;
  Censer's drift 0.157; the head 0.080 / 0.064 (mostly a hue shift, white to gold); the tags 0.325 / 0.262.
- **Whole fights** (the lab's verify, 15 fights, each as the rows, the shipped look, and the shipped look
  drawn through the renderer): the simulation identical to the base in all 15 at the kill; drawn, nothing
  thrown, the picture's discs the ground's on every step, the SMITE and BLESSING tags exactly the rule's, the
  weapon row unwritten; the head cools 0.29-0.43s after a clock close (0.575 once, through stops) and the
  ground goes 0.29s into the verdict. **Control:** a copy that nudges the foe 1e-9 in the SMITE tag's branch
  differs on all 13 Censer fights and not on the 2 without Censer.
- **Frame cost: not measured** (no Electron on this PC; the lab deferred it). §6.

**Readings declared** (the builder's docstring, 13-19; art and sound are Code's picks):
13. The picture reads the window off `ultHoly && alive && !over` and keeps its own state on the fighter; the
    head cools at the close, a death or the verdict, and the ground fades out in the verdict.
14. The discs are the simulation's, read and never written; the bloom on the presentation clock, the fade on
    the sim's; drawn for their whole life, LIVE in a window and INERT outside one.
15. On the ground is `tickHolyGround`'s own test as it ran, read off the tally; the tag rule; the picture
    writes its `cons*` fields, the tags and `taught` only, and draws no RNG.
16. The voices on the sim path are two `SFX.play` calls (the disc's bell, the heal chime); the cast's voice is
    `fireUlt`'s own; the smite tick is silent; there is no close voice.
17. A disc planted by a killing blow rings its bell on the death voice's step.
18. No `fx.js` field; the nova's `SPECS.censer` is the orchestrator's to take out.
19. The nova's art is retired with the nova; the charge rune redrawn.

### 5b. No new `fx.js` field: the incense is drawn, and the nova's spec goes out of both copies by the orchestrator

The design asks for "incense motes rising from each disc (both `fx.js` copies)". A SPECS field fires once,
at the cast, from the one `m.ultFx` slot. The picture lab measured what that slot gives this relic over 101
Consecration windows (16 foes x 2 seeds, both sides; `fxprobe.out`):
- the slot is Censer's a median **0.68s** of the window clock (max 0.72; the opponent's cast took it 14
  times): a field borne on it could exist for **7.8%** of the window;
- **no disc exists at the cast**: 163 discs were planted in those windows (17 windows planted none), a median
  4.33s into the window (p10 0.98), and **10 of the 163** while the slot was still Censer's;
- a disc stands a median **203 units** from where a burst is drawn (p10 67, p90 369), farther than its own
  radius on 84%.

So the incense is DRAWN, off every disc, in the world pass (5a): the Zenith, Canopy, Tendril, Quarrelstorm,
Ascension and Bulwark precedent. **Rick's to overrule.**

The nova's own spec, `SPECS.censer` (a 1500-particle burst), is the design's "nova's field spec out". `fx.js`
is shared by every build in the batch, so this builder never edits it, and stage 6 refuses to write if its
inlined copy moved (reading 18). The orchestrator takes the entry out of both copies with `fx_remove.py
--relic censer` at the carry. Its exact text (the stage-5 review asked for it whole, indentation included):

```
    censer: { mode: 'burst', n: 1500, sp: [180, 540], grav: 40, drag: 2.2,
              life: [0.40, 1.00], heavy: 0.0, size: [0.7, 2.0],
              spawn: 0.08, up: 20 },
```

`src/render/fx.js` lines 120-122 today (830a7026987903b4); `sc-tendril-t3` 32220-32222; the b25.5
32326-32328; the fx link 32692-32694. **Tried on a scratch copy** of the fx link's inlined module
(`fx_remove.py --fxjs`; `runs/stage6_fx_remove_scratch.txt`): the three lines come out whole, only the block
and the stamps move (28fc58641370a1a9 → 2bc829dc324f0040, the picture lab's shipped look's stamp), and the
page becomes 8af05d81c8d72f29. The page is safe without it (`sync` returns on a missing spec); the picture
lab's `engine_ab` (4218/4218) and whole-fight identity ran on its own spec-out page. **Until the carry, the
stage-6 link still fires the burst at every cast, and so does the clip (5f).**

### 5c. The voice

Every number here is `tools/censer_voice_lab.py`'s (845c809a8ebae571; its final run lab3, Chromium
151.0.7922.34; every render an OfflineAudioContext at 48 kHz through `Sfx.buildChain`, a candidate rendered
from its arm's own text). Its controls reproduce the four published numbers (rune-crack 0.608 / 450 ms,
hit@11.6 0.443 / 80 ms), and levels are read against Censer's own blow at 25.5.

- **The cast, the thurible swing — JINGLE, of 5** (v78 §4: "a chain-rattle into a low bell, 0.5s"). Nine links
  of the chain ringing as bands of noise (Q 6, 30 ms, 3.3-6.1 kHz), rising in level, then a church bell
  struck on A — hum A2, prime A3, tierce, quint and nominal A4 — with the clapper's knock (15 synth calls).
  The bell strikes 206 ms in, after the rattle's 9 onsets (5.8 dB under the bell, centroid 4852 Hz); audible
  495 ms; the bell's strongest peak 110 Hz, 99% of its power under 500 Hz, a peak 315 cents off every
  harmonic (a bell, not a harmonic tone); its loudest 50 ms -2.9 dB re the blow at 25.5 (its quietest draw),
  +19.0 dB re the wall tick; register at most 0.69 (Ironhail's cast, on the batch line) against rune-crack,
  the school's and the warhammers' casts, the seal, the death voice, the clank, the blow and the batch line's
  30 other voices. All five candidates pass (worst register 0.69-0.76); CHURCH, BRONZE, JINGLE (0.69) and
  SWING (0.72) tie within the rule's 0.05, and the tie goes to the fewest synth calls (JINGLE 15; the others
  33-36). Seven controls each fail their own gate (the bell alone, the rattle alone, the bell two octaves
  up, harmonic partials, a 1.5s ring, the bell before the rattle, rune-crack itself).
- **A disc opening — BOWL, of 5** (§4: "a soft bell tone, pitch by disc count"). A struck bowl: two sines on
  its 1 : 2.71 modes, the upper at 0.3 and dying half as long; **one step of the score's A minor pentatonic a
  disc standing, C5 D5 E5 G5 A5** (523, 587, 659, 784, 880 Hz; counts clamped to 1..5). Audible 400 ms at
  every count; its loudest 50 ms -11.0 dB re the blow and +11.0 dB re the wall tick; over the heaviest blow
  on its frame (hit@45, its loudest draw) by +17.7 / +15.7 / +17.8 / +13.0 / +13.6 dB in its note's
  third-octave (counts 1-5); at counts 1 and 5, +19.9 / +13.4 over a crit and +19.7 / +17.5 over the median
  blow (@33); register at most
  0.66 (Angelus's cast) against the heal chime, Zenith's tick, the wall tick, hex-snap, the blow, rune-crack,
  the cast and the peers. CHAPEL (0.85 against Angelus's cast), LOW and HIGH (0.92 against the spark itself)
  are out; CUP passes at 0.68. Six controls each fail their own gate (one note for every count, 3 dB loud,
  harmonic partials, dying in 40 ms, a bar's bright modes with a click, the heal chime itself).
- **The heal — the `spark` collect voice, reused, unchanged** (§4), once per blessing with n the blessing
  Censer carries after it (Zenith's call word for word): 1290-1730 Hz, audible 135 ms, +7.3 dB re the wall,
  +21.2 to +23.9 dB over the score's p90. The bell and the chime on one frame move each other's band by
  +0.00 / -0.03 dB (3 of 1063 heals come within 0.1s of a disc).
- **The smite tick is silent** (§4: "nothing new"; no smite voice exists in the synth). **There is no close
  voice**: the design names none. Flagged for Rick (§6), not made.
- **Wiring** (reading 16). The cast is `fireUlt`'s own prelude call, `SFX.play("ult", { w: f.w.id })`: Censer
  had no arm and fell through to rune-crack, which 11 other relics on the b25.5 still use (Lastlight,
  Spellbreaker, Ironhail, Lightkeeper, Farwarden, Aureole, Oathwound, Heartwood, Gloamwire, Portcullis,
  Bindweed), so the two arms go in BEFORE that fallback, which is re-emitted unchanged. The bell plays in
  `resolveHit`, once per disc planted, after `holyTally.discs++`, with n the caster's discs standing after the
  push (a block-scoped count that reads `m.holyGround` and writes nothing); the blow keeps its own `hit`
  voice. The chime plays in `tickHolyGround` after `T.bless++`.
- **The lab's wire run** (148 fights, Censer both sides x every foe, seeds 109601-2): 148/148 identical, every
  other SFX call identical in order, kind and options; **456 casts, 456 cast voices; 716 discs, 716 bells (32
  on a killing blow: reading 17); 1063 blessings, 1063 chimes**; the bells' counts {1: 329, 2: 224, 3: 109,
  4: 43, 5: 9, 6: 2}, the chimes' {1: 325, 2: 260, 3: 199, 4: 135, 5: 144}. **Control:** the rows plus one
  sim write (the foe nudged 1e-9 on a disc) leave 4/148 fights identical. End to end, the rows applied as
  text: 74/74 fights identical, every voice where it belongs; the arms through the patched page's own
  `SFX.play` equal the candidates (worst 6e-08); 132 other voices unchanged (worst 1.5e-07); `ult/censer` is
  no longer rune-crack (0.682 apart). Its own `engine_ab` on its page: 4218/4218.
- **A real window** (Censer v Farwarden, side B, seed 109602; cast 61.22s, 3 discs and 8 heals by 69.68s):
  each bell over the fight in its note's third-octave +5.2 / +15.3 / +10.2 dB; the chimes +10.3 to +33.2 dB;
  the cast's bell +37.0 dB at 400 Hz over the strike's 150 ms (its 110 Hz hum +4.8: the score's bass shares
  that band), the rattle +17.3 dB at 5080 Hz. `05-reference/v109/censer-pick-real-window.wav` and its
  `-without` twin hold that window with and without the new voices.
- **Main-thread cost a call:** the cast 0.40 ms, the bell and the chime under the timer's resolution.
- **With the batch line's other Sfx rows** (Angelus, Lodestone, Lightkeeper, Widowmaker, Oracle, Portcullis,
  Coldiron, Ironhail, Bindweed): both orders render every arm alike (worst 1.8e-07), and Censer's arms are
  unchanged by them.

### 5d. The probe's stage 6: [10] the voices, [11] the picture's hook

`censer_probe.py` is now c588b606b1fc7741 (stages 1-5's was 5d78670c3787524e, kept in scratch). Checks [1]-[9] are
unchanged but for one detail of [6]'s once-a-fight table check (below). Two checks are new, one for each half
of stage 6, and **the link itself switches each one on** (the disc bell's arm in `AC.SFX.play.toString()`,
`tickConsecration` on the Match), so the same probe still reads [1]-[9] alone on a link without stage 6.
Once a fight is over it steps 2s more of the verdict (the step's `over` path, the presentation clock only)
for these two checks alone.

- **[10] the voices.** `SFX.play` is wrapped for the run (put back after it) and every call recorded with
  where it was made. Censer's two arms and the heal chime are read; **a ward's shatter plays its own crit HIT
  voice inside `hurt()`**, which is not one of them, and so it cannot pass or fail [10]. It fails:
  - a Censer cast without exactly one cast voice (w "censer"), inside `fireUlt`, or the cast voice anywhere
    else (a foe's cast included);
  - a Censer blow that plants a disc and does not play exactly one bell with n the caster's discs standing
    after the push, or a bell from any other blow, or anywhere else;
  - a ground-ticker call that plays anything but one chime per blessing it laid (n Censer's blessing after
    it): so **no voice on a close, by the clock or by a death**, and none on a smite tick;
  - the chime anywhere but the ground's ticker and the two other relics' spark tickers (`tickSun`,
    `tickSparks`, which play their own); any of the three in the picture's hook or in the verdict;
  - and every one of the run is accounted for: cast voices = casts, bells = discs, chimes = blessings.
- **[11] the picture's hook.** `tickConsecration` (the picture's one call on the step path) is wrapped. It
  fails a call that changes either fighter (every own number, flag and string but `cons*`, every array's
  length, every status, the window, the tally, the cooldowns, the weapon row and its ult) or the match
  (every own number, flag and string, every array's length but `tags`, every disc's x, y, t0 and side), or
  draws the RNG, or plays a voice. And the picture as declared, **rebuilt from the tally the way [4] rebuilds
  the smite** (readings 13-15): the head not lit (`consFade` 1) in an open window, lit with none, or a close
  that is not a fade to 0 over exactly 0.6 of its clock (0.3s) — by the clock, on a death or at `over`; the
  picture's discs not the caster's discs of `m.holyGround`, by identity and in order, or a disc's bloom clock
  not the presentation clock since it appeared; "on the ground" not the ticker's own answer; a smite tick
  without its flash; a SMITE tag not exactly on the first smite of each on-ground stretch (at the foe, with
  its count), a BLESSING tag not exactly on the first blessing of each (on Censer, with its count), or any
  other tag; the foe carrying any of it; the head lit or the ground drawn after 2s of the verdict.
- **The drawn subset** (`--drawn 6`, the default): the first seed's fights, both sides, every foe, drawn
  through the renderer (`AC.__draw`, the post chain off, 270x480) every 6th step while the picture shows and
  every 60th otherwise, through the kill and the verdict; [11] fails a drawn frame that throws, draws the
  match's RNG or changes the simulation. **[6]'s once-a-fight check of `SHAPES` now reads it key by key**:
  the renderer keeps memos there (Lightkeeper's finding), so what a draw writes to an underscore key is taken
  into the check's start, and every other write still fails [6]. The run prints the memos it took in.

### 5e. Stage 6's gates — every one able to fail

- **engine_ab b25.5 → fx, ALL 38 WITH Censer, n=6: 4218/4218 identical** (`runs/stage6_engine_ab38.txt`;
  38/38 distinct winners, 4218 distinct seeds, 22.7-114.9s; the ids are `runs/stage6_ids38.txt`). Presentation
  moves no fight, Censer's own included. **Control:** the b25.5 against `mP1` (below: its picture nudges
  the foe 1e-9 on a smite tick) with Censer, Farwarden, Dawnbringer and Twinshade at n=6: **18/36 differ**, and Censer's pairings are 18 of the 36
  (`runs/stage6_engine_ab_control.txt`).
- **censer_probe (c588b606b1fc7741): 11/11 on the fx link** (`runs/stage6_probe_fx.txt`, `.json`): 444
  fights, Censer both sides x 37 foes x 6 seeds, and the first seed's 74 drawn; 23 min. **[1]-[9] print
  every mechanism line the b25.5 prints under the stages 1-5 probe, to the character,
  and every counter of that run's json is equal** (`runs/stage6_probe_cmp.txt`): 3.13 casts a fight; 1.61 discs,
  4.68 smites and 2.60 blessings a cast; the foe on the ground 21.29% of window frames; 50.5%; 1.22 million
  window frames diffed whole. The new probe on the b25.5 itself (`--drawn 0`) reads 9/9, every line and counter
  as before, and says "stage 6: not on this link" (`runs/stage6_probe_b25.5.txt`). Then:
  - **[10] the voices:** 1390 cast voices for 1390 casts, each inside `fireUlt`; **2244 bells for 2244 discs**,
    each n the caster's discs standing (n 1-6: 1045 / 711 / 325 / 116 / 34 / 13; 80 on a killing blow), and
    2436 other blows silent; **3619 chimes for 3619 blessings** (n 1-5: 1067 / 852 / 671 / 493 / 536); 6194
    smite-tick frames with no blessing, silent; **every close silent: 1149 by the clock and 70 by a death**;
    silent through 2s of the verdict in all 444 fights (171 with the sim's window still open); 270 chimes of
    the two other relics' own spark tickers, and none anywhere else;
  - **[11] the picture:** 6,003,029 `tickConsecration` calls, none of which changed the simulation, drew the
    RNG or played a voice; the head lit on every one of the 2,625,224 calls in an open window, in 1389
    windows: one cast's window was closed by a death on the very step it opened, before the picture's first
    look (the arithmetic: [1]'s 70 death closes are the picture's 2 on Censer's death, 67 of its 238 at
    `over` -- the other 171 open at `over` -- and that one); **every close a 0.3s fade**: 1149 by the clock,
    2 on Censer's death, 238 at `over`; the discs
    mirrored on 4,452,456 calls, 2244 discs, every bloom clock exact; on the ground: the foe on 569,461
    window calls, Censer on 212,519, neither on 1,843,244; 6505 smite ticks flashed; **SMITE on 5036 stretches'
    first ticks (1469 ticks inside a tagged stretch, untagged), BLESSING on 3589 (30 inside)**; after 2s of
    the verdict the picture gone in all 444, 245 of them lit at `over`;
  - **the drawn 74:** 57,774 frames through the renderer (54,522 with the picture up, 8455 of them in a hit
    stop, 2445 in the verdict), none of which threw, drew the match's RNG or changed the simulation; the
    renderer's memos taken into [6]'s start: `_facetCache`, `_fxc`, `_inkCache`, `_shadeCache`, `_t`
    (Lightkeeper's five). **The base, drawn** (the b25.5, the first seed, `--drawn 6`;
    `runs/stage6_probe_b25.5_drawn_s1.txt`): 10/10, [1]-[9] and the drawn check, 8405 frames through the
    renderer (every 60th step: nothing of stage 6's to show) with the same five memos -- what the renderer
    writes, the base's draws write alike.
- **The probe's controls**, scratch copies of the fx link with one edit each (`runs/stage6_mutants6.py`, their
  hashes in `runs/stage6_mutants6.txt`; the first seed, both sides, every foe, 74 fights), each failing its own
  check and passing the other ten:

```
mutant          sha16             breaks  how                                                              probe      fails               fights
mV1-closevoice  892ea594bd11da00  [10]    a heal chime on EVERY close of the window, the clock's and a death's   10/11  [10] 207x    identical
mP1-picwrite    c44e145b67091a40  [11]    tickConsecration nudges the foe 1e-9 on a smite tick (a sim write)    10/11  [11] 1106x   move
mT1-tagevery    3aebbac40f5d9d99  [11]    the SMITE tag on every smite tick, not each stretch's first           10/11  [11] 242x    identical
mD1-drawwrite   034efa632e41c21e  [11]    drawConsecration nudges side a 1e-9 when it draws (a drawn frame)     10/11  [11] 38015x  move (drawn)
```

- The clean fx link on the same 74 fights (the first seed, no drawing) reads 11/11
  (`runs/stage6_probe_fx_s1.txt`), and mV1 and mT1 leave its tallies and win rate exactly as they are: a voice
  and a tag are presentation, so the two presentation-only faults are caught by the checks that read the
  presentation, and by nothing else.
- mV1 fails on 193 clock closes and 14 death closes ("the ground's ticker played [spark collect] for 0
  blessing(s) on a clock close"): **the check that a close is silent is the check that no close voice ever
  sounds on a death**; the design has no close voice, so the mutant gives the ground one.
- mP1 fails on every smite tick the picture sees ("the picture wrote the simulation: vx ..."), read on the
  call itself; its fights move (the `engine_ab` control above), and [1]-[9] still pass, because they rebuild
  every frame from its own state.
- mD1 is caught only by the drawn subset ("a drawn frame changed the simulation: vy ..."), on the frames that
  draw the ground: the check that a DRAW writes nothing, which the headless hooks cannot see.
- mT1 fails where the rule says a stretch's later ticks go untagged ("1 SMITE tag(s) on a call with 1 smite
  tick(s), want 0").
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337, at 0.5 / 6 / 12 / 22 / 31 / 40s) are **24/24
  pixel-identical** (`runs/stage6_render_ab_others.txt`). **Control:** Censer v Slagheart 109149 (the clip's
  fight) at 31.5 / 33 / 35 / 37 / 39 / 40.8, inside the window that runs 31.225-41.017, is **0/6 identical**
  (`runs/stage6_render_ab_control.txt`; the frame's mean luma -1.7 of 255 at 31.5, the nova's glyph ring and
  smoke gone from the cast, then +1.8 to +7.4 as the ground goes down).
- **chain_audit** `--builder censer_build.py`, relic = tip = the fx link: **ALL 22 INSERTS SURVIVE**, stages
  1-5's ten and stage 6's twelve (`runs/stage6_chain_audit.txt`); the thirteenth row, the life token, adds no
  code and so is not an insert the tool can read. **Control:** the same relic with the b25.5 as the tip loses
  11 of stage 6's and exits 1 (`runs/stage6_chain_audit_control.txt`). **Two rows it cannot watch:** the heal
  chime's line is Zenith's and Daybreak's word for word, so its marker stands 3 times in the relic and 2 in the
  base and never reads LOST; and the life token's removal has no marker. The builder watches both on every
  stage-6 build: the chime's line must be in the page exactly once more than in its source, and `censer: 1.6`
  and `u.w === "censer"` must be gone. Two of the twelve (the retired art branches) are found by their comment
  text, the code they leave being shorter than the tool's floor.
- **tip_audit:** identical to the b25.5's, line for line, but the file name (`runs/stage6_tip_audit_fx.txt`;
  the one MISSING is Burn's `feed`, the base's own).
- **The builder's own guards** (`runs/stage6_builder_checks.txt`, the final builder 0d97b0a19fe72d27; the same
  run on 3e2a19d64f97c39e before the docstring's reading 5 was reworded, `stage6_builder_checks_first.txt`):
  - all five links rebuild byte-identical from the bare tip, `sc-tendril-t3`, LF, no CR;
  - **stage 6 refuses** to run twice (its names are in its own output), on stages 3, 2 and 1, on the bare tip
    (each: the profile at the blade BLADE names is not there), over an existing link, to a name not
    `sc-censer*`; stage 5 refuses on the fx link;
  - **its scan of stage 6's ADDED code** (a re-emitted anchor aside) refuses seventeen scratch copies of the
    builder, each with one forbidden thing written into a stage-6 insert: a sim write in `tickConsecration`
    (the foe nudged), the RNG in a draw method, the one `ultFx` slot, a beat, a hurt in the heal row, a status
    laid (stun), a splice of the sim's discs, an index write into them, a write to the tally, `Math.random`, a
    shared table through an alias (`Q_ = STATUS.smite`), the shared weapon (`w.reach`), a sim write in a draw
    method (the match's clock), the disc bell's line changed (`n_ + 1`), a voice in the picture's fields row, a
    sim write in the fields row (the charge), and the synth struck outside the Sfx row. **A harmless edit in the
    Sfx arm writes its page** (a different one), and the unmutated copy writes the fx link, 3d68c7648a9cb3a8;
  - on stage 6 it also refuses if the inlined `fx.js` moved, if the nova's art is still drawn off the ultFx
    record or its life entry is in the map, if the rune-crack fallback is not kept once after Censer's arms, and
    unless each arm, call, pass and method is wired exactly once and `tickConsecration` is `tickPresentation`'s
    second call. The generator (`runs/stage6_gen_s6.py`) was run once; it refuses a builder that already
    carries S6. Two hand edits followed it, said here: the profile check takes the blade on stage 6
    (`dmg:25.5`, not the shipped 28.77; commented in the builder), and `fill` came out of the array-mutation
    list (the canvas's `c.fill()` matched it; `copyWithin` stays in).
- **compose6** (above; `runs/stage6_compose6.txt`, `stage6_compose6.sh`): 0 FAIL.
- **shell_identity** is not run here: the app's json is shared, and the orchestrator runs it on the carried link.
- **The labs' own gates** (§5a, §5c): the picture — bloom share +0.0001, with three controls that fail; whole-
  fight identity on 15 fights x 3 (the rows, the shipped look, drawn), with a 1e-9 control that differs on all
  13 Censer fights; 91/91 other-relic render frames on 13 pairs, with Censer controls at 0/7 and 0/7;
  `chain_audit` 9/9 on three carries, with a control that loses 9; `engine_ab` 4218/4218 on its shipped look.
  The voice — the 148/148 wire run, with a sim-write control at 4/148; 74/74 end to end; `engine_ab` 4218/4218
  on its own page.

**What the design's stage 4 asked for, and where it went** (§5: "nova's field spec out", "bloom measured (disc
must add ≤ +0.01 arena-mean lift)", engine_ab, shell_identity, render_ab, chain_audit, "one fight watched"):
the bloom measured, +0.0000 for the floor (§5a); the nova's field spec out of both copies — the orchestrator's
at the carry, tried in scratch (§5b); `engine_ab` 4218/4218 with Censer in; `render_ab` 24/24 with a control;
`chain_audit` 22/22 with a control; `shell_identity` the orchestrator's; one fight watched, the clip (§5f).

### 5f. The clip (Rick's to overrule)

`tools/_censer_pick.py` (from `_ironwood_pick.py`, by way of `_angelus_pick.py`) scores a window against v78
§4 as built. A window qualifies only if it shows everything: the cast voice, a close BY ITS CLOCK with both
alive (the head cooling; a death's close or a kill is the death voice's and the verdict's), at least two discs
with bells at two or more pitches, a smite tick, a blessing with its chime, a disc still standing at the
close (so the tail shows the ground going inert), and nothing taking the screen: no cast or banner of the
foe's, no act banner, not the scrunch card, and no kill inside the clip. Twinshade is left out (discs at a
shade) and so are Censer's own school (a sanctified foe wears the same white and gold shell). Scored on the
discs, the distinct pitches, the smite ticks, the heals, the foe's frames on the ground, the discs standing
at the close and the hit stops while lit.

It ran 32 foes x 4 seeds (`runs/stage6_pick.txt`: 2 of 128 windows show everything, both against
Grudgebearer) and then 12 more seeds (`runs/stage6_pick_wide.txt`: 4 of 384). The pick is **Censer v
Slagheart, seed 109149**:
- the cast at 31.225; the window closes by its clock at 41.017: 8s on the window clock, 9.79s of match time;
- 4 discs, their bells at n 1, 2, 3, 4 (every step of the climb but the top), 9 smite ticks, 6 blessings
  (the chime at n 1-5), the foe on the ground 29.7% of the window's frames, 4 discs standing at the close;
- no banner, card or kill in the clip; the fight runs on past the clip's end (42.8, both alive).

The runner-up, Grudgebearer 109408, scored 1.5 lower (3 discs, pitches 1-3).

    python cinema_clip.py --game <scratch>/batch/censer/links/sc-censer-consecration-b25.5-fx.html \
      --a censer --b slagheart --seed 109149 --at 30.02 --window 12.79 --end-at-window --fps 60 \
      --w 540 --out ../07-shorts/v109/consecration-window.mp4

`--at` is the cast less 1.2, `--window` the window's 9.79s of match time plus 1.2 and 1.8 (the window clock
stops in the freezes, so 8 + 3 would end the clip before the close).

The clip (`runs/stage6_clip_check.txt`, `stage6_clip_log.txt`, `stage6_clip_timeline.txt`):
- **14.6s, 877 frames**: the window and 1.8s past the close, longer than the 12.79s of match time it films
  because the director slows the play from its T3 cut at 36.7, as on any clip;
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 3.73 MB (ce22f4b273fb92df);
- **AAC mean -23.1 dB, max -2.5 dB; -21.4 LUFS integrated, LRA 4.6 LU, true peak -2.5 dBFS;**
- the fight's state at the clip's end (t 42.8167, hp 46.35 / 24.962, 16 clanks) is the headless fight's
  (`stage6_clip_timeline.py`).

Five frames, checked through the pipeline (the post chain and the director), matched to the fight's own
event times by the HUD's clock; tiled in `05-reference/v109/consecration-clip-5frames.png`
(002705a450472840, 2700x960):
- 1.30s (31.3): the cast, 0.08s after it: the banner and the head's hot gold core;
- 2.25s (32.3): the first disc (31.69, its bell at n 1) standing, lattice and rim; SMITE 3 where the foe was
  smitten (31.83) and BLESSING 1 on Censer on the same step;
- 4.30s (34.3): two discs (the second at 33.71, its bell at n 2); the foe on the second, SMITE 4;
- 9.60s (38.5): four discs (the fourth at 37.83, n 4) and Censer standing on them: BLESSING 5 (38.53), the
  head lit; SMITE 4 on the foe;
- 13.40s (41.6): 0.6s after the clock close with 4 discs standing: the ground inert (dimmer), the head cooled.

**The white spray round the foe in the cast's frames (1.3-1.6s) is the nova's own `SPECS.censer` burst** (a
`burst` goes to the quarry), still on this link until the carry's `fx_remove.py` (5b). The clip is
`07-shorts/v109/consecration-window.mp4` (gitignored). **Rick's to overrule.**

### 5g. Where each event hangs (the fx link)

The lines, in `sc-censer-consecration-b25.5-fx.html` (grep the quoted text on a carried link;
`runs/stage6_lines.txt` has them on the fx link and on the b25.5):

```
the cast       fireUlt 16468: the shared prologue (banner, 0.08s hit stop, beat "ult", SFX.play("ult", { w: f.w.id }) 16495,
               this.ultFx; the life map line 16587 now "aureole: 1.6, " -- Censer's 1.6 gone), then
               `if (u.kind === "holyground"){` 16871: `f.ultHoly = { t: 0, dur: u.dur, cd: 0, bcd: 0 };` 16877, returns
a disc         resolveHit: `this.holyGround.push({ x: foe.x, y: foe.y, t0: this.holyT,` 14817, `self.holyTally.discs++;` 14819
the ground     `this.tickHolyGround(dt);` 9043 (after tickTendril, before tickHits); `tickHolyGround(dt){` 13755: the purge 13760,
               the close 13767 (the clock or a death), `T.foeOn++` 13781, the smite 13784, `T.selfOn++` 13789, the blessing
               13792, `T.bless++` 13793
the voices     Sfx arms: `} else if (w === "censer"){` 7434, `} else if (w === "censer-disc"){` 7461, before the shared
               `} else {  // rune-crack` 7481; the bell's call in resolveHit 14830 (after `self.holyTally.discs++;`);
               the chime's in tickHolyGround 13799 (after `T.bless++;`)
the picture    fields after `this.holyTally = null;` 7784 (`this.consFade = 0;` ...); `this.tickConsecration(dt);` 9085,
               tickPresentation's second call; `tickConsecration(dt){` 13827 (before tickWinnow);
               `if (__world) this.drawConsecration(m);` 19577 (the world pass, after drawTree);
               `this.drawConsecrationTop(m);` 19653 (the emissive pass, after drawSunTop); `drawConsecration(m){` 20680 and
               `drawConsecrationTop(m){` 20828 (before drawMotes); ULTSIG `censer(c, t, cf, P){` 639 (redrawn)
the nova's art the two `u.w === "censer"` branches gone: their comments at 21683 (drawUltUnder) and 22568 (drawUltOver);
  (retired)    fx SPECS.censer still inline at 32692-32694 (the orchestrator's, 5b)
```

## 6. What is left, and whose

- **Rick:**
  - the veto (design §6.1);
  - **the clip** (§5f, `07-shorts/v109/consecration-window.mp4`) and every art and sound pick in §5 — the incense
    gold at 0.18 and the inert disc at 0.07, the lattice, the head's hot gold core, the foe's rim, the drift, the
    redrawn charge rune; JINGLE for the cast and BOWL for the disc (its pitch climbing one step of A minor
    pentatonic a disc standing) — under "you pick i overrule";
  - **no `fx.js` field** (§5b): the design's "incense motes rising from each disc (both `fx.js` copies)" are drawn
    off each disc instead, because the one ultFx slot is Censer's for 7.8% of a window and no disc exists at the
    cast;
  - **the smite tick is silent and the window's close has no voice** (§5c): the design names nothing new for the
    tick and no close voice, so none was made;
  - **a disc planted by a killing blow rings its bell** on the death voice's step (reading 17; 32 of 716 discs in
    the voice lab's run);
  - **the blade target** (design §6.2): the design's own is the shipped rate, and on 151 the shipped nova reads
    50.1% on these fights, so the shipped rate and 50% are one point: 25.5 (49.6%). Had the target been the
    design's published 50.3 on 141, the pick would not move. The design's "about 26.5" reads 53.6 here. **25 and
    25.5 bracket the crossing about equally** (the line puts it at 25.26; 25 reads 51.2, 25.5 49.6): the pick is
    the nearer of two neighbours in a grid whose points sit within ±1.9 of the line, not a fine reading;
  - **the ground in the window only** (§0 reading 2, the lab's): the prose's other reading, holy ground that
    smites and heals for its whole 8s life, window or not, reads 71.75% at 28.77 against the built 60.9 (§2). The
    picture now shows the difference: a disc outside its window is drawn INERT (§5a);
  - **the caster's centre** (§0 reading 4, the prose's explicit word): the lab's ball test is worth about +1.75
    (62.65 against 60.9 at 28.77) and 0.2 of a blessing a cast;
  - **discs that outlive their window work again at the next cast** (§0 reading 2): the lab's list could never
    carry one (8 + 8 against its 16); at the engine's 14 it does on 21% of casts;
  - the brief's stage-1 gate ("~54% at 28.77") is arm B WITH the tick damage the design dropped, on 141;
    without it the lab reads 50.4 on 151 and the build 51.6 (§2). Its stage-2 gate ("~58%") reads 58.6 in the
    lab and 60.9 built, the window clock; **its "~1.3 discs a cast" reads 1.55 built** (1.32 in the lab): the
    window clock's tenth more blows, and a disc for the killing blow, which the lab never plants (§2);
  - the brief's blade grid (26 / 26.5 / 27) all read over the shipped rate, so the grid was widened down inside
    "the hammer row 20-29" (§4);
  - the field version (design §6.3: discs under the caster's own feet, arm D, 84.5% published) is not built;
  - the type spread at 25.5, 35 to 70 (bows 35, greatswords 70; item 12/32), and the matchups it moves most
    (Ironwood -20, Shroudmaul -17.5; Paradox +22.5, Thornshear +17.5);
  - a blow on a Twinshade shade consecrates the shade's ground (21 of 2244 discs on the final link).
- **The orchestrator (DONE at the carry, §7, but for shell_identity):**
  - carry the five stages with `censer_build.py --stage 1/2/3/5/6 --src <tip>` (the change sets are line for
    line the same on every newer tip tried, up to `sc-lightkeeper-fxout`: §5, compose6) and prove the carry with
    `engine_ab`;
  - take the nova's `SPECS.censer` out of both copies of `fx.js` with `fx_remove.py --relic censer` at the carry
    (§5b, its exact text; tried on a scratch copy). Until then a Censer cast still fires the nova's burst, and
    the clip shows it;
  - `shell_identity` on the carried link (the app's json is shared; not run here);
  - the app pointer (`app/main.js` GAME) waits for Rick's check of the whole batch.
- **Not measured here:** the picture's frame cost in the app (no Electron on this PC; the picture lab deferred
  it). A later session with the app installed, or the orchestrator.
- **Stage 1-5's review notes, taken at stage 6:** the fx spec's exact text (§5b); the inert disc (§5a); reading 5
  reworded (there is no mirror match: `Match` forbids one; the builder's docstring and §0); the discs-a-cast gate
  and the 25 / 25.5 bracket (above).

## 7. The carry onto the chain, and the nova's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Lightkeeper with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the retired
nova's particle field out:

```
sc-lightkeeper-fxout.html              the batch line's tip (Lightkeeper, fx out)   088189f3517b6f11
  -> sc-censer-stub.html                  stage 1                                  8f74957506250acf
  -> sc-censer-ground.html                stage 2                                  f13f25a36051b2f3
  -> sc-censer-consecration.html          stage 3                                  f95e469f23bd2b0c
  -> sc-censer-consecration-b25.5.html    stage 5                                  73b396f225784f45
  -> sc-censer-consecration-b25.5-fx.html stage 6                                  ae411af7b64ba742
  -> sc-censer-fxout.html                 SPECS.censer out of both fx.js copies    00a2e2e10448c492
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail, Widowmaker and Lightkeeper (redesigned on the chain since), n=6: **3570/3570 identical**
  (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-lightkeeper-fxout` against the carried stage-6 link, every relic on the tip but
  Censer (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`): the redesign moves
  no other relic's fight on the batch line.

**The nova's field spec out: `tools/fx_remove.py --relic censer`**, the entry's three lines; the
`/* ---- NOVAS ... */` header above it stays: it still heads Deadfall's entry (`runs/fxout/fx_remove.txt`).
**fx.js 830a7026987903b4 -> 866f45e37dc54e3f.** One comment is now stale and is left for whoever next edits fx.js:
Deadfall's says "the four novas above it", and none are above it any more (Widowmaker, Lightkeeper and
Censer have gone from under it).

**Gates on `sc-censer-fxout`** (`runs/fxout/`, run one at a time at idle priority: Rick was on the
PC):
- engine_ab against `sc-censer-consecration-b25.5-fx`, all 42 relics, n=6: **5166/5166 identical**;
- `censer_probe.py` on the carried link: **11/11** -- it met every relic carried since its scratch
  base and needed no change;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Censer v Slagheart 109149
  through the cast (31.25-31.65s), 0/5 identical** -- the burst is gone;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity: NOT YET RUN.** It launches the Electron app, and Rick was using the PC; it runs when
  he says he is offline, and its result is added here.

**The clip, re-filmed on `sc-censer-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v109/consecration-window.mp4` (3.69 MB, 14.6s on screen; `runs/fxout/clip.txt`), the cast without
the burst.
