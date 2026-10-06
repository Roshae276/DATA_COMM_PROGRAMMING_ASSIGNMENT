
def encode_nrz_l(data):
    signal = []

    for bit in data:
        if bit == "0":
            signal.append(1)
        else:
            signal.append(-1)

    return signal
    
    

def encode_nrz_i(data):
    signal = []
    current_level = -1

    for bit in data:
        if bit == "1":
            current_level = -current_level

        signal.append(current_level)

    return signal


def encode_manchester(data):
    signal = []

    for bit in data:
        if bit == "0":
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])

    return signal


def encode_differential_manchester(data):
    signal = []
    current_level = 1

    for bit in data:
        if bit == "0":
            current_level = -current_level

        signal.append(current_level)

        current_level = -current_level
        signal.append(current_level)

    return signal


def encode_ami(data):
    signal = []
    last_pulse = -1

    for bit in data:
        if bit == "0":
            signal.append(0)
        else:
            last_pulse = -last_pulse
            signal.append(last_pulse)

    return signal





if __name__ == "__main__":
    data = "0101"

    encoded_signal = encode_nrz_l(data)

    print("Input data:", data)
    # print("NRZ-L signal:", encoded_signal)
    

    print("NRZ-L:", encode_nrz_l(data))
    print("NRZ-I:", encode_nrz_i(data))
    
    print("Manchester:", encode_manchester(data))
    print("Differential Manchester:",
      encode_differential_manchester(data))
    print("AMI:", encode_ami("101101"))