/* Runs the particle field's per-frame cost in ELECTRON, on the real GPU, and
 * prints JSON. Driven by tools/ult_particle_lab.py --cost; nothing to run here
 * by hand.
 *
 * THIS FILE EXISTS BECAUSE THE FIRST MEASUREMENT WAS TAKEN THROUGH PLAYWRIGHT
 * AND WAS WORTHLESS. Playwright launches with --disable-gpu, so its WebGL and
 * its Canvas rasterisation are SwiftShader -- software. It reported a 43 ms
 * BASELINE for a frame the app draws in 9, which is not a small error, it is a
 * different machine. post_cost.py's header says exactly this and defaults to
 * Electron for exactly this reason; the caveat was ignored once and this is
 * the correction.
 *
 * Deliberately NOT offscreen and NOT with hardware acceleration disabled, and
 * the window is SHOWN -- the same three choices postcost_electron.js makes,
 * for the same reasons. A hidden window can have its compositing throttled or
 * skipped, and a frame that was never composited is cheap for a reason that
 * has nothing to do with the particles.
 */
const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..');

function arg(name, dflt) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : dflt;
}

const GAME = arg('game', path.join(REPO, '02-chain', 'sc-paradox-frame.html'));
/* THE CONFIG COMES FROM A FILE, NOT THE COMMAND LINE. It carries whole JS
 * sources, which contain `>`, `&` and `|` -- and electron.cmd is a BATCH
 * shim, so cmd.exe parses those before Electron ever sees them and the run
 * dies with "> was unexpected at this time." A path has no metacharacters. */
const CFG = JSON.parse(fs.readFileSync(arg('cfgfile'), 'utf8'));

app.whenReady().then(async () => {
  const w = new BrowserWindow({
    width: 700, height: 900, show: true, backgroundColor: '#0b0b10',
    webPreferences: { backgroundThrottling: false },
  });
  try {
    await w.loadFile(GAME);
    await w.webContents.executeJavaScript(
      'new Promise((r, j) => { let n = 0; const t = setInterval(() => {' +
      '  if (window.AC && AC.WEAPONS) { clearInterval(t); r(1); }' +
      '  else if (++n > 200) { clearInterval(t); j(new Error("AC never appeared")); }' +
      '}, 50); })');
    /* The page keeps its own rAF loop and it would step the sim under the
       measurement. Same flag render.py and postcost_electron.js set. */
    await w.webContents.executeJavaScript('window.__frozen = true; 1');
    await w.webContents.executeJavaScript(CFG.fx + '; 1');
    await w.webContents.executeJavaScript(
      '(' + CFG.setup + ')(' + JSON.stringify(CFG.setupArgs) + '); 1');
    await w.webContents.executeJavaScript('(' + CFG.fx + ')(); 1');
    const out = await w.webContents.executeJavaScript(
      '(' + CFG.cost + ')(' + JSON.stringify(CFG.costArgs) + ')');
    const rend = await w.webContents.executeJavaScript(
      "(() => { const g = document.createElement('canvas').getContext('webgl2');"
      + " if (!g) return 'no webgl2';"
      + " const d = g.getExtension('WEBGL_debug_renderer_info');"
      + " return d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL)"
      + "          : g.getParameter(g.RENDERER); })()");
    process.stdout.write(JSON.stringify({ rows: out, renderer: rend }));
    app.exit(0);
  } catch (e) {
    process.stderr.write('fx_cost failed: ' + (e && e.stack || e) + '\n');
    app.exit(1);
  }
});
