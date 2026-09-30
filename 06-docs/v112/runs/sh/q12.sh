#!/bin/bash
# STAGE 6 PROBE (lane B, Idle): the stage-6 link at --stage 6 over 444 fights (--no-draw; the drawn subset is the
# seeds-1 run, stage6_probe_fx_drawn), the final at --stage 5 (the stage-6 checks off), the four stage-6 mutants
# (each must fail its own check only), then the fifteen stage 0-5 controls again on this probe.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs/stage6_probe; L=$S/links
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) q12 $1" >> $S/runs/q12.log; }
powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'Idle'" && log "Idle; probe $(sha256sum heartwood_probe.py | cut -c1-16)"
$PY heartwood_probe.py --game $L/sc-heartwood-b11-fx.html --stage 6 --no-draw --json $R/probe_fx.json > $R/probe_fx.txt 2>&1; log "probe fx (stage 6, no draw) rc=$?"
$PY heartwood_probe.py --game $L/sc-heartwood-b11.html --stage 5 --json $R/probe_b11.json > $R/probe_b11.txt 2>&1; log "probe b11 (stage 5) rc=$?"
for n in s6-close-voice s6-kill-voice s6-grove-sim s6-grove-rng; do
  $PY heartwood_probe.py --game $S/mut/mut-$n.html --stage 6 --no-draw --json $R/probe_mut-$n.json > $R/probe_mut-$n.txt 2>&1; log "probe mut-$n rc=$?"
done
for n in m1-window-labclock m2-every-other-blow m3-pin-before-knock m4-weapon-free m5-entangle-2 m6-root-hitstop m7-charge16 m8-row-no-entangle m9-root-stundr m10-ticker-stundr m11-blade-shipped x1-freeze-kept x2-root-0.8 x3-kill-roots x4-entangle-clock x5-cast-pins; do
  $PY heartwood_probe.py --game $S/mut/mut-$n.html --stage 5 --json $R/probe_mut-$n.json > $R/probe_mut-$n.txt 2>&1; log "probe mut-$n rc=$?"
done
log end
