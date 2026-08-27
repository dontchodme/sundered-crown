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
    show: !IDENTITY,
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
      backgroundThrottling: !IDENTITY,
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

  if (IDENTITY) {
    /* Drives the page's own runIdentity() rather than reimplementing the
     * sweep here. Two implementations of one measurement is how the two sides
     * agree on a shared mistake and the check passes on it. */
    try {
      await new Promise((r) => win.webContents.once('did-finish-load', r));
      await win.webContents.executeJavaScript(
        'new Promise((r, j) => { let n = 0; const t = setInterval(() => {' +
        '  if (typeof AC !== "undefined" && AC && AC.WEAPONS) { clearInterval(t); r(1); }' +
        '  else if (++n > 200) { clearInterval(t); j(new Error("window.AC never appeared")); }' +
        '}, 50); })');
      await win.webContents.executeJavaScript('runIdentity()');
      const said = await win.webContents.executeJavaScript(
        'document.getElementById("identityOut").textContent');
      process.stdout.write(said + '\n');
      app.exit(0);
    } catch (e) {
      process.stderr.write('identity check failed: ' + (e && e.message || e) + '\n');
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
