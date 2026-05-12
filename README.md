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

## Repository Structure

```
EEG2VIS-benchmark/
├── data/                            # Preprocessed EEG data (Git LFS)
│   ├── test001_preprocessed_trials.npz
│   ├── test002_preprocessed_trials.npz
│   └── ...                          # 162 subjects total
├── ori_label/                       # Original experiment stimulus materials
│   ├── VIS_{XXXX}_table.html        # Data table shown to participants
│   ├── VIS_{XXXX}_nlquery.html      # Natural language query
│   ├── VIS_{XXXX}_chart.html        # Vega-Lite visualization (bar/line/pie chart)
│   ├── controls.js                  # Page navigation control script
│   ├── eeg_marker1008.py            # EEG event marker sending script
│   └── README.txt                   # Data provenance notes
├── explore_data.py                  # Data exploration script
└── README.md
```

### `data/` — Preprocessed EEG Signals

Contains 162 `.npz` files, one per subject. Each file stores trial-segmented EEG data across three cognitive phases (table → query → vis), with 31 channels at 200 Hz, padded/cropped to 3000 time points (15 s) per phase. See [Data Structure](#data-structure) above for details.

### `ori_label/` — Experiment Stimulus Materials

Contains 3600 sets of stimulus materials (VIS_1 ~ VIS_3600), each consisting of three HTML files:

| File | Content |
|---|---|
| `VIS_{XXXX}_table.html` | The **data table** presented to participants during the table-viewing phase |
| `VIS_{XXXX}_nlquery.html` | The **natural language query** participants read during the query-reading phase |
| `VIS_{XXXX}_chart.html` | The **visualization chart** (Vega-Lite) displayed during the visualization-viewing phase |

These materials serve as the ground-truth labels for linking EEG signals to specific visual stimuli. Users can parse the HTML files to extract structured information (e.g., table content, query text, Vega-Lite spec) for their own modeling pipelines.

## Quick Start

```python
import numpy as np

# Load one subject
data = np.load("data/test001_preprocessed_trials.npz", allow_pickle=True)
info = data["info"].item()
trials = data["trials"]

print(f"Subject has {info['n_trials']} trials, SR={info['sampling_rate']} Hz")

# Access first trial, visualization phase
eeg_vis = trials[0]["vis"]  # shape: (31, 3000)
print(f"Vis phase EEG shape: {eeg_vis.shape}")
```

## License

This dataset is released under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.

- You are free to share and adapt the data for **non-commercial** purposes.
- You must give appropriate credit and indicate any changes made.

