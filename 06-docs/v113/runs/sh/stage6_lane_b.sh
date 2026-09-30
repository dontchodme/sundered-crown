#!/bin/bash
# lane B: engine_ab (all 38 ids, Thornwake included) and its controls, then the base drawn control -- one browser, idle priority
T=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $T/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$T/links; R=$T/runs; M=$T/mut6
log(){ echo "$(date +%H:%M:%S) $*" >> $T/s6/laneB.log; }
log start
$I engine_ab.py --a $L/sc-thornwake-b26.5.html --b $L/sc-thornwake-b26.5-fx.html --ids dawnbringer,widowmaker,grudgebearer,thornwake,lastlight,gravemourn,slagheart,spellbreaker,ironhail,lightkeeper,farwarden,aureole,censer,emberedge,oathwound,heartwood,nightfell,axiom,twinshade,redflail,foregone,vinesower,bulwarden,marrowdraw,paradox,thornshear,vesper,shroudmaul,cindercleave,ravelbone,gloamwire,bloodmirror,duskreave,starwarden,morningstar,ironwood,portcullis,bindweed --n 6 > $R/stage6_engine_ab38.txt 2>&1; log "engine_ab38 rc $?"
$I engine_ab.py --a $L/sc-thornwake-b26.5.html --b $M/mP1-picwrite.html --ids thornwake,paradox,aureole,gravemourn --n 6 > $R/stage6_engine_ab_control_mP1.txt 2>&1; log "engine_ab control mP1 rc $?"
$I engine_ab.py --a $L/sc-thornwake-b26.5.html --b $M/mV1-closevoice.html --ids thornwake,paradox,aureole,gravemourn --n 6 > $R/stage6_engine_ab_mV1.txt 2>&1; log "engine_ab mV1 (blind) rc $?"
$I engine_ab.py --a $L/sc-thornwake-b26.5.html --b $M/mP2-invisible.html --ids thornwake,paradox,aureole,gravemourn --n 6 > $R/stage6_engine_ab_mP2.txt 2>&1; log "engine_ab mP2 (blind) rc $?"
$I thornwake_probe.py --game $L/sc-thornwake-b26.5.html --stage 5 --seeds 1 --drawn 24 --json $R/stage6_probe_b26.5_drawn.json > $R/stage6_probe_b26.5_drawn.txt 2>&1; log "probe b26.5 drawn (control) rc $?"
log done
echo done > $T/s6/laneB.done
