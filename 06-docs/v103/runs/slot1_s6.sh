#!/bin/bash
# stage 6, slot 1 (one browser at a time): the clip's timeline, render_ab (others + control), the probe on fx
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
B93="$S/links/sc-coldiron-temper-b93.html"; FX="$S/links/sc-coldiron-temper-fx.html"
cd C:/dev/sundered-crown/tools
$PY "$S/s6/clip_timeline.py" > "$S/s6/clip_timeline.txt" 2>&1; echo "exit $?" >> "$S/s6/clip_timeline.txt"
{ echo "render_ab.py --a <b93> --b <fx> --pairs paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337  (frames: the default 0.5,6,12,22,31,40)   $(date '+%F %T')"
  $PY -u render_ab.py --a "$B93" --b "$FX" --pairs paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337; echo "exit $?"; } > "$S/s6/render_ab_others.txt" 2>&1
{ echo "render_ab.py --a <b93> --b <fx> --pairs coldiron:vinesower:103349 --frames 33,35,37,39,41  (inside the clip's window, cast 32.05, clock close 41.92)   $(date '+%F %T')"
  $PY -u render_ab.py --a "$B93" --b "$FX" --pairs coldiron:vinesower:103349 --frames 33,35,37,39,41; echo "exit $?"; } > "$S/s6/render_ab_control.txt" 2>&1
{ echo "coldiron_probe.py --game <fx> --json s6/probe_fx_final.json   probe $(sha256sum coldiron_probe.py | cut -c1-16)   $(date '+%F %T')"
  $PY -u coldiron_probe.py --game "$FX" --json "$S/s6/probe_fx_final.json"; echo "exit $?"; } > "$S/s6/probe_fx_final.txt" 2>&1
echo done > "$S/s6/slot1_s6.done"
