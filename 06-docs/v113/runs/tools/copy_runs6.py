"""v113 stage 6: copy the stage's small run files into 06-docs/v113/runs/ -- the stage6_* txt and json whole, the
generator's and the build's printouts, the two labs' row files, outputs and state notes (renamed stage6_voice_* /
stage6_picture_*; cp1252 output transcoded to UTF-8), the scratch tools into runs/tools/ (the picture lab's scripts
as stage6_picture_*.py) and the lane scripts into runs/sh/. LF text. Nothing large: the labs' big jsons, the
pages, the pngs, the wavs and the clips stay where they are.
    python copy_runs6.py <S> <repo>"""
import pathlib, sys
S = pathlib.Path(sys.argv[1]); REPO = pathlib.Path(sys.argv[2])
R, S6, V, P = S / "runs", S / "s6", S / "stage6-voice", S / "stage6-picture"
OUT = REPO / "06-docs" / "v113" / "runs"
(OUT / "tools").mkdir(parents=True, exist_ok=True); (OUT / "sh").mkdir(parents=True, exist_ok=True)
n = {"runs": 0, "labs": 0, "tools": 0, "sh": 0}
def text(p):
    b = p.read_bytes()
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        t = b.decode("cp1252")                   # a console that printed cp1252 (the picture lab's engine_ab, chain)
    return t.replace("\r\n", "\n")
def put(p_in, p_out, key):
    p_out.write_text(text(p_in), encoding="utf-8", newline="\n"); n[key] += 1
for p in sorted(R.glob("stage6_*")):
    if p.suffix in (".txt", ".json", ".log"):
        put(p, OUT / p.name, "runs")
put(S6 / "gen_s6.txt", OUT / "stage6_gen_s6.txt", "runs")
put(S6 / "build_s6.txt", OUT / "stage6_build_s6.txt", "runs")
put(S6 / "smoke_fx_s1.txt", OUT / "stage6_probe_smoke_fx_s1.txt", "runs")
LABS = [(V / "rows_final.json", "stage6_voice_rows.json"), (V / "run_final.log", "stage6_voice_run_final.log"),
        (V / "STATE.md", "stage6_voice_STATE.md"),
        (P / "rows_final.json", "stage6_picture_rows.json"), (P / "STATE.md", "stage6_picture_STATE.md"),
        (P / "m3_summary.txt", "stage6_picture_m3_summary.txt"), (P / "m2_summary.txt", "stage6_picture_m2_summary.txt"),
        (P / "verify.out", "stage6_picture_verify.out"), (P / "verify_v2_partial.out", "stage6_picture_verify_v2_partial.out"),
        (P / "fxprobe.out", "stage6_picture_fxprobe.out"), (P / "fxprobe_base.out", "stage6_picture_fxprobe_base.out"),
        (P / "fx_diag.out", "stage6_picture_fx_diag.out"), (P / "renderab.out", "stage6_picture_renderab.out"),
        (P / "sil_final.out", "stage6_picture_sil_final.out"), (P / "order.out", "stage6_picture_order.txt"),
        (P / "chain.out", "stage6_picture_chain.out"), (P / "engine_ab38.txt", "stage6_picture_engine_ab38.txt"),
        (P / "engine_ab_control.txt", "stage6_picture_engine_ab_control.txt"), (P / "sheet_header.txt", "stage6_picture_sheet_header.txt"),
        (P / "electron/cost.out", "stage6_picture_cost.out"), (P / "electron/cost_ll.out", "stage6_picture_cost_ll.out"),
        (P / "electron/ident.out", "stage6_picture_ident.out"), (P / "electron/ident_ctl.out", "stage6_picture_ident_ctl.out")]
for src, name in LABS:
    put(src, OUT / name, "labs")
for name in ("gen_s6.py", "neg_builder6.py", "builder_negatives_s1to5.py", "mutants6.py", "mutant_table6.py",
             "probe_cmp6.py", "clip_timeline6.py", "clip_audio6.py", "patch_probe6.py", "assemble_doc.py",
             "copy_runs6.py", "idle_exec.py"):
    put(S6 / name, OUT / "tools" / name, "tools")
for p in sorted(P.glob("tw_*.py")) + [P / "scythe_sil.py"]:
    put(p, OUT / "tools" / ("stage6_picture_" + p.name), "tools")
for name in ("lane_a.sh", "lane_b.sh", "lane_c1.sh", "lane_c2.sh", "rebuild_check6.sh"):
    put(S6 / name, OUT / "sh" / ("stage6_" + name), "sh")
print(n)
tot = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
cnt = sum(1 for f in OUT.rglob("*") if f.is_file())
big = [(f.name, f.stat().st_size) for f in OUT.rglob("*") if f.is_file() and f.stat().st_size > 60000]
print(f"runs/: {cnt} files, {tot / 1024:.0f} KB; over 60 KB: {big}")
