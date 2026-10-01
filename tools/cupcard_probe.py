#!/usr/bin/env python
"""THE WORLD CUP'S VERDICT CARD, PROVED OFF AND LOOKED AT (v118).

    python cupcard_probe.py --ab    --a ../02-chain/sc-candidate-49.html --b ../02-chain/sc-cupcard.html \
                            --blob <one cupjson blob>
    python cupcard_probe.py --sheet <out.png> --b ../02-chain/sc-cupcard.html <blob.json> ...

render_ab samples a fight at fixed match times, and the verdict beat is not at a fixed time: it
arms 1.05s after the kill and holds to the end of the clip. So this samples ONE finished fight
through its verdict beat -- before the panel arms, as it eases in, held -- at 1080x1920, every
pixel hashed.

--ab   four runs in one browser, one rasteriser:
         A, card unset   vs  B, card unset   must be IDENTICAL on every frame (the card off is
                                              invisible -- the claim under test)
         A               vs  A again         must be IDENTICAL (the probe's own noise floor; if
                                              this differs, the first line proved nothing)
         B, card unset   vs  B, blob set     must be identical BEFORE the panel arms and DIFFER
                                              after (the control that can come back wrong)
       Presentation randomness (sparks, the shake) is pinned by a seeded Math.random installed
       in every page, the way render_ab pins the shake.

--sheet  B with each blob set, the held verdict frame, saved full-size beside <out.png> and the
         panel crops stacked into <out.png> for reading at phone size.
"""
from __future__ import annotations
import argparse, base64, json, pathlib, sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent

RUN_JS = r"""(cfg) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  let s = 20260930 >>> 0;
  Math.random = () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  if (cfg.blob) AC.CONFIG.cup = cfg.blob;
  const cv = document.getElementById('cv'), dt = AC.CONFIG.physics.dt;
  const m = new AC.Match(cfg.a, cfg.b, cfg.seed >>> 0);
  AC.__inject(m);
  AC.SFX.play = function () {};
  if (typeof POSTFX !== 'undefined') POSTFX.reset();
  let g = 0;
  while (!m.over && g++ < 400000) m.step(dt);
  const frames = [];
  const shoot = (tag) => {
    m.shake = 0;
    AC.__draw(m);
    const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
    let h = 2166136261 >>> 0;
    for (let i = 0; i < d.length; i++) { h ^= d[i]; h = Math.imul(h, 16777619) >>> 0; }
    return { tag, resultT: +(m.resultT || 0).toFixed(3), mode: m.scrunchMode, hash: h,
             png: cfg.png ? cv.toDataURL('image/png') : null };
  };
  for (const at of cfg.after) {
    while ((m.resultT || 0) < at - dt * 0.5) m.step(dt);
    frames.push(shoot(at));
  }
  const r = AC.renderer, S = AC.CONFIG.scrunch;
  const py = r.arenaTop + r.ah * S.k + S.gap;
  const sheet = [];
  for (const b of (cfg.blobs || [])) { AC.CONFIG.cup = b; sheet.push(shoot(b.fixture)); }
  /* DOES THE CARD EVER RUN IN THE SIM? Count _panelCup calls, with the card set, across
     simulate() of every pairing given -- then across one draw of this finished match, which
     must count, or the counter is not wired and the zero means nothing. */
  let simcheck = null;
  if (cfg.simcheck) {
    let calls = 0;
    const orig = r._panelCup;
    if (orig) r._panelCup = function () { calls++; return orig.apply(this, arguments); };
    const fights = [];
    for (const [a, b, s] of cfg.simcheck) fights.push(AC.simulate(a, b, s >>> 0));
    const inSim = calls;
    AC.__draw(m);
    simcheck = { fights: fights.length, inSim, inDraw: calls - inSim,
                 summaries: fights.map(f => [f.winner, f.hp, f.duration]) };
    if (orig) r._panelCup = orig;
  }
  return { winner: m.winner ? m.winner.w.id : null, t: +m.t.toFixed(2), frames, sheet, simcheck,
           panel: { x: 24, y: py, w: r.W - 48, h: S.bottom - py } };
}"""


