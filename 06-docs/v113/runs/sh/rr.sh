#!/bin/bash
# relic_rate BOTH SIDES: $1 link, $2 tag, $3 block, $4.. --set args (optional)
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
L=$1; T=$2; B=$3; shift 3
if [ $# -gt 0 ]; then SET="--set $*"; else SET=""; fi
$PY relic_rate.py --game $L --relic thornwake --n 10 --seed0 $B $SET --label "$T" --json $S/runs/stage5_rr_${T}_$B.json > $S/runs/stage5_rr_${T}_$B.txt 2>&1
echo "rc=$?" >> $S/runs/stage5_rr_${T}_$B.txt
