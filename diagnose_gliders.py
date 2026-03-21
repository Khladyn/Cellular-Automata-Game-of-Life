import numpy as np
from engine import GameOfLifeEngine
from assets import load_pattern

def track_gliders():
    width, height = 100, 100
    engine = GameOfLifeEngine(width, height)
    load_pattern(engine, "gosper_glider_gun")
    
    # Run until first glider passes (80, 80)
    for step in range(300):
        engine.step()
        # Look specifically around (80, 80)
        region = engine.grid[75:90, 75:90]
        if np.any(region):
            live_y, live_x = np.where(region == 1)
            # Full coordinates
            full_y = live_y + 75
            full_x = live_x + 75
            print(f"Step {step}: {len(live_x)} cells in region.")
            # If it's just one glider (5 cells)
            if 5 <= len(live_x) <= 6:
                print(f"  Glider found at X:{full_x} Y:{full_y}")
                # Print local grid to see shape
                print(region)
                return

if __name__ == "__main__":
    track_gliders()
