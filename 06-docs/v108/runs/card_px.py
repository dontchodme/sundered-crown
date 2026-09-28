"""v108 §0 reading 13: the card MEASURED IN PIXELS (v83 §4: "trim at build to <=72; measure in pixels")
on the two surfaces an ult tip is drawn on, with the page's own fonts and code:
  the ult bar (drawBar): 500 18px 'Atkinson Hyperlegible Next', wrapped in tw = W/2 - tx - 12, 2 lines drawn
  the scrunch panel (_panelFacts -> _scrunchWrap(tip, colW - 14, 21, 3)): shrinks 21 -> 15px to fit 3 lines
Every relic's tip on the link, and the design's 74-character first line beside its 68-character alternate."""
import json, pathlib, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from scpage import game
JS = r"""async (extra) => {
  const FACE = "500 18px 'Atkinson Hyperlegible Next'";
  await document.fonts.load(FACE); await document.fonts.ready;
  const loaded = document.fonts.check(FACE);
  AC.setResolution(1080, 1920);
  const R = AC.renderer, c = R.ctx, W = R.W;
  const pad = 34, SR = 42, tx = pad + SR * 2 + 20, half = W / 2, tw = Math.abs(half - tx) - 12;
  const colW = ((W - 48) - 22 * 2 - 26) / 2;
  const bar = (tip) => { c.save(); c.font = "500 18px 'Atkinson Hyperlegible Next',sans-serif";
    const words = tip.split(" "), lines = []; let ln = "";
    for (const w of words){ const t2 = ln ? ln + " " + w : w;
      if (c.measureText(t2).width > tw && ln){ lines.push(ln); ln = w; } else ln = t2; }
    if (ln) lines.push(ln);
    const widest = Math.max(...lines.map(l => c.measureText(l).width));
    const one = c.measureText(tip).width; c.restore();
    return { lines: lines.length, widest: Math.round(widest), one: Math.round(one) }; };
  const scr = (tip) => { const r = R._scrunchWrap(tip, colW - 14, 21, 3); return { size: r.size, lines: r.lines.length }; };
  const rows = AC.WEAPONS.map(w => ({ id: w.id, chars: (w.ult.tip || "").length, bar: bar(w.ult.tip || ""), scr: scr(w.ult.tip || "") }));
  const ex = extra.map(t => ({ id: "(design) " + t.length + "ch", chars: t.length, bar: bar(t), scr: scr(t), tip: t }));
  return { loaded, W, tw, colW, rows, ex };
}"""
g = pathlib.Path(sys.argv[1]).resolve()
extra = ["Iron hail: bolts drop from above onto the foe; each one that lands sunders",
         "Iron hail falls on the foe from above; every bolt that lands sunders"]
with game(game_path=g) as (page, errors):
    r = page.evaluate(JS, extra)
    assert not errors, errors
if not r["loaded"]:
    raise SystemExit("REFUSING TO REPORT -- Atkinson Hyperlegible Next did not load")
print(f"CARD IN PIXELS -- {g.name}   W {r['W']}   ult bar: 18px Atkinson, wrap width {r['tw']}px, 2 lines drawn   "
      f"scrunch: 21px ui-sans, wrap width {r['colW'] - 14:.0f}px, 3 lines, shrinks to 15")
rows = sorted(r["rows"], key=lambda x: -x["bar"]["one"])
print(f"  {'relic':<14}{'chars':>6}{'one line px':>12}{'bar lines':>10}{'widest':>8}{'scrunch px':>11}{'lines':>6}")
for x in rows + r["ex"]:
    flag = "  <-- dropped a line" if x["bar"]["lines"] > 2 else ""
    print(f"  {x['id']:<14}{x['chars']:>6}{x['bar']['one']:>12}{x['bar']['lines']:>10}{x['bar']['widest']:>8}{x['scr']['size']:>11}{x['scr']['lines']:>6}{flag}")
ih = next(x for x in r["rows"] if x["id"] == "ironhail")
print(f"\n  ironhail's card: {ih['chars']} chars, {ih['bar']['one']}px on one line, {ih['bar']['lines']} lines in the ult bar "
      f"(nothing dropped: {ih['bar']['lines'] <= 2}), the scrunch at {ih['scr']['size']}px in {ih['scr']['lines']} lines; "
      f"rank {1 + [x['id'] for x in rows].index('ironhail')} of {len(rows)} by width")
