#!/bin/bash
# lane C1 (after lane B frees its browser): the pick, render_ab on the other relics, tip_audit -- one browser, idle priority
T=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $T/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$T/links; R=$T/runs
until [ -e $T/s6/laneB.done ]; do sleep 5; done
log(){ echo "$(date +%H:%M:%S) $*" >> $T/s6/laneC.log; }
log start C1
$I _thornwake_pick.py --game $L/sc-thornwake-b26.5-fx.html > $R/stage6_pick.txt 2>&1; log "pick rc $?"
$I render_ab.py --a $L/sc-thornwake-b26.5.html --b $L/sc-thornwake-b26.5-fx.html --pairs paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337 > $R/stage6_render_ab_others.txt 2>&1; log "render_ab others rc $?"
$I tip_audit.py --game $L/sc-thornwake-b26.5-fx.html > $R/stage6_tip_audit_fx.txt 2>&1; log "tip_audit fx rc $?"
log done C1
echo done > $T/s6/laneC1.done
