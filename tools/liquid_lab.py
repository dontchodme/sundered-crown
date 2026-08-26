#!/usr/bin/env python3
"""The glass/liquid lab: build the standalone page, and shoot it.

The look is judged here, on pictures, BEFORE a line of it goes near the game.
Three of the last four visual passes in this project shipped code that was
correct and a picture that was wrong, and every one of them was caught by a
contact sheet rather than by reading the diff.

    python3 liquid_lab.py --sheet    ../05-reference/liquid-sheet.png
    python3 liquid_lab.py --hall     ../05-reference/liquid-hall.png
    python3 liquid_lab.py --strip    ../05-reference/liquid-strip.png
"""
from __future__ import annotations
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
CORE = HERE.parent / "04-experiments" / "_liquid_core.js"
LAB  = HERE.parent / "04-experiments" / "liquid-lab.html"

PRELUDE = r"""
const TAU = Math.PI * 2;
const clamp = (v,a,b) => Math.max(a, Math.min(b, v));
const lerp  = (a,b,t) => a + (b-a)*t;
const AFFINITIES = {
  sanctified: { key:"sanctified", name:"Sanctified", core:"#FFF6E2", glow:"#FFFFFF", dark:"#5A4E30" },
  bloodsworn: { key:"bloodsworn", name:"Bloodsworn", core:"#E03A4E", glow:"#FF97A2", dark:"#450710" },
  dwarven:    { key:"dwarven",    name:"Dwarven",    core:"#9C6326", glow:"#E8A34E", dark:"#2E1B0A" },
  verdant:    { key:"verdant",    name:"Verdant",    core:"#4FD06B", glow:"#BCF7C7", dark:"#0D3A1A" },
  umbral:     { key:"umbral",     name:"Umbral",     core:"#A45CF0", glow:"#DDB8FF", dark:"#280A44" },
  runic:      { key:"runic",      name:"Runic",      core:"#4A9EFF", glow:"#BCDDFF", dark:"#08264F" },
  vigil:      { key:"vigil",      name:"Vigil",      core:"#F06BB8", glow:"#FFD1EC", dark:"#4A0A31" },
};
const ROSTER = [
  ["dawnbringer","Dawnbringer","sanctified"],["widowmaker","Widowmaker","bloodsworn"],
  ["grudgebearer","Grudgebearer","dwarven"],["thornwake","Thornwake","verdant"],
  ["lastlight","Lastlight","sanctified"],["gravemourn","Gravemourn","umbral"],
  ["slagheart","Slagheart","dwarven"],["spellbreaker","Spellbreaker","runic"],
  ["ironhail","Ironhail","dwarven"],["lightkeeper","Lightkeeper","vigil"],
  ["farwarden","Farwarden","vigil"],["aureole","Aureole","sanctified"],
  ["censer","Censer","sanctified"],["emberedge","Emberedge","dwarven"],
  ["oathwound","Goreshard","bloodsworn"],["heartwood","Heartwood","verdant"],
  ["nightfell","Nightfell","umbral"],["axiom","Axiom","runic"],
];
function shellHash(a, b){
  let h = (Math.imul(a + 1, 374761393) + Math.imul(b + 1, 668265263)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177) | 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
"""

