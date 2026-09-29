#!/bin/bash
# Review round 2, stage 5 at blade 20.5 -- ONE browser at a time (verify holds the other):
#  reproduce (relic_rate on b205, no --set) ; built vs lab at 20.5 with the two clock controls ; the 'after' control
#  (the lab's order, the engine's clock) at 23.5 and 20.5 ; tip_audit ; engine_ab on the 38 base ids.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
F="$S/links/sc-lodestone-b205.html"
cd C:/dev/sundered-crown/tools
FOES="$(cat "$S/runs/foes33.txt")"
for b in 2207 2317; do
  $PY relic_rate.py --game "$F" --relic lodestone --n 10 --seed0 $b --label "built b205, no set" --json "$S/runs/stage5_rr_built_b205_$b.json" > "$S/runs/stage5_rr_built_b205_$b.txt" 2>&1; echo "rr $b rc=$?"
done
for b in 2207 2317; do
  $PY ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic grudgebearer --cell runic:warhammer --mech overlays/rebound.js --arms C --P blade=20.5 --seeds 20 --seed0 $b --foes "$FOES" --label "lab C at blade 20.5" --out "$S/runs/lab_C205_$b.json" > "$S/runs/lab_C205_$b.txt" 2>&1; echo "labC205 $b rc=$?"
  $PY ult_overlay.py --game "$F" --relic lodestone --mech overlays/rebound.js --arms SHIP --seeds 20 --seed0 $b --foes "$FOES" --label "built b205" --out "$S/runs/built_b205_$b.json" > "$S/runs/built_b205_$b.txt" 2>&1; echo "built205 $b rc=$?"
  $PY ult_overlay.py --game ../02-chain/sc-tendril-t3.html --relic grudgebearer --cell runic:warhammer --mech overlays/rebound.js --arms C --P blade=20.5 dur=9.2 --seeds 20 --seed0 $b --foes "$FOES" --label "lab C at blade 20.5, the engine's window" --out "$S/runs/lab92_C205_$b.json" > "$S/runs/lab92_C205_$b.txt" 2>&1; echo "lab92C205 $b rc=$?"
  $PY ult_overlay.py --game "$S/ctl/ctl-labclock-b205.html" --relic lodestone --mech overlays/rebound.js --arms SHIP --seeds 20 --seed0 $b --foes "$FOES" --label "ctl lab clock b205" --out "$S/runs/ctl_labclock_b205_$b.json" > "$S/runs/ctl_labclock_b205_$b.txt" 2>&1; echo "labclock205 $b rc=$?"
  $PY ult_overlay.py --game "$S/ctl/ctl-after-rebuttal.html" --relic lodestone --mech overlays/rebound.js --arms SHIP --seeds 20 --seed0 $b --foes "$FOES" --label "ctl after (the lab's order) rebuttal 23.5" --out "$S/runs/ctl_after_rebuttal_$b.json" > "$S/runs/ctl_after_rebuttal_$b.txt" 2>&1; echo "after235 $b rc=$?"
  $PY ult_overlay.py --game "$S/ctl/ctl-after-b205.html" --relic lodestone --mech overlays/rebound.js --arms SHIP --seeds 20 --seed0 $b --foes "$FOES" --label "ctl after (the lab's order) b205" --out "$S/runs/ctl_after_b205_$b.json" > "$S/runs/ctl_after_b205_$b.txt" 2>&1; echo "after205 $b rc=$?"
done
$PY tip_audit.py --game "$F" > "$S/runs/tip_audit_b205.txt" 2>&1; echo "tip_audit rc=$?"
$PY engine_ab.py --a ../02-chain/sc-tendril-t3.html --b "$F" --ids "$(cat "$S/runs/ids38.txt")" --n 6 > "$S/runs/engine_ab38_b205.txt" 2>&1; echo "engine_ab rc=$?"
echo STAGE5-B205-DONE
