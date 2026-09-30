"""v112 stage 6: the doc's edits. Reads the fix round's doc (03a17a4e4769251d; S/doc_final.md is its copy), applies the
stage-6 changes (header, intro, link table, shas, the review's note 4, §0, §4a, §5's title), replaces the old §6
("What is left") with the new §6 / §6a / §7 (s6/sec6.md with s6/gates6.md and s6/clip6.md filled in, and the
@@...@@ values from s6/fill.json) and §8 (s6/sec8.md), and writes the repo doc and S/doc_final.md (LF). SCRATCH.
    python doc6_apply.py"""
import hashlib, json, pathlib
S = pathlib.Path(__file__).resolve().parent.parent
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v112/heartwood-rootfast-build-v112.md")
src = (S / "doc_final.md").read_bytes()
assert hashlib.sha256(src).hexdigest()[:16] == "03a17a4e4769251d", "not the fix round's doc"
d = src.decode("utf-8")
assert "\r\n" not in d
import sys
DRY = "--dry" in sys.argv
F = json.loads((S / "s6" / ("fill_dry.json" if DRY else "fill.json")).read_text(encoding="utf-8"))


def rep(a, b):
    global d
    assert d.count(a) == 1, (d.count(a), a[:100])
    d = d.replace(a, b, 1)


# ---- the header
rep("# v112 — HEARTWOOD / ROOTFAST (REDESIGN), BUILD. STAGES 0-5 DONE, IN SCRATCH:",
    "# v112 — HEARTWOOD / ROOTFAST (REDESIGN), BUILD. STAGES 0-6 DONE, IN SCRATCH:")
rep(" Stage 6 (picture, voice, carry) is next, on `sc-heartwood-b11`.\n",
    " **Stage 6, the picture and the voice, is built (`sc-heartwood-b11-fx`, §6):** eleven rows byte-exact to the two "
    "labs'; the sword greens hilt to tip with a leaf scale at the cast, sheds leaf motes for the window and withers tip "
    "to hilt at the close; each root marks the held ball for Tendril's four shoots (drawn on the carry: this base has "
    "no Tendril picture, so here the held ball keeps Paradox's hexagon) and the ENTANGLE tag prints the root's count; a "
    "green creak (RISING) at the cast and Tendril's root voice, 4.1 dB quieter, on every rooted blow, and no close "
    "voice; the freeze's plate, cage and life entry retired, and no `fx.js` field (`SPECS.heartwood` is the "
    "orchestrator's `fx_remove` at the carry). engine_ab 4218/4218 with Heartwood in; " + F["HEAD_PROBE"] + "; render_ab "
    "24/24 with a control at 4/12 differing; chain_audit 20/20 with controls; tip_audit as the base; the builder's 49 "
    "stage-6 negatives refuse. The clip is with Rick (§7); the carry, `fx_remove` and `shell_identity` are the "
    "orchestrator's (§8).\n")
rep("the four links were deleted by hand and rebuilt byte-identical, and the probe, its mutants, the builder's\n"
    "negatives, `chain_audit` and the dry carry and compose were re-run.\n",
    "the four links were deleted by hand and rebuilt byte-identical, and the probe, its mutants, the builder's\n"
    "negatives, `chain_audit` and the dry carry and compose were re-run. **Stage 6 was integrated the same day**\n"
    "from the two stage-6 labs' row files (§6): built, gated and filmed, with nothing of stages 0-5 moved.\n")
# ---- the link table
rep("  -> sc-heartwood-b11.html         stage 5  the blade 12.65 -> 11, nearest 50% (the brief's stage 3)  aff84a04b303a402   THE FINAL LINK\n",
    "  -> sc-heartwood-b11.html         stage 5  the blade 12.65 -> 11, nearest 50% (the brief's stage 3)  aff84a04b303a402   the final ruleset\n"
    "  -> sc-heartwood-b11-fx.html      stage 6  the picture and the voice (the brief's stage 4)           ceba5e801f4cf91b   THE FINAL LINK\n")
rep("**Every link rebuilds byte-identical** from the bare base with the final builder (`runs/rebuild_final.txt`,\n"
    "builder sha256[:16] **4550a53a2b5ac4bf**, the fix round's; the four links themselves were deleted by hand and\n"
    "rebuilt by it with the same four shas, `runs/rebuild_fix.txt`), and no `sc-heartwood*` name is on `02-chain/`.\n"
    "The probe is `tools/heartwood_probe.py` sha256[:16] **9634f7a6c2d42cb1** (the fix round's, eight checks). The stage numbers are\n",
    "**Every link rebuilds byte-identical** from the bare base with the final builder (`runs/rebuild6.txt`, builder\n"
    f"sha256[:16] **{F['BUILDER']}**, stage 6's; the fix round's 4550a53a2b5ac4bf rebuilt the first four the same,\n"
    "`runs/rebuild_final.txt`, and the four links themselves were deleted by hand and rebuilt by it with the same four\n"
    "shas, `runs/rebuild_fix.txt`), and no `sc-heartwood*` name is on `02-chain/`. The probe is\n"
    f"`tools/heartwood_probe.py` sha256[:16] **{F['PROBE']}** (stage 6's: the fix round's eight checks, 9634f7a6c2d42cb1,\n"
    "and [9]-[10] for the voice and the picture). The stage numbers are\n")
