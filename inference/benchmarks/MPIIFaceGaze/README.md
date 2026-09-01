# MPIIFaceGaze Benchmark

Evaluates GLAMIA on MPIIFaceGaze: single-frame 9-point personalization of the 2D linear mapper per participant, plus a within-day vs. cross-day calibration decay analysis. Methodology details are in the paper.

## Setup

Obtain MPIIFaceGaze and extract it so the repository root contains `datasets/extracted/MPIIFaceGaze/` with `p00–p14/`.

## Step 1 — Extract features

Runs the released 3D model over all frames and caches predicted gaze angles with the ground-truth screen coordinates:

```bash
# Run from the inference/ directory (defaults resolve relative to the repository root)
uv run benchmarks/MPIIFaceGaze/extract_features.py
```

Useful flags: `--data-dir`, `--weights`, `--output-dir`, `--device`.

Output: `experiments/mpiifacegaze/mpiifacegaze_features.csv`.

## Step 2 — Run the benchmark

```bash
uv run benchmarks/MPIIFaceGaze/benchmark.py --margin-ratio 0.10
```

Useful flags: `--margin-ratio` (default 0.10), `--features-csv`, `--output-dir`.

Outputs in `experiments/mpiifacegaze/results/`:
- `mpiifacegaze_global_benchmark.csv` — per-participant and mean error
- `mpiifacegaze_cross_day_decay.csv` — within-day vs. cross-day breakdown
- `benchmark_summary.md`

## Expected results

| Metric | Value |
|---|---|
| Global mean | **234.53 px** (14.28% diag) |
| Within-day mean | **196.99 px** (12.13% diag) |

Reference copies are shipped in [`results/mpiifacegaze/`](../../../results/mpiifacegaze/).
