#!/usr/bin/env python3
"""Every line of fight-card wording, as a clickable review page.

    python3 wording_sheet.py --game sc-intro.html --out wording-review.html

Extracts the EXACT strings the card composes — from the build's own
WEAPONS/STATUS/AFFINITIES through the same relicStatus/relicShot calls — so
the review page cannot drift from what renders. Click any line to attach a
note; Export produces a JSON block to hand back, and each entry names the
data field a change would edit (STATUS.x.tip, <relic>.ult.tip, ...), so
notes map straight to anchors.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib

from scpage import game

HERE = pathlib.Path(__file__).parent

EXTRACT_JS = """() => {
  const out = { relics: [], shared: [] };
  for (const w of AC.WEAPONS){
    const aff = AC.AFFINITIES[w.aff];
    const rs = AC.relicStatus(w);
    const n = (w.onHit && w.onHit[rs.key]) || (w.onSelf && w.onSelf[rs.key]) || 1;
    const r = { id: w.id, name: w.name, school: aff.name, core: aff.core,
                lines: [] };
    if (w.mode === "swing")
      r.lines.push({ id: w.id + ".tracks",
                     tag: "", label: "TRUESTRIKE",
                     text: "Swords track their target instead of rotating",
                     source: "card constant (introcard_build.py)" });
    if (rs.def)
      r.lines.push({ id: w.id + ".status",
                     tag: "ON HIT",
                     label: (rs.self ? "GAIN " : "") +
                            (rs.def.maxStacks > 1 ? "+" + n + " " : "") +
                            rs.def.name.toUpperCase(),
                     text: rs.def.tip,
                     source: "STATUS." + rs.key + ".tip (shared by every " +
                             rs.key + " relic + the in-arena explainer)" });
    r.lines.push({ id: w.id + ".ult",
                   tag: "ULTIMATE", label: w.ult.name.toUpperCase(),
                   text: (w.ult.tip || "") + " · " + w.ult.charge + "s cooldown",
                   source: w.id + ".ult.tip (+ charge)" });
    out.relics.push(r);
  }
  const b = AC.CONFIG.combat.baseHP;
  out.shared = [
    { id: "tape.damage", text: "DAMAGE / HIT", source: "tape row label" },
    { id: "tape.reach",  text: "REACH — ranged relics print ANY",
      source: "tape row label" },
    { id: "tape.swing",  text: "SWING SPEED", source: "tape row label" },
    { id: "tape.weight", text: "WEIGHT", source: "tape row label" },
    { id: "tape.hp",     text: b + " HP EACH", source: "CONFIG.combat.baseHP" },
    { id: "card.title",  text: "SUPER WEAPON BALL: THE SUNDERED CROWN",
      source: "card header" },
    { id: "card.vs",     text: "VS", source: "the stamp on the clash" },
    { id: "page.h1",     text: document.querySelector("h1").textContent,
      source: "page heading + subtitle (above the stage)" },
    { id: "page.title",  text: document.title, source: "browser tab title" },
    { id: "fight.footer", text: "SUPER WEAPON BALL: THE SUNDERED CROWN · seed <n>",
      source: "in-fight footer under the arena" },
  ];
  return out;
}"""

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sundered Crown — fight-card wording review</title>
<style>
  body{background:#0A0810;color:#EDE3D0;font-family:ui-sans-serif,system-ui,sans-serif;
       max-width:860px;margin:0 auto;padding:28px 16px 80px;line-height:1.5}
  h1{font-family:ui-serif,Georgia,serif;color:#C9A227;letter-spacing:.14em;
     font-size:22px;text-transform:uppercase}
  p.hint{color:#8B7F94;font-size:14px}
  .relic{border:1px solid #2C2438;border-left:6px solid var(--core,#C9A227);
         border-radius:8px;margin:18px 0;padding:10px 16px;background:#14111E}
  .relic h2{font-family:ui-serif,Georgia,serif;font-size:24px;margin:6px 0 0}
  .relic .school{font-size:12px;letter-spacing:.18em;text-transform:uppercase;
                 color:var(--core,#C9A227);margin-bottom:8px}
  .line{padding:8px 10px;margin:6px 0;border-radius:6px;cursor:pointer;
        border:1px solid transparent}
  .line:hover{background:#1D1828;border-color:#3E3350}
  .line.noted{border-color:#C9A227;background:#1c1710}
  .tag{font-size:11px;letter-spacing:.14em;color:#5E5140;font-weight:700;
       margin-right:8px;text-transform:uppercase}
  .label{font-weight:800;color:var(--core,#FFF4D0);margin-right:8px}
  .text{color:#B4A996}
  .src{display:block;font-size:11px;color:#524A5E;margin-top:2px}
  textarea{width:100%;margin-top:8px;background:#0C0914;color:#EDE3D0;
           border:1px solid #3E3350;border-radius:6px;padding:8px;font-size:14px;
           min-height:60px;display:none}
  textarea.open{display:block}
  #export{position:fixed;bottom:18px;right:18px;background:linear-gradient(180deg,#C9A227,#8A6D12);
          color:#1A1206;font-weight:700;border:1px solid #E8C65A;border-radius:6px;
          padding:12px 18px;cursor:pointer;letter-spacing:.08em}
  #out{white-space:pre-wrap;background:#100D18;border:1px solid #2C2438;border-radius:6px;
       padding:12px;font-family:ui-monospace,monospace;font-size:12px;display:none;
       margin-top:20px}
  h3.shared{color:#8B7F94;letter-spacing:.14em;text-transform:uppercase;font-size:13px;
            margin-top:30px}
</style></head><body>
<h1>Fight-card wording — click a line, leave a note</h1>
<p class="hint">Every string below is extracted from the build itself, composed
exactly as the card composes it. Click a line to open a note box — write the
replacement wording or the complaint. When done, hit <b>Export notes</b> and
send back the block it produces (it also downloads as a file). Nothing saves
on its own — export before closing.</p>
__BODY__
<h3 class="shared">Shared card strings</h3>
__SHARED__
<button id="export">Export notes</button>
<div id="out"></div>
<script>
"use strict";
document.querySelectorAll(".line").forEach(el => {
  el.addEventListener("click", ev => {
    if (ev.target.tagName === "TEXTAREA") return;
    const ta = el.querySelector("textarea");
    ta.classList.toggle("open");
    if (ta.classList.contains("open")) ta.focus();
  });
  el.querySelector("textarea").addEventListener("input", ev => {
    el.classList.toggle("noted", ev.target.value.trim().length > 0);
  });
});
document.getElementById("export").addEventListener("click", () => {
  const notes = [];
  document.querySelectorAll(".line").forEach(el => {
    const v = el.querySelector("textarea").value.trim();
    if (v) notes.push({ id: el.dataset.id, source: el.dataset.source,
                        current: el.dataset.current, note: v });
  });
  const blob = JSON.stringify(notes, null, 2);
  const out = document.getElementById("out");
  out.style.display = "block";
  out.textContent = notes.length
    ? "Copy this back to Claude (also downloading as sc-wording-notes.json):\\n\\n" + blob
    : "No notes yet — click a line and type first.";
  if (notes.length){
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([blob], {type: "application/json"}));
    a.download = "sc-wording-notes.json";
    a.click();
  }
  out.scrollIntoView({behavior: "smooth"});
});
</script></body></html>
"""


