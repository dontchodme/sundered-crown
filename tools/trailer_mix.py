"""Sound for the World Cup trailer: score + the game's own fight audio per cut + announcer.

Writes mix_pre.wav (float, unnormalised) and prints the speech-to-bed separation,
measured the only way that means anything: LUFS of the voice stem against LUFS of
the (ducked) bed, over the windows where the voice is actually speaking.
Delivery loudness (-14 LUFS, -2 dBTP, two-pass loudnorm + alimiter level=false,
the shorts chain) is applied afterwards by trailer_deliver.py.
"""
import subprocess, sys, pathlib, json
import numpy as np, soundfile as sf
from scipy import signal
import pyloudnorm as pyln

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from trailer_edit import F, VO, DUR, tb
from clip_spread import resolve_ffmpeg

FFMPEG = resolve_ffmpeg()
HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parent / "07-shorts" / "worldcup-trailer"      # every render product lives here (mp4/wav gitignored)
SR = 48000
N = int(DUR * SR)
VO_GAIN_DB = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0     # measured: +7.5 LU speech-to-bed at 3.0 / -9.0
DUCK_DB = float(sys.argv[2]) if len(sys.argv) > 2 else -9.0

music, sr = sf.read(WORK / 'music.wav', dtype='float32'); assert sr == SR
music = music.T[:, :N]

_clip = {}


def clip_audio(name):
    if name not in _clip:
        p = subprocess.run([FFMPEG, '-v', 'error', '-i', str(WORK / 'clips' / name / 'clip.mp4'), '-vn', '-ac', '2',
                            '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
        _clip[name] = np.frombuffer(p.stdout, np.float32).reshape(-1, 2).T.copy()
    return _clip[name]


sfx = np.zeros((2, N), np.float32)
for s in F:
    a = clip_audio(s['clip'])
    dur_out = s['t1'] - s['t0']
    i0 = int(round(s['s'] * SR)); n_src = int(round(dur_out * s['speed'] * SR))
    x = a[:, i0:i0 + n_src]
    if x.shape[1] < n_src:
        x = np.pad(x, ((0, 0), (0, n_src - x.shape[1])))
    n_out = int(round(dur_out * SR))
    if abs(s['speed'] - 1) > 1e-3:          # tape: slower and lower, like the director's own drag
        x = signal.resample(x, n_out, axis=1).astype(np.float32)
    x = x[:, :n_out]
    fi, fo = int(0.004 * SR), int(0.02 * SR)
    x[:, :fi] *= np.linspace(0, 1, fi); x[:, -fo:] *= np.linspace(1, 0, fo)
    j = int(round(s['t0'] * SR))
    sfx[:, j:j + n_out] += x[:, :max(0, min(n_out, N - j))] * 10 ** (s['sfx'] / 20)

vo = np.zeros((2, N), np.float32)
for fn, at in VO:
    y, vsr = sf.read(WORK / 'vo' / fn, dtype='float32')
    y = signal.resample_poly(y, SR, vsr).astype(np.float32)
    j = int(round(at * SR)); n = min(len(y), N - j)
    vo[0, j:j + n] += y[:n]; vo[1, j:j + n] += y[:n]
vo *= 10 ** (VO_GAIN_DB / 20)

# duck the bed under the voice: envelope with 15ms attack, 220ms release, 60ms look-ahead
env = np.abs(vo[0])
win = int(0.02 * SR)
env = np.sqrt(np.convolve(env ** 2, np.ones(win) / win, mode='same'))
key = (env > 0.01).astype(np.float32)
look = int(0.06 * SR)
key = np.maximum(key, np.concatenate([key[look:], np.zeros(look, np.float32)]))
att, rel = np.exp(-1 / (0.015 * SR)), np.exp(-1 / (0.22 * SR))
g = np.zeros(N, np.float32); cur = 0.0
for i in range(N):
    k = key[i]
    cur = (att * cur + (1 - att) * k) if k > cur else (rel * cur + (1 - rel) * k)
    g[i] = cur
duck = 10 ** (DUCK_DB * g / 20)

bed = (music + sfx) * duck
mix = bed + vo
sf.write(WORK / 'mix_pre.wav', mix.T, SR, subtype='FLOAT')
sf.write(WORK / 'stem_vo.wav', vo.T, SR, subtype='FLOAT')
sf.write(WORK / 'stem_bed.wav', bed.T, SR, subtype='FLOAT')

meter = pyln.Meter(SR)
mask = key > 0
idx = np.where(mask)[0]
vo_l = meter.integrated_loudness(vo[:, idx].T)
bed_l = meter.integrated_loudness(bed[:, idx].T)
sfx_l = meter.integrated_loudness(sfx.T)
mus_l = meter.integrated_loudness(music.T)
print(json.dumps({'vo_gain_db': VO_GAIN_DB, 'duck_db': DUCK_DB, 'speech_LUFS_in_vo_windows': round(vo_l, 2),
                  'bed_LUFS_in_vo_windows': round(bed_l, 2), 'speech_to_bed_LU': round(vo_l - bed_l, 2),
                  'music_LUFS': round(mus_l, 2), 'fight_audio_LUFS': round(sfx_l, 2),
                  'peak': float(np.max(np.abs(mix)))}, indent=1))
