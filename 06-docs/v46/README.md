# v46 — THE IGNITION OPEN. A fight now starts as a shot.

**2026-08-29.** Rick watched `05-reference/v46-ignition/ignition-open-both-solo.mp4`
— the "both" variant out of `tools/ignition_lab.py`, one of four the lab
rendered off one seed — and said *"lets make it happen capn"*. This is that,
moved out of the lab's capture-time monkey patches and into the build.

```
02-chain/sc-paradox-ignition.html   <- THE BUILD OF RECORD
built off 02-chain/sc-paradox-crucible.html by tools/ignition_build.py
src/render/open.js                  <- the module, inlined byte for byte
tools/ignition_probe.py             <- the picture, measured, 11/11
01-live UNTOUCHED, still on sixteen, still not a target
```

---

## 1. WHAT SHIPPED

The first **2.83 seconds** of every fight are now a shot, in three parts, all
of them a pure function of `m.t`. (2.35s as first approved; §6.6 is the word
that bought the other 0.48s.)

| | |
|---|---|
| **the camera** | fighter A at 2.25x easing to 2.02x, a hard cut at 1.33s to fighter B, then a pull wide from 2.03s to 2.83s |
| **the ignition** | A flares at 0.10s and B at 1.43s — each 0.10s after the cut to it, which is the whole difference between "both" and the ignition-only variant — each in its own affinity palette: a white core strike for three frames, an expanding ring, a corona that overshoots and settles, 0.90s each |
| **the swell** | every `shadowBlur` in the hall powers on: 0.30 -> overshoot 1.42 -> exactly 1.0 over 0.95s |

Then it hands the lens back and the build is, frame for frame, the build it was
made from.

**Four hooks, all in `Renderer.draw`, all one line.** The numbers live in
`SWBOpen.LOOK` in the module, not in the builder's glue — `post_build.py`'s
rule, for the reason it states: a second copy of "which opening" in the glue is
how a build ships something nobody picked.

---

## 2. THE THREE DECISIONS THAT ARE NOT THE LAB'S

### 2.1 THE CLOCK IS SIM TIME, AND THE LAB'S WAS WALL TIME

The lab was right to use wall time and this would be wrong to. During the
opening there are no cuts, so `CINE.timeScale` is 1 and the two clocks are the
same number — inside a five-second capture harness. In the build they are not
interchangeable, for three reasons the lab never had to face:

1. **The post chain draws every frame four times** (readouts, emissive, world,
   composite). A pure function of `m.t` is idempotent; a wall-clock one would
   advance four times per frame. This project has paid for that lesson twice —
   `post_build.py`'s camera shake, which presented as juddering **physics**,
   and `fx.js`, which is aged off `ultFx.t` for exactly this reason.
2. **The app's rAF and the capture's fixed cadence must agree.** A dropped
   frame in the app is then fewer samples of the same shot, not a different
   shot, and the mp4 is byte-identical either way.
3. **No `Math.random` anywhere.** The handheld drift is the engine's own
   two-frequency formula from `CINE.update`, evaluated at `m.t`.

Check 10 of the probe is the receipt: a frame drawn three times at one sim time
is one frame, hash for hash.

### 2.2 THE FLARE IS DRAWN OVER THE COMPOSITE, SO IT DOES NOT BLOOM

`fx_build.py` hooks inside `drawUltOver` **precisely so its fields reach the
bloom.** This hooks after `POSTFX.frame` for the opposite reason: the flare
Rick approved was drawn after the composite in the lab, so it is unbloomed, and
that is what was approved.

It is also the safer of the two. `CLAUDE.md` §4.1b and §4.1c are both about
white art handed to this chain — a radial gradient from `#FFFFFF` centred on a
body already at 0.892 luma did not light the ball, it **erased** it. The flare's
core is `#FFFFFF` at 0.95 alpha. Putting it in the emissive pass would be that
mistake a third time, on purpose.

### 2.3 THE SUBJECT-FIT CLAMP — THE ONE THING ADDED TO THE LOOK

