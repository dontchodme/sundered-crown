#!/usr/bin/env python3
"""THE 3x3 BLOCK, AND THE massRef FIX, IN ONE STEP.

    python3 roster15_build.py --src sc-buf.html --out sc-r15.html

WHY THESE THREE RELICS AND NOT v13's TWO
-----------------------------------------
`resume-here-v13.md` §5.5 prescribes a complete 3x3 block over
types {greatsword, bow, warhammer} x schools {sanctified, dwarven, vigil} and
says two relics remain, giving cycle rank 4. Measured on the actual roster,
both halves of that are wrong:

  * five of nine cells ship; FOUR are missing, not two. Emberedge and
    Hearthguard were built by `factor_test.py` as throwaway forced-damage
    probes, never as roster relics, and Emberedge failed at 73.6% winrate.
  * adding v13's two gives **cycle rank 2**, not 4.

And the deeper problem, which §5.4 states and §5.5 then ignores: **vigil is the
one school the factored model cannot represent.** Every other school applies a
constant status magnitude across its relics — dwarven is `sunder:1` on both
Grudgebearer and Ironhail — but vigil is `ward:1` on Lightkeeper and `ward:2.5`
on Farwarden. That 2.5x is a per-relic scalar with no place in
`base[type] x mod[school]`, so every prediction routed through vigil is
contaminated before it is made.

Counting only cycles that never touch vigil:

    plan                       relics   total rank   CLEAN rank
    v13's two                    11          2            1
    + dwarven greatsword         12          3            2      <-- this build
    + vigil warhammer too        13          4            2

**The fourth relic buys one more constraint and zero clean ones.** Three.

THE NON-NEGOTIABLE CONSTRAINT
-----------------------------
The new relics carry their school's EXISTING status magnitude — `smite:1`,
`sunder:1`. Giving Aureole `smite:2` would recreate vigil's defect inside the
two schools the whole experiment depends on being clean.

WHY massRef MOVES IN THE SAME BUILD
------------------------------------
`massref_probe.py`: the shipped 2.7 is the v9 SIX-relic mean on a roster of
nine, so the whole roster falls 6.9% slow against neutral. Fixing it is a
PHYSICS change — it moves fall rate, which moves contact rate, which makes any
damage table tuned before it a measurement of a different game. It has to land
before the tuner runs, not after, and never on its own.

    mean(sqrt(mass))^2 over the TWELVE-relic roster is what this sets.

**`engine_ab.py` against any earlier build will now FAIL, by design.** The
physics moved. `verify.py` on this roster is the check that matters.
"""
from __future__ import annotations
import argparse, math, pathlib, re, sys

RELICS = '''
  /* ---- THE 3x3 BLOCK. Three cells added so the factored damage model has
     something it can be wrong about. sundered-crown-factor.md.
     Every stat except name, ultimate and blurb is fixed by the TYPE — these
     are not new characters so much as the missing intersections of characters
     that already exist. The statuses match their school exactly, on purpose. */

  { id:"aureole", name:"Aureole", aff:"sanctified", shape:"bow",
    blades:[0], reach:54, width:9, artW:44, dmg:12, spin:2.8, mode:"ranged", mass:1.6,
    onHit:{ smite:1 },
    /* A ranged relic without a `shot` block has no projectile, so it can only
       ever damage anything by walking into it. verify.py caught this — the
       first tuner pass drove Aureole to dmg 41.45 compensating for a weapon
       that could not shoot, and that number came within one check of being
       written up as evidence against the factored damage model. Copied from
       Ironhail and Farwarden, which share it exactly: the shot is a property
       of the TYPE. */
    shot:{ cadence:0.34, speed:380, r:24, life:3.4, grav:0, dmgMul:1.0,
           tip:"Fires along its facing · shots can be clanked" },
    ult:{ name:"Benediction", charge:14, kind:"beam", dmg:15, heal:28, tip:"Shaft of light: 15 damage, heals 28" },
    blurb:"A monstrance strung as a bow. What leaves it has already been blessed." },

  { id:"censer", name:"Censer", aff:"sanctified", shape:"warhammer",
    blades:[0], reach:76, width:26, artW:54, dmg:24, spin:1.6, mode:"spin", mass:5.0, knockMul:2.3,
    onHit:{ smite:1 },
    ult:{ name:"Consecration", charge:15, kind:"nova", radius:300, dmg:12, apply:{smite:3}, knock:300, tip:"Nova: 12 damage, 3 Smite, knockback" },
    blurb:"Swung on its chain until the censer is heavier than what it blesses." },

  { id:"emberedge", name:"Emberedge", aff:"dwarven", shape:"greatsword",
    blades:[0], reach:116, width:14, artW:40, dmg:8, spin:3.4, mode:"swing", arc:1.5, mass:3.0,
    onHit:{ sunder:1 },
    ult:{ name:"Forgefall", charge:14, kind:"nova", radius:220, dmg:17, apply:{sunder:4}, knock:180, tip:"Nova: 17 damage, 4 Sunder, short knockback" },
    blurb:"Quenched once and never since. It does not cut so much as split." },
'''

