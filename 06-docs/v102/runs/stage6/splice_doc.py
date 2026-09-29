"""Splice stage 6 into 06-docs/v102/lodestone-rebuttal-build-v102.md: the header line, the links block,
the builder sentence, a pointer in §3, §5 (replaced: 'Stage 6 (next)' -> the build), §6 (replaced).
Refuses to run twice. Keeps a copy of the doc before the splice in s6/doc_before_splice.md."""
import pathlib, re, shutil
S = pathlib.Path(__file__).resolve().parent
D = pathlib.Path("C:/dev/sundered-crown/06-docs/v102/lodestone-rebuttal-build-v102.md")
s = D.read_text(encoding="utf-8")
assert "\r\n" not in s
if "## 5. Stage 6: the picture and the voice" in s:
    raise SystemExit("already spliced")
shutil.copy(D, S / "doc_before_splice.md")

def one(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new, 1)

# the header line
first = s.split("\n", 1)[0]
assert first.startswith("# v102 — LODESTONE / REBUTTAL, BUILD. STAGES 0-5 DONE, IN SCRATCH:")
new_first = first.replace("STAGES 0-5 DONE, IN SCRATCH:", "STAGES 0-6 DONE, IN SCRATCH:", 1)
assert new_first.endswith("Carry onto the chain and stage 6 (picture, voice) next.")
new_first = new_first[: -len("Carry onto the chain and stage 6 (picture, voice) next.")] + (
    "**Stage 6, the picture and the voice, is `sc-lodestone-b205-fx`** (§5): twelve rows byte-exact to the "
    "two labs' files. engine_ab over all 39 relics, Lodestone included, is 4446/4446 identical. The probe "
    "is 12/12, with two new checks ([10] the voice, [11] the picture) and five mutants each failing only "
    "its own. render_ab is 24/24 (the Lodestone control 0/6); chain_audit 20/20. There is no fx.js field: "
    "the rune motes are drawn. The clip is `07-shorts/v102/rebuttal-window.mp4`. Carry onto the chain next.")
one(first + "\n", new_first + "\n")

# the links block
one("""  -> sc-lodestone-b205.html      stage 5  the blade, 23.5 -> 20.5                  6d736451a1ffc2df
""", """  -> sc-lodestone-b205.html      stage 5  the blade, 23.5 -> 20.5                  6d736451a1ffc2df
  -> sc-lodestone-b205-fx.html   stage 6  the picture and the voice (§5)            7a095b143d66fbdb
""")

# the builder sentence
one("""Every link rebuilds byte-identical from the builder (`tools/lodestone_build.py`, sha256[:16]
`0731db270893647b`; `runs/build_s*.txt`).""",
"""Every link rebuilds byte-identical from the builder (`tools/lodestone_build.py`, sha256[:16]
`c74cd4a4508bfcf5` since stage 6, `0731db270893647b` before it; stages 1-5 are the same bytes from
both; `runs/build_s*.txt`, `runs/stage6/builder_checks.txt`).""")

# §3: a pointer to stage 6's checks
one("""[9] "the next cast does not wait": no cast while the walls are lit; no cast held back (the charge never left at or over ult.charge)
```
""", """[9] "the next cast does not wait": no cast while the walls are lit; no cast held back (the charge never left at or over ult.charge)
```

Stage 6 adds two checks, [10] the voice and [11] the picture. Each switches itself on from the page, so
the same probe still reads [0]-[9] alone on stages 2, 3 and 5 (§5d).
""")

# §5 and §6
i5 = s.index("## 5. Stage 6 (next)\n")
i6 = s.index("## 6. What is left, and whose\n")
sec5 = "".join((S / f).read_text(encoding="utf-8") for f in ("doc_s6_a.md", "doc_s6_d.md", "doc_s6_e.md"))
sec6 = (S / "doc_s6_left.md").read_text(encoding="utf-8")
assert "{{" not in sec5 + sec6, "unfilled placeholder"
tail = s[i6:]
# §6 runs to the end of the doc
s = s[:i5] + sec5.rstrip("\n") + "\n\n" + sec6.rstrip("\n") + "\n"
assert tail.count("## ") == 1, "something after §6"
D.write_text(s, encoding="utf-8", newline="\n")
print("spliced:", len(s), "chars")
