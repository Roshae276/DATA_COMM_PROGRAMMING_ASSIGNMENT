# from line_coding import encode_nrz_l
import matplotlib.pyplot as plt


def plot_signal(signal, title):
    time = list(range(len(signal) + 1))

    # Repeat the last level so the waveform ends correctly.
    levels = signal + [signal[-1]] if signal else []

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


# if __name__ == "__main__":
#     data = "0101"
#     signal = encode_nrz_l(data)

#     plot_signal(signal, "NRZ-L Encoding")
