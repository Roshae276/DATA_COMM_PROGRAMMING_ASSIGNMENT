import random

def generate_random_data(length):
    data = ""
    
    for i in range(length):
        bit = random.randint(0,1)
        data = data+str(bit)
        
    return data

    
def generate_data_with_zeros(length,zero_count):
    if zero_count > length:
        print("Zero count cannot be greater than length.")
        return ""
    
    data = generate_random_data(length)
    
    position = random.randint(0,length-zero_count)
    data = list(data)
    
    for i in range(zero_count):
        data[position+i] = "0"
        
    data = "".join(data)
    
    return data

def expand_from_center(data, left, right):

    while left >= 0 and right < len(data) and data[left] == data[right]:
        left = left - 1
        right = right + 1

    return data[left + 1:right]

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

## worst case O(n2)

## to check if our function is working or not aur ham nahi chahte ki hamara ye code automatically baar baar chale import karne par isliye ham chahte hai ki jab ham directly ye file chalaye
# if __name__ == "__main__":
#     print("Random data:")
#     print(generate_random_data(20))

#     print("\nData with four zeros:")
#     print(generate_data_with_zeros(20, 4))

#     print("\nData with eight zeros:")
#     print(generate_data_with_zeros(20, 8))
    
#     print(expand_from_center("101", 1, 1))
#     print(expand_from_center("1001", 1, 2))

if __name__ == "__main__":

    data = generate_random_data(20)

    print("Digital data:")
    print(data)

    print("Longest palindrome:")
    print(find_longest_palindrome(data))