`Renderer.draw`'s feasibility clamp — both relics' magnified bodies must fit
the usable frame — is **why an opening shot could not exist before**: at spawn
separation (~503 su) it pulls any asked zoom back to ~1.0. The opening stands
it down for its 2.83s, exactly as the lab's `__openShot` gate did.

But that clamp was bought with a probe that found **8/8 wall-adjacent
set-pieces clipping relic body, by 137–376px**, and standing it down gives that
guarantee up. Measured, with only the lean clamp the lab had:

```
worst subject margin, swept over 12 pairings x the whole opening
    -12.5px   spellbreaker v twinshade, 0.74s, subject A
     -4.5px   ironhail v oathwound (the approved seed), 1.4s, subject B
```

Small — 4px of a 1625px design frame is under two device pixels at 540 wide —
but it is the ball being cut, and inside a shot that has to hold its zoom the
renderer's usual answer (pull back) is not available. So the opening
re-establishes the guarantee for **the one relic being filmed**, with the same
solve and the same precedence the renderer uses for a cut: the subject-fit
clamp wins over the lean clamp.

> **AND IT COSTS ALMOST NOTHING OF WHAT WAS APPROVED.** On the approved seed it
> moves the camera on **1 of 115 samples, by 4.4px** — 2.2px at the delivery
> width. Swept over 24 pairings afterwards, the worst margin is +0.0px: the
> clamp binding, which is what it is for.

---

## 3. WHAT IT DOES NOT DO, AND ONE OF THEM IS A QUESTION FOR RICK

**THE SOUND OF IT IS THE ANNOUNCER — see §6.** This section used to say the
opening was silent and that a sound would be offered as a spread. It was, he
answered, and the answer was better than the question.

**A DIRECTOR CUT INSIDE THE OPENING LOSES THE CAMERA.** Measured: `cinePlan`
schedules a first cut before 2.83s on **2 of 120 pairings (1.7%)**, at 1.62s
and 1.64s. The opening wins those — the cut still runs, its time dilation and
its audio duck still apply, and the lens is handed back mid-cut. It is rare
enough to leave alone and it is now a number rather than a hope.

**AND IT ONLY REACHES A SHORT THAT STARTS AT ZERO** — which, this section said
when it was written, implied shorts do not. **They do, by default.** Corrected
in §6.7 off the code: `shorts_build.py --lead` defaults to None and hands
`cinema_clip` `--full`. The live question is length, not placement.

---

## 4. THE VERIFICATION

```
IS IT THE SAME OPENING?     18/19    PIXEL-IDENTICAL to the lab's own
                                     implementation at identical clocks -- §4.1
ignition_probe.py            11/11   the picture, one check per sentence
engine_ab.py --n 10         150/150  identical field for field, 6 relics
render_ab.py  after release  20/20   PIXEL-IDENTICAL at 3,6,12,22,31s
render_ab.py  in the window  12/16   DIFFERS at 0.3/1.0/2.0s, identical at
                                     2.34s -- which is after the shot releases
post_identity.py             PASS    325,708 px identical, max delta 0
chain_audit.py               PASS    fx, post and this builder's inserts all
                                     survive to the tip
verify.py --n 40             12/13   the same 12/13 as the tip it was built
                                     from, and the same FAIL: Lightkeeper/
                                     Farwarden 74.6s against a 70s pairing
                                     ceiling. Winrate spread 14.9pp, overall
                                     mean 48.8s, 0/12000 timeouts -- every
                                     number unmoved. See §0.
```

### 4.1 THE ONE THAT MATTERS: IS IT THE SAME OPENING?

Everything above says the build is sound. Only one measurement says it is the
picture **Rick approved**, and the first attempt at it was misleading.

Rendering the lab's `both` off the old tip and the build's own opening off the
new one, through the same 60fps harness, and diffing 324 frames:

```
identical frames 131/324, mean |delta| 1.43/255, worst 7.10 at t=0.22s
```

That reads like a real difference and it is not one. **The lab harness
evaluates the opening one frame BEHIND the sim**: `_sub()` steps the match to
frame *i+1* and then calls the driver with `this.wall`, which is still frame
*i*. The build evaluates at the sim time of the frame being drawn. Shifting the
comparison by a frame in either direction makes it worse (2.82 -> 4.28 and
5.72), which is what says the alignment is right and the offset is inside the
16.7ms.

