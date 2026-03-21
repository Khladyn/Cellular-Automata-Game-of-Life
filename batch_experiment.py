import numpy as np
from experiment import ExperimentRunner
from assets import load_pattern


def run_research_batch(target_noise_levels, pattern_name="gosper_glider_gun", trials_per_level=100, steps_per_trial=500,
                       failure_threshold=0.20):
    """
    Experimental Execution Layer.
    Calculates the System Reliability R(p) for the Gosper-Stochastic Limit.
    """
    # Methodology 4.1: Deterministic Seed for Reproducibility.
    # Ensures that 'random' noise is identical across different pattern classes for fair comparison.
    np.random.seed(42)

    print(f"\nSTARTING RESEARCH BATCH (Pattern: {pattern_name.upper()} | Trials: {trials_per_level})")
    print("-" * 85)
    print(f"{'Noise Level':<12} | {'Success Rate':<15} | {'Avg Step Fail':<15} | {'Std Dev'}")
    print("-" * 85)

    all_results = {}

    for p in target_noise_levels:
        failure_steps = []
        successes = 0

        for trial in range(trials_per_level):
            # Methodology 4.4: Initialization of a 100x100 Grid Environment.
            runner = ExperimentRunner(100, 100, density=0)

            # Spatial Strategy: Centering the pattern to create a 'Vacuum Buffer'.
            load_pattern(runner.control, pattern_name, None, None)
            
            if pattern_name == "gosper_glider_gun":
                # Place eater to intercept gliders at default offset (85, 84)
                load_pattern(runner.control, "eater", x_offset=85, y_offset=84)

            runner.test.grid = runner.control.grid.copy()

            failed = False
            for step in range(steps_per_trial):
                # Apply the Transition Function δ and Bernoulli Noise Agent η.
                runner.step(noise_p=p)

                # Evaluation Metric: Calculating Hamming Distance (D_H).
                # info_integrity = 1.0 - (D_H / Total_Cells)
                stats = runner.get_delta_stats()
                info_integrity = stats[3]

                # Methodology 4.5: Threshold for Structural Collapse.
                # If Information Integrity drops below 80% (failure_threshold 0.2),
                # the pattern is considered 'Dissipated'.
                if info_integrity < (1.0 - failure_threshold):
                    failure_steps.append(step)
                    failed = True
                    break

            if not failed:
                successes += 1
                failure_steps.append(steps_per_trial)

        # Methodology 4.4: Statistical Convergence using Central Limit Theorem.
        success_rate = (successes / trials_per_level) * 100
        avg_fail = np.mean(failure_steps)
        std_fail = np.std(failure_steps)

        avg_display = f"{avg_fail:.1f}" if failure_steps else "N/A"
        std_display = f"{std_fail:.1f}" if failure_steps else "N/A"

        # Data Output for Section 5: Results and Analysis.
        print(f"{p:<12.1e} | {success_rate:<15.1f}% | {avg_display:<15} | {std_display}")

        all_results[p] = {
            'success_rate': success_rate,
            'avg_fail': avg_fail,
            'std_fail': std_fail
        }

    print("-" * 85)
    print(f"BATCH COMPLETE FOR {pattern_name.upper()}\n")
    return all_results