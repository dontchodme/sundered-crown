#!/usr/bin/env python3
"""THE IGNITION OPEN — look prototype, rendered off the build of record.

Four variants of the first ~5.4s of the same fight, same seed:

    control     the open as it ships today (wide hall, cold relics)
    ignition    the relics IGNITE: staggered flare + a global glow power-on
    camera      the opening owns the camera: fighter A, cut, fighter B, pull wide
    both        camera + ignition, flares synced to the cuts

Nothing in 02-chain/ is edited. Two in-memory patches at capture time, the
BLUR_SCALE_JS pattern from cinema_clip.py:

  1. `Renderer.draw`'s both-relics-must-fit feasibility clamp is gated on
     `window.__openShot`. That clamp is CORRECT for mid-fight cuts and is
     exactly why an opening shot cannot exist today: at spawn separation
     (~503 su) it pulls any asked zoom back to ~1.0. The gate is the
     prototype of "the opening owns the camera" (FX brief §3.4's argument,
     aimed at t=0).
  2. `shadowBlur` gains a global time multiplier so every glow in the hall
     can power on over the first second (device-space, both cv and _bbuf,
     same guard as BLUR_SCALE_JS).

The flare itself is drawn OVER the composited frame in the relic's own
affinity palette, in sim coordinates through the renderer's real transform
(pad/arenaTop/_cineCam/scale/k). Draw and grab are one evaluate — atomic,
scrunch-harness lesson (a).

Deterministic: eases are pure functions of wall time; no Math.random
anywhere in the overlay or the driver. (The capture as a whole inherits the
engine's known nondeterminism — shake, synth noise — which is out of scope
here, v43b §16.)

RUNTIME CAVEAT: this container is not the pinned pair (RUNTIME-DRIFT.md).
The fight a seed names here can differ from the same seed on yert. The A/B
is internally valid — all four variants render from one runtime — but
re-pick the seed on the pinned runtime before filming anything that ships.

    python ignition_lab.py --scan --a ironhail --b oathwound --n 40
    python ignition_lab.py --render --a ironhail --b oathwound --seed <S>

(On yert: `python`, not `python3`, and ffmpeg needs the PATH export from
CLAUDE.md §5 in a bare terminal.)

FIRST RENDERED 2026-08-30 in a Cowork container off sc-paradox-crucible,
ironhail v oathwound seed 55196 (first clank 2.22s there; re-scan on the
pinned runtime). Output: 05-reference/v46-ignition/.
"""
from __future__ import annotations

import argparse, base64, json, pathlib, subprocess, sys, time

from scpage import game

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out-ignition"

# ---------------------------------------------------------------- patches ---

DRAW_GATE_JS = r"""() => {
  /* Gate the both-relics-must-fit clamp on window.__openShot. The clamp is
     right for cuts; the opening shot is the one framing decision it must not
     make. Instance patch via source surgery; page untouched on disk. */
  if (window.__drawGated) return "already";
  const src = AC.renderer.draw.toString();
  const anchor = "if (z > 1.02 && m){";
  if (src.split(anchor).length !== 2) return "ANCHOR NOT FOUND OR NOT UNIQUE";
  const patched = src.replace(anchor, "if (z > 1.02 && m && !window.__openShot){");
  AC.renderer.draw = eval("(function " + patched + ")");
  window.__drawGated = true;
  return "ok";
}"""

BLUR_IGNITE_JS = r"""() => {
  /* Global glow power-on: every shadowBlur is multiplied by window.__igniteMul.
     Same property, same canvas guard as cinema_clip.py's BLUR_SCALE_JS; at
     __igniteMul === 1 the setter is exact identity. */
  if (window.__blurIgnite) return "already";
  const cv = document.getElementById('cv');
  const proto = CanvasRenderingContext2D.prototype;
  const base = Object.getOwnPropertyDescriptor(proto, 'shadowBlur');
  window.__igniteMul = 1;
  Object.defineProperty(proto, 'shadowBlur', {
    configurable: true,
    get(){ return base.get.call(this); },
    set(v){
      if (v && window.__igniteMul !== 1 && this.canvas &&
          (this.canvas === cv || this.canvas === AC.renderer._bbuf)) {
        v = v * window.__igniteMul;
      }
      base.set.call(this, v);
    }
  });
  window.__blurIgnite = true;
  return "ok";
}"""

# ------------------------------------------------------ driver and overlay ---

