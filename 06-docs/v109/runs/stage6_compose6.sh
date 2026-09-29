#!/bin/bash
# COMPOSE, STAGE 6 (v109 §5): censer_build.py stages 1,2,3,5,6 against the other in-progress batch builders (aureole s5,
# heartwood s3, spellbreaker s3 -- their last stages today), both ways and in two stacks, and on the line's newest tips on
# 02-chain. compose2's shape (runs/compose2.sh). On every tip the change set of stages 1-5 must be line for line t3's
# (98dc422a898f5043) and the change set of stage 6 alone (b25.5 -> fx there) line for line t3's.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/censer"
PY=python
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/s6/compose6"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
NFAIL=0
echo "# compose6 $(date +%H:%M) builders: $(for b in censer aureole heartwood spellbreaker; do printf '%s %s ' $b $(sha256sum ${b}_build.py | cut -c1-16); done)"
chain(){ local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "  ($b stage $st on $(basename "$src") refused: $(grep -vE '^\s*ok|^$' "$dir/$nm.log" | tail -2 | tr '\n' ' '))" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
last(){ local x; for x in "$@"; do :; done; echo "${x#*:}"; }
ok(){ echo "ok   $*"; }
bad(){ echo "FAIL $*"; NFAIL=$((NFAIL+1)); }
cs(){ diff "$1" "$2" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16; }
CE=(1:sc-censer-stub.html 2:sc-censer-ground.html 3:sc-censer-consecration.html 5:sc-censer-consecration-b25.5.html 6:sc-censer-consecration-b25.5-fx.html)
AU=(1:sc-aureole-stub.html 2:sc-aureole-halo.html 3:sc-aureole-bless.html 5:sc-aureole-b12.5.html)
HW=(1:sc-heartwood-stub.html 2:sc-heartwood-root.html 3:sc-heartwood-rootfast.html)
SB=(1:sc-spellbreaker-stub.html 2:sc-spellbreaker-stun.html 3:sc-spellbreaker-unmaking.html)
CELAST=$(last "${CE[@]}")
l=$(chain censer $BASE "$D/ce-alone" "${CE[@]}"); rc=$?
[ $rc = 0 ] && [ "$(basename "$l")" = "$CELAST" ] && ok "censer 1,2,3,5,6 on sc-tendril-t3 alone reach $CELAST" || bad "censer alone: rc $rc at $(basename "$l")"
for f in stub ground consecration consecration-b25.5 consecration-b25.5-fx; do
  cmp -s "$D/ce-alone/sc-censer-$f.html" "$S/links/sc-censer-$f.html" && ok "the builder rebuilds sc-censer-$f byte for byte" || bad "sc-censer-$f does not rebuild"; done
T15=$(cs $BASE "$D/ce-alone/sc-censer-consecration-b25.5.html"); T6=$(cs "$D/ce-alone/sc-censer-consecration-b25.5.html" "$D/ce-alone/$CELAST")
echo "--   on t3: change set of stages 1-5 $T15, of stage 6 alone $T6"
[ "$T15" = 98dc422a898f5043 ] && ok "stages 1-5 change set on t3 is compose2's 98dc422a898f5043" || bad "stages 1-5 change set on t3 moved: $T15"
for p in aureole:AU heartwood:HW spellbreaker:SB; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  t=$(chain $b $BASE "$D/$b-first" "${!arr}"); arc=$?
  [ $arc = 0 ] && echo "--   $b alone on the base reaches $(basename "$t") (its last today)" || { bad "$b alone on the base stops at $(basename "$t")"; continue; }
  x=$(chain censer "$t" "$D/$b-first/ce" "${CE[@]}"); rc=$?
  if [ $rc = 0 ] && [ "$(basename "$x")" = "$CELAST" ]; then
    A6=$(cs "$D/$b-first/ce/sc-censer-consecration-b25.5.html" "$x")
    [ "$A6" = "$T6" ] && ok "censer 1-6 on $b's $(basename "$t"): stage 6's change set is t3's ($A6)" || bad "censer 6 on $b's: change set $A6 (t3 $T6)"
  else bad "censer on $b's $(basename "$t"): rc $rc at $(basename "$x")"; fi
  y=$(chain $b "$l" "$D/ce-first-$b" "${!arr}"); rc=$?
  [ $rc = 0 ] && [ "$(basename "$y")" = "$want" ] && ok "$b's stages on censer's fx link reach $want" || bad "$b on censer's fx: rc $rc at $(basename "$y")"
done
# stack 1: censer 1-6 first, then the other three
src=$l; for p in aureole:AU heartwood:HW spellbreaker:SB; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  n=$(chain $b "$src" "$D/stack1/$b" "${!arr}"); rc=$?
  [ $rc = 0 ] && [ "$(basename "$n")" = "$want" ] && ok "stack1 (censer first): $b reaches $want" || bad "stack1: $b rc $rc at $(basename "$n")"; src=$n; done
# stack 2: the other three first, censer 1-6 last
src=$BASE; for p in aureole:AU heartwood:HW spellbreaker:SB; do b=${p%%:*}; arr="${p#*:}[@]"
  n=$(chain $b "$src" "$D/stack2/$b" "${!arr}"); src=$n; done
x=$(chain censer "$src" "$D/stack2/ce" "${CE[@]}"); rc=$?
if [ $rc = 0 ] && [ "$(basename "$x")" = "$CELAST" ]; then A6=$(cs "$D/stack2/ce/sc-censer-consecration-b25.5.html" "$x")
  [ "$A6" = "$T6" ] && ok "stack2: censer 1-6 last on the other three ($(basename "$src")), stage 6 change set t3's" || bad "stack2: change set $A6"
else bad "stack2: censer rc $rc at $(basename "$x")"; fi
# the line's newest tips on 02-chain
for TIP in sc-widowmaker-fxout sc-oracle-fx sc-angelus-b9-fx sc-lightkeeper-fxout; do
  F=../02-chain/$TIP.html; [ -f $F ] || { echo "--   $TIP not on 02-chain"; continue; }
  x=$(chain censer $F "$D/on-$TIP" "${CE[@]}"); rc=$?
  if [ $rc = 0 ] && [ "$(basename "$x")" = "$CELAST" ]; then
    A15=$(cs $F "$D/on-$TIP/sc-censer-consecration-b25.5.html"); A6=$(cs "$D/on-$TIP/sc-censer-consecration-b25.5.html" "$x")
    [ "$A15" = "$T15" ] && [ "$A6" = "$T6" ] && ok "on $TIP ($(sha256sum $F | cut -c1-16)): stages 1-5 $A15, stage 6 $A6 -- t3's both; fx there $(sha256sum "$x" | cut -c1-16)" \
      || bad "on $TIP: stages 1-5 $A15 (t3 $T15), stage 6 $A6 (t3 $T6)"
    grep -h "tail kept" "$D/on-$TIP"/sc-censer-consecration-b25.5-fx.html.log | head -1
  else bad "censer on $TIP: rc $rc at $(basename "$x")"; fi
done
echo "# $NFAIL FAIL"
