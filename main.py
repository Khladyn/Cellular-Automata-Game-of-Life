import argparse
from visualization.viz import run_visualization
from visualization.plot_results import generate_full_research_dashboard

def main():
    parser = argparse.ArgumentParser(description="Game of Life: Stochastic Dissolution Research Tool")
    parser.add_argument("--viz", action="store_true", help="Run the interactive visualization instead of the research batch")
    
    args = parser.parse_args()

    if args.viz:
        print("Starting Game of Life: Stochastic Dissolution Visualization...")
        print("Closing the window will terminate the simulation.")
        # Interactive Visualization Parameters
        run_visualization(
            width=100, 
            height=80, 
            steps=300, 
            initial_noise=0.0, 
            max_noise=0.02
        )
    else:
        print("Starting Game of Life: Research Batch & Dashboard Generation...")
        # The Logarithmic Search Space derived from Eigen's Error Threshold (1971)
        ultra_fine_levels = [1e-4, 5e-5, 1e-5, 5e-6, 1e-6, 5e-7, 1e-7]
        generate_full_research_dashboard(ultra_fine_levels)

if __name__ == "__main__":
    main()
