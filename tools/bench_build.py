#!/usr/bin/env python3
"""Build sundered-crown-perf.html: the artifact plus a live performance lab.

Why this exists. Frame cost was measured three ways in this container and the
three disagreed about which draw dominates:

  * `AC.__draw(m)` timed directly              -> 0.8 ms   (v6's number)
  * the same draw with the raster forced       -> 49 ms
  * the same again on the accelerated canvas   -> 590 ms, 95% of it the grain blit

The first is wrong everywhere: Canvas2D returns before it has drawn anything,
so v6 timed command recording. The other two are both "right" for their own
backend, and neither backend is Rick's. A headless container has no GPU, so the
only honest instrument is one that runs in the browser that is actually
stuttering.

This builds a copy of the artifact with:
  * a live HUD: real rAF frame time, median and p95 over a rolling window
  * per-feature kill switches, so a suspect can be A/B'd live at 1x speed
  * BENCH: runs a scripted match and reports median frame time by phase
  * a report you can paste straight back into the session

The game source is not modified beyond guarded hooks, and this file is NOT the
artifact — sundered-crown.html is untouched.
"""
from __future__ import annotations

import argparse

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
# --src/--out so the lab can be pointed at any build in the chain. The point
# is the CONTROL: resume-here §5 says always profile the previous build through
# the same harness, so the way to use this is to build a perf page from the old
# artifact AND from the new one and run BENCH in both.
#
#   python3 bench_build.py --src sundered-crown-all.html --out sc-perf-old.html
#   python3 bench_build.py --src sc-next.html            --out sc-perf-new.html
_ap = argparse.ArgumentParser(description=__doc__)
_ap.add_argument("--src", default="sundered-crown.html")
_ap.add_argument("--out", default="sundered-crown-perf.html")
_A = _ap.parse_args()

SRC = (HERE / _A.src).read_text(encoding="utf-8")
OUT = HERE / _A.out


def rep(src, old, new, label, expect=1):
    n = src.count(old)
    if n != expect:
        sys.exit(f"anchor {label}: found {n}, expected {expect}\n  {old[:90]}")
    return src.replace(old, new)


s = SRC

# --- the switchboard, defined before any game code runs -----------------------
SWITCHBOARD = """<script>
/* Performance lab. Every switch defaults to false = feature ON. */
window.__PERF = {
  off: { shadows:0, grain:0, cracks:0, wash:0, vignette:0, wallglow:0,
         ult:0, motes:0, fx:0, sigil:0, trail:0, status:0, tags:0 },
};
function __sb(v){ return window.__PERF.off.shadows ? 0 : v; }
</script>
"""
s = rep(s, "<script>", SWITCHBOARD + "<script>", "switchboard head", expect=1)

# --- every shadowBlur assignment routes through the switch --------------------
# `[^;\n]+` and not `[^;]+`, and the difference is a shipped broken artifact.
#
# glow_build.py's weapon-glow section carries a COMMENT containing the words
# `shadowBlur = 20`, with no semicolon on that line. The old pattern happily
# matched it and then ran greedily to the next semicolon eleven lines later,
# producing `const _glowCache = new Map());` -- a syntax error that took the
# whole page down with "AC is not defined" and a blank arena. A shadowBlur
# assignment never spans a line in this codebase, so refusing to cross one
# costs nothing and makes prose harmless.
s, n_sb = re.subn(r"shadowBlur\s*=\s*(?!0;)([^;\n]+);", r"shadowBlur = __sb(\1);", s)
if n_sb < 25:
    sys.exit(f"only {n_sb} shadowBlur sites rewritten")

# --- individual suspects ------------------------------------------------------
s = rep(s, "c.drawImage(grain.cv, f.x - gw / 2, f.y - gw / 2, gw, gw);",
        "if (!window.__PERF.off.grain) c.drawImage(grain.cv, f.x - gw / 2, f.y - gw / 2, gw, gw);",
        "grain blit")

s = rep(s, "const cracks = shellCracks(f.side);",
        "const cracks = window.__PERF.off.cracks ? [] : shellCracks(f.side);",
        "cracks")

