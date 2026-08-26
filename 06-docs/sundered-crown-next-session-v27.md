# Next session — v27

**2026-08-16.** The session that picked a lane and rebuilt the front of the
video. Rick chose **the channel as the product in its own right**; the game
front is parked. Everything below serves shorts.

Built from `sc-seed-v26.zip`. New chain tip candidate `sc-cardspin.html`
`ec9b8d753235385d`, from `sc-ember.html` `6e73c5776cdee56a`, one anchor.
`01-live/sundered-crown.html` `51c9bf566f9eb679` untouched.

---

# 0. The one command

```
python3 shorts_build.py --game ../02-chain/sc-cardspin.html \
        --a axiom --b nightfell --seed 20260816 --cold-open
```

Capture → cold open → hook VO → mix → measure, in one call. The VO is generated
inside the pipeline; `--vo` is now optional.

Last run: cold open ended at sim 1.35s on the first clank; 1080x1920 h264+aac,
63.5s, 25.7 MB, **-15.8 LUFS / -4.2 dBTP**, limiter 0.5. Four of five gates
pass. The one failure is `under 60s`, and it is **the seed, not the pipeline** —
20260816 is a 54.19s fight picked by hand for visual tests, well outside
`pick.py`'s 28–44s band. Re-run through `pick` and it lands.

---

# 1. What changed, and why

## 1a. The cold open — `render.py`, `cinema_clip.py`

The retention problem was not the seed distribution. `CONFIG.intro.dur` is 4.0s
and every short ships `--intro`, so **the video's time-to-first-hit is 4.0 plus
the sim's**:

```
                              card   sim tFirst   in the VIDEO
seed 2072567088                4.0        9.10         13.10s
population median              4.0        2.02          6.02s
best seed measured             4.0        1.82          5.82s
```

Selection can buy 7.3s off the sim clock and still cannot put a hit on screen
before ~5.8s, because the first four are a card. Cross-checked against real
output: short-4 was a 22.6s match that became a **31.3s video** — 8.7s of cards,
28% of the file.

**The fix cost a reordering, not a feature.** `Match.step()` returns early while
`introT > 0`, and `Renderer.drawIntro()` paints over `this.draw(m)` — the match
*as it stands*, not one pinned at t=0. So the card can be raised mid-match: the
fight freezes, the card plays over the live picture, and the fight resumes on
the identical frame. Falsified before use (`coldopen2.py`):

```
[1] straight-through and late-card summarise identically   Thornwake 110hp 30.68s
[2] control — card over a genuinely frozen t=0 scene       0.000
    the same bands with the card raised at t=6.0           0.703
    predicted from the 0.80 scrim (bare 3.749 x 0.20)      0.750
[3] the frame after the card equals the frame before it    0.000
```

**Where the cut goes is measured, not chosen.** The card's own first beat is a
clank at 0.46s — two cards colliding. Raise it on the fight's first clank and
the two impacts become one. Across 144 matches (6 pairings x 24 seeds):

```
first CLANK       median 3.18s   p25 1.78   p75 4.58   p90 7.78   max 18.18
first landed HIT  median 3.44s   p25 1.84   p75 5.12   p90 7.53   max 16.88
```

A fixed timer would cut mid-approach: only 17% have clanked by 1.5s, 48% by
3.0s. So the anchor is the event and the clock is only a cap.

`render.py` needed audio remapping — `renderAudio` shifted every event by the
card length, correct only when the card is first. Each event now carries the
`introT` it fired under, so the three regions (pre-cut fight, the card's own
clank and bell, post-cut fight) can be told apart. **`cinema_clip.py` needed
none of this**: it stamps events at WALL time, which keeps advancing under the
card, so the mix already lines up.

**Rick accepted a known defect.** At the cut, `_introScene` drops `drawHud` and
`drawFooter` in one frame and the scrim snaps to 80%, giving ~0.46s of
near-black before the cards arrive. Correct when the card was first (nothing to
lose), a hard blackout when it is late. Rick: "ok with how it is now" — it reads
as an impact beat. Fixing it means patching `drawIntro` and moving the tip hash.

## 1b. Late seeds are rejected at selection — `pick.py`

The cap inside the renderer can only cut mid-approach, which is the thing Rick
does not want. So the real fix is one step earlier: **do not pick that seed.**
`pick.py` now runs a second early-exit pass per seed recording first clank and
first hit, rejects anything past `--max-open` (default 6.0s), and rewards an
open inside 1.8s. On axiom v nightfell, 150 seeds at a 4.0s cap: **12 rejected.**

A flag bug was caught on read — `main()` never passed `max_open` to `scan()`, so
the CLI option did nothing. Fixed before the run.

`ultscan.py` has the same blind spot and has NOT been given the same treatment.

## 1c. The card art turns — `cardspin_build.py`

`spin` is already per-relic data, so the card art is driven from the relic's own
rate: the card now shows the SWING SPEED it prints two rows below. It flies in
1.30 rad off the reading angle and is **arrested exactly on the reading angle at
the clash**, then sways ±0.45 rad at `spin x 0.22`.

Shipped settings (S45): `--sweep 1.30 --sway 0.45 --sway-rate 0.22`.
`engine_ab` 180/180 identical; presentation only.

## 1d. The opening hook — `cinema_vo.py`, `shorts_build.py`

```
"Who wins?"  ·0.38s·  "Axiom,"  ·0.14s·  "or Nightfell."     bm_lewis
```

Both pauses are **real silence between separate clips**, because punctuation
does not control Kokoro's timing — `?...`, `? ...` and `.` all produce the same
contour, measured.

`bm_lewis` replaces `am_onyx`. Onyx won the earlier sweep on depth alone and is
the flattest of the deep voices, which is the "not engaging" Rick heard. Kokoro
has no emotion control, so pitch movement IS the delivery:

