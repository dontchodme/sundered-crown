#!/bin/bash
# COMPOSE TEST (v109): censer_build.py against every other in-progress batch builder on this line, both ways and in two
# stacks, and on the line's newer tips on 02-chain. v107's compose11, with Censer in Lightkeeper's place. Every verdict
# comes from a chain's exit status: "ok" when a chain reached the LAST stage of its list; when another builder stops short
# of its own last stage, the verdict compares where it stops on Censer's b25.5 with where it stops on the base alone.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/censer"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/tmp/compose2"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
NFAIL=0
echo "# compose $(date +%H:%M) builders: $(for b in censer lightkeeper widowmaker aureole coldiron ironhail lodestone oracle angelus; do printf '%s %s ' $b $(sha256sum ${b}_build.py | cut -c1-16); done)"
chain(){ local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "  ($b stage $st on $(basename "$src") refused: $(grep -vE '^\s*ok|^$' "$dir/$nm.log" | tail -2 | tr '\n' ' '))" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
last(){ local x; for x in "$@"; do :; done; echo "${x#*:}"; }
verdict(){ local rc=$1 got=$(basename "$2") want=$3 arc=$4 alone=$(basename "$5") text=$6
  if [ "$rc" = 0 ] && [ "$got" = "$want" ]; then echo "ok   $text reach $got (the last stage)";
  elif [ "$rc" != 0 ] && [ "$arc" != 0 ] && [ "$got" = "$alone" ]; then echo "ok   $text stop at $got, exactly where they stop on the base alone (that builder's own state)";
  else echo "FAIL $text reach $got (rc $rc; want $want; on the base alone: $alone rc $arc)"; NFAIL=$((NFAIL+1)); fi; }
CE=(1:sc-censer-stub.html 2:sc-censer-ground.html 3:sc-censer-consecration.html 5:sc-censer-consecration-b25.5.html)
LK=(1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html)
WM=(1:sc-widowmaker-s1.html 2:sc-widowmaker-s2.html 5:sc-widowmaker-s5.html)
AU=(1:sc-aureole-s1.html 2:sc-aureole-s2.html 3:sc-aureole-s3.html 5:sc-aureole-s5.html)
CI=(1:sc-coldiron-s1.html 2:sc-coldiron-s2.html 3:sc-coldiron-s3.html 4:sc-coldiron-s4.html 5:sc-coldiron-s5.html 6:sc-coldiron-s6.html)
IH=(1:sc-ironhail-s1.html 2:sc-ironhail-s2.html 3:sc-ironhail-s3.html 6:sc-ironhail-s6.html)
LS=(1:sc-lodestone-s1.html 2:sc-lodestone-s2.html 3:sc-lodestone-s3.html 5:sc-lodestone-s5.html)
OR=(1:sc-oracle-s1.html 2:sc-oracle-s2.html 3:sc-oracle-s3.html 5:sc-oracle-s5.html)
AN=(1:sc-angelus-s1.html 2:sc-angelus-s2.html 3:sc-angelus-s3.html 5:sc-angelus-s5.html)
CELAST=$(last "${CE[@]}")
l=$(chain censer $BASE "$D/ce-alone" "${CE[@]}"); rc=$?
verdict $rc "$l" "$CELAST" 1 "" "censer 1,2,3,5 on sc-tendril-t3 alone"
for f in stub ground consecration consecration-b25.5; do
  if cmp -s "$D/ce-alone/sc-censer-$f.html" "$S/links/sc-censer-$f.html"; then echo "ok   the builder rebuilds sc-censer-$f byte for byte"; else echo "FAIL sc-censer-$f does not rebuild"; NFAIL=$((NFAIL+1)); fi; done
PAIRS="lightkeeper:LK widowmaker:WM aureole:AU coldiron:CI ironhail:IH lodestone:LS oracle:OR angelus:AN"
declare -A ALONE ALONERC
for p in $PAIRS; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  t=$(chain $b $BASE "$D/$b-first" "${!arr}"); arc=$?; ALONE[$b]=$t; ALONERC[$b]=$arc
  [ $arc = 0 ] && echo "--   $b alone on the base reaches $(basename "$t") (its last)" \
               || echo "--   $b alone on the base stops at $(basename "$t") (its builder's own state, not this build's)"
  x=$(chain censer "$t" "$D/$b-first/ce" "${CE[@]}"); rc=$?
  verdict $rc "$x" "$CELAST" 1 "" "censer 1,2,3,5 on $b's $(basename "$t"):"
  if [ "$(basename "$l")" = "$CELAST" ]; then
    y=$(chain $b "$l" "$D/ce-first-$b/$b" "${!arr}"); rc=$?
    verdict $rc "$y" "$want" $arc "$t" "$b's stages on censer's b25.5"
  fi
done
# stack 1: in version order with censer in its place (v103 coldiron, v104 angelus, v105 oracle, v106 widowmaker, v107 lightkeeper,
# v108 ironhail, lodestone, v109 CENSER, v110 aureole)
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM lightkeeper:LK ironhail:IH lodestone:LS censer:CE aureole:AU; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack1/$b" "${!arr}"); rc=$?
  if [ $b = censer ]; then verdict $rc "$n" "$want" 1 "" "stack1: censer's stages";
  else verdict $rc "$n" "$want" "${ALONERC[$b]}" "${ALONE[$b]}" "stack1: $b's stages"; fi
  src=$n; done
# stack 2: the others first, censer last
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM lightkeeper:LK ironhail:IH lodestone:LS aureole:AU; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack2/$b" "${!arr}"); rc=$?
  verdict $rc "$n" "$want" "${ALONERC[$b]}" "${ALONE[$b]}" "stack2: $b's stages"; src=$n; done
x=$(chain censer "$src" "$D/stack2/ce" "${CE[@]}"); rc=$?
verdict $rc "$x" "$CELAST" 1 "" "stack2: censer 1,2,3,5 last, on the others stacked ($(basename "$src")):"
grep -h "tail kept" "$D"/stack2/ce/*.log | head -1
# the line's newer tips on 02-chain: the change set there must be line for line the change set on sc-tendril-t3
A1=$(diff ../02-chain/sc-tendril-t3.html "$S/links/$CELAST" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
for TIP in sc-tendril-fx sc-coldiron-temper-fx sc-ironhail-fxout sc-lodestone-b205-fx sc-widowmaker-b1075-fx sc-widowmaker-fxout; do
  F=../02-chain/$TIP.html; [ -f $F ] || { echo "--   $TIP not on 02-chain"; continue; }
  x=$(chain censer $F "$D/on-$TIP" "${CE[@]}"); rc=$?
  verdict $rc "$x" "$CELAST" 1 "" "censer 1,2,3,5 on $TIP ($(sha256sum $F | cut -c1-16)):"
  if [ $rc = 0 ]; then A2=$(diff $F "$x" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
    if [ "$A1" = "$A2" ]; then echo "ok   the change set on $TIP is line for line the change set on sc-tendril-t3 ($A1); b25.5 there $(sha256sum "$x" | cut -c1-16)";
    else echo "FAIL the change set differs on $TIP: t3 $A1, $A2"; NFAIL=$((NFAIL+1)); fi; fi
done
echo "# $NFAIL FAIL"
