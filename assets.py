import numpy as np

# Initial State Configurations (S_0)
# These represent the 'Information Density' of each pattern class.
# Reference: Wolfram (2002) - Classification of CA Universalities.
PATTERNS = {
    # Class 3: Spaceships (The Kinetic Information Unit)
    # This represents data 'in transit' across the Moore Neighborhood.
    "glider": [
        ".O.",
        "..O",
        "OOO"
    ],
    # Class 4: Infinite Growth / Engines (The Logic Gate)
    # The primary 'Unit of Computation' for the Gosper-Stochastic Limit (L_GS).
    # Its high cell count (N) makes it the most 'fragile' under Bernoulli noise.
    "gosper_glider_gun": [
        "........................O...........",
        "......................O.O...........",
        "............OO......OO............OO",
        "...........O...O....OO............OO",
        "OO........O.....O...OO..............",
        "OO........O...O.OO....O.O...........",
        "..........O.....O.......O...........",
        "...........O...O....................",
        "............OO......................"
    ],
    # Class 2: Oscillators (Temporal Complexity)
    # A period-3 pattern representing a high-density 'cyclic' attractor.
    # Vulnerable to 'Phase-Shift' errors during its 3-step transition.
    "pulsar": [
        "..OOO...OOO..",
        ".............",
        "O....O.O....O",
        "O....O.O....O",
        "O....O.O....O",
        "..OOO...OOO..",
        ".............",
        "..OOO...OOO..",
        "O....O.O....O",
        "O....O.O....O",
        "O....O.O....O",
        ".............",
        "..OOO...OOO.."
    ],
    # Class 1: Still Lifes (The Control Group)
    # The 'Baseline of Robustness' (N=4).
    # Used to identify the minimum threshold of Stochastic Stability.
    "block": [
        "OO",
        "OO"
    ],
    # Eater 1: A stable 7-cell still life (Fishhook) that consumes gliders.
    "eater": [
        "OO..",
        "O.O.",
        "..O.",
        "..OO"
    ]
}


def get_pattern_array(name: str):
    """
    Pattern Parser / Matrix Encoder.
    Converts Symbolic Grammar ('.', 'O') into a Binary State Matrix (0, 1).
    """
    if name not in PATTERNS:
        raise ValueError(f"Pattern '{name}' not found.")

    lines = PATTERNS[name]
    height = len(lines)
    width = len(lines[0])

    arr = np.zeros((height, width), dtype=np.uint8)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'O':
                arr[y, x] = 1
    return arr


def load_pattern(engine, name: str, x_offset: int = None, y_offset: int = None):
    """
    Spatial Initialization Logic.
    Centers the pattern to minimize 'Edge-Wrapping' (Toroidal) noise artifacts
    during early simulation steps.
    """
    pattern = get_pattern_array(name)
    ph, pw = pattern.shape

    # Rationale: Centering provides a 'Vacuum Buffer' for noise accumulation analysis.
    if x_offset is None:
        x_offset = (engine.width - pw) // 2
    if y_offset is None:
        y_offset = (engine.height - ph) // 2

    # Spatial Boundary Enforcement:
    # Ensures the simulation maintains 'Information Integrity' at the grid limits.
    y_start = max(0, y_offset)
    y_end = min(engine.height, y_offset + ph)
    x_start = max(0, x_offset)
    x_end = min(engine.width, x_offset + pw)

    py_start = y_start - y_offset
    py_end = py_start + (y_end - y_start)
    px_start = x_start - x_offset
    px_end = px_start + (x_end - x_start)

    engine.grid[y_start:y_end, x_start:x_end] = pattern[py_start:py_end, px_start:px_end]