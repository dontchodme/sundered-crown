# v105 — ORACLE / FORESIGHT, BUILD. STAGES 0-6 DONE AND ON THE CHAIN (built in scratch on `sc-tendril-t3`, carried onto `sc-widowmaker-fxout`, §7). Stage 1 is arm A, fight for fight. The mechanism is the lab's: 7/7 read inside the hooks, and 12 mutants each fail their own check and only it (two are the review's, which the first probe could not see; §3a). The win rate runs over the lab's because of the engine's window clock and the prose's no-spin aim; put the lab's three constructions back and the build reads arm C, at 16.23 and again at 10. The blade sits at the measured crossing, 10 (49.5% both sides), UNDER the brief's 11.5-12. The brief names no other knob, so nothing else moved, and the miss is said. At stage 5, engine_ab over the 38 others 4218/4218 identical and verify 11/13, the two reds being the clock bands. Stage 6 draws the rune-eye, the rune at the lead with its sight-line and drawn motes (no `fx.js` field), the window arrows' rune, the flare and the HEX tag ticking by two, and voices the cast, the sigil, the snap and the close, from the labs' rows byte-exact: the probe reads 9/9 inside the hooks, six stage-6 mutants each fail their own check and only it, engine_ab over all 39 is 4446/4446 identical and render_ab 24/24 (the Oracle control 1/6). The clip is with Rick. Not on the chain: the orchestrator carries it.

Claude Code on DESKTOP-DERRAFT, claimed 2026-09-27 08:54 UTC (`CLAIMS.md`). Input: `06-docs/v75/ORACLE-BUILD-BRIEF.md` +
`runic-bow-design-v75.md`, and nothing else (rule 0). Builder `tools/oracle_build.py`, probe `tools/oracle_probe.py`,
runs in `runs/`. **A NEW relic: the 39th on its base** (`sc-tendril-t3` carries 38; the brief's "42nd" counts the grid's
cells, and the relic's number on the chain is the carry's). Built IN SCRATCH on the chain tip the batch forked from, while
other builds ran on the same tip; the links are in the batch scratch (`<scratch>/batch/oracle/links/`), not in `02-chain/`.
Five sessions built it (four usage-limit cuts); every link was rebuilt from the builder after each cut and matched to the byte.
A sixth and a seventh session (one more cut) fixed it after an adversarial review (§3a): the probe was blind to two
mutants that move fights, and chain_audit could not watch the aim. Links 2, 3 and 5 were rebuilt for that (they play
every fight the first build played, §3a); stage 1 rebuilt byte-identical. Stage 6 took two more sessions (one cut); all
five links were then rebuilt from the final builder and matched to the byte (`runs/stage6_rebuild_final.txt`).

```
sc-tendril-t3.html          the base (Bindweed stage 5 over Portcullis stage 5; 38 relics)      5a6216e3b629fad4
  -> sc-oracle.html          stage 1  the relic, ult stubbed (charge 1e9)                        d68f270896af8fe3
  -> sc-oracle-aim.html      stage 2  the aim, charge 14 (arm B)                                 1932863f5ab0f88a
  -> sc-oracle-sight.html    stage 3  the double hex, hex 0 -> 1 (arm C)                          23229388fac65e8a
  -> sc-oracle-b10.html      stage 5  the blade, 16.23 -> 10                                     72dcd8aa43e5b501
  -> sc-oracle-fx.html       stage 6  the picture and the voice (+23,005 chars)                  4e8f47301b97d7d7
```

The brief has no stage 4. `python oracle_build.py --stage 1|2|3|5|6 --src <link> --out <link>` (absolute paths work).
**Builder ae5d6f4e641a2b16, probe dfeee05201267ed0** (sha256[:16]); every link above rebuilds from this builder to the
byte. Stages 0-5 closed on builder 1e18f0642c2de40c and probe df3ca99e5cbd41d5: stage 6 added the S6 table, `--stage 6`
and readings 11-15 to the builder (stages 1-5 still write the same bytes), and [8], [9] and the cast's one-beat clause
to the probe (§6a). The clip is `07-shorts/v105/foresight-window.mp4` (bbd98ccb2179a5f0; §7).
The first build of links 2 / 3 / 5 (8bfe5968101e10de / 1b599fca2040534e / 2610d11c5c35fdf8) differs from these only in
the aim's three local names and one comment (§3a). Every number in §2 that was measured on those first links is carried
by the fight-for-fight proof in §3a, and the rest were measured again on these.

## 0. What this build stands on

