# WHAT IS NOT IN THE REPO, AND HOW TO GET IT BACK

*(Was WHATS-NOT-IN-THIS-ZIP.md. The zip is retired; `.gitignore` now enforces what this file describes.)*

Everything here regenerates from what IS here. Nothing that was reasoned about
is missing; only things that are large and derivable.

## Rendered clips — `*.mp4`

**The seed IS the fight.** Every clip in this project is a deterministic
function of (build, relic, foe, seed), and the exact command for this
session's is at the bottom of `SEED.md`:

```
cd tools
python3 cinema_clip.py --game ../02-chain/sc-paradox-frame.html \
  --a paradox --b heartwood --seed 25064 --lead 18 --fps 60 --w 540 \
  --out ../07-shorts/v43/stasis-v-heartwood.mp4
ffmpeg -i X.mp4 -filter_complex "[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -movflags +faststart Y.mp4
```

A 13 MB mp4 committed eight times is 100 MB of history nobody can delete, and
it says nothing the seed does not.

## Candidate sounds — `*.wav`

`05-reference/v43/field-cast-candidates.wav` and `field-hold-candidates.wav`
are what Rick picked from. Both regenerate:

```
python3 field_lab.py            # six casts
python3 field_lab.py --hold     # four holds
```

## The voiceover model — `tools/kokoro-v1.0.onnx`, `tools/voices-v1.0.bin`

338 MB. `tools/FETCH-KOKORO.md` restores them. Nothing in v43 used them.

## The reference images from v39–v42 — a SECOND ZIP

`sunderedcrownv43-reference.zip` carries the whole of `05-reference/`,
including this session's. The main zip carries only `05-reference/v43/`.

**This is a delivery limit and not a decision about what matters.** The tree
crossed 30 MiB this session — four sessions of filmstrips, zooms and arena
photographs are 14 MiB of it — so it is split rather than pruned. Unzip the
reference archive over the same tree and it merges back into place:

```
unzip -o sunderedcrownv43.zip
unzip -o sunderedcrownv43-reference.zip
```

`MANIFEST.txt` lists every file from BOTH, so a merged tree can be checked
against it in one pass.

## The clip renderer's frame cache — `07-shorts/*/_clip_frames/`

Intermediate PNGs. `cinema_clip.py` rebuilds them and deletes them itself on a
clean run.

---

## What IS in here and should be

The 1 MB HTML builds. They are text, a diff between two of them is the most
useful artefact this project produces, and being able to run
`engine_ab --a <previous> --b <this>` is what proves a relic did not move the
roster. `MANIFEST.txt` carries a hash and a size for every one of them.
