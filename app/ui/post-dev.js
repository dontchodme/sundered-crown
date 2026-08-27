/* THE POST CHAIN, IN THE APP, WITH THE A/B TOGGLE.
 *
 * `docs/RENDERER-BRIEF.md` §5 and §8.2. This file is the ITERATION harness —
 * it loads src/render/post.js into the running app so the look can be worked
 * on where a person can see it. The chain itself lives in that module and not
 * here, because the same module has to go into the build later via
 * tools/post_build.py; anything that ends up only in this file is a divergence
 * between the app and the mp4 waiting to happen.
 *
 * HOW IT GETS ITS PIXELS WITHOUT TOUCHING THE ENGINE
 *
 * The game keeps rendering to its own #cv exactly as it does today. An overlay
 * canvas is stacked on top of it in the shell document, and each frame the
 * game's canvas is uploaded as a texture and the composited result drawn into
 * the overlay. Nothing is injected into the engine, no draw call is
 * intercepted, and turning the overlay off leaves the original canvas visible
 * underneath — untouched, because it was never written to.
 *
 * That is deliberate and it is the A/B toggle's whole value: OFF is not a
 * neutral pass through the new code, it is the old code with the new code not
 * running. `docs/RENDERER-BRIEF.md` §7 gate 4 — the control has to stay
 * available or later comparisons have nothing to compare to.
 *
 * The one thing this arrangement is NOT is the shipping path. In the build the
 * chain will run inside the engine's own frame, before the canvas reaches the
 * screen. Here it runs one upload later. For iterating on a look that is the
 * same picture; for measuring frame cost it is not, and §7 gate 3 wants
 * tools/hud_cost.py rather than the number in this panel.
 */
'use strict';

const POST = {
  on: false,
  post: null,
  overlay: null,
  ro: null,           // the readout layer, drawn separately
  roCtx: null,
  src: null,          // the game's #cv
  raf: 0,
  err: null,
  lastT: 0,
  /* CPU-side wall clock around render(), smoothed. Honest about what it is:
     it does not see GPU time, and it is one upload more than the build will
     pay. A number to notice a regression by, not a number to quote. */
  ms: 0,
  frames: 0,
};

function postBoot(gameWindow) {
  POST.src = gameWindow.document.getElementById('cv');
  if (!POST.src) { postFail('the game has no #cv canvas'); return; }
  if (!window.SWBPost) { postFail('src/render/post.js did not load'); return; }
  if (!window.SWBPost.supported()) { postFail('no WebGL2 on this machine'); return; }

  /* The readout layer's own canvas. See postFrame: the engine only ever
     draws to #cv, so the two passes cannot share it. */
  POST.ro = document.createElement('canvas');
  POST.roCtx = POST.ro.getContext('2d');

  const ov = document.createElement('canvas');
  ov.id = 'postOverlay';
  ov.style.cssText = 'position:fixed; pointer-events:none; display:none; z-index:5;';
  document.body.appendChild(ov);
  POST.overlay = ov;

  try {
    POST.post = window.SWBPost.create(ov);
  } catch (e) {
    postFail(String(e.message || e));
    return;
  }

  postStatus('ready · ' + POST.post.version + ' · 0 effect passes');
}

function postFail(why) {
  POST.err = why;
  const b = document.getElementById('btnPost');
  if (b) b.disabled = true;
  postStatus('unavailable — ' + why);
}

function postStatus(s) {
  const el = document.getElementById('postOut');
  if (el) el.textContent = s;
}

/* The overlay has to sit exactly on the game canvas and carry exactly its
   backing-store size. Both matter and for different reasons: the CSS rect is
   what makes it line up on screen, and width/height being equal to the
   SOURCE's backing store is what keeps sampling 1:1 — the moment it is not,
   passthrough resamples and selfTest goes red for a reason that is nothing to
   do with the shader. */
function postSync() {
  const src = POST.src, ov = POST.overlay;
  if (!src || !ov) return;
  const f = document.getElementById('game').getBoundingClientRect();
  const r = src.getBoundingClientRect();
  ov.style.left = (f.left + r.left) + 'px';
  ov.style.top = (f.top + r.top) + 'px';
  ov.style.width = r.width + 'px';
  ov.style.height = r.height + 'px';
}