def load(browser, path, cfg, errors):
    page = browser.new_page(viewport={"width": 620, "height": 1000})
    page.on("pageerror", lambda e: errors.append(f"{path.name}: {e}"))
    page.on("console", lambda mm: errors.append(f"{path.name}: {mm.text}") if mm.type == "error" else None)
    page.goto(path.as_uri())
    page.wait_for_function("window.AC && window.AC.WEAPONS && window.__fontsReady !== false", timeout=30000)
    out = page.evaluate(RUN_JS, cfg)
    page.close()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", default="../02-chain/sc-candidate-49.html")
    ap.add_argument("--b", default="../02-chain/sc-cupcard.html")
    ap.add_argument("--pair", default="angelus:lodestone:20260930", help="a:b:seed, the fight")
    ap.add_argument("--after", default="0.3,0.9,1.15,1.3,1.6,2.4,3.4",
                    help="seconds after the kill to sample (the panel arms at 1.05, eases 0.42)")
    ap.add_argument("--ab", action="store_true")
    ap.add_argument("--blob", help="--ab: the blob for the must-differ control")
    ap.add_argument("--sheet", help="--sheet: the contact sheet to write")
    ap.add_argument("blobs", nargs="*")
    A = ap.parse_args()
    pa, pb = (HERE / A.a).resolve(), (HERE / A.b).resolve()
    a, b, seed = A.pair.split(":")
    after = [float(x) for x in A.after.split(",")]
    errors: list[str] = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True, args=["--disable-frame-rate-limit", "--disable-gpu", "--no-sandbox"])
        print(f"Chromium {br.version}   fight {a} v {b} seed {seed}")
        base = dict(a=a, b=b, seed=int(seed), after=after)
        if A.ab:
            if not A.blob:
                sys.exit("! --ab needs --blob for the must-differ control")
            blob = json.loads(pathlib.Path(A.blob).read_text(encoding="utf-8"))
            sc = [["angelus", "lodestone", 1], ["heartwood", "lightkeeper", 1022773507],
                  ["emberedge", "farwarden", 220813412], ["ironhail", "dawnbringer", 554373919]]
            runs = {
                "A": load(br, pa, dict(base, simcheck=sc), errors),
                "B": load(br, pb, base, errors),
                "A2": load(br, pa, base, errors),
                "Bcard": load(br, pb, dict(base, blob=blob, simcheck=sc), errors),
            }
            br.close()
            if errors:
                print("! page errors:\n  " + "\n  ".join(errors[:10]))
                return 1
            w = {k: v["winner"] for k, v in runs.items()}
            print(f"  fight ends at {runs['A']['t']}s, {w['A']} wins; panel {runs['A']['panel']}")
            if len(set(w.values())) != 1:
                print(f"! the four runs disagree on the winner: {w}")
                return 1
            ok = True
            print(f"\n  {'after kill':>10} {'mode':>7}   A=B   A=A2   B=Bcard")
            for fa, fb, fa2, fc in zip(*(runs[k]["frames"] for k in ("A", "B", "A2", "Bcard"))):
                armed = fc["mode"] == "result"
                same_ab, same_aa, same_bc = fa["hash"] == fb["hash"], fa["hash"] == fa2["hash"], fb["hash"] == fc["hash"]
                want_bc = not armed
                row_ok = same_ab and same_aa and (same_bc == want_bc)
                ok &= row_ok
                print(f"  {fa['tag']:>9}s {str(fc['mode']):>7}   {'yes' if same_ab else 'NO':>3}   "
                      f"{'yes' if same_aa else 'NO':>4}   {('same' if same_bc else 'differs'):>7}"
                      f"{'' if row_ok else '   <-- ' + ('want differs' if armed else 'want same')}")
            sk = runs["Bcard"]["simcheck"]
            # and the fights themselves: the card-set build's must be the source build's
            same = runs["A"]["simcheck"]["summaries"] == sk["summaries"]
            sim_ok = sk["inSim"] == 0 and sk["inDraw"] > 0 and same
            ok &= sim_ok
            print(f"\n  card set, _panelCup calls: {sk['inSim']} across {sk['fights']} "
                  f"simulate() fights, {sk['inDraw']} in one draw of the verdict "
                  f"{'(the card never runs in the sim; the counter counts)' if sim_ok else '<-- FAIL'}")
            print(f"  the same {sk['fights']} fights, card set vs the source build: "
                  f"{'identical' if same else 'DIFFER'}")
            n = len(runs["A"]["frames"])
            print(f"\n{'PASS' if ok else 'FAIL'}  card off: {sum(x['hash'] == y['hash'] for x, y in zip(runs['A']['frames'], runs['B']['frames']))}/{n} "
                  f"verdict-beat frames identical to the source build; noise floor A=A2 "
                  f"{sum(x['hash'] == y['hash'] for x, y in zip(runs['A']['frames'], runs['A2']['frames']))}/{n}; "
                  f"card on differs on {sum(x['hash'] != y['hash'] for x, y in zip(runs['B']['frames'], runs['Bcard']['frames']))}"
                  f"/{sum(f['mode'] == 'result' for f in runs['Bcard']['frames'])} armed frames")
            return 0 if ok else 1
        if A.sheet:
            blobs = [json.loads(pathlib.Path(p).read_text(encoding="utf-8")) for p in A.blobs]
            r = load(br, pb, dict(base, after=[3.4], blobs=blobs, png=True), errors)
            br.close()
            if errors:
                print("! page errors:\n  " + "\n  ".join(errors[:10]))
                return 1
            from PIL import Image
            import io
            out = pathlib.Path(A.sheet).resolve()
            out.parent.mkdir(parents=True, exist_ok=True)
            P = r["panel"]
            y0, y1 = int(P["y"]) - 16, int(P["y"] + P["h"]) + 16
            crops = []
            for s in r["sheet"]:
                im = Image.open(io.BytesIO(base64.b64decode(s["png"].split(",", 1)[1]))).convert("RGB")
                im.save(out.parent / f"{out.stem}-{s['tag']}.png")
                crops.append(im.crop((0, y0, 1080, y1)))
            cols = 2
            rows = (len(crops) + cols - 1) // cols
            ch = y1 - y0
            sheet = Image.new("RGB", (1080 * cols + 20 * (cols - 1), ch * rows + 20 * (rows - 1)), (40, 40, 40))
            for i, c in enumerate(crops):
                sheet.paste(c, ((i % cols) * 1100, (i // cols) * (ch + 20)))
            sheet.save(out)
            print(f"  panel {P}\n  {len(crops)} cards -> {out}  ({sheet.size[0]}x{sheet.size[1]})")
            return 0
    print("! say --ab or --sheet")
    return 2


if __name__ == "__main__":
    sys.exit(main())
