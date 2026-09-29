"""THE SILHOUETTE'S FRAME COST, interleaved A/B in ONE page on the REAL GPU (Electron 44, the app's 453x805,
chain on): ld-final.html's square head (SHAPES._whConjured as the rows redraw it) against the base's conjured
slices (the base's own `_whConjured` text, read out of sc-lodestone-b205.html and installed beside it), the order
alternating draw to draw. The glow sprite is cached by (shape, L, W, colour, k) and does not depend on the head's
function, so both arms share it and only the live shape differs -- which is the silhouette's cost.
  WEAPON: the caster's drawWeapon (5 calls a timing, 1px readback), at rest and with the walls lit.
  FRAME:  the whole AC.__draw with the arena as it stands, at rest and lit.
usage: cost_sil.py [foe seed side]. SCRATCH."""
import json, pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import ld_rows as L
EXE = pathlib.Path(r"C:\dev\sundered-crown\app\node_modules\.bin\electron.cmd")
PAGE = (HERE.parent / "ld-final.html").resolve()
old = L.sil_old(L.src_text())
meth = old[old.index("  _whConjured(c, L, W, p){"):].rstrip()
assert meth.endswith("},")
OLDFN = "(function(){ const o = {" + meth[:-1] + "}; return o._whConjured; })()"
JS = r"""async ([foe, seed, side, oldSrc]) => {
  AC.setResolution(453, 805);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const S = AC.SHAPES, NEW = S._whConjured, OLD = eval(oldSrc);
  const DT = AC.CONFIG.physics.dt, r = AC.renderer, ctx = document.getElementById("cv").getContext("2d");
  const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
  const me = m.a.w.id === "lodestone" ? m.a : m.b;
  const q = (a, p) => { a = a.slice().sort((x, y) => x - y); return a[Math.min(a.length - 1, Math.floor(p * a.length))]; };
  const raf = () => new Promise(res => requestAnimationFrame(res));
  const world = () => { const K = r.k * r.scale; ctx.setTransform(K, 0, 0, K, r.k * r.pad, r.k * r.arenaTop); };
  const weap = (fn) => { S._whConjured = fn; const t0 = performance.now();
    world(); for (let i = 0; i < 5; i++) r.drawWeapon(m, me); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.getImageData(0, 0, 1, 1); const d = (performance.now() - t0) / 5; S._whConjured = NEW; return d; };
  const frame = (fn) => { S._whConjured = fn; m.shake = 0; const t0 = performance.now(); AC.__draw(m);
    ctx.getImageData(0, 0, 1, 1); const d = performance.now() - t0; S._whConjured = NEW; return d; };
  const out = {};
  const run = async (tag) => {
    const P = { wNew: [], wOld: [], fNew: [], fOld: [] };
    for (let i = 0; i < 160; i++){
      if (i % 4 === 0) await raf();
      const o = (i & 1) ? [OLD, NEW] : [NEW, OLD];
      for (const fn of o) (fn === NEW ? P.wNew : P.wOld).push(weap(fn));
      for (const fn of o) (fn === NEW ? P.fNew : P.fOld).push(frame(fn));
    }
    out[tag] = {};
    for (const [k, a] of Object.entries(P)) out[tag][k] = { n: a.length, med: q(a, 0.5), p90: q(a, 0.9) };
  };
  let g = 0;
  while (m.t < 4 && g++ < 5000) m.step(DT);
  for (let i = 0; i < 6; i++){ frame(NEW); frame(OLD); }
  await run("rest");
  g = 0;
  while (!(me.lodeFade > 0 && me.lodeAge > 0.8 && !(me.lodeOut > 0)) && !m.over && g++ < 40000) m.step(DT);
  if (!m.over) await run("lit");
  return out;
}"""
FIGHTS = [("spellbreaker", 99015, "a"), ("dawnbringer", 99001, "a")]
args = sys.argv[1:]
if args:
    FIGHTS = [(args[i], int(args[i + 1]), args[i + 2]) for i in range(0, len(args), 3)]
res = {}
for foe, seed, side in FIGHTS:
    cfg = {"js": JS, "args": [foe, seed, side, OLDFN]}
    f = pathlib.Path(tempfile.gettempdir()) / "sc_ld_costsil_cfg.json"
    f.write_text(json.dumps(cfg), encoding="utf-8")
    of = pathlib.Path(tempfile.gettempdir()) / f"sc_ld_costsil_out_{foe}.json"
    r = None
    for attempt in range(3):
        if of.exists(): of.unlink()
        p = subprocess.run([str(EXE), str(HERE / "cost_electron.js"), "--game", str(PAGE), "--cfgfile", str(f), "--outfile", str(of)],
                           capture_output=True, text=True, timeout=1500, shell=False)
        if of.exists():
            r = json.loads(of.read_text(encoding="utf-8")); break
        print("FAILED rc", p.returncode, foe, "attempt", attempt, [l for l in p.stderr.splitlines() if "cache" not in l.lower()][-10:], flush=True)
    if r is None: continue
    res[foe] = r
    print(f"{foe:12s} {r['renderer'][:44]}", flush=True)
    for k, o in r["out"].items():
        print(f"    {k:4s} WEAPON square med {o['wNew']['med']:.3f} p90 {o['wNew']['p90']:.3f} | conjured med {o['wOld']['med']:.3f} p90 {o['wOld']['p90']:.3f}"
              f"   || FRAME square med {o['fNew']['med']:.2f} p90 {o['fNew']['p90']:.2f} | conjured med {o['fOld']['med']:.2f} p90 {o['fOld']['p90']:.2f}  (n {o['wNew']['n']})", flush=True)
(HERE / "cost_sil.json").write_text(json.dumps(res, indent=1))
