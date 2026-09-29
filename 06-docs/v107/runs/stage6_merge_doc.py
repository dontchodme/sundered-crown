"""Merge stage 6's sections into the v107 doc (resume of 2026-09-29 08:xx).
Replaces '## 5. Stage 6 (next)' .. the end with s6int/doc_s6_sections.md (edited below), and updates the header and
§0's composition paragraph for compose15. Every edit is an exactly-once replacement or it stops. Writes LF.
--tip-probe <file>: the one-seed probe on the angelus-tip fx link, read into §5e."""
import hashlib, pathlib, re, sys
S = pathlib.Path(r"C:/Users/Ye/AppData/Local/Temp/claude/C--Users-Ye-Desktop-mtg-cmdr-deck-generator-claude-code-output/f43b1615-f237-4ba7-9f4f-144b4ddc956e/scratchpad/batch/lightkeeper")
DOC = pathlib.Path("C:/dev/sundered-crown/06-docs/v107/lightkeeper-bulwark-build-v107.md")
h = lambda b: hashlib.sha256(b).hexdigest()[:16]
doc = DOC.read_bytes().decode("utf-8"); assert "\r" not in doc
print("doc in", h(doc.encode()), doc.count("\n"), "lines")
sec = (S / "s6int/doc_s6_sections.md").read_text(encoding="utf-8"); assert "\r" not in sec

def rep(t, a, b, what):
    n = t.count(a)
    if n != 1: sys.exit(f"STOP: {what}: anchor found {n}x")
    return t.replace(a, b, 1)

# ---- the tip probe (bonus) ----
tp = None
if len(sys.argv) > 2 and sys.argv[1] == "--tip-probe":
    tp = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    m = re.search(r"^\s+(\d+)/(\d+)\s*$", tp, re.M); assert m, "no n/N line in the tip probe"
    fights = re.search(r"(\d+) fights", tp).group(1)
    casts = re.search(r"whole-state diffs clean: (\d+) wall frames .*?, (\d+) casts", tp)
    drawn = re.search(r"drawn frames (\d+) \((\d+) with the picture up", tp)
    voice = re.search(r"raises (\d+)\s+tinks (\d+).*?gongs (\d+)\s+folds (\d+).*?death closes silent (\d+)", tp)
    fails = [l.strip()[:3] for l in tp.splitlines() if re.match(r"^\s+\[\d+\] FAIL", l)]
    TIP = (f"- **On the line's tip of 08:04** (a bonus, not one of the gates asked for): the fx link the builder writes on "
           f"`sc-angelus-b9-fx` (42 relics; compose15, f1dcb017f69db079), under the final probe, one seed, both sides, every foe, "
           f"drawn every 30th step: **{m.group(1)}/{m.group(2)}**" + (f" ({', '.join(fails)} FAIL)" if fails else "") +
           f" ({fights} fights, {casts.group(2)} casts, {int(casts.group(1)):,} wall frames clean; {voice.group(1)} raises, "
           f"{voice.group(2)} tinks, {int(voice.group(3)):,} gongs, {voice.group(4)} folds, {voice.group(5)} death closes silent; "
           f"{int(drawn.group(1)):,} frames drawn, {int(drawn.group(2)):,} with the picture up; "
           f"`runs/stage6_probe_on_angelus_tip_s1.txt`). The carry's own probe and `engine_ab` are still the orchestrator's.")
    import textwrap
    TIP = textwrap.fill(TIP, width=108, subsequent_indent="  ", break_long_words=False, break_on_hyphens=False) + "\n"

# ---- edits to the drafted sections ----
sec = rep(sec, """compose12 to
compose14 (§0) prove it on every other in-progress builder and on every newer tip of the line.""",
"""compose12 to
compose15 (§0) prove it on every other batch builder and on every newer tip of the line, up to its tip
of 08:04 on 2026-09-29, `sc-angelus-b9-fx`.""", "intro compose")
sec = rep(sec, """`lightkeeper_probe.py` is now v6 (ce9d1b07ee1b449f; v5, 8f4e1403afdd978d, is backed up in scratch).""",
"""`lightkeeper_probe.py` is now v6 (e1e09479216f72d6, its final form; its first form was ce9d1b07ee1b449f, and
v5, 8f4e1403afdd978d, is backed up in scratch).""", "5d hash")
sec = rep(sec, "Ironhail bolt (the lab; the probe's own reading is in §5a).", "Ironhail bolt (the lab; the probe's own reading is in §5e).", "5a ref")
sec = rep(sec, "Checks [1]-[8] are v5's, unchanged. Two checks are new,",
          "Checks [1]-[8] are v5's, but for one change to [7]'s once-a-fight table check (the last bullet). Two checks are new,", "5d unchanged")