So the two were put side by side with the clock removed as a variable — same
page, same match, same sim state, same rasteriser, `m.shake` pinned — the build's
`SWBOpen` against the lab's driver at **identical** clock values:

```
t     0.00  0.05  0.10  0.14  0.20  0.30  0.50  0.70  0.85  0.86
      0.95  1.00  1.20  1.54  1.56  1.80  2.00  2.20      max |delta| 0
t     2.34                                    mean 0.0786, 1.14% of frame
```

**Eighteen of nineteen instants are byte-for-byte identical**, including every
flare frame, both seams and the whole pull. The nineteenth is the last 10ms:
the module hands the lens back once `z <= 1.02`, where the lab left `CINE.zoom`
at 1.0005 and let the renderer's own branch run one more frame at a zoom of
five ten-thousandths. The build's version is the cleaner of the two.

`tools/out-ignition/` holds both renders. The still-frame A/B was a throwaway;
its result is this section.

**`engine_ab` coming back identical is necessary and proves nothing about the
picture** — `Fighter`, `Match` and `Sfx` contain no reference to a canvas,
which is exactly why a renderer change returns 150/150 whether it was harmless
or a disaster. That is what `ignition_probe.py` is for, and why every one of
its checks is about pixels or about the transform that makes them.

Two of its checks earned their place by failing first:

- **check 3** asserted the subject was at frame centre and found it 467px away.
  It was not a bug: the LEAN clamp binds on 45 of 115 samples, and the same
  clamp, at the same overscan, is in the approved clip. The check was measuring
  an intention rather than a property. It now measures the property that
  matters — the subject is not cropped — and it swept the roster to find the
  −12.5px in §2.3, which one seed would never have shown.
- **check 7** read the swell's dimming as a missing flare. Switching the whole
  module off changes the camera, the flare and the swell at once. Suppressing
  **one contributor at a time** (`CLAUDE.md` §4.1c) separates them: the flare
  puts **+0.1206** luma on relic A's own disc, and the swell puts **−0.0030**
  at 0.07s and **+0.0039** at 0.30s.

---

## 5. THE APP POINTER WAS STALE, AND IT IS NOT ANY MORE

`app/main.js` still read `02-chain/sc-paradox-arc.html` — one build behind, so
the app has been showing a game **without** the Crucible true-stun change since
that shipped. It is now on `sc-paradox-ignition.html`.

`docs/ARCHITECTURE.md` §1's guarantee is that the app cannot show Rick
something the mp4 will not, and a pointer nobody moves is the quiet way that
guarantee stops being true. It is one line in one file and it needs to move in
the same commit as every future build of record.

---

## 6. THE SOUND OF IT IS THE ANNOUNCER

Asked what the flare should sound like, Rick said: *"i think sound should be
the announcer. does that sound right to you?"*

It was a better question than the one he was asked. §3 of this document, as
first written, was looking for a WebAudio strike to go under the flare. The
announcer already existed — `cinema_vo.py`, `bm_lewis`, chosen on a measured
f0/IQR sweep — and he had already decided where it goes, on 2026-08-28: *"the
announcer has to be at the start of the fight. it doesnt make sense anywhere
else."*

**What it never had was a picture built to its shape.** Its home was the 4.0s
intro card; the card was retired for losing 71–75% of the audience present when
it appeared; the line kept the card's pacing and played at 0.0 over whatever
the fight happened to be doing. `docs/APP-FEATURES-BRIEF.md` §1 is the record.

### 6.1 WHAT THE SHIPPED LINE WAS ACTUALLY DOING

Measured against the new opening, ironhail v goreshard:

```
0.10s   IRONHAIL ignites
0.95s   GORESHARD ignites
1.18s   "Ironhail,"        1.08s after its own flare -- and 0.23s after the OTHER
2.19s   "or Goreshard."    1.24s late, over the pull wide
3.17s   the line ends      past the end of the shot and past the first clank
```

