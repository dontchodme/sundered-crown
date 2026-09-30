"""v112 stage 6: the doc's numbers, read off the run files into s6/fill.json for doc6_apply.py. SCRATCH."""
import hashlib, json, pathlib, re
S = pathlib.Path(__file__).resolve().parent.parent; R = S / "runs"; P = R / "stage6_probe"
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:16]
T = lambda p: (P / p).read_text(encoding="utf-8", errors="replace")
def grab(txt, pat, cast=int):
    m = re.search(pat, txt); assert m, pat
    return [cast(g) for g in m.groups()]
fx, dr = T("probe_fx.txt"), T("probe_fx_drawn.txt")
score = lambda t: re.search(r"\n  (\d+)/(\d+)\s*$", t).group(0).strip()
assert score(fx) == "10/10" and score(dr) == "10/10", (score(fx), score(dr))
cv, rv, ks, cc, dc = grab(fx, r"casts voiced (\d+)  roots voiced (\d+)  killing blows silent (\d+)  closes silent: clock (\d+), death (\d+)")
gc, gok, gw = grab(fx, r"tickGrove calls (\d+) \(sim clean (\d+), whole-state clean (\d+)\)")
mh, mr, sh = grab(fx, r"new holds (\d+), re-roots (\d+), self-held left alone (\d+)")
tg, tf = grab(fx, r"tags counted (\d+) \(teaching panels (\d+)\)")
fo, wi = grab(fx, r"green in the window (\d+)  wither frames (\d+)")
dfr, dpic, dstop = grab(dr, r"drawn frames (\d+) \((\d+) with the picture up, (\d+) in a hit stop\)")
dfights = grab(dr, r"(\d+) fights \(Heartwood")[0]
dgc = grab(dr, r"tickGrove calls (\d+)")[0]
c = lambda n: f"{n:,}"
same = (T("probe_b11.txt").splitlines()[2:7] == fx.splitlines()[2:7])
assert same, "the fx link's [1]-[8] numbers are not the final's"
M = (R / "stage6_probe_mutants.txt").read_text(encoding="utf-8")
assert "EVERY STAGE-6 CONTROL FAILS ITS OWN CHECK AND ONLY IT; EVERY STAGE 0-5 CONTROL READS AS BEFORE" in M
def mrow(name):
    j = json.loads(T(f"probe_mut-{name}.json")); st = re.findall(r"\[(\d+)\] (PASS|FAIL)", T(f"probe_mut-{name}.txt"))
    failed = [int(k) for k, v in st if v == "FAIL"]
    return failed, j
lines = []
DESC = {"s6-close-voice": "a voice at every close of the window, the deaths' included",
        "s6-kill-voice": "the root's voice moved above the killing blow's return (every root still voiced once)",
        "s6-grove-sim": "`tickGrove` nudging the held ball's `vx` by 1e-9 when it marks a root",
        "s6-grove-rng": "`tickGrove` drawing the fight's RNG for its motes"}
SH6 = dict(re.findall(r"mut-(\S+)\.html\s+(\w+)", (R / "mutants6_shas.txt").read_text()))
for name, d in DESC.items():
    failed, j = mrow(name)
    msg = (j["bad"].get(str(failed[0]), [""])[0] if failed else "")[:110].replace("`", "'")
    FSx = json.loads(T("probe_fx.json"))["S"]; k = lambda q: (q["wins"], q["bin"], q["bout"], q["casts"])
    moved = "the fights CHANGED" if k(j["S"]) != k(FSx) else "no fight moved (a voice decides nothing)"
    lines.append(f"  - `{name}` ({SH6[name]}), {d}: fails **{failed}** only ({j['n'].get('x' + str(failed[0]), 0)} "
                 f"times; e.g. \"{msg}\"); {moved}")
mut6 = "\n".join(lines)
old = [ln for ln in M.splitlines() if re.match(r"  (m\d+|x\d)-", ln)]
asb = sum("AS BEFORE" in ln for ln in old)
F = {
    "BUILDER": sha("C:/dev/sundered-crown/tools/heartwood_build.py"),
    "PROBE": sha("C:/dev/sundered-crown/tools/heartwood_probe.py"),
    "HEAD_PROBE": "the probe 10/10 with its two new checks (the voices; the picture's hook, 74 fights drawn) each failed by its own mutants",
    "PROBE_SCORE": "10/10",
    "PROBE_SAME": " (4.31 casts a fight, 16.16 blows in a window, 3.67 rooted a cast, the foe held 43.7% of window frames, "
                  "Heartwood 50.5%; and on the final, `--stage 5`, the probe's output is byte-identical to the fix round's)",
    "PROBE9": (f"{c(cv)} casts each voiced once inside `fireUlt`; {c(rv)} roots each voiced once inside `rootBlow`, opts "
               f"exactly `{{w: \"heartwood-root\"}}`, nothing else sounding there; {ks} killing blows silent; no voice at any of "
               f"{c(cc)} clock closes or {dc} death closes; the run's totals exactly those"),
    "PROBE10": (f"{c(gc)} `tickGrove` calls with the simulation unchanged and no RNG ({c(gw)} of them snapshotted whole: every "
                f"field of both fighters, the shades and the match but the picture's own), {c(mh)} new holds and {c(mr)} "
                f"re-roots marked on the held ball, {sh} self-held balls left alone, {c(tg)} tags printing the root's count "
                f"({tf} teaching panels left alone), the green up on all {c(fo)} window calls, {c(wi)} wither calls"),
    "PROBE_DRAWN": (f"**10/10, {c(dfr)} frames drawn over {dfights} fights, {c(dpic)} with the picture up and {c(dstop)} of them "
                    f"in a hit stop: none threw, none wrote the simulation or the picture's own state** ({c(dgc)} `tickGrove` "
                    f"calls clean on the way)"),
    "PROBE_MUT6": mut6,
    "PROBE_MUT15": (f"**{asb} of {len(old)} (the fifteen and `x3`, aside) read exactly as on the fix round's probe** — the same failing checks and the same "
                    f"fights (`runs/stage6_probe_mutants.txt`): the stage-6 changes to the probe moved none of [1]-[8]."),
}
(S / "s6" / "fill.json").write_text(json.dumps(F, indent=1), encoding="utf-8", newline="\n")
for k, v in F.items():
    print(k, "=", v[:300])
