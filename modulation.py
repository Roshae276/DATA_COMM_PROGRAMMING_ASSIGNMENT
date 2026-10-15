
import numpy as np
import matplotlib.pyplot as plt


def validate_modulation_parameters(step_size, initial_value):
    """Validate Delta Modulation parameters."""
    if not np.isfinite(step_size) or step_size <= 0:
        raise ValueError("Step size must be a positive finite number.")

    if not np.isfinite(initial_value):
        raise ValueError("Initial value must be a finite number.")


def delta_modulation_encode(samples, step_size=0.5, initial_value=0.0):
    """
    Encode analog samples using Delta Modulation.

    Returns:
        bits: 1 means step up; 0 means step down.
        reconstructed: Encoder-side staircase values.
    """
    try:
        samples = np.asarray(samples, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Samples must be numeric.") from error

    if samples.ndim != 1 or len(samples) == 0:
        raise ValueError("Samples must be a non-empty one-dimensional sequence.")

    if not np.all(np.isfinite(samples)):
        raise ValueError("Samples must contain only finite numbers.")

    validate_modulation_parameters(step_size, initial_value)

    step_size = float(step_size)
    reference = float(initial_value)
    bits = []
    reconstructed = []

    for sample in samples:
        if sample > reference:
            bit = 1
            reference += step_size
        else:
            bit = 0
            reference -= step_size

        bits.append(bit)
        reconstructed.append(reference)

    return bits, reconstructed


def delta_modulation_decode(bits, step_size=0.5, initial_value=0.0):
    """Reconstruct the staircase from Delta Modulation bits."""
    bits = list(bits) if isinstance(bits, (list, tuple, np.ndarray)) else None
    if not bits:
        raise ValueError("Bits must be a non-empty sequence.")

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("Bits must contain only 0 and 1 values.")

    validate_modulation_parameters(step_size, initial_value)

    step_size = float(step_size)
    reference = float(initial_value)
    reconstructed = []

    for bit in bits:
        if bit == 1:
            reference += step_size
        else:
            reference -= step_size

        reconstructed.append(reference)

    return reconstructed


def plot_delta_modulation(samples, reconstructed):
    """Plot the input samples and reconstructed staircase."""
    if len(samples) != len(reconstructed) or len(samples) == 0:
        raise ValueError(
            "Samples and reconstructed signal must have equal, nonzero lengths."
        )

    time = np.arange(len(samples))

    plt.figure(figsize=(10, 5))
    plt.plot(time, samples, marker="o", label="Analog input")
    plt.step(
        time,
        reconstructed,
        where="post",
        label="DM reconstructed staircase",
    )

    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.title("Delta Modulation: Input and Reconstructed Signal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analog_samples = [0.2, 0.7, 1.1, 0.6, 0.1]
    step_size = 0.5
    initial_value = 0.0

    bits, encoder_staircase = delta_modulation_encode(
        analog_samples, step_size, initial_value
    )
    decoded_staircase = delta_modulation_decode(
        bits, step_size, initial_value
    )

    print("Analog samples:", analog_samples)
    print("Delta Modulation bits:", bits)
    print("Encoder staircase:", encoder_staircase)
    print("Decoder staircase:", decoded_staircase)
    print(
        "Encoder/decoder agreement:",
        "PASS" if encoder_staircase == decoded_staircase else "FAIL",
    )

    plot_delta_modulation(analog_samples, decoded_staircase)
