"""v106 scratch: every refusal of widowmaker_build.py, re-checked (round 3)."""
import pathlib, subprocess, sys, hashlib
W = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
T = pathlib.Path(r"C:/dev/sundered-crown/tools"); BASE = r"C:/dev/sundered-crown/02-chain/sc-tendril-t3.html"
L = W / "links"; tmp = W / "refusal_tmp"; tmp.mkdir(exist_ok=True)
print("widowmaker_build.py sha16", hashlib.sha256((T / "widowmaker_build.py").read_bytes()).hexdigest()[:16])
cases = [
 ("overwrite an existing link", "5", L / "sc-widowmaker-drain.html", L / "sc-widowmaker-b1075.html"),
 ("a link not named sc-widowmaker*", "1", BASE, tmp / "sc-other.html"),
 ("stage 2 on the base (skips stage 1)", "2", BASE, tmp / "sc-widowmaker-x2.html"),
 ("stage 5 on stage 1", "5", L / "sc-widowmaker-stub.html", tmp / "sc-widowmaker-x5.html"),
 ("stage 1 on a built link", "1", L / "sc-widowmaker-drain.html", tmp / "sc-widowmaker-x1.html"),
 ("stage 2 twice", "2", L / "sc-widowmaker-drain.html", tmp / "sc-widowmaker-x22.html"),
 ("stage 5 twice", "5", L / "sc-widowmaker-b1075.html", tmp / "sc-widowmaker-x55.html"),
 ("a name already on the chain", "1", BASE, tmp / "sc-tendril-t3.html"),
]
allref = True
for what, st, src, out in cases:
    r = subprocess.run([sys.executable, "widowmaker_build.py", "--stage", st, "--src", str(src), "--out", str(out)], cwd=T, capture_output=True, text=True, encoding="utf-8")
    msg = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["?"])[-1]
    refused = r.returncode != 0 and not (out.exists() and out.parent == tmp)
    allref &= refused
    print(f"[{'REFUSED' if refused else 'WROTE!'}] {what} :: {msg}")
print("all refuse:", allref)
