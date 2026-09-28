"""BIND PICK (v103, scratch): the brief's stage 2 says "FILM a bind won". The picture is stage 6's,
so this only FINDS the window to film: Coldiron (side A, the clip's convention) against every foe,
seeds 99001.., reading won binds inside resolveClank on the final link. A window scores when it
closes on its clock with both alive, and ranks by won binds, a bind that takes the foe past 6, and
the foe's peak. Reads only; prints the top candidates with the cast's match time.
usage: bind_pick.py <link> [seeds]"""
import sys, pathlib, json
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game

JS = r"""([seeds]) => {
  const P = AC.Match.prototype, oClank = P.resolveClank, oFire = P.fireUlt, DT = AC.CONFIG.physics.dt;
  let cur = null;
  P.fireUlt = function(f, foe){
    const r = oFire.call(this, f, foe);
    if (f.w.id === "coldiron" && cur) cur.wins.push({ t0: this.t, binds: [], won: 0, past6: 0, peak: 0, close: null });
    return r;
  };
  P.resolveClank = function(A, B, hx, hy){
    const me = A.w.id === "coldiron" ? A : B.w.id === "coldiron" ? B : null;
    const foe = me === A ? B : A, s0 = foe.stacks("sunder"), open = me && !!me.ultTemper;
    const r = oClank.call(this, A, B, hx, hy);
    if (open && cur && cur.wins.length){
      const W = cur.wins[cur.wins.length - 1], s1 = foe.stacks("sunder");
      if (s1 > s0){ W.won++; if (s1 > 6 && s0 <= 6) W.past6++; W.binds.push([+this.t.toFixed(2), s0, s1]); }
    }
    return r;
  };
  const out = [];
  const foes = AC.WEAPONS.map(w => w.id).filter(i => i !== "coldiron");
  for (const fid of foes) for (const sd of seeds){
    const m = new AC.Match("coldiron", fid, sd);
    cur = { wins: [] };
    let open = false, steps = 0;
    while (!m.over && steps < 160 / DT){
      m.step(DT); steps++;
      const W = cur.wins[cur.wins.length - 1];
      if (W && m.a.ultTemper) W.peak = Math.max(W.peak, m.b.stacks("sunder"));
      if (open && !m.a.ultTemper && W && W.close === null) W.close = { t: +m.t.toFixed(2), alive: m.a.alive && m.b.alive };
      open = !!m.a.ultTemper;
    }
    for (const W of cur.wins) if (W.close && W.close.alive)
      out.push({ foe: fid, seed: sd, at: +W.t0.toFixed(2), close: W.close.t, won: W.won, past6: W.past6, peak: W.peak,
                 binds: W.binds, winner: m.winner ? m.winner.w.id : null });
  }
  P.resolveClank = oClank; P.fireUlt = oFire;
  out.sort((x, y) => (y.past6 - x.past6) || (y.won - x.won) || (y.peak - x.peak));
  return out.slice(0, 12);
}"""

link = pathlib.Path(sys.argv[1]).resolve()
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
with game(game_path=link) as (page, errors):
    R = page.evaluate(JS, [[99001 + 7 * i for i in range(n)]])
    assert not errors, errors
print(f"BIND PICK on {link.name}: Coldiron side A, every foe x {n} seeds; windows that close on their clock")
for r in R:
    print(f"  coldiron v {r['foe']:<13} seed {r['seed']}  cast at {r['at']:6.2f}  close {r['close']:6.2f}  "
          f"won binds {r['won']}  past 6 by a bind {r['past6']}  foe peak {r['peak']}  winner {r['winner']}  binds {r['binds']}")
