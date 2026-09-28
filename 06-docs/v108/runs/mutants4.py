"""Probe controls for v108 §3 after the THIRD review: scratch mutants of THE FINAL LINK,
sc-ironhail-sunder, for the clauses the review found unguarded (who is struck, and by how much).
Written to <S>/tmp/mut4-*.html; never a link. c-caster and c-chip are the reviewer's own strings
(scratchpad/rev3_ironhail/mk_mut.py) and must come out byte-identical to the reviewer's files;
c-selfsunder is this build's, for the new sunder-target clause of [5].
  c-caster      [4]  the hail also strikes its caster: a caster within hitR + R of the spot when a
                     bolt lands takes hurt(caster, dropDmg, foe) (v83 6.3: it does not; reading 9)
  c-chip        [4]  a landing also takes 1 hp straight off the foe, outside hurt() and past the
                     ward (v83 4: "hurt(foe, 4, f) ... and nothing else")
  c-selfsunder  [5]  each landing also sunders the caster (the same apply, on f)"""
import pathlib, sys, hashlib
S = pathlib.Path(sys.argv[1]); src = (S / "links" / "sc-ironhail-sunder.html").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest()[:16] == "1bedab05b9803465"
RV = S.parent.parent / "rev3_ironhail"
M = {
 "c-caster":   ("      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R)){ T.missed++; continue; }\n",
                "      if (f.alive && Math.hypot(f.x - d.x, f.y - d.y) < u.hitR + R) this.hurt(f, u.dropDmg, foe);\n"
                "      if (!foe.alive || !(Math.hypot(foe.x - d.x, foe.y - d.y) < u.hitR + R)){ T.missed++; continue; }\n"),
 "c-chip":     ("      this.hurt(foe, u.dropDmg, f);\n", "      this.hurt(foe, u.dropDmg, f);\n      if (foe.hp > 1) foe.hp -= 1;\n"),
 "c-selfsunder": ('      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }\n',
                  '      if (u.sunder > 0){ foe.apply("sunder", u.sunder, d.side); f.apply("sunder", u.sunder, d.side); T.sunder += u.sunder; }\n'),
}
for k, (a, b) in M.items():
    assert src.count(a) == 1, (k, src.count(a))
    s = src.replace(a, b, 1)
    out = S / "tmp" / f"mut4-{k}.html"
    out.write_text(s, encoding="utf-8", newline="\n")
    rv = RV / f"mut-{k}.html"
    same = ("= the reviewer's file" if rv.exists() and rv.read_bytes() == out.read_bytes()
            else ("DIFFERS from the reviewer's file" if rv.exists() else "(this build's)"))
    print(k, hashlib.sha256(s.encode()).hexdigest()[:16], same)
