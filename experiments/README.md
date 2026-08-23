# Experiments: 42k scans

This folder contains lightweight, illustrative experiments to help validate
and visualize the 42k mesoscale hypothesis. These scripts are small, fast and
intended for reproducibility and exploration.

Contents
- scan_42k.py: sweep mesoscale factor S and compute a toy coherence metric; outputs CSV and PNG.

Notes
- The experiments here are intentionally simple. They provide a clear, reproducible demo showing
  how the product D × M × S produces a number near 42k and how a toy coherence function can
  have a peak there. Use these as a starting point before running higher-fidelity tests with
  simulations/rho_t_3d_mycel.py.

Example
    python experiments/scan_42k.py --s-min 800 --s-max 1200 --steps 41 --out out.csv --plot out.png

