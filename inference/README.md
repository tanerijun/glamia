# GLAMIA Inference

Inference pipeline, webcam demo, and public-benchmark evaluation for GLAMIA. Run `uv sync` here first.

## Webcam demo

```bash
uv run demo.py --weights ../weights/glamia_gaze360_mobileone_s1.pth
```

Nine-point calibration, then live point-of-gaze estimation. Optional flags: `--source` (camera index or video file), `--device {auto,cpu,cuda}`, `--smooth-facebbox`, `--smooth-gaze`.

## Benchmarks

- [`benchmarks/EVE/`](benchmarks/EVE/README.md) — paper evaluation on the EVE dataset (44 subjects, 138.97 px / 40.02 mm).
- [`benchmarks/MPIIFaceGaze/`](benchmarks/MPIIFaceGaze/README.md) — test with within-day / cross-day analysis.

Both follow the same two-step pattern: `extract_features.py` caches per-frame 3D gaze features using the released checkpoint (GPU recommended), then `benchmark.py` fits the personalized linear mapper and evaluates.

## Library usage

```python
from src.inference import GazePipeline3D, Mapper

# 3D gaze direction: BlazeFace detection -> MobileOne-S1 -> pitch/yaw in degrees
pipeline = GazePipeline3D(weights_path="../weights/glamia_gaze360_mobileone_s1.pth")
for face in pipeline(frame_bgr):          # one dict per detected face
    pitch, yaw = face["gaze"]["pitch"], face["gaze"]["yaw"]

# Personalized 2D screen mapping (9-point calibration, closed-form OLS)
mapper = Mapper()
for (pitch, yaw), (x, y) in calibration_samples:   # 9 grid targets
    mapper.add_calibration_point([[pitch, yaw]], (x, y))
mapper.train()
x, y = mapper.predict([pitch, yaw])        # point of gaze in screen pixels
```

## Layout

- `src/models/` — MobileOne-S1 (fused-inference form) and the pitch/yaw gaze head.
- `src/inference/` — `GazePipeline3D` (BlazeFace → crop → model → softmax-expected angles), `GazePipeline2D` (+ mapper), `Mapper` (OLS affine mapping with optional dynamic adaptation).
- `src/utils/` — preprocessing transforms and optional Kalman smoothers.
- `mediapipe_models/` — BlazeFace face detector.
