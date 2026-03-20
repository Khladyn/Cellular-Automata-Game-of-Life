import numpy as np
from engine import GameOfLifeEngine

class ExperimentRunner:
    """Runs two Game of Life simulations side-by-side and compares them."""
    
    def __init__(self, width: int, height: int, density: float = 0.2):
        self.control = GameOfLifeEngine(width, height)
        self.test = GameOfLifeEngine(width, height)
        
        # Seed control
        self.control.seed(density)
        # Copy the state to test so they start identical
        self.test.grid = self.control.grid.copy()
        
    def step(self, noise_p: float = 0.001):
        """
        Advance both simulations by one step.
        Apply noise only to the test simulation.
        Returns the delta (mask of differences).
        """
        # 1. Update both
        self.control.step()
        self.test.step()
        
        # 2. Apply noise to Test
        self.test.apply_stochastic_noise(noise_p)
        
        # 3. Calculate Delta
        return self.get_delta()

    def get_delta(self):
        """Identifies which pixels differ between Control and Test."""
        # XOR identifies bits that are different (1 if different, 0 if same)
        return self.control.grid ^ self.test.grid

    def get_delta_stats(self):
        """Returns the number of differing cells and the percentage."""
        delta = self.get_delta()
        diff_count = np.sum(delta)
        total_cells = delta.size
        return diff_count, (diff_count / total_cells) * 100

if __name__ == "__main__":
    # Quick demonstration
    runner = ExperimentRunner(50, 50, density=0.3)
    print(f"Initial diff count: {runner.get_delta_stats()[0]}")
    
    for i in range(10):
        runner.step(noise_p=0.01) # 1% noise
        diff_count, diff_pct = runner.get_delta_stats()
        print(f"Step {i+1}: Differences = {diff_count} ({diff_pct:.2f}%)")