```
voice          f0 Hz   pitch IQR   total
bm_lewis          85       5.5st   2.57s   <- deeper AND 1.5x the movement
bm_fable          86      14.5st   3.57s   theatrical; magnitude may be tracker error
am_onyx           89       3.7st   2.73s   previous
am_echo          103       6.6st   2.98s
am_michael       117       2.8st   2.56s   flattest — included as control
```

**Names are read from the build, not title-cased from the id.** `oathwound`
displays as **Goreshard**; verified end-to-end (ids `oathwound`/`censer` produce
"Who wins? Goreshard... or Censer.").

The hook is generated **before** the mix, feeding `shorts_build.py`'s existing
ceiling ladder. That preserves the tool's law — *never patch a mix, re-capture*
— which `hook_vo.py` breaks by construction. **`hook_vo.py` is for one-off
experiments only and is not the shipping path.**

---

# 2. Wrong turns, recorded honestly

**Three probes failed for the wrong reason before one failed for the right one.**

1. **Cold-open check [2]**, floor of 3.0 pulled out of the air, compared whole
   card frames. The cards cover ~70% of the frame and the scrim passes 20% of
   the scene, so a live scene that moves 5.79 bare shows as 0.35 globally. The
   floor rejected a true hypothesis. Fixed by measuring only card-free bands and
   deriving the expected value from `globalAlpha`.

2. **Card-art fit.** First version fitted the art to its circumscribed radius so
   any angle was safe — **-48%** on `axiom`, `nightfell`, `lightkeeper`. Then the
   arithmetic showed v3 already extends past `artH` at its own -0.38 pose, so the
   250x148 band is a layout hint and not a clip: I had invented a constraint the
   shipped card does not honour. Scale reverted to v3's; the ANGLE is bounded
   instead.

3. **Edge-ink probe** failed at 158 vs a 150 limit. Resolved by side: left and
   right read **8 at every phase** — the art never approaches them. The 158 was
   the bottom edge mid-entry, with card B still in flight. `introfit_probe.py`
   excludes entrance phases for exactly this reason and mine did not.

4. **Voice sweep "question falls" column — discard it.** All twelve voices fall
   on "Who wins?" because *wh*-questions fall in English. Rising would be wrong.
   The metric assumed all questions rise.

5. **Continuous card rotation is blocked** and the measurement is incomplete.
   T18/T30/TC60/TC85 all put ink at y=293 against a 290 limit while the v3
   control sat at 252 — but 293 is the crop floor, so they are **clamped and the
   true extent is unknown**. Redo with a taller search region before pursuing.

Also caught by a probe rather than by reading: `I.clash` is `drawIntro`'s local
and is not in scope inside `_introCard`. Now `CONFIG.intro.clash`.

---

# 3. Files

**Patched:** `render.py` (`--cold-open`), `pick.py` (`--max-open`),
`cinema_clip.py` (`--cold-open`), `shorts_build.py` (auto-VO, `--cold-open`,
`--vo-vol`, `--voice`, `--gap`, `--name-gap`), `cinema_vo.py` (`bm_lewis`
default, `--voice`, `--parts`/`--gaps`).

**New:** `cardspin_build.py`, `hook_vo.py`, `coldopen2.py`, `firstbeat.py`,
`spin_probe.py`, `spin_shot.py`, `edge_side.py`, `sweep_shot.py`.

**Not in the seed:** `kokoro-v1.0.onnx` (325 MB) and `voices-v1.0.bin` (28 MB),
pulled from GitHub releases. Re-fetch, do not ship in the zip.

**Chain cleanup:** eight sweep builds (`sc-spin-0.52` … `-TC85`) deleted.

---

# 4. Carried forward, untouched

- `cineScore` **cannot film an ultimate** — the `ult` beat maxes at 0.90 against
  a 1.90 floor. Every set-piece so far played at plain speed. For a showcase
  channel this is backwards.
- `cineScore` scores spikes against a fight's own baseline, so **front-loaded
  fights and cinematic fights are anti-correlated**. Fixing retention costs the
  cuts until the scoring changes.
- `cineSpill` eats the second fighter's HUD during every cut, in all seven
  shipped shorts.
- Capture is not bit-reproducible (shake jitter, synth noise); true peak moves
  ~1 dB between renders.
- `SPOKEN` in `cinema_vo.py` covers 5 of 17 names. `Slagheart`, `Emberedge`,
  `Heartwood`, `Nightfell`, `Goreshard` are untested compounds.
- Audio still ~1.8 dB under the platform norm at best; the ladder ran three
  rungs deep on the last build and it is not known whether the louder VO caused
  it.
- Game front parked: no persistence, no stakes, no reason to return. Deliberate.

---

# 5. Open decisions

1. **Promote `sc-cardspin.html` `ec9b8d753235385d` to the chain tip of record?**
   The whole pipeline now films it and nothing points at it.
2. **Re-run the final test on a `pick`-selected seed** inside the 28–44s band,
   so the `under 60s` gate passes on a real candidate.
3. **Is `--vo-vol 2.0` right in this chain?** The +6 dB Rick approved was
   measured in `hook_vo.py`'s -19.5 LUFS chain with no limiter; `shorts_build`
   targets -14 with an alimiter, so the number does not transfer and must be
   re-measured by ear.
4. **Did the louder VO drive the ceiling ladder three rungs deep**, or was it
   this fight's ult density? Check before batching.
5. **Give `ultscan.py` the `max_open` treatment**, so late openers cannot reach
   a render by the other path.
6. **`cineScore` ult path at its own lower bar** — deferred twice now. It is the
   single largest gap between what the channel promises and what it films.
