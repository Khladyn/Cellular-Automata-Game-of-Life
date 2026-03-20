import numpy as np

class GameOfLifeEngine:
    """Core Game of Life engine with vectorized B3/S23 rule and stochastic noise."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        
    def seed(self, density: float = 0.2):
        """Randomly seed the grid with a given density."""
        self.grid = (np.random.random((self.height, self.width)) < density).astype(np.uint8)
        
    def step(self):
        """Perform one step of the Game of Life using vectorized update rules."""
        # Neighbor counting using slicing (vectorized)
        # We sum all 8 neighbors for each cell
        neighbors = (
            np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grid, 1, axis=0), 0, axis=1) +
            np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(self.grid, 0, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grid, 0, axis=0), -1, axis=1) +
            np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grid, -1, axis=0), 0, axis=1) +
            np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)
        )
        
        # B3/S23 Rule:
        # Survival: Alive if 2 or 3 neighbors
        # Birth: Dead if 3 neighbors
        birth = (self.grid == 0) & (neighbors == 3)
        survive = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        self.grid = (birth | survive).astype(np.uint8)
        
    def apply_stochastic_noise(self, p: float):
        """Flip cell states with probability p across the entire grid."""
        if p <= 0:
            return
            
        noise_mask = np.random.random(self.grid.shape) < p
        # Flip bits: 0 becomes 1, 1 becomes 0 where noise_mask is True
        self.grid ^= noise_mask.astype(np.uint8)
