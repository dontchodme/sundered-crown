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
      /* The post chain reads the game's finished canvas and composites it
         into an overlay. It does not touch the engine, and OFF leaves the
         original pixels on screen because they were never written to.
         docs/RENDERER-BRIEF.md §5. */
      postBoot(w);
      postWire();
    } else if (++tries > 100) {
      clearInterval(wait);
      $('build').textContent = 'window.AC never appeared — engine did not boot';
    }
  }, 50);
}

/* The game page carries its own title, picker panel, log and the cinema demo
   panel. Inside the shell those are duplicated or in the way. Hiding them with
   a stylesheet from THIS side keeps the engine file untouched — Phase 1's rule.
 *
 * The sizing matters more than it looks. The game sets
 *   #stage { width: min(430px, 96vw); aspect-ratio: 9/16 }
 * plus 18px/44px body padding, which inside a narrow iframe overflows and puts
 * scrollbars on the arena. Rather than fight it for pixels, the stage is made
 * to BE the iframe: 100% x 100%, no padding, no scroll. The iframe already
 * carries aspect-ratio 1080/1920, which is the same 9:16, so proportions hold —
 * and the game's own ResizeObserver -> fitCanvas() -> renderer.resize() picks
 * up the new size, exactly as it does when a browser window is resized.
 *
 * #cinePanel is hidden WITHOUT !important on purpose: the rail's toggle flips
 * an inline style, and inline loses to !important. */
function hideGameChrome(w) {
  const st = w.document.createElement('style');
  st.textContent = `
    h1, .panel, #log { display: none !important; }
    #cinePanel { display: none; }
    html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; }
    body { display: block; min-height: 0; gap: 0; }
    #stage {
      width: 100%; height: 100%; margin: 0;
      aspect-ratio: auto; border: none; border-radius: 0; box-shadow: none;
    }`;
  w.document.head.appendChild(st);
}

/* The cinema panel is a real feature of the engine — director on/off, force a
   set-piece, A/B the same seed with the director off. It is hidden by default
   because it sits over the arena, not because it is junk. */
function toggleCinePanel() {
  const p = frame.contentWindow.document.getElementById('cinePanel');
  if (!p) return;
  const showing = p.style.display === 'block';
  p.style.display = showing ? 'none' : 'block';
  $('btnCine').classList.toggle('pri', !showing);
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
  postReset();          // the trail buffer belongs to the fight that filled it

  frame.contentWindow.AC.SFX.resume && frame.contentWindow.AC.SFX.resume();
}

