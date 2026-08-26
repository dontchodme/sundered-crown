#!/usr/bin/env python3
"""Teach render.py to play the fight card LATE -- a cold open.

    python3 coldopen_patch.py            # patches tools/render.py in place

WHY THIS IS A RENDERER CHANGE AND NOT AN ENGINE CHANGE. The card is already
capable of this and nobody noticed: Match.step() returns early while introT > 0,
and Renderer.drawIntro() paints over `this.draw(m)` -- the match AS IT STANDS,
not a match pinned at t=0. So raising introT at t=6.0s freezes the fight where
it is, plays the card over the live picture, and hands the fight back on the
same frame. Measured, seed 1039818459, grudgebearer v thornwake:

    [1] straight-through and late-card summarise identically  Thornwake 110hp 30.68s
    [2] control (card over a genuinely frozen t=0 scene)       0.000
        the same bands with the card raised at t=6.0           0.703
        predicted from the 0.80 scrim (bare 3.749 x 0.20)      0.750
    [3] the frame after the card equals the frame before it    0.000

The tip build is untouched, 01-live is untouched, and no hash moves.

WHERE THE CUT GOES -- MEASURED, NOT CHOSEN. The card's own first beat is a clank
at 0.46s: two cards flying in from opposite edges and colliding. Raise it on the
fight's first clank and the two impacts become one. Across 144 matches (6
pairings x 24 seeds) on sc-ember:

    first clank   median 3.18s   p25 1.78   p75 4.58   p90 7.78   max 18.18

so the anchor is the event and the cap is the clock: first clank or --cold-open
SECONDS, whichever lands first. The median cold open is ~3.2s of two relics
closing, and the 18-second tail is truncated.

THE PART THAT ACTUALLY BREAKS. renderAudio() shifts EVERY event by the card
length, which is correct only when the card is first. With a late card the mix
has three regions -- fight before the cut (no shift), the card's own clank and
bell (placed by how much card is left), fight after the cut (shifted). Getting
this wrong is silent: the video looks right and the sound is a beat off. Each
event now carries the introT it fired under so the three cases can be told
apart, and the bed's act times are mapped the same way.
"""
from __future__ import annotations
import pathlib, sys

HERE = pathlib.Path(__file__).parent
TARGET = pathlib.Path("/home/claude/sc/sc/tools/render.py")

EDITS = [
    # 1. the SFX trap records the card clock alongside the match clock
    ("SFX trap carries introT",
     "    AC.SFX.play = function (kind, p) { self.events.push({ t: m.t, kind, p: p || {} }); };",
     "    /* `intro` is the card clock AT THE MOMENT THE SOUND FIRED. It is the\n"
     "       only way to tell the card's own clank from a clank in the hall:\n"
     "       both are pushed with the same frozen m.t. */\n"
     "    AC.SFX.play = function (kind, p) {\n"
     "      self.events.push({ t: m.t, intro: m.introT, kind, p: p || {} });\n"
     "    };"),

    # 2. raiseCard
    ("raiseCard()",
     "  state() {\n    const m = this.m;",
     "  /* Raise the card mid-match. Nothing else is touched: step() gates the\n"
     "     whole simulation on introT, so the fight is frozen, not rewound, and\n"
     "     it resumes on the identical frame. Returns the match time of the cut,\n"
     "     which the audio pass needs to place events either side of it. */\n"
     "  raiseCard(sec) { this.m.introT = sec; return this.m.t; },\n"
     "\n"
     "  state() {\n    const m = this.m;"),

    # 3. audio: three regions instead of one shift
    ("renderAudio takes the cut time",
     "  async renderAudio(dur, offset) {",
     "  async renderAudio(dur, offset, cutT) {\n"
     "    /* cutT < 0 means the card was first and every event sits after it --\n"
     "       the original behaviour. Otherwise the mix has three regions:\n"
     "         ev.intro > 0     the card's own clank: placed by how much card\n"
     "                          was left when it fired\n"
     "         ev.t <= cutT     fight audio from the cold open: NOT shifted\n"
     "         ev.t >  cutT     fight audio after the card: shifted by offset\n"
     "       The triggering clank itself sits exactly at cutT and belongs to the\n"
     "       cold open, so the comparison is strict. */\n"
     "    const vtime = (t, intro) =>\n"
     "      (intro > 0) ? cutT + (offset - intro)\n"
     "                  : (cutT < 0 || t > cutT) ? t + offset : t;"),

    ("bed act times respect the cut",
     "      S.bed(0, dur + tail,\n"
     "            AC.CONFIG.acts.slice(1).map(a => a.t + offset));",
     "      S.bed(0, dur + tail,\n"
     "            AC.CONFIG.acts.slice(1).map(a => vtime(a.t, 0)));"),

    ("events placed by region",
     "    for (const ev of this.events) {\n      cursor = ev.t + offset;",
     "    for (const ev of this.events) {\n      cursor = vtime(ev.t, ev.intro || 0);"),
]

