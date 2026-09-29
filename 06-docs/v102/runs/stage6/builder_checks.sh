#!/bin/bash
# v102 stage 6: the builder's refusals, and every link rebuilt from the real tip byte for byte (no browser).
S=C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools; T="$S/s6/tmp"; rm -rf "$T"; mkdir -p "$T"
echo "BUILDER CHECKS, STAGE 6  $(date '+%Y-%m-%d %H:%M')  lodestone_build.py $(sha256sum lodestone_build.py | cut -c1-16)"
try(){ echo "-- $1:"; shift; $PY lodestone_build.py "$@" > "$T/try.txt" 2>&1; rc=$?; echo "   $(tail -1 "$T/try.txt")"; echo "   exit $rc"; }
try "stage 6 on the fx link (twice)" --stage 6 --src "$S/links/sc-lodestone-b205-fx.html" --out "$T/sc-lodestone-x1.html"
try "stage 6 over an existing link (overwrite)" --stage 6 --src "$S/links/sc-lodestone-b205.html" --out "$S/links/sc-lodestone-b205-fx.html"
try "stage 6 on stage 3 (blade 23.5, not the final)" --stage 6 --src "$S/links/sc-lodestone-rebuttal.html" --out "$T/sc-lodestone-x2.html"
try "stage 6 on stage 2 (hurl 0)" --stage 6 --src "$S/links/sc-lodestone-runes.html" --out "$T/sc-lodestone-x3.html"
try "stage 6 on stage 1 (stub)" --stage 6 --src "$S/links/sc-lodestone.html" --out "$T/sc-lodestone-x4.html"
try "stage 6 on the tip (no stages 1-5)" --stage 6 --src ../02-chain/sc-tendril-t3.html --out "$T/sc-lodestone-x5.html"
try "stage 5 on the fx link" --stage 5 --src "$S/links/sc-lodestone-b205-fx.html" --out "$T/sc-lodestone-x6.html"
echo "-- REBUILD from the real tip, stages 1, 2, 3, 5, 6, byte for byte:"
src=../02-chain/sc-tendril-t3.html
for st in 1 2 3 5 6; do out="$T/sc-lodestone-rb-s$st.html"; $PY lodestone_build.py --stage $st --src "$src" --out "$out" > "$T/rb-s$st.txt" 2>&1 || echo "   stage $st FAILED: $(tail -1 "$T/rb-s$st.txt")"; src="$out"; done
for pair in "rb-s1 sc-lodestone" "rb-s2 sc-lodestone-runes" "rb-s3 sc-lodestone-rebuttal" "rb-s5 sc-lodestone-b205" "rb-s6 sc-lodestone-b205-fx"; do set -- $pair
  a=$(sha256sum "$T/sc-lodestone-$1.html" | cut -c1-16); b=$(sha256sum "$S/links/$2.html" | cut -c1-16); echo "   $2: rebuilt $a  link $b  $([ "$a" = "$b" ] && echo IDENTICAL || echo DIFFER)"; done
