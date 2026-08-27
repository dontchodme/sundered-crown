/* THE SHEET. Driven by tools/post_spread.py; nothing to run here by hand.
 *
 * THIS RUNS THE LOOP THE MP4 RUNS, and for several sheets it did not.
 * cinema_clip.py resets CINE, plans the cuts with cinePlan, and then drives
 * every frame through CINE.pump and CINE.drawLerped -- the same body the live
 * page uses. Stepping the sim by hand and calling AC.__draw skips all of it:
 * no cuts, no zoom, no bars, no wash, no time dilation, and no interpolated
 * draw. A sheet built that way photographs a picture the video will never
 * contain, which is exactly the divergence docs/ARCHITECTURE.md §1 exists to
 * prevent -- and it is worse than useless for judging an effect that is meant
 * to RAMP WITH THE CUT.
 *
 * `CINE` and `cinePlan` are reachable by bare name here because this runs in
 * the game's own realm, and a top-level const is visible to other classic
 * scripts in the same realm. Only ACROSS realms -- the app shell reaching
 * into the frame -- does it need the AC export.
 */
(cfg) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  const FPS = 60, raw = 1 / FPS;
  const cv = document.getElementById('cv');
  const R = AC.renderer;

  const ov = document.createElement('canvas');
  ov.style.display = 'none';
  document.body.appendChild(ov);
  const post = SWBPost.create(ov);

  /* The readout layer gets its own canvas: the renderer only ever draws to
     #cv, so one pass has to be copied off before the other overwrites it. */
  const ro = document.createElement('canvas');
  ro.width = cv.width; ro.height = cv.height;
  const roCtx = ro.getContext('2d');
  /* and the emissive pass, which is what the bloom actually reads */
  const em = document.createElement('canvas');
  em.width = cv.width; em.height = cv.height;
  const emCtx = em.getContext('2d');

  const state = () => ({
    enabled: true,
    dt: 1 / FPS,
    rect: { x: R.pad * R.k, y: R.arenaTop * R.k, w: R.aw * R.k, h: R.ah * R.k },
    cine: { on: !!CINE.on, cut: !!CINE.cut, wash: CINE.wash || 0,
            bars: CINE.bars || 0, zoom: CINE.zoom || 1,
            flash: CINE.flash || 0, streak: CINE.streak || 0,
            tier: CINE.cut ? (CINE.cut.fatal ? 'KILL' : 'T' + CINE.cut.tier) : null,
            fatal: CINE.cut ? !!CINE.cut.fatal : false },
  });

  const drawAt = (m, alpha) => {
    /* CAMERA SHAKE IS PINNED OFF FOR THE WHOLE SHEET, and it has to be. The
       offset is Math.random() per DRAW, and a post column draws twice per
       frame -- readouts, then the world -- where the control draws once. The
       columns would consume the random stream at different rates and shake by
       different amounts: a difference between tiles caused by the instrument
       rather than by the thing being compared. hud_cost.py pins it for the
       same reason. */
    m.shake = 0;
    if (alpha > 0) CINE.drawLerped(R, m, alpha); else AC.__draw(m);
  };

  const cols = cfg.cols;
  const TW = cfg.tile, TH = Math.round(TW * 1920 / 1080);
  const PAD = 14, HEAD = 96, ROWH = TH + 40;
  const W = PAD + cols.length * (TW + PAD);
  const H = HEAD + cfg.moments.length * ROWH + PAD;

  const sheet = document.createElement('canvas');
  sheet.width = W; sheet.height = H;
  const s = sheet.getContext('2d');
  s.fillStyle = '#0B0B10'; s.fillRect(0, 0, W, H);
  s.fillStyle = '#E8E4F0';
  s.font = '700 26px sans-serif';
  s.fillText(cfg.title, PAD, 34);
  s.fillStyle = '#8A8296';
  s.font = '400 15px monospace';
  s.fillText(cfg.sub, PAD, 58);
  s.fillText(cfg.runtime, PAD, 78);

  const report = [];
  const baseline = [];

  for (let c = 0; c < cols.length; c++) {
    const key = cols[c];
    let m = null, curPair = -1, frame = 0;

    if (key === 'off' && cfg.effect === 'adapt') {
      post.setBloom(Object.assign({}, SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
                                  { adapt: 0 }));
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
      post.setGrade(SWBPost.GRADE[SWBPost.GRADE.DEFAULT]);
    }
    else if (key === 'off' && cfg.effect === 'clamp') {
      post.setBloom(Object.assign({}, SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
                                  { clamp: 0 }));
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
      post.setGrade(SWBPost.GRADE[SWBPost.GRADE.DEFAULT]);
    }
    else if (key === 'off' && cfg.effect === 'grade') {
      /* The control keeps the chosen bloom and trails and turns off ONLY the
         grade, so the sheet asks one question. */
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
      post.setGrade(null);
    }
    else if (key === 'off' && cfg.effect === 'cut') {
      post.setBloom(Object.assign({}, SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
                                  { cutGain: 0 }));
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
    } else if (key === 'off' && cfg.effect === 'trails') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(null);
    } else if (key === 'off') {
      post.setBloom(null); post.setTrails(null);
    } else if (key === 'chosen') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
    } else if (cfg.effect === 'cut') {
      post.setBloom(Object.assign({}, SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
                                  { cutGain: SWBPost.CUTRAMP[key] }));
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
    } else if (cfg.effect === 'adapt') {
      post.setBloom(Object.assign({}, SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
                                  { adapt: SWBPost.ADAPT[key] }));
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
      post.setGrade(SWBPost.GRADE[SWBPost.GRADE.DEFAULT]);
    } else if (cfg.effect === 'clamp') {
      /* Only the clamp varies. Everything else is the chosen look, control
         included -- the control being clamp OFF, which is what shipped and
         what Rick called too loud. */
      post.setBloom(Object.assign({}, SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT],
                                  { clamp: SWBPost.CLAMP[key] }));
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
      post.setGrade(SWBPost.GRADE[SWBPost.GRADE.DEFAULT]);
    } else if (cfg.effect === 'grade') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(SWBPost.TRAILS[SWBPost.TRAILS.DEFAULT]);
      post.setGrade(SWBPost.GRADE[key]);
    } else if (cfg.effect === 'trails') {
      post.setBloom(SWBPost.SPREAD[SWBPost.SPREAD.DEFAULT]);
      post.setTrails(SWBPost.TRAILS[key]);
    } else {
      post.setTrails(null);
      post.setBloom(SWBPost.SPREAD[key]);
    }
    const chainOn = post.passes.length > 0;

    for (let r = 0; r < cfg.moments.length; r++) {
      const row = cfg.moments[r];
      if (row.pair !== curPair) {
        const P = cfg.pairs[row.pair];
        CINE.on = true; CINE.interp = true; CINE.reset(); CINE.acc = 0;
        CINE.plan = cinePlan(P.a, P.b, P.seed >>> 0).cuts;
        m = new AC.Match(P.a, P.b, P.seed >>> 0);
        m.introT = 0;
        AC.__inject(m);
        AC.SFX.play = function () {};
        AC.SFX.resume = function () {};
        curPair = row.pair;
        frame = 0;
      }

      /* Fast-forward WITHOUT drawing, then the warm frames with everything
         live -- a trail is history and needs real frames run into it. Frame
         indices, not seconds: with the director on, wall time and sim time
         are two different clocks and only one of them is the video's. */
      const target = row.frame;
      const warmFrom = Math.max(0, target - cfg.warm);
      let alpha = 0;
      while (frame < warmFrom) { CINE.pump(raw, m, 1); frame++; }
      post.resetHistory();
      let drawn = cv;
      while (frame < target) {
        alpha = CINE.pump(raw, m, 1);
        frame++;
        if (chainOn) {
          R.roMode = 2; drawAt(m, alpha);
          roCtx.clearRect(0, 0, ro.width, ro.height);
          roCtx.drawImage(cv, 0, 0);
          R.roMode = 3; drawAt(m, alpha);
          emCtx.clearRect(0, 0, em.width, em.height);
          emCtx.drawImage(cv, 0, 0);
          R.roMode = 1; drawAt(m, alpha);
          const st = state();
          st.readouts = ro;
          st.emissive = em;
          post.render(cv, st);
          drawn = ov;
        } else {
          R.roMode = 0; drawAt(m, alpha);
          drawn = cv;
        }
      }
      R.roMode = 0;

      const x = PAD + c * (TW + PAD), y = HEAD + r * ROWH;
      s.drawImage(drawn, x, y, TW, TH);
      s.strokeStyle = key === 'off' ? '#C9A227' : '#2A2436';
      s.lineWidth = key === 'off' ? 2 : 1;
      s.strokeRect(x + 0.5, y + 0.5, TW - 1, TH - 1);

      if (key === 'off') {
        if (chainOn) baseline[r] = { px: post.readPixels(), gl: true };
        else baseline[r] = { px: cv.getContext('2d')
                               .getImageData(0, 0, cv.width, cv.height).data,
                             gl: false };
      }

      let changed = 0, meanAdd = 0;
      if (key !== 'off' && baseline[r]) {
        const px = post.readPixels(), base = baseline[r].px;
        const baseGl = baseline[r].gl;
        const w2 = cv.width, h2 = cv.height;
        let diff = 0, add = 0;
        for (let yy = 0; yy < h2; yy += 3) {
          const gy = h2 - 1 - yy;
          for (let xx = 0; xx < w2; xx += 3) {
            const i3 = (gy * w2 + xx) * 4;
            const j3 = (baseGl ? (gy * w2 + xx) : (yy * w2 + xx)) * 4;
            const dd = Math.abs(px[i3] - base[j3])
                     + Math.abs(px[i3 + 1] - base[j3 + 1])
                     + Math.abs(px[i3 + 2] - base[j3 + 2]);
            if (dd) { diff++; add += dd; }
          }
        }
        const n = Math.ceil(h2 / 3) * Math.ceil(w2 / 3);
        changed = +(100 * diff / n).toFixed(1);
        meanAdd = +(add / n).toFixed(2);
      }

      const st = state();
      const P = cfg.pairs[row.pair];
      s.fillStyle = key === 'off' ? '#C9A227' : '#E8E4F0';
      s.font = '700 15px sans-serif';
      s.fillText(key === 'off'
                 ? (cfg.effect === 'trails' ? 'TRAILS OFF  (control, bloom on)'
                  : cfg.effect === 'grade' ? 'GRADE OFF  (control, chain on)'
                  : cfg.effect === 'adapt' ? 'NO ADAPT  (control, as shipped)'
                  : cfg.effect === 'cut' ? 'RAMP OFF  (control, flat intensity)'
                  : 'OFF  (control, the untouched 2D canvas)')
                 : (key === 'chosen' ? 'AS CHOSEN' : key.toUpperCase()),
                 x, y + TH + 18);
      s.fillStyle = '#8A8296';
      s.font = '400 12px monospace';
      const tag = st.cine.tier ? '  ' + st.cine.tier + ' CUT' : '';
      if (key === 'off') {
        /* SHORT ON PURPOSE. The pairing and the seed are in the header; a
           caption long enough to run under the next column's makes the sheet
           harder to read than no caption at all. */
        s.fillText('frame ' + target + '  ' + (target / FPS).toFixed(2) + 's'
                   + tag, x, y + TH + 34);
      } else if (cfg.effect === 'cut') {
        s.fillText('cutGain ' + SWBPost.CUTRAMP[key] + '   wash '
                   + st.cine.wash.toFixed(3) + '   ' + changed + '% px  +'
                   + meanAdd, x, y + TH + 34);
      } else if (cfg.effect === 'adapt') {
        s.fillText('adapt ' + (SWBPost.ADAPT[key] || 'off') + '   ' + changed
                   + '% px  ' + meanAdd, x, y + TH + 34);
      } else if (cfg.effect === 'clamp') {
        s.fillText('clamp ' + (SWBPost.CLAMP[key] || 'off') + '   ' + changed
                   + '% px  +' + meanAdd, x, y + TH + 34);
      } else if (cfg.effect === 'grade') {
        const o = SWBPost.GRADE[key];
        s.fillText('vig ' + o.vignette + '  grain ' + o.grain + '  con '
                   + o.contrast + '   ' + changed + '% px', x, y + TH + 34);
      } else if (cfg.effect === 'chosen') {
        s.fillText('bloom ' + SWBPost.SPREAD.DEFAULT + ' + trails '
                   + SWBPost.TRAILS.DEFAULT + '   ' + changed + '% px  +'
                   + meanAdd, x, y + TH + 34);
      } else if (cfg.effect === 'trails') {
        s.fillText(SWBPost.TRAILS[key].seconds + 's tail   ' + changed
                   + '% px  +' + meanAdd, x, y + TH + 34);
      } else {
        const o = SWBPost.SPREAD[key];
        s.fillText('thr ' + o.threshold + '  int ' + o.intensity + '   '
                   + changed + '% px  +' + meanAdd, x, y + TH + 34);
      }
      if (key !== 'off') {
        report.push({ frame: target, variant: key, pctChanged: changed,
                      meanAdd: meanAdd, wash: +st.cine.wash.toFixed(3),
                      tier: st.cine.tier });
      }
    }
  }
  post.setBloom(null);
  post.setTrails(null);
  post.setGrade(null);
  return { png: sheet.toDataURL('image/png').slice(22), w: W, h: H,
           report: report,
           renderer: (() => {
             const g2 = ov.getContext('webgl2');
             const d = g2.getExtension('WEBGL_debug_renderer_info');
             return d ? g2.getParameter(d.UNMASKED_RENDERER_WEBGL)
                      : g2.getParameter(g2.RENDERER);
           })() };
}