function wireControls() {
  /* FIGHT IS ALWAYS A NEW FIGHT. It used to read the seed box and replay
   * whatever was in it -- which made it identical to Replay, because
   * `trackSeed` writes the live seed into that box four times a second. The
   * box is a READOUT of the fight on screen (and the thing worth copying out
   * of the app); it was never meant to be an instruction to repeat it.
   *
   * So the two buttons say what their labels always claimed: Fight rolls a
   * new seed on the same two relics, Replay runs the seed in the box again. */
  $('btnFight').onclick = () => startFight(undefined);

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

  /* ---- THE ANNOUNCER ------------------------------------------------------
   *
   * The line is rendered by cinema_vo.py in the main process and comes back as
   * base64 wav. Nothing about the text leaves this machine: Kokoro is local and
   * offline, which is why the card says so.
   *
   * WHAT IS MEASURED AND WHY. The intro card is dead (rule 1), so the 4.0s
   * ceiling the voiceover was written against is gone too -- and Rick chose the
   * START of the fight for the line, which has no hard ceiling at all. That
   * makes length a judgement rather than a limit, so this shows the SECONDS the
   * line actually renders to and marks it amber past the opening, instead of
   * refusing to render. `verify.py` caps ult tips at 72 characters and this
   * project has form for a hard cap, but a cap is a decision and it is his.
   *
   * The shipped hook is 2.99s ("Who wins? Paradox, or Heartwood."), which is
   * the number to compare against. */
  const SOFT_SECS = 6.0;   // roughly a quarter of a 23s clip
  const VO_MIX_GAIN = 2.0; // shorts_build.mix_graph's own `volume` term
  let voAudio = null, voCtx = null;

  const voSay = (msg, cls) => {
    const el = $('voStub');
    el.hidden = !msg;
    el.textContent = msg || '';
    el.className = cls || 'stub';
  };

  const stopVo = () => {
    if (voAudio) { voAudio.pause(); voAudio.src = ''; voAudio = null; }
    $('btnStop').hidden = true;
  };

  (async () => {
    /* Populated from the voices file itself, not from a list typed in here --
     * a hardcoded picker drifts from the model the moment either changes. */
    const sel = $('voVoice');
    const r = await window.swb.voices();
    if (!r.ok) { sel.innerHTML = '<option>bm_lewis</option>'; voSay(r.reason); return; }
    const groups = {};
    for (const v of r.voices) (groups[v.group] ||= []).push(v.id);
    sel.innerHTML = Object.entries(groups).map(([g, ids]) =>
      `<optgroup label="${g}">` +
      ids.map((id) => `<option value="${id}"${id === r.default ? ' selected' : ''}>` +
                      `${id}${id === r.default ? ' — voice of record' : ''}</option>`).join('') +
      '</optgroup>').join('');
  })();

  /* Relic id is not its display name -- `oathwound` shows as 'Goreshard'.
   * Read off the build, the same rule shorts_build.display_names follows. */
  const displayName = (id) => {
    const w = frame.contentWindow?.AC?.WEAPONS?.find((x) => x.id === id);
    return w ? w.name : id;
  };

  $('btnLoadDefault').onclick = async () => {
    /* Fetched, not rebuilt here. cinema_vo owns the line and its gaps; a second
     * construction in the UI is how "load default" ends up loading something
     * that is not the default. */
    const r = await window.swb.hookScript({ a: displayName($('selA').value),
                                            b: displayName($('selB').value) });
    if (!r.ok) { voSay(r.reason); return; }
    $('vo').value = r.script;
    voSay('Loaded. The `|0.38` marks are the pauses — edit the words, move the '
        + 'bars, change the numbers. Rendered as-is this is the same audio the '
        + 'short ships, to the byte.');
  };

  $('btnStop').onclick = stopVo;

  $('btnPreview').onclick = async () => {
    stopVo();
    const btn = $('btnPreview');
    /* EMPTY IS NOT AN ERROR -- it is the default line for the two relics on
     * screen, which is what the short ships with. */
    const text = $('vo').value.trim();
    btn.disabled = true;
    btn.textContent = 'Rendering…';
    $('voMeter').textContent = '';
    try {
      const r = await window.swb.speak({ text, voice: $('voVoice').value,
                                         a: displayName($('selA').value),
                                         b: displayName($('selB').value) });
      if (!r.ok) { voSay(r.reason); return; }
      voSay('');
      const secs = r.seconds;
      const over = secs !== null && secs > SOFT_SECS;
      $('voMeter').className = over ? 'note over' : 'note ok';
      /* The default renders as separate parts joined by measured silence; a
       * typed line is one continuous read. Same words, different length -- so
       * the readout says WHICH it just played rather than leaving the seconds
       * looking inconsistent between two presses of the same button. */
      $('voMeter').textContent =
        `${secs === null ? '?' : secs.toFixed(2)}s · ${r.voice} · ` +
        (r.hook ? 'default line, as the short ships it'
                : `your line, ${r.chars} chars`) +
        (over ? ` — past ${SOFT_SECS}s, it will run well into the fight` : '');
      /* PLAYED AT THE LEVEL IT HAS IN A SHORT, NOT AT THE LEVEL OF THE FILE.
       *
       * The wav this returns is byte-identical to the one shorts_build feeds
       * the mix -- verified by sha256 against 07-shorts/v44's hook wav. But
       * the FILE is -21.5 LUFS, and in a short it goes through `volume=2.0`
       * and then sits in a mix normalised to -14 as a whole. Playing the file
       * raw is about 6dB down on what the short sounds like, which is why the
       * default line "didn't sound the same" when the audio was in fact the
       * same bytes.
       *
       * 2.0 is not a number invented here: it is the exact `volume` term from
       * shorts_build.mix_graph. An <audio> element cannot go above 1.0, so the
       * gain is applied through Web Audio and the element is left alone. The
       * FILE is never modified -- it is the mix's input and boosting it here
       * would double-apply on the next render. */
      voAudio = new Audio('data:audio/wav;base64,' + r.wav);
      voAudio.onended = stopVo;
      try {
        voCtx ||= new AudioContext();
        if (voCtx.state === 'suspended') await voCtx.resume();
        const src = voCtx.createMediaElementSource(voAudio);
        const gain = voCtx.createGain();
        gain.gain.value = VO_MIX_GAIN;
        src.connect(gain).connect(voCtx.destination);
      } catch (e) {
        /* If Web Audio is unavailable the line still plays, just quiet. Said
         * out loud rather than silently sounding wrong. */
        voSay('playing at file level — Web Audio unavailable: ' + (e.message || e));
      }
      $('btnStop').hidden = false;
      await voAudio.play();
    } catch (e) {
      voSay(String(e && e.message || e));
    } finally {
      btn.disabled = false;
      btn.textContent = 'Preview voice';
    }
  };

  /* ---- CREATE SHORT -------------------------------------------------------
   * The job runs in the main process and PUSHES. Nothing here polls: a capture
   * says something once a second and a second clock in the UI would only be a
   * thing to keep in step with the first. */
  let shortRunning = false;
  const shSay = (t) => { $('shProg').textContent = t || '\u00a0'; };
  const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

  window.swb.onShortProgress((d) => {
    if (d.stage === 'capture') {
      /* FRAMES AND ELAPSED, NOT A PERCENTAGE. The capture runs until the match
       * ends, so the denominator is genuinely unknown -- a bar here would be
       * invented, which is the thing this card is not allowed to be. */
      shSay(`capturing — ${d.frames.toLocaleString()} frames · ${mmss(d.elapsed)}`);
    }
  });

  window.swb.onShortLog((d) => {
    const el = $('shLog');
    el.hidden = false;
    el.textContent += d.line + '\n';
    el.scrollTop = el.scrollHeight;
    if (/^\[\d\/3\]/.test(d.line)) shSay(d.line);
  });

  window.swb.onShortDone((d) => {
    shortRunning = false;
    $('btnShort').disabled = false;
    $('btnCancelShort').hidden = true;
    if (d.cancelled) { shSay('cancelled'); return; }
    if (!d.ok) { shSay(''); alertInto('btnShort', d.reason); return; }
    shSay(`done — ${d.seconds}s`);
    $('btnReveal').hidden = false;
    $('btnReveal').onclick = () => window.swb.revealFile(d.file);
    const grid = $('shFrames');
    grid.hidden = false;
    grid.innerHTML = (d.frames || []).map((f) =>
      `<img src="data:image/jpeg;base64,${f.jpg}" title="${f.t.toFixed(1)}s">`).join('');
  });

  $('shWhole').onchange = () => {
    const whole = $('shWhole').checked;
    $('shLead').disabled = whole;
    $('shLeadRow').style.opacity = whole ? 0.45 : 1;
  };
  $('shWhole').onchange();

  $('btnCancelShort').onclick = () => window.swb.cancelShort();

  $('btnShort').onclick = async () => {
    if (shortRunning) return;
    $('shLog').textContent = '';
    $('shFrames').hidden = true;
    $('btnReveal').hidden = true;
    shSay('starting…');
    const r = await window.swb.createShort({
      a: $('selA').value, b: $('selB').value,
      seed: Number($('seed').value) >>> 0,
      /* EMPTY LEAD MEANS THE WHOLE FIGHT. shorts_build passes --full when no
       * --lead is given, and --full is what start=0 comes from. */
      lead: $('shWhole').checked ? null : (Number($('shLead').value) || 18),
      vo: $('vo').value, voice: $('voVoice').value,
    });
    if (r.ok) {
      shortRunning = true;
      $('btnShort').disabled = true;
      $('btnCancelShort').hidden = false;
      return;
    }
    shSay('');
    if (!r.ok) alertInto('btnShort', r.reason);
  };

  $('btnCine').onclick = toggleCinePanel;
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
