#!/bin/bash
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
for t in stub bramble snare; do bash $S/runs/built.sh $S/links/sc-thornwake-$t.html $t $1; echo "$(date +%H:%M:%S) built $t $1 done" >> $S/runs/lane_built_$1.log; done
