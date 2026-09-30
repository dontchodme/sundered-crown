"""v112 stage 6: copy stage 6's small run files into 06-docs/v112/runs/ (LF text): the gates' outputs flat, the
probe's passes into runs/stage6_probe/, the two labs' own small outputs into runs/stage6_picture/ and
runs/stage6_voice/ (their big frame/measure jsons stay in scratch), the scratch tools into runs/tools/ and the
queues into runs/sh/.    python copy_runs6.py <S> <repo>"""
import pathlib, sys
S = pathlib.Path(sys.argv[1]); REPO = pathlib.Path(sys.argv[2])
R = S / "runs"; OUT = REPO / "06-docs" / "v112" / "runs"
for sub in ("tools", "sh", "stage6_probe", "stage6_picture", "stage6_voice"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
n = {}
def lf(p_in, p_out, key):
    p_out.write_text(p_in.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    n[key] = n.get(key, 0) + 1
FLAT = ["stage6_gen.txt", "build_stage6.txt", "rebuild6.txt", "builder_negatives.txt", "builder_negatives6.txt",
        "carry_compose6.txt", "mutants6_shas.txt", "stage6_engine_ab38.txt", "stage6_engine_ab_control.txt",
        "stage6_render_ab.txt", "stage6_render_ab_control.txt", "stage6_chain_audit.txt",
        "stage6_chain_audit_control.txt", "stage6_chain_audit_control_base.txt", "stage6_tip_audit_fx.txt",
        "stage6_tip_audit_b11.txt", "stage6_pick.txt", "stage6_clip_log.txt", "stage6_clip_probe.txt",
        "stage6_clip_aac.txt", "stage6_probe_mutants.txt", "q10.log", "q11.log", "q12.log", "ids38.txt"]
for f in FLAT:
    p = R / f
    if p.exists():
        lf(p, OUT / f, "flat")
    else:
        print("missing", f)
for f in ("q10.sh", "q11.sh", "q12.sh", "clip6.sh"):
    lf(R / f, OUT / "sh" / f, "sh")
lf(S / "tools" / "rebuild6.sh", OUT / "sh" / "rebuild6.sh", "sh")
for p in sorted((R / "stage6_probe").iterdir()):
    if p.suffix in (".txt", ".json"):
        lf(p, OUT / "stage6_probe" / p.name, "probe")
P = S / "stage6-picture"
for f in ("STATE.md", "rows_final.json", "m1_summary.txt", "m2_summary.txt", "sil_final.out", "fxprobe.out",
          "renderab.out", "verify_stamp2.out", "verify_tip.out", "verify.out", "cost.out", "order.out", "chain.out",
          "probe_tipfx.txt", "pick_green.json", "seq.out", "seq2.out", "snap_dawnbringer_99001_a.out",
          "snap_dawnbringer_99001_b.out", "snap_gravemourn_99015_a.out", "snap_spellbreaker_2207_a.out"):
    if (P / f).exists():
        lf(P / f, OUT / "stage6_picture" / (f if not f.endswith(".out") else f[:-4] + ".txt"), "picture")
for p in sorted(P.glob("*.py")):
    lf(p, OUT / "stage6_picture" / p.name, "picture")
V = S / "stage6-voice"
for f in ("STATE.md", "rows_final.json", "run_final.txt", "run_final.json", "carry_ironhail.txt", "reg_all_ironhail.txt",
          "reg_all_cands_ironhail.txt", "explore1.txt", "explore2.txt", "explore3.txt", "explore4.txt"):
    lf(V / f, OUT / "stage6_voice" / f, "voice")
for p in sorted(V.glob("*.py")):
    lf(p, OUT / "stage6_voice" / p.name, "voice")
lf(S / "stage6-voice-report.json", OUT / "stage6_voice" / "stage6-voice-report.json", "voice")
for f in ("builder_negatives.py", "builder_negatives6.py", "mutants6.py", "mutant_table6.py", "carry_compose6.py", "copy_runs6.py"):
    lf(S / "tools" / f, OUT / "tools" / f, "tools")
for f in ("gen_s6.py", "patch_probe6.py", "wire_main.py", "analyze.py", "fill6.py", "doc6_apply.py", "patch_doc6b.py", "patch_doc6c.py"):
    lf(S / "s6" / f, OUT / "tools" / f, "tools")
lf(S / "STATE-stage6.md", OUT / "STATE-stage6.md", "flat")
print(n)
tot = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"{OUT}: {sum(1 for f in OUT.rglob('*') if f.is_file())} files, {tot/1024:.0f} KB")