HARNESS = r"""
/* ------------------------------------------------------------- THE LAB --- */
const SCALE = 1080 / 520;              // the game's own arena scale, exactly
const R     = 34;                      // sim units
const BASE  = 300;

function mkF(side, affKey, hp, ghost, maxHp){
  return { side, aff: AFFINITIES[affKey], x: 0, y: 0, vx: 0, vy: 0,
           hp, hpGhost: ghost == null ? hp : ghost, maxHp: maxHp == null ? BASE : maxHp,
           mend: 0, flash: 0, slTilt: 0, slTiltV: 0, slHeave: 0, slHeaveV: 0,
           slA2: 0, slA2V: 0, slA3: 0, slA3V: 0, slVx: 0, slVy: 0, slJolt: 0 };
}

function bg(c, w, h){
  const g = c.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, "#0B0A12"); g.addColorStop(1, "#07060D");
  c.fillStyle = g; c.fillRect(0, 0, w, h);
}

/* ---- SHEET: every school against every stage of the fight, at 1:1 ------- */
function sheet(){
  const HPS  = [1.0, 0.78, 0.52, 0.30, 0.12, 0.03];
  const rows = Object.keys(AFFINITIES);
  const CELL = Math.round(R * 2.5 * SCALE);       // 207 px, ball is 138
  const PADL = 150, PADT = 54;
  const cv = document.getElementById("cv");
  cv.width  = PADL + HPS.length * CELL + 20;
  cv.height = PADT + rows.length * CELL + 90;
  const c = cv.getContext("2d");
  bg(c, cv.width, cv.height);
  c.font = "600 15px ui-monospace,monospace"; c.fillStyle = "#8A85A0";
  HPS.forEach((hp, i) => {
    c.textAlign = "center";
    c.fillText(Math.round(hp * BASE) + " HP", PADL + i * CELL + CELL / 2, 32);
  });
  rows.forEach((k, r) => {
    c.textAlign = "right"; c.fillStyle = AFFINITIES[k].core;
    c.fillText(k, PADL - 14, PADT + r * CELL + CELL / 2 + 5);
    HPS.forEach((hp, i) => {
      const f = mkF(r % 2, k, hp * BASE, Math.min(1, hp + 0.10) * BASE);
      /* a plausible mid-slosh, so the sheet is not judging a still pond */
      f.slTilt = (shellHash(r * 7 + i, 3) - 0.5) * 0.55;
      f.slA2   = (shellHash(r * 7 + i, 5) - 0.5) * 0.12;
      f.slA3   = (shellHash(r * 7 + i, 9) - 0.5) * 0.08;
      f.slJolt = 0.4;
      MARKS.mode = Q.get("marks") || "none";
      c.save();
      c.translate(PADL + i * CELL + CELL / 2, PADT + r * CELL + CELL / 2);
      c.scale(SCALE, SCALE);
      drawGlassRelic(c, { t: 3.1 + i * 0.7 }, f, R, { base: BASE });
      c.restore();
    });
  });
  /* the phone strip: the same row at the size it is actually watched */
  c.textAlign = "left"; c.fillStyle = "#8A85A0";
  c.fillText("at 1/3 — phone size", PADL, cv.height - 58);
  rows.forEach((k, r) => {
    HPS.forEach((hp, i) => {
      const f = mkF(r % 2, k, hp * BASE, Math.min(1, hp + 0.10) * BASE);
      f.slTilt = (shellHash(r * 7 + i, 3) - 0.5) * 0.55;
      c.save();
      c.translate(PADL + (r * HPS.length + i) * 26 + 13, cv.height - 26);
      c.scale(SCALE / 3, SCALE / 3);
      drawGlassRelic(c, { t: 3.1 }, f, R, { base: BASE });
      c.restore();
    });
  });
}

/* ---- HALL: the real physics, so the slosh is judged in motion ----------- */
const HALL = { w: 520, h: 800, gravity: 900, cruise: 405, relax: 0.62,
               speedMin: 250, speedMax: 1300, heightVary: 1.0, floorBounce: 0.97 };
let balls = [], simT = 0;
function hallInit(seed){
  balls = [mkF(0, "bloodsworn", 300), mkF(1, "runic", 300)];
  balls.forEach((f, i) => {
    f.x = 140 + i * 240; f.y = 260 + i * 180;
    const a = shellHash(seed + i, 1) * TAU;
    f.vx = Math.cos(a) * 480; f.vy = Math.sin(a) * 480;
    f.slVx = f.vx; f.slVy = f.vy;
  });
  simT = 0;
}
function hallStep(dt){
  simT += dt;
  for (const f of balls){
    f.vy += HALL.gravity * dt;
    f.x += f.vx * dt; f.y += f.vy * dt;
    const lo = 12 + R, hiX = HALL.w - 12 - R, hiY = HALL.h - 12 - R;
    if (f.x < lo){ f.x = lo; f.vx = Math.abs(f.vx); }
    if (f.x > hiX){ f.x = hiX; f.vx = -Math.abs(f.vx); }
    if (f.y < lo){ f.y = lo; f.vy = Math.abs(f.vy); }
    if (f.y > hiY){ f.y = hiY; f.vy = -Math.abs(f.vy) * HALL.floorBounce; }
    const sp0 = Math.hypot(f.vx, f.vy);
    if (sp0 > 1e-6){
      const k = 1 - Math.exp(-HALL.relax * dt);
      const drop = clamp(hiY - f.y, 0, hiY - lo);
      const e = HALL.cruise * HALL.cruise + 2 * HALL.gravity * HALL.heightVary * ((hiY - lo) * 0.5 - drop);
      const target = Math.sqrt(Math.max(HALL.speedMin * HALL.speedMin, e));
      const sp = clamp(sp0 + (target - sp0) * k, HALL.speedMin, HALL.speedMax);
      f.vx *= sp / sp0; f.vy *= sp / sp0;
    }
    SLOSH.step(f, dt, HALL.gravity);
    f.hp = Math.max(6, f.hp - dt * 7.5);
    if (f.hpGhost == null) f.hpGhost = f.hp;
    f.hpGhost += (f.hp - f.hpGhost) * (1 - Math.exp(-5.5 * dt));
  }
}
function hallDraw(){
  const cv = document.getElementById("cv");
  cv.width = Math.round(HALL.w * SCALE); cv.height = Math.round(HALL.h * SCALE);
  const c = cv.getContext("2d");
  bg(c, cv.width, cv.height);
  c.save(); c.scale(SCALE, SCALE);
  c.strokeStyle = "#241D33"; c.lineWidth = 2;
  c.strokeRect(12, 12, HALL.w - 24, HALL.h - 24);
  for (const f of balls) drawGlassRelic(c, { t: simT }, f, R, { base: BASE });
  c.restore();
}
window.__hall = { init: hallInit, step: hallStep, draw: hallDraw };

/* ---- STRIP: one relic, one bounce, frame by frame ----------------------- */
function strip(affKey, frames, dtPer){
  const cv = document.getElementById("cv");
  const CELL = Math.round(R * 2.5 * SCALE);
  cv.width = frames * CELL; cv.height = CELL + 30;
  const c = cv.getContext("2d");
  bg(c, cv.width, cv.height);
  const f = mkF(0, affKey, 300 * 0.62, 300 * 0.72);
  f.x = 260; f.y = 700; f.vx = 520; f.vy = 780; f.slVx = f.vx; f.slVy = f.vy;
  let t = 0;
  for (let i = 0; i < frames; i++){
    for (let s = 0; s < Math.round(dtPer / (1/120)); s++){
      const dt = 1/120; t += dt;
      f.vy += HALL.gravity * dt; f.x += f.vx * dt; f.y += f.vy * dt;
      const hiY = HALL.h - 12 - R, hiX = HALL.w - 12 - R, lo = 12 + R;
      if (f.y > hiY){ f.y = hiY; f.vy = -Math.abs(f.vy) * 0.97; }
      if (f.x > hiX){ f.x = hiX; f.vx = -Math.abs(f.vx); }
      if (f.x < lo){ f.x = lo; f.vx = Math.abs(f.vx); }
      SLOSH.step(f, dt, HALL.gravity);
    }
    c.save();
    c.translate(i * CELL + CELL / 2, CELL / 2 + 8);
    c.scale(SCALE, SCALE);
    const sx = f.x, sy = f.y; f.x = 0; f.y = 0;
    drawGlassRelic(c, { t }, f, R, { base: BASE });
    f.x = sx; f.y = sy;
    c.restore();
    c.fillStyle = "#8A85A0"; c.font = "500 12px ui-monospace,monospace";
    c.textAlign = "center";
    c.fillText("t=" + t.toFixed(2), i * CELL + CELL / 2, cv.height - 8);
  }
}
window.__sheet = sheet; window.__strip = strip;
const Q = new URLSearchParams(location.search);
MARKS.mode = Q.get("marks") || "none";
if (Q.get("mode") === "sheet") sheet();
else if (Q.get("mode") === "strip") strip(Q.get("aff") || "bloodsworn", 10, 0.055);
else { hallInit(7); hallDraw();
       (function loop(){ for (let i=0;i<2;i++) hallStep(1/120); hallDraw(); requestAnimationFrame(loop); })(); }
window.__labReady = true;
"""

