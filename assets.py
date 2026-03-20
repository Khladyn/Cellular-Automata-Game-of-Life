import numpy as np

# Patterns defined as list of strings where 'O' is alive and '.' is dead
PATTERNS = {
    "glider": [
        ".O.",
        "..O",
        "OOO"
    ],
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
    "block": [
        "OO",
        "OO"
    ]
}

def get_pattern_array(name: str):
    """Returns a numpy array for the requested pattern name."""
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
    Loads a pattern into the engine's grid.
    If offsets are None, it centers the pattern.
    """
    pattern = get_pattern_array(name)
    ph, pw = pattern.shape
    
    if x_offset is None:
        x_offset = (engine.width - pw) // 2
    if y_offset is None:
        y_offset = (engine.height - ph) // 2
        
    # Boundary checks / slicing
    y_start = max(0, y_offset)
    y_end = min(engine.height, y_offset + ph)
    x_start = max(0, x_offset)
    x_end = min(engine.width, x_offset + pw)
    
    # Slice the pattern if it's partially outside
    py_start = y_start - y_offset
    py_end = py_start + (y_end - y_start)
    px_start = x_start - x_offset
    px_end = px_start + (x_end - x_start)
    
    engine.grid[y_start:y_end, x_start:x_end] = pattern[py_start:py_end, px_start:px_end]

if __name__ == "__main__":
    from engine import GameOfLifeEngine
    e = GameOfLifeEngine(50, 20)
    load_pattern(e, "gosper_glider_gun", 5, 5)
    print("Loaded Gosper Glider Gun:")
    # Simple print of the grid segment
    print(e.grid[5:14, 5:41])