function postFrame() {
  POST.raf = requestAnimationFrame(postFrame);
  if (!POST.on || !POST.post) return;
  postSync();
  const t0 = performance.now();
  /* REAL SECONDS BETWEEN COMPOSITED FRAMES, and the trail decays against
     this rather than against a frame count. The app runs at whatever rAF
     gives it and cinema_clip captures at a fixed 60 — a per-frame decay
     would make the same seed smear differently on screen and in the mp4,
     which is the divergence Electron was chosen to prevent. */
  const dt = POST.lastT ? Math.min(0.25, (t0 - POST.lastT) / 1000) : 1 / 60;
  POST.lastT = t0;
  try {
    const st = postState();
    st.dt = dt;
    st.readouts = postReadouts();
    POST.post.render(POST.src, st);
  } catch (e) {
    postToggle(false);
    postFail(String(e.message || e));
    return;
  }
  const cost = performance.now() - t0;
  POST.ms = POST.ms ? POST.ms * 0.9 + cost * 0.1 : cost;
  if ((++POST.frames & 31) === 0) {
    const sel = document.getElementById('bloom');
    const tr = document.getElementById('trails');
    const gr2 = document.getElementById('grade');
    postStatus('ON · bloom ' + (sel ? sel.value : '?')
               + ' · trails ' + (tr ? tr.value : '?')
               + ' · grade ' + (gr2 ? gr2.value : '?') + ' · '
               + POST.post.passes.length + ' passes · '
               + POST.ms.toFixed(2) + ' ms/frame CPU-side');
  }
}

/* THE READOUT PASS.
 *
 * The engine's own rAF loop has already drawn this frame. It drew it at
 * roMode 1 -- the world WITHOUT the damage floats, status tags and ult-name
 * callout -- because postToggle set that when the chain came on. So #cv holds
 * the bloom's source, and this draws the missing three into a canvas of their
 * own for the compositor to put back on top afterwards.
 *
 * It costs one extra draw per frame, and it is a cheap one: three text layers,
 * no arena, no fighters, no ult art. tools/post_cost.py is where that gets
 * priced rather than assumed.
 *
 * The mode is restored to 1 before returning, because the engine's next frame
 * is drawn by the engine and has to come out as the world again.
 */
function postReadouts() {
  const w = document.getElementById('game').contentWindow;
  const AC = w.AC;
  if (!AC || !AC.renderer || !AC.match) return null;
  const src = POST.src, ro = POST.ro;
  if (ro.width !== src.width || ro.height !== src.height) {
    ro.width = src.width; ro.height = src.height;
  }
  AC.renderer.roMode = 2;
  AC.__draw(AC.match);
  POST.roCtx.clearRect(0, 0, ro.width, ro.height);
  POST.roCtx.drawImage(src, 0, 0);
  AC.renderer.roMode = 1;
  AC.__draw(AC.match);          // put the world back on #cv for the upload
  return ro;
}

/* The state the chain is handed. Everything here is READ from the running
   engine and nothing is written back — the renderer is not the sim, but the
   director is not this file's to move either.
 *
 * `rect` is the arena in SOURCE pixels. docs/RENDER-LAYERS.md §1: every
 * emissive layer in the frame is inside it and the HUD sits above it, so a
 * pass restricted to this rect leaves the readout alone by geometry. The
 * numbers come off the live renderer rather than the constants, because the
 * scrunch moves three of the four every frame it runs. */
function postState() {
  const w = document.getElementById('game').contentWindow;
  /* THROUGH `AC`, NOT OFF THE WINDOW. The engine is one classic script and
     `renderer`, `CINE` and `match` are top-level `const` — which makes them
     lexical globals, NOT properties of `window`. `w.renderer` is undefined
     even while `renderer` is perfectly alive, and the failure reads as "the
     engine did not boot". The export surface at the bottom of the build is
     the only reliable way in.
     `CINE` IS NOT ON IT. See docs/RENDER-LAYERS.md and brief §6: ramping the
     chain with the director's own tier needs it exported, which is a change
     to the build and therefore a builder change, not an app change. Until
     then this is null and nothing may quietly start guessing at it. */
  const AC = w.AC || {};
  const r = AC.renderer;
  const C = AC.CINE;
  const k = r ? r.k : 1;
  return {
    enabled: true,
    rect: r ? { x: r.pad * k, y: r.arenaTop * k, w: r.aw * k, h: r.ah * k }
            : null,
    cine: C ? { on: !!C.on, cut: !!C.cut, tier: C.tier || null, zoom: C.zoom || 1,
                wash: C.wash || 0, bars: C.bars || 0, flash: C.flash || 0,
                streak: C.streak || 0, fx: C.fx || 0, fy: C.fy || 0 }
            : null,
  };
}

function postToggle(want) {
  POST.on = (want === undefined) ? !POST.on : !!want;
  const b = document.getElementById('btnPost');
  if (b) {
    b.classList.toggle('pri', POST.on);
    b.textContent = POST.on ? 'Post chain: ON' : 'Post chain: OFF';
  }
  POST.overlay.style.display = POST.on ? 'block' : 'none';
  /* THE ENGINE DRAWS THE WORLD WHILE THE CHAIN IS ON, and the whole frame
     while it is off. Off has to be the untouched picture or the A/B toggle is
     comparing two new things instead of one new thing against the old one. */
  const gw = document.getElementById('game').contentWindow;
  if (gw && gw.AC && gw.AC.renderer) gw.AC.renderer.roMode = POST.on ? 1 : 0;
  if (POST.on) {
    postSync();
    if (!POST.raf) POST.raf = requestAnimationFrame(postFrame);
  } else {
    postStatus('OFF — the control. These are the untouched 2D pixels.');
  }
}