s = rep(s, """    for (const [f, cy] of [[m.a, H*0.13], [m.b, H*0.87]]){
      const rg = c.createRadialGradient(W*0.5, cy, 0, W*0.5, cy, H*0.52);""",
        """    if (!window.__PERF.off.wash) for (const [f, cy] of [[m.a, H*0.13], [m.b, H*0.87]]){
      const rg = c.createRadialGradient(W*0.5, cy, 0, W*0.5, cy, H*0.52);""",
        "wash")

s = rep(s, """    const vg = c.createRadialGradient(cx, cy, H*0.26, cx, cy, H*0.74);
    vg.addColorStop(0, "#00000000"); vg.addColorStop(1, "#000000BB");
    c.fillStyle = vg; c.fillRect(0, 0, W, H);""",
        """    if (!window.__PERF.off.vignette){
      const vg = c.createRadialGradient(cx, cy, H*0.26, cx, cy, H*0.74);
      vg.addColorStop(0, "#00000000"); vg.addColorStop(1, "#000000BB");
      c.fillStyle = vg; c.fillRect(0, 0, W, H);
    }""", "vignette")

# The wall glow exists in two forms now: the shipped single strokeRect, and
# glow_build.py --walls' four edge strokes. The lab has to hook whichever this
# source has -- a kill switch that silently stopped killing anything would make
# every A/B taken with it a lie, so this asserts it hooked exactly one of them.
WALL_OLD = ("""      c.strokeStyle = "#E0433F"; c.lineWidth = 4;
      c.shadowColor = "#E0433F"; c.shadowBlur = __sb(30);
      c.strokeRect(n, n, W-n*2, H-n*2);""",
            """      c.strokeStyle = "#E0433F"; c.lineWidth = 4;
      if (!window.__PERF.off.wallglow){ c.shadowColor = "#E0433F"; c.shadowBlur = __sb(30); }
      c.strokeRect(n, n, W-n*2, H-n*2);""")
WALL_NEW = ("""      c.strokeStyle = "#E0433F"; c.lineWidth = 4; c.lineCap = "square";
      c.shadowColor = "#E0433F"; c.shadowBlur = __sb(30);""",
            """      c.strokeStyle = "#E0433F"; c.lineWidth = 4; c.lineCap = "square";
      if (!window.__PERF.off.wallglow){ c.shadowColor = "#E0433F"; c.shadowBlur = __sb(30); }""")
# THE THIRD FORM: wallglow_build.py's buffered glow, where the whole effect is
# one call. The switch cannot toggle a `shadowBlur` here because there no
# longer is one on this canvas — the blur happens on a 264x407 buffer inside
# the method. Killing the CALL is the honest equivalent: what the A/B is asked
# to price is the effect, and in this build the effect is the method.
WALL_BUF = ("""      this._wallGlow(c, W, H, n);""",
            """      if (!window.__PERF.off.wallglow) this._wallGlow(c, W, H, n);
      else { c.strokeStyle = "#E0433F"; c.lineWidth = 4;
             c.strokeRect(n, n, W - n*2, H - n*2); }""")
_hooked = 0
for _old, _new in (WALL_OLD, WALL_NEW, WALL_BUF):
    if s.count(_old) == 1:
        s = s.replace(_old, _new, 1); _hooked += 1
if _hooked != 1:
    sys.exit(f"anchor wall glow: hooked {_hooked} forms, expected exactly 1")

s = rep(s, "const s = this._ult(m); if (!s) return;",
        "const s = window.__PERF.off.ult ? null : this._ult(m); if (!s) return;",
        "ult set-pieces", expect=2)

s = rep(s, "    this.drawMotes(m);", "    if (!window.__PERF.off.motes) this.drawMotes(m);", "motes")
s = rep(s, "    this.drawStatus(m, f);", "    if (!window.__PERF.off.status) this.drawStatus(m, f);", "status fx")
s = rep(s, "    this.drawTags(m);", "    if (!window.__PERF.off.tags) this.drawTags(m);", "status tags")
s = rep(s, "    this.drawFx(m);", "    if (!window.__PERF.off.fx) this.drawFx(m);", "fx")

