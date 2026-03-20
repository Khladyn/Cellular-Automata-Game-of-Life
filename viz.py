import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from experiment import ExperimentRunner
from assets import load_pattern
import numpy as np

def run_visualization(width=100, height=80, steps=1000, initial_noise=0.0, max_noise=0.01):
    """
    Research-grade visualization tracking Information Integrity.
    """
    runner = ExperimentRunner(width, height, density=0)
    load_pattern(runner.control, "gosper_glider_gun", 10, 10)
    runner.test.grid = runner.control.grid.copy()
    
    state = {
        'paused': False,
        'current_idx': 0,
        'history': [],
        'layout': None,
        'collapse_step': None,
        'integrity_history': []
    }

    # Initial state
    stats = runner.get_delta_stats()
    # stats = (diff_count, diff_pct, survival_score, info_integrity)
    state['history'].append((runner.control.grid.copy(), runner.test.grid.copy(), 0.0, stats))
    state['integrity_history'].append(stats[3]) # Use Information Integrity

    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 0.6])
    
    ax_ctrl = fig.add_subplot(gs[0, 0])
    ax_test = fig.add_subplot(gs[0, 1])
    ax_delta = fig.add_subplot(gs[0, 2])
    ax_graph = fig.add_subplot(gs[1, :])

    im1 = ax_ctrl.imshow(state['history'][0][0], cmap='binary', vmin=0, vmax=1)
    ax_ctrl.set_title("Control (Reference Pattern)")
    
    im2 = ax_test.imshow(state['history'][0][1], cmap='binary', vmin=0, vmax=1)
    ax_test.set_title("Test (Noise Injected)")
    
    # Still show the full delta visually, but the graph is focused on the pattern
    im3 = ax_delta.imshow(state['history'][0][0] ^ state['history'][0][1], cmap='magma', vmin=0, vmax=1)
    ax_delta.set_title("Delta (Visual Diff)")
    
    # Graph Setup
    line, = ax_graph.plot([], [], color='green', label='Information Integrity')
    ax_graph.set_xlim(0, steps)
    ax_graph.set_ylim(-0.05, 1.05)
    ax_graph.set_xlabel("Step")
    ax_graph.set_ylabel("Pattern Retention Score")
    ax_graph.set_title("Information Decay (Intended vs. Actual Logic Cells)")
    ax_graph.grid(True, alpha=0.3)
    
    marker, = ax_graph.plot([], [], 'go', markersize=4)
    collapse_line = ax_graph.axvline(x=-1, color='red', linestyle='--', alpha=0)

    text = fig.suptitle(f"Step: 0 | Noise: 0.0000 | Pattern Integrity: 100% [Playing]")

    def update_ui():
        idx = state['current_idx']
        mode = "[Paused]" if state['paused'] else "[Playing]"
        
        # Mark the collapse step if we are at or past it
        if state['collapse_step'] is not None and idx >= state['collapse_step']:
            mode = f"[Collapsed at Step {state['collapse_step']}]"
            text.set_color('red')
        else:
            text.set_color('black')
        
        if idx < len(state['history']):
            _, _, noise, stats = state['history'][idx]
            # Use info_integrity (index 3) for the readout
            text.set_text(f"Step: {idx} | Noise: {noise:.6f} | Pattern Integrity: {stats[3]:.2%} {mode}")
            
            x_data = list(range(len(state['integrity_history'])))
            line.set_data(x_data, state['integrity_history'])
            marker.set_data([idx], [state['integrity_history'][idx]])
            
            if state['collapse_step'] is not None:
                collapse_line.set_xdata([state['collapse_step']])
                collapse_line.set_alpha(0.8)

        fig.canvas.draw_idle()

    def on_key(event):
        if event.key == ' ':
            state['paused'] = not state['paused']
        elif event.key == 'left':
            state['paused'] = True
            state['current_idx'] = max(0, state['current_idx'] - 1)
        elif event.key == 'right':
            state['paused'] = True
            state['current_idx'] = min(steps, state['current_idx'] + 1)
        update_ui()

    fig.canvas.mpl_connect('key_press_event', on_key)

    def update(frame):
        if not state['paused']:
            if state['current_idx'] < steps:
                state['current_idx'] += 1
        
        idx = state['current_idx']
        
        while len(state['history']) <= idx:
            step_num = len(state['history'])
            noise_p = initial_noise + (max_noise - initial_noise) * (step_num / steps)
            runner.step(noise_p=noise_p)
            s = runner.get_delta_stats()
            state['history'].append((runner.control.grid.copy(), runner.test.grid.copy(), noise_p, s))
            state['integrity_history'].append(s[3]) # Use info_integrity
            # Detect Collapse for the first time
            if state['collapse_step'] is None and runner.check_collapse(threshold=0.5):
                state['collapse_step'] = step_num
                state['paused'] = True
                print(f"Collapse detected at Step {step_num}. Noise Probability: {noise_p:.6f}")
                break

        ctrl, test, _, _ = state['history'][idx]
        im1.set_data(ctrl)
        im2.set_data(test)
        im3.set_data(ctrl ^ test)
        update_ui()
        return [im1, im2, im3, line, marker, collapse_line, text]

    ani = FuncAnimation(fig, update, frames=None, interval=30, blit=False, cache_frame_data=False)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    run_visualization()
