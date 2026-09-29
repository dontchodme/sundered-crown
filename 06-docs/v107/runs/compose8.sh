#!/bin/bash
# COMPOSE TEST 8 (v107, resume 7): compose7 re-run with the builders as they stand at 22:05 (ironhail moved), and on the newest tip 02-chain/sc-coldiron-temper-fx (Coldiron carried)
# (the review's fourth finding: compose6 printed "ok?" on every run). Every verdict now comes from a chain's exit status:
#   - "ok" when a chain reached the LAST stage of its list;
#   - when another builder stops short of its own last stage, the verdict compares where it stops on lightkeeper's b9.5
#     with where it stops on the base alone: the same stage is "ok (its own state)", anything else is FAIL.
# lightkeeper_build.py against EVERY other in-progress batch builder as it stands now (widowmaker, coldiron, ironhail,
# lodestone, oracle, angelus), both ways, and in two stacks; and on the line's tip sc-tendril-fx. Scratch only: tmp/compose8.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/tmp/compose8"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
NFAIL=0
echo "# compose8 $(date +%H:%M) builders: $(for b in lightkeeper widowmaker coldiron ironhail lodestone oracle angelus; do printf '%s %s ' $b $(sha256sum ${b}_build.py | cut -c1-16); done)"
# chain BUILDER SRC DIR STAGE:NAME... -> prints the last file reached; exit 0 only if every stage wrote
chain(){ local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "  ($b stage $st on $(basename "$src") refused: $(grep -vE '^\s*ok|^$' "$dir/$nm.log" | tail -2 | tr '\n' ' '))" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
last(){ local x; for x in "$@"; do :; done; echo "${x#*:}"; }
verdict(){ # verdict RC REACHED WANT_LAST ALONE_RC ALONE_REACHED TEXT
  local rc=$1 got=$(basename "$2") want=$3 arc=$4 alone=$(basename "$5") text=$6
  if [ "$rc" = 0 ] && [ "$got" = "$want" ]; then echo "ok   $text reach $got (the last stage)";
  elif [ "$rc" != 0 ] && [ "$arc" != 0 ] && [ "$got" = "$alone" ]; then echo "ok   $text stop at $got, exactly where they stop on the base alone (that builder's own state)";
  else echo "FAIL $text reach $got (rc $rc; want $want; on the base alone: $alone rc $arc)"; NFAIL=$((NFAIL+1)); fi; }
LK=(1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html)
WM=(1:sc-widowmaker-s1.html 2:sc-widowmaker-s2.html 5:sc-widowmaker-s5.html)
CI=(1:sc-coldiron-s1.html 2:sc-coldiron-s2.html 3:sc-coldiron-s3.html 4:sc-coldiron-s4.html 5:sc-coldiron-s5.html 6:sc-coldiron-s6.html)
IH=(1:sc-ironhail-s1.html 2:sc-ironhail-s2.html 3:sc-ironhail-s3.html 5:sc-ironhail-s5.html)
LS=(1:sc-lodestone-s1.html 2:sc-lodestone-s2.html 3:sc-lodestone-s3.html 5:sc-lodestone-s5.html)
OR=(1:sc-oracle-s1.html 2:sc-oracle-s2.html 3:sc-oracle-s3.html 5:sc-oracle-s5.html)
AN=(1:sc-angelus-s1.html 2:sc-angelus-s2.html 3:sc-angelus-s3.html 5:sc-angelus-s5.html)
LKLAST=$(last "${LK[@]}")
# lightkeeper alone on the base (the reference for the stacks)
l=$(chain lightkeeper $BASE "$D/lk-alone" "${LK[@]}"); rc=$?
verdict $rc "$l" "$LKLAST" 1 "" "lightkeeper 1,2,3,5 on sc-tendril-t3 alone"
PAIRS="widowmaker:WM coldiron:CI ironhail:IH lodestone:LS oracle:OR angelus:AN"
declare -A ALONE ALONERC
for p in $PAIRS; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  # b alone on the base: where its own stage list reaches
  t=$(chain $b $BASE "$D/$b-first" "${!arr}"); arc=$?; ALONE[$b]=$t; ALONERC[$b]=$arc
  [ $arc = 0 ] && echo "--   $b alone on the base reaches $(basename "$t") (its last)" \
               || echo "--   $b alone on the base stops at $(basename "$t") (its builder's own state, not this build's)"
  # lightkeeper on b's last reached stage
  x=$(chain lightkeeper "$t" "$D/$b-first/lk" "${LK[@]}"); rc=$?
  verdict $rc "$x" "$LKLAST" 1 "" "lightkeeper 1,2,3,5 on $b's $(basename "$t"):"
  # b's stages on lightkeeper's b9.5
  if [ "$(basename "$l")" = "$LKLAST" ]; then
    y=$(chain $b "$l" "$D/lk-first-$b/$b" "${!arr}"); rc=$?
    verdict $rc "$y" "$want" $arc "$t" "$b's stages on lightkeeper's b9.5"
  fi
done
# stack 1: the six in version order with lightkeeper in its place (v103 coldiron, v104 angelus, v105 oracle, v106 widowmaker, v107 LIGHTKEEPER, v108 ironhail, lodestone)
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM lightkeeper:LK ironhail:IH lodestone:LS; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack1/$b" "${!arr}"); rc=$?
  if [ $b = lightkeeper ]; then verdict $rc "$n" "$want" 1 "" "stack1: lightkeeper's stages";
  else verdict $rc "$n" "$want" "${ALONERC[$b]}" "${ALONE[$b]}" "stack1: $b's stages"; fi
  src=$n; done
# stack 2: the six first, lightkeeper last
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM ironhail:IH lodestone:LS; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack2/$b" "${!arr}"); rc=$?
  verdict $rc "$n" "$want" "${ALONERC[$b]}" "${ALONE[$b]}" "stack2: $b's stages"; src=$n; done
x=$(chain lightkeeper "$src" "$D/stack2/lk" "${LK[@]}"); rc=$?
verdict $rc "$x" "$LKLAST" 1 "" "stack2: lightkeeper 1,2,3,5 last, on the other six stacked ($(basename "$src")):"
grep -h "tail kept" "$D"/stack2/lk/*.log | head -1
# the line's tip moved after the batch's base: Bindweed / Tendril stage 6 (sc-tendril-fx, 2c9cb29). This builder on it:
FX=../02-chain/sc-tendril-fx.html
echo "# sc-tendril-fx $(sha256sum $FX | cut -c1-16)"
x=$(chain lightkeeper $FX "$D/on-fx" "${LK[@]}"); rc=$?
verdict $rc "$x" "$LKLAST" 1 "" "lightkeeper 1,2,3,5 on sc-tendril-fx (the line's current tip):"
[ $rc = 0 ] && echo "     on-fx b9.5 $(sha256sum "$x" | cut -c1-16)"
# the inserts are the same text on both tips: diff(t3 -> b9.5) and diff(fx -> fx+b9.5) carry the same added/removed lines
A1=$(diff ../02-chain/sc-tendril-t3.html "$S/links/sc-lightkeeper-bulwark-b9.5.html" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
A2=$(diff $FX "$D/on-fx/sc-lightkeeper-bulwark-b9.5.html" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
if [ "$A1" = "$A2" ]; then echo "ok   the change set on sc-tendril-fx is line for line the change set on sc-tendril-t3 ($A1)"; else echo "FAIL the change set differs: t3 $A1 fx $A2"; NFAIL=$((NFAIL+1)); fi

# the newest tip on 02-chain: Coldiron carried (sc-coldiron-temper-fx). This builder on it:
CT=../02-chain/sc-coldiron-temper-fx.html
echo "# sc-coldiron-temper-fx $(sha256sum $CT | cut -c1-16)"
x=$(chain lightkeeper $CT "$D/on-ct" "${LK[@]}"); rc=$?
verdict $rc "$x" "$LKLAST" 1 "" "lightkeeper 1,2,3,5 on sc-coldiron-temper-fx (the newest tip on 02-chain):"
[ $rc = 0 ] && echo "     on-ct b9.5 $(sha256sum "$x" | cut -c1-16)"
A3=$(diff $CT "$D/on-ct/sc-lightkeeper-bulwark-b9.5.html" | grep -E "^[<>]" | sort | sha256sum | cut -c1-16)
if [ "$A1" = "$A3" ]; then echo "ok   the change set on sc-coldiron-temper-fx is line for line the change set on sc-tendril-t3 ($A1)"; else echo "FAIL the change set differs: t3 $A1 coldiron-temper-fx $A3"; NFAIL=$((NFAIL+1)); fi
# the scratch links from this builder on the base are the links
for n in stub wall bulwark bulwark-b9.5; do
  if cmp -s "$D/lk-alone/sc-lightkeeper-$n.html" "$S/links/sc-lightkeeper-$n.html"; then echo "ok   lk-alone sc-lightkeeper-$n.html == the link";
  else echo "FAIL lk-alone sc-lightkeeper-$n.html differs from the link"; NFAIL=$((NFAIL+1)); fi; done
echo "# compose8: $NFAIL FAIL"
exit $NFAIL
