#!/usr/bin/env python3
"""THE FIGHT CARD IS REMOVED. Rule 1, open item 2, five sessions unmoved.

    python cardstrip_build.py --src ../02-chain/sc-nightfell.html \
                              --out ../02-chain/sc-nocard.html

Rick, 2026-08-31: *"if we can afford to remove the fight card then do it.
theres no sense in keeping it as i dont intend to use it again. we can just
archive it."*

## WHAT THE CARD WAS

A four-second full-screen title card at the head of every match: two relic
plates sliding in from top and bottom, clashing at the centreline, a tape of
scrolling text between them, and a bell on the reveal. It was retired as a
DELIVERABLE long ago -- CLAUDE.md rule 1, "THE FIGHT CARD IS DEAD. Nothing
ships with one." -- after `08-analytics` measured it losing 71-75% of the
audience before the fight started. `cinema_clip --intro` and `--cold-open`
have refused to run without `--legacy-card` ever since.

But it was never taken OUT, and a dead feature that still runs is not free:

  * it is 545 lines of renderer nobody reads and every future renderer change
    has to not break,
  * it holds `Match` state (`introT`) that thirty tools zero defensively,
  * it owns a reentry guard (`_introScene`) that four unrelated draw calls
    still branch on, and
  * `CONFIG.intro.dur` is arithmetic in the seal times and in the app's own
    capture length, so the card is inside the clock of a build that never
    shows it.

## THE CARD IS ARCHIVED, NOT DELETED

Every removed line goes to `04-experiments/_fight-card-retired.js` with the
sha of the build it came out of. Rick asked for it archived; `04-experiments`
is where this project keeps unshipped variants and controls, and the file
carries enough context to be read cold.

## WHAT THIS IS NOT ALLOWED TO CHANGE

**THE FIGHT.** The card is presentation and the engine says so in its own
words -- `step()`'s hold branch: *"The card holds the match at t=0. Nothing in
the sim advances, so the recorded duration and every statistic stay exactly
what they would be without an intro"*, and *"simulate() never sets introT, so
no sweep ever runs this branch."* `engine_ab` must therefore be bit-identical
over all 27 relics, and that is the gate.

**THE SCRUNCH PANEL**, which ships and which is the ONLY surface a viewer
reads copy on now. It looked like a dependency and is not: `drawScrunchPanel`
composes its own facts from `STATUS[].tip`, `relicStatus()`, `w.ult.tip` and
`w.ult.charge`, and its own comment says why it deliberately stopped calling
`_introFacts`. So `w.ult.tip` does NOT become write-only data the way `blurb`
did -- it keeps its reader, and verify's 72-character limit still governs it.

**`_artShape` AND `_artBox`**, which sit in the middle of the card's block and
are not the card's: `_artShape` draws the relic silhouette for the tug bar as
well. That is why the excision below is two spans and not one, and why it
asserts on what it is about to remove rather than trusting a line range.

## THE ASSERTION THAT MATTERS

A printed count is something a person has to notice (v53, the seventh
`f.w.reach` read). So this REFUSES TO WRITE if a single mention of `introT`,
`_intro`, or `CONFIG.intro` survives anywhere in the output.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# ---- THE TWO SPANS OF RENDERER, BY HEAD AND TAIL --------------------------
# Bounded excision rather than a literal anchor: 545 lines is too much text to
# hold in a builder, and a line range is not an assertion. Each cut states
# what it expects to be removing and refuses on anything else.
CUTS = [
    ("the card itself, and the section comment that introduces it",
     "  /* ------------------------------------------------------------- intro --- */",
     "  /* The silhouette, drawn identically for the card and for the",
     ("drawIntro(m){", "_introCard(f, y0, CH, imp, fade){",
      "_introTape(m, restA + CH", "this._introFx(m, imp, fade)"),
     (7000, 15000)),
    ("its facts, layout, tape and effects",
     "  /* The facts, as data.  Rick 08-14: no SHOOTS line",
     "  /* One line, not two. The taller hall took the space",
     ("_introLayout(facts, top, bot){", "_introWrap(text, maxW, size, maxLines){",
      "_introTape(m, topY, botY, imp, fade){", "_introFx(m, imp, fade){"),
     (7000, 14000)),
]

# ---- AND THE REFERENCE SITES ---------------------------------------------
EDITS = [

("CONFIG.intro", '''  intro: { dur: 4.0, clash: 0.46, reveal: 0.50 },''',
 '''  /* `intro` IS GONE WITH THE FIGHT CARD (`cardstrip_build.py`). It was
     { dur: 4.0, clash: 0.46, reveal: 0.50 } and it was arithmetic in three
     places that had nothing to do with a title card -- the seal times, the
     app's capture length, and the director's "do not cut yet" guard. A dead
     feature whose constants are inside the clock is not dormant. */'''),

("Match.introT", '''    this.introT = 0;''',
 '''    /* `introT` IS GONE WITH THE FIGHT CARD. It held the match at t=0 while
       the card played; nothing else ever read it as anything but "is the card
       up". Thirty tools still zero it defensively and all thirty are
       harmless -- assigning to a field no code reads is a no-op. */'''),

("step.hold", '''    /* The card holds the match at t=0. Nothing in the sim advances, so the
       recorded duration and every statistic stay exactly what they would be
       without an intro. */
    if (this.introT > 0){
      /* Presentation clock only — simulate() never sets introT, so no sweep
         ever runs this branch. The clank is the cards meeting at the
         centreline; the bell stays on the cut. Both fire on clock CROSSINGS
         so a 4x-speed dt cannot fire either twice. */
      const el0 = CONFIG.intro.dur - this.introT;
      this.introT -= dt;
      if (el0 < CONFIG.intro.clash &&
          CONFIG.intro.dur - this.introT >= CONFIG.intro.clash)
        SFX.play("clank", { mass: Math.max(this.a.w.mass, this.b.w.mass) });
      if (this.introT <= 0) SFX.play("seal");   // the bell, on the reveal
      return;
    }
    if (this.over){ this.decay(dt); return; }''',
 '''    /* THE CARD'S HOLD IS GONE. It froze the match at t=0 for four seconds
       and its own comment is the proof this removal cannot move a fight:
       "Nothing in the sim advances, so the recorded duration and every
       statistic stay exactly what they would be without an intro", and
       "simulate() never sets introT, so no sweep ever runs this branch."
       A match now starts on its first step. */
    if (this.over){ this.decay(dt); return; }'''),

("draw.dispatch", '''    if (m.introT > 0 && !this._introScene){ this.drawIntro(m); return; }''',
 '''    /* The fight card's entry point stood here. It is gone, and with it the
       `_introScene` reentry guard that four unrelated draw calls below had to
       branch on -- the card drew the real match behind its own scrim, so
       every one of those was asking "am I being drawn inside a title card?".
       Nothing is, ever again. */'''),

("draw.scrunchGuard", '''    let __sk = 1, __sv = null;
    if (!this._introScene){
      __sk = this.scrunchK(m);''',
 '''    let __sk = 1, __sv = null;
    {
      __sk = this.scrunchK(m);'''),

("draw.hud", '''      if (!this._introScene) this.drawHud(m);''',
 '''      this.drawHud(m);'''),

("draw.footer", '''    if (!this._introScene) this.drawFooter(m);''',
 '''    this.drawFooter(m);'''),

("drawTug", '''    if (!TUG.on || this._introScene) return;''',
 '''    if (!TUG.on) return;'''),

# ---- AND THE PROSE THAT EXPLAINED IT SOMEWHERE ELSE ----------------------
# A comment describing a field that no longer exists is worse than no comment,
# and this codebase teaches through its comments -- so the three sentences
# elsewhere in the build that leaned on `introT` to explain something else are
# rewritten rather than left dangling.
("prose.config", '''     `introT` defaults to 0 on a Match, so simulate(), batch() and the tuner are''',
 '''     Nothing holds a match at t=0 any more -- the fight card is gone
     (`cardstrip_build.py`) -- so simulate(), batch() and the tuner are'''),

("prose.clocks", '''    /* Presentation clocks. Like introT in that simulate() never arms them --
       `scrunchAuto` is set by __inject and newMatch, which only presentation
       and capture layers call -- and UNLIKE introT in that step() has no early
       return for them. The hall makes room; it does not stop. */''',
 '''    /* Presentation clocks: simulate() never arms them, because `scrunchAuto`
       is set by __inject and newMatch, which only presentation and capture
       layers call. The hall makes room; it does not stop.

       This paragraph used to draw its contrast against the fight card's
       `introT`, which DID stop the hall. There is nothing left to contrast
       with: `step()` has no early return for anything but the fight ending. */'''),
# ---- AND THE PANEL'S OWN COMMENTS, WHICH DEFINED IT AGAINST THE CARD -----
# `drawScrunchPanel` explained itself three times by reference to the thing
# being removed -- "so the panel and the card cannot drift", "the same single
# source of truth the card reads". With the card gone those sentences describe
# a relationship that has no other end. They are not deleted: the REASON the
# panel composes its own facts is still the reason, and it is now the whole
# teaching surface rather than the second one, which is worth saying out loud.
("panel.header", '''  /* The panel. Laid out FOR this strip rather than borrowed from the middle of
     a full-screen card -- `_introTape` is 546px tall and centred for a 1920
     frame, and reusing it meant scaling it to 0.9 and hoping. Every position
     below is derived from the box it is actually given, so the panel adapts if
     `k` moves instead of being re-tuned by hand. */''',
 '''  /* The panel. Laid out FOR this strip rather than borrowed from the middle
     of the full-screen fight card that used to open every match -- that card's
     tape was 546px tall and centred for a 1920 frame, and reusing it meant
     scaling it to 0.9 and hoping. Every position below is derived from the box
     it is actually given, so the panel adapts if `k` moves instead of being
     re-tuned by hand. (The card is gone entirely now --
     `cardstrip_build.py` -- so this is not one of two teaching surfaces any
     more. It is the only one.) */'''),

("panel.facts", '''     Every string comes from `_introFacts` and `STATUS[].tip`, which the intro
     card already uses -- so the panel and the card cannot drift, and the
     ">=40 char" tip discipline verify.py enforces still governs the copy. */
  /* SELF-CONTAINED fact composition and wrapping.

     Earlier cuts called `_introFacts` / `_introWrap` so the panel and the intro
     card could not drift. That is the right instinct and the wrong dependency:
     those helpers were extracted late in the chain, and `01-live` composes the
     same facts INLINE inside `_introCard`. A patch that only applies to builds
     newer than the extraction is not a patch for the live session.

     So the panel composes its own, from the same single source of truth the
     card reads -- `STATUS[].tip`, `relicStatus()`, `w.ult.tip` and
     `w.ult.charge`. The STRINGS cannot drift because there is only one copy of
     them; only the composition is duplicated, and the panel is its own surface
     with its own layout anyway. The cooldown goes on a chip rather than being
     concatenated into the tip, which is where the newer card puts it too. */''',
 '''     Every string comes from `STATUS[].tip`, `relicStatus()`, `w.ult.tip`
     and `w.ult.charge`, and the tip-length discipline verify.py enforces
     governs all of it. */
  /* SELF-CONTAINED fact composition and wrapping.

     THIS IS NOW THE ONLY PLACE THE GAME TEACHES ANYTHING, and that raises the
     stakes on the paragraph below rather than lowering them. The fight card
     was the other one and it is gone (`cardstrip_build.py`); if a string is
     wrong here, it is wrong everywhere a viewer can see.

     It composes its own facts rather than sharing a helper, and that was a
     deliberate call back when there WAS something to share with: the extracted
     helpers arrived late in the chain and `01-live` composed the same facts
     inline, so a patch against the helper was not a patch for the live
     session. The argument outlives the card. THE STRINGS cannot drift because
     there is only one copy of them -- `STATUS[].tip`, `relicStatus()`,
     `w.ult.tip`, `w.ult.charge` -- and only the composition is local, which is
     right for a surface with its own layout. The cooldown goes on a chip
     rather than being concatenated into the tip. */'''),
]


def one(src: str, old: str, new: str, label: str) -> str:
    # THE BALANCE CHECK COMPARES OLD AGAINST NEW, NOT NEW AGAINST ITSELF.
    # Every other builder in this repo asserts `new` is self-balanced, which
    # works while every replacement is a whole block. It is wrong the moment a
    # replacement starts inside one comment and ends inside the next -- and
    # rewriting the scrunch panel's two paragraphs does exactly that, so the
    # self-balanced form refused a substitution that was correct. What actually
    # has to hold is that the edit does not CHANGE the nesting, which is the
    # delta being zero.
    d_open = new.count("/*") - old.count("/*")
    d_close = new.count("*/") - old.count("*/")
    if d_open != d_close:
        raise SystemExit(f"BLOCK {label}: this edit changes comment nesting by "
                         f"{d_open:+d} '/*' and {d_close:+d} '*/'. The page "
                         f"will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def cut(src: str, label: str, head: str, tail: str, musts, bounds):
    lo, hi = bounds
    if src.count(head) != 1:
        raise SystemExit(f"CUT {label}: head is not unique ({src.count(head)}).")
    if src.count(tail) != 1:
        raise SystemExit(f"CUT {label}: tail is not unique ({src.count(tail)}).")
    i, j = src.index(head), src.index(tail)
    span = src[i:j]
    if not (i < j and lo < len(span) < hi):
        raise SystemExit(f"CUT {label}: the span is {len(span)} characters, "
                         f"outside {lo}..{hi}. Refusing.")
    for m in musts:
        if m not in span:
            raise SystemExit(f"CUT {label}: the span does not contain {m!r}. "
                             f"Refusing.")
    if span.count("/*") != span.count("*/"):
        raise SystemExit(f"CUT {label}: the span's comments are unbalanced, so "
                         f"the cut would take a `*/` the rest of the file needs.")
    print(f"  cut   {label}: {len(span)} characters, "
          f"{span.count(chr(10))} lines")
    return src[:i] + src[j:], span


ARCHIVE_HEAD = '''/* THE FIGHT CARD, RETIRED. Removed from the build by tools/cardstrip_build.py.
 *
 * Rick, 2026-08-31: "if we can afford to remove the fight card then do it.
 * theres no sense in keeping it as i dont intend to use it again. we can just
 * archive it."
 *
 * WHAT IT WAS. A four-second full-screen title card at the head of every
 * match: a relic plate sliding down from the top, another up from the bottom,
 * the two clashing at the centreline at `CONFIG.intro.clash`, a tape of
 * scrolling text between them, and a bell on the reveal. `drawIntro` drew the
 * real renderer's real match behind a scrim, which is what the `_introScene`
 * reentry guard was for.
 *
 * WHY IT WENT. It was retired as a DELIVERABLE long before it was removed as
 * CODE -- `08-analytics` measured it losing 71-75%% of the audience before the
 * fight began, and CLAUDE.md rule 1 has read "THE FIGHT CARD IS DEAD. Nothing
 * ships with one" for six versions. `cinema_clip --intro` and `--cold-open`
 * refused to run without `--legacy-card` for just as long. What finally
 * removed it is that a dead feature is not free: 545 lines of renderer that
 * every future renderer change has to not break, a `Match` field thirty tools
 * zeroed defensively, a draw-time reentry guard on four unrelated calls, and
 * `CONFIG.intro.dur` sitting inside the seal-time arithmetic of a build that
 * never showed a card.
 *
 * WHAT REPLACED IT. Nothing, on purpose. The teaching moved to the SCRUNCH
 * PANEL, which is drawn over the live fight at the first point of contact and
 * composes its own facts from `STATUS[].tip`, `relicStatus()`, `w.ult.tip`
 * and `w.ult.charge` -- so removing this cost the game no copy at all.
 *
 * THIS FILE IS A RECORD AND NOT A MODULE. It will not run as it stands: these
 * are `Renderer` methods lifted out of a class body, and they read `IC`,
 * `CONFIG.intro`, `shellHash`, `_artShape`, `_artBox` and `_introScene`, of
 * which the middle two no longer exist in the build. To revive it, take the
 * build it was cut from (sha below) rather than pasting this back.
 *
 * CUT FROM   %SRC% sha256:%SHA%
 * BY         tools/cardstrip_build.py
 * ON         the build that became %OUT%
 */

'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-nightfell.html")
    ap.add_argument("--out", default="../02-chain/sc-nocard.html")
    ap.add_argument("--archive",
                    default="../04-experiments/_fight-card-retired.js")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    arc_p = (HERE / A.archive).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    sha = hashlib.sha256(s0.encode()).hexdigest()
    print("\nTHE FIGHT CARD -- removed, and archived")
    print(f"  src {src_p.name}  {sha[:16]}")
    if "drawIntro" not in s0:
        raise SystemExit("this source has no fight card -- already stripped")

    spans = []
    for label, head, tail, musts, bounds in CUTS:
        s, span = cut(s, label, head, tail, musts, bounds)
        spans.append(span)

    for label, old, new in EDITS:
        s = one(s, old, new, label)

    # THE APP'S OWN TOGGLE AND THE SEAL ARITHMETIC. Located rather than
    # anchored verbatim, because these live in the page's UI glue where the
    # surrounding text is long and changes often.
    for label, old, new in [
        # THE PAGE HAD A BUTTON FOR IT. `introOn` and its handler go with the
        # card; a control that toggles a feature that no longer exists is the
        # worst kind of dead code, because it looks operable.
        ("app.button", '''    <button id="btnIntro">Intro card</button>\n''', ""),
        ("app.flag", "let introOn = true;\n", ""),
        ("app.handler", '''const btnIntro = document.getElementById("btnIntro");
btnIntro.onclick = () => {
  introOn = !introOn;
  btnIntro.textContent = introOn ? "Intro card" : "No intro";
  btnIntro.classList.toggle("off", !introOn);
  if (match && match.t === 0) match.introT = introOn ? CONFIG.intro.dur : 0;
};

''', ""),
        ("app.arm", "  match.introT = introOn ? CONFIG.intro.dur : 0;\n", ""),
        ("cine.gate", "&& !m.over && m.introT <= 0", "&& !m.over"),
        ("cine.cut", "if (!this.cut && m.introT <= 0){", "if (!this.cut){"),
        ("capture.gate", "!(m.introT > 0) && m.t >= 0 && m.t < t;",
         "m.t >= 0 && m.t < t;"),
        ("seal.dur", "const dur = CONFIG.timeout + CONFIG.intro.dur + 6;",
         "const dur = CONFIG.timeout + 6;"),
        ("seal.times", "CONFIG.acts.slice(1).map(a => match.introT + a.t)",
         "CONFIG.acts.slice(1).map(a => a.t)"),
    ]:
        s = one(s, old, new, label)

    # THE ASSERTION, AND IT IS WHY THIS IS SAFE TO DO AT ALL. A printed count
    # is something a person has to notice; this is not.
    # COMMENTS ARE STRIPPED FIRST. This build explains itself in the file and
    # the replacement comments above deliberately NAME what they removed --
    # `curse_check` fired on its own explanation once and `curse_build` refused
    # to write on its, both in one session.
    import re as _re
    code = _re.sub(r"/\*[\s\S]*?\*/", "", s)
    code = _re.sub(r"^\s*//.*$", "", code, flags=_re.M)
    survivors = [ln.strip() for ln in code.splitlines()
                 if "introT" in ln or "_intro" in ln or "CONFIG.intro" in ln
                 or "introOn" in ln or "btnIntro" in ln]
    if survivors:
        raise SystemExit(
            "THE CARD IS NOT FULLY OUT. These lines still reference it:\n  "
            + "\n  ".join(survivors[:10]))
    print("  gone  no live reference to introT, _intro, CONFIG.intro, "
          "introOn or btnIntro survives")

    arc_p.parent.mkdir(parents=True, exist_ok=True)
    arc_p.write_text(
        ARCHIVE_HEAD.replace("%SRC%", src_p.name).replace("%SHA%", sha)
                    .replace("%OUT%", out_p.name)
        + "\n\n/* ---- 1 of 2 ---- */\n" + spans[0]
        + "\n\n/* ---- 2 of 2 ---- */\n" + spans[1],
        encoding="utf-8", newline="\n")
    print(f"  arc {arc_p.name}  {len(spans[0]) + len(spans[1])} characters kept")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)")
    print("\n  NEXT:")
    print(f"    python engine_ab.py --a {A.src} --b {A.out} --n 8   # ALL 27")
    print(f"    python verify.py --game {A.out} --n 40")
    print(f"    python cinema_clip.py --game {A.out} --a nightfell "
          f"--b bulwarden --seed 3301 --full")
    return 0


if __name__ == "__main__":
    sys.exit(main())
