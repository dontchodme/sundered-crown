/* Electron main process.
 *
 * PHASE 1 RULE: the game HTML is loaded UNCHANGED. Nothing in this file edits,
 * rewrites or injects into the engine. The shell is a host, not a fork.
 *
 * Why a custom protocol instead of loading file:// directly:
 * two file:// pages are opaque, mutually inaccessible origins, so the shell
 * could not reach into the game frame to drive it. Serving both from one
 * `swb://app` origin makes them same-origin without turning webSecurity off.
 * Disabling webSecurity would also work and would be the wrong habit to build.
 */
const { app, BrowserWindow, ipcMain, protocol, net, dialog, shell } = require('electron');
const path = require('node:path');
const fs = require('node:fs');
const url = require('node:url');

const REPO = path.resolve(__dirname, '..');

/* THE BUILD THE APP SHOWS. One place, so it cannot drift from what the video
 * pipeline renders. Keep it pointed at the build of record. */
const GAME = process.env.SWB_GAME || '02-chain/sc-paradox-frame.html';

/* `npm run identity` has advertised this flag since the shell was written and
 * nothing read it, so the script started the app normally and the gate could
 * only be run by a person clicking a button. A gate that needs a human to run
 * it does not get run: Phase 1's test had never been carried to a verdict
 * until 2026-08-26, and when it was, it failed. See docs/RUNTIME-DRIFT.md.
 *
 * With the flag the window is hidden, the same runIdentity() the button calls
 * is driven from here, and the process exits on the result. */
const IDENTITY = process.argv.includes('--identity-check');

/* Same idea for the post chain. NOT a general "run this JS" flag: the gates
 * are a fixed, named set, because a main process that will evaluate whatever
 * it is handed is a hole that gets used for something else six months later.
 * See docs/RENDERER-BRIEF.md §8.2. */
const POSTCHECK = process.argv.includes('--post-check');
const HEADLESS_GATE = IDENTITY || POSTCHECK;

/* THE POST-CHAIN GATE, run in the page by --post-check.
 *
 * It drives the harness in app/ui/post-dev.js, which the headless
 * tools/post_identity.py does NOT touch -- that one loads src/render/post.js
 * into the game page directly and so says nothing about whether the overlay,
 * its geometry or its state plumbing work. This closes that gap.
 *
 * IT REFUSES TO PASS ON AN EMPTY FRAME. A hidden window may never composite,
 * and a passthrough check on a blank canvas is blank-equals-blank: a green
 * result that measured nothing. So the source frame's distinct colours are
 * counted first and a thin one is reported as SKIP, not PASS. verify.py has
 * the same guard for the same reason -- "renderer draws a non-blank frame". */
