#!/bin/bash
# Review round 3, on the rebuilt links (only the row comment changed) -- ONE browser (the probes hold the other):
#  reproduce (relic_rate on b205, no --set, vs the d20.5 sweep); stage 1 = arm A FIGHT FOR FIGHT (f4f_overlay.py, both
#  blocks); the built SHIP runs of stages 2, 3 and 5 re-run against round 2's; tip_audit; engine_ab on the 38 base ids.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
F="$S/links/sc-lodestone-b205.html"; R="$S/runs"; mkdir -p "$R/r3"
cd C:/dev/sundered-crown/tools
FOES="$(cat "$R/foes33.txt")"
for b in 2207 2317; do
  $PY relic_rate.py --game "$F" --relic lodestone --n 10 --seed0 $b --label "built b205 (round 3), no set" --json "$R/stage5_rr_built_b205_$b.json" > "$R/stage5_rr_built_b205_$b.txt" 2>&1; echo "rr $b rc=$? $(date +%T)"
done
$PY "$R/reproduce.py" "$R" "$F" "$S/links/sc-lodestone-rebuttal.html" 20.5 > "$R/stage5_reproduce_b205.txt" 2>&1; echo "reproduce rc=$?"
for b in 2207 2317; do
  $PY "$R/f4f_overlay.py" --game ../02-chain/sc-tendril-t3.html --relic grudgebearer --cell runic:warhammer --mech overlays/rebound.js --arms A --seeds 20 --seed0 $b --foes "$FOES" --label "lab A, per fight" --out "$R/f4f_labA_$b.json" > "$R/f4f_labA_$b.txt" 2>&1; echo "f4f labA $b rc=$? $(date +%T)"
  $PY "$R/f4f_overlay.py" --game "$S/links/sc-lodestone.html" --relic lodestone --mech overlays/rebound.js --arms SHIP --seeds 20 --seed0 $b --foes "$FOES" --label "stage 1, per fight" --out "$R/f4f_s1_$b.json" > "$R/f4f_s1_$b.txt" 2>&1; echo "f4f s1 $b rc=$? $(date +%T)"
done
{ for b in 2207 2317; do echo "block $b:"; $PY "$R/cmp_f4f.py" "$R/f4f_labA_$b.json" "$R/f4f_s1_$b.json"; done; } > "$R/stage1_vs_A_f4f.txt" 2>&1; echo "cmp_f4f done"
for pair in "sc-lodestone-runes:runes" "sc-lodestone-rebuttal:rebuttal" "sc-lodestone-b205:b205"; do
  L="${pair%%:*}"; N="${pair##*:}"
  for b in 2207 2317; do
    $PY ult_overlay.py --game "$S/links/$L.html" --relic lodestone --mech overlays/rebound.js --arms SHIP --seeds 20 --seed0 $b --foes "$FOES" --label "built $N (round 3)" --out "$R/r3/built_${N}_$b.json" > "$R/r3/built_${N}_$b.txt" 2>&1; echo "built $N $b rc=$? $(date +%T)"
  done
done
{ for N in runes rebuttal b205; do for b in 2207 2317; do $PY "$R/cmp_rerun.py" "$R/built_${N}_$b.json" "$R/r3/built_${N}_$b.json"; done; done; } > "$R/built_rerun_r3.txt" 2>&1; echo "cmp_rerun done"
$PY tip_audit.py --game "$F" > "$R/tip_audit_b205.txt" 2>&1; echo "tip_audit rc=$?"
$PY engine_ab.py --a ../02-chain/sc-tendril-t3.html --b "$F" --ids "$(cat "$R/ids38.txt")" --n 6 > "$R/engine_ab38_b205.txt" 2>&1; echo "engine_ab rc=$? $(date +%T)"
echo STAGE5R3-DONE
