#!/bin/bash
# The PC is at ~96% CPU from the batch's other builds, and a drawn probe run takes 30+ min. After the clean
# one-seed run finishes, stop qM.sh (before its drawn mV1) and run mV1, mV2, mP1 WITHOUT the drawn subset
# (--no-draw): they aim at [10] and at tickLode, which the headless run reads whole. mP2 (a drawn frame
# writing the sim) and mP3 keep the drawn subset (qM2.sh).
L=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone
P=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
until grep -q "^EXIT" $L/s6/probe_fx_s1.txt 2>/dev/null; do sleep 3; done
sleep 2
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'qM\.sh' -or \$_.CommandLine -match 'sc-lodestone-mV1-close-on-death' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue; \$_.ProcessId }" > $L/s6/qM3_killed.txt 2>&1
rm -f $L/s6/probe_mut_mV1-close-on-death.txt
cd C:/dev/sundered-crown/tools
for m in mV1-close-on-death mV2-touch-before-hex mP1-lode-writes; do
  $P -u lodestone_probe.py --game $L/s6/mut/sc-lodestone-$m.html --seeds 1 --no-draw > $L/s6/probe_mut_$m.txt 2>&1; echo "EXIT $?" >> $L/s6/probe_mut_$m.txt
done
echo QM3 DONE
