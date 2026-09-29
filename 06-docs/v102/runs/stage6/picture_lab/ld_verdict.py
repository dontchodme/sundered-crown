"""THE VERDICT FRAME PROBE (v102 section 5's must-do: `ultRunes` outlives a kill by a blow, so the picture must
gate on `!over`). Whole fights to the kill, then EVERY 3rd step for 3.5s of verdict drawn at 540x960 (chain on,
shake zeroed, Math.random pinned): on every frame the verdict panel is up (scrunchMode "result" and the hall
scrunched), NO rune may be drawn -- the picture's six drawing methods are wrapped harness-side and must not be
entered -- and the frame must be pixel-identical to the same frame with the picture's three entry points
shadowed. Counts the fights that END LIT (ultRunes still set at the kill: the case the gate exists for).
THE CONTROL: ld-ungated.html is ld-final with the gate removed (`const Z = f.ultRunes;`) -- it must draw runes
over the panel on the fights that end lit. usage: ld_verdict.py [page...]. SCRATCH."""
import sys, json, pathlib
sys.path.insert(0, r"C:\dev\sundered-crown\tools")
from scpage import game
HERE = pathlib.Path(__file__).parent
FOES = ["spellbreaker", "dawnbringer", "gravemourn", "grudgebearer", "aureole", "twinshade", "widowmaker", "axiom",
        "paradox", "heartwood", "shroudmaul", "lastlight"]
JS = r"""([foe, seed, side]) => {
  window.__frozen = true;
  const pan = document.getElementById("cinePanel"); if (pan) pan.style.display = "none";
  AC.setResolution(540, 960); AC.SFX.play = function(){}; AC.SFX.resume = function(){}; AC.CINE.on = false;
  const DT = AC.CONFIG.physics.dt, r = AC.renderer, cv = document.getElementById("cv"), ctx = cv.getContext("2d");
  const m = side === "a" ? new AC.Match("lodestone", foe, seed) : new AC.Match(foe, "lodestone", seed);
  const me = m.a.w.id === "lodestone" ? m.a : m.b;
  m.scrunchAuto = AC.CONFIG.scrunch.on;          // as the app arms it (presentation only)
  const realRandom = Math.random;
  const pin = (s) => () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const INNER = ["_lodeWalls", "_lodeMotes", "_lodeFlare", "_lodeStreak", "_lodeBolt", "_lodeHead"];
  const ENTRY = ["drawLode", "drawLodeTop", "_lodeHead"];
  let calls = 0;
  const orig = {};
  for (const k of INNER){ orig[k] = r[k]; r[k] = function(){ calls++; return orig[k].apply(this, arguments); }; }
  const frame = (hide) => { const saved = [];
    if (hide) for (const h of ENTRY){ r[h] = function(){}; saved.push(h); }
    const ks = m.shake; m.shake = 0; Math.random = pin(0x5EEDF00D);
    try { AC.__draw(m); } finally { Math.random = realRandom; m.shake = ks;
      for (const h of saved){ if (INNER.includes(h)) r[h] = function(){ calls++; return orig[h].apply(this, arguments); }; else delete r[h]; } }
    return new Uint8ClampedArray(ctx.getImageData(0, 0, cv.width, cv.height).data); };
  let step = 0;
  while (!m.over && step < 200 / DT){ m.step(DT); step++; }
  const out = { foe, seed, side, t: +m.t.toFixed(3), litAtKill: !!me.ultRunes, meAlive: me.alive,
                fadeAtKill: +(me.lodeFade || 0).toFixed(3), frames: 0, panel: 0, panelCalls: 0, panelPixDiff: 0,
                preCalls: 0, lastCallAfter: null, firstPanelAfter: null };
  let s = 0;
  while (s * DT < 3.5){
    m.step(DT); s++;
    if (s % 3) continue;
    const c0 = calls;
    const A = frame(false);
    const drew = calls > c0;
    out.frames++;
    if (drew) out.lastCallAfter = +(s * DT).toFixed(4);
    const up = m.scrunchMode === "result" && r.scrunchK(m) < 0.999;
    if (up){
      if (out.firstPanelAfter === null) out.firstPanelAfter = +(s * DT).toFixed(4);
      out.panel++;
      if (drew) out.panelCalls++;
      const B = frame(true);
      let d = 0; for (let i = 0; i < A.length; i++) if (A[i] !== B[i]){ d++; break; }
      if (d) out.panelPixDiff++;
    } else if (drew) out.preCalls++;
  }
  for (const k of INNER) r[k] = orig[k];
  return out;
}"""
pages = [pathlib.Path(p) for p in sys.argv[1:]] or [HERE / "ld-final.html", HERE / "ld-ungated.html"]


def make_ungated():
    s = (HERE / "ld-final.html").read_text(encoding="utf-8")
    old = "      const Z = (this.over || !f.alive) ? null : f.ultRunes;\n      if (Z){\n        if (!(f.lodeFade > 0) || f.lodeOut > 0){"
    assert s.count(old) == 1
    s = s.replace(old, old.replace("(this.over || !f.alive) ? null : f.ultRunes", "f.ultRunes"))
    (HERE / "ld-ungated.html").write_text(s, encoding="utf-8")


if __name__ == "__main__":
    make_ungated()
    allres = {}
    for pg in pages:
        pg = pg if pg.is_absolute() else HERE / pg
        res = []
        with game(game_path=pg) as (page, errors):
            for i, foe in enumerate(FOES):
                for seed, side in ((102001 + i, "a"), (102101 + i, "b")):
                    r = page.evaluate(JS, [foe, seed, side])
                    assert not errors, errors[:3]
                    res.append(r)
        allres[pg.name] = res
        lit = [x for x in res if x["litAtKill"]]
        print(f"{pg.name}: {len(res)} fights, {len(lit)} END LIT (ultRunes set at the kill; caster alive in {sum(1 for x in lit if x['meAlive'])}); "
              f"verdict frames {sum(x['frames'] for x in res)}, with the panel up {sum(x['panel'] for x in res)}; "
              f"panel frames with a rune drawn {sum(x['panelCalls'] for x in res)}; panel frames that differ from the picture hidden "
              f"{sum(x['panelPixDiff'] for x in res)}; the panel first up {min(x['firstPanelAfter'] for x in res if x['firstPanelAfter'] is not None):.3f}s "
              f"after the kill; the last rune drawn {max((x['lastCallAfter'] or 0) for x in res):.3f}s after it "
              f"(lit fights: {sorted(set((x['lastCallAfter'] or 0) for x in lit))[:6]}...)", flush=True)
        for x in res:
            if x["panelCalls"] or x["panelPixDiff"]:
                print(f"    {x['foe']} {x['seed']}{x['side']}: lit {x['litAtKill']} alive {x['meAlive']} panel {x['panel']} rune frames {x['panelCalls']} pix {x['panelPixDiff']}")
    (HERE / "verdict.json").write_text(json.dumps(allres, indent=1))