**Every name was being spoken over the wrong relic.** Not an argument against
his instinct — the strongest possible argument for it.

### 6.2 THE SPREAD, AND ARM C

Three arms over the same 5.4s of the build's own opening. One line, one voice,
only the timing moving — the same shape as the placement spread he answered in
August, and the shape `06-docs/v43` says lands a sound in one round trip.

| arm | | |
|---|---|---|
| A | as it ships | the control; names 1.08s and 1.24s late |
| B | names on the flares | `Ironhail,` 0.10 · `Goreshard.` 0.97 |
| **C** | **names, then the question** | **B, plus `Who wins?` at 1.95 on the pull** |

**"go c".** So the question stops being the opener and becomes the button,
landing as the hall opens and the first clank arrives at 2.22s.

### 6.3 THE PART THAT IS ENGINEERING, NOT COPY

> **A GAP THAT SYNCS ONE PAIRING MIS-SYNCS THE NEXT.** The line used to be
> parts joined by two constant gaps. The flares are at fixed times and the
> names are not a fixed length — across the roster they run 0.69s to 1.00s, a
> spread of 0.31s — so constants cannot put two different names on two fixed
> beats. The parts are now placed at **absolute onsets**.

Three consequences, all of them the point:

1. **The onsets are READ OUT OF `src/render/open.js`** (`ignition_beats()`),
   never copied into the audio tool. One source of truth, and it fails loudly
   if the pattern stops matching rather than falling back to constants — a line
   silently timed to numbers that no longer match the picture is the exact
   defect this change exists to remove.
2. **The lead silence is baked into the wav**, so every consumer places the
   file at 0.0 and gets the sync for free. `shorts_build.py --vo-at` was
   already 0.0. `cinema_clip.py --vo-at` was still **0.3** — the same
   inherited "after the card is up" 300ms, which for five sessions waited for
   nothing and now actively pushed every name late. It is 0.0.
3. **The box syntax grew `@`.** `|0.38` is a pause; `|@1.95` is an onset. The
   app hands its textarea straight to `--script`, so `--print-hook-script` →
   textarea → render must come back byte-identical to `--hook`, and it does:
   both wavs hash `01d91524ca3366f1`.

### 6.4 THE NAMES DO NOT ALL FIT, AND THE NUMBER IS 0.15s

`tools/vo_sync_probe.py`, all 25 relics, both spoken forms:

```
the stagger between the flares            0.85s
first names longer than it                11/25   worst Emberedge 1.00s
the SECOND NAME lands late by (worst)     0.15s   nine frames at 60fps
the QUESTION lands late by (worst)        0.14s
                                          PASS against a stated 0.20s bar
```

A part that overruns its onset is **delayed, never overlapped and never
clipped**, and the drift is printed on every single render. Fifty renders
cover all 300 pairings, because the second name's drift depends only on the
first name's length and the question's only on the second's.

The fix, if 0.15s ever turns out to be visible, is `flareB` in `open.js` — one
number, and a change to a look Rick approved, so it is his and not this file's.

### 6.5 WHAT IS STILL OPEN

**The app's ignition is still silent**, because the engine has no sound files
by design (§1: *"fully synthesized in WebAudio. There are no sound files."*).
The announcer lives in the clip's mix, as all voiceover does. If the app should
have an ignition you can hear, that is a separate and much smaller thing — a
synthesized strike under the voice — and it was not asked for.

### 6.6 AND THEN THE "or" CAME BACK, WHICH COST 0.48s OF OPENING

Rick, on arm C as shipped: *"can we make the ignition last just a bit longer to
fit in the or so it can still say Ironhail OR goreshard. who wins?"*

**The conjunction cannot go where it reads like it should.** Written
`["<A>,", "or <B>.", "Who wins?"]` — the obvious way — the second part is placed
on flareB, so the flare lights on the word "or" and the name arrives 0.4s
afterwards. The name is the thing that has to hit the light.

So it hangs off the END of the first part: `["<A>, or", "<B>.", "Who wins?"]`.
Both names still start exactly on their own ignitions and the conjunction fills
the gap between them — which now has to be big enough to hold it.

