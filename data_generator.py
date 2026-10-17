
import random


def generate_random_data(length):
    """Generate a random binary string of the requested positive length."""
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")

    return "".join(str(random.randint(0, 1)) for _ in range(length))


def generate_data_with_zeros(length, zero_count):
    """Generate binary data containing a run of consecutive zeros."""
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")

    if not isinstance(zero_count, int) or zero_count <= 0:
        raise ValueError("Zero count must be a positive integer.")

    if zero_count > length:
        raise ValueError("Zero count cannot be greater than length.")

    data = list(generate_random_data(length))
    position = random.randint(0, length - zero_count)

    for i in range(position, position + zero_count):
        data[i] = "0"

    return "".join(data)


def find_longest_palindrome(data):
    """
    Find the longest contiguous palindromic substring in O(N) time
    using Manacher's Algorithm.
    """
    if not isinstance(data, str):
        raise ValueError("Data must be a string.")

    if not data:
        return ""

    # Transform string with delimiters and sentinels (^ and $) to avoid bounds checking
    transformed = "^#" + "#".join(data) + "#$"
    n = len(transformed)
    p = [0] * n
    center = 0
    right = 0

    max_len = 0
    center_idx = 0

    for i in range(1, n - 1):
        i_mirror = 2 * center - i

        if right > i:
            p[i] = min(right - i, p[i_mirror])
        else:
            p[i] = 0

        while transformed[i + 1 + p[i]] == transformed[i - 1 - p[i]]:
            p[i] += 1

        if i + p[i] > right:
            center = i
            right = i + p[i]

        if p[i] > max_len:
            max_len = p[i]
            center_idx = i

    start = (center_idx - max_len) // 2
    return data[start:start + max_len]


if __name__ == "__main__":
    data = generate_random_data(20)

    print("Digital data:")
    print(data)

    print("Longest palindrome:")
    print(find_longest_palindrome(data))

    print("\nData containing four consecutive zeros:")
    print(generate_data_with_zeros(20, 4))

    print("\nData containing eight consecutive zeros:")
    print(generate_data_with_zeros(20, 8))
