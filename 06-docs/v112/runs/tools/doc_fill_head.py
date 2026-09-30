"""v112: fill @@HEAD@@ and @@VERIFY@@ in doc_final.md (2026-09-30), then check no placeholder is left."""
import pathlib, sys
S = pathlib.Path(sys.argv[1])
d = (S / "doc_final.md").read_text(encoding="utf-8")
HEAD = ("# v112 — HEARTWOOD / ROOTFAST (REDESIGN), BUILD. STAGES 0-5 DONE, IN SCRATCH: stage 1 is arm A fight for "
        "fight on both blocks; the root on every blow is the lab's mechanism (probe 7/7 on every stage from 2 on, read "
        "inside the hooks, every number pinned by the stage, \"nothing else\" snapshotted whole; eleven mutants of the "
        "final, each failing its own check and only that); the built relic reads 3-5 over its lab arms by the window "
        "clock, attributed with controls both ways; **THE BLADE IS 11, THE MEASURED POINT NEAREST 50% BOTH SIDES, BY "
        "RICK'S RULING (\"you pick the blades. do whatevers best for balance.\", 2026-09-29): 51.4% both sides, against "
        "the shipped freeze's 32.4% on the same seeds.** The design's own target (its §6.2, written before the ruling) is "
        "measured beside it: the blade left at 12.65 reads 58.6, its \"11.5–12 for 50\" reads 55.7 / 57.4. **The charge is "
        "13** — the design's \"Charge 15\" converted to the game's clock (14 and 15 priced beside it; flagged). Gates on "
        "the final: engine_ab 3996/3996 on the other 37; verify 11/13 (Heartwood 51.8%, was 30.5%; the reds are the two "
        "clock bands only); chain_audit 9/9; tip_audit as the base. Stage 6 (picture, voice, carry) is next, on "
        "`sc-heartwood-b11`.")
VERIFY = ("**11/13** (`runs/verify_final.txt`; 28,120 matches, 40 seeds x 703 pairings, 2869s). **Heartwood 51.8%** "
          "(on the base it was 30.5%, the floor: v101 `runs/verify_t3.txt`). Every relic in 30-70%: Axiom 34.5 .. "
          "Gloamwire 63.3 (spread 28.9pp; the base's 33.2). **\"Both sides can win every matchup\" now PASSES** — on "
          "the base it failed on Heartwood v Twinshade 0/40 and Heartwood v Bindweed 0/40, both the shipped Heartwood's "
          "pairings. **The two reds are the clock bands**, as on every link since the minute pace, and not this "
          "relic's: pairing means 38.6s (Gravemourn/Ironhail) .. 100.0s (Farwarden/Starwarden), and the overall mean "
          "61.0s (the base's 60.8s). Heartwood sits at index 16 of 38, so verify plays it side A against the 22 relics "
          "after it and side B against the 15 before (an appended relic is side B everywhere; a redesign keeps its "
          "row).")
for k, v in (("@@HEAD@@", HEAD), ("@@VERIFY@@", VERIFY)):
    assert d.count(k) == 1, k
    d = d.replace(k, v, 1)
assert "@@" not in d
(S / "doc_final.md").write_text(d, encoding="utf-8", newline="\n")
print("ok")
