"""Card vs plate, at the same VIDEO second, on the same fight and seed.

Not the same SIM second -- the whole point is that the two timelines diverge.
The card freezes the world for 4.0s, so video second 5 shows a fight that is
still standing at 1.86s. The plate does not, so video second 5 shows a fight
that has been going for 5 seconds. This renders both timelines as a viewer
would meet them.
"""
import argparse, base64, pathlib, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

CARD  = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PLATE = pathlib.Path("/home/claude/sc/sc/02-chain/sc-nameplate.html").resolve()

SETUP = """([a,b,seed])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 window.__m=new AC.Match(a,b,seed>>>0);window.__m.introT=0;
 AC.__inject&&AC.__inject(window.__m);AC.__draw(window.__m);return 1;}"""
STEPN = "([n])=>{const dt=AC.CONFIG.physics.dt;for(let i=0;i<n;i++)window.__m.step(dt);return window.__m.t;}"
DRAW  = "()=>{AC.__draw(window.__m);return document.getElementById('cv').toDataURL('image/jpeg',0.92).slice(23);}"
CLANK = """([a,b,seed])=>{const dt=AC.CONFIG.physics.dt;
 const m=new AC.Match(a,b,seed>>>0);m.introT=0;
 for(let k=0;k<Math.round(20/dt)&&!m.over;k++){const c0=m.clankCount;m.step(dt);
   if(m.clankCount>c0) return m.t;} return 2.0;}"""


def timeline(page, a, b, seed, cut, secs, mode, dt):
    """Render `secs` of VIDEO for one build. `cut` is the sim time the overlay
    is raised at. Steps are taken one video-frame at a time so the overlay's
    own clock and the sim clock stay in the relationship the renderer sees."""
    page.evaluate(SETUP, [a, b, seed])
    out, raised, v = [], False, 0.0
    want = list(secs)
    n_per = max(1, int(round(dt ** -1 / 30)))          # ~30 video steps/sec
    step_v = n_per * dt
    guard = 0
    while want and guard < 100000:
        if not raised and v >= cut:
            if mode == "card":
                page.evaluate("()=>{window.__m.introT=AC.CONFIG.intro.dur;}")
            else:
                page.evaluate("()=>{window.__m.plateT=AC.CONFIG.plate.dur;}")
            raised = True
        if want and v >= want[0] - 1e-6:
            out.append((want.pop(0), page.evaluate(DRAW)))
            continue
        page.evaluate(STEPN, [n_per])
        v += step_v
        guard += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="ironhail")
    ap.add_argument("--b", default="oathwound")
    ap.add_argument("--seed", type=int, default=1676955306)
    ap.add_argument("--secs", default="0,2,3,4,5,6,8")
    ap.add_argument("--out", default="/home/claude/tt/nameplate-sheet.png")
    a = ap.parse_args()
    secs = [float(x) for x in a.secs.split(",")]

    with sync_playwright() as p:
        br = p.chromium.launch(args=["--no-sandbox"])
        pc, pp = br.new_page(), br.new_page()
        pc.goto(CARD.as_uri());  pc.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
        pp.goto(PLATE.as_uri()); pp.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
        dt = pp.evaluate("AC.CONFIG.physics.dt")
        cut = pp.evaluate(CLANK, [a.a, a.b, a.seed])
        print(f"  {a.a} v {a.b} seed {a.seed} -- first clank at {cut:.2f}s, overlay raised there")
        rows = [("CARD  (fight frozen 4.0s)", timeline(pc, a.a, a.b, a.seed, cut, secs, "card", dt)),
                ("PLATE (fight never stops)", timeline(pp, a.a, a.b, a.seed, cut, secs, "plate", dt))]
        br.close()

    W, H = 1080, 1920
    sc = 0.155
    w, h = int(W * sc), int(H * sc)
    pad, top, lead = 12, 26, 150
    sheet = Image.new("RGB", (lead + len(secs) * (w + pad), top + 2 * (h + top) + 8), (16, 16, 18))
    d = ImageDraw.Draw(sheet)
    for r, (label, frames) in enumerate(rows):
        y = top + r * (h + top)
        d.text((10, y + h // 2 - 6), label, fill=(226, 220, 205))
        for i, (sec, b64) in enumerate(frames):
            im = Image.open(__import__("io").BytesIO(base64.b64decode(b64))).resize((w, h))
            x = lead + i * (w + pad)
            sheet.paste(im, (x, y))
            if r == 0:
                d.text((x + w // 2 - 22, y - 16), f"{sec:.0f}s", fill=(160, 156, 146))
    sheet.save(a.out)
    print(f"  wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
