#!/usr/bin/env python
"""THE STAFF ROW'S BUILDER KIT -- what every staff builder after Culverin shares. v89.

`culverin_build.py` wrote these helpers first and keeps its own copies (it is
committed and gated; it is not refactored under itself). Briarwand onward
import them from here, so the next six builders carry only their own edits.

    one(src, old, new, label)      replace exactly one occurrence, or refuse
    strip_comments(js)             block and line comments out, for checks
    syntax_check(html, label)      `node --check` every inline script
    relic_entry(code, rid)         a WEAPONS entry, comments stripped
    fnum(v) / shot_js(S)           numbers and a shot block, as the page writes them
    check_bow_body(code)           v89 §1: a staff's physics are Ironhail's, read off the page
    check_no_rng(edits)            no ADDED line draws the match rng
    write_link(...)                stamp, syntax-check, write LF, print the sha
    audit(stages, tip)             every added line of every stage is in the tip
"""
from __future__ import annotations
import hashlib, pathlib, re, shutil, subprocess, tempfile

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# v89 §1: the staff's physics are the bow's EXACTLY.
BODY = dict(blades="[0]", reach=54, width=9, artW=44, spin=2.8, mode='"ranged"', mass=1.6)


def one(src: str, old: str, new: str, label: str) -> str:
    """Replace exactly one occurrence, or refuse."""
    d_old = old.count("/*") - old.count("*/")
    d_new = new.count("/*") - new.count("*/")
    if d_old != d_new:
        raise SystemExit(f"BLOCK {label}: comment balance moves {d_old:+d} -> "
                         f"{d_new:+d}. The page will not parse.")
    n = src.count(old)
    if n != 1:
        raise SystemExit(
            f"ANCHOR {label}: expected exactly 1 occurrence, found {n}.\n"
            f"  The source has moved under this builder. Do not weaken the\n"
            f"  anchor -- find out what changed.\n"
            f"  anchor head: {old.splitlines()[0][:90]!r}")
    print(f"  ok    {label}")
    return src.replace(old, new, 1)


def strip_comments(js: str) -> str:
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    return re.sub(r"//[^\n]*", "", js)