const POST_GATE = `(async () => {
  const wait = (test, ms) => new Promise((res, rej) => {
    const t0 = Date.now();
    const t = setInterval(() => {
      if (test()) { clearInterval(t); res(true); }
      else if (Date.now() - t0 > ms) {
        clearInterval(t);
        rej(new Error('gave up waiting -- ' + (typeof POST === 'undefined'
          ? 'post-dev.js never ran'
          : 'POST.err=' + POST.err + ' post=' + !!POST.post + ' src=' + !!POST.src)));
      }
    }, 50);
  });
  await wait(() => typeof POST !== 'undefined' && (POST.err || (POST.post && POST.src)), 15000);
  if (POST.err) return ['SKIP  post chain unavailable -- ' + POST.err];

  const src = POST.src;
  /* WAIT FOR PAINT, do not sample once and judge. A hidden window throttles
     rAF hard, so the engine may not have drawn its first frame by the time
     window.AC exists -- and a single early sample makes this gate flaky in
     the one direction that matters, reporting a blank canvas as though the
     renderer were broken. Poll until there is a picture, then decide. */
  const colours = () => {
    const px = src.getContext('2d').getImageData(0, 0, src.width, src.height).data;
    const s2 = new Set();
    for (let i = 0; i < px.length; i += 4 * 97) {
      s2.add((px[i] << 16) | (px[i + 1] << 8) | px[i + 2]);
      if (s2.size > 64) break;
    }
    return s2.size;
  };
  try { await wait(() => colours() >= 16, 20000); } catch (e) { /* reported below */ }
  const seen = { size: colours() };
  if (seen.size < 16) {
    return ['SKIP  the source frame has only ' + seen.size + ' distinct colours ('
            + src.width + 'x' + src.height + ').',
            '      A hidden window did not composite, so passthrough would be',
            '      checked against a blank canvas. That is not a pass.'];
  }

  postToggle(true);
  /* THE PLUMBING IS WHAT THIS GATE CHECKS, so the effects come off first.
     With bloom on, a difference is the POINT and zero would be the bug --
     which would make a green here mean the opposite of what it says. The
     picker is put back afterwards so the app is left as the user had it. */
  const sel = document.getElementById('bloom');
  const selT = document.getElementById('trails');
  const was = sel ? sel.value : null;
  const wasT = selT ? selT.value : null;
  /* BOTH of them, and the first version of this cleared only bloom -- so the
     passthrough test ran with the trail pass still registered and reported
     zero differing pixels anyway, because the frame it happened to catch had
     nothing above the trail's threshold. A green that measured nothing, which
     is the same class of fault as the blank-frame case above. The assertion
     below is the one that would have caught it. */
  const selG = document.getElementById('grade');
  const wasG = selG ? selG.value : null;
  POST.post.setBloom(null);
  POST.post.setTrails(null);
  POST.post.setGrade(null);
  const st = postState();
  const r = POST.post.selfTest(src, st);
  if (sel && was !== null) { sel.value = was; postBloom(was); }
  if (selT && wasT !== null) { selT.value = wasT; postTrails(wasT); }
  if (selG && wasG !== null) { selG.value = wasG; postGrade(wasG); }
  /* AFTER the render, not before: the overlay's backing store is sized by
     resize() inside render(), so reading it first measures the 300x150 a
     canvas is born at and reports a mismatch that is really a stale read. */
  const geo = POST.overlay.getBoundingClientRect();
  const sized = POST.overlay.width === src.width && POST.overlay.height === src.height;
  postToggle(false);

  /* AND THEN THE LIVE PATH, WITH THE EFFECTS ON. The check above turns them
     off on purpose -- it is asking whether the plumbing is invisible. That
     leaves the two-pass readout draw, which only runs while the chain is on,
     completely unexercised, and "it should work" is not a thing this project
     gets to say about a picture. */
  let live = 'live path NOT run';
  try {
    postToggle(true);
    const ro = postReadouts();
    const st2 = postState();
    st2.dt = 1 / 60;
    st2.readouts = ro;
    POST.post.render(src, st2);
    const after = POST.post.readPixels();
    let diff = 0;
    const w2 = src.width, h2 = src.height;
    const base2 = src.getContext('2d').getImageData(0, 0, w2, h2).data;
    for (let y = 0; y < h2; y += 3) {
      const gy = h2 - 1 - y;
      for (let x = 0; x < w2; x += 3) {
        const i = (gy * w2 + x) * 4, j = (y * w2 + x) * 4;
        if (after[i] !== base2[j] || after[i+1] !== base2[j+1]
            || after[i+2] !== base2[j+2]) diff++;
      }
    }
    const n2 = Math.ceil(h2 / 3) * Math.ceil(w2 / 3);
    const roMode = document.getElementById('game').contentWindow.AC.renderer.roMode;
    live = 'live path ok -- readouts ' + (ro ? ro.width + 'x' + ro.height : 'NULL')
         + ', ' + (100 * diff / n2).toFixed(1) + '% px differ from the world pass'
         + ', roMode left at ' + roMode;
    if (!ro) live = 'live path FAILED -- postReadouts() returned null';
    if (roMode !== 1) live += '  !! roMode should be 1 while the chain is on';
    postToggle(false);
  } catch (e) {
    live = 'live path THREW -- ' + (e && e.message || e);
  }

  const out = [];
  out.push(live);
  out.push('[post] ' + POST.post.version + '  ' + src.width + 'x' + src.height
           + '  ' + r.passes + ' effect passes  ' + seen.size + '+ colours in source');
  out.push('[post] overlay backing store ' + POST.overlay.width + 'x' + POST.overlay.height
           + (sized ? ' (1:1 with source)' : '  MISMATCHED'));
  out.push('[post] overlay on screen ' + Math.round(geo.width) + 'x' + Math.round(geo.height)
           + ' at ' + Math.round(geo.left) + ',' + Math.round(geo.top));
  out.push('[post] arena rect ' + (st.rect
           ? [Math.round(st.rect.x), Math.round(st.rect.y),
              Math.round(st.rect.w), Math.round(st.rect.h)].join(',')
           : 'null') + '   cine ' + (st.cine ? 'read' : 'null'));
  out.push('');
  if (r.passes !== 0) {
    out.push('SKIP  ' + r.passes + ' effect passes were still registered when');
    out.push('      the passthrough was measured, so a zero here would mean');
    out.push('      nothing -- it would only say this frame had nothing bright');
    out.push('      enough for them to touch. The gate cleared the wrong set.');
  } else if (!sized) {
    out.push('FAIL  the overlay is not 1:1 with the source, so passthrough');
    out.push('      resamples and every later comparison is off by a filter.');
  } else if (r.differing === 0) {
    out.push('PASS  ' + r.total.toLocaleString() + ' px identical, max delta 0,');
    out.push('      through the app harness and not only the module.');
  } else {
    out.push('FAIL  ' + r.differing.toLocaleString() + ' of ' + r.total.toLocaleString()
             + ' px differ, max delta ' + r.maxDelta);
    if (r.sample) out.push('      first at ' + r.sample.x + ',' + r.sample.y
                           + '  got ' + r.sample.got.join(',')
                           + '  want ' + r.sample.want.join(','));
  }
  return out;
})()`;

