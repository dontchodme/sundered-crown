#!/bin/bash
# lane S1: the pick, render_ab on the other relics, tip_audit -- one job at a time, idle priority
SB=<scratch>
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $SB/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$SB/links; R=$SB/runs
log(){ echo "$(date +%H:%M:%S) $*" >> $SB/s6/laneS.log; }
log start S1
$I _spellbreaker_pick.py --game $L/sc-spellbreaker-b7.5-fx.html > $R/stage6_pick.txt 2>&1; log "pick rc $?"
$I render_ab.py --a $L/sc-spellbreaker-b7.5.html --b $L/sc-spellbreaker-b7.5-fx.html --pairs paradox:heartwood:25064,twinshade:lastlight:991,bulwarden:vinesower:70707,axiom:grudgebearer:31337 > $R/stage6_render_ab_others.txt 2>&1; log "render_ab others rc $?"
$I tip_audit.py --game $L/sc-spellbreaker-b7.5-fx.html > $R/stage6_tip_audit_fx.txt 2>&1; log "tip_audit rc $?"
log done S1
echo done > $SB/s6/laneS1.done
