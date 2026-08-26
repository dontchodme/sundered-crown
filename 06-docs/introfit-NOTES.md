# THE FIGHT CARD v3 — the legibility pass

**2026-08-15.** `introfit_build.py --src sc-daybreak.html --out
sc-introfit.html`, applied to the chain tip `c25a90cc0ca82f68`; result
**`71c0a0c0c1ea6996`**, the new chain tip. `01-live` is untouched — still
v21's `ba423d8e…`. Rick's brief, in full:

> They currently are pretty hard to read especially on mobile. All of the
> info is scrunched at the bottom and a lot of leftover space is being
> unused. Can we make the text more legible and use more of its available
> space? Can we also separate the status effect text from the ult text a bit
> to make them more distinguishable from each other?

---

# 1. What was actually wrong, in numbers

The canvas is 1080 wide and a phone renders it about 390pt across, so the
card draws at **~0.36x**. Every canvas px is a third of a point in the hand.

* **The type.** v2's tips were 25px — 9pt on the phone. But its shrink-to-fit
  guard (`while (width > 1022) fs -= 1`, floor 19) had quietly taken **8 of
  the roster's tips below 25px, and the longest to 20px** — 7pt — because the
  ult line carried `tip + " · " + charge + "s cooldown"`. The smallest text
  on the card was attached to its most important fact. Measured, not
  eyeballed: introfit_probe [B].
* **The space.** v2 bottom-anchored the facts —
  `yy = y0 + CH - 22 - sum(heights)` — so a 560px card carried everything in
  its bottom ~240 and left the rest empty. Ink in the card's text column,
  y 280–430, on v2: **0.0000**. Nothing. Forty percent of each card was air.
* **The separation.** Status and ultimate were four identical left-aligned
  rows in the same two greys. Nothing said where one fact ended.

# 2. What v3 does

**Fills the card.** Frame margin 118 -> 104, card 560 -> 574. That is free:
the tape between the cards keeps its exact **678..1242** band, so nothing in
`_introTape` moves. Facts start under a header rule and the slack is *spent* —
panels stretch (capped at +46 so a two-fact card does not become two slabs)
and the remainder widens the gaps. Same column on v3: **0.0800**.

**Bigger type that wraps.** Tips 25 -> **30px** and they WRAP to a second
line instead of shrinking; the shrink survives only for a string no break can
fit, with a 20px floor it never reaches. Names 31 -> 36, tags 19 -> 20,
school 24 -> 25, tape labels 23 -> 27, the HP line 22 -> 26. The ultimate's
`· 16s cooldown` tail is off the sentence and onto a **right-aligned chip** —
it was stealing the width that forced the shrink in the first place. Smallest
face anywhere on the roster now: **26px**.

**Status and ultimate are different objects.** Each is a panel with its own
tinted ground and accent rail — the status in the fighter's school colour,
the ultimate in gold with a lit border and the cooldown chip. The gap above
the ultimate (28) is twice the gap above the status (14), so the grouping is
spatial as well as chromatic. TRUESTRIKE drops to a one-line strip: it is a
class property, not a headline, and the hierarchy should say so.

**Silhouettes are fitted, not scaled.** v2 drew every weapon at a shared
`scale(2.2)`. That made the greatswords overrun the band and the twinblades a
speck — and on v3's first cut, with a shorter header, Thornwake's scythe hung
**57px out of the top of the card**. `_artBox(w)` rasterises the shape once
per weapon into a scratch canvas and measures its true extent, and the card
scales each weapon to fill a fixed art box. The shapes are drawing code, not
geometry: `reach` and `artW` predict a greatsword's bounds and lie about a
bow's, so the only honest way to fit one to a box is to draw it and look.
`_artShape` is now the single function both the card and the measurement
call, so a bbox cannot disagree with what is drawn.

# 3. The layout is factored, so it can be falsified

v2's layout was inline arithmetic inside a draw call. The only way to know a
card fit was to look at one, and Rick looks at three. v3 splits it:

