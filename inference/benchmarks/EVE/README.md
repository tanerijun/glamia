# EVE Benchmark

Reproduces the GLAMIA paper's evaluation on the EVE dataset. Methodology details are in the paper.

## Setup

1. Obtain EVE and extract it so the repository root contains `datasets/extracted/EVE/` with `train01–39/`, `val01–05/`, and `test01–10/`.
2. The pipeline uses the frontal webcam videos (`webcam_c.mp4`) and Tobii ground truth (`webcam_c.h5`) from each stimulus step.
3. The 3D backbone is the released checkpoint (`weights/glamia_gaze360_mobileone_s1.pth`, Gaze360-trained, never fine-tuned on EVE) — all evaluated participants are unseen.

## Step 1 — Extract features

Runs BlazeFace + MobileOne-S1 over every frame and caches predicted gaze angles with the ground-truth screen coordinates (GPU recommended; resumable per participant/step):

```bash
# Run from the inference/ directory
uv run benchmarks/EVE/extract_features.py --split val    # val01–05
uv run benchmarks/EVE/extract_features.py --split train  # train01–39 (needed for --split all)
```

Useful flags: `--data-dir`, `--weights`, `--output-dir`, `--stride`, `--device`.

## Step 2 — Run the benchmark

Fits the mapper per participant and evaluates held-out frames (CPU-only, reads the cached features):

```bash
uv run benchmarks/EVE/benchmark.py --split val
uv run benchmarks/EVE/benchmark.py --split all
```

Useful flags: `--window-size` (default 11), `--min-window-frames` (default 3), `--margin-ratio` (default 0.05), `--features-csv`, `--output-dir`.

Outputs land in `experiments/eve/` at the repository root:

| Split | Output |
|---|---|
| `val` | `experiments/eve/results/` |
| `train` | `experiments/eve/extended/results/` |
| `all` | `experiments/eve/all_44/results/` |

## Expected results

| Split | Subjects | Valid frames | Mean PoG error |
|---|---|---|---|
| `val` | 5 | 162,260 | **127.42 px / 36.70 mm** (5.78% diag) |
| `all` | 44 | 1,496,859 | **138.97 px / 40.02 mm** (6.31% diag) |

Reference copies of these outputs are shipped in [`results/eve/`](../../../results/eve/).
