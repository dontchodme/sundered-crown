#!/usr/bin/env python3
"""THE VESSEL, IN THE GAME. Not a check -- a pair of eyes on the real page.

Runs a real Match to a chosen clock time, at the real 1080x1920, and shoots the
real canvas. The lab proved the look in isolation; this is the only thing that
proves it against the actual hall, the actual weapons, the actual HUD and the
actual statuses landing on it.

    python3 liquid_shot.py --src ../02-chain/sc-liquid.html --at 6,16,26,34
    python3 liquid_shot.py --src ../02-chain/sc-liquid.html --roster
"""
from __future__ import annotations
import argparse, base64, io, pathlib
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent

DRIVE = r"""
window.__L = {
  init(a, b, seed){
    AC.setResolution(1080, 1920);
    AC.SFX.play = function(){}; AC.SFX.resume = function(){};
    this.m = new AC.Match(a, b, seed >>> 0);
    AC.__inject(this.m);
    this.m.introT = 0;
    return true;
  },
  /* Step to a wall-clock time on the SIM tick, exactly as the offline render
     does, so what is shot here is what a video of this build would contain. */
  to(t){
    const dt = AC.CONFIG.physics.dt;
    let guard = 0;
    while (this.m.t < t && guard++ < 200000) this.m.step(dt);
    AC.__draw(this.m);
    return { t: +this.m.t.toFixed(2), over: !!this.m.over,
             a: Math.round(this.m.a.hp), b: Math.round(this.m.b.hp),
             drips: (this.m.drips || []).length,
             tilt: +(this.m.a.slTilt || 0).toFixed(3),
             heave: +(this.m.a.slHeave || 0).toFixed(3) };
  },
  /* THE DEATH, frame by frame. It is the one path a mid-match sample can
     never reach and the one nobody looks at until it ships wrong. */
  death(a, b, seed, n, every){
    AC.setResolution(1080, 1920);
    AC.SFX.play = function(){}; AC.SFX.resume = function(){};
    const m = new AC.Match(a, b, seed >>> 0); AC.__inject(m); m.introT = 0;
    const dt = AC.CONFIG.physics.dt;
    let g = 0;
    while (!m.over && g++ < 200000) m.step(dt);
    /* the killFlight carries the loser into a wall before the shell goes;
       run until the shatter actually starts */
    while (m.deathAge <= 0 && g++ < 200000) m.step(dt);
    const out = [];
    for (let i = 0; i < n; i++){
      for (let k = 0; k < every; k++) m.step(dt);
      AC.__draw(m);
      out.push({ age: +m.deathAge.toFixed(2),
                 png: document.querySelector('canvas').toDataURL('image/png').slice(22) });
    }
    return { loser: m.loser.w.name, deathHp: Math.round(m.loser.deathHp), frames: out };
  },

  /* One relic, one HP value, drawn on its own ground at true canvas scale --
     for the roster sheet, where eighteen fights would be eighteen fights. */
  cell(id, hpFrac, side, t, S){
    const cv = document.createElement('canvas');
    const R = AC.CONFIG.physics.ballR, sc = 1080 / AC.CONFIG.arena.w;
    cv.width = Math.round(R * 2.6 * sc * S); cv.height = cv.width;
    const c = cv.getContext('2d');
    c.fillStyle = '#0A0912'; c.fillRect(0, 0, cv.width, cv.height);
    /* a real Match so the fighter is a real Fighter -- same hidden class,
       same defaults, no hand-built stand-in that could flatter the draw.
       The opponent is whatever relic is NOT this one; it is never drawn. */
    const foe = AC.WEAPONS.find(w => w.id !== id).id;
    const m = new AC.Match(id, foe, 4242); AC.__inject(m); m.introT = 0;
    const f = m.a;
    f.hp = AC.CONFIG.combat.baseHP * hpFrac;
    f.hpGhost = AC.CONFIG.combat.baseHP * Math.min(1, hpFrac + 0.022);
    f.side = side;
    /* a plausible mid-slosh rather than a still pond -- the ball is almost
       never level in a real frame and judging it level flatters it */
    f.slTilt = (AC.__hash(side * 7 + Math.round(hpFrac * 9), 3) - 0.5) * 0.62;
    f.slA2 = (AC.__hash(side * 7 + Math.round(hpFrac * 9), 5) - 0.5) * 0.13;
    f.slA3 = (AC.__hash(side * 7 + Math.round(hpFrac * 9), 9) - 0.5) * 0.09;
    f.slJolt = 0.45;
    f.x = 0; f.y = 0;
    c.save();
    c.translate(cv.width / 2, cv.height / 2);
    c.scale(sc * S, sc * S);
    AC.renderer.ctx = c;
    AC.__glass(c, { t: t }, f, R, { base: AC.CONFIG.combat.baseHP });
    c.restore();
    return cv.toDataURL('image/png').slice(22);
  },
};
true
"""


