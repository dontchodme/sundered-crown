# CINEMA — experimental director. DEMO, not shipped.

Massive hit stop, a slow-motion push into the point of contact, letterbox, and
a mix that ducks and drags under it. Built as a patch over `sc-sil.html` so it
is a reviewable diff and can be thrown away in one command.

    python3 cinema_build.py --in sc-sil.html --out sc-cinema.html
    python3 cinema_check.py --n 20          # the falsification pass
    python3 cinema_probe.py --n 80          # what it actually picks
    python3 cinema_clip.py  --lead 6        # the mp4 (add --ab for the control)

Open `sc-cinema.html` and use the panel top-right.
`C` toggles the director, `F` forces a set-piece, `V` replays the same seed
with the director flipped.

## The one law

**The director cannot change who wins.** Structurally, not by discipline.

Everything rests on the fact that the frame loop already runs a fixed-timestep
accumulator:

    acc += raw * speed
    while (acc >= dt) match.step(dt)

The director's only lever on time is how much WALL time it hands to that line.
The sim still consumes it in identical `CONFIG.physics.dt` slices, so the
sequence of steps is what it would have been at 1.0 — slower, or stopped, but
never different. Slowing the picture cannot slow the fight.

This is also why the cinematic freeze is **not** `m.hitStop`. Hit stop lives
inside `step()` and `m.t` advances through it, so lengthening *that* really
would change the match. The freeze is `timeScale = 0` in the loop instead.

The only additions to the sim are three `beat()` calls, in the same family as
the existing `note()` and `statusTag()`.

### Verified

    [1] ENGINE A/B            432/432 summaries byte-identical vs sc-sil.html
    [2] TIME-SCALE INVARIANCE 48 runs at 0.5x / 0.13x / 0.05x + a hard freeze,
                              all identical to their 1.0x reference
    [3] PRESCAN FIDELITY      the plan equals what the match actually produces,
                              beat for beat
    [4] INTERPOLATED RENDER   whole matches driven through CINE.pump and drawn
                              through CINE.drawLerped, identical to simulate()
    cinema_check.py --selftest proves attack 1 can fail (it detects a
    one-field 0.01s corruption)

## Prescan, not reaction

`new Match(a,b,seed)` is deterministic and steppable, so the director runs the
whole match headless in a few ms and picks a **cut list before frame 1**. That
buys what reaction cannot:

  * **anticipation** — the push starts 0.55s BEFORE the killing blow
  * **exact rarity** — "the best moment in this match", not a threshold guess
  * **escalation** — the biggest cut is last

A reactive director is in the build for A/B only.

## Rarity is a BAR, not a budget — and the bar is high

A moment qualifies on its own merits or not at all; zero cuts in a match is a
correct answer. The bar sits at **1.90** under the kinetic model, chosen from a
sweep that asks `cinePlan` itself (over 120 matches):

    bar     0     1     2    3+   mean   finishes filmed   volley share
    1.05    3%   17%   30%   50%   2.77      77%               32%
    1.45   17%   34%   21%   28%   1.75      41%               40%
    1.90   41%   37%   16%    7%   0.90      18%               52%   <- shipped
    2.20   55%   36%    8%    2%   0.57      14%               62%

At 1.90 a set-piece is a rare, special occurrence: two matches in five show
nothing at all, most of the rest show exactly one, and only the top ~18% of
killing blows get filmed. Half of everything chosen is an exchange. There is no
per-match quota in either direction — a wild fight can still earn four.

### What prescan is and is not used for

It is used for **timing** (start the push before the blow lands) and **pacing**
(when two qualifying moments fall inside `minGap`, the stronger one survives —
so pacing never costs you the better moment just because it came second).

It is **not** used for ranking. Nothing is selected for being the biggest thing
in *this* match; everything is selected for clearing an absolute bar. Seeing
the whole fight in advance does not make the director pick a winner out of a
weak field.

## Anatomy of a cut — three movements, and the order is the whole thing

Matrix ordering. The tension lives in the approach, not the aftermath.

    1. THE DROP     time falls away BEFORE the blow. Camera stays WIDE --
                    the point of this movement is that you can see. The mix
                    goes underwater, the score tape-slows and drops in pitch,
                    a swell rises underneath.
    2. THE WHIP     at contact: frozen for five or six frames while the lens
                    SNAPS in, plus the boom. A tenth of a second, not a drift.
    3. THE RELEASE  out of the peak immediately, then time overshoots past 1.0
                    and the mix opens. Coming back hard is what makes the hold
                    mean anything.

