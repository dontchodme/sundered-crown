"""Write Portcullis's stage 6 into tools/portcullis_build.py from the labs' byte-exact row files.

Ironwood's gen_s6.py pattern (scratch/build/iw6): the rows are the labs' own files; the picture rows
alone must reproduce the picture lab's stamp, the voice rows alone the voice lab's end-to-end sha, and
both together the voice lab's combined page; no row's anchor may sit inside another's; rows whose
anchors share a line in the base are MERGED into one edit; the S6 list is written with triple-quoted
strings, and --stage 6 is wired (refuses to run twice; S6 scanned for ultFx and w.* writes).
"""
import json, pathlib, hashlib

S = pathlib.Path("C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/portcullis")
fv_raw = (S / "stage6-voice/rows_final.json").read_bytes()
fp_raw = (S / "stage6-picture/rows_final.json").read_bytes()
fv = json.loads(fv_raw.decode("utf-8"))
fp = json.loads(fp_raw.decode("utf-8"))
fv = fv["rows"] if isinstance(fv, dict) else fv
fp = fp["rows"] if isinstance(fp, dict) else fp
print(f"voice rows {len(fv)} ({len(fv_raw)} bytes, sha {hashlib.sha256(fv_raw).hexdigest()[:16]}); "
      f"picture rows {len(fp)} ({len(fp_raw)} bytes, sha {hashlib.sha256(fp_raw).hexdigest()[:16]})")
assert len(fv) == 5 and len(fp) == 8

# THE RETURNED REPORTS against the files: each lab's full report (report_file) carries its rows whole;
# they must equal the row files field for field (label, anchor, mode, code), in order.
for rep_name, rows_ in (("stage6-voice-report.json", fv), ("stage6-picture-report.json", fp)):
    rep = json.loads((S / rep_name).read_text(encoding="utf-8"))["rows"]
    assert len(rep) == len(rows_), rep_name
    for x, r in zip(rep, rows_):
        assert all(x[k] == r[k] for k in ("label", "anchor", "mode", "code")), (rep_name, r["label"])
print("the labs' reports: every row equal to its row file (label, anchor, mode, code), in order")

base_p = pathlib.Path("C:/dev/sundered-crown/02-chain/sc-tendril-t3.html")
g = base_p.read_bytes().decode("utf-8")
print("base", base_p.name, hashlib.sha256(g.encode()).hexdigest()[:16], "(want 5a6216e3b629fad4)")
assert hashlib.sha256(g.encode()).hexdigest()[:16] == "5a6216e3b629fad4"


def new_of(r):
    return {"before": r["code"] + r["anchor"], "after": r["anchor"] + r["code"], "replace": r["code"]}[r["mode"]]


def apply(t, rows):
    for r in rows:
        assert t.count(r["anchor"]) == 1, r["label"]
        t = t.replace(r["anchor"], new_of(r), 1)
    return t


sha = lambda t: hashlib.sha256(t.encode()).hexdigest()[:16]
pic = apply(g, fp)
print("picture-only sha", sha(pic), "(picture lab's stamp: de1cf49480a06745)")
assert sha(pic) == "de1cf49480a06745"
assert pic == (S / "stage6-picture/pc-final.html").read_bytes().decode("utf-8")
voi = apply(g, fv)
print("voice-only sha", sha(voi), "(voice lab's end-to-end: 817c69c9dfe9463b)")
assert sha(voi) == "817c69c9dfe9463b"
both = apply(g, fv + fp)
comb = (S / "stage6-voice/sc-portcullis-pic-voice.html").read_bytes().decode("utf-8")
print("voice+picture sha", sha(both), "(the voice lab's combined page:", sha(comb) + ")")
assert both == comb == apply(g, fp + fv)

# NO ROW'S ANCHOR MAY SIT INSIDE ANOTHER'S, and no row's code may carry any row's anchor except its own
# re-emitted one (a replace row that re-emits its anchor keeps it findable for the next relic's row).
rows = fv + fp
for i, a in enumerate(rows):
    for j, b in enumerate(rows):
        if i != j:
            assert a["anchor"] not in b["anchor"], (a["label"], b["label"])
            assert a["anchor"] not in b["code"], (a["label"], "carried by", b["label"])

# ROWS WHOSE ANCHORS SHARE A LINE IN THE BASE ARE MERGED INTO ONE EDIT.
spans = []
for r in rows:
    i = g.index(r["anchor"]); j = i + len(r["anchor"])
    l0 = g.rfind("\n", 0, i) + 1
    l1 = g.find("\n", j - 1 if r["anchor"].endswith("\n") else j)
    spans.append([l0, l1, i, j, [r]])
spans.sort(key=lambda x: x[0])
groups = []
for sp in spans:
    if groups and sp[0] <= groups[-1][1]:
        G = groups[-1]
        G[1] = max(G[1], sp[1]); G[2] = min(G[2], sp[2]); G[3] = max(G[3], sp[3]); G[4] += sp[4]
    else:
        groups.append(sp)
