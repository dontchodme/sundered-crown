"""v112 stage 6: two corrections after doc6_apply.py (which read the fix round's doc, 03a17a4e4769251d): the window's
match time is the window's hit stops (every blow's and the cast's), not only the roots'; and the clip was sent to
Rick. Patches the repo doc and S/doc_final.md in place (LF). SCRATCH."""
import hashlib, pathlib
S = pathlib.Path(__file__).resolve().parent.parent
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v112/heartwood-rootfast-build-v112.md")
d = DOC.read_text(encoding="utf-8")
assert d == (S / "doc_final.md").read_text(encoding="utf-8")
R = [("window 10.28s of match time (8 on the window clock; the rest is the root's hit stops)",
      "window 10.28s of match time (8 on the window clock; the rest is the window's hit stops)"),
     ("**Rick's to overrule.** Not yet sent to him (the batch's clips go\ntogether at his verification).",
      "**Rick's to overrule.** Sent to him 2026-09-30 (the session's file card), with\nthe two base artifacts named.")]
for a, b in R:
    assert d.count(a) == 1, a[:60]
    d = d.replace(a, b)
out = d.encode("utf-8")
DOC.write_bytes(out); (S / "doc_final.md").write_bytes(out)
print("doc", hashlib.sha256(out).hexdigest()[:16], len(out))
