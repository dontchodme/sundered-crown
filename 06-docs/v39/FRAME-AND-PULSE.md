# v39b — THE PULSE, AND THE FRAME. Two notes on Rick's read of the first cut.

**2026-08-20.** Both from watching `foregone-v-threshmaw.mp4`.

```
02-chain/sc-foregone.html   76e5d4e7e80661ee   the thicker pulse
02-chain/sc-safeframe.html  90e20add92032cfb   <-- BUILD OF RECORD CANDIDATE
frame_probe          9/9
engine_ab            1890/1890 IDENTICAL on all TWENTY-ONE, sc-foregone vs sc-safeframe
verify.py --n 40     13/13 . 0/8400 timeouts . spread 14.1pp . mean 37.8s
07-shorts/v39/foregone-v-threshmaw-tiktok.mp4   44.7s . 1080x1920 full-bleed
```

---

# 1. THE PULSE — AND THE KNOB WAS THE STROKE, NOT THE RADIUS

Rick: *"the novas need to be much larger. i was thinking a big thick pulse of
electricity"* → *"by larger i mean the thickness of the rings themselves not
the area they cover."*

The area was already right. `drawRings` carries the answer:

```
c.lineWidth = r.w * (1 - k * 0.7);
```

The stroke already tapers as the ring opens, so raising `w` buys the SHAPE as
well as the size — it leaves thick and thins as it spreads, which is what a
discharge does. At `w` 7 and 4 these were hairlines expanding across a hall 880
units wide, and reading them as small was reading the width.

```
  bloom       7  ->  44   in `core`, plus a second ring
  bloom hot   —  ->  16   in `glow` at 0.84 radius, 0.40 life
  small pulse 4  ->  16
  the sigil's own breathing ring   1.4 -> 7, and it tapers now too
```

**Two rings for a bloom, not one fat one.** A single 44px stroke reads as a
painted band; electricity is a saturated body with a hot edge inside it, so the
second ring arrives with the first and is gone before it. That is the arc-flash
the eye already knows.

`Match.ring` is shared by all twenty-one relics and is **deliberately
untouched** — only this relic's call sites moved.

---

# 2. THE FRAME — THE FIX WAS IN THE WRONG PLACE, AND IT WAS MINE TO FIND

Rick: *"the last few videos have been poorly cropped. they are missing a lot of
the bottom of the frame. these should be formated for tiktok."*

**The game renders full-bleed 1080x1920 and always has.** `cinema_clip
--shorts` was shrinking it to 79% and boxing it: 114px bars either side and
312px of dead black at the bottom.

That was a deliberate fix from an earlier session to an earlier complaint of
Rick's — action at the bottom was getting cut off, `cinema_edge_probe` showed
the FILE was clean (0/8 wall cuts clipped the near relic), and the diagnosis
was that TikTok's caption bar was covering it. **The diagnosis was right and
the fix was in the wrong place.** Shrinking the whole frame to dodge the
platform's UI spends every pixel in the video to protect the bottom sixth of
it, and next to a feed where everything else is edge to edge it reads as
amateur.

## The arena was width-bound, and the old comment said so

```
this.aw = this.W - this.pad * 2;          // 1056
this.scale = this.aw / CONFIG.arena.w;    // 2.031
this.ah = CONFIG.arena.h * this.scale;    // 1625
this.arenaTop = this.hud + 24;            // 176
```

*"The arena is width-bound — its height follows from the sim and the frame
width — so the height the HUD gave back cannot become more arena."* True, and
it also meant the hall ran **176..1801 of 1920** and its bottom 200px lived
under a caption.

`scale` is the smaller of the two bounds now, which is what a fitted layout
should always have been: the old expression is correct only for viewports at or
below the arena's own 0.65 aspect, and 9:16 is 0.5625.

