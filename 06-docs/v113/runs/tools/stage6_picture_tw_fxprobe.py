"""WHY NO fx.js FIELD (v84 section 4: "Field: leaf motes off each bramble, both copies"): on real fights (a page,
undrawn, both sides), per Bramblesnare window -- how long Thornwake keeps the one ultFx slot (window clock) and why it
lost it; the ultFx life at the cast; when each bramble of the window is planted (window clock) and whether the slot was
still Thornwake's then; how far each bramble is from the point a SPECS field is drawn at; and how much of each
bramble's life falls after its window has closed. The base's SPECS.thornwake is a `fall` (not a burst), so
`drawUltOver` draws it at [u.x, u.y]: WHERE THORNWAKE STOOD AT THE CAST. A SPECS field fires ONCE, at the slot's cast
edge, and lives on that slot; the brambles are planted later, one a blow, at the struck ball, and live 6s.
usage: tw_fxprobe.py [page]. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
import idle  # noqa
from scpage import game
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (HERE / "tw-final-fx.html").resolve()
FOES = ["oathwound", "gravemourn", "grudgebearer", "lastlight", "paradox", "spellbreaker", "twinshade", "widowmaker",
        "axiom", "slagheart", "thornshear", "dawnbringer", "heartwood", "morningstar", "lightkeeper", "starwarden"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true; AC.SFX.play = function(){};
  const DT = AC.CONFIG.physics.dt;
  const m = side === "a" ? new AC.Match("thornwake", foe, seed) : new AC.Match(foe, "thornwake", seed);
  const me = m.a.w.id === "thornwake" ? m.a : m.b, src = me === m.a ? "a" : "b";
  const W = []; let cur = null, step = 0, np = 0;
  const born = new Map();
  while (step < 200 / DT && !m.over){
    m.step(DT); step++;
    const Z = me.ultBramble;
    if (Z && !cur){ const u = m.ultFx; cur = { life: u ? u.life : null, w: u ? u.w : null, fx: u ? u.x : null, fy: u ? u.y : null,
                                               held: null, lost: null, dur: 0, closeT: null, brambles: [] }; W.push(cur); }
    for (const [b, rec] of born) if (m.brambles.indexOf(b) < 0){ rec.gone = m.brambleT; born.delete(b); }
    if (!Z){ if (cur && cur.held === null){ cur.held = cur.dur; cur.lost = "window ended first"; }
             if (cur && cur.closeT === null) cur.closeT = m.brambleT;
             cur = null; np = me.brambleTally ? me.brambleTally.planted : 0; continue; }
    cur.dur = Z.t;
    const u = m.ultFx, mine = u && u.w === "thornwake" && u.src === src;
    if (cur.held === null && !mine){ cur.held = Z.t; cur.lost = u ? "opponent's cast" : "expired"; }
    const T = me.brambleTally;
    while (T && T.planted > np){
      np++;
      const G = m.brambles.filter(b => b.side === src), b = G[G.length - 1];
      if (b){ const rec = { t: +Z.t.toFixed(3), slot: cur.held === null, t0: b.t0, gone: null, win: cur,
                            dist: cur.fx === null ? null : Math.hypot(b.x - cur.fx, b.y - cur.fy) };
              cur.brambles.push(rec); born.set(b, rec); }
    }
  }
  /* each bramble's life after its window's close (the brambles' clock), cut at the match's end */
  const out = W.map(w => ({ life: w.life, w: w.w, held: w.held, lost: w.lost, dur: w.dur,
    brambles: w.brambles.map(r => { const end = r.gone !== null ? r.gone : m.brambleT, close = w.closeT !== null ? w.closeT : end;
      return { t: r.t, slot: r.slot, dist: r.dist, life: end - r.t0, after: Math.max(0, end - Math.max(close, r.t0)) }; }) }));
  return out;
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
D = [d for x in res for d in x["brambles"]]
inslot = sum(1 for d in D if d["slot"])
dist = sorted(d["dist"] for d in D if d["dist"] is not None)
ts = sorted(d["t"] for d in D)
aft = sum(d["after"] for d in D); lif = sum(d["life"] for d in D)
nod = sum(1 for x in res if not x["brambles"])
print(f"PAGE {PAGE.name}")
print(f"{n} Bramblesnare windows on {len(FOES)} foes x 2 seeds (both sides); ultFx life at the cast: {sorted(set(str(x['life']) for x in res))}; "
      f"slot's owner at the cast: {sorted(set(str(x['w']) for x in res))}")
print(f"  the slot is Thornwake's for a median {held[n//2]:.2f}s of window clock (max {held[-1]:.2f}; window 8s); lost to: {lost}")
print(f"  a slot-borne field could exist for {share*100:.1f}% of the window's clock")
print(f"  {len(D)} brambles planted in these windows ({nod} windows plant none), planted a median {q(ts, .5):.2f}s into the window "
      f"(p10 {q(ts, .1):.2f}); {inslot} of {len(D)} planted while the slot was still Thornwake's")
print(f"  a bramble is a median {q(dist, .5):.0f} units from where the field is drawn (Thornwake at the cast; p10 {q(dist, .1):.0f}, "
      f"p90 {q(dist, .9):.0f}); more than the bramble's own radius (80) away on {sum(1 for d in dist if d > 80) / max(1, len(dist)) * 100:.0f}%")
print(f"  {aft / max(1e-9, lif) * 100:.1f}% of the brambles' lives ({aft:.0f} of {lif:.0f} s) fall after their window has closed")
(HERE / "fxprobe.json").write_text(json.dumps(res, indent=1))
