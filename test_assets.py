from engine import GameOfLifeEngine
from assets import load_pattern, get_pattern_array
import numpy as np

def test_load_pattern():
    engine = GameOfLifeEngine(10, 10)
    
    # Test: Load Glider at (1,1)
    load_pattern(engine, "glider", 1, 1)
    glider = get_pattern_array("glider")
    
    # Check if pattern is there
    assert np.array_equal(engine.grid[1:4, 1:4], glider), "Glider not loaded correctly at offset"
    print("Test: Load Pattern at Offset passed!")
    
    # Test: Centering
    engine_center = GameOfLifeEngine(10, 10)
    load_pattern(engine_center, "glider")
    # Glider is 3x3. Centering on 10x10: (10-3)//2 = 3. So offset 3,3.
    assert np.array_equal(engine_center.grid[3:6, 3:6], glider), "Glider not centered correctly"
    print("Test: Load Pattern Centered passed!")

if __name__ == "__main__":
    test_load_pattern()