```
_introFacts(f)              the descriptors + wrapped tips (pure, measures)
_introLayout(facts,top,bot) assigns y/h, returns {fits, natSlack}
_introCard(...)             draws what those two decided
IC                          every metric in one object, exported on AC
```

`AC.IC` on the export surface is not decoration — it is what lets the probe
lay out **all 16 relics** and assert, instead of screenshotting three.

# 4. Every check

```
introfit_probe [A]  16/16 relics fit; tightest headroom before stretch 16px
                    16/16 tips wrap clean (none overruns its column)
                    16/16 silhouettes inside the header band
                    16/16 names clear of the art by >30px
               [B]  smallest tip face 26px vs v2's 20px — and the same
                    measurement is taken on v2, because a legibility claim
                    that cannot distinguish the two builds is not one
               [C]  32/32 card-overflow bands clean (16 relics x 2 slots,
                    each paired against the longest tip in the game).
                    This is the check that caught the scythe.
               [D]  the dead band carries facts: 0.0800 vs v2's 0.0000
               [E]  gap above ULTIMATE > gap above ON HIT, 16/16
               [F]  all 16 rendered at phone width — introfit-roster.png
intro_probe    [1]  120 matches identical field for field           PASS
               [2]  reveal continuity, |diff| 0.000                 PASS
               [3]  hall visible at the first card frame, 0.0308 vs
                    0.0049 on sc-c2 — see §5                        PASS
               [4]  the tape band differs 24.8 from the bare scene  PASS
               [5]  0 bright pixels within 6px of any frame edge    PASS
               [6]  8 status tips ≤536px in the in-arena panel      PASS
engine_ab --n 55    6600/6600 identical across all 16 ids           PASS
verify.py --n 60    13/13.  Grudgebearer 63.0, Dawnbringer 54.4,
                    floor Farwarden 46.1 — towers intact            PASS
tip_audit           0 gaps                                          PASS
anchors             7 edits + 1 span, each hitting exactly once
```

No tip text changed, so the wording law and the in-arena explainer panel are
untouched. The card still reads every value live from WEAPONS/STATUS/CONFIG
at draw time; `relicStatus`/`relicShot` remain the single source verify.py's
legibility contract calls.

# 5. A check that cannot fail is comparing nothing

intro_probe [3] asserts the hall is visible behind the scrim on the first
card frame, *and that the same measurement fails on the build being
replaced*. That control was v1, which drew a solid black rectangle. Once the
card was in the baseline, `--src` was itself a card build: out 0.0308 vs src
0.0304, and the differential arm could no longer fail **no matter what the
patch did**. It had become a decoration without anyone touching it.

It now takes `--pre` — the last build with no card, `sc-c2.html` — and passes
honestly: **0.0308 vs 0.0049**, 6.3x. Recorded as a trap for the next
session, because it generalises: any probe whose control eventually absorbs
the thing it controls for goes quietly green forever.

# 6. What is owed

1. **WATCH IT, with sound.** `05-reference/introfit-preview.mp4` is 30fps and
   silent; the clank and the bell still need the live page.
   `05-reference/introfit-before-after.png` is v2 vs v3 at 380px, and
   `introfit-roster.png` is all 16 at phone width.
2. **The first card frame, on a phone.** `_artBox` rasterises both fighters'
   silhouettes once per page — 2 x ~1ms in this container, and it lands on
   the first frame that draws a card. That is a real one-frame cost on a slow
   device and nobody has watched for it. If it shows, hoist it to page load.
3. **The card-hold frame cost, on a phone.** In-container p50 15.5ms (v2) vs
   16.3ms (v3) — inside this box's noise, which says "not obviously worse",
   not "fine". The standing phone debt now includes this.
4. **A wording look at the wrapped lines.** Several ult tips now break across
   two lines and the break point is wherever the measurement lands
   (`3 Curse / stacks`). `wording_sheet.py` is the tool if any read badly.
