"""The probe's stage-6 extension must not count into [1]-[6]'s counters: every counter name the stages 1-5
probe increments keeps its number of `inc(` sites in the new probe, and every name the new probe adds is
new. Names are read from the source (literal strings and template heads). Pass the old and new probe."""
import collections, re, sys, hashlib
def sites(path):
    s = open(path, encoding="utf-8").read()
    c = collections.Counter()
    for m in re.finditer(r'\binc\(\s*(?:"([^"]+)"|`([^`$]*)(?:\$\{[^}]*\}[^`]*)?`|([^,)]+))', s):
        name = m.group(1) or ((m.group(2) or "") + ("*" if "${" in m.group(0) else "")) or ("EXPR:" + m.group(3).strip())
        c[name] += 1
    return c, hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
(o, so), (n, sn) = sites(sys.argv[1]), sites(sys.argv[2])
print(f"old probe {so}: {sum(o.values())} inc sites, {len(o)} names; new probe {sn}: {sum(n.values())} sites, {len(n)} names")
bad = [k for k in o if n.get(k, 0) != o[k]]
for k in sorted(o):
    print(f"  kept   {k:28s} old {o[k]}  new {n.get(k, 0)}{'   <- MOVED' if n.get(k, 0) != o[k] else ''}")
added = sorted(k for k in n if k not in o)
print("  added  " + ", ".join(f"{k} ({n[k]})" for k in added))
clash = [k for k in added if any(k.rstrip('*') and (k.rstrip('*').startswith(j.rstrip('*')) or j.rstrip('*').startswith(k.rstrip('*'))) and j.endswith('*') for j in o)]
print(f"{'PASS' if not bad and not clash else 'FAIL'}: {len(bad)} old counters moved, {len(clash)} new names inside an old template")
sys.exit(1 if bad or clash else 0)
