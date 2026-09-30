"""WHY NO fx.js FIELD (v85 section 4: "Field: leaf motes off the blade, both copies"): on real fights (a page,
undrawn, both sides), per Rootfast window -- how long Heartwood keeps the one ultFx slot (window clock) and why it
lost it (a SPECS field fires ONCE, at the slot's cast edge, key = w|src, at the slot's (x, y), and lives only
while the slot is Heartwood's); where the blade is against that spawn point through the window (the blade's
midpoint and tip at window clock 1, 3, 5, 7s, as `drawWeapon` draws it). usage: hw_fxprobe.py [page]. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (HERE.parent / "links" / "sc-heartwood-b11.html").resolve()
FOES = ["aureole", "gravemourn", "grudgebearer", "lastlight", "paradox", "spellbreaker", "twinshade", "widowmaker",
        "axiom", "slagheart", "thornshear", "dawnbringer", "bindweed", "morningstar", "lightkeeper", "starwarden"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true; AC.SFX.play = function(){};
  if (!AC.WEAPONS.find(w => w.id === foe)) return null;
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, TAU = Math.PI * 2;
  const m = side === "a" ? new AC.Match("heartwood", foe, seed) : new AC.Match(foe, "heartwood", seed);
  const me = m.a.w.id === "heartwood" ? m.a : m.b, src = me === m.a ? "a" : "b";
  const blade = () => { const a = me.theta + (me.bladeSet || me.w.blades)[0] * TAU, L = me.w.reach * m.actMods.reach * me.reachMul + 6;
    const bx = me.x + Math.cos(a) * (R - 6), by = me.y + Math.sin(a) * (R - 6);
    return { mid: [bx + Math.cos(a) * L * 0.6, by + Math.sin(a) * L * 0.6], tip: [bx + Math.cos(a) * L, by + Math.sin(a) * L] }; };
  const W = []; let cur = null, step = 0;
  while (step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultRoot;
    if (Z && !cur){ const u = m.ultFx; cur = { fx: u ? u.x : null, fy: u ? u.y : null, life: u ? u.life : null, w: u ? u.w : null,
                                               atMe: !!(u && u.x === me.x && u.y === me.y), held: null, lost: null, dur: 0, at: {} }; W.push(cur); }
    if (!Z){ if (cur && cur.held === null){ cur.held = cur.dur; cur.lost = "window ended first"; } cur = null; continue; }
    cur.dur = Z.t;
    for (const T of [1, 3, 5, 7]) if (!(T in cur.at) && Z.t >= T && cur.fx !== null){
      const B = blade(); cur.at[T] = [Math.hypot(B.mid[0] - cur.fx, B.mid[1] - cur.fy), Math.hypot(B.tip[0] - cur.fx, B.tip[1] - cur.fy)]; }
    const u = m.ultFx, mine = u && u.w === "heartwood" && u.src === src;
    if (cur.held === null && !mine){ cur.held = Z.t; cur.lost = u ? "opponent's cast" : "expired"; }
  }
  return W;
}"""
res = []
with game(game_path=PAGE) as (page, errors):
    for i, foe in enumerate(FOES):
        for seed, side in ((2207 + i, "a"), (5150 + i, "b")):
            w = page.evaluate(JS, [foe, seed, side])
            assert not errors, errors[:3]
            if w is None: continue
            for x in w: x.update(foe=foe, seed=seed, side=side)
            res += w
for x in res:
    if x["held"] is None: x["held"] = x["dur"]; x["lost"] = "match ended in the window"
n = len(res)
held = sorted(x["held"] for x in res)
lost = {}
for x in res: lost[x["lost"]] = lost.get(x["lost"], 0) + 1
share = sum(min(x["held"], x["dur"]) for x in res) / max(1e-9, sum(x["dur"] for x in res))
atMe = sum(1 for x in res if x["atMe"])
print(f"{PAGE.name}: {n} Rootfast windows on {len(set(x['foe'] for x in res))} foes x 2 seeds (both sides); ultFx life at the cast: "
      f"{sorted(set(x['life'] for x in res))}; the slot's spawn point is the caster's own spot on {atMe}/{n}")
print(f"  the slot is Heartwood's for a median {held[n//2]:.2f}s of window clock (max {held[-1]:.2f}); lost to: {lost}")
print(f"  a slot-borne field could exist for {share*100:.1f}% of the window's clock")
for T in ("1", "3", "5", "7"):
    xs = [x["at"][T] for x in res if T in x["at"]]
    if not xs: continue
    md = sorted(v[0] for v in xs); tp = sorted(v[1] for v in xs)
    print(f"  t={T}s: the blade's midpoint is a median {md[len(md)//2]:.0f} units from the cast point (p90 {md[int(.9*len(md))]:.0f}); "
          f"its tip {tp[len(tp)//2]:.0f} (p90 {tp[int(.9*len(tp))]:.0f})  n={len(xs)}")
(HERE / ("fxprobe_" + PAGE.stem + ".json")).write_text(json.dumps(res, indent=1))
