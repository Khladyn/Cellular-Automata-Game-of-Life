import argparse
from visualization.viz import run_visualization
from visualization.plot_results import generate_full_research_dashboard

def main():
    parser = argparse.ArgumentParser(description="Game of Life: Stochastic Dissolution Research Tool")
    parser.add_argument("--viz", action="store_true", help="Run the interactive visualization instead of the research batch")
    parser.add_argument("--pattern", type=str, default="gosper_glider_gun", 
                        choices=["block", "pulsar", "glider", "gosper_glider_gun"],
                        help="Pattern to use for visualization (default: gosper_glider_gun)")
    parser.add_argument("--noise", type=float, default=1e-5,
                        help="Constant noise probability for visualization (default: 1e-5)")
    parser.add_argument("--no-noise", action="store_true",
                        help="Run the simulation without any stochastic noise (p=0)")
    parser.add_argument("--ramp", action="store_true",
                        help="If set, noise will ramp from 0 to --noise over the course of the simulation")
    parser.add_argument("--save", type=str, default=None,
                        help="If set, saves the final visualization frame to this path and exits")
    parser.add_argument("--no-eater", action="store_true",
                        help="Disable the default Eater 1 pattern")
    parser.add_argument("--eater-x", type=int, default=85,
                        help="X coordinate for the Eater 1 pattern (default: 85)")
    parser.add_argument("--eater-y", type=int, default=84,
                        help="Y coordinate for the Eater 1 pattern (default: 84)")
    
    args = parser.parse_args()

    if args.viz:
        if args.save:
            print(f"Generating screenshot: {args.save} (Eater: {not args.no_eater})")
        else:
            print(f"Starting Visualization: {args.pattern} @ {'Ramping' if args.ramp else 'Constant'} Noise {args.noise:.1e}")
            if args.no_noise:
                print("Deterministic Mode: Stochastic noise disabled (p=0)")
            if not args.no_eater:
                print(f"Eater 1 deployed at ({args.eater_x}, {args.eater_y})")
            print("Controls: [Space] Pause/Play/Replay | [F] Jump to Failure | [Left/Arrow] Step Frame | [Esc] Close")
        
        noise_level = 0.0 if args.no_noise else args.noise
        init_noise = 0.0 if (args.ramp or args.no_noise) else noise_level
        
        run_visualization(
            pattern_name=args.pattern,
            width=100, 
            height=100, 
            steps=500, 
            initial_noise=init_noise, 
            max_noise=noise_level,
            collapse_threshold=0.2,
            save_path=args.save,
            use_eater=not args.no_eater,
            eater_offset=(args.eater_x, args.eater_y)
        )
    else:
        print("Starting Game of Life: Research Batch & Dashboard Generation...")
        # The Logarithmic Search Space derived from Eigen's Error Threshold (1971)
        ultra_fine_levels = [1e-4, 5e-5, 1e-5, 5e-6, 1e-6, 5e-7, 1e-7]
        generate_full_research_dashboard(ultra_fine_levels)

if __name__ == "__main__":
    main()
