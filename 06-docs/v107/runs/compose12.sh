#!/bin/bash
# COMPOSE TEST 12 (v107, stage 6): compose11's harness with Lightkeeper's list now 1, 2, 3, 5 AND 6 (the picture and
# the voice), the other in-progress batch builders AS THEY STAND NOW (widowmaker, coldiron, ironhail, lodestone, oracle,
# angelus, and the two started since compose11: censer and aureole), both ways and in two stacks; then this builder's
# whole list on every newer tip of the batch line (sc-tendril-fx, sc-coldiron-temper-fx, sc-ironhail-sunder-fx,
# sc-ironhail-fxout, sc-lodestone-b205-fx, sc-widowmaker-fxout), where STAGE 6's change set (the diff from the b9.5 link
# to the fx link, its lines sorted) must be the one it writes on sc-tendril-t3. Every verdict from a chain's exit status:
#   - "ok" when a chain reached the LAST stage of its list;
#   - when another builder stops short of its own last stage, the verdict compares where it stops on lightkeeper's fx
#     link with where it stops on the base alone: the same stage is "ok (its own state)", anything else is FAIL.
# Scratch only: tmp/compose12.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/tmp/compose12"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
NFAIL=0
echo "# compose12 $(date +%H:%M) builders: $(for b in lightkeeper widowmaker coldiron ironhail lodestone oracle angelus censer aureole; do printf '%s %s ' $b $(sha256sum ${b}_build.py | cut -c1-16); done)"
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
LK=(1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html 6:sc-lightkeeper-bulwark-b9.5-fx.html)
WM=(1:sc-widowmaker-s1.html 2:sc-widowmaker-s2.html 5:sc-widowmaker-s5.html 6:sc-widowmaker-s6.html)
CI=(1:sc-coldiron-s1.html 2:sc-coldiron-s2.html 3:sc-coldiron-s3.html 4:sc-coldiron-s4.html 5:sc-coldiron-s5.html 6:sc-coldiron-s6.html)
IH=(1:sc-ironhail-s1.html 2:sc-ironhail-s2.html 3:sc-ironhail-s3.html 6:sc-ironhail-s6.html)
LS=(1:sc-lodestone-s1.html 2:sc-lodestone-s2.html 3:sc-lodestone-s3.html 5:sc-lodestone-s5.html 6:sc-lodestone-s6.html)
OR=(1:sc-oracle-s1.html 2:sc-oracle-s2.html 3:sc-oracle-s3.html 5:sc-oracle-s5.html)
AN=(1:sc-angelus-s1.html 2:sc-angelus-s2.html 3:sc-angelus-s3.html 5:sc-angelus-s5.html)
CE=(1:sc-censer-s1.html 2:sc-censer-s2.html 3:sc-censer-s3.html 5:sc-censer-s5.html)
AU=(1:sc-aureole-s1.html 2:sc-aureole-s2.html 3:sc-aureole-s3.html 5:sc-aureole-s5.html)
LKLAST=$(last "${LK[@]}")
# lightkeeper alone on the base (the reference for the stacks)
l=$(chain lightkeeper $BASE "$D/lk-alone" "${LK[@]}"); rc=$?
verdict $rc "$l" "$LKLAST" 1 "" "lightkeeper 1,2,3,5,6 on sc-tendril-t3 alone"
for n in stub wall bulwark bulwark-b9.5 bulwark-b9.5-fx; do
  if cmp -s "$D/lk-alone/sc-lightkeeper-$n.html" "$S/links/sc-lightkeeper-$n.html"; then echo "ok   lk-alone sc-lightkeeper-$n.html == the link";
  else echo "FAIL lk-alone sc-lightkeeper-$n.html differs from the link"; NFAIL=$((NFAIL+1)); fi; done
