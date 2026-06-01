# ρ_t 3D Mycel Simulations

## Overview

Interactive 3D visualization of the ρ_t (Time Density) Framework in action.

The mycel network demonstrates:
- **Triplet Structure**: 6 neighbor connections per node (3 axes × 2 directions)
- **Energy Diffusion**: ρ_t spreading through the network
- **Self-Organization**: Emergent patterns from local rules
- **3D Geometry**: True 3D space representation

## Quick Start

```bash
# Install dependencies
pip install -r requirements_sim.txt

# Run simulation (full size)
python rho_t_3d_mycel.py

# Quick test
python rho_t_3d_mycel.py --fast

# Save outputs
python rho_t_3d_mycel.py --save ./output_run_001
```

## Advanced Usage

```bash
# Custom parameters
python rho_t_3d_mycel.py --points 1000 --iterations 200 --verbose

# Fast iteration
python rho_t_3d_mycel.py --points 400 --iterations 100 --fast

# Save all frames
python rho_t_3d_mycel.py --save ./frames --verbose
```

## What You're Seeing

### Colors (via Colormap)
- **Dark (Blue/Purple)**: Low ρ_t (Sparse regions)
- **Bright (Yellow/White)**: High ρ_t (Dense regions)

### Sizes
- **Larger nodes**: More accumulated energy
- **Smaller nodes**: Lower energy levels

### Connections (Filaments)
- **Cyan lines**: Network connections between nodes
- **Thicker lines**: Stronger ρ_t coupling
- **Sparse network**: Self-organized structure

## Physics Explained

### ρ_t Diffusion
```
Each step:
- Node keeps 83% of its own ρ_t
- Adopts 17% from neighbor average
- Thermal noise (0.025σ)
- Result: Smooth spreading + stability
```

### Movement
```
Nodes drift toward high-ρ_t neighbors:
- Force ∝ Neighbor ρ_t difference
- Creates clustering of dense regions
- 3D space allows natural spreading
```

### Energy Accumulation
```
When ρ_t > 3.2 threshold:
- Excess energy stored in node
- Node size grows (visualization)
- Energy represents "activity"
```

## Output Files

Running with `--save` produces:
- `rho_t_3d_mycel_000.png` - Initial state
- `rho_t_3d_mycel_040.png` - Early evolution
- `rho_t_3d_mycel_160.png` - Final state

## Performance

| Points | Iterations | Time (laptop) |
|--------|-----------|---------------|
| 400    | 100       | ~10s          |
| 850    | 160       | ~45s          |
| 1000   | 200       | ~60s          |
| 2000   | 160       | ~180s         |

**Tip**: Use `--fast` for development!

## Mathematical Foundation

See `../docs/3D_VISUALIZATION.md` for:
- Full ρ_t equations
- Triplet structure explanation
- Connection to allzeit_zustand
- Physical interpretation

## Extensions

Want to try:
1. **Different neighbor counts**: Try modifying k_neighbors
2. **Different diffusion rates**: Modify line `self.rho[i] * 0.83`
3. **Different geometries**: Try cubic or cylindrical initial positions
4. **GPU acceleration**: Use cupy instead of numpy

## Troubleshooting

**Simulation is slow?**
- Use `--fast` for quick iteration
- Reduce `--points` or `--iterations`

**Memory issues?**
- Start with `--points 400`
- Use `--iterations 50` first

**Plot not showing?**
- Make sure matplotlib backend is set correctly
- Try: `export MPLBACKEND=TkAgg`

## Citation

If you use this simulation in research, cite:

```
@software{dsp_trin_re_regulation_2026,
  author = {ternarythinker},
  title = {ρ_t 3D Mycel Simulation},
  url = {https://github.com/ternarythinker/DSP-trin-re-regulation},
  year = {2026}
}
```

---

**Enjoy exploring the structure of time density!** ⚛️ 🧬 ✨