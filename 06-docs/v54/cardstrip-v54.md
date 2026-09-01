# v54b — THE FIGHT CARD IS OUT. Six sessions after rule 1 declared it dead, and the thing that made it worth removing is not the 545 lines — it is that a retired feature's constants were still inside the clock.

**2026-08-31.** `tools/cardstrip_build.py`, `02-chain/sc-nightfell.html` →
`02-chain/sc-nocard.html`. Archive:
`04-experiments/_fight-card-retired.js`.

Rick: *"if we can afford to remove the fight card then do it. theres no sense
in keeping it as i dont intend to use it again. we can just archive it."*

---

# 1. WHAT WAS ACTUALLY REMOVED

The card had been dead as a **deliverable** since `08-analytics` measured it
losing 71–75% of the audience before the fight started. Rule 1 has read *"THE
FIGHT CARD IS DEAD. Nothing ships with one"* for six versions and
`cinema_clip --intro` has refused to run without `--legacy-card` for just as
long.

None of that removed it as **code**:

```
545 lines   drawIntro, _introCard, _introFacts, _introLayout, _introWrap,
            _introTape, _introFx — plus the two section comments introducing
            them, which is what makes it 491 lines of code and 54 of prose
  1 field   Match.introT, which thirty tools still zero defensively
  1 guard   _introScene, branched on by four unrelated draw calls
  1 config  CONFIG.intro { dur, clash, reveal }
  1 button  the page's own "Intro card" toggle, and the `introOn` flag
  3 flags   cinema_clip's --intro, --cold-open, --legacy-card
```

**The reason it was worth doing is the config, not the line count.**
`CONFIG.intro.dur` was arithmetic in three places that have nothing to do with
a title card: the act/seal times (`match.introT + a.t`), the app's own capture
length (`CONFIG.timeout + CONFIG.intro.dur + 6`), and the director's
don't-cut-yet guard. **A dead feature whose constants are inside the clock is
not dormant** — it is a four-second offset that every future timing question
has to know to subtract.

---

# 2. THE THREE THINGS CHECKED BEFORE ANYTHING WAS CUT

## 2a. IT CANNOT MOVE A FIGHT, AND THE ENGINE HAD ALREADY PROVED IT

`step()`'s hold branch, in its own words:

> *"The card holds the match at t=0. Nothing in the sim advances, so the
> recorded duration and every statistic stay exactly what they would be
> without an intro"* … *"Presentation clock only — simulate() never sets
> introT, so no sweep ever runs this branch."*

Measured anyway, because a comment is a claim: **`engine_ab` 2808/2808 matches
identical field for field across all 27 relics**, and **`render_ab` 36/36
frames pixel-identical** over six pairings at 1.5s to 40s. `verify --n 40`
returns the same 12/13 with the same known Lightkeeper/Farwarden 77.3s, the
same 18.2pp spread, and the same 48.8s overall mean.

## 2b. THE SCRUNCH PANEL LOOKED LIKE A DEPENDENCY AND IS NOT

This was the one that could have cost the game copy. The panel's own comment
said *"Every string comes from `_introFacts` and `STATUS[].tip`, which the
intro card already uses"* — which reads like the card owns the composition.

It does not. `drawScrunchPanel` **deliberately stopped** sharing those helpers
and composes its own facts from `STATUS[].tip`, `relicStatus()`, `w.ult.tip`
and `w.ult.charge`. So `w.ult.tip` keeps its reader and does **not** become
write-only data the way `blurb` did (v52 open decision 5).

> **BUT THE PANEL IS NOW THE ONLY SURFACE THE GAME TEACHES ANYTHING ON.** A
> wrong string is now wrong everywhere a viewer can see it. That is an
> argument FOR open item 4 — `tip_audit` still does not check ult tips — not
> against it.

## 2c. `_artShape` AND `_artBox` ARE NOT THE CARD'S

They sit in the middle of the card's block and `_artShape` also draws the
relic silhouette for the tug bar. That is why the excision is **two spans and
not one**, and why each span asserts on what it contains rather than trusting
a line range.

---

# 3. THE PROSE WAS PART OF THE REMOVAL

Four comments elsewhere in the build defined themselves **by reference to the
card**: the config header (*"`introT` defaults to 0 on a Match, so simulate()
…"*), the presentation-clock paragraph (*"Like introT in that … UNLIKE introT
in that …"*), and both of the scrunch panel's.

In a codebase that teaches through its comments, a paragraph explaining itself
against something that no longer exists is worse than no paragraph. All four
are rewritten by the builder, and **both cuts were moved back to start at the
section comment that introduces them** — the first pass cut at the method
header and left a twenty-line description of a four-second card hanging above
nothing.

> This is the same finding as the DEADFALL prose commit two hours earlier, and
> it is now twice in one session: **a mechanic is not removed until the
> sentences about it are.**

---

# 4. TWO THINGS THE BUILDER LEARNED THE HARD WAY

**A SELF-BALANCED COMMENT CHECK IS THE WRONG CHECK.** Every builder in this
repo asserts the replacement text has matching `/*` and `*/`. That works while
every edit is a whole block, and it is wrong the moment one starts inside one
comment and ends inside the next — which rewriting the panel's two paragraphs
does. It refused a correct substitution. What has to hold is that the edit does
not **change** the nesting, so the check is now a delta between old and new.

**AND THE FLAG EXCISION TOOK A NEIGHBOUR.** `--cold-open`, `--intro` and
`--legacy-card` were removed by slicing between two indices, and
`--verdict-hold` was sitting between them. It died on the first render with an
`AttributeError`, which is the good case; a flag with a default that silently
stopped being parsed would not have. **Index-based excision in a builder is
fine because the builder asserts on its span; index-based excision in a
hand-patch is not.**

---

# 5. WHAT THE COLD OPEN'S FINDING BECAME

`--cold-open` filmed the fight first and dropped the card in on the first
clank. The card is gone but the finding under it is not, and it is preserved
as a comment where the code used to be:

> The EVENT is the anchor; the clock is only a cap. Over 144 matches a timer
> alone cuts mid-approach — 17% have clanked by 1.5s, 48% by 3.0s.

That is exactly why `scrunchAuto` arms the panel on `clankCount > 0` rather
than on a timer, which is now the line immediately below where the cold open
used to be.

---

# Open decisions

1. **`04-experiments/_fight-card-retired.js` IS A RECORD, NOT A MODULE.** It
   will not run as it stands — these are `Renderer` methods lifted out of a
   class body, and they read `IC`, `CONFIG.intro` and `_introScene`, of which
   two no longer exist. The header says to revive it from the build sha it was
   cut from rather than by pasting it back. If that is not the right archive
   shape, say so now while the sha is fresh.
2. **`tools/card_sheet.py` IS NOW DOUBLY DEAD.** It was already broken —
   hardcoded to `sundered-crown-vigil.html`, a build that does not exist — and
   it photographed fight cards. It is a candidate for deletion rather than
   repair, and `tools/README.md` already flags it as an ancestor kept for
   reference.
3. **`introfit_probe.py` AND `introfit_build.py` STILL EXIST** and their
   subject does not. Same question as 2: delete, or keep as chain history?
   Nothing runs them and the chain does not need them to reproduce the tip.
4. **THE 545 LINES ARE GONE AND SO IS AN ARGUMENT FOR `roMode`.** Not
   investigated. The card had its own scrim-and-reentry path through `draw()`
   and it is worth someone checking whether any renderer flag existed only to
   serve it.
