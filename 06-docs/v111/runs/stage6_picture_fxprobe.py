"""WHY NO NEW fx.js FIELD (v79 section 4: "Field: rune motes off the blades, both copies"): on real fights
(au-final-fx, undrawn, both sides), per Unmaking window -- how long Spellbreaker keeps the one ultFx slot (window clock)
and why it lost it; the ultFx life at the cast; and how far her centre (the blades ride her) is from
the point a SPECS field would spawn at (the slot's x, y: where she cast), over the window's clock. A SPECS field fires
ONCE, at the slot's cast edge, keyed w|src, at the slot's (x, y), and lives on that slot; the blades it would decorate
ride her for 8s (their tips ~96 units out). usage: fxprobe.py [page]. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (HERE / "sb-final-fx.html").resolve()
FOES = ["oathwound", "gravemourn", "grudgebearer", "lastlight", "paradox", "aureole", "twinshade", "widowmaker",
        "axiom", "slagheart", "thornshear", "dawnbringer", "heartwood", "morningstar", "lightkeeper", "starwarden"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true; AC.SFX.play = function(){};
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR;
  const m = side === "a" ? new AC.Match("spellbreaker", foe, seed) : new AC.Match(foe, "spellbreaker", seed);
  const me = m.a.w.id === "spellbreaker" ? m.a : m.b, src = me === m.a ? "a" : "b";
  const W = []; let cur = null, step = 0;
  while (step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultUnmake;
    if (Z && !cur){ const u = m.ultFx; cur = { life: u ? u.life : null, w: u ? u.w : null, fx: u ? u.x : me.x, fy: u ? u.y : me.y,
                                               held: null, lost: null, dur: 0, d: [], slotT: [] }; W.push(cur); }
    if (!Z){ if (cur && cur.held === null){ cur.held = cur.dur; cur.lost = "window ended first"; } cur = null; continue; }
    cur.dur = Z.t;
    const u = m.ultFx, mine = u && u.w === "spellbreaker" && u.src === src;
    if (cur.held === null && !mine){ cur.held = Z.t; cur.lost = u ? "opponent's cast" : "expired"; }
    if (step % 12 === 0) cur.d.push([+Z.t.toFixed(2), Math.hypot(me.x - cur.fx, me.y - cur.fy)]);
  }
  return W;
}"""
res = []
with game(game_path=PAGE) as (page, errors):
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
D = sorted(d for x in res for t, d in x["d"]); D1 = sorted(d for x in res for t, d in x["d"] if t >= 1)
far = sum(1 for d in D1 if d > 96) / max(1, len(D1))
print(f"{n} Unmaking windows on {len(FOES)} foes x 2 seeds (both sides); ultFx life at the cast: {sorted(set(str(x['life']) for x in res))}")
print(f"  the slot is Spellbreaker's for a median {held[n//2]:.2f}s of window clock (max {held[-1]:.2f}; window 8s); lost to: {lost}")
print(f"  a slot-borne field could exist for {share*100:.1f}% of the window's clock")
print(f"  her centre (the blades' hub) is a median {q(D,.5):.0f} units from the field's spawn point (p10 {q(D,.1):.0f}, p90 {q(D,.9):.0f}); "
      f"after the first second median {q(D1,.5):.0f} (p90 {q(D1,.9):.0f}); more than a blade's tip (96) away on {far*100:.0f}% of those samples")
(HERE / "fxprobe.json").write_text(json.dumps(res, indent=1))
