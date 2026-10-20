
def validate_binary_data(data):
    if not isinstance(data, str) or not data:
        raise ValueError("Data must be a non-empty binary string.")
    if any(bit not in "01" for bit in data):
        raise ValueError("Data must contain only 0 and 1.")


def validate_signal(signal):
    if not signal:
        raise ValueError("Signal must be a non-empty sequence.")
    if any(level not in (-1, 0, 1) for level in signal):
        raise ValueError("Signal levels must be -1, 0, or 1.")


# ─── B8ZS ────────────────────────────────────────────────────────────────────
# Maps last pulse polarity -> 8-symbol substitution [000 V B 0 V B]
# where V (violation) has the same polarity as the previous pulse.
_B8ZS_SUB = {
     1: [0, 0, 0,  1, -1, 0, -1,  1],
    -1: [0, 0, 0, -1,  1, 0,  1, -1],
}


def encode_b8zs(data):
    """AMI with B8ZS substitution for each run of eight zeros."""
    validate_binary_data(data)

    signal = []
    last_pulse = -1
    i = 0

    while i < len(data):
        if data[i:i + 8] == "00000000":
            pattern = _B8ZS_SUB[last_pulse]
            signal.extend(pattern)
            last_pulse = pattern[-1]
            i += 8
        elif data[i] == "0":
            signal.append(0)
            i += 1
        else:
            last_pulse = -last_pulse
            signal.append(last_pulse)
            i += 1

    return signal


# ─── HDB3 ────────────────────────────────────────────────────────────────────
# Maps (pulse_count_is_odd, last_pulse) -> 4-symbol substitution
# odd count  -> 000V (violation only, no balance pulse needed)
# even count -> B00V (balance pulse + violation, same polarity)
_HDB3_SUB = {
    (True,   1): [0,  0, 0,  1],
    (True,  -1): [0,  0, 0, -1],
    (False,  1): [-1, 0, 0, -1],
    (False, -1): [ 1, 0, 0,  1],
}


def encode_hdb3(data):
    """AMI with HDB3 substitution for each run of four zeros."""
    validate_binary_data(data)

    signal = []
    last_pulse = -1
    pulse_count = 0
    i = 0

    while i < len(data):
        if data[i:i + 4] == "0000":
            pattern = _HDB3_SUB[(pulse_count % 2 == 1, last_pulse)]
            signal.extend(pattern)
            last_pulse = pattern[-1]
            pulse_count = 0
            i += 4
        elif data[i] == "0":
            signal.append(0)
            i += 1
        else:
            last_pulse = -last_pulse
            signal.append(last_pulse)
            pulse_count += 1
            i += 1

    return signal


# ─── B8ZS Decoder ────────────────────────────────────────────────────────────

def decode_b8zs(signal):
    validate_signal(signal)

    result = []
    last_pulse = -1
    i = 0

    while i < len(signal):
        if i + 8 <= len(signal):
            expected = _B8ZS_SUB[last_pulse]
            if signal[i:i + 8] == expected:
                result.extend("00000000")
                last_pulse = expected[-1]
                i += 8
                continue

        level = signal[i]
        if level == 0:
            result.append("0")
        else:
            if level == last_pulse:
                raise ValueError("Invalid AMI/B8ZS polarity violation.")
            last_pulse = level
            result.append("1")

        i += 1

    return "".join(result)


# ─── HDB3 Decoder ────────────────────────────────────────────────────────────

def decode_hdb3(signal):
    validate_signal(signal)

    result = []
    last_pulse = -1
    pulse_count = 0
    i = 0

    while i < len(signal):
        if i + 4 <= len(signal):
            chunk = signal[i:i + 4]

            # 000V pattern: first three are zeros, fourth repeats last pulse
            if chunk[:3] == [0, 0, 0] and chunk[3] != 0 and chunk[3] == last_pulse:
                result.extend("0000")
                last_pulse = chunk[3]
                pulse_count = 0
                i += 4
                continue

            # B00V pattern: lookup confirms it matches the even-count substitution
            expected_b00v = _HDB3_SUB[(False, last_pulse)]
            if chunk == expected_b00v and pulse_count % 2 == 0:
                result.extend("0000")
                last_pulse = chunk[3]
                pulse_count = 0
                i += 4
                continue

        level = signal[i]
        if level == 0:
            result.append("0")
        else:
            if level == last_pulse:
                raise ValueError("Invalid AMI/HDB3 polarity violation.")
            last_pulse = level
            result.append("1")
            pulse_count += 1

        i += 1

    return "".join(result)


if __name__ == "__main__":
    test_cases = [
        "100000000",
        "00000000",
        "11000000100000000",
        "10000000",
        "100000000",
        "1000000000000",
        "110000010000010000",
    ]

    for name, encoder, decoder in (
        ("B8ZS", encode_b8zs, decode_b8zs),
        ("HDB3", encode_hdb3, decode_hdb3),
    ):
        print(f"\n{name} tests")

        for data in test_cases:
            signal = encoder(data)
            decoded = decoder(signal)
            status = "PASS" if decoded == data else "FAIL"
            print(f"{data} -> {signal} -> {decoded}: {status}")
