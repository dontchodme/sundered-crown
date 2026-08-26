"""Is the scrunch presentation-only, and is the fight actually running under it?

Same discipline as nameplate_probe: every check can fail, and the ones that
matter carry a control. The headline is the same one-liner -- the card stops the
match clock, this must not.
"""
import base64, io, json, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

import sys as _s
# base build (no scrunch) and the scrunched build under test; overridable so the
# same probe covers sc-scrunch (vs sc-cardspin) and sc-healthscrunch (vs sc-health)
CARD    = pathlib.Path(_s.argv[1] if len(_s.argv) > 1 else
                       "/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
SCRUNCH = pathlib.Path(_s.argv[2] if len(_s.argv) > 2 else
                       "/home/claude/sc/sc/02-chain/sc-scrunch.html").resolve()
A, B, SEED = "ironhail", "oathwound", 1676955306
# Pairs are derived from the ROSTER THE BUILDS ACTUALLY SHARE, not hardcoded.
# 01-live carries 16 relics and the chain carries 17 -- slagheart was added
# downstream -- so a fixed pair list throws "Unknown relic id" on the older
# build, which is a probe fault reported as a build failure.
PAIRS = None

SETUP = """([a,b,seed,auto])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 const m=new AC.Match(a,b,seed>>>0); m.introT=0;
 AC.__inject(m); m.scrunchAuto=auto; window.__m=m; return 1;}"""
# `m.shake` feeds Math.random() straight into draw()'s translate, so drawing
# the SAME match state twice does not produce the same pixels whenever a shake
# is live. That is PRE-EXISTING and documented (v26 section 4: "worth a seeded
# rng for shake ... if renders are ever expected to be reproducible") --
# measured at 0.697 on the UNPATCHED 01-live build against 0.000 on the chain
# tip. The image checks below zero it before drawing so they measure the hall,
# not the RNG. It is the probe doing this, not the build.
RUN = """([sec])=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
 for(let i=0;i<Math.round(sec/dt);i++) m.step(dt);
 m.shake = 0;
 AC.__draw(m);
 return {img:document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23),
         t:+m.t.toFixed(4), mode:m.scrunchMode};}"""

fails = 0
def check(ok, name, detail=""):
    global fails
    if not ok: fails += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  -- {detail}" if detail else ""))

def band_diff(p1, p2, bands):
    a = Image.open(io.BytesIO(base64.b64decode(p1))).convert("L")
    b = Image.open(io.BytesIO(base64.b64decode(p2))).convert("L")
    tot = n = 0
    for y0, y1 in bands:
        ca = a.crop((0, y0, 1080, y1)).tobytes(); cb = b.crop((0, y0, 1080, y1)).tobytes()
        for i in range(0, len(ca), 5): tot += abs(ca[i]-cb[i]); n += 1
    return tot / n

with sync_playwright() as p:
    br = p.chromium.launch(args=["--no-sandbox"])
    pc, ps = br.new_page(), br.new_page()
    errs = []
    ps.on("pageerror", lambda e: errs.append(str(e)))
    pc.goto(CARD.as_uri());    pc.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    ps.goto(SCRUNCH.as_uri()); ps.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    ra_ids = pc.evaluate("AC.WEAPONS.map(w => w.id)")
    rb_ids = ps.evaluate("AC.WEAPONS.map(w => w.id)")
    shared = [i for i in ra_ids if i in rb_ids]
    PAIRS = [(shared[i], shared[(i * 5 + 3) % len(shared)])
             for i in range(6)]
    PAIRS = [(a, b) for a, b in PAIRS if a != b]
    print(f"  rosters: base {len(ra_ids)}, patched {len(rb_ids)}, shared {len(shared)}")
    print(f"  pairs:   {', '.join(a + ' v ' + b for a, b in PAIRS)}")
    S = ps.evaluate("AC.CONFIG.scrunch")
    # Sample the hold RELATIVE to the first clank, which is what arms the
    # scrunch. A fixed 3.2s assumed a ~2.0s clank; on 01-live the same seed
    # is a different fight and the ease was still running at that moment, so
    # the probe reported k=0.7086 as a build failure when it was a sampling
    # one.
    CLANK = ps.evaluate("""([a,b,seed])=>{const dt=AC.CONFIG.physics.dt;
      const m=new AC.Match(a,b,seed>>>0); m.introT=0;
      for(let k=0;k<Math.round(20/dt)&&!m.over;k++){const c0=m.clankCount;
        m.step(dt); if(m.clankCount>c0) return m.t;} return 2.0;}""", [A, B, SEED])
    HOLD_AT = CLANK + S["ease"] + 0.6
    LATE_AT = CLANK + S["ease"] + 2.0
    BACK_AT = CLANK + S["ease"] * 2 + S["intro"] + 1.5
    print(f"  first clank {CLANK:.2f}s -> sampling the hold at {HOLD_AT:.2f}s")
    print(f"\n  CONFIG.scrunch: k={S['k']} ease={S['ease']} intro={S['intro']}\n")

    # ---- [1] the simulation is untouched -------------------------------
    same = []
    for a, b in PAIRS:
        for i in range(12):
            sd = (20260819 + i*7919) & 0xFFFFFFFF
            ra = json.loads(pc.evaluate("([a,b,s])=>JSON.stringify(AC.simulate(a,b,s>>>0))", [a,b,sd]))
            rb = json.loads(ps.evaluate("([a,b,s])=>JSON.stringify(AC.simulate(a,b,s>>>0))", [a,b,sd]))
            same.append(ra == rb)
    check(all(same), "[1] engine_ab: 72 matches simulate identically in both builds",
          f"{sum(same)}/{len(same)}")

    # ---- [2] the clock. THE HEADLINE ------------------------------------
    pc.evaluate(SETUP, [A, B, SEED, False])
    pc.evaluate("()=>{window.__m.introT=AC.CONFIG.intro.dur;}")
    t_card = pc.evaluate(RUN, [3.0])["t"]
    ps.evaluate(SETUP, [A, B, SEED, True])
    r = ps.evaluate(RUN, [3.0])
    check(t_card < 0.001, "[2a] CONTROL -- the CARD build's clock does not move in 3s",
          f"m.t = {t_card:.4f}s")
    check(abs(r["t"] - 3.0) < 0.05 and r["mode"] == "tape",
          "[2b] the SCRUNCH build's clock moves 3s and the tape is armed",
          f"m.t = {r['t']:.4f}s, mode = {r['mode']}")

    # ---- [3] the hall is live while the panel is up ---------------------
    def at(sec, auto=True):
        ps.evaluate(SETUP, [A, B, SEED, auto])
        return ps.evaluate(RUN, [sec])
    HALL = [(200, 1200)]
    a1, a1b = at(HOLD_AT)["img"], at(HOLD_AT)["img"]
    a2 = at(LATE_AT)["img"]
    check(band_diff(a1, a1b, HALL) < 0.20, "[3a] CONTROL -- the same moment twice reads ~0 in the hall",
          f"{band_diff(a1,a1b,HALL):.3f}")
    check(band_diff(a1, a2, HALL) > 2.0, "[3b] the hall MOVES while the panel is up",
          f"{band_diff(a1,a2,HALL):.3f}")

    # ---- [4] the hall really is smaller, and really does come back ------
    full = at(max(0.3, CLANK - 0.6))["img"]   # before the first clank
    held = at(HOLD_AT)["img"]
    back = at(BACK_AT)["img"]
    LOWER = [(1290, 1800)]                   # hall at full size; empty when scrunched
    check(band_diff(full, held, LOWER) > 1.0, "[4a] the frame changes below the scrunched hall",
          f"{band_diff(full,held,LOWER):.3f}")
    ks = ps.evaluate("()=>AC.renderer ? null : null")
    kh = at(HOLD_AT); kb = at(BACK_AT)
    kk = ps.evaluate("()=>({k:AC.renderer.scrunchK(window.__m), pad:AC.renderer.pad, aw:AC.renderer.aw})")
    check(abs(kk["aw"] - 1056) < 0.5 and abs(kk["pad"] - 12) < 0.5,
          "[4b] the layout fields are handed back untouched after every draw",
          f"aw={kk['aw']:.1f} pad={kk['pad']:.1f} (design: 1056 / 12)")
    ps.evaluate(SETUP, [A, B, SEED, True]); ps.evaluate(RUN, [BACK_AT])
    kback = ps.evaluate("()=>AC.renderer.scrunchK(window.__m)")
    check(kback > 0.999, f"[4c] by {BACK_AT:.1f}s the hall is back to full size", f"k = {kback:.4f}")
    kmid = None
    ps.evaluate(SETUP, [A, B, SEED, True]); ps.evaluate(RUN, [HOLD_AT])
    kmid = ps.evaluate("()=>AC.renderer.scrunchK(window.__m)")
    check(abs(kmid - S["k"]) < 0.001, "[4d] during the hold the hall sits exactly at CONFIG.scrunch.k",
          f"k = {kmid:.4f}")

    # ---- [5] the verdict panel, and the scrim that must NOT appear ------
    ps.evaluate(SETUP, [A, B, SEED, True])
    end = ps.evaluate("""()=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
      let g=0; while(!m.over && g++<40000) m.step(dt);
      for(let i=0;i<Math.round(2.2/dt);i++) m.step(dt);
      AC.__draw(m);
      return {mode:m.scrunchMode, hp:Math.ceil(m.winner.hp),
              img:document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23)};}""")
    check(end["mode"] == "result", "[5a] the verdict beat arms after the kill", f"mode = {end['mode']}")
    px = Image.open(io.BytesIO(base64.b64decode(end["img"]))).convert("L")
    hall_lum = sum(px.crop((100, 300, 980, 1100)).tobytes()[::7]) / len(px.crop((100,300,980,1100)).tobytes()[::7])
    ps.evaluate(SETUP, [A, B, SEED, False])          # scrunch OFF -> the old full-screen card
    end2 = ps.evaluate("""()=>{const dt=AC.CONFIG.physics.dt,m=window.__m;
      let g=0; while(!m.over && g++<40000) m.step(dt);
      for(let i=0;i<Math.round(2.2/dt);i++) m.step(dt);
      AC.__draw(m);
      return document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23);}""")
    px2 = Image.open(io.BytesIO(base64.b64decode(end2))).convert("L")
    hall_lum2 = sum(px2.crop((100,300,980,1100)).tobytes()[::7]) / len(px2.crop((100,300,980,1100)).tobytes()[::7])
    check(end["hp"] > 0, "[5b] the verdict has an HP number to state", f"{end['hp']} HP")
    print(f"        hall luminance at the verdict: scrunch {hall_lum:.1f}  vs  full-screen card {hall_lum2:.1f}")
    check(hall_lum > hall_lum2, "[5c] the hall is BRIGHTER at the verdict than under the old card"
                                " -- the shatter is not behind a scrim",
          f"{hall_lum:.1f} vs {hall_lum2:.1f}")
    check(not errs, "[6] no page errors", str(errs[:2]))
    br.close()

print(f"\n  {'ALL PASS' if not fails else str(fails) + ' FAILED'}")
sys.exit(1 if fails else 0)