PAIRS="widowmaker:WM coldiron:CI ironhail:IH lodestone:LS oracle:OR angelus:AN censer:CE aureole:AU"
declare -A ALONE ALONERC
for p in $PAIRS; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  t=$(chain $b $BASE "$D/$b-first" "${!arr}"); arc=$?; ALONE[$b]=$t; ALONERC[$b]=$arc
  [ $arc = 0 ] && echo "--   $b alone on the base reaches $(basename "$t") (its last)" \
               || echo "--   $b alone on the base stops at $(basename "$t") (its builder's own state, not this build's)"
  x=$(chain lightkeeper "$t" "$D/$b-first/lk" "${LK[@]}"); rc=$?
  verdict $rc "$x" "$LKLAST" 1 "" "lightkeeper 1,2,3,5,6 on $b's $(basename "$t"):"
  if [ "$(basename "$l")" = "$LKLAST" ]; then
    y=$(chain $b "$l" "$D/lk-first-$b/$b" "${!arr}"); rc=$?
    verdict $rc "$y" "$want" $arc "$t" "$b's stages on lightkeeper's fx link"
  fi
done
# stack 1: in version order with lightkeeper in its place (v103 coldiron, v104 angelus, v105 oracle, v106 widowmaker,
# v107 LIGHTKEEPER, v108 ironhail, lodestone, then the two started since, censer and aureole)
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM lightkeeper:LK ironhail:IH lodestone:LS censer:CE aureole:AU; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack1/$b" "${!arr}"); rc=$?
  if [ $b = lightkeeper ]; then verdict $rc "$n" "$want" 1 "" "stack1: lightkeeper's stages";
  else verdict $rc "$n" "$want" "${ALONERC[$b]}" "${ALONE[$b]}" "stack1: $b's stages"; fi
  src=$n; done
# stack 2: the others first, lightkeeper last
src=$BASE; for p in coldiron:CI angelus:AN oracle:OR widowmaker:WM ironhail:IH lodestone:LS censer:CE aureole:AU; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack2/$b" "${!arr}"); rc=$?
  verdict $rc "$n" "$want" "${ALONERC[$b]}" "${ALONE[$b]}" "stack2: $b's stages"; src=$n; done
x=$(chain lightkeeper "$src" "$D/stack2/lk" "${LK[@]}"); rc=$?
verdict $rc "$x" "$LKLAST" 1 "" "stack2: lightkeeper 1,2,3,5,6 last, on the others stacked ($(basename "$src")):"
grep -h "tail kept" "$D"/stack2/lk/*.log | head -1
# THE NEWER TIPS OF THE BATCH LINE: the whole list on each, and stage 6's change set against sc-tendril-t3's
C0=$(diff "$S/links/sc-lightkeeper-bulwark-b9.5.html" "$S/links/sc-lightkeeper-bulwark-b9.5-fx.html" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
A0=$(diff $BASE "$S/links/sc-lightkeeper-bulwark-b9.5.html" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
echo "# stage 6's change set on sc-tendril-t3: $C0 (stages 1-5's: $A0)"
for tip in sc-tendril-fx sc-coldiron-temper-fx sc-ironhail-sunder-fx sc-ironhail-fxout sc-lodestone-b205-fx sc-widowmaker-fxout; do
  T=../02-chain/$tip.html
  x=$(chain lightkeeper $T "$D/on-$tip" "${LK[@]}"); rc=$?
  verdict $rc "$x" "$LKLAST" 1 "" "lightkeeper 1,2,3,5,6 on $tip ($(sha256sum $T | cut -c1-16)):"
  if [ $rc = 0 ]; then
    A=$(diff $T "$D/on-$tip/sc-lightkeeper-bulwark-b9.5.html" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
    C=$(diff "$D/on-$tip/sc-lightkeeper-bulwark-b9.5.html" "$x" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16)
    if [ "$A" = "$A0" ] && [ "$C" = "$C0" ]; then echo "ok   on $tip: stages 1-5's change set $A and stage 6's $C are sc-tendril-t3's; fx $(sha256sum "$x" | cut -c1-16)";
    else echo "FAIL on $tip: change sets 1-5 $A (t3 $A0), 6 $C (t3 $C0)"; NFAIL=$((NFAIL+1)); fi
  fi
done
echo "# compose12: $NFAIL FAIL"
exit $NFAIL
