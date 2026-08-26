# SHATTER + RUNIC GLASS — drop over sc-seed-v27

Two ALTERNATIVE proposals for Axiom, both built from `02-chain/sc-cardspin.html`
`ec9b8d753235385d`. They are not a chain and do not compose — pick one.

    v3  02-chain/sc-shatter.html   98965a7f49ac32d7   2-D fracture, 10 pieces
    v2  02-chain/sc-glass.html     b3342dafc360d57c   1-D slices, irregular

## Rebuild

    cd tools
    python3 shatter_build.py --src ../02-chain/sc-cardspin.html \
                             --out ../02-chain/sc-shatter.html
    python3 glass_build.py   --src ../02-chain/sc-cardspin.html \
                             --out ../02-chain/sc-glass.html --open -0.15

## Controls — not spare files

    02-chain/sc-sh-none.html    868364c2246abfdf   v3 facet+bind off, for glass_probe
    02-chain/sc-glass-nb.html   60eed45d59cd22f4   v2 bind+pool off, for glass_probe
    02-chain/sc-glass-np.html   7371c5a5b3e31bd0   v2 pool off, attributes the IoU cost
    02-chain/sc-glass30.html    79b1e4418a98392f   v2 at open -0.30, more cut angle

glass_probe needs a bind-free build: the filaments cross the very daylight it
measures.

## Checks

    python3 glass_probe.py   --a ../02-chain/sc-cardspin.html \
                             --b ../02-chain/sc-sh-none.html --n 10        5/5
    python3 twin_identity.py --a ../02-chain/sc-cardspin.html \
                             --b ../02-chain/sc-shatter.html
        _twinConjured 0px, _whConjured 0px. It reports NOT IDENTICAL overall and
        is RIGHT to: _gsConjured moved, which is the point. Read the rows.
    python3 engine_ab.py     --a ../02-chain/sc-cardspin.html \
                             --b ../02-chain/sc-shatter.html --n 120       1800/1800
    python3 verify.py --game ../02-chain/sc-shatter.html --n 40            13/13
    python3 silhouette_probe.py --game ../02-chain/sc-shatter.html \
                                --types greatsword --footprint             0.330 min

## NOT DONE — the one thing that needs your hardware

The art costs ~2.5x the shipped weapon to draw (micro-benchmark, relative only).
A frame-level number was attempted and is noise under software rendering.
`bench_build.py` on a GPU is the instrument. See open decision #2.

Write-ups: `claude/sundered-crown-shatter.md` (v3) and
`claude/sundered-crown-runic-glass.md` (v2).
