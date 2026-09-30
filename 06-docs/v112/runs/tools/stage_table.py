"""v112 §2: stage 0 and the stages against it, and the window-clock controls, from runs/*.json. Reads only.
    python stage_table.py <S>"""
import json, pathlib, sys
R = pathlib.Path(sys.argv[1]) / "runs"
def arm(name, a):
    return json.loads((R / f"{name}.json").read_text())["arms"][a]
def two(prefix, a):
    x = [arm(f"{prefix}_{b}", a) for b in ("2207", "2317")]
    return x
def w(x): return 100 * x["win"]
def pool(xs): return sum(w(x) for x in xs) / len(xs)
L = []
L.append("STAGE 0 -- the design's lab (ult_overlay + rootfast.js) on Chromium 151, on the base sc-tendril-t3, Heartwood side A,")
L.append("the design's 33 foes (the 34-relic roster minus the donor) x 20 seeds, seed0 2207 / 2317, 660 fights an arm a block\n")
L.append(f"{'arm':<40}{'block 1':>9}{'block 2':>9}{'pooled':>9}   casts   blows in/out    roots/cast  trans/cast  pinned%   census frozen (all / windows)")
def row(label, xs):
    c = sum(x["casts"] for x in xs) / 2; hi = sum(x["hitsIn"] for x in xs) / 2; ho = sum(x["hitsOut"] for x in xs) / 2
    st = lambda k: sum(x["stats"].get(k, 0) for x in xs) / 2
    cen = [x.get("census") for x in xs]
    cs = ""
    if all(cen):
        fa = sum(q["frozen"] for q in cen) / sum(q["steps"] for q in cen)
        fw = sum(q["winFrozen"] for q in cen) / max(1, sum(q["win"] for q in cen))
        cs = f"{100*fa:.2f}% / {100*fw:.2f}%"
    tr = f"{st('trans'):.2f}" if any("trans" in x["stats"] for x in xs) else "  -"
    L.append(f"{label:<40}{w(xs[0]):>9.1f}{w(xs[1]):>9.1f}{pool(xs):>9.2f}   {c:5.2f}   {hi:5.2f}/{ho:5.2f}     {st('roots'):5.2f}      {tr:>5}      {st('f_pinnedPct'):5.1f}    {cs}")
row("A    no ultimate (lab charge 16)", two("s0_ASBC", "A"))
row("SHIP the shipped freeze (engine 15)", two("s0_ASBC", "SHIP"))
row("B    the root 1.0 (lab charge 16)", two("s0_ASBC", "B"))
row("C    + entangle (lab charge 16)", two("s0_ASBC", "C"))
row("B    the root 1.0 (lab charge 15)", two("lab_c15_trans", "B"))
row("C    + entangle (lab charge 15)", two("lab_c15_trans", "C"))
L.append("")
L.append("BUILT (rf_lab.py --arms SHIP on the link: its own ultimate, the same side, foes and seeds)")
row("stage 1 sc-heartwood-stub", two("built_stub", "SHIP"))
row("stage 2 sc-heartwood-root (charge 13)", two("built_root", "SHIP"))
row("stage 3 sc-heartwood-rootfast (charge 13)", two("built_rootfast", "SHIP"))
row("stage 5 sc-heartwood-b11 (blade 11) FINAL", two("built_b11", "SHIP"))
L.append("  against: the lab's arm C at the final's numbers (blade 11, charge 15 on the lab's clock, rootFor 1.0)")
row("lab C, blade 11, c15, dur 8", two("lab_c15_b11", "C"))
row("lab C, blade 11, c15, dur 9.42 (engine's)", two("lab_c15_b11_dur942", "C"))
L.append("")
L.append("CONTROLS FOR THE WINDOW CLOCK (v112 §2)")
row("lab at the engine's window: B, c15, dur 9.42", two("lab_c15_dur942", "B"))
row("lab at the engine's window: C, c15, dur 9.42", two("lab_c15_dur942", "C"))
row("build on the lab's clock: stage 2", [arm(f"ctl-labclock-root_{b}", "SHIP") for b in ("2207", "2317")])
row("build on the lab's clock: stage 3", [arm(f"ctl-labclock-rootfast_{b}", "SHIP") for b in ("2207", "2317")])
L.append("")
L.append("PUBLISHED (Chromium 141, sc-trunk, seed0 2207, 10 seeds) AGAINST THE SAME 330 FIGHTS REPLAYED ON 151")
P = "C:/dev/sundered-crown/06-docs/v85/runs/"
pb = json.loads(pathlib.Path(P + "rootfast_base.json").read_text())["arms"]
p8 = json.loads(pathlib.Path(P + "rootfast_r08.json").read_text())["arms"]["C"]
p10 = json.loads(pathlib.Path(P + "rootfast_r10.json").read_text())["arms"]["C"]
q = json.loads((R / "pub151_base.json").read_text())["arms"]
q8 = json.loads((R / "pub151_r08.json").read_text())["arms"]["C"]; q10 = json.loads((R / "pub151_r10.json").read_text())["arms"]["C"]
for lab, A, B in (("A", pb["A"], q["A"]), ("SHIP", pb["SHIP"], q["SHIP"]), ("B root 0.45 (the lab default)", pb["B"], q["B"]),
                  ("C root 0.45 (the lab default)", pb["C"], q["C"]), ("C root 0.8", p8, q8), ("C root 1.0 (taken)", p10, q10)):
    same = sum(1 for k in A["byFoe"] if abs(A["byFoe"][k] - B["byFoe"].get(k, -1)) < 1e-9)
    L.append(f"  {lab:<32} published {w(A):5.1f}   on 151 {w(B):5.1f}   foes' rates identical {same:>2}/33   "
             f"pinned {A['stats']['f_pinnedPct']:5.2f} -> {B['stats']['f_pinnedPct']:5.2f}   roots {A['stats']['roots']:.2f} -> {B['stats']['roots']:.2f}   "
             f"blows in {A['hitsIn']:.2f} -> {B['hitsIn']:.2f}")
text = "\n".join(L) + "\n"
(R / "stage_table.txt").write_text(text, encoding="utf-8", newline="\n")
print(text)
