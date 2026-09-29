"""v106 scratch control (§2): the built stage-2 link with its window on MATCH time.

The engine's window runs 8s of the window tickers' clock (it stops in a hit
stop). The lab's ran 8 step-seconds, frozen steps included. This variant keeps
everything of `sc-widowmaker-drain.html` but the window's clock: the cast
records the match clock (`this.t`, which advances on frozen steps too) and
`tickDrain` closes the window 8s of match time later -- the lab's window on
the engine. Two lines. A scratch file, never a link.

    python make_matchclock_variant.py <sc-widowmaker-drain.html> <out.html>

Measured (runs/ctl_built_matchclock_*, ctl_probe_matchclock.txt): SHIP 53.2 /
56.7 (pooled 55.0) against the lab's live-steps arm 54.8 / 55.0 (54.9); 20.3 hp
a cast (lab 20.3); the probe fails [1] (the window clock) and nothing else.
"""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
edits = [("      f.ultDrain = { t: 0, dur: u.dur };",
          "      f.ultDrain = { t: 0, dur: u.dur, t0: this.t };   // SCRATCH VARIANT: the window on match time"),
         ("      Z.t += dt;\n      if (Z.t >= Z.dur || !f.alive || !foe.alive){ f.ultDrain = null; continue; }",
          "      Z.t = this.t - Z.t0;   // SCRATCH VARIANT: match time, frozen steps included (the lab's window)\n"
          "      if (Z.t >= Z.dur - 1e-9 || !f.alive || !foe.alive){ f.ultDrain = null; continue; }")]
for a, b in edits:
    assert src.count(a) == 1, a
    src = src.replace(a, b, 1)
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8", newline="\n")
print("written", sys.argv[2])
