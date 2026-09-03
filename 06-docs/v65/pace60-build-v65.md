# v65 — THE MINUTE, BUILT. `sc-minute.html`, and the mean is 60.2s.

**2026-09-02, Claude Code.** Built to `06-docs/v65/pace-60-v65.md` §5, on
Rick's ruling of **S = H = 1.30** and **accept the pairing ceiling**.
`tools/pace60_build.py`, one link: `02-chain/sc-lastthree.html` →
`02-chain/sc-minute.html`.

Runtime: **the repo's pinned pair** — Chromium 151 / playwright 1.62.0. The
design document was priced on Chromium 141 in a Cowork container, so §1 below
is the reproduction control and it is the first thing to read.

```
combat.baseHP        400 -> 520
SECOND SEAL          t: 21 -> 27      collapse.startT 21 -> 27, in the same edit
THIRD SEAL           t: 49 -> 64
timeout              120 -> 156       a backstop, not a win condition
```

---

## 0. THE DESIGN REPRODUCES ON THE PINNED RUNTIME, TO A TENTH OF A SECOND

This is the one thing that had to be checked before anything else was
believed, and it is the check that could have come back wrong.

```
                              mean   med   p90    max   t/out  ults   worst pairing
v65 §1  today      Cr141      47.5  47.7  60.3   79.9     0     4.2   Lightkeeper/Farwarden 77.7s
BUILT   sc-lastthree Cr151    47.5  48.1  60.2   92.4     0     4.2   lightkeeper/farwarden  78.0s

v65 §3  1.30/1.30  Cr141      60.1  59.7  75.7  107.5     0     5.5   Lightkeeper/Axiom 99.2s
BUILT   sc-minute    Cr151    60.2  59.7  75.7  115.9     0     5.5   farwarden/axiom  102.1s
```

`pace_roster_probe.py --cells 1.0:1.0 --n 3`, 528 pairings × 3 seeds = 1,584
fights each. **Mean, median, p90, timeouts and ults per fight all land on the
published numbers**, and the worst pairing is the same set of four relics.
Only the MAXIMUM moves (92.4 against 79.9 on the control, 115.9 against
107.5 on the build) — a maximum is one fight out of 1,584 and the two
runtimes are known to disagree on individual fights while agreeing on
distributions (`docs/RUNTIME-DRIFT.md`). **Nothing in `06-docs/v65/pace-60-v65.md`
needs re-reading on the other branch**, which is not something this project
has been able to say about a Cowork-priced document before.

**Rick asked for the average closer to a minute. It is 60.2 seconds.**

## 1. What was built, and why the collapse is inside the same edit

Six anchored edits, `tools/pace60_build.py`. Four are the numbers Rick ruled;
two are prose that would otherwise have gone stale, which in this codebase is
part of the change rather than tidying after it.

| # | edit | why |
|---|---|---|
| 1 | `baseHP` 400 → 520 | H = 1.30 |
| 2 | SECOND SEAL `t` 21 → 27 | S = 1.30 |
| 3 | THIRD SEAL `t` 49 → 64 | S = 1.30 |
| 4 | `collapse.startT` 21 → 27, **in the same tuple as the comment above it** | the hall must start closing ON the seal |
| 5 | `timeout` 120 → 156, comment rewritten | see below |
| 6 | curse's *"against a 120s timeout"* → 156s | the comparison is still true; the figure was not |

**Edit 4 is one edit and not two on purpose.** The comment above `collapse`
has said since 2026-08-29 that the hall starts closing on the Second Seal
because *"a wall that starts closing at an unexplained clock time is exactly
the invisible correction this project deleted `seek` over"* — a rule that
lives only in prose is a rule waiting to be broken by the next builder that
scales one of the two. So the builder **reads both numbers back out of its
own output and refuses to write if they disagree**, and the comment now
records that the rule has been applied twice (15 → 21 → 27) rather than
stated once.

**Edit 5 is the comment as much as the number.** The block standing over
`timeout` was written for 120: it cited a 1,200-fight sweep, a 76.6s maximum,
*"120 is 57% above the observed maximum"*, and a music bed of
`CONFIG.timeout + intro.dur + 6` — and **`intro.dur` has not existed since
`cardstrip_build.py` removed the fight card**. Every figure in it was about a
build that no longer exists and one of its fields was gone. The replacement
carries the roster measurement, the 45% margin over the longest fight anybody
has measured, the bed at 162s against 126s, and Rick's ruling on the pairing
ceiling.

