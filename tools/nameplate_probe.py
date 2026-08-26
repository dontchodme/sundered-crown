"""Does the name plate do the one thing it exists to do -- leave the fight running?

Six checks, each written so it can FAIL. Two of them are controls, because a
discriminator with no negative case discriminates nothing (the lesson coldopen2
learned the hard way).

The headline claim is falsifiable in one line: with the CARD up the match clock
does not move, and with the PLATE up it must.
"""
import base64, io, json, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

CARD  = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
PLATE = pathlib.Path("/home/claude/sc/sc/02-chain/sc-nameplate.html").resolve()
A, B, SEED = "ironhail", "oathwound", 1676955306          # short-10, the shipped fight
PAIRS = [("ironhail","oathwound"),("emberedge","thornwake"),("dawnbringer","censer"),
         ("gravemourn","heartwood"),("axiom","nightfell"),("slagheart","lightkeeper")]

# The plate covers screen y 172-372. To prove the fight is LIVE we must look at
# rows the plate does not touch; to prove the plate is DRAWN we look only at the
# rows it does. Two disjoint band sets, one per question.
HALL_BANDS  = [(420, 1800)]        # the hall, well below the plate
PLATE_BANDS = None                 # read from the build's own CONFIG at runtime,
BELOW_BANDS = None                 # so this probe cannot go stale when it moves

SETUP = """([a,b,seed])=>{window.__frozen=true;AC.setResolution(1080,1920);
 AC.SFX.play=function(){};AC.SFX.resume=function(){};
 window.__m=new AC.Match(a,b,seed>>>0);window.__m.introT=0;
 AC.__inject&&AC.__inject(window.__m);AC.__draw(window.__m);return 1;}"""
STEP = "([n])=>{const dt=AC.CONFIG.physics.dt;for(let i=0;i<n;i++)window.__m.step(dt);AC.__draw(window.__m);return window.__m.t;}"
GRAB = "()=>document.getElementById('cv').toDataURL('image/jpeg',0.95).slice(23)"

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
        for i in range(0, len(ca), 5):
            tot += abs(ca[i] - cb[i]); n += 1
    return tot / n

with sync_playwright() as p:
    br = p.chromium.launch(args=["--no-sandbox"])
    pc, pp = br.new_page(), br.new_page()
    pc.goto(CARD.as_uri());  pc.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    pp.goto(PLATE.as_uri()); pp.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    dt = pp.evaluate("AC.CONFIG.physics.dt")
    P = pp.evaluate("AC.CONFIG.plate")
    PLATE_BANDS = [(int(P["y"]) + 4, int(P["y"] + P["h"]) - 4)]
    BELOW_BANDS = [(int(P["y"] + P["h"]) + 24, 1800)]
    print(f"  plate band from CONFIG: y {P['y']}-{P['y']+P['h']}, dur {P['dur']}s")

    print(f"\n  card build  {CARD.name}\n  plate build {PLATE.name}\n")

    # ---- [1] the simulation is untouched, across the roster --------------
    same = []
    for a, b in PAIRS:
        for i in range(12):
            s = (20260819 + i * 7919) & 0xFFFFFFFF
            ra = json.loads(pc.evaluate("([a,b,s])=>JSON.stringify(AC.simulate(a,b,s>>>0))", [a, b, s]))
            rb = json.loads(pp.evaluate("([a,b,s])=>JSON.stringify(AC.simulate(a,b,s>>>0))", [a, b, s]))
            same.append(ra == rb)
    check(all(same), "[1] engine_ab: 72 matches simulate identically in both builds",
          f"{sum(same)}/{len(same)} identical")

    # ---- [2] THE HEADLINE. Does the clock move under the overlay? --------
    n3 = int(round(3.0 / dt))
    pc.evaluate(SETUP, [A, B, SEED]); pc.evaluate("()=>{window.__m.introT=AC.CONFIG.intro.dur;}")
    t_card = pc.evaluate(STEP, [n3])
    pp.evaluate(SETUP, [A, B, SEED]); pp.evaluate("()=>{window.__m.plateT=AC.CONFIG.plate.dur;}")
    t_plate = pp.evaluate(STEP, [n3])
    check(t_card < 0.001, "[2a] CONTROL -- with the CARD up, 3s of stepping moves the clock 0.00s",
          f"m.t = {t_card:.4f}s")
    check(abs(t_plate - 3.0) < 0.05, "[2b] with the PLATE up, 3s of stepping moves the clock 3s",
          f"m.t = {t_plate:.4f}s  (card build: {t_card:.4f}s)")

    # ---- [3] the hall behind the plate is a LIVE fight -------------------
    def shot(page, at, plate):
        page.evaluate(SETUP, [A, B, SEED])
        if plate: page.evaluate("()=>{window.__m.plateT=AC.CONFIG.plate.dur;}")
        if at: page.evaluate(STEP, [int(round(at / dt))])
        else:  page.evaluate("()=>AC.__draw(window.__m)")
        return page.evaluate(GRAB)

    live0 = shot(pp, 0.0, True)
    live0b = shot(pp, 0.0, True)          # the CONTROL: same state, twice
    live1 = shot(pp, 1.2, True)           # 1.2s in, plate still up (dur 3.0)
    null = band_diff(live0, live0b, HALL_BANDS)
    live = band_diff(live0, live1, HALL_BANDS)
    check(null < 0.20, "[3a] CONTROL -- the same frame twice reads ~0 in the hall bands",
          f"mean |diff| {null:.3f}")
    check(live > 2.0, "[3b] the hall MOVES while the plate is up",
          f"mean |diff| {live:.3f} vs control {null:.3f}")

    # ---- [4] the plate is actually drawn, and actually leaves ------------
    bare = shot(pp, 1.2, False)           # same moment, plate never raised
    drawn = band_diff(live1, bare, PLATE_BANDS)
    check(drawn > 8.0, "[4a] the plate band differs from the same frame without it",
          f"mean |diff| {drawn:.3f} in rows {PLATE_BANDS[0]}")
    # A stronger claim than "it is drawn": the occlusion is BOUNDED. Everything
    # below the plate must be byte-for-byte what it would be with no plate at
    # all -- otherwise the plate is eating hall the occupancy probe never
    # cleared it to eat.
    spill = band_diff(live1, bare, BELOW_BANDS)
    check(spill < 0.05, "[4c] nothing below the plate changes -- the occlusion is bounded",
          f"mean |diff| {spill:.4f} in rows {BELOW_BANDS[0]}")
    pp.evaluate(SETUP, [A, B, SEED])
    pp.evaluate("()=>{window.__m.plateT=AC.CONFIG.plate.dur;}")
    pp.evaluate(STEP, [int(round(3.6 / dt))])
    gone = pp.evaluate(GRAB)
    pp.evaluate(SETUP, [A, B, SEED]); pp.evaluate(STEP, [int(round(3.6 / dt))])
    gone_bare = pp.evaluate(GRAB)
    check(band_diff(gone, gone_bare, PLATE_BANDS) < 0.20,
          "[4b] by 3.6s the plate is GONE -- frame is identical to one that never had it",
          f"mean |diff| {band_diff(gone, gone_bare, PLATE_BANDS):.3f}")

    br.close()

print(f"\n  {'ALL PASS' if not fails else str(fails) + ' FAILED'}")
sys.exit(1 if fails else 0)
