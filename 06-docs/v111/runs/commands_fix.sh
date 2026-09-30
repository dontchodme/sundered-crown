#!/bin/bash
# Append the fix round's commands to runs/commands.txt (once): the by-hand list, then lanes N and O as they ran.
SB=<scratch>
C=$SB/runs/commands.txt
grep -q "## FIX ROUND" $C && { echo "already appended"; exit 0; }
cat $SB/runs/commands_fix_manual.part >> $C
for L in N O P; do
  echo "" >> $C; echo "## lane $L (fix round)" >> $C
  sed -e "s#C:/Users/Ye/AppData/Local/Programs/Python/Python313/python.exe#python#g" -e "s#$SB#<scratch>#g" $SB/runs/jobs$L.txt >> $C
done
echo "appended; $(wc -l < $C) lines"