def esc(s): return html.escape(str(s), quote=True)


def line_div(ln):
    label = f'<span class="label">{esc(ln.get("label", ""))}</span>' \
        if ln.get("label") else ""
    tag = f'<span class="tag">{esc(ln.get("tag", ""))}</span>' \
        if ln.get("tag") else ""
    return (f'<div class="line" data-id="{esc(ln["id"])}" '
            f'data-source="{esc(ln["source"])}" data-current="{esc(ln["text"])}">'
            f'{tag}{label}<span class="text">{esc(ln["text"])}</span>'
            f'<span class="src">{esc(ln["source"])}</span>'
            f'<textarea placeholder="replacement wording or note…"></textarea>'
            f'</div>')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--game", default="sc-intro.html")
    ap.add_argument("--out", default="wording-review.html")
    a = ap.parse_args()
    with game(game_path=(HERE / a.game).resolve()) as (pg, errs):
        data = pg.evaluate(EXTRACT_JS)
        assert not errs, errs

    body = []
    for r in data["relics"]:
        body.append(f'<div class="relic" style="--core:{esc(r["core"])}">'
                    f'<h2>{esc(r["name"].upper())}</h2>'
                    f'<div class="school">{esc(r["school"])}</div>')
        body.append(line_div({"id": r["id"] + ".name", "text": r["name"],
                              "source": "relic name"}))
        for ln in r["lines"]:
            body.append(line_div(ln))
        body.append("</div>")
    shared = [line_div(ln) for ln in data["shared"]]

    out = HERE / a.out
    out.write_text(PAGE.replace("__BODY__", "\n".join(body))
                       .replace("__SHARED__", "\n".join(shared)),
                   encoding="utf-8")
    n = sum(1 + len(r["lines"]) for r in data["relics"]) + len(data["shared"])
    print(f"{a.out}  — {n} reviewable lines from {a.game}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
