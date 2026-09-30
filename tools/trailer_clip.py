#!/usr/bin/env python3
"""cinema_clip.py with the game's music bed muted -- the trailer carries its own score
(trailer_music.py), and fourteen tape-slowed beds cut together would clash on every cut.

Everything else is cinema_clip.py unmodified: the director, the SFX through the game's own
synth, the picture. The mute is done in the page (S2.bed throws, and renderAudio's own
try/catch already falls back to "no bed"), so no file in 02-chain/ is touched.

    python trailer_clip.py --game ../02-chain/sc-nightglass-fx.html --a widowmaker --b duskreave \
        --seed 7739596 --at 15.8 --window 3.0 --end-at-window --w 1080 --png --no-card --out clip.mp4
"""
import contextlib, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import scpage, cinema_clip

_orig = scpage.game


@contextlib.contextmanager
def _nobed(*a, **k):
    with _orig(*a, **k) as (page, errs):
        page.evaluate("() => { const P = Object.getPrototypeOf(AC.SFX);"
                      " P.bed = function(){ throw new Error('trailer: bed muted'); }; }")
        yield page, errs


cinema_clip.game = _nobed

if __name__ == "__main__":
    sys.exit(cinema_clip.main())