OPEN_JS = r"""() => {
  const easeOutCubic = u => 1 - Math.pow(1 - u, 3);
  const smooth = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);
  const eob = (u, c) => { u = Math.min(1, Math.max(0, u));      // ease-out-back
    const c1 = c === undefined ? 1.70158 : c, c3 = c1 + 1;
    return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2); };
  const lerp = (a, b, u) => a + (b - a) * u;

  /* CFG is set per variant from python. Times are WALL seconds; during the
     opening there are no cuts, so wall time and match time agree. */
  window.__openCfg = null;

  /* ---- the camera driver: runs AFTER CINE.pump, so its writes are what the
     renderer reads. Idle update() forces zoom to 1 every frame, which is why
     this cannot be done by setting a target once. Handheld: idle zeroes
     hx/hy, so the opening borrows the engine's own two-frequency drift at a
     small amplitude — deterministic, same formula, CINE.update's. */
  window.__openCam = function (wall, m) {
    const cfg = window.__openCfg;
    const release = () => {
      window.__openShot = false;
      if (window.__osSave !== undefined) { CINE.overscan = window.__osSave;
                                           window.__osSave = undefined; }
    };
    if (!cfg || !cfg.cam) { release(); return; }
    const S = cfg.shots;
    const last = S[S.length - 1];
    if (wall >= last.t1) { release(); return; }
    let shot = null;
    for (const s of S) if (wall >= s.t0 && wall < s.t1) { shot = s; break; }
    if (!shot) { release(); return; }
    /* The lean clamp allows (1-1/z)*overscan of half-frame travel; at the
       shipped 0.55 a corner spawn pins against the frame edge. The opening
       may lean further — the floor bleed covers it — restored on release. */
    if (window.__osSave === undefined) { window.__osSave = CINE.overscan; }
    CINE.overscan = 0.95;
    const u = (wall - shot.t0) / (shot.t1 - shot.t0);
    const A = AC.CONFIG.arena;
    const pos = id => id === 'a' ? [m.a.x, m.a.y]
              : id === 'b' ? [m.b.x, m.b.y]
              : id === 'mid' ? [(m.a.x + m.b.x) / 2, (m.a.y + m.b.y) / 2]
              : [A.w / 2, A.h / 2];
    const p0 = pos(shot.from || shot.at), p1 = pos(shot.to || shot.at);
    const e = shot.ease === 'smooth' ? smooth(u) : easeOutCubic(u);
    const sx = lerp(p0[0], p1[0], e), sy = lerp(p0[1], p1[1], e);
    const z = lerp(shot.z0, shot.z1, e);
    window.__openShot = z > 1.02;
    /* The renderer zooms ABOUT (fx·scale) — the focus point keeps its screen
       position, which leaves a corner spawn magnified in its corner. To put
       the SUBJECT at frame centre C, solve for the pivot p from
       s' = p + z(s − p) = C  →  p = (C − z·s)/(1 − z), then hand the renderer
       fx = p/scale. Blend the pivot back to C as z approaches 1, where the
       transform tends to identity and the formula tends to a pole. */
    const r = AC.renderer, sc = r.scale;
    const C = [r.aw / 2, r.ah / 2];
    const spx = [sx * sc, sy * sc];
    let p;
    if (z > 1.06) {
      p = [(C[0] - z * spx[0]) / (1 - z), (C[1] - z * spx[1]) / (1 - z)];
      const w = Math.min(1, (z - 1.02) / 0.30);   // fade the pole away
      p = [lerp(C[0], p[0], w), lerp(C[1], p[1], w)];
    } else p = C.slice();
    const amp = (cfg.handheld === undefined ? 2.6 : cfg.handheld) *
                Math.min(1, (z - 1) / 0.6);
    CINE.hx = (Math.sin(CINE.hh * 2.30) * 0.62 + Math.sin(CINE.hh * 3.71 + 1.1) * 0.38) * amp;
    CINE.hy = (Math.sin(CINE.hh * 1.93 + 0.6) * 0.58 + Math.sin(CINE.hh * 4.17) * 0.42) * amp;
    CINE.zoom = z;
    CINE.fx = CINE.tfx = p[0] / sc; CINE.fy = CINE.tfy = p[1] / sc;
  };

  /* ---- the glow power-on: 0.30 -> overshoot ~1.42 -> exactly 1.0. */
  window.__openSwell = function (wall) {
    const cfg = window.__openCfg;
    if (!cfg || !cfg.ignite) { window.__igniteMul = 1; return; }
    const T = 0.95, u = wall / T;
    window.__igniteMul =
      u >= 1 ? 1
      : u < 0.5 ? lerp(0.30, 1.42, easeOutCubic(u / 0.5))
      : lerp(1.42, 1.0, smooth((u - 0.5) / 0.5));
  };

  /* ---- the flare, drawn over the composited frame in sim coordinates.
     Transform replicated from Renderer.draw: setTransform(k) · translate(pad,
     arenaTop) · [cine push] · scale(scale). Shake and punch are zero before
     first contact, which is the only window this draws in. */
  window.__openFx = function (wall, m) {
    const cfg = window.__openCfg;
    if (!cfg || !cfg.ignite) return;
    const r = AC.renderer, c = r.ctx;
    const jobs = [[m.a, cfg.flareA], [m.b, cfg.flareB]];
    c.save();
    c.setTransform(r.k, 0, 0, r.k, 0, 0);
    c.translate(r.pad, r.arenaTop);
    if (r._cineCam) {
      const [px, py, z] = r._cineCam;
      c.translate(px, py); c.scale(z, z); c.translate(-px, -py);
    }
    c.scale(r.scale, r.scale);
    c.globalCompositeOperation = 'lighter';
    for (const [f, t0] of jobs) {
      if (t0 === undefined || t0 === null) continue;
      const t = wall - t0;
      if (t < 0 || t > 0.9) continue;
      const u = t / 0.9;
      /* corona — the relic's own glow colour, overshooting then settling */
      const R = 96 * eob(Math.min(1, t / 0.55), 2.2);
      const ca = t < 0.20 ? 0.80 * (t / 0.20)
                          : 0.80 * Math.pow(1 - (t - 0.20) / 0.70, 1.4);
      if (ca > 0.01 && R > 1) {
        const g = c.createRadialGradient(f.x, f.y, 2, f.x, f.y, R);
        g.addColorStop(0, f.aff.glow);
        g.addColorStop(0.55, f.aff.core);
        g.addColorStop(1, 'rgba(0,0,0,0)');
        c.globalAlpha = ca;
        c.fillStyle = g;
        c.beginPath(); c.arc(f.x, f.y, R, 0, Math.PI * 2); c.fill();
      }
      /* expanding ring — the strike's report */
      const ru = Math.min(1, t / 0.62);
      if (ru < 1) {
        c.globalAlpha = 0.55 * (1 - ru);
        c.strokeStyle = f.aff.core;
        c.lineWidth = 9 * (1 - ru) + 1.5;
        c.beginPath();
        c.arc(f.x, f.y, 20 + 150 * easeOutCubic(ru), 0, Math.PI * 2);
        c.stroke();
      }
      /* white core strike, 3-4 frames */
      if (t < 0.14) {
        const cu = t / 0.14;
        c.globalAlpha = 0.95 * Math.pow(1 - cu, 0.8);
        c.fillStyle = '#FFFFFF';
        c.beginPath(); c.arc(f.x, f.y, 12 + 36 * cu, 0, Math.PI * 2); c.fill();
      }
    }
    c.restore();
    c.globalAlpha = 1;
    c.globalCompositeOperation = 'source-over';
  };
  return "ok";
}"""

