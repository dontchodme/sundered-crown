# v107 — LIGHTKEEPER / BULWARK (REDESIGN), BUILD. STAGES 1-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-angelus-b9-fx`, the nova's field spec out of both `fx.js` copies: §7; shell_identity 200/200): stage 1 is arm A to the fight; the wall is the lab's (probe 8/8 on the whole state: both fighters, the match with Twinshade's shades, every shot and the shared module tables, after the third review; seventeen mutants, each caught alone); built against the lab inside noise at both stages, the window clock measured and worth nothing here; no knob to move (the design names none); **the blade at the shipped rate, the design's own default: 9.5 (44.3% both sides against the shipped nova's 43.6% on the same fights)**. The 50% crossing, blade 10 (47.6%), is Rick's other choice (open decision 2), measured and gated beside it. engine_ab: the 37 others identical. verify 10/13, one red new and Lightkeeper's: it wins all 40 against Marrowdraw. The builder re-applies to the line's newer tips (`sc-tendril-fx`, `sc-coldiron-temper-fx` since Coldiron's carry, and `sc-ironhail-sunder-fx` / `sc-ironhail-fxout`, Ironhail's carry, committed in 0303511) with the same change set, and on `sc-tendril-fx` the probe and `engine_ab` pass too. **Stage 6, the picture and the voice, is built (`sc-lightkeeper-bulwark-b9.5-fx`, §5):** the wall drawn on the test's own line, rising out of the ward ring and folding back into it; a gong a block, a tink an arrow, a plate's ring rising at the cast and falling at the close; the nova's art out. `engine_ab` 4218/4218 with Lightkeeper in; the probe (v6) 10/10, its two new checks (the voice, the picture: 444 fights and 74 drawn) each failed by its own control; the clip is with Rick. The builder, stages 1-6, applies with the same change sets to every newer tip of the line, up to its tip of 08:04, `sc-angelus-b9-fx` (compose15, 0 FAIL). The nova's `fx.js` spec is the orchestrator's to take out at the carry. Claude Code has it.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 (`CLAIMS.md`, the BUILD row under the
redesign's). Input: `06-docs/v77/lightkeeper-bulwark-redesign-v77.md` and nothing else (rule 0).
Builder `tools/lightkeeper_build.py`, probe `tools/lightkeeper_probe.py`, runs in `runs/`.
**A REDESIGN, not a new relic:** Lightkeeper ships in the base; its nova (Bulwark) is replaced by the
design's wall, and the roster stays 38.

```
sc-tendril-t3.html                    the base: the chain tip (Bindweed stage 5)                 5a6216e3b629fad4
  -> sc-lightkeeper-stub.html          stage 1  the nova out, the wall's block in, stubbed (1e9)  e7d4efcc27e97d13
  -> sc-lightkeeper-wall.html          stage 2  the wall: arrows, the shove; charge 14 (arm B)    a22bc1f8cb4b2dfe
  -> sc-lightkeeper-bulwark.html       stage 3  the bank, 0 / 0 -> 3 / 3 (arm C)                  b0776ae2de382e67
  -> sc-lightkeeper-bulwark-b9.5.html  stage 5  the blade, 10.54 -> 9.5 (the shipped rate)        d60a5c63b785ad04
  -> sc-lightkeeper-bulwark-b9.5-fx.html  stage 6  the picture and the voice; the nova's art out   e3f16bf01f0e2995
```

**Built in scratch** (the batch runs its builds in parallel on one tip); the orchestrator carries the
links onto the chain in the handoff's order (Exsanguinate, then Bulwark) by rebuilding them with this
builder on the tip of the day and proving each carry with `engine_ab`. Every link above rebuilds
byte-identical from the bare tip with the final builder, a559dc47824545e9 (stage 6 added; `runs/rebuild_final.txt`,
`runs/stage6_builder_checks.txt`), and no name is on `02-chain/`. The third-round builder, 0cc27d7b775b6d2c,
built the first four; stage 6 added its rows and guards and changed none of them.

**The review, and what it changed.** An adversarial review of the first draft found one should-fix:
the draft set the blade at the 50% crossing (10) and called it the batch's standard, which is written
nowhere (not in `CLAUDE.md`, `CLAIMS.md` or the v87 handoff), while the design names its target twice
— §4, "the blade comes from 10.54 to about 9.5 ... the build settles it wide to the shipped rate", and
the §5 brief, "the blade, wide on 151 at 9 / 9.5 / 10 to the shipped rate" — and the handoff's row
says "~9.5". Rule 0 takes the design's own default and flags the other: **the final link is now
blade 9.5**, and blade 10 is Rick's other choice under open decision 2 ("shipped 48.5 or 50"). The
draft's `sc-lightkeeper-bulwark-b10.html` (97746e35cc3e500d) was deleted by hand; its runs are kept,
named `*_b10*`, as the measured record of that choice. The review's four notes are taken too: the
window's length is declared (§0), the literal reading of the shove's direction is put to Rick with
its size (§0, §6), the order in which the stage-5 points were read is said (§4), and `runs/commands.txt`
now names the files as they were copied.

**The second review, and what it changed.** A second adversarial review found one should-fix, in the
probe and not the build: its "nothing else" ([7]) and its cast check ([2]) compared only calls to
hurt / beat / rng, the hit stop, position and hp (and, at the cast, the foe's hp, shield and
velocity), so a wall that also stunned, pinned or hexed would pass. The reviewer's mutant `r5-stun` (a
block also stuns the foe 0.3s) took Lightkeeper from 43.9% to 76.1% and passed 8/8. The links were
clean: the review read the ticker and the cast line by line, and neither writes any of those fields.
**The probe now diffs the whole state** (§3): every field of both fighters and of the match, and
every field of every shot, before and after each wall frame, and after the cast from the end of the
engine's shared prologue. The only changes it allows are the ones another check rebuilds exactly.
(The third review found two things that diff still did not read, the contents of the match's arrays
and the shared module tables. The third-round probe reads both; see the next paragraph.)
[6] now rebuilds the ward exactly. The final link still passes 8/8, with every mechanism number what
it was, and `r5-stun` fails [7] alone. The mutants are now fifteen: the eight, `r5-stun`, a hex on a
block (`r6-hex`), a sunder at the cast (`r7-castsunder`, for the widened [2]), and the reviewer's
other four (`r1`-`r4`), each re-run under the stricter probe. Each changes fights, and each fails its
own check and only that one (§3).
The builder now refuses an insert that stuns, pins, burdens or lays any status but the ward. It also
declares, as part of reading 2, the review's note on Gloamwire: when the wall sticks the last arrow of
a Crossweave volley, the volley's release waits for the next `tickShots` (§0). The probe counts such
volleys: 80 in its 444 fights, all in the 12 against Gloamwire. §4 now cites the lab's own arm C
against Marrowdraw (1.0 / 1.0 on 151, 0.9 published), where it said "a reading". The builder's
comment says +0.6, as §4 does. None of this changes a link. All four rebuild byte-identical from the
second-round builder (28fedb3011a90e1a), so the rates, the ladder, `engine_ab`, `verify` and `tip_audit`
stand. The probe, the mutants, `chain_audit` and the composition test were re-run.

