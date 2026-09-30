#!/bin/bash
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_ctl.log; }
# wait for the probe lane to finish (one browser per lane)
while ! grep -q "probe snare" $S/runs/q_probe23.log 2>/dev/null; do sleep 10; done
for t in bramble snare; do for b in 2207 2317; do bash $S/runs/built.sh $S/links/ctl-labclock-$t.html ctl-labclock-$t $b; log "ctl-labclock-$t $b"; done; done
for b in 2207 2317; do bash $S/runs/labdur.sh $b 9.17 917; log "lab dur 9.17 $b"; done
bash $S/runs/pub151.sh; log "pub151"