**Measured across all 25 relics**, because the room has to fit the worst one:

```
"<name>, or"      worst 1.33s (Ironhail)   median 1.22s   min 1.00s (Aureole)
the "or" costs    a mean 0.37s -- much more than the word, it carries a
                  trailing beat, which is exactly what a "<A>, or ... <B>" wants
so flareB >=      0.10 + 1.33 = 1.43s for EVERY pairing to land exactly
```

Shot 1 grows by that 0.48s; shots 2 and 3 keep their own lengths and slide, so
the relationship Rick approved — **each relic ignites 0.10s after the cut to
it** — is untouched. The question stays at pull + 0.40 and lands at 2.43,
which is exactly where the longest possible second name ends.

| | before the "or" | after |
|---|---|---|
| opening | 2.35s | **2.83s** |
| cut to B | 0.85s | 1.33s |
| flareB | 0.95s | 1.43s |
| the question | 1.95s | 2.43s |
| names that miss their flare | 11 of 25, worst 0.15s | **0 of 25, worst 0.00s** |

The extra room did not just fit a word — it removed the drift entirely. Every
relic in the roster now starts its name on its own light, exactly.

> **AND THE PROBE PASSED FOR THE WRONG REASON FIRST.** `vo_sync_probe.py` built
> the spoken forms itself (`f"{n},"`), so when the parts grew an "or" it went on
> timing the bare name and reported 0.00s drift on **a string the tool no longer
> says**. It now takes its forms from `cinema_vo.hook_parts` and cannot drift
> from what is spoken. CLAUDE.md §4.6 — an instrument that fires where the
> mechanic does not measures something else — in miniature, caught in one commit.

> **THE LAB STILL HOLDS THE ORIGINAL SHOT TABLE.** `tools/ignition_lab.py` is
> the prototype of what was approved on 2026-08-29 and has not been re-timed.
> That is deliberate: it is the record of the four variants, not the build.

### 6.7 WHERE SHORTS ACTUALLY OPEN, SINCE THIS DOCUMENT GOT IT WRONG ONCE

§3 said the opening "only reaches a short that starts at zero", implying shorts
do not. They do, by default:

```
shorts_build.py       --lead defaults to None -> passes --full -> starts at 0.0
the app's Create      empty lead box -> same path -> starts at 0.0
--lead N              starts N seconds before the killing blow. The v43 clip of
                      record was --lead 18: 23.0s of a ~45s fight
cinema_clip.py alone  its own --lead still defaults to 6.0
```

So the opening reaches every short that does not pass `--lead`, and the open
question is not placement but **length**: ~53s opening at zero, against ~23s at
lead 18. That is Rick's call and it is a different question from this one.

---

## 7. THE STAKES BAND — hook brief §5a, built 2026-08-30

Rick sent `stakes-open.mp4` and the hook brief. §5a promoted the band to a
build when he retired the stinger it was riding on: *"i dont think i wanna
persue the hook stack or pre showing the later part of the fight. its a bit
jaring and confusing to look at. i do want to persue the stakes line."*

**Shipping home, as the brief specified it:** a capture-side flag on
`cinema_clip.py` — `--stakes`, `--stakes-sub`, `--stakes-in`, `--stakes-out`,
`--stakes-y` — following the outro card's precedent, so the band and the
ignition open ship as ONE bundle and slate 1 stays a single variable.

**It leaves on an event, not a clock.** The band fades out on the first clank,
which is where `scrunchAuto` arms the tape, so the introduction job hands over
to the scrunch legend at the moment the legend exists and neither is ever on
screen doing half of it alone. Same anchor `--vo-at clank` uses.

`tools/stakes_probe.py`, and three of its checks earned their place by failing:

```
0  the band installs                                          ok
1  the band is actually drawn                +0.089 luma on the strip
2  in on the clock, out on the CLANK    full by 0.15s (asked 0.25s), clank
                                        2.22s, gone by 2.53s (asked 2.57s)
3  the relic being FILMED never reaches its rows              SEE §7.2
4  no --stakes, no change                     133/133 frames identical
5  the line fits inside the frame       no bright pixel in the outer 5px
```

