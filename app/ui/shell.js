/* The app shell. It DRIVES the game; it does not modify it.
 *
 * Same-origin (both served from swb://app) is what makes this possible: the
 * shell reaches window.AC inside the frame and calls the same functions the
 * game's own buttons call. No injection into the engine, no fork of it.
 */
'use strict';

const $ = (id) => document.getElementById(id);
const frame = $('game');

let AC = null;   // the game's export surface, once it exists

/* ---------------------------------------------------------------- boot ---- */

async function boot() {
  const game = await window.swb.gamePath();
  $('build').textContent = game;
  frame.src = 'swb://app/' + game;
  frame.addEventListener('load', onGameLoad, { once: true });
}

function onGameLoad() {
  const w = frame.contentWindow;

  /* The game builds its roster and starts a match at the bottom of its own
     script, so AC exists by load. Poll anyway rather than assume — a silent
     null here would surface later as an unrelated-looking error. */
  let tries = 0;
  const wait = setInterval(() => {
    if (w.AC && w.AC.WEAPONS) {
      clearInterval(wait);
      AC = w.AC;
      hideGameChrome(w);
      fillRoster();
      wireControls();
      trackSeed(w);
    } else if (++tries > 100) {
      clearInterval(wait);
      $('build').textContent = 'window.AC never appeared — engine did not boot';
    }
  }, 50);
}

/* The game page carries its own title, picker panel and log. Inside the shell
   those are duplicated. Hiding them with a stylesheet from THIS side keeps the
   engine file untouched, which is Phase 1's rule. */
function hideGameChrome(w) {
  const st = w.document.createElement('style');
  st.textContent = `h1,.panel,#log{display:none!important}
    body{margin:0;display:grid;place-items:center;min-height:100vh}
    #stage{margin:0}`;
  w.document.head.appendChild(st);
}

function fillRoster() {
  for (const sel of [$('selA'), $('selB')]) {
    sel.innerHTML = '';
    for (const wpn of AC.WEAPONS) {
      const o = document.createElement('option');
      o.value = wpn.id;
      o.textContent = wpn.name;
      sel.appendChild(o);
    }
  }
  $('selA').selectedIndex = 0;
  $('selB').selectedIndex = Math.min(1, AC.WEAPONS.length - 1);
}

/* The seed of the fight on screen, kept live. This is the one number worth
   copying out of the app: it is the whole of a fight, and it is what the
   render pipeline takes. */
function trackSeed(w) {
  setInterval(() => {
    if (document.activeElement === $('seed')) return;   // don't fight the typist
    if (w.__lastSeed !== undefined) $('seed').value = String(w.__lastSeed);
  }, 250);
}

/* ------------------------------------------------------------ controls ---- */

function startFight(seed) {
  const a = $('selA').value, b = $('selB').value;
  AC.newMatch(a, b, seed);
  frame.contentWindow.AC.SFX.resume && frame.contentWindow.AC.SFX.resume();
}

function wireControls() {
  $('btnFight').onclick = () => {
    const raw = $('seed').value.trim();
    startFight(raw === '' ? undefined : (Number(raw) >>> 0));
  };

  $('btnReplay').onclick = () => {
    const raw = $('seed').value.trim();
    if (raw === '') return;
    startFight(Number(raw) >>> 0);
  };

  $('btnRandom').onclick = () => {
    const n = AC.WEAPONS.length;
    let i = Math.floor(Math.random() * n), j = Math.floor(Math.random() * n);
    if (i === j) j = (j + 1) % n;
    $('selA').selectedIndex = i;
    $('selB').selectedIndex = j;
    $('seed').value = '';
    startFight(undefined);
  };

  $('btnCopySeed').onclick = () => navigator.clipboard.writeText($('seed').value);

  $('btnPreview').onclick = async () => {
    const r = await window.swb.speak({ text: $('vo').value });
    if (!r.ok) $('voStub').textContent = r.reason;
  };

  $('btnShort').onclick = async () => {
    const r = await window.swb.createShort({
      a: $('selA').value, b: $('selB').value,
      seed: Number($('seed').value) >>> 0,
      vo: $('vo').value,
    });
    if (!r.ok) alertInto('btnShort', r.reason);
  };

  $('btnIdentity').onclick = runIdentity;
}

function alertInto(id, msg) {
  const b = $(id);
  const was = b.textContent;
  b.textContent = msg;
  setTimeout(() => { b.textContent = was; }, 2600);
}

/* ------------------------------------------------- the Phase 1 test ------- */
/* Not "does it open" — does it run the SAME ENGINE headless Chromium runs.
 * Writes results to out/shell_identity_app.json; tools/shell_identity.py runs
 * the same seeds under Playwright and diffs. See docs/ARCHITECTURE.md §3.
 */
async function runIdentity() {
  const out = $('identityOut');
  const btn = $('btnIdentity');
  btn.disabled = true;
  out.className = '';
  out.textContent = 'running 200 fights…';

  await new Promise(r => setTimeout(r, 30));   // let the paint land

  const ids = AC.WEAPONS.map(w => w.id);
  const rows = [];
  const t0 = performance.now();
  for (let i = 0; i < 200; i++) {
    const a = ids[i % ids.length];
    const b = ids[(i * 7 + 3) % ids.length];
    if (a === b) continue;
    const seed = (i * 2654435761 + 12345) >>> 0;
    rows.push({ a, b, seed, r: AC.simulate(a, b, seed) });
  }
  const secs = (performance.now() - t0) / 1000;

  const path = await window.swb.writeIdentity({
    build: $('build').textContent,
    ua: navigator.userAgent,
    chrome: (navigator.userAgent.match(/Chrome\/([\d.]+)/) || [])[1] || '?',
    rows,
  });

  out.textContent =
    `${rows.length} fights in ${secs.toFixed(1)}s  (${(rows.length / secs).toFixed(0)}/s)\n` +
    `Chromium ${(navigator.userAgent.match(/Chrome\/([\d.]+)/) || [])[1]}\n\n` +
    `wrote ${path}\n\nNow run:\n  cd tools\n  python3 shell_identity.py`;
  btn.disabled = false;
}

boot();
