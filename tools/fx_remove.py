"""TAKE ONE RETIRED ULT'S PARTICLE FIELD OUT OF BOTH COPIES OF fx.js -- the batch orchestrator's
`sync_fx_remove`, for a redesign whose builder was built in scratch and so could not touch the shared
`src/render/fx.js` (v108 onward).

    python fx_remove.py --relic ironhail --src ../02-chain/<tip>.html --out ../02-chain/<new>.html

It is dawn_build.py's `sync_fx_remove` (v97), lifted out of the builder:
  - the spec is the entry `<relic>: { ... },` in SPECS, with the one comment directly above it
    (never a section header like `/* ---- NOVAS ... */`, which heads a group of entries);
  - it must be exactly once in src/render/fx.js AND in the inlined copy, and the inlined copy (header
    to THE ULT FIELDS) must equal src/render/fx.js before anything is written;
  - both stamps are re-cut (the full sha256 and its 16-char prefix, wherever the page prints them);
  - the inlined copy must equal the new fx.js after the write, and NOTHING ELSE in the page moves
    (the page with the block and the stamps put back is the source, byte for byte);
  - a link is written once; src/render/fx.js is written last, only after the page is on disk.
It adds nothing: whatever the redesign draws instead is drawn by its own builder's stage 6.
"""
import argparse, difflib, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
FX_JS = HERE.parent / "src" / "render" / "fx.js"
PROTECTED = "sundered-crown-v43.html"
HEAD = re.compile(r"/\* ---- src/render/fx\.js, inlined by fx_build\.py\. sha256:([0-9a-f]{64}) ---- \*/\n")
TAIL = re.compile(r"/\* -+ THE ULT FIELDS -+")


def inlined(s):
    h = HEAD.search(s)
    if not h:
        raise SystemExit("no inlined fx.js header in this build")
    t = TAIL.search(s, h.end())
    return h, s[h.end():t.start()].rstrip("\n")


def spec_block(mod, relic, keep_comment=False):
    """The SPECS entry for `relic`, with the comment directly above it (unless keep_comment), as
    whole lines."""
    key = re.escape(relic)
    m = re.search(r"(?m)^( *)(?:" + key + r"|'" + key + r"'): \{", mod)
    if not m:
        raise SystemExit(f"no SPECS entry for {relic!r} in src/render/fx.js")
    if len(re.findall(r"(?m)^ *(?:" + key + r"|'" + key + r"'): \{", mod)) != 1:
        raise SystemExit(f"{relic!r} opens more than one entry in src/render/fx.js")
    start = m.start()
    end = mod.index("},\n", m.end()) + 3
    if "{" in mod[m.end():end - 3]:
        raise SystemExit(f"{relic!r}'s entry nests a brace -- read it by hand")
    # the comment directly above, if the line before the entry closes one -- but never a SECTION
    # HEADER (`/* ---- NOVAS: ... ---- */`): that heads a group of entries, not this one (v106: it
    # sits over Widowmaker, Lightkeeper and Censer, and goes with none of them)
    before = mod[:start]
    if not keep_comment and before.rstrip(" ").endswith("*/\n"):
        c = before.rfind("/*")
        line0 = before.rfind("\n", 0, c) + 1
        if (before[line0:c].strip() == "" and "*/" not in before[c:-4]
                and not re.match(r"/\* -{2,}", before[c:])):
            start = line0
    return mod[start:end]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--relic", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry", action="store_true", help="check everything, write nothing")
    ap.add_argument("--keep-comment", action="store_true",
                    help="remove the entry's lines only and leave the comment above it (v110: Aureole's comment states a rule the beams below it still follow)")
    ap.add_argument("--fxjs", default=None,
                    help="a COPY of fx.js to read and rewrite instead of src/render/fx.js (tests in "
                         "scratch: a scratch link built on an older tip carries an older fx.js)")
    A = ap.parse_args()
    fx_js = pathlib.Path(A.fxjs).resolve() if A.fxjs else FX_JS
    if A.fxjs and fx_js == FX_JS.resolve():
        raise SystemExit("--fxjs is for a copy; leave it off to use src/render/fx.js")
    src_p, out_p = (HERE / A.src).resolve(), (HERE / A.out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is written once")
    s0 = src_p.read_text(encoding="utf-8")
    mod = fx_js.read_text(encoding="utf-8")
    print(f"\nFX REMOVE -- {A.relic}'s particle field out of both copies")
    print(f"  src {src_p.name}  {hashlib.sha256(s0.encode()).hexdigest()[:16]}")

    h, body = inlined(s0)
    if body != mod.rstrip():
        raise SystemExit("src/render/fx.js and the inlined copy have DIVERGED before this tool "
                         "wrote anything (a rebuild? restore fx.js: git checkout -- src/render/fx.js)")
    old_sha = h.group(1)
    if hashlib.sha256(mod.encode("utf-8")).hexdigest() != old_sha:
        raise SystemExit("the page's fx.js stamp is not src/render/fx.js's sha256")
    blk = spec_block(mod, A.relic, A.keep_comment)
    if mod.count(blk) != 1 or s0.count(blk) != 1:
        raise SystemExit(f"{A.relic}'s spec is not exactly once in both copies")
    print("  the block, removed whole:")
    for ln in blk.rstrip("\n").split("\n"):
        print("    | " + ln)

    mod2 = mod.replace(blk, "", 1)
    new_sha = hashlib.sha256(mod2.encode("utf-8")).hexdigest()
    s = s0.replace(blk, "", 1)
    n_full, n_short = s.count(old_sha), s.count(old_sha[:16]) - s.count(old_sha)
    s = s.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
    if inlined(s)[1] != mod2.rstrip():
        raise SystemExit("the inlined copy and the new fx.js DIVERGED across this tool's own write")
    gone, came = [], []
    for op in difflib.unified_diff(s0.split("\n"), s.split("\n"), n=0, lineterm=""):
        if op.startswith(("---", "+++", "@@")):
            continue
        (gone if op[0] == "-" else came).append(op[1:])
    stamp_old = [ln for ln in gone if old_sha[:16] in ln]
    if ([ln for ln in gone if old_sha[:16] not in ln] != blk.rstrip("\n").split("\n")
            or [ln.replace(old_sha, new_sha).replace(old_sha[:16], new_sha[:16])
                for ln in stamp_old] != came):
        raise SystemExit("REFUSING TO WRITE -- the page moved somewhere other than the block and "
                         "the stamps")
    if re.search(r"(?m)^ *(?:" + re.escape(A.relic) + r"|'" + re.escape(A.relic) + r"'): \{ mode:", s):
        raise SystemExit(f"REFUSING TO WRITE -- a {A.relic} field spec is still in the page")
    print(f"  ok    only the block and {n_full} full + {n_short} short stamp(s) moved; "
          f"stamp {old_sha[:16]} -> {new_sha[:16]}")

    if A.dry:
        print(f"  DRY   would write {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]} "
              f"and src/render/fx.js  {new_sha[:16]}")
        return 0
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"  wrote {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}")
    fx_js.write_text(mod2, encoding="utf-8", newline="\n")
    print(f"  wrote {'src/render/fx.js' if fx_js == FX_JS else fx_js}  {new_sha[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
