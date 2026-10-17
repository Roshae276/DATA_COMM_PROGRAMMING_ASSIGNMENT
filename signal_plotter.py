
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


if __name__ == "__main__":
    test_signal = [1, 1, -1, 0, -1, 1]
    plot_signal(test_signal, "Digital Signal Test")
