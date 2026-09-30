"""Put renderAudio wavs through the clip's own audio encode (cinema_clip.py: -c:a aac -b:a 128k -ac 2) and back to
mono 48 kHz 16-bit, the form clip_audio6.py read. Output next to each input as <stem>_aac<k>.wav.
    python aac_roundtrip.py <k> <in.wav> [<in.wav> ...]"""
import pathlib, subprocess, sys
sys.path.insert(0, "C:/dev/sundered-crown/tools")
from clip_spread import resolve_ffmpeg  # noqa: E402
FF = resolve_ffmpeg(); k = sys.argv[1]
for p in map(pathlib.Path, sys.argv[2:]):
    m4a = p.with_name(f"{p.stem}_aac{k}.m4a"); out = p.with_name(f"{p.stem}_aac{k}.wav")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", str(p),
                    "-c:a", "aac", "-b:a", "128k", "-ac", "2", str(m4a)], check=True)
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", str(m4a),
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(out)], check=True)
    m4a.unlink()
    print(out.name)
