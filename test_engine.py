import numpy as np
from engine import GameOfLifeEngine

def test_engine():
    # Test 1: Block (Static)
    engine = GameOfLifeEngine(4, 4)
    # Block in the middle
    # 0 0 0 0
    # 0 1 1 0
    # 0 1 1 0
    # 0 0 0 0
    engine.grid[1:3, 1:3] = 1
    
    initial_grid = engine.grid.copy()
    engine.step()
    assert np.array_equal(engine.grid, initial_grid), "Block should be static"
    print("Test 1 (Block) passed!")
    
    # Test 2: Blinker (Period 2)
    engine = GameOfLifeEngine(5, 5)
    # Blinker in the middle
    # 0 0 0 0 0
    # 0 0 1 0 0
    # 0 0 1 0 0
    # 0 0 1 0 0
    # 0 0 0 0 0
    engine.grid[1:4, 2] = 1
    
    engine.step()
    # Should become horizontal:
    # 0 0 0 0 0
    # 0 0 0 0 0
    # 0 1 1 1 0
    # 0 0 0 0 0
    # 0 0 0 0 0
    expected_step_1 = np.zeros((5, 5), dtype=np.uint8)
    expected_step_1[2, 1:4] = 1
    assert np.array_equal(engine.grid, expected_step_1), "Blinker should flip to horizontal"
    
    engine.step()
    # Should flip back
    expected_step_2 = np.zeros((5, 5), dtype=np.uint8)
    expected_step_2[1:4, 2] = 1
    assert np.array_equal(engine.grid, expected_step_2), "Blinker should flip back to vertical"
    print("Test 2 (Blinker) passed!")
    
    # Test 3: Stochastic Noise
    engine = GameOfLifeEngine(100, 100)
    p = 0.1
    # Noise flipped 10% on average
    engine.apply_stochastic_noise(p)
    actual_p = np.mean(engine.grid)
    print(f"Test 3 (Stochastic): actual noise density = {actual_p:.4f} (expected ~{p})")
    assert 0.05 < actual_p < 0.15, "Stochastic noise density out of range"
    print("Test 3 (Stochastic) passed!")

if __name__ == "__main__":
    test_engine()
