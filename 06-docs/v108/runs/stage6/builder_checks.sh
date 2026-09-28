#!/bin/bash
# v108 stage 6: the builder's refusals, and every link rebuilt from the real tip byte for byte (no browser).
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/ironhail
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools; T="$S/s6/tmp"; rm -rf "$T"; mkdir -p "$T"
echo "BUILDER CHECKS, STAGE 6  $(date '+%H:%M')  ironhail_build.py $(sha256sum ironhail_build.py | cut -c1-16)"
try(){ echo "-- $1:"; shift; $PY ironhail_build.py "$@" > "$T/try.txt" 2>&1; rc=$?; echo "   $(tail -1 "$T/try.txt")"; echo "   exit $rc"; }
try "stage 6 on the fx link (twice)" --stage 6 --src "$S/links/sc-ironhail-sunder-fx.html" --out "$T/sc-ironhail-x1.html"
try "stage 6 over an existing link (overwrite)" --stage 6 --src "$S/links/sc-ironhail-sunder.html" --out "$S/links/sc-ironhail-sunder-fx.html"
try "stage 6 on the 50% link (b14)" --stage 6 --src "$S/links/sc-ironhail-b14.html" --out "$T/sc-ironhail-x2.html"
try "stage 6 on stage 2 (hail, sunder 0)" --stage 6 --src "$S/links/sc-ironhail-hail.html" --out "$T/sc-ironhail-x3.html"
try "stage 6 on stage 1 (stub)" --stage 6 --src "$S/links/sc-ironhail-stub.html" --out "$T/sc-ironhail-x4.html"
try "stage 6 on the tip (no stages 1-3)" --stage 6 --src ../02-chain/sc-tendril-t3.html --out "$T/sc-ironhail-x5.html"
echo "-- REBUILD from the real tip, stages 1, 2, 3, 6 (and 5 --alt50 on 3), byte for byte:"
src=../02-chain/sc-tendril-t3.html
for st in 1 2 3 6; do out="$T/sc-ironhail-rb-s$st.html"; $PY ironhail_build.py --stage $st --src "$src" --out "$out" > "$T/rb-s$st.txt" 2>&1 || echo "   stage $st FAILED"; src="$out"; done
$PY ironhail_build.py --stage 5 --alt50 --src "$T/sc-ironhail-rb-s3.html" --out "$T/sc-ironhail-rb-b14.html" > "$T/rb-b14.txt" 2>&1 || echo "   b14 FAILED"
for pair in "rb-s1 sc-ironhail-stub" "rb-s2 sc-ironhail-hail" "rb-s3 sc-ironhail-sunder" "rb-s6 sc-ironhail-sunder-fx" "rb-b14 sc-ironhail-b14"; do set -- $pair
  a=$(sha256sum "$T/sc-ironhail-$1.html" | cut -c1-16); b=$(sha256sum "$S/links/$2.html" | cut -c1-16); echo "   $2: rebuilt $a  link $b  $([ "$a" = "$b" ] && echo IDENTICAL || echo DIFFER)"; done