/* THE CHECK. With no effect passes the chain must be invisible: same bytes
   out as in. If this is not zero, the plumbing is bending the picture before
   anything has asked it to, and every side-by-side filmstrip after it is
   comparing two unknowns instead of one change. */
function postSelfTest() {
  if (!POST.post) return;
  const btn = document.getElementById('btnPostTest');
  btn.disabled = true;
  postStatus('checking every pixel…');
  /* Next frame, so the game has finished drawing the one being measured. */
  requestAnimationFrame(() => {
    let r;
    try {
      r = POST.post.selfTest(POST.src, postState());
    } catch (e) {
      postStatus('self-test threw — ' + (e.message || e));
      btn.disabled = false;
      return;
    }
    const head = r.differing === 0
      ? 'PASS  ' + r.total.toLocaleString() + ' px identical'
      : 'FAIL  ' + r.differing.toLocaleString() + ' of '
        + r.total.toLocaleString() + ' px differ, max delta ' + r.maxDelta;
    const tail = r.sample
      ? '\nfirst at ' + r.sample.x + ',' + r.sample.y
        + '  got ' + r.sample.got.join(',') + '  want ' + r.sample.want.join(',')
      : '';
    const note = r.passes > 0
      ? '\n(' + r.passes + ' effect passes are ON — a difference is expected;'
        + ' turn them off to check the plumbing)'
      : '';
    postStatus(head + tail + note);
    /* selfTest renders with enabled forced true, so the overlay now holds a
       frame even if the toggle is off. Put the picture back the way the
       toggle says it should be. */
    if (!POST.on) POST.overlay.style.display = 'none';
    btn.disabled = false;
  });
}

/* The spread lives in src/render/post.js as SWBPost.SPREAD, so this picker,
   tools/post_spread.py's filmstrip and whatever the builder eventually puts in
   the chain are all reading the SAME three settings. Three places holding
   three copies of "mid" is how Rick ends up approving one thing and shipping
   another. */
function postBloom(key) {
  if (!POST.post) return;
  const o = (key === 'off') ? null : (window.SWBPost.SPREAD[key] || null);
  POST.post.setBloom(o);
  POST.ms = 0;
  postStatus(POST.on
    ? 'ON · bloom ' + key + ' · measuring…'
    : 'OFF — the control. These are the untouched 2D pixels. (bloom ' + key + ')');
}

function postTrails(key) {
  if (!POST.post) return;
  POST.post.setTrails(key === 'off' ? null : (window.SWBPost.TRAILS[key] || null));
  POST.post.resetHistory();
  POST.ms = 0;
}

/* A trail is one fight's history. Carried across a restart, the first frame
   of the new fight arrives with the last one smeared over it. */
function postReset() {
  if (POST.post) POST.post.resetHistory();
  POST.lastT = 0;
}

function postGrade(key) {
  if (!POST.post) return;
  POST.post.setGrade(key === 'off' ? null : (window.SWBPost.GRADE[key] || null));
  POST.ms = 0;
}

function postWire() {
  const b = document.getElementById('btnPost');
  const t = document.getElementById('btnPostTest');
  const sel = document.getElementById('bloom');
  if (b) b.onclick = () => postToggle();
  if (t) t.onclick = postSelfTest;
  if (sel) {
    /* The default comes from the module, not from the markup, so the app and
       the filmstrip cannot disagree about which one Rick picked. */
    const def = (window.SWBPost && window.SWBPost.SPREAD.DEFAULT) || 'mid';
    if ([...sel.options].some((o) => o.value === def)) sel.value = def;
    sel.onchange = () => postBloom(sel.value);
    postBloom(sel.value);
  }
  const gr = document.getElementById('grade');
  if (gr) {
    const gdef = (window.SWBPost && window.SWBPost.GRADE.DEFAULT) || 'off';
    if ([...gr.options].some((o) => o.value === gdef)) gr.value = gdef;
    gr.onchange = () => postGrade(gr.value);
    postGrade(gr.value);
  }
  const tr = document.getElementById('trails');
  if (tr) {
    /* From the module, like bloom's, so the app and the filmstrip cannot
       disagree about which one was picked. */
    const tdef = (window.SWBPost && window.SWBPost.TRAILS.DEFAULT) || 'off';
    if ([...tr.options].some((o) => o.value === tdef)) tr.value = tdef;
    tr.onchange = () => postTrails(tr.value);
    postTrails(tr.value);
  }
  window.addEventListener('resize', postSync);
}
