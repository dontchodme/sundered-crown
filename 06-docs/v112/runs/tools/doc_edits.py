"""v112: the doc's resume-3 edits (2026-09-30) on doc_draft.md -> doc_final.md. Placeholders @@PROBE@@ @@MUT@@
@@VERIFY@@ @@HEAD@@ are filled later by doc_fill.py."""
import pathlib, sys
S = pathlib.Path(sys.argv[1])
d = (S / "doc_draft.md").read_text(encoding="utf-8")
def rep(old, new):
    global d
    assert d.count(old) == 1, old[:80]
    d = d.replace(old, new, 1)

# the header line is rewritten at the fill
first, rest = d.split("\n", 1)
d = "@@HEAD@@\n" + rest

rep("""design's, and the roster stays 38. Built on DESKTOP-DERRAFT, Chromium 151.0.7922.34, Python 3.13,
playwright 1.62.""",
"""design's, and the roster stays 38. Built on DESKTOP-DERRAFT, Chromium 151.0.7922.34, Python 3.13,
playwright 1.62. **The build was cut twice by usage limits**; each resume re-checked what was on disk before
going on (the base's sha, every link rebuilt byte-identical by the builder, every run file complete), and the
last pieces — stage 5 against its lab arm (§2), the probe and its mutants re-run on the patched probe (§3),
verify (§4a) and a fresh dry carry — were run on 2026-09-30.""")

rep("""    `fx.js` copy's `SPECS.heartwood` (32372; `src/render/fx.js` line 194). This build touches neither copy
    of `fx.js` (`tools/fx_remove.py` takes a retired spec out of both at the carry, the batch's procedure).""",
"""    `fx.js` copy's `SPECS.heartwood` (the base's line 32304; 32372 on the final), exactly this text, with no
    comment of its own (the "A FREEZE HOLDS" comment above it is Thornwake's entry's):

    ```
        heartwood: { mode: 'fall', n: 1050, sp: [30, 120], grav: 110, drag: 1.0,
                     life: [0.80, 1.70], heavy: 0.02, size: [0.6, 1.9],
                     spawn: 0.85, up: 0 },
    ```

    This build touches neither copy of `fx.js` (`tools/fx_remove.py` takes a retired spec out of both at
    the carry, the batch's procedure). `src/render/fx.js` on disk follows the batch line's tip, where the
    orchestrator has already taken other retired specs out (the entry is its line 191 today), so the base's
    inlined copy is the reference here.""")

rep("""     (no lab arm: the blade)                                                                        stage 5 (blade 11):  @@S5A@@""",
"""     (the blade: its own lab arm below)                                                             stage 5 (blade 11):  55.2 / 54.1           54.6""")

rep("""every designed number; Rick's batch ruling converted the charge only, and his blade ruling sets the blade
on the built relic (§4), so the clock's lift is priced out by the blade.
""",
"""every designed number; Rick's batch ruling converted the charge only, and his blade ruling sets the blade
on the built relic (§4), so the clock's lift is priced out by the blade.

**The final against its own lab arm** (`runs/lab_c15_b11_*`, `runs/built_b11_*`; the lab's arm C at the
final's numbers: `--P rootFor=1.0 charge=15 blade=11`, the same 33 foes, seeds and side):

```
                                                     block 1 / 2    pooled
lab C, blade 11, charge 15, dur 8 (the lab's window)  52.3 / 49.5    50.9     4.20 casts, 13.9 blows in windows, 3.25 rooted a cast, pinned 41.8%
lab C, blade 11, charge 15, dur 9.42 (the engine's)   55.2 / 54.5    54.8     4.24 casts, 16.3 blows in windows, 3.76 rooted a cast, pinned 42.3%
BUILT stage 5, sc-heartwood-b11 (the final)           55.2 / 54.1    54.6     (the probe: 4.31 casts, 16.2 blows in windows, 3.67 rooted a cast, pinned 43.7%)
```

The final reads +3.7 over its lab arm at the lab's window and 0.2 under it at the engine's: the window clock
again, at the blade the ruling chose, and nothing else. (Side A against the design's 33 foes reads 54.6 where
`relic_rate` both sides against all 37 reads 51.4 (§4): against the same 33, both sides, the final reads 55.2;
the four relics built since are among its worst — Ironwood 0, Bindweed 12.5, Morningstar 32.5, Portcullis
37.5 of 40.)
""")

rep("""grid, no bisection; `runs/stage5_rr_*`, table `runs/stage5_table.txt`):""",
"""grid, no bisection; `runs/stage5_rr_*`, table `runs/stage5_table.txt`; `stage5_rr_final_*` is stage 3's
link at 12.65, named when the blade held there, and `stage5_rr_b11_*` the final):""")

(S / "doc_final.md").write_text(d, encoding="utf-8", newline="\n")
print("ok", d.count("@@"))
