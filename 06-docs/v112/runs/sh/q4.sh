#!/bin/bash
# RICK'S RULING (the final is stage 5, sc-heartwood-b11): THE PROBE ON EVERY STAGE FROM 2, THE MUTANTS OF THE FINAL,
# THE GATES ON THE FINAL. ONE JOB AT A TIME (the build-load limit). q4.log has the timeline.
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/heartwood
R=$S/runs; L=$S/links; F=$L/sc-heartwood-b11.html
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
log(){ echo "$(date +%H:%M:%S) $*" >> $R/q4.log; }
log start; sleep 4   # the launcher lowers this shell to Idle first; every child inherits it
$PY heartwood_probe.py --game $F --stage 5 --json $R/probe_b11.json > $R/probe_b11.txt 2>&1; log "probe b11 (stage 5, the final) rc=$?"
$PY heartwood_probe.py --game $L/sc-heartwood-rootfast.html --stage 3 --json $R/probe_rootfast.json > $R/probe_rootfast.txt 2>&1; log "probe rootfast (stage 3) rc=$?"
$PY heartwood_probe.py --game $L/sc-heartwood-root.html --stage 2 --json $R/probe_root.json > $R/probe_root.txt 2>&1; log "probe root (stage 2) rc=$?"
for n in m1-window-labclock m2-every-other-blow m3-pin-before-knock m4-weapon-free m5-entangle-2 m6-root-hitstop m7-charge16 m8-row-no-entangle m9-root-stundr m10-ticker-stundr m11-blade-shipped; do
  $PY heartwood_probe.py --game $S/mut/mut-$n.html --stage 5 --json $R/probe_mut-$n.json > $R/probe_mut-$n.txt 2>&1; log "probe mut-$n rc=$?"
done
for n in m8-row-no-entangle m9-root-stundr m10-ticker-stundr; do
  $PY $S/tools/heartwood_probe_v1.py --game $S/mut/mut-$n.html --json $R/probev1_mut-$n.json > $R/probev1_mut-$n.txt 2>&1; log "OLD probe mut-$n rc=$?"
done
$PY $S/tools/mutant_table.py $S > /dev/null 2>&1; log "mutant table rc=$?"
$PY engine_ab.py --a ../02-chain/sc-tendril-t3.html --b $F --ids $(cat $R/ids37.txt) --n 6 > $R/engine_ab37.txt 2>&1; log "engine_ab37 rc=$?"
$PY engine_ab.py --a ../02-chain/sc-tendril-t3.html --b $F --ids heartwood,grudgebearer,aureole,gravemourn --n 6 > $R/engine_ab_control.txt 2>&1; log "engine_ab control rc=$?"
$PY tip_audit.py --game $F > $R/tip_audit_final.txt 2>&1; log "tip_audit final rc=$?"
$PY tip_audit.py --game ../02-chain/sc-tendril-t3.html > $R/tip_audit_base.txt 2>&1; log "tip_audit base rc=$?"
$PY chain_audit.py --relic $F --tip $F --builder heartwood_build.py > $R/chain_audit.txt 2>&1; log "chain_audit rc=$?"
$PY chain_audit.py --relic $F --tip ../02-chain/sc-tendril-t3.html --builder heartwood_build.py > $R/chain_audit_control.txt 2>&1; log "chain_audit control rc=$?"
$PY verify.py --game $F --n 40 > $R/verify_final.txt 2>&1; log "verify final rc=$?"
log end
