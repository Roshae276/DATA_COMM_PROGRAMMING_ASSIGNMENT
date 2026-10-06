# Digital Data Generator --- Code Walkthrough

This document explains `data_generator.py` in simple terms so a teammate
can understand what each function does, how the logic works, and how to
test it.

## 1. Purpose of this file

The `data_generator.py` file handles the first part of the Digital
Signal Encoder and Decoder assignment:

-   Generate a random binary sequence.
-   Generate a binary sequence containing a chosen number of consecutive
    zeros, such as `0000` or `00000000`.
-   Find the longest palindromic substring in a binary sequence.

A binary sequence contains only `0` and `1`.

Example:

``` text
101101001
```

## 2. Required setup

The random generator uses Python's built-in `random` module. You do not
need to install it separately.

Make sure you are in the project folder and your virtual environment is
active, then run:

``` bash
python data_generator.py
```

## 3. Importing the random module

``` python
import random
```

-   `import` makes a module available to this file.
-   `random` is a built-in Python module with functions for generating
    random values.
-   We use `random.randint(0, 1)` to generate either `0` or `1`.

## 4. Function: `generate_random_data(length)`

### Code

``` python
def generate_random_data(length):
    data = ""

    for i in range(length):
        bit = random.randint(0, 1)
        data = data + str(bit)

    return data
```

### Line-by-line explanation

**`def generate_random_data(length):`**

Defines a function named `generate_random_data`. The parameter `length`
tells the function how many bits to generate.

**`data = ""`**

Creates an empty string. We will add each generated bit to this string.

**`for i in range(length):`**

Repeats the indented code `length` times. For example, `range(5)`
produces the values `0, 1, 2, 3, 4`, so the loop runs five times.

**`bit = random.randint(0, 1)`**

Generates either integer `0` or integer `1`.

**`data = data + str(bit)`**

`data` is a string, so `str(bit)` converts the integer into text. The
new bit is added to the end of the string.

**`return data`**

Sends the completed binary string back to the code that called the
function.

### Example

Calling:

``` python
generate_random_data(5)
```

could return:

``` text
10110
```

The exact output changes between runs. Random output does not have to
contain equal numbers of zeros and ones.

### Complexity

For a sequence of length `n`, this version runs a loop `n` times.
Because repeatedly adding to a string can copy existing characters, its
practical running time may be quadratic in the length of the sequence.
For the modest sequence sizes used in this assignment, this simple
version is easy to follow. If very large sequences are needed, building
a list of bits and joining it once would be more efficient.

## 5. Function: `generate_data_with_zeros(length, zero_count)`

### Code

``` python
def generate_data_with_zeros(length, zero_count):

    if zero_count > length:
        print("Zero count cannot be greater than length.")
        return ""

    data = generate_random_data(length)

    position = random.randint(0, length - zero_count)

    data = list(data)

    for i in range(zero_count):
        data[position + i] = "0"

    data = "".join(data)

    return data
```

### What does it do?

It creates a random sequence and replaces the bits at one randomly
chosen location with consecutive zeros.

-   `length`: total number of bits.
-   `zero_count`: number of consecutive zeros to insert.
-   `position`: starting index where the zeros will be placed.

### Line-by-line explanation

**Input validation**

``` python
if zero_count > length:
    print("Zero count cannot be greater than length.")
    return ""
```

It is impossible to place more zeros than the total sequence length. If
`zero_count` is greater than `length`, the function prints a message and
returns an empty string.

**Generate the initial sequence**

``` python
data = generate_random_data(length)
```

Reuses the earlier function instead of duplicating the random-generation
logic.

**Choose the starting position**

``` python
position = random.randint(0, length - zero_count)
```

Python string/list indexes begin at `0`. The last valid starting
position is `length - zero_count`, because all the zeros must fit inside
the sequence.

For example, with `length = 10` and `zero_count = 4`, the starting
position can be any integer from `0` through `6`.

**Convert the string to a list**

``` python
data = list(data)
```

Python strings cannot be changed one character at a time because strings
are immutable. Converting the string to a list lets us replace
individual characters.

