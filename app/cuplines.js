/* The lines a Crown Cup run prints, read in the main process (main.js,
 * swb:cupRun). Its own file because main.js cannot load without Electron and
 * this has to be testable without it:  node app/test_cuplines.js
 *
 * BYTES FIRST, THEN TEXT. Python writes a pipe in the machine's ANSI code page
 * unless something tells it otherwise -- cp1252 on these machines -- and
 * cup.py's band copy puts a middle dot in every group line ("GROUP A · MATCH
 * 3 OF 3"). Read as UTF-8, that dot arrives as U+FFFD, on the one line in the
 * panel Rick reads in order to veto the copy. A shell that sets
 * PYTHONIOENCODING=utf-8 sends UTF-8 instead, so neither can be assumed. Each
 * LINE is tried as UTF-8 and read as cp1252 only if it is not valid UTF-8
 * (ASCII always is, so the common line costs nothing), and lines are cut on
 * the byte 0x0A before anything is decoded, so a character that straddles
 * two reads is never decoded in halves.
 */
'use strict';

const UTF8 = new TextDecoder('utf-8', { fatal: true });

/* cp1252 at 0x80-0x9F. Everywhere else in the page it is Latin-1 and each
 * byte is its own code point. U+FFFD for the five bytes cp1252 leaves out. */
const CP1252_80 =
  '€�‚ƒ„…†‡ˆ‰Š‹Œ�Ž�' +
  '�‘’“”•–—˜™š›œ�žŸ';

function decodeLine(buf) {
  try { return UTF8.decode(buf); } catch {}
  let s = '';
  for (const c of buf) {
    s += (c >= 0x80 && c < 0xa0) ? CP1252_80[c - 0x80] : String.fromCharCode(c);
  }
  return s;
}

/* One per stream. push(chunk) returns the complete lines the chunk finished;
 * end() returns what was left with no newline after it. */
function lineSplitter() {
  let rest = Buffer.alloc(0);
  const text = (b) => decodeLine(b).replace(/\r$/, '');
  return {
    push(chunk) {
      const buf = rest.length ? Buffer.concat([rest, chunk]) : chunk;
      const lines = [];
      let start = 0, nl;
      while ((nl = buf.indexOf(0x0a, start)) !== -1) {
        lines.push(text(buf.subarray(start, nl)));
        start = nl + 1;
      }
      rest = Buffer.from(buf.subarray(start));
      return lines;
    },
    end() {
      const last = rest.length ? [text(rest)] : [];
      rest = Buffer.alloc(0);
      return last;
    },
  };
}

/* The two kinds of progress line the brief names; everything else is log and
 * comes back null.
 *
 *   [cup] 12/65 A3 thornshear v vesper seed 1606666929 -> 02-groups\A\13 - A3 - ...mp4
 *   [cup] 12/65 A3 already filmed: 02-groups\A\13 - A3 - ...mp4
 *   [cup] band: GROUP A · MATCH 3 OF 3 / WINNER TAKES THE GROUP
 *   [cup] done 12/65
 *   [progress] capture frames=2140 elapsed=38.0      shorts_build's, passed through
 *
 * The [progress] pattern is createShort's own, unchanged: cup.py prints
 * shorts_build's lines through as they are. The closing tally
 * ("[cup] 31/65 filmed - schedule: ...") matches none of these on purpose --
 * it is the run's last word, and it goes to the log. */
function parseLine(line) {
  let m;
  if ((m = /^\[progress\] capture frames=(\d+) elapsed=([\d.]+)/.exec(line))) {
    return { stage: 'capture', frames: +m[1], elapsed: +m[2] };
  }
  if (!line.startsWith('[cup] ')) return null;
  if ((m = /^\[cup\] (\d+)\/(\d+) (\S+) (\S+) v (\S+) seed (\d+) -> (.+)$/.exec(line))) {
    return { kind: 'fixture', i: +m[1], total: +m[2], id: m[3], a: m[4], b: m[5],
             seed: +m[6], file: m[7] };
  }
  if ((m = /^\[cup\] (\d+)\/(\d+) (\S+) already filmed: (.+)$/.exec(line))) {
    return { kind: 'skip', i: +m[1], total: +m[2], id: m[3], file: m[4] };
  }
  if ((m = /^\[cup\] band: (.*)$/.exec(line))) return { kind: 'band', text: m[1] };
  if ((m = /^\[cup\] done (\d+)\/(\d+)$/.exec(line))) {
    return { kind: 'fixtureDone', i: +m[1], total: +m[2] };
  }
  return null;
}

/* What a failed run said. cup.py fails through sys.exit("! ..."), and its
 * refusals can run to several lines: the runtime check puts each problem on
 * its own line under the "!" and ends on "--force to override". The last line
 * alone would say how to override a check without saying which check failed.
 * So: from the last line that starts with "!" to the end; the last line if
 * there is none (a traceback ends on its own reason). */
function failureText(log, max = 6) {
  const tail = log.filter((l) => l.trim()).slice(-40);
  for (let i = tail.length - 1; i >= 0; i--) {
    if (tail[i].startsWith('!')) return tail.slice(i, i + max).join('\n');
  }
  return tail.length ? tail[tail.length - 1] : '';
}

module.exports = { decodeLine, lineSplitter, parseLine, failureText };