# ---- capture harness: cinema_clip.py's HARNESS, trimmed to what this lab
# needs (no card, no cold-open, no motion blur), with three hook lines for the
# opening driver. renderAudio is carried VERBATIM.

HARNESS = r"""
window.__clip = {
  m: null, events: [], curve: [], wall: 0, acc: 0, on: true,

  init(idA, idB, seed, on) {
    const AC = window.AC;
    this.on = on; this.events = []; this.curve = []; this.wall = 0; this.acc = 0;
    window.__frozen = true;
    CINE.on = on; CINE.interp = true; CINE.reset(); CINE.acc = 0;
    if (on) { const p = cinePlan(idA, idB, seed); CINE.plan = p.cuts; }
    else CINE.plan = [];
    const m = new AC.Match(idA, idB, seed);
    m.introT = 0;
    this.m = m; window.__match = m; AC.__inject && AC.__inject(m);
    const self = this;
    AC.SFX.play = function (kind, p) {
      self.events.push({ t: self.wall, kind, p: p || {} });
    };
    AC.SFX.resume = function () {};
    window.__openSwell && window.__openSwell(0);
    window.__openCam && window.__openCam(0, m);
    AC.__draw(m);
    return { seed: m.seed, t: m.t,
             cuts: CINE.plan.map(c => +c.t.toFixed(2)) };
  },

  _sub(raw) {
    const AC = window.AC, m = this.m, dt = AC.CONFIG.physics.dt;
    let alpha = 0;
    if (this.on) {
      alpha = CINE.pump(raw, m, 1);
    } else {
      this.acc += raw;
      let steps = 0;
      while (this.acc >= dt && steps < 4000) { m.step(dt); this.acc -= dt; steps++; }
    }
    /* the opening drives the camera AFTER the pump, so its writes are what
       the renderer reads; idle update() would otherwise force zoom to 1 */
    window.__openSwell && window.__openSwell(this.wall);
    window.__openCam && window.__openCam(this.wall, m);
    if (alpha > 0) CINE.drawLerped(AC.renderer, m, alpha); else AC.__draw(m);
    window.__openFx && window.__openFx(this.wall, m);
  },

  frame(raw, q) {
    const m = this.m;
    this._sub(raw);
    this.wall += raw;
    this.curve.push([ +this.wall.toFixed(4),
                      this.on ? +CINE.timeScale.toFixed(4) : 1,
                      this.on ? +CINE.send.wet.toFixed(3) : 0,
                      this.on ? Math.round(CINE.send.lp) : 20000,
                      this.on ? +CINE.send.dry.toFixed(3) : 1,
                      +m.t.toFixed(4) ]);
    const url = q === null
      ? document.getElementById('cv').toDataURL('image/png')
      : document.getElementById('cv').toDataURL('image/jpeg', q);
    return { i: url.slice(url.indexOf(',') + 1),
             o: m.over, t: m.t, c: m.clankCount,
             sm: m.scrunchMode || null };
  },

  async renderAudio(dur, tailArg) {
    const AC = window.AC, sr = 48000;
    const tail = (tailArg === undefined ? 2.4 : tailArg) + 0.5;
    const oc = new OfflineAudioContext(2, Math.ceil((dur + tail) * sr), sr);
    let cursor = 0;
    const proxy = new Proxy(oc, {
      get(t, k) {
        if (k === 'currentTime') return cursor;
        const v = Reflect.get(t, k);
        return typeof v === 'function' ? v.bind(t) : v;
      },
    });
    const input = oc.createGain();
    const lp = oc.createBiquadFilter(); lp.type = 'lowpass'; lp.Q.value = 0.7;
    const dry = oc.createGain();
    const conv = oc.createConvolver(); conv.buffer = CineAudio.hall(oc, 2.6, 2.4);
    const wet = oc.createGain(); wet.gain.value = 0;
    input.connect(lp); lp.connect(dry); dry.connect(oc.destination);
    lp.connect(conv); conv.connect(wet); wet.connect(oc.destination);
    let pw = -1, pl = -1, pd = -1;
    for (const [t, ts, w, f, d] of this.curve) {
      if (w !== pw) { wet.gain.setValueAtTime(w, t); pw = w; }
      if (f !== pl) { lp.frequency.setValueAtTime(f, t); pl = f; }
      if (d !== pd) { dry.gain.setValueAtTime(d, t); pd = d; }
    }
    const S = Object.create(Object.getPrototypeOf(AC.SFX));
    S.ok = true; S.on = true; S.ctx = proxy;
    S.bus = AC.SFX.constructor.buildChain(oc, input);
    S.noise = S._noiseBuffer.call({ ctx: oc });
    for (const e of this.events) { cursor = Math.max(0, e.t); S.play(e.kind, e.p); }
    const bedT = []; let bt = 0, pwall = 0;
    for (const row of this.curve) {
      const [w, ts] = row;
      bt += Math.max(0.06, Math.min(1, this.on ? ts : 1)) * (w - pwall);
      pwall = w; bedT.push(bt);
    }
    const sealMatch = AC.CONFIG.acts.slice(1).map(a => a.t);
    const sealBed = [];
    for (const st of sealMatch) {
      const i = this.curve.findIndex(r => r[5] >= st);
      if (i >= 0) sealBed.push(+bedT[i].toFixed(3));
    }
    let bedBuf = null;
    try {
      const bd = bt + 4;
      const ob = new OfflineAudioContext(2, Math.ceil(bd * 44100), 44100);
      const S2 = Object.create(Object.getPrototypeOf(AC.SFX));
      S2.ok = true; S2.on = true; S2.ctx = ob;
      S2.bus = ob.createGain(); S2.bus.connect(ob.destination);
      S2.noise = S2._noiseBuffer.call({ ctx: ob });
      S2.bed.call(S2, 0, bd, sealBed);
      bedBuf = await ob.startRendering();
    } catch (e) { bedBuf = null; }
    if (bedBuf) {
      const src = oc.createBufferSource(); src.buffer = bedBuf;
      const g = oc.createGain(); g.gain.value = 0.9;
      src.connect(g); g.connect(input);
      let pr = -1;
      for (const [t, ts] of this.curve) {
        const v = Math.max(0.06, Math.min(1, this.on ? ts : 1));
        if (Math.abs(v - pr) > 0.01) { src.playbackRate.setValueAtTime(v, t); pr = v; }
      }
      src.start(0);
    }
    const buf = await oc.startRendering();
    const n = buf.length, L = buf.getChannelData(0), R = buf.getChannelData(1);
    const bytes = new Uint8Array(44 + n * 4), dv = new DataView(bytes.buffer);
    const wr = (o, s) => { for (let i = 0; i < s.length; i++) dv.setUint8(o + i, s.charCodeAt(i)); };
    wr(0, 'RIFF'); dv.setUint32(4, 36 + n * 4, true); wr(8, 'WAVEfmt ');
    dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 2, true);
    dv.setUint32(24, sr, true); dv.setUint32(28, sr * 4, true);
    dv.setUint16(32, 4, true); dv.setUint16(34, 16, true);
    wr(36, 'data'); dv.setUint32(40, n * 4, true);
    let o = 44;
    for (let i = 0; i < n; i++) {
      for (const C of [L, R]) {
        let v = Math.max(-1, Math.min(1, C[i]));
        dv.setInt16(o, v < 0 ? v * 32768 : v * 32767, true); o += 2;
      }
    }
    let bin = '';
    for (let i = 0; i < bytes.length; i += 8192)
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 8192));
    return btoa(bin);
  },
};
"""