# A ROW'S ANCHOR IS WIDENED WHEN THE CHAIN WILL CARRY IT TWICE. The bank voice's anchor,
# `        T.banked += f.shield - b0;`, is Portcullis's own line, but Lightkeeper's Bulwark (in flight on
# the same tip) writes the same line twice more; so the builder's edit takes Portcullis's whole bank
# block, from `      if (u.bank > 0){` (`f.shield + u.bank)` is tickRam's alone) to that line, and puts
# it back unchanged in front of the row's own text. The output is byte-identical to the row's.
WIDEN = {"tickRam: the ward's bank voice, after the bank's three writes": "      if (u.bank > 0){"}
edits = []
order = {id(r): k for k, r in enumerate(rows)}
for l0, l1, i, j, rs in groups:
    if len(rs) == 1:
        r = rs[0]
        if r["label"] in WIDEN:
            a0 = g.rindex(WIDEN[r["label"]], 0, i)
            pre = g[a0:i]
            assert pre.count(chr(10)) == 6 and "f.shield + u.bank)" in pre and g.count(pre + r["anchor"]) == 1, pre
            edits.append((order[id(r)], r["label"], pre + r["anchor"], pre + new_of(r)))
            print(f"WIDENED: {r['label']!r} to {pre.count(chr(10)) + 1} lines from {WIDEN[r['label']]!r}")
            continue
        edits.append((order[id(r)], r["label"], r["anchor"], new_of(r)))
    else:
        old = g[i:j]
        new = apply(old, rs)
        edits.append((min(order[id(r)] for r in rs), " + ".join(r["label"] for r in rs), old, new))
        print("MERGED:", [r["label"] for r in rs])
edits.sort()
edits = [e[1:] for e in edits]
print(f"{len(rows)} rows -> {len(edits)} edits ({len(rows) - len(edits)} merged)")
t = g
for label, old, new in edits:
    assert t.count(old) == 1, label
    t = t.replace(old, new, 1)
assert t == both, "the edits do not reproduce the rows"
for a_ in edits:
    for b_ in edits:
        if a_ is not b_:
            assert a_[1] not in b_[1], (a_[0], "inside", b_[0])
# THE CARRY: every edit's old text once in each build in flight on the same tip (read only).
B = S.parent
for q in sorted(B.glob("*/links/*.html")) + [B / "bindweed/stage6-picture/bw-final.html"]:
    if q.parent.parent.name == "portcullis":
        continue
    h = q.read_bytes().decode("utf-8")
    bad = [(lab, h.count(o)) for lab, o, _ in edits if h.count(o) != 1]
    print(f"  carry {q.parent.parent.name}/{q.name}: " + ("every edit's old text once" if not bad else f"FAILS {bad}"))
    assert not bad

out = ["", "# ---------------------------------------------------------------- stage 6 --",
       "# THE PICTURE AND THE VOICE (v72 §7.1-7.2), picked on measurements under",
       "# Rick's \"you pick i overrule\" by the picture lab and `portcullis_voice_lab.py`",
       "# (v100 §6). Presentation only: engine_ab over all 38 relics, Portcullis",
       "# included, is the proof. The rows are byte-exact to the labs' own files: the",
       "# five voice rows first, then the eight picture rows; no two share a line of",
       "# the base, so none is merged. Every replace row re-emits its anchor, so",
       "# another relic's row on the same line (Bindweed's voice on rune-crack)",
       "# applies in either order. ONE ANCHOR IS WIDENED: the bank voice's line,",
       "# `T.banked += f.shield - b0;`, is written twice more by Lightkeeper's",
       "# Bulwark (in flight), so its edit takes Portcullis's whole bank block, from",
       "# `if (u.bank > 0){`, and puts it back unchanged: the same bytes out.",
       "S6 = ["]
for label, old, new in edits:
    for s in (label, old, new):
        assert "'''" not in s and "\\" not in s, label
    out += ["", f"({label!r},", " '''" + old + "''',", " '''" + new + "'''),"]
out += ["", "]", ""]
block = "\n".join(out)

p = pathlib.Path("C:/dev/sundered-crown/tools/portcullis_build.py")
s = p.read_bytes().decode("utf-8")
assert "\r\n" not in s and "S6 = [" not in s
anchor = '\nSTAGE_OUT = {"1": "sc-portcullis", "2": "sc-ram", "3": "sc-onslaught", "5": "sc-onslaught-b23"}\n'
assert s.count(anchor) == 1
s = s.replace(anchor, block + '\nSTAGE_OUT = {"1": "sc-portcullis", "2": "sc-ram", "3": "sc-onslaught", "5": "sc-onslaught-b23",\n'
              '             "6": "sc-onslaught-fx"}\n', 1)
