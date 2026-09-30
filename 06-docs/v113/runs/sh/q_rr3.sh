#!/bin/bash
# THE HALF-STEP GRID over 24-28 (a fixed grid, read after, no bisection): 26.5, 25.5, 27.5, 24.5
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
F=$S/links/sc-thornwake-snare.html
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_rr3.log; }
while ! grep -q "pub151" $S/runs/q_ctl.log 2>/dev/null; do sleep 5; done
for d in 26.5 25.5 27.5 24.5; do for b in 2207 2317; do bash $S/runs/rr.sh $F d$d $b dmg=$d; log "d$d $b"; done; done
log end
