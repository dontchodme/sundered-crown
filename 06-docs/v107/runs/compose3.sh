#!/bin/bash
# COMPOSE TEST (v107): lightkeeper_build.py on top of the other in-progress batch builders' links, and they on top of it.
# Nothing here is a chain link; everything lands in tmp/compose3.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/tmp/compose3"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
chain(){ # $1 builder, $2 src, $3 dir, rest: stage:name pairs; echoes the last out
  local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "FAIL $b stage $st on $(basename "$src"): $(tail -3 "$dir/$nm.log" | tr '\n' ' ')" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
LK=(1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html)
WM=(1:sc-widowmaker-stub.html 2:sc-widowmaker-drain.html 5:sc-widowmaker-bzz.html)
CI=(1:sc-coldiron.html 2:sc-coldiron-mass.html 3:sc-coldiron-bind.html 4:sc-coldiron-temper.html 5:sc-coldiron-temper-bzz.html)
IH=(1:sc-ironhail-stub.html 2:sc-ironhail-hail.html 3:sc-ironhail-sunder.html 5:sc-ironhail-bzz.html)
LS=(1:sc-lodestone.html 2:sc-lodestone-runes.html 3:sc-lodestone-rebuttal.html 5:sc-lodestone-bzz.html)
for pair in "widowmaker WM" "coldiron CI" "ironhail IH" "lodestone LS"; do set -- $pair; b=$1; arr="$2[@]"
  # each alone under lightkeeper, and lightkeeper under each
  t=$(chain $b $BASE "$D/$b-first" "${!arr}") && l=$(chain lightkeeper "$t" "$D/$b-first/lk" "${LK[@]}") && echo "ok   lightkeeper 1,2,3,5 on $b's last link ($(basename "$t"))"
  l=$(chain lightkeeper $BASE "$D/lk-first-$b" "${LK[@]}") && t=$(chain $b "$l" "$D/lk-first-$b/$b" "${!arr}") && echo "ok   $b's stages on lightkeeper's b9.5"
done
# all four stacked, then lightkeeper
src=$BASE; for pair in "widowmaker WM" "coldiron CI" "ironhail IH" "lodestone LS"; do set -- $pair; arr="$2[@]"; src=$(chain $1 "$src" "$D/stack/$1" "${!arr}") || break; done
l=$(chain lightkeeper "$src" "$D/stack/lk" "${LK[@]}") && echo "ok   lightkeeper 1,2,3,5 on all four stacked ($(basename "$src"))"
grep -h "tail kept" "$D"/stack/lk/*.log | head -2
# all four stacked with coldiron first (widowmaker's stage 5 moves the donor coldiron copies), then lightkeeper
src=$BASE; for pair in "coldiron CI" "widowmaker WM" "ironhail IH" "lodestone LS"; do set -- $pair; arr="$2[@]"; src=$(chain $1 "$src" "$D/stackb/$1" "${!arr}") || break; done
l=$(chain lightkeeper "$src" "$D/stackb/lk" "${LK[@]}") && echo "ok   lightkeeper 1,2,3,5 on all four stacked, coldiron first ($(basename "$src"))"
grep -h "tail kept" "$D"/stackb/lk/*.log | head -1