SCAN_JS = r"""([a, b, seed, horizon]) => {
  window.__frozen = true;
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const dt = AC.CONFIG.physics.dt;
  const m = new AC.Match(a, b, seed >>> 0); m.introT = 0;
  let clank = null;
  for (let k = 0; k < Math.round(horizon / dt) && !m.over; k++) {
    const c0 = m.clankCount;
    m.step(dt);
    if (clank === null && m.clankCount > c0) { clank = m.t; break; }
  }
  const plan = cinePlan(a, b, seed >>> 0);
  return JSON.stringify({
    clank, firstCut: plan.cuts.length ? +plan.cuts[0].t.toFixed(2) : null,
    cuts: plan.cuts.map(c => +c.t.toFixed(2)) });
}"""

# The four variants. Camera shots: fighter A, hard cut to fighter B, pull wide
# — timed so the pull lands just before a ~2.3s first clank arms the scrunch.
SHOTS = [
    {"t0": 0.00, "t1": 0.85, "at": "a", "z0": 2.25, "z1": 2.02},
    {"t0": 0.85, "t1": 1.55, "at": "b", "z0": 2.25, "z1": 2.02},
    {"t0": 1.55, "t1": 2.35, "from": "b", "to": "center",
     "z0": 2.02, "z1": 1.00, "ease": "smooth"},
]
VARIANTS = {
    "control":  {"cam": False, "ignite": False},
    "ignition": {"cam": False, "ignite": True,  "flareA": 0.10, "flareB": 0.55},
    "camera":   {"cam": True,  "ignite": False, "shots": SHOTS},
    "both":     {"cam": True,  "ignite": True,  "shots": SHOTS,
                 "flareA": 0.10, "flareB": 0.95},
}
LABELS = {"control": "CONTROL — AS SHIPS TODAY", "ignition": "IGNITION",
          "camera": "OPENING CAMERA", "both": "CAMERA + IGNITION"}


