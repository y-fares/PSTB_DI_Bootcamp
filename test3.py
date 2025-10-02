ask_number = int(input("Please enter a number: "))
if ask_number < 0:
    print("That number is less than 0!")
elif ask_number > 0:
    print("That number is greater than 0!")
else:
    print("You picked 0!")