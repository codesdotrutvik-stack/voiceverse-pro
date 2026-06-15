# print("Hello world!")
# # 

# print("Hello world!")
# print("How are you?")
# #

# print("Hello World! , How are you?")
# #

# print(21)
# #

# print(21+20)
# #

# print(21-25)
# #

# name = "Ashok"
# print("Hello : ",name)
# # 

# name = "Ashok" #string
# age = 21 #integer
# percentage = 87.99 #floting value
# print("My name is : ",name , " \nMy age is : ",age , " \nIn collage My percentage is : ",percentage)
# # 

# # 
# name = "Ashok" #string
# name2 = name
# print("My name is : ",name2 )
# # 

# name = "Ashok" #string
# age = 21 #integer
# print(type(name))
# print(type(age))
# #

# # 
# name1 = "Ashok"
# name2 = 'Ashok'
# name3 = '''Ashok'''
# print(name1)
# print(name2)
# print(name3)

# #

# age = 21
# old = False
# a = None
# print(type(age))
# print(type(old))
# print(type(a))


# # 

# a =  2
# b = 5
# sum = a + b
# sum1 = a - b
# print(sum)
# print(sum1)

# #

# # print("hello world")


# # String variable
# name = "Rahul"

# # Number variable  
# age = 25

# # Boolean variable
# is_student = True

# # Print variables
# print(name)
# print(age)
# print(is_student)

# # Create these variables
# your_name = "NIRBHAY"
# your_age = 25
# your_city = "SURAT"
# is_learning = True

# # Print all variables
# print(your_name)
# print(your_age)
# print(your_city)
# print(is_learning)

# fruits = ["apple", "mango", "banana"]

# print(fruits)

# person = {
#     "name": "Rahul",
#     "age": 25,
#     "city": "Ahmedabad"
# }

# print(person)

# first = "AI"
# last = "Agent"
# full = first + " " + last  # Concatenation: "AI Agent"
# print(full * 3)


# numbers = [1, 2, 3]
# numbers.append(4)      # Add item: [1, 2, 3, 4]
# numbers.remove(2)      # Remove item: [1, 3, 4]
# print(numbers[0])      # Access first item: 1
# print(len(numbers))
# print(numbers)




my_name = "Nirbhay"
my_age = 24
favorite_color = "White"
my_hobbies = ["Reading", "Coding", "Cricket"]
my_location = {
    "city": "Surat",
    "country": "India"
}
print("=" * 40)
print("PERSONAL INFORMATION")
print("=" * 40)
print("Name:", my_name)
print("Age:", my_age)
print("Favorite Color:", favorite_color)
print()
print("Hobbies:")
for hobby in my_hobbies:
    print("  -", hobby)
print()
print("Location:")
print("  City:", my_location["city"])
print("  Country:", my_location["country"])
print("=" * 40)

num1 = 25
num2 = 7
sum_result = num1 + num2
difference = num1 - num2
product = num1 * num2
division = num1 / num2
remainder = num1 % num2
results = [sum_result, difference, product, division, remainder]

print("=" * 40)
print("Calculate")
print("=" * 40)
print("Sum:", sum_result)
print("Difference:", difference)
print("Product:", product)
print("Division:", division)
print("Remainder:", remainder)
print("Results List:", results)
print("Length of list:", len(results))

# IF ELSE #
age = 17

if age >= 18:
 print ("you can vote ")
else :
   print ("you can not vote")

mark = 75

if mark >= 90:
   print ("Grade A")
elif mark >= 75:
   print ("Grade B")
elif mark >= 60:
   print ("Grade c")
else :
   print ("Grade d")

# For loop #

for x in range(1,15):
   print (x, "This is for loop demo")


total = 0
for n in range(1, 100):
    total = total + n
print("total sum is :", total)


# Simple function #
def my_name():
   print ("NB")

my_name()

# Function with parameter #
def square(num):
    print(num * num)

square(5)  # 25
square(4)  # 16

# Function with return #
def square(num):
    return num * num

result = square(8)
print(result) 

# Two parameters #
def multiply(a, b):
    return a * b

print(multiply(4, 5))  # 20



# String methods you MUST know
text = "  Hello Python World  "

# Common methods
print(text.lower())     
print(text.upper())      
print(text.strip())      
print(text.split())     
print("-".join(["a","b","c"]))  
print(text.replace("Python", "Java"))  
print(text.find("Python"))  
print("Python" in text)     
