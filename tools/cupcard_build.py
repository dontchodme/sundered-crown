#!/usr/bin/env python
"""THE WORLD CUP'S VERDICT CARD (v118) -- one presentation-only link on the frozen build.

    python cupcard_build.py --src ../02-chain/sc-candidate-49.html --out ../02-chain/sc-cupcard.html

Plan v115 §5.3, built from its sketch on Rick's word (2026-09-30: "build it from the sketch").
The scrunch panel's verdict beat holds the HP recap. This link gives it a third mode,
`CONFIG.cup`: when a blob is set, the verdict beat draws what the result DID -- a group table
(relic, W, L, HP; a marker on this fixture's winner; what is left in the group) or a knockout
result (the round, the winner through, where it goes next, the relics left). When it is null
-- the live page, the app's single shorts, every film that is not a Cup fixture -- everything
renders exactly as before.

Three inserts and nothing else:

    CONFIG_NEW   `cup: null` in CONFIG, beside the scrunch it belongs to
    HOOK_NEW     drawScrunchPanel's verdict branch: the card when CONFIG.cup is set
    PANEL_NEW    Renderer._panelCup, which draws the blob and decides nothing

The blob comes from `cup.py cupjson` (every string, the row order, the marker), reaches the page
through `shorts_build.py --cup-json` -> `cinema_clip.py --cup-json`, and is set on AC.CONFIG
before the fight starts. The builder refuses: an anchor that is not exactly once, any line it
did not mean to move, an added line that draws the rng or writes a Match field, a page that does
not parse, and an existing link.
"""
from __future__ import annotations
import argparse, difflib, hashlib, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from staffkit import one, strip_comments, syntax_check, check_no_rng

CONFIG_OLD = """             resultDelay: 1.05, gap: 22, bottom: 1812 },
"""
CONFIG_NEW = CONFIG_OLD + """  /* THE WORLD CUP'S VERDICT CARD (v118, cupcard_build.py; plan v115 §5.3). Null on the
     live page and on every film but a Cup fixture's, where cinema_clip sets it from the blob
     `cup.py cupjson` writes (shorts_build --cup-json). Set, the scrunch panel's verdict beat
     draws that blob -- a group table or a knockout result -- in place of the HP recap.
     Presentation only: nothing in Match, Fighter or the director reads it, and every string
     on the card is cup.py's, composed from the ledger, so the renderer decides nothing. */
  cup: null,
"""

HOOK_OLD = """    if (m.scrunchMode === "result") this._panelResult(m, x, y, w, h);
"""
HOOK_NEW = """    /* v118: a World Cup fixture's card in place of the recap, when cup.py set one */
    if (m.scrunchMode === "result" && CONFIG.cup) this._panelCup(m, CONFIG.cup, x, y, w, h);
    else if (m.scrunchMode === "result") this._panelResult(m, x, y, w, h);
"""

