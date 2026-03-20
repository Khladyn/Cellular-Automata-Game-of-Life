from engine import GameOfLifeEngine
from assets import load_pattern
import numpy as np

def check_pulsar_period():
    engine = GameOfLifeEngine(20, 20)
    load_pattern(engine, "pulsar")
    
    initial_state = engine.grid.copy()
    states = [initial_state]
    
    for i in range(1, 6):
        engine.step()
        current_state = engine.grid.copy()
        for prev_idx, prev_state in enumerate(states):
            if np.array_equal(current_state, prev_state):
                print(f"Step {i} matches Step {prev_idx}. Period is {i - prev_idx}.")
                return
        states.append(current_state)

if __name__ == "__main__":
    check_pulsar_period()