### 7.1 THE PROTOTYPE FITTED FOR THE WRONG REASON

The band's font was built as `700 * 0 + '700 ' + Math.round(64*k) + 'px ...'`.
That leading `700 * 0` evaluates to `0`, so the string is `"0700 32px ui-serif,
Georgia, serif"` — **not a valid font**, which a canvas silently ignores,
keeping whatever font it already had. The prototype's line was therefore
smaller than it asked to be, and it fitted the frame by accident.

Transcribed correctly into the build, the line rendered at its real 64px and
ran off **both** edges — "TWO WEAPONS. ONE SURVIVES." became "WO WEAPONS. ONE
SURVIVES". Invisible to every number in this repo, obvious in one glance:
`CLAUDE.md` §4.1's defect class, arriving by way of a typo that was hiding it.

The band now measures its own line and shrinks to fit, never grows past the
design size — which it has to anyway, because five candidate lines of different
lengths and a delivery width that is a flag cannot share one point size. Check
5 is the permanent guard.

### 7.2 AND THE BAND COLLIDES WITH THE OPENING ON SOME PAIRINGS

The brief placed the band at y = 14.5% by eye, *"measured against both camera
shots"* — the camera shots of the 2.35s opening. **The opening is 2.83s now**
(§6.6), so the subject sits somewhere else at every instant, and the placement
was measured against a shot table that no longer exists.

Swept over 19 pairings, asking how high the FILMED relic climbs while the band
is up:

```
spellbreaker v twinshade   subject top at   88px, 0.72s   <- above the band's TOP
dawnbringer v gravemourn                   158px, 0.60s
aureole v lastlight                        201px, 0.56s
ironhail v oathwound (the record seed)     175px, 0.58s   <- grazes the hairline
                                     the band occupies 139-214px
```

On the filmed seed the band's lower hairline just clips the top of the ball —
invisible in motion. On spellbreaker v twinshade **the caption cuts the ball in
half.**

> **AND THERE IS NO FIXED PLACEMENT THAT CLEARS IT.** To sit above the worst
> case the band's bottom would have to be at 88px, putting its top at 13px —
> inside the HUD. The lean clamp is what does it: it stops the opening centring
> a subject that is high in the hall (§2.3), so on some pairings the relic is
> simply up there.

Four ways out were put to Rick — accept it; move the band up to ~y=9% (fixes
the common case, still fails the worst); a picker floor rejecting pairings
whose subject climbs into the band; or give the opening a top inset.

**"do 4".**

### 7.3 THE BAND TELLS THE OPENING HOW MUCH FRAME IT HAS TAKEN

`SWBOpen.topInset` — device pixels of frame, from the top, that something else
has claimed. `--stakes` publishes its own bottom edge into it at install; the
subject-fit clamp in `cam()` subtracts it before deciding what fits.

**This is the letterbox rule applied to a caption.** `Renderer.draw`'s own
feasibility clamp already subtracts `barH` before solving what fits the usable
frame; the opening now does the same for whatever is laid over it. The
principle the brief argued for ults in FX §3.4 — the shot owns the camera —
is the reason it belongs here rather than in the band: a caption should not
have to know about relic radii, and a shot should not be framed against a
frame it does not have.

Three things it is careful about:

- **Device pixels, published by the drawer.** The band is drawing in device
  space over the composited frame; making it convert to arena-local design
  units would be a conversion every future writer has to remember. `cam()`
  converts once, where the clamp lives.
- **Held for the whole opening, not released on the fade.** The band leaves on
  the clank, the opening runs to 2.83s; releasing the inset with the band would
  step the camera in the middle of the pull. A constant inset never moves.
- **The new constraint wins an impossible window.** If the disc cannot fit
  between caption and floor at this zoom, staying out from behind the caption
  is what is kept — the floor has the rest of the frame to give.

Measured over 24 pairings, worst subject top against a band bottom of 214px:

