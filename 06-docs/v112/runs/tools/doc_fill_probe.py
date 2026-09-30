"""v112: fill @@PROBE@@ and @@MUT@@ in doc_final.md from runs/probe_*.txt and runs/probe_mutants.txt (2026-09-30)."""
import pathlib, sys
S = pathlib.Path(sys.argv[1]); R = S / "runs"
d = (S / "doc_final.md").read_text(encoding="utf-8")
PROBE = """- **sc-heartwood-b11 (stage 5, the final): 7/7** (`runs/probe_b11.txt`; 444 fights): 4.31 casts a fight;
  16.16 blows in windows (15.97 on the opponent, the rest on Twinshade's shades) and 11.08 outside; **3.67
  blows rooted a cast and 2.07 roots a cast as transitions** (a blow that finds the ball unpinned); the foe
  pinned **43.7%** of window frames (the lab's read, after the step); entangle applied by rooted blows
  **2.97 x** the blows rooted (the channel's 2 + 1; a blow on a shade puts the channel on the shade and the
  +1 on Twinshade); 142 killing blows rooted nobody; 88 shade blows rooted Twinshade; 3,075 re-roots on a
  held ball (48 under a longer hold, where pinV was rightly kept); 731,314 held steps still in `move()` and
  729,484 held hit loops with the weapon locked and no blow; **15.2% of window steps frozen**; a clock
  window is exactly 960 calls; 7,177 root calls and 108,272 ticker calls snapshotted whole and clean.
  Heartwood 50.5% in the probe's own fights.
- **sc-heartwood-rootfast (stage 3): 7/7** (`runs/probe_rootfast.txt`): 4.10 casts; 15.12 blows in windows
  and 10.48 outside; 3.59 rooted and 2.06 transitions a cast; pinned 42.9%; entangle 2.98 x; 180 killing
  blows unrooted; 61 shade roots; 15.1% frozen; 63.7%.
- **sc-heartwood-root (stage 2): 7/7** (`runs/probe_root.txt`): 4.10 casts; 14.81 blows in windows and
  10.41 outside; 3.52 rooted and 1.99 transitions a cast; pinned 42.2%; entangle 1.98 x (the channel's own
  only: [5] asserts no extra entangle at `extraEnt` 0); 15.1% frozen; 59.9%.

**The probe's own flaw, found by its controls and fixed.** In the first pass (`runs/probe_first/`) the mutant
that roots every other blow (`m2`) failed [2] — and also [3] and [5], on the same unrooted blows (the pin not
written, the +1 not applied): three checks for one broken sentence. [3] and [5] now read only the blows that
rooted; whether a blow in the window rooted at all is [2]'s sentence, and a blow that roots nobody must still
leave the pin alone ([3]). The coverage conditions (a check that never ran is not a pass) are unchanged. On a
correct link the change reads the same blows, so the stages' numbers did not move; every probe and every
mutant was re-run on the patched probe (sha256[:16] c27d97940d22dbd7) on 2026-09-30, and each mutant now fails
its own check(s) and only those."""
mut = (R / "probe_mutants.txt").read_text(encoding="utf-8").rstrip("\n")
LIST = """The mutants (`runs/mutants_shas.txt`):
- `m1` the window on the lab's clock (`tickRootfast` also ticks on every frozen step) -> [1];
- `m2` only every other blow in the window roots -> [2];
- `m3` the root written BEFORE the knock, so pinV is the pre-knock vector -> [3];
- `m4` the root frees the weapon (`pinFree = 1`) -> [4];
- `m5` entangle +2 on a root instead of +1 -> [5];
- `m6` the root stops the world (Paradox's pin's 0.06 hit stop) -> [6];
- `m7` the lab's charge 16 unconverted -> [7];
- `m8` the row lost its entangle (`extraEnt` 0) -> [5] and [7];
- `m9` the root also resets the foe's stun diminishing returns -> [6];
- `m10` the window's ticker resets the caster's stun diminishing returns -> [6];
- `m11` the blade back at the shipped 12.65 (byte-identical to stage 3's link) -> [7].

"""
assert d.count("@@PROBE@@") == 1 and d.count("@@MUT@@") == 1
d = d.replace("@@PROBE@@", PROBE, 1).replace("@@MUT@@", mut, 1)
old = "m1-m7 are one sentence each."
assert d.count(old) == 1
d = d.replace(old, LIST + old, 1)
(S / "doc_final.md").write_text(d, encoding="utf-8", newline="\n")
print("ok", d.count("@@"))
