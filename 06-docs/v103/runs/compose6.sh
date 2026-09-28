#!/bin/bash
# v103 stage 6: COMPOSITION on the batch's CURRENT scratch links and the REAL tip (no browser).
# forward: coldiron_build.py stages 1-6 chained on each other build's newest link and on 02-chain/sc-tendril-fx;
# reverse: each other builder's stages chained on sc-coldiron-temper-fx (the stage-6 link).
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
B="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch"
T="$B/coldiron/rebuild/compose6"; rm -rf "$T"; mkdir -p "$T"
cd C:/dev/sundered-crown/tools
echo "COMPOSITION, STAGE 6  $(date '+%Y-%m-%d %H:%M')  coldiron_build.py $(sha256sum coldiron_build.py | cut -c1-16)"
echo "-- forward: coldiron stages 1-6 on the real tip and each newest scratch link"
for L in /c/dev/sundered-crown/02-chain/sc-tendril-fx angelus/links/sc-angelus-b9 ironhail/links/sc-ironhail-b14 \
         lightkeeper/links/sc-lightkeeper-bulwark-b9.5 lodestone/links/sc-lodestone-b205 oracle/links/sc-oracle-aim \
         widowmaker/links/sc-widowmaker-b1075; do
  case $L in /*) src="$L.html";; *) src="$B/$L.html";; esac
  n=$(basename $L); d="$T/fwd/$n"; mkdir -p "$d"; base="$src"; ok=""
  for st in 1 2 3 4 5 6; do
    out="$d/s$st.html"
    if $PY coldiron_build.py --stage $st --src "$src" --out "$out" > "$d/s$st.txt" 2>&1; then ok="$ok$st"; src="$out"
    else ok="$ok[$st REFUSED: $(grep -m1 -E 'ANCHOR|REFUS|wrong base|refus|goes on' "$d/s$st.txt")]"; break; fi
  done
  echo "  $n ($(sha256sum "$base" | cut -c1-16)): stages $ok  -> $(grep -o '[0-9]* relics in the roster' "$d/s6.txt" 2>/dev/null), s6 $(sha256sum "$d/s6.html" 2>/dev/null | cut -c1-16) ($(grep -o '[+-][0-9]* chars' "$d/s6.txt" 2>/dev/null))"
done
echo "-- reverse: each builder's stages on sc-coldiron-temper-fx"
fx="$B/coldiron/links/sc-coldiron-temper-fx.html"
rev(){ bld=$1; pre=$2; shift 2; d="$T/rev/$bld"; mkdir -p "$d"; src="$fx"; ok=""
  for st in "$@"; do
    out="$d/$pre-oncoldironfx-s$st.html"
    if $PY ${bld}_build.py --stage $st --src "$src" --out "$out" > "$d/s$st.txt" 2>&1; then ok="$ok$st "; src="$out"
    else ok="$ok[$st REFUSED: $(grep -m1 -iE 'ANCHOR|REFUS|wrong|refus|not settled|needs|goes on|expected|not measured|HOLDS' "$d/s$st.txt" | cut -c1-110)]"; break; fi
  done
  echo "  ${bld}_build.py stages $*: $ok"; }
rev angelus sc-angelus 1 2 3 5
rev ironhail sc-ironhail 1 2 3
rev lightkeeper sc-lightkeeper 1 2 3 5
rev lodestone sc-lodestone 1 2 3 5
rev oracle sc-oracle 1 2 3
rev widowmaker sc-widowmaker 1 2 5
rev bindweed sc-tendril 6
rev portcullis sc-onslaught 6
