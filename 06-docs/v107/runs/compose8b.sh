#!/bin/bash
# COMPOSE TEST 8b (v107, resume 7): Ironhail's builder (491643c55a34fa56) now carries stages 1, 2, 3 and 6 (its stage 5
# writes nothing by its own design: the blade holds). compose8 plays its old list (1,2,3,5), which stops at stage 3 by
# Ironhail's own state; this plays its CARRY list, 1,2,3,6, both ways with lightkeeper's four stages. Verdicts from the
# chains' exit status. Scratch only: tmp/compose8b.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
export PYTHONIOENCODING=utf-8
cd C:/dev/sundered-crown/tools
D="$S/tmp/compose8b"; rm -rf "$D"; mkdir -p "$D"
BASE=../02-chain/sc-tendril-t3.html
NFAIL=0
echo "# compose8b $(date +%H:%M) builders: lightkeeper $(sha256sum lightkeeper_build.py | cut -c1-16) ironhail $(sha256sum ironhail_build.py | cut -c1-16)"
chain(){ local b=$1 src=$2 dir=$3; shift 3; mkdir -p "$dir"
  for sn in "$@"; do st=${sn%%:*}; nm=${sn#*:}
    if ! $PY ${b}_build.py --stage $st --src "$src" --out "$dir/$nm" > "$dir/$nm.log" 2>&1; then echo "  ($b stage $st on $(basename "$src") refused: $(grep -vE '^\s*ok|^$' "$dir/$nm.log" | tail -2 | tr '\n' ' '))" >&2; echo "$src"; return 1; fi
    src="$dir/$nm"; done; echo "$src"; }
v(){ if [ "$1" = 0 ] && [ "$(basename "$2")" = "$3" ]; then echo "ok   $4 reach $3 (the last stage)"; else echo "FAIL $4 reach $(basename "$2") (rc $1; want $3)"; NFAIL=$((NFAIL+1)); fi; }
LK=(1:sc-lightkeeper-stub.html 2:sc-lightkeeper-wall.html 3:sc-lightkeeper-bulwark.html 5:sc-lightkeeper-bulwark-b9.5.html)
IH=(1:sc-ironhail-s1.html 2:sc-ironhail-s2.html 3:sc-ironhail-s3.html 6:sc-ironhail-s6.html)
t=$(chain ironhail $BASE "$D/ih-first" "${IH[@]}"); v $? "$t" sc-ironhail-s6.html "ironhail 1,2,3,6 on sc-tendril-t3 alone:"
x=$(chain lightkeeper "$t" "$D/ih-first/lk" "${LK[@]}"); v $? "$x" sc-lightkeeper-bulwark-b9.5.html "lightkeeper 1,2,3,5 on ironhail's s6:"
l=$(chain lightkeeper $BASE "$D/lk-first" "${LK[@]}"); v $? "$l" sc-lightkeeper-bulwark-b9.5.html "lightkeeper 1,2,3,5 on sc-tendril-t3 alone:"
y=$(chain ironhail "$l" "$D/lk-first/ih" "${IH[@]}"); v $? "$y" sc-ironhail-s6.html "ironhail 1,2,3,6 on lightkeeper's b9.5:"
cmp -s "$l" "$S/links/sc-lightkeeper-bulwark-b9.5.html" && echo "ok   lk-first b9.5 == the link" || { echo "FAIL lk-first b9.5 differs from the link"; NFAIL=$((NFAIL+1)); }
echo "# compose8b: $NFAIL FAIL"
exit $NFAIL
