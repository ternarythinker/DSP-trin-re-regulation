# DSP ρ_t Framework: From Quantum Biology to Robotics

## Vision

A three-layer hierarchical architecture for AI-driven robotics, inspired by mycelial networks and quantum biology, optimized for real-time control, thermal self-regulation, and swarm intelligence.

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: KI/Decision Engine (Python/ML)                │
│  - Neural Networks for high-level planning              │
│  - Sensor fusion and world model                        │
│  - Command generation (12-bit ρ_t format)              │
└──────────────────┬──────────────────────────────────────┘
                   │ Commands: "Move servo 2 to 45°"
                   ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: ρ_t Bootloader (x86 Assembly / Verilog)       │
│  - 512-byte ultra-lean control kernel                  │
│  - Proton/Elektron/Neutron context logic               │
│  - Frust-Zähler: Thermal throttling & safety          │
│  - Neuron 255: Error tracking & feedback               │
│  - Real-time impulse interpretation                    │
└──────────────────┬──────────────────────────────────────┘
                   │ PWM/GPIO signals
                   ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: FPGA Hardware (Lattice iCE40 Verilog)         │
│  - Decentralized DSP-Nodes (mycelial topology)         │
│  - Multi-core parallel execution                       │
│  - Hardware PWM for servo/motor control                │
│  - ADC/sensor interfaces (real-time feedback)          │
│  - Thermal management (voltage scaling)                │
└─────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### Proton (E⁺ Rahmen)
- **Positive Energy Frame**
- Defines context: which servo? which register? which output channel?
- Hardware: upper bits (9-12) of 12-bit instruction
- Biological parallel: axon (defines pathway)

### Elektron (E⁻ Impuls)
- **Negative Impulse**
- The actual command/data value
- Hardware: lower bits (0-8) of 12-bit instruction
- Biological parallel: neurotransmitter (carries signal)

### Neutron (Balance)
- **Equilibrium Logic**
- Stabilization and redundancy
- Hardware: XOR operations, state rotation
- Biological parallel: proprioception (self-awareness)

### Frust-Zähler (Temperature)
- **Thermal Regulation**
- Accumulates on invalid commands (error heat)
- Triggers system pause at threshold (1500 = ~80°C)
- Forces abdominal cooling (reset)
- Safety mechanism against thermal runaway

### Neuron 255 (Memory)
- **Error & Result Storage**
- Permanent record of last operation
- 0xFFFF = failure state
- Tracks system health and failures

---

## Command Format (12-bit)

```
Bit 11-9:  Proton (Rahmen/Context) - 0-7 registers
Bit 8-6:   WO (Destination address) - 0-7
Bit 5-3:   RECHNUNG (Operation) - 0-7
Bit 2-0:   WOHIN (Source) - 0-7

Example: Move value from register 3 to output 2
         0010_010_011_110 = 0x2AE
         ↑    ↑   ↑   ↑
       Prot Dest Reg Src
```

---

## Implementation Status

### Layer 1: KI Engine
- **Status**: Planned
- **Example**: `robotics/servo_control.py`
- Converts high-level actions to 12-bit commands

### Layer 2: ρ_t Bootloader
- **Status**: ✅ Implemented (x86 Assembly)
- **Location**: `bootloader/rho_t_framework.asm`
- **Tested**: QEMU simulation
- **Size**: 512 bytes (MBR format)
- **Features**:
  - 22-instruction interpreter loop
  - Proton/Elektron XOR context
  - Thermal throttling
  - Error logging (Neuron 255)

### Layer 3: FPGA Hardware
- **Status**: 🔄 In progress
- **Target**: Lattice iCE40 HX1K (iCEBreaker)
- **Language**: Verilog
- **Architecture**:
  - Multiple ρ_t CPU instances (8-16 nodes)
  - Hardware PWM generators
  - ADC/sensor interfaces
  - I2C/SPI for communication
  - Thermal monitoring

---

## Use Cases

### 1. Robot Arm with Force Control
```
KI: "Grasp object, max force 20N"
     ↓
Bootloader: Parse Proton=servo_id, Elektron=force
     ↓
FPGA: Generate PWM, monitor force sensor
     ↓
Frust-Zähler: If force exceeds 1500 units → abort & cool
```

### 2. Swarm Robotics (Decentralized)
```
Single iCE40 with 8 ρ_t CPUs
     ↓
Each CPU controls one drone/agent independently
     ↓
Shared Proton bus for context (formation, objective)
     ↓
Local Elektron impulses (individual motor control)
     ↓
Emergent swarm behavior without central bottleneck
```

### 3. Bio-Inspired Movement (Mycelial Robot)
```
Inspired by DSP-Node network topology
     ↓
Multiple servo joints = mycelial "fruiting bodies"
     ↓
Energy distribution = nutrient transport
     ↓
Sensor feedback = chemical signals
     ↓
Self-organizing growth-like movement patterns
```

### 4. Quadrotor/Drone
```
IMU sensors (gyro, accel) → Bootloader state
     ↓
Frust = battery voltage + motor heat
     ↓
Auto-throttle: reduce thrust if Frust > threshold
     ↓
Neuron 255: log crash/failure events
     ↓
Recovery logic: safe landing on thermal shutdown
```