## 2. The gates

```
pace60_build      6/6 anchors, 7/7 upstream markers, seal == collapse, braces
                  and block comments balanced
pace_roster_probe mean 60.2s on all 528 pairings x 3 seeds, 0 timeouts   §0
engine_ab         135 of 135 matches DIFFER  -- the point of the change
chain_audit       duskreave_build.py 28/28 inserts survive into sc-minute
text diff         72 lines, and they are the six edits and the stamp
verify --n 40     see §3
```

**THE TEXT DIFF IS THE STRONGEST OF THESE AND IT IS ALSO THE CHEAPEST.**
`sc-lastthree.html` against `sc-minute.html` is 72 diff lines: one stamp, four
numbers, two rewritten comments, and nothing else. Every upstream insert
survives because none of them was touched — that is provable by reading the
diff, where `chain_audit` can only assert it insert by insert.

**`engine_ab` FAILING IS THE PASS HERE.** 135 of 135 matches differ, mean
duration up about 14 seconds on the six-relic sample (51.8 → 66.2 on the first
pairing, 42.3 → 61.2 on the third), winners changing on 2 of the first 3
seeds. A pace change that left any fight identical would mean the constants
were not being read.

## 3. verify — 11/13, and BOTH REDS ARE THE CLOCK

`verify.py --game ../02-chain/sc-minute.html --n 40`, 21,120 matches in
1,279s. **Mean duration 60.1s** — a third instrument, on 40 seeds a pairing
rather than 3, landing on the roster probe's 60.2.

```
  PASS  no JS errors or page exceptions
  PASS  every status and ultimate has viewer-facing text
  PASS  all 528 pairings ran
  PASS  every match resolved                   0 unresolved
  PASS  both sides can win every matchup
  PASS  timeout rate <= 10%                    0/21120 = 0.0%
  PASS  every relic winrate in 30%-70%         Heartwood 35.2 .. Ironhail 60.6 (25.4pp)
  FAIL  every pairing mean duration in 18-70s  Lightkeeper/Farwarden 99.0s
  FAIL  overall mean duration in 28-54s        60.1s
  PASS  every pairing clanks at least once
  PASS  no pairing resolves on fewer than 6 hits
  PASS  capture path pins the canvas to 1080x1920
  PASS  renderer draws a non-blank frame
```

**THE FIRST RED IS THE KNOWN ONE AND RICK RULED IT.** Lightkeeper/Farwarden
has failed this check on every build since `pace_build` — 74.6s, 75.7s,
76.9s, 74.8s — and it is now **99.0s**, red by twenty-nine seconds instead of
by five. v65 decision 2 is to accept it, as `pace_build` accepted it. Nothing
new is wrong; the same four relics are further out.

**THE SECOND RED IS NEW, AND THE BUILD FAILED IT BY DOING EXACTLY WHAT RICK
ASKED FOR.** `verify`'s overall-mean band is **28-54s**, written for a game
whose mean was 37.3s and left alone when `pace_build` took it to 49.3 — the
top of the band, which is why it never fired. A 60-second target cannot fit
inside it. **The band now contradicts a ruling.**

**IT WAS NOT WIDENED HERE, AND THAT IS DELIBERATE.** A gate moved by the
build it is judging is not a gate, and this one is read by every future build
in the chain, so it is chain-wide and Rick's — the same shape as the pairing
band he has now declined to move twice. What is NOT acceptable is leaving it
unexplained: a session that reads `11/13` next month must be able to tell a
band that is stale from a build that is broken, and that is what this section
is for.

**AND THE PREDICTION THAT DID NOT LAND IS THE USEFUL ONE.** The design
expected *"verify to want two or three damage touches, the way `pace_build`
wanted Grudgebearer's"*. **It wants none.** Every one of the 33 relics is
inside 30-70% — Heartwood 35.2% to Ironhail 60.6% — so the winrate check
passes outright and no damage number needs to move. The roster spread does
widen: 25.4pp here, against the 20.0pp `06-docs/v63` measured on this branch,
and the paired n~96 probe agrees on the direction (24.0 -> 31.2pp). **Nobody
is out of band and the spread is worth watching, which is a different
sentence from "somebody needs tuning".**

