"""What would 'scrunch the arena, cards at the bottom' actually look like?

A MOCK, not a build. Nothing is written to 02-chain -- this monkey-patches the
renderer's layout fields at draw time so the question can be answered with a
picture before anything is committed to. Rick has already had one thing built
that was the wrong thing; this is the cheaper order.

THE CONSTRAINT THAT SHAPES EVERYTHING: the hall is 520x800 sim units and the
renderer is width-bound (`scale = aw / CONFIG.arena.w`). Shrinking its height
therefore shrinks its width by the same factor -- the aspect is fixed, and
changing CONFIG.arena is a simulation change that would force a retune. So
scrunching to 65% height costs 35% of the width too, and the slack becomes
empty side margin. That cost is the whole design question and it is what these
frames are for.

The bottom panel reuses `_introTape` verbatim -- the existing VS block, which is
already laid out wide and short and already carries damage / reach / swing
speed / weight. That is information the HUD genuinely does not have, which is
what the name plate got wrong.
"""
import base64, io, pathlib, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

GAME = pathlib.Path("/home/claude/sc/sc/02-chain/sc-cardspin.html").resolve()
A, B, SEED, AT = "ironhail", "oathwound", 1676955306, 3.4
KS = [0.75, 0.65, 0.55]
TAPE_H = 546          # measured from _introTape: 180 lead + 4x84 rows + tail

SETUP = """([a,b,seed,at])=>{
  window.__frozen=true; AC.setResolution(1080,1920);
  AC.SFX.play=function(){}; AC.SFX.resume=function(){};
  const dt=AC.CONFIG.physics.dt;
  const m=new AC.Match(a,b,seed>>>0); m.introT=0;
  AC.__inject&&AC.__inject(m);
  for(let k=0;k<Math.round(at/dt);k++) m.step(dt);
  window.__m=m; return 1;}"""

SCRUNCH = """([k, tapeH])=>{
  const R = AC.renderer, m = window.__m, c = R.ctx;
  const S = {pad:R.pad, aw:R.aw, scale:R.scale, ah:R.ah, arenaTop:R.arenaTop};
  /* the hall, scaled about its own top-centre */
  R.aw = S.aw * k; R.ah = S.ah * k; R.scale = S.scale * k;
  R.pad = (R.W - R.aw) / 2;
  R.arenaTop = S.arenaTop;
  const drawFooter = R.drawFooter;
  R.drawFooter = function(){};                 // it would land inside the panel
  AC.__draw(m);
  R.drawFooter = drawFooter;

  const bottom = R.arenaTop + R.ah;
  const panelY = bottom + 22;
  const panelH = 1812 - panelY;                // 1812 = last row clear of the
                                               // TikTok caption zone
  c.setTransform(R.k,0,0,R.k,0,0);
  c.save();
  c.fillStyle = "#0C0914";
  R.roundRect.call(R, 24, panelY, R.W - 48, panelH, 14); c.fill();
  c.strokeStyle = "#C9A22755"; c.lineWidth = 2;
  R.roundRect.call(R, 24, panelY, R.W - 48, panelH, 14); c.stroke();

  /* the two names, left and right, because the tape identifies its sides by
     COLOUR alone -- in the shipped card the vertical order of the two cards
     taught that mapping, and without them nothing does */
  c.textAlign = "left";
  c.font = "700 34px ui-serif,Georgia,serif";
  c.fillStyle = m.a.aff.core;
  c.fillText(m.a.w.name.toUpperCase(), 56, panelY + 46);
  c.textAlign = "right";
  c.fillStyle = m.b.aff.core;
  c.fillText(m.b.w.name.toUpperCase(), R.W - 56, panelY + 46);

  /* the VS block, scaled to whatever room the scrunch actually left */
  const s = Math.min(1, (panelH - 64) / tapeH);
  c.translate(R.W/2, panelY + 52);
  c.scale(s, s);
  c.translate(-R.W/2, 0);
  R._introTape.call(R, m, 0, 0, 2.0, 1.0);
  c.restore();
  /* hand the layout back untouched -- this is a mock, it must not leak */
  /* GRAB BEFORE RESTORING, and in this same evaluate. An earlier cut restored
     the layout and grabbed in a second call -- and the page's own rAF loop
     redrew a normal frame in the gap, so every 'scrunched' shot was a photo of
     the unscrunched hall. The frames looked plausible, which is what made it
     worth an explicit note. */
  const img = document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23);
  Object.assign(R, S);
  return JSON.stringify({k, arenaW:Math.round(S.aw*k), bottom:Math.round(bottom),
                         panelH:Math.round(panelH), tapeScale:+s.toFixed(2), img});
}"""
GRAB = "()=>document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23)"
CARD = """()=>{const m=window.__m; const s=m.introT; m.introT=AC.CONFIG.intro.dur*0.35;
  AC.__draw(m); m.introT=s; return document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23);}"""

with sync_playwright() as p:
    br = p.chromium.launch(args=["--no-sandbox"]); pg = br.new_page()
    pg.goto(GAME.as_uri()); pg.wait_for_function("window.AC && window.AC.WEAPONS", timeout=30000)
    pg.evaluate(SETUP, [A, B, SEED, AT])
    shots = []
    shots.append(("NOW — fight, no overlay",
                  pg.evaluate("()=>{AC.__draw(window.__m);return document.getElementById('cv').toDataURL('image/jpeg',0.93).slice(23);}")))
    shots.append(("NOW — the card (fight frozen)", pg.evaluate(CARD)))
    import json as _j
    for k in KS:
        r = _j.loads(pg.evaluate(SCRUNCH, [k, TAPE_H]))
        img = r.pop("img")
        print("  ", r)
        shots.append((f"SCRUNCH {int(k*100)}%  (fight running)", img))
    br.close()

sc = 0.30
w, h = int(1080*sc), int(1920*sc)
pad, top = 16, 30
sheet = Image.new("RGB", (pad + len(shots)*(w+pad), top + h + pad), (16,16,18))
d = ImageDraw.Draw(sheet)
for i,(lab,b64) in enumerate(shots):
    im = Image.open(io.BytesIO(base64.b64decode(b64))).resize((w,h))
    x = pad + i*(w+pad); sheet.paste(im, (x, top))
    d.text((x+2, top-18), lab, fill=(222,216,202))
sheet.save("/home/claude/tt/scrunch-mock.png")
print("  wrote /home/claude/tt/scrunch-mock.png", sheet.size)