sec = rep(sec, """- It also MEASURES, and does not gate, how far along the bar each scorch lands from where its arrow
  truly died.
""", """- It also MEASURES, and does not gate, how far along the bar each scorch lands from where its arrow
  truly died.
- **[2] and [7] allow nothing new.** The picture's fields are written only in `tickBulwark`, which
  `tickPresentation` calls after the step's tickers (`this.tickBulwark(dt);` is its first line), never
  on a wall frame or at the cast; the voice is `SFX.play`, which holds no sim state. So v5's diff, with
  its allow-lists unchanged, still reads every `bulwark*` field on every wall frame and every cast, and
  a flash, a float or a scorch written inside `tickLightwall` or `fireUlt` would fail it. (Stage 5's §6
  expected stage 6 to name its fields in an allow-list; hanging the picture off the presentation tick
  made that unnecessary.)
""", "5d allow")
sec = rep(sec, """    - `mP1`, `tickBulwark` nudging the foe 1e-9 on a bank: «MP1» (`runs/stage6_probe_mut_mP1.txt`, 444
      fights, no drawing).""",
"""    - `mP1`, `tickBulwark` nudging the foe 1e-9 on a bank: **[10] fails 30,090 times** ("tickBulwark
      changed the sim: vx", read on the call itself) (`runs/stage6_probe_mut_mP1.txt`, 444
      fights, no drawing).""", "5e mP1")
sec = rep(sec, """    - `mD1`, a DRAWN frame nudging the caster 1e-9: **[10] fails 12,350 times**, on the drawn subset only
      (`runs/stage6_probe_mut_mD1.txt`, the first seed's 74 fights, drawn every 30th step).""",
"""    - `mD1`, a DRAWN frame nudging the caster 1e-9: **[10] fails 12,350 times**, on the drawn subset only:
      every drawn frame that draws the bar ("a drawn frame changed the sim") (`runs/stage6_probe_mut_mD1.txt`,
      the first seed's 74 fights, drawn every 30th step).""", "5e mD1")
sec = rep(sec, """- **The rows, re-checked from the builder** (`runs/stage6_rows_recheck.txt`): `S6` is the two row files
  byte for byte, in order; the stamps above.""",
"""- **The rows, re-checked from the final builder, a559dc47824545e9** (`runs/stage6_rows_recheck.txt`, 08:10 on
  2026-09-29): `S6` is the two row files byte for byte, in order (voice 4, picture 9); the picture rows
  alone 728d64f8397290a1, the voice rows alone a8629a7fe94d50b9, both orders e3f16bf01f0e2995, no CR.""", "5e rows")
if tp:
    sec = rep(sec, """- **render_ab:** the other relics' pairs""", TIP + """- **render_ab:** the other relics' pairs""", "5e tip probe")