s = rep(s, "    c.rotate(m.t * 0.055);", "    if (window.__PERF.off.sigil) { c.restore(); } else {\n    c.rotate(m.t * 0.055);", "sigil open")
s = rep(s, """    c.closePath(); c.stroke();
    c.restore();

    if (!window.__PERF.off.vignette){""",
        """    c.closePath(); c.stroke();
    c.restore();
    }

    if (!window.__PERF.off.vignette){""", "sigil close")

# --- the lab ------------------------------------------------------------------
LAB = r"""
<style>
#perf{position:fixed;top:8px;left:8px;z-index:99;font:11px ui-monospace,Menlo,monospace;
  background:#0B0910EE;border:1px solid #C9A22755;border-radius:8px;padding:8px 10px;
  color:#E8D5A8;max-width:330px;line-height:1.45}
#perf h4{margin:0 0 6px;font:600 12px system-ui;color:#C9A227;letter-spacing:.04em}
#perf .big{font:600 20px ui-monospace;color:#FFF4D0}
#perf .bad{color:#E0433F} #perf .ok{color:#4FD06B}
#perf label{display:inline-block;width:96px;cursor:pointer;user-select:none}
#perf input{vertical-align:-1px;margin-right:4px}
#perf button{font:600 11px system-ui;background:#C9A227;color:#140F1C;border:0;
  border-radius:5px;padding:5px 9px;cursor:pointer;margin:6px 4px 0 0}
#perf textarea{width:100%;height:150px;margin-top:6px;background:#05040A;color:#9FE8B0;
  border:1px solid #333;border-radius:5px;font:10px ui-monospace;display:none}
#perf .hint{color:#8A7F9A;font-size:10px;margin-top:5px}
</style>
<div id="perf">
  <h4>PERF LAB &mdash; press P to hide</h4>
  <div><span class="big" id="pfMs">--</span> ms/frame &nbsp; <span id="pfFps">--</span> fps
       &nbsp;<span id="pfP95">p95 --</span></div>
  <div id="pfCtx" class="hint">&nbsp;</div>
  <div style="margin-top:6px">
    <label><input type="checkbox" data-k="shadows">shadows</label>
    <label><input type="checkbox" data-k="grain">grain blit</label>
    <label><input type="checkbox" data-k="cracks">cracks</label>
    <label><input type="checkbox" data-k="wash">wash</label>
    <label><input type="checkbox" data-k="vignette">vignette</label>
    <label><input type="checkbox" data-k="sigil">sigil</label>
    <label><input type="checkbox" data-k="wallglow">wall glow</label>
    <label><input type="checkbox" data-k="ult">ult FX</label>
    <label><input type="checkbox" data-k="motes">motes</label>
    <label><input type="checkbox" data-k="fx">sparks</label>
    <label><input type="checkbox" data-k="status">status fx</label>
    <label><input type="checkbox" data-k="tags">status tags</label>
  </div>
  <div class="hint">Ticked = that feature is OFF. Watch the number.</div>
  <button id="pfBench">Full sweep (~4 min)</button>
  <button id="pfQuick">QUICK — use this one (~60s)</button>
  <button id="pfCopy">Copy report</button>
  <textarea id="pfOut" readonly></textarea>
</div>
<script>
(() => {
  const $ = id => document.getElementById(id);
  const box = $('perf');
  for (const el of box.querySelectorAll('input[data-k]'))
    el.onchange = () => { window.__PERF.off[el.dataset.k] = el.checked ? 1 : 0; };
  addEventListener('keydown', e => {
    if (e.key === 'p' || e.key === 'P') box.style.display =
      box.style.display === 'none' ? '' : 'none';
  });

  const med = a => { const b=[...a].sort((x,y)=>x-y); return b[b.length>>1] || 0; };
  const pct = (a,q) => { const b=[...a].sort((x,y)=>x-y); return b[Math.floor(b.length*q)] || 0; };

  /* Live HUD: real rAF deltas. This is the only number that answers "is it
     laggy" — it is the frame the compositor actually got. */
  let ring = [], lastT = performance.now(), benching = false;
  function tick(now){
    const d = now - lastT; lastT = now;
    if (d > 0 && d < 500) ring.push(d);
    if (ring.length > 90) ring.shift();
    if (!benching && ring.length > 20){
      const m = med(ring), p = pct(ring, 0.95);
      $('pfMs').textContent = m.toFixed(1);
      $('pfMs').className = 'big ' + (m > 18 ? 'bad' : 'ok');
      $('pfFps').textContent = (1000/m).toFixed(0);
      $('pfP95').textContent = 'p95 ' + p.toFixed(1);
      const mm = AC.match;
      $('pfCtx').textContent = mm ? `t=${mm.t.toFixed(1)}s  inset=${mm.inset.toFixed(0)}`
        + `  ult=${mm.ultFx ? mm.ultFx.w : '-'}  fx=${mm.fx.length}`
        + `  dmg=${(1-mm.a.hp/mm.a.maxHp).toFixed(2)}/${(1-mm.b.hp/mm.b.maxHp).toFixed(2)}` : '';
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  /* Deep probe: force the raster with a 1px readback so a section's cost is
     its own, not whatever the queue flushes later. Distorts the absolute
     number upward; use it for ranking, not for fps. */
  const SECTIONS = ["drawHud","drawArena","drawMotes","drawUltUnder","drawFx",
                    "drawFighter","drawUltOver","drawRings","drawFloats",
                    "drawArenaFrame","drawClock","drawBanner","drawFooter"];
  function deepProbe(frames){
    const cv = document.getElementById('cv'), cx = cv.getContext('2d');
    const flush = () => cx.getImageData(cv.width-1, cv.height-1, 1, 1).data[3];
    const r = AC.renderer, acc = {}, orig = {};
    for (const n of SECTIONS){
      if (typeof r[n] !== 'function') continue;
      orig[n] = r[n]; acc[n] = 0;
      r[n] = function(){ const t0=performance.now(); const o=orig[n].apply(this,arguments);
                         flush(); acc[n]+=performance.now()-t0; return o; };
    }
    const m = AC.match, whole = [];
    for (let i=0;i<4;i++){ AC.__draw(m); flush(); }
    for (const k in acc) acc[k] = 0;
    for (let i=0;i<frames;i++){
      const t0=performance.now(); AC.__draw(m); flush(); whole.push(performance.now()-t0);
    }
    for (const n in orig) r[n] = orig[n];
    const per = {}; for (const k in acc) if (acc[k]/frames > 0.02) per[k] = acc[k]/frames;
    return { whole: med(whole), per };
  }

  /* A/B WITHOUT ANY READBACK.

     The first version A/B'd with a getImageData flush after every draw. That
     is the single most reliable way to make Chrome demote an accelerated 2D
     canvas to software — which means the ranking it produced may have been the
     ranking of a canvas the readbacks themselves broke. Rick's report showed a
     3070 spending 9.6 ms on two full-canvas gradient fills, which a 3070 does
     not do; that is a software-raster number.

     So: draw the same frozen frame N times inside ONE rAF callback and read the
     rAF delta. All the raster work happens, nothing is read back, and the
     per-draw cost is the delta over N. Costs below the refresh interval become
     visible because N of them are not. */
  function liveProbe(reps, frames){
    return new Promise(resolve => {
      const m = AC.match, ts = []; let warm = 6, prev = performance.now();
      function step(now){
        const d = now - prev; prev = now;
        if (warm > 0) warm--; else ts.push(d / reps);
        if (ts.length >= frames) return resolve(med(ts));
        for (let i = 0; i < reps; i++) AC.__draw(m);
        requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  function frozenLateFrame(){
    AC.SFX.on = false;
    /* PIN THE SEED. `newMatch` draws a fresh random one, so every run of this
       harness timed a DIFFERENT FIGHT -- different cracks, statuses, desperate
       ring, ult charge, all of which cost real milliseconds. Build-to-build
       comparisons were therefore carrying an unknown amount of fight-to-fight
       variation, and this project had already written that exact bug into its
       do-not list one day earlier after a pixel-diff compared two different
       matches. Same seed, every build, every run. */
    { /* Seed the source newMatch actually draws from, so this works on EVERY
         build: the shipped `newMatch(idA,idB)` rolls Math.random, while the
         cinema patch's takes a seedIn. Passing a third argument would pin one
         and silently not the other, which is worse than not pinning at all. */
      const _mr = Math.random; let _s = 20403356 >>> 0;   /* CHOSEN, not arbitrary: the first pinned seed
         produced a fight in which fighter A never fell below 50% HP, so the
         `damage > 0.5` band reported `—` for everyone, permanently. This one
         populates all four bands (855 / 1848 / 297 / 530 samples) over a full
         50s match. Verified in-container against 40 candidates. */
      Math.random = () => { _s = (Math.imul(_s, 1103515245) + 12345) >>> 0;
                            return _s / 4294967296; };
      try { AC.newMatch('grudgebearer','spellbreaker'); } finally { Math.random = _mr; }
    }
    const m = AC.match; m.introT = 0;
    const dt = AC.CONFIG.physics.dt;
    while (m.t < 26) m.step(dt);
    m.shake = 0;
    window.__frozen = true;
    return m;
  }

  async function bench(){
    benching = true;
    const out = $('pfOut'); out.style.display = 'block';
    out.value = 'running…';
    const L = [];
    const gl = (() => { try {
      const g = document.createElement('canvas').getContext('webgl');
      const d = g && g.getExtension('WEBGL_debug_renderer_info');
      return d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'unknown';
    } catch(e){ return 'unknown'; } })();
    const cv = document.getElementById('cv');
    L.push('SUNDERED CROWN PERF REPORT v2 (no readbacks)');
    L.push('gpu     ' + gl);
    L.push('dpr     ' + devicePixelRatio + '   window ' + innerWidth + 'x' + innerHeight);
    L.push('canvas  ' + cv.width + 'x' + cv.height + '  k=' + AC.renderer.k.toFixed(3)
           + '  (' + (100*cv.width*cv.height/(1080*1920)).toFixed(0) + '% of 1080x1920)');
    L.push('');

    for (const k in window.__PERF.off) window.__PERF.off[k] = 0;
    for (const el of box.querySelectorAll('input[data-k]')) el.checked = false;

    /* ---- phase pass: real rAF deltas over a real match ---- */
    window.__frozen = false;
    AC.SFX.on = false;
    /* PIN THE SEED. `newMatch` draws a fresh random one, so every run of this
       harness timed a DIFFERENT FIGHT -- different cracks, statuses, desperate
       ring, ult charge, all of which cost real milliseconds. Build-to-build
       comparisons were therefore carrying an unknown amount of fight-to-fight
       variation, and this project had already written that exact bug into its
       do-not list one day earlier after a pixel-diff compared two different
       matches. Same seed, every build, every run. */
    { /* Seed the source newMatch actually draws from, so this works on EVERY
         build: the shipped `newMatch(idA,idB)` rolls Math.random, while the
         cinema patch's takes a seedIn. Passing a third argument would pin one
         and silently not the other, which is worse than not pinning at all. */
      const _mr = Math.random; let _s = 20403356 >>> 0;   /* CHOSEN, not arbitrary: the first pinned seed
         produced a fight in which fighter A never fell below 50% HP, so the
         `damage > 0.5` band reported `—` for everyone, permanently. This one
         populates all four bands (855 / 1848 / 297 / 530 samples) over a full
         50s match. Verified in-container against 40 candidates. */
      Math.random = () => { _s = (Math.imul(_s, 1103515245) + 12345) >>> 0;
                            return _s / 4294967296; };
      try { AC.newMatch('grudgebearer','spellbreaker'); } finally { Math.random = _mr; }
    }
    AC.match.introT = 0;
    const rows = [];
    let prev = performance.now();
    await new Promise(done => {
      function step(now){
        const d = now - prev; prev = now;
        const m = AC.match;
        if (d > 0 && d < 500 && m) rows.push([m.t, d, m.inset, m.ultFx ? m.ultFx.w : '',
                                              1 - m.a.hp/m.a.maxHp]);
        if (m && !m.over && m.t < 50) return requestAnimationFrame(step);
        done();
      }
      requestAnimationFrame(step);
    });
    const band = (name, sel) => {
      const v = rows.filter(sel).map(r => r[1]);
      if (v.length < 8) { L.push('  ' + name.padEnd(26) + ' —'); return; }
      L.push('  ' + name.padEnd(26) + ' n=' + String(v.length).padEnd(5)
        + ' med ' + med(v).toFixed(1).padStart(6) + ' ms  p95 ' + pct(v,0.95).toFixed(1).padStart(6)
        + '  worst ' + Math.max.apply(null, v).toFixed(0).padStart(5));
    };
    L.push('LIVE FRAME TIME (rAF deltas, 1x speed, sound off)');
    band('pre-collapse, no ult', r => r[2] === 0 && !r[3]);
    band('collapsing, no ult',   r => r[2] > 0 && !r[3]);
    band('ultimate on screen',   r => !!r[3]);
    band('damage > 0.5',         r => r[4] > 0.5);
    L.push('  (a median at the display refresh interval means it is keeping up;');
    L.push('   above it means frames are being missed)');
    L.push('');

    /* ---- resolution: the #1 fix, measured on this machine ---- */
    frozenLateFrame();
    const fitted = cv.width;
    const atFitted = await liveProbe(8, 26);
    AC.setResolution(1080, 1920);
    const atFull = await liveProbe(8, 26);
    L.push('BACKING STORE (same frame, no readback)');
    L.push('  1080x1920 (2.07 Mpx)   ' + atFull.toFixed(2).padStart(7) + ' ms/draw');
    L.push('  ' + (fitted + 'x' + Math.round(fitted*16/9) + ' fitted').padEnd(22)
           + atFitted.toFixed(2).padStart(7) + ' ms/draw   '
           + (atFull/Math.max(0.001, atFitted)).toFixed(2) + 'x faster');
    L.push('');

    /* ---- feature A/B at full resolution, where the costs are largest ---- */
    /* PAIRED BASELINES. v1 measured `base` once and compared twelve features
       against it over several minutes. On a phone the device heats during the
       run, so each successive feature is measured under worse conditions and
       its delta is corrupted by drift rather than by the feature. Measured
       2026-08-13 on an Adreno 660: the last three features in the list came
       back at +3.16, +12.54 and +13.61 ms -- turning a feature OFF made the
       frame SLOWER, three times in a row, in list order.

       Two runs of the SAME build differed 68.71 vs 48.91 ms on base. What did
       NOT move across those runs: the live frame time (25.0 / 33.3 both times)
       and the shadow SHARE (83% both times). Ratios survive a thermal state
       that absolutes do not.

       So: sandwich every feature between two fresh baselines, report the drift
       between them, and take the delta against their mean. Drift becomes
       visible instead of silently landing in the answer. */
    L.push('FEATURE A/B (frozen frame, 1080x1920, PAIRED baselines)');
    const FEAT = window.__QUICK ? ['shadows']
      : ['shadows','grain','cracks','wash','vignette','sigil',
         'wallglow','ult','motes','fx','status','tags'];
    for (const k of FEAT){
      const b0 = await liveProbe(8, window.__QUICK ? 20 : 14);
      window.__PERF.off[k] = 1;
      const v  = await liveProbe(8, window.__QUICK ? 20 : 14);
      window.__PERF.off[k] = 0;
      const b1 = await liveProbe(8, window.__QUICK ? 20 : 14);
      const bb = (b0 + b1) / 2;
      L.push('  base  ' + b0.toFixed(2).padStart(7) + ' -> ' + b1.toFixed(2).padStart(7)
             + '   drift ' + (b1-b0>=0?'+':'') + (b1-b0).toFixed(2) + ' ms'
             + (Math.abs(b1-b0) > 0.15*bb ? '   <-- DRIFTING, distrust this row' : ''));
      L.push('  ' + ('no ' + k).padEnd(14) + v.toFixed(2).padStart(8) + ' ms   '
             + (v-bb >= 0 ? '+' : '') + (v-bb).toFixed(2)
             + '   (' + (100*(bb-v)/bb).toFixed(0) + '% of the frame)');
    }

    window.__frozen = false;
    /* PIN THE SEED. `newMatch` draws a fresh random one, so every run of this
       harness timed a DIFFERENT FIGHT -- different cracks, statuses, desperate
       ring, ult charge, all of which cost real milliseconds. Build-to-build
       comparisons were therefore carrying an unknown amount of fight-to-fight
       variation, and this project had already written that exact bug into its
       do-not list one day earlier after a pixel-diff compared two different
       matches. Same seed, every build, every run. */
    { /* Seed the source newMatch actually draws from, so this works on EVERY
         build: the shipped `newMatch(idA,idB)` rolls Math.random, while the
         cinema patch's takes a seedIn. Passing a third argument would pin one
         and silently not the other, which is worse than not pinning at all. */
      const _mr = Math.random; let _s = 20403356 >>> 0;   /* CHOSEN, not arbitrary: the first pinned seed
         produced a fight in which fighter A never fell below 50% HP, so the
         `damage > 0.5` band reported `—` for everyone, permanently. This one
         populates all four bands (855 / 1848 / 297 / 530 samples) over a full
         50s match. Verified in-container against 40 candidates. */
      Math.random = () => { _s = (Math.imul(_s, 1103515245) + 12345) >>> 0;
                            return _s / 4294967296; };
      try { AC.newMatch('grudgebearer','spellbreaker'); } finally { Math.random = _mr; }
    }
    benching = false;
    out.value = L.join('\n');
  }

  $('pfBench').onclick = () => { window.__QUICK = false; bench(); };
  $('pfQuick').onclick  = () => { window.__QUICK = true;  bench(); };
  $('pfCopy').onclick = () => {
    const t = $('pfOut'); t.style.display='block'; t.select();
    document.execCommand('copy');
  };
})();
</script>
"""

