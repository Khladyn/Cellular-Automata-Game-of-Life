import numpy as np
from experiment import ExperimentRunner
from assets import load_pattern

def run_research_batch(target_noise_levels, pattern_name="gosper_glider_gun", trials_per_level=100, steps_per_trial=300, failure_threshold=0.20):
    """
    Runs multiple trials per noise level for a specific pattern to find 
    the average Step of Failure and Reliability.
    """
    print(f"\nSTARTING RESEARCH BATCH (Pattern: {pattern_name.upper()} | Trials: {trials_per_level})")
    print("-" * 85)
    print(f"{'Noise Level':<12} | {'Success Rate':<15} | {'Avg Step Fail':<15} | {'Std Dev'}")
    print("-" * 85)

    all_results = {}

    for p in target_noise_levels:
        failure_steps = []
        successes = 0
        
        for trial in range(trials_per_level):
            # 1. Initialize for this trial with the specified pattern
            runner = ExperimentRunner(100, 80, density=0)
            load_pattern(runner.control, pattern_name, 10, 10)
            runner.test.grid = runner.control.grid.copy()
            
            failed = False
            for step in range(steps_per_trial):
                runner.step(noise_p=p)
                
                # Check for 'Collapse' using Information Integrity (Pattern Retention)
                stats = runner.get_delta_stats()
                info_integrity = stats[3]
                
                if info_integrity < (1.0 - failure_threshold):
                    failure_steps.append(step)
                    failed = True
                    break 
            
            if not failed:
                successes += 1
        
        # Calculate statistics
        success_rate = (successes / trials_per_level) * 100
        avg_fail = np.mean(failure_steps) if failure_steps else 0.0
        std_fail = np.std(failure_steps) if failure_steps else 0.0
        
        avg_display = f"{avg_fail:.1f}" if failure_steps else "N/A"
        std_display = f"{std_fail:.1f}" if failure_steps else "N/A"
        
        print(f"{p:<12.1e} | {success_rate:<15.1f}% | {avg_display:<15} | {std_display}")
        
        all_results[p] = {
            'success_rate': success_rate,
            'avg_fail': avg_fail,
            'std_fail': std_fail
        }

    print("-" * 85)
    print(f"BATCH COMPLETE FOR {pattern_name.upper()}\n")
    return all_results

if __name__ == "__main__":
    # Research-grade Logarithmic Levels
    ultra_fine_levels = [1e-4, 1e-5, 1e-6]
    
    # 1. THE EXPERIMENT: Complex Pattern
    run_research_batch(ultra_fine_levels, pattern_name="gosper_glider_gun", trials_per_level=100, steps_per_trial=500)
    
    # 2. THE CONTROL GROUP: Simple Static Pattern
    # This proves that the noise isn't just "killing everything" but specifically disrupting logic.
    run_research_batch(ultra_fine_levels, pattern_name="block", trials_per_level=100, steps_per_trial=500)
