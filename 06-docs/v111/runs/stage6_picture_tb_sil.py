"""THE SILHOUETTE: the resting twinblade of every twinblade relic at the app's 453x805, chain on: the weapon's own
contrast |dL| (pixels that change when that fighter's weapon is not drawn, outside its ball), its mean
luma and area. 8 frames a relic (t 2.5..6.5, out of any hit stop / flash / cast), foe Grudgebearer,
seed 4242, the relic as side A. Writes a strip of crops. usage: bow_sil.py page out.json. SCRATCH."""
import sys, json, base64, io, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
PAGE = pathlib.Path(sys.argv[1]) if pathlib.Path(sys.argv[1]).is_absolute() else HERE / sys.argv[1]
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "bow_sil.json"
import os
IDS = os.environ.get("SIL_IDS", "spellbreaker,widowmaker,twinshade,thornshear,starwarden").split(",")
JS = r"""([id, seed]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(453, 805); AC.SFX.play = function(){}; AC.SFX.resume = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = new AC.Match(id, "grudgebearer", seed), me = m.a, th = m.b;
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const frame = (noW) => { const dw = r.drawWeapon;
    if (noW) r.drawWeapon = function(mm, f){ if (f === me) return; return dw.call(this, mm, f); };
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    try { AC.__draw(m); } finally { Math.random = realRandom; m.shake = ks; r.drawWeapon = dw; }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data); };
  const L = (d, i) => (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
  const out = [], K = r.k * r.scale, R = AC.CONFIG.physics.ballR;
  let step = 0, n = 0, crop = null;
  while (m.t < 6.5 && n < 8){
    m.step(DT); step++;
    if (m.t < 2.5 || step % 50) continue;
    if (m.hitStop > 0 || me.flash > 0 || th.flash > 0 || me.ultsFired || m.ultFx) continue;
    const A = frame(false), B = frame(true);
    const [bx, by] = toDev(me.x, me.y), reach = (me.w.reach + 40) * K;
    let wn = 0, ws = 0, wl = 0;
    for (let y = 0; y < cv.height; y++) for (let x = 0; x < cv.width; x++){
      const q = (x - bx) ** 2 + (y - by) ** 2;
      if (q > reach * reach || q < (R * K) ** 2) continue;
      const i = (y * cv.width + x) * 4, dl = L(A, i) - L(B, i);
      if (Math.abs(dl) < 0.02) continue;
      wn++; ws += Math.abs(dl); wl += L(A, i);
    }
    out.push({ t: +m.t.toFixed(2), w: { n: wn, dL: wn ? ws / wn : 0, L: wn ? wl / wn : 0, areaU: wn / (K * K) } });
    if (!crop){ frame(false); const s = Math.round(reach); crop = { png: cv.toDataURL("image/png"), box: [Math.round(bx - s), Math.round(by - s), 2 * s] }; }
    n++;
  }
  return { id, aff: me.aff.key, shape: me.w.shape, out, crop };
}"""
res = []
with game(game_path=PAGE) as (page, errors):
    for id_ in IDS:
        r = page.evaluate(JS, [id_, 4242])
        assert not errors, errors[:3]
        res.append(r)
tiles = []
rank = []
for r in res:
    o = r["out"]
    md = lambda f: sorted(x["w"][f] for x in o)[len(o) // 2]
    rank.append((md("dL"), r["id"]))
    print(f"{r['id']:12s} {r['aff']:10s} {r['shape']} n {len(o)}  BLADES |dL| med {md('dL'):.3f} (min {min(x['w']['dL'] for x in o):.3f} "
          f"max {max(x['w']['dL'] for x in o):.3f})  luma {md('L'):.3f}  area {md('areaU'):.0f} u2")
    if r["crop"]:
        im = Image.open(io.BytesIO(base64.b64decode(r["crop"]["png"].split(",", 1)[1]))).convert("RGB")
        x, y, s = r["crop"]["box"]
        tiles.append(im.crop((x, y, x + s, y + s)).resize((200, 200), Image.LANCZOS))
    r.pop("crop", None)
rank.sort(reverse=True)
print("rank by |dL|:", " > ".join(f"{i} {v:.3f}" for v, i in rank))
if tiles:
    sh = Image.new("RGB", (200 * len(tiles), 200))
    for i, t in enumerate(tiles): sh.paste(t, (200 * i, 0))
    sh.save(HERE / "snaps" / (OUT.stem + "_twinblades.png"))
OUT.write_text(json.dumps(res, indent=1))
