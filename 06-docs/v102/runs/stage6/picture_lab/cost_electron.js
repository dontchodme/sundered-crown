/* Frame cost of the Rebuttal picture on the REAL GPU, through Electron (the
   app's runtime), the fxcost_electron.js pattern: shown window, no throttling,
   raster forced with a 1px readback inside rAF. Scratch copy; prints JSON.
   Attempt 3: OTHER BUILDS RUN ELECTRON ON THIS PC AT THE SAME TIME and two
   instances on the default userData (%APPDATA%\Electron) collide (r1 died
   after one fight, r2 at once, both on "Unable to move the cache"). A private
   userData per run, the result written to --outfile too, and a crashed
   renderer / closed window reported (widowmaker's attempt-3 fix). */
const { app, BrowserWindow } = require('electron');
const fs = require('fs'), path = require('path'), os = require('os');
function arg(n, d){ const i = process.argv.indexOf('--' + n); return i >= 0 ? process.argv[i + 1] : d; }
const GAME = arg('game'), CFG = JSON.parse(fs.readFileSync(arg('cfgfile'), 'utf8'));
app.setPath('userData', fs.mkdtempSync(path.join(os.tmpdir(), 'sc-ld-el-')));
const OUTF = arg('outfile', null);
app.on('window-all-closed', () => { process.stderr.write('window-all-closed\n'); app.exit(4); });
app.whenReady().then(async () => {
  const w = new BrowserWindow({ width: 700, height: 900, show: true, backgroundColor: '#0b0b10',
                                webPreferences: { backgroundThrottling: false } });
  w.webContents.on('render-process-gone', (e, d) => { process.stderr.write('render-process-gone ' + JSON.stringify(d) + '\n'); app.exit(3); });
  try {
    await w.loadFile(GAME);
    await w.webContents.executeJavaScript('new Promise((r, j) => { let n = 0; const t = setInterval(() => {' +
      ' if (window.AC && AC.WEAPONS) { clearInterval(t); r(1); } else if (++n > 200) { clearInterval(t); j(new Error("no AC")); }' +
      '}, 50); })');
    await w.webContents.executeJavaScript('window.__frozen = true; 1');
    const out = await w.webContents.executeJavaScript('(' + CFG.js + ')(' + JSON.stringify(CFG.args) + ')');
    const rend = await w.webContents.executeJavaScript(
      "(() => { const g = document.createElement('canvas').getContext('webgl2'); if (!g) return 'no webgl2';" +
      " const d = g.getExtension('WEBGL_debug_renderer_info'); return d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); })()");
    const J = JSON.stringify({ out, renderer: rend });
    if (OUTF) fs.writeFileSync(OUTF, J);
    process.stdout.write(J);
    app.exit(0);
  } catch (e) { process.stderr.write('cost failed: ' + (e && e.stack || e) + '\n'); app.exit(1); }
});
