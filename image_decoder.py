import numpy as np
from PIL import Image

from decoder import (
    decode_nrz_l,
    decode_nrz_i,
    decode_manchester,
    decode_differential_manchester,
    decode_ami,
)
from scrambling import decode_b8zs, decode_hdb3

IMAGE_SCHEME_DECODERS = {
    "NRZ-L": decode_nrz_l,
    "NRZ-I": decode_nrz_i,
    "MANCHESTER": decode_manchester,
    "DIFFERENTIAL MANCHESTER": decode_differential_manchester,
    "AMI": decode_ami,
    "B8ZS": decode_b8zs,
    "HDB3": decode_hdb3,
}


def extract_levels_from_image(image_path, num_intervals):
    """
    Analyze the waveform image and extract discrete voltage levels (-1, 0, 1).
    Reads the image pixels, identifies the signal line, and samples each interval.
    """
    if num_intervals <= 0:
        raise ValueError("Number of intervals must be positive.")

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as error:
        raise ValueError(f"Unable to read waveform image '{image_path}': {error}")

    arr = np.array(img)

    # Detect the blue waveform pixels (step line plotted in signal_plotter)
    is_signal = (arr[:, :, 2] > 140) & (arr[:, :, 0] < 120) & (arr[:, :, 1] < 120)
    y_coords, x_coords = np.where(is_signal)

    if len(x_coords) == 0:
        raise ValueError("No signal waveform detected in the image.")

    x_min, x_max = int(x_coords.min()), int(x_coords.max())
    y_min, y_max = int(y_coords.min()), int(y_coords.max())

    y_mid = (y_min + y_max) / 2.0
    threshold = (y_max - y_min) / 4.0
    dx = (x_max - x_min) / num_intervals

    extracted_levels = []

    for k in range(num_intervals):
        x_center = x_min + (k + 0.5) * dx
        half_window = max(2, int(dx * 0.15))
        x_start = max(x_min, int(x_center - half_window))
        x_end = min(x_max, int(x_center + half_window) + 1)

        window_mask = is_signal[:, x_start:x_end]
        y_window, _ = np.where(window_mask)

        if len(y_window) > 0:
            avg_y = float(np.mean(y_window))
            # Image y=0 is at top: smaller y is higher voltage (+1)
            if avg_y < y_mid - threshold:
                extracted_levels.append(1)
            elif avg_y > y_mid + threshold:
                extracted_levels.append(-1)
            else:
                extracted_levels.append(0)
        else:
            extracted_levels.append(0)

    return extracted_levels


def decode_signal_from_image(image_path, encoding_name, num_intervals):
    """
    Decode digital data by analyzing waveform parameters from an image.
    Fulfills the extra-credit requirement of image-based decoding.
    """
    decoder = IMAGE_SCHEME_DECODERS.get(encoding_name.upper())
    if decoder is None:
        raise ValueError(f"Unsupported encoding scheme for image decoder: {encoding_name}")

    levels = extract_levels_from_image(image_path, num_intervals)
    return decoder(levels)


if __name__ == "__main__":
    import os

    print("=" * 50)
    print("IMAGE WAVEFORM DECODER VERIFICATION")
    print("=" * 50)

    test_cases = [
        ("test_images/nrz_l_sample.png", "NRZ-L", 6, "101101"),
        ("test_images/manchester_sample.png", "Manchester", 12, "010011"),
        ("test_images/ami_b8zs_sample.png", "B8ZS", 10, "1000000001"),
    ]

    for path, scheme, intervals, expected in test_cases:
        if os.path.exists(path):
            decoded = decode_signal_from_image(path, scheme, intervals)
            status = "PASS" if decoded == expected else "FAIL"
            print(f"[{status}] {scheme:12} -> Decoded: {decoded:12} Expected: {expected}")
        else:
            print(f"[SKIP] Test image not found: {path}")
