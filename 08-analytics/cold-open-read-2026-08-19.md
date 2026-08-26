# THE COLD OPEN, RE-READ AT MATURITY — 2026-08-19

Every number below was read off TikTok Studio's per-video page today, 19 Aug,
between 06:30 and 06:50 PDT. It supersedes the v28 read in
`sundered-crown-posting-schedule-week1.md`, which was taken on 16 Aug with two
cold opens live, one of them two hours old.

**Rick's read going in — "very marginal improvement in retention" — is half
right, and the half that is wrong matters more than the half that is right.**

---

## 1. THE NUMBERS

```
COLD OPEN                       posted      len  views   watch   %len   full   stopped
Axiom v Nightfell            8/16 02:14     63    327   13.78s  21.9%   7.1%    0:04
Ironhail v Goreshard         8/16 15:56     44    287   11.72s  26.6%  13.5%    0:02
Emberedge v Thornwake        8/17 08:15     48    301   11.33s  23.6%   7.9%    0:01
Dawnbringer v Censer         8/18 08:15     48    278    8.11s  16.9%   4.6%    0:01

NO COLD OPEN (card first)
Ironhail v Widowmaker        8/13 23:08     42    240    9.71s  23.1%   7.7%    0:01
Farwarden v Nightfell        8/14 16:46     54    652    8.56s  15.9%   4.8%    0:02
Nightfell v Emberedge        8/14 16:46     48    498    8.41s  17.5%   6.9%    0:02
Gravemourn v Dawnbringer     8/13 23:27     47    325    7.87s  16.7%   5.0%    0:02
Slagheart v Lightkeeper      8/15 12:47     47    247    7.33s  15.6%   6.4%    0:02
Widowmaker v Goreshard       8/14 17:13     40    300    7.24s  18.1%   3.9%    0:02
Dawnbringer v Grudgebearer   8/13 15:03     42    302    6.85s  16.3%   3.5%    0:02
Grudgebearer v Thornwake     8/13 23:26     45    337    6.46s  14.4%   3.8%    0:01

EXCLUDED — the mean rests on too few plays to mean anything
Grudgrwaker v Thornwake      8/12 16:41     38     18   24.87s  65.4%  14.7%    0:01
Grudgebearer v Thornwake #2  8/14 18:29     31     31   15.09s  48.7%  20.8%    0:02
```

Both excluded posts sit at the very top of the channel on watch time and
completion. That is the signature of a post seen almost only by people who went
looking for it, not of a video that holds an audience. Excluding them is stated
rather than done quietly, because **including them would put the no-cold-open
average above the cold-open one** and the whole read would flip on two posts
with 49 views between them.

## 2. WHAT SURVIVES

```
                        cold open   baseline   difference   Mann-Whitney   exact perm
average watch time        11.23s      7.80s      +44.0%       p=0.014       p=0.008
watch time / video length  22.25%     17.20%     +29.4%       p=0.024       p=0.024
watched full video          8.28%      5.25%     +57.6%       p=0.055       p=0.042
views                     298         363        -17.8%       p=0.770       p=0.741
```

**Retention moved. Distribution did not.** On n=4 against n=8, an exact
permutation test over all 495 arrangements puts the watch-time gap at p=0.008 —
that is not noise. The views column is flat-to-negative and nowhere near
significant, and **the two best-distributed videos on the channel (652 and 498
views) are both baseline.** Whatever the cold open is buying, the algorithm has
not yet paid for it in reach.

Length is a real confound and was tested rather than assumed: across all twelve
videos, length and watch seconds correlate at r=+0.60 (p=0.04), and the longest
video on the channel is a cold open. Correcting for it cuts the effect roughly
in half — from +44% to +29% — but does not erase it.

## 3. TWO v28 CLAIMS THAT DO NOT SURVIVE

**(a) "The drop-off point moved."** It did not. Axiom's 0:04 is unique on the
channel and did not repeat. Two of four cold opens read **0:01** — worse than the
baseline mode of 0:02. Baseline videos also read 0:01 three times. The metric is
noisy at this granularity and carries no signal in either direction. v28 made it
the headline; it should not have.

