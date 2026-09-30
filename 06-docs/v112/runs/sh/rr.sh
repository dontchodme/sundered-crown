#!/bin/bash
# STAGE 5: relic_rate.py, BOTH SIDES, every other relic a foe, 10 seeds a foe a side: $1 tag, $2 game (abs), $3 block, $4.. --set knobs
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
T=$1; G=$2; B=$3; shift 3
if [ $# -gt 0 ]; then SET="--set $*"; else SET=""; fi
cd C:/dev/sundered-crown/tools && $PY relic_rate.py --game $G --relic heartwood --n 10 --seed0 $B $SET --label "$T" --json C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/stage5_rr_${T}_$B.json > C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood/runs/stage5_rr_${T}_$B.txt 2>&1
