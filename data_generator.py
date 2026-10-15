
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


def expand_from_center(data, left, right):
    """Expand around a center and return the matching substring."""
    while (
        left >= 0
        and right < len(data)
        and data[left] == data[right]
    ):
        left -= 1
        right += 1

    return data[left + 1:right]


def find_longest_palindrome(data):
    """Find the longest contiguous palindromic substring."""
    if not isinstance(data, str):
        raise ValueError("Data must be a string.")

    longest = ""

    for i in range(len(data)):
        odd = expand_from_center(data, i, i)
        if len(odd) > len(longest):
            longest = odd

        even = expand_from_center(data, i, i + 1)
        if len(even) > len(longest):
            longest = even

    return longest


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