```
  foot    scale      aw      ah   bottom   side   bound by
     0    2.031  1056.0  1624.6   1800.6   12.0   width      <- the old layout
   120    2.015  1047.8  1612.0   1788.0   16.1   height
   240    1.865   969.8  1492.0   1668.0   55.1   height
   340    1.740   904.8  1392.0   1568.0   87.6   height     <- shipped
   460    1.590   826.8  1272.0   1448.0  126.6   height
```

## THE OLD LAYOUT IS A VALUE OF THE NEW CODE, AND THAT IS ASSERTED IN PIXELS

At `FRAME.foot = 0` the available height is 1744, `1744/800 = 2.18` is looser
than `1056/520 = 2.031`, the width binds exactly as it always did, and all four
numbers come out unchanged. `frame_probe` asserts that against **a rendered
frame** — `0 differing pixels of 1080x1920` — and not against the four
constants, because four numbers agreeing is not the same as a picture agreeing.

So the constant can be dialled to nothing without a second code path existing
to be wrong.

## What it costs, stated plainly

The arena's aspect is 0.65 and the box above the strip is 0.75, so the hall can
no longer touch the side walls: **905 wide in a 1080 frame, 88px of the game's
own background either side.** That is background and not letterbox — the hall
has a drawn frame and the margin reads as composition — and it is 905 against
the **852** the encode was boxing, so the picture is LARGER in both dimensions
than what shipped before.

**This changes the framing of every relic's video, not just this one.**

`cinema_clip --shorts` now emits `scale=1080:1920` and nothing else. A build
without `FRAME` still renders its hall to y=1800 and will have its bottom wall
covered — the correct trade to surface loudly rather than to paper over a
second time.

---

# 3. THE POSTING CUT

`07-shorts/v39/foregone-v-threshmaw-tiktok.mp4` — 44.7s, 1080x1920 full-bleed,
`--shorts` delivery encode, bm_lewis VO at 0.3s over live action. **No card and
no cold open**, per v38 §10.

Seed 912479, picked by `foregone_pick.py` — new, because `cinema_pick` scores a
seed on its cut list alone, which is the right question for a director demo and
the wrong one for a relic reveal. A Converse fight is only worth filming if the
ULTIMATE is legible in it, so this one sorts on trail length and on whether the
reversal CONNECTS, and it reports what the crowd exception costs on each
candidate seed rather than leaving v38 open decision 8 assumed.

Two casts, at 15.3s and 32.5s, both laying the full twelve sigils; the second
connects twelve rings against the first's three. That spread is the ultimate's
real variance and it is the reason the seed was chosen.

---

# Open decisions

1. **`FRAME.foot` is 340 and was chosen, not swept.** 17.7% of the frame.
   TikTok's own guidance is nearer 25%; most creators use ~17%. The cost curve
   is in §2 and nobody has looked at 240 or 460 on a real feed.
2. **The top nav still overlaps the HUD.** The strip was taken entirely from
   the bottom because that is where the caption is; the ult names sit at y≈27
   and a top overlay reaches ~130.
3. **Every relic's video reframes.** Nothing has been re-rendered except this
   one, so the back catalogue and the new cuts will not match.
4. **`orbDmg`, `orbR`, `pulse` and `lay` are still unswept**, and the ring
   widths above were set from one still. v39 README open decisions 1 and 2.

---

# 4. v39c — THE PLASMA FIELD. Rick's reference, and what it changed.

Rick, over four notes and one screenshot of Razor's Plasma Field:

    "the novas need to be much larger ... i mean the thickness of the rings
     themselves not the area they cover"
    "i also would like them to be slower moving"
    "i also think they should cause knockback and feel like they have some
     weight to them"
    "lets not make the rings so perfectly circular. a jagged circle of thick
     lightning" -> "too jagged. dial it back a bit"
    "how about some thinner hair line arcs coming off the ring to give it a
     more realistic look and a sense of 3d?"
    "lets also add some lightning/plasma sound effects"

