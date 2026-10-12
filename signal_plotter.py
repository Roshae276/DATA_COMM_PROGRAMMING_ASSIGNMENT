
import matplotlib.pyplot as plt


def plot_signal(signal, title):
    """Plot a digital line-coded signal using a step waveform."""
    if not isinstance(signal, (list, tuple)) or not signal:
        raise ValueError("Signal must be a non-empty list or tuple.")

    if any(
        isinstance(level, bool) or level not in (-1, 0, 1)
        for level in signal
    ):
        raise ValueError("Signal levels must be -1, 0, or 1.")

    time = list(range(len(signal) + 1))
    levels = list(signal) + [signal[-1]]

    plt.figure(figsize=(10, 4))
    plt.step(time, levels, where="post")
    plt.xlabel("Signal interval")
    plt.ylabel("Voltage level")
    plt.title(title)
    plt.yticks([-1, 0, 1])
    plt.ylim(-1.5, 1.5)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    test_signal = [1, 1, -1, 0, -1, 1]
    plot_signal(test_signal, "Digital Signal Test")
