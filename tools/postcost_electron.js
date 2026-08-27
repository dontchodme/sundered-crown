/* Runs tools/postcost.js in ELECTRON, on the real GPU, and prints JSON.
 * Driven by tools/post_cost.py; nothing to run here by hand.
 *
 * Deliberately NOT offscreen and NOT with hardware acceleration disabled --
 * which is the opposite of mathfp_electron.js, and for the opposite reason.
 * The fingerprint wants V8 and does not care about the rasteriser; this wants
 * the rasteriser and nothing else. A cost measured on SwiftShader is a
 * measurement of SwiftShader.
 *
 * The window is shown. A hidden window can have its compositing throttled or
 * skipped entirely, and a frame that was never composited is cheap for a
 * reason that has nothing to do with the chain.
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
const CFG = JSON.parse(arg('cfg', '{}'));

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
    /* The game keeps its own rAF loop running and it would step the sim under
       the measurement. Same flag render.py sets. */
    await w.webContents.executeJavaScript('window.__frozen = true; 1');
    await w.webContents.executeJavaScript(
      fs.readFileSync(path.join(REPO, 'src', 'render', 'post.js'), 'utf8') + '; 1');
    const js = fs.readFileSync(path.join(HERE, 'postcost.js'), 'utf8');
    const out = await w.webContents.executeJavaScript(
      '(' + js + ')(' + JSON.stringify(CFG) + ')');
    process.stdout.write(JSON.stringify(out));
    app.exit(0);
  } catch (e) {
    process.stderr.write('post_cost failed: ' + (e && e.stack || e) + '\n');
    app.exit(1);
  }
});
