"""A portrait of every relic for the trailer's 7x7 wall: the game's own renderer, one frame after
0.5 s of a fight, name tag blanked, framed toward the weapon. The 41 in GAME from GAME; the 8
only on the design batch's line from its tip -- trailer_gfx.MYSTERY draws those 8 dark with a
question mark, because Rick has not passed them yet.
"""
import sys, base64, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scpage import game, resolve_game
OUT = pathlib.Path(__file__).resolve().parent.parent / '07-shorts' / 'worldcup-trailer' / 'portraits'
OUT.mkdir(parents=True, exist_ok=True)
JS = r"""
([id, foe, S, theta]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const mm = new AC.Match(id, foe, 20260817);
  mm.introT = 0; AC.__inject(mm);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  while (mm.t < 0.5) mm.step(AC.CONFIG.physics.dt);
  const r = AC.renderer, cv = document.getElementById('cv');
  const clean = (f) => { f.status = {}; f.ringFlash = 0; f.mend = 0; f.stun = 0; f.flash = 0; f.vx = 0; f.vy = 0; f.trail = []; };
  mm.shake = 0; mm.hitStop = 0; mm.banner = null; mm.floats = []; mm.sparks = []; mm.fx = []; mm.rings = [];
  const f = mm.a, g = mm.b; clean(f); clean(g);
  const aw = r.aw !== undefined ? null : null;
  const cx = AC.CONFIG.arena ? AC.CONFIG.arena.w / 2 : 265, cy = AC.CONFIG.arena ? AC.CONFIG.arena.h / 2 : 400;
  f.theta = theta; f.x = cx; f.y = cy;
  g.x = -4000; g.y = -4000;
  const shot = () => {
    const dx = r.pad + f.x * r.scale + Math.cos(theta) * 120, dy = r.arenaTop + f.y * r.scale + Math.sin(theta) * 120;
    const t = document.createElement('canvas'); t.width = S; t.height = S;
    t.getContext('2d').drawImage(cv, Math.round(dx - S/2), Math.round(dy - S/2), S, S, 0, 0, S, S);
    return t.toDataURL('image/png').slice(22);
  };
  const nm = f.w.name; f.w.name = ''; AC.__draw(mm); const a = shot(); f.w.name = nm;
  const b = a;
  return {a, b, aff: f.w.aff, name: f.w.name, shape: f.w.shape, ult: f.w.ult.name, cx, cy, scale: r.scale};
}"""
builds = {'game': '../02-chain/sc-nightglass-fx.html', 'batch': '../02-chain/sc-aureole-fxout.html'}
meta = {}
for tag, g in builds.items():
    with game(game_path=resolve_game(g)) as (page, errs):
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        if tag == 'batch':
            ids = [i for i in ids if i not in meta]
        for rid in ids:
            foe = 'axiom' if rid != 'axiom' else 'heartwood'
            res = page.evaluate(JS, [rid, foe, 720, -0.9])
            (OUT / f'{rid}.png').write_bytes(base64.b64decode(res['a']))
            meta[rid] = {kk: res[kk] for kk in ('aff', 'name', 'shape', 'ult')} | {'build': tag}
        assert not errs, errs[:3]
        print(tag, len(ids), res['cx'], res['cy'], res['scale'])
json.dump(meta, open(OUT / 'meta.json', 'w'), indent=1)
SCHOOLS = ['sanctified', 'bloodsworn', 'dwarven', 'verdant', 'umbral', 'runic', 'vigil']
SHAPES = ['greatsword', 'twinblade', 'warhammer', 'scythe', 'flail', 'bow', 'staff']
grid = {f'{s}|{w}': next((r for r, v in meta.items() if v['aff'] == s and v['shape'] == w), None)
        for s in SCHOOLS for w in SHAPES}
missing = [k for k, v in grid.items() if v is None]
assert not missing, f'cells with no relic: {missing}'
json.dump(grid, open(OUT / 'grid.json', 'w'), indent=1)
print(len(meta), 'relics, 49 cells filled')
