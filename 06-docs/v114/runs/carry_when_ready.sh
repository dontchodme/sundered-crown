#!/bin/bash
# v114: wait for Heartwood's fx-out link (the tip Goreshard carries onto), then carry, prove, gate.
R=/c/dev/sundered-crown
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad"
for i in $(seq 1 360); do [ -f $R/02-chain/sc-heartwood-fxout.html ] && break; sleep 30; done
[ -f $R/02-chain/sc-heartwood-fxout.html ] || { echo "NO HEARTWOOD FXOUT after 3h"; exit 1; }
sleep 5
cd $R && C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe -u "$S/build/carry.py" --relic oathwound --moved ironhail,widowmaker,lightkeeper,censer,aureole,spellbreaker,thornwake,heartwood --tip 02-chain/sc-heartwood-fxout.html --scratch-final "$S/batch/goreshard/links/sc-goreshard-b10.25-fx.html" --step tools/goreshard_build.py:1:sc-goreshard-stub.html --step tools/goreshard_build.py:2:sc-goreshard-price.html --step tools/goreshard_build.py:5:sc-goreshard-b10.25.html --step tools/goreshard_build.py:6:sc-goreshard-b10.25-fx.html --runs 06-docs/v114/runs && bash 06-docs/v114/runs/fxout/fxout.sh