- **The relic** is the bow type's profile off Ironhail's row, the lab's donor (`ult_overlay --relic ironhail --cell
  runic:bow`): blades [0], reach 54, width 9, artW 44, spin 2.8, ranged, mass 1.6, and the type's `shot` block (cadence
  0.34, speed 380, r 24, life 3.4, grav 0, dmgMul 1.0), at Ironhail's blade 16.23 until stage 5; aff runic, onHit hex 1,
  and the design's 68-character card. The builder asserts the profile on Ironhail's row (its blade may move under
  Ironhail's redesign; the profile may not), the school's channel on the four runic relics, `STATUS.hex`, `ballisticAngle`
  returning `atan2` at grav 0, the ranged branch of `tickWeapon`, and the order of `resolveHit`'s onHit loop.
- **The charge is 14:** the design's 16 on the lab's clock, converted (Rick's batch ruling). Measured for this fighter on
  arm C with a scratch copy of the lab that counts, before each lab step, the steps that start frozen (`m.hitStop > 0 ||
  m.latch || m.splitHold`), 660 fights a block (`runs/aim_census.js`, `runs/s0_census_C_*`): **11.27% / 11.26% of the
  lab's steps are frozen (14.01% / 14.12% inside windows)**, so the lab's 16 is the engine's 16 x 0.887 = 14.2, and 14.
  The census copy reproduces arm C to the fight (75.2% on both blocks).
- **The lab is `ult_overlay.py` with `overlays/aim.js`**, the brief's own stage-0 command. Its defaults are the settled
  numbers (turn 6, hexExtra 1, lead on; the harness's charge 16 and window 8): **nothing to flag.**
- **Readings** (in the builder's docstring):
  1. **The window is `{t, dur}` on the window tickers' clock**, not the brief's `{ t0, end }` in match time: every
     window in the batch runs on that clock, and a freeze freezes the world. `tickSight` advances it.
  2. **The aim turns while stunned.** The lab turned the facing on every window frame, and the design says "each window
     frame" and names Tendril's construction, which turns while stunned. A stunned bow still cannot FIRE (`tickFire`'s
     own rule, untouched); it comes out of the stun already aimed. 16% of window frames are stunned frames (the probe).
     It does not turn in a hit stop: `tickWeapon` does not run there.
     **The text against this reading** is the brief's §1: the facing turns toward the lead "instead of `theta +=
     spin·dt` (the ranged branch)". In the engine the ranged branch sits AFTER the stun lock, so a stunned bow never
     reaches it. The build reads the parenthesis as naming the statement the aim replaces (the spin's advance), not as
     placing the aim under the lock, because the design's "each window frame" and "Tendril's construction" are the
     explicit words and the lab priced the turn on every frame. **Priced (§2):** the bow held while stunned reads
     44.1 / 49.2 = 46.6% both sides, against the link's 49.5 on the same fights: the reading is worth about +3.
     Rick's to overrule (§6).
  3. **The spin does not advance theta in the window** — the prose, twice (design §5, "the spin does not advance theta
     while the window runs"; brief §0, "spin does not advance theta in-window"). The lab left the engine's spin running
     and turned at 6 on top of it, so its turn was 6 ± 2.8 while acquiring and exact while locked; the build turns at 6
     flat. Priced in §2 (+3.8).
  4. **The second hex is on a shot only** — the prose is explicit (design §5, "when a SHOT owned by a caster with
     ultSight lands"; §1, "an arrow that lands hexes twice"). The lab added it on every `me.hits` step, which also
     counts the bow's blade blows (1.1 a cast). A shot is `mul !== undefined` in `resolveHit`, the engine's own test.
     Priced in §2 (0.4, nothing).
  5. **The second hex goes on a live foe, the opponent only** (the lab's `foe.alive`; never a Twinshade shade), after
     the channel's own stack.
  6. **`apply`'s source is a side letter** (the engine's contract; the lab passed the Fighter; hex has no reader of it).
  7. **The window closes on either death** (the lab's close) or its clock.
  8. **On a window frame where either fighter is dead the aim holds** (no spin, no turn; the lab aimed only while both
     lived); the window closes in that step's `tickSight`.
  9. **The blurb** is the design's §1 sentence, shortened; the card is the design's. Rick's to overrule, as every name is.
     The card says "each hit hexes twice", but by reading 4 only an arrow does: the 1.6 blade blows a cast inside a
     window hex once. The mechanism follows the prose (worth +0.4, §2); the card's wording is Rick's (§6).
  10. **The brief's stage-2 gate "theta within 6·dt of the lead bearing on every window frame after the first
     half-second (asserted)" cannot hold, and does not hold in the lab either.** The lead is `foe + v_foe x tof`, and
     the foe's velocity jumps on every bounce and knock, so the lead bearing jumps faster than 6 rad/s can follow. The
     lab's own facing sits within 6·dt of it on **43.6% (arm B) / 43.5% (arm C)** of those frames (`runs/aim_lock.js`,
     `runs/s0_lock_BC_2207`); the build's on 41.3% / 40.9%. What IS asserted, on every window frame, is the
     construction itself: theta + clamp(the shortest angle to the lead, ±turn x dt). The lock is printed; 98% of the
     frames off it fall within 0.6s of a jump in the foe's velocity.
- **Names:** kind `"sight"`, fields `ultSight` / `sightTally`, ticker `tickSight`, all free on the base (grepped).
  "sigil" is Converse's (`drawSigils`, `m.sigils`): stage 6 must not reuse it.
- **The clock:** the window and the turn run on the window tickers' clock (`tickWeapon` and `tickSight` both stop in a
  hit stop). The lab ran both through freezes. v99 §4, v100 §2 and v101 §2 measured what that is worth; §2 here does.

## 1. Stages 1, 2, 3, 5, 6

Every anchor is replaced exactly once or the builder refuses, and each one composes with builds carried before or after
it:
- **the row** goes at the END of `WEAPONS`, on the array's closing `];` and the comment after it ("The single source of
  truth for ...": unique, names no relic);
- **the fields** go after `this.vineTally = null;`;
- **the cast branch** goes before `if (u.kind === "tendril"){`;
- **the aim** is a new `else if (f.ultSight)` before tickWeapon's `else if (f.stun > 0){ /* weapon locked */ }`,
  which is re-emitted;
- **the second hex** goes after `resolveHit`'s onHit loop, before the curse figure's comment ("THE BLOW LEAVES A
  FIGURE ON THE FLOOR"), which is re-emitted;
- **the ticker call** goes after `this.tickTendril(dt);`;
- **the method** goes before `tickWinnow(dt){`.

Nothing waits, so the cast's stable prefix is not touched. The builder asserts its base by content (never by which relic
is last), strips comments before checking the ult block and scanning its inserts (no `rng()`, `Math.random`, `spawnFx`
or `ultFx`; no write to the shared weapon row, `w.*`; no pin, stun or hit stop; no hurt, beat, knock, resolve or
shatter), refuses to overwrite a link, runs `node --check` on the page and writes LF.

**chain_audit can watch every insert, and the builder checks it.** For each insert it has applied, the builder takes the
line chain_audit recognises that insert by (chain_audit's own `_cands`: the longest line the insert adds, code first,
the first one the build contains) and refuses to write unless that line is in the output exactly once. The first build
failed this without anyone seeing it: the aim's longest line, `const dl = Math.atan2(Math.sin(want - f.theta), ...)`,
is also a line of Tendril's seek, so chain_audit read "ok" for the aim on a tip that did not have it. The aim's locals
are now `leadX` / `leadY` / `bearing` (no float moves). The builder with the old names refuses stage 2
(`runs/builder_marker_control.txt`).

- **Stage 1** appends the row with the ultimate stubbed at charge 1e9 (+952 chars, 39 relics).
- **Stage 2** (+4,270 chars):
  - the fields `ultSight` / `sightTally`, null on every relic;
  - the cast: `f.ultSight = { t: 0, dur }`, and nothing resolves;
  - the aim in `tickWeapon` — the facing turns at `turn` toward `bearing = ballisticAngle(lead - f)`, which is `atan2`
    on a grav-0 bow — with the lead `(leadX, leadY) = foe + v_foe x (|foe - f| / shot.speed)`;
  - the second-hex clause in `resolveHit`, inert at hex 0;
  - `tickSight` after `tickTendril`: the clock, the close on the clock or either death, the probe's tally;
  - charge 14.
- **Stage 3** flips `hex` 0 -> 1.
- **Stage 5** moves Oracle's own `dmg` from 16.23 to 10 (-3 chars).
- **Stage 6** adds the picture and the voice (+23,005 chars): eleven anchored edits, the two labs' rows byte-exact.
  Its anchors, its refusals and its own scan of the added code are in §6 and §6a; at stage 6 the marker check covers
  all 21 inserts.

`tickFire` is untouched: the stream fires on its own cadence along the aimed facing.

## 2. Stage 0 and the stages against it — the window clock and the spin, measured

`ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic ironhail --cell runic:bow --mech overlays/aim.js
--arms A,B,C --seeds 20 --foes <33>`. That is seed0 2207 and 2317, 660 fights an arm a block. The foes are the design's
roster: the 34 minus the donor (`runs/foes33.txt`). The built links run `--relic oracle --arms SHIP` on the same foes and
seeds (the same seed formula, Oracle as side A).

```
                       lab on 151 (1 / 2)   published 141 (660)   lab at dur 9.31 (1 / 2)   BUILT (1 / 2)               pooled
A   no ultimate        32.4 / 33.5          31.1                                            stage 1: 32.4 / 33.5        identical, fight for fight
B   the aim            67.1 / 66.7          68.2                  71.5 / 73.6               stage 2: 82.6 / 84.1        83.4 (lab 66.9)
C   + the double hex   75.2 / 75.2          73.2                  77.9 / 78.0               stage 3: 85.9 / 87.0        86.5 (lab 75.2)
A at blade 10          7.0 / 4.5                                                                                        5.8
C at blade 10          32.7 / 31.8                               41.4 / 38.8 (dur 9.41)    stage 5: 50.8 / 55.5        53.1 (lab 32.3)
```

**Published vs 151:** A 31.1 → 33.0, B 68.2 → 66.9, C 73.2 → 75.2 (pooled 1320). All three are inside two standard errors.
The brief's own reproduction targets ("A ~31%, C ~73%") hold.

**The lab's mechanism on 151** (arm C, block 2207):
- 3.08 casts; 12.59 blows in windows and 11.66 outside a fight;
- 4.09 blows a cast in windows: 2.98 arrows and 1.11 blade blows (`runs/s0_lock_BC_2207`, counted inside `resolveHit`).
  The lab's own "arrowHits" column, 3.93, counts every `me.hits` step its frame hook sees, blade blows included;
- the foe at 2.82 hex on a window frame;
- the lock 43.5%; 14.0% of window steps frozen.

**The built relic reads 11 over arm C at stage 3 and 16 over arm B at stage 2.** Four controls, each a scratch copy of the
built link with one of the lab's constructions put back (`runs/ctl_*`; the variants are `runs/variants.py`), same foes,
seeds and side. (The controls were cut from the first build of the links; the rebuilt ones play every fight the same,
§3a.)

```
control (on the stage-3 link unless named)                              block 1 / 2   pooled   what it is worth
the lab's clock: the window and the aim run through hit stops too       81.4 / 80.9   81.2     the engine's clock: +5.3
the lab's spin: the spin keeps turning theta, the aim rides on top      81.1 / 84.2   82.7     the prose's no-spin aim: +3.8
the lab's hex: the second hex on every blow in a window, blades too     85.9 / 86.2   86.1     the prose's arrows-only: +0.4 (nothing)
all three of the lab's constructions                                    75.6 / 73.3   74.5     = lab C 75.2
stage 2, the lab's clock                                                78.2 / 76.2   77.2     the engine's clock: +6.2
stage 2, the lab's clock and spin                                       69.4 / 68.9   69.2     the no-spin aim: +8.0; = lab B 66.9 (+2.3)
```

The clock controls run the window and the aim through the hit stop's frozen path. The rarer latch and split-hold
freezes are not covered, which is the most the +2.3 at stage 2 can be besides noise (1320 fights, ±1.3 a side).

**The whole gap is the two constructions, and nothing is mis-built:**
1. **The window clock**, worth about +5 at stage 3. The engine's 8s are 8 seconds of the window tickers' clock, which
   stops in a hit stop, and 14.1% of window steps are frozen, so a window is ~9.3s of match time. The lab's 8 were
   8 step-seconds, frozen ones included. The lab run at 9.31s reads 78.0 against its 75.2 at 8. This is the clock v99 §4,
   v100 §2 and v101 §2 measured; here it pushes up, through more arrows a window (3.66 against the lab's 2.98).
2. **The no-spin aim**, worth about +4 at stage 3 (+8 at stage 2, on the lab's clock). The prose says the spin does
   not advance theta in the window. The lab's facing kept spinning at 2.8 under a 6 rad/s turn, so when the lead
   jumped against the spin it was acquired more slowly.
3. **The second hex on arrows only** is worth nothing (the lab's extra hex on 1.1 blade blows a cast reads +0.4).

With the lab's three constructions put back, the build reproduces arm C (74.5 against 75.2). The build keeps the
engine's convention and the prose, and every designed number; stage 5 prices the result with the blade.

**At the stage-5 blade the same gap is +21, and the same controls account for it** (`runs/ctl10_*`, `runs/lab10_*`; the
variants are the same `variants.py` edits on `sc-oracle-b10`, same foes, seeds and side):

```
at blade 10                                                   block 1 / 2   pooled   what it is worth
BUILT sc-oracle-b10                                           50.8 / 55.5   53.1
the lab's clock                                               45.0 / 44.5   44.8     the engine's clock: +8.4
the lab's spin                                                35.2 / 35.0   35.1     the prose's no-spin aim: +18.1
all three of the lab's constructions                          33.2 / 33.6   33.4     = lab C at 10, 32.3 (+1.1)
the lab (arm C) at the engine's window, dur 8 / 0.850 = 9.41  41.4 / 38.8   40.1     the clock in the lab: +7.8
the lab's body (arm A) at 10                                   7.0 / 4.5     5.8
```

**Reading 2, priced the other way** (§0): the bow held while stunned in the window (`variants.py mut-stunlock` on the
rebuilt `sc-oracle-b10`; `relic_rate` both sides, 38 foes, the stage-5 grid's seeds; `runs/stunlock_rr_*`) reads
**44.1 / 49.2, pooled 46.6%** (side A 47.5, side B 45.8; mean fight 66.8s), against the link's 50.7 / 48.3 = 49.5% on
the same 1,520 fights. The reading is worth about **+3 (2.8)** at the blade the relic ships at; a difference of two
1,520-fight rates has a standard error of about 1.8, so it is real but small. It is not part of the lab gap: the lab
turned the facing on every window frame, as the build does. The probe fails the control on [2] only (§3a).

The window here is 9.41 because 15.0% of window steps are frozen at blade 10 (the probe, §3). At 10 the body is
5.8%, so the ultimate carries nearly the whole win rate and the relic sits on the steep middle of the curve. The same
two constructions buy about twice the points they bought near the ceiling at 16.23: the no-spin aim +18 (against +4),
the clock +8 (against +5). The three constructions put back land on the lab again (33.4 against 32.3, inside a standard
error of ±1.3). **That is why the brief's band misses.** The brief's "expect 11.5-12" was priced on the lab's
spin-riding aim and its step clock. The prose's aim on the engine's clock is a stronger ultimate, so its crossing is
lower. §4 says what that leaves for Rick.

## 3. The probe (`oracle_probe.py`, one check per sentence, read inside the hooks)

It wraps `step`, `tickWeapon`, `tickFire`, `tickCharge`, `fireUlt`, `resolveHit` and `tickSight` on the Match prototype
and plays Oracle against every other relic, from both sides, 6 seeds a foe a side (456 fights). Each check is one
sentence:

1. **the window:** the cast opens `{t: 0, dur}`; the clock advances exactly dt on each window-ticker frame; the window
   closes on the first frame it reaches `dur`, or on either death, and never otherwise; only Oracle ever carries
   `ultSight`. And on entering `tickSight` the window is exactly what the cast or the last `tickSight` left (the same
   object, `t` and `dur`), so no writer elsewhere in the step can stretch or cut it.
2. **the aim:** on every window frame, stunned or not, the facing is exactly theta + clamp(the shortest angle to the
   lead, ±turn x dt); it does not move in a hit stop; outside the window it spins as ever (held while stunned).
3. **the stream:** `tickFire` untouched — one shot along `f.theta` at the shot speed when the cadence runs out, in the
   window and out, and none while stunned or down; and on entering `tickFire` the cadence clock is what the last
   `tickFire` left (only `tickFire` writes `fireCd` in this engine).
4. **the arrow as ever:** every blow's damage rebuilt exactly from the captured crit and jitter draws; the blow's own
   hit stop (a ward's own shatter aside); one hit beat.
5. **the double hex:** an arrow landing in a window applies the channel's hex and exactly one more, with a side letter;
   there is nothing extra on a blade blow or outside a window, and the tally matches.
6. **nothing else:** `tickWeapon` writes the caster's facing and nothing else. Every other field of both fighters
   (the balls, `spinDir`, `fireCd`, `stun`, hp, ...; the foe's facing too), both swing phases, both status maps, the
   tally, and the match's clock, stop and shots are snapshotted across it, in the window and out. The caster's charge
   is [7]'s and its window [1]'s, so every field has one owner. `tickSight` writes only its window and tally; no
   apply moves the stop.
7. **the cast** ("every 16s", 14 on the game's clock; "nothing waits"): it fires on the frame the charge reaches
   `charge`, and never under an open window. On every live frame with no cast the charge fills by exactly dt, and on
   a dead or ended one it does not move. On entering `tickCharge` the charge is what the last `tickCharge` left (0 at
   the first): only `tickCharge` writes it in this engine, so any other writer is a faster or slower clock.

"A check that never ran is not a pass": each check also requires its events to have happened (window frames, stunned
aim frames, shots in and out, blows in and out, second hexes, casts, and each owner's entries).

**Stage 6 adds two checks and a clause** (§6a): [8] the voice and [9] the picture, each switched on by the page itself;
and [7] now also fails a cast that files anything but exactly one `ult` beat (the brief's stage 6: "cast files `ult`").
On `sc-oracle-b10` the new probe reads 7/7, every line identical to the stage-5 run in the table below but that clause
(1,714 casts, one beat each; `runs/stage6_probe_b10.txt`); on `sc-oracle-fx` it reads 9/9 with every stage-5 line
identical too.

```
                                   stage 2 (aim)   stage 3 (sight)   stage 5 (b10)    lab C (2207)         lab C at 10 (2207)
checks                             7/7             7/7               7/7
casts a fight                      3.03            3.05              3.76             3.08                 3.76
blows in / out of windows a fight  14.50 / 10.27   15.05 / 10.02     21.52 / 12.16    12.59 / 11.66        17.07 / 13.91
arrow hits a cast                  3.53            3.66              4.09             2.98
blade blows in windows a cast      1.26            1.28              1.63             1.11
second hexes a cast                0               3.52              4.03             (3.93: every blow)   (4.48: every blow)
foe hex on a window frame          2.25            2.79              2.96             2.82                 2.94   (the lab's f_foeStk)
the lock (after 0.5s)              41.3%           40.9%             39.2%            43.5%
window steps frozen                14.7%           14.6%             15.0%            14.0%
stunned window frames              16.1%           15.7%             16.3%
Oracle win (both sides, 38 foes)   81.4%           83.1%             49.6%            (side A, 33: 75.2)   (side A, 33: 32.7)
```

The foe-hex row is per fight, as the lab's `f_foeStk` is. The lab's columns come from its own frame hook, the build's
from the probe's hooks; the lab's "arrow hits" column counts every `me.hits` step, blade blows included, so it is
split here only where `runs/s0_lock_BC_2207` counted inside `resolveHit` (arm C at 16.23).

- **Hex applied by window arrows** at stage 3 is 9,990 for 5,090 arrows. That is two a hit (the brief's gate), less 190
  arrows that killed: the second hex needs a live foe.
- **Outside the windows** the bow lands 2.0 arrows in 8s of live time on every link. The brief's "~1.1 a
  window-equivalent" is not a column the lab prints, and it is not reproduced here; the in-window arrows a cast and the
  split of blows are.
- **The window's length on the window clock** is exactly `dur`. 1,065 of 1,269 windows closed by the clock at stage 3
  (1,402 of 1,549 at stage 5); the rest closed on a death.
- **Mutants:** twelve scratch copies of `sc-oracle-b10`, each breaking one sentence in a way that changes fights. §3a
  has the table: each fails its own check and only that one.
- **Stage 1 is arm A fight for fight** on both blocks: the win rate, the blow counts (0 / 19.76 and 0 / 19.70) and every
  foe's rate are identical (`runs/built_oracle_*` against `runs/s0_ABC_*`).
- **Drawn:** stage 3's fights run through the renderer (`AC.__draw`) against 6 foes, both sides, 36,750 draws (35,313 in
  a window): no throw, no sim write (`runs/draw_smoke_sight.txt`). Kind `"sight"` falls through every renderer table.
  SPECS has no `oracle` entry, so the cast spawns no field.

### 3a. The fix round: what the review found, and what changed

An adversarial review of the first build found two mutants that move fights and still passed the probe 7/7, and one
insert chain_audit could not watch. Both findings were right; this is what was done about them.

- **The charge ([7]).** The review's `rv-charge` adds `f.charge += 0.25 * dt` inside the aim, so a window feeds the
  charge 25% faster and the designed "every 16s" (14 on the game's clock) breaks. The first probe computed "due" from
  whatever the charge was when `tickCharge` began, so it followed the inflated value and passed. Only `tickCharge`
  writes the charge in this engine (the constructor, `f.charge += dt`, and `f.charge = 0` at the cast; grepped). The
  fixed [7] keeps each fighter's charge as `tickCharge` left it and fails if it differs on the next entry (0 at the
  first). It also fails a live frame with no cast whose charge did not fill by exactly dt.
- **Every field across tickWeapon ([6]).** The review's `rv-spindir` sets `f.spinDir` in the aim, so the bow leaves
  each window spinning the way it last turned: "outside the window the spin runs as ever" breaks. The first [6]
  compared only the two balls across `tickWeapon`, and [2]'s out-of-window check reads `spinDir` fresh each frame, so it
  followed the corrupted value. The fixed [6] snapshots every field of both fighters across `tickWeapon` (the foe's
  facing included), both swing phases, both status maps, the tally, and the match's clock, stop and shots. It skips
  only the caster's facing ([2]), charge ([7]) and window ([1]), so each field has one owner and a mutant fails once.
- **The same hole in [1] and [3], closed the same way** (not in the review; found by asking where else a check reads
  its own input fresh). [1] read the window's `t` fresh on entering `tickSight`, and [3] read `fireCd` fresh on
  entering `tickFire`. So a writer anywhere else in the step could stretch the window or quicken the stream unseen.
  Both now keep what their owner left: the cast or `tickSight` for the window, `tickFire` for `fireCd` (grepped: only
  the constructor and `tickFire` write it). Two new mutants prove it: `mut-winclock` (the aim runs the window's clock
  back 10%) and `mut-cdhit` (each window arrow that lands takes 0.05 off the cadence clock).
- **chain_audit and the aim.** See §1: the aim's locals are renamed, and the builder refuses any insert whose
  chain_audit marker is not in the output exactly once. The first build's aim marker was also a line of Tendril's
  seek; the control of the rebuilt link against the base now loses all 10 inserts (§4).

The mutants (`runs/fix_summary.txt`, `runs/probe2_<mutant>.txt`, `runs/eab2_<mutant>.txt`; `variants.py`). Each is
probed with `--seeds 2` (152 fights), and engine_ab runs against the link on Oracle and 7 foes at n=4. The "first
probe" column is `oracle_probe.py` as it stood before this round (`runs/probeprev_*`; that probe is kept as
`runs/oracle_probe_prev.py`, 8654bc7e7e3a3e52):

```
mutant                                                            fixed probe   first probe    engine_ab (112; Oracle's own 28)
[7] rv-charge: the aim adds 0.25 dt to the charge (review)        [7] only      7/7, blind     28 differ
[6] rv-spindir: the aim sets spinDir (review)                     [6] only      7/7, blind     24 differ
[1] mut-winclock: the aim runs the window's clock back 10%        [1] only      7/7, blind     28 differ
[3] mut-cdhit: a window arrow that lands takes 0.05 off fireCd    [3] only      7/7, blind     28 differ
[1] mut-window: the window 1% long (dur x 1.01 at the cast)       [1] only      [1] only       28 differ
[2] mut-nolead: aim at where the foe IS                           [2] only      [2] only       28 differ   (Oracle 98.7%: the design's 97.6%)
[3] mut-cadence: the stream 10% quicker in the window             [3] only      [3] only       28 differ
[4] mut-dmg: the window's arrows 10% harder                       [4] only      [4] only       28 differ
[5] mut-bladehex: the second hex on blade blows too               [5] only      [5] only       25 differ
[6] mut-nudge: the aim nudges the caster (vx += 1e-9)             [6] only      [6] only       28 differ
[7] mut-wait: the cast waits 0.5 past its charge                  [7] only      [7] only       28 differ
control: no turn while stunned (reading 2 the other way)          [2] only                     28 differ
```

Every mutant fails its own check and only that one, and every one changes fights. No count exceeds Oracle's own 28,
every listed difference is an Oracle fight, and each mutated line runs only under Oracle's window or cast. The last row is a control, not a mutant: it prices reading 2 (§2). The probe asserts the
reading, so the control fails [2].

**The rebuilt links play every fight the first build played** (`runs/fix_summary.txt`), so every number measured on
the first links stands for these:
- engine_ab, first build → rebuilt, on Oracle and 7 foes at n=6: 168/168 identical field for field, at stages 2, 3
  and 5 (`runs/eab_oldnew_*`);
- the SHIP runs, both blocks, 33 foes x 20 seeds: every key identical, the win, the casts, the blows and every foe's
  rate (`runs/built2_*` against `runs/built_*`: 82.6 / 84.1, 85.9 / 87.0, 50.8 / 55.5);
- the probe's mechanism lines, identical at all three stages (`runs/probe2_*` against `runs/probe_*`);
- relic_rate on the rebuilt stage 5, both sides, both blocks: identical in every key but the file name to the first
  build's run and to the grid's `--set dmg=10` run (`runs/s5link2_rr_*`);
- engine_ab over the 38 base relics, verify and tip_audit, all run again on the rebuilt link (§4): the same results.

## 4. Stage 5: the blade — 10

Both sides (`relic_rate.py`: each seed played from both sides; every other relic a foe, 10 seeds a foe a side, 760 fights
a block; seed0 2207 and 2317; `--set dmg=X` on `sc-oracle-sight`; `runs/stage5_rr_d*`):

```
blade   block 1   block 2   pooled (1520)   side A   side B   mean fight
 9.5    50.5      47.4      48.9            48.0     49.9     67.4s
10      50.7      48.3      49.5            51.1     47.9     66.5s
10.5    56.2      53.3      54.7            55.5     53.9     65.9s
11      58.7      56.7      57.7            58.2     57.2     64.3s
11.5    59.9      63.0      61.4            61.6     61.3     63.5s
12      66.4      68.2      67.3            68.7     65.9     62.5s
12.5    69.2      69.9      69.5            72.4     66.7     61.5s
```

- **The brief's three points read 61.4 / 67.3 / 69.5, and the crossing is ~10**, under the brief's "expect 11.5-12".
  9.5 and 10 read within a standard error (±1.3) of each other and of 50. For scale, the body alone (stage 1, blade
  16.23, the same runs) reads 34.1 / 34.6, pooled 34.4% (`runs/s1_rr_*`).
- **The brief names no other knob.** Its stage 5 is the blade alone, and its §3 lists the turn as "NOT TO RE-BUY".
  Charge and window are the design's. So nothing else moves, and no measured point inside the band is near 50: the
  nearest, 11.5, reads 61.4. The band is the design's forecast of the crossing ("Crossing near 11.8 ... Expect
  11.5-12", design §4), not a target of its own. **So the blade goes to the measured point nearest 50%, 10 (49.5%).**
- **The miss of the band is the §2 gap**, measured at 10 itself: the no-spin aim +18, the window clock +8, and the
  lab's three constructions put back land on the lab's arm C at 10. It is **said here and left to Rick**.
  - If he wants the band, 11.5 (61.4%) is one number in `TUNED`.
  - 10 is inside the row's range. The bow row's floor is Gloamwire at 9.5 and Farwarden at 12.73 (design §4).
- **The built link is the measured relic:** `relic_rate` on `sc-oracle-b10` with no `--set` reproduces both blocks
  exactly — 50.66% and 48.29%, both sides, the mean duration (66.3805 / 66.5670s), the timeouts and every foe of 38
  (`runs/s5link_rr_*`, and on the rebuilt link `runs/s5link2_rr_*`; `ladder.py same`).
- **The fights are long:** 66.5s at 10, against 55s at 16.23. A bow at the row's floor blade that lands most of its
  arrows in windows.
- **The ladder at 10** (40 fights a foe, `runs/ladder_b10.txt`):
  - by type: bow 57%, greatsword 52, flail 51, scythe 48, warhammer 47, twinblade 40;
  - worst: Gloamwire 15%, Twinshade 20, Dawnbringer 25, Duskreave 27.5, Spellbreaker 30, Shroudmaul 30;
  - best: Vesper 82.5, Redflail 82.5, Heartwood 72.5, Marrowdraw 70, Vinesower 67.5, Farwarden 67.5.
  - The design's (arm C at 12): bow 69, flail 69, greatsword 48, scythe 46, twinblade 45, warhammer 39. The spread
    narrows (17 points by type against 30), and **the brief's "hammers ~39%" reads 47**. The type spread is item
    12/32, Rick's.

- **engine_ab sc-tendril-t3 → sc-oracle-b10, the 38 others, n=6: 4218/4218 identical** (`runs/engine_ab38_2.txt`, on
  the rebuilt link; the first build's `runs/engine_ab38.txt` read the same; 38/38 distinct winners, 4218 distinct
  seeds, 22.7-114.9s). Adding Oracle moves no other fight.
- **verify --n 40 on sc-oracle-b10 (39 relics, 29,640 fights): 11/13** (`runs/verify2_b10.txt`, on the rebuilt link:
  identical to the first build's `runs/verify_b10.txt` but for the wall-clock line).
  - The two reds are the clock bands, red on every link since the minute pace: pairing means 38.3s
    (Ironhail/Marrowdraw) .. 98.4s (Lightkeeper/Starwarden), overall 61.1s (the base's 60.8).
  - Oracle 49.6% (side B in every pairing, as verify plays an appended relic); every relic in 30-70%
    (Heartwood 32.2 .. Gloamwire 66.1). No JS error, every tip present, every pairing resolved, no timeout.
  - The base's third red is green here. sc-tendril-t3's verify (`v101/runs/verify_t3.txt`) had Heartwood 0/40
    against Twinshade and against Bindweed. verify's seed is ONE running LCG over the pairings in roster order, and
    Oracle's pairings, appended to every row, move every later pairing onto other seeds. engine_ab above says no fight
    moved. The counter is Heartwood's (item 12/32), not Oracle's.
- **tip_audit:** identical to sc-tendril-t3's except for the file name (`runs/tip_audit2_b10.txt` on the rebuilt link,
  `runs/tip_audit_base.txt`). The one MISSING line (Burn's `feed`) is the base's.
- **chain_audit** `--builder oracle_build.py`, relic = tip = the rebuilt sc-oracle-b10: **ALL 10 INSERTS SURVIVE**, each
  marker once in the relic (`runs/chain_audit2.txt`). **Control:** the same relic against sc-tendril-t3 as the tip
  **loses all 10** and exits 1 (`runs/chain_audit2_control.txt`). On the first build it lost 9: the aim read "ok"
  there off Tendril's copy of its marker line (`runs/chain_audit_control.txt`), which is what §1's rename fixes.
- **The carry, dry, with the fixed builder** (`runs/carry_dry4.txt`). The builder's four stages apply, parse and pass the
  marker check on each of these, and chain_audit reads all 10 inserts on each carried stage 5:
  - `sc-lodestone-b205-fx` (4568c2995d06f696, the batch line's newest link when this closed, Lodestone's carry;
    `runs/carry_dry5.txt`, with the final builder);
  - `sc-ironhail-fxout` (4b3775e5900172ea; Ironhail's redesign moves the donor's blade, never its profile);
  - `sc-tendril-fx` (Bindweed stage 6, eea0cde5536955b3);
  - `sc-coldiron-temper-fx` (67cc3e6e05d5326e);
  - `sc-ironhail-sunder-fx` (b51c2539999dd272).

  It refuses yert's staff line (`sc-nightglass-fx`, 4d250f8c708ce261), which has no window tickers. The first build's
  dry runs (`runs/carry_dry*.txt`) also covered `sc-onslaught-fx` and the in-flight scratch links of five other builds.
  These were scratch files, not links; the orchestrator's engine_ab proves the carry.

## 5. Stage 6: what it stands on — the state and the line map

The picture and voice labs (§6) built on this (line numbers are the rebuilt `sc-oracle-b10`'s, 72dcd8aa43e5b501;
from line 9808 on they are the first build's + 3, the aim's longer comment):

- **State:**
  - `f.ultSight = {t, dur}` while the window runs, null otherwise. `t` is window-clock seconds; it freezes in a hit stop.
  - `f.sightTally = {casts, frames, foeHex, arrows, hex}`, cumulative over the fight: the probe's count, and nothing in
    the simulation reads it.
  - The ult: `{kind:"sight", charge 14, dur 8, turn 6, hex 1}`. The fields are declared at 7713-7714.
- **Step order** (8840-8846, each fighter): `tickStatus`, `move`, `tickWeapon` (the aim), `tickFire` (the stream),
  `tickCharge` (the cast). Then `tickShots` (8894: arrows land, `resolveHit`), and later `tickSight` (8953, after
  `tickTendril`).
- **The cast** is `fireUlt` (16272). The generic head sets `hitStop` 0.08 (16296), files the `ult` beat (16297), plays
  `SFX.play("ult", {w:"oracle"})` (16299; on stage 5 it falls to the rune-crack `else`, 7435, and stage 6 puts
  Oracle's arm before it) and records `m.ultFx = {kind:"sight", w:"oracle", ...}` (16307) with the default life 1.5.
  The inlined SPECS (`var SPECS`, 32288; the base's 32193) has no `oracle` entry (Oracle is new and retires none), so
  the cast spawns no field and there is no fx_spec text to report. The `kind === "sight"` branch (16675) opens the
  window (`f.ultSight = { t: 0, dur: u.dur }`, 16679) and returns.
- **The aim** is `tickWeapon`'s `else if (f.ultSight)` (9812-9822). The lead is `leadX = foe.x + foe.vx * tof`,
  `leadY = foe.y + foe.vy * tof`, with `tof = |foe - f| / 380`, and `bearing` is the angle to it. That is the rune's
  point: a pure function of state, which the renderer can recompute. In a hit stop the positions hold but `vy` keeps
  earning gravity (the step's frozen path), so a lead recomputed there drifts slightly. The picture should hold the
  last live one.
- **An arrow** leaves in `tickFire` (9896; cadence 9967; `spawnShot` 10036, `this.shots.push` 10046; `SFX.play("loose")`
  10095) along `f.theta`. It lands in `tickShots`' hit branch → `resolveHit(src, foe, ..., s.dmgMul, s.over)` (10455).
  The second hex is 14806-14813 (its comment from 14799, after the onHit loop at 14772; the apply itself is 14810).
- **The close** is `tickSight` (13680; the close is line 13686) on the clock or either death. Nothing marks it after:
  the eye-shut and the 0.3s sigil fade need a presentation-only field set there, as `winnowFade` does. Stage 6 keeps
  its own on the fighter: `foreFade`, eased to 0 over 0.3s after `ultSight` is gone.
- **The silhouette:** Oracle draws through `drawWeapon` (24013) → `litWeapon(c, f.w.shape, reach + 6, f.w.artW, pal,
  f.drawK, a)` (24184; `SHAPES[f.w.shape]` is the fallback at 24185) → `SHAPES.bow` (3169). A bow has no head: the
  shape is the whole weapon. Its `p.key === "runic"` branch (3363) already cuts the limbs into segments held by the
  string and draws a sigil at the grip (3382), turning with `SHAPES._t`: the design's "a recurve etched with a sigil at
  the grip" is on screen before any art row.
- **Where it can draw:** arrows are `drawShots` (25774). The window hooks are the world-pass floor calls (`drawDawn` /
  `drawSun` / `drawTree`, 19361-19372) and the emissive pass after `drawMotes`.
- **Names that are taken:** `drawSigils` / `m.sigils` (Converse), and `"vine"` / `tickVines` (the Thicket).

## 6. Stage 6: the picture and the voice — `sc-oracle-fx`

Picked on measurements under Rick's "you pick i overrule", by two labs run in parallel on `sc-oracle-b10` (the picture
lab's scratch, `or_rows.py`, and `tools/oracle_voice_lab.py`), and built as `oracle_build.py --stage 6`: **eleven
anchored edits (voice 4, picture 7), byte-exact to the labs' own row files** (voice rows 4f3e2656c44f9237, picture rows
72e885b17b2e193e; `runs/stage6_gen_check.txt`, written by the scratch generator `runs/gen_s6.py`, Ironwood's pattern):
- the returned rows equal the files (labels, anchors, modes and the quoted code);
- **the picture rows alone reproduce the picture lab's stamp, 1bdec440699e6fd7 (+16,149 chars)**; the voice rows alone
  reproduce the voice lab's end-to-end page, b65621b4f4847be5 (+6,856); both together write 4e8f47301b97d7d7 (+23,005),
  the voice lab's own interleaving stamp;
- no two rows share an anchor line (11 rows, 11 anchor-line groups), so nothing is merged; no row's anchor sits inside
  another's; voice-then-picture, picture-then-voice and 20 shuffles write the same bytes.

The picture sheet is `05-reference/v105/oracle-picture-sheet.png` (28de9498285c1d0e); the wavs are
`05-reference/v105/oracle-*.wav` (49, gitignored).

```
sc-oracle-b10.html   stage 5                                                    72dcd8aa43e5b501
  -> sc-oracle-fx.html   stage 6  the picture and the voice (+23,005 chars)      4e8f47301b97d7d7
```

`--stage 6` goes on stage 5 once: it refuses a source whose Oracle ult block or blade is not stage 5's, and one that
already carries any of stage 6's names (`tickForesight`, `drawForesight`, `_foreEye`, `foreFade` and the four voice
keys). The anchors, each replaced exactly once:
- **the voice's Sfx arms** go BEFORE the shared rune-crack fallback (`} else {  // rune-crack`), which 12 other relics on
  this link still use; the fallback line is untouched;
- **the sigil's strike** goes after `tickSight`'s last tally line (`T.foeHex += foe.stacks("hex");`), so it plays inside
  a running window and never on the closing frame;
- **the snap** goes after the second hex's own tally line (`T.hex += self.w.ult.hex;`), inside its guard;
- **the close voice** goes before `tickSight`'s close line, which it leaves alone;
- **the picture's fields** go after `this.ultSight = null; this.sightTally = null;` (stage 2's own lines);
- **its tick** after `tickPresentation(dt){ this.tickNovaFx(dt);`; **`tickForesight`** before `tickWinnow(dt){`;
- **the floor call** after `if (__world) this.drawTree(m);`; **the emissive call** after `this.drawShots(m);`;
  **the eye** after Canopy's `this._drawBark(m, f, c);` line in `drawFighter`; **the drawing methods** before
  `drawMotes(m){`.

**The picture** (v75 §6.1; every number is the picture lab's, headless Chromium 151 at 540x960 with the post chain on,
76 frames across 9 fights in 9 states — rest, cast, open, mid, stop, hit, hit2, close, over — the foes white sanctified,
umbral, dwarven, runic and verdant among them):
- **The cast, the rune-eye:** on the caster's glass, a sigil ring in the school's core sweeps round the shell from the
  top, and an eye across the glass opens its lids over 0.25s; the iris looks at the rune. It opens under the engine's own
  "Foresight" banner, which `fireUlt` already places on the caster. **Strokes and no fill:** the health level keeps a
  median 91% of its contrast under the eye (worst 0.55; 491 window frames, caster hp 0.25-0.75, 8 fights), where a dark
  almond kept 83% (28% at worst) and a 38% almond 84% (44%).
- **The rune at the lead:** the bow's grip sigil laid on the floor — a ring and the triangle inside it, turning, r 14,
  the school's glow at 0.5 — at the LEAD the aim turns toward, `foe + v_foe x |foe - f| / 380`. It is re-read only on a
  step the window clock moved (the aim ran on exactly those), so it holds its point through a hit stop as the bow does.
  **The lead is outside the live hall on 67.9% of live window frames** (overshoot median 183 units, p90 557; 24 fights),
  so the rune is drawn where the bow's line to the lead leaves the hall (inset + 16): the bearing the bow turns to is
  kept and the rune stays on the floor, often at a wall or in a corner. It chases that point with a 0.05s time
  constant: unsmoothed, it jumped more than 150 units on 3.2% of frames (about twice a second); at 0.05s on 0.28%, at a
  median lag of 25 units (p90 106); 0.1s had none but lagged 54. The design says it "slides".
- **The sight-line:** thin, from the nock (the reach along the facing, where the arrows leave) to the rune's rim. When
  the bow is on the lead it is the arrows' own path; until then the angle between the line and the bow is the turn still
  to make (the bow sits within turn x dt of the lead on ~39% of window frames, §3).
- **The rune motes** run along the line, nock to rune, placed on the presentation clock (no state, no RNG): the
  design's field, drawn (below).
- **The window arrows:** every one of the caster's arrows in flight while the window is up carries a short core trail
  (drawn from its velocity, like the arrow's own streak) and the grip sigil riding behind the head over a dark disc, so
  it reads as a different arrow at any size. That matches the mechanic: the second hex pays on any shot that lands in
  the window, whenever it was loosed.
- **A landed window arrow:** a rune flare on the foe — the sigil's ring thrown out round the shell and a triangle
  turning in it, over 0.3s, following the foe's live position. A ring and not a disc, so no ball is lit over its own
  body. The arrow's own HEX tag (the channel's onHit tag, printed "HEX") takes the foe's count after both hexes ("HEX
  n"), so **the hex tag ticks by two**, capped at 5. A killing arrow draws no flare and no tag (the shatter owns that
  frame). Both are found by watching `sightTally.arrows` / `.hex` rise: `resolveHit` makes no call for the picture.
- **The close:** the lids meet and the ring and rune fade over 0.3s, on a clock close, on either death and at the
  verdict; eye and rune reach 0 a median 0.29s after a clock close (0.29-0.58s when a hit stop falls inside).
- **The silhouette is left as it is:** Oracle's runic bow reads |dL| 0.123 at the app's size (453x805, 8 frames a
  bow), 4th of the 7 bows (Aureole 0.217, Farwarden 0.187, Vinesower 0.186; Marrowdraw 0.122, Gloamwire 0.099, Ironhail
  0.093 below), and `SHAPES.bow`'s runic branch already draws the design's "sigil at the grip". No row touches
  `SHAPES.bow`.
- **The art hangs off the Fighter** (`fore*` fields: `foreFade`, `foreAge`, `foreOut`, `foreT`, `foreLead`,
  `foreRune`, `foreSeen`, `foreFx`), driven in `tickPresentation` by `tickForesight`, never off `m.ultFx` (open item
  25). The one write outside the fighter is a hex tag's `val`, which only `drawTags` reads. Names are `fore*` /
  `Foresight` because `drawSigils` / `m.sigils` are Converse's; the voice's `"oracle-sigil"` is an SFX key, not either.
- **Bloom:** the picture's share of the arena lift max +0.0005 (min -0.0005; gate +0.02); raw luma added max +0.0034;
  arena clip 0.0163 with, 0.0160 without. **Controls that must fail, and do:** a white-hot halo on the caster pushes its
  disc past 0.90 on 55/63 window frames; the rune as a 200-unit white radial lifts +0.107 (over 0.02 on 22/76 frames);
  the flare as a white disc over the foe pushes the foe's disc past 0.90 on 12/18 flare frames.
- **Discs:** foe art max +0.0103 (+0.0188 with the re-counted tag text); the white sanctified foe past 0.90 on 7 frames
  with the picture and the same 7 without (the body, not the picture); umbral / dwarven / runic / verdant foes max |d|
  0.0078 / 0.0103 / 0.0060 / 0.0074. The caster's own disc: art max +0.065 (the eye's glow strokes), past 0.90 on the
  same 2 frames with and without: lighter, never erased.
- **Legibility** (median |dL|, out of a hit stop / in one): eye 0.158 / 0.160 (closing 0.135 / 0.200), floor rune
  0.164 / 0.164, sight-line 0.143 / 0.136, motes 0.210 / 0.232, arrow rune 0.334 / 0.333, core trail 0.105 / 0.118,
  hit flare 0.370 / 0.315, HEX n tag 0.242 / 0.227. By state: cast 0.117, open 0.181, mid 0.175, stop 0.219, hit
  0.235, hit2 0.243, close 0.141, over 0.190.
- **Frame cost, real GPU** (Electron 44, RTX 3070, interleaved A/B, 3 fights, the machine loaded by the parallel builds
  to 57-89 ms frames): the picture's own calls a median 0.5-0.7 ms (p90 0.7-1.1) in the cast, window, hit and close, 0.0
  at rest; the whole-frame medians with and without the rows sit within the machine's noise (-2.8 to +4.9 ms, both signs).
- **Whole fights drawn** through the kill and 3s of verdict, the post chain alternating: 15 fights, 20,344 draws, 16,701
  with the picture up (2,507 in a hit stop), nothing thrown; 172 window arrows landed, 169 flares (the other 3 killed);
  169 second hexes on a live foe, each leaving the arrow's tag within 3R carrying the foe's count: +2 on 66, capped at 5
  on 101, +3 on 2 (another hex landed in the same step); the rune never left the live hall; the shared weapon row never
  written.

**No `fx.js` field** — the brief's stage 6 and the design's §6.1 ask for "rune motes along the sight-line" as a field
"in both copies". The picture lab measured why a SPECS field cannot be that, on 125 Foresight windows (16 foes x 2
seeds, both sides): a field rides the one `m.ultFx` slot, which Oracle holds for a median 0.67s of the 8s window (7.6%
of its clock); the opponent's cast took the slot first in 20 of 125 windows and it expired in the other 103; and a field
spawns once, at the caster's spot at the cast, while the sight-line's midpoint sits a median 209 units from that point
(p10 74, p90 400; 215 after the first second). So the motes are DRAWN instead, in the world pass along the line, for the
whole window. The inlined SPECS on this base has no `oracle` entry (Oracle is new and retires none), these rows add
none, and neither copy of `fx.js` was touched: **fx_spec NONE.** The Zenith, Canopy and Tendril precedent. **Rick's to
overrule.**

**The voice** (v75 §6.2; `oracle_voice_lab.py`, Chromium 151.0.7922.34, 152 fights and 571 windows on seeds
105701-105702; the controls reproduce the published rune-crack 0.608 / 450 ms, BAR 0.364 / 300 ms and hit@11.6 0.443 /
80 ms; 13 relics fall through to rune-crack on the base, Oracle among them, to within 6e-8):
- **Cast — SIGIL (of 5):** "a rune-eye 'open' — a filtered inhale into a soft chime, 0.4s". Band-passed noise swelling
  for 0.33s (the longest attack a `_sweep` allows), its band climbing 660 -> 6652 Hz so it passes the chime's note at its
  top (x1.27 over the swell, rise 87 ms, no peak more than 2.5 dB over its neighbours: air); 3 ms off its top, the
  chime: the sigil's own note, E7 (2640 Hz), with a faint bar mode at 2.76x, struck as four in-phase strikes over 30 ms
  so it enters in 23 ms and not as a click. Audible 395 ms; -3.2 to -2.4 dB re the blow at dmg 10; worst register 0.65
  (the school's snap). BELL and GLASS (A6) failed: register 0.81 against rune-crack's 1676 Hz partial.
- **Sigil — FLICK (of 9):** "a very quiet sustained shimmer (re-struck, 2-3 kHz band, peak <= 0.15) while it is
  drawn". A held note does not exist in the synth, so `tickSight` re-strikes 2640 Hz on the window's 1st frame and every
  8th after (15 a second), 0.3s a strike at gain 0.001924; 4.5 strikes overlap, a 5.1 dB shimmer at 15 Hz. Steady
  loudest 50 ms +3.0 dB over the bowstring and -9.0 dB under the wall tick (the quietest voice in the fight); +29.4 dB
  over the score in its third-octave (+28.4 at the least); peak 0.0065; 100% of its power in 2-3 kHz; under the score
  0.27s after the close. On the window's clock, so a hit stop holds the strikes as it holds the sigil.
- **Snap — SEMI (of 3):** "a hit: the bow's own arrow voice plus a hex snap; pitch by count". The school's own
  `hex-snap`, every frequency x 2^(step/12) for step 0-4 at counts 1-5, n = the count the foe carries after the second
  hex: 3003 / 3184 / 3377 / 3581 / 3790 Hz measured, within 5 cents; count 1 IS the school's snap (to 3e-8). At least
  +9.2 dB over the blow it lands on, in its own third-octave; worst register 0.63 (the wall tick). The arrow's own hit
  voice and hit beat are the engine's, untouched.
- **Close — FULL (of 8):** "the chime reversed". Every mode of the cast's chime, its fall run backwards as a climb
  re-struck at whole cycles ~11 ms apart (44 strikes of 0.1s), ending where the chime began, cut there. ENV-CORR 0.92
  with the chime's own samples reversed; loudest at 0.75 of its span; audible 325 ms, at the chime's own level. Only on a
  clock close with both fighters alive.
- **Every control failed its gate, as it has to:** TICK, HISS, CLICK, EXHALE and RC-NOW (cast); STEADY, BUZZ, GAP, LOW,
  LOUD, CEILING, HELD, FLUTTER and GAPS (sigil); FLAT, DOWN and BURIED (snap); AGAIN (close).
- **The Sfx row** reproduces each lab candidate through the patched `play()` (worst 9e-8); the other 126 voices are
  unchanged (worst 1e-7); `ult/oracle` is no longer rune-crack. With eight other relics' scratch Sfx rows applied in
  either order, every arm renders alike (worst 1.2e-7).
- **Wiring:** the cast is `fireUlt`'s own `ult`/oracle call; the sigil one plain `SFX.play` in `tickSight` on window
  frames 1, 9, 17 ... read off the window's own clock (`Math.round(Z.t / dt) % 8 === 1`); the snap one `SFX.play` right
  after the second hex, inside its guard (a shot, the caster in its window, the foe alive and not a shade), `n` read
  with `foe.stacks`; the close one guarded `SFX.play` before the close line, `Z.t >= Z.dur && f.alive && foe.alive`:
  never on a death (a caster's death ends the fight; a close after the foe's death belongs to its kill), never once the
  fight is over (`step()` stops calling `tickSight`).
- **The lab's wire run** (152 fights): 152/152 fights identical and every other SFX call identical in order and
  options; 571 casts, 571 cast voices; 62,423 strike frames, 62,423 strikes; 2,253 second hexes, 2,253 snaps (counts
  2: 384, 3: 145, 4: 245, 5: 1,479 — 66% at the cap); 467 clock closes, 467 close voices, none on the 56 death closes
  or the 48 fight-ends. The sim-write control (the foe nudged 1e-9 on a snap) came back 3/152 identical, so the check
  can fail. End to end, the rows applied as text: 76/76 fights identical to the unpatched page, 0 page errors.
- **A real window** (Oracle v Morningstar, 105701): the snaps +8.1 to +12.4 dB over the fight, the cast +6.7, the close
  +19.9 over its first 0.4s; the shimmer over the score for 100% of the window and adding at least 3 dB in its band for
  73% of it. The longest real gap between strikes in a clock window: median 0.258s, max 1.317s (a long hit stop).
- **Cost per call:** cast 0.3-0.4 ms, sigil about 0, snap 0.2 ms, close 1.5-1.7 ms.
- **A toolkit finding, for the orchestrator to record** (CLAUDE.md 4.5 does not say it): `_tone` ramps its gain to
  0.0001 ABSOLUTE, so a strike at gain g falls only 20·log10(g/0.0001) dB over its whole `dur`. At the sigil's first
  level (g about 0.0002) that is about 7 dB: round 1's 1-2.7s strikes piled twenty deep and were heard 1.0-2.5s after
  the close, and round 1's closes, which assumed an 80 dB fall, correlated NEGATIVELY with the literal reversal. Round 2
  (these rows) uses 0.3s strikes and closes built on the actual fall. It affects any very quiet voice in the game.

**Readings declared** (the builder's docstring, 11-15, and the labs' own lists; art and sound are Code's picks):
11. **The rune is the lead the aim turns toward**, re-read only on a step the window clock moved, so it holds through a
    hit stop; drawn where the bow's line to the lead leaves the hall (the lead is outside it on 67.9% of frames), eased
    at 0.05s.
12. **No `fx.js` field**, though the brief says "Field in both copies" (above). Rick's to overrule.
13. **A landed window arrow is seen by `sightTally` rising** (resolveHit makes no call for the picture): a flare on the
    foe, and the arrow's own HEX tag takes the foe's count, so "the hex tag ticks by two". A killing arrow neither flares
    nor re-counts a tag.
14. **The eye is strokes and no fill** (the health level reads through it); it shuts over 0.3s at any close, a death or
    the verdict included.
15. **The sigil's "sustained shimmer" is a note re-struck** on the window's 1st, 9th, 17th ... frame, on the window
    clock, never on the closing frame. "Pitch by count" is the foe's hex count just after the second hex (2-5 in play:
    the channel's own hex lands first, so count 1 never sounds). The close voice plays on a clock close with both alive,
    never on a death. "0.4s" is audible 330-470 ms; "very quiet" is between the bowstring's loudest and half the wall
    tick's quietest while at least +6 dB over the score; "shimmer" is 2-6 dB deep at 4-20 Hz; the cast sits between 0.5x
    and 1.0x the blow (the batch's rule); the close keeps the chime's own level.

The picture lab's own further readings: every arrow of the caster's in flight in the window carries the rune (the second
hex pays on any shot that lands in it); the flare follows the foe's live position; the sight-line leaves the bow at an
angle while the bow is still turning (locked on ~39% of frames).

### 6a. Stage 6's gates — every one able to fail

- **engine_ab sc-oracle-b10 → sc-oracle-fx, ALL 39 WITH Oracle, n=6: 4446/4446 identical** field for field
  (`runs/stage6_engine_ab39.txt`; 39/39 distinct winners, 4446 distinct seeds, 20.3-118.1s; the ids are
  `runs/ids39.txt`). Presentation moves no fight. **Control:** the same gate against `mut6-foevx` (one sim write in the
  picture: `foe.vx += 1e-9` at each flare in `tickForesight`), on Oracle, Grudgebearer, Aureole and Gravemourn at n=6:
  **17/36 differ** (`runs/stage6_engine_ab_control.txt`). The write can only move Oracle's 18 fights.
- **oracle_probe: 9/9** on sc-oracle-fx (`runs/stage6_probe.txt`; 456 fights, Oracle both sides x 38 foes x 6 seeds).
  **Stage 5's numbers hold to the digit:** every line of the stage-5 run (`runs/probe2_b10.txt`) comes back identical
  (3.76 casts a fight; 21.52 / 12.16 blows in / out of windows; 4.03 second hexes a cast; the lock 39.2%; 1,402 clock
  and 147 death closes; 15.0% of window steps frozen; Oracle 49.6%). Two new checks, each switched on by the link
  itself, and a clause on [7]:
  - **[7] the cast files exactly one `ult` beat** (the brief's stage 6: "Beats: cast files `ult`; arrows file as
    ever" — the arrows' one hit beat a blow is [4]'s, unchanged): 1,714 casts, one beat each. On sc-oracle-b10 the
    new probe reads 7/7, identical to stage 5's run but for that clause (`runs/stage6_probe_b10.txt`).
  - **[8] the voice** (on because "oracle-sigil" is in `AC.SFX.play.toString()`):
    - casts: 1,714 cast voices for 1,714 casts, each inside `fireUlt`;
    - the sigil: 184,946 strikes, exactly one on each window's 1st, 9th, 17th ... frame as the probe counts the frames
      itself (1,477,057 window frames), and none on any other frame or on a closing frame;
    - snaps: 6,912 for 6,912 second hexes, each at the count the foe carries just after it (2: 1,096, 3: 468, 4: 690,
      5: 4,658 — 67% at the cap; count 1 never, as the channel's own hex lands first), none on a blade blow or outside a
      window;
    - closes: 1,402 close voices on 1,402 clock closes, and **none on the 147 death closes**;
    - every Oracle voice of the run is accounted for by its event, and each is of kind `ult`. A ward's shatter plays its
      own crit hit voice inside `hurt()`: that is the hit's voice, never counted against these.
  - **[9] the picture** (on because the Match has `tickForesight`):
    - 6,843,602 `tickForesight` calls: none changed a sim field of either fighter or the match (bodies, facing, charge,
      stun, statuses, window, tally, clock, stop, verdict, shots in the air), and none drew the RNG;
    - the eye at 1 on all 3,215,138 presentation ticks of an open window and never rising outside one; no picture state
      on the other fighter;
    - one flare record on each tick a landed window arrow is first seen on a live foe (6,891), none on the 112 killing
      arrows; a fresh HEX tag carrying the foe's count on each of those ticks (6,891: 2: 1,086, 3: 472, 4: 683, 5:
      4,650). Counted per presentation tick, so two arrows landing in one step make one flare, and a foe killed later in
      the step gets none: hence 6,891 here against the 6,912 snaps;
    - the DRAWN subset (the first seed, both sides, every foe: 76 fights, drawn every 6th step while the picture shows):
      55,645 frames through the renderer (50,488 with the picture up, 7,516 of them in a hit stop, 1,497 with the eye
      opening or shutting); none threw, none changed the sim, and each of the 76 drawn fights ends exactly where its
      undrawn replay does.
  - The one-seed run alone (76 fights, all drawn) also reads 9/9 (`runs/stage6_probe_smoke.txt`).
- **The stage-6 mutants** (`runs/stage6_mutant_diffs.txt`, `runs/stage6_probe_mut6-*.txt`): six scratch copies of
  sc-oracle-fx, each one line off, probed at `--seeds 1` (76 fights; the drawn subset only where the mutant is in a
  draw). **Each fails its own check and only that one:**

```
mutant                                                                 probe                 fails
[8] mut6-closedeath: the close voiced on every close, deaths included  [8] only, 8/9           27  (26 death closes + the run's total)
[8] mut6-sigil4: the sigil struck every 4th window frame, not 8th      [8] only, 8/9       31,308  (62,640 strikes for 31,333 due)
[8] mut6-snapn: the snap pitched one count low                         [8] only, 8/9        1,205  (every snap + the run's total)
[9] mut6-foevx: tickForesight nudges the foe 1e-9 at a flare           [9] only, 8/9        1,225  (one a flare; its fights move)
[9] mut6-drawvx: drawForesightTop nudges side A 1e-9 while it shows    [9] only, 8/9       50,960  (drawn frames + drawn fights' ends)
[9] mut6-flarekill: a killing arrow flares too                         [9] only, 8/9           24  (one a killing arrow)
```

  engine_ab sees `mut6-foevx` (17/36 differ, above). It cannot see the other five: `mut6-drawvx` writes only inside a
  draw, which engine_ab never makes, and the voice and flare mutants write nothing the fight reads. That is why [8] and
  [9] read inside the hooks.
- **The builder's own scan** of stage 6's added code (a re-emitted anchor aside, comments stripped): no `rng()`,
  `Math.random`, `spawnFx` or `ultFx`; no call that applies, hurts, heals, beats, resolves, shatters, casts, knocks or
  spawns a shot; and it writes only its own `fore*` fields, the canvas, a tag's count (`val`), a flare record's clock and
  an oscillator's pitch. The stage-1-5 scans (no `w.*` write, no pin, stun or hit stop, no hurt, beat, knock, resolve or
  shatter) run over the S6 inserts too, and chain_audit's marker for each of the 21 inserts is in the output exactly once
  (`runs/build_stage6.txt`). **Controls** (`runs/stage6_builder_controls_final.txt`, each a copy of the final builder
  with one bad line in an S6 row; each refuses and writes nothing): `tickForesight` writing `foe.vx` ("writes foe.vx");
  the presentation call drawing `this.rng()` ("draws the RNG"); the presentation call writing `this.a.theta` ("writes
  a.theta"); the snap row calling `foe.apply` ("calls into the simulation"). Stage 6 also refuses a second write, its own
  output ("'tickForesight' is already in this source"), stage 3 ("stage 6 goes on stage 5") and the base ("needs stage 1
  under it"; `runs/stage6_rebuild_final.txt`).
- **render_ab:** the other relics' pairs (paradox:heartwood:25064, twinshade:lastlight:991, bulwarden:vinesower:70707,
  axiom:grudgebearer:31337) are **24/24 pixel-identical**. **Control:** Oracle v Heartwood 105312 at t = 6 / 16 / 20 /
  31 / 35 / 39.5 (its windows run 15.07-23.78 and 30.38-39.73) is **1/6 identical**: the one identical frame is t = 6,
  before the first cast; all five window frames differ (`runs/stage6_render_ab.txt`).
- **chain_audit** `--builder oracle_build.py`, relic = tip = sc-oracle-fx: **ALL 21 INSERTS SURVIVE**, each marker once
  (`runs/stage6_chain_audit.txt`). **Control:** the same relic against sc-oracle-b10 as the tip **loses all 11 of stage
  6's inserts** (the ten of stages 1-5 read "ok") and exits 1 (`runs/stage6_chain_audit_control.txt`).
- **tip_audit:** identical to sc-oracle-b10's except for the file name (`runs/stage6_tip_audit_fx.txt`); the one
  MISSING line (Burn's `feed`) is the base's.
- **The links rebuild to the byte** from the final builder (ae5d6f4e641a2b16) into a scratch folder: all five,
  sc-oracle through sc-oracle-fx (`runs/stage6_rebuild_final.txt`).
- **The carry, dry** (`runs/carry_dry6.txt`, the final builder): stages 1, 2, 3, 5 and 6 apply, parse and pass the marker
  check on five later links, +23,005 chars at stage 6 on each, and chain_audit reads all 21 inserts on each carried stage
  6:
  - `sc-widowmaker-fxout` (04fdd2e2daa17c26, the batch line's newest link when this closed);
  - `sc-widowmaker-b1075-fx` (94875b2b314c5625);
  - `sc-lodestone-b205-fx` (4568c2995d06f696);
  - `sc-ironhail-fxout` (4b3775e5900172ea);
  - `sc-tendril-fx` (eea0cde5536955b3, Bindweed's stage 6, which shares the rune-crack fallback and the draw-call lines).

  These were scratch files, not links; the orchestrator's engine_ab proves the carry. The picture lab also applied the
  rows on `sc-ironhail-sunder-fx` and with eight other relics' scratch picture rows, and the voice lab its Sfx row with
  eight other relics' Sfx rows, in either order.
- **shell_identity** was not run here: the app's json is shared, and the orchestrator runs it on the carried link.
- **The labs' own gates** (§6 above):
  - picture: bloom share +0.0005 (gate +0.02), with a halo, a radial and a disc control that each fail;
  - picture: 15 whole fights hashed every step, drawn and undrawn identical to the base at the kill, with a 1e-9
    `foe.vx` control that differs on all 13 Oracle fights and on none of the 2 without;
  - picture: 54/54 other-relic render frames identical, with an Oracle control at 1/6;
  - picture: 15 whole fights drawn without a throw;
  - voice: the 152/152 wire run with a sim-write control at 3/152 identical, and 76/76 end to end.

## 7. The clip (Rick's to overrule)

`tools/_oracle_pick.py` (from `_ironwood_pick.py`, by way of `_bindweed_pick.py`) scores a window against v75 §6. Three
things are required: the window must close BY ITS CLOCK with both alive (the only close that shuts the eye to its
reversed chime; a death close is silent and a kill takes the picture), it must land at least one window arrow that
hexes twice, and the fight must run on through the clip's 1.8s tail. Points then come from:
- the window arrows that land (0.35 each, up to 12);
- the hex counts heard (1.0 per distinct count the snaps carry, up to 5: the snap steps a semitone a count, so a window
  that climbs 2-3-4-5 beats one that sits at the cap);
- the rune AT the lead (1.5 x the share of window frames whose lead is inside the hall, so the rune is the prophecy and
  not its clamp at the wall);
- the lock (1.0 x the share of window frames the bow already sits within turn x dt of the lead, so the sight-line is
  the arrows' path).

It ran 12 foes x 6 seeds with Oracle as side A, the side `cinema_clip --a` films (`runs/stage6_pick.txt`). The pick is
**Oracle v Heartwood, seed 105312**:
- the cast lands at 30.38, and the 9.35s window closes by its clock at 39.73 with both alive;
- 9 window arrows land and all 9 hex twice; the snaps carry the counts 2, 3, 4 and 5 (the foe starts the window at 0);
- the lead is inside the hall on 44.8% of its window frames and the bow is locked on 53.1% (over all windows: 32% and
  39%).

The runner-up, Vinesower 105238, scored 0.88 lower: 9 arrows as well, but only the counts 2, 4 and 5.

    python cinema_clip.py --game <scratch>/batch/oracle/links/sc-oracle-fx.html --a oracle --b heartwood \
      --seed 105312 --at 29.18 --window 12.35 --end-at-window --fps 60 --w 540 \
      --out ../07-shorts/v105/foresight-window.mp4

The clip (`runs/stage6_clip_log.txt`, `runs/stage6_clip_aac.txt`):
- 12.37s: 741 frames from 1.2s before the cast to 1.8s past the close; the fight is still on at 41.53 (the kill is at
  72.53);
- 540x960 h264 at 60 fps, AAC 48 kHz stereo, 2,748,787 bytes, sha256[:16] bbd98ccb2179a5f0;
- **AAC mean -22.3 dB, max -1.6 dB.**

The window's events on the match clock (`runs/stage6_clip_events.txt`, `runs/clip_events.py`): the cast at 30.383
(video 1.20); nine second hexes at video 2.16 (n 2), 4.46 (4), 4.55 (5), 5.42 (5), 5.53 (5), 8.66 (3), 8.99 (5), 9.40
(5) and 10.20 (5); the clock close at 39.733 (video 10.55).

**The four voices, read out of the clip's own AAC** (`runs/stage6_clip_tone.txt`, `runs/clip_tone.py`):
- the sigil's E7 line (2640 Hz) stands **+37.1 dB** (video 1.6-5.6) and **+35.0 dB** (5.6-10.5) over the median of its
  2.4-2.9 kHz band inside the window, and -1.0 dB before the cast and -2.3 dB after the close: on for the window, off
  either side;
- the chime's bar mode (2640 x 2.76 = 7286 Hz), which only the cast and the close carry, stands **+25.9 dB** over its
  band at the cast's chime (video 1.45-1.95) and **+44.0 dB** at the close (10.50-11.00), and -1.0 / -8.1 / -9.0 / -6.3
  dB before the cast, mid-window and after the close;
- the snaps lift the mix +4.4 to +9.6 dB RMS (50 ms) over the 150 ms before them.

Five frames, checked through the pipeline (post chain, director; `ffmpeg` tile, scratch `s6/frames/`):
- 1.5s: the "Foresight" banner, the rune-eye open on the caster's glass, the sight-line down to the rune, which stands
  at the bottom wall (the lead beyond the hall, reading 11);
- 2.25s: HEX 2 on the foe and the rune flare round its shell;
- 4.6s: HEX 4 then HEX 5, two flares, a window arrow in flight with its rune;
- 8.75s: HEX 3: three seconds without a landed arrow let the foe's hex (2.6s) run down, and the count climbs again;
- 11.2s: the eye gone, 0.65s after the clock close.
And the close itself at 10.4 / 10.6 / 10.8 / 11.2s: open, open, the lids meeting, gone.

Heartwood casts Rootfast mid-window (the 4.6s frame): its banner and its roots on Oracle share the screen with the eye.
The clip is `07-shorts/v105/foresight-window.mp4` (gitignored). **Rick's to overrule.**

## 8. What is left, and whose

- **Rick:**
  - the blade under the brief's band (10 against 11.5-12), with nothing else moved, because the brief names no knob.
    The gap is the prose's no-spin aim and the engine's window clock, measured at 10 (§2). 11.5 would read 61.4%;
  - reading 2, the aim turning while stunned: the brief's "(the ranged branch)" reads the other way, and the bow held
    while stunned reads 46.6% against the link's 49.5 (about 3 points; §0, §2). If he rules it the other way, the
    relic loses those points and the stage-5 grid runs again on that link (about +0.3 on the blade, by the grid's slope);
  - the card's "each hit hexes twice", where only an arrow does (reading 4; a blade blow in a window hexes once). Keep
    the mechanism and reword the card, or keep the card;
  - the hammers at 47 (the brief's 39) and the type spread (item 12/32);
  - the 66.5s mean fight;
  - the untaken direct aim (98%, design open decision 1);
  - the blurb and every name;
  - **the clip, and the picture and voice picks** (§6, §7);
  - **the drawn rune motes in place of the brief's `fx.js` field** (reading 12; the measurements are in §6);
  - **the rune at the wall:** the lead is outside the hall on two window frames in three, so the rune often stands at a
    wall or in a corner while the foe bounces elsewhere. That is the build's truth, the linear prophecy overshooting
    (the design's own reason direct aim is stronger), not a bug; the clip's first frame shows it;
  - **the E7 shared on purpose** by the cast, the sigil and the close (register 0.85-0.96 among themselves); the
    alternative that passes and ties on register is LOW, an A5 chime;
  - **66% of snaps play the top note** (count 5, the cap), and count 1 never sounds in play;
  - **a hit stop longer than 0.3s silences the shimmer** until the world moves again (the worst clock window had a
    1.317s gap), and in the live app the sigil's strikes meet at arbitrary phase (the same note, a less regular flicker
    than a clip's 120 Hz grid gives);
  - the eye's glow strokes lift the caster's disc up to +0.065 mean luma, never past 0.90; the charge sigil and the
    banner letters have no Oracle entry (the design asks for none; they fall back to the bow's silhouette and the plain
    banner); a HEX tag reads +3 when another hex lands in the same step (2 of 169).
- **The orchestrator (ALL DONE at the carry, §7):**
  - carry the five links onto the batch line's tip with `oracle_build.py --src <tip>`, one relic at a time (stages 1, 2,
    3, 5, 6), and prove each with engine_ab; the builder refuses a carry on which chain_audit could not watch one of its
    21 inserts;
  - **run `oracle_probe.py --game <the carried stage-6 link>` on the carry (9/9)** and chain_audit with `--builder
    oracle_build.py` against every later tip: the probe reads the mechanism, the voice and the picture inside the hooks;
    chain_audit only proves the inserts' lines are still there;
  - run shell_identity on the carried link (not run here: the app's json is shared);
  - send the clip to Rick (one clip per ultimate); record the `_tone` finding (§6) in CLAUDE.md 4.5 if it agrees;
  - the brief's stage 6 also says "Move `GAME`": not this build's to touch (yert's staff row is the build of record
    now); `app/main.js` moves only when Rick has nothing to overrule on the batch's clips.
- **Stage 6:** done. Nothing of it waits on the build; what remains is Rick's eye and ear. The brief's "one fight
  watched" is MEASURED here, not watched: the picture lab drew 15 whole fights through the kill and the verdict, and
  the probe drew 76, none throwing and none writing the sim; the clip is the window, not a whole fight.
- **Standing, not this build's:** the two verify clock bands (every link's since the minute pace); Heartwood's 0/40
  pairings on the base's verify (item 12/32).

## 7. The carry onto the chain

Built and gated in scratch on `sc-tendril-t3`, then carried onto the batch line after Widowmaker's redesign with the
same builder, one stage at a time (`--src` the previous link):

```
sc-widowmaker-fxout.html           the batch line's tip (Widowmaker's redesign)   04fdd2e2daa17c26
  -> sc-oracle.html                  stage 1                                  5062f06b97b11fa5
  -> sc-oracle-aim.html              stage 2                                  84cc63d90bfdbb6b
  -> sc-oracle-sight.html            stage 3                                  88d398ce0a98766f
  -> sc-oracle-b10.html              stage 5                                  cfd7c8e507d21f10
  -> sc-oracle-fx.html               stage 6                                  15cf62f96f72653a
```

**The carry is proven two ways**, because the scratch base is older than the tip:
- **scratch A/B** -- the scratch stage-6 link against the carried one, every id of the scratch build
  but Ironhail and Widowmaker (both redesigned on the chain since), n=6: **3996/3996 identical**
  (`runs/carry_engine_ab.txt`);
- **tip A/B** -- the tip `sc-widowmaker-fxout` against the carried stage-6 link, every relic on the tip
  (40), n=6: **4680/4680 identical** (`runs/carry_engine_ab_tip.txt`): Oracle moves no other relic's
  fight on the batch line, the redesigns and the relics carried since included.

**Gates on the carried stage-6 link** (`runs/carry/`):
- engine_ab stage 5 -> stage 6 over all 41 relics on this tip, Oracle included, n=6: **4920/4920
  identical** (`engine_ab_s6.txt`);
- `oracle_probe.py` **9/9** on the carried link, [the stage-6 checks] on (`probe_fx.txt`) -- the
  probe met every relic carried since its scratch base (Coldiron's Temper, Ironhail's hail, Lodestone's
  walls, Widowmaker's drain) and needed no change;
- tip_audit exit 0; yert's staff carry, dry run onto this link: all stages hold (`staff_carry_dry.txt`);
- **shell_identity 195/195** (app Chromium 152 vs headless 151; the pointer not moved, the json
  restored).

The clip stays the scratch one (`07-shorts/v105/foresight-window.mp4`): Oracle v Heartwood 105312 is inside the scratch A/B (neither relic moved),
so the carried fight is the filmed one.

**The roster is 41 on the batch line.**
