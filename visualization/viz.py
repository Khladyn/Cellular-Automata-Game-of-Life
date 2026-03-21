import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from experiment import ExperimentRunner
from assets import load_pattern
import numpy as np

def run_visualization(pattern_name="gosper_glider_gun", width=100, height=100, steps=500, initial_noise=1e-5, max_noise=None, collapse_threshold=0.2, save_path=None, use_eater=True, eater_offset=(85, 84)):
    """
    Research-grade visualization tracking Information Integrity.
    Aligned with batch_experiment.py logic.
    """
    if max_noise is None:
        max_noise = initial_noise

    runner = ExperimentRunner(width, height, density=0)
    load_pattern(runner.control, pattern_name)
    
    if use_eater:
        # Place eater to intercept gliders at default or specified offset
        load_pattern(runner.control, "eater", x_offset=eater_offset[0], y_offset=eater_offset[1])
        
    runner.test.grid = runner.control.grid.copy()
    
    state = {
        'paused': False,
        'current_idx': 0,
        'history': [],
        'layout': None,
        'collapse_step': None,
        'integrity_history': [],
        'announced_collapse': False
    }

    # Initial state
    stats = runner.get_delta_stats()
    state['history'].append((runner.control.grid.copy(), runner.test.grid.copy(), initial_noise, stats, np.zeros((height, width), dtype=bool)))
    state['integrity_history'].append(stats[3])

    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 0.5])
    
    ax_ctrl = fig.add_subplot(gs[0, 0])
    ax_test = fig.add_subplot(gs[0, 1])
    ax_delta = fig.add_subplot(gs[0, 2])
    ax_graph = fig.add_subplot(gs[1, :])

    # Add grid lines for coordinate tracking
    for ax in [ax_ctrl, ax_test, ax_delta]:
        ax.set_xticks(np.arange(-0.5, width, 10), minor=False)
        ax.set_yticks(np.arange(-0.5, height, 10), minor=False)
        ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.1, alpha=0.5)
        ax.grid(which='major', color='blue', linestyle='-', linewidth=0.5, alpha=0.3)
        ax.tick_params(axis='both', which='major', labelsize=8)

    from matplotlib.colors import ListedColormap
    # Custom colormap: 0=White, 1=Black (Live), 2=Red (Noise/Error)
    test_cmap = ListedColormap(['white', 'black', 'red'])

    im1 = ax_ctrl.imshow(state['history'][0][0], cmap='binary', vmin=0, vmax=1)
    ax_ctrl.set_title(f"Control: {pattern_name}", pad=8)
    
    # Initialize test image with the 3-color map
    im2 = ax_test.imshow(state['history'][0][1], cmap=test_cmap, vmin=0, vmax=2)
    ax_test.set_title("Test (Red = Direct Bit Flips)", pad=8)
    
    im3 = ax_delta.imshow(state['history'][0][0] ^ state['history'][0][1], cmap='magma', vmin=0, vmax=1)
    ax_delta.set_title("Entropy Delta (XOR)", pad=8)
    
    line, = ax_graph.plot([], [], color='green', label='Information Integrity')
    ax_graph.set_xlim(0, steps)
    ax_graph.set_ylim(-0.05, 1.05)
    ax_graph.set_xlabel("Step (t)")
    ax_graph.set_ylabel("Integrity Φ(t)")
    ax_graph.set_title(f"Information Decay @ Noise p={initial_noise:.1e}", pad=8)
    ax_graph.grid(True, alpha=0.3)
    
    marker, = ax_graph.plot([], [], 'go', markersize=4)
    collapse_line = ax_graph.axvline(x=-1, color='red', linestyle='--', alpha=0, label=f'Dissipation Threshold ({1-collapse_threshold:.0%})')
    ax_graph.legend(loc='lower left')

    text = fig.suptitle(f"Pattern: {pattern_name.upper()} | Step: 0 | Integrity: 100%", y=0.97, fontsize=14, fontweight='bold')

    def update_frame(idx):
        while len(state['history']) <= idx:
            step_num = len(state['history'])
            if initial_noise == max_noise:
                noise_p = initial_noise
            else:
                noise_p = initial_noise + (max_noise - initial_noise) * (step_num / steps)
            
            # runner.step() now returns the noise mask
            noise_mask = runner.step(noise_p=noise_p)
            s = runner.get_delta_stats()
            state['history'].append((runner.control.grid.copy(), runner.test.grid.copy(), noise_p, s, noise_mask))
            state['integrity_history'].append(s[3])
            
            if state['collapse_step'] is None and s[3] < (1.0 - collapse_threshold):
                state['collapse_step'] = step_num

        # Use the actual idx provided to show movement past collapse
        ctrl, test, noise, stats, noise_mask = state['history'][idx]
        
        im1.set_data(ctrl)
        
        # Create a display grid for the test map:
        # 0 = Dead, 1 = Live
        # 2 = SOURCE NOISE (Red) - the cells that were flipped in the CURRENT step
        display_test = test.copy().astype(np.uint8)
        # Apply red color ONLY to the bits that were just flipped by noise in this step
        display_test[noise_mask == 1] = 2
        
        im2.set_data(display_test)
        im3.set_data(ctrl ^ test)
        
        mode = ""
        if state['collapse_step'] is not None and idx >= state['collapse_step']:
            mode = f"[DISSIPATED at Step {state['collapse_step']}]"
            text.set_color('red')
            collapse_line.set_xdata([state['collapse_step']])
            collapse_line.set_alpha(0.8)
        else:
            text.set_color('black')

        text.set_text(f"Pattern: {pattern_name.upper()} | Step: {idx} | Noise: {noise:.1e} | Integrity: {stats[3]:.2%} {mode}")
        
        x_data = list(range(len(state['integrity_history'])))
        line.set_data(x_data, state['integrity_history'])
        marker.set_data([idx], [state['integrity_history'][idx]])
        return [im1, im2, im3, line, marker, collapse_line, text]

    if save_path:
        print(f"Generating non-interactive screenshot for {pattern_name}...")
        # Run until collapse or max steps
        for i in range(steps + 1):
            update_frame(i)
            if state['collapse_step'] is not None:
                break
        
        plt.tight_layout(rect=[0, 0, 1, 0.96], h_pad=2.5)
        plt.savefig(save_path, dpi=150)
        plt.close(fig)
        print(f"Screenshot saved to: {save_path}")
        return

    def update(frame):
        if not state['paused']:
            if state['current_idx'] < steps:
                state['current_idx'] += 1
        
        update_frame(state['current_idx'])
        
        # Reset announced_collapse if we are before the collapse step
        # This allows auto-pause to trigger again on replay
        if state['collapse_step'] is not None and state['current_idx'] < state['collapse_step']:
            state['announced_collapse'] = False

        # Auto-pause only at the exact moment of collapse (once)
        if (state['collapse_step'] is not None and 
            state['current_idx'] == state['collapse_step'] and 
            not state['announced_collapse']):
            
            state['paused'] = True
            state['announced_collapse'] = True
            print(f"Structural Collapse detected at Step {state['current_idx']}. Pausing for inspection (Press Space to continue)...")
            
        return [im1, im2, im3, line, marker, collapse_line, text]

    def on_key(event):
        if event.key == ' ':
            if state['current_idx'] >= steps:
                # Replay from 0
                state['current_idx'] = 0
                state['paused'] = False
                state['announced_collapse'] = False
                print("Replaying simulation from Step 0...")
            else:
                state['paused'] = not state['paused']
        elif event.key == 'f':
            if state['collapse_step'] is not None:
                state['current_idx'] = state['collapse_step']
                state['paused'] = True
                print(f"Jumped to Failure Point (Step {state['collapse_step']})")
            else:
                print("Failure point not yet reached.")
        elif event.key == 'left':
            state['paused'] = True
            state['current_idx'] = max(0, state['current_idx'] - 1)
        elif event.key == 'right':
            state['paused'] = True
            state['current_idx'] = min(steps, state['current_idx'] + 1)

    fig.canvas.mpl_connect('key_press_event', on_key)
    ani = FuncAnimation(fig, update, frames=None, interval=30, blit=False, cache_frame_data=False)
    plt.tight_layout(rect=[0, 0, 1, 0.96], h_pad=2.5)
    plt.show()


if __name__ == "__main__":
    run_visualization()
