"""v114 scratch control (§2): the built stage-2 link with its window on MATCH time.

The engine's window runs 8s of the window tickers' clock (it stops in a hit
stop). The lab's ran 8 step-seconds, frozen steps included. This variant keeps
everything of `sc-goreshard-price.html` but the window's clock: the cast
records the match clock (`this.t`, which advances on frozen steps too) and
`tickPrice` closes the window 8s of match time later -- the lab's window on
the engine. Two lines (v106's make_matchclock_variant.py, for this relic). A
scratch file, never a link.

    python make_matchclock_variant.py <sc-goreshard-price.html> <out.html>
"""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
edits = [("      f.ultPrice = { t: 0, dur: u.dur };",
          "      f.ultPrice = { t: 0, dur: u.dur, t0: this.t };   // SCRATCH VARIANT: the window on match time"),
         ("      Z.t += dt;\n      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultPrice = null; continue; }",
          "      Z.t = this.t - Z.t0;   // SCRATCH VARIANT: match time, frozen steps included (the lab's window)\n"
          "      if (Z.t >= Z.dur - 1e-9 || !f.alive || !foe.alive){ f.ultPrice = null; continue; }")]
for a, b in edits:
    assert src.count(a) == 1, a
    src = src.replace(a, b, 1)
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8", newline="\n")
print("written", sys.argv[2])
