#!/usr/bin/env python3
"""THE NEW FIGHTERS, AS A CLICKABLE REVIEW PAGE.

    python3 fighter_review.py --game sc-gs7.html --out fighter-review.html

`wording_sheet.py` reviews the STRINGS. This reviews the FIGHTER: what it looks
like posed on the card, what it looks like mid-fight, what its outline is with
the colour stripped off, and every field a change would edit — art branch,
status, ultimate, stats, damage — each naming its exact anchor.

Same contract as the wording sheet, for the same reason: every value is read
out of the build's own `WEAPONS` / `STATUS` / `AFFINITIES` through the same
`relicStatus` / `relicShot` calls the renderer uses, so the review page cannot
drift from what actually renders. Images are captured from the build itself at
1080x1920 and embedded as data URLs, so the file is self-contained and survives
being mailed around.

Click any row to attach a note. Export writes a JSON block naming the data field
each note edits, so the reply maps straight onto anchors.

WHAT IT DELIBERATELY SHOWS THAT IS NOT FLATTERING
-------------------------------------------------
The "ULT ART" row reports whether the relic has a `drawUltUnder` / `drawUltOver`
branch at all, because ult art is dispatched per relic id and a relic without a
branch fires a working ultimate that draws nothing. Ten of sixteen relics are in
that state, and a review page that showed only the pretty card would hide it.
"""
from __future__ import annotations
import argparse, base64, html, io, json, pathlib, sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scpage import game

HERE = pathlib.Path(__file__).parent

CARD_JS = """([a, b, seed, e]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const m = new AC.Match(a, b, seed);
  AC.__inject && AC.__inject(m);
  m.introT = e === null ? 0 : Math.max(0, AC.CONFIG.intro.dur - e);
  if (e === null) for (let i = 0; i < 150; i++) m.step(1/60);
  AC.__draw(m);
  return document.getElementById('cv').toDataURL('image/png');
}"""

# The silhouette, colour stripped — the same question silhouette_probe asks,
# asked here per relic so it sits next to the thing it is a test of.
SIL_JS = """([id, S]) => {
  const w = AC.WEAPONS.find(x => x.id === id);
  const cv = document.createElement('canvas');
  cv.width = S; cv.height = Math.round(S * 0.52);
  const c = cv.getContext('2d');
  c.fillStyle = '#0A0810'; c.fillRect(0, 0, cv.width, cv.height);
  /* The palette must be a REAL affinity object with every field the shape
     reads — `key` above all, which is what the per-school structural branches
     switch on. Flatten only the colour fields. Building a bare {core, glow, …}
     literal instead throws inside `_facet`, which is what the first version of
     this did. Same construction as silhouette_probe.py.
     NOT --footprint: hardcoded near-black literals are not flattened here. The
     greatswords are <=10% invisible that way (blind-ink doc), which is fine for
     a thumbnail and would not be for a measurement. */
  const p = Object.assign({}, AC.AFFINITIES[w.aff]);
  p.core = p.glow = p.steel = p.dark = "#FFFFFF";
  AC.SHAPES._t = 0.6;
  /* L and W must keep the TYPE's real proportions — a greatsword is
     reach 116 / artW 40, so W/L is 0.345. Drawing it at 0.16 (which the first
     version did) makes a different object: the barbs, the thorn hook and the
     shard gaps are all sized off W, and they collapse into a plain blade at
     half thickness. Read them off the relic instead of choosing them. */
  const L = S * 0.62, W = L * (w.artW / w.reach);
  c.save();
  c.translate(S * 0.13, cv.height / 2);
  AC.SHAPES[w.shape](c, L, W, p, null, w.aff);
  c.restore();
  return cv.toDataURL('image/png');
}"""

FACTS_JS = """([ids]) => {
  const src = document.documentElement.outerHTML;
  return ids.map(id => {
    const w = AC.WEAPONS.find(x => x.id === id);
    const aff = AC.AFFINITIES[w.aff];
    const rs = AC.relicStatus(w);
    const n = (w.onHit && w.onHit[rs.key]) || (w.onSelf && w.onSelf[rs.key]) || 1;
    return {
      id, name: w.name, school: aff.name, core: aff.core,
      shape: w.shape, blurb: w.blurb,
      dmg: w.dmg, reach: w.reach, spin: w.spin, mass: w.mass, mode: w.mode,
      statusKey: rs.key, statusName: rs.def && rs.def.name, statusN: n,
      statusTip: rs.def && rs.def.tip,
      ultName: w.ult.name, ultKind: w.ult.kind, ultTip: w.ult.tip,
      ultCharge: w.ult.charge,
      // Ult art is dispatched on `u.w === "<id>"`. No branch, no set-piece.
      artUnder: src.includes('u.w === "' + id + '"'),
      overCount: (src.match(new RegExp('u\\\\.w === "' + id + '"', 'g')) || []).length
    };
  });
}"""

