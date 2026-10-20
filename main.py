
from data_generator import (
    generate_random_data,
    generate_data_with_zeros,
    find_longest_palindrome,
    find_longest_zero_sequence,
)

from line_coding import (
    encode_nrz_l,
    encode_nrz_i,
    encode_manchester,
    encode_differential_manchester,
    encode_ami,
)

from scrambling import (
    encode_b8zs,
    encode_hdb3,
    decode_b8zs,
    decode_hdb3,
)

from signal_plotter import plot_signal, plot_scrambling_comparison
from image_decoder import decode_signal_from_image

from decoder import (
    decode_nrz_l,
    decode_nrz_i,
    decode_manchester,
    decode_differential_manchester,
    decode_ami,
)

from modulation import (
    delta_modulation_encode,
    delta_modulation_decode,
    plot_delta_modulation,
)


ENCODERS = {
    "1": ("NRZ-L", encode_nrz_l),
    "2": ("NRZ-I", encode_nrz_i),
    "3": ("Manchester", encode_manchester),
    "4": ("Differential Manchester", encode_differential_manchester),
    "5": ("AMI", encode_ami),
}

DECODERS = {
    "NRZ-L": decode_nrz_l,
    "NRZ-I": decode_nrz_i,
    "MANCHESTER": decode_manchester,
    "DIFFERENTIAL MANCHESTER": decode_differential_manchester,
    "AMI": decode_ami,
    "B8ZS": decode_b8zs,
    "HDB3": decode_hdb3,
}

SCRAMBLERS = {
    "1": ("B8ZS", encode_b8zs),
    "2": ("HDB3", encode_hdb3),
}


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False

        print("Please enter yes or no.")


def _make_data_generators():
    """
    Build a dispatch table for data source options.
    Keys are the menu option strings; values are zero-argument callables
    that return the binary string (after prompting for length if needed).
    """

    def _with_length(zero_count=None):
        try:
            length = int(input("Enter sequence length: "))
        except ValueError:
            print("Please enter a valid integer length.")
            return None

        if length <= 0:
            print("Length must be positive.")
            return None

        if zero_count is None:
            return generate_random_data(length)

        if length < zero_count:
            print(f"Length must be at least {zero_count}.")
            return None

        return generate_data_with_zeros(length, zero_count)

    return {
        "1": lambda: _with_length(None),
        "2": lambda: _with_length(4),
        "3": lambda: _with_length(8),
        "4": lambda: input("Enter binary data: ").strip(),
    }


_DATA_GENERATORS = _make_data_generators()


def get_digital_data():
    print("\nChoose digital data source:")
    print("1. Generate random data")
    print("2. Generate data with four consecutive zeros")
    print("3. Generate data with eight consecutive zeros")
    print("4. Enter binary data manually")

    choice = input("Choose an option: ").strip()
    generator = _DATA_GENERATORS.get(choice)

    if generator is None:
        print("Invalid option.")
        return None

    data = generator()

    if data is None:
        return None

    if not data or any(bit not in "01" for bit in data):
        print("Invalid input. Enter a non-empty binary string.")
        return None

    return data


def decode_and_display(image_path, encoding_name, num_intervals, original_data):
    print("\n[Extra Credit] Decoding signal by analyzing image waveform parameters...")
    try:
        decoded_data = decode_signal_from_image(image_path, encoding_name, num_intervals)
    except Exception as error:
        print("Image decoding failed:", error)
        return

    print("Decoded digital data (from image):", decoded_data)
    print(
        "Longest palindrome in decoded data:",
        find_longest_palindrome(decoded_data),
    )

    if decoded_data == original_data:
        print("Image decoding verification: PASS (Matched original data!)")
    else:
        print("Image decoding verification: MISMATCH")
        print("Original data: ", original_data)
        print("Decoded data:  ", decoded_data)


