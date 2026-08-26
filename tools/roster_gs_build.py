#!/usr/bin/env python3
"""COMPLETE THE GREATSWORD COLUMN — all seven schools on one type.

    python3 roster_gs_build.py --src sc-everything.html --out sc-gs7.html

WHY THIS COLUMN, AND WHY IT IS CHEAP
------------------------------------
`greatsword`, `scythe`, `twinblade` and `warhammer` each already dispatch on all
seven schools and each already has all seven silhouettes written — `_gsBarbed`,
`_gsGrown`, `_gsEaten`, `_gsConjured` and the rest are in the artifact today,
drawn and approved, with no relic wearing them. **Twenty cells have finished art
and no fighter.** (bow has no school branches at all — every bow is one shape
under a palette — and `flail` has no method, so those two columns are NOT cheap
and are deliberately not touched here.)

Of those twenty, the greatsword four are worth the most:

```
school       relics   types it appears in     constrains anything?
sanctified      3     gs, bow, warhammer      yes
dwarven         3     gs, bow, warhammer      yes
vigil           2     gs, bow                 yes
bloodsworn      1     twinblade               NO
verdant         1     scythe                  NO
umbral          1     flail                   NO
runic           1     twinblade               NO
```

Four of seven schools have exactly one relic, each in a different type, so a
school modifier for them is not merely unmeasured — it is **unmeasurable**, with
nothing to compare against. This build gives all four a second cell in a type
three other schools already occupy, which is the first complete column the
roster has ever had and the first time those four schools enter the factor model
at all.

WHAT IS FIXED BY THE TYPE, AND WHAT IS NOT
------------------------------------------
Every stat except name, status, ultimate and blurb is copied from the existing
greatswords exactly — `reach 116, width 14, artW 40, spin 3.4, mode "swing",
arc 1.5, mass 3.0`. These are the missing intersections of characters that
already exist, not new characters, and the 3x3 block established that the type
axis has to be held rigid or the experiment measures the wrong thing.

Each carries **its own school's existing status magnitude exactly**, for the
same reason: `hemorrhage:2` because Widowmaker is 2, `entangle:2` because
Thornwake is 2, `curse:1`, `hex:1`.

DAMAGE IS A PLACEHOLDER AND WILL BE WRONG
-----------------------------------------
`dmg` is 9.05 on all four — the mean of the three tuned greatswords (7.32,
10.56, 9.26). It is not an estimate of anything. It cannot be: deriving a
starting value needs a school modifier, and the whole reason these four schools
were chosen is that they do not have one yet.

This is a SKETCH build by explicit decision — Rick's call is to watch the feel
before spending a tuner pass. What that decision does NOT buy is skipping the
structural checks. `verify.py` once caught a ranged relic shipped with no `shot`
block, and the tuner had driven its damage to 41.45 compensating for a weapon
that could not fire — a broken relic hiding inside a plausible number. Guessed
damage plus unrun structural checks is exactly how that happens twice, so
`--check` (on by default) loads the output and asserts every new relic draws,
swings, lands hits and reads legibly before this writes anything.

THE ULTIMATE IS THE CONFOUND — SAID OUT LOUD THIS TIME
------------------------------------------------------
`sundered-crown-factor-cause.md` measured the ultimate at up to **+41% of base
damage**, and that it — not the school — is what broke factorisation on the
greatsword column. So each ultimate below is written in its school's idiom and
kept deliberately modest, and none of these four relics should ever be used to
test the factor model without first building a matched-ultimate arm with
`gs_arm_build.py --ult`. Recorded here rather than rediscovered later.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, sys

HERE = pathlib.Path(__file__).parent
PROTECTED = "sundered-crown.html"

# Every field that is not name/status/ultimate/blurb is the TYPE's, verbatim
# from Dawnbringer, Emberedge and Lightkeeper.
# The TYPE's stats, minus damage. `dmg` was a single shared 9.05 while these
# four were a sketch — deliberately identical so the school effect could be
# read off the winrate spread at equal damage. That measurement is done (43.5pp)
# and the tuner has since converged each one separately, so a shared constant
# would now quietly overwrite four different answers with one.
GS = 'blades:[0], reach:116, width:14, artW:40, spin:3.4, mode:"swing", arc:1.5, mass:3.0,'

# Converged by tune.py --rounds 8 --n 90 --seed0 424242 on the 16-relic roster,
# 2026-08-14: final spread 4.7pp, mean 39.5s, 0% timeouts. Sketch values were
# 9.05 across the board; the spread between these four IS the school effect.
TUNED_GS = {
    "oathwound": 9.17,
    "heartwood": 12.65,
    "nightfell": 15.83,
    "axiom": 7.42
}

RELICS = f"""
  /* ---- THE GREATSWORD COLUMN, COMPLETED. Four cells added so that all seven
     schools appear on one type for the first time. Every stat except name,
     status, ultimate and blurb is fixed by the TYPE and copied from the three
     greatswords already here.

     `dmg` is 9.05 on all four — the mean of the tuned three — and it is a
     PLACEHOLDER, not an estimate. A real starting value needs a school
     modifier, and these are precisely the four schools that do not have one.
     Watch them, then tune them. roster_gs_build.py. */

  {{ id:"oathwound", name:"Goreshard", aff:"bloodsworn", shape:"greatsword",
    {GS} dmg:9.17,
    onHit:{{ hemorrhage:2 }},
    ult:{{ name:"Bloodprice", charge:14, kind:"beam", dmg:16, apply:{{hemorrhage:3}},
          tip:"Deals 16 damage and applies 3 Hemorrhage stacks" }},
    blurb:"Serrated the whole length. It leaves teeth in the wound, and the bleeding does the rest." }},

  {{ id:"heartwood", name:"Heartwood", aff:"verdant", shape:"greatsword",
    {GS} dmg:12.65,
    onHit:{{ entangle:2 }},
    ult:{{ name:"Rootfast", charge:15, kind:"freeze", radius:230, dmg:9, apply:{{entangle:3}},
          freeze:1.3, tip:"Roots for 1.3 seconds, deals 9 damage and applies 3 Entangle stacks" }},
    blurb:"Not forged — grown, and still growing. Puts down roots where it lands." }},

  {{ id:"nightfell", name:"Nightfell", aff:"umbral", shape:"greatsword",
    {GS} dmg:15.83,
    onHit:{{ curse:1 }},
    ult:{{ name:"Eclipse", charge:15, kind:"nova", radius:250, dmg:11, apply:{{curse:3}},
          knock:150, tip:"Nova: deals 11 damage and applies 3 Curse stacks — knocks back" }},
    blurb:"A reaper's blade. What it takes off a life never grows back." }},

  {{ id:"axiom", name:"Axiom", aff:"runic", shape:"greatsword",
    {GS} dmg:7.42,
    onHit:{{ hex:1 }},
    ult:{{ name:"Corollary", charge:13, kind:"bolt", dmg:18, apply:{{hex:3}},
          tip:"Deals 18 damage and applies 3 Hex stacks" }},
    blurb:"Blade-shards held in formation by nothing at all. Close the gaps and it is a sword again." }},