Killing-blow figures:

    drop     lead 0.10s of MATCH time, rate falling 0.15x -> 0.07x   ~1.0s screen
    whip     freeze 0.095s, lens 1.06x -> 2.20x over 0.11s
    settle   0.28s, 2.20x -> 1.28x
    hold     0.45s at 0.22x
    release  0.42s, back to 1.0x and 1.10x speed

**`lead` is in SIM seconds, not wall seconds.** The screen duration of the drop
is roughly `lead / dropTo`, and the match only ever loses `lead`. Measured on
the first attempt: at lead 0.10 with a 0.16s ramp, the ramp consumed most of
the lead and the drop lasted 0.6s — a stumble, not a held breath. It then went
too far the other way at 1.8s. 1.0s is the third pass.

**The drop keeps decelerating** rather than parking at a constant rate — 0.15x
falling to 0.07x across the approach. A flat rate reads as "the video is in
slow motion"; a rate still decreasing as the blow arrives reads as time itself
giving way, which is the thing being imitated.

**There is no tier 1.** It fired on a 0.05s lead, about a tenth of a second of
screen time — too short to read as anything but a hitch. A moment either gets
the treatment or it does not.

**The peak can be far higher than a sustained push could ever be** — 2.20x
against the 1.32x of the sustained build — precisely because nobody has to live
in it. It is a strike, and it is out of it within a quarter second. An earlier
version had this inverted: freeze first, then a slow drift in, which put the
slow motion *after* the moment it was supposed to be building toward and made
the zoom a sustained crop rather than a strike. `cine-beat.png` walks the
whole thing frame by frame.

### The boom

Three layers, because one is a beep and two is a thud:

    SUB     a sine falling a full octave, 68 -> 30Hz. The body.
    CRACK   a short filtered noise transient. The leading edge -- without it
            the sub arrives late to its own impact, because a 40Hz cycle is
            25ms long and the ear places the hit by the transient.
    TAIL    a low band sent hot into the hall, so the reverb carries it.

In front of all of it, a gate: the send is choked to near nothing for ~70ms.
Silence in front of a sound is worth more than level on it.

## Audio: the reverb is the small half

The score is pre-scheduled automation against real time, so **slowing the sim
cannot slow it** — the picture would drag while the music walked on unbothered.
That is the commonest way this effect gets built wrong.

Fix: render the bed ONCE through an `OfflineAudioContext` using `SFX.bed()`
unmodified, play the result as a single buffer, and ramp its `playbackRate`
with the director. The music then slows AND DROPS IN PITCH with the picture,
which is the sound people actually mean by slow motion. Toggle it in the panel
to hear the difference; falls back to the live scheduled bed if
OfflineAudioContext is unavailable.

## The slow motion was genuinely choppy, and it was arithmetic

Rick: *"the slow mo feels like it's choppy and losing frames. It might not
actually be but that's how it feels."* It actually is. Nothing is being
dropped — nothing new is being **produced**.

The sim runs on a fixed `CONFIG.physics.dt` of 1/120. At a 0.07x drop a 60fps
frame feeds the accumulator 0.0012s, so a step lands only every 7.1 frames:

    timeScale 1.00   step every  0.5 frames   content at 120 Hz
    timeScale 0.25   step every  2.0 frames   content at  30 Hz
    timeScale 0.10   step every  5.0 frames   content at  12 Hz
    timeScale 0.07   step every  7.1 frames   content at 8.4 Hz

The display runs at 60 and the world updates at 8. This is unavoidable for any
fixed-timestep sim below about 0.25x, and 0.25x is far too fast for the effect,
so the rate cannot be the answer.

**The answer is the standard one: keep the fixed step, and render BETWEEN
steps.** Snapshot the visual state before a step batch, then draw
`lerp(previous, current, acc/dt)`.

Measured over one killing-blow set-piece at 60fps (`cinema_smooth_probe.py`):

    interp   frames  distinct   %    longest identical run
    OFF          61        40   66%          8 frames
    ON           61        61  100%          1 frame

