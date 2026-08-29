#!/usr/bin/env python3
"""DOES A SET-PIECE GET BETTER WITH PARTICLES IN IT? — FX-RUNTIME-BRIEF.md §3.2.

    python ult_particle_lab.py                       off / light / heavy
    python ult_particle_lab.py --arms off,heavy --w 1080

§3.2 asks for a GPU particle runtime in `src/render/fx.js` sharing `post.js`'s
context -- state in a texture, ping-pong integrated, thousands of instances.
That is the right way to SHIP particles. It is the wrong way to find out
whether particles are what these set-pieces are missing.

So this draws them in Canvas 2D, offline, on one relic. If the answer is yes
the GPU runtime is worth building and this prototype is what it has to match;
if the answer is no, it cost an afternoon instead of two sessions. That
sequencing is the same one that killed §3.1's envelope in twenty minutes, and
the same one `CLAUDE.md` §4.0 states outright: film before you tune.

CANVAS 2D IS A LEGITIMATE INSTRUMENT HERE AND A BAD SHIPPING VEHICLE. The
video is captured offline, where a 40 ms frame costs wall-clock and nothing
else, so the prototype can afford hundreds of sprites the app could not. The
app's budget is 4.77 ms (`post_cost.py`, 2026-08-28) and that is what §3.2's
texture-state system is FOR. None of that changes what the picture looks like,
which is the only thing being asked here.

THE SUBJECT IS SLAGBURST, per the brief -- an explosion is the purest particle
case, and it is one of the thinnest set-pieces in the filmstrip.

    The `burst` phase is CAPTURED FROM A REAL FIGHT, not hand-written. The
    ultfx library only holds Slagburst's `cold` phase -- the out-of-range
    fizzle, which has no art branch at all and draws nothing. Writing a burst
    block by hand would put a picture on screen the game never produces, which
    is `CLAUDE.md` §4.1 committed deliberately. `05-reference/post/
    slagburst-burst.json` is a real one: n=7 stacks, radius 230, life 1.45.

DETERMINISM, §6, honoured even in a prototype because it is free here. Every
particle's randomness comes from mulberry32 keyed on `(seed, index)` -- never
`Math.random` -- and the integration steps a FIXED dt rather than a frame time.
Two runs of the same arm are identical, and the arms differ only in density.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game
from clip_spread import resolve_ffmpeg

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-frame.html"
BURST = REPO / "05-reference" / "post" / "slagburst-burst.json"
EL_JS = HERE / "fxcost_electron.js"
EL_BIN = [REPO / "app" / "node_modules" / ".bin" / n
          for n in ("electron.cmd", "electron")]

# A SPREAD, NOT A GUESS (Rule 2). One variable -- how many -- because "should
# there be particles at all" is the question and a spread that moved colour and
# count together could not answer it.
ARMS = {"off": 0, "light": 120, "heavy": 420}

FX_JS = r"""() => {
  /* A deterministic ember field, drawn into the arena transform right after
     drawUltOver, so it sits exactly where the ult art sits: over the fighters,
     under the HUD. Wrapping the method rather than drawing after AC.__draw is
     what keeps that layering honest -- readouts_build.py split the HUD out of
     the bloom's source on purpose and a late overlay would land on the wrong
     side of it. */
  const R = AC.renderer;
  if (R.__fxWrapped) return false;
  R.__fxWrapped = true;

  function mulberry32(a){
    return function(){
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const FX = window.__fx = {
    n: 0, parts: [], t: 0, born: false,

    /* Spawned as data, not as a loop over Math.random: index i always gets the
       same five numbers, so a re-run is bit-identical and an arm difference is
       density and nothing else. §6.1. */
    reset(n, seed){
      this.n = n; this.parts = []; this.t = 0; this.born = false;
      const rnd = mulberry32((seed | 0) ^ 0x51AB1E);
      for (let i = 0; i < n; i++){
        const a = rnd() * Math.PI * 2;
        const sp = 90 + rnd() * rnd() * 620;      /* squared: most are slow */
        const heavy = rnd() < 0.14;
        this.parts.push({
          a: a, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 40,
          x: 0, y: 0,
          life: (heavy ? 0.85 : 0.40) + rnd() * (heavy ? 0.75 : 0.65),
          age: 0,
          r: heavy ? 2.6 + rnd() * 3.4 : 0.9 + rnd() * 1.9,
          spin: (rnd() - 0.5) * 18, rot: rnd() * 6.28,
          heavy: heavy, seedv: rnd(),
        });
      }
    },

    /* FIXED dt, §6.2. A particle field integrated on frame time is a clip
       that cannot be rebuilt from its seed. */
    step(dt){
      const G = 520, DRAG = 1.9;
      for (const p of this.parts){
        if (p.age > p.life) continue;
        p.age += dt;
        const d = Math.exp(-DRAG * dt);
        p.vx *= d; p.vy = p.vy * d + G * dt;
        p.x += p.vx * dt; p.y += p.vy * dt;
        p.rot += p.spin * dt;
      }
      this.t += dt;
    },

    draw(c, cx, cy){
      if (!this.n) return;
      c.save();
      c.translate(cx, cy);
      /* EMBERS ADDITIVE, DEBRIS NOT. The bloom reads the emissive layer, so an
         ember that is `lighter` becomes light and a debris chunk that is not
         stays an object. CLAUDE.md §4.1b: a thing that is only ever added is
         not an object, it is a hole. */
      for (const p of this.parts){
        if (p.age > p.life) continue;
        const k = p.age / p.life, fade = 1 - k * k;
        if (p.heavy){
          c.globalCompositeOperation = "source-over";
          c.globalAlpha = 0.85 * fade;
          c.save();
          c.translate(p.x, p.y); c.rotate(p.rot);
          c.fillStyle = "#1A0A05";
          c.fillRect(-p.r, -p.r * 0.6, p.r * 2, p.r * 1.2);
          c.globalCompositeOperation = "lighter";
          c.globalAlpha = fade * (0.5 + 0.5 * p.seedv);
          c.fillStyle = k < 0.5 ? "#FF9A3C" : "#8C2A0A";
          c.fillRect(-p.r, -p.r * 0.6, p.r * 2, p.r * 0.35);
          c.restore();
        } else {
          c.globalCompositeOperation = "lighter";
          c.globalAlpha = fade;
          /* cooling: white -> ember -> dull red, which is what a spark does
             and what a single flat colour never says */
          c.fillStyle = k < 0.25 ? "#FFF6E2" : (k < 0.62 ? "#FF9A3C" : "#8C2A0A");
          c.beginPath();
          c.arc(p.x, p.y, p.r * (1 - 0.45 * k), 0, 6.2832);
          c.fill();
        }
      }
      c.restore();
    },
  };

  const orig = R.drawUltOver.bind(R);
  R.drawUltOver = function(m){
    orig(m);
    const u = m.ultFx;
    if (!u || !FX.n) return;
    FX.draw(this.ctx, u.tx, u.ty);
  };
  return true;
}"""

SETUP_JS = r"""([block, w, h]) => {
  AC.setResolution(w, h);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(block.w, "bulwarden", 25064);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.30; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.52; m.b.y = A.h * 0.52;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.shake = 0;
  window.__lab = { m: m, block: block };
  return { life: block.life, n: block.n, radius: block.radius };
}"""

FRAME_JS = r"""([t, mt, q, dt]) => {
  const L = window.__lab, m = L.m, b = L.block;
  m.t = mt;
  m.ultFx = Object.assign({}, b, {
    src: "a", tgt: "b", x: m.b.x, y: m.b.y, tx: m.b.x, ty: m.b.y,
    aff: m.a.aff, t: t });
  if (t >= 0 && !window.__fx.born){ window.__fx.born = true; }
  if (window.__fx.born && dt > 0){
    /* the sim's own dt, halved into two sub-steps, so the field is integrated
       at 120 Hz exactly as the physics is */
    window.__fx.step(dt / 2); window.__fx.step(dt / 2);
  }
  const real = Math.random;
  Math.random = function(){ return 0.5; };   /* no unseeded noise in the frame */
  AC.__draw(m);
  Math.random = real;
  const u = document.getElementById('cv').toDataURL('image/jpeg', q);
  return u.slice(u.indexOf(',') + 1);
}"""


COST_JS = r"""([counts, reps, n]) => {
  /* WHAT DOES THE FIELD COST PER FRAME, on this canvas, on the real GPU?
     The same shape post_cost.py uses: median of `reps` repetitions of `n`
     draws, because one scheduling hiccup in a run of five should not become
     the answer. The 2D draw is measured first as the baseline, then the same
     draw with the field on top; the DIFFERENCE is the field. */
  const L = window.__lab, m = L.m, b = L.block;
  m.ultFx = Object.assign({}, b, { src:"a", tgt:"b", x:m.b.x, y:m.b.y,
                                   tx:m.b.x, ty:m.b.y, aff:m.a.aff, t:0.35 });
  const med = (a) => { a = a.slice().sort((x,y)=>x-y); return a[a.length>>1]; };
  const ctx = document.getElementById('cv').getContext('2d');

  /* FORCE THE RASTER, ONCE, AT THE END -- postcost.js's technique and the
     reason this is a rewrite. Canvas2D command submission is asynchronous, so
     timing a loop of draws without a readback measures how fast the calls were
     QUEUED. The first version of this did exactly that and reported a 1.20 ms
     baseline for a frame post_cost.py measures at 9.06 on the same canvas --
     an eightfold error, in the flattering direction, on the number that was
     about to decide whether §3.2's GPU runtime gets built.

     Inside a rAF as well: outside one the compositor can defer the whole
     batch past the measurement. */
  function timed(draws){
    return new Promise(res => {
      requestAnimationFrame(() => {
        const t0 = performance.now();
        for (let i = 0; i < draws; i++) AC.__draw(m);
        ctx.getImageData(0, 0, 1, 1);
        res((performance.now() - t0) / draws);
      });
    });
  }

  return (async () => {
    const out = [];
    for (const c of counts){
      window.__fx.reset(c, 25064);
      for (let i = 0; i < 40; i++) window.__fx.step(1/120);   /* mid-flight */
      const reps_ms = [];
      for (let r = 0; r < reps; r++) reps_ms.push(await timed(n));
      out.push({ n: c, ms: med(reps_ms) });
    }
    window.__fx.reset(0, 25064);
    return out;
  })();
}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--burst", default=str(BURST))
    ap.add_argument("--arms", default="off,light,heavy")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--lead", type=float, default=0.30)
    ap.add_argument("--tail", type=float, default=1.1)
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--q", type=float, default=0.95)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--out", default=str(REPO / "07-shorts" / "particles"))
    ap.add_argument("--cost", action="store_true",
                    help="measure ms/frame against particle count instead of "
                         "rendering clips. The number that decides whether "
                         "§3.2's GPU runtime is needed at all")
    ap.add_argument("--cost-w", type=int, default=453,
                    help="the app's canvas, which is the only realtime "
                         "surface; the video is captured offline")
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    bp = pathlib.Path(args.burst)
    if not path.exists() or not bp.exists():
        print(f"! need {path} and {bp}")
        return 2
    block = json.loads(bp.read_text(encoding="utf-8"))["block"]
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    for a in arms:
        if a not in ARMS:
            print(f"! unknown arm {a!r}; have {list(ARMS)}")
            return 2

    ff = resolve_ffmpeg("ffmpeg")
    out = pathlib.Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    H = round(args.w * 16 / 9)
    dt = 1.0 / args.fps

    if args.cost:
        # THROUGH ELECTRON, NOT PLAYWRIGHT. Playwright launches with
        # --disable-gpu, so its Canvas rasteriser is SwiftShader and a number
        # off it is a measurement of SwiftShader: the first run of this
        # reported a 43 ms baseline for a frame the app draws in 9. That is
        # not noise, it is a different machine. post_cost.py's header says so
        # and defaults to Electron; this follows it.
        exe = next((q for q in EL_BIN if q.exists()), None)
        if exe is None:
            print("! no Electron in app/node_modules -- run `npm install` in "
                  "app/.\n  This measurement is NOT worth taking through "
                  "Playwright; see the header.")
            return 2
        W = args.cost_w
        cfg = {"fx": FX_JS, "setup": SETUP_JS,
               "setupArgs": [block, W, round(W * 16 / 9)],
               "cost": COST_JS, "costArgs": [[0, 120, 420, 900, 2000], 5, 30]}
        # Written to a file rather than passed as an argument: cfg carries
        # whole JS sources and electron.cmd is a batch shim, so cmd.exe would
        # parse the `>` in them first and fail with "> was unexpected at this
        # time" before Electron started.
        cfgf = pathlib.Path(tempfile.gettempdir()) / "sc_fxcost_cfg.json"
        cfgf.write_text(json.dumps(cfg), encoding="utf-8")
        r = subprocess.run([str(exe), str(EL_JS), "--game", str(path),
                            "--cfgfile", str(cfgf)],
                           capture_output=True, text=True)
        if r.returncode != 0 or "{" not in r.stdout:
            print("! electron run failed")
            print((r.stderr or r.stdout)[-1200:])
            return 1
        res = json.loads(r.stdout[r.stdout.index("{"):])
        rows, rend = res["rows"], res["renderer"]
        base = rows[0]["ms"]
        print(f"\nPARTICLE COST  {W}x{round(W*16/9)} (the app's canvas)  "
              f"median of 5 x 30 draws")
        print(f"  {rend}\n")
        print(f"  {'particles':>10}{'ms/frame':>11}{'added':>9}"
              f"{'% of 16.67':>12}")
        for r in rows:
            print(f"  {r['n']:>10}{r['ms']:>11.3f}{r['ms']-base:>9.3f}"
                  f"{100*r['ms']/16.67:>11.0f}%")
        print(f"\n  THE APP HAS 4.77 ms OF HEADROOM (post_cost.py, "
              f"2026-08-28).\n  A Canvas 2D field that fits inside it does "
              f"not need §3.2's GPU runtime\n  to reach the app -- and the "
              f"video, captured offline, never needed one.")
        return 0

    with game(game_path=path) as (page, errors):
        info = page.evaluate(SETUP_JS, [block, args.w, H])
        page.evaluate(FX_JS)
        life = info["life"]
        print(f"slagburst  n={info['n']} stacks  radius={info['radius']}  "
              f"life={life:.2f}s")
        n_lead = round(args.lead * args.fps)
        n_body = round((life + args.tail) * args.fps)

        for arm in arms:
            page.evaluate("([n]) => window.__fx.reset(n, 25064)", [ARMS[arm]])
            tmp = out / f"_f_{arm}"
            if tmp.exists():
                shutil.rmtree(tmp)
            tmp.mkdir(parents=True)
            i = 0
            for f in range(n_lead):
                b64 = page.evaluate(FRAME_JS, [-1.0, f / args.fps, args.q, 0.0])
                (tmp / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(b64))
                i += 1
            for f in range(n_body):
                t = min(life, f / args.fps)
                b64 = page.evaluate(
                    FRAME_JS, [t, (n_lead + f) / args.fps, args.q, dt])
                (tmp / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(b64))
                i += 1
            mp4 = out / f"slagburst-{arm}.mp4"
            subprocess.run(
                [ff, "-y", "-hide_banner", "-loglevel", "error",
                 "-framerate", str(args.fps), "-i", str(tmp / "f_%05d.jpg"),
                 "-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf),
                 "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)],
                check=True)
            shutil.rmtree(tmp)
            print(f"   {arm:<6} {ARMS[arm]:>4} particles  {i} frames -> "
                  f"{mp4.name}  {mp4.stat().st_size/1e6:.1f} MB")

        if errors:
            print("! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    print("\nSame set-piece, same seed, same length. The ONLY difference is how "
          "many\nparticles are in it -- `off` is the game exactly as it ships.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
