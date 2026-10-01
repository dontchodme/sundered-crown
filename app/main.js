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
 * pipeline renders. Keep it pointed at the build of record.
 *
 * AND IT IS ONE PLACE THAT STILL HAS TO BE MOVED BY HAND, WHICH IS THE WHOLE
 * FAILURE MODE. v48 shipped Vesper -- new build of record, twenty-seven
 * relics -- with every gate green and this line still naming the twenty-sixth,
 * so the app would have shown the PREVIOUS relic while the video rendered the
 * new one. Nothing catches it: `shell_identity` compares the app against
 * headless on whatever GAME says, so it passes on a stale pointer, and
 * `chain_audit` never looks outside 02-chain. It was caught because somebody
 * grepped before saying "go and watch it in the app".
 *
 * IF YOU ADD A RELIC, THIS LINE IS PART OF THE CARRY. */
const GAME = process.env.SWB_GAME || '02-chain/sc-cupcard.html';

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
          : 'POST.err=' + POST.err + ' fx=' + !!POST.fx)));
      }
    }, 50);
  });
  await wait(() => typeof POST !== 'undefined' && (POST.err || POST.fx), 15000);
  if (POST.err) return ['SKIP  post chain unavailable -- ' + POST.err];

  const w = document.getElementById('game').contentWindow;
  const AC = w.AC, src = w.document.getElementById('cv');

  const colours = () => {
    const px = src.getContext('2d').getImageData(0, 0, src.width, src.height).data;
    const s2 = new Set();
    for (let i = 0; i < px.length; i += 4 * 97) {
      s2.add((px[i] << 16) | (px[i + 1] << 8) | px[i + 2]);
      if (s2.size > 64) break;
    }
    return s2.size;
  };
  try { await wait(() => colours() >= 16, 20000); } catch (e) {}
  const seen = colours();
  if (seen < 16) {
    return ['SKIP  the source frame has only ' + seen + ' distinct colours.',
            '      A hidden window did not composite, so nothing below would',
            '      have measured anything. That is not a pass.'];
  }

  const out = [];
  out.push('[post] build ' + POST.fx.post.version + '  ' + src.width + 'x'
           + src.height + '  chain ' + (POST.fx.on ? 'ON' : 'OFF')
           + '  passes: ' + POST.fx.post.passes.map(p => p.name).join('+'));
  out.push('[post] shell ' + (window.SWBPost ? window.SWBPost.VERSION : '?')
           + '   defaults ' + window.SWBPost.SPREAD.DEFAULT + '/'
           + window.SWBPost.TRAILS.DEFAULT + '/' + window.SWBPost.GRADE.DEFAULT);

  /* ONE CHAIN, AND THIS IS THE ASSERTION THAT SAYS SO. If the shell ever
     builds its own again, the app post-processes an already post-processed
     frame and shows Rick something the mp4 cannot contain. */
  if (POST.overlay || (POST.post && POST.post !== POST.fx.post)) {
    out.push('');
    out.push('FAIL  the shell is running a SECOND chain. There must be one,');
    out.push('      and it lives in the build.');
    return out;
  }
  out.push('[post] one chain: the shell drives the one in the build');

  /* the live path: the chain on, a real composited frame */
  POST.fx.on = true;
  POST.fx.reset();
  AC.renderer.roMode = 0;
  AC.__draw(AC.match);
  const lit = colours();
  out.push('[post] chain ON draws ' + lit + '+ distinct colours');

  /* and the plumbing, with every pass off */
  const b = document.getElementById('bloom').value;
  const t2 = document.getElementById('trails').value;
  const g = document.getElementById('grade').value;
  POST.fx.post.setBloom(null);
  POST.fx.post.setTrails(null);
  POST.fx.post.setGrade(null);
  POST.fx.on = false;
  AC.renderer.roMode = 1;
  AC.__draw(AC.match);
  AC.renderer.roMode = 0;
  const r = POST.fx.post.selfTest(src, {
    enabled: true,
    rect: { x: AC.renderer.pad * AC.renderer.k,
            y: AC.renderer.arenaTop * AC.renderer.k,
            w: AC.renderer.aw * AC.renderer.k,
            h: AC.renderer.ah * AC.renderer.k },
  });
  document.getElementById('bloom').value = b;
  document.getElementById('trails').value = t2;
  document.getElementById('grade').value = g;
  postApply();
  POST.fx.on = true;

  out.push('');
  if (r.passes !== 0) {
    out.push('SKIP  ' + r.passes + ' passes were still registered when the');
    out.push('      passthrough was measured, so a zero would mean nothing.');
  } else if (r.differing === 0) {
    out.push('PASS  ' + r.total.toLocaleString() + ' px identical, max delta 0,');
    out.push('      through the chain in the build, not a copy of it.');
  } else {
    out.push('FAIL  ' + r.differing.toLocaleString() + ' of '
             + r.total.toLocaleString() + ' px differ, max delta ' + r.maxDelta);
    if (r.sample) out.push('      first at ' + r.sample.x + ',' + r.sample.y);
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

/* ---- PYTHON, FOR THE TWO FEATURES THAT SHELL OUT --------------------------
 *
 * execFile, NEVER exec: the announcer's text is user input and it goes in as
 * ONE ARGV ELEMENT. With a shell in the way a line containing `&` or a quote
 * would be a command, not a sentence. There is no shell here and there must
 * not be one.
 *
 * `python`, not `python3`: the python.org installer makes python.exe and
 * py.exe and no python3.exe, so python3 hits a Microsoft Store stub that
 * reports Python is not installed. Three tools in tools/ had this bug and it
 * cost a render today. CLAUDE.md §5. SWB_PYTHON overrides for a venv.
 */
const { execFile } = require('node:child_process');
const os = require('node:os');
const PYTHON = process.env.SWB_PYTHON || 'python';

/* The last non-empty line of a tool's stderr is where its complaint is; the
 * lines above it are a traceback nobody in the UI can act on. */
function lastLine(t) {
  const lines = String(t || '').split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  return lines.length ? lines[lines.length - 1] : '';
}

/* THE CHILD'S PATH, NOT THIS PROCESS'S.
 *
 * winget installs ffmpeg without a shim, so it is only on PATH if the user
 * added it -- and a GUI app inherits the PATH of whatever launched it, which
 * may predate that. The app itself never needs ffmpeg; shorts_build's ENCODE
 * stage does, three minutes into a job, long after the capture has succeeded.
 * So the failure looked like a mystery: the frames were all there and the
 * pipeline died at the end.
 *
 * Resolved and injected here rather than asking the user to fix their
 * environment, and it is also why docs/ARCHITECTURE.md §5 says to ship
 * ffmpeg-static with the app: this is the same problem, patched. */
function childEnv() {
  const ff = resolveFfmpeg();
  if (ff === 'ffmpeg') return process.env;          // already on PATH
  const dir = path.dirname(ff);
  const key = Object.keys(process.env).find((k) => k.toUpperCase() === 'PATH') || 'PATH';
  return { ...process.env, [key]: dir + path.delimiter + (process.env[key] || '') };
}

function runPython(args, { timeout = 120000 } = {}) {
  return new Promise((resolve) => {
    execFile(PYTHON, args, { cwd: path.join(REPO, 'tools'), timeout,
                             env: childEnv(),
                             maxBuffer: 16 * 1024 * 1024 },
      (err, stdout, stderr) => resolve({
        ok: !err, code: err ? (err.code ?? -1) : 0,
        stdout: String(stdout || ''), stderr: String(stderr || ''),
        timedOut: !!(err && err.killed),
      }));
  });
}

/* Duration straight out of the RIFF header rather than off cinema_vo's stdout.
 * Parsing a tool's printed text is a contract nobody wrote down; the header is
 * one. Walks the chunks because a WAV is not required to put `data` at byte 36
 * -- soundfile does, but a file that has been through anything else may not. */
function wavSeconds(buf) {
  if (buf.length < 12 || buf.toString('ascii', 0, 4) !== 'RIFF') return null;
  let off = 12, fmt = null;
  while (off + 8 <= buf.length) {
    const id = buf.toString('ascii', off, off + 4);
    const size = buf.readUInt32LE(off + 4);
    if (id === 'fmt ') {
      fmt = { channels: buf.readUInt16LE(off + 10),
              rate: buf.readUInt32LE(off + 12),
              bits: buf.readUInt16LE(off + 22) };
    } else if (id === 'data' && fmt) {
      const bytesPerFrame = fmt.channels * Math.max(1, fmt.bits / 8);
      if (!bytesPerFrame || !fmt.rate) return null;
      return size / bytesPerFrame / fmt.rate;
    }
    off += 8 + size + (size % 2);
  }
  return null;
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

/* ---- CREATE SHORT -------------------------------------------------------
 *
 * A full capture is ~2,800-4,000 frames and 4-5 minutes -- and a worst-case
 * pairing on the v65 pace runs to ~7,000 frames and ~8 -- so this cannot be a
 * call that returns a file. It starts a job, streams what the pipeline says,
 * and can be cancelled. ONE AT A TIME: two captures would fight over the same
 * _clip_frames directory and the second would encode the first one's frames.
 *
 * The pipeline is shorts_build.py, unchanged and unreimplemented. Its mix
 * graph has one flag (`alimiter ... level=false`) that is invisible in the
 * output and merely makes the file clip if forgotten, and its law -- never
 * patch a mix, re-capture -- is held by construction there. Moving any of that
 * in here would be rewriting the one part of this project that is measured.
 */
let JOB = null;

function jobSend(win, channel, payload) {
  if (win && !win.isDestroyed()) win.webContents.send(channel, payload);
}

/* ONE JOB AT A TIME INCLUDES THE SECONDS BEFORE ONE STARTS. createShort
 * renders a typed announcer line (cinema_vo, several seconds) between its
 * guard and the spawn that sets JOB, and a guard that reads only JOB lets a
 * Crown Cup run -- or a second short -- start inside that window. */
let STARTING = false;

function busyReason() {
  if (JOB) return JOB.kind === 'cup' ? `the Crown Cup is running (${JOB.cmd})`
                                     : 'a short is already rendering';
  return STARTING ? 'a short is starting' : null;
}

/* ffmpeg is needed to pull frames off the finished file. winget installs it
 * without a shim, so `ffmpeg` is not on PATH until the user adds it -- and a
 * GUI app inherits the PATH it was LAUNCHED with, which may predate that. So:
 * PATH first, then the place winget actually puts it, then say so plainly. */
function resolveFfmpeg() {
  const candidates = ['ffmpeg'];
  const local = process.env.LOCALAPPDATA;
  if (local) {
    const base = path.join(local, 'Microsoft', 'WinGet', 'Packages');
    try {
      for (const d of fs.readdirSync(base)) {
        if (!d.startsWith('Gyan.FFmpeg')) continue;
        for (const b of fs.readdirSync(path.join(base, d))) {
          const exe = path.join(base, d, b, 'bin', 'ffmpeg.exe');
          if (fs.existsSync(exe)) candidates.push(exe);
        }
      }
    } catch {}
  }
  for (const c of candidates.slice(1)) if (fs.existsSync(c)) return c;
  return 'ffmpeg';
}

/* FOUR FRAMES OFF THE FINISHED FILE, BECAUSE EVERY FAILURE THIS PIPELINE HAS
 * PRODUCED WAS INVISIBLE TO ITS OWN CHECKS AND OBVIOUS IN ONE FRAME: relics
 * halved by the bottom edge, a beige-washed kill, a voiceover naming a relic
 * the card does not call by that name. The delivery checks pass on all of
 * those. SHORTSHANDOFF's second law, enforced in the UI rather than trusted. */
function pullFrames(mp4, seconds) {
  const ff = resolveFfmpeg();
  const at = [0.10, 0.35, 0.65, 0.92].map((f) => Math.max(0, seconds * f));
  return Promise.all(at.map((t) => new Promise((resolve) => {
    const out = path.join(os.tmpdir(), `swb-f-${Date.now()}-${Math.round(t * 100)}.jpg`);
    execFile(ff, ['-y', '-hide_banner', '-loglevel', 'error', '-ss', String(t),
                  '-i', mp4, '-frames:v', '1', '-q:v', '4', out], (err) => {
      if (err || !fs.existsSync(out)) return resolve(null);
      let b64 = null;
      try { b64 = fs.readFileSync(out).toString('base64'); } catch {}
      try { fs.unlinkSync(out); } catch {}
      resolve(b64 ? { t, jpg: b64 } : null);
    });
  }))).then((r) => r.filter(Boolean));
}

async function createShort(e, opts = {}) {
  if (JOB) return { ok: false, reason: 'a short is already rendering' };
  const win = BrowserWindow.fromWebContents(e.sender);

  const a = String(opts.a || '').trim(), b = String(opts.b || '').trim();
  const seed = Number(opts.seed) >>> 0;
  if (!a || !b) return { ok: false, reason: 'pick two relics first' };
  if (a === b) return { ok: false, reason: 'a relic cannot fight itself' };

  /* ONE DIRECTORY PER JOB, because shorts_build puts `_clip_frames` NEXT TO
   * THE OUTPUT FILE. Two renders sharing a parent folder share that frame
   * directory and interleave into each other -- the second capture's frames
   * land among the first's and the encode splices two different fights into
   * one file. Measured: 4,747 h264 decode errors against 0 for a render that
   * had its folder to itself.
   *
   * The in-app guard stops two jobs from the button, and cannot see a render
   * started from a terminal. A folder per job makes the collision impossible
   * rather than merely disallowed. */
  /* WHERE A SHORT LANDS.
   *
   *   07-shorts/app/2026-08-28/1904-dawnbringer-v-widowmaker-2195072936/
   *       1904-dawnbringer-v-widowmaker-2195072936.mp4
   *       ...-hook.wav          the voiceover, kept beside its render
   *       _clip_frames/         transient, deleted on a clean pass
   *
   * A DATE FOLDER because a day's output is the unit a person actually looks
   * for, and a TIME PREFIX because within a day the order they were made in is
   * the order they are worth comparing in -- `ls` sorts them correctly with no
   * effort.
   *
   * A FOLDER PER JOB because shorts_build puts `_clip_frames` NEXT TO THE
   * OUTPUT FILE. Two renders sharing a parent share that directory and
   * interleave: the second capture's frames land among the first's and the
   * encode splices two different fights into one file. Measured at 4,747 h264
   * decode errors against 0 for a render that had its folder to itself. The
   * in-app guard stops two jobs from the button and cannot see one started
   * from a terminal -- a folder per job makes it impossible rather than
   * merely disallowed. */
  const now = new Date();
  const p2 = (n) => String(n).padStart(2, '0');
  const day = `${now.getFullYear()}-${p2(now.getMonth() + 1)}-${p2(now.getDate())}`;
  const hhmm = `${p2(now.getHours())}${p2(now.getMinutes())}`;
  const stem = `${hhmm}-${a}-v-${b}-${seed}`;
  const dir = path.join(REPO, '07-shorts', 'app', day, stem);
  fs.mkdirSync(dir, { recursive: true });
  const out = path.join(dir, `${stem}.mp4`);

  /* ABSOLUTE. GAME is repo-relative ('02-chain/...'), and shorts_build
   * resolves --game against its OWN directory -- `HERE / game` -- so passing
   * it through unchanged looked for tools/02-chain/... and the job died on its
   * first line. The app and the tools do not share a base directory and there
   * is no reason they should; the path that crosses between them is absolute. */
  const gameAbs = path.isAbsolute(GAME) ? GAME : path.join(REPO, GAME);
  const args = ['shorts_build.py', '--game', gameAbs, '--a', a, '--b', b,
                '--seed', String(seed), '--no-card', '--out', out];
  /* --no-card is not a preference. cinema_clip REFUSES --intro without
   * --legacy-card: the fight card is retired (rule 1) and card-first videos
   * lose 71-75% of the audience present when it appears. */
  if (opts.lead) args.push('--lead', String(Number(opts.lead)));

  /* THE ANNOUNCER BOX HAS TO REACH THE SHORT, AND `--vo` TAKES A WAV.
   *
   * shorts_build renders the default hook itself when no --vo is given, which
   * is the right behaviour for an empty box. A typed line is not text it can
   * accept: passing it as --vo would hand a sentence where a file path goes.
   * So the line is rendered HERE first, through the same --script path the
   * preview uses, and the wav is handed over.
   *
   * Written next to the mp4 rather than into tmp: shorts_build names its own
   * hook wav that way, and a voiceover that outlives its render is worth
   * having when a mix is questioned later. */
  const line = String(opts.vo ?? '').trim();
  if (line) {
    const voOut = out.replace(/\.mp4$/, '-vo.wav');
    const rv = await runPython(['cinema_vo.py', '--a', a, '--b', b,
                                '--script', line, '--voice',
                                String(opts.voice || 'bm_lewis'),
                                '--out', voOut], { timeout: 180000 });
    if (!rv.ok || !fs.existsSync(voOut)) {
      return { ok: false, reason: lastLine(rv.stderr) || 'the voice line failed to render' };
    }
    args.push('--vo', voOut);
  }

  const child = require('node:child_process').spawn(PYTHON, args,
    { cwd: path.join(REPO, 'tools'), windowsHide: true, env: childEnv() });
  JOB = { child, out, cancelled: false, log: [] };

  const feed = (buf, stream) => {
    for (const raw of String(buf).split(/\r?\n/)) {
      const line = raw.trimEnd();
      if (!line) continue;
      JOB.log.push(line);
      const m = /^\[progress\] capture frames=(\d+) elapsed=([\d.]+)/.exec(line);
      if (m) {
        jobSend(win, 'swb:shortProgress',
                { stage: 'capture', frames: +m[1], elapsed: +m[2] });
      } else {
        jobSend(win, 'swb:shortLog', { line, stream });
      }
    }
  };
  child.stdout.on('data', (d) => feed(d, 'out'));
  child.stderr.on('data', (d) => feed(d, 'err'));

  child.on('close', async (code) => {
    const cancelled = JOB && JOB.cancelled;
    const log = JOB ? JOB.log : [];
    JOB = null;
    if (cancelled) return jobSend(win, 'swb:shortDone', { ok: false, cancelled: true });
    if (code !== 0 || !fs.existsSync(out)) {
      return jobSend(win, 'swb:shortDone', { ok: false,
        reason: log.filter(Boolean).slice(-1)[0] || `shorts_build exited ${code}`, log });
    }
    /* The tool prints its own measured delivery line; the duration is read back
     * off it rather than assumed, and the frames are sampled against it. */
    const dur = (() => {
      for (const l of log) {
        const m = /([\d.]+)s\s+[\d.]+MB/.exec(l);
        if (m) return parseFloat(m[1]);
      }
      return 23;
    })();
    const frames = await pullFrames(out, dur);
    jobSend(win, 'swb:shortDone',
            { ok: true, file: out, seconds: dur, frames, log });
  });

  return { ok: true, started: true, out };
}

ipcMain.handle('swb:createShort', async (e, opts) => {
  const busy = busyReason();
  if (busy) return { ok: false, reason: busy };
  STARTING = true;
  try { return await createShort(e, opts); } finally { STARTING = false; }
});

ipcMain.handle('swb:cancelShort', async () => {
  if (!JOB || JOB.kind === 'cup') return { ok: false, reason: 'no short is rendering' };
  JOB.cancelled = true;
  /* The python parent spawns cinema_clip as a child; killing the parent alone
   * leaves a Playwright Chromium capturing into a directory nobody is watching.
   * /T takes the tree. */
  try {
    require('node:child_process').execFile(
      'taskkill', ['/pid', String(JOB.child.pid), '/T', '/F'], () => {});
  } catch { try { JOB.child.kill(); } catch {} }
  return { ok: true };
});

/* ---- THE CROWN CUP -------------------------------------------------------
 *
 * 06-docs/v115/CROWN-CUP-APP-BRIEF-v115.md. tools/cup.py films the whole
 * tournament in posting order by spawning the same shorts_build.py that
 * createShort spawns -- the same arguments plus the stakes band, one folder
 * per fixture -- and prints shorts_build's own lines through. So this is
 * createShort's shape again, a job, a stream and a cancel around a different
 * script, and it SHARES createShort's JOB: a cup run and a single short would
 * split the machine's capture budget and talk over each other on progress.
 *
 * NOTHING ABOUT THE TOURNAMENT IS DECIDED HERE. The draw, the seed rule, the
 * band copy, the folders and the freeze are cup.py's -- it refuses a build or
 * a machine that is not the ledger's, so the freeze is held by the tool and
 * not by anybody's memory -- and this file names three of its commands and
 * hands it the app's own GAME. --force and --redo are never sent: a redraw is
 * terminal-only because a draw is a commitment.
 *
 * SWB_CUP_DIR points the panel at another folder inside the repo, the way
 * SWB_GAME points the window at another build. It is how the panel is tested
 * on a stand-in field without a draw ever landing in 07-shorts/cup1/, where a
 * ledger IS the tournament. */
const cupLines = require('./cuplines');
const CUP_DIR = (() => {
  try {
    const d = resolveInsideRepo('/' + (process.env.SWB_CUP_DIR || '07-shorts/cup1'));
    if (d) return d;
  } catch {}
  return path.join(REPO, '07-shorts', 'cup1');
})();
const CUP_CMDS = ['draw', 'seeds', 'film'];

function readLedger() {
  return JSON.parse(fs.readFileSync(path.join(CUP_DIR, 'ledger.json'), 'utf8'));
}

/* cup.py -> shorts_build -> cinema_clip -> a Playwright Chromium, four deep.
 * /T takes the tree, as cancelShort's does; the parent alone would leave a
 * browser capturing into a folder nobody is watching. */
function killTree(child) {
  if (process.platform === 'win32') {
    execFile('taskkill', ['/pid', String(child.pid), '/T', '/F'], () => {});
  } else {
    try { child.kill(); } catch {}
  }
}

/* A CANCEL MUST NOT LEAVE A FILE THAT cup.py WILL SKIP. cup.py resumes by
 * skipping every fixture whose mp4 exists, and shorts_build writes the
 * delivered mp4 IN PLACE during its mix -- so a cancel in a fixture's last
 * seconds leaves a partial file at the final path, and the next Film all
 * would pass over it as filmed. The file of the fixture that was in flight is
 * removed, and only when the ledger holds no clean film of it: cup.py stamps
 * `filmed` after shorts_build exits 0, never before. */
function removeUnfilmed(fixture) {
  if (!fixture) return;
  let f;
  try { f = (readLedger().fixtures || []).find((x) => x.id === fixture.id); } catch { return; }
  if (!f || f.filmed) return;
  const abs = path.resolve(CUP_DIR, fixture.file);
  if (!abs.startsWith(CUP_DIR + path.sep) || !abs.endsWith('.mp4')) return;
  /* The tree is still dying when cup.py's pipe closes, and Windows will not
   * delete a file an ffmpeg still holds open. */
  let tries = 0;
  const rm = () => {
    try { fs.rmSync(abs, { force: true }); } catch { if (++tries < 20) setTimeout(rm, 250); }
  };
  rm();
}

/* The ledger as it stands on disk, or {none:true}. cup.py writes it through a
 * temp file and a rename after every fixture, so a read mid-run is whole. */
ipcMain.handle('swb:cupLedger', async () => {
  const dir = path.relative(REPO, CUP_DIR).split(path.sep).join('/');
  const running = JOB && JOB.kind === 'cup' ? JOB.cmd : null;
  let ledger;
  try { ledger = readLedger(); } catch (err) {
    if (err.code === 'ENOENT') return { none: true, dir, running };
    return { ok: false, dir, running, reason: `${dir}/ledger.json: ${err.message}` };
  }
  return { ok: true, dir, running, ledger,
           schedule: fs.existsSync(path.join(CUP_DIR, 'SCHEDULE.md')) };
});

ipcMain.handle('swb:cupRun', async (e, opts = {}) => {
  const busy = busyReason();
  if (busy) return { ok: false, reason: busy };
  const cmd = String(opts.cmd || '');
  if (!CUP_CMDS.includes(cmd)) return { ok: false, reason: `not a cup command: ${cmd}` };

  /* createShort's line: GAME made absolute, because the tools resolve a
   * relative --game against tools/ and not against the repo. */
  const gameAbs = path.isAbsolute(GAME) ? GAME : path.join(REPO, GAME);
  /* `-u` because cup.py's own lines are print()s without a flush, and a pipe
   * is block-buffered: the log would arrive in 8 KB lumps, a whole Seed all
   * in one at the end. shorts_build flushes its own. */
  const args = ['-u', 'cup.py', '--dir', CUP_DIR, cmd, '--game', gameAbs];
  if (cmd === 'draw') {
    const seed = String(opts.seed ?? '').trim();
    if (!/^\d{1,15}$/.test(seed)) return { ok: false, reason: 'the draw seed is a whole number' };
    args.push('--seed', seed);
  }
  /* --only is for the brief's gate 3 (one real `film --only A1`, driven from
   * here) and for going back to one fixture. No button sends it. */
  if (opts.only !== undefined && opts.only !== null && opts.only !== '') {
    const only = String(opts.only);
    if (cmd === 'draw' || !/^[A-Z0-9]{1,4}(-\d{1,2})?$/.test(only)) {
      return { ok: false, reason: `not a fixture id: ${only}` };
    }
    args.push('--only', only);
  }

  const win = BrowserWindow.fromWebContents(e.sender);
  const child = require('node:child_process').spawn(PYTHON, args,
    { cwd: path.join(REPO, 'tools'), windowsHide: true, env: childEnv() });
  const job = { kind: 'cup', cmd, child, cancelled: false, over: false, log: [], fixture: null };
  JOB = job;

  const take = (line, stream) => {
    if (!line.trim()) return;
    const p = cupLines.parseLine(line);
    /* once a second for minutes: progress, never log -- createShort's rule */
    if (p && p.stage) return jobSend(win, 'swb:cupProgress', p);
    job.log.push(line);
    if (job.log.length > 4000) job.log.splice(0, 1000);
    if (p) {
      if (p.kind === 'fixture') job.fixture = { id: p.id, file: p.file };
      else if (p.kind === 'fixtureDone' || p.kind === 'skip') job.fixture = null;
      jobSend(win, 'swb:cupProgress', p);
    }
    jobSend(win, 'swb:cupLog', { line, stream });
  };
  const outLines = cupLines.lineSplitter(), errLines = cupLines.lineSplitter();
  child.stdout.on('data', (d) => { for (const l of outLines.push(d)) take(l, 'out'); });
  child.stderr.on('data', (d) => { for (const l of errLines.push(d)) take(l, 'err'); });
  const flush = () => {
    for (const l of outLines.end()) take(l, 'out');
    for (const l of errLines.end()) take(l, 'err');
  };
  const finish = (payload) => {
    if (job.over) return;
    job.over = true;
    if (JOB === job) JOB = null;
    jobSend(win, 'swb:cupDone', { cmd, ...payload });
  };

  child.on('error', (err) => {
    flush();
    finish({ ok: false, reason: `could not start ${PYTHON}: ${err.message}` });
  });
  child.on('close', (code) => {
    flush();
    if (job.cancelled) {
      if (cmd === 'film') removeUnfilmed(job.fixture);
      return finish({ ok: false, cancelled: true });
    }
    if (code !== 0) {
      return finish({ ok: false, code,
                      reason: cupLines.failureText(job.log) || `cup.py exited ${code}` });
    }
    finish({ ok: true, last: job.log[job.log.length - 1] || '' });
  });

  return { ok: true, started: true, cmd };
});

ipcMain.handle('swb:cupCancel', async () => {
  if (!JOB || JOB.kind !== 'cup') return { ok: false, reason: 'the cup is not running' };
  JOB.cancelled = true;
  killTree(JOB.child);
  return { ok: true };
});

/* Closing the window ends a cup run instead of orphaning it. A Film all is
 * hours of browsers, and with the window gone there is nothing left to watch
 * them or cancel them; the run carries on from where it stopped when the
 * button is pressed again. */
app.on('before-quit', () => {
  if (JOB && JOB.kind === 'cup' && !JOB.over) {
    JOB.cancelled = true;
    killTree(JOB.child);
  }
});

/* THE ANNOUNCER. cinema_vo.py already speaks arbitrary text verbatim and
 * carries the two things that must not be reimplemented here: the SPOKEN
 * compound-splitting table (Kokoro says "Ironhail" as one mushy cluster; ten
 * relic names are corrected in it) and --parts/--gaps (punctuation does not
 * control timing in Kokoro, so a pause has to be real measured silence). So
 * this SHELLS OUT to it rather than reproducing any of that in JS.
 *
 * The audio comes back as base64 and is played by the page. The alternative
 * was serving the temp wav over the swb:// protocol, which means widening the
 * protocol handler to a directory outside the repo -- a general file-reading
 * capability, bought to avoid one base64 encode of a 100 KB file. */
let VOICE_CACHE = null;

ipcMain.handle('swb:voices', async () => {
  if (VOICE_CACHE) return VOICE_CACHE;
  const r = await runPython(['vo_voices.py'], { timeout: 20000 });
  if (!r.ok) return { ok: false, reason: lastLine(r.stderr) || `python exited ${r.code}` };
  try {
    const parsed = JSON.parse(r.stdout);
    if (parsed.ok) VOICE_CACHE = parsed;
    return parsed;
  } catch {
    return { ok: false, reason: 'vo_voices.py did not return JSON' };
  }
});

/* The default line IN THE BOX'S OWN SYNTAX, so "load default" cannot drift
 * from what --hook renders. Returns before cinema_vo imports Kokoro, so it is
 * a process spawn and not a model load. */
ipcMain.handle('swb:hookScript', async (_e, opts = {}) => {
  const a = String(opts.a || '').trim(), b = String(opts.b || '').trim();
  if (!(a && b)) return { ok: false, reason: 'no relics on screen' };
  const r = await runPython(['cinema_vo.py', '--a', a, '--b', b,
                             '--print-hook-script'], { timeout: 20000 });
  if (!r.ok) return { ok: false, reason: lastLine(r.stderr) || 'could not build the line' };
  return { ok: true, script: r.stdout.trim() };
});

ipcMain.handle('swb:speak', async (_e, opts = {}) => {
  const text = String(opts.text ?? '').trim();
  const voice = String(opts.voice || 'bm_lewis');
  /* EMPTY BOX MEANS THE DEFAULT LINE, NOT AN ERROR. The announcer's job is the
   * line the short already ships -- "<A>, <B>. Who wins?", each name placed on
   * its own ignition -- and the textarea is there to CHANGE it for a fight or
   * add something extra, not to be the only way to get a voice at all.
   *
   * `--hook` is the same flag shorts_build calls, so this preview is the line
   * the short will contain and not a second construction of it. The parts live
   * in cinema_vo.hook_parts and their onsets are read out of
   * src/render/open.js by cinema_vo.ignition_beats -- nowhere else, and never
   * copied into this file. */
  const hook = !text;
  const na = String(opts.a || '').trim(), nb = String(opts.b || '').trim();
  if (hook && !(na && nb)) {
    return { ok: false, reason: 'no relics on screen to name — start a fight first' };
  }
  if (text.length > 400) {
    return { ok: false, reason: `${text.length} characters is past the 400 this ` +
                                `preview will render. Shorten it, or raise the ` +
                                `limit deliberately.` };
  }
  /* A voice the model does not carry fails deep inside onnxruntime with a
   * message about an array shape. Checked here so it fails as a sentence. */
  if (!/^[a-z]{2}_[a-z]+$/.test(voice)) {
    return { ok: false, reason: `not a voice id: ${voice}` };
  }
  for (const f of ['kokoro-v1.0.onnx', 'voices-v1.0.bin']) {
    if (!fs.existsSync(path.join(REPO, 'tools', f))) {
      return { ok: false, reason: `missing tools/${f} — see tools/FETCH-KOKORO.md` };
    }
  }

  const out = path.join(os.tmpdir(), `swb-vo-${Date.now()}.wav`);
  /* `--script`, NOT `--text`. The box carries the line's TIMING now -- `|` for
   * a pause, `@T` for an absolute onset -- so loading the default line into it
   * and rendering gives back the same audio, verified byte-for-byte. With
   * --text it did not: the words survived and the measured silences did not,
   * and it came back as one flat continuous read. */
  const args = hook
    ? ['cinema_vo.py', '--a', na, '--b', nb, '--hook', '--voice', voice, '--out', out]
    : ['cinema_vo.py', '--a', na || 'A', '--b', nb || 'B',
       '--script', text, '--voice', voice, '--out', out];
  const r = await runPython(args, { timeout: 180000 });
  if (!r.ok || !fs.existsSync(out)) {
    if (r.timedOut) return { ok: false, reason: 'the voice render timed out' };
    const last = lastLine(r.stderr) || lastLine(r.stdout);
    return { ok: false, reason: last || `cinema_vo.py exited ${r.code}` };
  }
  let buf;
  try { buf = fs.readFileSync(out); } finally { try { fs.unlinkSync(out); } catch {} }
  return { ok: true, voice, hook, chars: text.length,
           line: hook ? `Who wins? ${na}, or ${nb}.` : text,
           seconds: wavSeconds(buf), wav: buf.toString('base64') };
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
