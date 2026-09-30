"""The announcer lines. Kokoro bm_lewis -- the hook voice the shorts ship with (shorts_build.py
--voice default) -- en-gb, speed 1.0; trailer_edit.VO uses the _100 takes. Model files: tools/FETCH-KOKORO.md.
Phonemes checked with k.tokenizer.phonemize before use (all eight lines read as written).
"""
import json, os, pathlib, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "07-shorts" / "worldcup-trailer" / "vo"
OUT.mkdir(parents=True, exist_ok=True)
os.chdir(OUT)
k = Kokoro(str(HERE / "kokoro-v1.0.onnx"), str(HERE / "voices-v1.0.bin"))
LINES = {
 'l1': 'Forty-nine fighters.',
 'l2': 'One crown.',
 'l3': 'Sixteen groups.',
 'l4': 'One knockout.',
 'l5': 'Win, or go home.',
 'l6': 'Who takes the crown?',
 'l7': 'The Super Weapon Ball World Cup.',
 'l8': "Follow, so you don't miss a match.",
}
meta = {}
for key, text in LINES.items():
    for spd in (1.0, 0.92):
        sm, sr = k.create(text, voice='bm_lewis', speed=spd, lang='en-gb')
        sm = np.asarray(sm, dtype=np.float32)
        loud = np.where(np.abs(sm) > 0.012)[0]
        sm = sm[max(0, loud[0]-int(sr*0.02)): loud[-1]+int(sr*0.08)]
        name = f'{key}_{int(spd*100)}.wav'
        sf.write(name, sm, sr)
        meta[name] = round(len(sm)/sr, 3)
json.dump(meta, open('meta.json','w'), indent=1)
print(json.dumps(meta, indent=1))
