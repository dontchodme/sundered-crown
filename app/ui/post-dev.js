/* THE POST CHAIN CONTROLS. It drives the chain; it does not own one.
 *
 * This file used to build its own SWBPost instance and composite into an
 * overlay canvas stacked on the game. That was correct for exactly as long as
 * the chain was NOT in the build -- iterate in the app, then let the builder
 * put it in the chain (`docs/RENDERER-BRIEF.md` §5).
 *
 * tools/post_build.py has now put it in the chain. So the game composites its
 * own frames, and an overlay here would post-process an ALREADY
 * post-processed picture: two blooms, two grades, and an app showing something
 * the mp4 will never contain. That is the one fault docs/ARCHITECTURE.md §1
 * exists to prevent, and it would have arrived through the door marked "the
 * feature is finished".
 *
 * So there is exactly one chain, it lives in the build, and this is a remote
 * control for it. The A/B toggle is better for it too: OFF is now genuinely
 * the shipping renderer with the chain switched off, rather than a second code
 * path that resembles it.
 */
'use strict';

const POST = {
  fx: null,          // the game's POSTFX, through the AC export
  err: null,
};

function postBoot(gameWindow) {
  const AC = gameWindow.AC || {};
  if (!AC.POSTFX) {
    postFail('this build has no post chain -- run tools/post_build.py');
    return;
  }
  POST.fx = AC.POSTFX;

  /* THE TWO COPIES MUST BE THE SAME FILE. The shell loads src/render/post.js
     for the spread constants its pickers offer; the build has the same file
     inlined by post_build.py. If they ever drift the app offers settings the
     chain cannot honour -- so it is checked rather than trusted. */
  const mine = window.SWBPost && window.SWBPost.VERSION;
  const theirs = POST.fx.post && POST.fx.post.version;
  if (mine && theirs && mine !== theirs) {
    postFail('post.js version mismatch -- shell ' + mine + ', build ' + theirs
             + '. Re-run tools/post_build.py.');
    return;
  }

  postSync();
  postStatus((POST.fx.on ? 'ON' : 'OFF') + ' in the build · ' + theirs
             + ' · ' + passNames());
}

function passNames() {
  if (!POST.fx || !POST.fx.post) return 'no passes';
  const n = POST.fx.post.passes.map((p) => p.name);
  return n.length ? n.join(' + ') : 'no passes';
}

function postFail(why) {
  POST.err = why;
  for (const id of ['btnPost', 'btnPostTest', 'bloom', 'trails', 'grade']) {
    const el = document.getElementById(id);
    if (el) el.disabled = true;
  }
  postStatus('unavailable -- ' + why);
}

function postStatus(s) {
  const el = document.getElementById('postOut');
  if (el) el.textContent = s;
}

/* Push the three pickers into the ONE chain. The settings objects come from
   the shell's copy of the module and are plain data, so handing them across
   the frame boundary is safe -- and the version check in postBoot is what
   makes it safe rather than lucky. */
function postApply() {
  if (!POST.fx || !POST.fx.post) return;
  const S = window.SWBPost;
  const g = (id) => {
    const el = document.getElementById(id);
    return el ? el.value : 'off';
  };
  POST.fx.post.setBloom(g('bloom') === 'off' ? null : S.SPREAD[g('bloom')]);
  POST.fx.post.setTrails(g('trails') === 'off' ? null : S.TRAILS[g('trails')]);
  POST.fx.post.setGrade(g('grade') === 'off' ? null : S.GRADE[g('grade')]);
  POST.fx.reset();
  postStatus((POST.fx.on ? 'ON' : 'OFF') + ' · ' + passNames());
}

/* The pickers start where the BUILD starts, not where the markup does. What
   ships is SWBPost.SPREAD.DEFAULT and friends; if this file disagreed, the app
   would open showing a look nobody chose. */
function postSync() {
  const S = window.SWBPost;
  if (!S) return;
  const set = (id, v) => {
    const el = document.getElementById(id);
    if (el && [...el.options].some((o) => o.value === v)) el.value = v;
  };
  set('bloom', S.SPREAD.DEFAULT);
  set('trails', S.TRAILS.DEFAULT);
  set('grade', S.GRADE.DEFAULT);
  postButton();
}

function postButton() {
  const b = document.getElementById('btnPost');
  if (!b || !POST.fx) return;
  b.classList.toggle('pri', !!POST.fx.on);
  b.textContent = POST.fx.on ? 'Post chain: ON' : 'Post chain: OFF';
}

function postToggle(want) {
  if (!POST.fx) return;
  POST.fx.on = (want === undefined) ? !POST.fx.on : !!want;
  if (POST.fx.on) POST.fx.reset();
  postButton();
  postStatus(POST.fx.on
    ? 'ON · ' + passNames()
    : 'OFF -- the control. The shipping renderer, chain switched off.');
}

/* A fight's trail history belongs to that fight. */
function postReset() {
  if (POST.fx) POST.fx.reset();
}

/* THE CHECK. With no passes registered the chain must be invisible: the same
   bytes out as in. If it is not, the plumbing is bending the picture before
   anything has asked it to, and every comparison after that is between two
   unknowns rather than one change. */
function postSelfTest() {
  if (!POST.fx || !POST.fx.post) return;
  const btn = document.getElementById('btnPostTest');
  btn.disabled = true;
  postStatus('checking every pixel…');

  const w = document.getElementById('game').contentWindow;
  const AC = w.AC;
  const src = w.document.getElementById('cv');
  const wasOn = POST.fx.on;

  requestAnimationFrame(() => {
    let r;
    try {
      /* Everything off, and the WORLD pass left on #cv: selfTest compares the
         composite against the canvas it was handed, so that canvas has to be
         the chain's own input rather than a finished frame. */
      POST.fx.post.setBloom(null);
      POST.fx.post.setTrails(null);
      POST.fx.post.setGrade(null);
      POST.fx.on = false;
      AC.renderer.roMode = 1;
      AC.__draw(AC.match);
      AC.renderer.roMode = 0;
      r = POST.fx.post.selfTest(src, {
        enabled: true,
        rect: { x: AC.renderer.pad * AC.renderer.k,
                y: AC.renderer.arenaTop * AC.renderer.k,
                w: AC.renderer.aw * AC.renderer.k,
                h: AC.renderer.ah * AC.renderer.k },
      });
    } catch (e) {
      postStatus('self-test threw -- ' + (e.message || e));
      POST.fx.on = wasOn;
      postApply();
      btn.disabled = false;
      return;
    }
    POST.fx.on = wasOn;
    postApply();

    const head = r.passes !== 0
      ? 'SKIP  ' + r.passes + ' passes were still registered, so a zero here'
        + '\n      would mean nothing.'
      : r.differing === 0
        ? 'PASS  ' + r.total.toLocaleString() + ' px identical, max delta 0'
        : 'FAIL  ' + r.differing.toLocaleString() + ' of '
          + r.total.toLocaleString() + ' px differ, max delta ' + r.maxDelta;
    const tail = (r.sample && r.differing)
      ? '\nfirst at ' + r.sample.x + ',' + r.sample.y
        + '  got ' + r.sample.got.join(',') + '  want ' + r.sample.want.join(',')
      : '';
    postStatus(head + tail);
    btn.disabled = false;
  });
}

function postWire() {
  const b = document.getElementById('btnPost');
  const t = document.getElementById('btnPostTest');
  if (b) b.onclick = () => postToggle();
  if (t) t.onclick = postSelfTest;
  for (const id of ['bloom', 'trails', 'grade']) {
    const el = document.getElementById(id);
    if (el) el.onchange = postApply;
  }
}
