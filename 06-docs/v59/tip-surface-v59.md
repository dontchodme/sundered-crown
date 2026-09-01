# v59 — THE TIP BUDGET WAS NEVER THE PANEL'S. A status tip is drawn on two surfaces, the tight one is the in-arena reminder, and `tip_audit` — the gate `CLAUDE.md` calls "the one that actually protects the layout" — measures the right box in the wrong typeface, so it disagrees with itself by 27% depending on which machine runs it. Four changes for Code, none of them read by the sim.

**2026-09-01, Cowork.** Measured against `02-chain/sc-nightfell.html` through
the build's own `_scrunchWrap` and `_tagFirst`, with the bundled face loaded
via `document.fonts` before any `measureText`. Runtime only.

---

# 0. THE THING THAT WAS WRONG BEFORE ANY OF THIS

`cell-repricing-v57.md` open decision 5 and `cindercleave-design-v57.md` open
decision 7 both say:

> ***`STATUS.curse.tip` STILL SHIPS THE PRE-REWORK WORDING** — "Hits reflect 8%
> of the damage that cursed". Open since v55, still 40 characters, still one
> line.*

**It is not pre-rework wording.** `06-docs/v53/curse-build-v53.md` §2 lists that
exact string in the table of what the curse rework SHIPPED, and `CLAUDE.md`
records it as Rick's own line. It has been carried as an open bug through three
documents. **It is 41 characters, not 40.** Closed, and closed as a mistake
rather than as work.

The line does have a real defect, and Rick fixed it himself when shown:
**curse remembers three blows and the line describes one.** A reader guesses the
bonus is 8% where a full pool is 24%.

```
was    Hits reflect 8% of the damage that cursed                    41 ch  475 px
now    Hits reflect 8% of the damage that cursed, stacks 3 times    57 ch  653 px
```

---

# 1. A STATUS TIP IS DRAWN TWICE AND ONLY ONE OF THEM IS TIGHT

```
THE PANEL      _panelFacts -> _scrunchWrap(r.tip, colW - 14, 21, 3)
               467 px a line, 21px, WRAPS to 3 lines, then shrinks to 15.
               System font stack. Generous: 112 characters still render at
               full size inside three lines in the widest font measured
THE REMINDER   _tagFirst, the pop-up the first time a status lands in a fight
               box 596 * k, text inset 30 * k each side -> 536 px
               ONE LINE. NO WRAP. NO CLIP. 25px, and the BUNDLED
               'Atkinson Hyperlegible Next'         <-- THE REAL GATE
```

**`_tagFirst` does not measure the string and does not clip it.** A tip wider
than 536 px simply draws out of the box and into the hall. Photographed: Rick's
57-character line runs 117 px past the border.