PANEL_OLD = """  /* The verdict, in the same strip. The point of putting it here instead of
"""
PANEL_NEW = """  /* THE WORLD CUP'S VERDICT CARD (v118, plan v115 §5.3) -- what the result DID, where the
     recap would have said how it was won. The plan's sketch, both halves:

       GROUP F                 W  L   HP          ROUND OF 16
       > Thornshear            2  0  310          THORNSHEAR (tick) through
         Vesper                1  1  142          next: v VESPER · QF 2
         Axiom                 0  2    -
       1 MATCH LEFT · F3 TOMORROW                 weapon ball world cup · 12 relics left

     IT DRAWS AND DECIDES NOTHING. Every string, the row order and the marker arrive in the
     blob from `cup.py cupjson`, built from the ledger as it stood after this fixture -- the
     place the stakes band's copy comes from, under the same no-spoiler rule -- so a wrong
     word is fixed in one Python function and is testable without a browser. The only thing
     read here is each relic's school colour, off WEAPONS, for the name that won.

     The marker and the tick are PATHS, not glyphs: U+25B6 has an emoji presentation, and a
     font fallback that picks it up would put a blue button in the table. Every line is
     measured and shrunk to its column, never grown, as the stakes band is. */
  _panelCup(m, cup, x, y, w, h){
    const c = this.ctx, pad = 30;
    const SANS = "ui-sans-serif,system-ui,sans-serif", SERIF = "ui-serif,Georgia,serif";
    const font = (wt, px, fam) => { c.font = wt + " " + px + "px " + fam; };
    const fit = (s, wt, px, fam, maxW) => {
      font(wt, px, fam);
      const tw = c.measureText(s).width;
      if (tw > maxW){ px = Math.max(12, Math.floor(px * maxW / tw)); font(wt, px, fam); }
      return px;
    };
    const school = id => {
      const wp = WEAPON_BY_ID[id], af = wp && AFFINITIES[wp.aff];
      return af ? af.core : "#EDE3D0";
    };
    const str = v => (v === undefined || v === null) ? "" : String(v);
    c.textBaseline = "alphabetic";

    if (cup.kind === "group"){
      const x0 = x + pad, x1 = x + w - pad;
      const cHP = x1, cL = x1 - 150, cW = cL - 80;     /* right edges of the number columns */
      const head = y + pad + 30;
      c.textAlign = "left"; c.fillStyle = "#C9A227";
      fit(str(cup.title), "700", 32, SANS, cW - 60 - x0);
      c.fillText(str(cup.title), x0, head);
      font("700", 22, SANS); c.fillStyle = "#7E7263"; c.textAlign = "right";
      const cols = Array.isArray(cup.cols) ? cup.cols : ["W", "L", "HP"];
      [cW, cL, cHP].forEach((cx, i) => c.fillText(str(cols[i]), cx, head));
      const top = y + pad + 50, bot = y + h - pad - 50;
      c.strokeStyle = "#C9A22744"; c.lineWidth = 2;
      c.beginPath(); c.moveTo(x0, top); c.lineTo(x1, top);
      c.moveTo(x0, bot); c.lineTo(x1, bot); c.stroke();
      const rows = Array.isArray(cup.rows) ? cup.rows.slice(0, 3) : [];
      const rh = (bot - top) / 3;
      rows.forEach((r, i) => {
        const cy = top + rh * (i + 0.5);
        if (r.mark){
          /* this fixture's winner: a faint gold band behind the row and a wedge at its head */
          c.fillStyle = "#C9A22716";
          c.fillRect(x0 - 10, cy - rh / 2 + 5, x1 - x0 + 20, rh - 10);
          c.fillStyle = "#C9A227";
          c.beginPath(); c.moveTo(x0, cy - 13); c.lineTo(x0 + 22, cy); c.lineTo(x0, cy + 13);
          c.closePath(); c.fill();
        }
        const nx = x0 + 40;
        c.textAlign = "left";
        c.fillStyle = r.mark ? school(r.id) : "#EDE3D0";
        const px = fit(str(r.name), "700", 46, SERIF, cW - 70 - nx);
        c.fillText(str(r.name), nx, cy + px * 0.34);
        font("700", 44, SANS); c.textAlign = "right"; c.fillStyle = "#EDE3D0";
        [[cW, r.w], [cL, r.l], [cHP, r.hp]].forEach(([cx, v]) => c.fillText(str(v), cx, cy + 15));
      });
      c.textAlign = "left"; c.fillStyle = "#C6BBA6";
      fit(str(cup.footer), "700", 28, SANS, x1 - x0);
      c.fillText(str(cup.footer), x0, y + h - pad - 12);
      return;
    }

    /* the knockout, the play-in and the final: the round, the winner, where it goes next */
    const W2 = x + w / 2, maxW = w - pad * 2;
    c.textAlign = "center"; c.fillStyle = "#C9A227";
    fit(str(cup.title), "700", 32, SANS, maxW);
    c.fillText(str(cup.title), W2, y + 62);
    /* NAME, the tick, the verdict: measured as one group, shrunk together, centred */
    const name = str(cup.name), verdict = str(cup.verdict);
    const NP = 64, VP = 38, GAP = 24, TICK = 36;
    const lineW = k => {
      font("700", Math.round(NP * k), SERIF); const a = c.measureText(name).width;
      font("700", Math.round(VP * k), SANS);  const b = c.measureText(verdict).width;
      return { a, b, all: a + (GAP * 2 + TICK) * k + b };
    };
    let k = 1, lw = lineW(1);
    if (lw.all > maxW){ k = maxW / lw.all; lw = lineW(k); }
    const by = y + h * 0.42;
    let lx = W2 - lw.all / 2;
    c.textAlign = "left";
    font("700", Math.round(NP * k), SERIF);
    const col = school(cup.winner);
    c.fillStyle = col; c.shadowColor = col; c.shadowBlur = 40;
    c.fillText(name, lx, by);
    c.shadowBlur = 0;
    lx += lw.a + GAP * k;
    const ty = by - NP * k * 0.32;
    c.strokeStyle = "#C9A227"; c.lineWidth = 6 * k; c.lineCap = "round"; c.lineJoin = "round";
    c.beginPath(); c.moveTo(lx, ty); c.lineTo(lx + TICK * k * 0.38, ty + TICK * k * 0.36);
    c.lineTo(lx + TICK * k, ty - TICK * k * 0.46); c.stroke();
    lx += (TICK + GAP) * k;
    font("700", Math.round(VP * k), SANS); c.fillStyle = "#EDE3D0";
    c.fillText(verdict, lx, by);
    c.textAlign = "center";
    if (cup.next){
      c.fillStyle = "#C6BBA6";
      fit(str(cup.next), "500", 34, SANS, maxW);
      c.fillText(str(cup.next), W2, y + h * 0.64);
    }
    c.fillStyle = "#7E7263";
    fit(str(cup.footer), "500", 26, SANS, maxW);
    c.fillText(str(cup.footer), W2, y + h - pad - 10);
  }

""" + PANEL_OLD

