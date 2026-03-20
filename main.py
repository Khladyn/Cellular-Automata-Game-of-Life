from viz import run_visualization

if __name__ == "__main__":
    print("Starting Game of Life: Stochastic Dissolution Experiment...")
    print("Closing the window will terminate the simulation.")
    
    # You can tweak parameters here:
    # width/height: Grid size
    # steps: How long the animation runs
    # max_noise: The final probability of a bit flip (0.05 = 5% of cells flip every step)
    run_visualization(
        width=100, 
        height=80, 
        steps=300, 
        initial_noise=0.0, 
        max_noise=0.02
    )