def syntax_check(html: str, label: str) -> None:
    """Parse the page's own script the way a browser will (CLAUDE.md 4.11)."""
    node = shutil.which("node")
    if not node:
        raise SystemExit("no `node` on PATH -- refusing to write an unchecked build")
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html)
    if not blocks:
        raise SystemExit("no inline <script> found in the output")
    with tempfile.TemporaryDirectory() as d:
        for i, b in enumerate(blocks):
            f = pathlib.Path(d) / f"b{i}.js"
            f.write_text(b, encoding="utf-8")
            r = subprocess.run([node, "--check", str(f)], capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(f"REFUSING TO WRITE -- {label} does not parse.\n  "
                                 + "\n  ".join((r.stderr or "").strip().splitlines()[:12]))
    print(f"  ok    syntax  {len(blocks)} inline script block(s) parse")


def relic_entry(code: str, rid: str) -> str:
    m = re.search(r'\{ id:"' + rid + r'"[\s\S]*?blurb:"[^"]*" \}', code)
    if not m:
        raise SystemExit(f"no WEAPONS entry for {rid!r}")
    return m.group(0)


def fnum(v) -> str:
    """A number as the page writes it -- and a boolean as JS writes one (Crozier's
    `pierce: true`; `str(True)` would put a Python name into the page)."""
    if isinstance(v, bool):
        return "true" if v else "false"
    return repr(v) if isinstance(v, float) else str(v)


def shot_js(S: dict) -> str:
    """A shot block as the page writes it; strings (the spell's name) quoted."""
    keys = [k for k in S if k != "tip"]
    parts = [f'{k}:"{S[k]}"' if isinstance(S[k], str) else f"{k}:{fnum(S[k])}" for k in keys]
    return "shot:{ " + ", ".join(parts) + f',\n           tip:"{S["tip"]}" }},'


def check_bow_body(code: str) -> None:
    """v89 §1: the staff's physics are the bow's EXACTLY -- read off Ironhail."""
    ih = relic_entry(code, "ironhail")
    for k, v in BODY.items():
        if not re.search(rf"\b{k}:\s*{re.escape(str(v))}(?=[,\s}}])", ih):
            raise SystemExit(f"REFUSING TO WRITE -- Ironhail's {k} is not {v}; "
                             "the bow's physics moved under this builder")
    print("  ok    body  the bow's physics, read off Ironhail")


def check_entry(code: str, rid: str, shot: dict, dmg, stubbed: bool) -> str:
    """The relic's own entry carries the body, the shot and the blade this run wrote."""
    ent = relic_entry(code, rid)
    for k, v in BODY.items():
        if not re.search(rf"\b{k}:\s*{re.escape(str(v))}(?=[,\s}}])", ent):
            raise SystemExit(f"REFUSING TO WRITE -- {rid}'s {k} is not {v}")
    m = re.search(r"shot:\{([^}]*)\}", ent).group(1)
    for k, v in shot.items():
        if k == "tip":
            continue
        pat = rf'\b{k}:"{re.escape(v)}"' if isinstance(v, str) else rf"\b{k}:{re.escape(fnum(v))}(?=[,\s])"
        if not re.search(pat, m):
            raise SystemExit(f"REFUSING TO WRITE -- {rid}'s shot {k} is not {v}")
    if f'tip:"{shot["tip"]}"' not in m:
        raise SystemExit(f"REFUSING TO WRITE -- {rid}'s shot tip is not this run's")
    if len(shot["tip"]) > 46:
        raise SystemExit("REFUSING TO WRITE -- the shot tip is over verify's 46")
    if f"dmg:{fnum(dmg)}," not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- {rid}'s blade is not {dmg}")
    if 'shape:"staff"' not in ent:
        raise SystemExit(f"REFUSING TO WRITE -- {rid} is not a staff")
    if stubbed != ("charge:1e9" in ent):
        raise SystemExit(f"REFUSING TO WRITE -- {rid}'s ultimate is "
                         f"{'live' if stubbed else 'stubbed'}; this stage wants it the other way")
    return ent


def added_lines(old: str, new: str) -> list[str]:
    olds = set(old.splitlines())
    return [l for l in new.splitlines() if l not in olds]


def check_no_rng(edits) -> None:
    for label, old, new in edits:
        ins = strip_comments("\n".join(added_lines(old, new)))
        if "rng()" in ins or "spawnFx" in ins or "Math.random" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the match RNG")


def write_link(src_p: pathlib.Path, out_p: pathlib.Path, s0: str, s: str, builder: str, stage) -> None:
    code0, code = strip_comments(s0), strip_comments(s)
    if code.count("Math.random") != code0.count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    s = f"<!-- GENERATED by {builder} --stage {stage} --src {src_p.name} -->\n" + s
    syntax_check(s, out_p.name)
    out_p.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out_p.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")


def paths(src: str, out: str):
    src_p, out_p = (HERE / src).resolve(), (HERE / out).resolve()
    if out_p.name == PROTECTED:
        raise SystemExit("refusing to write the live build")
    if out_p.exists():
        raise SystemExit(f"refusing to overwrite {out_p.name} -- a link is written once. "
                         "Delete it by hand if this is a rebuild.")
    if not src_p.exists():
        raise SystemExit(f"no such build: {src_p}")
    return src_p, out_p


def audit(stages, tip_p: pathlib.Path) -> int:
    """DID EVERY EDIT SURVIVE? Every stage's edits replayed; every line of CODE
    an edit ADDS must be in the tip. A line a LATER stage of the same builder
    replaces is superseded, not lost; an edit labelled "the relic's note ..."
    rewrites comment prose and is checked against the tip with comments kept.
    (`chain_audit.py` cannot read function-built tables: open item 31.)"""
    raw = tip_p.read_text(encoding="utf-8")
    tip = strip_comments(raw)
    flat = [(i, st, e) for i, (st, edits) in enumerate(stages) for e in edits]
    total = lost = superseded = 0
    for i, st, (label, old, new) in flat:
        prose = label.startswith("the relic's note")
        strip = (lambda x: x) if prose else strip_comments
        later = set()
        for j, _st, (_l, o2, _n) in flat:
            if j > i:
                later |= set(strip(o2).splitlines())
        olds = set(strip(old).splitlines())
        added = [l for l in strip(new).splitlines()
                 if l not in olds and len(l.strip()) > 6 and l.strip() not in ("}", "});", "},")]
        body = raw if prose else tip
        miss = [l for l in added if l not in body and l not in later]
        sup = [l for l in added if l not in body and l in later]
        total += 1
        if sup:
            superseded += 1
            print(f"  ok    stage {st}  {label}: {len(sup)} line(s) replaced by a later stage, by design")
        if miss:
            lost += 1
            print(f"  LOST  stage {st}  {label}: {len(miss)} of {len(added)} lines, first {miss[0].strip()[:70]!r}")
    print(f"\n  {total - lost}/{total} inserts survive in {tip_p.name}"
          f" ({superseded} carry lines a later stage replaced on purpose)"
          + ("" if not lost else "  <-- A DOWNSTREAM EDIT ATE SOMETHING"))
    return 0 if not lost else 1
