import matplotlib.pyplot as plt
import numpy as np
import os
from batch_experiment import run_research_batch


def generate_full_research_dashboard(levels):
    """
    Data Visualization & Analysis Layer.
    Translates raw stochastic data into a comparative study of
    computational robustness across different CA complexity classes.
    """
    # 4.1 Computational Environment: Directory for result persistence
    output_dir = "research_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 4.2 Pattern Taxonomy: Mapping Classes to Wolfram's Formal Hierarchy
    classes = {
        "Class 1: Static (Block)": "block",
        "Class 2: Oscillator (Pulsar)": "pulsar",
        "Class 3: Spaceship (Glider)": "glider",
        "Class 4: Complex (Glider Gun)": "gosper_glider_gun"
    }

    # 4.4 Simulation Parameters for Statistical Power
    TRIALS = 100
    STEPS = 500

    master_data = {}

    for label, pattern_name in classes.items():
        # Execution of the Batch Experiment (2,800 Total Runs across all classes)
        data = run_research_batch(levels, pattern_name=pattern_name, trials_per_level=TRIALS, steps_per_trial=STEPS)
        master_data[label] = data

        # --- INDIVIDUAL CLASS ANALYSIS ---
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        noise_levels = sorted(data.keys())
        avg_fails = [data[p]['avg_fail'] for p in noise_levels]
        std_fails = [data[p]['std_fail'] for p in noise_levels]
        success_rates = [data[p]['success_rate'] for p in noise_levels]

        # Individual Survival Curve: Visualizing Temporal Decay (Accumulated Entropy)
        # Error bars represent the 1σ standard deviation (N=100)
        ax1.errorbar(noise_levels, avg_fails, yerr=std_fails, fmt='-o', color='tab:blue', capsize=5)
        ax1.set_xscale('log')  # Log-scale identifies orders of magnitude sensitivity
        ax1.set_title(f"Survival Analysis: {label}")
        ax1.set_ylabel(f"Steps survived (max {STEPS})")
        ax1.grid(True, alpha=0.1)

        # Individual Reliability Bar Chart: Mapping Failure Rates
        # Highlights the specific noise floor where System Reliability drops.
        x_labels = [f"{p:.1e}" for p in noise_levels]
        ax2.bar(x_labels, success_rates, color='tab:green', alpha=0.6)
        ax2.set_ylim(0, 105)
        ax2.set_title(f"System Reliability: {label}")
        ax2.set_ylabel("Success Rate %")

        fig.suptitle(f"SCA Robustness Analysis: {label}", y=0.97, fontsize=14, fontweight='bold')
        plt.tight_layout(rect=[0, 0, 1, 0.98], h_pad=3.0)
        safe_label = label.split(':')[0].lower().replace(' ', '_')
        file_path = os.path.join(output_dir, f'results_{safe_label}.png')
        plt.savefig(file_path)
        plt.close()
        print(f"Saved individual graph for {label} to {file_path}")

    # --- 3. MASTER COMPARISON DASHBOARD ---
    # Section 5: Comparative Evaluation of Frameworks (The "Big Picture")
    print("\nGenerating Master Comparison Plots...")
    fig_master, (ax_surv, ax_rel) = plt.subplots(2, 1, figsize=(12, 14))

    # High-contrast color palette for distinction between complexity classes
    colors = ['#2c3e50', '#e67e22', '#27ae60', '#e74c3c']

    for (label, data), color in zip(master_data.items(), colors):
        noise_levels = sorted(data.keys())
        avg_fails = [data[p]['avg_fail'] for p in noise_levels]
        std_fails = [data[p]['std_fail'] for p in noise_levels]
        success_rates = [data[p]['success_rate'] for p in noise_levels]

        # Comparative Survival Analysis: Identifies the 'Complexity-Fragility Gap'
        ax_surv.errorbar(noise_levels, avg_fails, yerr=std_fails, fmt='-o',
                         label=label, color=color, capsize=3, alpha=0.8)

        # Comparative System Reliability: Tracks the Sigmoidal Phase Transition
        ax_rel.plot(noise_levels, success_rates, '-o', label=label, color=color, linewidth=2)

    # Formal Formatting for Academic Inclusion
    ax_surv.set_xscale('log')
    ax_surv.set_xlabel("Noise Probability (Log Scale)")
    ax_surv.set_ylabel(f"Average Steps Survived (max {STEPS})")
    ax_surv.set_title("Survival Analysis Across CA Classes", fontweight='bold', fontsize=14)
    ax_surv.legend()
    ax_surv.grid(True, which="both", alpha=0.1)

    # Reliability Plot Finalization: Highlighting the 50% threshold (R_0.5)
    ax_rel.set_xscale('log')
    ax_rel.set_xlabel("Noise Probability (Log Scale)")
    ax_rel.set_ylabel("Success Rate %")
    ax_rel.set_ylim(-5, 105)
    ax_rel.set_title("System Reliability Across CA Classes", fontweight='bold', fontsize=14)
    ax_rel.axhline(50, color='black', linestyle='--', alpha=0.5, label="Threshold of Collapse (50%)")
    ax_rel.legend()
    ax_rel.grid(True, which="both", alpha=0.1)

    fig_master.suptitle("Comparative Analysis of CA Complexity Classes under Stochastic Noise", y=0.98, fontsize=16, fontweight='bold')
    plt.tight_layout(pad=4.0, rect=[0, 0, 1, 0.99])
    master_file = os.path.join(output_dir, 'master_comparison_dashboard.png')
    plt.savefig(master_file, dpi=300)  # High-DPI for publication quality
    print(f"\nMASTER DASHBOARD SAVED: '{master_file}'")
    plt.show()


if __name__ == "__main__":
    # The Logarithmic Search Space derived from Eigen's Error Threshold (1971)
    ultra_fine_levels = [1e-4, 5e-5, 1e-5, 5e-6, 1e-6, 5e-7, 1e-7]
    generate_full_research_dashboard(ultra_fine_levels)