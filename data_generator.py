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

## to check if our function is working or not aur ham nahi chahte ki hamara ye code automatically baar baar chale import karne par isliye ham chahte hai ki jab ham directly ye file chalaye
if __name__ == "__main__":
    print("Random data:")
    print(generate_random_data(20))

    print("\nData with four zeros:")
    print(generate_data_with_zeros(20, 4))

    print("\nData with eight zeros:")
    print(generate_data_with_zeros(20, 8))