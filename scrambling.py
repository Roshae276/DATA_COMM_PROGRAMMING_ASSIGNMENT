
def encode_b8zs(data):
    signal = []
    last_pulse = -1
    i = 0

    while i < len(data):
        if data[i:i + 8] == "00000000":
            if last_pulse == 1:
                pattern = [0, 0, 0, 1, -1, 0, -1, 1]
            else:
                pattern = [0, 0, 0, -1, 1, 0, 1, -1]

            signal.extend(pattern)
            last_pulse = pattern[-1]
            i += 8

        else:
            if data[i] == "0":
                signal.append(0)
            else:
                last_pulse = -last_pulse
                signal.append(last_pulse)

            i += 1

    return signal


def encode_hdb3(data):
    signal = []
    last_pulse = -1
    pulse_count = 0
    i = 0

    while i < len(data):
        if data[i:i + 4] == "0000":

            if pulse_count % 2 == 1:
                pattern = [0, 0, 0, last_pulse]

            else:
                balancing_pulse = -last_pulse
                pattern = [
                    balancing_pulse, 0, 0, balancing_pulse
                ]

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



if __name__ == "__main__":
    data = "11000010"

    print("Input data:", data)
    print("HDB3 signal:", encode_hdb3(data))
