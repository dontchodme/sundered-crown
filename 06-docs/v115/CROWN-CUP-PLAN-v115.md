# THE CROWN CUP — a World-Cup-style tournament, one match per short (v115)

Cowork, 2026-09-27. Plan only — nothing here is built. Working name "Crown Cup I"
until Rick names it (§9.1).

**What this is.** Every relic in the game plays a tournament for the crown. One
fight is one short, posted two a day, and a viewer who opens any one of them can
tell where they are in the tournament and what the fight decides. The first
tournament (Weapon Balls World Cup 1, 2026-08) ran on the old Unity game with a
hand-driven screen-capture pipeline and stalled at 24 of 65 matches. This one
runs on our engine, where a fight is a seed and a short renders itself, so the
whole tournament can be rendered before the first post goes up.

## 0. Rick's rulings (2026-09-27)

| question | ruling |
|---|---|
| the field | **all 49**, once the design batch and the seven staves have shipped and he has had his eye on them. The build is frozen for the whole tournament. |
| the shape | **16 groups of 3, then a knockout from the round of 16.** |
| the pace | **two shorts a day.** |
| how a match is decided | **fixed by rule, in advance** — the fight's seed comes from the match itself, published before anyone sees a result. One fight per match; luck is part of the format, as it was in World Cup 1. |

## 1. The field and the shape

49 relics: the 42 of the grid (7 schools × 6 weapon types) and the 7 staves.
Sixteen groups of three hold 48, so the 49th is settled the same way everything
else is — by a fight.

```
video  1        PLAY-IN         the 49th relic v the last relic drawn, for the last group slot
videos 2-49     GROUP STAGE     16 groups × 3 matches; each relic fights twice
videos 50-57    ROUND OF 16     the 16 group winners
videos 58-61    QUARTER-FINALS
videos 62-63    SEMI-FINALS
video  64       THIRD PLACE     (recommended kept — it pairs with the final's eve, §9.2)
video  65       THE FINAL       posted alone on the last day
```

**65 shorts, 33 days at two a day.** Group stage days 1-25, round of 16 days
25-29, quarters 29-31, semis 31-32, third place day 32, final day 33.

**Why groups of three.** Every relic gets two shorts before anything is
eliminated, the group stage is 48 videos instead of World Cup 1's 72-for-48-relics,
and the shape has a property groups of four do not: the **third match of every
group is either the decider or the tiebreaker**, so the last short of each group
always carries a stake the band can name (§5.1).

