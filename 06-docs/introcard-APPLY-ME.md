# THE FIGHT CARD v2 — the clash. A patch for the live session.

**2026-08-14.** `introcard_build.py --src sundered-crown.html --out
sc-intro.html`, built and checked against the seed's SHIPPED `f78e0253…`;
result `45ed97ca…`. Rick's brief: kill the fade from black and slide the
cards in; real numbers and plainer language instead of abstractions.
**Experimental — nothing here is a ship decision.** Revised same-day from
Rick's review of the first cut — see §6.

---

# 1. What the four seconds now do

```
0.00-0.46   the cards fly in from top and bottom and MEET at the centreline
0.46        CLANK — sparks sideways out of the seam, ring, damped shake, and
            the actual clank sound (fired from Match.step on a clock crossing)
0.46-0.74   the cards rebound to rest; the tape grows out of the impact point
0.74-3.50   the hold — everything readable, every value a real number
3.50-4.00   the reveal: cards leave the way they came, the scrim lifts, the
            HUD fades in, and the bell lands on the hall ALREADY LIT.
            There is no cut: the last intro frame IS the first fight frame,
            asserted as pixels (probe [2], mean |diff| 0.000).
```

The card never sits on black. A Match at t=0 already draws — fighters at
their spawns, sigil, washes — so the backdrop is the real hall under an 80%
scrim, via a `_introScene` reentry guard in `draw()`. The scene pass skips
`drawHud`/`drawFooter` (they double-printed the names and the seed against
the cards); both fade back in with the reveal, which is what makes the cut
frame byte-identical to a fight frame.

# 2. The tale of the tape — real numbers, pairwise

Replaces the roster-normalised bars, which said "more than him" but never how
much, and cost four saccades and a memory task per stat. One shared band:
value left, value right, mirrored bars scaled to the LARGER OF THE PAIR,
winner's side lit in its school colour, loser dimmed, numbers counting up as
the bars grow. Rows: DAMAGE/HIT · REACH · SWING SPEED · WEIGHT, plus
"300 HP EACH" (read from `CONFIG.combat.baseHP`).

Per-card facts are two lines each — tag + name announce, the tip explains
at full width and 25px (the size the old card proved at phone scale; the
one-line version squeezed tips to 19px and the longest ultimate still
clipped the frame). Facts per Rick's review: the SHOOTS line is GONE (the
silhouette and the ANY reach already say it); swing relics carry
`IT TRACKS — Swings at its foe — other weapons spin blind`; the status line
is `EVERY HIT / IT GAINS +n STATUS` with its tip; the ultimate reads
`ULTIMATE > name > what it does with numbers > cooldown`. Every value is
read from WEAPONS/STATUS/CONFIG at draw time; `relicStatus`/`relicShot`
stay the single source the legibility contract calls. RANGED prints `ANY`
with a full bar.

# 3. Every check, including the one that proves the checks work

```
introcard_build.py        28 anchors (8 structural + 16 tip edits + 4 brand/
                          convention edits), each hit exactly once; opens its own
                          output and draws every card phase for melee /
                          ranged / self-status pairs — no exceptions
intro_probe.py  [1]       engine A/B src vs out, 120 pinned matches          PASS
                [2]       reveal continuity, |diff| 0.000 over the frame     PASS
                [3]       hall visible on the first card frame — AND the
                          same measurement FAILS on the unpatched build
                          (lit 0.0298 vs 0.0049), so it is measuring
                          something real                                     PASS
                [4]       the tape band differs 23.3 from the bare scene     PASS
                [6]       every STATUS tip fits the in-arena explainer
                          panel (8 tips ≤ 536px at its 25px) — the popup
                          reminders read the same tips the card does, so
                          longer language had to be proven to fit           PASS
                [5]       frame-edge clip audit, 4 pairings x 4 phases,
                          0 bright pixels within 6px of any edge (the
                          impact flash's seam band is excluded by design —
                          it is a deliberate full-bleed beam). Added after
                          the first cut shipped "ANY" clipped and the
                          longest ult line ran off the frame; the audit
                          caught the second one before Rick did            PASS
engine_ab.py --n 200      3000/3000 identical, 6/6 distinct winners          PASS
verify.py --n 150         13/13 (42.5s mean, spread 3.3pp — unchanged)       PASS
anchor counts             sundered-crown / sc-r15 / sc-cine: all 28 at 1 each
```

**verify.py change, one line:** the ult-tip length contract moves 44 -> 72
chars — ult tips render on their own 25px line now, so the budget is the
line, not the old tag row. Status tips keep 40 (the in-arena first-landing
panel still prints those). The seed's verify.py here already carries it;
the live session applies the same one-liner or verify will fail the two
longer ult tips by design.

`introT` still defaults to 0 and is only set by presentation layers;
`CONFIG.intro` gains `clash`/`reveal` but `dur` stays 4.0 — the clash costs
0.46s and the reveal 0.50s, and the tape reads faster than two separate
stat blocks, so retention keeps its price. The clank/bell fire on clock
CROSSINGS so 4x speed cannot double-fire them.

