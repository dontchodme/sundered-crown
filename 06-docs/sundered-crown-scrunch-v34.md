# SCRUNCH — the hall makes room, the fight never stops. BUILT AND CHECKED.

**2026-08-19.** `scrunch_build.py --src ../02-chain/sc-cardspin.html --k 0.70`,
applied to `ec9b8d753235385d`; result **`189c41e5a5191b8f`**. `01-live`
untouched. **Supersedes `sundered-crown-nameplate-v33.md`, which is abandoned.**

Two corrections from Rick, both right, both after something had been built:

> *"the nameplate drops down and covers the top of the screen just to show the
> same information that was always there... what if we scrunch up the arena and
> show the fight cards at the bottom?"*

> *"i dont think stats are what the scrunch should show. it should show what the
> status effects and ults do"*

The plate was decoration — the HUD already carried both names, so a banner
repeating them bought nothing. And the stat tape was inert trivia: damage/hit
and weight are numbers a viewer cannot act on. **The statuses and ultimates are
the things that are about to happen on screen**, and a panel explaining them is
a legend for the next forty seconds rather than a pre-fight formality.

Three tools: `scrunch_build.py`, `scrunch_probe.py` (12 checks, 3 controls),
`scrunch_shot.py`.

---

# 1. WHAT IT DOES

On the first clank the hall scales to **0.70** over 0.42s, holds 3.0s, and
scales back. The freed strip at the bottom carries a two-column legend. At the
kill it scrunches again and the strip carries the verdict.

```
                          CARD                      SCRUNCH
duration                  4.0s                      3.84s (0.42 + 3.0 + 0.42)
simulation                FROZEN                    running throughout
the hall                  invisible                 70%, fully visible
what it says              4 stat bars + abilities   both abilities, both ults,
                                                    with cooldowns
at the kill               full-screen card over     verdict in the strip, hall
                          a 60% scrim               untouched
```

**Every string comes from `_introFacts` and `STATUS[].tip`** — the same source
the intro card uses — so the panel and the card cannot drift, and the `<=40
char` tip discipline `verify.py` enforces still governs the copy.

# 2. THE PRICE, STATED

The hall is 520x800 sim units and the renderer is width-bound
(`scale = aw / CONFIG.arena.w`), so **cutting its height cuts its width by the
same factor**. `CONFIG.arena` is a simulation constant and changing it would
force a retune, so it is not on the table. At k=0.70 the hall is 739px wide in
a 1080 frame and **170px of margin appears on each side**. It reads as a
deliberate letterbox rather than a mistake, but it is real and it is the cost.

k was chosen twice. First from a sheet at 0.75 / 0.65 / 0.55: 0.75 left only
396px of strip, 0.55 shrank the relics too far. Then **raised from 0.65 to
0.70** once the panel stopped carrying stat bars — the legend is shorter than
the tape was, so the extra room went back to the hall rather than to whitespace.