"""

CHECK_JS = r"""
(ids) => {
  const out = [];
  for (const id of ids){
    const w = AC.WEAPONS.find(x => x.id === id);
    if (!w){ out.push({id, err:"not in WEAPONS"}); continue; }
    const st = AC.relicStatus(w);
    const r = { id,
      art: !!AC.SHAPES[w.shape],
      statusKey: st && st.key, statusDef: !!(st && st.def),
      statusTip: st && st.def ? st.def.tip : null,
      ultTip: w.ult && w.ult.tip, ultName: w.ult && w.ult.name,
      // A melee relic has no `shot`; relicShot must agree, or the fight card
      // and verify.py will disagree about whether it is ranged.
      shot: AC.relicShot(w) };
    // Does it actually fight? Four opponents, pinned seeds. The failure this
    // guards is a relic that exists, draws, and never lands anything.
    let hits = 0, wins = 0, n = 0;
    for (const opp of ["dawnbringer","grudgebearer","thornwake","widowmaker"]){
      if (opp === id) continue;
      for (let s = 1; s <= 4; s++){
        const m = AC.simulate(id, opp, 0x51ED0000 + s * 7919);
        hits += m.hits.a + m.hits.b; n++;
        if (m.winner === w.name) wins++;
      }
    }
    r.meanHits = hits / n; r.winrate = wins / n;
    out.push(r);
  }
  return out;
}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="sc-everything.html")
    ap.add_argument("--out", default="sc-gs7.html")
    ap.add_argument("--no-check", action="store_true",
                    help="skip loading the output in a browser (do not)")
    A = ap.parse_args()

    if pathlib.Path(A.out).name == PROTECTED:
        print(f"REFUSED — {PROTECTED} is the shipped artifact.", file=sys.stderr)
        return 1
    src = HERE / A.src
    if not src.exists():
        print(f"! missing {src}", file=sys.stderr)
        return 2
    s = src.read_text(encoding="utf-8")

    # The anchor is the END of the WEAPONS array. `\n];\n` appears many times in
    # the file, so it is anchored on the last relic's blurb terminator instead —
    # asserted to appear exactly once, the same discipline the cinema and intro
    # patches used across five builders.
    ANCHOR = '''    blurb:"Quenched once and never since. It does not cut so much as split." },

];'''
    if s.count(ANCHOR) != 1:
        # sc-r15 / sc-everything end on Emberedge; the shipped 9-relic roster
        # ends on Farwarden. Try that, and refuse if neither is unique.
        ANCHOR = '''    blurb:"Every hit it lands becomes a plate. Every plate becomes the next arrow." },

];'''
        if s.count(ANCHOR) != 1:
            print("! could not find a unique end-of-WEAPONS anchor. Diff before "
                  "re-anchoring — do not loosen it.", file=sys.stderr)
            return 3
    head, tail = ANCHOR[:-3], ANCHOR[-3:]     # keep the blurb line, insert before `];`
    s = s.replace(ANCHOR, head + RELICS + tail, 1)

    # The stamp goes immediately AFTER the doctype, matching roster15_build.py
    # and wallglow_build.py. This is a CONVENTION, not a correctness fix: a
    # comment ahead of `<!DOCTYPE html>` does NOT trigger quirks mode in an
    # HTML5 parser — measured, `document.compatMode` is `CSS1Compat` either way.
    # `introcard_build.py` stamps before the doctype and is fine.
    #
    # The doctype is located rather than assumed to be at byte 0, and anything
    # already ahead of it is preserved: reordering another builder's provenance
    # to satisfy a convention would be a worse trade than an untidy header.
    doc = "<!DOCTYPE html>\n"
    i = s.find(doc)
    if i < 0:
        print("! source has no doctype — refusing to guess where the stamp goes",
              file=sys.stderr)
        return 4
    stamp = (f"<!-- GENERATED by roster_gs_build.py --src {A.src} — "
             f"do not hand-edit or tune in place -->")
    s = s[:i + len(doc)] + stamp + "\n" + s[i + len(doc):]
    if i > 0:
        print(f"  note: {A.src} has {i} bytes ahead of its doctype "
              f"(another builder's stamp) — left as found, not reordered")

    out = HERE / A.out
    out.write_text(s, encoding="utf-8")
    print(f"{A.src} -> {A.out}   {len(src.read_text())} -> {len(s)} bytes")
    print(f"  sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}")

    if A.no_check:
        print("  ! checks skipped")
        return 0

    sys.path.insert(0, str(HERE))
    from scpage import game
    ids = ["oathwound", "heartwood", "nightfell", "axiom"]
    with game(game_path=out) as (page, errors):
        rows = page.evaluate(CHECK_JS, ids)
        if errors:
            print(f"! page errors: {errors[:3]}", file=sys.stderr)
            return 5

    bad = []
    print(f"\n  {'relic':<12}{'status':<14}{'ult':<12}{'hits/match':>11}{'winrate':>9}")
    for r in rows:
        if r.get("err"):
            bad.append(f"{r['id']}: {r['err']}"); continue
        print(f"  {r['id']:<12}{str(r['statusKey'])+':'+str(r['statusDef']):<14}"
              f"{str(r['ultName']):<12}{r['meanHits']:>11.1f}{r['winrate']:>9.0%}")
        if not r["art"]:            bad.append(f"{r['id']}: no SHAPES entry")
        if not r["statusDef"]:      bad.append(f"{r['id']}: status has no STATUS entry")
        if not r["statusTip"]:      bad.append(f"{r['id']}: status has no viewer text")
        if not r["ultTip"]:         bad.append(f"{r['id']}: ultimate has no viewer text")
        if r["shot"]:               bad.append(f"{r['id']}: melee relic reports a shot block")
        # The Aureole failure, generalised: a relic that cannot land anything.
        if r["meanHits"] < 6:       bad.append(f"{r['id']}: only {r['meanHits']:.1f} hits/match")
        if len(r["ultTip"] or "") > 72:
            bad.append(f"{r['id']}: ult tip {len(r['ultTip'])} chars (max 72)")

    print()
    if bad:
        print("  STRUCTURAL CHECK FAILED:")
        for b in bad: print("   ", b)
        out.unlink()
        print(f"\n  {A.out} deleted — a sketch may have guessed damage, "
              f"not a broken relic.")
        return 6
    print("  structural check PASS — all four draw, swing, land hits and read legibly")
    print("  NOTE: the winrates above are 16 pinned matches against FOUR fixed")
    print("  opponents — a smoke test, not a balance measurement. verify.py's")
    print("  120-pairing sweep is the one that decides. These four are tuned as")
    print("  of 2026-08-14 (spread 5.8pp over the full roster).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