protocol.registerSchemesAsPrivileged([{
  scheme: 'swb',
  privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true },
}]);

/* Path traversal is the one thing a file-serving handler must not get wrong.
 * Resolve, then prove the result is still inside the repo. A `..` that escapes
 * is refused, not clamped. */
function resolveInsideRepo(pathname) {
  const rel = decodeURIComponent(pathname).replace(/^\/+/, '');
  const abs = path.resolve(REPO, rel);
  const root = REPO + path.sep;
  if (abs !== REPO && !abs.startsWith(root)) return null;
  return abs;
}

function registerProtocol() {
  protocol.handle('swb', (req) => {
    const { pathname } = new URL(req.url);
    const abs = resolveInsideRepo(pathname);
    if (!abs || !fs.existsSync(abs) || !fs.statSync(abs).isFile()) {
      return new Response('not found', { status: 404 });
    }
    return net.fetch(url.pathToFileURL(abs).toString());
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1180,
    height: 980,
    show: !HEADLESS_GATE,
    backgroundColor: '#0b0b10',
    title: 'Super Weapon Ball — The Sundered Crown',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,   // non-negotiable
      nodeIntegration: false,   // non-negotiable
      sandbox: true,            // non-negotiable
      /* A hidden window gets its timers throttled to about 1 Hz, and the
       * shell reaches window.AC through a setInterval poll. Only relaxed for
       * the headless gate, where nothing is being shown to throttle for. */
      backgroundThrottling: !HEADLESS_GATE,
    },
  });
  win.loadURL('swb://app/app/ui/shell.html');
  return win;
}

/* ---- IPC. Every capability the page has is named here and nowhere else. ---- */

ipcMain.handle('swb:gamePath', () => GAME);

ipcMain.handle('swb:repoRoot', () => REPO);

/* Phase 1's falsification test, from the app's side. Writes the app's own
 * simulate() results to disk so tools/shell_identity.py can diff them against
 * headless Chromium. See docs/ARCHITECTURE.md §3. */
ipcMain.handle('swb:writeIdentity', async (_e, payload) => {
  const out = path.join(REPO, 'out', 'shell_identity_app.json');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(payload, null, 2));
  return out;
});

ipcMain.handle('swb:revealFile', async (_e, p) => {
  const abs = resolveInsideRepo(p.startsWith('/') ? p : '/' + p);
  if (!abs) return false;
  shell.showItemInFolder(abs);
  return true;
});

/* PLACEHOLDER, and deliberately honest about it. Phase 3 replaces this with a
 * real job queue over shorts_build.py: a full 60fps capture is ~2,800 frames
 * and 3-4 minutes, so this can never be a blocking call that returns a file.
 * It returns progress or it lies. */
ipcMain.handle('swb:createShort', async () => {
  return { ok: false, reason: 'not built yet — docs/ARCHITECTURE.md §5' };
});

/* PLACEHOLDER. Phase 2. cinema_vo.py --text already speaks arbitrary text
 * verbatim; this wires to it. */
ipcMain.handle('swb:speak', async () => {
  return { ok: false, reason: 'not built yet — docs/ARCHITECTURE.md §4' };
});

app.whenReady().then(async () => {
  registerProtocol();
  const win = createWindow();

  if (HEADLESS_GATE) {
    /* Drives the page's own runIdentity() rather than reimplementing the
     * sweep here. Two implementations of one measurement is how the two sides
     * agree on a shared mistake and the check passes on it. */
    try {
      /* The gate runs with no devtools and no window, so a page error is
       * otherwise a shrug. Forward it. */
      win.webContents.on('console-message', (ev) => {
        if (ev.level === 'error' || ev.level === 'warning') {
          process.stderr.write('  page: ' + ev.message
                               + '  (' + ev.sourceId + ':' + ev.lineNumber + ')' + '\n');
        }
      });
      await new Promise((r) => win.webContents.once('did-finish-load', r));
      await win.webContents.executeJavaScript(
        'new Promise((r, j) => { let n = 0; const t = setInterval(() => {' +
        '  if (typeof AC !== "undefined" && AC && AC.WEAPONS) { clearInterval(t); r(1); }' +
        '  else if (++n > 200) { clearInterval(t); j(new Error("window.AC never appeared")); }' +
        '}, 50); })');
      if (IDENTITY) {
        await win.webContents.executeJavaScript('runIdentity()');
        const said = await win.webContents.executeJavaScript(
          'document.getElementById("identityOut").textContent');
        process.stdout.write(said + '\n');
      } else {
        const said = (await win.webContents.executeJavaScript(POST_GATE))
          .join(String.fromCharCode(10));
        process.stdout.write(said + '\n');
      }
      app.exit(0);
    } catch (e) {
      process.stderr.write((IDENTITY ? 'identity' : 'post') + ' check failed: '
                           + (e && e.stack || e && e.message || e) + '\n');
      app.exit(1);
    }
    return;
  }

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
