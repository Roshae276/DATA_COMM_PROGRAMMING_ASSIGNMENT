
def validate_binary_data(data):
    """Validate that input is a non-empty binary string."""
    if not isinstance(data, str) or not data:
        raise ValueError("Data must be a non-empty binary string.")
    if any(bit not in "01" for bit in data):
        raise ValueError("Data must contain only 0 and 1.")


# NRZ-L: 0 -> +1V, 1 -> -1V
_NRZ_L_MAP = {"0": 1, "1": -1}


def encode_nrz_l(data):
    """NRZ-L: 0 -> +1, 1 -> -1."""
    validate_binary_data(data)
    return [_NRZ_L_MAP[bit] for bit in data]


def encode_nrz_i(data, initial_level=-1):
    """NRZ-I: transition on 1; start at the specified level."""
    validate_binary_data(data)

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or 1.")

    signal = []
    current_level = initial_level

    for bit in data:
        # multiply by -1 on '1', keep unchanged on '0'
        current_level *= (-1) ** int(bit)
        signal.append(current_level)

    return signal


# Manchester (IEEE 802.3): 0 -> [+1, -1], 1 -> [-1, +1]
_MANCHESTER_MAP = {"0": [1, -1], "1": [-1, 1]}


def encode_manchester(data):
    """Manchester: 0 -> [+1, -1], 1 -> [-1, +1]."""
    validate_binary_data(data)
    signal = []
    for bit in data:
        signal.extend(_MANCHESTER_MAP[bit])
    return signal


def encode_differential_manchester(data, initial_level=1):
    """
    Differential Manchester:
    Start at the specified level, transition at the beginning for 0,
    and always transition in the middle of each bit.
    """
    validate_binary_data(data)

    if initial_level not in (-1, 1):
        raise ValueError("Initial level must be -1 or 1.")

    signal = []
    current_level = initial_level

    for bit in data:
        # flip at bit-start for 0; no flip for 1
        current_level *= (-1) ** (1 - int(bit))
        signal.append(current_level)
        # always flip at mid-bit
        current_level = -current_level
        signal.append(current_level)

    return signal


def encode_ami(data, initial_pulse=-1):
    """AMI: 0 -> 0; successive 1 bits alternate pulse polarity."""
    validate_binary_data(data)

    if initial_pulse not in (-1, 1):
        raise ValueError("Initial pulse must be -1 or 1.")

    signal = []
    last_pulse = initial_pulse

    for bit in data:
        if bit == "0":
            signal.append(0)
        else:
            last_pulse = -last_pulse
            signal.append(last_pulse)

    return signal


if __name__ == "__main__":
    data = "0101"

    print("Input data:", data)
    print("NRZ-L:", encode_nrz_l(data))
    print("NRZ-I:", encode_nrz_i(data))
    print("Manchester:", encode_manchester(data))
    print("Differential Manchester:",
          encode_differential_manchester(data))
    print("AMI:", encode_ami(data))

    try:
        encode_nrz_l("012")
    except ValueError as error:
        print("Invalid-input test passed:", error)
