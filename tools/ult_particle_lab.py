#!/usr/bin/env python3
"""DO PARTICLES MAKE A SET-PIECE BETTER? — FX-RUNTIME-BRIEF.md §3.2.

    python ult_particle_lab.py                       all four relics, off vs on
    python ult_particle_lab.py --ids emberedge --arms off,light,heavy
    python ult_particle_lab.py --cost                ms/frame vs particle count

§3.2 asks for a GPU particle runtime in `src/render/fx.js` sharing `post.js`'s
context -- state in a texture, ping-pong integrated, thousands of instances.
That is the right way to SHIP particles and the wrong way to find out whether
particles are what these set-pieces lack. So this draws them in Canvas 2D: an
afternoon instead of two sessions if the answer is no. Same sequencing that
killed §3.1's envelope in twenty minutes, and the rule `CLAUDE.md` §4.0 states
outright -- film before you tune.

ANSWERED 2026-08-28, BOTH HALVES:

  * Rick picked the heaviest arm on Slagburst. Particles land.
  * And they do not need a GPU. Measured on the real hardware, 420 particles
    cost 1.64 ms of the app's 4.77 ms headroom (`--cost`). The "about a dozen
    sprites per frame" figure §3.2 was written against was really about
    `shadowBlur`: the existing art's sprites each drag a full-canvas shadow
    and these carry none.

FOUR SHAPES, FOUR BEHAVIOURS, because an explosion field on a beam looks wrong.
The emitter is spec-driven rather than one effect reused -- §3.2's "twenty-five
short declarative specs" in miniature. Four is enough to find out whether the
vocabulary generalises or whether Slagburst was a lucky fit.

BLOCKS ARE CAPTURED FROM REAL FIGHTS, never hand-written. Slagburst's comes
from `05-reference/post/slagburst-burst.json` because the ultfx library only
holds its `cold` phase -- the out-of-range fizzle, which has no art branch and
draws nothing. The rest come from `ultfx-library.json`. A hand-written block
puts a picture on screen the game never produces, which is `CLAUDE.md` §4.1
committed on purpose.

DETERMINISM, §6, honoured even in a prototype because it is free here. Every
particle's randomness is mulberry32 keyed on `(seed, index)` -- never
`Math.random` -- and the field integrates a FIXED dt rather than a frame time.
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
from ult_envelope_lab import life_map

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
BUILD = REPO / "02-chain" / "sc-paradox-frame.html"
BURST = REPO / "05-reference" / "post" / "slagburst-burst.json"
LIB = REPO / "05-reference" / "post" / "ultfx-library.json"
EL_JS = HERE / "fxcost_electron.js"
EL_BIN = [REPO / "app" / "node_modules" / ".bin" / n
          for n in ("electron.cmd", "electron")]

# Density arms. One variable, because "should there be particles at all" is the
# question and a spread that moved colour and count together could not answer
# it. `heavy` is the multiplier Rick chose on Slagburst.
ARMS = {"off": 0.0, "light": 0.30, "heavy": 1.0}

# Colours are NOT in the specs. They come from the relic's own affinity at draw
# time (`aff.core`, `aff.dark`), because a hand-picked palette per relic is the
# kind of number `CLAUDE.md` §4.9 says not to strand in a prototype -- and
# because the schools already own their colour.
SPECS = {
    # THE EXPLOSION. Hard radial, heavy gravity, tumbling debris.
    "emberedge": dict(mode="burst", n=420, sp=(90, 710), grav=520, drag=1.9,
                      life=(0.40, 1.05), heavy=0.14, size=(0.9, 2.8),
                      spawn=0.0, up=40),
    # A NOVA IS A BURST THAT DOES NOT FALL. Faster, lighter, shorter, and it
    # keeps its ring instead of slumping -- gravity is most of what separates
    # "explosion" from "shockwave" and it is one number.
    "widowmaker": dict(mode="burst", n=360, sp=(240, 620), grav=90, drag=2.6,
                       life=(0.30, 0.75), heavy=0.05, size=(0.8, 2.2),
                       spawn=0.05, up=0),
    # A BEAM SHEDS ALONG ITS LENGTH, not from a point, and its motes drift UP
    # out of it. Negative gravity is what makes a beam read as light rather
    # than as an explosion pointed sideways.
    "aureole": dict(mode="beam", n=300, sp=(20, 120), grav=-120, drag=1.2,
                    life=(0.45, 1.10), heavy=0.0, size=(0.7, 2.0),
                    spawn=0.55, up=0),
    # A SUSTAINED FIELD seeds motes THROUGHOUT its radius across its whole
    # life, barely moving. Nothing is thrown; the air is full.
    "lastlight": dict(mode="field", n=340, sp=(8, 55), grav=-30, drag=0.8,
                      life=(0.60, 1.40), heavy=0.0, size=(0.6, 1.8),
                      spawn=0.75, up=0),
}

DEFAULT_IDS = ["emberedge", "widowmaker", "aureole", "lastlight"]

FX_JS = r"""() => {
  /* A deterministic particle field, drawn into the arena transform right after
     drawUltOver, so it sits where the ult art sits: over the fighters, under
     the HUD. Wrapping the method rather than drawing after AC.__draw is what
     keeps that layering honest -- readouts_build.py split the readouts out of
     the bloom's source on purpose, and a late overlay would land on the wrong
     side of that split. */
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

  window.__fx = {
    n: 0, parts: [], t: 0, spec: null,

    /* Spawned as data, not as a loop over Math.random: index i always draws
       the same numbers in the same order, so a re-run is bit-identical and a
       difference between arms is the spec and nothing else. Section 6.1. */
    reset(spec, seed, geom, scale){
      this.spec = spec;
      this.parts = []; this.t = 0;
      this.n = spec ? Math.round(spec.n * (scale === undefined ? 1 : scale)) : 0;
      if (!this.n) return;
      const rnd = mulberry32((seed | 0) ^ 0x51AB1E);
      const S = spec, L = geom || {};
      for (let i = 0; i < this.n; i++){
        const a = rnd() * Math.PI * 2;
        /* squared, so most are slow and a few carry. A uniform speed reads as
           a shell rather than as a spray. */
        const sp = S.sp[0] + rnd() * rnd() * (S.sp[1] - S.sp[0]);
        let ox = 0, oy = 0, vx, vy;
        if (S.mode === "beam"){
          const u = rnd();
          const dx = (L.tx - L.x) || 0, dy = (L.ty - L.y) || 0;
          ox = dx * u; oy = dy * u;
          const len = Math.hypot(dx, dy) || 1;
          ox += (-dy / len) * (rnd() - 0.5) * 26;
          oy += (dx / len) * (rnd() - 0.5) * 26;
          vx = Math.cos(a) * sp * 0.4; vy = Math.sin(a) * sp * 0.4;
        } else if (S.mode === "field"){
          /* sqrt so the disc fills evenly instead of clustering at the middle */
          const rr = Math.sqrt(rnd()) * (L.radius || 200);
          ox = Math.cos(a) * rr; oy = Math.sin(a) * rr;
          const b = rnd() * Math.PI * 2;
          vx = Math.cos(b) * sp; vy = Math.sin(b) * sp;
        } else {
          vx = Math.cos(a) * sp; vy = Math.sin(a) * sp - (S.up || 0);
        }
        const heavy = rnd() < (S.heavy || 0);
        this.parts.push({
          x: ox, y: oy, vx: vx, vy: vy,
          birth: rnd() * (S.spawn || 0),
          life: S.life[0] + rnd() * (S.life[1] - S.life[0]),
          age: -1,
          r: heavy ? 2.6 + rnd() * 3.4
                   : S.size[0] + rnd() * (S.size[1] - S.size[0]),
          spin: (rnd() - 0.5) * 18, rot: rnd() * 6.28,
          heavy: heavy, seedv: rnd(),
        });
      }
    },

    /* FIXED dt, section 6.2. A field integrated on frame time is a clip that
       cannot be rebuilt from its seed. */
    step(dt){
      const S = this.spec;
      if (!S) return;
      this.t += dt;
      const d = Math.exp(-S.drag * dt);
      for (const p of this.parts){
        if (this.t < p.birth) continue;              /* not emitted yet */
        if (p.age < 0) p.age = 0;
        if (p.age > p.life) continue;
        p.age += dt;
        p.vx *= d; p.vy = p.vy * d + S.grav * dt;
        p.x += p.vx * dt; p.y += p.vy * dt;
        p.rot += p.spin * dt;
      }
    },

    draw(c, cx, cy, aff){
      if (!this.n) return;
      const hot = "#FFF6E2",
            mid = (aff && aff.core) || "#FF9A3C",
            cool = (aff && aff.dark) || "#8C2A0A";
      c.save();
      c.translate(cx, cy);
      /* MOTES ADDITIVE, DEBRIS NOT. The bloom reads the emissive layer, so a
         mote drawn `lighter` becomes light while a chunk that is not stays an
         object. CLAUDE.md 4.1b: a thing that is only ever added is not an
         object, it is a hole. */
      for (const p of this.parts){
        if (p.age < 0 || p.age > p.life) continue;
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
          c.fillStyle = k < 0.5 ? mid : cool;
          c.fillRect(-p.r, -p.r * 0.6, p.r * 2, p.r * 0.35);
          c.restore();
        } else {
          c.globalCompositeOperation = "lighter";
          c.globalAlpha = fade;
          /* cooling: white -> the school's own core -> its dark. One flat
             colour never says a particle is losing energy. */
          c.fillStyle = k < 0.25 ? hot : (k < 0.62 ? mid : cool);
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
    const F = window.__fx, u = m.ultFx;
    if (!u || !F.n || !F.spec) return;
    /* a burst happens AT the foe; a beam and a field belong to the caster */
    const at = F.spec.mode === "burst" ? [u.tx, u.ty] : [u.x, u.y];
    F.draw(this.ctx, at[0], at[1], u.aff);
  };
  return true;
}"""

SETUP_JS = r"""([id, foe, block, life, w, h]) => {
  AC.setResolution(w, h);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(id, foe, 25064);
  m.introT = 0;
  const A = AC.CONFIG.arena;
  m.a.x = A.w * 0.30; m.a.y = A.h * 0.30;
  m.b.x = A.w * 0.66; m.b.y = A.h * 0.58;
  m.a.vx = m.a.vy = m.b.vx = m.b.vy = 0;
  m.shake = 0;
  window.__lab = { m: m, block: block, life: life };
  return { life: life,
           geom: { x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y,
                   radius: block.radius || 220 } };
}"""

FRAME_JS = r"""([t, mt, q, dt]) => {
  const L = window.__lab, m = L.m, b = L.block;
  m.t = mt;
  m.ultFx = Object.assign({}, b, {
    src: "a", tgt: "b", x: m.a.x, y: m.a.y, tx: m.b.x, ty: m.b.y,
    aff: m.a.aff, t: t, life: L.life });
  if (dt > 0){
    /* the sim's own dt, in two sub-steps, so the field integrates at 120 Hz
       exactly as the physics does */
    window.__fx.step(dt / 2); window.__fx.step(dt / 2);
  }
  const real = Math.random;
  Math.random = function(){ return 0.5; };   /* no unseeded noise in the frame */
  AC.__draw(m);
  Math.random = real;
  const u = document.getElementById('cv').toDataURL('image/jpeg', q);
  return u.slice(u.indexOf(',') + 1);
}"""

COST_JS = r"""([spec, counts, reps, n]) => {
  /* WHAT DOES THE FIELD COST PER FRAME, on this canvas, on the real GPU?
     The same shape post_cost.py uses: the median of `reps` repetitions of `n`
     draws, because one scheduling hiccup in a run of five should not become
     the answer. */
  const L = window.__lab, m = L.m, b = L.block;
  m.ultFx = Object.assign({}, b, { src:"a", tgt:"b", x:m.a.x, y:m.a.y,
                                   tx:m.b.x, ty:m.b.y, aff:m.a.aff,
                                   t:0.35, life:L.life });
  const med = (a) => { a = a.slice().sort((x,y)=>x-y); return a[a.length>>1]; };
  const ctx = document.getElementById('cv').getContext('2d');

  /* FORCE THE RASTER, ONCE, AT THE END -- postcost.js's technique, and the
     reason this is a rewrite. Canvas2D submission is asynchronous, so timing a
     loop of draws with no readback measures how fast the calls were QUEUED.
     The first version did exactly that and reported a 1.20 ms baseline for a
     frame post_cost.py measures at 9.06 on the same canvas: an eightfold
     error, in the flattering direction, on the number about to decide whether
     a session of GPU work happened.

     Inside a rAF as well -- outside one the compositor can defer the whole
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
      const s = c ? Object.assign({}, spec, { n: c }) : null;
      window.__fx.reset(s, 25064, { x:m.a.x, y:m.a.y, tx:m.b.x, ty:m.b.y,
                                    radius: 220 }, 1);
      for (let i = 0; i < 40; i++) window.__fx.step(1/120);   /* mid-flight */
      const reps_ms = [];
      for (let r = 0; r < reps; r++) reps_ms.push(await timed(n));
      out.push({ n: c, ms: med(reps_ms) });
    }
    window.__fx.reset(null, 25064, {}, 0);
    return out;
  })();
}"""


def block_for(ident, lib, burst_json):
    """A REAL captured block, or nothing. Never a hand-written one."""
    if ident == "emberedge":
        return json.loads(burst_json.read_text(encoding="utf-8"))["block"], "burst"
    e = lib.get(ident)
    if not e or not e.get("phases"):
        return None, None
    ph = e["phases"][-1]
    return e["blocks"].get(ph), ph


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default=str(BUILD))
    ap.add_argument("--burst", default=str(BURST))
    ap.add_argument("--ids", default=",".join(DEFAULT_IDS))
    ap.add_argument("--arms", default="off,heavy")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--lead", type=float, default=0.30)
    ap.add_argument("--tail", type=float, default=1.1)
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--q", type=float, default=0.95)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--out", default=str(REPO / "07-shorts" / "particles"))
    ap.add_argument("--cost", action="store_true",
                    help="ms/frame against particle count instead of clips. "
                         "The number that decides whether §3.2's GPU runtime "
                         "is needed at all")
    ap.add_argument("--cost-w", type=int, default=453,
                    help="the app's canvas, the only realtime surface; the "
                         "video is captured offline")
    args = ap.parse_args()

    path = pathlib.Path(args.game).resolve()
    bp = pathlib.Path(args.burst)
    if not path.exists() or not bp.exists():
        print(f"! need {path} and {bp}")
        return 2
    lib = json.loads(LIB.read_text(encoding="utf-8")) if LIB.exists() else {}
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    for a in arms:
        if a not in ARMS:
            print(f"! unknown arm {a!r}; have {list(ARMS)}")
            return 2
    for i in ids:
        if i not in SPECS:
            print(f"! no spec for {i!r}; have {list(SPECS)}")
            return 2

    out = pathlib.Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    H = round(args.w * 16 / 9)
    dt = 1.0 / args.fps

    if args.cost:
        # THROUGH ELECTRON, NOT PLAYWRIGHT. Playwright launches --disable-gpu,
        # so its Canvas rasteriser is SwiftShader and a number off it measures
        # SwiftShader: the first run reported a 43 ms baseline for a frame the
        # app draws in 9. post_cost.py's header says exactly this and defaults
        # to Electron; this follows it.
        exe = next((q for q in EL_BIN if q.exists()), None)
        if exe is None:
            print("! no Electron in app/node_modules -- run `npm install` in "
                  "app/.\n  This measurement is NOT worth taking through "
                  "Playwright; see the header.")
            return 2
        W, ident = args.cost_w, ids[0]
        blk, _ = block_for(ident, lib, bp)
        with game(game_path=path) as (page, _e):
            lives = life_map(path, page)
        life = blk.get("life") or lives.get(ident) or 1.5
        cfg = {"fx": FX_JS, "setup": SETUP_JS,
               "setupArgs": [ident, "bulwarden", blk, life, W,
                             round(W * 16 / 9)],
               "cost": COST_JS,
               "costArgs": [SPECS[ident], [0, 120, 420, 900, 2000], 5, 30]}
        # A file, not an argument: cfg carries whole JS sources and
        # electron.cmd is a batch shim, so cmd.exe parses the `>` in them and
        # dies with "> was unexpected at this time" before Electron starts.
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
        print(f"\nPARTICLE COST  {ident}  {W}x{round(W*16/9)} (the app's "
              f"canvas)  median of {5} x {30} draws")
        print(f"  {rend}\n")
        print(f"  {'particles':>10}{'ms/frame':>11}{'added':>9}"
              f"{'% of 16.67':>12}")
        for row in rows:
            print(f"  {row['n']:>10}{row['ms']:>11.3f}{row['ms']-base:>9.3f}"
                  f"{100*row['ms']/16.67:>11.0f}%")
        print(f"\n  THE APP HAS 4.77 ms OF HEADROOM (post_cost.py, "
              f"2026-08-28).\n  A Canvas 2D field that fits inside it does not "
              f"need §3.2's GPU runtime\n  to reach the app -- and the video, "
              f"captured offline, never needed one.")
        return 0

    ff = resolve_ffmpeg("ffmpeg")
    made = []
    with game(game_path=path) as (page, errors):
        lives = life_map(path, page)
        page.evaluate(FX_JS)
        for ident in ids:
            blk, ph = block_for(ident, lib, bp)
            if blk is None:
                print(f"! {ident}: no captured block; skipping rather than "
                      f"writing one by hand")
                continue
            life = blk.get("life") or lives.get(ident)
            if not life:
                print(f"! {ident}: no life in the block or in Match's map; "
                      f"skipping rather than guessing")
                continue
            info = page.evaluate(SETUP_JS,
                                 [ident, "bulwarden", blk, life, args.w, H])
            spec = SPECS[ident]
            print(f"\n{ident:<12} {spec['mode']:<6} phase={ph or '-':<6} "
                  f"life={life:.2f}s  n={spec['n']}")
            n_lead = round(args.lead * args.fps)
            n_body = round((life + args.tail) * args.fps)
            for arm in arms:
                page.evaluate(
                    "([s, g, k]) => window.__fx.reset(s, 25064, g, k)",
                    [spec, info["geom"], ARMS[arm]])
                tmp = out / f"_f_{ident}_{arm}"
                if tmp.exists():
                    shutil.rmtree(tmp)
                tmp.mkdir(parents=True)
                i = 0
                for f in range(n_lead):
                    b64 = page.evaluate(FRAME_JS,
                                        [-1.0, f / args.fps, args.q, 0.0])
                    (tmp / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(b64))
                    i += 1
                for f in range(n_body):
                    t = min(life, f / args.fps)
                    b64 = page.evaluate(
                        FRAME_JS, [t, (n_lead + f) / args.fps, args.q, dt])
                    (tmp / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(b64))
                    i += 1
                mp4 = out / f"{ident}-{arm}.mp4"
                subprocess.run(
                    [ff, "-y", "-hide_banner", "-loglevel", "error",
                     "-framerate", str(args.fps), "-i", str(tmp / "f_%05d.jpg"),
                     "-c:v", "libx264", "-preset", "slow", "-crf",
                     str(args.crf), "-pix_fmt", "yuv420p",
                     "-movflags", "+faststart", str(mp4)], check=True)
                shutil.rmtree(tmp)
                made.append(mp4)
                print(f"   {arm:<6} {round(spec['n']*ARMS[arm]):>4} particles "
                      f"{i} frames -> {mp4.name}  "
                      f"{mp4.stat().st_size/1e6:.1f} MB")
        if errors:
            print("\n! page errors:")
            for e in errors[:8]:
                print("   ", e)
            return 1

    print(f"\n{len(made)} clips in {out}")
    print("Same set-piece, same seed, same length in every pair. `off` is the "
          "game\nexactly as it ships; the only difference is the field.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
