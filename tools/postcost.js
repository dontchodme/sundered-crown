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
  const ov = document.createElement('canvas');
  ov.style.display = 'none';
  document.body.appendChild(ov);
  const post = SWBPost.create(ov);
  const gl = ov.getContext('webgl2');
  const one = new Uint8Array(4);

  const R = AC.renderer;
  const state = () => ({
    enabled: true, dt: 1 / 60,
    rect: { x: R.pad * R.k, y: R.arenaTop * R.k, w: R.aw * R.k, h: R.ah * R.k },
    cine: AC.CINE ? { on: !!AC.CINE.on, cut: !!AC.CINE.cut } : null,
  });

  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  const renderer = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)
                       : gl.getParameter(gl.RENDERER);

  /* Each configuration is a name and a setup. `chain: false` means the post
     module is not called at all -- the honest baseline, because that is what
     ships today. */
  const CONFIGS = [
    { name: '2D draw only', chain: false, bloom: null, trails: null },
    { name: '+ chain, no effects', chain: true, bloom: null, trails: null },
    { name: '+ bloom ' + SWBPost.SPREAD.DEFAULT, chain: true,
      bloom: SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT], trails: null },
    { name: '+ trails ' + SWBPost.TRAILS.DEFAULT, chain: true, bloom: null,
      trails: SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT] },
    { name: '+ both (as chosen)', chain: true,
      bloom: SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
      trails: SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT] },
  ];

  const measure = (c) => new Promise((res) => {
    post.setBloom(c.bloom);
    post.setTrails(c.trails);
    post.resetHistory();
    for (let i = 0; i < cfg.warm; i++) {
      AC.__draw(m);
      if (c.chain) post.render(cv, state());
    }
    requestAnimationFrame(() => {
      const t0 = performance.now();
      for (let i = 0; i < cfg.n; i++) {
        AC.__draw(m);
        if (c.chain) post.render(cv, state());
      }
      /* One sync at the end. readPixels for the GL path, getImageData for the
         2D-only row -- both block until the work they are waiting on is
         actually done, which is the whole point. */
      if (c.chain) gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, one);
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
    post.setBloom(null);
    post.setTrails(null);
    return { renderer: renderer, size: cv.width + 'x' + cv.height,
             at: +m.t.toFixed(2), rows: rows };
  })();
}
