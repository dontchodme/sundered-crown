#!/usr/bin/env python3
"""SLAGBURST'S FALSIFICATION HARNESS.

    python3 ultember_check.py --game ../02-chain/sc-ember.html

Every assert here states what would count as evidence that the ultimate is
broken, and several of them exist because the thing they check was wrong at
some point during the build. In particular:

  [5] the status cap swallowing the split, so the wielder who had banked the
      MOST stacks got the smallest burst
  [6] the detonation double-dipping — pricing its damage through a
      dmgTakenMul that still contained the very stacks it was consuming
  [15] a dropped fuse leaving its overflow bookkeeping behind, so the NEXT
      Slagburst detonated on stale arithmetic

Art samples and the fifteen-relic set-piece regression are at the bottom: a
mechanic that works while the set-piece throws is still a broken ultimate,
and a new ult branch that quietly breaks another relic's art is worse.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from scpage import game

# Drive the sim from Python-supplied scenarios. Every case builds a Match,
# poses it, fires by hand, and reports raw state — no thresholds are decided
# in JS, so the assertions live where they can be read.
JS = r"""
([cases]) => {
  const out = [];
  const D = AC.WEAPON_BY_ID ? null : null;
  for (const cs of cases) {
    const m = new AC.Match(cs.a, cs.b, cs.seed >>> 0);
    const f = m.a, foe = m.b;
    const u = f.w.ult;
    m.introT = 0;
    // Pose: put them at a chosen separation, at rest, mid-arena.
    const A = AC.CONFIG.arena;
    f.x = A.w * 0.5 - cs.dist / 2; f.y = A.h * 0.5;
    foe.x = A.w * 0.5 + cs.dist / 2; foe.y = A.h * 0.5;
    f.vx = f.vy = foe.vx = foe.vy = 0;
    if (cs.bank) foe.apply("sunder", cs.bank);
    if (cs.foeHp !== undefined) foe.hp = cs.foeHp;
    if (cs.selfHp !== undefined) f.hp = cs.selfHp;
    const rec = { case: cs.name };
    rec.bankAtCast = foe.stacks("sunder");
    const hpBefore = foe.hp;

    rec.tAtCast = m.t;
    m.fireUlt(f, foe);
    rec.castDmg = +(hpBefore - foe.hp).toFixed(4);
    rec.sunderAfterCast = foe.stacks("sunder");
    rec.slagLit = !!f.ultSlag;
    rec.over = f.ultSlag ? f.ultSlag.over : null;
    rec.phaseAtCast = m.ultFx ? m.ultFx.phase : null;
    rec.fxNAtCast = m.ultFx ? m.ultFx.n : null;
    rec.chargeAtCast = f.charge;
    rec.hitStopAtCast = m.hitStop;

    // Freeze the world except the fuse: no swinging, no movement, so the
    // detonation is measured against a known state rather than a brawl.
    if (cs.quiet) {
      f.hitCd = []; foe.hitCd = [];
      f.stun = 1e9;            // wielder cannot swing; the fuse is not gated on it
      foe.stun = 1e9;
    }
    const hpPreDet = foe.hp;
    const vPre = Math.hypot(foe.vx, foe.vy);
    const dt = AC.CONFIG.physics.dt;
    let steps = 0;
    rec.detFrame = -1;
    while (steps < Math.ceil((cs.run || 1.2) / dt)) {
      const litBefore = !!f.ultSlag;
      if (cs.killFoeAt !== undefined && steps === cs.killFoeAt) { foe.hp = 0; foe.alive = false; }
      if (cs.killSelfAt !== undefined && steps === cs.killSelfAt) { f.hp = 0; f.alive = false; }
      m.step(dt);
      steps++;
      if (litBefore && !f.ultSlag && rec.detFrame < 0) {
        rec.detFrame = steps; rec.tAtDet = m.t;
      }
    }
    rec.detDmg = +(hpPreDet - foe.hp).toFixed(4);
    rec.sunderAfterDet = foe.stacks("sunder");
    rec.knock = +(Math.hypot(foe.vx, foe.vy) - vPre).toFixed(1);
    rec.phaseAfter = m.ultFx ? m.ultFx.phase : null;
    rec.fxN = m.ultFx ? m.ultFx.n : null;
    rec.slagStillLit = !!f.ultSlag;
    rec.ultData = { split: u.split, fuse: u.fuse, dmgBase: u.dmgBase,
                    dmgPer: u.dmgPer, knockBase: u.knockBase,
                    knockPer: u.knockPer, radius: u.radius, charge: u.charge,
                    kind: u.kind, name: u.name, tip: u.tip };
    out.push(rec);
  }
  return out;
}
"""

# Two consecutive casts on one match: the stale-overflow trap.
TWICE_JS = r"""
() => {
  const m = new AC.Match("emberedge", "nightfell", 424242);
  const f = m.a, foe = m.b, u = f.w.ult, A = AC.CONFIG.arena;
  m.introT = 0;
  const pose = () => { f.x = A.w*0.5 - 40; f.y = A.h*0.5;
                       foe.x = A.w*0.5 + 40; foe.y = A.h*0.5;
                       f.vx=f.vy=foe.vx=foe.vy=0; f.stun=1e9; foe.stun=1e9;
                       f.hitCd=[]; foe.hitCd=[]; };
  const dt = AC.CONFIG.physics.dt;
  const run = (bank, dropIt) => {
    pose();
    delete foe.status.sunder;
    foe.hp = foe.maxHp;
    if (bank) foe.apply("sunder", bank);
    m.fireUlt(f, foe);
    const over = f.ultSlag ? f.ultSlag.over : null;
    if (dropIt) { f.ultSlag = null; return { over, dmg: 0, dropped: true }; }
    const before = foe.hp;
    for (let i = 0; i < Math.ceil(0.9 / dt); i++) m.step(dt);
    return { over, dmg: +(before - foe.hp).toFixed(3), dropped: false };
  };
  const dropped = run(6, true);      // fuse lit on 6 banked, then abandoned
  const after   = run(0, false);     // next cast on a clean foe: must be n=3
  return { dropped, after };
};
"""

ART_JS = r"""
([ids]) => {
  window.__frozen = true;
  AC.setResolution(1080, 1920);
  AC.SFX.play = function(){}; AC.SFX.resume = function(){};
  const out = [];
  for (const id of ids) {
    const foe = id === "nightfell" ? "emberedge" : "nightfell";
    const m = new AC.Match(id, foe, 5150501);
    AC.__inject && AC.__inject(m);
    m.introT = 0;
    for (let i = 0; i < 90; i++) m.step(AC.CONFIG.physics.dt);
    m.fireUlt(m.a, m.b);
    const cv = document.getElementById('cv');
    const g = cv.getContext('2d');
    let ink = 0, frames = 0;
    // Sample a few points across the set-piece's life, counting non-background
    // pixels. A branch that throws leaves this at 0 and takes the page's
    // error handler with it.
    for (const adv of [2, 14, 40, 70]) {
      for (let i = 0; i < adv; i++) m.step(AC.CONFIG.physics.dt);
      AC.__draw(m);
      frames++;
      const seen = new Set();
      for (let y = 0; y < cv.height; y += 53)
        for (let x = 0; x < cv.width; x += 53) {
          const d = g.getImageData(x, y, 1, 1).data;
          seen.add((d[0] >> 3) + ',' + (d[1] >> 3) + ',' + (d[2] >> 3));
        }
      ink += seen.size;
    }
    out.push({ id, colours: Math.round(ink / frames) });
  }
  return out;
}
"""


class T:
    def __init__(self):
        self.rows = []

    def ok(self, cond, name, detail=""):
        self.rows.append((bool(cond), name, detail))

    def report(self):
        for ok, name, detail in self.rows:
            print(f"  {'PASS' if ok else 'FAIL'}  {name}"
                  + (f"  — {detail}" if detail else ""))
        f = sum(1 for r in self.rows if not r[0])
        print(f"\n{len(self.rows) - f}/{len(self.rows)} checks passed"
              + ("" if not f else f"  ({f} FAILED)"))
        return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="../02-chain/sc-ember.html")
    a = ap.parse_args()
    t = T()

    cases = [
        dict(name="zero-bank", a="emberedge", b="nightfell", seed=11, dist=80,
             bank=0, quiet=True, run=1.2),
        dict(name="bank3", a="emberedge", b="nightfell", seed=11, dist=80,
             bank=3, quiet=True, run=1.2),
        dict(name="bank6", a="emberedge", b="nightfell", seed=11, dist=80,
             bank=6, quiet=True, run=1.2),
        dict(name="out-of-range", a="emberedge", b="nightfell", seed=11,
             dist=600, bank=2, quiet=True, run=1.2),
        dict(name="foe-dies-in-fuse", a="emberedge", b="nightfell", seed=11,
             dist=80, bank=4, quiet=True, run=1.2, killFoeAt=6),
        dict(name="self-dies-in-fuse", a="emberedge", b="nightfell", seed=11,
             dist=80, bank=4, quiet=True, run=1.2, killSelfAt=6),
    ]

    with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
        recs = {r["case"]: r for r in page.evaluate(JS, [cases])}
        twice = page.evaluate(TWICE_JS)
        ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
        art = page.evaluate(ART_JS, [ids])
        page_errors = list(errors)

    U = recs["zero-bank"]["ultData"]
    dt = 1 / 120   # AC.CONFIG.physics.dt, reported for context only

    def expect(n):
        return U["dmgBase"] + U["dmgPer"] * n

    t.ok(not page_errors, "no JS errors or page exceptions",
         "" if not page_errors else str(page_errors[:2]))

    # [1] the data actually changed shape
    t.ok(U["kind"] == "detonate" and U["name"] == "Slagburst",
         "[1] Emberedge carries kind:detonate / Slagburst",
         f"{U['kind']} / {U['name']}")
    t.ok(len(U["tip"]) <= 72, "[2] ult tip within the 72-char contract",
         f"{len(U['tip'])} chars")

    # [3] the cast resolves nothing
    z = recs["zero-bank"]
    t.ok(z["castDmg"] == 0, "[3] the cast itself deals no damage",
         f"cast dmg {z['castDmg']}")
    t.ok(z["slagLit"] and z["phaseAtCast"] == "fuse",
         "[4] the cast lights a fuse and says so on screen",
         f"lit={z['slagLit']} phase={z['phaseAtCast']}")

    # [5] the split is the floor, and the cap does not eat it
    t.ok(z["sunderAfterCast"] == U["split"],
         "[5a] a zero-bank cast splits the shell to the floor",
         f"{z['sunderAfterCast']} stacks (split {U['split']})")
    b6 = recs["bank6"]
    t.ok(b6["over"] == U["split"],
         "[5b] a full-bank cast carries the capped overflow, not loses it",
         f"over={b6['over']} at bank {b6['bankAtCast']}")

    # [6] the detonation pays the right number, and pays it once
    for nm, n in (("zero-bank", 3), ("bank3", 6), ("bank6", 9)):
        r = recs[nm]
        t.ok(abs(r["detDmg"] - round(expect(n))) <= 1,
             f"[6] {nm}: detonation prices {n} stacks, no double-dip",
             f"dealt {r['detDmg']}, expected {round(expect(n))}")

    # monotone in banked stacks — the whole point of a detonator
    t.ok(recs["zero-bank"]["detDmg"] < recs["bank3"]["detDmg"]
         < recs["bank6"]["detDmg"],
         "[7] burst grows with banked stacks",
         f"{recs['zero-bank']['detDmg']} < {recs['bank3']['detDmg']}"
         f" < {recs['bank6']['detDmg']}")

    # [8] fuse timing, measured in SIM time.
    #     This assert was wrong THREE times before it was right, and every
    #     way is worth keeping written down.
    #       1. It assumed dt=1/60. The engine runs 1/120, so every frame count
    #          it reported was double.
    #       2. It then compared match time to the fuse and read 0.633s against
    #          a 0.55s fuse, and I guessed hit-stop froze the match clock.
    #          It does not: `m.t` keeps advancing through hit-stop.
    #       3. What hit-stop actually freezes is the FIGHTER tick — and the
    #          fuse ticks there, alongside every status, the Crucible's cap
    #          and Daybreak's window. So the fuse costs 0.55s of fighter time,
    #          which is 0.55 + (the cast's own 0.08 hit-stop) of match time.
    #     That is correct and consistent engine behaviour, not a slow fuse.
    #     The assert now names the relationship instead of a magic number, so
    #     a future change to either clock fails it loudly.
    dsim = z["tAtDet"] - z["tAtCast"]
    hs = z["hitStopAtCast"]
    t.ok(abs(dsim - (U["fuse"] + hs)) <= 3 * dt,
         "[8] the fuse burns one fuse of FIGHTER time, hit-stop included",
         f"{dsim:.4f}s of match time = fuse {U['fuse']} + the cast's own "
         f"hit-stop {hs:.3f} ({z['detFrame']} frames at dt={dt:.5f})")

    # [9] Sunder is consumed
    t.ok(all(recs[k]["sunderAfterDet"] == 0
             for k in ("zero-bank", "bank3", "bank6")),
         "[9] the detonation consumes every stack",
         ", ".join(f"{k}:{recs[k]['sunderAfterDet']}"
                   for k in ("zero-bank", "bank3", "bank6")))

    # [10] knockback scales
    kz, k6 = recs["zero-bank"]["knock"], recs["bank6"]["knock"]
    t.ok(k6 > kz > 0, "[10] the throw scales with the burst",
         f"3 stacks {kz}, 9 stacks {k6}")

    # [11] out of range does nothing but say so
    o = recs["out-of-range"]
    t.ok(not o["slagLit"] and o["castDmg"] == 0 and o["detDmg"] == 0
         and o["phaseAtCast"] == "cold"
         and o["sunderAfterCast"] == o["bankAtCast"],
         "[11] out of range: nothing splits, nothing detonates, art says cold",
         f"lit={o['slagLit']} phase={o['phaseAtCast']} det={o['detDmg']}")

    # [12] a fuse whose fighters die drops cleanly
    fd = recs["foe-dies-in-fuse"]
    sd = recs["self-dies-in-fuse"]
    t.ok(not fd["slagStillLit"], "[12a] foe dying mid-fuse drops the fuse")
    # The contract is that a dead wielder's fuse NEVER RESOLVES — not that
    # the state object is tidied up. tickCharge's pre-existing guard
    # (`if (!f.alive || this.over) return;`) returns before the slag block can
    # clear it, so the fuse stays lit on the corpse. That is unobservable:
    # nothing reads ultSlag except the block that guard skips, and hp<=0 has
    # already ended the match. Asserting tidiness here would have pushed a
    # change into shared death code to satisfy a harness, which is backwards.
    t.ok(sd["detDmg"] == 0,
         "[12b] wielder dying mid-fuse never resolves its detonation",
         f"det dmg {sd['detDmg']}, state left lit on the corpse "
         f"(unreachable): {sd['slagStillLit']}")

    # [13] the charge is owed from the cast
    t.ok(z["chargeAtCast"] == 0, "[13] charge resets at the cast, not the burst",
         f"charge {z['chargeAtCast']}")

    # [14] the set-piece throws one shard per consumed stack, and the fuse
    #      tell already shows that same number
    t.ok(recs["bank6"]["fxNAtCast"] == 9 and recs["bank6"]["fxN"] == 9,
         "[14] fuse cracks and burst shards both equal the true stack count",
         f"fuse n={recs['bank6']['fxNAtCast']}, burst n={recs['bank6']['fxN']}")
    t.ok(recs["bank6"]["phaseAfter"] == "burst",
         "[14b] the set-piece advances fuse -> burst")

    # [15] a dropped fuse leaves no arithmetic behind
    t.ok(twice["dropped"]["over"] == 3
         and abs(twice["after"]["dmg"] - round(expect(3))) <= 1,
         "[15] an abandoned fuse does not inflate the next Slagburst",
         f"dropped over={twice['dropped']['over']}, "
         f"next burst {twice['after']['dmg']} (expected {round(expect(3))})")

    # art regression across the whole roster
    blank = [r for r in art if r["colours"] < 12]
    t.ok(not blank, "[16] every relic's set-piece still draws",
         "" if not blank else f"blank: {blank}")
    em = [r for r in art if r["id"] == "emberedge"][0]
    t.ok(em["colours"] >= 20, "[17] Slagburst's own set-piece is not thin",
         f"{em['colours']} distinct sampled colours")

    return 1 if t.report() else 0


if __name__ == "__main__":
    sys.exit(main())