sec = rep(sec, """The runner-up, Lastlight 107312, scored 0.2 lower (11 blocks, 6 arrows).
""", """The runner-up, Lastlight 107312, scored 0.2 lower (11 blocks, 6 arrows).

The command is the pattern's, `--at <cast - 1.2> --window <dur + 1.2 + 1.8> --end-at-window`, with `dur`
read as the window's length in match time, 10.22s: the window clock stops in the freezes, so 8 + 3 would
end the clip 0.43s before the close, and the fold would not be in it.
""", "5f window")
sec = rep(sec, """    a559dc47824545e9, `--stage 1, 2, 3, 5, 6` on the tip of the day, with `engine_ab` on each carry, and
    **the probe (v6) on the carried fx link** (it reads [1]-[10] there, and would fail [7] or [10] if a
    carry let other code write the state on a wall frame or in the picture's hook). The builder composes
    with every other in-progress batch builder as they stood at 03:20 on 2026-09-29 (`runs/compose14.txt`,
    0 FAIL), and it writes the same change sets on every newer tip of the line (§0);""",
"""    a559dc47824545e9, `--stage 1, 2, 3, 5, 6` on the tip of the day, with `engine_ab` on each carry, and
    **the probe (v6) on the carried fx link** (it reads [1]-[10] there, and would fail [7] or [10] if a
    carry let other code write the state on a wall frame or in the picture's hook). Exsanguinate is on
    the line now (254f9c4), so nothing waits ahead of this carry. The builder composes with every other
    batch builder as they stood at 08:07 on 2026-09-29 (`runs/compose15.txt`, 0 FAIL: the six committed
    and Censer, Aureole, Spellbreaker and Heartwood), and it writes the same change sets on every newer
    tip of the line up to `sc-angelus-b9-fx`, the tip of 08:04 (§0)""" + (",\n    where the stage-6 link it writes reads the probe's 10/10 on one seed (§5e)" if tp and "10/10" in TIP else "") + """. On `sc-tendril-fx` the carried b9.5 passed the
    probe (8/8 under v5) and `engine_ab` (3996/3996) at stage 5 (§0);""", "6 orchestrator")
sec = rep(sec, """- **Standing, not this build's:**""", """- **Stage 6 (Code's): done** (§5). What is left of it is the orchestrator's (the spec out, `shell_identity`,
  the clip to Rick) and Rick's (every pick is his to overrule).
- **Standing, not this build's:**""", "6 stage6")

# ---- the doc ----
i = doc.index("## 5. Stage 6 (next)\n")
assert doc.count("## 5. Stage 6 (next)\n") == 1 and doc[i:].count("## 6. What is left, and whose") == 1
doc = doc[:i] + sec
doc = rep(doc, "applies with the same change sets to every newer tip of the line, up to `sc-lodestone-b205-fx` and `sc-widowmaker-fxout`.",
          "applies with the same change sets to every newer tip of the line, up to its tip of 08:04, `sc-angelus-b9-fx` (compose15, 0 FAIL).", "header")
doc = rep(doc, """pairing both ways and both stacks reaching every builder's last stage, the same change sets on the
  same six tips.
""", """pairing both ways and both stacks reaching every builder's last stage, the same change sets on the
  same six tips. **And as `compose15` (08:07 on 2026-09-29), after the line moved again** (Lodestone
  61043aa, Widowmaker 254f9c4, Oracle 76c474a and Angelus 3f9b0d0 committed; the line's tip is now
  `sc-angelus-b9-fx`, 85b8af63055d1108, 42 relics), against every other batch builder as it stood: the
  six committed (Widowmaker bf8dff45e6870fa4, Coldiron f194fa06f46454c9, Ironhail 491643c55a34fa56,
  Lodestone c74cd4a4508bfcf5, Oracle ae5d6f4e641a2b16, Angelus 0e4e2fc3ff5813de) and the four in
  progress (Censer 78501578c5773570, Aureole c7641c026661b686, and the two started since compose14,
  Spellbreaker 463b49d265b3258c and Heartwood 04567e2ed899524a, stages 1-3 each: neither writes a stage 5
  as it stands). **0 FAIL**, 64 verdicts, both ways and both stacks, and the same two change sets on
  eight tips: the six above, `sc-oracle-fx` (15cf62f96f72653a) and `sc-angelus-b9-fx`
  (`runs/compose15.sh` -> `compose15.txt`, `.err`).
""", "§0 compose15")
doc = rep(doc, "`compose12.txt` / `compose13.txt`, are kept for the record.",
          "`compose12.txt` / `compose13.txt` / `compose14.txt`, are kept for the record.", "§0 record")
assert "«" not in doc and "»" not in doc, "a placeholder is left"
assert "\r" not in doc and doc.endswith("\n")
DOC.write_bytes(doc.encode("utf-8"))
print("doc out", h(doc.encode()), doc.count("\n"), "lines")