EDITS = [
    ("CONFIG.cup", CONFIG_OLD, CONFIG_NEW),
    ("the verdict branch", HOOK_OLD, HOOK_NEW),
    ("Renderer._panelCup", PANEL_OLD, PANEL_NEW),
]

# an added line that WRITES a field of the match or a fighter would be the card reaching into
# the sim; reads (`m.winner`) and comparisons are fine, assignments are not
# (a CHAIN of fields: `m.a.hp = 1` is the write that matters, and a one-dot pattern misses it)
SIM_WRITE = re.compile(r"\b(?:m|this\.m|match|f|wn|ls|AC)(?:\.[A-Za-z_$][\w$]*|\[[^\]]*\])+"
                       r"\s*(?:[-+*/%]?=(?!=)|\+\+|--)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    A = ap.parse_args()
    src, out = (HERE / A.src).resolve(), (HERE / A.out).resolve()
    if not out.name.startswith("sc-cupcard"):
        raise SystemExit(f"refusing {out.name}: this builder's links are sc-cupcard*")
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out.name} -- a link is written once")
    if not src.exists():
        raise SystemExit(f"no such build: {src}")
    raw = src.read_bytes()
    if b"\r" in raw:
        raise SystemExit(f"{src.name} has CR bytes -- the anchors are LF; refusing")
    s0 = raw.decode("utf-8")
    if "_panelCup" in s0 or re.search(r"^\s*cup:\s*null,", s0, re.M):
        raise SystemExit(f"{src.name} already carries the card")
    print(f"\nTHE WORLD CUP'S VERDICT CARD (v118) -- src {src.name} "
          f"{hashlib.sha256(raw).hexdigest()[:16]}")
    s = s0
    for label, old, new in EDITS:
        s = one(s, old, new, label)
    check_no_rng(EDITS)
    for label, old, new in EDITS:
        hit = SIM_WRITE.search(strip_comments(new.replace(old, "", 1)))
        if hit:
            raise SystemExit(f"REFUSING TO WRITE -- insert '{label}' writes a sim field: {hit.group(0)!r}")
    if strip_comments(s).count("Math.random") != strip_comments(s0).count("Math.random"):
        raise SystemExit("REFUSING TO WRITE -- this build adds a Math.random")
    print("  ok    no rng, no Math.random, no Match/Fighter field written")
    # NOTHING ELSE MOVED: the only line that goes is the verdict branch; every other change is an add
    gone, came = [], []
    for op in difflib.unified_diff(s0.split("\n"), s.split("\n"), n=0, lineterm=""):
        if op.startswith(("---", "+++", "@@")):
            continue
        (gone if op[0] == "-" else came).append(op[1:])
    want_gone = [HOOK_OLD.rstrip("\n")]
    # each insert's own lines, its trailing newline not counted as a line
    want_came = sum((new.replace(old, "", 1).split("\n")[:-1] for _, old, new in EDITS), [])
    if gone != want_gone or sorted(came) != sorted(want_came):
        raise SystemExit(f"REFUSING TO WRITE -- the diff is not the three inserts "
                         f"({len(gone)} lines gone, {len(came)} came; wanted 1 and {len(want_came)})")
    print(f"  ok    diff  1 line replaced, {len(came)} added, nothing else moved")
    s = (f"<!-- GENERATED by cupcard_build.py --src {src.name} (v118: the World Cup's verdict "
         f"card, CONFIG.cup; plan v115 §5.3) -->\n") + s
    syntax_check(s, out.name)
    out.write_text(s, encoding="utf-8", newline="\n")
    print(f"\n  out {out.name}  {hashlib.sha256(s.encode()).hexdigest()[:16]}"
          f"   ({len(s) - len(s0):+d} chars, written LF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
