#!/bin/bash
# v117: the roster the game will carry, built IN SCRATCH only (nothing here is committed as a link):
# the batch line's final tip, Rick's Daybreak circle in place of the line (yert's sunrise_build.py,
# stages 1, 3, 5), then yert's seven staves (staff_carry.py). The balance pass is measured on it.
set -e
PY="C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe"
R=/c/dev/sundered-crown
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/balance"
TIP=${1:-$R/02-chain/sc-goreshard-fxout.html}
cd $R/tools
rm -f "$S"/r-sunrise*.html "$S"/roster49.html
$PY sunrise_build.py --stage 1 --src "$TIP" --out "$S/r-sunrise.html"
$PY sunrise_build.py --stage 3 --src "$S/r-sunrise.html" --out "$S/r-sunrise-fx.html"
$PY sunrise_build.py --stage 5 --src "$S/r-sunrise-fx.html" --out "$S/r-sunrise-e26.html"
$PY staff_carry.py --src "$S/r-sunrise-e26.html" --out "$S/roster49.html"
echo "relics: $(grep -o '{ id:"[a-z]*", name:"' "$S/roster49.html" | wc -l)"
sha256sum "$S/roster49.html" | cut -c1-16
