# Steps to make this project

## Step 1 Initialize Git repo
- First of all initialize a empty git repository using this command : git init
- Second check the git status using command : git status
  
## Step 2 Create python env and install dependencies
- create python virtual environment using command : python -m venv venv
- activate the environment using command : venv\Scripts\Activate
- install libraries
- pip install numpy matplotlib
- push everything on github by the following commands : 
- git status
- git add .
- git commit -m "Initialized the project setup"
- git remote add origin https://github.com/Roshae276/DATA_COMM_PROGRAMMING_ASSIGNMENT.git
- git push -u origin main
  
## Step 3 Now the project requires a digital data generator
- matlab ki ye chahiye ki random digital sequence generate ho
- ye generate kare aisi sequence jisme four ya eight consequtive 0's ya 1's ho
- generated data me find kare longest palindromic subsequence
- ham data generator ke liye alag file banayenge data_generator.py
  
## Step 4 Inside data_generator.py
- ab random data generate karna hai to uske liye 
- python ki random library import karenge
- sabse simple kaam ek function banaya 
- python me function def ka use karke banate hai
- length input liya ki kitni length ki hame digit sequence chahiye
- uske baad ab ham data ko ek string ki tarah treat karenge taaki ham individual bits ko dekh paye
- consequtive four zeros aur eight zeros dekh paye
- palindrome dhund paye
- sequence ko display kar sakte hai
- uske baad length tak ki range me loop lagakar bit generate kar lenge kyuki hame 0 aur 1 ki hi digital seq chahiye
- uske baad generated bit seq ko string me convert karke data me add kar lenge
- fir data jo ki hamari sequence generate hogyi usko return kr denge
  ```
  def generate_sequence_data(length):
    data = ""
    for i in range(length):
        bit = random.randint(0,1)
        data = data+str(bit)
    return data

  ```
  - ab ham chahte hai ki consecutive 4 zeros aur 8 zeros ki sequence banana kyuki vo hame scrambling mai chahiye
  - aik aur function banayenge
  - jisme ham zero_count ki hame kitne zero chahiye aur length daalenge
  - ab hamara function kya krega ki jo pehle hamne function banaya tha na usko reuse karke jitni length ham input denge us length ka random seq generate karega uske baad 
  - ye ek position select karega random library ka use karke aur us position se aage zero_count tak 0 daalta jaega
  - ab hamari python string immutable hoti hai to usko ham pehle list me convert krenge aur fir usme 0 daalenge fir se usko string me convert kar denge
  
  ```
  def generate_random_data_with_zeros(length, zero_count):
    data = generate_random_data(length)

    position = random.randint(0,length-zero_count)
    data = list(data)
    
    for i in range(zero_count):
        data[position+i] = "0"
        
    data = "".join(data)
    
    return data
  ```
  
