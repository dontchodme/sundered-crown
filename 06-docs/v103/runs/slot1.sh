#!/bin/bash
# slot 1 after engine_ab: tip_audit on the base and the final link, then verify --n 40 on the final.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
cd C:/dev/sundered-crown/tools
until grep -q -E "ENGINE A/B|Traceback" "$S/runs/engine_ab38.txt" 2>/dev/null; do sleep 5; done
$PY tip_audit.py --game ../02-chain/sc-tendril-t3.html > "$S/runs/tip_audit_base.txt" 2>&1
$PY tip_audit.py --game "$S/links/sc-coldiron-temper-b93.html" > "$S/runs/tip_audit_b93.txt" 2>&1
$PY verify.py --game "$S/links/sc-coldiron-temper-b93.html" --n 40 > "$S/runs/verify_b93.txt" 2>&1
echo slot1 done
