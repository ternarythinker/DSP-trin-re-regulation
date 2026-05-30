#!/usr/bin/env python3
"""
ρ_t Allzeit Mycel - 3D Visualization
=====================================

Simuliert die 3D-Struktur von ρ_t (Zeitdichte) in einem Myzel-ähnlichen Netzwerk.

Features:
- 850 Punkte in 3D Raum
- 160 Iterationen mit Dynamik
- Filament-Verbindungen basierend auf ρ_t Stärke
- Live-Plotting mit matplotlib

Usage:
    python rho_t_3d_mycel.py
    
Oder für schnelle Iteration:
    python rho_t_3d_mycel.py --fast --points 400 --iterations 100

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import time
from pathlib import Path

class RhoT3DMycel:
    """
    3D Myzel-Simulation basierend auf ρ_t Framework
    
    Physics:
    - ρ_t = Zeitdichte (Energy concentration)
    - Nachbarn = 6 (Triplet-Struktur: 3 Achsen × 2 Richtungen)
    - Dynamik = Diffusion + Self-Organization
    """
    
    def __init__(self, num_points: int = 850, k_neighbors: int = 6, seed: int = 42):
        """
        Initialize 3D Mycel Network
        
        Args:
            num_points: Number of nodes in network
            k_neighbors: Neighbor connections per node
            seed: Random seed for reproducibility
        """
        np.random.seed(seed)
        
        print(f"🧬 Initializing ρ_t 3D Mycel with {num_points} nodes...")
        
        # 3D Positionen (Gaußverteilung)
        self.pos = np.random.normal(0, 1.4, (num_points, 3))
        
        # ρ_t Zeitdichte (Exponential + Basis)
        self.rho = np.ones(num_points) * 0.8 + np.random.exponential(1.0, num_points)
        
        # Energie (accumulates over time)
        self.energy = np.zeros(num_points)
        
        self.num_points = num_points
        self.k = k_neighbors
        self.iteration = 0
        
        # Berechne Nachbarn (O(n²) aber nur einmal!)
        self.neighbors = self._find_neighbors()
        print(f"✅ Network initialized. Finding nearest {k_neighbors} neighbors...\n")
    
    def _find_neighbors(self):
        """Find k nearest neighbors for each point (3D KD-Tree would be faster!)"""
        neighbors = []
        for i in range(self.num_points):
            # Euclidean distance
            dist = np.sum((self.pos - self.pos[i])**2, axis=1)
            dist[i] = 1e9  # Exclude self
            nearest = np.argsort(dist)[:self.k]
            neighbors.append(nearest)
        return np.array(neighbors)
    
    def step(self):
        """
        One simulation step
        
        Physics:
        1. ρ_t Diffusion (83% local, 17% neighbor average)
        2. Energy accumulation (when ρ_t > threshold)
        3. 3D Movement (force-directed towards neighbors)
        """
        new_rho = self.rho.copy()
        
        # Step 1: ρ_t Diffusion + Noise
        for i in range(self.num_points):
            neigh = self.neighbors[i]
            avg_neigh = np.mean(self.rho[neigh])
            
            # Local conservation + neighbor influence + thermal noise
            new_rho[i] = (self.rho[i] * 0.83 + 
                         avg_neigh * 0.17 + 
                         np.random.normal(0, 0.025))
            
            # Step 2: Energy accumulation above threshold
            if new_rho[i] > 3.2:
                self.energy[i] += (new_rho[i] - 3.2) * 0.1
        
        # Ensure positive ρ_t
        self.rho = np.maximum(0.1, new_rho)
        
        # Step 3: 3D Movement (force-directed layout)
        for i in range(self.num_points):
            neigh = self.neighbors[i]
            # Vectors to neighbors
            dir_vec = self.pos[neigh] - self.pos[i]
            # Force weighted by ρ_t difference
            force = np.mean(dir_vec * self.rho[neigh][:, np.newaxis], axis=0) * 0.0065
            self.pos[i] += force
        
        self.iteration += 1
    
    def get_stats(self):
        """Return simulation statistics"""
        return {
            'iteration': self.iteration,
            'avg_rho': float(np.mean(self.rho)),
            'max_rho': float(np.max(self.rho)),
            'high_density_zones': int(np.sum(self.rho > 4.5)),
            'total_energy': float(np.sum(self.energy))
        }
    
    def plot_3d(self, title: str = None, save_path: str = None, show: bool = True):
        """
        Plot 3D Visualization
        
        Args:
            title: Custom title
            save_path: Save to file instead of showing
            show: Display plot
        """
        if title is None:
            title = f"ρ_t 3D Mycel | Iteration {self.iteration}"
        
        fig = plt.figure(figsize=(14, 11))
        ax = fig.add_subplot(111, projection='3d')
        
        # Node coloring by ρ_t density
        scatter = ax.scatter(
            self.pos[:, 0], self.pos[:, 1], self.pos[:, 2],
            c=self.rho,
            s=self.energy * 8 + 10,
            cmap='magma',
            alpha=0.85,
            edgecolors='black',
            linewidth=0.2,
            vmin=np.percentile(self.rho, 5),
            vmax=np.percentile(self.rho, 95)
        )
        
        # Filament connections (only strong ones)
        for i in range(self.num_points):
            for j in self.neighbors[i]:
                if j > i:  # Avoid double-drawing
                    strength = np.sqrt(self.rho[i] * self.rho[j])
                    if strength > 1.65:  # Threshold for visibility
                        alpha = min(0.45, strength * 0.2)
                        ax.plot(
                            [self.pos[i,0], self.pos[j,0]],
                            [self.pos[i,1], self.pos[j,1]],
                            [self.pos[i,2], self.pos[j,2]],
                            color='#00ddff',
                            alpha=alpha,
                            lw=0.7
                        )
        
        # Colorbar
        cbar = fig.colorbar(scatter, ax=ax, label='ρ_t (Time Density)', shrink=0.6)
        
        # Labels
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        ax.grid(False)
        ax.set_facecolor('#1a1a1a')
        fig.patch.set_facecolor('#0a0a0a')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, facecolor='#0a0a0a')
            print(f"   💾 Saved: {save_path}")
        
        if show:
            plt.show()
        
        plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="ρ_t 3D Mycel Simulation - Visualizing Time Density Networks"
    )
    parser.add_argument('--points', type=int, default=850, help='Number of nodes')
    parser.add_argument('--iterations', type=int, default=160, help='Simulation steps')
    parser.add_argument('--fast', action='store_true', help='Quick test run')
    parser.add_argument('--save', type=str, default=None, help='Save outputs to directory')
    parser.add_argument('--verbose', action='store_true', help='Detailed output')
    
    args = parser.parse_args()
    
    # Quick test mode
    if args.fast:
        args.points = 400
        args.iterations = 80
        print("⚡ FAST MODE: Reduced simulation size\n")
    
    # Initialize
    sim = RhoT3DMycel(num_points=args.points)
    
    # Create output directory if saving
    if args.save:
        out_dir = Path(args.save)
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Output directory: {out_dir}\n")
    
    # Run simulation
    print(f"🚀 Running {args.iterations} iterations...\n")
    start_time = time.time()
    
    for i in range(args.iterations):
        sim.step()
        
        # Print stats
        if i % 40 == 0 or i == args.iterations - 1:
            stats = sim.get_stats()
            elapsed = time.time() - start_time
            print(f"[{i:3d}/{args.iterations}] | "
                  f"ρ_t avg: {stats['avg_rho']:.3f} | "
                  f"high zones: {stats['high_density_zones']:3d} | "
                  f"energy: {stats['total_energy']:.2f} | "
                  f"time: {elapsed:.1f}s")
            
            # Save visualization at key points
            if args.save and (i % 40 == 0 or i == args.iterations - 1):
                save_path = out_dir / f"rho_t_3d_mycel_{i:03d}.png"
                sim.plot_3d(save_path=str(save_path), show=False)
    
    elapsed_total = time.time() - start_time
    print(f"\n✅ Simulation complete in {elapsed_total:.1f}s")
    
    # Final statistics
    stats = sim.get_stats()
    print(f"\n📊 Final Statistics:")
    print(f"   Iterations: {stats['iteration']}")
    print(f"   Avg ρ_t: {stats['avg_rho']:.4f}")
    print(f"   Max ρ_t: {stats['max_rho']:.4f}")
    print(f"   High Density Zones (ρ_t > 4.5): {stats['high_density_zones']}")
    print(f"   Total Energy Accumulated: {stats['total_energy']:.2f}")
    
    # Show final plot
    print(f"\n📺 Displaying final 3D visualization...")
    sim.plot_3d()


if __name__ == "__main__":
    main()
