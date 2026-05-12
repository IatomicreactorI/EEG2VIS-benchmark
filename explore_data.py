"""
EEG Preprocessed Trials Data Explorer
======================================
This script reads and inspects the structure of preprocessed EEG trial data (.npz files).
"""

import numpy as np
import os
import sys


def explore_single_file(filepath):
    """Load and print the full structure of a single .npz file."""
    print(f"{'='*60}")
    print(f"File: {os.path.basename(filepath)}")
    print(f"Size: {os.path.getsize(filepath) / 1e6:.1f} MB")
    print(f"{'='*60}")

    data = np.load(filepath, allow_pickle=True)

    # --- Info ---
    info = data["info"].item()
    print("\n[INFO]")
    for k, v in info.items():
        print(f"  {k}: {v}")

    # --- Trials ---
    trials = data["trials"]
    print(f"\n[TRIALS] total: {len(trials)}")

    for i, trial in enumerate(trials):
        print(f"\n  Trial {i}:")
        for key, val in trial.items():
            if hasattr(val, "shape"):
                print(f"    {key}: shape={val.shape}, dtype={val.dtype}, "
                      f"min={val.min():.4f}, max={val.max():.4f}, mean={val.mean():.4f}")
            elif isinstance(val, dict):
                print(f"    {key}: {val}")
            else:
                print(f"    {key}: {val}")


def summarize_all_files(folder):
    """Print a summary table of all .npz files in the folder."""
    files = sorted([f for f in os.listdir(folder) if f.endswith(".npz")])
    print(f"\n{'='*60}")
    print(f"Dataset Summary: {len(files)} subjects")
    print(f"{'='*60}")
    print(f"{'File':<45} {'Trials':>6} {'Channels':>8} {'Timepoints':>10} {'SR':>4}")
    print("-" * 75)

    total_trials = 0
    for f in files:
        path = os.path.join(folder, f)
        data = np.load(path, allow_pickle=True)
        info = data["info"].item()
        t0 = data["trials"][0]
        n_trials = info["n_trials"]
        total_trials += n_trials
        channels = t0["table"].shape[0]
        timepoints = t0["table"].shape[1]
        sr = info["sampling_rate"]
        print(f"{f:<45} {n_trials:>6} {channels:>8} {timepoints:>10} {sr:>4}")

    print("-" * 75)
    print(f"Total trials across all subjects: {total_trials}")


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        summarize_all_files(folder)
    else:
        # Default: explore the first file
        files = sorted([f for f in os.listdir(folder) if f.endswith(".npz")])
        if files:
            explore_single_file(os.path.join(folder, files[0]))
            print(f"\n\nRun with --all to see a summary of all {len(files)} files.")
        else:
            print("No .npz files found in the current directory.")