def scan(args):
    rows = []
    with game(game_path=(HERE / args.game).resolve()) as (page, errors):
        for i in range(args.n):
            seed = args.seed0 + i * args.stride
            r = json.loads(page.evaluate(SCAN_JS, [args.a, args.b, seed, 8.0]))
            ok = (r["clank"] is not None and args.lo <= r["clank"] <= args.hi
                  and (r["firstCut"] is None or r["firstCut"] >= args.cut_after))
            rows.append((seed, r, ok))
            if ok:
                print(f"  CANDIDATE seed {seed}: first clank {r['clank']:.2f}s, "
                      f"first cut {r['firstCut']}, cuts {r['cuts'][:4]}")
        if errors:
            print("page errors:", errors[:3], file=sys.stderr)
    good = [s for s, r, ok in rows if ok]
    print(f"\n{len(good)}/{args.n} candidates with clank in "
          f"[{args.lo},{args.hi}]s and no cut before {args.cut_after}s")
    if good:
        print("PICK:", good[0])
    return 0


def render(args):
    OUT.mkdir(exist_ok=True)
    fps, q, secs = args.fps, args.q, args.secs
    n_frames = int(secs * fps)
    meta = {}
    with game(game_path=(HERE / args.game).resolve()) as (page, errors):
        page.evaluate(f"AC.setResolution({args.w}, {round(args.w * 16 / 9)})")
        for name, js, want in (("draw gate", DRAW_GATE_JS, ("ok", "already")),
                               ("blur ignite", BLUR_IGNITE_JS, ("ok", "already")),
                               ("open driver", OPEN_JS, ("ok",))):
            r = page.evaluate(js)
            if r not in want:
                sys.exit(f"! {name} patch failed: {r}")
        page.evaluate(HARNESS)
        for tag, cfg in VARIANTS.items():
            if args.only and tag not in args.only:
                continue
            vdir = OUT / tag
            vdir.mkdir(exist_ok=True)
            for f in vdir.glob("*"):
                f.unlink()
            page.evaluate("([c]) => { window.__openCfg = c; window.__openShot = false; "
                          "window.__igniteMul = 1; }", [cfg])
            info = page.evaluate("([a,b,s]) => window.__clip.init(a,b,s,true)",
                                 [args.a, args.b, args.seed])
            t0 = time.time()
            states = []
            for i in range(n_frames):
                r = page.evaluate("([raw,q]) => window.__clip.frame(raw,q)",
                                  [1.0 / fps, q])
                (vdir / f"f_{i:05d}.jpg").write_bytes(base64.b64decode(r["i"]))
                states.append((r["t"], r["c"], r["sm"]))
            clank_at = next((i / fps for i, s in enumerate(states) if s[1] > 0), None)
            scr_at = next((i / fps for i, s in enumerate(states) if s[2]), None)
            wav_b64 = page.evaluate("([d]) => window.__clip.renderAudio(d, 0)",
                                    [n_frames / fps + 0.2])
            (vdir / "a.wav").write_bytes(base64.b64decode(wav_b64))
            meta[tag] = {"cuts": info["cuts"], "clank_wall": clank_at,
                         "scrunch_wall": scr_at}
            print(f"  {tag}: {n_frames} frames in {time.time()-t0:.0f}s, "
                  f"first clank at {clank_at}s wall, scrunch at {scr_at}s, "
                  f"plan cuts {info['cuts'][:4]}")
        if errors:
            print("page errors:", errors[:6], file=sys.stderr)
            if any("pageerror" in e for e in errors):
                sys.exit("! page errors during capture — do not trust the frames")

    # ---- encode each variant, native 540x960
    for tag in VARIANTS:
        if args.only and tag not in args.only:
            continue
        vdir = OUT / tag
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-framerate", str(fps), "-i", str(vdir / "f_%05d.jpg"),
             "-i", str(vdir / "a.wav"),
             "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
             "-c:v", "libx264", "-preset", "medium", "-crf", "19",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
             "-shortest", "-movflags", "+faststart",
             str(OUT / f"{tag}.mp4")], check=True)
    (OUT / "meta.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="../02-chain/sc-paradox-crucible.html")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--a", default="ironhail")
    ap.add_argument("--b", default="oathwound")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--seed0", type=int, default=46001)
    ap.add_argument("--stride", type=int, default=613)
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--lo", type=float, default=2.1, help="earliest ok first clank")
    ap.add_argument("--hi", type=float, default=2.8, help="latest ok first clank")
    ap.add_argument("--cut-after", type=float, default=3.2,
                    help="no director cut before this")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--q", type=float, default=0.85)
    ap.add_argument("--secs", type=float, default=5.4)
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()
    if args.scan:
        return scan(args)
    if args.render:
        if args.seed is None:
            sys.exit("--render needs --seed (run --scan first)")
        return render(args)
    sys.exit("pass --scan or --render")


if __name__ == "__main__":
    raise SystemExit(main())
