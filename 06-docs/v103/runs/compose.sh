#!/bin/bash
# v103 review fix: COMPOSITION re-run on the batch's CURRENT scratch links (no browser).
# forward: coldiron_build.py stages 1-5 chained on each other build's newest link;
# reverse: each other builder's stages chained on sc-coldiron-temper-b93.
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
B="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch"
T="$B/coldiron/rebuild/compose"; rm -rf "$T"; mkdir -p "$T"
cd C:/dev/sundered-crown/tools
echo "COMPOSITION  $(date '+%Y-%m-%d %H:%M')  coldiron_build.py $(sha256sum coldiron_build.py | cut -c1-16)"
echo "-- forward: coldiron stages 1-5 on each newest scratch link"
for L in angelus/links/sc-angelus-b9 bindweed/links/sc-tendril-fx ironhail/links/sc-ironhail-b14 \
         lightkeeper/links/sc-lightkeeper-bulwark-b9.5 lodestone/links/sc-lodestone-b215 oracle/links/sc-oracle-aim \
         portcullis/links/sc-onslaught-fx widowmaker/links/sc-widowmaker-b1075; do
  n=$(basename $L); d="$T/fwd/$n"; mkdir -p "$d"; src="$B/$L.html"; ok=""
  for st in 1 2 3 4 5; do
    out="$d/s$st.html"
    if $PY coldiron_build.py --stage $st --src "$src" --out "$out" > "$d/s$st.txt" 2>&1; then ok="$ok$st"; src="$out"
    else ok="$ok[$st REFUSED: $(grep -m1 -E 'ANCHOR|REFUS|wrong base|refus' "$d/s$st.txt")]"; break; fi
  done
  echo "  $n ($(sha256sum "$B/$L.html" | cut -c1-16)): stages $ok  -> $(grep -o '[0-9]* relics in the roster' "$d/s5.txt" 2>/dev/null)"
done
echo "-- reverse: each builder's stages on sc-coldiron-temper-b93"
b93="$B/coldiron/links/sc-coldiron-temper-b93.html"
rev(){ bld=$1; pre=$2; shift 2; d="$T/rev/$bld"; mkdir -p "$d"; src="$b93"; ok=""
  for st in "$@"; do
    out="$d/$pre-oncoldiron-s$st.html"
    if $PY ${bld}_build.py --stage $st --src "$src" --out "$out" > "$d/s$st.txt" 2>&1; then ok="$ok$st "; src="$out"
    else ok="$ok[$st REFUSED: $(grep -m1 -iE 'ANCHOR|REFUS|wrong|refus|not settled|needs|goes on|expected' "$d/s$st.txt" | cut -c1-110)]"; break; fi
  done
  echo "  ${bld}_build.py stages $*: $ok"; }
# (a stage 5 whose number is not measured yet refuses by design: "not measured" / "not settled")
rev angelus sc-angelus 1 2 3 5
rev ironhail sc-ironhail 1 2 3 5
rev lightkeeper sc-lightkeeper 1 2 3 5
rev lodestone sc-lodestone 1 2 3 5
rev oracle sc-oracle 1 2 3 5
rev widowmaker sc-widowmaker 1 2 5
rev bindweed sc-tendril 6
rev portcullis sc-onslaught 6
