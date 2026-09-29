"""Assemble v110's build doc with stage 6: from the stage-5 doc (s6/doc.pre-s6.md, ec341c72c2a403b7), exact-once
edits to the header and §0-§1, §5 and §6 replaced by s6/doc_s5.md and s6/doc_s6.md with their placeholders filled
from s6/doc_vals.json. `--dry` writes s6/doc_test.md instead of the repo's doc."""
import hashlib, json, pathlib, re, sys
S6 = pathlib.Path(__file__).resolve().parent
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v110/aureole-benediction-build-v110.md")
src = (S6 / "doc.pre-s6.md").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest()[:16] == "ec341c72c2a403b7"
V = json.loads((S6 / "doc_vals.json").read_text(encoding="utf-8"))
s5 = (S6 / "doc_s5.md").read_text(encoding="utf-8")
s6 = (S6 / "doc_s6.md").read_text(encoding="utf-8")
for k, v in V.items():
    s5 = s5.replace("«" + k + "»", v)
    s6 = s6.replace("«" + k + "»", v)
assert "«" not in s5 + s6, re.findall(r"«[A-Z0-9_]+»", s5 + s6)

HEAD = ("# v110 — AUREOLE / BENEDICTION (REDESIGN), BUILD. STAGES 1-6 DONE, IN SCRATCH: stage 1 is arm A to the fight; "
        "the halo is the lab's mechanism, on the engine's window clock (measured); the blade to the design's target, the "
        "shipped rate: 12.5 (56.1% both sides, against the shipped 54.1%); the 50% alternative is 11.5 (48.8%). **Stage 6, "
        "the picture and the voice, is built (`sc-aureole-b12.5-fx`, §5):** thirteen rows byte-exact to the two labs'; a "
        "ring of light at the halo's own radius under both balls, brightening while a foe is inside, a rim on the foe, "
        "motes drifting in, SMITE and BLESSING once a stretch; a choir swell at the cast (C4 and G4, re-struck), a bright "
        "C6 note as a foe comes inside, the spark collect a blessing, the swell reversed at a clock close (none on a "
        "death); the beam's art out, and no `fx.js` field (the motes are drawn). engine_ab 4218/4218 with Aureole in; "
        f"the probe {V['PROBE_OK']}, its two new checks (the voices, the picture's hook, 74 fights drawn) each failed by "
        "its own mutants; render_ab 24/24 with a control at 0/6; chain_audit 21/21 with a control; compose6 0 FAIL up to "
        "`sc-censer-fxout`. The clip is with Rick. The beam's `fx.js` spec is the orchestrator's to take out at the carry. "
        "Review round 2026-09-29: chain_audit now watches the blade (9 of 9 inserts at stage 5); every link unchanged.\n")
lines = src.split("\n", 1)
assert lines[0].startswith("# v110 — AUREOLE / BENEDICTION (REDESIGN), BUILD. STAGES 1-5 DONE")
doc = HEAD + lines[1]

reps = [
 ("Builder `tools/aureole_build.py`, probe `tools/aureole_probe.py`, runs in `runs/`.",
  "Builder `tools/aureole_build.py` (7cf0a20f6b53a2c3; stages 1-5's was c7641c026661b686), probe\n"
  "`tools/aureole_probe.py` (fc096aca9624bb99; stages 1-5's was afa389b746f9c12b), runs in `runs/` (stage 6's are\n"
  "`runs/stage6_*`)."),
 ("  -> sc-aureole-b12.5.html    stage 5  the blade 16.01 -> 12.5, to the shipped rate         21ea91d0f3c14274   THE FINAL LINK\n",
  "  -> sc-aureole-b12.5.html    stage 5  the blade 16.01 -> 12.5, to the shipped rate         21ea91d0f3c14274\n"
  "       -> sc-aureole-b12.5-fx.html   stage 6  the picture and the voice (presentation)   f3228d8d1509edbb   THE FINAL LINK\n"),
 ("stage 4 (v100's numbering).\n",
  "stage 4 (v100's numbering). In §2-§4, written at stage 5, \"the final link\" is `sc-aureole-b12.5`; stage 6 is\n"
  "presentation and moves no fight (engine_ab 4218/4218 with Aureole in, §5e), so every number there holds for the\n"
  "fx link.\n"),
 ("(`runs/build_fixround.txt`). The builder refuses to overwrite a link, a stage on the wrong stage, a\n"
  "second stage 1, a name outside `sc-aureole*`, a name 02-chain already has, and a base without\n"
  "Tendril's ticker.\n",
  "(`runs/build_fixround.txt`). The builder refuses to overwrite a link, a stage on the wrong stage, a\n"
  "second stage 1, a name outside `sc-aureole*`, a name 02-chain already has, and a base without\n"
  "Tendril's ticker. **With stage 6** the builder is 7cf0a20f6b53a2c3: it rebuilds all six links from the base\n"
  "byte for byte, the five above unchanged, and refuses stage 6 twice, on Rick's 50% link, on any stage but 5 and\n"
  "on the base (`runs/stage6_builder_checks.txt`, §5e).\n"),
 ("  - **presentation, kept by stages 1-5 and the brief's stage 4's to retire** (link stage 6; nothing in\n"
  "    the simulation reads any of it):",
  "  - **presentation, kept by stages 1-5 and retired by link stage 6** (§5; nothing in the simulation\n"
  "    reads any of it):"),
 ("`src/render/fx.js` still carries the same entry (line 142); this build touches neither copy.",
  "`src/render/fx.js` still carries the same entry (line 142 then; 136-139 today, Censer's burst out); this build\n"
  "    touches neither copy, and the orchestrator's `fx_remove.py` takes it out at the carry (§5b)."),
 ("  13. **The beam is out** at stage 1 (brief stage 1): the block and the heal; its picture, voice and\n"
  "      field spec are stage 6's (above).",
  "  13. **The beam is out** at stage 1 (brief stage 1): the block and the heal; its picture and voice are\n"
  "      retired and replaced at stage 6 (§5, readings 14-20), and its field spec is the orchestrator's (§5b)."),
 ("character. Stage 5 is the blade.\n", "character. Stage 5 is the blade. Stage 6 is the picture and the voice (§5).\n"),
]
for a, b in reps:
    assert doc.count(a) == 1, (doc.count(a), a[:80])
    doc = doc.replace(a, b, 1)
i = doc.find("## 5. Stage 6 next: the picture, the voice, the beam's field spec out")
assert i > 0 and doc.count("## 6. What is left, and whose") == 1
doc = doc[:i] + s5.rstrip("\n") + "\n\n" + s6.rstrip("\n") + "\n"
assert "\r" not in doc
out = S6 / "doc_test.md" if "--dry" in sys.argv else DOC
out.write_text(doc, encoding="utf-8", newline="\n")
print(f"wrote {out}  {hashlib.sha256(doc.encode()).hexdigest()[:16]}  {len(doc.encode())} bytes, {doc.count(chr(10))} lines")
