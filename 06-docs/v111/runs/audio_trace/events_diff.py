"""Diff two recorded SFX.play logs (render_trace.py's <tag>_events.json: [wall t, kind, opts]) and the director
curves beside them. Prints: counts by kind/voice on each side, every event only on one side, every event on both
sides whose opts differ, the first divergence in time, and whether the send curves agree (and the hall's wet max).
    python events_diff.py <dir> <tagA> <tagB> [--t0 77.98333]"""
import json, sys, collections, pathlib
D, A, B = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
T0 = float(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[4] == "--t0" else 77.98333
ea = json.loads((D / f"{A}_events.json").read_text()); eb = json.loads((D / f"{B}_events.json").read_text())
key = lambda e: (round(e[0], 6), e[1], json.dumps(e[2], sort_keys=True))
name = lambda e: e[1] + (":" + e[2]["w"] if isinstance(e[2], dict) and "w" in e[2] else "")
print(f"events {A}: {len(ea)}   {B}: {len(eb)}")
ca, cb = collections.Counter(map(name, ea)), collections.Counter(map(name, eb))
for k in sorted(set(ca) | set(cb)):
    print(f"  {k:28s} {A} {ca[k]:4d}   {B} {cb[k]:4d}" + ("" if ca[k] == cb[k] else "   <-- differs"))
sa, sb = collections.Counter(map(key, ea)), collections.Counter(map(key, eb))
onlyA, onlyB = sa - sb, sb - sa
print(f"only in {A}: {sum(onlyA.values())}; only in {B}: {sum(onlyB.values())}")
for side, S in ((A, onlyA), (B, onlyB)):
    for (t, k, p), n in sorted(S.items()):
        print(f"  only {side:4s} wall {t:8.4f} (match {T0 + t:7.3f})  {k} {p}" + (f" x{n}" if n > 1 else ""))
# same (t, kind) on both sides with different opts
ta = collections.defaultdict(list); tb = collections.defaultdict(list)
for e in ea: ta[(round(e[0], 6), e[1])].append(json.dumps(e[2], sort_keys=True))
for e in eb: tb[(round(e[0], 6), e[1])].append(json.dumps(e[2], sort_keys=True))
chg = [(k, ta[k], tb[k]) for k in sorted(set(ta) & set(tb)) if sorted(ta[k]) != sorted(tb[k])]
print(f"same time and kind, different opts: {len(chg)}")
for k, x, y in chg:
    print(f"  wall {k[0]:.4f} {k[1]}: {A} {x}  {B} {y}")
first = min([k[0] for k in onlyA] + [k[0] for k in onlyB] + [k[0][0] for k in chg] + [1e9])
print(f"first divergence: wall {first:.4f} s (match {T0 + first:.3f})")
same_before = [e for e in ea if e[0] < first]
print(f"events before it, identical on both sides: {len(same_before)}")
ca_, cb_ = (D / f"{A}_curve.json").read_text(), (D / f"{B}_curve.json").read_text()
cv = json.loads(ca_)
print(f"director curves: {'IDENTICAL' if ca_ == cb_ else 'DIFFER'} ({len(cv)} frames); wet max {max(r[2] for r in cv)}, "
      f"lowpass min {min(r[3] for r in cv)}, dry min {min(r[4] for r in cv)}, timeScale min {min(r[1] for r in cv)}")
