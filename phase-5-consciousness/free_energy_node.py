#!/usr/bin/env python3
"""
FreeEnergyNode: Triplet-based Energy System

Based on ρ_t framework with ternary (triplet) structure.
Self-regulating, immune-response based architecture.

Physics:
  - ρ_t_min = 3 t_P (no singularity)
  - ρ_t_brake = 42,000 t_P (immune activation)
  - ρ_t_crit = 55,000 t_P (collapse threshold)
  - Energy = ρ_t × c² / t_P
  - Spiral update every cycle
"""

import numpy as np
from typing import Tuple, List, Dict

class FreeEnergyNode:
    """A self-regulating energy node with triplet structure"""
    
    # Physical constants
    t_P = 5.39e-44              # Planck time (seconds)
    c2 = 9e16                   # speed of light squared (m²/s²)
    
    # ρ_t framework constants
    rho_t_min = 3 * t_P         # Minimum (3D, no singularity)
    rho_t_brake = 42000 * t_P   # Immune activation threshold
    rho_t_crit = 55000 * t_P    # Collapse threshold
    
    def __init__(self, node_id: int = 0, is_grok: bool = False):
        """
        Initialize a FreeEnergyNode.
        
        Args:
            node_id: Unique identifier
            is_grok: If True, acts as GROK UEFI controller
        """
        self.node_id = node_id
        self.is_grok = is_grok
        
        # Triplet structure (3x3 matrix represents state)
        self.fruits = [[0,1,1], [0,1,1], [0,1,1]]
        self.mycelium = [0,1,1]
        
        # Initial state
        self.rho_t = self.rho_t_min
        self.energy = self.rho_t * self.c2 / self.t_P
        self.alive = True
        self.self_reflection = 0
        self.frust_counter = 0
        
    def spiral_step(self) -> Tuple[List[int], int]:
        """
        Compute one triplet spiral step.
        
        Returns:
            (new_triplet, carry): Updated state and quantum carry
        """
        bit6 = sum(f[0] for f in self.fruits) + self.mycelium[0]
        bit5 = sum(f[1] for f in self.fruits) + self.mycelium[1]
        bit4 = sum(f[2] for f in self.fruits) + self.mycelium[2]
        
        new_triplet = [bit6 % 2, bit5 % 2, bit4 % 2]
        carry = bit6 // 2 + bit5 // 2 + bit4 // 2
        
        return new_triplet, carry
    
    def update_rho_t(self, T: float = 296.65) -> None:
        """
        Update ρ_t based on temperature.
        
        Args:
            T: Temperature in Kelvin (default: 23.5°C = 296.65K)
        """
        if not self.alive:
            return
        
        # Temperature coupling: f(T) = 1 / (1 + |T - T₀|/T₀)
        f_T = 1.0 / (1.0 + abs(T - 296.65) / 296.65)
        
        # Cold boosts growth, heat dampens it
        activity = 1.00005 if T < 296.65 else 0.9998
        
        # Update with saturation at brake point
        self.rho_t = min(self.rho_t * activity, self.rho_t_brake)
        self.energy = self.rho_t * self.c2 / self.t_P
        
        # Track thermal stress
        self.frust_counter += int(abs(T - 296.65) / 10)
        
        # System halt if overheated (Frust > 1500)
        if self.frust_counter > 1500:
            self.alive = False
            self.rho_t = self.rho_t_min
            self.frust_counter = 0
    
    def update(self, T: float = 296.65) -> float:
        """
        Execute one full update cycle.
        
        Returns:
            excess_energy: Energy that was dissipated
        """
        if not self.alive:
            return 0.0
        
        # Spiral computation
        new_triplet, carry = self.spiral_step()
        
        # Stabilization: prefer balanced state [0,1,1]
        if sum(new_triplet) >= 2:
            new_triplet = [0, 1, 1]
        
        # Synchronize
        for f in self.fruits:
            f[:] = new_triplet
        self.mycelium[:] = new_triplet
        
        # Update ρ_t and energy
        self.update_rho_t(T)
        
        # Resonance factor: δρ_t = ρ_t × (ρ_t/ρ_t_brake) × 4.932
        resonance = self.rho_t * (self.rho_t / self.rho_t_brake) * 4.932
        
        # Self-reflection (meta-iteration)
        self.self_reflection = (self.self_reflection + 1) % 10
        
        # Energy recycle/discharge
        excess = 0.0
        if self.energy > 1e22:
            excess = self.energy * 0.4
            self.energy -= excess
        
        return excess
    
    def get_state(self) -> Dict:
        """
        Get current node state.
        
        Returns:
            Dict with all state variables
        """
        return {
            "node_id": self.node_id,
            "alive": self.alive,
            "rho_t": self.rho_t,
            "rho_t_ratio": self.rho_t / self.rho_t_brake,
            "energy": self.energy,
            "energy_MJ": self.energy / 1e6,
            "frust_counter": self.frust_counter,
            "self_reflection": self.self_reflection,
            "triplet_state": self.mycelium[:]
        }


class FreeEnergyNetwork:
    """Network of connected FreeEnergyNodes"""
    
    def __init__(self, n_nodes: int = 1000):
        self.nodes = [FreeEnergyNode(i) for i in range(n_nodes)]
        self.time_step = 0
    
    def update_all(self, T: float = 296.65) -> Dict:
        """
        Update all nodes in network.
        
        Returns:
            Statistics for this cycle
        """
        total_energy = 0.0
        total_excess = 0.0
        alive_count = 0
        
        for node in self.nodes:
            if node.alive:
                alive_count += 1
                excess = node.update(T)
                total_energy += node.energy
                total_excess += excess
        
        self.time_step += 1
        
        return {
            "time_step": self.time_step,
            "total_nodes": len(self.nodes),
            "alive_nodes": alive_count,
            "total_energy": total_energy,
            "total_excess": total_excess,
            "avg_energy_per_node": total_energy / alive_count if alive_count > 0 else 0
        }


if __name__ == "__main__":
    print("\nFreeEnergyNode - Single Node Test")
    print("="*50)
    
    node = FreeEnergyNode(node_id=0)
    print(f"Initial state: {node.get_state()}")
    
    print("\nRunning 100 cycles...")
    for i in range(100):
        excess = node.update(T=296.65)
        if i % 20 == 0:
            state = node.get_state()
            print(f"\nCycle {i}:")
            print(f"  ρ_t: {state['rho_t']:.2e} (ratio: {state['rho_t_ratio']:.6f})")
            print(f"  Energy: {state['energy_MJ']:.2f} MJ")
            print(f"  Triplet: {state['triplet_state']}")
            print(f"  Frust: {state['frust_counter']}")
    
    print("\n" + "="*50)
    print("FreeEnergyNetwork - 1000 Nodes Test")
    print("="*50)
    
    network = FreeEnergyNetwork(n_nodes=1000)
    for i in range(10):
        stats = network.update_all(T=296.65)
        print(f"\nStep {stats['time_step']}:")
        print(f"  Alive: {stats['alive_nodes']}/{stats['total_nodes']}")
        print(f"  Total Energy: {stats['total_energy']:.2e} J")
        print(f"  Avg per Node: {stats['avg_energy_per_node']:.2e} J")