# 4. To apply on the live line

Drop the patch's five .py files beside your existing tools (they import the
local scpage.py), then:

```
python3 verify_tip_patch.py                  # the 44 -> 72 ult-tip contract
python3 introcard_build.py --src sundered-crown.html --out sc-intro.html
python3 intro_probe.py     --src sundered-crown.html --out sc-intro.html
python3 engine_ab.py --a sundered-crown.html --b sc-intro.html
python3 verify.py --game sc-intro.html --n 150
share_build --src sc-intro.html              # the phone page picks it up whole
```

The builder is deterministic: applied to the seed's `f78e0253…` it must
reproduce `45ed97ca…` byte for byte (reference/sc-intro.html in the patch is
that exact file — diff against it before trusting anything else). On a line
that has moved past f78e0253, the 28 anchors decide, and every one must hit
exactly once.

Anchors are cut around structure (region boundaries, the step() card clock,
the draw() dispatch, two call sites, and the eight tip literals), the same
discipline that carried
the cinema patch across five builders. If any anchor reports ≠1, diff before
re-anchoring — do not loosen it. The builder refuses to write
`sundered-crown.html` and stamps its output GENERATED.

# 5. What is owed, in order

1. **WATCH IT, with sound.** The probe cannot hear the clank land on the
   card impact or the bell land on the reveal, and the whole design is a
   rhythm. `sc-intro.html` at phone size. `intro_clip.py` renders a 30fps
   silent mp4 (the GIF is 12.5fps and reads choppy — measured in-container,
   an intro frame costs within ~10% of a mid-fight frame, so the live page
   is as smooth as the fight; the GIF was the artifact).
2. **Phone frame cost during the card.** The intro frame is scene + scrim +
   card layer, with `shadowBlur` on the VS and the card art — small
   surfaces, but this week established nobody predicts blur cost by eye.
   One QUICK run on a card frame prices it.
3. **The wording pass.** `wording_sheet.py` generates `wording-review.html`
   from any build — every card string, clickable, exports notes as JSON
   naming the exact data field each change edits. Rick has the current one.

# 6. Rick's same-day review, applied

* SHOOTS line removed; `IT TRACKS` added on swing relics; ultimate line
  reordered to ULTIMATE > name > effect-with-numbers > cooldown.
* Facts restructured to two lines after the one-line form clipped
  (probe [5] is the regression check).
* Tip language (tips are the single source, so the card AND the in-arena
  explainer pick these up): `a stack` -> `per stack` on smite, hemorrhage,
  entangle, sunder; ward `Shields, then shatters when broken` ->
  `Blocks damage, blasts its breaker`; Quarrelstorm -> `Fires a nova of
  arrows`; Exsanguinate -> `Fires a Hemorrhage nova: 3 stacks, 16 damage,
  knocks back`; Reprisal -> `Gains spin speed, then spends the ward as
  bonus damage on one shot` (Rick asked for a percentage — the code adds
  the ward pool as FLAT damage on top of dmg:34, so the line stays honest
  about the mechanic).

# 7. The full wording pass (sc-wording-notes.json), applied and codified

Rick reviewed every card line via `wording-review.html` and the notes are law:

* **Title**: `SUPER WEAPON BALL: The Sundered Crown` — on the card header,
  the page <title>, the <h1> (subtitle drops the stale relic count), and the
  in-fight footer. The card's seed line is deleted (footer/result keep it).
* **TRUESTRIKE** replaces the IT TRACKS line on swing relics: `TRUESTRIKE —
  Swords track their target instead of rotating`.
* **ON HIT** is the status tag everywhere — including ward, which is banked
  by landing hits, so `ON HIT · GAIN WARD` is what the code does. The `+n`
  count is suppressed when maxStacks is 1 (printing `+2.5 WARD` taught a
  stack mechanic that does not exist; Farwarden's 2.5 is a banking-rate
  multiplier).
* **Status tips are effect clauses** (the card's tag line and the arena
  panel both already print the name/count): `Deals 1.5 damage per second
  per stack` (smite, hemorrhage) · `Increases damage taken by 11% per
  stack` · `Slows swing speed by 13% per stack` · `Stuns the weapon 0.2s,
  faster per stack` (hex, numbers from stunFor/stunEvery) · `Drains maximum
  hp, permanently` (curse — "permanently" kept: it is the one status that
  never expires) · `Shield; blasts 40% of it when broken` (ward, from
  shatter:0.40).
* **Ult tips are sentences** with numbers filled from data; Widowmaker's
  knockback dropped per the note; Reprisal spends "the ward", not a
  percentage that does not exist.
* **The convention is codified in the source**: the STATUS comment block now
  states the rule (effect clause, verb first, real numbers, "per stack",
  ≤40 status / ≤72 ult) so the next relic follows it, and probe [6] enforces
  the panel fit. `popup-check.png` shows the in-battle reminders carrying
  the new language.