**I cannot watch video and said so.** The link was a clip; what made this
work was the SCREENSHOT of the ability page, and the thing worth reading in
it is that **the reference's core band is smoother than mine was.** Its
lightning read does not come from the silhouette at all — it comes from a
corona of fine filaments hugging a fairly clean band. That is the note Rick
arrived at independently two messages later.

## 4.1 THE WAVE TRAVELS NOW, AND THAT WAS FORCED BY "SLOWER"

The rings resolved their damage on the frame they were born and then drew an
expanding ring for half a second afterwards. At the old speed that was nearly
invisible. At `bloomTravel` 0.62 **the damage would land two thirds of a
second before the plasma arrived** — the picture would be lying about its own
rule, which is the one thing this codebase does not let an ultimate do.

So the waves travel and connect when they pass, LINEARLY: `drawRings`' shared
easing is `k*k*0.7 + k*0.3`, which accelerates — right for a shockwave leaving
an impact, wrong for a field being driven outward, and a constant rate is the
only one a viewer can lead.

**`band` is one number for the picture and the rule.** `_wave` draws across
`r ± band` and `_tickWaves` connects across `r ± band`. What the viewer sees
is the hitbox. The jag amplitude is capped at half the band for the same
reason — a spike reaching past `band` would draw outside its own hitbox.

Consequence, and it is a real mechanic: **a wave can be outrun.** 210 u/s for
a bloom against a 405 cruise.

## 4.2 THE WEIGHT, AND WHAT IT COST

Knockback outward from **the wave's own centre** — the sigil, not the caster —
because the plasma is the thing pushing. Bloom 210 against
`CONFIG.combat.knock`'s 165; sigil wave 70. × `knockMul` like every other
knock in the game.

```
  dmg    26     24     22     20     18     17     16     15     12
  win  66.5   63.7   62.9   58.5   51.7   51.2   49.8   47.5   41.0
```

**22 was 50.8% before the waves and 62.9% after. The knock is worth about six
points of blade.** 16 taken, and it changes what the relic IS: it paid 10%
against the type's mean of 24.4 and was a scythe that HAS an ultimate — the
opposite shape to Lastlight. At 16 it pays 34% and sits BELOW Lastlight's
17.5. It is an ultimate with a scythe attached after all, which is legitimate
and is now the second such relic on this type — **but it arrived by accident,
when a presentation note turned into a knockback and nobody re-asked the
question.**

An undesigned side effect, recorded as one: **ring hit counts roughly doubled**
(8% → 18% of rings reaching the foe on a natural cast) because the knock
shoves the foe into neighbouring waves.

## 4.3 THE PICTURE — FOUR PASSES, A JAG, AND A CORONA

A plasma field is not a fat line, it is a VOLUME with structure. Four passes
over one path, composited with `lighter` so they SUM and the middle of the
filament goes white while its edges stay school blue — the one thing a single
stroke of any width cannot do.

`jag` is a named knob, a fraction of the band, one number for both wave sizes.
**0.50 was "too jagged"** — at half the band the radial swing is the same order
as the band's own thickness and the loop reads as a saw. **0.26**, with
vertices 46 → 34, because depth was not the only problem: short runs read as a
cog. Lightning is long straight runs with sharp corners.

**And it MORPHS rather than scaling.** The offsets lerp between two hash sets
three times across a wave's life. A fixed jagged shape blown up over 0.6s is a
logo zooming, not a discharge.

**The 3D is draw order, not perspective.** A third of the hairline filaments
are stroked BEFORE the band, so the band occludes them and they read as the
far side of a torus; the rest go over it. Per-filament alpha does the rest.
This is the cheapest honest depth cue a flat canvas has, and it is the one the
reference is using.

Two bugs found on the way, both only visible in states nobody looks at:

- **Newborn waves were solid white starbursts.** A wave born at radius 7 with
  a band of 26 has an amplitude of 13, so vertices swung THROUGH the centre.
  Waves are born at 0.8 of their own band now — a loop from the first frame.
- **The soft glow pass swallowed small rings.** 2.4 band widths is 36px on a
  ring 45 across, which fills the hole and turns the band back into a disc.
  Clamped to the radius.

