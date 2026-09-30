#!/bin/bash
# THE LAB AT THE ENGINE'S LENGTHS (control 1b): every one of the lab's three clocks stretched to what the engine's
# unfrozen seconds come to in match time -- window 8 / (1 - 0.128) = 9.17, bramble life 6 / (1 - 0.11) = 6.74,
# the thorns' cooldown 0.5 / (1 - 0.11) = 0.56 -- arms B and C, both blocks
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
while ! grep -q "d24 2317" $S/runs/q_rr1.log 2>/dev/null; do sleep 5; done
for b in 2207 2317; do
$PY $S/tools/tw_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic thornwake --mech C:/dev/sundered-crown/tools/overlays/bramble.js --arms B,C --P dur=9.17 patchLife=6.74 tickCd=0.56 --seeds 20 --seed0 $b --foes $(cat $S/runs/foes33.txt) --label "lab at the engine's lengths, block $b" --out $S/runs/lab_len_$b.json > $S/runs/lab_len_$b.txt 2>&1
echo "$(date +%H:%M:%S) lab len $b rc=$?" >> $S/runs/q_lablen.log
done
