"""v112 stage 6: the carry, dry, also onto sc-thornwake-fxout (the orchestrator put it on 02-chain after
Thornwake's carry, while this build closed): the doc's three mentions of the carried Thornwake tip. SCRATCH."""
import hashlib, pathlib
S = pathlib.Path(__file__).resolve().parent.parent
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v112/heartwood-rootfast-build-v112.md")
d = DOC.read_text(encoding="utf-8")
assert d == (S / "doc_final.md").read_text(encoding="utf-8")
R = [("`sc-thornwake-b26.5-fx` with Thornwake's redesign carried (5abbc99ce0067b6a -> 54ad747c117766d2), every anchor once,\n"
      "the root's shoots drawn on all four;",
      "`sc-thornwake-b26.5-fx` with Thornwake's redesign carried (5abbc99ce0067b6a -> 54ad747c117766d2) and its fx-out,\n"
      "`sc-thornwake-fxout` (5841a505d58390a5 -> 5cc323540b8ad132), every anchor once, the root's shoots drawn on all five;"),
     ("and `sc-thornwake-b26.5-fx` (Thornwake's redesign, carried onto the chain at 10:23 today) each print",
      "and `sc-thornwake-b26.5-fx` / `sc-thornwake-fxout` (Thornwake's redesign, carried onto the chain today) each print"),
     ("    `sc-thornwake-b26.5-fx` with Thornwake's redesign carried, the shoots drawn on all four;",
      "    `sc-thornwake-b26.5-fx` / `sc-thornwake-fxout` with Thornwake's redesign carried, the shoots drawn on all five;")]
for a, b in R:
    assert d.count(a) == 1, a[:70]
    d = d.replace(a, b)
out = d.encode("utf-8")
DOC.write_bytes(out); (S / "doc_final.md").write_bytes(out)
print("doc", hashlib.sha256(out).hexdigest()[:16], len(out))
