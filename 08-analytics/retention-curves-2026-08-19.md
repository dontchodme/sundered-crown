# THE SURVIVAL CURVES, AND WHY THE NEXT LEVER IS NOT THE ONE WE THOUGHT

**2026-08-19, same session as `sundered-crown-coldopen-read-v31.md`.** That note
worked from TikTok's summary metrics. This one works from the **per-second
survival curves**, which turn out to be available and change several answers.

Rick, on reading v31: *"looks like our work on retention was even better than i
thought... I think the health bar rework will help us retain viewers who do stick
around past 5 seconds even longer."*

**First half: yes, and the curves show the mechanism. Second half: the data says
that specific bet does not pay, and also says to ship the health rework anyway,
for a different reason and against a different metric.**

---

# 0. A NEW INSTRUMENT — the per-second curve is fetchable

TikTok Studio's retention panel says only *"most viewers stopped watching at
0:0X"*. The underlying per-second curve is served by the same insight endpoint
the page already calls, and can be pulled from the console of a logged-in
session:

```js
const B = "https://www.tiktok.com/aweme/v2/data/insight/?locale=en&aid=1988"
        + "&app_name=tiktok_creator_center&device_platform=web_pc&channel=tiktok_web"
        + "&os=win&tz_name=America%2FLos_Angeles&tz_offset=-25200&type_requests=";
const get = async (id, kind) => fetch(
  B + encodeURIComponent(JSON.stringify([{insigh_type: kind, aweme_id: String(id)}])),
  {credentials: "include"}).then(r => r.json());

await get(AWEME_ID, "video_retention_rate_realtime");  // {timestamp:"3000", value:0.56} per second
await get(AWEME_ID, "video_info");                     // .statistics -> play/digg/comment/share/collect
```

`aweme_id`s are in the DOM of `/tiktokstudio/content` (`/7[56]\d{17}/`), and in
the URL of any video's analytics page.

**Known bias, stated because it is not resolved.** The area under each curve runs
**11–20% below** the average watch time TikTok reports for the same video —
consistently, and in the same direction for all eight. Most likely the reported
average counts loops while the curve is capped at 100% at t=0. That is a
hypothesis, **not something checked**. It does not move any conclusion below:
the curve ranks the eight videos in the same order as the reported averages, and
every argument here is about *shape*.

# 1. THE COLD OPEN'S MECHANISM, FINALLY VISIBLE

```
                          r(1)   r(2)   r(5)  r(10)  r(20)   loss in second 2
COLD OPEN
Axiom v Nightfell         0.85   0.70   0.34   0.26   0.14        0.15
Ironhail v Goreshard      0.85   0.68   0.35   0.24   0.18        0.17
Emberedge v Thornwake     0.80   0.65   0.31   0.23   0.17        0.15
Dawnbringer v Censer      0.81   0.65   0.28   0.19   0.10        0.16
NO COLD OPEN
Gravemourn v Dawnbringer  0.77   0.50   0.25   0.17   0.12        0.27
Widowmaker v Goreshard    0.77   0.49   0.26   0.17   0.10        0.28
Nightfell v Emberedge     0.79   0.47   0.24   0.18   0.11        0.32
Slagheart v Lightkeeper   0.78   0.46   0.21   0.13   0.09        0.32
```

**The cold open cuts the loss in second 2 from 0.298 to 0.158 — a 47% smaller
cliff — and does essentially nothing else.** Survival to 0:02 goes 0.48 → 0.67.
Every advantage the cold open holds for the remaining forty seconds was bought
in that one second. This is a cleaner result than v31's summary statistics: an
intervention aimed at a specific window moved that window and only that window.

It is also the strongest reason to believe the effect is real rather than a
fight-quality artifact. Four fights with nothing in common produced the same
change at the same second.

# 2. THE TAIL DOES NOT RESPOND TO CONTENT

Re-base every curve so the 0:05 cohort is 100% and ask who is left afterwards:

```
                          r10/r5  r20/r5  r30/r5   mean tail
COLD OPEN mean              0.72    0.46    0.35     0.436
NO COLD OPEN mean           0.68    0.44    0.33     0.429     difference +1.6%
```

Ranked by tail, the two groups **interleave completely**: Emberedge (cold, 0.495),
Ironhail (cold, 0.483), Nightfell v Emberedge (base, 0.453), Slagheart (base,
0.444), Gravemourn (base, 0.414), Widowmaker (base, 0.405), Axiom (cold, 0.395),
Dawnbringer v Censer (cold, 0.371).

These eight videos are not similar content. One has an ultimate as both the
killing blow and the KILL cut; one has a nine-shard Slagburst at the mechanic's
ceiling; one finishes on 2 HP of 300; one earns no cinematic cut at all. **That
variation moves the post-0:05 tail by 1.34× between best and worst, and the
ordering is uncorrelated with anything we did on purpose.**

