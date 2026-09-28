# Makes perfight_overlay.py: a scratch copy of tools/ult_overlay.py that ALSO writes every fight's
# row (arm, foe, seed, win, dur, casts, hits in/out) into its json, so stage 1 can be compared
# with the lab's arm A fight by fight (the v108 review's note: ult_overlay's json keeps no
# per-fight rows). Nothing else changes.
import pathlib
src = pathlib.Path("C:/dev/sundered-crown/tools/ult_overlay.py").read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new, 1)
src = one(src, "sys.path.insert(0, str(pathlib.Path(__file__).parent))",
          "sys.path.insert(0, 'C:/dev/sundered-crown/tools')")
src = one(src, "pathlib.Path(a.out).write_text(json.dumps(out, indent=1))",
          "out['rows'] = [{k: r[k] for k in ('arm', 'foe', 'seed', 'win', 'dur', 'casts', 'hitsIn', 'hitsOut')} for r in rows]\n"
          "pathlib.Path(a.out).write_text(json.dumps(out, indent=1))")
pathlib.Path(__file__).with_name("perfight_overlay.py").write_text(src, encoding="utf-8", newline="\n")
print("ok")
