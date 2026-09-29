"""Assemble v109's doc with stage 6: from the backup (doc.pre-s6.md, bacf75e1c198a71e) + doc_s5.md + doc_s6.md + the gates.

    python assemble_doc.py [--out <path>]   (default: the repo doc; --out a scratch file for a dry run)

Every edit is an exactly-once replacement of the backup's own text; it refuses otherwise.
"""
import hashlib, pathlib, sys

S6 = pathlib.Path(__file__).resolve().parent
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v109/censer-consecration-build-v109.md")
out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else DOC
src = (S6 / "doc.pre-s6.md").read_text(encoding="utf-8")
assert hashlib.sha256(src.encode()).hexdigest()[:16] == "bacf75e1c198a71e", "the backup moved"
V = dict(line.split("=", 1) for line in (S6 / "doc_vals.txt").read_text(encoding="utf-8").splitlines() if "=" in line)
s5 = (S6 / "doc_s5.md").read_text(encoding="utf-8")
s6 = (S6 / "doc_s6.md").read_text(encoding="utf-8")
gates = (S6 / "doc_gates.md").read_text(encoding="utf-8").rstrip("\n")
s5 = s5.replace("«GATES»", gates).replace("«PROBE_SHA»", V["PROBE_SHA"])
assert "«" not in s5 and "«" not in s6, "a placeholder is left"


def one(t, a, b):
    assert t.count(a) == 1, (t.count(a), a[:80])
    return t.replace(a, b, 1)


t = src
head = t.split("\n", 1)[0]
assert head.startswith("# v109 — CENSER / CONSECRATION (REDESIGN), BUILD. STAGES 0-5 DONE")
t = one(t, head, V["HEAD"])
t = one(t, "`tools/censer_build.py` (78501578c5773570), probe `tools/censer_probe.py` (5d78670c3787524e), runs in `runs/`.",
        f"`tools/censer_build.py` ({V['BUILDER_SHA']}; stages 1-5's was 78501578c5773570), probe `tools/censer_probe.py`\n"
        f"({V['PROBE_SHA']}; stages 1-5's was 5d78670c3787524e), runs in `runs/` (stage 6's are `runs/stage6_*`).")
t = one(t, "  -> sc-censer-consecration-b25.5.html       stage 5  the blade, 28.77 -> 25.5 (the shipped rate)          56c49ad3f0ccb3aa\n",
        "  -> sc-censer-consecration-b25.5.html       stage 5  the blade, 28.77 -> 25.5 (the shipped rate)          56c49ad3f0ccb3aa\n"
        "  -> sc-censer-consecration-b25.5-fx.html    stage 6  the picture and the voice (presentation)             3d68c7648a9cb3a8\n")
t = one(t, "`engine_ab`. Every link above rebuilds byte-identical from the final builder (re-checked on resume, and in\n"
           "`runs/compose2.txt`), and no `sc-censer*` name is on `02-chain/`.",
        "`engine_ab`. Every link above rebuilds byte-identical from the final builder (re-checked on resume, in\n"
        "`runs/compose2.txt`, and with the stage-6 link in `runs/stage6_builder_checks.txt` and\n"
        "`runs/stage6_compose6.txt`), and no `sc-censer*` name is on `02-chain/`.")
t = one(t, "for no other relic\" and builds (§0, what is retired).\n",
        "for no other relic\" and builds (§0, what is retired). compose2 ran on the stages 1-5 builder (78501578c5773570);\n"
        "the final one writes the same four links byte for byte, and **compose6** (§5, 0 FAIL) runs stages 1, 2, 3, 5 and\n"
        "6 with the three builders in progress since (Aureole, Heartwood, Spellbreaker), both ways and in two stacks, and\n"
        "on the line's four newest tips up to `sc-lightkeeper-fxout` (088189f3517b6f11): stages 1-5 make the change set\n"
        "98dc422a898f5043 on every one, and stage 6 alone bc494860e7c77ee9 on every one.\n")
t = one(t, "  5. **The ground is its caster's**: a disc carries its side, and only its own caster's window reads it (the\n"
           "     lab had one caster; in a mirror match each Censer smites on and is healed by its own ground).\n",
        "  5. **The ground is its caster's**: a disc carries its side, which names its caster for the purge (its\n"
        "     `groundLife`) and for the probe, and only its own caster's window reads it (the lab had one caster).\n"
        "     There is no mirror match: `Match` refuses a relic against itself, so no test can tell this side test\n"
        "     from none (the stage-5 review's mutant mx4-side behaves identically in every legal match).\n")
t = one(t, "reads who is still a nova and never refuses on it). **The nova's presentation keyed on the id stays until\n"
           "  stage 6**, where design §5 retires it (\"nova's field spec out\"):",
        "reads who is still a nova and never refuses on it). **The nova's presentation keyed on the id is retired at\n"
        "  stage 6** (§5), as design §5 asks (\"nova's field spec out\"):")
t = one(t, "(the glyph ring and the smoke, now drawn for the cast record's `life` 1.6 at the",
        "(the glyph ring and the smoke, drawn through stage 5 for the cast record's `life` 1.6 at the")
t = one(t, "  fallback voice. Nothing in the simulation reads any of it (engine_ab, §4).",
        "  fallback voice (Censer's own two arms now stand before it). Nothing in the simulation reads any of it\n"
        "  (engine_ab, §4 and §5e).")
t = one(t, "Every probe number in this doc is from the final probe (`censer_probe.py` 5d78670c3787524e) but the four\n"
           "lab-field runs,",
        "Every probe number in §0-§4 is from the stages 1-5 probe (`censer_probe.py` 5d78670c3787524e; stage 6's,\n"
        "c588b606b1fc7741, prints every one of its lines and counters alike on the final link: §5e) but the four\n"
        "lab-field runs,")
i5, i6 = t.index("\n## 5. Stage 6 (next)\n"), t.index("\n## 6. What is left, and whose\n")
t = t[:i5 + 1] + s5.rstrip("\n") + "\n\n" + s6.rstrip("\n") + "\n"
assert "\r" not in t
out.write_text(t, encoding="utf-8", newline="\n")
b = out.read_bytes()
print(f"wrote {out} {len(b)} bytes, {t.count(chr(10))} lines, sha16 {hashlib.sha256(b).hexdigest()[:16]}, CR {b.count(b'\r')}")
