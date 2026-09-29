"""v106 scratch: relic_rate on the built stage-5 link (no --set) against the --set dmg=10.75 run on the
stage-2 link, and against the pre-round-2 bytes of the same link: every key but game/set/label."""
import json, pathlib
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
skip = {"game", "set", "label"}
for b in (2207, 2317):
    new = json.load(open(W / "runs" / f"stage5_rr_built_b1075_{b}.json"))
    ref = json.load(open(W / "runs" / f"stage5_rr_d10.75_{b}.json"))
    old = json.load(open(W / "old_runs_r2" / f"stage5_rr_built_b1075_{b}.json"))
    keys = sorted(set(new) | set(ref))
    diff = [k for k in keys if k not in skip and new.get(k) != ref.get(k)]
    diffo = [k for k in keys if k not in skip and new.get(k) != old.get(k)]
    print(f"block {b}: rate {new['rate']*100:.1f} (A {new['rateA']*100:.1f}, B {new['rateB']*100:.1f}), mean {new['dur']:.2f}s; "
          f"differs from --set dmg=10.75 in {diff or 'nothing'}; from the pre-round-2 bytes in {diffo or 'nothing'}; keys compared {len([k for k in keys if k not in skip])}")
