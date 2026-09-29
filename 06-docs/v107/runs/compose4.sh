#!/bin/bash
# COMPOSE TEST 4 (v107, resume 3): lightkeeper_build.py against EVERY other in-progress batch builder as it stands now
# (widowmaker, coldiron, ironhail, lodestone, oracle, angelus), both ways, and in two stacks. Scratch only: tmp/compose4.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/tmp/compose4"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
echo "# compose4 $(date +%H:%M) builders: $(for b in lightkeeper widowmaker coldiron ironhail lodestone oracle angelus; do printf '%s %s ' $b $(sha256sum ${b}_build.py | cut -c1-16); done)"
chain(){ local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "FAIL $b stage $st on $(basename "$src"): $(grep -vE '^\s*ok|^$' "$dir/$nm.log" | tail -3 | tr '\n' ' ')" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
LK=(1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html)
WM=(1:sc-widowmaker-s1.html 2:sc-widowmaker-s2.html 5:sc-widowmaker-s5.html)
CI=(1:sc-coldiron-s1.html 2:sc-coldiron-s2.html 3:sc-coldiron-s3.html 4:sc-coldiron-s4.html 5:sc-coldiron-s5.html)
IH=(1:sc-ironhail-s1.html 2:sc-ironhail-s2.html 3:sc-ironhail-s3.html 5:sc-ironhail-s5.html)
LS=(1:sc-lodestone-s1.html 2:sc-lodestone-s2.html 3:sc-lodestone-s3.html 5:sc-lodestone-s5.html)
OR=(1:sc-oracle-s1.html 2:sc-oracle-s2.html 3:sc-oracle-s3.html 5:sc-oracle-s5.html)
AN=(1:sc-angelus-s1.html 2:sc-angelus-s2.html 3:sc-angelus-s3.html 5:sc-angelus-s5.html)
PAIRS="widowmaker:WM coldiron:CI ironhail:IH lodestone:LS oracle:OR angelus:AN"
for p in $PAIRS; do b=${p%%:*}; arr="${p#*:}[@]"
  t=$(chain $b $BASE "$D/$b-first" "${!arr}") || echo "--   $b's own stage list stops at $(basename "$t") (its builder's own state, not this build's)"
  chain lightkeeper "$t" "$D/$b-first/lk" "${LK[@]}" >/dev/null && echo "ok   lightkeeper 1,2,3,5 on $b's stages (to $(basename "$t"))"
  l=$(chain lightkeeper $BASE "$D/lk-first-$b" "${LK[@]}") && { t=$(chain $b "$l" "$D/lk-first-$b/$b" "${!arr}"); echo "ok?  $b's stages on lightkeeper's b9.5 reach $(basename "$t")"; }
done
# stack 1: the six in version order with lightkeeper in its place (v103 coldiron, v104 angelus, v105 oracle, v106 widowmaker, v107 LIGHTKEEPER, v108 ironhail, lodestone)
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM lightkeeper:LK ironhail:IH lodestone:LS; do b=${p%%:*}; arr="${p#*:}[@]"
  n=$(chain $b "$src" "$D/stack1/$b" "${!arr}") && echo "ok   stack1 + $b" || echo "--   stack1: $b stops at $(basename "$n") (its own state)"; src=$n; done
# stack 2: the six first, lightkeeper last
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM ironhail:IH lodestone:LS; do b=${p%%:*}; arr="${p#*:}[@]"
  n=$(chain $b "$src" "$D/stack2/$b" "${!arr}") || echo "--   stack2: $b stops at $(basename "$n") (its own state)"; src=$n; done
chain lightkeeper "$src" "$D/stack2/lk" "${LK[@]}" >/dev/null && echo "ok   lightkeeper 1,2,3,5 on the other six stacked ($(basename "$src"))"
grep -h "tail kept" "$D"/stack2/lk/*.log | head -1
