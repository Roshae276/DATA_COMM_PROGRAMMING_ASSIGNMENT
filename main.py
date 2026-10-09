from data_generator import (
    generate_random_data,
    find_longest_palindrome
)

from line_coding import (
    encode_nrz_l,
    encode_nrz_i,
    encode_manchester,
    encode_differential_manchester,
    encode_ami
)

from scrambling import encode_b8zs, encode_hdb3
from signal_plotter import plot_signal


encoders = {
    "NRZ-L": encode_nrz_l,
    "NRZ-I": encode_nrz_i,
    "MANCHESTER": encode_manchester,
    "DIFFERENTIAL MANCHESTER": encode_differential_manchester,
    "AMI": encode_ami,
    "B8ZS": encode_b8zs,
    "HDB3": encode_hdb3
}

data_sources = {
    "1": lambda: generate_random_data(16),
    "2": lambda: input("Enter binary data: ").strip()
}


def main():
    print("Digital Signal Encoder and Decoder")
    print("1. Generate random data")
    print("2. Enter binary data")

    choice = input("Choose an option: ").strip()

    get_data = data_sources.get(choice)

    if get_data is None:
        print("Invalid option.")
        return

    data = get_data()

    if not data or any(bit not in "01" for bit in data):
        print("Invalid input. Enter a non-empty binary string.")
        return

    print("\nDigital data:", data)
    print("Longest palindrome:", find_longest_palindrome(data))

    print("\nAvailable encoders:")
    for name in encoders:
        print("-", name)

    encoding_name = input("Choose an encoder: ").strip().upper()
    encoder = encoders.get(encoding_name)

    if encoder is None:
        print("Invalid encoder name.")
        return

    signal = encoder(data)

    print("\nSelected encoding:", encoding_name)
    print("Encoded signal:", signal)

    plot_signal(signal, encoding_name + " Signal")


if __name__ == "__main__":
    main()