# THE TUNED DAMAGE TABLE. `tune.py`'s own docstring says it and this build
# ignored it: "A GENERATED file is not a place to store a tuned value ... the
# builder is the source of truth." `tune.py --apply` wrote these into
# sc-r15.html, which this script regenerates from scratch, so all twelve died
# on the next rebuild -- verified, 12 of 12. Its guard refuses names containing
# -bow/-vigil/-phone/-perf and "sc-r15" is not on that list, so it applied
# without complaint. The guard is now a marker in the file (see GEN_MARK) and
# the numbers live here.
#
# Provenance: tune.py --rounds 8 --n 90, seed0 424242, on the 12-relic roster
# at massRef 2.509. Converged 4.4pp spread / 39.3s / 20.3 mean hits.
# An independent run at seed0 987654 reproduced every value to rms |log| 0.020.
TUNED = {
    "dawnbringer": 8.88,
    "widowmaker": 11.95,
    # 27.93 -> 23.50, 2026-08-29. Grudgebearer came out of the pace
    # change at 62.8% (+/-2.5 over 1,440 fights) because a longer fight
    # suits a heavy hitter; 23.50 puts it at 53.8%, mid-roster.
    # ALSO APPLIED AT THE TIP by pace_build.py, because this chain
    # cannot be replayed from here -- ultcarry_build.py exists exactly
    # because some links have owning builders that cannot be replayed.
    # If the two ever disagree, THIS ONE IS RIGHT and the tip is stale.
    "grudgebearer": 23.50,
    "thornwake": 31.35,
    "gravemourn": 44.1,
    "spellbreaker": 8.81,
    "ironhail": 16.23,
    "lightkeeper": 10.54,
    "farwarden": 12.73,
    "aureole": 16.01,
    "censer": 28.77,
    "emberedge": 12.32
}

GEN_MARK = "<!-- GENERATED by roster15_build.py — do not hand-edit or tune in place -->"

PROTECTED = "sundered-crown.html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="sc-buf.html")
    ap.add_argument("--out", default="sc-r15.html")
    a = ap.parse_args()
    if pathlib.Path(a.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    here = pathlib.Path(__file__).parent
    t = (here / a.src).read_text(encoding="utf-8")

    i = t.index("const WEAPONS = [")
    j = t.index("\n];", i)
    for wid in ("aureole", "censer", "emberedge"):
        if f'id:"{wid}"' in t:
            print(f"! {wid} already on the roster", file=sys.stderr)
            return 1
    t = t[:j] + "\n" + RELICS + t[j:]
    print("  [roster15] +3 relics: Aureole, Censer, Emberedge")

    # massRef, derived from the NEW twelve-relic roster
    i2 = t.index("const WEAPONS = [")
    blk = t[i2:t.index("\n];", i2)]
    masses = [float(m) for m in re.findall(r"mass:([0-9.]+)", blk)]
    if len(masses) != 12:
        print(f"! parsed {len(masses)} masses, expected 12", file=sys.stderr)
        return 1
    neutral = round((sum(math.sqrt(m) for m in masses) / len(masses)) ** 2, 3)
    old = re.search(r"massRef:\s*([0-9.]+)", t).group(1)
    t = re.sub(r"massRef:\s*[0-9.]+", f"massRef: {neutral}", t, count=1)
    mult = [(m / neutral) ** 0.5 for m in masses]
    print(f"  [roster15] massRef {old} -> {neutral}   "
          f"mean fall multiplier {sum(mult)/len(mult):.3f} (was 0.931)")

    # the tuned table, applied here so it survives a rebuild
    applied = 0
    for wid, d in TUNED.items():
        i3 = t.find(f'id:"{wid}"')
        if i3 < 0:
            print(f"! TUNED names a relic not in the roster: {wid}", file=sys.stderr)
            return 1
        j3 = t.find("ult:", i3)
        seg, k3 = re.subn(r"dmg:\s*[0-9.]+", f"dmg:{d:g}", t[i3:j3], count=1)
        if k3 != 1:
            print(f"! expected one dmg: for {wid}, found {k3}", file=sys.stderr)
            return 1
        t = t[:i3] + seg + t[j3:]
        applied += 1
    print(f"  [roster15] tuned damage applied to {applied} relics")

    if GEN_MARK not in t:
        t = t.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + GEN_MARK, 1)

    out = here / a.out
    out.write_text(t, encoding="utf-8")
    print(f"{a.src} -> {a.out}")

    from scpage import game
    with game(game_path=out.resolve()) as (pg, errs):
        n = pg.evaluate("()=>AC.WEAPONS.length")
        ids = pg.evaluate("()=>AC.WEAPONS.map(w=>w.id)")
        mr = pg.evaluate("()=>AC.CONFIG.physics.massRef")
        bad = pg.evaluate("""()=>{ const out=[];
          for (const w of AC.WEAPONS){
            if (!w.ult || !w.ult.tip) out.push(w.id+': ult has no tip');
            if (!w.blurb) out.push(w.id+': no blurb');
          }
          for (const id of ['aureole','censer','emberedge']){
            try { AC.simulate(id, 'grudgebearer', 12345); }
            catch(e){ out.push(id+' cannot fight: '+e.message); }
          }
          return out; }""")
        if errs: print("! PAGE ERRORS:\n  " + "\n  ".join(errs[:4]), file=sys.stderr); return 1
        if bad:  print("! ROSTER ERRORS:\n  " + "\n  ".join(bad), file=sys.stderr); return 1
    print(f"  check: {n} relics, massRef {mr}, every ult has viewer text, "
          f"all three new relics can fight")
    print("\n  NEXT: tune.py --game " + a.out + " --rounds 8 --n 90 --apply")
    print("  engine_ab against any earlier build will FAIL — the physics moved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
