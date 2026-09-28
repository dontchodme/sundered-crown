#!/bin/bash
# stage 6 session 6: the widened-guard builder rebuilds stages 1-6 from the base, byte for byte
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/coldiron"
R="$S/rebuild/v7"; cd C:/dev/sundered-crown/tools
echo "REBUILD OF RECORD CHECK  coldiron_build.py $(sha256sum coldiron_build.py | cut -c1-16)  $(date '+%F %T')"
prev=C:/dev/sundered-crown/02-chain/sc-tendril-t3.html
echo "  base sc-tendril-t3 $(sha256sum $prev | cut -c1-16)"
for st in 1 2 3 4 5 6; do
  case $st in 1) n=sc-coldiron;; 2) n=sc-coldiron-mass;; 3) n=sc-coldiron-bind;; 4) n=sc-coldiron-temper;; 5) n=sc-coldiron-temper-b93;; 6) n=sc-coldiron-temper-fx;; esac
  rm -f "$R/$n.html"
  $PY coldiron_build.py --stage $st --src "$prev" --out "$R/$n.html" > "$R/build_s$st.txt" 2>&1 || { echo "  stage $st FAILED"; cat "$R/build_s$st.txt"; exit 1; }
  a=$(sha256sum "$R/$n.html" | cut -c1-16); b=$(sha256sum "$S/links/$n.html" | cut -c1-16)
  [ "$a" = "$b" ] && v=identical || v=DIFFERENT
  echo "  stage $st $n rebuilt $a  link $b  $v"
  prev="$R/$n.html"
done