## The hazard rate says why

```
                       hazard, seconds 0-3      hazard, after 0:05      ratio
cold open                    0.182                    0.040             4.6x
no cold open                 0.303                    0.040             7.7x
```

After 0:05 every video sits at **0.032–0.050 departures per second per surviving
viewer**, and stays there. There is no elbow. Taking each video's three largest
hazard spikes after 0:05, they cluster at 0:05 itself and at the last few seconds
before the video ends — **not at any shared mid-video moment**. The stickiest
stretch of every video is 0:15–0:30, where hazard drops to 0.020–0.056.

A comprehension failure — *"I can't tell who's winning, I'm out"* — would show up
as a cluster of departures at a particular moment. It does not appear. What the
tail looks like is memoryless departure: a fixed small chance per second of
scrolling on, independent of what is on screen.

**Caveat, and it matters.** All eight videos share one presentation. This sample
proves that *fight-to-fight* variation does not move the tail. It cannot prove
that a *presentation* change would not, because none has been tried. The health
rework is a bigger change than picking a different fight. But nothing in this
data predicts it will move the tail, and the honest prior is that it will not.

# 3. PRICING THE TWO LEVERS

Priced at the best shape **this channel has already produced**, rather than at
perfection:

```
                         now      front (best r1+r2)     tail (best post-0:05)
cold-open mean          9.42s      9.78s   (+4%)          10.32s   (+10%)
```

The front lever is nearly spent — the cold open already took it, and Axiom is
*already* at the best observed r(1) and r(2). What remains at the front is
**second 1**: every video loses 15–23% of viewers before the one-second mark,
the cold open barely touched it (0.222 → 0.172), and the ceiling on closing it
completely is +16% to +23%. The opening frame is still a near-empty dark arena
with the relics apart — v28 open decision 3, never actioned.

So on retention alone, Rick's instinct is defensible: the tail has more remaining
headroom than the front. §2 is the reason to be sceptical of collecting it.

# 4. THE FINDING THAT OUTRANKS ALL OF THIS

```
                          views   likes   comments   SHARES   saves
Dawnbringer v Censer        278       8          2        0       0
Emberedge v Thornwake       301       5          4        0       2
Ironhail v Goreshard        287       8          0        0       1
Axiom v Nightfell           327       9          2        0       0
Slagheart v Lightkeeper     247       7          1        0       0
Widowmaker v Goreshard      300       4          0        0       2
Nightfell v Emberedge       498      10          1        0       3
Gravemourn v Dawnbringer    325      10          7        0       0
                          -----                        -----
                           2563                            0
```

**Zero shares across 2,563 views.** Not low — zero, on every video pulled. Likes
run 2–3% of views, which is ordinary. Saves are 0–3. Comments are alive.

Shares and rewatches are the main currency TikTok pays reach in. This is the
mechanical answer to v31's open question — *retention up 44%, reach flat* — and
it is a better answer than "the algorithm has not paid yet." **A video nobody
sends to anybody does not travel, however long people watch it.** Every video on
this channel lands in the same 240–340 band because nothing escapes the initial
push, and nothing escapes the initial push because nothing gets shared.

**This reframes the health rework, and improves the case for it.** From
`sundered-crown-health-legibility.md` §2, written before any of these numbers
existed:

> *the payoff of every short is a number the video never states. The week-1 notes
> celebrate 2 HP of 300, won on 12 HP, Ironhail on 8 HP. That is the editorial
> value of the slate, and it is currently unreadable on the device the slate is
> made for.*

That is a **share** argument, not a retention argument. The reason to make the
health readable is that the ending is the thing worth sending to someone, and
right now the viewer cannot see it happen. Graded on mid-video retention, the
rework will probably read as a null. Graded on shares, saves and completion, it
is aimed at exactly the thing that is broken.

---

# Open decisions

1. **Ship the health rework — but register it against the right metric.**
   `sc-health.html` `3a2f369554bcefb1` is built and unshipped. **Prediction to
   register before filming: shares > 0 and saves per view roughly double.
   Post-0:05 hazard does NOT move** (it sits at 0.032–0.050 across every video
   ever posted). If watch time rises and the hazard curve is unchanged, the gain
   came from somewhere else and should be found before it is credited.
2. **Do not ship it into the middle of the cold-open read.** Short-11
   (`Gravemourn v Heartwood`, aweme `7675630746765200654`) went up today and has
   no retention data yet; short-12 is next. Finish the slate on
   `sc-cardspin.html`, then change one thing.