**Group standings.** 3 points a win. Two wins takes the group outright (6 of the
8 possible outcomes). The other 2 outcomes are a three-way 1-1 tie — expect it
in about a quarter of the groups — broken by **HP remaining across the group**
(the winner's leftover HP in each win; a loss scores 0), World Cup 1's rule. If
that ties too, the lower draw number advances; the ledger states which rule
decided every group.

**Side balance.** The engine is measured "both sides" for a reason: the side a
relic starts on is not nothing. The group pattern is `P1 v P2, P2 v P3, P3 v P1`,
so every relic is side 1 once and side 2 once. In the knockout the relic with
the **lower draw number is side 1** — a rule that has nothing to do with
strength, stated on the bracket.

## 2. The draw

Random, from a published seed, with one constraint for the viewer's sake: **no
two relics of the same school or the same weapon type in one group.** Sixteen
groups, three different schools and three different weapons in each — no mirror
matches in the group stage, every group looks different. The knockout is
unconstrained.

The draw orders all 49. The first 48 fill the groups A-P greedily under the
constraint (re-shuffling from the same seed stream until a legal draw exists —
takes about a dozen tries on a 7×7 roster; checked); the 49th is the
**challenger**, who plays the last relic drawn for the last slot in group P.
The challenger has to be legal in group P too, or the draw re-rolls.

The roster is read off the frozen build (`AC.WEAPONS`), never typed — `oathwound`
displays as Goreshard and every new relic's id is the builder's, not the doc's.

## 3. How a match is decided — the rule

```
seed(match, k) = int( sha256("crown-cup-1/<fixture>/<side1 id>/<side2 id>/<k>")[:8], 16 ) & 0x7fffffff
```

`k` starts at 0. The fight is the first `k` that **ends in a kill** (a timeout is
a draw, and the tournament has no draws) **and whose director plan carries a
fatal cut** (without one the kill is filmed as ordinary air — `pick_fight.py`'s
hard filter, and the reason v41 lost two renders). Neither test looks at who
won. `k` is recorded in the ledger for every match; it should almost always be
0, and a match where it is not is still the rule's fight, not a chosen one.

What this replaces: `pick_fight.py` ranks candidate seeds by closeness and by
how much the director found to cut. Good for a one-off short; in a tournament
that is choosing the winner with a preference for drama. Here the rule picks,
and the person rendering finds out who won the same way the viewer does.

**Determinism is per runtime.** `(build, a, b, seed)` is the same fight on the
same V8 and not necessarily on another (`docs/RUNTIME-DRIFT.md`). So the whole
tournament — every seed test and every render — runs on **one machine, one
build file, the pinned Chromium 151**, and the ledger records the build's
sha256 and the machine. A fight re-rendered elsewhere is not evidence of
anything.

**Publish before computing.** The draw seed, the seed rule and the frozen
build's hash go into the ledger and onto the bracket page — committed — *before*
the group stage is rendered. After that the results are whatever the rule says.

## 4. Everything renders before day 1

Because the seed is a function of the match and the engine is deterministic,
results are known the moment a seed is tested, and the knockout draw follows
from the group results. So the **entire tournament renders as one batch** before
the first post: 65 captures at a few minutes each is an afternoon of machine
time, resumable (`shorts_build.py --capture-only` / `--encode-only`). Then the
33-day slate is a posting queue, scheduled on TikTok and YouTube in advance,
with nothing left to do on the day but check it went up.

The only spoiler is Rick. The bracket page (§5.5) shows results only as far as
the last posted match; the ledger holds the rest.

## 5. How the viewer follows along

Five surfaces, in the order a viewer meets them. Four already exist as flags
or formats; one is a build change.

### 5.1 The stakes band over the opening (exists: `--stakes` / `--stakes-sub`)

The band fades on the first clank, so it is only ever over the opening — the
right place for "where am I". The main line carries the round, the gold
sub-line what the fight decides:

```
PLAY-IN                     49 RELICS. 48 PLACES.
GROUP F · MATCH 1 OF 3      ONLY ONE KEEPS THE CROWN
GROUP F · MATCH 2 OF 3      VESPER MUST WIN TO STAY IN
GROUP F · MATCH 3 OF 3      WINNER TAKES THE GROUP          / DECIDER · LOSER GOES HOME
ROUND OF 16                 WINNER MEETS VESPER
QUARTER-FINAL 2             LAST EIGHT
SEMI-FINAL 1                ONE FIGHT FROM THE FINAL
THIRD PLACE                 ...
THE FINAL                   ONLY ONE KEEPS THE CROWN
```

The sub-line is **generated from the standings, not written by hand**, the way
World Cup 1's `narrate.py` did it: every "X is out if" claim brute-forced
against the remaining fixtures under the worst tiebreak for the relic in
question, so the band never says a relic is through or out when it is not.
`stakes_probe.py` re-runs on the longest lines; the band's pixel budget was set
for "TWO WEAPONS. ONE SURVIVES."

Trade named: the shipped stakes line is the first-time-watcher's ("TWO WEAPONS.
ONE SURVIVES." / "ONLY ONE KEEPS THE CROWN", hook brief v46) and it goes for
the tournament's duration. The crown sub-line survives on match 1 of each
group and on the final. Rick's veto on all copy (§9.3).

### 5.2 The announcer (exists: the hook VO)

The hook stays exactly as it is — *"Who wins? A, or B."* — because it was cut
to 2.02s to land before the clash and every extra word costs the hook (hook_vo
docstring). The round is on the band, in the viewer's eye, and does not need
saying.

What is new is an **outro line over the verdict panel**: *"Thornshear tops group
F."* / *"Vesper goes through. Axiom is out."* / *"Thornshear. Into the quarter-
finals."* — one sentence, generated from the ledger, `bm_lewis`, placed in the
tail with `--verdict-hold` stretched to fit it (the tail already follows that
flag). Same brute-force check as the band.

### 5.3 The verdict card — a standings mode (BUILD CHANGE, Code's)

The scrunch panel's verdict beat currently holds the HP/stats recap, or the
like-and-follow call when `CONFIG.cta.on` is set. A third mode, **`CONFIG.cup`**,
draws what the result did instead:

```
group match                              knockout match
┌────────────────────────────┐          ┌────────────────────────────┐
│ GROUP F         W  L   HP  │          │ ROUND OF 16                │
│ ▶ Thornshear    2  0  310  │          │ THORNSHEAR  ✓  through     │
│   Vesper        1  1  142  │          │ next: v VESPER · QF 2      │
│   Axiom         0  2    —  │          │                            │
│ 1 MATCH LEFT · F3 TOMORROW │          │ crown cup · 12 relics left │
└────────────────────────────┘          └────────────────────────────┘
```

The panel is fed a JSON blob (`CONFIG.cup = {...}`) written by the cup tool for
that match; the renderer draws it and does nothing else — a presentation-only
surface, gated like the CTA was (`engine_ab` identical, `shell_identity`
200/200, no `fx.js` field). Held for `--verdict-hold`, long enough to read three
rows. This is the one surface where the *result* lands, and it is the one that
makes a viewer who missed yesterday's short able to catch up from today's.

### 5.4 Caption, title, playlist (a convention)

One format, held constant for 65 posts, so the series reads as a series:

```
TikTok    Crown Cup · Group F · Match 2 — Thornshear vs Vesper  #superweaponball #weaponballs #weaponball #crowncup
YouTube   Super Weapon Ball Crown Cup — R16: Thornshear vs Vesper #weaponballs #weaponball
```

A YouTube playlist and a TikTok playlist for the series; every post's pinned
comment is the bracket link (§5.5) and yesterday's result in one line. Post
times fixed (morning / evening slots) so a follower knows when the next match
lands.

### 5.5 The bracket page (Cowork's)

A single hosted page — link in bio, in every pinned comment — showing the draw,
the sixteen group tables and the knockout tree, filled in **only as far as the
last posted match**, with the next fixture and its post time at the top. It is
generated from the ledger by the cup tool and republished after each post
(or twice a day by a scheduled task). It also states the rules: the seed rule,
the side rule, the tiebreak, the frozen build's hash — the fairness argument in
public, where World Cup 1 never got its bracket built at all.

Optional: a 1080×1920 still of the bracket, exported from the same page,
posted as a non-fight image at the end of the group stage and before the final.

## 6. The tools

**`tools/cup.py`** (Cowork writes it; no game engine in it beyond reading the
roster and testing seeds through `scpage.py`):

```
python cup.py draw      --game <frozen tip> --seed <draw seed>     # roster off the build, groups, challenger → ledger
python cup.py fixtures                                             # the 65 in posting order, sides per §1
python cup.py seeds     --game <frozen tip>                        # the rule of §3 applied; results into the ledger
python cup.py next / python cup.py post <fixture>                  # posting cursor
python cup.py lines <fixture>                                      # stakes band + outro line, brute-force checked
python cup.py cupjson <fixture>                                    # the CONFIG.cup blob for the verdict card
python cup.py render <fixture>                                     # the shorts_build command, filled in
python cup.py bracket --out bracket.html                           # the page, filled to the posting cursor
```

Ledger: `07-shorts/cup1/ledger.json` — draw seed, build hash, machine, groups,
every fixture's seed and `k`, result, HP, post date. Committed to git; mp4s stay
gitignored as ever (the seed rebuilds them). `test_cup.py` falsifies the line
generator against hand-worked groups (World Cup 1's `test_narrate.py`, ported).

**Build change** (Code's, from a brief when this plan is accepted): the
`CONFIG.cup` verdict card of §5.3, as a builder like `cta_build.py` was — one
link on the frozen tip, presentation-only, gated identical.

**Exists and needs no change:** the stakes band and sub-line, the hook VO, the
verdict hold, the full ignition open (`shorts_build` default), the loudness
chain, `shorts_build --capture-only/--encode-only` for the batch.

## 7. Order of work

```
1. batch lands + Nightglass; Rick's eye on each; the staff branch and the batch
   line carried onto one another (CLAUDE.md §0 says this is the gate)
2. FREEZE: one tip, one hash, one machine. No relic changes until the final posts.
3. Code: the CONFIG.cup verdict card, gated.               Cowork: cup.py + tests.
4. Rick: names the cup, vetoes the copy table, picks the draw seed (any number).
5. cup.py draw → the ledger and the bracket page go up EMPTY, with the rules.
   Publish. This is the commitment.
6. cup.py seeds → results. cup.py render × 65, in an afternoon, resumable.
7. Spot-check: watch the play-in, one group's three, a semi. The rule's fight is
   the fight even if it is ugly (§8).
8. Queue 33 days of posts. Day 1.
```

## 8. Risks, named

- **A fighter looks broken on camera mid-tournament.** It does not get patched
  — a patched build is a different tournament. Note it, fix it after the final.
  This is why step 1 waits for Rick's eye on all 49.
- **The rule's fight is a dull one.** It will happen; it is the price of the
  fairness argument and Rick has taken it. The full ignition open and the
  director still do their work; only the seed choice is gone.
- **Three-way ties** in ~4 groups, broken on HP. The band and the card have to
  explain it in one line ("through on HP remaining"). Copy in the veto table.
- **Length.** Minute-pace fights with the full open run 48-88s. A 33-day series
  of 60-90s shorts is what was ruled on 2026-09-16; this plan does not reopen it.
- **Runtime drift.** One machine, one Chromium, one hash — §3. If the machine
  changes mid-render, the remaining fights re-seed on the new one and the ledger
  says so; already-posted results stand.
- **Retention on dead rubbers.** Groups of three have none: every third match
  decides something, and match 2 usually eliminates someone. That is the shape
  doing the work.

## 9. Open decisions

1. **The name.** Working title "Crown Cup". A spread: *Crown Cup I* · *The
   Crowning* · *The Sundered Crown Championship* · *Trial of the Crown*. The
   name goes on the band, the captions, the bracket page and the playlist, so
   it is needed before step 4.
2. **Third-place match** — kept in the count above (video 64). Drop it and the
   final pairs with the second semi on day 32 instead of posting alone.
3. **The copy table in §5.1** — every line is a draft for Rick's veto; the
   shipped stakes line goes dark for 33 days.
4. ~~Should cup.py be written now?~~ **Done the same day** — Rick asked for the
   clip tool to drive it; see §10 and `CROWN-CUP-APP-BRIEF-v115.md`.
5. **Post slots** — which two times of day.
6. **The draw as content** — a draw-reveal post (not a match) before day 1, or
   just the bracket page.
7. **Dead rubbers** — film the ~4 group matches that decide nothing (honest
   band, every relic gets two shorts), or skip them (~61 shorts, 31 days)?

## 10. Corrections after building `cup.py` (Cowork, 2026-09-27, same day)

`tools/cup.py` and `tools/test_cup.py` now exist and are tested (§6 is no
longer a proposal; `CROWN-CUP-APP-BRIEF-v115.md` is the app side, for Code).
Building it falsified two claims above:

1. **§3 — the fatal-cut condition is dropped from the rule.** It was put there
   as "does not look at the winner". Measured on `sc-tendril-fx` at Chromium
   141, 240 seeds a pairing: the director finds a fatal cut in only 6–34% of
   kills, and requiring one moves the win rate by up to 26 points (Gloamwire v
   Paradox 84% → 58%; Spellbreaker v Censer 40% → 17%; Twinshade v Vinesower
   58% → 82%). A filmable kill is a kind of kill, and which relic delivers it
   is not independent of the relic. The rule is now **"ends in a kill", full
   stop**; whether the director found the finale is recorded per fixture. In
   the 33-fixture test run it found 4 of 33 — so most finales will play at
   plain speed unless the director learns to file a fatal cut on every kill
   (a separate call, in the brief).
2. **§1 — "no dead rubbers" was wrong.** In a group of three with a fixed
   order (P1 v P2, P2 v P3, P3 v P1), P2 plays the first two matches; when P2
   wins both, the third match is between two relics on 0 points and decides
   nothing. That is one ordering in four, so about four groups in sixteen end
   on a dead rubber. The band says so honestly (`GROUP DECIDED · X IS
   THROUGH`). Whether to film those four or skip them is a new open decision
   (§9.7): skipping saves four shorts and breaks "every relic gets two".

Also seen in the test run: 3 of 8 groups went to the HP tiebreak — the
quarter-of-groups estimate in §1 holds. The seed rule's `k` was 0 on every
fixture once the fatal-cut test was removed (timeouts are rare at minute pace).
