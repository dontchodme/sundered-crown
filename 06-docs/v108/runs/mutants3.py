"""Probe controls for v108 §3 after the SECOND review: scratch mutants of THE FINAL LINK,
sc-ironhail-sunder, for the two checks the review sharpened. Written to <S>/tmp/mut3-*.html;
never a link. The r-* strings are the reviewer's own (scratchpad/review_ironhail/mk_mut.py and the
review text); r-beatspot is this build's, for the (x, y) clause of [7].
  r-double    [1]  the hail ticked twice a step (window 4s, cadence 0.2s, fall 0.15s of fight)
  r-half      [1]  the hail ticked on every other unfrozen step (window 16s, cadence 0.8s, fall 0.6s)
  r-beatside  [7]  the fatal beat credits the kill to the loser's side (presentation: no fight moves)
  r-beatspot  [7]  the fatal beat is filed at the caster's spot, not the foe's (presentation)"""
import pathlib, sys, hashlib
S = pathlib.Path(sys.argv[1]); src = (S / "links" / "sc-ironhail-sunder.html").read_text(encoding="utf-8")
TICK = "    this.tickHail(dt);                  // QUARRELSTORM (v83)\n"
M = {
 "r-double":   (TICK, TICK + "    this.tickHail(dt);\n"),
 "r-half":     (TICK, "    if ((this._hk = (this._hk || 0) + 1) % 2) this.tickHail(dt);                  // QUARRELSTORM (v83)\n"),
 "r-beatside": ('this.beat({ kind: "hit", side: d.side === "a" ? 0 : 1,',
                'this.beat({ kind: "hit", side: d.side === "a" ? 1 : 0,'),
 "r-beatspot": ("                    x: foe.x, y: foe.y, dmg: u.dropDmg, crit: false,",
                "                    x: f.x, y: f.y, dmg: u.dropDmg, crit: false,"),
}
for k, (a, b) in M.items():
    assert src.count(a) == 1, (k, src.count(a))
    s = src.replace(a, b, 1)
    out = S / "tmp" / f"mut3-{k}.html"
    out.write_text(s, encoding="utf-8", newline="\n")
    print(k, hashlib.sha256(s.encode()).hexdigest()[:16])
