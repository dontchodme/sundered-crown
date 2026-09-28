#!/bin/bash
# stage 6: the rest of the mutant probes split over the two browsers (17:15). The first loop
# (probes6_mut.sh) was stopped while mS1 ran; its probe ran on to the end in the same file.
# usage: probes6_mut_split.sh A   (waits for mS1's probe, then mS3, mS2)
#        probes6_mut_split.sh B   (waits for slot1_s6.sh, then mS4)
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
cd C:/dev/sundered-crown/tools
run(){ echo "coldiron_probe.py --game s6/mut/mut-$1.html   probe $(sha256sum coldiron_probe.py | cut -c1-16)   $(date '+%F %T')" > "$S/s6/probe_mut_$1.txt"
       $PY -u coldiron_probe.py --game "$S/s6/mut/mut-$1.html" >> "$S/s6/probe_mut_$1.txt" 2>&1; echo "exit $?" >> "$S/s6/probe_mut_$1.txt"; }
if [ "$1" = A ]; then
  while kill -0 81257 2>/dev/null; do sleep 5; done
  echo "exit (not captured: the loop that started this probe was stopped at 17:15 to split the rest over two browsers; the probe ran to its end, its summary above)" >> "$S/s6/probe_mut_mS1-close-on-death.txt"
  run mS3-iron-writes; run mS2-anvil-count-before
  echo done > "$S/s6/probes6_split_A.done"
else
  while [ ! -f "$S/s6/slot1_s6.done" ]; do sleep 5; done
  run mS4-draw-writes
  echo done > "$S/s6/probes6_split_B.done"
fi
