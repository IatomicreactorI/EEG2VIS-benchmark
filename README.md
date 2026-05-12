# EEG2VIS Benchmark — Preprocessed EEG Data

Preprocessed and trial-segmented EEG data for the **EEG2VIS** benchmark. Each file corresponds to one participant and contains EEG signals recorded during a visualization comprehension task.

## Dataset Overview

| Property | Value |
|---|---|
| Subjects | 162 |
| File format | `.npz` (NumPy compressed archive) |
| Channels | 31 EEG channels |
| Sampling rate | 200 Hz |
| Time points per phase | 3000 (15 s per phase) |
| Task phases | `table` → `query` → `vis` |

## File Naming

```
test{XXX}_preprocessed_trials.npz
```

where `XXX` is a zero-padded subject ID (e.g., `test001`, `test002`, …, `test163`).

## Data Structure

Each `.npz` file contains two keys:

### `info` (dict)

| Field | Type | Description |
|---|---|---|
| `n_trials` | `int` | Number of trials for this subject |
| `phases` | `list[str]` | Phase names: `['table', 'query', 'vis']` |
| `sampling_rate` | `int` | Sampling rate in Hz (200) |

### `trials` (array of dicts, length = `n_trials`)

Each trial is a dictionary with the following keys:

| Key | Shape | Type | Description |
|---|---|---|---|
| `table` | `(31, 3000)` | `float64` | EEG data during the **table-viewing** phase |
| `query` | `(31, 3000)` | `float64` | EEG data during the **query-reading** phase |
| `vis` | `(31, 3000)` | `float64` | EEG data during the **visualization-viewing** phase |
| `times` | dict | — | Padded/cropped time range per phase (all `(0, 3000)`) |
| `original_times` | dict | — | Original sample indices before padding/cropping |

**Dimensions**: `(channels, time_points)` — 31 EEG channels × 3000 time points (15 seconds at 200 Hz).

## Quick Start

```python
import numpy as np

# Load one subject
data = np.load("test001_preprocessed_trials.npz", allow_pickle=True)
info = data["info"].item()
trials = data["trials"]

print(f"Subject has {info['n_trials']} trials, SR={info['sampling_rate']} Hz")

# Access first trial, visualization phase
eeg_vis = trials[0]["vis"]  # shape: (31, 3000)
print(f"Vis phase EEG shape: {eeg_vis.shape}")
```

## License

Please refer to the original dataset license and cite accordingly.