`CLAUDE.md` attributes "536px on one line at 25px" to the scrunch panel. The
number is right and the surface is wrong — the panel wraps and always did. The
one-line 25px surface that the 48-character cap was written for is `_tagFirst`,
and `_introWrap` (the fight card's, the other candidate) is **defined and never
called** in this build.

## 1.1 EVERY SHIPPED TIP, IN THE FONT IT IS ACTUALLY DRAWN IN

```
status       ch   Atkinson 25px    slack of 536
blessing     33        378             +158
entangle     35        431             +105
smite        37        441              +95
hex          38        447              +89
ward         40        455              +81
sunder       39        472              +64
curse        41        475              +61
```

Nothing is close. Sunder is the tightest at 472 and always has been.

## 1.2 THE GATE MEASURES THE WRONG TYPEFACE, AND IT IS NOT A ROUNDING ERROR

`tip_audit.py`'s EXTRACT sets `"500 25px ui-sans-serif,system-ui,sans-serif"`.
That is correct for the panel and **wrong for the surface that can overflow.**
One string, `"Hits reflect 8% of the damage that cursed"`, at 25px:

```
'Atkinson Hyperlegible Next'  (what _tagFirst draws)    475 px
'Segoe UI'                    (Rick's PC resolves here) 414 px
Arial / Liberation metrics                              459 px
'DejaVu Sans'                 (a Linux render)          526 px
```

**On Rick's machine the gate reports 414 px for a line that draws at 475**, so
it has 61 px of imaginary headroom and would wave through a tip that overflows.
In a Linux container it reports 526 and is pessimistic instead. `v53`'s recorded
**471 px** matches none of the four, so the number has now been different in at
least three environments.

> `CLAUDE.md` already carries this lesson once — *"a previous version of this
> tool used a 400-weight -apple-system stack and measured every tip ~13%
> narrow ... if two tools measure the same thing, they have to measure it the
> same way."* It recurred because the build moved to a bundled webfont on that
> surface and the tool did not follow. **The bundled face is embedded in the
> build as a data URI, so measuring in it is machine-independent** — this is
> not a trade-off, it is strictly better.

---

# 2. THE FOUR CHANGES

```
 #  WHERE                     WHAT
 1  STATUS.curse.tip          -> "Hits reflect 8% of the damage that cursed, stacks 3 times"
 2  _tagFirst                 const w = 596 * k   ->   760 * k
 3  verify.py                 status tip cap 48   ->   72
 4  tip_audit.py EXTRACT      measure "500 25px 'Atkinson Hyperlegible Next'",
                              await document.fonts, and compare against
                              (tagBoxW - 60) read from the source rather than a
                              literal 536
```

**Change 2 is Rick's, from a spread of four widths photographed at 1080x1920.**
720 fits his line by 7 px and visibly crowds the border; 760 leaves 47 and still
sits inside the hall; 800 was offered and not taken.

```
box    text budget    his line 653 px
596        536            -117   overflows today
720        660              +7   technically fits, looks squeezed
760        700             +47   <- RICK'S
800        740             +87
```

The widening applies to **all eight statuses**, which is why it was his call and
not a mechanical consequence of change 1. Nothing else gets wider — the next
longest tip is sunder at 472.

**Change 3 is not needed for change 1 if change 2 lands**, since the character
cap and the pixel budget are independent gates and 57 > 48 either way. 72 is
the number ult tips already use, on the same column, through the same wrapper.
The "40" stated twice in the v51 brief was folklore; `verify.py` has enforced 48
since it was written, in the line under a comment that said 40.

---

# 3. THE GATES

```
engine_ab     IDENTICAL on all 27, every match. None of the four is read by the
              sim, and this is the cheapest possible proof of it. If a bit
              moves, THAT is the finding and it stops the change
tip_audit     after change 4, re-run it over all eight statuses and expect the
              numbers in §1.1, not the ones it prints today
verify        completes; curse's tip is 57 characters and passes at 72
frame_probe   the pop-up is 164 px wider. Confirm it still clamps inside the
              arena at 1080x1920 and at the phone resolution — `x = clamp(g.x -
              w/2, 6, A.w - w - 6)` has 167 arena units of margin at 760, so
              this should be free, and "should be free" is why to check it
LOOK AT ONE   photograph a REAL first-application pop-up off a real match, for
              all eight statuses. Everything in this document is either a
              measurement or a hand-drawn tag; nobody has yet seen the widened
              box appear in a fight
```

---

# 4. WHAT NOT TO DO

- **Do not clip or ellipsise in `_tagFirst`.** The overflow is a symptom; a clip
  would hide the next one instead of failing loudly.
- **Do not add wrapping to `_tagFirst`.** The box is 92 px tall with the name on
  one line and the tip on the other; a second tip line has nowhere to go without
  a height change nobody has designed.
- **Do not "fix" the panel.** It wraps, it shrinks, it was never the problem.
- **Do not change the other seven tips** while the box is being widened. One
  change at a time on a surface that appears in every fight.

---

# Open decisions

1. **DOES THE WIDER BOX WANT A TALLER ONE TOO?** 760 x 92 is a flatter
   rectangle than 596 x 92. Not measured, not a mechanic, and only visible once
   change 2 is photographed in a real fight.

2. **THE OTHER SEVEN TIPS NOW HAVE 228 px OF ROOM EACH.** §1.1 — every one of
   them was written against 536 and the shortest is 378. Whether any of them is
   short because it was squeezed is a question for Rick, one tip at a time, and
   `hex` is the one with previous form: it is in `tip_audit`'s own docstring as
   the line that misled the person who wrote the wording convention.

3. **`tip_audit` STILL CANNOT SEE A MISLEADING TIP**, only an incomplete one —
   its own docstring says so. Curse's line was complete by that test and
   understated its effect threefold for a build and a half. There is no
   mechanical version of this check and the reviewer is Rick.
