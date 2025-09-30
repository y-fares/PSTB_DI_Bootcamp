##Complete the exercises below by writing an expression in Python to answer the question:
#Declare a variable called first and assign it to the value "Hello World".
first = "Hello World"
#Write a comment that says "This is a comment."
# This is a comment.
#Log a message to the terminal that says "I AM A COMPUTER!"
print("I AM A COMPUTER!")
#Write an if statement that checks if 1 is less than 2 and if 4 is greater than 2. If it is, show the message "Math is fun."
if (1 < 2) and (4 > 2):
    print("Math is fun.")
else :
    print("Math is not fun.")
#Assign a variable called nope to an absence of value.
nope = None
#Use the language’s “and” boolean operator to combine the language’s “true” value with its “false” value.
true_and_false = True and False
#Calculate the length of the string "What's my length?"
len1 = len("What's my length?")
#Convert the string "i am shouting" to uppercase.
var1 = "i am shouting"
upperVar1 = var1.upper()
#Convert the string "1000"to the number 1000.
str1 = "1000"
num1 = int(str1)
#Combine the number 4 with the string "real" to produce "4real".
niou = "4"+"real"
#Record the output of the expression 3 * "cool".
record_output = 3 * "cool"
#Record the output of the expression 1 / 0.
try:
    bad_div = 1 / 0
except Exception as e:
    print(e)
#Determine the type of [].
type_of_list = type([])
#Ask the user for their name, and store it in a variable called name.
name = input("Comment tu t'appelles ?")
#Ask the user for a number. If the number is negative, show a message that says "That number is less than 0!" If the number is positive, show a message that says "That number is greater than 0!" Otherwise, show a message that says "You picked 0!.
ask_number = float(input("Please enter a number: "))
if ask_number < 0:
    print("That number is less than 0!")
elif ask_number > 0:
    print("That number is greater than 0!")
else:
    print("You picked 0!")
#Find the index of "l" in "apple".
l_index = "apple".index("l")
#Check whether "y" is in "xylophone".
is_y_in_xylophone = "y" in "xylophone"
#Check whether a string called my_string is all in lowercase.
my_string = "example"
is_all_lowercase = my_string.islower()