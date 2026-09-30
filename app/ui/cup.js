/* THE CROWN CUP PANEL. 06-docs/v115/CROWN-CUP-APP-BRIEF-v115.md.
 *
 * The tournament is tools/cup.py's -- the draw, the seed rule, the band copy,
 * the folders, the freeze -- and this panel presses three of its commands and
 * shows what it says. Its own file, because it needs nothing from the game
 * frame: a cup run films off GAME in its own browsers, and the ledger is the
 * whole state, read back from disk after every run and every fixture.
 *
 * TWO BARS, AND ONLY THE OUTER ONE KNOWS ITS DENOMINATOR. The outer is
 * fixture i of n, which cup.py counts. The inner is that fixture's own
 * pipeline in shorts_build's three stages (capture, encode, mix, a third
 * each), and inside the capture a COUNT of frames and never a percentage:
 * the capture runs until the match ends, and cinema_clip.py says at its
 * [progress] line why a denominator there would be invented.
 */
(() => {
  'use strict';
  const $c = (id) => document.getElementById(id);
  if (!window.swb || !window.swb.cupLedger || !$c('cupCard')) return;

  const LOG_KEEP = 400;      // lines the panel keeps; a Film all prints thousands
  const VERB = { draw: 'drawing', seeds: 'seeding', film: 'filming' };
  let state = null;          // the last cupLedger() answer
  let running = null;        // the command the main process is running

  const say = (id, t) => { $c(id).textContent = t || ' '; };
  const note = (id, t) => { const el = $c(id); el.hidden = !t; el.textContent = t || ''; };
  const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  const bar = (which, frac) => {
    $c('cupBar' + which).hidden = frac === null;
    if (frac !== null) {
      $c('cupFill' + which).style.width = `${(Math.max(0, Math.min(1, frac)) * 100).toFixed(1)}%`;
    }
  };
  /* A refusal is said on the button that was pressed, as the short card does. */
  const flash = (id, msg) => {
    const b = $c(id), was = b.textContent;
    b.textContent = msg;
    setTimeout(() => { b.textContent = was; }, 2600);
  };
  /* Relic ids are not display names -- `oathwound` shows as Goreshard -- and
   * the ledger carries the roster it was drawn from, so names come from there. */
  const name = (id) => (state && state.ledger && state.ledger.roster
                        && state.ledger.roster[id] && state.ledger.roster[id].name) || id;

  function counts(L) {
    const F = L.fixtures || [];
    return {
      total: F.length,
      seeded: F.filter((f) => f.result).length,
      filmed: F.filter((f) => f.file).length,     // what `cup.py status` counts
      failed: F.filter((f) => f.film_error).map((f) => f.id),
    };
  }

  function render() {
    const s = state || {};
    const L = s.ledger;
    const c = L ? counts(L) : null;
    const busy = !!running;

    if (L) {
      say('cupStatus', `ledger: ${c.total} fixtures · ${c.seeded} seeded · ${c.filmed} filmed`);
      const b = L.build || {};
      note('cupBuild', `draw seed ${L.draw_seed} · ${b.path || '?'} ${String(b.sha256 || '').slice(0, 12)}`
                       + ` · ${L.machine || '?'} · Chromium ${L.chromium || '?'}`);
    } else {
      say('cupStatus', s.none ? `no ledger in ${s.dir} — nothing drawn yet`
                              : (s.reason || 'reading the ledger…'));
      note('cupBuild', '');
    }

    /* Draw only while there is no ledger (a draw is a commitment); Seed all
     * once drawn and until every fixture has its fight; Film all once they
     * all have. cup.py would refuse the rest itself -- this only stops the
     * buttons offering what it will refuse. */
    $c('cupSeed').disabled = busy || !s.none;
    $c('btnCupDraw').disabled = busy || !s.none;
    $c('btnCupSeeds').disabled = busy || !L || c.seeded === c.total;
    $c('btnCupFilm').disabled = busy || !L || c.seeded < c.total;
    $c('btnCupCancel').hidden = !busy;
    $c('btnCupOpen').disabled = !L;

    /* A FAILED FILM IS SAID EVERY TIME THE LEDGER IS READ, not once. cup.py
     * resumes by skipping any fixture whose mp4 exists, and shorts_build
     * writes the mp4 before it measures it -- so a delivery that failed its
     * marks is on disk, and the next Film all passes over it as filmed. */
    note('cupFailed', c && c.failed.length
      ? `${c.failed.join(', ')}: the last film failed (the log says why), and the mp4 it `
        + 'wrote is still there. Film all skips a fixture whose mp4 exists, so it will not '
        + 'film this again: delete that mp4 first, or re-film it from a terminal with '
        + '--only and --redo.'
      : '');
  }

  async function refresh() {
    try { state = await window.swb.cupLedger(); } catch (e) {
      state = { reason: String((e && e.message) || e) };
    }
    if (state.running && !running) running = state.running;   // a reload mid-run
    render();
  }

  async function start(opts, button) {
    if (running) return;
    $c('cupLog').textContent = '';
    $c('cupLog').hidden = true;
    note('cupWarn', '');
    note('cupBand', '');
    bar('Outer', null);
    bar('Inner', null);
    say('cupOuter', `${VERB[opts.cmd]}…`);
    say('cupInner', '');
    const r = await window.swb.cupRun(opts);
    if (!r.ok) { say('cupOuter', ''); flash(button, r.reason); return; }
    running = opts.cmd;
    render();
  }

  $c('btnCupDraw').onclick = async () => {
    const seed = $c('cupSeed').value.trim();
    if (!/^\d{1,15}$/.test(seed)) { flash('btnCupDraw', 'a whole number'); return; }
    const game = await window.swb.gamePath();
    const w = $c('game') && $c('game').contentWindow;
    const n = w && w.AC && w.AC.WEAPONS ? w.AC.WEAPONS.length : null;
    const ok = window.confirm(
      `Draw the Crown Cup from ${game}${n ? ` (${n} relics)` : ''} with draw seed ${seed}?\n\n`
      + 'A draw is a commitment. The app will not redraw it -- a redraw is terminal-only, '
      + 'with --force -- and the plan publishes the draw seed, the seed rule and the build '
      + 'hash before anything is seeded.');
    if (ok) start({ cmd: 'draw', seed }, 'btnCupDraw');
  };
  $c('btnCupSeeds').onclick = () => start({ cmd: 'seeds' }, 'btnCupSeeds');
  $c('btnCupFilm').onclick = () => start({ cmd: 'film' }, 'btnCupFilm');
  $c('btnCupCancel').onclick = () => window.swb.cupCancel();
  $c('btnCupOpen').onclick = () => {
    if (state && state.dir) {
      window.swb.revealFile(`${state.dir}/${state.schedule ? 'SCHEDULE.md' : 'ledger.json'}`);
    }
  };

  window.swb.onCupProgress((d) => {
    if (d.stage === 'capture') {
      say('cupInner', `capture — ${d.frames.toLocaleString()} frames · ${mmss(d.elapsed)}`);
    } else if (d.kind === 'fixture') {
      bar('Outer', (d.i - 1) / d.total);
      say('cupOuter', `${d.i}/${d.total}  ${d.id}  ${name(d.a)} v ${name(d.b)}`);
      bar('Inner', 0);
      say('cupInner', 'starting…');
      note('cupBand', '');
    } else if (d.kind === 'skip') {
      bar('Outer', d.i / d.total);
      say('cupOuter', `${d.i}/${d.total}  ${d.id}  already filmed`);
    } else if (d.kind === 'band') {
      note('cupBand', d.text);
    } else if (d.kind === 'fixtureDone') {
      bar('Outer', d.i / d.total);
      bar('Inner', 1);
      say('cupInner', 'delivered');
      refresh();
    }
  });

  window.swb.onCupLog((d) => {
    const el = $c('cupLog');
    el.hidden = false;
    el.textContent += d.line + '\n';
    const lines = el.textContent.split('\n');
    if (lines.length > LOG_KEEP + 1) el.textContent = lines.slice(-LOG_KEEP - 1).join('\n');
    el.scrollTop = el.scrollHeight;
    /* shorts_build's own stage lines: [1/3] capture, [2/3] encode, [3/3] mix.
     * The short card reads the same lines for its status. */
    const m = /^\[(\d)\/3\]\s+(.*)$/.exec(d.line);
    if (m) {
      bar('Inner', Number(m[1]) / 3);
      if (m[1] !== '1') say('cupInner', m[2].replace(/\s+/g, ' '));
    }
  });

  window.swb.onCupDone((d) => {
    running = null;
    note('cupBand', '');
    bar('Inner', null);
    say('cupInner', '');
    if (d.cancelled) {
      say('cupOuter', `cancelled — press ${d.cmd === 'film' ? 'Film all' : 'it'} again to carry on`);
    } else if (!d.ok) {
      say('cupOuter', `${d.cmd} stopped`);
      note('cupWarn', d.reason);
    } else {
      if (d.cmd === 'film') bar('Outer', 1); else bar('Outer', null);
      say('cupOuter', `${d.cmd} done — ${String(d.last || '').replace(/^\[cup\]\s*/, '').trim()}`);
    }
    refresh();
  });

  refresh();
})();
