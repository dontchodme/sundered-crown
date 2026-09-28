"""Splice stage 6 into 06-docs/v108/ironhail-quarrelstorm-build-v108.md (backup kept in s6/)."""
import pathlib, sys, shutil
S = pathlib.Path(__file__).resolve().parent
D = pathlib.Path("C:/dev/sundered-crown/06-docs/v108/ironhail-quarrelstorm-build-v108.md")
doc = D.read_text(encoding="utf-8")
assert "\r\n" not in doc
if "## 5. Stage 6: the picture and the voice" in doc:
    raise SystemExit("already spliced")
shutil.copy(D, S / "doc_before_splice.md")
fill = dict(a.split("=", 1) for a in sys.argv[1:])

draft = (S / "doc_s6_draft.md").read_text(encoding="utf-8")
gates = (S / "doc_s6_gates.md").read_text(encoding="utf-8")
clip = (S / "doc_s6_clip.md").read_text(encoding="utf-8")
left = (S / "doc_s6_left.md").read_text(encoding="utf-8")
sec5 = draft.replace("PENDING_GATES\n", gates).replace("PENDING_CLIP\n", clip)
for k, v in fill.items():
    sec5 = sec5.replace(k, v)
assert "PENDING" not in sec5 and "MS4_COUNT" not in sec5 and "PROBE_SUNDER_NOTE" not in sec5, "unfilled"


def one(s, a, b):
    assert s.count(a) == 1, a[:80]
    return s.replace(a, b, 1)


# 1. the header line
old_h = doc.split("\n", 1)[0]
assert old_h.startswith("# v108 — IRONHAIL / QUARRELSTORM, BUILD. STAGES 0-5 DONE")
new_h = (old_h.replace("STAGES 0-5 DONE", "STAGES 0-6 DONE", 1)
         .replace(" Carry (stages 1-3) onto the chain and stage 6 (picture, voice, the nova's field out) next.",
                  " STAGE 6, the picture and the voice, is built on the final as `sc-ironhail-sunder-fx` "
                  "(presentation only: engine_ab 4218/4218 over all 38 relics, Ironhail included; probe 11/11): "
                  "the limbs in the forge, a rune and a falling bolt a drop, a thud a landing pitched by the "
                  "foe's count, a quieter one a miss, and no close voice. The carry is stages 1, 2, 3 and 6; "
                  "the nova's field spec leaves both copies of `fx.js` by the orchestrator's sync_fx_remove."))
assert new_h != old_h and "Carry (stages 1-3)" not in new_h
doc = new_h + "\n" + doc.split("\n", 1)[1]

# 2. the carry
doc = one(doc, "builder with `--src <tip>` and proves the carry with `engine_ab`. **The carry is stages 1, 2 and 3**;\nstage 3's link is the final.",
          "builder with `--src <tip>` and proves the carry with `engine_ab`. **The carry is stages 1, 2, 3 and 6**;\n"
          "stage 3's link is the final mechanism, and stage 6 (the picture and the voice) goes on it.")

# 3. the stage-6 note, before the link table
note = ("**Stage 6, the picture and the voice** (§5), built on the final after the third review: fifteen\n"
        "edits byte-exact to the picture lab's and the voice lab's row files, written into the builder as\n"
        "`S6` with a `--stage 6` that goes on the final once. The probe gains [10] (the voice) and [11] (the\n"
        "picture), each switched on from the page, each failed by its own controls; engine_ab over all 38\n"
        "relics, render_ab, chain_audit and tip_audit read it as presentation only. The clip is\n"
        "`07-shorts/v108/quarrelstorm-window.mp4` (§5e). Readings 15-21 are the builder's.\n\n```\n")
doc = one(doc, "reworded (§0); (3) the brief's gates are now set against the built links too, with the misses marked\n(§2, §6).\n\n```\n",
          "reworded (§0); (3) the brief's gates are now set against the built links too, with the misses marked\n(§2, §6).\n\n" + note)

# 4. the link table
doc = one(doc, "                                         shipped 16.23, the shipped rate; it writes nothing\n",
          "                                         shipped 16.23, the shipped rate; it writes nothing\n"
          "  -> sc-ironhail-sunder-fx.html  stage 6  the picture and the voice, on the final        b8ff2014a954be3f\n"
          "                                         (brief stage 4; the nova's field spec is the orchestrator's)\n")

# 6. readings 15-21 in section 0 (the builder's docstring, declared here too)
R = """  15. **The cast voice** is the cast's own `SFX.play("ult", {w: "ironhail"})` in `fireUlt`'s generic
      head, which fell through to rune-crack: an arm is ADDED before that shared fallback (the bellows
      huff) and the fallback line is re-emitted unchanged for the relics that still fall through.
  16. **The landing voice** plays once per landed bolt, in `tickHail` after its hurt and its sunder,
      pitched by the count the foe then carries (the number its tag shows, 1-6); a killing landing
      thuds too, under the death voice.
  17. **The miss voice** plays once per missed bolt, on its landing frame, on the miss line's own test
      read first (the anchor guards it: if that line changes, the row stops applying).
  18. **The close has no voice** (v83 §4: "close -- nothing").
  19. **The picture** is drawn from the match's bolts (`m.hail`, read) and the fighter's own `quarrel*`
      fields (never `m.ultFx`, open item 25); a bolt that resolves is found by `hailTally` rising, so
      `tickHail` makes no call for the picture. The limbs read `ultHail && !over` and cool at the
      verdict; a bolt the kill leaves in the air fades on `quarrelEnd`. **One sunder tag on the foe at a
      time** (Tendril's and Temper's rule): a landing with a tag already up sets its count in place; a
      killing landing tags nothing (the shatter owns that frame).
  20. **"Field: iron-spark motes on landings, both copies" is DRAWN**, not an `fx.js` field (§5c: a
      SPECS field fires once, at the cast edge, on the one ultFx slot, which Ironhail holds for a median
      0.62s of its 8s window). The nova's field spec (`SPECS.ironhail`) is the brief's "nova's field
      spec out": it leaves both copies by the orchestrator's `sync_fx_remove`; this builder edits neither.
  21. **The nova's art is retired with the nova:** `drawUltUnder`'s floor dust and `drawUltOver`'s
      release flash (keyed on the ultFx slot's `"ironhail"`), the charge rune's eight heads (now three
      bolts onto a crossed rune) and the banner's fan (the letters now fall).
"""
doc = one(doc, "its cast branch in `fireUlt` is **retired**. `spawnShot` stays: every bow fires through it.\n",
          "its cast branch in `fireUlt` is **retired**. `spawnShot` stays: every bow fires through it.\n" + R)
doc = one(doc, "  `src/render/fx.js`. Until then the cast still plays the nova's picture over the hail.\n",
          "  `src/render/fx.js`. Until then the cast still plays the nova's picture over the hail. **Stage 6\n"
          "  (§5) retires all of it but two:** the `ultFx` life entry (1.3) stays as the cast's record, with\n"
          "  no art keyed on it now, and `SPECS.ironhail` leaves both copies of `fx.js` by the orchestrator's\n"
          "  `sync_fx_remove` (§5c).\n")

# 5. section 5 and section 6
i5 = doc.index("## 5. Stage 6 (next)\n")
i6 = doc.index("## 6. What is left, and whose\n")
doc = doc[:i5] + sec5.rstrip("\n") + "\n\n" + left
D.write_text(doc, encoding="utf-8", newline="\n")
print("spliced:", len(doc), "chars")