For example:

``` text
"1010"  ->  ['1', '0', '1', '0']
```

**Replace the chosen positions**

``` python
for i in range(zero_count):
    data[position + i] = "0"
```

The loop changes `zero_count` consecutive positions to the string
character `"0"`.

If `position = 3` and `zero_count = 4`, indexes `3`, `4`, `5`, and `6`
are set to zero.

**Convert back to a string**

``` python
data = "".join(data)
```

Joins all list characters together without adding anything between them.

**Return the sequence**

``` python
return data
```

Returns the sequence containing the requested run of zeros.

### Important behavior

This function guarantees **at least** `zero_count` consecutive zeros at
the chosen position. It does not guarantee that the sequence contains
*exactly* that many consecutive zeros, because neighboring random bits
may already be zeros.

For example, a request for four zeros could produce six consecutive
zeros.

### Example calls

``` python
generate_data_with_zeros(20, 4)
generate_data_with_zeros(20, 8)
```

The results will vary because the initial sequence and starting position
are random.

### Validation note

The current check handles `zero_count > length`. It does not yet
validate negative values or a zero-length request. If those inputs may
be supplied by users, add validation for them before calling
`random.randint`.

## 6. Function: `expand_from_center(data, left, right)`

### Code

``` python
def expand_from_center(data, left, right):

    while left >= 0 and right < len(data) and data[left] == data[right]:
        left = left - 1
        right = right + 1

    return data[left + 1:right]
```

### What is a palindrome?

A palindrome reads the same forwards and backwards.

Examples:

``` text
101
1001
11111
```

A palindrome must be a **continuous substring** of the input string. We
are not rearranging bits or skipping positions.

### Main idea: expand around a center

Every palindrome has either:

-   One center character, for an odd-length palindrome such as `101`.
-   A center between two characters, for an even-length palindrome such
    as `1001`.

The function starts from the supplied center and expands outward while
the characters on both sides match.

### Line-by-line explanation

**Function definition**

``` python
def expand_from_center(data, left, right):
```

-   `data` is the input binary string.
-   `left` is the initial left index.
-   `right` is the initial right index.

For an odd-length palindrome, both indexes start at the same position.
For an even-length palindrome, `right` starts at `left + 1`.

**Expansion condition**

``` python
while left >= 0 and right < len(data) and data[left] == data[right]:
```

All three conditions must be true:

1.  `left >= 0`: the left index has not gone before the start.
2.  `right < len(data)`: the right index has not reached beyond the end.
3.  `data[left] == data[right]`: the characters match.

Python evaluates these conditions from left to right and stops when a
condition is false, so the character indexes are checked only while they
are in range.

**Move outward**

``` python
left = left - 1
right = right + 1
```

After a matching pair is found, move one position farther left and one
position farther right to check the next pair.

**Return the substring**

``` python
return data[left + 1:right]
```

When the loop stops, the indexes have moved one step beyond the matching
palindrome. The slice starts at `left + 1` and stops just before
`right`. Python slices include the start index but exclude the end
index.

### Example

``` python
expand_from_center("101", 1, 1)
```

returns:

``` text
101
```

And:

``` python
expand_from_center("1001", 1, 2)
```

returns:

``` text
1001
```

## 7. Function: `find_longest_palindrome(data)`

### Code

``` python
def find_longest_palindrome(data):

    longest = ""

    for i in range(len(data)):

        odd = expand_from_center(data, i, i)

        if len(odd) > len(longest):
            longest = odd

        even = expand_from_center(data, i, i + 1)

        if len(even) > len(longest):
            longest = even

    return longest
```

### What does it do?

It checks every possible center and returns the longest palindrome it
finds.

### Line-by-line explanation

**Start with an empty answer**

``` python
longest = ""
```

No palindrome has been found yet.

**Visit every index**

``` python
for i in range(len(data)):
```

If `data` has length `6`, the loop visits indexes `0` through `5`.

**Check an odd-length palindrome**

``` python
odd = expand_from_center(data, i, i)
```

Uses index `i` as a single-character center. This finds odd-length
palindromes.

