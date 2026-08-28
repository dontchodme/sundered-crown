# Kokoro model files — not in the repo

`cinema_vo.py` needs two files that are gitignored for size (339 MB combined).
Fetch them into `tools/` before generating any voiceover.

**ONE COMMAND PER LINE, NO CONTINUATIONS.** The previous version of this file
wrapped the URLs with a trailing `\`, which is a BASH continuation. Rick's
shell is PowerShell, where `\` is not one — so the pasted block ran the URL
into the following line and curl was handed
`...voices-v1.0.bincd C:\dev\sundered-crown`. It failed with *"URL rejected:
Port number was not a decimal number"*, wrote a 9-byte file, and exited in a
way that looks like a network problem. Same trap as `python3` in CLAUDE.md §5:
these docs were written in a Linux container and are records, not instructions.

```powershell
cd C:\dev\sundered-crown\tools
```

```powershell
curl.exe -L -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
```

```powershell
curl.exe -L -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

`curl.exe`, not `curl` — in PowerShell `curl` is an alias for
`Invoke-WebRequest`, which does not take `-L` or `-o` and fails differently.

## CHECK THE SIZES. A PARTIAL DOWNLOAD IS NOT AN ERROR HERE.

Both files must be exactly:

```
kokoro-v1.0.onnx   325,532,387 bytes
voices-v1.0.bin     28,214,398 bytes
```

```powershell
Get-ChildItem kokoro-v1.0.onnx, voices-v1.0.bin | Select-Object Name, Length
```

A truncated `voices-v1.0.bin` does not make `cinema_vo.py` fail cleanly — it
fails inside the ONNX runtime, a long way from the cause. Check the bytes.

Verified working 2026-08-16. Voice of record is `bm_lewis` (en-gb); see
NEXT-SESSION.md §1d for why.