def png(b64): return Image.open(io.BytesIO(base64.b64decode(b64)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="../02-chain/sc-liquid.html")
    ap.add_argument("--a", default="widowmaker")
    ap.add_argument("--b", default="axiom")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--at", default="7,17,27,35")
    ap.add_argument("--roster", action="store_true")
    ap.add_argument("--death", action="store_true")
    ap.add_argument("--out", default=None)
    A = ap.parse_args()

    src = pathlib.Path(A.src)
    if not src.is_absolute():
        src = (HERE / A.src).resolve()
    out = pathlib.Path(A.out) if A.out else (
        HERE.parent / "05-reference" /
        ("liquid-death.png" if A.death else "liquid-roster.png" if A.roster else "liquid-ingame.png"))

    errs: list[str] = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
        pg = br.new_page(viewport={"width": 700, "height": 1200})
        pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
        pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}")
              if m.type == "error" else None)
        pg.goto(src.as_uri())
        pg.wait_for_function("window.AC && window.AC.WEAPONS && window.__fontsReady !== false",
                             timeout=25000)
        # the two internals the sheet needs, exposed without touching the build
        # Wrapped and returning `true` on purpose: an evaluate() whose last
        # expression IS a function gets CALLED by the harness, with no
        # arguments, which is how this first failed.
        pg.evaluate("() => { window.AC.__hash = shellHash;"
                    "        window.AC.__glass = drawGlassRelic;"
                    "        window.AC.__slosh = SLOSH; return true; }")
        pg.evaluate(DRIVE)

        if A.death:
            r = pg.evaluate("([a,b,s,n,e]) => window.__L.death(a,b,s,n,e)",
                            [A.a, A.b, A.seed, 8, 14])
            print(f"  {r['loser']} died holding {r['deathHp']} HP")
            ims = [png(f["png"]) for f in r["frames"]]
            br.close()
            w, h = ims[0].size
            sc = 0.30
            tw, th = int(w * sc), int(h * sc)
            sheet = Image.new("RGB", (tw * len(ims), th + 22), "#0A0912")
            d = ImageDraw.Draw(sheet)
            for i, im in enumerate(ims):
                sheet.paste(im.resize((tw, th), Image.LANCZOS), (i * tw, 22))
                d.text((i * tw + 6, 6), f"age {r['frames'][i]['age']}s", fill="#8A85A0")
            sheet.save(out)
        elif A.roster:
            ids = pg.evaluate("AC.WEAPONS.map(w => [w.id, w.name, w.aff])")
            HPS = [1.0, 0.74, 0.46, 0.22, 0.06]
            cells, S = {}, 1.0
            for i, (wid, nm, aff) in enumerate(ids):
                for h in HPS:
                    cells[(wid, h)] = png(pg.evaluate(
                        "([i,h,s,t,S]) => window.__L.cell(i,h,s,t,S)",
                        [wid, h, i % 2, 2.4 + h * 3.1, S]))
            br.close()
            cw = cells[(ids[0][0], 1.0)].width
            PADL, PADT = 190, 46
            sheet = Image.new("RGB", (PADL + len(HPS) * cw + 16,
                                      PADT + len(ids) * cw + 78), "#0A0912")
            d = ImageDraw.Draw(sheet)
            for j, h in enumerate(HPS):
                d.text((PADL + j * cw + cw // 2 - 22, 22), f"{round(h*300)} HP", fill="#8A85A0")
            for i, (wid, nm, aff) in enumerate(ids):
                d.text((10, PADT + i * cw + cw // 2 - 6), f"{nm}", fill="#C6C0D5")
                d.text((10, PADT + i * cw + cw // 2 + 8), f"{aff}", fill="#6A6480")
                for j, h in enumerate(HPS):
                    sheet.paste(cells[(wid, h)], (PADL + j * cw, PADT + i * cw))
            # the honest read: the whole roster at the size it is watched
            d.text((PADL, sheet.height - 58), "at 1/3 — phone size", fill="#8A85A0")
            for i, (wid, nm, aff) in enumerate(ids):
                for j, h in enumerate(HPS):
                    th = cells[(wid, h)].resize((cw // 3, cw // 3), Image.LANCZOS)
                    sheet.paste(th, (PADL + (i * len(HPS) + j) * (cw // 3 + 1),
                                     sheet.height - 42))
            sheet.save(out)
        else:
            times = [float(x) for x in A.at.split(",")]
            print(pg.evaluate("([a,b,s]) => window.__L.init(a,b,s)", [A.a, A.b, A.seed]))
            shots = []
            for t in times:
                st = pg.evaluate("([t]) => window.__L.to(t)", [t])
                print("  ", st)
                shots.append(png(pg.evaluate(
                    "() => document.querySelector('canvas').toDataURL('image/png').slice(22)")))
            br.close()
            w, h = shots[0].size
            sc = 0.42
            tw, th = int(w * sc), int(h * sc)
            sheet = Image.new("RGB", (tw * len(shots), th), "#0A0912")
            for i, im in enumerate(shots):
                sheet.paste(im.resize((tw, th), Image.LANCZOS), (i * tw, 0))
            sheet.save(out)

    if errs:
        print("! PAGE ERRORS")
        for e in errs[:10]:
            print("   ", e)
        return 1
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
