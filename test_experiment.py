import numpy as np
from experiment import ExperimentRunner

def test_experiment_no_noise():
    # 1. Test: No noise -> Simulations should stay identical
    runner = ExperimentRunner(10, 10, density=0.5)
    for _ in range(20):
        runner.step(noise_p=0)
        diff_count, _ = runner.get_delta_stats()
        assert diff_count == 0, f"Simulations diverged without noise (diff count: {diff_count})"
    print("Test: No noise (Identity) passed!")

def test_experiment_with_noise():
    # 2. Test: With noise -> Simulations should diverge
    runner = ExperimentRunner(50, 50, density=0.2)
    # Give it a few steps with noise
    for _ in range(5):
        runner.step(noise_p=0.05)
    
    diff_count, _ = runner.get_delta_stats()
    assert diff_count > 0, "Simulations did not diverge with noise"
    print(f"Test: With noise (Divergence) passed! (Diff count: {diff_count})")

if __name__ == "__main__":
    test_experiment_no_noise()
    test_experiment_with_noise()
