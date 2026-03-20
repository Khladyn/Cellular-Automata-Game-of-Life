import numpy as np


class GameOfLifeEngine:
    """
    Core Stochastic Cellular Automata (SCA) Engine.
    Implements the Mapping: δ_stochastic(P) = δ_deterministic(P) ⊕ η
    where η is the Bernoulli Noise Agent.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Representing the Grid as a Finite Automaton Matrix
        self.grid = np.zeros((height, width), dtype=np.uint8)

    def seed(self, density: float = 0.2):
        """Initial Configuration (S_0) used for benchmarking entropy growth."""
        self.grid = (np.random.random((self.height, self.width)) < density).astype(np.uint8)

    def step(self):
        """
        The Transition Function (δ).
        Implements the B3/S23 (Conway, 1970) rule via 2D Vectorized Convolution.
        """
        # Neighbor counting via Toroidal Topology (np.roll)
        # This treats the grid as a closed surface, ensuring information
        # conservation at the boundaries.
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

        # B3/S23 Boolean Logic:
        # Implements the 'Syntax' of the Wolfram (2002) Framework.
        birth = (self.grid == 0) & (neighbors == 3)
        survive = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))

        self.grid = (birth | survive).astype(np.uint8)

    def apply_stochastic_noise(self, p: float):
        """
        The Bernoulli Noise Agent (η).
        Introduces environmental entropy via Bit-Flip Operations (XOR).
        Reference: Shannon (1948) - Information Entropy.
        """
        if p <= 0:
            return

        # Generates a mask where each cell has probability 'p' of being True
        noise_mask = np.random.random(self.grid.shape) < p

        # XOR Operator (^=):
        # Flips state (0->1 or 1->0) to simulate 'bit-flip' errors.
        # This creates the 'Interface Issue' between determinism and noise.
        self.grid ^= noise_mask.astype(np.uint8)