**The third review, and what it changed.** A third adversarial review found two should-fixes, again
in the probe and the doc, not the build. First, the "whole-state" diff compared the match's arrays
by length and element identity only, so the Fighters inside one (`this.shades`, Twinshade's shades,
which are `new Fighter(...)`) and the contents of the shots at the cast were unread; and it read none
of the shared module tables but `WEAPONS`. The reviewer's two mutants passed 8/8 while changing fights:
`v3-shade` (a block also shoves any shade inside R + 8, against reading 8; 60 of 60 fights against
Twinshade differ) and `v4-global` (a block writes `STATUS.ward.cap = 120`, which then holds for every
later match on the page; [6] missed it too, since it reads the live cap). Second, the doc claimed the
diff covered more than it did. **The probe (v5) now reads both** (§3): every match array by its length,
element identity AND content (the whole array's JSON), with a shade diffed field by field like a
fighter (`shades[i].<field>`); and `STATUS`, `CONFIG` and `AFFINITIES` before and after every wall
frame and every cast, with those three plus `WEAPONS` and `SHAPES` once a fight against their values
at the start of the run. Its JSON writes a fighter, a shade and the match as tags and a Map or a Set
with its entries. A value it cannot serialise fails [7]. What JSON still cannot tell apart inside a
record is said in §3. The final link is still 8/8 with every mechanism number what it was, and
`v3-shade` and `v4-global` each fail [7] alone. All seventeen mutants were re-run under v5, and each
fails its own check and only that one (§3). The builder took the review's note: it now refuses an
insert that writes `STATUS`, `CONFIG`, `AFFINITIES`, `WEAPONS` or `SHAPES`, by name or through a local
alias (`const W = STATUS.ward` then `W.cap = ...`), and `++`/`--` now count as writes in all its write
checks. Ten scratch variants of it refuse, and its clean copy writes the stage-2 link unchanged
(`runs/builder_negtest3.txt`). The composition test now takes each verdict from the chain's exit
status (`runs/compose7.sh`; the review's fourth note). **No link changes:** all four rebuild
byte-identical from the final builder, 0cc27d7b775b6d2c.

## 0. What this build stands on

- **The relic** is Lightkeeper as shipped: the vigil greatsword (reach 116, width 14, artW 40, dmg
  10.54, spin 3.4, swing, arc 1.5, mass 3.0; onSelf ward 1, knockMul 1.0) and its nova, Bulwark
  (charge 15, radius 260, dmg 12, knock 180). The builder asserts the profile and the nova block, by
  content, before it touches them. Names kept (design §5): LIGHTKEEPER / BULWARK; the card is the
  design's 71 characters, `A wall of light: arrows die on it, foes bounce off it, blocks bank ward`.
- **The shipped relic's rate on the base, the reference** (`relic_rate`, both sides, two blocks, 1480
  fights, `runs/ref_shipped_rr_*`): **43.6%** (side A 45.3, side B 42.0), mean 74.2s. This is "the
  shipped rate" the blade is settled to: the handoff reads every gate against the 151 run, never the
  published decimal (the design's 48.5 is the nova on Chromium 141).
- **The charge is 14.** The design names none: its lab priced every arm at the harness default, 16 on
  the lab's clock (`P` in `v77/runs/wall_base.json`, `wall_bank3.json`). Rick's batch ruling converts
  it. Measured for this fighter by a scratch copy of `ult_overlay.py` that counts, before each lab step,
  the frozen ones (`runs/wall_census.py`; 660 fights, block 2207, `runs/s0_census_2207`): on arm C
  14.5% of the lab's steps are frozen (15.9% inside windows, 13.5% outside), so the lab's 16 is the
  engine's 13.7, and 14 (arm B: 14.2%, 13.7). The shipped 15 was the nova's and goes with it.
- **The window is 8 seconds.** The design's prose says only "for a duration"; its lab priced every arm
  at `P.dur` 8, and the build takes the lab's number. It runs on the window tickers' clock, the batch's
  convention for every window ("weapons as designed": the number is the design's, the clock the
  engine's); §2 measures what that clock makes of it (about 9.6s of match time) and what that is worth
  (nothing measurable here). The design names no other length.
- **The lab is `overlays/wall.js` through `ult_overlay.py`**, with no `--cell` (a redesign): arm A is
  the relic with its ultimate suppressed, SHIP the nova live, B the wall, C the wall and the bank.
  **Flagged: the lab's own defaults are bankBall 10 / bankShot 5** (the 79.1% arm the design passed
  over), not the settled 3 / 3. Every lab arm here passes `--P bankBall=3 bankShot=3`, the brief's own
  stage-0 command.
- **Readings** (in the builder's docstring):
  1. **The facing is `theta`**, the greatsword's swinging blade angle (aim + sin(phase) x arc), which
     is what the lab read (`me.theta`) and what the picture says ("swinging with the aim").
  2. **Every live shot in the hall is an arrow to the wall**, whoever loosed it (the lab's loop), tested
     at `(s.r || 6) + 6`. **A net's arrow is made `stuck`** with tickShots' own endpoint write, so
     `tickNet` keeps its anchors (design §5's prose; the lab spliced every arrow); every other shot is
     spliced. A stuck arrow is inert and skipped. **The write is copied, the release is not.** In
     `tickShots` the endpoint write is followed in the same call by `this.releaseVolleys()`, which
     detonates a Crossweave volley once every arrow of it is stuck (`volleyDone`: Gloamwire's hurt, beat
     and hit stop, on Lightkeeper). When the wall sticks the *last* live arrow of a volley, that release
     waits for the next `tickShots`: one frame later, or after the whole freeze if a blow in `tickHits`
     starts a hit stop that frame. `tickNet` (which runs before `tickShots`) passes once over the fully
     stuck volley in between; its shove is zero, since the summed velocity of two stuck arrows is zero,
     but `strandSpent` and the net's counters are touched (presentation and tallies; nothing in the
     simulation reads them). Calling `releaseVolleys()` from the wall would put Gloamwire's hurt, beat
     and hit stop inside the wall's frame, which the design's "no damage, no beat, no hit stop" and the
     window clock both rule out, so the delay is the reading. The probe counts these volleys:
     80 in its 444 fights on the final link, all in the 12 against Gloamwire, the only relic whose
     arrows are nets (`runs/probe_b9.5_v4.txt`; second review round).
  3. **The shove is the lab's:** along the wall's normal, to the side of the wall the foe stands on (the
     sign of (foe - centre) . facing, 0 counting as ahead), so it cannot pass; `H.knock`'s arithmetic.
     The prose ("knocked 500 along the wall's normal away from the caster's side") can also be read
     literally, always outward; `wall.js` uses the same words and computes the side, and "cannot pass"
     (§1) supports it, so the build takes the lab's. **It touches many blocks:** 44% of the
     final link's blocks (5796 of 13272 in `runs/probe_b9.5`) are a foe behind the wall, which the literal reading would shove away from the
     caster instead of back to its own side, and that reading changes 216 of 222 fights but **not the rate, measurably:** 42.0% against
     44.3 at blade 9.5 and 50.3 against 47.6 at blade 10 (1480 fights each, both sides, two blocks;
     the standard error of a difference is about 1.8) (§6, Rick's).
  4. **A pinned foe is not blocked at all** (the lab's test): no shove, no bank, the cooldown not spent.
  5. **The cooldown runs through the whole window**, touching or not, from 0 at the cast (the lab's).
  6. **The bank is the vigil branch's three writes** (shield to the cap, shieldMax, `apply("ward", 1)`
     with no source), once per block, ball or arrow, even at the cap (it restarts the ward's clock).
  7. **The window closes on its clock or either death** (the lab's). No wither and no wait: the design
     names none, and a cast cannot come under a standing wall (8 < 14 on one clock).
  8. **The target is the opponent**, never a Twinshade shade (the lab's `foe`). The probe checks it:
     since the third review, every shade is diffed field by field around every wall frame (§3).
  9. **Nothing else:** no damage, no beat, no hit stop, no rng draw on a wall frame, and no stun, pin,
     burden or status but the bank's own ward; the sword swings as ever. (The cast keeps the engine's
     generic prelude, as every ultimate does: the banner, a 0.08s hit stop, the `ult` beat and voice,
     the `ultFx` record.) The builder refuses an insert that beats, stops, hurts, draws the rng, writes
     the shared weapon, or (second review round) stuns, pins, burdens or lays any status but the ward,
     or (third review round) writes a shared module table (`STATUS`, `CONFIG`, `AFFINITIES`,
     `WEAPONS`, `SHAPES`) by name or through an alias. The inserts read two of them (`STATUS.ward` as
     `W`, `CONFIG.physics.ballR`) and write none. The probe's [2] and [7] read the whole state (§3).
- **Design open decision 3 stays as designed:** the wall does not stop the foe's blade (a blade reaches
  through it). Rick's if he wants it otherwise.
- **Names:** the kind is `"lightwall"` (`"wall"` is a live SFX kind), the fields `ultWall` / `wallTally`,
  the ticker `tickLightwall`: none of them is in the base or in any in-progress builder
  (`twinshade_probe` keeps a local stats key `ultWall`, not an engine field).
- **The clock:** the window and the cooldown run on the window tickers' clock, which stops in a hit
  stop (the convention of every window in the batch). The lab ran both through freezes (§2).
- **What is retired.** The nova's three numbers leave Lightkeeper's row and its kind becomes
  `"lightwall"`. **The nova itself stays:** Censer's Consecration (and, on this base, Widowmaker's
  Exsanguinate) are `kind:"nova"` and the generic tail of `fireUlt` is theirs; the lightwall branch
  returns before it. **The nova's presentation keyed on the id stays through stage 5**, and stage 6
  retires it, as design §5 asks ("nova's field spec out, the wall's in"): ULTSIG `lightkeeper`
  (redrawn), the two `u.w === "lightkeeper"` draw branches (the plate ring, drawn at the 300 fallback
  radius for the cast's 1.5s on the links before stage 6), the `life` map's 1.5; and `fx.js` SPECS
  `lightkeeper` (the burst), which leaves both copies by the orchestrator's `fx_remove.py` at the carry
  (§5). Lightkeeper had no voice arm of its own, and its cast played the `ult` fallback (rune-crack)
  until stage 6 gave it one. Nothing in the simulation reads any of it.
- **Composition.** The first draft refused a base where Widowmaker is no longer a nova, and Widowmaker's
  own redesign (v106) takes it off the nova and carries first; the builder now reads who is still a
  nova and never refuses on it (it touches none of the nova's code). Re-tested with the second-round builder
  (28fedb3011a90e1a) against EVERY other in-progress batch builder on this chain as it stood at 12:47
  (Widowmaker, Coldiron, Ironhail, Lodestone, Oracle, Angelus; `runs/compose5.sh` -> `compose5.txt`,
  builder hashes in its header; Coldiron and Lodestone had moved since 12:00): this builder's four
  stages on each one's stages, each one's stages on this b9.5, this one in its place in a
  version-order stack of all seven, and this one on the other six stacked: **every one applies**.
  (Ironhail's and Oracle's own stage 5 do not write yet, by their builders' own state: Ironhail's
  holds its blade at stage 3, Oracle's stage 5 is unmeasured. Their stages 1-3 are in every stack.)
  **Re-run at 16:56 (`runs/compose6.sh` -> `compose6.txt`)**, after Widowmaker (dfad3817c8ac7754),
  Coldiron (1def68ac25637c8a, now with a stage 6) and Lodestone (7586e97be3d59344) had moved again:
  every one still applies, both ways and in both stacks. **The line's tip has also moved:** Bindweed's
  stage 6, `sc-tendril-fx.html` (eea0cde5536955b3, commit 2c9cb29), sits on `sc-tendril-t3`. This
  builder's four stages apply to it, and the change they make there is line for line the change they
  make on `sc-tendril-t3` (the sorted diff lines hash alike, 4d8cfccbf2ce5cbf). The carried b9.5 on
  that tip (383a547dfdfc4279, scratch) was run through the probe and through `engine_ab` against
  `sc-tendril-fx` with the 37 others. **The probe reads 8/8, and every line it prints is the line it
  prints on the b9.5 above** (43.9%, the whole state clean on the same 1,754,465 frames, 80 volleys held;
  `runs/probe_onfx_b9.5.txt`). **`engine_ab` passes, 3996/3996 identical** (`runs/engine_ab37_onfx.txt`).
  So the carry onto the line's new tip is already proved for this relic's own fights and for the others'.
  **Re-run at 18:08 with the third-round builder (`runs/compose7.sh` -> `compose7.txt`, `.err`)**,
  against the six as they stood then (Widowmaker a3b2d26d581735c7, Coldiron f194fa06f46454c9, Ironhail
  3c24bc2e4e59326b, Lodestone 0731db270893647b, Oracle 907a2237c3be0ff7, Angelus bb95f0eb4d9ff2c9).
  **0 FAIL.** Each verdict now comes from the chain's exit status: "ok" means the chain reached the last
  stage of its list, and a builder that stops short (Ironhail and Oracle at their stage 3, by their own
  state, as above) is "ok" only if it stops at the same stage on this b9.5 as on the base alone.
  compose6 printed "ok?" on every run, whatever the result (the review's fourth note). On
  `sc-tendril-fx` the b9.5 is again 383a547dfdfc4279, with the same change set (4d8cfccbf2ce5cbf), and
  the four links this builder writes on the base are the links (`cmp`). Under the third-round probe the
  carried b9.5 reads **8/8, every printed line (the mechanism, 43.9%, and the whole state clean on
  the same 1,754,465 frames, 11,790 with a shade, 1945 casts and 444 fights' tables) what the b9.5 on
  the base prints** (`runs/probe_onfx_b9.5_v5.txt`, `v5_vs_v4.txt`).
  **Re-run at 22:01 (`runs/compose8.sh` -> `compose8.txt`, `.err`; and `compose8b`)**, after Ironhail's
  builder moved (491643c55a34fa56, now with a stage 6 that goes on its stage 3) and Coldiron was carried
  onto `02-chain` (`sc-coldiron` ... `sc-coldiron-temper-fx`, 67cc3e6e05d5326e, on `sc-tendril-fx`):
  **0 FAIL.** The other five builders are unchanged since compose7. This builder's four stages apply to
  **the newest tip on `02-chain`, `sc-coldiron-temper-fx`**, and the change they make there is again
  line for line the change on `sc-tendril-t3` (4d8cfccbf2ce5cbf; the carried b9.5 there is scratch
  272ba770d9667639, not run). compose8 plays Ironhail's old list (1, 2, 3, 5), which stops at its stage 3
  by its own design ("THE BLADE HOLDS ... there is nothing to write"); `compose8b` plays its carry list,
  1, 2, 3 and 6, both ways with this builder's four stages: 0 FAIL, and this builder's b9.5 on the base
  is the link (`cmp`).
  **Re-run at 01:17 on 2026-09-28 (`runs/compose9.sh` -> `compose9.txt`, `.err`)**, after Oracle's builder
  moved (ce740d13ef9dfacf; its stage 5 still unmeasured, so it stops at its stage 3 by its own state, on
  the base alone as on this b9.5) and Ironhail began its carry onto `02-chain` (`sc-ironhail-stub` ...
  `sc-ironhail-sunder-fx`, b51c2539999dd272, uncommitted, on `sc-coldiron-temper-fx`): **0 FAIL**, with
  Ironhail played by its carry list (1, 2, 3, 6) in every pairing and both stacks. This builder's four
  stages apply to **the newest batch tip, `sc-ironhail-sunder-fx`**, and the change there is again line
  for line the change on `sc-tendril-t3` (4d8cfccbf2ce5cbf; the carried b9.5 there is scratch
  d9ea1546b4a9eedc, not run). The four links this builder writes on the base are the links (`cmp`).
  **Re-run at 01:49 (`runs/compose10.sh` -> `compose10.txt`, `.err`)**, after Oracle's builder moved again
  (00a0aa12c14314fd; its stage 5 now writes, so Oracle reaches its last stage on the base alone, on this
  b9.5 and in both stacks) and the batch line's tip moved to `sc-ironhail-fxout.html` (4b3775e5900172ea,
  01:28, uncommitted: Ironhail's carry with its retired `SPECS` entry taken out of both `fx.js` copies by
  `fx_remove.py`): **0 FAIL**, every other builder unchanged since compose9. This builder's four stages
  apply to `sc-ironhail-fxout`, with the same change set (4d8cfccbf2ce5cbf; the carried b9.5 there is
  scratch f2d72d2b1f7546a1, not run), and the four links it writes on the base are the links (`cmp`).
  **Re-run at 02:55 (`runs/compose11.sh` -> `compose11.txt`, `.err`)**, the last of stages 1-5,
  after Widowmaker (51c97e69a975ca92), Lodestone (c74cd4a4508bfcf5) and Angelus (e5b0d70b8555a916) had
  moved again, and after Ironhail's carry was committed (0303511, 02:13; `sc-ironhail-fxout.html`,
  4b3775e5900172ea, is the batch line's tip): **0 FAIL**, every pairing both ways and both stacks
  reaching every builder's last stage. This builder's four stages apply to `sc-tendril-fx`,
  `sc-coldiron-temper-fx`, `sc-ironhail-sunder-fx` and `sc-ironhail-fxout` with the same change set
  (4d8cfccbf2ce5cbf), and the four links it writes on the base are the links (`cmp`).
  **With stage 6 (`runs/compose12.sh` -> `compose12.txt`, `.err`; 23:35 on 2026-09-28)**, this builder's
  list is 1, 2, 3, 5 and 6, played against the eight other in-progress batch builders as they stood:
  Widowmaker bf8dff45e6870fa4, Coldiron f194fa06f46454c9, Ironhail 491643c55a34fa56 (its carry list 1, 2,
  3, 6), Lodestone c74cd4a4508bfcf5, Oracle c835ba672ae4bff7, Angelus 0e4e2fc3ff5813de, and the two
  started since compose11, Censer 78501578c5773570 and Aureole c95150a03738e777. **0 FAIL**, both ways and
  in both stacks, with the five links this builder writes on the base the links (`cmp`). Stage 6's
  change set on `sc-tendril-t3` (the b9.5 -> fx diff, its lines sorted) is 36aa852004da2d15, and the
  whole list writes the same two change sets (stages 1-5: 4d8cfccbf2ce5cbf; stage 6: 36aa852004da2d15) on
  every newer tip of the line: `sc-tendril-fx`, `sc-coldiron-temper-fx`, `sc-ironhail-sunder-fx`,
  `sc-ironhail-fxout`, and the two newest on `02-chain`, `sc-lodestone-b205-fx` (4568c2995d06f696,
  Lodestone's carry) and `sc-widowmaker-fxout` (04fdd2e2daa17c26, Exsanguinate's carry; both uncommitted
  when this ran). **Re-run on 2026-09-29 as `compose13` (03:10)**, after Oracle (ae5d6f4e641a2b16) and
  Angelus had each grown a stage 6 (their lists now end at it) and Aureole had moved (f28b8dcae7fa0883):
  0 FAIL. **And as `compose14` (03:20) with the final builder, a559dc47824545e9** (the stage-6 builder
  3b41d58c1df9dee4 with one comment corrected; nothing it writes changed): **0 FAIL**, 52 verdicts, every
  pairing both ways and both stacks reaching every builder's last stage, the same change sets on the
  same six tips. **And as `compose15` (08:07 on 2026-09-29), after the line moved again** (Lodestone
  61043aa, Widowmaker 254f9c4, Oracle 76c474a and Angelus 3f9b0d0 committed; the line's tip is now
  `sc-angelus-b9-fx`, 85b8af63055d1108, 42 relics), against every other batch builder as it stood: the
  six committed (Widowmaker bf8dff45e6870fa4, Coldiron f194fa06f46454c9, Ironhail 491643c55a34fa56,
  Lodestone c74cd4a4508bfcf5, Oracle ae5d6f4e641a2b16, Angelus 0e4e2fc3ff5813de) and the four in
  progress (Censer 78501578c5773570, Aureole c7641c026661b686, and the two started since compose14,
  Spellbreaker 463b49d265b3258c and Heartwood 04567e2ed899524a, stages 1-3 each: neither writes a stage 5
  as it stands). **0 FAIL**, 64 verdicts, both ways and both stacks, and the same two change sets on
  eight tips: the six above, `sc-oracle-fx` (15cf62f96f72653a) and `sc-angelus-b9-fx`
  (`runs/compose15.sh` -> `compose15.txt`, `.err`).
  The earlier runs, `compose.txt` / `compose_b.txt` / `compose3.txt` / `compose4.txt` / `compose5.txt` /
  `compose6.txt` / `compose7.txt` / `compose8.txt` / `compose9.txt` / `compose10.txt` / `compose11.txt` /
  `compose12.txt` / `compose13.txt` / `compose14.txt`, are kept for the record.

## 1. Stages 1-3

Stage 1 replaces the nova block in Lightkeeper's row with the wall's, stubbed at charge 1e9 (the old
cast unreachable, the new never reached), so the relic is arm A. Stage 2 adds `ultWall` / `wallTally`
after `vineTally`, the `kind === "lightwall"` cast branch before the tendril's (it opens `{t 0, dur 8,
cd 0}` and returns), `tickLightwall` after `tickTendril` (after `tickShots` has moved this frame's
arrows, before `tickHits`; the method itself sits before `tickWinnow`) and the charge 14, with the bank
written at 0 / 0 and inert. Stage 3 is the bank, 3 / 3. Every anchor is a stable line other builds keep.

`tickLightwall`, each window frame on the window clock: the wall is rebuilt from the ball and `theta`
(centre 50 ahead, half-length 110, perpendicular); every live shot within `r + 6` of it dies (a net's
stuck, the rest spliced) and banks 3; then, the cooldown clear and the foe unpinned and within `R + 8`
of it, the foe is shoved 500 along the normal to its own side, the cooldown is 0.4, and 3 is banked.

## 2. Stage 0 and the stages against it — the window clock, measured

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic lightkeeper --mech overlays/wall.js
--arms A,SHIP,B,C --P bankBall=3 bankShot=3 --seeds 20 --foes <33>`, seed0 2207 and 2317, 660 fights an
arm a block, Chromium 151.0.7922.34. The foes are the design's 33 (the 34-relic roster less the donor,
which here is the relic itself). The built links run `--arms SHIP` on the same foes and seeds.

```
                          published 141 (330)   lab on 151 (1 / 2)   BUILT (1 / 2)          pooled
A    no ultimate          38.8                  38.2 / 38.8          stage 1: 38.2 / 38.8   identical, fight for fight
SHIP the nova             48.5                  44.4 / 44.1          (the base)
B    the wall, no bank    38.8                  42.6 / 45.9          stage 2: 44.8 / 42.6   43.7 (lab 44.2)
C    + bank 3 / 3         60.6                  61.5 / 61.7          stage 3: 60.9 / 60.5   60.7 (lab 61.6)
```

The mechanism on the lab's own fights (the probe run on the lab's field: the 33 foes, side A, the lab's
seeds, which are the fights the SHIP arm plays; `runs/probe_labfield_*`):

```
                         casts   blocks / cast   arrows / cast   banked / cast   shield (a fight's window frames)   blows in / out
lab B (both blocks)      4.23    6.58            1.40            -               11.1                               11.1 / 13.2
built stage 2            4.11    6.65            1.56            -               10.5                               12.8 / 11.7
lab C                    4.43    6.73            1.40            23.7            18.6                               11.7 / 13.8
built stage 3            4.31    6.83            1.54            24.1            18.5                               13.5 / 12.3
```

On those fights the probe's Lightkeeper wins exactly what the SHIP arm reads (44.8 / 42.6 and 60.9 /
60.5), and 8/8 (`runs/probe_labfield_*`). The charge conversion holds (4.31 casts against the lab's
4.43; the lab's cadence is fixed at 16 lab-seconds, the engine's is 14 and restarts at each cast). The
blocks and the bank are the lab's to within 2%; the built window catches 10% more arrows (arrows fly in
unfrozen time, and the built window holds 8 unfrozen seconds, the lab's ~6.7) and holds more of the
sword's blows (13.5 against 11.7). The designed gates hold: "~6.8 blocks and ~1.4 arrows a cast", "~24
ward a cast".

**Published against 151.** On the design's own seeds (330 fights) on `sc-trunk`, 151 reads A 36.7, SHIP
43.9, B 38.5 (`runs/repro_trunk_wall_base`): the nova lost ~4.6 points to the runtime. On this base
**the design's control does not hold: the wall alone is worth +5.8 over A in the lab itself** (44.2
against 38.5; +1.8 on sc-trunk at 151, 0.0 published). The built wall reads the same (43.7), so the
build is not what moved it; the brief's stage-1 gate "relic ~39%" is a 141 number. Flagged for Rick.
Its stage-2 gate, "relic ~61% at 10.54", holds (60.7).

**The gap, attributed.** Stage 2 reads 0.5 under arm B and stage 3 0.9 under arm C; a pooled rate of
1320 fights has a standard error of about 1.3, so both are inside it. Two controls bracket it
(`runs/lab957_*`, `runs/ctl_labclock_*`):

```
                                                           wall (B)             bulwark (C)
the lab                                                    42.6 / 45.9  44.2    61.5 / 61.7  61.6
the build (the window clock)                               44.8 / 42.6  43.7    60.9 / 60.5  60.7
the lab at the engine's window (dur 9.57)                  40.8 / 42.7  41.7    62.6 / 61.2  61.9
the build on the lab's clock (ticked through freezes)      42.4 / 42.3  42.4    59.4 / 59.1  59.2
```

The engine's 8s are 8 seconds of the window clock; 16.4% of window steps are frozen (the probe), so a
window is ~9.6s of match time where the lab's was 8 step-seconds. **Here that is worth nothing
measurable**: every row is within 2.7 points of the others (the standard error of a difference between
two 1320-fight rates is about 1.9), where the same
clock was worth -5 on Canopy (v99 §4), +4.3 on Onslaught (v100 §2) and +11 on Tendril (v101 §2). The
mechanism says why: the wall pays per block, and the blocks come on a 0.4s cooldown that runs on the
same clock as the window, so the longer match-time window holds about the same count; and even the lab
given 9.57s (8.0 blocks and 27.9 banked a cast) reads 61.9. Nothing is mis-built, and the engine's
convention and every designed number are kept.

## 3. The probe (`lightkeeper_probe.py`, one check per sentence, read inside the hooks)

It wraps `step`, `fireUlt`, `resolveHit` and `tickLightwall`, plays Lightkeeper against every other
relic from both sides (444 fights; `--foes/--sides/--seedstep` give the lab's field), and REBUILDS the
wall on every window frame from the frame's own `theta`, position and shots, with the engine's segment
distance, then compares what the ticker did:

- [1] **"for a duration"**: the window is `dur` on the window clock and closes on either death; no cast
  under a standing wall; only Lightkeeper carries `ultWall`; **the ticker runs exactly once on every
  live step and never on a frozen one** (the window clock itself, read from the step).
- [2] **"the nova is out"**: a cast opens exactly `{t 0, dur, cd 0}` and **writes nothing else**. The
  probe reads it inside the cast: the engine's shared prologue (ultsFired, the banner, the note, the
  shake, the cast's 0.08s hit stop, the `ult` beat, the `ultFx` record) is every relic's, so the
  snapshot is taken when the prologue assigns `ultFx`, its last statement before the kind branches
  (an accessor on the match for the length of the call, put back as the plain field it was). After the
  cast every field of both fighters and of the match (as [7] reads them: the arrays' contents, the
  shades and the shots included) and the shared tables `STATUS`, `CONFIG` and `AFFINITIES` must be as
  they were then, except the caster's `ultWall` and a `wallTally` whose `casts` went up by one.
- [3] **"arrows die on it"**: every live shot inside `(r || 6) + 6` of the rebuilt wall dies (a net's
  with exactly the endpoint write, the rest spliced), none outside it; every field of every other
  shot, stuck or live, unchanged.
- [4] **"an enemy that runs into it"**: a block exactly when the foe is inside `R + 8`, unpinned, the
  cooldown clear; never two closer than 0.4s; the cooldown 0.4 after one.
- [5] **"bounces off and cannot pass"**: exactly 500 along the normal to the foe's side; no other
  velocity change on a wall frame.
- [6] **"the shield grows"**: min(cap, shield + 3) an arrow, then + 3 a block, shieldMax, and the ward
  exactly as `apply("ward", 1)` leaves it once a bank (stacks to the cap, `t` the ward's 5s, `src`
  untouched), rebuilt from the engine's lines; the ward unmoved on a frame with no bank; nothing at
  bank 0; nothing on the foe.
- [7] **nothing else**: no hurt, beat, rng draw or hit stop on a wall frame, and **a whole-state diff**
  (second review round, completed in the third) before and after the ticker:
  - **both fighters**, every own field: stun, stunDR, pin, pinV, pinMax, burden, the `status` table key
    by key with its stacks, `t` and `src`, the foe's shield and shieldMax, position, hp, and the rest.
    Primitives are compared by value; objects by their JSON.
  - **the match**, every own field: primitives by value, records by their JSON, and **every array by
    its length, its element identities and its content** (the whole array's JSON). A Fighter inside an
    array, i.e. a Twinshade shade, is also diffed field by field like a fighter (`shades[i].<field>`).
    On a wall frame the shots are left to [3], which reads every field of every one; at the cast they
    are in the diff.
  - **the shared module tables** `STATUS`, `CONFIG` and `AFFINITIES`, around every wall frame (and every
    cast, [2]); and once a fight, those three plus `WEAPONS` and `SHAPES`, against their values when the
    run began. So a write to a table is caught on its frame, and a table left changed is caught in
    every later fight.

  The only changes allowed are the ones another check rebuilds exactly: the caster's `ultWall` /
  `wallTally` ([1] [3] [4] [6]), shield, shieldMax and ward ([6]), the foe's vx / vy ([5]), and the
  dying arrows ([3]). [6] rebuilds the cap from the live `STATUS.ward`, the engine's own; [7] is what
  holds that table to its start.

  **What the diff can and cannot see.** The JSON is the browser's own (the engine never serialises
  anything). For the run only, and removed after it, a fighter, a shade and the match are written as
  tags (no cycle, no deep copy), and a Map or a Set is written with its entries (plain JSON writes `{}`).
  A value the probe cannot serialise fails [7]: a field it cannot read is not a pass. Two things JSON
  still cannot tell apart **inside a record**: NaN, Infinity and null (all written null), and one
  function for another. A fighter's own top-level fields are compared by value, so there both are
  seen. And a property set on a Map or a Set itself, not as an entry, is not written, so not seen
  (found at stage 6, §5d). The shared tables in the diff are the five the engine exports on `AC`. Its other top-level
  `const`s (caches such as `ART_BOX` and the like) are not in it. The builder's static refusal covers
  the same five by name.
- [8] **"the sword swings as ever"**: every Lightkeeper blow rebuilt exactly from its captured jitter
  and crit draws, in the window and out.

Results under the third-round probe, v5 (every relic, both sides, 6 seeds; `runs/probe_*_v5`). The
header and the three mechanism lines of every v5 run are character for character what the second-round
probe (v4) printed on the same link (`runs/v5_vs_v4.py` -> `v5_vs_v4.txt`), and v4's were the first
form's (`runs/probe_wall.txt`, `probe_bulwark.txt`, `probe_b9.5.txt`), so neither widening of the diff
moved a number. Outside [2] and [7] the only change from v4 to v5 is the JSON writer that [3] and [6]
also use (native, with the tags, in place of a replacer); the counts of [1], [3], [4], [5], [6] and [8]
are the same in every v5 run as in its v4 run, mutants included (the table below).
- **sc-lightkeeper-wall (stage 2): 8/8.** 4.11 casts; 6.67 blocks and 1.29 arrows a cast; shield 10.3 on
  a window frame; 12.6 blows in windows and 11.6 outside; 264 net arrows stuck, 2096 spliced; 16.0% of
  window steps frozen. The whole state is clean on 1,651,734 wall frames (11,679 of them with a
  Twinshade shade in the hall) and 1826 casts, and the five shared tables after every one of the 444
  fights; 81 volleys held.
- **sc-lightkeeper-bulwark (stage 3): 8/8.** 4.36 casts; 6.74 blocks, 1.29 arrows and 23.2 banked a
  cast; shield 18.1 on a window frame; 13.3 / 12.4 blows; 267 net arrows stuck, 2225 spliced; 16.4%
  frozen; Lightkeeper 57.0% at the shipped 10.54. The whole state is clean on 1,749,636 wall frames
  (12,409 with a shade in the hall) and 1937 casts, and the five shared tables after every one of the
  444 fights; 83 volleys held (`runs/probe_bulwark_v5.txt`; the same numbers as v4).
- **sc-lightkeeper-bulwark-b9.5 (stage 5, the final link): 8/8** (`runs/probe_b9.5_v5`). 4.38 casts; 6.82
  blocks, 1.24 arrows and 23.5 banked a cast; shield 16.7 on a window frame; 13.6 / 12.6 blows; blocks
  ahead of the wall 7476, behind it 5796; 7376 pinned contacts passed over; 255 net arrows stuck, 2158
  spliced; closes 1699 on the clock, 43 on a death (the rest end with the fight); 16.5% frozen (a
  window ~9.58s of match time). Lightkeeper wins 43.9% of the 444. **The whole state is clean on
  1,754,465 wall frames (11,790 with a shade in the hall) and 1945 casts, and the five shared tables
  are unwritten after every one of the 444 fights.** 80 Crossweave volleys are left fully stuck for
  the next `tickShots` (reading 2). (The first draft's b10 link: 8/8 under the first form,
  `runs/probe_b10`.)
- **On the lab's field** (the 33 foes, side A, the lab's seeds, both blocks; `runs/probe_labfield_*_v4`,
  under v4 and not re-run under v5: they are the like-for-like mechanism column of §2, and v5 moves no
  mechanism number on any link it has read): all four runs are 8/8, with the whole state clean (wall:
  2,454,343 and 2,443,696 frames; bulwark: 2,570,732 and 2,575,996). Their mechanism lines and win
  rates are the first form's to the character, and they are the SHIP arm's rates (44.8 / 42.6 and
  60.9 / 60.5; §2).
- **Controls: seventeen scratch mutants of the final link** (`runs/mutants.py`, `runs/ctl_variant.py` for
  m2, hashes in `runs/mutants_hashes.txt`; `runs/probe_mut_<m>_v5.txt`, `runs/fightdiff_mut_*`; the table
  is `runs/mutant_table.py` -> `mutant_table.txt`, the second round's `mutant_table_v4.txt`). Each
  changes fights (fightdiff: Lightkeeper against every relic, both sides, 3 seeds, 222 fights), and
  under the third-round probe (v5) each fails its own check and only that one. `r5-stun` is the second
  reviewer's mutant (the same code; the reviewer's copy carries a comment), `r1`-`r4` are that
  reviewer's other four, and `v3-shade` and `v4-global` are the third reviewer's two, replacement for
  replacement (`cmp` identical to theirs):

```
mutant         what it breaks                                       fails            probe win  fights changed  Lightkeeper wins
m1-window      the window 10% long on the window clock              [1] 166234 only  44.8%      213/222         105 -> 106
m2-clock       the ticker also on frozen steps (the lab's clock)    [1] 636877 only  43.5%      216/222         105 -> 103
m3-arrows      the arrow kill zone 4 wider                          [3] 1509 only    43.7%      41/222          105 -> 110
m4-cd          the cooldown 10% short after a block                 [4] 16818 only   46.6%      215/222         105 -> 96
m5-shove       the shove 10% strong                                 [5] 13514 only   43.7%      216/222         105 -> 101
m6-bank        a ball block banks 4                                 [6] 13285 only   48.0%      216/222         105 -> 122
m7-stop        a block stops the world 0.05s                        [7] 26056 only   48.9%      216/222         105 -> 108
m8-side        the shove always outward (the prose read literally)  [5] 5707 only    42.3%      216/222         105 -> 100
r1-netsplice   a net arrow spliced, not stuck (reviewer)            [3] 297 only     43.9%      6/222           105 -> 105
r2-pinned      a pinned foe blocked too (reviewer)                  [4] 312 only     44.1%      6/222           105 -> 105
r3-castcd      the cast opens with the cooldown running (reviewer)  [2] 1976 only    44.8%      204/222         105 -> 106
r4-noward      an arrow's bank skips the ward (reviewer)            [6] 2241 only    44.1%      9/222           105 -> 103
r5-stun        a block also stuns the foe 0.3s (reviewer)           [7] 14787 only   76.1%      216/222         105 -> 174
r6-hex         a block also lays a Hex on the foe                   [7] 15137 only   79.5%      216/222         105 -> 174
r7-castsunder  the cast also lays two Sunder on the foe             [2] 1955 only    52.7%      221/222         105 -> 119
v3-shade       a block also shoves a Twinshade shade (reviewer)     [7] 1726 only    44.6%      6/222           105 -> 103
v4-global      a block writes STATUS.ward.cap = 120 (reviewer)      [7] 445 only     44.4%      31/222          105 -> 108
```

  The final link is 8/8 on the same 444 fights, at 43.9% (`runs/probe_b9.5_v5.txt`). "fails" counts
  failed reads, not fights. The fifteen rows above the last two are, count for count, the second
  round's (`mutant_table_v4.txt`): v5 reads every check and every mechanism line of every one of them
  exactly as v4 did (`runs/v5_vs_v4_mut.py` -> `v5_vs_v4_mut.txt`, fifteen lines SAME), so the wider
  diff found nothing new in them and lost nothing. `v3-shade` fails [7] on 1726 wall frames, each
  "the wall also moved the match's shades[1].vx, shades[1].vy"; it can change only the fights against
  Twinshade (only Twinshade's split pushes a shade into `m.shades`), and it changes 6, fightdiff's 6
  against Twinshade (the reviewer's 60 of 60 was 20 seeds). `v4-global` fails [7]
  445 times: once on the first wall frame that writes the cap ("the wall also moved the shared table
  STATUS") and once in each of the 444 fights, whose once-a-fight check finds `STATUS` changed from
  the run's start, so the leak into every later fight on the page is seen in every one of them.
  m7-stop's count is twice the first form's (13028): its hit stop is now also seen as the match's
  `hitStop` field in the whole-state diff, still inside [7]. r1, r2 and r4 change few
  fights (6, 6 and 9 of 222) because what they break seldom decides one: a Crossweave net (only
  Gloamwire's arrows are nets), a pinned foe at the wall with the cooldown clear, and the ward's clock
  after an arrow's bank (the shield itself is still banked). Each still changes fights, and each fails
  its own check alone (297 to 2241 failed reads).
  The eight m-mutants failed their own check alone under the first form as well (`runs/probe_mut_<m>.txt`).
  r5-stun passed the first form 8/8 (the reviewer's run). r6-hex and r7-castsunder write only fields
  that the first form never read (a status table), so they were not run under it. v3-shade and
  v4-global passed the second-round probe (v4) 8/8 (the reviewer's runs), which is the third review's
  first finding. (The first draft's seven mutants of
  b10 did the same under the first form: `runs/probe_mut_*_b10.txt`, `fightdiff_mut_*_b10.txt`.)
- **Stage 1 is arm A fight for fight** on both blocks: every foe's rate and every blow count identical
  (`runs/cmp_arms.py` on `built_stub_*` against `s0_ASBC_*` arm A).
- **v6, for stage 6** (`lightkeeper_probe.py` e1e09479216f72d6; §5d). It adds [9], the voice, and [10],
  the picture, and the link switches each one on; it reads `SHAPES` key by key. **On the b9.5, which has
  neither, v6 reads 8/8, and every line it prints is the line v5 printed** (`runs/probe_b9.5_v6.txt`
  against `probe_b9.5_v5.txt`, character for character but the timing), so v6 moved nothing v5 read.

## 4. Stage 5: the blade — 9.5, the shipped rate

Both sides (`relic_rate.py`: each seed from both sides; every other relic a foe, 10 seeds a foe a side,
740 fights a block; seed0 2207 and 2317; `runs/stage5_rr_*`, `runs/stage5_table.txt`):

```
                                     blade   block 1   block 2   pooled (1480)   side A   side B   mean s
the shipped nova (the base)          10.54   43.8      43.5      43.6            45.3     42.0     74.2
Bulwark (stage 3, --set dmg)         9       37.7      39.2      38.4            38.2     38.6     81.2
Bulwark (stage 3, --set dmg)         9.5     43.6      44.9      44.3            44.5     44.1     80.9
Bulwark (stage 3, --set dmg)         10      47.3      47.8      47.6            46.9     48.2     80.6
Bulwark (stage 3, --set dmg)         10.25   54.6      56.5      55.5            55.1     55.9     80.3
Bulwark (stage 3, --set dmg)         10.5    52.8      54.1      53.4            54.2     52.7     79.6
Bulwark (stage 3 as built)           10.54   55.9      56.4      56.1            56.8     55.5     79.7
sc-lightkeeper-bulwark-b9.5, no set  9.5     43.6      44.9      44.3            44.5     44.1     80.9
```

- **The knob: none moved.** The design gives the build no knob to move before the blade (the bank's 3
  is its own choice, priced in the design's §4, not a lever it hands the build).
- **The target is the shipped rate, the design's own** (§4: "the build settles it wide to the shipped
  rate"; §5: "the blade, wide on 151 at 9 / 9.5 / 10 to the shipped rate"; the handoff's row: "~9.5").
  The shipped rate on 151 is the nova's **43.6%** on these same fights. **Blade 9.5 is the measured
  point nearest it: 44.3% (+0.6 on the unrounded rates, 44.26 against 43.65)**, side A and side B
  within 0.4 of each other. The line through the six points puts the shipped rate at 9.47 (through the
  brief's three alone, at 9.52); 9 reads 5.2 under and 10 3.9 over. Open decision 2 ("shipped 48.5 or 50") leaves the other target to Rick; the design's 48.5
  is the nova on 141, and on 151 the nova reads 43.6.
- **Rick's other choice, 50%, is one number away: blade 10, 47.6%**, the measured point nearest 50%
  inside the brief's band (the six-point line crosses 50% at 10.03, 11.2 points a unit of blade; the
  brief's three alone, at 10.22). The first draft built it (`sc-lightkeeper-bulwark-b10`, 97746e35cc3e500d,
  deleted) and gated it: `relic_rate` with no set reproduced 47.3 / 47.8 exactly, probe 8/8, engine_ab
  3996/3996 identical, verify 10/13 with Lightkeeper at 51.8% (`runs/*_b10*`, `engine_ab37_b10.txt`).
  To take it: `BLADE = 10` in the builder and rebuild stage 5.
- **The order the points were read in, and their noise.** The brief's three (9, 9.5, 10) were read
  first; 10.25, 10.5 and 10.54 (stage 3 as built) were added after, outside the brief's band, to place
  the 50% crossing that the first draft was aiming at. Nothing was bisected. The table is not
  monotonic: 10.25 reads 55.5, 3.1 above the six-point line (2.4 standard errors of a 1480-fight
  point, 1.3), and the step from 10 to 10.25 is +7.9 against the line's +2.8; 10.5 then reads 2.1
  under 10.25. That is noise at 1480 fights a point, and it does not touch the choice: 9.5 is a
  measured point inside the band, and the three points of the band are the line's (residuals -0.4,
  +0.8, -0.4 on their own fit).
- **The built link is the measured relic:** `relic_rate` on `sc-lightkeeper-bulwark-b9.5` with no knob
  set reproduces the `--set dmg=9.5` runs exactly on both blocks (43.65 / 44.86%, side A and side B,
  every foe, every type, the mean duration to the digit; `runs/cmp_rr_b9.5.txt`).
- **The wall lengthens Lightkeeper's fights**: 80.9s mean against the nova's 74.2.

**The ladder at 9.5** (40 fights a foe, `runs/ladder_b9.5.txt`), beside the shipped nova on the same
fights: by type bow 80% (shipped 62), scythe 50 (48), twinblade 48 (54), greatsword 36 (43), flail 30
(28), warhammer 24 (30). Worst **Heartwood 0 of 40** (shipped 10%), Ironwood 2.5 (27.5), Axiom 12.5,
Spellbreaker 15; best Marrowdraw 100, Lastlight 95, Gloamwire 85, Aureole 82.5. The largest gains:
Lastlight +42.5, Thornshear +40, Redflail +30, Thornwake and Vinesower +27.5; the largest losses:
Ironwood -25, Spellbreaker and Twinshade -22.5, Foregone -20, Duskreave -17.5. The wall is a bow-killer
and a heavy-hitter's wall to climb: **the bows at 80% are item 12/32 (the type spread), Rick's**, and
Marrowdraw at 100% is verify's new red (below).
(At 10: `runs/ladder_b10.txt`, bows 80, warhammer 31, Heartwood 15.)

- **engine_ab sc-tendril-t3 -> sc-lightkeeper-bulwark-b9.5, the 37 others (all but Lightkeeper), n=6:
  3996/3996 identical** (`runs/engine_ab37_b9.5.txt`). The redesign moves no other relic's fight.
- **verify --n 40 on sc-lightkeeper-bulwark-b9.5 (38 relics, 28120 matches): 10/13**, the base's count
  (`runs/verify_b9.5.txt`; the base's is v101's `verify_t3`). **Lightkeeper 45.5%** (41.3 on the base,
  51.8 at the first draft's b10); every relic inside 30-70% (Heartwood 30.5 .. Gloamwire 63.2); no JS
  error, no timeout. The reds, and whose:
  1. **"both sides can win every matchup": Lightkeeper vs Marrowdraw 40/0 — NEW, and Lightkeeper's.**
     **The design's own lab measures it:** arm C (the wall and the bank 3 / 3, blade 10.54, side A)
     wins 1.0 / 1.0 against Marrowdraw on 151 on both blocks (`runs/s0_ASBC_2207.json`,
     `s0_ASBC_2317.json`, byFoe), and 0.9 in the published run (`v77/runs/wall_bank3.json`); even the
     lab's arm A, no ultimate at all, reads 0.95 / 0.95, and the nova 0.9 / 0.9. The build reproduces
     it (stage 3 on the lab's fights, `built_bulwark_*`: 1.0 / 0.95). relic_rate reads 100% for
     Lightkeeper against it at 9.5 (40 of 40 both sides, two blocks; 97.5 at 10; the shipped nova
     82.5), the far end of the bow line below. Rick's (§6); nothing in the build can move it without
     designing. The same check's
     other two, **Heartwood vs Twinshade 0/40 and Heartwood vs Bindweed 0/40, are the base's**, and
     engine_ab shows those fights identical.
  2. **"every pairing mean duration in 18-70s"**: red on every link since the minute pace. The longest
     pairing is now **Lightkeeper/Farwarden, 117.4s** (the base's longest, Farwarden/Starwarden, 100.0s;
     at b10, 113.6s): the wall lengthens Lightkeeper's fights (80.9s mean against the nova's 74.2).
  3. **"overall mean duration in 28-54s"**: 61.2s (the base 60.8), the same band, red on every link.
- **tip_audit:** identical to the base's, line for line (`runs/tip_audit_b9.5.txt`, `tip_audit_base.txt`).
- **chain_audit** (`--relic` and `--tip` the final link, `--builder lightkeeper_build.py`): all 8 inserts
  survive, the last "S5: the blade: the shipped rate" (`runs/chain_audit_b9.5.txt`; re-run with the
  second-round builder 28fedb3011a90e1a, the same 8/8: `runs/chain_audit_b9.5_v2.txt`; and with the
  final, third-round builder 0cc27d7b775b6d2c, the same 8/8: `runs/chain_audit_b9.5_v3.txt`).
- **What the second and third review rounds could move, and did not.** The builder's changes are a
  docstring, a comment and self-checks; its inserts are unchanged, and all four links rebuild
  byte-identical (`runs/rebuild_final.txt`). So `relic_rate`, the ladder, `engine_ab`, `verify` and
  `tip_audit` above are the final link's own, not re-run. The probe, the mutants, `chain_audit` and the
  composition test were re-run in each round.

## 5. Stage 6: the picture and the voice — `sc-lightkeeper-bulwark-b9.5-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel (the picture
lab's scratch, `lk_rows.py`, and `tools/lightkeeper_voice_lab.py`), and built as `lightkeeper_build.py
--stage 6` on the final link (stage 5's b9.5): **thirteen anchored edits (voice 4, picture 9)**,
byte-exact to the labs' own row files (voice `rows_final.json` 814d0a16d8911102, picture f9b7579caa065664;
copied as `runs/stage6_voice_rows.json` and `stage6_picture_rows.json`). No two rows share an anchor, so
none is merged; no row's anchor sits inside another's; nine re-emit their anchor and four replace it (the
nova's two art branches, the charge rune, the life entry). Voice-then-picture and picture-then-voice write
the same bytes (e3f16bf01f0e2995). **The picture rows alone reproduce the picture lab's stamp
(728d64f8397290a1), and the voice rows alone the voice lab's (a8629a7fe94d50b9)**, both re-checked from
the builder as it stands (`runs/stage6_rows_recheck.txt`; the generator, `runs/stage6_gen_s6.py`, is
the pattern's: rows == files, the stamps, no nested anchor, merge by anchor, a `--stage 6` that refuses
to run twice). The picture sheet is `05-reference/v107/lightkeeper-picture-sheet.png` (4b4d17f751ca5597);
the wavs are `05-reference/v107/lightkeeper-*.wav` (gitignored). The two labs' full reports are
`runs/stage6_picture_report.json` and `runs/stage6_voice_report.json`.

**Built in scratch** on the b9.5 (38 relics) while other builds ran on the same tip; the orchestrator
carries it with the other four links. **It re-applies on a tip that carries other relics' stage 6:** the
Sfx row re-emits the shared rune-crack fallback unchanged (so another relic's arms anchored there apply
in either order); the three voice rows anchor on `tickLightwall`'s own lines; the picture's fields follow
this build's own stage-2 fields; its two calls and two method blocks sit beside shared lines
(`tickPresentation`'s first call, `drawTreeTop`, `tickWinnow`, `drawStatus`) and re-emit them unchanged;
the three retired art blocks are Lightkeeper's own; and the life-map row's anchor is the whole line
`ironhail: 1.3, lightkeeper: 1.5, farwarden: 2.6,`, which no other rows file touches. compose12 to
compose15 (§0) prove it on every other batch builder and on every newer tip of the line, up to its tip
of 08:04 on 2026-09-29, `sc-angelus-b9-fx`.

### 5a. The picture

v77 §5. Every number here is the picture lab's: headless Chromium 151 at 1080x1920 with the post chain
on, and Electron 44 on the RTX 3070 for the frame cost.

- **The wall is drawn on the line the test uses.** `drawBulwark` rebuilds it at draw time exactly as
  `tickLightwall` builds it (the centre 50 ahead along `theta`, 110 either way across the facing), so
  the bar is where the test is, and it swings with the blade because `theta` does (reading 1). The bar is
  6 wide in vigil pink with a 2-wide pale heart, under a soft halo 14 units a side drawn as three stacked
  strokes (no `shadowBlur`, no bloom).
- **The rise and the fold, 0.25s each.** The bar grows out of the ward ring's front arc (`_stWard`'s
  radius, R + 17, one plate wide round the facing) into the straight bar, smoothstepped, and the ring's
  front lights at alpha 0.4 at once. With no ward up it still rises from R + 17. The fold is the rise
  mirrored. It keys on `ultWall` going null, on the caster's death, or on the match's end, so a fight
  that ends with the wall up folds it in the verdict (0.24s after the kill). A contact while the bar is
  still rising snaps it up (Canopy's sprout rule): the wall is live from the cast's first frame.
- **A block** flashes the bar and its heart white for two frames (0.033s, source-over).
- **An arrow** leaves a 0.3s char mark where it died on the bar (`_stWard`'s own edge colour, #1A0512),
  riding the bar as it swings, with a white strike ring thrown off the spot for its first 0.12s. A
  stopped arrow is spliced before the picture can see it, so the picture keeps, as plain numbers, where
  each live shot will be after its next move (`tickShots`' own arithmetic) and scorches the ones nearest
  the wall; an arrow loosed and stopped inside one step scorches where the foe's bow tip meets the bar.
  Against where the arrow truly died, along the bar: median 0 units, max 4.0 on bows, 17.1 on one
  Ironhail bolt (the lab; the probe's own reading is in §5e).
- **The bank shows on the caster:** the vigil branch's own "+N" float (its colour, size and seat), a
  block's and an arrow's alike, of the amount really banked, so a shield at its cap floats nothing. Once
  a window, the WARD tag; the first in a match carries its one line (the vigil branch's own teaching).
  The once-a-window tag is the lab's addition (reading 18).
- **Motes:** ten motes shed off both faces of the bar for the whole window, placed along it by
  `shellHash` (no RNG), drifting off its face. This is the design's "field", drawn (below).
- **Every ball's disc is cut out of it** at 0.98 R (both fighters and Twinshade's shades; CLAUDE.md
  4.1b), so a foe pressed against the wall stands in front of the light. It draws in the world pass
  over both fighters: in front of the sword, and over the ward ring it rises out of.
- **The nova's art is retired:** `drawUltUnder`'s plate ring and `drawUltOver`'s eighteen plates (both
  on the ultFx slot at every cast), the life map's `lightkeeper: 1.5` (the slot falls to the map's own
  default, also 1.5, so nothing it does changes), and the charge rune, `ULTSIG.lightkeeper`, redrawn as
  five ward plates with a bar standing up out of their front as the charge fills and an arrow stopped
  against it.
- **The silhouette is left as it is:** the resting vigil greatsword reads |dL| 0.199 at the app's size,
  4th of the 7 greatswords (Dawnbringer 0.317, Axiom 0.300, Heartwood 0.215 above; Oathwound 0.179,
  Nightfell 0.161, Emberedge 0.107 below).
- **The art hangs off the Fighter** (`bulwarkFade`, `Age`, `Out`, `Flash`, `Seen`, `Shots`, `Scorch`,
  `Tagged`), never off `m.ultFx` (open item 25). `tickBulwark`, in `tickPresentation`, finds each block
  and arrow by watching `wallTally` rise, so neither `tickLightwall` nor the cast makes a call for the
  picture.
- **Bloom** (9 fights, 91 frames): the picture's share of the arena-mean lift max +0.0000 (gate +0.02);
  raw luma it adds at most +0.0040. The caster's disc moves -0.0002..+0.0002 (art only); live foes by
  affinity 0.0000 (sanctified, dwarven, bloodsworn), +0.0003 (runic), +0.0022 (umbral), +0.0029 (vigil).
  **Controls:** the bar as a 60-wide unclipped white light puts the foe's disc past 0.90 on 7/80 window
  frames and FAILS; a 200-unit wash lifts past 0.02 on 23/91 frames (max +0.093) and FAILS.
- **Legibility** (median |dL| of each component's own pixels, out of a hit stop / in one): the bar
  standing 0.146 / 0.141, its body 0.305 / 0.303, the halo 0.068 / 0.068, the motes 0.214 / 0.196, a
  block's flash 0.295, an arrow's strike 0.387 and its char 0.211, "+3" and WARD 0.219 / 0.229, the rise
  0.139, the cast frame inside its 0.08s stop 0.086, the close 0.140 / 0.148, the verdict 0.118. The
  weapon in the window reads 0.184 / 0.121 with the wall and 0.193 / 0.123 without it.
- **Frame cost** (Electron 44, RTX 3070, 453x805, chain on, interleaved A/B over 3 fights, the PC loaded
  by the parallel builds): `drawBulwark` alone a median 0.3-0.5 ms, p90 at most 0.7 ms in the window;
  whole-frame medians within -1.3..+1.8 ms of OFF, which is the noise (frames 28-75 ms under the load).
- **Whole fights drawn:** 26, 325-3227 draws each, nothing thrown; blocks = flashes, arrows = scorches
  and banks = floats in every fight; the WARD tag once a window; the fold 0.24-0.48s after a clock close
  and 0.24s after a kill.

### 5b. No new `fx.js` field: the motes are drawn, and the nova's field spec goes out of both copies by the orchestrator

The design asks for "motes along the bar, both copies" of `fx.js`. A SPECS
field fires once, at the cast, from the one `m.ultFx` slot. The picture lab measured what that slot
gives this wall over 145 Bulwark windows (16 foes x 2 seeds, both sides; `lk_fxprobe.py`):
- the slot was Lightkeeper's at the cast in 121 of the 145; in the other 24 the foe's cast on the same
  step took it (both charges are 14);
- it then held the slot a median 0.64s (max 0.72) of the 8s window clock, so a field borne on it could
  exist for 7.3% of the window;
- once the slot is gone, the bar's centre stands a median 181 units from the cast point (p10 66, p90
  370), and the bar turns a median 7.59 rad in a window.

So the motes are DRAWN in the world pass, for the whole window (above): the Zenith, Canopy, Tendril and
Quarrelstorm precedent. **Rick's to overrule.**

The nova's own spec, `SPECS.lightkeeper` (a 1500-particle burst), is the brief's "nova's field spec
out". `fx.js` is shared by every build in the batch, so this builder never edits it, and it refuses to
write if its inlined copy moved (reading 14). The orchestrator takes the entry out of both copies with
`fx_remove.py --relic lightkeeper` at the carry, as it did for Ironhail. Its exact text in the base's
inlined copy (`sc-tendril-t3` line 32217; the b9.5 line 32315; the fx link line 32669):

```
    lightkeeper: { mode: 'burst', n: 1500, sp: [210, 560], grav: 70,
                   drag: 2.5, life: [0.35, 0.85], heavy: 0.03,
                   size: [0.8, 2.2], spawn: 0.05, up: 0 },
```

Tried on a scratch copy of the fx link (`fx_remove.py --fxjs <a copy of its inlined module>`;
`runs/stage6_fx_remove_scratch.txt`): only the block and the stamps move, the inlined module's stamp goes
28fc58641370a1a9 -> a74732c13d4bae1b, and the page becomes 619efdb849eae43e. The page is safe without it
(`sync` returns on a missing spec); the picture lab's engine_ab and probe ran on its own spec-out page.
**Until the carry, the stage-6 link still fires the burst at every cast, and so does the clip (§5f).**

### 5c. The voice

v77 §5. Every number here is `tools/lightkeeper_voice_lab.py`'s (4d22ab905b2306d3, its final run lab9,
Chromium 151). Its controls reproduce all six published numbers (rune-crack 0.608 / 450 ms, BAR 0.364 /
300 ms, hit@11.6 0.443 / 80 ms), and levels are read against Lightkeeper's own blow at 9.5.

- **The cast, the raise — PLATE, of 7, and the only one of the 7 that passes.** A plate's ring (a sine
  with its 1.73, 2.33 and 3.91 modes at 0.55, 0.4 and 0.2) glides one octave, A3 -> A4, in 0.36s,
  swelling 0.35 -> 1, re-struck on whole cycles (212 synth calls). It climbs +1083 cents and never turns
  back (its largest step is 7% of the climb: a slide, not two notes); it swells +8.0 dB to its top (not
  a strike) and flutters 2.9 dB (the lab's gate 3); its 1.73x mode stands 249 cents off every harmonic
  (metal). Audible 400 ms; the loudest 50 ms -2.8 dB re the blow; +6.1 dB over the score where a phone
  hears it (gate +6); register at most 0.68 (Starwarden).
- **A ball block, the gong — LOW-E, of 5.** One strike: an 82.41 Hz sine (E2) under a plate's 1.73,
  2.33, 3.91 and 4.11 modes, each dying faster than the one below, with a soft 20 ms mallet thump. 0.50 of
  its power is under 120 Hz at the worst noise draw (the design: >= 0.4); gone by 240 ms (the design:
  <= 0.3s), audible 235; the note holds (+1 cent); -2.8 dB re the blow; on a phone its modes stand +13.0
  dB over the score at 317 Hz; register at most 0.72 (the hit). DEEP is out (0.82 against the death
  voice).
- **An arrow, the tink — PIN, of 7.** One strike of a 4186 Hz sine (C8) with its 1.73 and 2.33 modes.
  Rise under 1 ms, audible 40 ms, gone by 45; 42.6 dB over the noise round it (a note, not a tick); -8.3
  dB re the blow and +11.2 dB over the wall tick; register at most 0.61. **The flam:** the k-th arrow the
  wall stops in one call is struck 26 ms x min(5, k) late (the nova's flam), so four arrows on one frame
  are four onsets, the stack's peak 1.00x one tink's.
- **The close, the fold — FADE, of 3.** The raise's ring gliding down, A4 -> A3, as its swell unwinds.
  It falls -1082 cents; its envelope correlates 0.97 with the raise's samples literally reversed; audible
  395 ms; -0.0 dB re the raise (the design does not say "quiet"); flutter 1.7. MIRROR is out (flutter 3.5).
- **Wiring.** The raise is `fireUlt`'s own prelude call, `SFX.play("ult", { w: f.w.id })`: Lightkeeper had
  no arm and fell through to rune-crack, which eleven other relics on the b9.5 still use, so the four arms
  go in BEFORE that fallback, which is re-emitted unchanged (reading 10). The tink plays once per arrow,
  after `T.arrows++`, its k a `var` local to the ticker's call (hoisted, so it starts at 0 on each call).
  The gong plays once per ball block, after `T.blocks++`, before the shove and the bank. The fold plays
  before the window's own close line, only when the close is by the clock with both alive (reading 11: a
  caster's death ends the fight, and a close after the foe's death belongs to its kill flight; either way
  the death voice has it, and a wall still up when the fight ends folds in the picture only). The bank
  has no voice (v77 names none).
- **The lab's wire run** (148 fights, Lightkeeper both sides x every foe, seeds 107601-2): 148/148
  identical, and every other SFX call identical in order and options; 638 raises for 638 casts, 4412
  gongs for 4412 blocks, 749 tinks for 749 arrows (k 0: 704, 1: 35, 2: 7, 3: 3), and 567 folds for 567
  clock closes, none on the 9 death closes (8 the caster's, 1 the foe's) or on the 62 walls the fight's
  end cut off. **Control:** one sim write (the foe nudged 1e-9 on a block) leaves 4/148 fights identical.
  End to end, the rows applied as text: 74/74 fights identical on the b9.5, 76/76 on the batch-tip scratch
  f2d72d2b1f7546a1.
- **A real window** (Lightkeeper v Gloamwire, seed 107602; cast 64.02s, clock close 74.99s; 13 blocks, 7
  arrows), each event read in the band where it stands highest over everything else in the window: the
  raise +6.8 dB at 252 Hz, the gongs a median +13.2 dB, the tinks a median +7.6 dB at 4032 Hz, the fold
  +16.1 dB at 400 Hz. Two controls with known answers pass: AFTER (no new voice sounding) reads +0.0 at
  every instant, and every event heard at +3 dB or more reads lower with its voice 20 dB down. **The lab
  changed this check's reading after it had seen the results** (rounds 3, 4, 4b and 4c, each declared in
  its docstring, the earlier readings printed beside the final). The check only tests the picks; no
  candidate, pick, row or voice threshold changed after lab4. `05-reference/v107/lightkeeper-pick-real-window.wav`
  and its `-without` twin hold that window with and without the new voices.
- **Main-thread cost per call:** the raise 8.2-12.7 ms and the fold 7.4-9.0 ms (212-250 synth tones, once
  per cast or close); the gong 0.2-0.3 ms, the tink 0.1. Worth knowing for the app's realtime play.

**Readings declared** (the builder's docstring, 10-19; art and sound are Code's picks):
10. The raise is the cast's own voice, an Sfx arm before the shared fallback: no row in the simulation.
11. The fold sounds only on a clock close with both alive, never on a death.
12. The tinks of one frame are flammed, 26 ms x min(5, k).
13. The design's "motes along the bar (both fx.js copies)" are drawn, not a SPECS field (above).
14. The nova's `SPECS.lightkeeper` leaves both copies by the orchestrator's `fx_remove.py`, not here.
15. The bar is read off `ultWall && alive && !over`, and folds on any of the three.
16. A block and an arrow are found by watching `wallTally` rise; the scorch is placed from each live
    shot's predicted next position, nearest the wall first.
17. A contact while the bar is still rising snaps it up.
18. The bank shows on the caster in the vigil branch's own "+N", a block's and an arrow's alike, nothing
    at the cap; the WARD tag once a window.
19. The nova's art is retired with the nova: the plate ring, the plates, the life entry; the charge rune
    redrawn.

### 5d. The probe's v6: what stage 6 added

`lightkeeper_probe.py` is now v6 (e1e09479216f72d6, its final form; its first form was ce9d1b07ee1b449f, and
v5, 8f4e1403afdd978d, is backed up in scratch).
Checks [1]-[8] are v5's, but for one change to [7]'s once-a-fight table check (the last bullet). Two checks are new, one for each half of stage 6, and **the link
itself switches each one on**, so the same probe still reads [1]-[8] alone on a link without stage 6:

- **[9] the voice**, on when `"lightkeeper-gong"` is in `AC.SFX.play.toString()`. `SFX.play` is wrapped
  for the run (put back after it) and every call recorded. It fails:
  - a Lightkeeper cast without exactly one Lightkeeper voice inside `fireUlt`, the raise;
  - a `tickLightwall` call whose Lightkeeper voices are not exactly, in order, a tink for each arrow its
    wall stopped (k = the arrow's index among the call's kills, from 0) and then a gong for each block;
  - on a closing frame, a fold that is not there when the close is by the clock with both alive, or
    **a fold on a close made by a death**;
  - any other voice inside `tickLightwall`. The wall hurts nobody, so not even a ward's shatter can sound
    there (the shatter plays its own crit hit voice inside `hurt()`, and hurt is never called on a wall
    frame: [7]);
  - a Lightkeeper voice anywhere else (at `over`, in the verdict, on a draw): every one in the run must
    be accounted for by its event.
- **[10] the picture**, on when the Match has `tickBulwark`. It fails:
  - `tickBulwark` (the picture's one hook on the step) changing anything but its own `bulwark*` fields,
    the floats, the tags and `taught`. That is read on EVERY call, as every own primitive field of both
    fighters, their status, window and tally, the match's primitives, every shot and every shade; and on
    every call where the picture has something to do (a cast, a block, an arrow, a fold) as v5's whole-
    state diff of both fighters, the match and the shared tables. Or `tickBulwark` drawing the RNG;
  - the bar up (`bulwarkFade` exactly 1) other than exactly while `ultWall && alive && !over`, or rising
    again with no cast;
  - a block or an arrow the picture does not take in on the call after the ticker made it (each call's
    rise in the tally must be exactly the ticker's count since the last call); a block without its
    two-frame flash (0.066 on the presentation clock, which counts half-seconds: 0.033s); arrows without exactly
    min(n, 8) new scorches, each on the bar;
  - a bank without exactly one "+N" float of the banked amount at the caster's seat, or a float with no
    bank; the WARD tag not exactly once a window, on its first bank;
  - a bar up at `over` not folded to 0 by 0.51s into the verdict (the verdict is stepped, the hook
    passing straight through); an event the picture never showed;
  - on the DRAWN subset (the first seed, both sides, every foe: 74 fights, drawn through the renderer
    every 6th step while the picture shows and every 60th otherwise, through the kill and the verdict,
    the post chain off), a drawn frame that throws, draws the match's RNG or changes a sim field.
- It also MEASURES, and does not gate, how far along the bar each scorch lands from where its arrow
  truly died.
- **[2] and [7] allow nothing new.** The picture's fields are written only in `tickBulwark`, which
  `tickPresentation` calls after the step's tickers (`this.tickBulwark(dt);` is its first line), never
  on a wall frame or at the cast; the voice is `SFX.play`, which holds no sim state. So v5's diff, with
  its allow-lists unchanged, still reads every `bulwark*` field on every wall frame and every cast, and
  a flash, a float or a scorch written inside `tickLightwall` or `fireUlt` would fail it. (Stage 5's §6
  expected stage 6 to name its fields in an allow-list; hanging the picture off the presentation tick
  made that unnecessary.)
- **One change to v5's once-a-fight table check, made twice.** The renderer keeps memos in `SHAPES`, and
  the drawn subset is the first time the probe has drawn. v6's first form left out the four memo keys one
  drawn fight had shown (`runs/stage6_shapes_draw.txt`: `_t` and the `_shadeCache`, `_facetCache` and
  `_inkCache` colour memos, on the base link and the stage-6 link alike). **Its first full run on the fx
  link read 9/10: [7] failed 348 times**, "the shared table(s) SHAPES written (axiom, seed 107001)" and
  then every fight after it (96 of 444 clean; `runs/stage6_probe_v6first.txt`). A drawn Axiom fight
  creates a fifth memo, `_fxc` (a Map the renderer caches in). Every foe drawn on both links shows the
  same five keys, all underscore memos, and the base link writes them exactly as the stage-6 link does
  (`runs/stage6_shapes_draw_all.txt`). So it is the probe's own drawing, not the build. **The fix does not
  name memos.** v6 now reads `SHAPES` key by key, every key, once a fight. Each drawn frame snapshots
  `SHAPES`' underscore keys before and after the draw, and takes what that draw wrote into the check's
  start. So a draw's own memo writes pass, and every other write still fails [7]: a draw's write to any
  other key, and the simulation's write to any key, a memo included. The run prints the keys it took in.
  **Controls** (scratch pages, on a small drawn field, Axiom, Gloamwire and Redflail x 2 seeds, both sides,
  drawn every 30th step; `runs/stage6_probe_smoke_*.txt`):
  - the clean fx link reads 10/10 there, and lists the five memos;
  - `mS1`, a block that also writes a new underscore key into `SHAPES` (`SHAPES._lk`), fails [7] alone,
    12 times (every fight);
  - `mS2`, a block that also writes the renderer's own `SHAPES._t`, fails [7] alone, 6 times: in each of
    the 6 undrawn fights. In a drawn fight a later draw rewrites `_t`, and the check takes in the draw's
    value; the headless seeds are where that write is read;
  - a first `mS1`, which set `SHAPES._fxc.lk`, **passed**. Once a drawn Axiom fight has made `_fxc` the
    renderer's Map, `lk` is an own property of a Map, and the probe writes a Map by its entries. It is the
    JSON limit §3 states, and one more case of it: a property set on a Map or a Set is not seen.

### 5e. Stage 6's gates — every one able to fail

- **engine_ab b9.5 → fx, ALL 38 WITH Lightkeeper, n=6: 4218/4218 identical** (`runs/stage6_engine_ab38.txt`;
  38/38 distinct winners, 4218 distinct seeds, 22.7-156.0s; the ids are in `runs/stage6_ids38.txt`).
  **Control:** the b9.5 against `mP1`, a copy whose picture nudges the foe 1e-9 on a bank, with
  Lightkeeper, Gloamwire, Redflail and Aureole at n=6: **18/36 differ**, exactly Lightkeeper's 18 fights
  (`runs/stage6_engine_ab_control.txt`).
- **lightkeeper_probe v6 (e1e09479216f72d6): 10/10 on the fx link** (`runs/stage6_probe.txt`, `.json`; 444
  fights, Lightkeeper both sides x 37 foes x 6 seeds, and the first seed's 74 drawn; 49.5 min). **[1]-[8]
  print every mechanism line the b9.5 prints under v5, to the character:** 4.38 casts a fight; 6.82 blocks,
  1.24 arrows and 23.49 banked a cast; 43.9%; the whole state clean on 1,754,465 wall frames (11,790 with a
  shade in the hall), 1945 casts and all 444 fights' tables; 80 volleys held. Then:
  - **[9] the voice:** 1945 raises for 1945 casts, each inside `fireUlt`; 2413 tinks for 2413 arrows, each
    k its index in its call (111 calls stopped two or more); 13,272 gongs for 13,272 blocks; **1699 folds
    on the 1699 clock closes, and none on the 43 death closes**; nothing else sounds inside the ticker; and
    every Lightkeeper voice of the run is accounted for by its event (1945 / 2413 / 13,272 / 1699);
  - **[10] the picture:** 7,983,735 `tickBulwark` calls, none of which changed a sim field or drew the
    RNG, 336,616 of them (every one with something to do) under the whole-state diff; the bar up exactly
    while the window is (3,851,454 calls), rising 1945 times and folding 1945 times, 252 of them in the
    verdict; 13,272 flashes, 2413 scorches on the bar, 15,070 "+N" floats (one a bank), 1880 WARD tags (once
    a window that banks); **the drawn 74: 67,079 frames through the renderer (61,128 with the picture up,
    10,279 of them in a hit stop, 266 in the verdict), none threw, drew the match's RNG or changed the sim.**
    The renderer's memos it took into [7]'s start: `_facetCache`, `_fxc`, `_inkCache`, `_shadeCache`, `_t`;
  - **the scorch, measured** (not gated): of the 1946 arrows the picture saw in flight, at least 95% scorch
    exactly where they died (p50 and p95 0 units along the bar), but the worst lands 208.8 units off, the
    bar's other end; the 467 loosed and stopped inside one step land a median 3.2 units off (p95 66.4, max
    140.3). The picture places a stopped arrow among the shots it predicted, nearest the wall first; the
    likely cause of the far ones is a shot that died some other way that step standing nearer (not traced);
  - **the controls** (scratch copies of the fx link, `runs/stage6_mutants.py`), each failing its own
    check and passing the other nine:
    - `mV1`, the fold on EVERY close: **[9] fails 44 times**, on the 43 death closes and once in the
      run's accounting (1742 fold voices, 1699 accounted for) (`runs/stage6_probe_mut_mV1.txt`, 444 fights,
      no drawing);
    - `mP1`, `tickBulwark` nudging the foe 1e-9 on a bank: **[10] fails 30,090 times** ("tickBulwark
      changed the sim: vx", read on the call itself) (`runs/stage6_probe_mut_mP1.txt`, 444
      fights, no drawing). It changes fights (the engine_ab control above), and [1]-[8] still pass, because
      they rebuild every frame from its own state;
    - `mD1`, a DRAWN frame nudging the caster 1e-9: **[10] fails 12,350 times**, on the drawn subset only:
      every drawn frame that draws the bar ("a drawn frame changed the sim") (`runs/stage6_probe_mut_mD1.txt`,
      the first seed's 74 fights, drawn every 30th step). The clean fx
      link on the same field reads 10/10 (`runs/stage6_probe_seeds1_drawn30.txt`: 18,188 frames drawn,
      12,237 with the picture up);
    - `mS1` and `mS2`, the sim writing `SHAPES` (§5d): [7] alone.
  - the probe's first v6 form, which named four memos, read 9/10 here ([7], 348 times: §5d), and its
    `mV1` and `mP1` runs read as they do now (`runs/stage6_probe_*_v6first.txt`).
- **On the line's tip of 08:04** (a bonus, not one of the gates asked for): the fx link the builder writes
  on `sc-angelus-b9-fx` (42 relics; compose15, f1dcb017f69db079), under the final probe, one seed, both
  sides, every foe, drawn every 30th step: **10/10** (82 fights, 369 casts, 333,572 wall frames clean; 369
  raises, 428 tinks, 2,447 gongs, 323 folds, 6 death closes silent; 20,363 frames drawn, 13,708 with the
  picture up; `runs/stage6_probe_on_angelus_tip_s1.txt`). The carry's own probe and `engine_ab` are still
  the orchestrator's.
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991,
  bulwarden:vinesower:70707, axiom:grudgebearer:31337) are **24/24 pixel-identical**
  (`runs/stage6_render_ab.txt`). **Control:** Lightkeeper v Gloamwire 107602 at t = 64.5 / 66 / 68 / 70 / 72
  / 74, inside the window that runs 64.02-74.99, is **0/6 identical** (`runs/stage6_render_ab_control.txt`).
- **chain_audit** `--builder lightkeeper_build.py`, with relic = tip = the fx link: **ALL 21 INSERTS
  SURVIVE**, stages 1-5's 8 and stage 6's 13 (`runs/stage6_chain_audit.txt`). Two of the 13 (the retired
  art branches) are found by their comment text, the code they leave being shorter than the tool's floor.
  **Control:** the same relic with the b9.5 as the tip loses all 13 of stage 6's inserts and exits 1
  (`runs/stage6_chain_audit_control.txt`). Both re-run with the final builder: the same.
- **tip_audit:** identical to the b9.5's, line for line, but for the file name (`runs/stage6_tip_audit_fx.txt`).
- **The builder's own guards** (`runs/stage6_builder_checks.txt`, `stage6_builder_negtest.txt`,
  `builder_negtest3_rerun6.txt`; the final builder a559dc47824545e9):
  - stage 6 refuses to run twice (its names are already in its own output), on stages 3, 2 and 1, on the
    bare tip, over an existing link, to a name not `sc-lightkeeper*`; stage 5 refuses on the fx link;
  - all five links rebuild byte-identical from the bare tip, `sc-tendril-t3`, no CR byte;
  - its scan of stage 6's ADDED code (a re-emitted anchor aside) refuses thirteen scratch variants, each
    with one forbidden thing written into a stage-6 insert: a sim write (the foe nudged), an RNG draw, the
    one ultFx slot, a beat in the gong row, a hurt, a status laid (stun), a splice of the shots in the air,
    an index write into the shots, a write to the tally, `Math.random`, a shared table through an alias
    (`P = AFFINITIES.vigil`), the shared weapon (`w.reach`), and a sim write in a draw method (the match's
    clock). The clean copy writes the fx link, e3f16bf01f0e2995;
  - the third round's ten table and weapon variants still refuse on the stage-6 builder, and its clean
    copy still writes the stage-2 link, a22bc1f8cb4b2dfe;
  - on stage 6 it also refuses if the inlined `fx.js` moved, if the nova's art is still drawn on the ultFx
    slot or its life entry is still in the map, and unless each of the four voices and the picture's hook
    is wired exactly once.
- **The rows, re-checked from the final builder, a559dc47824545e9** (`runs/stage6_rows_recheck.txt`, 08:10 on
  2026-09-29): `S6` is the two row files byte for byte, in order (voice 4, picture 9); the picture rows
  alone 728d64f8397290a1, the voice rows alone a8629a7fe94d50b9, both orders e3f16bf01f0e2995, no CR.
- **shell_identity** is not run here: the app's json is shared, and the orchestrator runs it on the
  carried link. The picture lab ran the app's own identity rows in its own Electron harness (Electron 44 /
  Chrome 152, never the app's json) on its stamp page against headless 151: **274/274** (85 with
  Lightkeeper); **control:** the same json against a 1e-9 sim-write page fails 191/274.
- **The labs' own gates** (§5a, §5c):
  - picture: bloom share +0.0000, with two controls that fail; sim identity on 13 whole fights x 4 arms
    (with and without the spec, drawn and undrawn), with a 1e-9 control that differs on all 11 Lightkeeper
    fights; 54/54 other-relic render frames, with Lightkeeper controls at 0/6 and 0/6; 26 whole fights
    drawn without a throw; `chain_audit` 9/9 on three tips, with a control that loses 9;
  - voice: the 148/148 wire run, with a sim-write control at 4/148 identical; 74/74 and 76/76 end to end;
    `engine_ab` 4218/4218 and the probe (v5) 8/8 on its own page, identical to the b9.5's.

### 5f. The clip (Rick's to overrule)

`tools/_lightkeeper_pick.py` (from `_ironwood_pick.py`, by way of `_ironhail_pick.py`) scores a window
against v77 §5. Three things are required, or the window scores nothing:
- the window closes BY ITS CLOCK with both alive, the only close that folds in the ear (a death's close,
  or the match's end, plays no fold);
- it has a block, an arrow and a bank the viewer sees;
- the fight runs on through the clip's 1.8s tail, so the kill does not take the picture.

Points then come from the blocks (0.5 each, up to 8), the arrows (0.6 each, up to 6), a frame with two
or more arrows (0.5: the flam, the tinks heard one by one), the banks (0.2 each, up to 6) and the blade's
blows in the window (0.2 each, up to 8). It ran every foe (37) x 4 seeds, plus the labs' four looks
(Gloamwire 107602, Aureole 4101, Marrowdraw 2207, Spellbreaker 99015), with Lightkeeper as side A, the side
`cinema_clip --a` films (`runs/stage6_pick.txt`). The pick is **Lightkeeper v Threshmaw (Redflail, whose
Bloodmill throws spikes), seed 107201**:
- the cast lands at 48.84, and the window closes by its clock at 59.07: 8s on the window clock, 10.22s of
  match time (the freezes);
- 13 blocks, 9 arrows (two frames of two), 20 banks (66 ward banked), 7 blows;
- the fight runs on to 69.03.

The runner-up, Lastlight 107312, scored 0.2 lower (11 blocks, 6 arrows).

The command is the pattern's, `--at <cast - 1.2> --window <dur + 1.2 + 1.8> --end-at-window`, with `dur`
read as the window's length in match time, 10.22s: the window clock stops in the freezes, so 8 + 3 would
end the clip 0.43s before the close, and the fold would not be in it.

    python cinema_clip.py --game <scratch>/batch/lightkeeper/links/sc-lightkeeper-bulwark-b9.5-fx.html \
      --a lightkeeper --b redflail --seed 107201 --at 47.64 --window 13.22 --end-at-window --fps 60 \
      --w 540 --out ../07-shorts/v107/bulwark-window.mp4

The clip (`runs/stage6_clip_check.txt`, `stage6_clip_log.txt`):
- 18.45s, 1106 frames: the window and 1.8s past the close. It is longer than the 13.22s of match time it
  films because the director slows the play from its T3 cut at 56.2 (Bloodmill), as it does on any clip;
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 5.29 MB (2d52915287c69d12);
- **AAC mean -23.4 dB, max -1.5 dB.**

Five frames, checked through the pipeline (the post chain and the director), matched to the fight's own
event times (`runs/stage6_clip_timeline.txt`) by the HUD's clock; tiled in
`05-reference/v107/lightkeeper-clip-frames.png`:
- 1.40s (49.1): the bar rising out of the ward ring, under the Bulwark banner;
- 3.13s (50.8): a block: the bar white for its two frames, the foe turned back, "+3" and WARD on the caster;
- 10.85s (57.6): Bloodmill's spikes dying on the bar, white strike rings where they hit, "+3" and "+6";
- 11.05s (57.8): the bar swung round with the blade, spikes still in the air;
- 14.42s (59.2): the fold, the bar drawing back into the ward ring after the clock close at 59.07.

**The pink spray round the foe in the cast's frames (1.3-1.5s) is the nova's own `SPECS.lightkeeper`
burst** (a `burst` goes to the quarry), still on this link until the carry's `fx_remove.py` (§5b). The clip
is `07-shorts/v107/bulwark-window.mp4` (gitignored). **Rick's to overrule.**

### 5g. Where each event hangs (stage 5's link)

The lines the rows hang on, in `sc-lightkeeper-bulwark-b9.5.html` (grep the quoted text on a carried
link; `runs/stage6_lines.txt` has them on the b9.5 and on `sc-ironhail-fxout`):

```
the cast       fireUlt 16273: the generic prelude (banner, 0.08s hit stop, beat "ult", SFX.play("ult", { w: f.w.id }) 16300,
               this.ultFx 16308, life map "lightkeeper: 1.5" 16335), then `if (u.kind === "lightwall"){` 16676:
               `f.ultWall = { t: 0, dur: u.dur, cd: 0 };` 16681, `f.wallTally.casts++;` 16685
the ticker     `this.tickLightwall(dt);             // BULWARK (v77)` 8942, after tickTendril 8941, before tickHits;
               method `  tickLightwall(dt){` 13658; live steps only (the step's frozen returns come first)
a frame        `Z.t += dt;` 13663; the wall from `const ux = Math.cos(f.theta)` 13668 (centre 50 ahead, endpoints +-110
               along (-uy, ux)); theta is tickWeapon's `f.theta = aim + Math.sin(f.swingPhase) * (f.w.arc || 1.2);` 9791
the close      `if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultWall = null; continue; }` 13664 (the clock, or a death);
               a fight that ends with the wall up never closes it (the picture folds on ultWall -> null OR m.over)
an arrow dies  13678 (a net's: stuck) / 13679 (spliced); `T.arrows++` 13680; its bank `T.banks++` 13686
a block        `Z.cd = u.cd;` 13693, `T.blocks++` 13694, the side 13695, the shove 13697-13698, its bank `T.banks++` 13704
the wall's art arena weapon drawWeapon 24016 -> SHAPES.greatsword 3453; ward ring drawStatus 23501 -> _stWard 23641 (R + 17)
the nova's art drawUltUnder `else if (u.w === "lightkeeper")` 21226, drawUltOver 22043, fx SPECS.lightkeeper (fx.js 120,
  (retired)    inlined 32315), ULTSIG.lightkeeper 601 (drawn by _ultSigil 26526)
names taken    "wall" is an SFX kind (7569); tickVine/tickVines; ultFx is one slot (picture state goes on the fighter)
```

## 6. What is left, and whose

- **Rick:**
  1. **The blade target** (open decision 2). Built at the design's default, the shipped rate: **9.5,
     44.3%** against the nova's 43.6. The other choice, 50%: **10, 47.6%** (the crossing 10.03), one
     line in the builder, already measured and gated (§4).
  2. **The shove's direction.** The build reads "away from the caster's side" as the lab computed it
     (to the foe's own side of the wall). Read literally (always outward, away from the caster), a foe
     behind the wall (44% of blocks) is pushed away instead of back: it changes nearly every fight
     but measures **-2.3 at 9.5 (44.3 -> 42.0) and +2.7 at 10 (47.6 -> 50.3)**, 1480 fights each,
     both sides, two blocks (`runs/rr_m8side_*`, `rr_m8side_b10_*`; the scratch variant `m8-side`):
     inside the noise and of no steady sign. The review's "about +6" was 444 fights at blade 10, and
     it reproduces (48.4 -> 54.7, `runs/probe_mut_m8-side_on_b10.txt`); at 1480 fights it is +2.7.
     A design line either way, not a price.
  3. **The window's length**, 8s, is the lab's default; the design names none (§0).
  4. The wall not stopping the foe's blade (open decision 3, as designed).
  5. The design's B = A control not holding on 151 on this base (+5.8, lab and build alike).
  6. **Marrowdraw can no longer beat Lightkeeper** (verify 40/0; relic_rate 100% at 9.5, 97.5 at 10,
     82.5 against the nova): a new red of verify's "both sides can win every matchup", this relic's.
     The wall is an arrow-killer by design, and Marrowdraw is the bow it beats by the most. It is the
     design's own result: the lab's arm C reads 1.0 / 1.0 against Marrowdraw on 151 (0.9 published),
     and its arm A, with no ultimate, 0.95 (§4).
  7. The bows at 80% (item 12/32); Heartwood 0/40 at 9.5 (10% shipped, 15% at 10).
  8. The veto (waived for the batch).
  9. **Stage 6, the picture and the voice (§5): the clip, and every pick in it.** The voice: the raise
     PLATE, the gong LOW-E, the tink PIN, the fold FADE. The picture: the bar on the test's own line,
     rising out of the ward ring and folding back into it, the white flash, the scorch, the "+N" and the
     WARD tag, the charge rune redrawn. Things worth an eye or an ear:
     - **the motes are drawn, not an `fx.js` field** (§5b), against the design's "both copies";
     - **the raise is the only one of its 7 candidates that passes, and on thin margins**: flutter 2.9
       dB against the lab's gate of 3, and +6.1 dB heard against a gate of +6;
     - **the voice lab changed its real-window check's reading after seeing its results** (§5c). No
       pick, row or voice threshold moved after it, but the check that says the four voices are heard
       in a real fight is the lab's fourth reading of itself;
     - three registers against other batch relics' new voices are printed, not gated, and stand over
       the lab's own 0.80: Portcullis's slam against the gong 0.83, Widowmaker's cast against the fold
       0.84, Lodestone's cast against the raise 0.82. They meet only in those pairings;
     - the raise and the fold cost 8-13 ms of main thread per call (once per cast or close), worth
       knowing for the app's realtime play;
     - a scorch lands exactly where its arrow died for at least 95% of the arrows the picture saw in
       flight, but the worst of those 1946 landed at the bar's other end, and an arrow loosed and stopped
       inside one step lands a median 3 units off (p95 66): measured, not gated (§5e);
     - the WARD tag once a window is the lab's own addition (reading 18);
     - "one whole fight watched" (design §5) is MEASURED here, not watched: the picture lab drew 26 whole
       fights through the kill and the verdict, and the probe drew 74.
- **The orchestrator (ALL DONE at the carry, §7):**
  - **carry the five links** in the handoff's order (after Exsanguinate), rebuilt with this builder,
    a559dc47824545e9, `--stage 1, 2, 3, 5, 6` on the tip of the day, with `engine_ab` on each carry, and
    **the probe (v6) on the carried fx link** (it reads [1]-[10] there, and would fail [7] or [10] if a
    carry let other code write the state on a wall frame or in the picture's hook). Exsanguinate is on
    the line now (254f9c4), so nothing waits ahead of this carry. The builder composes with every other
    batch builder as they stood at 08:07 on 2026-09-29 (`runs/compose15.txt`, 0 FAIL: the six committed
    and Censer, Aureole, Spellbreaker and Heartwood), and it writes the same change sets on every newer
    tip of the line up to `sc-angelus-b9-fx`, the tip of 08:04 (§0),
    where the stage-6 link it writes reads the probe's 10/10 on one seed (§5e). On `sc-tendril-fx` the carried b9.5 passed the
    probe (8/8 under v5) and `engine_ab` (3996/3996) at stage 5 (§0);
  - **take `SPECS.lightkeeper` out of both `fx.js` copies** at the carry (`fx_remove.py --relic
    lightkeeper`, as for Ironhail; the exact text is in §5b, and it was tried on a scratch copy). This
    build never touched `src/render/fx.js`;
  - **run `shell_identity` on the carried fx link** (not run here: the app's json is shared). The picture
    lab's own Electron harness read 274/274 on its stamp page, with a control that fails (§5e);
  - send the clip to Rick (one clip per ultimate); the app's pointer is not this build's (the staff row
    is the build of record).
- **Stage 6 (Code's): done** (§5). What is left of it is the orchestrator's (the spec out, `shell_identity`,
  the clip to Rick) and Rick's (every pick is his to overrule).
- **Standing, not this build's:** verify's two clock bands (red on every link since the minute pace);
  Heartwood vs Twinshade and vs Bindweed 0/40 (the base's, fights identical by engine_ab); the engine's
  generic cast prelude (the BULWARK banner and its pale ring) still plays at every cast, as it does for
  every relic.

## 7. The carry onto the chain, and the nova's field spec out

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Angelus with the
same builder, one stage at a time (`--src` the previous link), and one more link that takes the retired
nova's particle field out:

```
sc-angelus-b9-fx.html                  the batch line's tip (Angelus stage 6)       85b8af63055d1108
  -> sc-lightkeeper-stub.html           stage 1                                      f568883a722ff9bc
  -> sc-lightkeeper-wall.html           stage 2                                      9c2faba089b9c294
  -> sc-lightkeeper-bulwark.html        stage 3                                      f5f2430551ef0d2b
  -> sc-lightkeeper-bulwark-b9.5.html   stage 5                                      f6cca22c0d2d402e
  -> sc-lightkeeper-bulwark-b9.5-fx.html stage 6                                     f1dcb017f69db079
  -> sc-lightkeeper-fxout.html          SPECS.lightkeeper out of both fx.js copies   088189f3517b6f11
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail and Widowmaker (redesigned on the chain since), n=6: **3780/3780 identical**
  (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-angelus-b9-fx` against the carried stage-6 link, every relic on the tip but
  Lightkeeper (41), n=6: **4920/4920 identical** (`runs/carry_engine_ab_tip.txt`): the redesign moves
  no other relic's fight on the batch line.

**The nova's field spec out: `tools/fx_remove.py --relic lightkeeper`**, the entry's three lines; the
`/* ---- NOVAS ... */` header above it stays for Censer (`runs/fxout/fx_remove.txt`).
**fx.js bb57bd38ca475650 -> 830a7026987903b4.**

**Gates on `sc-lightkeeper-fxout`** (`runs/fxout/`, run one at a time at idle priority: Rick was on the
PC):
- engine_ab against `sc-lightkeeper-bulwark-b9.5-fx`, all 42 relics, n=6: **5166/5166 identical**;
- `lightkeeper_probe.py` on the carried link: **10/10** -- it met every relic carried since its scratch
  base and needed no change;
- render_ab: the other relics' four pairs **24/24 identical**; **the control, Lightkeeper v Threshmaw
  (redflail) 107201 through the cast (48.87-49.25s), 0/5 identical** -- the burst is gone;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold;
- **shell_identity 200/200** (app Chromium 152 vs headless 151), run 2026-09-30 05:30 once Rick was off the PC (`runs/fxout/shell_identity.txt`; the pointer not moved, the json restored).

**The clip, re-filmed on `sc-lightkeeper-fxout`** (the §5 command, `--game` the carried link):
`07-shorts/v107/bulwark-window.mp4` (4.98 MB; 13.22s of match time, 18.4s on screen through the hit
stops; `runs/fxout/clip.txt`), the cast without the burst.