```
                      pairings with the filmed relic behind the caption
without the inset     4 of 24, worst 126px behind (spellbreaker v twinshade)
with the inset        0 of 24, worst 0px — tangent to the band's lower edge
```

`stakes_probe.py` 6/6, `ignition_probe.py` 11/11, `engine_ab` 150/150,
`render_ab` 20/20 pixel-identical after the opening releases.

> **AND TWO OF THE PROBE'S CHECKS WERE MEASURING THE WRONG PASS.** Check 3 read
> the relic positions out of the BARE capture — the one with no band and
> therefore no inset — so it went on reporting the old collision after the fix
> landed. And the control pass for check 4 deleted `window.__stakes` but left
> `topInset` set, which is a different camera, so "no --stakes is a no-op" read
> 105/133. Both are the same mistake: a flag that moves the picture has to be
> undone in full before anything is compared against it.

### 7.4 THE BRIEF'S §7 ASKED TO BE CHECKED AT THE TIP. IT WAS.

The hook brief says of itself: *"This brief has not seen the repo. It is
written off the project record through v45. Confirm at the tip before
building."* Three things it names, checked:

| the brief asks | at the tip |
|---|---|
| did the scrunch survive the rebuild into `C:\dev\sundered-crown` | **yes** — 41 references in the build, and it arms on the first clank in every clip rendered this session |
| is v43b's **converging limiter** in the tree | **yes** — `shorts_build.py`, `alimiter …level=false` with the mandatory-flag note intact |
| is v43b's **outro card**, **PCM segment path** and **`on_info.json`** in `cinema_clip.py` | **no. None of the three.** `cinema_clip.py` has no outro, no `on_info`, and the only occurrence of the word "outro" in the tool is a comment written this session quoting the brief |

That last row matters beyond bookkeeping: §5a specifies the stakes band as
*"a capture-side flag on `cinema_clip.py` following the outro card's
precedent"*, and **there is no outro card here to follow.** The flag was built
on the precedent that does exist — `--vo`, `--cold-open`, `--motion-blur`: a
capture-side option that changes what is photographed, not a post pass. The
comment in `cinema_clip.py` that first repeated the brief's phrasing has been
corrected to say so, because a false citation in a file is exactly the kind of
thing this repo's own §7 rule exists to stop.

Also worth recording against the brief, which predates today: **§2's ignition
open is built and shipped** (this document), **§2d's three named probe checks
all exist** and `ignition_probe.py` carries eight more, and **§3a's VO-alignment
worry is resolved** — the line is now placed on the opening's own flares (§6)
rather than colliding with anything.

### 7.5 THE COPY IS PICKED

Five candidates rendered in motion over the real opening — the same shape as
every spread this project trusts — and Rick, 2026-08-30: *"i think id reject
everything but 1"*.

```
1  TWO WEAPONS. ONE SURVIVES. / ONLY ONE KEEPS THE CROWN     <- SHIPS
2  WHICH BALL WOULD YOU PICK? / ONE OF THEM IS ABOUT TO LOSE
3  CROSSBOW vs SWORD          / A FIGHT TO THE LAST HIT
4  REAL PHYSICS. REAL STAKES. / STAY FOR THE FINAL BLOW
5  TWO ENTER. ONE FALLS.      / PHYSICS DECIDES EVERYTHING
```

It lives in `cinema_clip.STAKES_LINE` / `STAKES_SUB`, one place, the way the
announcer's line lives in `cinema_vo.hook_parts`. **A bare `--stakes` is the
shipped pair**; an explicit line is the caller's own copy; no flag is no band.
`shorts_build.py` passes a bare `--stakes` through bare, so the copy is never
written down twice.

The four rejected are kept in the source beside the one that shipped. A
rejected option is the reason the answer is trustworthy — the same record
`docs/APP-FEATURES-BRIEF.md` §1 keeps for the VO placement spread.

> **AND THE SPREAD DID ITS JOB IN ONE ROUND.** Copy 3 was the only
> pair-specific candidate ("CROSSBOW vs SWORD" names the actual weapon types)
> and would have needed generating per fight; it is out, so the shipped line is
> one constant string and there is nothing to build for it.
