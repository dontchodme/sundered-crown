#!/bin/bash
# one browser, sequential: the probe at 2 seeds on the stage-6 link and each stage-6 mutant, then the fight-for-fight compare
S="C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/angelus"
PY=/c/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe
cd C:/dev/sundered-crown/tools
echo "lane_mut6 start $(date '+%F %T %Z') probe $(sha256sum angelus_probe.py | cut -c1-16)"
$PY angelus_probe.py --game $S/links/sc-angelus-b9-fx.html --seeds 2 > $S/s6/probe_mut6_fx-s2.txt 2>&1; echo "fx-s2 exit $?"
for k in m9-chorddeath m10-overopen m11-picwrite m12-thudall; do
  $PY angelus_probe.py --game $S/s6/mut6/sc-angelus-$k.html --seeds 2 > $S/s6/probe_mut6_$k.txt 2>&1; echo "$k exit $?"
done
$PY $S/s6/mut_fights.py $S/links/sc-angelus-b9-fx.html $S/s6/mut6/sc-angelus-m9-chorddeath.html $S/s6/mut6/sc-angelus-m10-overopen.html $S/s6/mut6/sc-angelus-m11-picwrite.html $S/s6/mut6/sc-angelus-m12-thudall.html --seeds 2 > $S/s6/mut6_fights.txt 2>&1; echo "mut_fights exit $?"
echo "lane_mut6 end $(date '+%F %T %Z')"