def encode_and_plot(data):
    print("\nAvailable line-coding schemes:")

    for key, (name, _) in ENCODERS.items():
        print(f"{key}. {name}")

    choice = input("Choose an encoder: ").strip()

    if choice not in ENCODERS:
        print("Invalid encoder choice.")
        return

    encoding_name, encoder = ENCODERS[choice]
    scrambling_active = False
    ami_signal = None

    if choice == "5" and ask_yes_no(
        "Do you want scrambling? (yes/no): "
    ):
        print("\nChoose scrambling:")

        for key, (name, _) in SCRAMBLERS.items():
            print(f"{key}. {name}")

        scramble_choice = input("Choose scrambling: ").strip()

        if scramble_choice not in SCRAMBLERS:
            print("Invalid scrambling choice.")
            return

        encoding_name, encoder = SCRAMBLERS[scramble_choice]
        scrambling_active = True
        ami_signal = encode_ami(data)

    signal = encoder(data)
    image_path = "encoded_signal.png"

    if scrambling_active:
        print(f"\nSelected encoding: AMI with {encoding_name} Scrambling")
        print("Digital data stream given: ", data)
        print("Original AMI signal:       ", ami_signal)
        print(f"Scrambled signal ({encoding_name}): {signal}")

        comparison_path = "scrambled_comparison.png"
        print(f"Comparison waveform saved to '{comparison_path}'.")
        plot_scrambling_comparison(
            ami_signal, signal, encoding_name, save_path=comparison_path, show_plot=True
        )
        plot_signal(signal, f"{encoding_name} Signal", save_path=image_path, show_plot=False)
    else:
        print("\nSelected encoding:", encoding_name)
        print("Digital data stream given:", data)
        print("Encoded signal:          ", signal)
        print(f"Waveform saved to '{image_path}' for visual analysis.")
        plot_signal(signal, f"{encoding_name} Signal", save_path=image_path)

    if ask_yes_no("\nDo you want to decode the encoded signal? (yes/no): "):
        decode_and_display(image_path, encoding_name, len(signal), data)


def digital_workflow():
    data = get_digital_data()

    if data is None:
        return

    start, zlen = find_longest_zero_sequence(data)

    print("\nDigital data:", data)
    print(
        "Longest palindromic substring:",
        find_longest_palindrome(data),
    )

    if zlen > 0:
        print(f"Longest zero run: length={zlen}, starting at index {start}")

    encode_and_plot(data)


def analog_workflow():
    print("\nEnter analog samples separated by commas.")
    print("Example: 0.2, 0.7, 1.1, 0.6, 0.1")

    raw_samples = input("Analog samples: ").strip()

    try:
        samples = [
            float(value.strip())
            for value in raw_samples.split(",")
        ]

        if not samples:
            print("Enter at least one sample.")
            return

        step_size = float(input("Enter DM step size (e.g. 0.5): "))
        initial_value = float(
            input("Enter initial reference value (e.g. 0): ")
        )

        bits, encoder_staircase = delta_modulation_encode(
            samples,
            step_size=step_size,
            initial_value=initial_value,
        )

        decoded_staircase = delta_modulation_decode(
            bits,
            step_size=step_size,
            initial_value=initial_value,
        )

    except ValueError as error:
        print("Invalid input:", error)
        return

    print("\nAnalog samples:", samples)
    print("Delta Modulation bits:", bits)
    print("Encoder staircase:", encoder_staircase)
    print("Decoder staircase:", decoded_staircase)

    plot_delta_modulation(samples, decoded_staircase)

    if ask_yes_no("\nDo you want to line-encode these bits? (yes/no): "):
        digital_data = "".join(str(bit) for bit in bits)

        print("\nGenerated digital data:", digital_data)
        print(
            "Longest palindromic substring:",
            find_longest_palindrome(digital_data),
        )

        encode_and_plot(digital_data)


def main():
    print("=" * 45)
    print("DIGITAL SIGNAL ENCODER AND DECODER")
    print("=" * 45)
    print("1. Digital input")
    print("2. Analog input (Delta Modulation)")

    choice = input("Choose input type: ").strip()

    workflows = {
        "1": digital_workflow,
        "2": analog_workflow,
    }

    workflow = workflows.get(choice)

    if workflow is None:
        print("Invalid option.")
        return

    workflow()


if __name__ == "__main__":
    main()
