"""Which keys of SHAPES does DRAWING write, over the probe's whole drawn subset (every foe, both sides, the
first seed 107001, drawn through the renderer every 30th step and 0.5s past the end), on the link given?
Prints, per SHAPES key that moved against the run's start: the first fight that moved it and the kind of
value. Run on the base link (no stage 6) and on the stage-6 link: the renderer's memos move alike."""
import json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
JS = r"""([seed, every]) => {
  window.__frozen = true; AC.setResolution(270, 480); if (AC.POSTFX) AC.POSTFX.on = false;
  const js = v => { try { return JSON.stringify(v); } catch (e) { return "<unserialisable " + e.message + ">"; } };
  const start = {}; for (const k of Object.keys(AC.SHAPES)) start[k] = js(AC.SHAPES[k]);
  const first = {}, ids = AC.WEAPONS.map(w => w.id).filter(i => i !== "lightkeeper");
  for (const foe of ids) for (const side of [0, 1]){
    const m = side ? new AC.Match(foe, "lightkeeper", seed) : new AC.Match("lightkeeper", foe, seed);
    let n = 0; while (!m.over && n < 160 * 120){ m.step(1 / 120); n++; if (n % every === 0) AC.__draw(m); }
    for (let k = 0; k < 61; k++){ m.step(1 / 120); if (k % 10 === 0) AC.__draw(m); }
    for (const k of Object.keys(AC.SHAPES)) if (!(k in first) && js(AC.SHAPES[k]) !== start[k]) first[k] = `${foe} (side ${side ? "B" : "A"})`;
    for (const k of Object.keys(start)) if (!(k in AC.SHAPES) && !(k in first)) first[k] = `DELETED at ${foe}`;
  }
  const out = {}; for (const k of Object.keys(first)){ const v = AC.SHAPES[k];
    out[k] = [first[k], typeof v, v && typeof v === "object" ? Object.keys(v).length + " entries" : String(v).slice(0, 40), typeof AC.SHAPES[k] === "function"]; }
  return { moved: out, keys: Object.keys(AC.SHAPES).length, fns: Object.keys(AC.SHAPES).filter(k => typeof AC.SHAPES[k] === "function").length };
}"""
for g in sys.argv[1:]:
    with game(game_path=pathlib.Path(g).resolve()) as (page, errors):
        R = page.evaluate(JS, [107001, 30])
        assert not errors, errors[:3]
    print(pathlib.Path(g).name, f"SHAPES has {R['keys']} keys ({R['fns']} functions); moved by drawing:")
    for k, v in R["moved"].items():
        print(f"   {k:<22} first moved in the fight with {v[0]:<24} {v[1]:<8} {v[2]}")
