#!/bin/bash
# third-review fix: probe reruns in two lanes (at most two browsers from this build)
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail
RV=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/review-ironhail
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/queue6.log; }
pr(){ $PY ironhail_probe.py --game "$1" $3 > "$2" 2>&1; echo "exit $?" >> "$2"; log "probe $(basename $2) done"; }
if [ "$1" = A ]; then
  for t in hail b14; do pr $S/links/sc-ironhail-$t.html $S/runs/probe_$t.txt "--json $S/runs/probe_$t.json"; done
  for m in c-caster c-chip c-selfsunder; do pr $S/tmp/mut4-$m.html $S/runs/probe_mut4-$m.txt; done
  pr $RV/tmp/mut-r3-halfbow.html $S/runs/probe_review-r3-halfbow.txt
  for m in m1-frozen m2-cadence m3-fall; do pr $S/tmp/mut2-$m.html $S/runs/probe_mut2-$m.txt; done
  log "LANE A DONE"
else
  for m in r-double r-half r-beatside r-beatspot; do pr $S/tmp/mut3-$m.html $S/runs/probe_mut3-$m.txt; done
  for m in m4-sundermul m5-missund m6-stop m7-nobeat m8-bowquiet m8b-halfbow m9-novakept; do pr $S/tmp/mut2-$m.html $S/runs/probe_mut2-$m.txt; done
  log "LANE B DONE"
fi
