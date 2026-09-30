// Real cup.py output through app/cuplines.js, as main.js feeds it.
// Run twice: Python writing cp1252 (no PYTHONIOENCODING, like an app launched
// from a shortcut) and Python writing UTF-8 (a shell that sets it).
'use strict';
const { spawn } = require('node:child_process');
const path = require('node:path');
const L = require('C:/dev/sundered-crown/app/cuplines.js');

const PY = process.env.LOCALAPPDATA + '\\Programs\\Python\\Python313\\python.exe';
const TOOLS = 'C:\\dev\\sundered-crown\\tools';
const args = ['-u', 'cup.py', '--dir', 'C:\\dev\\sundered-crown\\07-shorts\\_cuptest', 'film',
              '--game', 'C:\\dev\\sundered-crown\\02-chain\\sc-tendril-fx.html', '--dry-run'];

function run(label, envPatch) {
  return new Promise((resolve) => {
    const env = { ...process.env };
    delete env.PYTHONIOENCODING;
    Object.assign(env, envPatch);
    const child = spawn(PY, args, { cwd: TOOLS, windowsHide: true, env });
    const out = L.lineSplitter(), err = L.lineSplitter();
    const lines = [], raw = [];
    child.stdout.on('data', (d) => { raw.push(d); lines.push(...out.push(d)); });
    child.stderr.on('data', (d) => lines.push(...err.push(d)));
    child.on('close', (code) => {
      lines.push(...out.end(), ...err.end());
      resolve({ label, code, lines, raw: Buffer.concat(raw) });
    });
  });
}

(async () => {
  let fails = 0;
  const check = (ok, what) => { console.log((ok ? '  ok   ' : '  FAIL ') + what); if (!ok) fails++; };
  const results = [];
  for (const [label, patch] of [['cp1252 pipe', {}], ['utf-8 pipe', { PYTHONIOENCODING: 'utf-8' }]]) {
    const r = await run(label, patch);
    results.push(r);
    const ev = r.lines.map(L.parseLine);
    const fx = ev.filter((e) => e && e.kind === 'fixture');
    const bands = ev.filter((e) => e && e.kind === 'band');
    console.log(`${label}: exit ${r.code}, ${r.lines.length} lines, ${fx.length} fixtures, ${bands.length} bands`);
    check(r.code === 0, `${label}: cup.py exited 0`);
    check(fx.length === 33 && fx[0].id === 'PI' && fx[1].id === 'A1' && fx[32].id === 'F',
          `${label}: 33 fixture events in posting order, PI first, F last`);
    check(fx.every((f, i) => f.i === i + 1 && f.total === 33 && /\.mp4$/.test(f.file)),
          `${label}: every counter i/33 and a file ending .mp4`);
    const groupBands = bands.filter((b) => b.text.startsWith('GROUP '));
    check(groupBands.length === 24 && groupBands.every((b) => b.text.includes('GROUP ') && b.text.includes(' \u00b7 MATCH ')),
          `${label}: all 24 group bands carry a real middle dot`);
    check(!r.lines.some((l) => l.includes('\ufffd')), `${label}: no U+FFFD on any line`);
    check(ev.filter((e) => e && e.kind === 'fixtureDone').length === 0,
          `${label}: a dry run prints no "done" lines (it continues before them)`);
  }
  check(JSON.stringify(results[0].lines) === JSON.stringify(results[1].lines),
        'both encodings decode to the same lines');
  // the control that can come back wrong: the naive decode of the cp1252 bytes
  const naive = results[0].raw.toString('utf8');
  check(naive.includes('\ufffd') && results[0].raw.includes(0xb7),
        'control: the cp1252 run really sent 0xB7, and a plain UTF-8 read turns it into U+FFFD');
  console.log(`\n${fails ? fails + ' FAILED' : 'ALL OK'}`);
  process.exit(fails ? 1 : 0);
})();
