# Game of Life: Stochastic Dissolution Research Tool

A specialized implementation of Conway's Game of Life (B3/S23) designed to study the effects of stochastic noise on pattern integrity. This tool uses a **Stochastic Cellular Automata (SCA)** engine to introduce Bernoulli noise (random bit-flips) and measure how information decays over time.

## 🚀 Quick Start

### 1. Installation
Ensure you have Python 3.8+ installed. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Interactive Visualization
Visualize the "Gosper Glider Gun" decaying under noise:
```bash
python main.py --viz
```

### 3. Run Research Batch
Generate a full research dashboard comparing different noise levels across pattern classes:
```bash
python main.py
```
Outputs are saved in the `research_output/` directory.

---

## 🎮 Interactive Controls
When running in `--viz` mode, use the following keys:
- **[Space]**: Pause / Play / Replay (at end of simulation)
- **[F]**: Jump to **Structural Collapse** (where integrity falls below 80%)
- **[Left/Right Arrow]**: Step backward/forward by one frame
- **[Esc]**: Close visualization

---

## 🛠 Command Line Options

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--viz` | Run the interactive visualization mode | Research Batch |
| `--pattern` | Choose: `block`, `pulsar`, or `glider` | `gosper_glider_gun` |
| `--noise` | Set the constant noise probability (p) | `1e-5` |
| `--no-noise` | Disable all stochastic noise (Deterministic mode) | `False` |
| `--ramp` | Increase noise linearly from 0 to `--noise` over 500 steps | `False` |
| `--save [path]` | Save the final frame as a screenshot and exit | `None` |
| `--no-eater` | Disable the "Eater 1" pattern (only for Glider Gun) | `False` |

---

## 💡 Example Commands

**Observe high-noise interference on a Pulsar oscillator:**
```bash
python main.py --viz --pattern pulsar --noise 1e-3
```

**Test "Information Decay" by ramping noise on a Glider:**
```bash
python main.py --viz --pattern glider --ramp --noise 1e-4
```

**Run a deterministic (no noise) simulation for benchmarking:**
```bash
python main.py --viz --no-noise
```

**Save a high-resolution screenshot of a failure state:**
```bash
python main.py --viz --pattern gosper_glider_gun --noise 5e-5 --save research_output/collapse_frame.png
```

---

## 🔬 Core Concepts

### Stochastic Noise (η)
The engine implements the mapping: `δ_stochastic(P) = δ_deterministic(P) ⊕ η`, where `η` is a Bernoulli Noise Agent. This introduces environmental entropy via XOR bit-flip operations.

### Visualization Color Guide
- **Black**: Live cells (Standard)
- **White**: Dead cells (Standard)
- **Red**: **Noise Birth** (Bit-flip forced a dead cell to live)
- **Blue**: **Noise Death** (Bit-flip forced a live cell to die)

### Information Integrity (Φ)
The tool tracks the "Information Integrity" by comparing the noisy simulation (Test) against a perfect, noise-free simulation (Control). Structural collapse is defined as the point where the test grid diverges significantly from the control.

---

## 📁 Project Structure
- `main.py`: Entry point for both research and visualization.
- `engine.py`: Core logic for the Game of Life and noise application.
- `assets.py`: Predefined patterns (Still Life, Oscillators, Spaceships).
- `visualization/`: Matplotlib-based rendering and dashboard generation.
- `research_output/`: Storage for generated plots and CSV data.
