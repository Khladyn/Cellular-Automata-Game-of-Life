import matplotlib.pyplot as plt
import numpy as np
from batch_experiment import run_research_batch

def generate_comparative_plots(levels):
    # 1. Gather data for both groups
    complex_data = run_research_batch(levels, pattern_name="gosper_glider_gun", trials_per_level=100, steps_per_trial=1000)
    simple_data = run_research_batch(levels, pattern_name="block", trials_per_level=100, steps_per_trial=1000)
    
    noise_levels = sorted(complex_data.keys())
    
    # Complex (Glider Gun) data
    complex_avg = [complex_data[p]['avg_fail'] for p in noise_levels]
    complex_std = [complex_data[p]['std_fail'] for p in noise_levels]
    complex_success = [complex_data[p]['success_rate'] for p in noise_levels]
    
    # Simple (Block) data
    simple_avg = [simple_data[p]['avg_fail'] for p in noise_levels]
    simple_std = [simple_data[p]['std_fail'] for p in noise_levels]

    # Create a 2-panel figure: Line Plot and Bar Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 14))

    # --- Plot 1: Survival Curve (Line Plot) ---
    ax1.errorbar(noise_levels, complex_avg, yerr=complex_std, fmt='-o', 
                 capsize=5, color='tab:blue', ecolor='tab:blue', alpha=0.8,
                 label='Gosper Glider Gun (Complex Logic)')
    
    ax1.errorbar(noise_levels, simple_avg, yerr=simple_std, fmt='-s', 
                 capsize=5, color='tab:gray', ecolor='tab:gray', alpha=0.5,
                 label='Static Block (Simple Control)')
    
    ax1.set_xscale('log')
    ax1.set_xlabel('Noise Probability Level (Log Scale)')
    ax1.set_ylabel('Average Steps to Collapse (Max 1000)')
    ax1.set_title('Survival Analysis: Complexity vs. Stability', fontweight='bold', pad=15)
    ax1.legend()
    ax1.grid(True, which="both", ls="-", alpha=0.1)

    # --- Plot 2: Reliability Limit (Bar Plot) ---
    # Specifically for the Complex Pattern (Glider Gun) to show its "Brittleness"
    x_labels = [f"{p:.1e}" for p in noise_levels]
    bars = ax2.bar(x_labels, complex_success, color='tab:blue', alpha=0.7)
    
    ax2.set_ylim(0, 105)
    ax2.set_xlabel('Noise Probability Level')
    ax2.set_ylabel('Success Rate (Survived 1000 Steps) %')
    ax2.set_title('System Reliability: The Stochastic Stability Limit', fontweight='bold', pad=15)
    
    # Add percentage labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

    plt.tight_layout(pad=5.0)
    plt.savefig('research_results.png', dpi=300)
    print("\nRESEARCH RESULTS SAVED: 'research_results.png'")
    plt.show()

if __name__ == "__main__":
    # Full Logarithmic research range
    ultra_fine_levels = [1e-4, 5e-5, 1e-5, 5e-6, 1e-6, 5e-7, 1e-7]
    generate_comparative_plots(ultra_fine_levels)
