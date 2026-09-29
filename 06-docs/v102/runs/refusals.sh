#!/bin/bash
# The builder's refusals, re-run on the current builder: each case must refuse and write nothing.
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone"
PY=C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe; L="$S/links"; T="$S/scr/refuse"; mkdir -p "$T"
cd C:/dev/sundered-crown/tools
R(){ echo "# $1"; shift; out=$($PY lodestone_build.py "$@" 2>&1); rc=$?; echo "$out" | tail -1; [ $rc -ne 0 ] || echo "!! DID NOT REFUSE (rc 0)"; }
R "overwrite" --stage 1 --src ../02-chain/sc-tendril-t3.html --out "$L/sc-lodestone.html"
R "a base without Tendril (sc-onslaught-b23)" --stage 1 --src ../02-chain/sc-onslaught-b23.html --out "$T/x1.html"
R "stage 1 twice" --stage 1 --src "$L/sc-lodestone.html" --out "$T/x2.html"
R "stage 2 on the base" --stage 2 --src ../02-chain/sc-tendril-t3.html --out "$T/x3.html"
R "stage 3 on stage 3" --stage 3 --src "$L/sc-lodestone-rebuttal.html" --out "$T/x4.html"
R "stage 5 on stage 2" --stage 5 --src "$L/sc-lodestone-runes.html" --out "$T/x5.html"
R "stage 5 on stage 5" --stage 5 --src "$L/sc-lodestone-b205.html" --out "$T/x6.html"
R "stage 2 twice" --stage 2 --src "$L/sc-lodestone-runes.html" --out "$T/x7.html"
R "the live build" --stage 1 --src ../02-chain/sc-tendril-t3.html --out "$T/sundered-crown.html"
echo "# files written: $(ls "$T" | wc -l)"