reps = [
 ('    stage 6   picture, voice, field       (not written yet)\n',
  '    stage 6   picture, voice              -> sc-onslaught-fx.html (no field: drawn sparks, v100 §6)\n'),
 ('''THE BASE is the chain tip, named and asserted.
"""''',
  '''STAGE 6, THE PICTURE AND THE VOICE (v72 §7.1-7.2), picked on measurements
under Rick's "you pick i overrule" (v100 §6). Declared:
  8. THE BANK'S VOICE IS NEW. §7.2 asks for "the ward's existing bank voice,
     reused"; there is none (the synth's 17 kinds: a ward banks in silence,
     and a ward that breaks plays the ordinary hit, a crit). So `ward-bank` is
     the ward's own new kind, as hex-snap is the runic school's, and only
     Onslaught plays it: the vigil blow's own bank stays silent, as it was.
  9. THE SLAM'S VOICE CARRIES THE SHIELD THE SLAM HIT FOR, before the bank; a
     slam at no shield still knocks and banks, so it thuds at the quiet end.
 10. A BANK AT THE CAP STILL SOUNDS: it adds nothing but restarts the ward's
     clock (the brief: "Slams = banks").
 11. THE CLOSE'S VOICE AND ITS FALLING PLATES only when the window closes by
     its clock with the caster alive; a death belongs to the death voice and
     the shatter (Zenith's, Daybreak's and Canopy's rule).
 12. NO fx.js FIELD. §7.1's "Field: spark motes off the plates on each slam,
     both copies" is drawn in the world pass instead (the slam's sparks, off
     the struck plate): a SPECS field spawns once, at the caster, on the cast
     edge of the one ultFx slot, and Portcullis's record lives 0.75s; 24 of
     324 slams land while it lives, and the opponent's cast takes the slot in
     52 of 82 windows (v100 §6). Zenith's and Canopy's precedent; Rick's to
     overrule.
 13. THE HEAD: the vigil route `_fhPlated` becomes the square plated head (a
     gored sphere never drawn by a shipped relic), and the haft's bands are
     gated on the vigil key. Portcullis is the only vigil flail (asserted), so
     no other relic's picture moves (render_ab).
 14. THE WARD'S RING STANDS DOWN while the shell stands (the shell is that
     ring, thickened, and its fill is the pool); it is back the frame the
     plates crack, because the bank outlives the window.
 15. THE PICTURE HANGS OFF THE FIGHTER, never `m.ultFx` (open item 25), and is
     driven in `tickPresentation`, which writes presentation fields, floats,
     tags and `taught` only; a slam is found by `ramTally.slams` rising, and
     its number is read off the slam's own `ram` beat.

THE BASE is the chain tip, named and asserted.
"""'''),
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('''        else:
            if f'bank:{ULT["bank"]},' not in code or f"dmg:{BLADE}," in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bank"])''',
  '''        elif A.stage == "6":
            if f"dmg:{BLADE}," not in relic_row(code, RELIC) or "drawRamTop" in code:
                raise SystemExit("stage 6 goes on stage 5, once")
            # THE HEAD ROUTE AND THE HAFT'S BANDS ARE THE VIGIL FLAIL'S, AND
            # PORTCULLIS IS THE ONLY ONE: no other relic's picture may move.
            vf = re.findall(r'\\{ id:"([a-z]+)", name:"[^"]*", aff:"vigil", shape:"flail"', code)
            if vf != [RELIC]:
                raise SystemExit(f"the vigil flails are {vf}, not Portcullis alone -- "
                                 "the head and the haft would move another relic")
            edits, want = S6, ult_block(ULT["charge"], ULT["bank"])
        else:
            if f'bank:{ULT["bank"]},' not in code or f"dmg:{BLADE}," in relic_row(code, RELIC):
                raise SystemExit("stage 5 goes on stage 3, once")
            edits, want = S5, ult_block(ULT["charge"], ULT["bank"])'''),
 ('''    for label, _old, new in S1 + S2 + S3 + S5:
        ins = strip_comments(new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")''',
  '''    for label, old, new in S1 + S2 + S3 + S5 + S6:
        # WHAT THE INSERT ADDS: an anchor it re-emits (a before / after row,
        # a replace row that keeps its line) is the base's, not the insert's.
        ins = strip_comments(new.replace(old, "", 1) if old in new else new)
        if "rng()" in ins or "spawnFx" in ins or "ultFx" in ins:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' draws the "
                             "RNG or uses the one ultFx slot")
        if re.search(r"\\bw\\.[A-Za-z_]\\w*(\\.\\w+)*\\s*(=[^=]|\\+=|-=|\\*=|/=|\\+\\+|--)", ins):
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes the "
                             "shared weapon row")'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b, 1)
p.write_bytes(s.encode("utf-8"))
print("stage 6 written:", len(edits), "edits;", p, len(s), "chars")