Checked across eight pairings for overflow, including the longest copy in the
game (Crucible: *"Pulls the foe in and consumes Sunder — +15% crit, +0.4x dmg
per stack"*, Bramblesnare, Slagburst). Nothing clips.

# 3. THE VERDICT BEAT

`drawResult` already stated the winning HP — but it does so behind a
**full-screen 60% scrim**, and its own source note records why that is a
problem: *"the most legible moment in the match — the loser visibly breaking —
played out behind 60% black."* They fixed it by delaying the card 1.05s. This
fixes it by moving the verdict off the hall entirely.

The panel prints the number every week-one note is written around — *2 HP of
300*, *won on 12 HP*, *Ironhail on 8 HP* — at 92px, while the shatter plays at
full brightness above it. `drawResult` stands down when the panel has the
verdict; both at once would put the scrim back.

Measured, not asserted: hall luminance at the verdict is **21.0 with the
scrunch against 15.4 under the old card**.

# 4. THE PROBE

```
PASS  [1]  engine_ab: 72 matches simulate identically in both builds
PASS  [2a] CONTROL -- the CARD build's clock does not move in 3s   (0.0000s)
PASS  [2b] the SCRUNCH build's clock moves 3s and the tape is armed (3.0000s)
PASS  [3a] CONTROL -- the same moment twice reads 0.000 in the hall
PASS  [3b] the hall MOVES while the panel is up                     (5.025)
PASS  [4a] the frame changes below the scrunched hall               (19.912)
PASS  [4b] the layout fields are handed back untouched after every draw
PASS  [4c] by 7.5s the hall is back to full size                    (k = 1.0000)
PASS  [4d] during the hold the hall sits exactly at CONFIG.scrunch.k
PASS  [5a] the verdict beat arms after the kill
PASS  [5b] the verdict has an HP number to state                    (8 HP)
PASS  [5c] the hall is BRIGHTER at the verdict than under the old card
PASS  [6]  no page errors
```

`[4b]` matters more than it looks: the mechanism is that `pad/aw/ah/scale` are
mutated for the duration of one draw, so every clip rect, relic and arena
frame follows for free. If they were ever left mutated, the next frame would
compound. The check reads them back after a scrunched draw and requires the
design values exactly.

# 5. TWO HARNESS BUGS WORTH RECORDING

**(a) The first mock photographed a lie that looked plausible.** It drew the
scrunched frame in one `evaluate` and grabbed the canvas in the next — and the
page's own rAF loop redrew a normal frame in the gap. Every "scrunched" shot
was the unscrunched hall, and it looked entirely believable. Draw and grab are
now atomic.

**(b) The first comparison video slandered the baseline.** The capture loop
arms the card on `m.t >= cut`, and by the kill `m.t` is 33s — so the CARD build
raised its INTRO card over its own verdict. The baseline looked far worse than
it is. A comparison that flatters the new thing is worthless; `__raised` is now
forced true before the verdict clip.

# 6. WHAT IS NOT DONE

1. **`cinema_clip.py` still raises `introT`.** No short can be rendered with
   this yet. That wiring is the next job and it is the only thing between this
   and a postable video.
2. **The VO is not re-aligned** — still delayed 300ms for a card at t=0.
3. **Nobody has heard it.** The card's synthetic clash `clank` and its `seal`
   bell are both gone; the real clank that triggers the scrunch is doing that
   work now.
4. **The relic ART is not in the panel.** The card showed each weapon's
   silhouette; the strip has no room for it at k=0.70.

# 7. Open decisions

1. **Watch `card-vs-scrunch.mp4`.** Both beats, side by side, same fight and
   seed. Everything above is measurement; this is the judgement.
2. **Is 3.0s enough to read six lines of copy?** The card had 4.0s and a frozen
   fight competing with nothing. This has 3.0s and a live fight competing for
   the eye. It is the one number most likely to be wrong.
3. **170px of margin each side.** Live with it, or fill it — the timer and clank
   count could move outboard, or the hall could be nudged off-centre.
4. **The gap between the ON HIT block and the ULTIMATE block** is breathing room
   at short copy and disappears at long copy. Bottom-anchoring the ultimate
   keeps its position stable across relics; flowing it would close the gap and
   move it around. Currently anchored.
5. **Same-palette pairings show it here too** — Dawnbringer v Censer puts two
   near-identical white rails and two identical `+1 SMITE / Deals 1.5 damage
   per second per stack` blocks side by side. The panel makes the v28 palette
   collision more visible, not less.

---

# 8. WITH THE HEALTH REWORK — `sc-healthscrunch.html` `be18906458e9a35f`

Rick: *"can i see it all with the new health bars too?"*

`scrunch_build.py --src ../02-chain/sc-health.html --k 0.70`. All nine anchors
survived the health build untouched, so the two changes compose without either
builder knowing about the other — which is the payoff for both being anchored
edits to `sc-cardspin.html` rather than divergent hand-edited forks.

**The one collision that could have happened, did not.** The health build's
lifeline is placed by `BAND.pos`, and `BAND.pos === "bottom"` sets
`arenaTop = 20` and puts the lifeline under the hall — exactly where the scrunch
panel lives. It ships as `"top"`, so the lifeline sits above the hall and the
panel below it. **If `BAND.pos` is ever flipped, these two fight for the same
strip.** Recorded here because nothing in either builder would catch it.

The same 12-check probe, run against `sc-health` as the base:

```
PASS  [1] engine_ab: 72/72 identical between sc-health and sc-healthscrunch
PASS  [2b] the clock moves 3.0000s under the panel
PASS  [4b] layout fields handed back untouched  (aw 1056, pad 12)
PASS  [5c] hall luminance at the verdict 21.0 vs 15.4
... all 12
```

What the combination actually does, frame by frame: the top band carries the
two ult sigils with quartered charge bars and the lifeline (`IRONHAIL 96% |
100% GORESHARD`); the hall carries the on-shell gauge; the bottom strip carries
the legend for three seconds and the verdict at the end. Mid-fight the lifeline
is doing the work the scrunch panel is not — at 21.0s it reads `67% | 34%` and
the fight is legible without any overlay at all.

**One redundancy, stated rather than hidden.** With the health build the ult
NAMES are already on screen permanently, so `QUARRELSTORM` appears both in the
top band and in the panel. That is not the name-plate mistake repeated: the band
names the ultimate, the panel says what it does and what it costs. Same for the
relic names — in the panel they are column headers, and dropping them would
leave two columns identified by colour alone, which is the thing this codebase
avoids everywhere else. But it is worth a look on the video before it is called
settled.

# 9. Open decisions (added)

6. **Do the scrunch and the health rework ship together or separately?** v32 §6
   argued for one change at a time and that argument has not weakened — two
   variables in one video costs the read on both. They compose cleanly; that is
   an argument about the code, not about the experiment.
7. **`BAND.pos` is now load-bearing for two features.** Worth a gate in
   `scrunch_build.py` that refuses to build against a source with
   `BAND.pos === "bottom"` rather than silently producing overlapping panels.
