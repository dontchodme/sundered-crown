"""FRAME COST on the REAL GPU through Electron (the app's runtime, electron 44), the app's 453x805, chain on.
Interleaved A/B on ld-final.html: OFF (the picture's three entry points shadowed on the renderer instance --
drawLode, drawLodeTop, _lodeHead -- which is the base's path for this relic in every frame) against ON (the
rows), same state, same process, the order alternating frame to frame:
  SEQUENCE: the fight as it plays -- 2 sim steps (1/60 s) then ONE draw of each, timed -- bucketed by phase:
            rest (no window), cast (the chain lighting: lodeAge < 0.6), lit (window, no touch record up), touch
            (a touch record up: flare / bar / streak), close (the go-dark). median, p90, max ms of the whole frame
            (1px readback forces the raster).
  ALONE:    the picture's own calls in the arena's frame: drawLode + drawLodeTop + the caster's drawWeapon (the
            head's rune), ON vs the same calls shadowed; and WEAPON: the caster's drawWeapon alone (the
            silhouette's cost; run the script with --page on the base link for the conjured head's).
usage: cost.py [--page P] [foe seed side]... SCRATCH."""
import json, pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).parent
EXE = pathlib.Path(r"C:\dev\sundered-crown\app\node_modules\.bin\electron.cmd")
args = sys.argv[1:]
PAGE = (HERE.parent / "ld-final.html").resolve()
TAG = "cost"
if args[:1] == ["--page"]:
    PAGE = pathlib.Path(args[1]).resolve(); TAG = "cost_" + PAGE.stem; args = args[2:]
JS = r"""async ([foe, seed, side, maxW]) => {
  AC.setResolution(453, 805);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, r = AC.renderer, ctx = document.getElementById("cv").getContext("2d");
  const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
  const me = m.a.w.id === "lodestone" ? m.a : m.b, th = me === m.a ? m.b : m.a;
  const HAS = typeof r.drawLode === "function";
  const HIDE = ["drawLode", "drawLodeTop", "_lodeHead"];
  const setOff = (off) => { for (const h of HIDE){ if (off) r[h] = function(){}; else delete r[h]; } };
  const q = (a, p) => { a = a.slice().sort((x, y) => x - y); return a[Math.min(a.length - 1, Math.floor(p * a.length))]; };
  const raf = () => new Promise(res => requestAnimationFrame(res));
  const drawT = (off) => { setOff(off); m.shake = 0; const t0 = performance.now(); AC.__draw(m);
    ctx.getImageData(0, 0, 1, 1); const dt = performance.now() - t0; setOff(0); return dt; };
  const world = () => { const K = r.k * r.scale; ctx.setTransform(K, 0, 0, K, r.k * r.pad, r.k * r.arenaTop); };
  const alone = (off) => { setOff(off); const t0 = performance.now();
    world(); if (HAS){ r.drawLode(m); r.drawLodeTop(m); } r.drawWeapon(m, me); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.getImageData(0, 0, 1, 1); const dt = performance.now() - t0; setOff(0); return dt; };
  const weap = () => { const t0 = performance.now();
    world(); for (let i = 0; i < 5; i++) r.drawWeapon(m, me); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.getImageData(0, 0, 1, 1); return (performance.now() - t0) / 5; };
  const P = { base: {}, rows: {}, aBase: {}, aRows: {}, weapon: {} };
  const push = (o, k, v) => (o[k] = o[k] || []).push(v);
  let step = 0, windows = 0, prev = null, flip = 0;
  for (let i = 0; i < 10; i++){ m.step(DT); drawT(0); drawT(1); }
  while (step < 200 / DT && !m.over){
    m.step(DT); m.step(DT); step += 2;
    const Z = me.ultRunes;
    if (Z && !prev) windows++;
    prev = Z;
    let ph = null;
    const fx = HAS ? me.lodeFx.some(x => x.t < 0.8) : false;
    if (Z && HAS && me.lodeAge < 0.6) ph = "cast";
    else if (Z && fx) ph = "touch";
    else if (Z) ph = "lit";
    else if (!Z && HAS && me.lodeFade > 0) ph = "close";
    else if (!Z && m.t > 3 && (P.base.rest || []).length < 90) ph = "rest";
    if (!ph) continue;
    if (windows > maxW) break;
    await raf();
    const order = (flip++ & 1) ? [1, 0] : [0, 1];
    for (const off of order) push(off ? P.base : P.rows, ph, drawT(off));
    for (const off of order) push(off ? P.aBase : P.aRows, ph, alone(off));
    push(P.weapon, ph, weap());
  }
  const out = { windows, touches: me.runeTally ? me.runeTally.touches : 0, has: HAS };
  for (const [nm, o] of Object.entries(P)){
    out[nm] = {};
    for (const [k, a] of Object.entries(o)) out[nm][k] = { n: a.length, med: q(a, 0.5), p90: q(a, 0.9), max: q(a, 1) };
  }
  return out;
}"""
FIGHTS = [("spellbreaker", 99015, "a"), ("dawnbringer", 99001, "a"), ("gravemourn", 99015, "a")]
if args:
    FIGHTS = [(args[i], int(args[i + 1]), args[i + 2]) for i in range(0, len(args), 3)]
res = {}
for foe, seed, side in FIGHTS:
    cfg = {"js": JS, "args": [foe, seed, side, 3]}
    f = pathlib.Path(tempfile.gettempdir()) / "sc_ld_cost_cfg.json"
    f.write_text(json.dumps(cfg), encoding="utf-8")
    of = pathlib.Path(tempfile.gettempdir()) / f"sc_ld_cost_out_{foe}_{seed}_{side}.json"
    r = None
    for attempt in range(3):
        if of.exists(): of.unlink()
        p = subprocess.run([str(EXE), str(HERE / "cost_electron.js"), "--game", str(PAGE), "--cfgfile", str(f), "--outfile", str(of)],
                           capture_output=True, text=True, timeout=1500, shell=False)
        if of.exists():
            r = json.loads(of.read_text(encoding="utf-8")); break
        print("FAILED rc", p.returncode, foe, "attempt", attempt, [l for l in p.stderr.splitlines() if "cache" not in l.lower()][-15:], p.stdout[-300:], flush=True)
    if r is None: continue
    res[foe] = r
    o = r["out"]
    print(f"{foe:12s} {r['renderer'][:44]}  page {PAGE.name} windows {o['windows']} touches {o['touches']}", flush=True)
    for k in ("rest", "cast", "lit", "touch", "close"):
        if k not in o["base"]: continue
        b_, w_ = o["base"][k], o["rows"][k]
        print(f"    {k:5s} n {b_['n']:3d}  FRAME off med {b_['med']:.2f} p90 {b_['p90']:.2f} max {b_['max']:.1f}"
              f"  | rows med {w_['med']:.2f} p90 {w_['p90']:.2f} max {w_['max']:.1f}"
              f"  || ALONE off {o['aBase'][k]['med']:.2f}/{o['aBase'][k]['p90']:.2f}  rows {o['aRows'][k]['med']:.2f}/{o['aRows'][k]['p90']:.2f}"
              f"  || WEAPON {o['weapon'][k]['med']:.3f}/{o['weapon'][k]['p90']:.3f}", flush=True)
(HERE / (TAG + ".json")).write_text(json.dumps(res, indent=1))