rep("blade), and the brief's stage 4 (picture, voice, carry) is the batch's stage 6 (§5). **The carry, dry:**",
    "blade), and the brief's stage 4 (picture, voice, carry) is the batch's stage 6 (§5 its brief, §6 the build). **The carry, dry:**")
rep("holding the same lines (only the order of independent blocks differs).\n",
    "holding the same lines (only the order of independent blocks differs). **And with stage 6** (`runs/carry_compose6.txt`):\n"
    "stages 1-6 on `sc-tendril-fx` (-> b11 3c61fccb5366245a, -fx c4aacc10bd6a7c29), `sc-spellbreaker-fxout` (f51666c08b8f2d9b\n"
    "-> fc6895cca67c5096), `sc-aureole-fxout` (1a2743c8b8ebe33e -> b7071c0aff03fd10) and the newest link on the chain,\n"
    "`sc-thornwake-b26.5-fx` with Thornwake's redesign carried (5abbc99ce0067b6a -> 54ad747c117766d2), every anchor once,\n"
    "the root's shoots drawn on all four; and with Thornwake's and Goreshard's builders, each now carrying its own stage 6,\n"
    "both orders hold the same lines.\n")
# ---- the review's notes
rep("Kept, and kept flagged for Rick (§0, §6):", "Kept, and kept flagged for Rick (§0, §8):")
rep("   6's (§5). **`sc-heartwood-b11` must not become the build of record before stage 6 retires or replaces\n"
    "   them** (§6).\n",
    "   6's (§5). **`sc-heartwood-b11` must not become the build of record before stage 6 retires or replaces\n"
    "   them** (§8). **Stage 6 has (§6):** the plate, the cage and the life entry are gone and the cast has its own\n"
    "   voice; `SPECS.heartwood` is the orchestrator's `fx_remove` at the carry, and until then a cast on\n"
    "   `sc-heartwood-b11-fx` still sheds the freeze's leaf-fall.\n")
# ---- §0
rep("  - **the presentation, kept by stages 1-5 and stage 6's to retire or keep** (nothing in the simulation reads",
    "  - **the presentation, kept by stages 1-5 and retired or kept by stage 6 (§6)** (nothing in the simulation reads")
rep("`u.w === \"heartwood\"` — the freeze's picture, which STILL PLAYS AT EVERY CAST on these links, spreading",
    "`u.w === \"heartwood\"` — the freeze's picture, which PLAYS AT EVERY CAST on the stage 1-5 links, spreading")
rep("  13. **What stays for stage 6** (above).\n",
    "  13. **What stays for stage 6** (above): stage 6 retires the plate, the cage and the life entry and voices the\n"
    "      cast (§6; the builder's readings 14-22); the sigil stays; `SPECS.heartwood` is the orchestrator's.\n")
# ---- §4a
rep("- **Not run here, and stage 6's** (the brief's stage 4): `shell_identity`, `render_ab` and the watched fight\n"
    "  (Electron waits while Rick is on this PC; the batch's load limit).\n",
    "- **Not run here, and stage 6's** (the brief's stage 4): `shell_identity`, `render_ab` and the watched fight\n"
    "  (Electron waits while Rick is on this PC; the batch's load limit). **Stage 6 ran `render_ab` (§6a) and the\n"
    "  watched fight (the clip, §7); `shell_identity` is the orchestrator's** (the app's json is shared).\n")
# ---- §5
rep("## 5. Stage 6 next: the picture, the voice, the carry (the brief's stage 4) — on `sc-heartwood-b11`\n\n",
    "## 5. Stage 6's brief, and the state it read (the brief's stage 4) — on `sc-heartwood-b11`\n\n"
    "*Written before stage 6 as its brief, and kept as the record of what the two labs read. Stage 6 is built in §6.*\n\n")
# ---- the old §6 out; §6, §6a, §7, §8 in
i = d.index("## 6. What is left, and whose\n")
sec6 = (S / "s6" / "sec6.md").read_text(encoding="utf-8")
sec6 = sec6.replace("@@GATES6@@", (S / "s6" / "gates6.md").read_text(encoding="utf-8").rstrip("\n"))
sec6 = sec6.replace("@@CLIP6@@", (S / "s6" / "clip6.md").read_text(encoding="utf-8").rstrip("\n"))
for k, v in F.items():
    sec6 = sec6.replace(f"@@{k}@@", v)
assert "@@" not in sec6, [ln for ln in sec6.splitlines() if "@@" in ln][:3]
d = d[:i] + sec6.rstrip("\n") + "\n\n" + (S / "s6" / "sec8.md").read_text(encoding="utf-8")
assert "@@" not in d
out = d.encode("utf-8")
if DRY:
    (S / "tmp" / "doc_dry.md").write_bytes(out)
else:
    DOC.write_bytes(out)
    (S / "doc_final.md").write_bytes(out)
print("doc written", hashlib.sha256(out).hexdigest()[:16], len(out), "bytes")
