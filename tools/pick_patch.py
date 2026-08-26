#!/usr/bin/env python3
"""Teach pick.py to reject seeds that open cold.

Once render.py opens on the fight and plays the card on the first clank, the
time to first contact stops being a curiosity and becomes the single most
expensive number in the video: it is dead air at the front, where a Short is
decided. Measured on sc-ember, 144 matches:

    first clank   median 3.18s   p25 1.78   p75 4.58   p90 7.78   max 18.18

The tail is the problem, not the middle. A cap inside render.py can only cut to
the card mid-approach, which is the thing Rick said he did not want -- so the
fix belongs HERE, one step earlier: do not pick that seed. The cap in render.py
stays as a safety net for a seed that got through anyway.

`AC.simulate` does not report contact times, so the scan runs a second pass that
steps only until the first clank and the first landed hit, then breaks. That is
much cheaper than stepping every match to completion, and it leaves the existing
summary path untouched so nothing about the current ranking moves except by the
new term.
"""
from __future__ import annotations
import pathlib, sys

T = pathlib.Path("/home/claude/sc/sc/tools/pick.py")

EDITS = [
("scan JS also measures time to contact",
'''SCAN_JS = r"""
([a, b, n, s0]) => {
  const out = [];
  let s = s0 >>> 0;
  for (let i = 0; i < n; i++) {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    const r = AC.simulate(a, b, s);
    out.push(r);
  }
  return out;
}
"""''',
'''SCAN_JS = r"""
([a, b, n, s0]) => {
  const out = [], dt = AC.CONFIG.physics.dt, CAP = Math.round(22 / dt);
  let s = s0 >>> 0;
  for (let i = 0; i < n; i++) {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    const r = AC.simulate(a, b, s);
    /* Second pass, early-exit: AC.simulate does not report WHEN contact
       happened, and with a cold open that is the most expensive number in the
       video. Stepping only to the first clank costs a fraction of a full
       match, and the summary above is left exactly as it was so the existing
       ranking cannot move except through the new term. */
    const m = new AC.Match(a, b, s); m.introT = 0;
    let clank = null, hit = null;
    for (let k = 0; k < CAP && !m.over; k++) {
      const c0 = m.clankCount, ha = m.a.hp, hb = m.b.hp;
      m.step(dt);
      if (clank === null && m.clankCount > c0) clank = m.t;
      if (hit === null && (m.a.hp < ha || m.b.hp < hb)) hit = m.t;
      if (clank !== null && hit !== null) break;
    }
    r.tOpen = clank; r.tHit = hit;
    out.push(r);
  }
  return out;
}
"""'''),

("score() rejects and rewards on time to contact",
'''def score(r, lo=28.0, hi=44.0):
    """Higher is more watchable. Every term is a stated opinion about Shorts."""
    if r["reason"] != "slain":
        return -1e9, "timeout"                       # a timeout is not an ending''',
'''def score(r, lo=28.0, hi=44.0, max_open=6.0):
    """Higher is more watchable. Every term is a stated opinion about Shorts."""
    if r["reason"] != "slain":
        return -1e9, "timeout"                       # a timeout is not an ending

    /* placeholder */'''),

("cold-open term",
'''    d = r["duration"]
    why = []
    s = 0.0''',
'''    # Time to first contact. With a cold open this is dead air at the front of
    # the video, where a Short is decided -- so a late opener is REJECTED
    # outright rather than merely penalised. p90 across the roster is 7.78s and
    # the worst seed measured 18.18s; those are not films, they are wallpaper.
    t_open = r.get("tOpen")
    if t_open is None or t_open > max_open:
        return -1e9, f"cold open {t_open if t_open is None else round(t_open, 1)}s"

    d = r["duration"]
    why = []
    s = 0.0

    # inside p25 (1.78s) is a fight that starts before the viewer can leave
    if t_open <= 1.8:
        s += 14.0; why.append("fast open")
    elif t_open <= 3.2:                              # inside the median
        s += 6.0'''),

("scan passes the cap through",
'''def scan(a, b, n=300, seed0=12345, lo=28.0, hi=44.0, top=5, game_path=None):''',
'''def scan(a, b, n=300, seed0=12345, lo=28.0, hi=44.0, top=5, game_path=None,
         max_open=6.0):'''),

("score call",
'''        sc, why = score(r, lo, hi)''',
'''        sc, why = score(r, lo, hi, max_open)'''),

("CLI",
'''    ap.add_argument("--hi", type=float, default=44.0)''',
'''    ap.add_argument("--hi", type=float, default=44.0)
    ap.add_argument("--max-open", type=float, default=6.0,
                    help="reject seeds whose first clank is later than this "
                         "(seconds). Roster p75 is 4.58s, p90 is 7.78s.")'''),
]

def main() -> int:
    s = T.read_text(encoding="utf-8")
    for label, old, new in EDITS:
        n = s.count(old)
        if n != 1:
            print(f"! anchor {label!r} hit {n} times, wanted 1", file=sys.stderr); return 1
        s = s.replace(old, new, 1)
    s = s.replace("\n    /* placeholder */", "")     # JS comment style slipped in
    T.write_text(s, encoding="utf-8")
    print(f"  patched {T} ({len(EDITS)} anchors)")
    return 0

raise SystemExit(main())
