#!/bin/bash
# STAGE 6: render_ab b11 -> b11-fx on four pairs of other relics (24 frames), then the control (Heartwood in a window)
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs; L=$S/links
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) q11 $1" >> $R/q11.log; }
powershell -NoProfile -Command "(Get-Process -Id $(cat /proc/$$/winpid)).PriorityClass = 'BelowNormal'"
$PY render_ab.py --a $L/sc-heartwood-b11.html --b $L/sc-heartwood-b11-fx.html --pairs ironhail:dawnbringer:4412,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337 > $R/stage6_render_ab.txt 2>&1; log "render_ab others rc=$?"
$PY render_ab.py --a $L/sc-heartwood-b11.html --b $L/sc-heartwood-b11-fx.html --pairs heartwood:spellbreaker:2207,paradox:heartwood:25064 > $R/stage6_render_ab_control.txt 2>&1; log "render_ab control rc=$?"
log end
