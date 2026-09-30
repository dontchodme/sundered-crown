"""Assemble the v113 doc with stage 6: the header, the link table, §0's stage-6 pointers, a new §5 (5, 5a-5g) and
a new §6. Reads the pre-stage-6 doc (s6/doc.pre6.md, 6b6c6289c97a8d3d) and the drafts; writes the repo doc, LF."""
import hashlib, pathlib, re
S = pathlib.Path(__file__).parent
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v113/thornwake-bramblesnare-build-v113.md")
pre = (S / "doc.pre6.md").read_bytes().decode("utf-8")
assert hashlib.sha256(pre.encode()).hexdigest()[:16] == "6b6c6289c97a8d3d"
assert "\r" not in pre
d = pre
subs = {k: (S / f).read_text(encoding="utf-8") for k, f in (("S5", "doc_s5.md"), ("S5E", "doc_s5e.md"),
                                                          ("S5F", "doc_s5f.md"), ("S5G6", "doc_s5g_s6.md"),
                                                          ("HEAD", "doc_head.md"), ("VALS", "doc_vals.txt"))}
vals = dict(l.split("=", 1) for l in subs["VALS"].splitlines() if "=" in l)


def one(a, b):
    global d
    assert d.count(a) == 1, a[:120]
    d = d.replace(a, b, 1)


# 0. the review round's note is now history
one("**Revised 2026-09-30 after the adversarial review. Only this doc changed**",
    "**Revised 2026-09-30 after the adversarial review, before stage 6. That round only this doc changed**")
# 1. the title line
t_end = d.find("\n")
one(d[:t_end], subs["HEAD"].split("\n", 1)[0])
# 2. the stage-6 paragraph after the review's revision note
one("controls.\n\n```\nsc-tendril-t3.html", "controls.\n\n" + subs["HEAD"].split("\n", 1)[1].strip("\n") + "\n\n```\nsc-tendril-t3.html")
# 3. the link table
one("  -> sc-thornwake-b26.5.html  stage 5  the blade, 31.35 -> 26.5: nearest 50% both sides (Rick's ruling)  fd5031063ecb6807   THE FINAL LINK\n```",
    "  -> sc-thornwake-b26.5.html  stage 5  the blade, 31.35 -> 26.5: nearest 50% both sides (Rick's ruling)  fd5031063ecb6807   THE FINAL LINK\n"
    "    -> sc-thornwake-b26.5-fx.html  stage 6  the picture and the voice (presentation; §5)           d306822d6914c08c   THE FX LINK\n```")
# 4. the paragraph under the table
one("byte-identical** from the bare base with the final builder (`runs/rebuild_final.txt`), and no",
    "byte-identical** from the bare base with the final builder (`runs/stage6_rebuild.txt`, the fx link among them;\n"
    "stages 1-5 before it: `runs/rebuild_final.txt`), and no")
one("carry) is the batch's stage 6 (§5), and **there is no stage 4** (the brief has two mechanism stages).",
    "carry) is the batch's stage 6 (§5, built), and **there is no stage 4** (the brief has two mechanism stages).")
one("**The carry, dry** (`runs/carry_dry.txt`): stages 1, 2, 3 and 5 apply",
    "**The carry, dry** (`runs/carry_dry.txt`; with stage 6, `runs/stage6_carry_dry.txt`, §5): stages 1, 2, 3 and 5 apply")
# 5. §0's pointers
one("  - **the presentation, kept by stages 1-5 and stage 6's to retire or keep** (nothing in the simulation reads",
    "  - **the presentation, kept by stages 1-5 and retired or kept by stage 6 (§5)** (nothing in the simulation reads")
one("  16. **What stays for stage 6** (above).",
    "  16. **What stayed for stage 6** (above); stage 6 retires the freeze's art and voice and keeps the charge sigil\n"
    "      and the banner's letters. Readings 17-22 are stage 6's (§5).")
one("  refuse for their reason; the unmodified copy builds stage 2's link byte-identical\n  (`runs/builder_negatives.txt`).",
    "  refuse for their reason; the unmodified copy builds stage 2's link byte-identical\n  (`runs/builder_negatives.txt`; "
    "re-run on the stage-6 builder, `runs/stage6_builder_negatives_s1to5.txt`). Stage 6's own\n  scan is §5e.")
one("## 1. Stages 1-3, and stage 5\n", "## 1. Stages 1-3, and stage 5 (stage 6: §5)\n")
# 6. §5 and §6
i5, i6 = d.find("## 5. Stage 6 next:"), d.find("## 6. What is left, and whose")
assert 0 < i5 < i6
d = d[:i5] + subs["S5"].replace("%%S5E%%", subs["S5E"].strip("\n") + "\n\n" + subs["S5F"].strip("\n")).rstrip("\n") \
    + "\n\n" + subs["S5G6"].strip("\n") + "\n"
for k, v in vals.items():
    d = d.replace("%%" + k + "%%", v)
left = re.findall(r"%%[A-Z0-9_]+%%", d)
assert not left, left
DOC.write_bytes(d.encode("utf-8"))
print(DOC.name, len(d.encode()), "bytes", hashlib.sha256(d.encode()).hexdigest()[:16], d.count("\n"), "lines")