**THE PER-RELIC DRIFT TABLE DOES NOT REPRODUCE, AND IT IS BELOW ITS OWN
RESOLUTION.** v65 §4 named Ravelbone and Marrowdraw as the big losers and Axiom
as the big gainer, at n~96 a relic. Re-run here on the pinned runtime with the
same seeds, the biggest movers are **Aureole -16.7, Oathwound -12.5 and
Gravemourn +12.5**, and Ravelbone and Axiom barely move. The document said
±5pp at 1σ, which is ±7pp on a difference, so 12-17pp is two to three sigma
and the two runs disagree about who is who. **That table names nobody
reliably** — it was right that SOMETHING moves and wrong about what, and
`verify --n 40` is the instrument that settled it by finding nothing outside
the band at all.

## 4. What did not get done, and one thing that was found on the way

**THE CHAIN IS FORKED AND THIS LINK INHERITS THE SHORTER BRANCH.** Auditing
`gloamwire_build.py`'s inserts into this build turned up **10 of 21 missing**
— the held trio, the nova, the drawn explosion and Crossweave's voice
(`S7`, `S7B`, `S8`, `S9`, `S11`). They are missing from `sc-lastthree` and
from `sc-static` as well, so **this is not something the pace change did**:
Crossweave's stages 7-12 live only in `sc-nova.html`, because that carry was
re-applied as a new link on top of `sc-bloodletting` at the same time the
Duskreave branch was growing from the same parent. The two branches are:

```
sc-bloodletting -> sc-nova         32 relics, FULL Crossweave, the build of record
sc-bloodletting -> sc-duskreave -> ... -> sc-lastthree   33 relics, Crossweave stages 1-6 ONLY
                                       -> sc-arclight -> ... -> sc-static  34 relics, blocked at stage 4
```

`sc-minute` is on the second branch, which is where v65's numbers were
measured and where the app's working-tree pointer already points. **Whoever
reconciles the branches will have to re-apply either the Crossweave carry or
this pace change on top of the other**, and this one is four constants and
two comments, so it is much the cheaper of the two to move: re-running
`pace60_build.py --src <other link>` is one flag, and the builder refuses if
the source already carries the numbers.

**`chain_audit.py` CANNOT SEE A BUILDER SHAPED LIKE `pace_build.py`, WHICH IS
OPEN ITEM 31 FOR THE FIFTH TIME.** Pointed at the first cut of this builder it
answered *"no `*_NEW` inserts found ... nothing to audit, which is itself a
failure"*. Its tuple-table discovery reads the LABEL from a row's first
element and the BODY from its last, so `(old, new, label)` — the shape
`pace_build.py` uses, and the shape this builder was written in because it is
imitating `pace_build.py` — is invisible to it. The builder's table was
reordered to `(label, old, new)` and the tool then found 2 of 6 (the two whose
replacement is multi-line; a single-line insert has no body it will accept).
**The reorder is provably inert: the output's sha256 is `7d8034a57ceb1a6d`
before and after.**

**IT WAS NOT FIXED IN THE TOOL, AND THAT IS DELIBERATE.** Accepting
single-line bodies would make every `(old, new, label)` builder report its own
LABELS as inserts — `"grudgebearer dmg 27.93 -> 23.50 (62.8% -> 53.8%)"` is
over the length filter and appears in no build — so the widening that looks
obvious would turn a tool that audits nothing into a tool that fails loudly on
correct chains. `curse_window_build.py` is invisible to it too and was
therefore not audited here.

**AND NOBODY HAS WATCHED A SIXTY-SECOND FIGHT.** §5 of the design document
asks for one end to end in the app before this is called done, and that is
CLAUDE.md §4.0: the thing this change alters is the LENGTH OF EVERY PICTURE —
how long a set-piece has to breathe, how many of them land in one fight (4.2
→ 5.5), and whether the hall closing eleven seconds later reads as pacing or
as a lull. No number here can see any of that.

## 5. THE CLIP PIPELINE, HANDLED

`06-docs/v65/pace-60-v65.md` §6 read the pipeline end to end against a minute
and fixed two things (`MAX_SECONDS = 180` in `shorts_build.py`, and
`cinema_clip.py`'s whole-fight cap moved off a bare `150` to
`CONFIG.timeout * 1.3 + 16`, read off the page). Both were checked and kept.
Three more went in here.

**THE LADDER FILTER NEEDED A GUARD, BECAUSE ITS FAILURE MODE IS SILENT AND
GREEN.** The fix that stops a length failure walking the loudness ladder is
`all(ok for k, ok in m["pass"].items() if k in LADDER_MARKS)` — and `all()`
over an empty generator is `True`. If a mark in `measure()` is ever renamed
and `LADDER_MARKS` is not, that test passes on the FIRST rung forever: the
ladder stops climbing, a genuine true-peak failure ships at 0.79, and nothing
anywhere says so. It asserts its own inputs now and exits with the two lists
printed. **A check whose failure mode is "everything passes" is the one that
has to be checked.**

