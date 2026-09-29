# Review round 3: the four links rebuilt after the row comment was reworded. Each new link against its round-2
# predecessor: the +/- lines, and the two pages with comments stripped (the builder's own strip) compared whole.
import difflib, hashlib, pathlib, re, sys
S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lodestone")
def strip(js): return re.sub(r"//[^\n]*", "", re.sub(r"/\*[\s\S]*?\*/", "", js))
def sha(b): return hashlib.sha256(b).hexdigest()[:16]
ok = True
for n in ("sc-lodestone", "sc-lodestone-runes", "sc-lodestone-rebuttal", "sc-lodestone-b205"):
    o = (S / "ctl/r2-links" / f"{n}.html").read_bytes(); w = (S / "links" / f"{n}.html").read_bytes()
    a, b = o.decode("utf-8"), w.decode("utf-8")
    d = [x for x in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0) if x[:1] in "+-" and not x.startswith(("+++", "---"))]
    same = strip(a) == strip(b); lines = len(a.splitlines()) == len(b.splitlines())
    print(f"{n:<24} round 2 {sha(o)} -> round 3 {sha(w)}   {len(d)} +/- lines   same line count: {lines}   identical with comments stripped: {same}")
    ok &= same and lines
    for x in d: print("    " + x)
print("ONLY THE ROW COMMENT CHANGED" if ok else "SOMETHING ELSE CHANGED")
