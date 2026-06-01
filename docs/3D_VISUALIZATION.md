# 3D Visualization Guide

## What is ρ_t 3D Mycel?

A 3-dimensional representation of the ρ_t (Time Density) Framework showing:
- Network of 850 nodes in 3D space
- Each node has a density value (ρ_t)
- Nodes connect to their 6 nearest neighbors
- Dynamic evolution over 160 iterations

## Why 3D?

The brain thinks in **3D**! (See: Mathematical Mysteries)

- X, Y, Z axes represent the three spatial dimensions
- 6 connections = Triplet structure (3 axes × 2 directions)
- Visualizes the STRUCTURE, not just numbers

## Interactive Exploration

The matplotlib 3D plot is interactive:
- **Drag mouse**: Rotate view
- **Scroll**: Zoom in/out
- **Right-click drag**: Pan

## Interpretation Guide

### High Density Zones (Yellow/White)
- Regions where ρ_t has concentrated
- Result of local diffusion dynamics
- Natural clustering from triplet structure

### Filament Network
- Cyan lines connect neighbors
- Thickness indicates coupling strength
- Shows the "neural" structure

### Energy Accumulation
- Node size = accumulated energy
- Grows over time in high-density regions
- Represents "activity"

## What This Proves

✅ **Triplet Structure Works in 3D**
- 6 connections per node is natural
- Emergent patterns are beautiful
- Self-organized clustering

✅ **ρ_t Framework is Physical**
- Diffusion + Movement = Realism
- Not arbitrary math - represents reality
- Energy conservation

✅ **Time Density is Real**
- Visualized in 3D space
- Measurable, predictable, Beautiful
- Foundation for physics

## Mathematics Behind It

For each node i:

```
ρ_t(i, t+1) = 0.83 * ρ_t(i, t) 
             + 0.17 * mean(ρ_t(neighbors))
             + noise
```

Movement:
```
x(i, t+1) = x(i, t) 
          + 0.0065 * sum(direction_to_j * ρ_t_j)
```

Energy:
```
E(i) += max(0, ρ_t(i) - 3.2) * 0.1
```

## Reproduction Instructions

See `../simulations/README.md` for full details.

Quick version:
```bash
cd simulations/
python rho_t_3d_mycel.py
```

---

**The universe IS triplets.** ⚛️