PAGE = """<!DOCTYPE html>
<meta charset="utf-8"><title>Fighter review — %(game)s</title>
<style>
 body{background:#0C0A12;color:#E8E2D4;font:15px/1.55 -apple-system,BlinkMacSystemFont,
      "Segoe UI",Roboto,sans-serif;margin:0;padding:26px 26px 120px}
 h1{font:600 22px/1.3 Georgia,serif;color:#C9A227;margin:0 0 4px}
 .sub{color:#8A8296;margin:0 0 22px;max-width:70ch}
 .relic{border:1px solid #262034;border-radius:12px;margin:0 0 26px;overflow:hidden;
        background:#120F1B}
 .hd{display:flex;align-items:baseline;gap:12px;padding:14px 18px;border-bottom:1px solid #262034}
 .hd b{font:600 20px Georgia,serif}
 .hd .sch{font:600 11px/1 sans-serif;letter-spacing:.14em;text-transform:uppercase}
 .body{display:flex;gap:18px;padding:18px}
 .shots{flex:0 0 auto;display:flex;gap:10px}
 .shots figure{margin:0;text-align:center}
 .shots img{border:1px solid #262034;border-radius:6px;display:block;background:#000}
 .shots figcaption{font:11px sans-serif;color:#6E6880;margin-top:5px}
 .rows{flex:1 1 auto;min-width:0}
 .row{border:1px solid transparent;border-radius:7px;padding:7px 10px;cursor:pointer;
      display:grid;grid-template-columns:132px 1fr;gap:12px;align-items:start}
 .row:hover{background:#191426;border-color:#2E2742}
 .row.has{border-color:#C9A227;background:#1B1608}
 .k{font:600 10px/1.7 sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#8A8296}
 .v{white-space:pre-wrap;word-break:break-word}
 .src{font:11px ui-monospace,Menlo,monospace;color:#5F5972;margin-top:3px}
 .warn{color:#E0433F;font-weight:600}
 .ok{color:#6BBF7A}
 textarea{display:none;width:100%%;margin-top:8px;background:#0A0810;color:#E8E2D4;
          border:1px solid #3A3252;border-radius:6px;padding:8px;font:14px inherit;
          resize:vertical;min-height:62px}
 .row.open textarea{display:block}
 #bar{position:fixed;left:0;right:0;bottom:0;background:#0C0A12ED;border-top:1px solid #262034;
      padding:12px 26px;display:flex;gap:14px;align-items:center;backdrop-filter:blur(6px)}
 button{background:linear-gradient(180deg,#C9A227,#8A6D12);color:#140F02;border:0;
        border-radius:7px;padding:9px 16px;font:600 14px sans-serif;cursor:pointer}
 #count{color:#8A8296;font:13px sans-serif}
 #out{white-space:pre-wrap;font:12px ui-monospace,monospace;background:#0A0810;
      border:1px solid #262034;border-radius:8px;padding:14px;margin-top:18px;display:none}
</style>
<h1>The four new greatswords — review</h1>
<p class="sub">Click any row to attach a note: what you'd change and to what. Rows are
the actual fields, and each names the anchor a change edits. Nothing is saved
automatically — hit <b>Export</b> before closing and paste the block back.</p>
%(relics)s
<div id="bar"><button id="export">Export notes</button>
<span id="count">0 notes</span></div>
<pre id="out"></pre>
<script>
document.querySelectorAll(".row").forEach(el => {
  el.addEventListener("click", ev => {
    if (ev.target.tagName === "TEXTAREA") return;
    el.classList.toggle("open");
    if (el.classList.contains("open")) el.querySelector("textarea").focus();
  });
  el.querySelector("textarea").addEventListener("input", ev => {
    el.classList.toggle("has", !!ev.target.value.trim());
    document.getElementById("count").textContent =
      document.querySelectorAll(".row.has").length + " notes";
  });
});
document.getElementById("export").addEventListener("click", () => {
  const notes = [];
  document.querySelectorAll(".row").forEach(el => {
    const v = el.querySelector("textarea").value.trim();
    if (v) notes.push({ relic: el.dataset.relic, field: el.dataset.field,
                        anchor: el.dataset.src, was: el.dataset.was, note: v });
  });
  const blob = JSON.stringify(notes, null, 2);
  const out = document.getElementById("out");
  out.style.display = "block";
  out.textContent = notes.length
    ? "Copy this back to Claude (also downloading as fighter-notes.json):\\n\\n" + blob
    : "No notes yet — click a row and type first.";
  if (notes.length){
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([blob], {type:"application/json"}));
    a.download = "fighter-notes.json"; a.click();
  }
});
</script>
"""


