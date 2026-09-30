"""THE GREY'S LOOK, by numbers: on real greyed frames (the foe's weapon inside a doubled hex stun, out of and in a hit
stop), the foe's weapon region (inside its reach, outside its ball) drawn as: PLAIN (the base's stun, 0.42 in colour:
`_unmkGreyed` -> false), FREE (the weapon unstunned: stun 0 for the draw), and each candidate grey (filter, alpha) by
shadowing `_unmkGreyFilter` / `_unmkGreyAlpha` on the renderer. Per candidate: |dL| and |dC| of the pixels it moves
against PLAIN (does the Unmaking's stop look different from a plain stop?) and against FREE (does it look stopped at
all?), and the weapon region's mean chroma (is it grey?). By the foe's school. Crops to a strip for looking.
usage: greycmp.py page out.json. SCRATCH."""
import sys, json, pathlib, io, base64, statistics as S
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
from PIL import Image
HERE = pathlib.Path(__file__).parent
PAGE = HERE / sys.argv[1]
OUT = HERE / (sys.argv[2] if len(sys.argv) > 2 else "greycmp.json")
VARS = [("A grayscale @0.6 (the design's words)", "grayscale(1)", 0.6),
        ("B grayscale contrast .6 @0.6", "grayscale(1) contrast(0.6)", 0.6),
        ("C grayscale brightness .7 @0.6", "grayscale(1) brightness(0.7)", 0.6),
        ("D grayscale contrast .5 brightness .85 @0.6", "grayscale(1) contrast(0.5) brightness(0.85)", 0.6),
        ("E grayscale @0.42", "grayscale(1)", 0.42)]
FIGHTS = [("dawnbringer", 99001, "a"), ("lastlight", 4242, "b"), ("aureole", 4101, "a"), ("morningstar", 8888, "b"),
          ("nightfell", 5150, "a"), ("twinshade", 99008, "a"), ("grudgebearer", 31337, "a"), ("heartwood", 2207, "a"),
          ("censer", 4101, "b"), ("paradox", 4242, "b"), ("widowmaker", 777, "a"), ("starwarden", 2317, "b")]
JS = r"""([foe, seed, side, vars, nWant]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(540, 960); AC.SFX.play = function(){}; AC.SFX.resume = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, R = AC.CONFIG.physics.ballR, A = AC.CONFIG.arena;
  const r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = side === "a" ? new AC.Match("spellbreaker", foe, seed) : new AC.Match(foe, "spellbreaker", seed);
  const me = m.a.w.id === "spellbreaker" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const toDev = (x, y) => [r.k * (r.pad + r.scale * x), r.k * (r.arenaTop + r.scale * y)];
  const K = r.k * r.scale;
  const frame = (mode, v) => {
    const sv = th.stun;
    if (mode === "plain" || mode === "free") r._unmkGreyed = function(){ return false; };
    if (mode === "free") th.stun = 0;
    if (mode === "var"){ r._unmkGreyFilter = function(){ return v[1]; }; r._unmkGreyAlpha = function(){ return v[2]; }; }
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    try { AC.__draw(m); } finally { Math.random = realRandom; m.shake = ks; th.stun = sv;
      delete r._unmkGreyed; delete r._unmkGreyFilter; delete r._unmkGreyAlpha; }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data);
  };
  const L = (d, i) => (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
  const C = (d, i) => (Math.max(d[i], d[i+1], d[i+2]) - Math.min(d[i], d[i+1], d[i+2])) / 255;
  const region = () => { const [bx, by] = toDev(th.x, th.y), reach = (th.w.reach * m.actMods.reach * th.reachMul + R + 20) * K, rb = R * K;
    const idx = []; const w = cv.width;
    for (let y = Math.max(0, Math.round(by - reach)); y < Math.min(cv.height, by + reach); y++)
      for (let x = Math.max(0, Math.round(bx - reach)); x < Math.min(w, bx + reach); x++){
        const q = (x - bx) ** 2 + (y - by) ** 2; if (q > reach * reach || q < rb * rb) continue; idx.push((y * w + x) * 4); }
    return idx; };
  const cmp = (a, b, idx) => { let n = 0, sl = 0, sc = 0;
    for (const i of idx){ const dl = L(a, i) - L(b, i), dc = C(a, i) - C(b, i);
      if (Math.abs(dl) < 0.02 && Math.abs(dc) < 0.02) continue; n++; sl += Math.abs(dl); sc += Math.abs(dc); }
    return { n, dL: n ? sl / n : 0, dC: n ? sc / n : 0 }; };
  const chroma = (a, b, idx) => { let n = 0, s = 0, sl = 0;   // the weapon's own pixels: those that differ from FREE-less? use pixels changed vs plain OR free
    for (const i of idx){ n++; s += C(a, i); sl += L(a, i); } return { C: n ? s / n : 0, L: n ? sl / n : 0 }; };
  const out = { foe, seed, side, aff: th.aff.key, frames: [] };
  let step = 0, lastAt = -999;
  const inHall = (f, pad) => f.x > pad && f.x < A.w - pad && f.y > pad && f.y < A.h - pad;
  while (!m.over && step < 200 / DT && out.frames.length < nWant){
    m.step(DT); step++;
    if (!(th.unmkGrey > 0.12) || !inHall(th, 90) || th.flash > 0 || me.flash > 0 || step - lastAt < 90) continue;
    lastAt = step;
    const idx = region();
    const plain = frame("plain"), free = frame("free");
    const fr = { t: +m.t.toFixed(3), stop: m.hitStop > 0, grey: +th.unmkGrey.toFixed(3), vars: [] };
    fr.plainVsFree = cmp(plain, free, idx);
    for (const v of vars){
      const g = frame("var", v);
      fr.vars.push({ vsPlain: cmp(g, plain, idx), vsFree: cmp(g, free, idx) });
    }
    if (out.frames.length === 0){
      const [bx, by] = toDev(th.x, th.y), s = Math.round((th.w.reach + 60) * K);
      const crops = [];
      for (const mode of ["free", "plain"]){ frame(mode); crops.push(cv.toDataURL("image/png")); }
      for (const v of vars){ frame("var", v); crops.push(cv.toDataURL("image/png")); }
      out.crop = { box: [Math.round(bx - s), Math.round(by - s), 2 * s], pngs: crops };
    }
    out.frames.push(fr);
  }
  return out;
}"""
res = []
with game(game_path=PAGE) as (page, errors):
    for foe, seed, side in FIGHTS:
        r = page.evaluate(JS, [foe, seed, side, VARS, 4])
        assert not errors, errors[:3]
        res.append(r)
        print(foe, seed, side, r["aff"], len(r["frames"]), flush=True)
