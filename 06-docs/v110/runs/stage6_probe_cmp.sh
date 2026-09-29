#!/bin/bash
# The stage-6 probe (fc096aca9624bb99) against the stage 1-5 probe's published run on the b12.5 (runs/probe_final.*):
# on the b12.5 itself, and on the fx link ([1]-[8] and every mechanism line; the file name, the stage-6 lines aside).
cd "$(dirname "$0")"
P=C:/dev/sundered-crown/06-docs/v110/runs/probe_final
export PYTHONIOENCODING=utf-8
{
echo "b12.5 under the stage-6 probe (fc096aca9624bb99, --drawn 0) vs runs/probe_final.txt (the stage 1-5 probe afa389b746f9c12b): every line but the stage-6 note (line ends ignored)"
diff --strip-trailing-cr <(grep -v "^  stage 6: not on this link" probe_b12.5_s6probe.txt) $P.txt && echo "IDENTICAL (every line)"
python -c "
import json
a=json.load(open('probe_b12.5_s6probe.json'));b=json.load(open('$P.json'))
print('counters n: equal (%d counters)' % len(a['n']) if a['n']==b['n'] else 'counters DIFFER: '+str({k:(a['n'].get(k),b['n'].get(k)) for k in set(a['n'])|set(b['n']) if a['n'].get(k)!=b['n'].get(k)}))
print('tally T: equal' if a['T']==b['T'] else 'T DIFFERS')"
echo
echo "the fx link under the stage-6 probe vs runs/probe_final.txt: every line but the stage-6 lines, [9]-[10] and the N/N, the file name aside"
diff --strip-trailing-cr <(grep -v "^  stage 6 \|^  drawn subset\|^  \[9\]\|^  \[10\]\|^  10/10" probe_fx.txt | sed 's/sc-aureole-b12.5-fx.html/LINK/') <(grep -v "^  8/8" $P.txt | sed 's/sc-aureole-b12.5.html/LINK/') && echo "IDENTICAL (every mechanism line and [1]-[8])"
python -c "
import json
a=json.load(open('probe_fx.json'));b=json.load(open('$P.json'))
d={k:(a['n'].get(k),b['n'].get(k)) for k in b['n'] if a['n'].get(k)!=b['n'].get(k)}
print('the stages 1-5 run\'s %d counters: ' % len(b['n']) + ('all equal on the fx link' if not d else 'DIFFER: '+str(d)))
print('tally T: equal' if a['T']==b['T'] else 'T DIFFERS', '; win equal:', a['win']==b['win'])
print('the fx run adds %d counters of its own ([9]-[10])' % len([k for k in a['n'] if k not in b['n']]))"
} > probe_cmp.txt 2>&1
cat probe_cmp.txt
