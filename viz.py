import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from experiment import ExperimentRunner
from assets import load_pattern
import numpy as np

def run_visualization(width=80, height=60, steps=200, initial_noise=0.0, max_noise=0.05):
    """
    Game of Life visualization with default toolbar and keyboard controls.
    Controls:
        Space: Pause/Resume
        Left Arrow: Step Backward (History)
        Right Arrow: Step Forward (History)
    """
    runner = ExperimentRunner(width, height, density=0)
    load_pattern(runner.control, "gosper_glider_gun", 10, 10)
    runner.test.grid = runner.control.grid.copy()
    
    state = {
        'paused': False,
        'current_idx': 0,
        'history': [],
        'layout': None
    }

    # Initial state
    stats = runner.get_delta_stats()
    state['history'].append((runner.control.grid.copy(), runner.test.grid.copy(), 0.0, stats))

    fig = plt.figure(figsize=(12, 7))
    
    def setup_layout(layout_type):
        fig.clear()
        if layout_type == 'horizontal':
            axes = [fig.add_subplot(1, 3, i+1) for i in range(3)]
        else:
            axes = [fig.add_subplot(3, 1, i+1) for i in range(3)]
        
        curr = state['history'][state['current_idx']]
        im1 = axes[0].imshow(curr[0], cmap='binary', vmin=0, vmax=1)
        axes[0].set_title("Control")
        im2 = axes[1].imshow(curr[1], cmap='binary', vmin=0, vmax=1)
        axes[1].set_title("Test (Noise)")
        im3 = axes[2].imshow(curr[0] ^ curr[1], cmap='magma', vmin=0, vmax=1)
        axes[2].set_title("Delta")
        
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        return axes, [im1, im2, im3]

    # Initialize
    state['layout'] = 'horizontal'
    axes, ims = setup_layout('horizontal')
    text = fig.suptitle(f"Step: 0 | Noise: 0.0000 [Playing]")

    def update_ui():
        idx = state['current_idx']
        mode = "[Paused]" if state['paused'] else "[Playing]"
        if idx < len(state['history']):
            _, _, noise, stats = state['history'][idx]
            text.set_text(f"Step: {idx} | Noise: {noise:.4f} | Diff: {stats[0]} ({stats[1]:.2f}%) {mode}")
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

    def on_resize(event):
        nonlocal axes, ims
        new_layout = 'horizontal' if event.width > event.height * 1.1 else 'vertical'
        if new_layout != state['layout']:
            state['layout'] = new_layout
            axes, ims = setup_layout(new_layout)
            update_ui()

    fig.canvas.mpl_connect('resize_event', on_resize)

    def update(frame):
        if not state['paused'] and state['current_idx'] < steps:
            state['current_idx'] += 1
        
        idx = state['current_idx']
        while len(state['history']) <= idx:
            step_num = len(state['history'])
            noise_p = initial_noise + (max_noise - initial_noise) * (step_num / steps)
            runner.step(noise_p=noise_p)
            s = runner.get_delta_stats()
            state['history'].append((runner.control.grid.copy(), runner.test.grid.copy(), noise_p, s))

        ctrl, test, _, _ = state['history'][idx]
        ims[0].set_data(ctrl)
        ims[1].set_data(test)
        ims[2].set_data(ctrl ^ test)
        update_ui()
        return ims + [text]

    ani = FuncAnimation(fig, update, frames=None, interval=50, blit=False, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    run_visualization()