rows = []
for r in res:
    if "crop" not in r: continue
    x, y, s = r["crop"]["box"]
    tiles = []
    for p in r["crop"]["pngs"]:
        im = Image.open(io.BytesIO(base64.b64decode(p.split(",", 1)[1]))).convert("RGB")
        tiles.append(im.crop((x, y, x + s, y + s)).resize((160, 160), Image.LANCZOS))
    row = Image.new("RGB", (160 * len(tiles), 160))
    for i, t in enumerate(tiles): row.paste(t, (160 * i, 0))
    rows.append(row)
    r.pop("crop")
if rows:
    sh = Image.new("RGB", (rows[0].width, 160 * len(rows)))
    for i, rw in enumerate(rows): sh.paste(rw, (0, 160 * i))
    sh.save(HERE / "snaps" / (OUT.stem + "_strip.png"))
OUT.write_text(json.dumps(res, indent=1))
med = lambda a: S.median(a) if a else float("nan")
print("columns of the strip: FREE (unstunned), PLAIN (the base's stun, 0.42 colour), then " + ", ".join(v[0][:1] for v in VARS))
allf = [(r["aff"], f) for r in res for f in r["frames"]]
print(f"{len(allf)} greyed frames; PLAIN vs FREE (the base's stop, for scale): |dL| {med([f['plainVsFree']['dL'] for _, f in allf]):.3f} "
      f"|dC| {med([f['plainVsFree']['dC'] for _, f in allf]):.3f}")
for j, v in enumerate(VARS):
    print(f"{v[0]}:")
    for aff in sorted(set(a for a, _ in allf)) + ["ALL"]:
        sub = [f for a, f in allf if aff == "ALL" or a == aff]
        vp = [f["vars"][j]["vsPlain"] for f in sub]; vf = [f["vars"][j]["vsFree"] for f in sub]
        print(f"   {aff:10s} n {len(sub):2d}  vs PLAIN |dL| {med([q['dL'] for q in vp]):.3f} |dC| {med([q['dC'] for q in vp]):.3f} px {med([q['n'] for q in vp]):.0f}"
              f"   vs FREE |dL| {med([q['dL'] for q in vf]):.3f} |dC| {med([q['dC'] for q in vf]):.3f} px {med([q['n'] for q in vf]):.0f}")
