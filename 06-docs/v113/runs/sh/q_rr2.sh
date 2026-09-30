#!/bin/bash
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
F=$S/links/sc-thornwake-snare.html
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_rr1.log; }
while ! grep -q "d30 2317" $S/runs/q_rr1.log 2>/dev/null; do sleep 10; done
for d in 27 26 25 24; do for b in 2207 2317; do bash $S/runs/rr.sh $F d$d $b dmg=$d; log "d$d $b"; done; done
