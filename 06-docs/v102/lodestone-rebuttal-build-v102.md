# v102 — LODESTONE / REBUTTAL, BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-ironhail-fxout`, §7): stage 1 is arm A fight for fight (1320 of 1320 fights identical in 16 fields); the mechanism is the lab's (the probe 10/10 on every stage, reading each fighter's and the Match's whole state around every rune tick; twelve mutants each failing only its own check, a thirteenth equivalent by design); stage 2 over arm H is the window clock, measured both ways; stage 3 is arm C. The blade is 20.5, the measured point whose pooled rate is nearest 50% (49.0% both sides, against 21's 53.9%). By blade distance to the line through the eight points (crossing 20.78) 21 is nearer, 0.22 against 0.28: Rick's (§6). The brief's forecast, 21.5-22, is where the LAB crosses on 151; the built relic reads 53.6% there, the window clock's +4 (measured). No knob moves. engine_ab 4218/4218 identical; verify 11/13 (Lodestone 46.9% side B; both reds are the clock bands, red on every link; the 21.5 cut's Axiom v Lodestone 0/40 is gone). **Stage 6, the picture and the voice, is `sc-lodestone-b205-fx`** (§5): twelve rows byte-exact to the two labs' files. engine_ab over all 39 relics, Lodestone included, is 4446/4446 identical. The probe is 12/12, with two new checks ([10] the voice, [11] the picture) and five mutants each failing only its own. render_ab is 24/24 (the Lodestone control 0/6); chain_audit 20/20. There is no fx.js field: the rune motes are drawn. The clip is `07-shorts/v102/rebuttal-window.mp4`. Carried onto the batch line (§7): both carry A/Bs identical, probe 12/12 there, shell_identity 200/200.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`). Input:
`06-docs/v70/LODESTONE-BUILD-BRIEF.md` + `runic-warhammer-design-v70.md`, and nothing else (rule 0).
Builder `tools/lodestone_build.py`, probe `tools/lodestone_probe.py`, runs in `runs/`. **A NEW relic:
the 39th on this tip** (the brief's "37th" counted the chain before Ironwood, Portcullis and
Bindweed; the carry order settles its final number).

**Built IN SCRATCH on the chain tip** (the batch's parallel builds): the links below are not in
`02-chain/`. The orchestrator carries them onto the chain one relic at a time by re-running the
builder with `--src <tip>` and proves the carry with `engine_ab`. The builder asserts its base by
content, never by which relic is last, and its anchors compose (§4, "re-applies").

**Review round 3 (this revision).**
1. **The probe's "nothing else" checks read the whole state now.** [6] and [7] compared fixed lists
   of fields, so an invented rune effect on any other field passed: the review's mutants, a touch
   that drains a second of the foe's ultimate charge (10/10 at +24 points) and one that flips its
   spin (10/10). Both checks now read a deep snapshot of each fighter's whole state, and the
   Match's, around every rune tick, and [4] rebuilds the foe's `status.hex` exactly (§3). The
   review's two mutants fail [6] only, and so does a new one on the Match (a touch that mutes
   clanks); a new one on the caster (a touch that feeds its own charge) fails [7] only; the
   review's third (the hurl thrown away from the hammer) fails [5] only. The link stays 10/10.
2. **The blade's stated criterion was wrong, and is corrected; the blade is not moved.** 20.5 is
   the measured point whose POOLED RATE is nearest 50% (49.0 against 21's 53.9). It is not the
   point nearest the fitted crossing in blade units: the line through the eight points crosses at
   20.78, which is 0.22 from 21 and 0.28 from 20.5. §4 says this, including the order in which the
   points were measured, and 20.5 against 21 is listed for Rick (§6).
3. **Stage 1 = arm A is now shown fight for fight** (a per-fight copy of the lab,
   `runs/f4f_overlay.py`; 16 fields a fight, both blocks: 1320 of 1320 identical), not only foe
   for foe (§2).
4. **Two departures from the brief are now declared** (§0): the brief's state shape
   `{t0, end, cd}` is built as `{t, dur, cd}` on the window clock, and the window has 959
   working frames where the lab's has 960.
5. **The stage-1 row comment was reworded**, because it stated the donor's blade and the stub
   as if they were current on every link. **The four links were rebuilt** and have new
   sha256s. Each differs from its round-2 link in that comment alone: 8 changed lines, the same
   line count, identical with comments stripped (`runs/relink_diff.txt`). Every gate was re-run on
   the rebuilt links; round 2's gate files are kept in `runs/r2/`.
6. Smaller: the builder's stage-5 comment no longer says v100 and v101 "settled theirs by blade
   distance" (they wrote "the measured point nearest the crossing", and there the two criteria
   agree; §4); the re-applies now include Cold Iron's stage 6 (nine tips, §4).

**Review round 2.** The blade moved from 21.5 to 20.5 (the stage-5 link is now `sc-lodestone-b205`;
`sc-lodestone-b215` is retired to scratch and its gate files to `runs/alt-b215/`). Reading 8 (the
blurb) is declared as what it is. Reading 1 now says the foe-death close is unreachable and a kill
leaves `ultRunes` set through the verdict (§5 says what stage 6 does about it). The probe asserts
the design's numbers ([0]) and counts the two death closes apart. The 'after' control (the lab's
order on the engine's clock) is run (§2). §6, "What is left, and whose", is new.

```
sc-tendril-t3.html               the base: the chain tip (Bindweed stage 5)        5a6216e3b629fad4
  -> sc-lodestone.html           stage 1  the relic, ult stubbed (charge 1e9)      32736d26461e3061
  -> sc-lodestone-runes.html     stage 2  the runed walls: touch + hex (arm H)     f779b5be09d8ae4e
  -> sc-lodestone-rebuttal.html  stage 3  the hurl, hurl 0 -> 700 (arm C)          d48dd38d92e55bd0
  -> sc-lodestone-b205.html      stage 5  the blade, 23.5 -> 20.5                  6d736451a1ffc2df
  -> sc-lodestone-b205-fx.html   stage 6  the picture and the voice (§5)            7a095b143d66fbdb
     (stage 4: none -- the brief has three stages)
  round 2's links, the same but for the row comment: 219cc73b0460ddf0, f6b9d99345d7bd52,
  0dac0cefbff88ead, 346b12ef6d3b67ac (runs/relink_diff.txt)
```