## 4.4 THE VOICE — SIX BRANCHES, AND THE INSTRUMENT IS NOISE

The first cut was tonal and came out a bell. **What makes a sound electrical
is that it is BROADBAND and has no pitch centre**: a crack is white noise
through a highpass with no ring-out, a fry is narrow noise re-triggered faster
than the ear can count. `_burst` is that primitive and this relic was barely
using it. `_burst` cannot sweep its filter, so a downward RIP is three
staggered grains at descending cutoffs — the spike storm's swell trick, run
the other way.

**`foregone-arc` is new and it is the one that matters.** Every other sound
this relic makes is fired by an EVENT, so a cast that never connected was
silent while filling the screen. This is the arc frying, on a 0.13s clock, for
as long as there is plasma on the floor — ~6 a second, and quiet, because
forty audible ones would be a wasp nest.

**Checked the thing that actually breaks.** `SFX.ult` is an if/else chain
ending in a generic rune-crack, so a `w` string with no branch plays the wrong
sound **silently, forever**. All six emitted names have a branch, with a
negative control on an invented one.

## 4.5 THE SEED WENT STALE, AND THE RENDER CAUGHT IT

Knockback is a sim change, so **912479 became a different fight** — its cut
list came back empty and `cinema_clip` died on `cuts[-1]`. Not a bad seed, a
stale one. Any tuning pass that touches the sim invalidates every picked seed
in the tree, and nothing says so anywhere.

Re-picked: **Foregone v Thornwake, seed 912368** — same weapon type, green
against blue for the cleanest read, Foregone wins, 2 cuts.
`07-shorts/v39/foregone-v-thornwake.mp4`, 45.2s, 1080x1920 full-bleed.

```
foregone_probe   16/16   hex at cap 1.0% -> 10.9%
engine_ab        1710/1710 IDENTICAL on the other twenty
verify --n 40    13/13 . Foregone 48.0% . spread 14.4pp . 0/8400 timeouts
```

## Open decisions, v39c

1. **The relic changed shape by accident.** 4.2. It is an ultimate with a
   scythe attached now and nobody chose that; the blade is where the knock
   was paid for because the blade is what was swept.
2. **`bloomKnock` 210 and `orbKnock` 70 are unswept.** They were priced
   against `CONFIG.combat.knock` and then the BLADE absorbed the difference.
   Sweeping the knock instead would give a different relic at the same 48%.
3. **A wave can be outrun and nothing measures how often.** 210 u/s against a
   405 cruise. The 18% ring-hit rate is the aggregate, not the story.
4. **A sim change invalidates every picked seed in the tree** and no tool says
   so. 4.5. `foregone_pick` re-runs cheaply; the back catalogue does not.
5. **`jag` 0.26, `arcEvery` 0.13 and every gain in 4.4 were set by eye and by
   one still.** I cannot hear the render, and nothing in this repo measures a
   mix.

---

# 5. v39d — FOUR NOTES OFF THE VIDEO, AND TWO OF THEM WERE ONE BUG

```
02-chain/sc-foregone.html   d2a36d41f4803520
02-chain/sc-safeframe.html  9cecdd1351edbda5   <-- BUILD OF RECORD CANDIDATE
foregone_probe  16/16 . frame_probe 11/11 . engine_ab 1710/1710
verify --n 40   13/13 . Foregone 49.9% . spread 14.2pp . 0/8400 timeouts
07-shorts/v39/foregone-v-thornwake-v3.mp4   43.0s . seed 911480
```

## 5.1 THE SCRUNCH GAP AND THE CUT-OFF BOTTOM WERE THE SAME LINE

Rick: *"something has gone really wrong with the scrunch. it has a huge gap in
the middle"* and *"it also looks like the bottom of the video is still cut
off."*

`CONFIG.scrunch.bottom` is a hardcoded **1812** in design space, from when 1812
simply meant "near the bottom of the frame". Reserving a strip made it two
bugs at once:

- the panel ran to 1812, **232px below the safe line**, so the ULTIMATE row —
  the one thing the panel exists to show — sat under the caption.
- `_panelFacts` pins ON HIT to the panel's TOP and ULTIMATE to its BOTTOM, so
  the space between them is `h` minus two fixed blocks. A shorter hall made
  `y` smaller and `h` bigger, and **the gap grew by 244px.**

`Math.min(S.bottom, H - FRAME.foot - 12)` fixes both and keeps the identity
exact: at `foot` 0 the safe line is 1908 and 1812 still wins.

**Why it shipped: `frame_probe` only ever rendered an ordinary frame.** 9/9
green while the one screen the change broke was never drawn. It photographs
the SCRUNCHED layout now and asserts the panel's bottom against the safe line.
11/11.

## 5.2 THE KNOCK WAS BACKWARDS, NOT ABSENT

Rick: *"where is the knockback happening on the rings? i see the green ball
passing right through them with no knockback."*

It was firing — 566 connections over 24 matches — and **making the foe
slower.** An outward impulse added to a ball that is 95% of the time moving
INTO the wave cancels momentum instead of throwing it:

```
                n  knock  radial in  radial out  moving IN  left OUT
  BEFORE, bloom 91    210       -425     (speed -121)   95%     ~half
  AFTER,  bloom 60    300       -330        +303        95%      100%
  AFTER,  sigil 266   150       -353        +162        94%      100%
```

The fix is not a bigger number, it is the right direction: **zero the inward
radial component first, then push.** A body caught by an expanding front
always leaves it going outward — which is what `resolveHit`'s knock gets free,
because a swing that connects has already carried the foe away.

**And the second half of Rick's note was also true.** The foe stood inside a
DRAWN band 26.2% of every cast while only 8% of those frames were a real
connection, because a spent wave kept drawing at full brightness. There is one
opponent, so a wave that has connected has nothing left to do. Spent waves
discharge to 34% alpha — still travelling, still fading, no longer promising a
hit they have already delivered.

## 5.3 THE SIGN ERROR WAS WORTH FIFTEEN POINTS OF WINRATE

```
  22 -> 50.8%   before the waves travelled
  22 -> 62.9%   travelling and knocking -- the bug
  16 -> 34.5%   once the knock pointed the right way
  24 -> 49.7%   TAKEN
```

A knock that BRAKES the foe keeps it in the trail to eat the next eleven
waves. A knock that THROWS it shoves it out of the trail. Same magnitude,
opposite sign, fifteen points of winrate.

**v39c recorded that this relic had become "an ultimate with a scythe attached
... by accident". That note was itself the artefact.** The accident was the
sign; fixing it put the shape back. At 24 against the type's mean of 24.4 this
is a scythe that HAS an ultimate — the opposite shape to Lastlight, as it was
before the knock existed. Both rows are kept in the builder, because **a
balance number that moves fifteen points on a sign error was measuring the
bug.**

## 5.4 THE SOUND WAS THE WRONG LENGTH, NOT THE WRONG PITCH

Rick: *"i cant tell if im hearing balls bouncing or lightning. im thinking
long zapping sounds like a tesla coil."*

The diagnosis is DURATION. Those events were 18 to 140 milliseconds, and at
that length anything is a click — the hall is already full of clicks, so the
ear filed them under the name it already had.

A coil does not click. Its voice is the **spark-gap break rate**: a harsh
sustained buzz near 130 Hz with enormous harmonic content, which is a
SAWTOOTH, plus the tear of the arc, which is sustained bandpass noise. `_tone`
gain only ever decays, so a sustain is built from overlapping stages — the
spike storm's swell trick, held flat instead of climbing.

Deliberately NOT Bloodmill's instrument: that was two sawtooths a few hertz
apart so the ear hears the BEAT as a growl. These are a fifth apart, so they
read as one harsh voice with no throb.