**`pick_fight.py` WAS ABOUT TO EXCLUDE MOST OF THE ROSTER.** Its `--secs`
default was a flat `18,55`, written when the mean fight was 47.5s. At this
pace the median is 59.7s and the p90 is 75.7s, so **the tool whose entire job
is finding a fight worth filming would have rejected the typical fight** and
reported "NOTHING QUALIFIES" on most pairings. The ceiling is read off the
build now: `0.46 x CONFIG.timeout` is **55.2 on the pace_build clock — the old
default, reproduced — and 71.8 here**, which is the same quantile of the same
distribution. Confirmed live: `--secs from the build: 18-71.8s`. Its docstring
also measured closeness *"against baseHP 300"*; the code has read `baseHP` off
the page since it was written, so only the prose was stale.

**AND THE FRAME-COUNT COMMENT THE DESIGN DOCUMENT LEFT.** `app/main.js` said a
full capture is *"~1,400-2,800 frames and 3-4 minutes"*, which is the number
the whole "this cannot be a call that returns a file" argument rests on. It is
2,800-4,000 and 4-5 minutes now, with the ~7,000-frame worst pairing named.

**MEASURED END TO END RATHER THAN REASONED ABOUT.** `shorts_build.py --game
02-chain/sc-minute.html --a duskreave --b gravemourn --seed 20`, a 58.1s whole
fight — the one path that exercises the new cap, the 180s gate and the ladder
in a single run:

```
  minute-first-cut.mp4
  1080x1920 h264+aac  64.3s  38.2MB  -15.8 LUFS  -2.0 dBTP  (limiter 0.63)
    PASS 1080x1920 · PASS h264+aac · PASS under 180s
    PASS -16..-13 LUFS · PASS TP <= -0.3
```

**5 of 5, and the delivered length is 64.3s** — the fight plus 6.2s of open
and verdict tail, which is the "+8s" §6 estimated. 3,855 frames, 455s to
render. **Under the code as it stood this morning this clip fails on `under
60s`, walks all three rungs of the ladder, ships at 0.50 / −4 dBTP and exits
1.**

**AND THE LADDER CLIMBED ON A REAL TRUE-PEAK FAILURE, WHICH THE STUB COULD NOT
SHOW.** Rung 0 measured **0.0 dBTP** against a mark of −0.3 and was rejected;
rung 1 at limiter 0.63 held it at −2.0. So the filtered test is doing both
halves of its job on real content — refusing to walk the ladder for a length
failure, and still walking it for the thing the ladder is for.
`07-shorts/v65/minute-first-cut.mp4`. **Nobody has watched it.**

## Open decisions

1. **WHICH LINK CARRIES THIS — still open, and now it has a second half.**
   v65 open decision 3 asked whether the pace lands on the app's
   `sc-lastthree` or on the Arclight chain. It landed on `sc-lastthree`,
   because that is where every number in the design document was measured and
   what the app's own pointer already names. **What §4 adds is that neither
   candidate carries the finished Crossweave** — only `sc-nova` does — so the
   real question is which branch becomes the trunk, and that is Rick's and the
   chain's, not this build's.
2. **THE APP POINTER.** `app/main.js` carries an uncommitted `GAME =
   sc-lastthree.html` against a committed `sc-nova.html`. It was left alone
   (it is somebody else's change and the last commit says so). **To watch a
   sixty-second fight it has to point at `sc-minute.html`**, which is one line
   — and moving it makes a 33-relic build with a partial Crossweave the thing
   the app shows. Rick's.
3. **WHETHER VERIFY'S BALANCE FINDINGS GET ACTED ON.** §3. `pace_build`
   answered its own with one damage touch (Grudgebearer 27.93 → 23.50) folded
   into the pace builder. No damage number is touched here, deliberately —
   the design document says which relic moved is verify's to say on the pinned
   runtime, and doing both in one link would leave the pace and the tune
   inseparable in `engine_ab`.
4. **THE PAIRING CEILING, RULED AND RESTATED.** Rick ruled accept. It is worth
   knowing that the same four relics — Lightkeeper, Axiom, Farwarden,
   Spellbreaker — have now been the answer three times running, and that
   tuning those four is the only thing that has ever been on the table for
   them.