**Update the best answer**

``` python
if len(odd) > len(longest):
    longest = odd
```

If the new palindrome is longer than the current answer, save it.

**Check an even-length palindrome**

``` python
even = expand_from_center(data, i, i + 1)
```

Uses the gap between positions `i` and `i + 1` as the center. This finds
even-length palindromes.

**Compare again**

``` python
if len(even) > len(longest):
    longest = even
```

Save the even-length palindrome if it is longer than the best one found
so far.

**Return the result**

``` python
return longest
```

After every center has been checked, return the longest palindrome
found.

If multiple palindromes share the maximum length, this implementation
returns the first one encountered during the scan.

### Example

``` python
find_longest_palindrome("101")
```

returns `"101"`.

``` python
find_longest_palindrome("1001")
```

returns `"1001"`.

``` python
find_longest_palindrome("111111")
```

returns `"111111"`, because a string made of identical characters is a
palindrome.

## 8. Testing the functions

You can put a small test section at the bottom of `data_generator.py`:

``` python
if __name__ == "__main__":
    print("Random data:")
    print(generate_random_data(20))

    print("\nData with four zeros:")
    print(generate_data_with_zeros(20, 4))

    print("\nData with eight zeros:")
    print(generate_data_with_zeros(20, 8))

    print("\nPalindrome tests:")
    print(find_longest_palindrome("101"))       # Expected: 101
    print(find_longest_palindrome("1001"))      # Expected: 1001
    print(find_longest_palindrome("101101"))    # Expected: 101101
    print(find_longest_palindrome("111111"))    # Expected: 111111
```

The condition:

``` python
if __name__ == "__main__":
```

means the test section runs when this file is executed directly. If
another file imports functions from `data_generator.py`, this test
section will not run automatically.

Run the file with:

``` bash
python data_generator.py
```

The random sequences will differ between runs, but the palindrome tests
should consistently return the expected results.

## 9. Time and space complexity

Let `n` be the length of the input sequence.

### Random generation

-   The loop generates `n` bits.
-   With repeated string concatenation, the implementation may take
    `O(n²)` time in the worst case because strings are immutable.
-   The resulting sequence occupies `O(n)` space.

### Generate a sequence with zeros

-   Generating the random data takes the time described above.
-   Converting to a list and replacing the selected characters takes
    `O(n)` time and space.
-   Overall, the current simple implementation may take `O(n²)` time due
    to the random generator's repeated concatenation.

### Longest palindrome

`find_longest_palindrome` checks `n` centers, and each expansion can
examine up to `n` characters.

-   **Time complexity:** `O(n²)`.
-   **Auxiliary space:** `O(1)` for the expansion indexes and variables,
    excluding returned substrings and the result storage. Python slicing
    creates a new string, so temporary/returned substring storage can
    use up to `O(n)` space.

This center-expansion approach is simpler to explain than checking every
possible substring and testing each one separately.

## 10. Quick reference

  ------------------------------------------------------------------------------------
  Function                                         Purpose
  ------------------------------------------------ -----------------------------------
  `generate_random_data(length)`                   Returns a random string of `0` and
                                                   `1` characters

  `generate_data_with_zeros(length, zero_count)`   Returns random data with at least
                                                   the requested number of consecutive
                                                   zeros

  `expand_from_center(data, left, right)`          Expands around a center and returns
                                                   the palindrome found there

  `find_longest_palindrome(data)`                  Checks odd and even centers and
                                                   returns the longest palindrome
  ------------------------------------------------------------------------------------

## 11. Before committing to GitHub

After checking that the code and tests work, run:

``` bash
git status
git add data_generator.py README.md
git commit -m "Document digital data generator and palindrome logic"
git push
```

If your repository already has a `README.md` for the whole project,
consider saving this walkthrough as `DATA_GENERATOR_README.md` instead,
so you do not overwrite the main project README.

## 12. Acknowledgment

This walkthrough is documentation for the implementation described
above. Make sure the final assignment report acknowledges any AI
assistance, as required by the assignment instructions, and ensure that
every team member understands the code they submit.
