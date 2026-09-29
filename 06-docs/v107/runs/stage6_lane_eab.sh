#!/bin/bash
# one Chromium at a time: engine_ab b9.5 -> b9.5-fx, all 38 ids (Lightkeeper IN), n 6
cd "/c/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper/s6int"
export PYTHONIOENCODING=utf-8
echo "eab38 start $(date +%H:%M:%S)" >> lanes.log
./bn.cmd C:/dev/sundered-crown/tools/engine_ab.py --a "C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper/links/sc-lightkeeper-bulwark-b9.5.html" --b "C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper/links/sc-lightkeeper-bulwark-b9.5-fx.html" --ids "dawnbringer,widowmaker,grudgebearer,thornwake,lastlight,gravemourn,slagheart,spellbreaker,ironhail,lightkeeper,farwarden,aureole,censer,emberedge,oathwound,heartwood,nightfell,axiom,twinshade,redflail,foregone,vinesower,bulwarden,marrowdraw,paradox,thornshear,vesper,shroudmaul,cindercleave,ravelbone,gloamwire,bloodmirror,duskreave,starwarden,morningstar,ironwood,portcullis,bindweed" --n 6 > runs/engine_ab38.txt 2>&1
echo "eab38 done $(date +%H:%M:%S) rc $?" >> lanes.log
