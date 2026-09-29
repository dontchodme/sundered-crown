"""THE BEATS (brief stage 6: "cast files `ult`; a touch files nothing -- measure beat_dist if in doubt"). beat_dist.py
is Twinshade's crowd-score tool and hardcoded to it, so this counts the director's beats directly, on the final bytes
and on the base: Match.prototype.beat, fireUlt and tickRunes are WRAPPED from outside the page (each wrapper calls the
original and only records), so every beat is attributed to the call it was filed inside.
  per Lodestone cast: the beats fireUlt files (must be exactly one, kind 'ult', w 'lodestone')
  inside tickRunes: every beat filed (must be 0) and every hitStop raise (must be 0)
  the fight's whole beat list by kind, final vs base (identical: the rows are presentation only)
usage: ld_beats.py. SCRATCH."""
import sys, pathlib, json
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
PAGES = {"final": HERE / "ld-final.html", "base": (HERE.parent / "links" / "sc-lodestone-b205.html").resolve()}
FOES = ["dawnbringer", "gravemourn", "spellbreaker", "widowmaker", "axiom", "twinshade", "shroudmaul", "morningstar"]
SEEDS = [102001, 102002]
JS = r"""([foes, seeds]) => {
  window.__frozen = true;
  const M = AC.Match.prototype, DT = AC.CONFIG.physics.dt;
  const ob = M.beat, of = M.fireUlt, ot = M.tickRunes;
  let where = null, log = null;
  M.beat = function(o){ if (log) log.push({ kind: o.kind, w: o.w, where, t: +this.t.toFixed(4) }); return ob.call(this, o); };
  M.fireUlt = function(f){ const w0 = where; where = "fireUlt:" + f.w.id; try { return of.apply(this, arguments); } finally { where = w0; } };
  let stopRaise = 0;
  M.tickRunes = function(dt){ const w0 = where, hs = this.hitStop; where = "tickRunes";
    try { return ot.apply(this, arguments); } finally { if (this.hitStop > hs) stopRaise++; where = w0; } };
  const fights = [];
  for (const foe of foes) for (const seed of seeds) for (const side of ["a", "b"]){
    const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
    const me = m.a.w.id === "lodestone" ? m.a : m.b;
    log = [];
    let casts = 0, prev = null, steps = 0;
    while (!m.over && steps < 200 / DT){ m.step(DT); steps++; if (me.ultRunes && !prev) casts++; prev = me.ultRunes; }
    const kinds = {};
    for (const b of log) kinds[b.kind] = (kinds[b.kind] || 0) + 1;
    fights.push({ foe, seed, side, casts, touches: me.runeTally ? me.runeTally.touches : 0,
                  ldFire: log.filter(b => b.where === "fireUlt:lodestone").map(b => b.kind + ":" + b.w),
                  inRunes: log.filter(b => b.where === "tickRunes").length, kinds, n: log.length,
                  sig: log.map(b => b.kind + "@" + b.t).join(",") });
  }
  M.beat = ob; M.fireUlt = of; M.tickRunes = ot;
  return { fights, stopRaise };
}"""
res = {}
for nm, pg in PAGES.items():
    with game(game_path=pg) as (page, errors):
        res[nm] = page.evaluate(JS, [FOES, SEEDS])
        res[nm]["errors"] = list(errors)
F, B = res["final"], res["base"]
bad_fire = [f for f in F["fights"] if f["ldFire"] != ["ult:lodestone"] * f["casts"]]
in_runes = sum(f["inRunes"] for f in F["fights"])
same = all(a["sig"] == b["sig"] for a, b in zip(F["fights"], B["fights"])) and len(F["fights"]) == len(B["fights"])
casts = sum(f["casts"] for f in F["fights"]); touches = sum(f["touches"] for f in F["fights"])
kinds = {}
for f in F["fights"]:
    for k, v in f["kinds"].items(): kinds[k] = kinds.get(k, 0) + v
print(f"{len(F['fights'])} Lodestone fights (8 foes x 2 seeds x both sides) on ld-final: {casts} casts, {touches} touches, {sum(f['n'] for f in F['fights'])} beats {kinds}")
print(f"  [1] {'PASS' if not bad_fire else 'FAIL'}  every Lodestone cast files exactly one beat, kind 'ult' (fireUlt: {casts} casts -> "
      f"{sum(len(f['ldFire']) for f in F['fights'])} beats){'' if not bad_fire else ' BAD ' + str([(f['foe'], f['seed'], f['side'], f['ldFire'][:4]) for f in bad_fire[:3]])}")
print(f"  [2] {'PASS' if in_runes == 0 and F['stopRaise'] == 0 else 'FAIL'}  a touch files nothing: beats filed inside tickRunes {in_runes}, hit-stop raises inside it {F['stopRaise']} ({touches} touches)")
print(f"  [3] {'PASS' if same else 'FAIL'}  every fight's beat list (kind @ t) identical to the base b205's")
print(f"  errors final {len(F['errors'])} base {len(B['errors'])}")
(HERE / "beats.json").write_text(json.dumps({k: {"stopRaise": v["stopRaise"], "fights": [{x: y for x, y in f.items() if x != "sig"} for f in v["fights"]]} for k, v in res.items()}, indent=1))
ok = not bad_fire and in_runes == 0 and F["stopRaise"] == 0 and same and not F["errors"] and not B["errors"]
print("BEATS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
