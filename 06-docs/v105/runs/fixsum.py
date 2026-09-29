"""Scratch (v105 §3a, the fix round): one file with
  1. the mutant table: each of the 12 mutants under the fixed probe (its failing checks), the previous probe's verdict on
     the four it could not see, and engine_ab against the link (Oracle + 7 foes, n=4);
  2. the identity of the rebuilt links with the first build: engine_ab old -> new field for field; the SHIP runs
     (every key of every arm, the byFoe rates and blow counts); the probe's mechanism lines; relic_rate on the stage-5
     link against the first build's and the grid's d10 run.

  python fixsum.py <runs dir>
"""
import json, pathlib, re, sys

R = pathlib.Path(sys.argv[1])
MUT = [("rv-charge", "the reviewer's: the window feeds the charge 25% faster (f.charge += 0.25 dt in the aim)", 7),
       ("rv-spindir", "the reviewer's: the aim sets spinDir, so the bow leaves each window spinning its last way", 6),
       ("mut-winclock", "the window stretched 10% by a writer in the aim (ultSight.t -= 0.1 dt)", 1),
       ("mut-cdhit", "the stream quickened by a writer in resolveHit (fireCd -= 0.05 a window arrow)", 3),
       ("mut-window", "the window 1% long (dur x 1.01 at the cast)", 1),
       ("mut-nolead", "no lead: aim at where the foe IS", 2),
       ("mut-cadence", "the stream 10% quicker in the window (tickFire touched)", 3),
       ("mut-dmg", "the window's arrows 10% harder", 4),
       ("mut-bladehex", "the second hex on blade blows too", 5),
       ("mut-nudge", "the aim nudges the caster (vx += 1e-9)", 6),
       ("mut-wait", "the cast waits 0.5 past its charge", 7),
       ("mut-stunlock", "CONTROL, reading 2 the other way: no turn while stunned", 2)]


def fails(p):
    t = p.read_text(errors="replace") if p.exists() else ""
    if not re.search(r"\d/7\s*$", t.strip()):
        return None, t
    return [int(x) for x in re.findall(r"\[(\d)\] FAIL", t)], t


def eab(p):
    t = p.read_text(errors="replace") if p.exists() else ""
    d = re.search(r"FAIL\s+every match identical field for field\s+\S+\s+(\d+) differ", t)
    if d:
        return d.group(1)
    if re.search(r"PASS\s+every match identical", t):
        return "0"
    return "?"


out = ["MUTANTS of sc-oracle-b10 72dcd8aa43e5b501 (variants.py; oracle_probe --seeds 2, 152 fights; "
       "engine_ab against the link, Oracle + 7 foes, n=4: 112 fights, Oracle's own 28)", ""]
ok_all = True
for k, what, want in MUT:
    f, t = fails(R / f"probe2_{k}.txt")
    nd = eab(R / f"eab2_{k}.txt")
    pv = ""
    pp = R / f"probeprev_{k}.txt"
    if pp.exists():
        pf, _ = fails(pp)
        pv = "   previous probe: " + ("n/a" if pf is None else ("PASSED 7/7 (blind)" if not pf else f"fails {pf}"))
    good = f == [want] and nd not in ("0", "?")
    ok_all &= good
    out.append(f"[{want}] {k:<13} {what:<92} fails {f}  engine_ab {nd}/112 differ  {'OK' if good else 'NOT OK'}{pv}")
    for line in t.splitlines():
        if "FAIL" in line and "[" in line:
            out.append("      " + line.strip()[:240])
out.append("")
out.append("EVERY MUTANT FAILS ITS OWN CHECK AND ONLY THAT ONE, AND CHANGES FIGHTS" if ok_all
           else "!! NOT EVERY MUTANT IS A CLEAN CONTROL")

out += ["", "IDENTITY: the rebuilt links (the aim's locals renamed) against the first build", ""]
for st in ("aim", "sight", "b10"):
    out.append(f"  engine_ab first -> rebuilt {st:<6} " + ("IDENTICAL field for field" if eab(R / f"eab_oldnew_{st}.txt") == "0"
                                                        else f"DIFFERS ({eab(R / f'eab_oldnew_{st}.txt')})"))
for st in ("aim", "sight", "b10"):
    for sd in (2207, 2317):
        a, b = R / f"built_{st}_{sd}.json", R / f"built2_{st}_{sd}.json"
        if not b.exists():
            out.append(f"  SHIP {st} {sd}: not run"); continue
        A, B = json.loads(a.read_text()), json.loads(b.read_text())
        same = A.get("arms") == B.get("arms")
        w = B["arms"]["SHIP"]["win"]
        out.append(f"  SHIP {st:<6} {sd}: win {100*w:.1f}  every arm key (win, n, casts, blows, byFoe) "
                   + ("IDENTICAL to the first build's" if same else "DIFFERS"))
for st in ("aim", "sight", "b10"):
    a, b = R / f"probe_{st}.txt", R / f"probe2_{st}.txt"
    if not b.exists() or not b.read_text().strip():
        out.append(f"  probe {st}: not run"); continue
    keep = lambda t: [l for l in t.splitlines() if l.strip() and "OWNERS" not in l and not l.strip().startswith("[")
                      and not re.match(r"^\s*\d/7\s*$", l)]
    out.append(f"  probe {st:<6} mechanism lines " + ("IDENTICAL to the first build's" if keep(a.read_text()) == keep(b.read_text())
                                                       else "DIFFER"))
for sd in (2207, 2317):
    b = R / f"s5link2_rr_{sd}.json"
    if not b.exists():
        out.append(f"  relic_rate {sd}: not run"); continue
    B = json.loads(b.read_text())
    for ref in (f"s5link_rr_{sd}.json", f"stage5_rr_d10_{sd}.json"):
        A = json.loads((R / ref).read_text())
        diff = [k for k in set(A) | set(B) if k not in ("game", "set", "label") and A.get(k) != B.get(k)]
        out.append(f"  relic_rate rebuilt b10 {sd} vs {ref:<24} " + ("IDENTICAL (every key but game/set/label)" if not diff
                                                                     else f"DIFFERS in {sorted(diff)}"))
print("\n".join(out))
