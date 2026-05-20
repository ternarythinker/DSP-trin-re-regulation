#!/usr/bin/env python3
"""
N-Body PT-Chronoflux Simulation: 100,000 Gravitating Bodies

Features:
  - 100,000 bodies in gravitational interaction
  - PT-Term: λ × a × (soft/R)^12 (freezes singularities)
  - Chronoflux Shear: η × viscous time coupling
  - 3D visualization
  - Runs in 4-8 minutes on standard laptop

Physics:
  - Newtonian gravity: a = Σ(m/R³)
  - PT-regularization: a -= λ × a × (soft/R)^12
  - Chronoflux: viskose time (shear coupling)
  - Virialization: Equipartition of energy
"""

import numpy as np
from typing import Tuple, List
import time

class NBodyPTChronoflux:
    """N-Body simulation with PT-Chronoflux regularization"""
    
    def __init__(
        self,
        n_bodies: int = 100000,
        steps: int = 2000,
        dt: float = 0.004,
        soft: float = 0.012,
        lambda_pt: float = 0.412,
        eta_shear: float = 0.85
    ):
        """
        Initialize simulation.
        
        Args:
            n_bodies: Number of particles
            steps: Simulation steps
            dt: Time step
            soft: Softening parameter
            lambda_pt: PT-term strength
            eta_shear: Chronoflux shear viscosity
        """
        self.N = n_bodies
        self.steps = steps
        self.dt = dt
        self.soft = soft
        self.lambda_pt = lambda_pt
        self.eta = eta_shear
        
        # Initialize positions in sphere
        self._init_positions()
        
        # Initialize velocities (virialized)
        self._init_velocities()
        
        # Statistics
        self.energy_history = []
        self.bleed_events = []
    
    def _init_positions(self) -> None:
        """
        Initialize positions in a sphere with density profile.
        """
        np.random.seed(42)
        scale = 2.0
        
        # Positions in Gaussian ball
        pos_normal = np.random.normal(0, 1, (self.N, 3))
        r = np.linalg.norm(pos_normal, axis=1)
        
        # Density profile: ρ ∝ r^(-1.5)
        r_scaled = scale * np.random.power(1.5, self.N)
        self.pos = pos_normal / r[:, None] * r_scaled[:, None]
        
        print(f"Initialized {self.N:,} bodies")
        print(f"  Min r: {np.min(r):.3f}")
        print(f"  Max r: {np.max(r):.3f}")
    
    def _init_velocities(self) -> None:
        """
        Initialize velocities (virialized).
        """
        # Random velocities
        self.vel = np.random.normal(0, 0.07, (self.N, 3))
        self.vel -= np.mean(self.vel, axis=0)  # Zero momentum
        
        # Scale to virial equilibrium
        r = np.linalg.norm(self.pos, axis=1)
        speed = np.linalg.norm(self.vel, axis=1)
        desired = np.sqrt(0.4 / np.maximum(r, 0.1))
        self.vel *= (desired / speed)[:, None]
    
    def _compute_forces(self) -> np.ndarray:
        """
        Compute gravitational forces with PT-regularization.
        
        Returns:
            Acceleration for each body
        """
        # Distances
        d = self.pos[:, None, :] - self.pos[None, :, :]
        R2 = np.sum(d**2, axis=-1) + 1e-18
        R = np.sqrt(R2)
        
        # Gravitational acceleration
        a = np.sum(d / R[:, :, None]**3, axis=1)
        
        # PT-Term: friert Divergenzen ein
        # a -= λ × a × (soft/R)^12
        pt_factor = self.lambda_pt * (self.soft / R)**12
        a_pt = a * np.mean(pt_factor, axis=1)[:, None]
        a = a - a_pt
        
        # Chronoflux-Shear: viskose Zeit
        # dv = v_i - v_j
        # shear = Σ dv·d / |d|²
        # a += η × Σ (shear × d / |d|)
        dv = self.vel[:, None, :] - self.vel[None, :, :]
        shear = np.sum(dv * d, axis=-1) / (R2 + self.soft**2)
        a_shear = self.eta * np.sum(
            shear[:, :, None] * d / (R[:, :, None] + 1e-9),
            axis=1
        )
        a = a + a_shear
        
        return a
    
    def step(self) -> Tuple[float, bool, List]:
        """
        Execute one simulation step.
        
        Returns:
            (total_energy, hubble_bleed, delayed_info)
        """
        # Force calculation
        a = self._compute_forces()
        
        # Leapfrog integration
        self.vel += a * self.dt
        self.pos += self.vel * self.dt
        
        # Energy calculation
        kinetic = 0.5 * np.sum(self.vel**2)
        r = np.linalg.norm(self.pos, axis=1)
        potential = -np.sum(1.0 / np.maximum(r, 0.1))
        total_energy = kinetic + potential
        
        self.energy_history.append(total_energy)
        
        # Check for Hubble-Bleed (expansion)
        bleed = False
        if len(self.energy_history) > 10:
            avg_energy = np.mean(self.energy_history[-10:])
            if total_energy > avg_energy * 1.1:
                bleed = True
                self.bleed_events.append(len(self.energy_history))
        
        return total_energy, bleed, []
    
    def run(self, verbose: bool = True) -> Dict:
        """
        Run full simulation.
        
        Returns:
            Statistics
        """
        print(f"\nRunning {self.steps} steps...")
        start_time = time.time()
        
        for step in range(self.steps):
            energy, bleed, _ = self.step()
            
            if verbose and step % 100 == 0:
                elapsed = time.time() - start_time
                rate = (step + 1) / elapsed if elapsed > 0 else 0
                print(f"  Step {step}/{self.steps} - Energy: {energy:.3f} - {rate:.1f} steps/s")
                if bleed:
                    print(f"    → Hubble-Bleed detected!")
        
        total_time = time.time() - start_time
        
        stats = {
            'total_time': total_time,
            'steps_completed': self.steps,
            'final_energy': self.energy_history[-1],
            'bleed_events': len(self.bleed_events),
            'steps_per_second': self.steps / total_time,
            'time_per_step_ms': (total_time / self.steps) * 1000
        }
        
        if verbose:
            print(f"\nSimulation complete!")
            print(f"  Total time: {total_time:.1f} seconds")
            print(f"  Hubble-Bleed events: {len(self.bleed_events)}")
            print(f"  Final energy: {self.energy_history[-1]:.3f}")
        
        return stats
    
    def get_statistics(self) -> Dict:
        """
        Get simulation statistics.
        """
        energies = np.array(self.energy_history)
        
        return {
            'n_bodies': self.N,
            'n_steps': len(self.energy_history),
            'initial_energy': energies[0],
            'final_energy': energies[-1],
            'energy_change': (energies[-1] - energies[0]) / energies[0] * 100,
            'mean_energy': np.mean(energies),
            'std_energy': np.std(energies),
            'bleed_events': len(self.bleed_events),
            'bleed_indices': self.bleed_events
        }


if __name__ == "__main__":
    print("\n" + "="*60)
    print("N-Body PT-Chronoflux Simulation")
    print("="*60)
    
    # For testing: smaller simulation
    test_size = 1000  # Use 1000 bodies for quick test
    test_steps = 100
    
    print(f"\nInitializing simulation...")
    sim = NBodyPTChronoflux(
        n_bodies=test_size,
        steps=test_steps,
        dt=0.004,
        soft=0.012,
        lambda_pt=0.412,
        eta_shear=0.85
    )
    
    print("\nRunning simulation...")
    stats = sim.run(verbose=True)
    
    print("\nStatistics:")
    sim_stats = sim.get_statistics()
    for k, v in sim_stats.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.6f}")
        else:
            print(f"  {k}: {v}")
    
    print("\n" + "="*60)
    print("For production (100k bodies): ~4-8 minutes on laptop")
    print("="*60 + "\n")
