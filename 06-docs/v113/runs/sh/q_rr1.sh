#!/bin/bash
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
F=$S/links/sc-thornwake-snare.html; BASE=C:/dev/sundered-crown/02-chain/sc-tendril-t3.html
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_rr1.log; }
for b in 2207 2317; do bash $S/runs/rr.sh $BASE shipped $b; log "shipped $b"; done
for b in 2207 2317; do bash $S/runs/rr.sh $F final3135 $b; log "final3135 $b"; done
for d in 28 29 30; do for b in 2207 2317; do bash $S/runs/rr.sh $F d$d $b dmg=$d; log "d$d $b"; done; done
