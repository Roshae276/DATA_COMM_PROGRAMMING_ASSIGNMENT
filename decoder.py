
from line_coding import (
    encode_nrz_l,
    encode_nrz_i,
    encode_manchester,
    encode_differential_manchester,
    encode_ami,
)


def validate_signal(signal):
    """Check that the signal contains valid line levels."""
    if not signal:
        raise ValueError("Encoded signal must not be empty.")
    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("Signal levels must be -1, 0, or 1.")


def decode_nrz_l(signal):
    """NRZ-L: +1 represents 0, and -1 represents 1."""
    validate_signal(signal)

    if any(level == 0 for level in signal):
        raise ValueError("NRZ-L signal cannot contain zero levels.")

    # direct lookup instead of conditional
    _nrz_l_inv = {1: "0", -1: "1"}
    return "".join(_nrz_l_inv[level] for level in signal)


def decode_nrz_i(signal, initial_level=-1):
    """NRZ-I: a level transition represents 1."""
    validate_signal(signal)

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or 1.")

    if any(level == 0 for level in signal):
        raise ValueError("NRZ-I signal cannot contain zero levels.")

    bits = []
    previous_level = initial_level

    for level in signal:
        bits.append("1" if level != previous_level else "0")
        previous_level = level

    return "".join(bits)


# Manchester decoding: map (first_half, second_half) -> bit
_MANCHESTER_DECODE = {
    (1, -1): "0",
    (-1, 1): "1",
}


def decode_manchester(signal):
    """Decode Manchester pairs using the project's encoding convention."""
    validate_signal(signal)

    if len(signal) % 2 != 0:
        raise ValueError("Manchester signal must have an even number of levels.")

    bits = []
    for i in range(0, len(signal), 2):
        pair = (signal[i], signal[i + 1])
        bit = _MANCHESTER_DECODE.get(pair)
        if bit is None:
            raise ValueError("Invalid Manchester signal pair.")
        bits.append(bit)

    return "".join(bits)


def decode_differential_manchester(signal, initial_level=1):
    """
    Decode Differential Manchester.
    A beginning transition represents 0; no beginning transition represents 1.
    """
    validate_signal(signal)

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or 1.")

    if len(signal) % 2 != 0:
        raise ValueError(
            "Differential Manchester signal must have an even number of levels."
        )

    bits = []
    previous_level = initial_level

    for i in range(0, len(signal), 2):
        first_half = signal[i]
        second_half = signal[i + 1]

        if first_half == second_half:
            raise ValueError(
                "Invalid Differential Manchester mid-bit transition."
            )

        # transition at bit-start -> 0, no transition -> 1
        bits.append("0" if first_half != previous_level else "1")
        previous_level = second_half

    return "".join(bits)


def decode_ami(signal):
    """Decode AMI while checking alternating pulse polarity."""
    validate_signal(signal)

    bits = []
    last_pulse = None

    for level in signal:
        if level == 0:
            bits.append("0")
        else:
            if last_pulse is not None and level == last_pulse:
                raise ValueError(
                    "Invalid AMI signal: consecutive pulses must alternate polarity."
                )
            bits.append("1")
            last_pulse = level

    return "".join(bits)


DECODERS = {
    "NRZ-L": decode_nrz_l,
    "NRZ-I": decode_nrz_i,
    "MANCHESTER": decode_manchester,
    "DIFFERENTIAL MANCHESTER": decode_differential_manchester,
    "AMI": decode_ami,
}


if __name__ == "__main__":
    test_data = "1011010010"

    tests = {
        "NRZ-L": (encode_nrz_l, decode_nrz_l),
        "NRZ-I": (encode_nrz_i, decode_nrz_i),
        "Manchester": (encode_manchester, decode_manchester),
        "Differential Manchester": (
            encode_differential_manchester,
            decode_differential_manchester,
        ),
        "AMI": (encode_ami, decode_ami),
    }

    print("Line Coding Encoder/Decoder Tests")
    print("Original data:", test_data)

    for name, (encoder, decoder) in tests.items():
        signal = encoder(test_data)
        decoded = decoder(signal)
        status = "PASS" if decoded == test_data else "FAIL"

        print(f"\n{name}")
        print("Encoded signal:", signal)
        print("Decoded data:", decoded)
        print("Status:", status)

    print("\nInvalid AMI test:")

    try:
        decode_ami([1, 1, 0, -1])
        print("FAIL: invalid AMI signal was accepted.")
    except ValueError as error:
        print("PASS:", error)
