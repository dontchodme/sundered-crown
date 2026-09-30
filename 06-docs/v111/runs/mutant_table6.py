"""Stage 6's probe controls, tabled: each mutant's failing checks (and their counts), its score, and its fights
against the clean fx link's on the same fights (the per-fight digest: won/lost and steps)."""
import hashlib, json, pathlib, re
SB = pathlib.Path(r"<scratch>")
R = SB / "runs"
MUT = [("mV1-closedeath", "[7]", "the close voice on EVERY close, a death's too", "stage6_probe_fx_s1"),
       ("mV2-stunx1", "[7]", "the stun voice on EVERY hex proc, x1 too", "stage6_probe_fx_s1"),
       ("mP1-picwrite", "[8]", "tickUnmaking nudges the foe 1e-9 at a HEX +2 relabel", "stage6_probe_fx_s1"),
       ("mG1-greyx1", "[8]", "the grey on EVERY hex proc (a plain stun greyed)", "stage6_probe_fx_s1"),
       ("mD1-drawwrite", "[8]", "drawUnmaking nudges side a 1e-9 when it draws (drawn only)", "stage6_probe_fx_drawn")]
def score(txt):
    m = re.search(r"^\s+(\d+)/(\d+)", txt, re.M); return f"{m.group(1)}/{m.group(2)}" if m else "?"
def win(txt):
    m = re.search(r"Spellbreaker win ([\d.]+)%", txt); return m.group(1) if m else "?"
print(f"{'mutant':16s} {'sha16':16s}  breaks  {'probe':6s} fails (count)                 fights vs the clean link   win   how")
for name, chk, how, ref in MUT:
    h = hashlib.sha256((SB / "mutants6" / f"sc-spellbreaker-{name}.html").read_bytes()).hexdigest()[:16]
    p = R / f"stage6_probe_mut_{name}.json"
    if not p.exists():
        print(f"{name:16s} {h}  {chk}   (not run yet)"); continue
    j = json.loads(p.read_text()); t = (R / f"stage6_probe_mut_{name}.txt").read_text(encoding="utf-8")
    fails = [f"[{k[1:]}] {v}x" for k, v in sorted(j["n"].items()) if re.fullmatch(r"x\d+", k)]
    nx = [ln.strip()[:4] for ln in t.splitlines() if "NOT EXERCISED" in ln]
    rp = R / (ref + ".json")
    cmp = "?"
    if rp.exists():
        ref_d = {tuple(d[:3]): d[3:] for d in json.loads(rp.read_text())["digest"]}
        mine = {tuple(d[:3]): d[3:] for d in j["digest"]}
        common = [k for k in mine if k in ref_d]
        ch = sum(1 for k in common if mine[k] != ref_d[k])
        cmp = f"{ch} of {len(common)} differ" if ch else f"identical ({len(common)})"
    print(f"{name:16s} {h}  {chk}   {score(t):6s} {', '.join(fails) + (' ' + ' '.join(nx) + ' n.e.' if nx else ''):30s} {cmp:26s} {win(t):>5s}  {how}")
cl = R / "stage6_probe_fx_s1.txt"
if cl.exists():
    t = cl.read_text(encoding="utf-8"); print(f"\nthe clean fx link on the same first-seed fights: {score(t)}, Spellbreaker win {win(t)}%")
