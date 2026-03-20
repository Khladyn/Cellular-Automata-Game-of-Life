import unittest
import numpy as np
from engine import GameOfLifeEngine
from assets import get_pattern_array, load_pattern, PATTERNS
from batch_experiment import run_research_batch

class TestGameOfLifeLogic(unittest.TestCase):
    """
    Formal Verification of the B3/S23 (Conway, 1970) Transition Function.
    Ensures the engine maintains 'Mathematical Integrity' across 
    Wolfram's CA Complexity Classes.
    """

    def setUp(self):
        # Using a 10x10 Grid for deterministic testing
        self.width = 10
        self.height = 10
        self.engine = GameOfLifeEngine(self.width, self.height)

    def test_still_life_stability(self):
        """
        Verification of Class 1: Still Lifes (Block).
        A 2x2 block should remain static (δ(P) = P).
        """
        load_pattern(self.engine, "block", 4, 4)
        initial_state = self.engine.grid.copy()
        
        self.engine.step()
        np.testing.assert_array_equal(self.engine.grid, initial_state, 
                                      "Block pattern (Class 1) must be static.")

    def test_oscillator_periodicity(self):
        """
        Verification of Class 2: Oscillators (Blinker).
        A 3x1 line should toggle between horizontal and vertical (Period 2).
        """
        # Manual Blinker Setup
        self.engine.grid[4, 3:6] = 1 # Horizontal
        
        # Step 1: Should become vertical
        self.engine.step()
        expected_v = np.zeros((10, 10), dtype=np.uint8)
        expected_v[3:6, 4] = 1
        np.testing.assert_array_equal(self.engine.grid, expected_v, 
                                      "Blinker failed horizontal -> vertical transition.")
        
        # Step 2: Should return to horizontal
        self.engine.step()
        expected_h = np.zeros((10, 10), dtype=np.uint8)
        expected_h[4, 3:6] = 1
        np.testing.assert_array_equal(self.engine.grid, expected_h, 
                                      "Blinker failed vertical -> horizontal return.")

    def test_spaceship_kinetics(self):
        """
        Verification of Class 3: Spaceships (Glider).
        Ensures 'Information Transit' across the Moore Neighborhood.
        """
        load_pattern(self.engine, "glider", 1, 1)
        # Glider moves (1,1) every 4 steps
        for _ in range(4):
            self.engine.step()
            
        # Check if glider has shifted to (2,2)
        # Note: Glider at (1,1) has bounding box at (1,1) to (3,3)
        # After 4 steps, it should be at (2,2) to (4,4)
        glider_pattern = get_pattern_array("glider")
        actual_slice = self.engine.grid[2:5, 2:5]
        np.testing.assert_array_equal(actual_slice, glider_pattern, 
                                      "Glider (Class 3) failed to propagate diagonally.")

    def test_toroidal_topology(self):
        """
        Verification of Boundary Conditions (Toroidal / Wrapping).
        Ensures 'Information Conservation' at the grid limits.
        """
        # Place a single cell at (0,0) and neighbors at (0,9), (9,0), (9,9)
        # This should trigger a birth at (0,0) or (9,9) etc.
        # Specifically: A 2x2 block at the corner.
        self.engine.grid[0, 0] = 1
        self.engine.grid[0, 9] = 1
        self.engine.grid[9, 0] = 1
        self.engine.grid[9, 9] = 1
        
        # This is a 2x2 block split across 4 corners. It should be static.
        self.engine.step()
        self.assertEqual(self.engine.grid[0, 0], 1)
        self.assertEqual(self.engine.grid[0, 9], 1)
        self.assertEqual(self.engine.grid[9, 0], 1)
        self.assertEqual(self.engine.grid[9, 9], 1)
        self.assertEqual(np.sum(self.engine.grid), 4, "Toroidal boundary failed to maintain Block stability.")

    def test_stochastic_noise_application(self):
        """
        Verification of the Bernoulli Noise Agent (η).
        Ensures noise correctly flips bits according to probability p.
        """
        p = 0.5
        # Set grid to all zeros
        self.engine.grid[:] = 0
        np.random.seed(42) # Deterministic noise for testing
        self.engine.apply_stochastic_noise(p)
        
        # Statistical check: approx 50% should be 1
        mean_val = np.mean(self.engine.grid)
        self.assertTrue(0.4 < mean_val < 0.6, f"Noise density {mean_val} outside expected range for p=0.5")

class TestAssetsAndExperiments(unittest.TestCase):
    """
    Verification of Data Integrity and Batch Execution Logic.
    """

    def test_pattern_loading_centering(self):
        """Verifies that patterns are loaded and centered correctly by default."""
        engine = GameOfLifeEngine(20, 20)
        load_pattern(engine, "block") # 2x2 pattern
        # Center of 20x20 is (10,10). (20-2)//2 = 9. So offset (9,9).
        self.assertEqual(engine.grid[9, 9], 1)
        self.assertEqual(engine.grid[10, 10], 1)
        self.assertEqual(np.sum(engine.grid), 4)

    def test_batch_experiment_execution(self):
        """
        Verifies that run_research_batch returns expected statistical structure.
        Ensures the 'Complexity-Fragility Gap' data can be generated.
        """
        noise_levels = [0.0, 1.0] # Test extremes
        # Very small batch for speed
        results = run_research_batch(noise_levels, "block", trials_per_level=2, steps_per_trial=10)
        
        self.assertIn(0.0, results)
        self.assertIn(1.0, results)
        self.assertEqual(results[0.0]['success_rate'], 100.0, "Zero noise should yield 100% success for Block.")
        self.assertEqual(results[1.0]['success_rate'], 0.0, "100% noise should yield 0% success.")

if __name__ == "__main__":
    unittest.main()
