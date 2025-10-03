# Challenge 1
# Ask the user for a number and a length.
# Create a program that prints a list of multiples of the number 
# until the list length reaches length.

nb = int(input("Enter a number: "))
length = int(input("Enter a length: "))

multiples = []
for i in range(1, length + 1):
    multiples.append(nb * i)
print(multiples)

# Challenge 2
# Write a program that asks a string to the user, 
# and display a new string with any duplicate consecutive letters removed.

str_user = input("Enter a string: ")
new_str = ""
for i in str_user:
    if i not in new_str:
        new_str += i
    else:
        continue
print(new_str)