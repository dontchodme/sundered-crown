"""WHY NO NEW fx.js FIELD (v70 section 6.1: "Field spec: rune motes along the lit walls, both copies"): on real
fights (the base link, undrawn, both sides), per Rebuttal window -- how long Lodestone keeps the one ultFx slot
(window clock) and why it lost it; the window clock of every touch and whether the slot was still Lodestone's
(a SPECS field fires ONCE, at the slot's cast edge, key = w|src, round the slot's (x, y) = where the caster
stood); how far each touch's wall point is from that spawn point; and how much of the lit walls' length lies
within the slot's 300-unit spawn radius at the cast. usage: ld_fxprobe.py [page] -> fxprobe.json / stdout."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
BASE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (HERE.parent / "links" / "sc-lodestone-b205.html").resolve()
FOES = ["aureole", "gravemourn", "grudgebearer", "lastlight", "paradox", "spellbreaker", "twinshade", "widowmaker",
        "axiom", "slagheart", "thornshear", "dawnbringer", "heartwood", "morningstar", "lightkeeper", "starwarden"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true; AC.SFX.play = function(){};
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
  const me = m.a.w.id === "lodestone" ? m.a : m.b, th = me === m.a ? m.b : m.a, src = me === m.a ? "a" : "b";
  const W = []; let cur = null, step = 0, seen = 0;
  const perimIn = (x, y, n, rad) => {           // share of the live hall's walls within rad of (x, y)
    const x0 = n, y0 = n, x1 = A.w - n, y1 = A.h - n; let tot = 0, inn = 0;
    const seg = (ax, ay, bx, by) => { const L = Math.hypot(bx - ax, by - ay), N = Math.ceil(L / 4);
      for (let i = 0; i < N; i++){ const s = (i + 0.5) / N, px = ax + (bx - ax) * s, py = ay + (by - ay) * s;
        tot++; if (Math.hypot(px - x, py - y) <= rad) inn++; } };
    seg(x0, y0, x1, y0); seg(x1, y0, x1, y1); seg(x1, y1, x0, y1); seg(x0, y1, x0, y0);
    return inn / tot; };
  let pre = null;
  const tr = m.tickRunes;                       // the foe's spot at the touch test (read, never written)
  m.tickRunes = function(dt){ const p = [th.x, th.y]; const k0 = me.runeTally ? me.runeTally.touches : 0;
    tr.call(this, dt); if (me.runeTally && me.runeTally.touches > k0) pre = p; };
  while (step < 200 / DT && !m.over){
    pre = null;
    m.step(DT); step++;
    const Z = me.ultRunes, T = me.runeTally;
    if (Z && !cur){ const u0 = m.ultFx, u = u0 && u0.w === "lodestone" && u0.src === src ? u0 : null; const n = m.inset || 0;
      cur = { fx: u ? u.x : null, fy: u ? u.y : null, life: u ? u.life : null, w: u ? u.w : null,
              atMe: u ? (u.x === me.x && u.y === me.y) : false, held: null, lost: null, touches: [], dur: 0,
              slotW: u0 ? u0.w + "|" + u0.src + "|" + u0.kind : null,
              perim300: u ? perimIn(u.x, u.y, n, u.radius || 300) : null, rad: u ? u.radius : null,
              nearWall: Math.min(me.x - n, A.w - n - me.x, me.y - n, A.h - n - me.y) };
      W.push(cur); }
    const k = T ? T.touches : 0;
    if (k > seen && cur && pre){
      const n = m.inset || 0, e = me.w.ult.pad, x = pre[0], y = pre[1];
      const walls = [];
      if (y <= n + R + e) walls.push([Math.min(A.w - n, Math.max(n, x)), n]);
      if (x >= A.w - n - R - e) walls.push([A.w - n, Math.min(A.h - n, Math.max(n, y))]);
      if (y >= A.h - n - R - e) walls.push([Math.min(A.w - n, Math.max(n, x)), A.h - n]);
      if (x <= n + R + e) walls.push([n, Math.min(A.h - n, Math.max(n, y))]);
      for (const p of walls) cur.touches.push({ t: Z ? Z.t : cur.dur, dC: Math.hypot(p[0] - cur.fx, p[1] - cur.fy), inSlot: cur.held === null });
    }
    seen = k;
    if (!Z){ if (cur && cur.held === null){ cur.held = cur.dur; cur.lost = "window ended first"; } cur = null; continue; }
    cur.dur = Z.t;
    const u = m.ultFx, mine = u && u.w === "lodestone" && u.src === src;
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
B = [b for x in res for b in x["touches"]]
Bd = [b for x in res if x["fx"] is not None for b in x["touches"]]
bt = sorted(b["t"] for b in B); dc = sorted(b["dC"] for b in Bd)
ins = sum(1 for b in B if b["inSlot"])
q = lambda a, p: a[min(len(a) - 1, int(p * len(a)))] if a else float("nan")
pr = sorted(x["perim300"] for x in res if x["perim300"] is not None)
print(f"  (the slot was not Lodestone's on the cast's own step in {sum(1 for x in res if x['fx'] is None)} windows: no spawn point; held by {sorted(set(x['slotW'] for x in res if x['fx'] is None))})")
nw = sorted(x["nearWall"] for x in res)
print(f"{n} Rebuttal windows on {len(FOES)} foes x 2 seeds (both sides); ultFx life at the cast: {sorted(set(x['life'] for x in res if x['life'] is not None))} "
      f"(half-seconds); radius {sorted(set(x['rad'] for x in res if x['rad'] is not None))}; the slot's spawn point is the caster's own spot on {sum(1 for x in res if x['atMe'])}/{n}")
print(f"  the slot is Lodestone's for a median {held[n//2]:.2f}s of window clock (max {held[-1]:.2f}); lost to: {lost}")
print(f"  a slot-borne field could exist for {share*100:.1f}% of the window's clock")
print(f"  the caster stands a median {q(nw, .5):.0f} units from its nearest wall at the cast (p10 {q(nw, .1):.0f}, p90 {q(nw, .9):.0f})")
print(f"  the share of the lit walls' length within the slot's spawn radius of the cast point: median {q(pr, .5)*100:.0f}% (p10 {q(pr, .1)*100:.0f}%, p90 {q(pr, .9)*100:.0f}%)")
print(f"  {len(B)} wall points touched: window clock median {q(bt, .5):.2f}s (p10 {q(bt, .1):.2f}); {ins} of {len(B)} while the slot was "
      f"still Lodestone's (a SPECS field would already be spawned: it fires once, at the cast edge)")
print(f"  a touched wall point is a median {q(dc, .5):.0f} units from the field's spawn point (p10 {q(dc, .1):.0f}, p90 {q(dc, .9):.0f})")
(HERE / "fxprobe.json").write_text(json.dumps(res, indent=1))
