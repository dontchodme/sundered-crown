import pathlib
p = pathlib.Path("C:/dev/sundered-crown/tools/heartwood_build.py"); s = p.read_text(encoding="utf-8")
reps = [
 ('    ap.add_argument("--stage", choices=["1", "2", "3", "5"], required=True)',
  '    ap.add_argument("--stage", choices=["1", "2", "3", "5", "6"], required=True)'),
 ('    if A.stage == "5" and (BLADE is None or BLADE == SHIPPED_DMG):\n        raise SystemExit("stage 5: the blade is not measured yet (BLADE)")',
  '    if A.stage in ("5", "6") and (BLADE is None or BLADE == SHIPPED_DMG):\n        raise SystemExit(f"stage {A.stage}: the blade is not measured yet (BLADE)")'),
 ('''    if A.stage == "1":
        for name in NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")''',
  '''    if A.stage == "1":
        for name in NAMES + S6_NAMES:
            if not free_name(name, code):
                raise SystemExit(f"'{name}' is already in the base")'''),
 ('''        else:
            want = ult_block(ULT["charge"], ULT["extraEnt"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{SHIPPED_DMG}," not in row):
                raise SystemExit("stage 5 goes on stage 3 (the entangle on, blade 12.65), once")
            blade = BLADE
            edits = S5''',
  '''        elif A.stage == "5":
            want = ult_block(ULT["charge"], ULT["extraEnt"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{SHIPPED_DMG}," not in row):
                raise SystemExit("stage 5 goes on stage 3 (the entangle on, blade 12.65), once")
            blade = BLADE
            edits = S5
        else:
            # STAGE 6 GOES ON STAGE 5: the entangle on, the blade BLADE, and none of
            # stage 6's names in the source yet (the picture and the voice go on once).
            want = ult_block(ULT["charge"], ULT["extraEnt"])
            if (" ".join(strip_comments(want).split()) != " ".join(relic_ult(code).split())
                    or f"dmg:{BLADE}," not in row or free_name("tickRootfast", code)):
                raise SystemExit(f"stage 6 goes on stage 5 (the entangle on, blade {BLADE}), once")
            for name in S6_NAMES:
                if not free_name(name, code):
                    raise SystemExit(f"'{name}' is already in this source -- stage 6 goes on once")
            blade = BLADE
            edits = S6'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b, 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
