
import matplotlib.pyplot as plt


def plot_signal(signal, title, save_path=None, show_plot=True):
    """Plot a digital line-coded signal using a step waveform."""
    if not signal:
        raise ValueError("Signal must be a non-empty sequence.")

    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("Signal levels must be -1, 0, or 1.")

    time = list(range(len(signal) + 1))
    levels = list(signal) + [signal[-1]]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.step(time, levels, where="post", color="blue", linewidth=2.5)
    ax.set_xlabel("Signal interval")
    ax.set_ylabel("Voltage level")
    ax.set_title(title)
    ax.set_yticks([-1, 0, 1])
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=100)

    if show_plot:
        plt.show()
    else:
        plt.close(fig)


def plot_scrambling_comparison(
    original_signal, scrambled_signal, scramble_name, save_path=None, show_plot=True
):
    """Plot original AMI signal and scrambled signal side-by-side (2 subplots) for comparison."""
    if not original_signal or not scrambled_signal:
        raise ValueError("Signals must not be empty.")

    time_orig = list(range(len(original_signal) + 1))
    levels_orig = list(original_signal) + [original_signal[-1]]

    time_scram = list(range(len(scrambled_signal) + 1))
    levels_scram = list(scrambled_signal) + [scrambled_signal[-1]]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax1.step(time_orig, levels_orig, where="post", color="blue", linewidth=2.2)
    ax1.set_ylabel("Voltage level")
    ax1.set_title("Standard AMI Signal (Unscrambled)")
    ax1.set_yticks([-1, 0, 1])
    ax1.set_ylim(-1.5, 1.5)
    ax1.grid(True)

    ax2.step(time_scram, levels_scram, where="post", color="crimson", linewidth=2.2)
    ax2.set_xlabel("Signal interval")
    ax2.set_ylabel("Voltage level")
    ax2.set_title(f"Scrambled Signal ({scramble_name})")
    ax2.set_yticks([-1, 0, 1])
    ax2.set_ylim(-1.5, 1.5)
    ax2.grid(True)

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=100)

    if show_plot:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    test_signal = [1, 1, -1, 0, -1, 1]
    plot_signal(test_signal, "Digital Signal Test")
