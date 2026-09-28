"""WHY NO NEW fx.js FIELD (v83 section 4: "Field: iron-spark motes on landings, both copies"): on real fights
(the base link, undrawn, both sides), per Quarrelstorm window -- how long Ironhail keeps the one ultFx slot
(window clock) and why it lost it; the window clock of every landing; how many landings fall while the slot
is still Ironhail's (a SPECS field fires ONCE, at the slot's cast edge, key = w|src, at the slot's (x, y),
so it cannot fire at a landing); how far each landing's spot is from the point a SPECS field would spawn
at. usage: ih_fxprobe.py [page] -> fxprobe.json / stdout. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (HERE.parent / "links" / "sc-ironhail-sunder.html").resolve()
FOES = ["aureole", "gravemourn", "grudgebearer", "lastlight", "paradox", "spellbreaker", "twinshade", "widowmaker",
        "axiom", "slagheart", "thornshear", "dawnbringer", "heartwood", "morningstar", "lightkeeper", "starwarden"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true; AC.SFX.play = function(){};
  const DT = AC.CONFIG.physics.dt;
  const m = side === "a" ? new AC.Match("ironhail", foe, seed) : new AC.Match(foe, "ironhail", seed);
  const me = m.a.w.id === "ironhail" ? m.a : m.b, src = me === m.a ? "a" : "b";
  const W = []; let cur = null, step = 0, landed = 0;
  while (step < 200 / DT && !m.over){
    const pre = m.hail.filter(d => d.side === src);
    m.step(DT); step++;
    const Z = me.ultHail, T = me.hailTally;
    if (Z && !cur){ const u = m.ultFx; cur = { fx: u ? u.x : null, fy: u ? u.y : null, life: u ? u.life : null, w: u ? u.w : null,
                                               ux: u ? [u.x, u.y] : null, me: [me.x, me.y], held: null, lost: null, lands: [], dur: 0 }; W.push(cur); }
    const L = T ? T.landed : 0;
    if (L > landed && cur){
      const gone = pre.filter(d => m.hail.indexOf(d) < 0);
      for (const d of gone) cur.lands.push({ t: Z ? Z.t : cur.dur, dC: Math.hypot(d.x - cur.fx, d.y - cur.fy), inSlot: cur.held === null });
    }
    landed = L;
    if (!Z){ if (cur && cur.held === null){ cur.held = cur.dur; cur.lost = "window ended first"; } cur = null; continue; }
    cur.dur = Z.t;
    const u = m.ultFx, mine = u && u.w === "ironhail" && u.src === src;
    if (cur.held === null && !mine){ cur.held = Z.t; cur.lost = u ? "opponent's cast" : "expired"; }
  }
  return W;
}"""
res = []
with game(game_path=BASE) as (page, errors):
    for i, foe in enumerate(FOES):
        for seed, side in ((2207 + i, "a"), (5150 + i, "b")):
            w = page.evaluate(JS, [foe, seed, side])
            assert not errors, errors[:3]
            for x in w: x.update(foe=foe, seed=seed, side=side)
            res += w
for x in res:
    if x["held"] is None: x["held"] = x["dur"]; x["lost"] = "match ended in the window"
n = len(res)
held = sorted(x["held"] for x in res)
lost = {}
for x in res: lost[x["lost"]] = lost.get(x["lost"], 0) + 1
share = sum(min(x["held"], x["dur"]) for x in res) / max(1e-9, sum(x["dur"] for x in res))
B = [b for x in res for b in x["lands"]]
bt = sorted(b["t"] for b in B); dc = sorted(b["dC"] for b in B)
ins = sum(1 for b in B if b["inSlot"])
q = lambda a, p: a[min(len(a) - 1, int(p * len(a)))] if a else float("nan")
atMe = sum(1 for x in res if x["ux"] and abs(x["ux"][0] - x["me"][0]) < 1e-6 and abs(x["ux"][1] - x["me"][1]) < 1e-6)
print(f"{n} Quarrelstorm windows on {len(FOES)} foes x 2 seeds (both sides); ultFx life at the cast: {sorted(set(x['life'] for x in res))}; "
      f"the slot's spawn point is the caster's own spot on {atMe}/{n}")
print(f"  the slot is Ironhail's for a median {held[n//2]:.2f}s of window clock (max {held[-1]:.2f}); lost to: {lost}")
print(f"  a slot-borne field could exist for {share*100:.1f}% of the window's clock")
print(f"  {len(B)} landings: window clock median {q(bt, .5):.2f}s (p10 {q(bt, .1):.2f}, min {bt[0] if bt else 'n/a'}); "
      f"{ins} of {len(B)} while the slot was still Ironhail's (a SPECS field would already be spawned: it fires once, at the cast edge)")
print(f"  a landing's spot is a median {q(dc, .5):.0f} units from the field's spawn point (p10 {q(dc, .1):.0f}, p90 {q(dc, .9):.0f})")
(HERE / "fxprobe.json").write_text(json.dumps(res, indent=1))