Mechanically: values are overwritten, the frame is drawn, and the exact saved
numbers are written back — same numbers in, same numbers out, no drift, and the
sim never observes an interpolated value because it is restored before the next
step. Objects are keyed by **reference**, which works because particles, rings
and projectiles are mutated in place and are only ever added or removed *by a
step*, so between steps the set is stable. Angles get shortest-path
interpolation, or a weapon crossing pi spins the wrong way for one frame.

Interpolated fields are a deliberate **whitelist**: geometry, not state. `hp`,
`charge` and `stun` are excluded — fractional health for a few frames buys
nothing, since the eye is tracking the weapon.

`cinema_check.py` attack 4 renders whole matches through the live path —
`CINE.pump` for stepping, `CINE.drawLerped` for the frame — and compares the
result to `simulate()`. If the restore were not exact, or if the sim ever saw
an interpolated value, that is where it would show.

The live page and the offline clip renderer now share `CINE.pump`, so the mp4
cannot show something the game does not — which is exactly the trap a bespoke
capture loop sets.

## The audit

A deliberate pass over everything built, hunting rather than confirming. Six
findings, all fixed and all covered by a probe:

  1. **The Force button crashed.** `begin()` was handed a raw beat with no
     `beats` array and the drop phase read `cut.beats[0].t`. begin() now
     synthesizes the array, so it cannot be handed a cut it cannot play.
  2. **Late fire.** A planned cut whose moment passed while another cut was
     playing would still fire, whipping the lens onto a position where nothing
     was happening any more. Stale cuts are now abandoned.
  3. **Volley/kill double-count.** A fatal hit inside a qualifying volley could
     also qualify standalone — two cuts for one moment, the second firing late.
     A volley now swallows its members (80 matches, 33 volleys, 0 overlaps).
  4. **`CINE.reset()` left the accumulator dirty** across matches.
  5. **The rate probe was fiction.** It re-implemented the selection rule in
     Python and had drifted three revisions behind the module — no volleys, the
     old dedupe. It now asks `cinePlan` itself.
  6. **The smoothness probe assumed its seed had a cut.** When the bar moved,
     it silently measured nothing. It now scans for a qualifying seed.

  And one on the process: my own record of the shipped bar was stale (1.05 in
  the notes, 1.50 in the file — recalibrated during the kinetic pass). The
  sweep was unaffected because it sets the floor per row, but it is the reason
  audits ask the file rather than the author.

All four falsification attacks pass after the fixes; `_audit_probe.py`
exercises findings 1-4 directly.

## Three fixes from play

**Volleys rushed, not wallowed.** The first volley ran its gaps at 0.5-0.6x,
which meant the exchange was SLOWER between blows than the fight it was
interrupting — a four-gap volley cost about four extra seconds and hurt the
flow of battle. `gapRate` is now 1.2-1.35: the sequence RUSHES between contacts
and slams to a drop only in the last few hundredths before each one, middle
blows hold for 65% of the whip so only the last contact gets the full freeze,
and the post-volley hold is halved because the exchange was the moment.
Measured: a 7-blow volley now costs +1.1s net; a 3-blow costs +1.0s; before,
+4-5s.

**Ranged cuts film both ends.** The shot records when and where it was loosed;
a ranged set-piece now starts AT the loose (capped 0.45s of match time back), a
ring blooms on the archer, a tracer line and comet head ride the bolt, the
camera pans down the flight, and an airy whoosh rises with it into the boom.
The flight always spends about 1.2s of screen whatever its match length, so a
long lob cannot buy itself three seconds of approach. Without both ends the
viewer cannot tell what caused the cinematic.

**The bottom of the arena no longer clips the action.** With a contact near the
bottom wall, the travel clamp capped the camera centre ABOVE the contact and
the zoom multiplied the contact's distance below that fixed point by z —
pushing the action ~100px past the bottom edge of the frame. Reported from
play, confirmed by the arithmetic (fs = fy·z − py·(z−1)), fixed by a second
clamp that solves that equation for the centre keeping the focus inside the
frame with a 10% margin. That clamp WINS over the lean clamp; the camera
centre is allowed to leave the viewport entirely to satisfy it, and the floor
bleed keeps the revealed strip from being a seam. Verified against forced
contacts at both walls in `cine-walls.png`.

