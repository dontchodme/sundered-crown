#!/bin/bash
# v108 stage 6: COMPOSITION on the real tip and the batch's CURRENT scratch links (no browser).
# forward: ironhail_build.py stages 1, 2, 3, 6 chained on each base; the stage-6 diff (s3 -> s6) must be the same on every base.
# reverse: each other builder's stages chained on sc-ironhail-sunder-fx (the stage-6 link).
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
B="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch"
T="$B/ironhail/compose6"; rm -rf "$T"; mkdir -p "$T"
cd C:/dev/sundered-crown/tools
echo "COMPOSITION, STAGE 6  $(date '+%Y-%m-%d %H:%M')  ironhail_build.py $(sha256sum ironhail_build.py | cut -c1-16)"
echo "-- forward: ironhail stages 1, 2, 3, 6 on the real tip and each newest link"
for L in /c/dev/sundered-crown/02-chain/sc-tendril-t3 /c/dev/sundered-crown/02-chain/sc-tendril-fx /c/dev/sundered-crown/02-chain/sc-onslaught-fx \
         coldiron/links/sc-coldiron-temper-fx angelus/links/sc-angelus-b9 lightkeeper/links/sc-lightkeeper-bulwark-b9.5 \
         lodestone/links/sc-lodestone-b205 oracle/links/sc-oracle-sight widowmaker/links/sc-widowmaker-b1075; do
  case $L in /*) src="$L.html";; *) src="$B/$L.html";; esac
  n=$(basename $L); d="$T/fwd/$n"; mkdir -p "$d"; base="$src"; ok=""
  for st in 1 2 3 6; do
    out="$d/sc-ironhail-s$st.html"
    if $PY ironhail_build.py --stage $st --src "$src" --out "$out" > "$d/s$st.txt" 2>&1; then ok="$ok$st"; src="$out"
    else ok="$ok[$st REFUSED: $(grep -m1 -E 'ANCHOR|REFUS|wrong base|refus|goes on' "$d/s$st.txt")]"; break; fi
  done
  if [ -f "$d/sc-ironhail-s6.html" ]; then
    diff "$d/sc-ironhail-s3.html" "$d/sc-ironhail-s6.html" | grep '^[<>]' > "$d/diff36.txt"
    dd="s3->s6 $(wc -l < "$d/diff36.txt") lines md5 $(md5sum < "$d/diff36.txt" | cut -c1-12)"
  else dd=""; fi
  echo "  $n ($(sha256sum "$base" | cut -c1-16)): stages $ok -> $(grep -o '[0-9]* relics in the roster' "$d/s6.txt" 2>/dev/null), s6 $(sha256sum "$d/sc-ironhail-s6.html" 2>/dev/null | cut -c1-16) ($(grep -o '[+-][0-9]* chars' "$d/s6.txt" 2>/dev/null)) $dd"
done
echo "-- reverse: each builder's stages on sc-ironhail-sunder-fx"
fx="$B/ironhail/links/sc-ironhail-sunder-fx.html"
rev(){ bld=$1; pre=$2; shift 2; d="$T/rev/$bld"; mkdir -p "$d"; src="$fx"; ok=""
  for st in "$@"; do
    out="$d/$pre-onironhailfx-s$st.html"
    if $PY ${bld}_build.py --stage $st --src "$src" --out "$out" > "$d/s$st.txt" 2>&1; then ok="$ok$st "; src="$out"
    else ok="$ok[$st REFUSED: $(grep -m1 -iE 'ANCHOR|REFUS|wrong|refus|not settled|needs|goes on|expected|not measured|HOLDS' "$d/s$st.txt" | cut -c1-110)]"; break; fi
  done
  echo "  ${bld}_build.py stages $*: $ok"; }
rev angelus sc-angelus 1 2 3 5
rev coldiron sc-coldiron 1 2 3 4 5 6
rev lightkeeper sc-lightkeeper 1 2 3 5
rev lodestone sc-lodestone 1 2 3 5
rev oracle sc-oracle 1 2 3
rev widowmaker sc-widowmaker 1 2 5
rev bindweed sc-tendril 6
rev portcullis sc-onslaught 6
echo "done $(date '+%H:%M')"
