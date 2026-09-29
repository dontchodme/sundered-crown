"""Scratch only: the stage-6 link as it will look after the carry's fx_remove -- SPECS.widowmaker out of the
page's inlined fx.js and its stamps re-cut, as tools/fx_remove.py does, WITHOUT touching src/render/fx.js
(which follows the batch tip). Removes the three lines of the entry only (the picture lab's removal; its sha
is checked), not the NOVAS header above it. Nothing else in the page may move."""
import hashlib, pathlib, re, sys, difflib
sys.path.insert(0, r"C:/dev/sundered-crown/tools")
import fx_remove as FR
S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/widowmaker")
src = S / "links/sc-widowmaker-b1075-fx.html"; out = S / "links/sc-widowmaker-b1075-fx-specout.html"
s0 = src.read_text(encoding="utf-8")
h, body = FR.inlined(s0)
mod = body + "\n"
old_sha = h.group(1)
assert hashlib.sha256(mod.encode()).hexdigest() == old_sha, "the inlined copy is not its stamp"
full = FR.spec_block(mod, "widowmaker")
three = full[full.index("    widowmaker: {"):]
for name, blk in (("with the NOVAS header (fx_remove's spec_block)", full), ("the three lines only", three)):
    print(f"  {name}: module sha -> {hashlib.sha256(mod.replace(blk, '', 1).encode()).hexdigest()[:16]}")
print("  the picture lab's removal: f710f845485543b6 (its report)")
mod2 = mod.replace(three, "", 1); new_sha = hashlib.sha256(mod2.encode()).hexdigest()
assert s0.count(three) == 1
s = s0.replace(three, "", 1).replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
assert FR.inlined(s)[1] + "\n" == mod2
gone = [l for l in difflib.unified_diff(s0.split("\n"), s.split("\n"), n=0, lineterm="") if l[:1] in "+-" and not l.startswith(("---", "+++"))]
print(f"  lines moved: {len(gone)} ({sum(1 for l in gone if old_sha[:16] in l or new_sha[:16] in l)} of them stamps)")
if out.exists(): raise SystemExit(f"{out.name} exists")
out.write_text(s, encoding="utf-8", newline="\n")
print(f"  wrote {out.name} {hashlib.sha256(s.encode()).hexdigest()[:16]}   module {old_sha[:16]} -> {new_sha[:16]}")
