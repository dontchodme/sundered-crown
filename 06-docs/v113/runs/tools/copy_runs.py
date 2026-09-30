"""v113: copy the build's small run files into 06-docs/v113/runs/ (txt whole; the relic_rate and probe jsons whole;
the lab jsons SLIM -- P and the per-arm summary, the one-row-a-fight list left out and kept in scratch), the scratch
tools the runs name into runs/tools/, and the queue scripts into runs/sh/. LF text.
    python copy_runs.py <S> <repo>"""
import json, pathlib, shutil, sys
S = pathlib.Path(sys.argv[1]); REPO = pathlib.Path(sys.argv[2])
R = S / "runs"; OUT = REPO / "06-docs" / "v113" / "runs"
(OUT / "tools").mkdir(parents=True, exist_ok=True); (OUT / "sh").mkdir(parents=True, exist_ok=True)
SKIP = set()
n = {"txt": 0, "json": 0, "slim": 0, "tools": 0, "sh": 0}
def lf(p_in, p_out):
    p_out.write_text(p_in.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n"), encoding="utf-8", newline="\n")
for p in sorted(R.iterdir()):
    if not p.is_file() or p.name in SKIP:
        continue
    if p.suffix in (".txt", ".log"):
        lf(p, OUT / p.name); n["txt"] += 1
    elif p.suffix == ".json":
        j = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(j, dict) and "rows" in j:
            slim = {k: v for k, v in j.items() if k != "rows"}
            slim["rows_note"] = (f"{len(j['rows'])} per-fight rows left out of the repo copy; the full json is in the "
                                 "build's scratch (batch/thornwake/runs/)")
            (OUT / p.name).write_text(json.dumps(slim, indent=1), encoding="utf-8", newline="\n"); n["slim"] += 1
        else:
            lf(p, OUT / p.name); n["json"] += 1
    elif p.suffix == ".sh":
        lf(p, OUT / "sh" / p.name); n["sh"] += 1
# the probe's earlier passes (v113 §3), small txt + json + log, into runs/probe_pass1/ and runs/probe_pass2/
for sub in ("probe_pass1", "probe_pass2"):
    if (R / sub).is_dir():
        (OUT / sub).mkdir(exist_ok=True)
        for p in sorted((R / sub).iterdir()):
            if p.suffix in (".txt", ".json", ".log"):
                lf(p, OUT / sub / p.name); n["txt"] += 1
for p in sorted((S / "tools").iterdir()):
    if p.is_file() and p.suffix in (".py", ".js", ".sh"):
        lf(p, OUT / "tools" / p.name); n["tools"] += 1
print(n)
tot = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"{OUT}: {sum(1 for f in OUT.rglob('*') if f.is_file())} files, {tot/1024:.0f} KB")