---

## Advantages Over Traditional Approaches

| Metric | Traditional KI→Robot | ρ_t Framework |
|--------|---------------------|---------------|
| **Latency** | 50-200ms (Python stack) | <1ms (Assembly/Hardware) |
| **Power Draw** | 50-100W (CPU/GPU) | 2-5W (FPGA) |
| **Code Size** | 100,000+ LOC | 512 bytes (Bootloader) |
| **Thermal Safety** | Ad-hoc, slow | Built-in Frust-Zähler |
| **Scalability** | Central bottleneck | Decentralized nodes |
| **Sensorik Integration** | Middleware heavy | Direct impulse coupling |
| **Debuggability** | Black-box ML | Traceable byte-by-byte |
| **Real-time Guarantee** | Soft/unreliable | Hard guarantee (HW) |

---

## Biological Inspiration

### Mycelial Network Parallels
- **Hyphen Filaments** ↔ Leiterbahnen (PCB traces)
- **Nutrient Transport** ↔ Power distribution
- **Chemical Signals** ↔ Digital impulses
- **Decentralized Growth** ↔ Parallel DSP-Nodes
- **Stress Response** ↔ Frust-Zähler throttling
- **Information Propagation** ↔ Proton broadcast + Elektron impulses

### Quantum-Inspired Biology
- **Proton (E⁺)** ↔ Positive potential, framework
- **Elektron (E⁻)** ↔ Negative impulse, information carrier
- **Neutron** ↔ Balance, stability mechanism
- **Energy State** ↔ ρ_t (Planck-time quantum density)

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] x86 Bootloader implementation
- [x] QEMU simulation
- [ ] Python simulator validation
- [ ] Documentation (THIS FILE)

### Phase 2: FPGA (Weeks 3-4)
- [ ] Verilog translation of Bootloader
- [ ] iCE40 HX1K port
- [ ] Hardware PWM generator
- [ ] Sensor interface (ADC/I2C)

### Phase 3: Robotics Integration (Weeks 5-6)
- [ ] Servo control examples
- [ ] Force sensor fusion
- [ ] Thermal throttling tests
- [ ] Single robot demo

### Phase 4: Swarm & AI (Weeks 7-8)
- [ ] Multiple iCE40 boards
- [ ] KI interface (Python → 12-bit commands)
- [ ] Swarm behavior simulation
- [ ] Bio-inspired movement algorithms

### Phase 5: Production (Weeks 9+)
- [ ] PCB design (custom robot controller)
- [ ] Firmware hardening
- [ ] Embedded Linux integration (RPi 3 host)
- [ ] Open-source release

---

## Getting Started

### Hardware You Need
1. **iCEBreaker FPGA** (~€60)
   - Lattice iCE40 HX1K
   - USB-JTAG on-board
   - RPi GPIO header compatible

2. **Raspberry Pi 3** (~€35)
   - Runs KI inference & coordination
   - Communicates with iCE40 via SPI/USB

3. **Servo Motors/Actuators** (~€20-50)
   - Controlled via FPGA PWM
   - Feedback via ADC

4. **Sensors** (~€30-50)
   - IMU, force sensors, distance sensors
   - ADC interface on FPGA

### Software You Need
1. **Verilog Toolchain**
   ```bash
   apt-get install yosys nextpnr icestorm
   ```

2. **Python KI Framework**
   ```bash
   pip install numpy tensorflow pytorch
   ```

3. **FPGA Programmer**
   ```bash
   apt-get install openocd
   ```

### Quick Start Example
```python
# Layer 1: KI decides
target_angle = 45.0
force = 0.5

# Layer 2: Encode to 12-bit command
proton = 2 << 9          # Servo 2
elektron = int(angle * 5.68)  # Angle in steps
cmd = proton | elektron

# Layer 3: Send to FPGA Bootloader
fpga.send_command(cmd)

# Feedback loop
actual_angle = fpga.read_servo_angle(2)
frust = fpga.read_thermal()
if frust > 1000:
    print("THERMAL WARNING!")
```

---

## Contributing

This is an open-source research project (MIT License).

Areas needing help:
- [ ] Verilog implementation & optimization
- [ ] FPGA testing on iCEBreaker
- [ ] KI inference models
- [ ] Mechanical design (robot platform)
- [ ] Documentation & tutorials
- [ ] Community feedback & use-case development

---

## References & Inspiration

- **Mycelial Networks**: Paul Stamets research on fungal intelligence
- **Quantum Biology**: Penrose-Hameroff orchestrated objective reduction
- **x86 Assembly**: Classic bootloader design
- **FPGA**: Open-source toolchain (Yosys, nextpnr, icestorm)
- **Robotics**: ROS, reactive control systems
- **AI**: Spiking neural networks, neuromorphic computing

---

## Contact & Discussion

Questions? Ideas? Want to contribute?

Open an issue or start a discussion in the repository.

**This is a community project – your input matters!**
