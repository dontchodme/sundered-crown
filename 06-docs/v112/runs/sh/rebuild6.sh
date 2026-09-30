#!/bin/sh
# v112 §7: every link from the bare base with the stage-6 builder, then stage 6's refusals. S = $1
S="$1"; PY=/c/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; B=/c/dev/sundered-crown/tools/heartwood_build.py
R="$S/tmp/rb9"; rm -rf "$R"; mkdir -p "$R"; BASE=/c/dev/sundered-crown/02-chain/sc-tendril-t3.html
sha() { sha256sum "$1" | cut -c1-16; }
echo "builder $(sha $B)   base sc-tendril-t3 $(sha $BASE)"
prev=$BASE
for p in "1 sc-heartwood-stub 08b489bafa264c3e" "2 sc-heartwood-root 22f403961e5203a6" "3 sc-heartwood-rootfast cc303b02f2aba1d9" "5 sc-heartwood-b11 aff84a04b303a402" "6 sc-heartwood-b11-fx ceba5e801f4cf91b"; do
  set -- $p
  $PY $B --stage $1 --src "$prev" --out "$R/$2.html" > "$R/$2.log" 2>&1; rc=$?
  got=$(sha "$R/$2.html" 2>/dev/null)
  [ "$got" = "$3" ] && v="IDENTICAL" || v="!! DIFFERS (want $3)"
  echo "stage $1  $2.html  rc $rc  $got  $v"
  prev="$R/$2.html"
done
grep -h "note  Tendril" "$R/sc-heartwood-b11-fx.log"
echo "--- stage 6's refusals"
try() { d="$1"; shift; $PY $B "$@" > "$R/ref.log" 2>&1; rc=$?; echo "$d: rc $rc  $(grep -h "refusing\|REFUSING\|goes on\|needs stage\|already in" "$R/ref.log" | head -1 | cut -c1-120)"; }
try "stage 6 on stage 3's link (blade 12.65)" --stage 6 --src "$R/sc-heartwood-rootfast.html" --out "$R/sc-heartwood-x1.html"
try "stage 6 on its own output" --stage 6 --src "$R/sc-heartwood-b11-fx.html" --out "$R/sc-heartwood-x2.html"
try "stage 6 on the base" --stage 6 --src "$BASE" --out "$R/sc-heartwood-x3.html"
try "stage 5 on stage 6's link" --stage 5 --src "$R/sc-heartwood-b11-fx.html" --out "$R/sc-heartwood-x4.html"
try "stage 6 over an existing link" --stage 6 --src "$R/sc-heartwood-b11.html" --out "$R/sc-heartwood-b11-fx.html"
try "stage 6 to a name outside sc-heartwood*" --stage 6 --src "$R/sc-heartwood-b11.html" --out "$R/sc-other-fx.html"
try "stage 1 on stage 6's link" --stage 1 --src "$R/sc-heartwood-b11-fx.html" --out "$R/sc-heartwood-x5.html"
ls "$R"/sc-heartwood-x*.html "$R"/sc-other-fx.html 2>/dev/null && echo "!! A REFUSAL WROTE A FILE" || echo "no refusal wrote a file"