PY_EDITS = [
    # 4. init with no card when cold-opening
    ("render() takes cold_open",
     "def render(a, b, seed, out, fps=30, hold=3.8, quality=0.94, max_seconds=90,\n"
     "           headless=True, verbose=True, keep=False, intro=None, game_path=None):",
     "def render(a, b, seed, out, fps=30, hold=3.8, quality=0.94, max_seconds=90,\n"
     "           headless=True, verbose=True, keep=False, intro=None, game_path=None,\n"
     "           cold_open=None):"),

    ("the card starts down on a cold open",
     "        page.evaluate(\"([a,b,s,i]) => window.__cap.init(a,b,s,i)\",\n"
     "                      [a, b, seed, intro])",
     "        # On a cold open the card starts DOWN and is raised on the first\n"
     "        # clank (or at the cap), so the fight opens on the hall.\n"
     "        page.evaluate(\"([a,b,s,i]) => window.__cap.init(a,b,s,i)\",\n"
     "                      [a, b, seed, 0.0 if cold_open is not None else intro])\n"
     "        cut_t = -1.0            # match time of the cut; <0 means no cold open\n"
     "        card_up = cold_open is None"),

    ("raise the card on the first clank",
     "            if fr[\"o\"]:\n                held += 1",
     "            if not card_up and (fr[\"c\"] > 0 or fr[\"t\"] >= cold_open):\n"
     "                # The event is the anchor and the clock is only the cap. A\n"
     "                # timer alone would cut mid-approach: only 17% of matches\n"
     "                # have clanked by 1.5s, 48% by 3.0s (144-match sweep).\n"
     "                cut_t = page.evaluate(\"([s]) => window.__cap.raiseCard(s)\",\n"
     "                                      [intro])\n"
     "                card_up = True\n"
     "                if verbose:\n"
     "                    why = \"first clank\" if fr[\"c\"] > 0 else \"cap\"\n"
     "                    print(f\"  cold open ends at sim {cut_t:.2f}s ({why}); \"\n"
     "                          f\"card up for {intro:.2f}s\", flush=True)\n"
     "            if fr[\"o\"]:\n                held += 1"),

    ("audio gets the cut time",
     "        wav_b64 = page.evaluate(\"([d,o]) => window.__cap.renderAudio(d,o)\",\n"
     "                                [dur, intro])",
     "        wav_b64 = page.evaluate(\"([d,o,c]) => window.__cap.renderAudio(d,o,c)\",\n"
     "                                [dur, intro, cut_t])"),

    ("report the cut",
     "        \"intro_seconds\": intro,",
     "        \"intro_seconds\": intro,\n"
     "        \"cold_open_seconds\": round(cut_t, 2) if cut_t >= 0 else None,"),

    ("CLI flag",
     "    ap.add_argument(\"--no-intro\", action=\"store_true\", help=\"skip the intro card\")",
     "    ap.add_argument(\"--no-intro\", action=\"store_true\", help=\"skip the intro card\")\n"
     "    ap.add_argument(\"--cold-open\", type=float, nargs=\"?\", const=5.0, default=None,\n"
     "                    metavar=\"CAP\",\n"
     "                    help=\"open on the fight and play the card on the first \"\n"
     "                         \"clank, or at CAP seconds, whichever comes first \"\n"
     "                         \"(default cap 5.0s -- p75 of first clank is 4.58s)\")"),

    ("pass it through",
     "                            keep=a.keep, intro=intro,",
     "                            keep=a.keep, intro=intro, cold_open=a.cold_open,"),
]


def main() -> int:
    s = TARGET.read_text(encoding="utf-8")
    for label, old, new in EDITS + PY_EDITS:
        n = s.count(old)
        if n != 1:
            print(f"! anchor for {label!r} hit {n} times, wanted exactly 1. "
                  f"Diff before re-anchoring -- do not loosen it.", file=sys.stderr)
            return 1
        s = s.replace(old, new, 1)
    TARGET.write_text(s, encoding="utf-8")
    print(f"  patched {TARGET}  ({len(EDITS)+len(PY_EDITS)} anchors, all unique)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
