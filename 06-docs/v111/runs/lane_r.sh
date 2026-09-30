#!/bin/bash
# lane R: stage 6's probe runs, mutants and engine_ab -- one job at a time, idle priority (Rick is on the PC)
SB=<scratch>
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
I="$PY $SB/s6/idle_exec.py $PY"
cd C:/dev/sundered-crown/tools
L=$SB/links; R=$SB/runs; M=$SB/mutants6
log(){ echo "$(date +%H:%M:%S) $*" >> $SB/s6/laneR.log; }
log start
$I spellbreaker_probe.py --game $L/sc-spellbreaker-b7.5.html --drawn 0 --json $R/stage6_probe_b7.5.json > $R/stage6_probe_b7.5.txt 2>&1; log "probe b7.5 rc $?"
$I spellbreaker_probe.py --game $L/sc-spellbreaker-b7.5-fx.html --drawn 0 --json $R/stage6_probe_fx.json > $R/stage6_probe_fx.txt 2>&1; log "probe fx rc $?"
$I spellbreaker_probe.py --game $L/sc-spellbreaker-b7.5-fx.html --seeds 1 --drawn 0 --json $R/stage6_probe_fx_s1.json > $R/stage6_probe_fx_s1.txt 2>&1; log "probe fx s1 rc $?"
for m in mV1-closedeath mV2-stunx1 mP1-picwrite mG1-greyx1; do
  $I spellbreaker_probe.py --game $M/sc-spellbreaker-$m.html --seeds 1 --drawn 0 --json $R/stage6_probe_mut_$m.json > $R/stage6_probe_mut_$m.txt 2>&1; log "probe $m rc $?"
done
DF=grudgebearer,twinshade,axiom,dawnbringer,nightfell,gravemourn
$I spellbreaker_probe.py --game $M/sc-spellbreaker-mD1-drawwrite.html --seeds 1 --foes $DF --drawn 24 --json $R/stage6_probe_mut_mD1-drawwrite.json > $R/stage6_probe_mut_mD1-drawwrite.txt 2>&1; log "probe mD1 rc $?"
$I engine_ab.py --a $L/sc-spellbreaker-b7.5.html --b $L/sc-spellbreaker-b7.5-fx.html --ids dawnbringer,widowmaker,grudgebearer,thornwake,lastlight,gravemourn,slagheart,spellbreaker,ironhail,lightkeeper,farwarden,aureole,censer,emberedge,oathwound,heartwood,nightfell,axiom,twinshade,redflail,foregone,vinesower,bulwarden,marrowdraw,paradox,thornshear,vesper,shroudmaul,cindercleave,ravelbone,gloamwire,bloodmirror,duskreave,starwarden,morningstar,ironwood,portcullis,bindweed --n 6 > $R/stage6_engine_ab38.txt 2>&1; log "engine_ab38 rc $?"
$I engine_ab.py --a $L/sc-spellbreaker-b7.5.html --b $M/sc-spellbreaker-mP1-picwrite.html --ids spellbreaker,farwarden,dawnbringer,twinshade --n 6 > $R/stage6_engine_ab_control.txt 2>&1; log "engine_ab control rc $?"
$I spellbreaker_probe.py --game $L/sc-spellbreaker-b7.5-fx.html --seeds 1 --drawn 24 --json $R/stage6_probe_fx_drawn.json > $R/stage6_probe_fx_drawn.txt 2>&1; log "probe fx drawn rc $?"
$I spellbreaker_probe.py --game $L/sc-spellbreaker-b7.5.html --seeds 1 --foes $DF --drawn 24 --json $R/stage6_probe_b7.5_drawn.json > $R/stage6_probe_b7.5_drawn.txt 2>&1; log "probe b7.5 drawn (control) rc $?"
log done
echo done > $SB/s6/laneR.done
