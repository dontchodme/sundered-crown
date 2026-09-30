"""The instrument, not the record (trailer_clips.JOBS is the record). How the trailer's fights were picked: for each relic, the cast with the most damage dealt in
the 3 s after it (cast between 4 s and 40 s, foe alive at +3 s), against foes whose ultimate
the design batch does not change. Also lists fights the ultimate finishes (KILL). GAME build.
"""
import pathlib
import sys, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scpage import game, resolve_game
JS = r"""([hero, foes, seeds]) => {
  const DT = AC.CONFIG.physics.dt, out = [];
  for (const foe of foes) for (const sd of seeds) for (const side of [0,1]) {
    const m = side ? new AC.Match(foe, hero, sd) : new AC.Match(hero, foe, sd);
    const me = m.a.w.id === hero ? m.a : m.b, th = me === m.a ? m.b : m.a;
    let fm = 0, ft = 0, casts = [], fc = [], i = 0;
    while (!m.over && i < 120 / DT) {
      m.step(DT); i++;
      if (me.ultsFired > fm) { fm = me.ultsFired; casts.push({t: m.t, hp: th.hp}); }
      if (th.ultsFired > ft) { ft = th.ultsFired; fc.push(+m.t.toFixed(2)); }
      for (const c of casts) if (c.d3 === undefined && m.t >= c.t + 3.0) c.d3 = c.hp - th.hp;
    }
    for (const c of casts) if (c.d3 === undefined) c.d3 = c.hp - th.hp;
    out.push({hero, foe, seed: sd, side, dur: +m.t.toFixed(2), winner: m.winner ? m.winner.w.id : null,
      casts: casts.map(c => ({t: +c.t.toFixed(2), d3: +c.d3.toFixed(1)})), foecasts: fc});
  }
  return out;
}"""
PLAN = {
 'culverin': ['spellbreaker','farwarden','foregone'],
 'crozier': ['oathwound','foregone','nightfell'],
 'bloodmirror': ['spellbreaker','foregone','heartwood'],
 'lastlight': ['oathwound','nightfell','redflail'],
 'paradox': ['emberedge','farwarden','heartwood'],
 'briarwand': ['oathwound','bulwarden','redflail'],
 'ravelbone': ['spellbreaker','foregone','heartwood'],
 'duskreave': ['emberedge','grudgebearer','heartwood'],
 'gloamwire': ['emberedge','grudgebearer','heartwood'],
}
seeds = [7700001 + 7919 * i for i in range(6)]
rows = []
with game(game_path=resolve_game('../02-chain/sc-nightglass-fx.html')) as (page, errs):
    for h, foes in PLAN.items():
        rows += page.evaluate(JS, [h, foes, seeds])
    assert not errs, errs[:3]
pass
def clear(r, t0, t1):  # foe ult not cast within 4s before or during the window
    return all(not (t0 - 4.0 <= f <= t1) for f in r['foecasts'])
for h in PLAN:
    L = []; K = []
    for r in rows:
        if r['hero'] != h: continue
        for c in r['casts']:
            if 4 <= c['t'] <= 40 and c['t'] + 3 < r['dur'] and clear(r, c['t'], c['t'] + 2.6):
                L.append((c['d3'], r['foe'], r['seed'], r['side'], c['t']))
            g = r['dur'] - c['t']
            if 0.8 <= g <= 2.6 and r['winner'] == h and clear(r, c['t'], r['dur']):
                K.append((round(g, 2), r['foe'], r['seed'], r['side'], c['t'], r['dur']))
    L.sort(reverse=True)
    print(h, 'MID', L[:3]); print(h, 'KILL', K[:4])
