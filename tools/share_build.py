#!/usr/bin/env python3
"""Wrap a build in the SHIPPED shell, patched for sharing.

    python3 share_build.py --src sundered-crown-all.html --out sundered-crown-share.html

v1 of this file hand-wrote a full-bleed phone shell -- a modal picker, a fading
control bar, no log -- and Rick's verdict was flat: "the ui for the public
handoff is really poor. what we had before was working great."

He is right, and the mistake is worth naming because it is the same one the
project has caught three times in other forms. The desktop shell is eleven
versions of accumulated decisions: the 9:16 card with the gold rim, the two
named slots, the button row, the event log that tells you WHY the fight went
the way it did. Replacing all of it with something written from scratch in one
sitting threw away every one of those decisions to solve a problem nobody had.

So this does not write a shell. It SLICES TWO THINGS from disk:

    the ENGINE   from --src           (the roster you want to share)
    the SHELL    from sundered-crown.html  (the UI that works)

and then applies a short list of exact-anchor patches for the things that are
genuinely different about a page going to strangers on unknown devices. Every
patch has to hit exactly once or the build fails, same as every other builder
here. The UI cannot drift from the one Rick approved, because it is not being
re-typed -- it is being copied.

--------------------------------------------------------------- THE PATCHES

  1. THE STAGE FITS THE VIEWPORT. The shipped card is `width:min(430px,96vw)`
     with a 9:16 aspect, which on a 390px phone is 665px of hall plus a title,
     a panel and a log -- about 1050px into a ~740px viewport, so the fight is
     half off-screen before you touch anything. Sized from HEIGHT instead, and
     `100dvh` so a mobile browser's disappearing chrome does not lie about it.
  2. THE RELIC COUNT IS DERIVED. The subtitle said "six relics". It is nine.
  3. SHARE METADATA. og: tags, a theme colour, and a viewport that tolerates a
     notch -- a link someone pastes into a chat should unfurl.
  4. `relicStatus` / `relicShot` ARE RE-EXPORTED. The shell carries its own
     `window.AC` and the shipped one predates both functions, so slicing it
     verbatim would drop them and verify.py's legibility contract would go
     quiet on exactly the two relics it was extended for.

Everything else -- the CSS, the markup, the selects, the button row, the log,
the frame loop -- is byte-identical to the shipped build, and the build asserts
both slices survived the trip.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
SHIPPED = "sundered-crown.html"
SCRIPT_OPEN = '<script>\n"use strict";'
SHELL_MARK = "/* ------------------------------------------------------------------ SHELL */"

# (label, anchor, replacement) -- applied to the SHELL slice (head + js).
PATCHES: list[tuple[str, str, str]] = [
    (
        # The anchor is the viewport meta ALONE. It used to include
        # `<title>The Sundered Crown</title>`, which meant the wording pass
        # renaming the page to "Super Weapon Ball: The Sundered Crown" silently
        # broke the shell slice — share_build could then only take its shell
        # from a build predating the rename, and quietly shipped the old title
        # onto every phone page. An anchor should be a structural landmark, not
        # a piece of copy somebody is expected to edit.
        "viewport + share metadata",
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#0A0810">\n'
        '<meta name="description" content="A spectator brawler with no input. Enchanted relics, one collapsing hall, no survivors. Pick two and watch.">\n'
        '<meta property="og:title" content="Super Weapon Ball: The Sundered Crown">\n'
        '<meta property="og:description" content="A spectator brawler with no input. Pick two relics and watch.">\n'
        '<meta property="og:type" content="website">',
    ),
    (
        "stage: size from height so a phone sees the whole hall",
        "  #stage{\n"
        "    width:min(430px,96vw); aspect-ratio:9/16; border-radius:6px; overflow:hidden;",
        "  /* SIZED FROM HEIGHT, not width. The shipped rule is width-first, which\n"
        "     is right on a desktop and puts two thirds of the hall below the fold\n"
        "     on a phone: 96vw of width is 665px of 9:16 hall, and the title, the\n"
        "     panel and the log still have to fit under it. Driving the height and\n"
        "     letting the aspect ratio derive the width keeps the whole fight on\n"
        "     screen at any size, and never grows past the 430px the desktop\n"
        "     layout was designed around.\n"
        "     `dvh` rather than `vh` because a mobile browser's chrome retracts on\n"
        "     scroll and `vh` reports the height it will have AFTERWARDS -- which\n"
        "     is a height this page can never reach, because it does not scroll. */\n"
        "  #stage{\n"
        "    aspect-ratio:9/16; width:auto; max-width:96vw;\n"
        "    height:min(calc(min(430px,96vw) * 16 / 9), calc(100vh - 250px));\n"
        "    height:min(calc(min(430px,96vw) * 16 / 9), calc(100dvh - 250px));\n"
        "    border-radius:6px; overflow:hidden;",
    ),
    (
        "log: give the hall the room on a short viewport",
        "  #log b{color:var(--gold);font-weight:700}",
        "  #log b{color:var(--gold);font-weight:700}\n"
        "  /* The log is the best thing in this UI and the first thing to give up\n"
        "     room when there is not enough: it is a record, so a short one still\n"
        "     works, while half a hall does not. */\n"
        "  @media (max-height:820px){ #log{max-height:84px} body{gap:10px;padding-top:12px} }\n"
        "  @media (max-height:680px){ #log{display:none} }",
    ),
    (
        "row label: stop clipping CHAMPION",
        "    width:52px; flex:none; font-weight:700; "
        "font-family:ui-sans-serif,system-ui,sans-serif;",
        "    /* Was a fixed 52px, which is two pixels narrower than CHAMPION at\n"
        "       this tracking -- the shipped build has been rendering CHAMPIO. It\n"
        "       survived eleven versions because a label you have read a thousand\n"
        "       times still parses with its last letter missing, which is exactly\n"
        "       the kind of thing that only shows up when the page goes to\n"
        "       someone who has never seen it. Sized to the content with the old\n"
        "       value kept as the floor, so the two rows still line up. */\n"
        "    width:auto; min-width:52px; white-space:nowrap;\n"
        "    flex:none; font-weight:700; "
        "font-family:ui-sans-serif,system-ui,sans-serif;",
    ),
    # THE TWO SUBTITLE PATCHES WERE REMOVED, 2026-08-14.
    #
    # They existed to fix an <h1> that said "six relics" as a literal — wrong
    # the moment the roster grew, and it grew three times. The fight-card
    # wording pass fixed that upstream by removing the count from the <h1>
    # altogether ("Super Weapon Ball / The Sundered Crown · one arena · no
    # survivors"), so both patches were solving a problem that no longer
    # exists — and their own word list stopped at "twelve", so on a
    # sixteen-relic roster the derived subtitle would have read "16 relics".
    #
    # A patch that outlives its bug does not sit harmlessly: its anchor is a
    # piece of copy, and the next rewording breaks the build instead of the
    # subtitle. Deleted rather than re-anchored.
    (
        "AC: re-export relicStatus / relicShot",
        "newMatch(selA.value, selB.value);\nrequestAnimationFrame(frame);",
        "/* The shell carries its own `window.AC` and the shipped one predates both\n"
        "   of these, so slicing it verbatim drops them -- and verify.py's\n"
        "   legibility contract would then go quiet on exactly the relics it was\n"
        "   extended for. Guarded, because a build without them is still valid. */\n"
        "if (typeof relicStatus === \"function\") window.AC.relicStatus = relicStatus;\n"
        "if (typeof relicShot   === \"function\") window.AC.relicShot   = relicShot;\n"
        "\n"
        "newMatch(selA.value, selB.value);\nrequestAnimationFrame(frame);",
    ),
]


def slice_engine(text: str, name: str) -> str:
    if text.count(SHELL_MARK) != 1:
        raise SystemExit(f"! {name}: expected exactly one SHELL marker, "
                         f"found {text.count(SHELL_MARK)}")
    if text.count(SCRIPT_OPEN) != 1:
        raise SystemExit(f"! {name}: could not find the single script opener")
    start = text.index(SCRIPT_OPEN) + len("<script>")
    return text[start:text.index(SHELL_MARK)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", default="sundered-crown-all.html",
                    help="the build whose ENGINE (roster, art, rules) is shared")
    ap.add_argument("--shell", default=SHIPPED,
                    help="the build whose SHELL is used. Default: the shipped UI.")
    ap.add_argument("--out", default="sundered-crown-share.html")
    a = ap.parse_args()

    src_p, shell_p = HERE / a.src, HERE / a.shell
    for p in (src_p, shell_p):
        if not p.exists():
            print(f"! missing {p}", file=sys.stderr)
            return 2

    src = src_p.read_text(encoding="utf-8")
    shell_src = shell_p.read_text(encoding="utf-8")

    engine = slice_engine(src, a.src)
    # The engine must be the simulation and nothing else. If any of these trip,
    # the split point has moved and this is not the game.
    must = ["const CONFIG", "const AFFINITIES", "const STATUS", "const WEAPONS",
            "const SHAPES", "class Sfx", "class Fighter", "class Match",
            "class Renderer", "function simulate", "function batch",
            "const WEAPON_BY_ID"]
    missing = [m for m in must if m not in engine]
    if missing:
        print("! engine slice is missing: " + ", ".join(missing), file=sys.stderr)
        return 2
    if "getElementById" in engine:
        print("! engine slice reaches into the DOM -- the split has moved", file=sys.stderr)
        return 2
    if len(engine) < 150_000:
        print(f"! engine slice is only {len(engine):,} bytes; expected 170k+", file=sys.stderr)
        return 2

    head = shell_src[:shell_src.index(SCRIPT_OPEN)]
    shell = shell_src[shell_src.index(SHELL_MARK):]
    ui = head + "\x00ENGINE\x00" + shell          # patch head and shell as one text

    for label, anchor, repl in PATCHES:
        n = ui.count(anchor)
        if n != 1:
            print(f"FAIL  {label}: anchor found {n} times, expected exactly 1",
                  file=sys.stderr)
            print(f"      anchor starts: {anchor[:78]!r}", file=sys.stderr)
            return 1
        ui = ui.replace(anchor, repl, 1)

    out = ui.replace("\x00ENGINE\x00", "<script>" + engine)

    # The whole point of this file: the shared page contains the verified engine
    # verbatim AND the shipped shell verbatim apart from a stated patch list.
    assert engine in out, "engine text was altered in transit"
    if out.count('<canvas id="cv"') != 1:
        print("! expected exactly one canvas#cv", file=sys.stderr)
        return 2
    if "selA" not in out or "id=\"log\"" not in out:
        print("! the shell lost its picker or its log", file=sys.stderr)
        return 2

    (HERE / a.out).write_text(out, encoding="utf-8")
    print(f"engine  {len(engine):>8,} bytes  (byte-identical slice of {a.src})")
    print(f"shell   {len(head) + len(shell):>8,} bytes  (from {a.shell}, "
          f"{len(PATCHES)} patches)")
    print(f"wrote   {a.out}  {len(out):>8,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