TEMPLATE = """<!doctype html><meta charset="utf-8">
<title>liquid lab</title>
<style>html,body{{margin:0;background:#08070E;}}canvas{{display:block;margin:0 auto;}}</style>
<canvas id="cv"></canvas>
<script>
{prelude}
{core}
{harness}
</script>
"""


def build() -> pathlib.Path:
    LAB.parent.mkdir(parents=True, exist_ok=True)
    LAB.write_text(TEMPLATE.format(prelude=PRELUDE, core=CORE.read_text(), harness=HARNESS))
    return LAB


def shot(mode: str, out: pathlib.Path, aff: str = "bloodsworn", settle: int = 0, marks: str = "none"):
    build()
    errs: list[str] = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, args=["--disable-gpu", "--no-sandbox"])
        pg = b.new_page(viewport={"width": 1400, "height": 1000},
                        device_scale_factor=1)
        pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
        pg.on("console", lambda m: errs.append(f"console.{m.type}: {m.text}")
              if m.type == "error" else None)
        pg.goto(LAB.as_uri() + f"?mode={mode}&aff={aff}&marks={marks}")
        pg.wait_for_function("window.__labReady === true", timeout=15000)
        if settle:
            pg.wait_for_timeout(settle)
        out.parent.mkdir(parents=True, exist_ok=True)
        pg.locator("#cv").screenshot(path=str(out))
        b.close()
    if errs:
        print("PAGE ERRORS:")
        for e in errs[:12]:
            print("   ", e)
        return 1
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="sheet", choices=["sheet", "hall", "strip"])
    ap.add_argument("--aff", default="bloodsworn")
    ap.add_argument("--settle", type=int, default=0)
    ap.add_argument("--marks", default="none", choices=["none","desperation","ticks"])
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = pathlib.Path(a.out) if a.out else HERE.parent / "05-reference" / f"liquid-{a.mode}.png"
    return shot(a.mode, out, a.aff, a.settle, a.marks)


if __name__ == "__main__":
    sys.exit(main())
