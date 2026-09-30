#!/bin/bash
# THE FIX ROUND (2026-09-30): the probe with [8] (the cast and the freeze out), the exact entangle record in [6],
# [3]/[5] reading the blows that rooted, [4] the living held balls. Every stage from 2, the eleven mutants and the
# review's five, and the 7-check probe (c27d9794) on the review's x1/x4/x5. Lane $1 of 2, Idle priority.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs; L=$S/links
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) lane$1 $2" >> $R/q8.log; }
powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'Idle'" && log $1 "Idle; probe $(sha256sum heartwood_probe.py | cut -c1-16)"
pm(){ $PY heartwood_probe.py --game $S/mut/mut-$1.html --stage 5 --json $R/probe_mut-$1.json > $R/probe_mut-$1.txt 2>&1; }
if [ "$1" = 1 ]; then
  $PY heartwood_probe.py --game $L/sc-heartwood-b11.html --stage 5 --json $R/probe_b11.json > $R/probe_b11.txt 2>&1; log 1 "probe b11 (stage 5) rc=$?"
  $PY heartwood_probe.py --game $L/sc-heartwood-rootfast.html --stage 3 --json $R/probe_rootfast.json > $R/probe_rootfast.txt 2>&1; log 1 "probe rootfast (stage 3) rc=$?"
  $PY heartwood_probe.py --game $L/sc-heartwood-root.html --stage 2 --json $R/probe_root.json > $R/probe_root.txt 2>&1; log 1 "probe root (stage 2) rc=$?"
  for n in x1-freeze-kept x4-entangle-clock x5-cast-pins x2-root-0.8 x3-kill-roots m1-window-labclock; do pm $n; log 1 "probe mut-$n rc=$?"; done
  for n in x1-freeze-kept x4-entangle-clock x5-cast-pins; do
    $PY $S/tools/heartwood_probe_v2_c27d9794.py --game $S/mut/mut-$n.html --stage 5 --json $R/probe7_mut-$n.json > $R/probe7_mut-$n.txt 2>&1; log 1 "7-check probe mut-$n rc=$?"
  done
else
  for n in m2-every-other-blow m3-pin-before-knock m4-weapon-free m5-entangle-2 m6-root-hitstop m7-charge16 m8-row-no-entangle m9-root-stundr m10-ticker-stundr m11-blade-shipped; do pm $n; log 2 "probe mut-$n rc=$?"; done
fi
log $1 end