**(b) The pre-registered >9s threshold was set against an incomplete baseline.**
`Ironhail v Widowmaker` (8/13, no cold open) reads **9.71s / 23.1% of length** —
above the threshold, and inside the cold-open range on the length-corrected
metric. It is not in the v28 baseline table. Clearing a bar that one control
video already cleared proves less than v28 claimed.

The v28 worry that the early read was flattered by a first, more-engaged pool is
also **wrong, in the useful direction**:

```
                       age at v28 read   watch then   watch now   drift    views then/now
Axiom v Nightfell            16h           13.54s      13.78s    +1.8%       320 -> 327
Ironhail v Goreshard          2h            9.98s      11.72s   +17.4%       266 -> 287
```

Maturation runs **upward**, and nearly all of it lands inside the first day.
Views are flat — +7 and +21 over three days. These videos are finished
distributing. So Dawnbringer v Censer, read at ~22h, is within a few percent of
final. **Its 8.11s is bad, not young.**

## 4. WHAT RICK IS ACTUALLY SEEING

The cold-open sequence declines monotonically in the order posted:

```
13.78s  ->  11.72s  ->  11.33s  ->  8.11s
21.9%       26.6%       23.6%       16.9%
```

The fourth is inside the baseline field on both metrics. That is the "marginal"
feeling, and it is a real pattern in the data — but it is one video, and it is
also the one v28 flagged as a risk **before any numbers existed**.

### The palette hypothesis, and why it is not yet a finding

v28 §2 kept short-08 knowingly: Dawnbringer and Censer are both `sanctified`, so
both balls carry the same palette. It is the only same-palette fight in the
cold-open set and it is the worst performer. Inside the cold-open set the story
is perfect:

```
COLD OPEN     contrast mean 24.0%   ·   same-palette 16.9% (n=1)   SUPPORTS
BASELINE      contrast mean 17.1%   ·   same-palette 18.1% (n=1)   CONTRADICTS
```

**The one independent test of the hypothesis points the other way.** Widowmaker
v Goreshard — both `bloodsworn`, same palette — reads 18.1%, above the baseline
mean. One video each side is not a test. The hypothesis is live and cheap to
check; it is not established, and it should not be acted on as though it were.

## 5. THE THING NOBODY HAS EXPLAINED

Two of four cold opens lose the modal viewer at **0:01** — before the cold open
has shown anything at all. That is not "the cold open does not work." It is a
first-frame problem, and v28 open decision 3 already named it: the opening frame
is a near-empty dark arena with the relics apart. The cold open fixed the
*second* four seconds. The first second was never touched.

---

# Open decisions

1. **Are there three cold opens or four?** Rick says three; the channel shows
   four (Axiom, Ironhail, Emberedge, Dawnbringer), and v28 records Axiom as a
   cold open. Dropping it was tested rather than guessed: the raw-seconds effect
   falls from +44% to +33% (perm p=0.024), and the **length-corrected effect does
   not move at all** — +29.4% to +30.1%. So Axiom's headline advantage was mostly
   its 63 seconds, and the finding survives without it. What is lost is the only
   0:04 drop-off on the channel, which §3(a) already discounts.
2. **Is short-08 a bad fight or the start of decay?** Shorts 11 and 12 answer it
   and are already built. Both are contrast palettes; short-11 has the fastest
   open in the slate at 1.59s. If 11 lands back at 11–13s, short-08 was the
   fight. If it lands at 8s, the effect is decaying and week two needs a
   different lever. **Recommend: post both unchanged, change nothing else.**
3. **Retention is up and reach is not.** That is the strategic question and it is
   Rick's, not the data's: keep optimising the front door on the theory that
   watch time eventually buys distribution, or accept that ~300 views is a
   discovery problem (hashtags, posting time, sound, hook text) that no amount
   of retention work touches.
4. **Week two aims at second 0, not seconds 0–4.** The opening frame is a dark
   near-empty arena. That is a one-line change to the capture start and is
   testable against the 0:01 reading.
5. **Cross-platform is still an uncontrolled confound.** YouTube was never
   reconciled with this read.
