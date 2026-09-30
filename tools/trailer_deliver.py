"""Loudness delivery (the shorts chain: -14 LUFS, -2.0 dBTP, two-pass loudnorm, alimiter level=false)
and the delivery encode. Then measure the delivered file, not the intermediate.

THE VIDEO IS RE-ENCODED TO 4.9 Mb/s, TWO-PASS, AND THAT IS A SIZE DECISION. trailer_cut.py writes a
crf-14 master (~47 MB for 30 s); the chat upload and the device bridge both cap below that (30 MB and
20 MB). Measured against the master: SSIM 0.9928 over all 1800 frames, 19.4 MB. TikTok and Shorts
re-encode far below either on upload.
"""
import json, os, re, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from clip_spread import resolve_ffmpeg

FFMPEG = resolve_ffmpeg()
HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parent / "07-shorts" / "worldcup-trailer"      # every render product lives here (mp4/wav gitignored)
video = sys.argv[1] if len(sys.argv) > 1 else str(WORK / "video.mp4")
out = sys.argv[2] if len(sys.argv) > 2 else str(WORK / "worldcup-trailer.mp4")
I, TP = -14.0, -2.0

p = subprocess.run([FFMPEG, '-hide_banner', '-nostats', '-i', str(WORK / 'mix_pre.wav'), '-af',
                    f'loudnorm=I={I}:TP={TP}:LRA=11:print_format=json', '-f', 'null', '-'],
                   capture_output=True, text=True)
m = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', p.stderr, re.S).group(0))
lim = 10 ** ((TP - 1.5) / 20)   # under the target because AAC overshoots: at 192k, 1.0 under measured -1.7 dBTP, 1.5 under -2.0
af = (f"loudnorm=I={I}:TP={TP}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
      f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
      f"aresample=48000,alimiter=attack=5:release=60:limit={lim:.4f}:level=false")
subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(WORK / 'mix_pre.wav'), '-af', af, '-ar', '48000',
                '-c:a', 'pcm_s24le', str(WORK / 'mix_final.wav')], check=True)
V = ['-c:v', 'libx264', '-preset', 'slower', '-b:v', '4900k', '-maxrate', '9000k', '-bufsize', '12000k',
     '-pix_fmt', 'yuv420p', '-passlogfile', str(WORK / 'x264pass')]
subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', video, *V, '-pass', '1', '-an', '-f', 'mp4', os.devnull], check=True)
subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', video, '-i', str(WORK / 'mix_final.wav'), '-map', '0:v:0',
                '-map', '1:a:0', *V, '-pass', '2', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest',
                '-movflags', '+faststart', out], check=True)
q = subprocess.run([FFMPEG, '-hide_banner', '-nostats', '-i', out, '-map', '0:a', '-af', 'ebur128=peak=true',
                    '-f', 'null', '-'], capture_output=True, text=True).stderr
summ = q[q.rfind('Summary:'):]
print('pass-1 measured:', {k: m[k] for k in ('input_i', 'input_tp', 'input_lra')})
print(summ)
