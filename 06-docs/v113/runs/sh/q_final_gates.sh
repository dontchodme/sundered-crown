#!/bin/bash
# LANE B: the stage-5 proof, the stage-5 row of built vs lab, the gates on the final. $1 = BLADE
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/thornwake
source $S/runs/lowpri.sh
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
F=$S/links/sc-thornwake-b$1.html; BASE=../02-chain/sc-tendril-t3.html
log(){ echo "$(date +%H:%M:%S) $*" >> $S/runs/q_final_gates.log; }
log start
for b in 2207 2317; do bash $S/runs/rr.sh $F b$1 $b; log "rr proof b$1 $b"; done
for b in 2207 2317; do bash $S/runs/built.sh $F final $b; log "built final $b"; done
for b in 2207 2317; do
  $PY $S/tools/tw_lab.py --game C:/dev/sundered-crown/02-chain/sc-tendril-t3.html --relic thornwake --mech C:/dev/sundered-crown/tools/overlays/bramble.js --arms C --P blade=$1 --seeds 20 --seed0 $b --foes $(cat $S/runs/foes33.txt) --label "lab C at blade $1, block $b" --out $S/runs/lab_C_b$1_$b.json > $S/runs/lab_C_b$1_$b.txt 2>&1; log "lab C blade $1 $b rc=$?"
done
$PY engine_ab.py --a $BASE --b $F --ids $(cat $S/runs/ids37.txt) --n 6 > $S/runs/engine_ab37.txt 2>&1; log "engine_ab37 rc=$?"
$PY engine_ab.py --a $BASE --b $F --ids thornwake,grudgebearer,aureole,gravemourn --n 6 > $S/runs/engine_ab_control.txt 2>&1; log "engine_ab control rc=$?"
$PY tip_audit.py --game $F > $S/runs/tip_audit_final.txt 2>&1; log "tip_audit final rc=$?"
$PY tip_audit.py --game $BASE > $S/runs/tip_audit_base.txt 2>&1; log "tip_audit base rc=$?"
$PY chain_audit.py --relic $F --tip $F --builder thornwake_build.py > $S/runs/chain_audit.txt 2>&1; log "chain_audit rc=$?"
$PY chain_audit.py --relic $F --tip $BASE --builder thornwake_build.py > $S/runs/chain_audit_control.txt 2>&1; log "chain_audit control (base tip) rc=$?"
$PY chain_audit.py --relic $F --tip $S/links/sc-thornwake-snare.html --builder thornwake_build.py > $S/runs/chain_audit_control_blade.txt 2>&1; log "chain_audit control (stage-3 tip) rc=$?"
$PY verify.py --game $F --n 40 > $S/runs/verify_final.txt 2>&1; log "verify final n40 rc=$?"
log end
