#!/bin/bash
# COMPOSE, STAGE 6 (v110 §6): aureole_build.py stages 1,2,3,5,6 on the line's tips (compose3's thirteen, plus
# the newest real tips on 02-chain: Censer carried, sc-censer-fxout and sc-censer-consecration-b25.5-fx, and
# sc-lightkeeper-fxout), and against the other in-progress batch builders (heartwood s3, spellbreaker s3: their
# last stages today) both ways. On every tip the change set of stages 1-5 must be t3's and the change set of
# stage 6 alone (b12.5 -> fx there) t3's -- or, where it is not, the lines that differ are printed.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch"
A="$S/aureole"
PY=python
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$A/s6/compose6"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
NFAIL=0
echo "# compose6 $(date +%H:%M) builders: $(for b in aureole censer heartwood spellbreaker; do printf '%s %s ' $b $(sha256sum ${b}_build.py | cut -c1-16); done)"
chain(){ local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "  ($b stage $st on $(basename "$src") refused: $(grep -vE '^\s*ok|^$' "$dir/$nm.log" | tail -2 | tr '\n' ' '))" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
last(){ local x; for x in "$@"; do :; done; echo "${x#*:}"; }
ok(){ echo "ok   $*"; }
bad(){ echo "FAIL $*"; NFAIL=$((NFAIL+1)); }
cs(){ diff "$1" "$2" | grep -E '^[<>]' | sort | sha256sum | cut -c1-16; }
AU=(1:sc-aureole-stub.html 2:sc-aureole-halo.html 3:sc-aureole-bless.html 5:sc-aureole-b12.5.html 6:sc-aureole-b12.5-fx.html)
HW=(1:sc-heartwood-stub.html 2:sc-heartwood-root.html 3:sc-heartwood-rootfast.html)
SB=(1:sc-spellbreaker-stub.html 2:sc-spellbreaker-stun.html 3:sc-spellbreaker-unmaking.html)
AULAST=$(last "${AU[@]}")
l=$(chain aureole $BASE "$D/au-alone" "${AU[@]}"); rc=$?
[ $rc = 0 ] && [ "$(basename "$l")" = "$AULAST" ] && ok "aureole 1,2,3,5,6 on sc-tendril-t3 alone reach $AULAST" || bad "aureole alone: rc $rc at $(basename "$l")"
for f in stub halo bless b12.5 b12.5-fx; do
  cmp -s "$D/au-alone/sc-aureole-$f.html" "$A/links/sc-aureole-$f.html" && ok "the builder rebuilds sc-aureole-$f byte for byte" || bad "sc-aureole-$f does not rebuild"; done
T15=$(cs $BASE "$D/au-alone/sc-aureole-b12.5.html"); T6=$(cs "$D/au-alone/sc-aureole-b12.5.html" "$D/au-alone/$AULAST")
N6=$(diff "$D/au-alone/sc-aureole-b12.5.html" "$D/au-alone/$AULAST" | grep -cE '^[<>]')
echo "--   on t3: change set of stages 1-5 $T15, of stage 6 alone $T6 ($N6 changed lines)"
diff "$D/au-alone/sc-aureole-b12.5.html" "$D/au-alone/$AULAST" | grep -E '^[<>]' | sort > "$D/t3_stage6_lines.txt"
tip(){ local F=$1 tag=$2
  x=$(chain aureole "$F" "$D/on-$tag" "${AU[@]}"); rc=$?
  if [ $rc = 0 ] && [ "$(basename "$x")" = "$AULAST" ]; then
    A15=$(cs "$F" "$D/on-$tag/sc-aureole-b12.5.html"); A6=$(cs "$D/on-$tag/sc-aureole-b12.5.html" "$x")
    r=$(grep -o '[0-9]* relics in the roster' "$D/on-$tag/$AULAST.log" | tail -1)
    if [ "$A15" = "$T15" ] && [ "$A6" = "$T6" ]; then
      ok "on $tag ($(sha256sum "$F" | cut -c1-16), $r): stages 1-5 $A15, stage 6 $A6 -- t3's both; fx there $(sha256sum "$x" | cut -c1-16)"
    elif [ "$A15" = "$T15" ]; then
      diff "$D/on-$tag/sc-aureole-b12.5.html" "$x" | grep -E '^[<>]' | sort > "$D/on-$tag/stage6_lines.txt"
      dl=$(diff "$D/t3_stage6_lines.txt" "$D/on-$tag/stage6_lines.txt" | grep -E '^[<>]')
      nd=$(echo "$dl" | grep -c .)
      # the only admissible difference: the life map's line, where another relic's own token has moved
      if [ -z "$(echo "$dl" | grep -v 'aureole: 1\.6\|censer: 1\.6\|^[<>] [<>] *$')" ]; then
        ok "on $tag ($(sha256sum "$F" | cut -c1-16), $r): stages 1-5 t3's; stage 6 $A6 -- t3's but for the life map's own line ($nd line(s): the tip's other tokens on it); fx there $(sha256sum "$x" | cut -c1-16)"
        echo "$dl" | cut -c1-160 | sed 's/^/        /'
      else bad "on $tag: stage 6 change set $A6 (t3 $T6):"; echo "$dl" | cut -c1-200 | head -12; fi
    else bad "on $tag: stages 1-5 $A15 (t3 $T15), stage 6 $A6 (t3 $T6)"; fi
  else bad "aureole on $tag: rc $rc at $(basename "$x")"; fi
  rm -f "$D/on-$tag"/*.html; }
for TIP in sc-censer-fxout sc-censer-consecration-b25.5-fx sc-lightkeeper-fxout sc-angelus-b9-fx sc-oracle-fx sc-widowmaker-fxout sc-ironhail-fxout sc-ironhail-sunder-fx sc-lodestone-b205-fx; do
  F=../02-chain/$TIP.html; [ -f $F ] && tip "$F" "$TIP" || echo "--   $TIP not on 02-chain"; done
for F in "$S/angelus/links/sc-angelus-b9-fx.html" "$S/censer/links/sc-censer-consecration-b25.5-fx.html" "$S/coldiron/links/sc-coldiron-temper-fx.html" \
         "$S/lightkeeper/links/sc-lightkeeper-bulwark-b9.5-fx.html" "$S/oracle/links/sc-oracle-fx.html" "$S/widowmaker/links/sc-widowmaker-b1075-fx-specout.html"; do
  [ -f "$F" ] && tip "$F" "scratch-$(basename $(dirname $(dirname "$F")))-$(basename "$F" .html)" || echo "--   $F missing"; done
# the other in-progress builders, both ways
for p in heartwood:HW spellbreaker:SB; do b=${p%%:*}; arr="${p#*:}[@]"; want=$(last "${!arr}")
  t=$(chain $b $BASE "$D/$b-first" "${!arr}"); arc=$?
  [ $arc = 0 ] && echo "--   $b alone on the base reaches $(basename "$t") (its last today)" || { bad "$b alone on the base stops at $(basename "$t")"; continue; }
  x=$(chain aureole "$t" "$D/$b-first/au" "${AU[@]}"); rc=$?
  if [ $rc = 0 ] && [ "$(basename "$x")" = "$AULAST" ]; then
    A6=$(cs "$D/$b-first/au/sc-aureole-b12.5.html" "$x")
    [ "$A6" = "$T6" ] && ok "aureole 1-6 on $b's $(basename "$t"): stage 6's change set is t3's ($A6)" || bad "aureole 6 on $b's: change set $A6 (t3 $T6)"
  else bad "aureole on $b's $(basename "$t"): rc $rc at $(basename "$x")"; fi
  y=$(chain $b "$l" "$D/au-first-$b" "${!arr}"); rc=$?
  [ $rc = 0 ] && [ "$(basename "$y")" = "$want" ] && ok "$b's stages on aureole's fx link reach $want" || bad "$b on aureole's fx: rc $rc at $(basename "$y")"
  rm -rf "$D/$b-first" "$D/au-first-$b"
done
rm -f "$D/au-alone"/*.html
echo "# $NFAIL FAIL"
