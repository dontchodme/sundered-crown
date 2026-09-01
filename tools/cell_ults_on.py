#!/usr/bin/env python3
"""Price open cells with the FIELD'S ULTIMATES LIVE — budget-v59 open decision 2.

row_price measures every cell in a world where no ultimate exists anywhere
(it passes noult=true for every pinned id, which is every weapon in the game).
This prices the same cells twice: once in that world, once in the world the
game actually plays in. The gap is the thing row_price cannot see.

The cell's OWN ultimate is suppressed in every arm — the cell has no ultimate
yet and inventing one would be the whole design.

Runtime only. Nothing is written to any build.
"""
import argparse, json, pathlib, statistics, sys, time
ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True)
ap.add_argument("--game", required=True)
ap.add_argument("--cells", required=True, help="aff:type,aff:type ...")
ap.add_argument("--seeds", type=int, default=10)
ap.add_argument("--secs", type=float, default=120.0)
ap.add_argument("--seed0", type=int, default=2207)
ap.add_argument("--out", default="/tmp/cell_ults_on.json")
a = ap.parse_args()
sys.path.insert(0, str(pathlib.Path(a.repo) / "tools"))
from scpage import game

TYPE_DONOR = {"greatsword": "dawnbringer", "twinblade": "widowmaker",
              "warhammer": "grudgebearer", "scythe": "thornwake",
              "flail": "gravemourn", "bow": "ironhail"}
# school channel, exactly as the school's own relics carry it
CHAN = {"bloodsworn": ("onHit", "hemorrhage", 2), "dwarven": ("onHit", "sunder", 1),
        "runic": ("onHit", "hex", 1), "sanctified": ("onHit", "smite", 1),
        "umbral": ("onHit", "curse", 1), "verdant": ("onHit", "entangle", 2),
        "vigil": ("onSelf", "ward", 1)}

JS = r"""([donor, aff, slot, key, per, on, fieldUlt, foes, seeds, secs]) => {
  const DT = AC.CONFIG.physics.dt;
  const w  = AC.WEAPONS.find(x => x.id === donor);
  const saved = { aff: w.aff,
    onHit:  w.onHit  ? JSON.parse(JSON.stringify(w.onHit))  : null,
    onSelf: w.onSelf ? JSON.parse(JSON.stringify(w.onSelf)) : null };
  const charges = new Map();
  for (const x of AC.WEAPONS) if (x.ult) charges.set(x.id, x.ult.charge);
  // the cell has no ultimate: the donor's is ALWAYS off.
  // fieldUlt decides whether everyone else's is on.
  for (const x of AC.WEAPONS) if (x.ult)
    x.ult.charge = (x.id === donor || !fieldUlt) ? 1e9 : charges.get(x.id);
  w.aff = aff; delete w.onHit; delete w.onSelf;
  if (on && key){ const o = {}; o[key] = per; w[slot] = o; }
  const rows = [];
  for (const f of foes) for (const sd of seeds){
    const m = new AC.Match(donor, f, sd);
    const me = m.a.w.id === donor ? m.a : m.b;
    let step = 0;
    while (!m.over && step < secs / DT){ m.step(DT); step++; }
    rows.push({ win: m.winner ? (m.winner === me ? 1 : 0) : -1,
                hits: me.hits, dur: step * DT });
  }
  w.aff = saved.aff; delete w.onHit; delete w.onSelf;
  if (saved.onHit)  w.onHit  = saved.onHit;
  if (saved.onSelf) w.onSelf = saved.onSelf;
  for (const x of AC.WEAPONS) if (x.ult) x.ult.charge = charges.get(x.id);
  const bad = AC.WEAPONS.filter(x => x.ult && x.ult.charge !== charges.get(x.id));
  return { rows, restored: bad.length === 0 };
}"""

def wr(rs):
    d = [r for r in rs if r["win"] >= 0]
    return sum(r["win"] for r in d) / len(d) if d else float("nan")

cells = [c.split(":") for c in a.cells.split(",")]
seeds = [a.seed0 + 11 * i for i in range(a.seeds)]
t0 = time.time(); out = {}
with game(game_path=pathlib.Path(a.game).resolve()) as (page, errors):
    ids = page.evaluate("() => AC.WEAPONS.map(w => w.id)")
    print(f"{len(ids)} relics in this build\n")
    hdr = f"  {'cell':<26}{'FIELD ULTS OFF':>22}{'FIELD ULTS ON':>22}{'gap':>8}"
    print(hdr); print(f"  {'':<26}{'floor':>10}{'lift':>12}{'floor':>10}{'lift':>12}")
    for aff, typ in cells:
        donor = TYPE_DONOR[typ]
        slot, key, per = CHAN[aff]
        foes = [i for i in ids if i != donor]
        r = {}
        for fu in (False, True):
            for on in (False, True):
                res = page.evaluate(JS, [donor, aff, slot, key, per, on, fu, foes, seeds, a.secs])
                assert not errors, errors
                assert res["restored"], "charges not restored"
                r[(fu, on)] = wr(res["rows"])
        offL = (r[(False, True)] - r[(False, False)]) * 100
        onL  = (r[(True,  True)] - r[(True,  False)]) * 100
        out[f"{aff} x {typ}"] = dict(floor_off=r[(False, False)], lift_off=offL,
                                     floor_on=r[(True, False)], lift_on=onL)
        print(f"  {aff+' x '+typ:<26}{r[(False,False)]:>10.1%}{offL:>+11.1f}pp"
              f"{r[(True,False)]:>10.1%}{onL:>+11.1f}pp{onL-offL:>+7.1f}", flush=True)
    print(f"\n  {len(cells)*4*len(foes)*a.seeds} fights in {time.time()-t0:.0f}s   errors: {errors}")
pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
