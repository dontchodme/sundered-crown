/* Runs mathfp.js inside ELECTRON's Chromium and prints the result as JSON on
   stdout. Driven by math_fingerprint.py; there is nothing to run here by hand.

   A blank page, not the game: the fingerprint is a property of the V8 build
   and loading 19,000 lines of engine to ask it would only add ways to fail. */
const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

const FP = path.join(__dirname, 'mathfp.js');

app.disableHardwareAcceleration();
app.whenReady().then(async () => {
  const w = new BrowserWindow({ show: false, webPreferences: { offscreen: true } });
  await w.loadURL('data:text/html,<!doctype html><title>mathfp</title>');
  const src = fs.readFileSync(FP, 'utf8');
  const r = await w.webContents.executeJavaScript('(' + src + ')()');
  process.stdout.write(JSON.stringify(r));
  app.exit(0);
}).catch(e => { process.stderr.write(String(e)); app.exit(1); });