s = rep(s, "</body>", LAB + "</body>", "lab", expect=1)
OUT.write_text(s, encoding="utf-8", newline="\n")
print(f"wrote {OUT}  ({len(s)//1024} KB, {n_sb} shadow sites hooked)")

# --- IT HAS TO LOAD -----------------------------------------------------------
# This builder rewrites source with a regex, which is a sharper instrument than
# the anchor patchers everywhere else in the toolchain: an anchor that misses
# fails loudly, a regex that over-matches produces a file that looks fine and is
# broken. It did exactly that once, and the artifact reached Rick because
# nothing in this file had ever opened its own output.
#
# So: load the page, and assert the game is actually alive in it. Cheap
# (~2s), and it is the same end-to-end shape verify.py's canvas check uses --
# assert the thing you care about, not a proxy for it.
try:
    from scpage import game as _smoke
except ImportError:                       # scpage not importable: say so, do not pass
    sys.exit("SMOKE SKIPPED: scpage.py not importable -- run this from the "
             "toolchain directory. Refusing to report a pass it did not run.")

with _smoke(game_path=OUT) as (_pg, _errs):
    _ok = _pg.evaluate("!!(window.AC && window.AC.WEAPONS && window.__PERF)")
if _errs:
    sys.exit("SMOKE FAIL: page errors in the lab it just wrote:\n  "
             + "\n  ".join(_errs))
if not _ok:
    sys.exit("SMOKE FAIL: window.AC / window.__PERF missing -- the lab loaded "
             "but the game did not start")
print("  smoke: page loads, no errors, AC and __PERF both live")
