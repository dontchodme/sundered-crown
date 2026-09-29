"""Which part of SHAPES does a drawn frame write? Base link vs stage-6 link, one fight drawn."""
import sys, pathlib, json
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
JS = r"""() => {
  const snap = () => { const o = {}; for (const k of Object.keys(AC.SHAPES)) o[k] = JSON.stringify(AC.SHAPES[k]); return o; };
  window.__frozen = true; AC.setResolution(270, 480);
  const s0 = snap();
  const m = new AC.Match("lightkeeper", "gloamwire", 107001);
  for (let i = 0; i < 3000 && !m.over; i++){ m.step(1/120); if (i % 50 === 0) AC.__draw(m); }
  const s1 = snap(), out = [];
  for (const k of Object.keys(s1)) if (s0[k] !== s1[k]){
    const a = JSON.parse(s0[k] || "{}"), b = JSON.parse(s1[k]);
    const keys = [...new Set([...Object.keys(a || {}), ...Object.keys(b || {})])].filter(x => JSON.stringify(a && a[x]) !== JSON.stringify(b && b[x]));
    out.push([k, keys, keys.map(x => String(JSON.stringify(b[x])).slice(0, 120))]); }
  return out; }"""
for g in sys.argv[1:]:
    with game(game_path=pathlib.Path(g).resolve()) as (page, errors):
        print(pathlib.Path(g).name, json.dumps(page.evaluate(JS)))