Which runs ran on which links. The lab runs, the census, the stage-5 sweep (on round 2's stage 3)
and the clock controls (`ctl-*`, built from round 2's links) ran in rounds 1-2 and are not
re-run: the rebuilt links differ from round 2's only inside one comment. Everything that GATES a
link was re-run on the rebuilt links: the built SHIP runs of stages 2, 3 and 5 (both blocks, every
arm number identical to round 2's, `runs/built_rerun_r3.txt`, `runs/r3/`), stage 1 against arm A
per fight, the probe on stages 2, 3 and 5 and the thirteen mutants (made from the rebuilt b205),
the reproduce check, tip_audit, chain_audit, the re-applies, engine_ab and verify. Round 2's gate
files are in `runs/r2/`.

Every link rebuilds byte-identical from the builder (`tools/lodestone_build.py`, sha256[:16]
`c74cd4a4508bfcf5` since stage 6, `0731db270893647b` before it; stages 1-5 are the same bytes from
both; `runs/build_s*.txt`, `runs/stage6/builder_checks.txt`). The builder refuses to overwrite a link, a base without
Tendril's slot, a stage on the wrong stage, a second stage 1, 2 or 5, and the live build
(`runs/builder_refusals.txt`, `runs/refusals.sh`, re-run on this builder: 9 of 9 refuse, nothing
written).

## 0. What this build stands on

- **The relic** is Grudgebearer's hammer profile, the lab's donor and every shipped hammer's (reach 76,
  width 26, artW 54, spin 1.6, spin mode, mass 5.0, knockMul 2.3), at its blade 23.5 until stage 5;
  aff runic, onHit hex 1 (the school's channel, as Spellbreaker, Axiom, Foregone and Paradox carry
  it), and the brief's 68-character card: `The walls are runed: a foe that touches one is hexed and
  hurled back`. The builder asserts the donor's profile, the five shipped hammers', the four runic
  channels, hex's numbers (5 stacks, 2.6s, a 0.2s stun every 1.15s), `move`'s wall clamp at n + R
  (what makes the touch a contact test) and the runic hammer head's route (`SHAPES.warhammer` ->
  `_whConjured`, never drawn by a shipped relic).
- **The charge is 14: the brief's 16 on the lab's clock, converted** (Rick's batch ruling). The census
  (`runs/s0_census_HC_2207`, `runs/rune_census.py`, written by `runs/make_census.py`: a scratch copy
  of `ult_overlay.py` that counts, before each lab step, whether it is frozen --
  `m.hitStop > 0 || m.latch || m.splitHold` -- on the whole arm and inside windows. It only reads:
  its arms H and C are stage 0's block 2207 foe for foe and blow for blow):

  ```
  arm C (the whole)   11.07% of lab steps frozen (546,371 of 4,934,683); 13.15% inside windows, 9.66% outside
                      lab 16 -> engine 16 x (1 - 0.1107) = 14.23 -> 14
  arm H (hex only)    10.38% of lab steps frozen; 11.07% inside windows -> 14.34 -> 14
  ```
- **The lab is `tools/ult_overlay.py` + `overlays/rebound.js`**, the brief's own stage-0 command, with
  the relic as side A against the design's roster: the 34-relic roster minus the donor (33 foes,
  `runs/foes33.txt`). **Lab defaults against the settled numbers:** `flingSpeed` 700, `flingCd` 0.5,
  `hexPer` 1, the touch pad 1.5 (a literal in the overlay), charge 16 and window 8 are the settled
  numbers; `flingDmg` defaults to 4, the REJECTED bite (design §3), and is read only by arm D, which
  no stage reads. The lab's hex source is the Fighter; the build's is a side letter (hex reads no
  source: no dps, no feed). The lab casts on a metronome (every 16 step-seconds) with no cast hit
  stop; the engine's `fireUlt` stops the world 0.08s at every cast (every relic's), which the
  converted charge carries.
- **Readings** (in the builder's docstring):
  1. **The window closes on its clock or EITHER death** (the lab closes on either; the design is
     silent). A dead foe touches nothing; a dead caster's runes hand the foe back to nobody. **On
     this engine the foe-death close is unreachable**: the only thing Lodestone does that can kill is
     a blow, in `tickHits`, which runs after `tickRunes`; that step's `checkEnd` sets `over`, and
     `step()` returns early from then on (`if (this.over){ this.decay(dt); return; }`), so
     `tickRunes` never runs again. The probe counts 0 foe-death closes on every stage, and a mutant
     that drops the clause is equivalent (§3). The caster-death close is reached (a foe's side channel
     kills the caster earlier in the step). **So a kill in `tickHits` -- either hammer's -- ends the
     match with `ultRunes` still set**, and it stays set through the verdict: 236 of 456 probe fights
     on the final link (the lab closed on `m.over` too; the build does not). The simulation reads
     nothing after the verdict; the picture must gate on `!m.over` (§5).
  2. **The cooldown runs through the whole window, touching or not, and starts clear at the cast**
     (the lab's `cd = 0` at onCast and `cd -= dt` every window frame): a foe already on a wall is
     touched on the first frame. **One frame short:** `tickRunes` adds `dt` to `Z.t` before its
     close test. The cast step's own tick is therefore window frame 1, and the 960th tick closes
     the window. That gives 959 working frames where the lab's window is open for 960, which is
     1/120s short on the window clock. The probe's [1] reads exactly this count ("959 window frames
     a clock close"). Nothing measurable moves with it, because the built window is already
     1.0-1.2s longer in match time (§2).
  3. **A pinned foe is not touched** (the lab returns before the wall test); its frames still spend
     the cooldown (the lab's `cd -= dt` comes first).
  4. **`apply`'s source is a side letter** (the engine's contract, Rick's ruling 4).
  5. **The target is the opponent**, never a Twinshade shade (the lab's `foe`).
  6. **The hurl is assigned in the window tickers' slot** (after `ballCollision`, before `tickHits`): a
     blow landing on the frame of a touch knocks on top of the hurl. The lab assigned after the
     whole step, over the blow's knock. §2 prices the order directly (the 'after' control): the lab's order on the engine's clock reads 58.85 against the built 59.1 at 23.5, and 52.0 against
     52.2 at 20.5: nothing measurable.
  7. **The hammer is the donor's profile and blade until stage 5**; the school's channel.
  8. **The blurb is composed by the build, not quoted**: "A hammer that runes the hall: whoever
     touches a wall is hexed and hurled straight back at the hammer." It follows the batch's
     "A <type> that ..." pattern (Canopy's, Onslaught's and Tendril's builds composed theirs the same
     way) from §1's words, "hurls them straight back at the hammer". The design's title line reads
     differently ("The walls are runed: whoever touches one is hexed and hurled back at the hammer");
     the card (68) is the brief's, word for word. The blurb is player-visible text, Rick's to reword.
- **No wait.** The design: "The next cast does not wait for anything." The cast line is untouched;
  at charge 14 against an 8s window on the same clock a cast cannot come while the walls are lit,
  and the probe asserts both (no cast under the runes, no cast held back).
- **Names:** kind `"runes"`, fields `ultRunes` / `runeTally`, ticker `tickRunes`; all free on the base
  (grepped; the builder refuses a stage 1 whose base carries any of them). No SFX kind or ultFx kind
  is named `rune*`. Links prefixed `sc-lodestone`, none in `02-chain/`.
- **The clock:** the window and the touch cooldown run on the window tickers' clock, which stops in a
  hit stop (every batch build's convention). The lab ran both through freezes and touched walls
  during them (§2). **The brief's state shape is replaced for the same reason.** Brief §1 gives
  `f.ultRunes = { t0, end, cd }`, which reads as timestamps. On this engine a timestamp would sit
  on `m.t`, which keeps running through hit stops, so that shape amounts to the lab's clock: a
  window of 8 match-seconds. The build uses `{t, dur, cd}` instead, with `t` counted on the window
  tickers' clock, as the batch's standing ruling requires. §2's lab-clock control runs on that
  clock (a window of 8 match-seconds, with the cooldown running through freezes and walls touched
  during them) and prices the difference.

## 1. Stages 1-3, and 5

Stage 1 appends the row at the END of the WEAPONS array (the anchor is the array's closing `];`
and the comment under it, which names no relic), the ultimate stubbed at 1e9. Stage 2 adds
`ultRunes` / `runeTally` after `this.vineTally = null;`, the `kind === "runes"` cast branch before
Tendril's, `tickRunes` called after `this.tickTendril(dt);` (after `ballCollision`, before
`tickHits`) and defined before `tickWinnow`, and charge 14, with the hurl written but 0. Stage 3 is
one number, `hurl:0` -> `hurl:700`. Stage 5 is the blade, `dmg:23.5` -> `dmg:20.5`, on Lodestone's
own row.

`tickRunes`, each window frame: the window clock (close at `dur` or on either death); the cooldown;
a pinned foe or a running cooldown ends the frame; a TOUCH when the foe's centre is within
`inset + R + pad` of any side of the CURRENT hall (`this.inset`, so the runes walk in with the
seals); then the hurl, `foe.vx, vy = hurl x unit(caster - foe)` (assigned), and
`foe.apply("hex", 1, side)`. Nothing else: the builder refuses an insert that writes `stun`,
`pin`, `pinMax`, `pinFree`, `pinV` or `hitStop`, calls `resolveHit`, `hurt` or `beat`, draws the
RNG, uses `spawnFx` or `ultFx`, or writes the shared weapon; it strips comments before every one of
those checks, counts `Math.random`, checks the ult block against what it printed and `node --check`s
the page.

## 2. Stage 0 and the stages against it — the window clock, measured both ways

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic grudgebearer --cell runic:warhammer
--mech overlays/rebound.js --arms A,B,H,C --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights
an arm a block (`runs/s0_ABHC_*`). The built links run `--relic lodestone --arms SHIP` on the same
foes and seeds (`runs/built_*`).

```
                      lab on 151 (1 / 2)   pooled   published 141   sc-trunk on 151   lab at the engine's window   build on the lab's clock   BUILT (1 / 2)                 pooled
A   no ultimate       20.2 / 22.4          21.3     21.4            20.6                                                                     stage 1: 20.2 / 22.4          identical, fight for fight
B   hurl only         28.6 / 28.2          28.4     23.6            29.2
H   hex on touch      51.5 / 52.1          51.8     53.2            52.0              55.2 / 55.3 (dur 9.0)        53.0 / 50.5 -> 51.8        stage 2: 56.2 / 54.8          55.5
C   hurl + hex        60.6 / 58.5          59.6     57.3            60.5              60.6 / 59.8 (dur 9.2)        58.8 / 61.1 -> 60.0        stage 3: 57.9 / 60.3          59.1
```

- **Stage 1 is arm A fight for fight** on both blocks, now shown per fight (the review's note:
  round 2 compared the JSONs' per-foe rates and blow counts, which is all they hold). A copy of the
  lab (`runs/f4f_overlay.py`, written by `runs/make_f4f.py`: `ult_overlay.py` plus a record of each
  fight, read after the fight is over) keeps every fight's winner, length in steps, both fighters'
  hits, hp, shield, crits and damage dealt, and the match's clanks and end reason -- 16 fields a
  fight. Lab arm A on the base against stage 1's SHIP on `sc-lodestone`: **block 2207, 660 of 660
  fights identical (20.15%); block 2317, 660 of 660 identical (22.42%)** (`runs/stage1_vs_A_f4f.txt`,
  `runs/cmp_f4f.py`, `runs/f4f_*.json`). The per-foe comparison is kept (`runs/stage1_vs_A.txt`).
- **Stage 5 against the lab at its blade** (C at 20.5, and at the forecast's 21.5, with the same two
  controls): §4.
- **Published (141) against 151 is the runtime, not the tip.** The lab run on the published base
  itself, `sc-trunk` (34 relics), on 151 (`runs/s0_trunk151_2207`, one block) reads A 20.6 / H 52.0 /
  B 29.2 / C 60.5 against the published 21.4 / 53.2 / 23.6 / 57.3, and the tip reads within 0.6 of
  sc-trunk on every arm. A reproduces (21.3 against 21.4); on 151 the hurl alone is worth +7 (B), not
  the published +2, the hurl on top of the hex +8 (C over H), not +4, and the whole +38, not +36.
  The design's "the hurl is worth nothing" (§3) is a 141 reading; its hex (+31 on 151, +32 on 141)
  holds.
- Lab mechanism on 151 (arm C, pooled): 3.43 casts; 8.40 touches a cast; the foe at 4.00 hex
  stacks on an average window frame; 7.48 blows in windows and 7.51 outside a fight. Arm H: 8.34
  touches, 3.95 stacks. The design's 8.4 and 4.0 hold.

**Stage 2 reads +3.7 over arm H, and it is the window clock.** The engine's 8s are 8 seconds of the
window tickers' clock, and 11-13% of window steps are frozen, so a built window is 9.0-9.2s of
match time (the probe: 9.00s at stage 2, 9.17s at stage 3) where the lab's was 8 step-seconds. Two
controls, each able to come back wrong:
1. **The lab at the engine's window** (`runs/lab90_H_*`, `lab92_C_*`: dur = 8 / (1 - the frozen
   share inside windows), 9.0 for H and 9.2 for C) reads H 55.25 against the built 55.5, C 60.2
   against the built 59.1.
2. **A scratch build on the lab's clock** (`ctl-labclock-*`, `runs/make_ctl.py`: `tickRunes` also
   called on every frozen step, so the window is 8 match-seconds, the cooldown runs through freezes
   and walls are touched during them; the build's own order otherwise) reads H 51.75 against the
   lab's 51.8 and C 59.95 against the lab's 59.6.

So the whole stage-2 gap is the clock. The hurl nearly saturates the window's worth: at C, 1.2s more
window buys +0.6 in the lab, where at H it buys +3.5. Stage 3 is arm C (59.1 against 59.6; the
block spread is 2.4). The build keeps the engine's convention and every designed number.

**The order of the hurl against the frame's blows (reading 6), priced directly.** The lab-clock
build keeps the build's order, so it prices the order only by landing on the lab. The third control
does it head on: **the 'after' build** (`ctl-after-*`, `runs/make_ctl.py`: `tickRunes` moved from the
window tickers' slot to after `checkEnd` and `decay`, the lab's slot, still only on unfrozen steps --
the lab's order on the engine's clock), side A, the 33 foes, 660 fights a block
(`runs/ctl_after_*`):

```
                       the built link (the build's order)   the 'after' build (the lab's order)   the build's order over the lab's
stage 3, blade 23.5    57.9 / 60.3 -> 59.1                  58.0 / 59.7 -> 58.85                  +0.25
stage 5, blade 20.5    52.4 / 52.0 -> 52.2                  52.3 / 51.7 -> 52.0                   +0.2
```

The lab's order reads a quarter of a point under the build's at both blades, far inside the noise
of a pooled reading (a standard error of 1.4 points at 1320 fights). The order is worth nothing measurable, now measured head on, and
reading 6 stands.

**The hurl adds zero freezes** (brief stage 3's gate). The probe's [6] reads every rune tick and
none moves `hitStop` (0 of 14,518 touches on the final link). The frozen share of window steps
rises from 11.7% (stage 2) to 13.3% (stage 3) because a hurled foe is hit more in the window (7.18 ->
8.35 blows), each blow its own hit stop; the lab's census moves the same way (H 11.07% -> C 13.15%
inside windows).

## 3. The probe (`lodestone_probe.py`, one check per sentence, read inside the hooks)

Wraps `tickRunes`, `resolveHit`, `fireUlt`, `tickCharge` and `step`; Lodestone against every other
relic, both sides, 6 seeds (456 fights). The window's length and the touch cadence are read on the
PROBE'S OWN window clock (its sum of dt over the ticks it saw), never the engine's `Z.t` / `Z.cd`.

```
[0] the numbers: the link's ult block is the design's -- charge 14 (16 converted), dur 8, pad 1.5, cd 0.5, hex 1, hurl 0 (stage 2) or 700
[1] "for a duration": the window is `dur` on the window clock (never ticked on a frozen step), closes on the caster's death; only Lodestone carries it
    (the foe's death close is counted apart and is unreachable, reading 1; fights ending with the walls still lit are counted and stepped 240 verdict steps on)
[2] "touches a wall": a touch only with the foe's centre within inset + R + pad of a side of the CURRENT hall, alive, unpinned
[3] "once per 0.5s": never closer than `cd` on the window clock; never a missed clear touch
[4] "hexes them": each touch apply("hex", 1) on the foe once, by side letter, and the foe's status.hex exactly that apply's
    own result (stacks, clock, source); no application and no change to status.hex on any other frame
[5] "hurls them straight back": the foe's velocity ASSIGNED hurl x unit(caster - foe), 700 +-1; untouched on every other
    frame, the closing one included (and at hurl 0)
[6] "the walls do no damage -- they hand the enemy back": no hurt, no resolveHit, no beat, no hit stop; NOTHING ELSE on the
    foe (a deep snapshot of its whole state but vx, vy and status.hex) or on the Match (its whole state), every rune tick
[7] "the caster's own touches do nothing": the tick never changes the caster (its whole state, deep, but the window's own
    record ultRunes / runeTally; counted on the frames it is on a wall; read on frames the runes hurt nobody -- a hurt is
    [6]'s, and a ward it breaks bursts at its source, the caster)
[8] every Lodestone blow the hammer's own, rebuilt exactly from the captured crit and jitter draws, in the window and out
[9] "the next cast does not wait": no cast while the walls are lit; no cast held back (the charge never left at or over ult.charge)
```

Stage 6 adds two checks, [10] the voice and [11] the picture. Each switches itself on from the page, so
the same probe still reads [0]-[9] alone on stages 2, 3 and 5 (§5d).

[0] makes the probe a standalone gate after a carry: a mis-carried number fails it, not only the
builder's own ult-block check. [1]'s close is split: the caster-death close is exercised on every
stage; the foe-death close reads 0 on every stage, as reading 1 says it must.

**The whole-state reads (review round 3).** The design gives a touch two effects and no more:
"hexes them, and hurls them straight back at the hammer ... The walls do no damage -- they hand
the enemy back." Round 2's [6] and [7] compared fixed lists of fields (the foe's position, hp,
shield, stun, pin and statuses; the caster's position, velocity, hp, shield, stun, pin and
statuses), so a rune that changed anything else passed: the review's two mutants of the final
link, a touch that drains a second of the foe's ultimate charge (67.3% against 43.0) and one that
flips its spin direction (44.5%), both read 10/10, and the builder's static refusals catch
neither. Now, around every rune tick, the probe takes a deep snapshot of each fighter's own
enumerable state and the Match's, before the tick and before it wraps anything, and again after:
numbers, booleans, strings, null / undefined, and plain objects, arrays, typed arrays, Maps and
Sets of those, walked to the bottom; a Twinshade shade walked like a fighter; the two fighters met
inside another field recorded by identity (each has its own snapshot); any other class instance
recorded by identity and NAMED in the output (none met on any stage); a cycle is a marker. It skips
the shared weapon `w` and the affinity `aff`, and exactly what the design lets a tick change,
each rebuilt exactly by its own check: the foe's `vx`, `vy` ([5], now on the closing frame too)
and `status.hex` ([4], now the whole status object against `apply`'s own result); the caster's
`ultRunes` and `runeTally` (the window's own record, [1] and [3]). Any other difference fails [6]
(the foe or the Match) or [7] (the caster) and names the field. **The one limit, for speed:** an
array longer than 16 is read as its length and its last 16 entries, walked -- the Match's growing
logs (`beats`, `fx`, `motes`, `drains`, `events`) and a few others the output names (`shots`,
`shades`, the fighters' `trail` and `tips`, Ironwood's `treeLeaves`, `ultTrace`): an append or a
change to a recent entry is caught, a rewrite of an old entry is not. A probe run is ~1.5 million
rune ticks, each read three ways; the run takes ~5.5 minutes where round 2's took one.

- **sc-lodestone-runes (stage 2): 10/10** (`runs/probe_runes.txt`). 3.76 casts; 8.49 touches and 8.49
  hex a cast; the foe at 3.94 hex stacks on an average window frame; 7.18 blows in windows and 7.20
  outside a fight; 75% of touches on a closed-in hall (10,850 of 14,552); 959 window frames a clock
  close, 9.00s of match time; 11.7% of window steps frozen. Closes on a death: the caster's 31, the
  foe's 0; 243 of 456 fights end with the walls still lit, all still lit 240 verdict steps on.
- **sc-lodestone-rebuttal (stage 3): 10/10** (`runs/probe_rebuttal.txt`). 3.51 casts; 8.56 touches,
  hexes and hurls a cast, every hurl at 700.000000; 3.97 stacks; 8.35 blows in windows and 6.86
  outside; 9.17s a clock-closed window; 13.3% frozen; the caster's death closes 36, the foe's 0; 243
  of 456 end lit. (Lab arm C on 151: 3.43 casts, 8.40 touches, 4.00 stacks, 7.48 / 7.51 blows. The
  built window holds more blows because it is longer in match time; its touch count does not grow,
  because the cooldown is on the same window clock.)
- **sc-lodestone-b205 (stage 5): 10/10** (`runs/probe_b205.txt`). 3.72 casts; 8.55 touches a cast
  (14,518 in all, 73% on a closed-in hall); 4.00 stacks; 8.96 / 7.20 blows; 9.16s; 13.3% frozen;
  1,413 clock closes; the caster's death closes 49, the foe's 0; 53,221 window frames with the caster
  itself on a wall, none of them changing it; 30,587 wall frames under the cooldown (the "missed
  touch" test's material); **236 of 456 fights end with the walls still lit (Lodestone won 127 of
  them, lost 109), all 236 still lit 240 verdict steps on** -- the stage-6 note in §5. The
  whole-state reads: 1,487,433 rune ticks, each read on the foe, the caster and the Match, none
  changing anything but the declared fields; no class instance met that the walk could not open.
  Every count is the same as round 2's probe on round 2's link (the new reads add checks, not
  numbers). Stages 2 and 3: 1,513,504 and 1,400,071 rune ticks read whole, the same.
- **Controls: thirteen mutants of the final link** (`runs/probe_mutants_b205.txt`,
  `runs/mutants_made_b205.txt`, `runs/make_ctl.py`, `runs/mutants_summary.py`; scratch
  `ctl/mut205r3/`), each one edit that changes fights (the probe's 456 fights read 43.0% on the
  link), each failing its own check and only that one (the count is the check's failures):

  ```
  mut-dur      Z.t += dt * 0.9           (the window 11% long)                       54.8%   fails [1] only (149,962)
  mut-pad      e = u.pad + 4.5           (a 6-unit band)                             47.6%   fails [2] only (12,261)
  mut-cd       Z.cd = u.cd * 0.8         (a touch every 0.4s)                        49.6%   fails [3] only (3,928)
  mut-hex2     apply("hex", u.hex + 1)   (two stacks a touch)                        55.3%   fails [4] only (14,677)
  mut-impulse  foe.vx += ..., vy += ...  (an impulse, not the throw)                 51.8%   fails [5] only (15,404)
  rv-dir       dx = foe.x - f.x, ...     (the hurl AWAY from the hammer; the review's) 40.8% fails [5] only (15,895)
  mut-bite     this.hurt(foe, 4, f)      (the design's rejected bite)                67.1%   fails [6] only (40,655)
  rv-drain     foe.charge -= 1 a touch   (drains the foe's ultimate; the review's)   67.3%   fails [6] only (15,194): "the foe's charge"
  rv-spin      foe.spinDir = -spinDir    (flips the foe's spin; the review's)        44.5%   fails [6] only (14,355): "the foe's spinDir"
  mut-clank    this.clankCd >= 0.3       (a touch mutes clanks: the Match)           46.3%   fails [6] only (13,216): "the match's clankCd"
  mut-self     the caster pushed off its own left wall                               51.3%   fails [7] only (13,493)
  mut-charge   f.charge += 0.25 a touch  (the caster's ultimate fed)                 56.4%   fails [7] only (17,090): "the caster ... charge"
  mut-death    drops `|| !foe.alive` from the close                                  43.0%   passes 10/10, every probe count identical: EQUIVALENT (reading 1)
  ```

  rv-drain and rv-spin are the review's own edits, re-made exactly on the rebuilt link: under
  round 2's probe both read 10/10 (the review's finding); under this one each fails [6] and
  nothing else, and names the field. mut-clank and mut-charge are two more of the same kind, on
  the Match and on the caster, which round 2's fixed lists could not see either. mut-bite now
  counts more [6] failures than in round 2 (40,655 against 26,323), the same bites seen again by
  the whole-state read. mut-death is the round-2 review's own mutant, kept as a control of
  reading 1: it removes the foe-death close and nothing changes -- the same win, every probe count
  identical -- which is what "unreachable" means. An earlier cut of the probe failed mut-bite on [7] as well: a rune
  that hurts a warded foe breaks the ward, and `shatter(f, src)` bursts at the source, which is the
  caster. That is [6]'s failure arriving at the caster, not a caster's touch, so [7] is read on the
  frames the runes hurt nobody (0 such frames on the link). mut-bite also prices the rejected bite
  again: +24.1 (67.1 against 43.0) in the probe's sample, the design's +12 (§3) on 141.
- **Stage 1 is arm A fight for fight** on both blocks (§2).

## 4. Stage 5: the blade — 20.5, the measured point nearest 50%

Both sides (`relic_rate.py`: each seed played from both sides; every other relic a foe, 10 seeds a
foe a side, 760 fights a block; seed0 2207 and 2317; `--set dmg=X` on `sc-lodestone-rebuttal`, whose
own blade is 23.5; `runs/stage5_rr_*`, `runs/stage5_table.txt`):

```
blade   block 1   block 2   pooled (1520)   side A   side B   mean
19      42.9      43.9      43.4            43.3     43.6     66.9s
20      48.4      42.1      45.3            43.7     46.8     65.9s
20.5    48.8      49.2      49.0            50.9     47.1     65.7s    <- the blade (sc-lodestone-b205)
21      54.7      53.0      53.9            54.7     53.0     65.3s
21.5    51.4      55.8      53.6            53.3     53.9     64.5s    (the brief's forecast band)
22      52.5      55.5      54.0            54.1     53.9     64.6s
23      57.0      57.4      57.2            58.0     56.3     63.3s
23.5    55.7      60.0      57.8            57.4     58.3     62.9s    (stage 3, no --set)
```

- **The order the points were measured in, said plainly.** The first attempt ran the integers, 19
  to 23, and picked 21 (53.9%). Resume 2 added 20.5, 21.5 and 23.5 (23.5 is stage 3 itself, with no
  `--set`) and picked 21.5, reading the brief's forecast band as a constraint. Review round 2 moved
  the blade to 20.5. The v87 handoff says a blade is settled "never by bisection". The half points
  are one refinement of the same grid, run both sides and on both blocks like the integers, not a
  search that halves toward the line. They were still added after a pick had been made, and a
  reader should know that. Every point is kept and reported.
- **The fit.** A least-squares line through all eight pooled points has a slope of 3.36 points per
  blade point and crosses 50% at 20.78. At 1520 fights a point the standard error is 1.28 points.
  The curve is not a line. The eight points scatter 1.73 points around the fit, against that 1.28
  standard error. Like the published curve (49.7 / 48.5 at 21, 50.3 at 22 on 141), it is flat from 21
  to 22 (53.9, 53.6, 54.0): those are the hammer's kill steps. On 151, with the engine's window,
  the flat sits near 54 rather than 50, so the crossing falls on the step below it, between 20.5 and
  21. The two measured points that bracket 50% cross, locally, at 20.60.
- **The blade is 20.5, THE MEASURED POINT WHOSE POOLED RATE IS NEAREST 50%.** It reads 49.0%
  (48.8 / 49.2; side A 50.9, side B 47.1), 0.8 standard errors under 50. 21 reads 53.9%, 3.0
  standard errors over. **By the other criterion the batch has used, blade distance to the fitted
  crossing, the blade is 21, not 20.5.** 20.78 is 0.22 from 21 and 0.28 from 20.5, and the line
  predicts 50.7% at 21 and 49.0% at 20.5. v100 and v101 wrote theirs as "the measured point
  nearest" the crossing (23 at ~22.8; 18 at ~18.2); there the two criteria agree -- 23 also read
  nearest 50% (50.8 against 22's 46.8), and 18 did (48.5 against 19's 55.6) -- so the batch has no
  precedent for the case where they part, which is this one. Round 2 of this build called 20.5 "the measured point
  nearest the crossing", and that was wrong in blade units. This build reads the measured rates
  and not the line, because the curve steps: at 21 the relic has already climbed the step to 54%,
  which the line averages away. **20.5 against 21 is Rick's** (§6). The brief's header says "The
  build owns the blade", and the v87 handoff says a design's blade is a bracket, settled wide, both
  sides, two blocks, on 151. 20.5 is above Bulwarden's 20.1, the row floor the design names (§4).
- **No knob moves.** The brief names none to move first: its §3 closes the hurl speed ("noise"), the
  cadence ("costs 7") and the bite ("not taken"). Said here.
- **The brief's forecast, 21.5-22, is where the LAB crosses; the built relic runs over it by the
  window clock.** Side A, the lab's 33 foes, 660 fights a block, with the two controls of §2, at the
  blade and at the forecast (`runs/lab_C205_*`, `built_b205_*`, `lab92_C205_*`, `ctl_labclock_b205_*`;
  `lab_C215_*`, `built_b215_*`, `lab92_C215_*`, `ctl_labclock_b215_*`):

  ```
                                         blade 20.5 (THE BLADE)          blade 21.5 (the forecast)
                                         block 1  block 2  pooled        block 1  block 2  pooled
  lab C on 151                           48.8     46.2     47.5          49.5     51.2     50.4
  BUILT (SHIP)                           52.4     52.0     52.2  +4.7    54.4     54.5     54.5  +4.1
  lab C at the engine's window (dur 9.2) 49.7     50.8     50.3          55.0     56.8     55.9
  the build on the lab's clock           44.4     44.2     44.3          51.7     52.6     52.1
  the build in the lab's order ('after') 52.3     51.7     52.0
  ```

  The built relic reads +4.7 over the lab at 20.5 and +4.1 at 21.5. Each control measures what the
  engine's window clock is worth, from its own side: the lab given the engine's longer window gains
  +2.8 at 20.5 and +5.5 at 21.5; the build put back on the lab's clock loses 7.9 at 20.5 and 2.3 at
  21.5. Each single difference carries about 2 points of noise (1320 fights a side, two separate
  simulations), and the pairs scatter both ways around the gap; pooled over the two blades the gap is
  4.4 and the two controls read 4.2 and 5.1. So the gap is the clock, as at stage 2, and the lab's
  order is not in it (the 'after' build: 52.0 against the built 52.2). Side A against the lab's 33
  foes, the lab crosses near 21.4 on 151 (47.5 at 20.5, 50.4 at 21.5), inside the design's band; the
  engine's window moves the built relic's crossing about a point lower, to 20.78 both sides against
  all 38.
- **The forecast point, for the record:** 21.5 reads 53.6% both sides (51.4 / 55.8; side A 53.3, side B
  53.9), 2.8 standard errors over 50. Its verify reading, side B only, was 50.8% (1520 fights,
  `runs/alt-b215/verify_b215.txt`), so its true rate may be nearer 52. Even so, 20.5 is still the
  measured point nearest 50%. The first cut of this build shipped 21.5, reading the forecast as a
  constraint, and review round 2 moved it. The first attempt's 21 (`sc-lodestone-b21`) and the
  21.5 link are both retired to scratch.
- **The built link is the measured relic:** `relic_rate` on `sc-lodestone-b205` with no knob set
  reproduces both blocks of the `--set dmg=20.5` run: every foe's rate, the by-type rates, both
  sides' rates and the mean duration identical (block 2207 48.82%, 65.61s; block 2317 49.21%,
  65.73s; `runs/stage5_reproduce_b205.txt`).
- **The ladder at 20.5** (40 fights a foe, `runs/ladder_b205.txt`), which the brief asks to print:
  greatsword 77%, bow 54, twinblade 44, scythe 42, flail 42, warhammer 33 (a 44-point spread; the
  design's, at 22 on 141, was 43 points: greatsword 73, flail 59, scythe 45, bow 44, twinblade 43,
  warhammer 30). Worst Ironwood 10%, Bulwarden 17.5, Lastlight 20, Foregone and Portcullis 22.5,
  Twinshade 25; best Axiom and Heartwood 90, Nightfell 87.5, Redflail 85. **Gloamwire reads 32.5, not
  the design's 0** (at 22 on 141). The warhammer row is the worst type, as the design's was. The
  spread and the worst foes are item 12/32, Rick's.
- **The probe on the stage-5 link: 10/10** (§3).

**The gates on the final link, `sc-lodestone-b205`.**

- **engine_ab sc-tendril-t3 -> sc-lodestone-b205, the 38 others, n=6: 4218/4218 identical**
  (`runs/engine_ab38_b205.txt`). Adding Lodestone moves no other fight.
- **verify --n 40 on sc-lodestone-b205 (39 relics, 29,640 matches): 11/13** (`runs/verify_b205.txt`;
  on the rebuilt link its every line but the wall time is round 2's, `runs/r2/verify_b205.txt`).
  Lodestone 46.9% (side B, as verify plays an appended relic; relic_rate's side B at 20.5 reads
  47.1); every relic in 30-70% (Heartwood 31.5 .. Gloamwire 66.6, spread 35.1pp); no JS errors, no
  timeouts. **"Both sides can win every
  matchup" passes**: at 21.5 it failed on Axiom v Lodestone 0/40, Lodestone's own pairing
  (`runs/alt-b215/verify_b215.txt`). The two reds are **the clock bands**, red on every link since the
  minute pace: the pairing band's extremes are Ironhail/Marrowdraw 38.3s and Lightkeeper/Starwarden
  98.4s (not Lodestone's pairings), the overall mean 61.1s (the base's 60.8). Neither is Lodestone's.
- **tip_audit on sc-lodestone-b205: identical to the base's** (`runs/tip_audit_b205.txt`,
  `tip_audit_base.txt`; the one unmentioned field, Burn's `feed`, is the base's own). The build adds
  no status and no status tip.
- **chain_audit --builder lodestone_build.py: 8/8 inserts survive** at sc-lodestone-b205
  (`runs/chain_audit_b205.txt`).
- **Re-applies.** Stages 1 -> 5, the same builder (`0731db270893647b`), onto nine other builds'
  current links in the batch: Bindweed's stage 6 (`sc-tendril-fx`, the chain tip), Portcullis's
  stage 6 (`sc-onslaught-fx`), Cold Iron's stage 5 and stage 6 (`sc-coldiron-temper-b93`,
  `sc-coldiron-temper-fx`), Angelus's `sc-angelus-b9` and Oracle's `sc-oracle-sight` (each a new
  relic already appended: Lodestone lands after it, 40 relics), and Widowmaker's (`b1075`),
  Ironhail's (`b14`) and Lightkeeper's (`bulwark-b9.5`) stage 5s. Every anchor applies once, every
  page parses, Lodestone is last in the array, each composed diff is the base -> b205 diff line
  for line (79 changed lines), and chain_audit reads 8/8 on every composed tip
  (`runs/compose_test_b205.txt`, `runs/compose_b205.py`).

## 5. Stage 6: the picture and the voice — `sc-lodestone-b205-fx`

Design §6.1-6.2 and the brief's stage 6, picked on measurements under Rick's "you pick i overrule"
by two labs run in parallel on the final (`sc-lodestone-b205`): the picture lab (scratch,
`stage6-picture/`) and `tools/lodestone_voice_lab.py`. It is built as **`lodestone_build.py --stage 6`
on the final**: **twelve anchored edits, byte-exact to the labs' own row files** (voice 3, picture 9).
No two rows share an anchor, so none is merged; eleven re-emit their anchor and one replaces the
runic hammer's route outright. The picture rows alone reproduce the picture lab's stamp
(`b40d52b7561c45f2`). The voice rows alone reproduce the voice lab's voice page (`8921a39052799d17`).
Voice and picture together are the voice lab's combined page to the byte (`7a095b143d66fbdb`), in
either order.

The generator (`runs/stage6/gen_s6.py`) checks four things before it writes anything: the returned rows
against the files, the stamp, that no anchor sits inside another's, and both orders. The labs' report
files, which reached disk after it ran, carry the same rows as data (3 and 9;
`runs/stage6/report_rows_check.txt`). It then writes
`S6` into the builder, with a `--stage 6` that:
- refuses to run twice (`'tickLode' is already in this source`);
- refuses anything but the final: stage 3, stage 2, stage 1 and the bare tip all refuse (`Lodestone's
  ult block or blade is not the final's`);
- scans every stage-6 insert and refuses:
  - an RNG draw or `ultFx`;
  - a call into the simulation (`apply`, `hurt`, `beat`, `resolveHit`, `tickRunes` ...);
  - a write to anything but its own `lode*` fields, the canvas, a record's own clock and path, a tag's
    count, `taught` and an oscillator's pitch;
  - a mutation of any array but its own;
  - a touch to the inlined `fx.js` copy.

The picture sheet is `05-reference/v102/lodestone-picture-sheet.png` (2200x3126, sha16
`2d2c10a5d6d9f297`). The voice lab's 47 wavs are `05-reference/v102/lodestone-*.wav` (gitignored by
`.gitignore`'s `*.wav`). Readings 9-16 are in the builder's docstring.

### 5a. The picture (v70 §6.1), as built

The picture lab's scratch is `stage6-picture/`, and its outputs are in `runs/stage6/picture_lab/`.

- **The cast: the rune chain lights.** A chain runs along the live hall's four walls (`m.inset`, so the
  runes walk in with the seals). It has two layers:
  - a soft 9-unit band and a hard 2.2-unit line in the school's core, 2 units in;
  - 60 runes, 12 on the top and the floor and 18 down each side, 12 units in, so a ball touching a wall
    stands on them. Each is one of six staves picked by `shellHash`, dark-stroked under a core line.

  **It lights from the caster's nearest wall outward, both ways round the loop, in 0.3s**
  (ease-out), so the far wall lights last. A spark runs at each front. It is timed on the
  presentation clock, so the 0.08s cast stop does not hold it.
- **Stays lit for the window, shedding rune motes** (the design's field, drawn: §5c). **28 motes** come
  off the lit walls and drift up to 31 units into the hall, each on its own place and phase by
  `shellHash`.
- **The head burns its rune while the walls are lit.** The school's triangle-in-ring sigil etched in
  the head's face (`_makerMark`'s own figure) burns in dark, glow and white while `lodeFade > 0`, and
  dims with the walls' 0.4s go-dark. It is drawn in `drawWeapon` only: weapon icons elsewhere are
  untouched.
- **A touch.** Four things happen:
  - **The flare.** The 60-unit span of each wall the foe met, level with the foe and kept whole on its
    wall, flares in the glow and white over a 16-unit core band for 0.15s. The runes in the span flare
    with it. A corner flares both walls.
  - **The bar.** A jagged rune-light snaps from the wall into the ball it hexes, over both balls, for
    **one frame**: the touch's step and the next on the MATCH clock (one frame at 60 fps). A hit stop
    beginning under it does not hold it.
  - **The rune-streak.** The hurled ball's own recorded path over the last 0.2s is drawn 20 units wide
    and tapering, with runes riding it.
  - **The HEX tag prints the foe's count on every touch.** There is one hex tag on the foe at a time
    (Tendril's rule): the hammer's own blow tags hex too, so a tag already up takes the new count in
    place.

  A touch on the kill's step draws nothing: the shatter owns that frame.
- **How a touch is found:** by watching `runeTally.touches` rise in `tickPresentation` at the end of
  the same step. The walls are re-derived from the foe against `inset + R + pad`, the touch test's own
  sides. So **`tickRunes` keeps no record for the picture**, the sim writes nothing new, and the
  probe's whole-state skip sets ([6], [7]) need no new line. The earlier revision of this doc (then
  §5) expected a record in `tickRunes` and a skip line; neither was needed. This was proven exact on
  every touch in 14 drawn fights.
- **The close: dark from the far wall inward, 0.4s.** The dark front runs from the point on the loop
  opposite the caster's nearest wall at the close, back toward that wall. **Declared, not in the
  design:** when the close is the caster's own death, the chain goes out all at once in 0.1s.
- **THE VERDICT GATE (§5's open item from stage 5): the walls read
  `(this.over || !f.alive) ? null : f.ultRunes`**, the tendril-fx gate. A blow's kill leaves `ultRunes`
  set through the verdict (reading 1), and the walls go dark at the kill anyway.
  - The picture lab's verdict frame probe covered 24 fights, 12 of them ending lit: **0 of 2352
    panel frames carry a rune**, and 0 differ from the picture hidden. The last rune is drawn 0.375s
    after the kill; the panel is first up at 1.075s.
  - **The control `ld-ungated` (`const Z = f.ultRunes;`) draws runes on 1176 panel frames** (98 in each
    of the 12 lit fights), so it FAILS as it must. The probe's [11] now gates the same thing on every
    link (§5d).
- **No new object in the hall:** everything is on the walls or the foe, in the world pass,
  source-over.
- **The silhouette: the runic warhammer's route is redrawn as the design's first cut.** Lodestone is
  the school's first warhammer. Before it, `SHAPES._whConjured` (three conjured slices, no haft) was
  drawn by no relic. It is now "a rune-etched square head on a dark haft":
  - a pale steel square head 0.8 x W on a side, with shaded lower faces and an etched border;
  - the school's sigil cut in its face and a core-coloured striking face;
  - a dark haft with two iron collars.

  Only a runic warhammer reaches it. At the app's 453x805, over 5 frames:

  | hammer | weapon \|dL\| | head \|dL\| | area |
  |---|---|---|---|
  | square head (built) | 0.239 | 0.317 | 4361 u2 |
  | conjured slices (before) | 0.243 | 0.352 | 2850 u2 |
  | a stone variant | 0.185 | 0.225 | |
  | the six shipped hammers | 0.126-0.219 | | |

  The square head is **first of the seven hammers**, as legible as the conjured slices on 1.5x the
  area, and cheaper to draw. In one page, interleaved, `drawWeapon` takes 11.16 against 12.66 ms at
  rest and 8.76 against 9.96 lit (Spellbreaker), and 9.34 against 10.56 and 8.82 against 9.86
  (Dawnbringer) (`picture_lab/cost_sil.out`).
- **The picture lab's numbers** (on the final, through the post chain, Chromium 151):
  - **Bloom** (88 frames, 9 fights, 540x960): the picture's share of the chain's arena-mean lift is
    at most **+0.0000** (min -0.0002; the gate is +0.02). Raw luma adds at most +0.0115.
  - **The discs:** the caster's moves by 0.0000 at most. The foe's moves by 0.0963 at most, which is
    the HEX tag's text printed on it; the art alone is -0.0138 to +0.0167. A disc past 0.90 on 1 of 88
    frames, with the picture and without it alike.
  - **Three controls come back wrong, as they must:**
    - a white halo on the caster puts its disc past 0.90 on 70 of 72 window frames;
    - a 100-unit white band round the hall lifts past +0.02 on 11 of 88 frames;
    - a 200-unit flash at each touch lifts past +0.02 on 5 of 88 and puts the foe's disc past 0.90 on 28.
  - **Legibility** (median |dL| of each part's own pixels, out of a hit stop / in one):

    | part | out / in |
    |---|---|
    | the lit walls | 0.197 / 0.164 |
    | the motes | 0.258 / 0.259 |
    | the head's rune | 0.390 / 0.148 |
    | the flare | 0.161 / 0.078 |
    | the bar | 0.297 / - |
    | the streak | 0.219 / 0.150 |
    | the HEX tag | 0.216 / 0.231 |

    The flare reads low in a stop; the bar, the streak and the tag carry the touch there.
  - **Frame cost** (Electron 44, RTX 3070 ANGLE, 453x805, the post chain on, interleaved frame by frame,
    the PC at about 96% CPU from other builds; frames ran 53-73 ms):
    - whole-frame medians, the rows against the picture off: **+1.7 to +1.8 ms lit, +2.1 to +3.1 on a
      touch, +1.7 to +2.0 at the cast, +0.3 to +1.4 at the close**; the rest column (-0.7 to +1.3) is
      noise;
    - the picture's own calls alone: +1.2 to +2.1 ms in the window;
    - mostly `_lodeWalls` (1.1-1.2 ms: 60 runes, each with its own transform and two strokes). A
      batched-rune candidate measured the same, so the rows were kept.
  - **Sim identity:** 14 whole fights (11 with Lodestone on both sides, 3 without), each undrawn and
    drawn: steps at the kill, state hash at the kill, winner and t all identical to the base. The
    1e-9 sim-write control differs on all 11 Lodestone fights that had a touch, and on none of the 3
    without. The bar is exactly one 60 fps frame on every touch, in both step phases (362 touches).
  - **Beats** (32 fights): `fireUlt` files exactly 125 `ult` beats for 125 casts. Inside `tickRunes`
    there are 0 beats and 0 hit-stop raises over 1083 touches, and every fight's beat list is b205's.
  - **One fight watched** (`picture_lab/watch.out`): Lodestone v Widowmaker, 102007, 73.2s, Lodestone wins, 4
    windows, 36 touches, 0 errors. It ends LIT (`ultRunes` set for 77 verdict frames). The picture goes
    dark 12 frames (0.4s) after the kill, no rune is on a panel frame, and the runes walk in with the
    third seal.
- **The picture lab's own flags:**
  - The ball (R 34) hides the middle of the flare on the touch frame (the design's 30-unit half-span:
    about ±13 units at the flare line). The flare shows fully as the hurl carries the ball off.
  - The streak's code comment says a rune "every 26 units" where the code uses 24. This is cosmetic,
    and was left alone rather than change the stamped bytes.

### 5b. The voice (v70 §6.2; `tools/lodestone_voice_lab.py`)

Every render is an OfflineAudioContext at 48 kHz through the game's own `Sfx.buildChain`. The lab's
controls reproduce v88's published rune-crack (0.608 / 450 ms), BAR (0.364 / 300 ms) and hit@11.6
(0.443 / 80 ms) before anything new is read. Levels are set against Lodestone's own blow (the hit at
20.5, quietest draw). Thirteen relics with no cast arm play rune-crack today, Lodestone among them.

- **The cast: EVEN, of 5** (5 more as controls). The design: "a rising four-note rune chime, one per
  wall, 0.5s total".
  - **A C E A**, the score's A-minor tonic triad up through its octave, from A4. A note every 125 ms,
    one per wall. Each note is a free bar's modes (a triangle and sines at 2.76x and 5.40x).
  - Audible **495 ms**. Every note jumps 32 dB or more in its own band at its onset. Its loudest 50 ms
    is **-2.9 dB re the blow**, and it is heard **+22.4 dB** over the score. Its register is at most
    0.66 against rune-crack, the runic and warhammer casts, the seal's chime, Zenith's cast and the
    blow.
  - **All five candidates pass the rules; the tiebreak picks.** On the most distinct register, to
    0.05, CHIME (0.759, against rune-crack) and GLASS (0.765, against Zenith) drop out. LOW (0.660),
    RUNE (0.668) and EVEN (0.658) share the band and all take 12 synth calls. The register unrounded
    then takes EVEN, which is LOW with its notes spread over the whole 0.5s (every 0.125s, not 0.1s)
    and the sharpest strikes of the five (32 dB against 19-26).
  - The controls come back wrong: CHORD (one chord, not four notes), FALL (falling), NOISE (not notes),
    SEAL (register 1.00) and RC-NOW (what it played before).
  - Lodestone had no arm and fell through to rune-crack, as 12 other relics on this link still do.
    The row ADDS its arms before that shared fallback and re-emits the fallback line unchanged.
- **A touch: ARC3, of 7** (5 controls). The design: "a sharp electric snap (<=80ms, peak <=0.5) with
  the hex's own stun voice underneath if it lands; pitch steps up with the stack count".
  - A 12 ms highpass crack on a held square at the count's note. **The note steps up the A-minor
    pentatonic, 218 / 260 / 292 / 329 / 391 Hz at counts 1-5**, every step 201 cents or more.
  - Rise under 1 ms; gone by 60 ms; peak 0.424 at most; its harmonics -7.5 dB re its note (a buzz).
    Its loudest 50 ms is -3.9 to -3.4 dB re the blow and **+6.3 dB or more over the hex-snap, which
    still stands +4.6 dB over it at 2.6 kHz** (heard under it, not lost in it).
  - Its register is at most 0.43 against the hex-snap, the wall tick, the blow, rune-crack, the clank,
    the burn and the cast.
  - **"The hex's own stun voice underneath"** is the runic school's `hex-snap` (reading 11), played
    under every touch: at hex 1 every touch's hex lands, and at the cap it refreshes.
  - The rejected, all on the hex-snap drowning under them at 2.6 kHz (ZAP +1.0, BUZZ +0.5, ARC -0.2,
    HIGH +2.0, CRACKLE -0.6 dB, against the +3 rule), and some also on a peak over 0.5 (BUZZ, ARC) or
    on register against the cast (ZAP 0.81, ARC 0.84). HUM passes and ties ARC3 on register; ARC3 has
    fewer calls.
  - The controls come back wrong: PING (a chime, not a buzz), FLAT (no pitch step), LONG (185 ms),
    LOUD (peak 0.902) and HEX (the hex-snap alone).
- **The close: MIRROR, of 4** (2 controls). The design: "the chime reversed, quiet".
  - The cast's four notes, each re-struck every whole number of cycles nearest 11 ms (in phase), at a
    level climbing as the cast's own decay reversed, each cut at its mirrored onset. All four swell
    and drop out from the top down, the root last.
  - **-9.0 dB under the cast's top** (-12.0 re the blow). Envelope correlation **0.93** with the
    literal reversal. Gone 685 ms after the window shuts; heard +11.8 dB over the score.
  - The literal reversal cannot ship: it needs an async render, and every clip rebuilds the synth
    synchronously (v88 §6b).
  - The rejected: DESCEND (the notes struck falling: correlation -0.33) and SLOW (0.23). The control
    AGAIN (the cast itself, quiet) fails. SHARP passes, and MIRROR takes it on correlation.
- **Wired and checked in the lab:**
  - Through the patched `play()` every arm reproduces its candidate (worst 6e-08, the touch at n = -1,
    0, 1-5, 7 and missing), and the 126 other voices are unchanged (worst 1e-07). `ult/lodestone` is
    no longer rune-crack (0.841).
  - **152 fights with the rows beside the original: 152 / 152 identical**, and every other voice call
    is identical in order and options. The control (the rows plus a 1e-9 nudge of the foe on a touch)
    is 4 / 152.
  - 565 casts gave 565 cast voices. **4894 touches gave 4894 snaps and 4894 hex-snaps.** 478 clock
    closes gave 478 close voices. **0 voices played on the 12 death closes and on the 75 windows
    still lit at the verdict.**
  - **In a real window** (Aureole v Lodestone, 102602, 13 touches): each touch over the fight
    **median +20.9 dB, least +5.3** against the gate of median 6 and least 3. The +5.3 is masked by
    Aureole's own cast on the same frame. The cast is heard +11.1 dB, the close +27.8.
  - With Bindweed's, Coldiron's, Portcullis's and Ironhail's Sfx rows applied too, in either order,
    every arm renders alike (worst 8.9e-08).
- **The voice lab's flags, printed and not gated** (Rick's to hear):
  - **70% of touches arrive at the hex cap of 5** (3436 of 4894 in the lab's fights; the probe's count
    is in §5d), so the pitch climb is heard over the first few touches of a window, and after that
    every touch snaps on G (391 Hz). The cap is the design's, not the voice's.
  - **The close costs 153 synth calls, 6.7 ms of main thread a call headless** (the cast 0.5, the
    touch 0.1). It fires once per clock close, about 1.5 a fight, and may show as a frame hitch live
    in Electron; nothing was measured there. DESCEND would cost 12 calls, but it fails "reversed".
  - Against the other batch relics' voices, the highest register of these three is 0.83, against
    Portcullis's cast, and 0.82, against Ironhail's cast (Bindweed's 0.64, Coldiron's 0.55). It is
    heard only when those two relics fight Lodestone.
  - **The hex's actual weapon stun (`tickStatus`'s `hexClock` stun) has no voice on any relic.**
    Giving it one would voice every hex in the game, not only this touch's. **Rick's call; not built.**
  - The wavs to hear first: `05-reference/v102/lodestone-pick-sequence.wav`, and
    `lodestone-pick-real-window.wav` against `lodestone-pick-real-window-without.wav`.

### 5c. No `fx.js` field -- the rune motes are drawn

v70 §6.1 says: "Field spec: rune motes along the lit walls, both copies." A SPECS field fires ONCE, at
the one ultFx slot's cast edge, at the caster (life 1.5 half-seconds, radius 300). The picture lab
measured the slot on real fights (`ld_fxprobe.py`: 118 Rebuttal windows, 16 foes x 2 seeds, both
sides):
- **The slot is Lodestone's for a median 0.66s of its 8s window** (max 0.72), so a slot-borne field
  could exist for 7.9% of the window. In 17 of 118 windows the opponent's cast took the slot on the
  cast's own step (Aureole's beam, Axiom's echo, Dawnbringer's dawn, Morningstar's sun, Widowmaker's
  nova).
- **The caster stands a median 87 units from its nearest wall**, and only a median 36% of the lit
  walls' length lies within the spawn radius (p10 27%, p90 63%).
- **Of 1034 wall points touched, the median is 263 units from the field's spawn point** (p10 124,
  p90 456), and only 103 touches came while the slot was still Lodestone's.

A field "along the lit walls" cannot live on that slot. So the motes are drawn: 28 of them, shed off
the lit walls for the whole window, following the lit front (they light with the chain and go dark with
it), on all four walls of the current hall. They add +0.0000 to the bloom. **No SPECS entry goes into
either copy:** the base's inlined `var SPECS = {` has no Lodestone entry, and the builder asserts the
inlined copy untouched. **`fx_spec` is NONE.** This is Zenith's, Canopy's and Temper's precedent.
**Rick's to overrule.**

### 5d. Stage 6's gates -- every one able to fail

Every file named here is in `runs/stage6/`. The labs' own outputs are in `runs/stage6/picture_lab/`
and `runs/stage6/voice_lab/`, and the mutants' probe runs are in `runs/stage6/mut/`.

**engine_ab** (sc-lodestone-b205 -> sc-lodestone-b205-fx, ALL 39 RELICS WITH Lodestone, n=6)
- **PASS: 4446 / 4446 matches identical field for field.** No page errors, 39 / 39 distinct winners,
  4446 distinct seeds, fights 20.3-118.1s (`engine_ab39.txt`). Presentation moves no fight,
  Lodestone's included.
- The labs' own engine_ab: b205 to the picture page, 4446 / 4446 (`picture_lab/engine_ab39.out`);
  b205 to the voice page, 4446 / 4446 (`voice_lab/engine_ab_voice.txt`).
- **The control** (the voice page plus one 1e-9 sim write on a touch, 8 relics) FAILS with 42 / 168
  differing, exactly Lodestone's 42 fights (`voice_lab/engine_ab_simctl.txt`).

**lodestone_probe: 12/12 on sc-lodestone-b205-fx** (`probe_fx.txt`, 456 fights, Lodestone both sides
x every foe x 6 seeds; the probe is `tools/lodestone_probe.py` `36f3bf08321637f0`, patched by
`patch_probe6.py`)
- **Every line of [0]-[9] and every mechanism number is `runs/probe_b205.txt`'s to the digit, but one**
  (`probe_fx_vs_b205.txt`): the whole-state walk's list of arrays read as length + last 16 now also
  names `caster.lodeFx`, the picture's own record. Its streak path runs to 96 numbers.
- The two new checks switch themselves on from the page: [10] when `"lodestone-touch"` is in
  `AC.SFX.play.toString()`, [11] when the Match has `tickLode`. So the same probe still reads ten
  checks on a link without stage 6. On `sc-lodestone-b205` it reads **10/10, every line identical to `runs/probe_b205.txt`**, which the
  stage-5 probe (`85b2d01e7897d0c7`) wrote (`probe_b205_newprobe.txt`, `probe_b205_newprobe_diff.txt`).
  The stage-2 and stage-3 links carry no stage 6 either and were not rerun under it.
- **[10] the voice:**
  - Exactly one cast voice inside every Lodestone `fireUlt` (1698), and none inside any other relic's
    cast.
  - Inside every `tickRunes` call, exactly its events' voices, in order:
    - a touch plays the snap, whose `n` is the count the foe carries after THAT touch's hex (read in
      the apply and again when the voice plays), and then the `hex-snap` under it. That is 14518 of
      each, at n 1-5 = 900 / 1099 / 1166 / 1166 / **10187** (70% at the cap, as the voice lab found);
    - a window that closes BY ITS CLOCK with both alive plays one close voice (1413);
    - a window that closes on a death plays nothing (49, all the caster's);
    - nothing else plays. `tickRunes` hurts nobody, so no ward shatter's own crit hit voice (played
      inside `hurt()`) can sound there: [6] fails any hurt first.
  - **The 236 fights that end with the walls still lit play no close at the verdict.**
  - Every Lodestone voice of the run is accounted for by those events.
- **[11] the picture:**
  - `tickLode`, the picture's one hook on the step, leaves the sim exactly as it found it on each of
    its **7,011,283 calls** and draws no RNG. The sim here is both fighters' bodies, statuses, window
    and tally, and the match's clock, stop, verdict, holds, hall, beats and shots.
  - The walls are lit (`lodeFade` exactly 1) exactly while the window is open, the match runs and
    the caster stands (3,198,716 calls), and are going dark on 151,536 more.
  - Every live touch gets exactly one new record at the foe's spot, carrying the walls the touch test
    met (`inset + R + pad` at the touch), its own count, clock and match time: 14515, 83 at a corner,
    10617 in a closed-in hall.
  - Every live touch has a HEX tag on the board reading the foe's count (14515, 4328 under the cap).
  - The 3 touches on a kill's step draw no record and add or recount no tag.
  - Walls still showing at `over` (lit, or already going dark) are dark 0.51s into the verdict (290
    fights; 236 of them end with the window itself still open).
  - No touch goes unseen by the picture.
  - **On the DRAWN subset**, 54,427 frames are drawn: 49,378 with the picture up, 6,775 of those in a
    hit stop, 316 in the verdict. None throws, draws the match's RNG or changes the sim. The drawn
    subset is the first seed, both sides, every foe, through the kill and the verdict, every 6th step
    while the picture shows, with the post chain off.
- **Controls, one thing each, each failing its own check alone.** They are `probe_mut_*.txt`, made by
  `mutants6.py`, on one seed (76 fights); the clean link on the same seed reads 12/12, with the drawn subset on
  (`probe_fx_s1.txt`):
  - **mV1**, the close voice on every close, a death's as well as the clock's, fails **[10] alone**:
    9 findings, the 8 death closes voiced and the run's accounting (244 close voices against 236 clock
    closes). The fights are unchanged (40.8%).
  - **mV2**, the snap played BEFORE its hex lands, fails **[10] alone**: 909 findings, every touch that
    added a stack snapping one count short (`"lodestone-touch:2@2"` where `3@3` is due). A refresh at
    the cap snaps at 5 either way. The fights are unchanged.
  - **mP1**, `tickLode` nudging the foe it records by 1e-9, fails **[11] alone**: 2405 findings, "tickLode
    changed the sim". It also moves the fights, 40.8% -> 63.2%, which engine_ab would catch too.
  - **mP2**, a drawn frame nudging the caster whose walls it draws by 1e-9, fails **[11] alone**:
    51,032 findings, "a drawn frame changed the sim", one on every drawn frame with the walls showing (the
    5,172 drawn frames it passes are the ones with them dark). Its fights move too, 40.8% -> 60.5%: on
    one seed every fight is in the drawn subset. Headless fights never draw, so only the drawn subset can
    see it: engine_ab, which runs headless, could not.
  - **mP3**, the walls reading `ultRunes` alone (the picture lab's `ld-ungated`, no `!over` gate),
    fails **[11] alone**: 20,570 findings, "lodeFade 1 with the window not live (over true, alive true)", and the walls lit at
    `over` are dark 0.51s later in only 12 fights, against the clean run's 46. The fights are unchanged (40.8%). It writes no sim field; it is the verdict bug stage 5 flagged, and
    the probe now gates it on every link.

  mV1, mV2 and mP1 ran with `--no-draw` (`qM3.sh`): the PC was at about 96% CPU from the batch's other
  builds, and a drawn one-seed run took 30 minutes. They aim at [10] and at `tickLode`, which the
  headless run reads whole. mP2 and mP3 ran with the drawn subset, as the clean run did.

**render_ab** (sc-lodestone-b205 -> sc-lodestone-b205-fx)
- **The other relics' pairs PASS: 24 / 24 frames pixel-identical** (`render_ab_others.txt`). The pairs
  are paradox:heartwood:25064, twinshade:lastlight:991, bulwarden:vinesower:70707 and
  axiom:grudgebearer:31337, at 0.5 / 6 / 12 / 22 / 31 / 40s.
- **The control, Aureole v Lodestone 102602 at 61.6-70s, inside a lit window, is 0 / 6 identical,
  exit 1**, as it must be (`render_ab_control.txt`).
- The labs' own: the picture lab's 54 / 54 on nine other pairs and 0 / 6 on each of two Lodestone
  pairs (`picture_lab/renderab.out`). The voice page against b205 is 24 / 24, and 8 / 8 over the lit
  window (a voice draws nothing); the voice page to picture+voice is 0 / 8
  (`voice_lab/render_ab_*.txt`).

**chain_audit** (`--relic sc-lodestone-b205-fx --tip sc-lodestone-b205-fx --builder lodestone_build.py`)
- **ALL 20 INSERTS SURVIVE, exit 0** (`chain_audit_fx.txt`): stages 1-5's eight and stage 6's twelve.
  One, stage 6's fighter fields, is found by its comment text: the code it adds is shorter than the
  audit's floor. The probe's [11] reads those fields on every fight.
- **The control** (the same relic against `sc-lodestone-b205` as the tip) finds **12 LOST, exit 1**
  (`chain_audit_fx_ctl.txt`): every stage-6 insert, and only those.

**tip_audit on sc-lodestone-b205-fx: exit 0, its body identical to the final's** (`tip_audit_fx.txt`
against `tip_audit_b205_utf8.txt`, both run today with a UTF-8 console, diffed past the first line,
the page's path: `tip_audit_diff.txt`). Stage 6 touches no status tip. Against stage 5's
`runs/tip_audit_b205.txt` the only difference is one em-dash, which that run's cp1252 console printed
as a replacement character.

**The builder** (`builder_checks.txt`, `builder_checks.sh`)
- It refuses seven things: to run twice, to overwrite, stage 6 on stage 3, on stage 2, on stage 1 and
  on the bare tip, and stage 5 on the fx link.
- **Stages 1, 2, 3, 5 and 6, rebuilt from `02-chain/sc-tendril-t3` into a temporary folder, match every
  link's sha**: stub 3273, runes f779, rebuttal d48d, b205 6d73, fx 7a09. Stages 1-5 are the rebuilt
  links of §1 to the byte: the builder grew by `S6` and its `--stage 6`, and nothing else in it moved.
- Rerun at the close of stage 6, after the session was cut by a usage limit: every line the same
  (`builder_checks_recheck.txt`).
- **Its own guards can fail** (`builder_controls.txt`, `builder_controls.py`). Ten copies of the
  builder, each with one forbidden thing written into a stage-6 insert, all REFUSE and write nothing.
  The ten are: a sim write (`foe.x +=`), an RNG draw, the ultFx slot, a `beat`, an `apply`, a write
  to the tally, a write to the window, a splice of `tags`, a write into `beats[...]`, and a
  `Math.random`. The unmodified builder writes `7a095b143d66fbdb`.

**It composes** (`compose6.txt`, `compose6.sh`)
- Stages 1, 2, 3, 5 and 6 chained on the real tip give `sc-lodestone-b205-fx` to the byte.
- On nine other builds, **stage 6 writes the same 590-line diff (md5 `403421dd3e62`) on every one**.
  The nine are: the batch line's tip as it stood (`sc-ironhail-fxout`), `02-chain/sc-tendril-fx`,
  `sc-onslaught-fx`, `sc-coldiron-temper-fx` and `sc-ironhail-sunder-fx`, and the batch's scratch
  links `sc-angelus-b9`, `sc-lightkeeper-bulwark-b9.5`, `sc-oracle-b10` and `sc-widowmaker-b1075`.
- The other way round, all apply on `sc-lodestone-b205-fx`: angelus 1-2-3-5, coldiron 1-6, ironhail
  1-2-3-6, lightkeeper 1-2-3-5, oracle 1-2-3-5, widowmaker 1-2-5, and bindweed's and portcullis's
  stage 6.
- The voice rows share the rune-crack fallback line with Bindweed's, Coldiron's, Portcullis's and
  Ironhail's Sfx rows, and the picture shares `tickPresentation`'s head. Both orders render alike.

**The verdict** (the stage-5 open item)
- The probe's [11] reads it on every link: walls lit at `over` are dark 0.51s in, and `lodeFade` is
  never 1 once `over` is set.
- The picture lab's frame probe: 0 of 2352 panel frames carry a rune. The ungated control: 1176 do.
- **The beats:** `fireUlt` files one `ult` beat a cast, and a touch files none. These are the picture
  lab's `beats.out` (125 of 125, 0 over 1083 touches, every beat list b205's) and the voice lab's
  `beats_ab.txt` (152 / 152 identical, 561 beats = 561 casts). The control that files a beat on every
  touch is 4 / 152.

**Not run here:** `shell_identity` (the app's json is shared: the orchestrator runs it), and verify
(stage 6 moves no fight: see engine_ab above, over all 39 ids).

### 5e. The clip (Rick's to overrule)

`tools/_lodestone_pick.py` (from `_ironwood_pick.py`, by way of `_ironhail_pick.py`) scores a window on
v70 §6.1-6.2. **It READS the voices**: `SFX.play` is wrapped, and it is a no-op headless. So the counts
are the `n` each snap was played at, and the close is the close voice itself. A window must meet three
conditions to score:
- it closes BY ITS CLOCK with both alive (the only close with the reversed chime and the far-wall
  go-dark);
- it has its cast voice and at least two touches;
- the fight runs on for the clip's 1.8s tail.

Each count the snaps are pitched at scores a point, so a window that climbs 1-2-3-4-5 beats one that
starts at the cap. A corner touch (two walls flare) and a touch in a closed-in hall add a little. It
ran on 12 foes x 6 seeds, plus the voice lab's real window (Aureole 102602) and the picture lab's
watched fight (Widowmaker 102007), Lodestone side A (`runs/stage6/pick.txt`).

**The pick: Lodestone v Heartwood, seed 102238**, cast at 47.82. It is a clock window of 9.61 match
seconds with 12 touches, **the foe's count heard at every step, 1 -> 5, from none**, one corner touch
(the floor and the left wall), and all of it in a hall closed in by the seals (score 18.10, against
Starwarden 102201's 18.00; Widowmaker 102007 17.60 and Aureole 102602 17.40).

    python tools/cinema_clip.py --game <scratch>/lodestone/links/sc-lodestone-b205-fx.html \
      --a lodestone --b heartwood --seed 102238 --at 46.62 --window 12.61 --end-at-window \
      --fps 60 --w 540 --out 07-shorts/v102/rebuttal-window.mp4

**`07-shorts/v102/rebuttal-window.mp4`**: 12.62s, 757 frames, 540x960 at 60fps, AAC 48 kHz stereo,
3,231,720 bytes. The fight is still on at the end (193 v 214; `clip.log`).

**The timeline** (`clip_timeline.txt`, clip time, the voices read off `SFX.play`):
- the cast at 1.20;
- the touches:

  | clip time | count | wall |
  |---|---|---|
  | 1.30 | 1 | the floor |
  | 2.04 | 2 | the floor |
  | 2.75 | 3 | the floor and the left wall (a corner) |
  | 3.70 | 4 | the right wall |
  | 4.51 | 5 | the right wall |
  | 5.24-10.43 | 5 | seven more, each wall |

  every touch with its `hex-snap`;
- **the clock close at 10.81**, with its close voice.

The match's two earlier windows (18 touches) are before the clip.

**Frames checked through the pipeline** (`05-reference/v102/lodestone-clip-tile.png`, an ffmpeg tile of
frames 81 / 166 / 277 / 426 / 660; `lodestone-clip-bar.png`, frames 164-166 cropped at the corner touch):
- **Frame 81 (1.35s):** the chain lighting from the caster's nearest corner. Runes are lit up the left
  wall and along the floor, a spark runs at each front, the rest of the hall is still dark, and HEX 1
  is on the foe with the "Rebuttal" banner.
- **Frame 166 (2.77s):** the whole loop lit with its 60 runes, the corner flare on the floor and the
  left wall, and HEX 3 on the foe.
- **Frame 277 (4.62s):** HEX 5 on the foe and the rune-streak off the hurled ball.
- **Frame 426 (7.10s):** the walls lit with their motes, and the square head's sigil burning.
- **Frame 660 (11.00s), 0.2s after the close:** the loop dark but for its last stretch in the top-right
  corner, going out from the far wall inward.
- **The bar is on frame 164 alone**, the touch's own frame: a jagged white bolt from the corner into
  the ball. Frames 165 and 166 carry the corner's flare and no bar.

The art renders through the post chain.

**The AAC** (`clip_aac.txt`): mean -22.0 dB, max -2.8 dB; integrated -19.9 LUFS, LRA 1.3 LU, true
peak -2.1 dBFS.

**The voices read off it** (`clip_audio_check.txt`: Goertzel on the decoded mono track, the 60 ms
after each event against the 60 ms before):
- **The cast's four notes step up at their onsets**: A4 +33.6 dB, C5 +15.9, E5 +14.4, A5 +38.7, 125 ms
  apart.
- **Every touch's snap is heard at its count's note**: 262 / 294 / 330 / 392 Hz at counts 2-5, +13.4
  to +41.0 dB.
  - The first touch comes 0.1s after the cast, under the chime. Its 220 Hz note reads -4.4 dB there,
    but its square's third harmonic (660 Hz) reads +17.1 dB.
  - Every touch's `hex-snap` reads +7.3 to +37.0 dB at 2.6 kHz.
- **The close:** the four notes swell and drop out top first. Over each note's last 0.1s before its
  cut, A5 reads +30.7 dB, E5 +31.6, C5 +20.0 and the root +3.9 against the 0.3s before the close. The
  level falls from -21 dBFS before the close to -37 dBFS under it: "quiet".

**Rick's to overrule, all of it.**

## 6. What is left, and whose

- **Rick:**
  - **the veto** (brief §4 item 1, design §7 item 1). If the hurl reads as the foe being
    "controlled" rather than thrown, the hex-only fallback is one number, `hurl:0`. The stage-2 link
    is exactly that at blade 23.5 (55.5% side A against the lab's arm H 51.8). The fallback at the
    settled blade is not measured; it would need its own stage 5. Nothing built waits on it. It is
    waived under the batch's no-vetoes ruling unless Rick raises it.
  - **the blade: 20.5 against 21.** The build ships 20.5, the measured point whose pooled rate is
    nearest 50% (49.0%, against 21's 53.9%). Measured by blade distance to the eight-point line
    (crossing 20.78), 21 is the nearer blade (0.22 against 0.28, and the line predicts 50.7% there).
    v100 and v101 wrote theirs as the measured point nearest the crossing, where both criteria
    picked the same blade; here they part. The curve steps between 20.5 and 21, and the measured
    rates say which side of 50 each point sits on, so this build reads the rates (§4). If Rick wants
    the blade-distance rule, the change is one number in the builder, `BLADE = 21`, plus new
    stage-5 and stage-6 links and their gates (probe, reproduce, engine_ab, verify).
  - **the design's forecast band**, 21.5-22, reads 53.6-54.0% built. The lab still crosses there on
    151 (50.4% at 21.5), and the gap is the window clock (§2, §4). This is also one number in the
    builder if Rick wants the band.
  - **Axiom v Lodestone in verify** is no longer red: at 20.5 "both sides can win every matchup" passes
    (at 21.5 it failed on Axiom v Lodestone 0/40). Axiom is still one of Lodestone's two most lopsided
    foes (Axiom and Heartwood, 90% each in its ladder; item 12/32).
  - **the spread** (brief §4 item 3, design §7 item 3; item 12/32): greatsword 77 to warhammer 33, 44
    points (the design's 43 at 22 on 141). The worst foes are Ironwood 10, Bulwarden 17.5 and
    Lastlight 20. Gloamwire reads 32.5, not the design's 0.
  - **the hurl is worth +7 on 151** (arm B), not the published +2, and +8 on top of the hex, not +4.
    The design's "the hurl is worth nothing" (§3) is a 141 reading. Nothing was changed for it.
  - **no arrival hitstun** (brief §4 item 4, design §7 item 4). A hurled foe carries no hitstun on
    arrival. The design prices this NO ("it is a throw, not a hit"); it is declared and none is built.
    The builder refuses an insert that writes `stun`, and the probe's [6] reads the foe's stun
    unchanged on every rune tick.
  - **the blurb** (reading 8) is the build's composition; the card is the brief's.
  - **Stage 6, all Code's picks under "you pick i overrule" (§5):**
    - the clip (`07-shorts/v102/rebuttal-window.mp4`, §5e);
    - the sheet (`05-reference/v102/lodestone-picture-sheet.png`);
    - the voices: the EVEN chime, the ARC3 snap stepping up the pentatonic with the `hex-snap` under
      it, and the MIRROR close (wavs in `05-reference/v102/`);
    - the picture: the chain lit outward in 0.3s, the 60 runes, the flare, the one-frame bar, the
      rune-streak, the HEX tag's count, the head's sigil burning, and the far-wall-inward go-dark;
    - **the rune motes drawn in place of an `fx.js` field** (§5c);
    - **the square head over the conjured slices** (the runic warhammer's route redrawn);
    - **the 0.1s go-dark on the caster's fall** (declared, not in the design);
    - the bar on the match clock (one frame at 60 fps);
    - the head's sigil fading with the walls, rather than cutting at `over`.
  - **The voice lab's flags** (§5b):
    - 70% of touches arrive at the hex cap, where the snap no longer climbs;
    - the close costs 153 synth calls (6.7 ms of main thread a call headless), about 1.5 a fight, and
      was not measured live in Electron;
    - Portcullis's cast registers 0.83 and Ironhail's 0.82 against these voices;
    - **the hex's own weapon stun (`tickStatus`) has no voice on any relic.** Giving it one would
      voice every hex in the game. That is a mechanic-wide call, Rick's, and not built.
  - **The picture lab's flags** (§5a): the ball hides the middle of the flare on the touch frame
    (ballR 34 against the design's 30-unit half-span), and the flare in a hit stop reads low (|dL|
    0.078; the bar, streak and tag carry the touch there); about +1.7-1.8 ms a lit frame on a busy PC.
- **The brief's gates, as run:**
  - stage 1's "verify 15-25%" is replaced by the stronger identity, **stage 1 = arm A fight for
    fight** (all 1320 fights of the two blocks, 16 fields a fight, `runs/stage1_vs_A_f4f.txt`; arm
    A itself reads 21.3%, inside 15-25). Stage 1's tip_audit is the final link's (identical to the
    base's). Stage 1's and stage 3's "engine_ab on 36" are the final link's engine_ab on all 38
    base ids (every stage adds only Lodestone's own row and code, which the probe reads);
  - stage 2's **"FILM the walls flaring"** is the stage-6 clip (§5e): nothing drew the walls before
    stage 6;
  - stage 5's "verify 30-70 on 37" is verify on 39, this tip's roster plus Lodestone;
  - stage 6's "field in both copies" is drawn instead (§5c), and "`GAME` moved" is the orchestrator's
    (below).
- **The orchestrator (ALL DONE at the carry, §7):**
  - carry the five links onto the chain with `lodestone_build.py --src <tip>`, stages 1, 2, 3, 5 and
    6, each on the one before. Stage 6 goes on the carried stage-5 link and refuses anything else.
    Prove each carry with engine_ab (stage 6 over every id, Lodestone included).
    `lodestone_probe.py --game <the carried link>` is the mechanism's own gate there: 10/10 on stages
    2, 3 and 5, and **12/12 on the stage-6 link** ([10] and [11] switch themselves on from the page);
  - `shell_identity` on the carried stage-6 link (not run here: the app's json is shared);
  - `app/main.js`'s `GAME` line is not this build's: the build of record is yert's staff row
    (`sc-nightglass-fx`) since 2026-09-28, and where the batch line meets it is the orchestrator's
    and Rick's call;
  - the clip to Rick (one clip per ultimate).
- **The probe's one declared limit (this build's, said so it is not mistaken for a pass):** the
  whole-state reads walk every field, but an array longer than 16 is read as its length and its last
  16 entries. Those arrays are the Match's growing logs, the fighters' trails and, since stage 6, the
  caster's `lodeFx` (its streak paths); all are named in the probe's output. So a rune that rewrote
  an OLD entry would pass. Nothing in `tickRunes` touches an array, and the picture keeps no record
  there (§5a). `tickLode`'s own writes are read by [11] against the sim, not the picture.
- **Standing, not this build's:** verify's two clock bands (pairing mean 18-70s, overall 28-54s),
  red on every link since the minute pace.

## 7. The carry onto the chain

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Ironhail's
redesign with the same builder, one stage at a time (`--src` the previous link):

```
sc-ironhail-fxout.html            the batch line's tip (Ironhail, fx spec out)   4b3775e5900172ea
  -> sc-lodestone.html             stage 1                                        3d5a9a1cc14e1922
  -> sc-lodestone-runes.html       stage 2                                        f3a7e0ba2e40971e
  -> sc-lodestone-rebuttal.html    stage 3                                        a13ca38cf21cbbd9
  -> sc-lodestone-b205.html        stage 5                                        e3ae46f68b371113
  -> sc-lodestone-b205-fx.html     stage 6                                        4568c2995d06f696
```

**The carry is proven two ways**, because the scratch base is older than the tip it lands on:

- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail, n=6: **4218/4218 identical** (`runs/carry_engine_ab.txt`). Ironhail is left out
  because the chain redesigned it after the scratch base: the first run over all 39 ids differed in
  exactly 228 fights, Ironhail's 38 foes x 6 seeds, the old nova against the new hail
  (`runs/carry_engine_ab_with_ironhail.txt`), and nothing else.
- **tip A/B** -- the tip `sc-ironhail-fxout` against the carried stage-6 link, every relic on the tip
  (39), n=6: **4446/4446 identical** (`runs/carry_engine_ab_tip.txt`). Lodestone moves no other
  relic's fight on the batch line, Coldiron's Temper and Ironhail's hail included.

**Gates on the carried stage-6 link** (`runs/carry/`):
- engine_ab stage 5 -> stage 6 over all 40 relics on this tip, Lodestone included, n=6: **4680/4680
  identical** (`engine_ab40_s6.txt`): the picture and the voice move no fight here either;
- `lodestone_probe.py` **12/12** (456 fights), [10] and [11] on (`probe_fx.txt`);
- tip_audit exit 0;
- **shell_identity 200/200** (app Chromium 152 vs headless 151; the pointer not moved, the json
  restored);
- yert's staff carry, dry run onto this link: all stages hold, syntax ok (`staff_carry_dry.txt`).

The clip stays the scratch one (`07-shorts/v102/rebuttal-window.mp4`): Lodestone v Heartwood 102238 is
inside the scratch A/B (neither moved), so the carried fight is the filmed one.

**The roster is 40 on the batch line.**
