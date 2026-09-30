"""ONE FIGHT WATCHED, frame by frame, at the app's size (453x805, chain on, shake as played, Math.random pinned
per frame so the page's own cosmetic randomness is repeatable): the whole fight at 2 fps, then her first and last
windows at 8 fps from 0.3s before the cast to 0.6s after the close, and the kill through 3s of verdict at 8 fps.
Writes watch/<tag>_*.png montages + watch/<tag>.json (per frame: t, window, fade, snap, stacks, stop, over,
hp). usage: watch.py page foe seed side tag. SCRATCH."""
import sys, base64, pathlib, json, io
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]); PAGE = PAGE if PAGE.is_absolute() else HERE / PAGE
FOE, SEED, SIDE, TAG = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
OUT = HERE / "watch"; OUT.mkdir(exist_ok=True)
JS = r"""([foe, seed, side]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(453, 805); AC.SFX.play = function(){}; AC.SFX.resume = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, cv = document.getElementById("cv");
  const m = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me = m.a.w.id === "oathwound" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  /* pass 1: where are its windows and the kill (a dry run on a twin match; the sim is deterministic) */
  const m0 = side === "a" ? new AC.Match("oathwound", foe, seed) : new AC.Match(foe, "oathwound", seed);
  const me0 = m0.a.w.id === "oathwound" ? m0.a : m0.b;
  const wins = []; let st = 0, prev = null, overAt = -1;
  while (st < 200 / DT){ m0.step(DT); st++;
    if (me0.ultPrice && !prev) wins.push([st, null]);
    if (!me0.ultPrice && prev) wins[wins.length - 1][1] = st;
    prev = me0.ultPrice;
    if (m0.over && overAt < 0) overAt = st;
    if (overAt >= 0 && st - overAt > 3 / DT) break; }
  for (const w of wins) if (w[1] === null) w[1] = overAt;
  const want = (s) => {
    if (s % 60 === 0) return "all";
    const dense = wins.length > 1 ? [wins[0], wins[wins.length - 1]] : wins;   // its first window and its last
    for (const [a, b] of dense) if (s >= a - 36 && s <= b + 72 && s % 15 === 0) return "win";
    if (overAt >= 0 && s >= overAt - 24 && s % 15 === 0) return "kill";
    return null; };
  const frames = []; let s = 0, thrown = null;
  while (s < st){
    m.step(DT); s++;
    const k = want(s); if (!k) continue;
    try { Math.random = pin(s * 7919); AC.__draw(m); } catch (e){ thrown = String(e.stack || e); Math.random = realRandom; break; }
    Math.random = realRandom;
    frames.push({ k, s, t: +m.t.toFixed(2), png: cv.toDataURL("image/png"), win: !!me.ultPrice, fade: +(me.goreFade || 0).toFixed(2),
                  age: +(me.goreAge || 0).toFixed(2), snap: +(me.goreOut || 0).toFixed(2), glow: +(me.goreGlow || 0).toFixed(2),
                  stk: th.stacks("hemorrhage"), stop: m.hitStop > 0, over: m.over, hp: +me.hp.toFixed(1), fhp: +th.hp.toFixed(1),
                  dr: me.priceTally ? me.priceTally.blows : 0 });
  }
  return { wins, overAt, steps: st, thrown, frames, winner: m.summary().winner };
}"""
with game(game_path=PAGE) as (page, errors):
    r = page.evaluate(JS, [FOE, SEED, SIDE])
    assert not errors, errors[:5]
print(f"{TAG}: windows (steps) {r['wins']} over at {r['overAt']} winner {r['winner']} thrown {r['thrown']} frames {len(r['frames'])}")
meta = []
groups = {"all": [], "win": [], "kill": []}
for f in r["frames"]:
    im = Image.open(io.BytesIO(base64.b64decode(f.pop("png").split(",", 1)[1]))).convert("RGB")
    t = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    d = ImageDraw.Draw(t)
    d.rectangle((0, 0, t.width, 26), fill=(0, 0, 0))
    d.text((3, 1), f"t{f['t']} {'WIN' if f['win'] else ''} f{f['fade']} a{f['age']} out{f['snap']} g{f['glow']}", fill=(255, 255, 0))
    d.text((3, 13), f"stk{f['stk']} {'STOP' if f['stop'] else ''} {'OVER' if f['over'] else ''} hp{f['hp']} foe{f['fhp']} pb{f['dr']}", fill=(255, 255, 0))
    groups[f["k"]].append(t); meta.append(f)
for k, ims in groups.items():
    if not ims: continue
    cols = 8
    for part in range(0, len(ims), 32):
        chunk = ims[part:part + 32]
        rows = (len(chunk) + cols - 1) // cols
        sh = Image.new("RGB", (cols * chunk[0].width, rows * chunk[0].height))
        for i, t in enumerate(chunk): sh.paste(t, ((i % cols) * t.width, (i // cols) * t.height))
        sh.save(OUT / f"{TAG}_{k}_{part // 32}.png")
(OUT / f"{TAG}.json").write_text(json.dumps({k: v for k, v in r.items() if k != "frames"} | {"frames": meta}, indent=0))
print("montages:", sorted(p.name for p in OUT.glob(f"{TAG}_*.png")))
