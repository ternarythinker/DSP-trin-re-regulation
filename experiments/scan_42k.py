#!/usr/bin/env python3
"""
experiments/scan_42k.py

Simple reproducible experiment to illustrate how a coherence metric varies
with mesoscale factor S, demonstrating a local optimum near S = 1000 (n ≈ 42k).

This is an illustrative toy model (fast, deterministic) intended to help
understand how the geometric product D × M × S relates to observed coherence.

Usage:
    python experiments/scan_42k.py --s-min 600 --s-max 1400 --steps 41 --out out.csv

Produces CSV and a sample PNG plot (out_plot.png).

"""

import math
import csv
import argparse
import os
import matplotlib.pyplot as plt

# Model constants (the geometric derivation)
D = 6   # directions: 3 axes * 2 directions
M = 7   # motif: center + 6 neighbors
TARGET_S = 1000
TARGET_N = D * M * TARGET_S

# Toy coherence function -- intentionally simple and reproducible.
# We combine an analytic Gaussian centered on TARGET_N with a small
# deterministic "network response" model to illustrate an extremum.

def coherence_score(n: float, sigma: float = 5000.0) -> float:
    """Return a coherence score in [0,1]. Higher is more coherent."""
    # Gaussian preference for the target n
    g = math.exp(-0.5 * ((n - TARGET_N) / sigma) ** 2)

    # Deterministic motif effect: motifs that are integer multiples of M
    # get a slight bonus (models discrete packing effects)
    motif_bonus = 1.0 if (abs((n / M) - round(n / M)) < 1e-6) else 0.98

    # Combined score
    score = g * motif_bonus
    return score


def run_scan(s_min: int, s_max: int, steps: int, out_csv: str, plot_png: str):
    S_values = []
    scores = []

    for i in range(steps):
        if steps == 1:
            S = (s_min + s_max) / 2.0
        else:
            S = s_min + i * (s_max - s_min) / float(steps - 1)
        n = D * M * S
        sc = coherence_score(n)
        S_values.append(S)
        scores.append(sc)

    # Save CSV
    os.makedirs(os.path.dirname(out_csv) or '.', exist_ok=True)
    with open(out_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['S', 'n', 'coherence'])
        for S, sc in zip(S_values, scores):
            n = D * M * S
            writer.writerow([S, int(n), float(sc)])

    # Plot
    plt.figure(figsize=(8,4))
    plt.plot(S_values, scores, marker='o')
    plt.axvline(TARGET_S, color='red', linestyle='--', label=f'Target S={TARGET_S}')
    plt.xlabel('Mesoscale factor S')
    plt.ylabel('Coherence score (toy model)')
    plt.title('Scan for coherence vs mesoscale factor S')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_png)
    print(f'Wrote CSV: {out_csv}\nWrote plot: {plot_png}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--s-min', type=int, default=600)
    parser.add_argument('--s-max', type=int, default=1400)
    parser.add_argument('--steps', type=int, default=41)
    parser.add_argument('--out', type=str, default='experiments/scan_42k_out.csv')
    parser.add_argument('--plot', type=str, default='experiments/scan_42k_plot.png')
    args = parser.parse_args()

    run_scan(args.s_min, args.s_max, args.steps, args.out, args.plot)