**Process note.** The tracer patch initially no-oped: a quick edit matched
stale text and Python's `str.replace` silently does nothing on a miss. Caught
because the follow-up edit's assert failed and the probe showed `prog=-1` on
every frame. Every module edit now asserts its anchor, the same rule
`cinema_build.py` has enforced from the start.

## The kill flash — its own pass

This one predates the director and applies with it OFF too; the set-piece is
just what made it visible. It was a full-frame `#FFF4D0` at 0.5 alpha for a
full second: about thirty frames of the picture washed flat beige at the exact
moment the match is decided. Two faults, and they are the same fault twice:

  * **The frame is not the subject.** The blow is. It is now a radial burst
    centred on the relic that just died, bright at the point of impact and gone
    by the edges.
  * **It decays with the SIM.** Under a 0.24x set-piece one second became four.
    While a cut runs it is clamped against the director's wall clock instead.

Compare the two rows of `cine-killshot.png` — the bottom row is the director
off, and it is legible now where it used to be a beige field.

## Two bugs the design could not see

**1. The chain trigger was structurally impossible.** It looked for three
same-side hits inside a 0.45s window — but `CONFIG.combat.hitCd` IS 0.45, so
one relic physically cannot land three hits in that span. It fired twice in
2,582 beats. The drama there is not speed anyway, it is being UNANSWERED:
redefined as a run from one side over 2.2s that a single reply ends.

**2. The kill flash is an impact-frame element being stretched like a world
element.** `m.finisher` decays with the sim, so under a 0.10x set-piece the
engine's ~1s full-screen white became ~10s of held white and the picture sat
flat beige through the most important moment in the match. Most presentation
state SHOULD stretch — that is what slow motion is — but a full-frame opaque
flash must not. It is now clamped against a wall-clock envelope the director
owns, and only while a cut is running.

Both were found by looking at rendered frames, not by reading code. The overlay
A/B sheet also killed two layers outright: a full-frame desaturation scrim at
0.75 was invisible against an already-desaturated arena, and a full-frame
additive flash at 0.55 blew the picture out. Same root cause — treating the
frame as the subject. Both are now centred on the point of contact.

## Known integration cost

`render.py` steps in lockstep at fixed dt and re-renders audio from the event
log against MATCH time. Cinematic dilation is a WALL-time effect, so the video
pipeline needs the same change `cinema_clip.py` makes: record a wall timeline,
schedule audio against it, and replay the send automation and bed playbackRate
from the recorded curve. Accepted as a walk-back-able risk.

## Files

    cinema_build.py            the patch. --check asserts the sim is untouched
    _cinema_module.js          the director
    _cinema_panel.js           the demo panel
    cinema_check.py            the falsification pass, with --selftest
    cinema_probe.py            score distribution and what gets chosen
    cinema_rate_probe.py       the floor sweep behind the rarity number
    cinema_overlay_probe.py    layer-by-layer A/B on a frozen frame
    cinema_smooth_probe.py     distinct frames per second of slow motion
    cinema_clip.py             the director-off / director-on mp4

## Settled

  * Ultimates get no guaranteed slot. They already carry their own set-piece,
    banner and name; the director highlights what the game does not already
    dress up.
  * Prescan only. The reactive director has been DELETED — it lost on every
    axis and there was no reason to carry it. The panel toggle is gone too.
  * The killing blow earns its place like everything else.

## Open decisions

1. **`overscan` at 0.55 is the compromise, and it is a real one.** Higher gets
   the shot closer to the action; too high pushes the collapsing walls out of
   frame entirely, and the walls are a lot of what says "arena". The three
   settings are rendered side by side in `cine-overscan.png` — pick from the
   picture rather than the number.
2. **Is `handheld: 7.0` enough, or is it invisible?** It is a 7-sim-unit drift
   on a 520-unit arena, chosen to be felt rather than seen. If the shot still
   reads as a crop, this is the next number to move, not zoom or bias.
3. **The HUD and the gold frame stay perfectly rigid while the arena moves.**
   That is my remaining suspect for "detached": the frame reads as a television
   set with a video playing inside it. Letting the gold frame scale at ~25% of
   the camera zoom would sell depth, but it is a bigger change and it touches
   the shipped composition, so I have not done it.
4. **Zoom is now 1.32 at peak and could still come down.** "Definitely
   over-zealous before and still may be" — 1.24 is the next step if so, and
   with overscan in place it costs less framing than it used to.