def shrink(data_url, width, quality=82):
    """Re-encode a 1080x1920 capture down to review size.

    The page embeds three stills per relic. At full resolution that is a 14 MB
    HTML file for four fighters, which is a bad thing to hand someone whose job
    is to open it and look. JPEG at review width is ~40x smaller and the
    judgement being asked for — silhouette, colour, legibility at a glance — is
    not one JPEG artefacts change. The build is the source of truth for pixels;
    this is a contact sheet.
    """
    im = Image.open(io.BytesIO(base64.b64decode(data_url.split(",", 1)[1])))
    im = im.convert("RGB")
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def row(relic, field, key, val, src, extra=""):
    return (f'<div class="row" data-relic="{html.escape(relic)}" '
            f'data-field="{html.escape(field)}" data-src="{html.escape(src)}" '
            f'data-was="{html.escape(str(val))}">'
            f'<div class="k">{html.escape(key)}</div>'
            f'<div><div class="v">{extra or html.escape(str(val))}</div>'
            f'<div class="src">{html.escape(src)}</div>'
            f'<textarea placeholder="what would you change?"></textarea></div></div>')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", default="sc-gs7.html")
    ap.add_argument("--out", default="fighter-review.html")
    ap.add_argument("--ids", default="oathwound,heartwood,nightfell,axiom")
    ap.add_argument("--foil", default="dawnbringer")
    ap.add_argument("--seed", type=int, default=90210)
    A = ap.parse_args()

    ids = A.ids.split(",")
    g = HERE / A.game
    if not g.exists():
        sys.exit(f"no such build: {g}")

    with game(game_path=g.resolve()) as (page, errors):
        facts = page.evaluate(FACTS_JS, [ids])
        shots = {}
        for rid in ids:
            shots[rid] = {
                "card": shrink(page.evaluate(CARD_JS, [rid, A.foil, A.seed, 2.2]), 440),
                "fight": shrink(page.evaluate(CARD_JS, [rid, A.foil, A.seed, None]), 440),
                "sil": shrink(page.evaluate(SIL_JS, [rid, 420]), 440, 90),
            }
        if errors:
            sys.exit(f"page errors: {errors[:3]}")

    blocks = []
    for f in facts:
        rid = f["id"]
        s = shots[rid]
        art_ok = f["overCount"] > 0
        art_txt = ('<span class="ok">has a set-piece</span>' if art_ok else
                   '<span class="warn">NO SET-PIECE — the ultimate fires and '
                   'draws nothing</span>')
        rows = [
            row(rid, "name", "Name", f["name"], f"WEAPONS[{rid}].name"),
            row(rid, "blurb", "Blurb", f["blurb"], f"WEAPONS[{rid}].blurb"),
            row(rid, "art", "Silhouette", f'{f["shape"]} / {f["school"]} branch',
                f'SHAPES._gs{f["school"][:1].upper()}… (the school branch of '
                f'SHAPES.{f["shape"]})'),
            row(rid, "status", "On hit",
                f'+{f["statusN"]} {f["statusName"]} — {f["statusTip"]}',
                f'WEAPONS[{rid}].onHit.{f["statusKey"]}  ·  tip is '
                f'STATUS.{f["statusKey"]}.tip (SHARED — editing it moves every '
                f'{f["statusKey"]} relic and the in-arena panel)'),
            row(rid, "ultname", "Ultimate", f'{f["ultName"]} ({f["ultKind"]}) — '
                f'{f["ultTip"]}',
                f'WEAPONS[{rid}].ult.name / .tip / .kind'),
            row(rid, "ultart", "Ult art", "", f'drawUltUnder / drawUltOver, '
                f'branch on u.w === "{rid}"', extra=art_txt),
            row(rid, "dmg", "Damage", f'{f["dmg"]}  — PLACEHOLDER, untuned',
                f'WEAPONS[{rid}].dmg (roster_gs_build.py holds it)'),
            row(rid, "type", "Type stats",
                f'reach {f["reach"]} · spin {f["spin"]} · mass {f["mass"]} · '
                f'{f["mode"]}',
                f'fixed by the TYPE — changing these makes it not-a-greatsword'),
            row(rid, "charge", "Ult charge", f'{f["ultCharge"]}',
                f'WEAPONS[{rid}].ult.charge'),
        ]
        blocks.append(f"""<div class="relic">
 <div class="hd"><b>{html.escape(f['name'])}</b>
  <span class="sch" style="color:{f['core']}">{html.escape(f['school'])}</span></div>
 <div class="body">
  <div class="shots">
   <figure><img src="{s['card']}" width="196"><figcaption>fight card</figcaption></figure>
   <figure><img src="{s['fight']}" width="196"><figcaption>mid-fight</figcaption></figure>
   <figure><img src="{s['sil']}" width="196"><figcaption>silhouette</figcaption></figure>
  </div>
  <div class="rows">{''.join(rows)}</div>
 </div></div>""")

    out = HERE.parent / A.out
    out.write_text(PAGE % {"game": html.escape(A.game), "relics": "\n".join(blocks)},
                   encoding="utf-8")
    kb = out.stat().st_size / 1024
    print(f"  {out}  ({kb:.0f} KB, self-contained)")
    print(f"  {len(facts)} relics x {len(rows)} reviewable fields")
    missing = [f["name"] for f in facts if f["overCount"] == 0]
    if missing:
        print(f"  flagged as having NO ult set-piece: {', '.join(missing)}")


if __name__ == "__main__":
    main()
