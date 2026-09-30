/* Falsify app/cuplines.js without Electron:
 *
 *     node app/test_cuplines.js
 *
 * Each case is where the obvious implementation breaks: a middle dot written
 * in cp1252, a character cut in half between two reads, a Windows line
 * ending, the closing tally that looks like a fixture, a refusal whose last
 * line is the override rather than the reason.
 */
'use strict';
const L = require('./cuplines');

let fails = 0;
const check = (ok, what) => {
  console.log((ok ? '  ok   ' : '  FAIL ') + what);
  if (!ok) fails++;
};
const DOT = '\u00b7';

console.log('decode');
check(L.decodeLine(Buffer.from([0x41, 0x20, 0xb7, 0x20, 0x4d])) === `A ${DOT} M`,
      'a cp1252 middle dot (0xB7 alone) reads as a middle dot, not U+FFFD');
check(L.decodeLine(Buffer.from(`A ${DOT} M`, 'utf8')) === `A ${DOT} M`,
      'a UTF-8 middle dot (C2 B7) reads as one middle dot, not "Â·"');
check(L.decodeLine(Buffer.from([0x97])) === '\u2014',
      'cp1252 0x97 is an em dash, not the C1 control Latin-1 would make it');
check(L.decodeLine(Buffer.from('[cup] done 3/33')) === '[cup] done 3/33', 'ASCII is ASCII');

console.log('split');
{
  const s = L.lineSplitter();
  const whole = Buffer.from(`[cup] band: GROUP A ${DOT} MATCH 3 OF 3 / WINNER TAKES THE GROUP\r\n`, 'utf8');
  const cut = whole.indexOf(0xc2) + 1;           // between the dot's two bytes
  const got = [...s.push(whole.subarray(0, cut)), ...s.push(whole.subarray(cut))];
  check(got.length === 1 && got[0] === `[cup] band: GROUP A ${DOT} MATCH 3 OF 3 / WINNER TAKES THE GROUP`,
        'a line cut inside a character comes out whole, and without its CR');
}
{
  const s = L.lineSplitter();
  const got = s.push(Buffer.from('one\ntwo\nthr'));
  check(got.length === 2 && got[1] === 'two', 'two lines out of a chunk that ends mid-line');
  check(s.push(Buffer.from('ee')).length === 0, 'nothing more until the newline arrives');
  const end = s.end();
  check(end.length === 1 && end[0] === 'three', 'the unterminated last line is handed back at the end');
  check(s.end().length === 0, 'and only once');
}

console.log('parse');
{
  const f = L.parseLine('[cup] 12/65 A3 thornshear v vesper seed 1606666929 -> '
    + '02-groups\\A\\13 - A3 - Thornshear vs Vesper\\13 - A3 - Thornshear vs Vesper.mp4');
  check(f && f.kind === 'fixture' && f.i === 12 && f.total === 65 && f.id === 'A3'
        && f.a === 'thornshear' && f.b === 'vesper' && f.seed === 1606666929
        && f.file === '02-groups\\A\\13 - A3 - Thornshear vs Vesper\\13 - A3 - Thornshear vs Vesper.mp4',
        'a fixture line: counter, id, both sides, seed, and the file after " -> "');
  const k = L.parseLine('[cup] 58/65 R16-1 oathwound v gloamwire seed 42 -> 03-round-of-16\\x.mp4');
  check(k && k.id === 'R16-1' && k.a === 'oathwound', 'a knockout id with a dash');
  const sk = L.parseLine('[cup] 4/33 A3 already filmed: 02-groups\\A\\x\\x.mp4');
  check(sk && sk.kind === 'skip' && sk.i === 4 && sk.id === 'A3', 'a fixture already filmed');
  const b = L.parseLine(`[cup] band: GROUP F ${DOT} MATCH 2 OF 3 / LOSE AND VESPER IS OUT`);
  check(b && b.kind === 'band' && b.text === `GROUP F ${DOT} MATCH 2 OF 3 / LOSE AND VESPER IS OUT`,
        'the band line, copy intact');
  const d = L.parseLine('[cup] done 12/65');
  check(d && d.kind === 'fixtureDone' && d.i === 12 && d.total === 65, 'a fixture done');
  const p = L.parseLine('[progress] capture frames=2140 elapsed=38.0');
  check(p && p.stage === 'capture' && p.frames === 2140 && p.elapsed === 38,
        "shorts_build's [progress], the same shape createShort sends");
  check(L.parseLine('[cup] 31/65 filmed - schedule: C:\\dev\\x\\SCHEDULE.md') === null,
        'the closing tally is log, not a fixture');
  check(L.parseLine('[2/3] encode   3512 frames (58.5s) -> 1080x1920') === null,
        "shorts_build's stage lines are log (the panel reads them there)");
  check(L.parseLine('  A1     Thornshear v Vesper  seed 1606666929 k=0 -> Thornshear') === null,
        "a seeds line is log: the brief parses [cup] and [progress] only");
}

console.log('failure');
{
  const refusal = ['[cup] 1/33 A1 ...', "! not the tournament's runtime (docs/RUNTIME-DRIFT.md):",
                   '    build differs: ledger 3f9a2c11d0e4, this file 77c1aa0b93f2',
                   '  --force to override; the ledger will say so.'];
  const t = L.failureText(refusal);
  check(t.startsWith("! not the tournament's runtime") && t.includes('build differs'),
        'a multi-line refusal keeps the line that names the failed check');
  check(L.failureText(['ok', 'Traceback (most recent call last):', 'ValueError: bad'])
        === 'ValueError: bad', 'no "!" line: the last line');
  check(L.failureText(['    FAIL  under 180s', '! A3 failed (exit 1); fix it and run `cup.py film` again', ''])
        .startsWith('! A3 failed'), 'a failed film: cup.py\'s own line, blank lines ignored');
}

console.log(`\n${fails ? fails + ' FAILED' : 'ALL OK'}`);
process.exit(fails ? 1 : 0);
