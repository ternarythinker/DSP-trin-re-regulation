import time

class DSPNode:
    def __init__(self, is_interface=False):
        self.fruits = [[0, 1, 1], [0, 1, 1], [0, 1, 1]]  # Start: 011
        self.mycelium = [0, 1, 1]
        self.energy = 1.8e17  # ρ_t = 2 t_P
        self.rho_t = 1.078e-43
        self.t_P = 5.39e-44
        self.c2 = 9e16
        self.beta = 4.42e81
        self.c0 = 3e8
        self.is_interface = is_interface
        self.alive = True

    def spiral_step(self):
        bit6 = sum(fruit[-3] for fruit in self.fruits) + self.mycelium[-3]
        bit5 = sum(fruit[-2] for fruit in self.fruits) + self.mycelium[-2]
        bit4 = sum(fruit[-1] for fruit in self.fruits) + self.mycelium[-1]
        
        new_triplet = [bit6 % 2, bit5 % 2, bit4 % 2]
        carry = bit6 // 2 + bit5 // 2 + bit4 // 2
        sum_input = bit6 + bit5 + bit4
        return new_triplet, sum_input, carry

    def update_rho_t(self):
        if not self.alive:
            return
        activity_factor = 1.0001  # Vereinfachtes Wachstum
        self.rho_t = min(self.rho_t * activity_factor, 5.39e-40)
        self.energy = self.rho_t * self.c2 / self.t_P  # E = E+

    def stabilize(self, new_triplet, sum_input):
        if sum_input >= 8:
            return [0, 1, 1]  # Stabil
        return new_triplet

    def recycle_energy(self, sum_input):
        if not self.alive:
            return 0
        if sum_input < 9:
            self.energy += self.energy * 0.01
        if self.energy > 1e23:  # Tod
            self.alive = False
            self.energy = 0
            print("Node gestorben – voller Speicher!")
            return 0
        if self.energy > 1e22:  # Verbrauch: Überschuss abwerfen
            excess = self.energy * 0.5
            self.energy -= excess
            return excess
        return 0

    def update(self):
        if not self.alive:
            return 0
        new_triplet, sum_input, carry = self.spiral_step()
        
        new_triplet = self.stabilize(new_triplet, sum_input)
        
        for i in range(len(self.fruits)):
            self.fruits[i][-3:] = new_triplet
        self.mycelium[-3:] = new_triplet
        
        self.update_rho_t()
        return self.recycle_energy(sum_input)

class DSP:
    def __init__(self):
        self.nodes = [DSPNode(is_interface=True)]
        self.grid_energy = 0
        self.last_update_time = time.time()  # Zeitpunkt des letzten Updates

    def simulate(self, max_hours):
        start_time = time.time()
        rounds = 0
        max_seconds = max_hours * 3600
        while (time.time() - start_time) < max_seconds:
            excess_energy = 0
            for node in self.nodes:
                excess_energy += node.update()
            self.grid_energy += excess_energy
            rounds += 1

            # Prüfe, ob 3 Minuten seit dem letzten Update vergangen sind
            current_time = time.time()
            if current_time - self.last_update_time >= 180:  # 180 Sekunden = 3 Minuten
                print(f"Runden bisher: {rounds}, Grid Energy: {self.grid_energy / 1e9:.2f} GW")
                self.last_update_time = current_time  # Update-Zeit aktualisieren

        print(f"Runden in {max_hours} Stunden: {rounds}")
        print(f"Grid Energy: {self.grid_energy / 1e9:.2f} GW")

# Simulation starten – 6 Stunden
if __name__ == "__main__":
    dsp = DSP()
    dsp.simulate(6)