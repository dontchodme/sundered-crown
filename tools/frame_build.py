#!/usr/bin/env python3
"""THE ARENA FITS A BOX, NOT A WIDTH. Vertical-video safe framing, in the game.

    python3 frame_build.py --src ../02-chain/sc-foregone.html \
                           --out ../02-chain/sc-safeframe.html

Rick: *"the last few videos have been poorly cropped. they are missing a lot of
the bottom of the frame. these should be formated for tiktok."*

## What was actually happening, and it was not a crop

The game renders full-bleed 1080x1920 and always has. **`cinema_clip --shorts`
was shrinking it to 79% and boxing it** -- 114px bars either side and 312px of
dead black at the bottom -- and that was a deliberate fix from an earlier
session to an earlier complaint of Rick's: action at the bottom was getting cut
off, `cinema_edge_probe` showed the FILE was clean (0/8 wall cuts clipped the
near relic), and the diagnosis was that TikTok's caption bar was covering it.

The diagnosis was right and the fix was in the wrong place. Shrinking the whole
frame to dodge the platform's UI costs every pixel of the video to protect the
bottom sixth of it, and it reads as amateur next to a feed where everything
else is edge to edge.

**The fix belongs in the layout.** Reserve a strip at the bottom of the DESIGN
space, fit the arena above it, and let the encode go full-bleed. Then nothing
is boxed and nothing that matters is covered.

## Why the arena did not already fit

```
this.pad = 12;
this.aw = this.W - this.pad * 2;          // 1056
this.scale = this.aw / CONFIG.arena.w;    // 1056 / 520 = 2.031
this.ah = CONFIG.arena.h * this.scale;    // 800 * 2.031 = 1625
this.arenaTop = this.hud + 24;            // 176
```

**Width-bound**, and the build's own comment says so: *"the arena is
width-bound -- its height follows from the sim and the frame width -- so the
height the HUD gave back cannot become more arena."* The hall therefore runs
176..1801 of 1920, and the bottom 200px of it sits under the caption.

This makes `scale` the smaller of the two bounds, which is what a fitted layout
should always have been, and recentres horizontally -- exactly what the scrunch
already does at the end of its own block.

## The identity, and it is exact

    FRAME.foot = 0  ->  availH = 1744, 1744/800 = 2.18 > 2.031,
                        so the WIDTH still binds and every one of the four
                        numbers comes out at its old value.

So the old layout is not approximated by this code, it is a **value** of it.
`frame_probe.py` asserts that against a pixel comparison rather than against
this paragraph.

## What it costs

The arena's aspect is 0.65 and the box above the strip is 0.75, so the arena
can no longer touch the side walls: at `foot` 340 it is 913 wide in a 1080
frame, leaving 84px of the game's own background either side. That is
background, not letterbox -- the hall has a drawn frame and the margin reads as
composition. It is also 84px against the 114px of black the encode was adding,
so the picture is LARGER than what ships today in both dimensions.

**This changes the framing of every relic's video, not just Foregone's.**
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

EDITS = [
    ("FRAME, the one named place",
     '''const BAND = { pos: "top" };''',
     '''const BAND = { pos: "top" };
/* VERTICAL-VIDEO SAFE FRAMING. `foot` is design-space pixels reserved at the
   BOTTOM of the 1080x1920 frame, below the arena, for the platform to draw its
   own caption, handle and music bar over. TikTok and Shorts both occupy
   roughly the bottom 15-20%; 340 is 17.7%.

   IT SHIPS AT ZERO. 340 was an over-correction and Rick rejected it twice:
   "the last few videos have been poorly cropped ... missing a lot of the
   bottom of the frame", and then again after the reserve existed, "the video
   still has the bottom of the frame cut off. why can we not stretch this to
   the full length?"

   Measured, on the same frame:

     foot    hall      runs        ink rows    fills   side margin
        0    1056x1625  176..1801    9..1847     96%    12px
      120    1048x1612  176..1788    9..1834     95%    16px
      340     905x1392  176..1568    9..1614     84%    88px

   The reserve cost twelve points of frame and 76px a side to protect the
   bottom sixth from a caption -- and the caption claim was an INFERENCE from
   an earlier session, never something Rick said. He has now twice said the
   opposite. The encode fix that came with it was right and stands: the
   79% letterbox is gone and the delivery is scale=1080:1920.

   The knob stays, with its cost measured, because the next platform may want
   it. The value is 0.

   ZERO IS AN EXACT IDENTITY, not an approximation of one -- at foot 0 the
   available height is 1744, 1744/800 = 2.18 is looser than 1056/520 = 2.031,
   the WIDTH binds exactly as it always did, and all four layout numbers come
   out at their old values. That is the negative control frame_probe.py runs,
   and it is why this constant can be dialled to nothing without a second code
   path existing to be wrong. */
const FRAME = { foot: %FOOT% };'''),

    ("the arena fits a box",
     '''    this.pad = 12;''',
     '''    this.pad = 12;
    /* Set below, from the fit. Left here so the field's declaration order and
       its old value are both still visible: 12 is what it is whenever the
       width binds, which is every case with FRAME.foot at 0. */'''),

    ("the scrunch panel lives in the safe box too",
     '''    const y = this.arenaTop + this.ah * k + S.gap;
    const h = S.bottom - y, x = 24, w = this.W - 48;''',
     '''    const y = this.arenaTop + this.ah * k + S.gap;
    /* AND THE PANEL LIVES IN THE SAME SAFE BOX THE HALL DOES.

       `CONFIG.scrunch.bottom` is a hardcoded 1812 in design space, from when
       1812 was simply "near the bottom of the frame". Reserving a strip made
       it two bugs at once, and Rick found both:

         the panel now runs to 1812, which is 232px BELOW the safe line -- so
         the ULTIMATE row, the one thing the panel exists to show, sits under
         the caption. "it also looks like the bottom of the video is still
         cut off."

         and `_panelFacts` pins ON HIT to the panel's top and ULTIMATE to its
         BOTTOM, so the space between them is `h` minus two fixed blocks. A
         shorter hall made `y` smaller, `h` bigger, and the gap grew by 244px.
         "something has gone really wrong with the scrunch. it has a huge gap
         in the middle."

       One clamp fixes both, and `Math.min` keeps the identity exact: at
       FRAME.foot 0 the safe line is 1908 and 1812 still wins, so nothing
       moves. frame_probe asserts that on a SCRUNCHED frame now -- the first
       version only ever rendered an ordinary one, which is why this shipped. */
    const h = Math.min(S.bottom, this.H - FRAME.foot - 12) - y,
          x = 24, w = this.W - 48;'''),

    ("the fit itself",
     '''    this.aw = this.W - this.pad * 2;
    this.scale = this.aw / CONFIG.arena.w;
    this.ah = CONFIG.arena.h * this.scale;
    /* The arena is width-bound — its height follows from the 520x740 sim and
       the frame width — so the height the HUD gave back cannot become more
       arena. Centre the slack instead of letting it all pool at the bottom as
       a dead black band under the footer. */
    this.arenaTop = BAND.pos === "bottom" ? 20 : this.hud + 24;      // the hall now nearly fills what is left''',
     '''    /* THE ARENA FITS A BOX NOW, NOT A WIDTH.

       It was width-bound, and the comment that used to sit here said so:
       "the arena is width-bound -- its height follows from the sim and the
       frame width -- so the height the HUD gave back cannot become more
       arena." True, and it also meant the hall ran to 1801 of 1920 and the
       bottom 200px of it lived under a TikTok caption. `cinema_clip --shorts`
       was compensating by shrinking the WHOLE VIDEO to 79% and boxing it,
       which spends every pixel in the frame to protect the bottom sixth.

       `scale` is the smaller of the two bounds, which is what a fitted layout
       should always have been -- the old code was correct only for viewports
       at or below the arena's own 0.65 aspect, and 9:16 is 0.5625.

       Presentation only. `CONFIG.arena` is untouched, nothing here is read by
       the simulation, and `engine_ab` is the proof rather than this sentence. */
    this.arenaTop = BAND.pos === "bottom" ? 20 : this.hud + 24;
    const availW = this.W - 12 * 2;
    const availH = this.H - this.arenaTop - FRAME.foot - 12;
    this.scale = Math.min(availW / CONFIG.arena.w, availH / CONFIG.arena.h);
    this.aw = CONFIG.arena.w * this.scale;
    this.ah = CONFIG.arena.h * this.scale;
    /* Recentred, which is not new code -- the scrunch block already ends with
       `this.pad = (this.W - this.aw) / 2` for exactly this reason. */
    this.pad = (this.W - this.aw) / 2;'''),
]


def one(src: str, old: str, new: str, label: str) -> str:
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-foregone.html")
    ap.add_argument("--out", default="../02-chain/sc-safeframe.html")
    ap.add_argument("--foot", type=int, default=0,
                    help="design-space px reserved at the bottom. 0 is an "
                         "exact identity with the old layout.")
    A = ap.parse_args()

    src_p = (HERE / A.src).resolve()
    out_p = (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")

    s0 = src_p.read_text(encoding="utf-8")
    s = s0
    print(f"\nFRAME BUILD -- the arena fits a box, not a width")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")
    if "const FRAME" in s0:
        raise SystemExit("this source already has FRAME -- already built")

    for label, old, new in EDITS:
        s = one(s, old, new.replace("%FOOT%", str(A.foot)), label)
    if "%FOOT%" in s:
        raise SystemExit("unsubstituted placeholder left in the build")

    out_p.write_text(s, encoding="utf-8", newline="\n")
    h = hashlib.sha256(s.encode()).hexdigest()[:16]
    print(f"  out {out_p.name}  {h}   ({len(s) - len(s0):+d} bytes)  foot={A.foot}")
    print(f"\n  NEXT, and none of it is optional:")
    print(f"    python3 frame_probe.py --game {A.out} --ref {A.src}")
    print(f"    python3 engine_ab.py --a {A.src} --b {A.out} --n 9")
    print(f"    python3 verify.py --game {A.out} --n 40\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
