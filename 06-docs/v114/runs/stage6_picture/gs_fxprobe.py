"""WHY NO NEW fx.js FIELD (v81 section 4: "Field: blood motes off the blade, both copies"): on real fights (the
base link, undrawn, both sides), per Bloodprice window -- how long Goreshard keeps the one ultFx slot (window
clock) and why it lost it (a SPECS field fires ONCE, at the slot's cast edge, key = w|src, from the slot's own
points: x/y the caster where it cast, tx/ty the foe then -- a 'burst' is drawn at the foe, a 'beam' between
them); and where the blade is for the rest of the window: its middle's distance from both of those points,
sampled every 0.1s of window clock, and how far it turns. usage: gs_fxprobe.py [page]. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (HERE.parent / "links" / "sc-goreshard-b10.25.html").resolve()
FOES = ["aureole", "gravemourn", "grudgebearer", "lastlight", "paradox", "spellbreaker", "twinshade", "widowmaker",
        "axiom", "slagheart", "thornshear", "dawnbringer", "heartwood", "morningstar", "ironhail", "lightkeeper"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true; AC.SFX.play = function(){};
  const DT = AC.CONFIG.physics.dt;
  const m = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me = m.a.w.id === "oathwound" ? m.a : m.b, src = me === m.a ? "a" : "b", RB = AC.CONFIG.physics.ballR;
  const W = []; let cur = null, step = 0, nextS = 0;
  while (step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultPrice;
    if (Z && !cur){ const u = m.ultFx;
      cur = { mine: !!(u && u.w === "oathwound" && u.src === src), life: u ? u.life : null,
              p: u ? [u.x, u.y] : null, q: u ? [u.tx, u.ty] : null, held: null, lost: null, dP: [], dQ: [], th: [], dur: 0 };
      W.push(cur); nextS = 0; }
    if (!Z){ if (cur && cur.held === null){ cur.held = cur.dur; cur.lost = "window ended first"; } cur = null; continue; }
    cur.dur = Z.t;
    const u = m.ultFx, mine = u && u.w === "oathwound" && u.src === src;
    if (cur.held === null && !mine){ cur.held = Z.t; cur.lost = u ? "opponent's cast" : "expired"; }
    if (Z.t >= nextS && cur.p){
      nextS += 0.1;
      const reach = me.w.reach * m.actMods.reach * me.reachMul, rm = RB - 6 + (reach + 6) * 0.6;
      const cx = me.x + Math.cos(me.theta) * rm, cy = me.y + Math.sin(me.theta) * rm;
      cur.dP.push(Math.hypot(cx - cur.p[0], cy - cur.p[1])); cur.dQ.push(Math.hypot(cx - cur.q[0], cy - cur.q[1]));
      cur.th.push(me.theta);
    }
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
q = lambda a, p: a[min(len(a) - 1, int(p * len(a)))] if a else float("nan")
after = lambda x, key: [d for d, k in zip(x[key], range(len(x[key]))) if k * 0.1 >= x["held"]]
dP = sorted(d for x in res for d in after(x, "dP")); dQ = sorted(d for x in res for d in after(x, "dQ"))
import math
spans = []
for x in res:
    t = x["th"]
    if len(t) > 2:
        un = [t[0]]
        for v in t[1:]:
            d = (v - un[-1] + math.pi) % (2 * math.pi) - math.pi; un.append(un[-1] + d)
        spans.append(max(un) - min(un))
spans.sort()
print(f"{n} Bloodprice windows on {len(FOES)} foes x 2 seeds (both sides); ultFx life at the cast: {sorted(set(x['life'] for x in res))}; "
      f"the slot was Goreshard's at the cast on {sum(1 for x in res if x['mine'])}/{n}")
print(f"  the slot is Goreshard's for a median {held[n//2]:.2f}s of window clock (max {held[-1]:.2f}; the window is 8s); lost to: {lost}")
print(f"  a slot-borne field could exist for {share*100:.1f}% of the window's clock")
print(f"  after the slot is gone, the blade's middle is a median {q(dP, .5):.0f} units from the cast point (p10 {q(dP, .1):.0f}, p90 {q(dP, .9):.0f}) "
      f"and {q(dQ, .5):.0f} from the foe's point, where a 'burst' is drawn (p10 {q(dQ, .1):.0f}, p90 {q(dQ, .9):.0f}); {len(dP)} samples")
print(f"  the blade turns through a median {q(spans, .5):.2f} rad over a window (p10 {q(spans, .1):.2f}, p90 {q(spans, .9):.2f})")
(HERE / "fxprobe.json").write_text(json.dumps(res, indent=1))
