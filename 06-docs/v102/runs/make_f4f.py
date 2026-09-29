# Review round 3: writes f4f_overlay.py, a copy of tools/ult_overlay.py that ALSO keeps every fight's own record
# (winner, steps, both fighters' hits, hp, shield, crits and damage dealt, the match's clanks and end reason) in
# the out JSON as arms[arm]['fights'], so stage 1 can be set against lab arm A FIGHT FOR FIGHT, not only foe for
# foe. Nothing else changes: the record only reads, after the fight is over.
import pathlib, sys
src = pathlib.Path("C:/dev/sundered-crown/tools/ult_overlay.py").read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new, 1)
s = src
s = one(s, "sys.path.insert(0, str(pathlib.Path(__file__).parent))", "sys.path.insert(0, 'C:/dev/sundered-crown/tools')")
s = one(s, "                dur: step * DT, casts, hitsIn, hitsOut, S });",
        "                dur: step * DT, casts, hitsIn, hitsOut, S,\n"
        "                rec: [step, me.hits, foe.hits, me.hp, foe.hp, me.shield, foe.shield, me.crits, foe.crits,\n"
        "                      me.dealt, foe.dealt, m.clankCount, m.reason || null] });")
s = one(s, "                            byFoe={k: sum(v) / len(v) for k, v in byFoe.items()})",
        "                            byFoe={k: sum(v) / len(v) for k, v in byFoe.items()})\n"
        "    out['arms'][arm]['fights'] = [[r['foe'], r['seed'], r['win']] + r['rec'] for r in rs]")
out = pathlib.Path(sys.argv[1]); out.write_text(s, encoding="utf-8", newline="\n"); print("wrote", out)
