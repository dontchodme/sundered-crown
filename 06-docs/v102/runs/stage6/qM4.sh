#!/bin/bash
# mP2 (drawn) now on the free browser, to its own file; when qM2's mP3 is done, stop qM2 before its own mP2.
L=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone
P=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
( until grep -q "^EXIT" $L/s6/probe_mut_mP3-ungated.txt 2>/dev/null; do sleep 2; done
  powershell -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w $L/s6/stop_qM2.ps1)" > $L/s6/qM4_stopped.txt 2>&1 ) &
cd C:/dev/sundered-crown/tools
$P -u lodestone_probe.py --game $L/s6/mut/sc-lodestone-mP2-draw-writes.html --seeds 1 > $L/s6/probe_mut_mP2.q4.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_mut_mP2.q4.txt
wait
mv -f $L/s6/probe_mut_mP2.q4.txt $L/s6/probe_mut_mP2-draw-writes.txt
echo QM4 DONE
