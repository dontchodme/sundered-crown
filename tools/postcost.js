/* WHAT THE POST CHAIN COSTS PER FRAME. Driven by tools/post_cost.py.
 *
 * The house rules for this measurement are hud_cost.py's and they are not
 * optional, because getting them wrong turns the instrument into the result:
 *
 *   - N draws inside ONE rAF, not one draw per rAF. Per-frame rAF measures the
 *     display's cadence, not the work.
 *   - Force the raster ONCE, at the end. A getImageData (or a readPixels)
 *     every iteration can demote an accelerated canvas to software, and then
 *     the number is of a different renderer than the one that ships.
 *   - m.shake = 0. The camera offset calls Math.random(), so leaving it on
 *     makes every iteration draw a slightly different frame.
 *
 * And the rule this file adds: REPORT THE RENDERER. A number off SwiftShader
 * is not Rick's machine and is not a phone. What transfers between runtimes is
 * the RATIO between rows measured back to back in one session, which is the
 * only question the chain has to answer -- did it make the frame materially
 * more expensive than the 2D draw already was?
 */
(cfg) => {
  AC.setResolution(cfg.w, cfg.h);
  const m = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
  m.introT = 0;
  AC.__inject(m);
  AC.SFX.play = function () {};
  AC.SFX.resume = function () {};
  const dt = AC.CONFIG.physics.dt;
  while (m.t < cfg.at) m.step(dt);
  m.shake = 0;

  const cv = document.getElementById('cv');
  const ctx = cv.getContext('2d');
  const one = new Uint8Array(4);

  const R = AC.renderer;
  const state = () => ({
    enabled: true, dt: 1 / 60,
    rect: { x: R.pad * R.k, y: R.arenaTop * R.k, w: R.aw * R.k, h: R.ah * R.k },
    cine: AC.CINE ? { on: !!AC.CINE.on, cut: !!AC.CINE.cut } : null,
  });

  const gl = (typeof POSTFX !== 'undefined' && POSTFX.gl)
    ? POSTFX.gl.getContext('webgl2') : null;
  const dbg = gl && gl.getExtension('WEBGL_debug_renderer_info');
  const renderer = !gl ? 'no webgl'
    : (dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)
           : gl.getParameter(gl.RENDERER));

  /* MEASURES THE BUILD'S OWN CHAIN, not a copy of it. postcost used to
     create its own Post instance and time AC.__draw plus post.render -- which
     was right while the chain lived only in the app, and became wrong the
     moment post_build.py put it in the build: AC.__draw now composites by
     itself, so that arrangement was timing the work TWICE.

     POSTFX.on is the honest switch. Off is the shipping renderer with the
     chain off; on is everything, three draws and all. */
  /* BARE NAME, NOT window.POSTFX. POSTFX is a top-level const in the build,
     which makes it a lexical global and NOT a property of window -- the same
     trap CINE and `renderer` set, now for the third time today. It resolves
     by name here because this runs in the game's own realm. */
  const FX = (typeof POSTFX !== 'undefined') ? POSTFX : null;
  if (!FX) return { err: 'this build has no POSTFX -- run post_build.py' };
  FX.init();

  const CONFIGS = [
    { name: '2D draw only', on: false },
    { name: '+ chain, no effects', on: true },
    { name: '+ bloom ' + SWBPost.SPREAD.DEFAULT, on: true,
      bloom: SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT] },
    { name: '+ trails ' + SWBPost.TRAILS.DEFAULT, on: true,
      trails: SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT] },
    { name: '+ grade ' + SWBPost.GRADE.DEFAULT, on: true,
      grade: SWBPost.GRADE[SWBPost.GRADE.DEFAULT] },
    { name: '+ ALL (as chosen)', on: true,
      bloom: SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
      trails: SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT],
      grade: SWBPost.GRADE[SWBPost.GRADE.DEFAULT] },
  ];

  const measure = (c) => new Promise((res) => {
    FX.post.setBloom(c.bloom || null);
    FX.post.setTrails(c.trails || null);
    FX.post.setGrade(c.grade || null);
    FX.on = c.on;
    FX.reset();
    for (let i = 0; i < cfg.warm; i++) AC.__draw(m);
    requestAnimationFrame(() => {
      const t0 = performance.now();
      for (let i = 0; i < cfg.n; i++) AC.__draw(m);
      /* One sync at the end, never per iteration -- a readback every frame can
         demote an accelerated canvas to software and time a different
         renderer than the one that ships. */
      if (c.on) gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, one);
      else ctx.getImageData(0, 0, 1, 1);
      res((performance.now() - t0) / cfg.n);
    });
  });

  return (async () => {
    const rows = [];
    for (let rep = 0; rep < cfg.reps; rep++) {
      for (let i = 0; i < CONFIGS.length; i++) {
        const ms = await measure(CONFIGS[i]);
        rows.push({ name: CONFIGS[i].name, rep: rep, ms: ms });
      }
    }
    FX.post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
    FX.post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
    FX.post.setGrade(SWBPost.GRADE[SWBPost.GRADE.DEFAULT]);
    FX.on = true;
    return { renderer: renderer, size: cv.width + 'x' + cv.height,
             at: +m.t.toFixed(2), rows: rows };
  })();
}
