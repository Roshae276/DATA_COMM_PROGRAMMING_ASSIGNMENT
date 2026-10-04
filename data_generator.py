import random

def generate_random_data(length):
    data = ""
    
    for i in range(length):
        bit = random.randint(0,1)
        data = data+str(bit)
        
    return data

## to check if our function is working or not aur ham nahi chahte ki hamara ye code automatically baar baar chale import karne par isliye ham chahte hai ki jab ham directly ye file chalaye
if __name__ == "__main__":
    print(generate_random_data(10))