# Makes rf_lab.py: a scratch copy of tools/ult_overlay.py with TWO additions and nothing else changed:
#  (1) THE CENSUS (hail_census.py's, v108 §0): before each lab step, whether the step is frozen
#      (m.hitStop > 0 || m.latch || m.splitHold), in total and inside the lab's windows;
#  (2) EVERY FIGHT'S ROW in the json (perfight_overlay.py's, v108 §2), so a built link can be compared
#      with a lab arm fight by fight.
import pathlib
src = pathlib.Path("C:/dev/sundered-crown/tools/ult_overlay.py").read_text(encoding="utf-8")
def one(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new, 1)
src = one(src, "sys.path.insert(0, str(pathlib.Path(__file__).parent))",
          "sys.path.insert(0, 'C:/dev/sundered-crown/tools')")
src = one(src, "    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, casts = 0, hitsIn = 0, hitsOut = 0;\n",
          "    let t = 0, step = 0, nextCast = P.charge, castEnd = -1, casts = 0, hitsIn = 0, hitsOut = 0;\n"
          "    let fSteps = 0, fFrozen = 0, fWin = 0, fWinFrozen = 0;\n")
src = one(src, "      const h0 = me.hits;\n      m.step(DT); step++; t += DT;\n",
          "      const h0 = me.hits;\n"
          "      { const fz = m.hitStop > 0 || !!m.latch || !!m.splitHold, ow = castEnd >= 0 && t < castEnd;\n"
          "        fSteps++; if (fz) fFrozen++; if (ow){ fWin++; if (fz) fWinFrozen++; } }\n"
          "      m.step(DT); step++; t += DT;\n")
src = one(src, "                dur: step * DT, casts, hitsIn, hitsOut, S });",
          "                dur: step * DT, casts, hitsIn, hitsOut, S, fSteps, fFrozen, fWin, fWinFrozen });")
src = one(src, "    out[\"arms\"][arm] = dict(win=Wn, n=n, casts=casts / n,",
          "    _fs = sum(r['fSteps'] for r in rs); _ff = sum(r['fFrozen'] for r in rs)\n"
          "    _fw = sum(r['fWin'] for r in rs); _fwf = sum(r['fWinFrozen'] for r in rs)\n"
          "    print(f\"      census: frozen {_ff/max(1,_fs):.4f} of lab steps ({_ff}/{_fs}), \"\n"
          "          f\"{_fwf/max(1,_fw):.4f} in windows ({_fwf}/{_fw}), {(_ff-_fwf)/max(1,_fs-_fw):.4f} outside; \"\n"
          "          f\"lab {P['charge']:g} -> engine {P['charge']*(1-_ff/max(1,_fs)):.2f}\")\n"
          "    out[\"arms\"][arm] = dict(census=dict(steps=_fs, frozen=_ff, win=_fw, winFrozen=_fwf), win=Wn, n=n, casts=casts / n,")
src = one(src, "pathlib.Path(a.out).write_text(json.dumps(out, indent=1))",
          "out['rows'] = [{k: r[k] for k in ('arm', 'foe', 'seed', 'win', 'dur', 'casts', 'hitsIn', 'hitsOut', 'S')} for r in rows]\n"
          "pathlib.Path(a.out).write_text(json.dumps(out, indent=1))")
pathlib.Path(__file__).with_name("tw_lab.py").write_text(src, encoding="utf-8", newline="\n")
print("ok")