**`foregone-arc` is what carries it.** Fired every 0.13s, each event **0.20s
long, so they OVERLAP** — what the ear gets is not eight events a second, it
is one continuous rasp that starts when the ultimate does and stops when the
last wave dies. **The clock being faster than the decay is the whole trick.**

`foregone-bloom` is half a second now, and it can afford to be: only a
CONNECTING wave fires it, and a cast lands one or two of its twelve.

## Open decisions, v39d

1. **Nothing in this repo measures a mix.** Every gain, `arcEvery`, and the
   0.13-against-0.20 overlap were set by reasoning and not by listening. This
   is the largest unfalsified thing in the session and it has now produced one
   wrong answer already.
2. **`bloomKnock` 300 and `orbKnock` 150 are still unswept**, and after 5.3 it
   is clear they are not a small knob: the blade absorbed a 15-point swing
   that belonged to them.
3. **A spent wave at 34% is a number chosen off one still.** The alternative —
   not drawing it at all — was not tried and might read better.
4. **`frame_probe` now photographs two layouts. There may be a third.** The
   result panel (`_panelResult`) shares the same box and was never rendered by
   any probe.

---

# 6. v39e — THE RESERVE COMES OUT. `FRAME.foot` = 0.

Rick, after the reserve shipped: *"the video still has the bottom of the frame
cut off. why can we not stretch this to the full length?"*

**We can. The thing stopping it was the reserve, and the reserve was mine.**

§2 justified `foot` with a claim that TikTok's caption bar was covering the
action. That claim is an INFERENCE from an earlier session, written into a
code comment as though it were Rick's words. It is not. Rick has now said the
opposite twice — first about the 79% letterbox, then about the reserve that
replaced it. Both times the complaint is the same and it is not about the
platform: **the picture does not fill the frame.**

```
  foot    hall        runs         ink rows    fills   side margin
     0    1056x1625   176..1801     3..1855     96%    12px
   120    1048x1612   176..1788     9..1834     95%    16px
   340     905x1392   176..1568     9..1614     84%    88px
```

**The reserve cost twelve points of frame and 76px a side.** Horizontal fill
is 100% at zero.

The knob stays, with the cost curve above measured, because a platform may one
day want it. **The value is 0**, which is the value the identity check proves
is pixel-for-pixel the layout that existed before any of this.

The encode half of §2 stands and was always the right half: the 79% letterbox
is gone and delivery is `scale=1080:1920`.

## 6.1 WHERE THE LAST 4% ACTUALLY IS

The hall is 1056x1625 under a 176px HUD, so it ends at 1801 of 1920. **The
arena's own aspect is 0.65 (520x800 sim units) and the frame's is 0.5625.**
They do not match, so the hall fills the width or the height and not both —
and the width binds.

To make the hall reach the bottom edge, `CONFIG.arena` has to go
**520x800 -> 520x853, +6.6% taller.** That is not a rendering change. It is
the playfield: more room to fall, different clank geometry, every relic
re-tuned. It is a session, not a knob.

## 6.2 A CACHED CONTROL WITH NO INVALIDATION

`frame_probe` built its `foot=0` control `if not zero.exists()`. The cached
copy went stale the moment the RELIC's build changed underneath it — a
different game is a different fight is different pixels — and the identity
check then failed loudly for a reason that had nothing to do with the
identity.

**This is the stale-seed bug one file along** (5.x, 4.5): an artefact derived
from a build, cached, with nothing watching the build. It rebuilds
unconditionally now. 11/11.

## Open decisions, v39e

1. **The arena aspect is the only route to 100%** and it is a full re-tune.
   6.1. Unasked and unmeasured.
2. **Two things in this tree are now known to cache against a build with no
   invalidation** — picked seeds and the probe's control. There is no reason
   to think those are the only two.
3. **`FRAME.foot` ships at 0, so nothing exercises the non-zero path.** The
   cost curve in §6 is the only thing keeping it honest, and it was measured
   once.