3. **"If this trend continues" — the trend is down, not up.** The four cold opens
   run 13.78 → 11.72 → 11.33 → 8.11s. Expect short-11 near the middle of that
   range, not at the top of it. The read is what settles whether short-08 was a
   bad fight or the start of decay.
4. **Second 1 is the cheapest unclaimed win at the front.** 15–23% of every
   audience leaves before the one-second mark, looking at a dark near-empty
   arena. Ceiling +16–23%, and it is a capture-start change.
5. **Nothing here touches discovery.** 89–98% of traffic is For You; hashtags,
   sound and post time have never been varied. If §4 is right, the share rate is
   the ceiling on reach — but the hypothesis that a legible payoff produces
   shares is a hypothesis, and one video will not test it.

---

# 5. SECOND 1, MEASURED — added after Rick asked whether to build for it

I proposed second 1 as the cheapest remaining win. Testing that proposal
weakened it in a specific and useful way.

## The fights were ALREADY picked for fast opens

`firstbeat.py` on the filming build `sc-cardspin.html` `ec9b8d753235385d`,
144 matches across six pairings:

```
first CLANK       min 0.87   p25 1.78   median 3.18   p75 4.58   p90 7.78   max 18.18
a clank has landed by 1.5s in 16.7% of matches · by 2.0s in 31.2% · by 3.0s in 47.9%
```

The median fight has nothing happen for **3.18 seconds**. But the shipped
shorts are not median fights — `ultscan.py --max-open` already selected them:

```
short      fight                    1st clank   1st hit |  r(1)   r(2)
short-10   ironhail v goreshard        2.03s      1.84s |  0.85   0.68
short-09   emberedge v thornwake       1.68s      3.53s |  0.80   0.65
short-08   dawnbringer v censer        1.86s      1.68s |  0.81   0.65
short-11   gravemourn v heartwood      1.59s      3.73s |    --     --
short-12   widowmaker v aureole        2.02s      1.60s |    --     --
```

**Across the three shipped cold opens, an earlier first clank does not predict
better survival — it runs mildly backwards.** short-10 has the LATEST clank of
the three (2.03s) and the BEST r(1) and r(2). With n=3 and a spread of 0.35s
this is underpowered rather than contradictory, but it kills the obvious
version of the fix: **moving the first impact a few tenths earlier is a lever
that is already pulled and appears to be exhausted at this range.**

## What the opening second actually looks like

Rendered from the same build and the same seeds, at t=0.0, 1.0 and 2.0s
(`/home/claude/tt/opening-frames.png`):

```
mean frame luminance, 0-255      t=0.0s   t=1.0s   t=2.0s
short-10  ironhail v goreshard     19.3     19.6     20.2
short-09  emberedge v thornwake    20.8     21.3     21.1
short-08  dawnbringer v censer     28.9     29.5     26.5
separation between relics at 1.0s: 388-537 sim units (they meet around 2s)
```

**8–11% mean brightness.** Two small objects at opposite corners of a large dark
arena, a faint sigil ring between them, and a lot of nothing. That is the frame
that has to win a thumb in a feed. "Near-empty dark arena" was accurate.

Note that short-08 is the *brightest* of the three and the worst performer, so
"brighter is better" is not established either. What short-08 does show, plainly
and visually, is the palette collision v28 §2 flagged: at t=0 and t=1 Dawnbringer
and Censer are two similar pale cream blobs, where short-10 is gold against
crimson and short-09 orange against green. The statistical test in v31 §4 pointed
the other way; the frame supports the concern. Still not settled.

## What this changes

The remaining opening-second lever is **presentation, not timing** — brightness,
how much of the frame the relics occupy, and whether the pair reads apart at a
glance. None of that is prototyped, and the one version of the fix that was cheap
to reason about is the one the measurement just ruled out.

# Open decisions (revised)

1. **Nothing changes for short-12.** One video left in the slate; changing a
   variable now costs the read that this whole session exists to protect.
2. **Next build should be the health rework, not the opening frame** — it is
   already built (`sc-health.html` `d0bb4890b19edc47` in this seed), the opening
   frame fix is not specified, and §4's zero-share finding is a bigger problem
   than §3's watch-time headroom. Grade it on shares/saves/completion.
3. **Opening frame is the build after, and it needs a contact sheet first.**
   `health_sheet.py` and `stage_shot.py` are the right pattern: render t=0 for
   every pairing at phone scale and judge brightness, relic scale and pair
   contrast before it costs a posting slot. Do not spend the slot on a timing
   change — that is what the table above rules out.
4. **If the goal is watch time rather than reach, invert 2 and 3.** The opening
   frame has a +16–23% ceiling on watch time and the health rework probably has
   ~0%. The recommendation above assumes reach is the binding constraint, which
   is an argument from §4, not a fact.

---

# 6. THE CARD — Rick was right, and it is the biggest lever on the board

