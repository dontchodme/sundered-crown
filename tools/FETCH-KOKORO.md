# Kokoro model files — not in the seed

`cinema_vo.py` needs two files that are excluded from the handoff zip for size
(339 MB combined). Fetch them into `tools/` before generating any voiceover:

```
cd tools
curl -L -o kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o voices-v1.0.bin \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
pip install kokoro-onnx soundfile --break-system-packages
```

Verified working 2026-08-16: 325,532,387 and 28,214,398 bytes.
Voice of record is `bm_lewis` (en-gb). See NEXT-SESSION.md §1d for why.
