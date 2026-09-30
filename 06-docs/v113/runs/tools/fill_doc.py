"""Assemble 06-docs/v113/thornwake-bramblesnare-build-v113.md from the scratch pieces and the run files.
    python fill_doc.py <S> <out.md>"""
import json, pathlib, re, sys
S = pathlib.Path(sys.argv[1]); R = S / "runs"; OUT = pathlib.Path(sys.argv[2])
doc = (S / "doc_draft.md").read_text(encoding="utf-8")
body = "\n\n".join((S / f).read_text(encoding="utf-8").rstrip("\n") for f in ("doc_s2.md", "doc_s3.md", "doc_s4.md", "doc_s5.md"))
doc = doc.replace("@@SECTION2@@", body)

def pj(name):
    return json.loads((R / name).read_text(encoding="utf-8"))

# the probe table
rows = [("sc-thornwake-bramble", "2", "probe_bramble"), ("sc-thornwake-snare", "3", "probe_snare"), ("sc-thornwake-b26.5", "5", "probe_final")]
L = ["link                    stage  checks  casts  blows in/out   brambles  bites  dmg    snares  frozen  killing bites  wards broken  shade plants",
     "                                         a fight          a cast    a cast a cast  a cast  (window)"]
for link, st, tag in rows:
    j = pj(tag + ".json"); t = (R / (tag + ".txt")).read_text(encoding="utf-8")
    ok = re.search(r"\n  (\d+/\d+)\n", t).group(1)
    Sx, n = j["S"], j["n"]; F = Sx["fights"]; c = max(1, Sx["casts"])
    L.append(f"{link:<23} {st:<6} {ok:<7} {Sx['casts']/F:<6.2f} {Sx['bin']/F:.2f}/{Sx['bout']/F:<8.2f} {Sx['planted']/c:<9.2f} {Sx['ticks']/c:<6.2f} {Sx['dealt']/c:<6.1f} "
             f"{Sx['snares']/c:<7.2f} {100*Sx['winFrozen']/max(1,Sx['winSteps']):<7.1f} {n.get('fatalTick',0):<14} {n.get('wardBreaks',0):<13} {n.get('shadePlant',0)}")
doc = doc.replace("@@PROBETABLE@@", "\n".join(L))
fj = pj("probe_final.json")
doc = doc.replace("@@SHADEPLANT@@", str(fj["n"].get("shadePlant", 0)))
doc = doc.replace("@@DEADBITES@@", str(fj["n"].get("deadCasterBite", 0)))

# the mutant table
mt = (R / "probe_mutants.txt").read_text(encoding="utf-8").rstrip("\n")
doc = doc.replace("@@MUTTABLE@@", mt)
nm = len([l for l in (R / "mutants_shas.txt").read_text().splitlines() if l.strip()])
doc = doc.replace("@@NMUT@@", str(nm))

# stage 5
t5 = (R / "stage5_table.txt").read_text(encoding="utf-8").splitlines()
i_lad = next(i for i, l in enumerate(t5) if l.startswith("LADDER"))
tab = [l for l in t5[:i_lad] if not l.startswith("PROOF")]
while tab and not tab[-1].strip(): tab.pop()
doc = doc.replace("@@S5TABLE@@", "\n".join(tab))
lad = "\n".join(t5[i_lad - 1:]).strip("\n")
doc = doc.replace("@@LADDERS@@", lad)
fin = [json.loads((R / f"stage5_rr_b26.5_{b}.json").read_text()) for b in ("2207", "2317")]
w = sum(round(r["rate"] * r["games"]) for r in fin); g = sum(r["games"] for r in fin)
doc = doc.replace("@@FINALRATE@@", f"{100*w/g:.1f}% ({w} of {g})")
sa = sum(r["rateA"] for r in fin) / 2; sb = sum(r["rateB"] for r in fin) / 2
doc = doc.replace("@@SIDES@@", f"side A {100*sa:.1f}%, side B {100*sb:.1f}% (740 fights each, pooled over the blocks); "
                               f"block 2207 {100*fin[0]['rate']:.1f}%, block 2317 {100*fin[1]['rate']:.1f}%; mean {sum(r['dur'] for r in fin)/2:.1f}s")
proof = [l for l in t5 if l.startswith("PROOF")]
x = [json.loads((R / f"stage5_rr_b26.5_{b}.json").read_text()) for b in ("2207", "2317")]
doc = doc.replace("@@PROOF@@", "`relic_rate` on `sc-thornwake-b26.5` with NO knob set reproduces stage 3 `--set dmg=26.5` "
                  f"EXACTLY on both blocks: {100*x[0]['rate']:.2f}% / {100*x[1]['rate']:.2f}%, every one of the 37 foes' rates, "
                  f"both sides' rates, the timeouts and the mean duration ({x[0]['dur']:.4f}s / {x[1]['dur']:.4f}s) to the last digit "
                  "(`runs/stage5_table.txt`, the PROOF lines: " + "; ".join(p.split("->")[-1].strip() for p in proof) + ").")
doc = doc.replace("@@BLADE@@", "26.5").replace("@@FINALSHA@@", "fd5031063ecb6807")
gates = (S / "doc_gates.md").read_text(encoding="utf-8").rstrip("\n")
doc = doc.replace("@@GATES@@", gates)
extra = {k: (S / f"doc_{k.lower()}.md").read_text(encoding="utf-8").rstrip("\n") for k in ("LADDERNOTE", "LADDERRICK")}
for k, v in extra.items():
    doc = doc.replace(f"@@{k}@@", v)
left = re.findall(r"@@[A-Z0-9]+@@", doc)
if left:
    raise SystemExit(f"placeholders left: {sorted(set(left))}")
OUT.write_text(doc, encoding="utf-8", newline="\n")
print(f"{OUT}: {len(doc)} chars, {doc.count(chr(10))} lines")