Rick: *"i feel like we are seeing a huge dropoff during the fight card. it makes
me feel like it needs to go to keep eyes on the action."*

## What the card actually is

`CONFIG.intro = { dur: 4.0, clash: 0.46, reveal: 0.50 }`, and while it is up
`step()` returns early after decrementing `introT` — **the simulation is frozen.**
`drawIntro` covers ~58% of the frame with two cards and puts the rest behind an
80% scrim. It is a four-second dead stop, not a slow passage.

The cold open did not remove it. It moved it: card-first videos run the card at
video seconds 0.0–4.0; cold opens raise it on the first clank, so ~1.9–5.9.

## That makes it a natural experiment

If the card is what costs the audience, the hazard spike has to MOVE with it.

```
departures/s        s1     s2     s3     s4     s5     s6     s7     s8
card first        0.222  0.382  0.303  0.186  0.120  0.123  0.036  0.076
cold open         0.172  0.190  0.183  0.257  0.214  0.125  0.055  0.045
ratio              0.77   0.50   0.60   1.38   1.78   1.02   1.53   0.59
whose card is up   base   base   BOTH   BOTH   cold   cold   none   none
```

**The peak moves.** Card-first peaks at second 2 (0.382). Cold open peaks at
second 4 (0.257) — two seconds later, tracking a card raised ~1.9s later. By
second 6, when both cards are down, the two are identical (1.02x).

The cleanest single cell is **second 5**: the card-first video is playing the
fight, the cold open is showing the card, and the cold open sheds viewers at
**1.78x** the rate. Same second of video, different thing on screen.

```
card-first videos lose 71-75% of the audience present when the card appears
cold-open videos lose 55-63%
```

## What it is worth

Three interventions, priced against a measured fight-playing hazard of 0.158/s
(the mean of cold-open seconds 1–3 and card-first seconds 5–6 — the only two
places in the dataset where the fight is on screen early in a video):

```
                                mean effect on watch time
kill the card entirely                  +69%     video also gets 4s shorter; priced in
halve it to 2.0s                        +22%
run the fight under it, keep 4s         +15%     keeps the names and the VO
```

**+69% is an upper bound and here is exactly why it is soft:** the model lets
the enlarged cohort (68% surviving instead of 29%) decay at the rate the small,
self-selected cohort actually decayed at. A bigger crowd is a less committed
crowd and would bleed faster. The **lower** bound needs no model: the card
window runs at 0.195/s against a fight's 0.158/s, so those four seconds are
being bought at ~1.24x the going rate even if not one recovered viewer stays.

## Ranked against everything else measured this session

```
kill the 4s freeze                 +69%   upper bound, not built
the cold open                      +44%   DELIVERED
halve the card to 2s               +22%
close second 1 completely          +16-23%  theoretical, unreachable
run the fight under the card       +15%   keeps names and VO
best-in-set post-0:05 tail         +10%   the health-bar bet
best-in-set r(1)+r(2)               +4%
```

**Nothing else measured is close.** This was already on the board — v28 open
decision 3 listed "shorten the 4.0s card, run the fight live underneath it" as a
week-two candidate. It now has a number, and the number is bigger than the cold
open's.

## What the card is carrying, and what a replacement has to keep

Killing it outright costs the two relic names on screen, the matchup framing,
the VO that rides the card window, and the 0.46s clash beat with its seal bell.
For a viewer who has never seen the game, the names are how the picture is
parsed. **The design question is not "card or no card" — it is how to keep the
naming without stopping the fight.** A lower-third name plate over live action
gets most of the +69% while keeping everything the card carries; that is the
version worth prototyping first, and it is not the version the current builder
supports.

# Open decisions (revised again)

1. **The card outranks both the health rework and the opening frame.** It is
   the largest measured lever on the channel, and it is larger than the cold
   open that this session was convened to evaluate.
2. **Still do not change anything for short-12.** One video left. The cold-open
   read is nearly closed and it is worth closing.
3. **Prototype a live-action name plate, not a shorter card.** Shortening is the
   safe +22%; not freezing the sim is where the rest of it lives. Both are
   builder changes to `cinema_clip.py` and `CONFIG.intro`, neither touches the
   simulation, so `engine_ab` should stay bit-identical.
4. **Register the prediction:** if the card is the cause, killing the freeze
   moves r(6) from ~0.28 to ~0.45+ and leaves the post-0:05 conditional tail
   unchanged at 0.43. If the tail moves too, something else changed.
5. **This reframes the reach question rather than answering it.** +44% watch
   time bought no reach. Whether that is "watch time does not drive reach here"
   or "+44% was too small to trip anything" is untestable at n=4 — but the card
   fix is a much bigger swing than the cold open was, and it is the honest test
   of the theory.
