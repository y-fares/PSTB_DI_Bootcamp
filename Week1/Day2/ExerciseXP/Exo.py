import random

# Exercise 1: Converting Lists into Dictionaries
## Instructions
## You are given two lists. Convert them into a dictionary where the first list contains the keys and the second list contains the corresponding values.

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

niou_dict = dict(zip(keys, values))
print(niou_dict)

# Exercise 2: Cinemax
## Instructions
## Write a program that calculates the total cost of movie tickets for a family based on their ages.
## Family members’ ages are stored in a dictionary.
## The ticket pricing rules are as follows:
## Under 3 years old: Free
## 3 to 12 years old: $10
## Over 12 years old: $15

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}

def calculate_ticket_price(f):
    total_cost = 0
    for m, a in f.items():
        if a < 3:
            price = 0  # Under 3 years old: Free
        elif 3 <= a <= 12:
            price = 10 # 3 to 12 years old: $10
        else:
            price = 15 # Over 12 years old: $15
        
        print(f"{m.capitalize()} has to pay: ${price}")
        total_cost += price
    return total_cost

# Bonus: Allow the user to input family members’ names and ages, then calculate the total ticket cost.
total_cost = calculate_ticket_price(family)
print(f"The total cost for the family is: ${total_cost}")

niou_family = {}
while True:
    name = input("Enter family member's name (or type 'quit' to finish): ")
    if name.lower() == 'quit':
        break
    age = int(input(f"Enter {name}'s age: "))
    niou_family[name] = age

print("Calculating ticket prices for the new family:")
niou_total_cost = calculate_ticket_price(niou_family)
print(f"The new total cost for the family is: ${niou_total_cost}")

# Exercise 3: Zara
## Instructions
## Create and manipulate a dictionary that contains information about the Zara brand.
## name: Zara
## creation_date: 1975
## creator_name: Amancio Ortega Gaona
## type_of_clothes: men, women, children, home
## international_competitors: Gap, H&M, Benetton
## number_stores: 7000
## major_color: 
##     France: blue, 
##     Spain: red, 
##     US: pink, green

brand ={}
brand["name"] = "Zara"
brand["creation_date"] = 1975
brand["creator_name"] = "Amancio Ortega Gaona"
brand["type_of_clothes"] = ["men", "women", "children", "home"]
brand["international_competitors"] = ["Gap", "H&M", "Benetton"]
brand["number_stores"] = 7000
brand["major_color"] = {"France": "blue", "Spain": "red", "US": ["pink", "green"]}
print(brand)

# Change the value of number_stores to 2.
brand["number_stores"] = 2
# Print a sentence describing Zara’s clients using the type_of_clothes key.
print(f"Les types de vêtements des clients de Zara sont  : {brand['type_of_clothes']}")
# Add a new key country_creation with the value Spain.
brand["country_creation"] = "Spain"
# Check if international_competitors exists and, if so, add “Desigual” to the list.
if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")
# Delete the creation_date key.
del brand["creation_date"]
# Print the last item in international_competitors.
print(f"Le dernier élément ajouté à international_competitors est {brand["international_competitors"][-1]}")
# Print the major colors in the US.
print(brand["major_color"]["US"])
# Print the number of keys in the dictionary.
print(len(brand.keys()))
# Print all keys of the dictionary.
print(list(brand.keys()))

more_on_zara = {
    "creation_date": 1975, 
    "number_stores": 10000
}

brand.update(more_on_zara)

print(brand)

# Exercise 4: Some Geography
## Instructions
## Goal: Create a function that describes a city and its country.
def describe_city(city, country = "Unknown"):
    print(f"{city} is in {country}.")
describe_city("Reykjavik", "Iceland")
describe_city("Paris")

# Exercise 5 : Random
## Instructions
## Goal: Create a function that generates random numbers and compares them.

def my_func (nb:int):
    if (1 <= nb <= 100):
        number = random.randint(1, 100)
        if nb == number:
            print("Success!")
        else:
            print(f"Fail! Your number: {nb}, Random number: {number}")
my_func(50)

# Exercise 6 : Let’s create some personalized shirts !
## Instructions
## Goal: Create a function to describe a shirt’s size and message, with default values.

def make_shirt(size = "large", text = "I love Python"):
    print(f"The size of the shirt is {size} and the text is '{text}'.")

make_shirt("L", "Hello World")
make_shirt() # Call make_shirt() to make a large shirt with the default message.
make_shirt(size = "medium") # Call make_shirt() to make a medium shirt with the default message.
make_shirt(size = "L", text = "Hello World") # Call make_shirt() to make a shirt of any size with a different message.
make_shirt(size = "small", text = "Hello!")

# Exercise 7 : Temperature Advice
## Goal: Generate a random temperature and provide advice based on the temperature range.


def get_random_temp(month:int) -> float:
    if month in [12, 1, 2]:         # Winter
        return random.uniform(-10, 16)
    elif month in [3, 4, 5]:        # Spring
        return random.uniform(5, 25)
    elif month in [6, 7, 8]:        # Summer
        return random.uniform(15, 35)
    elif month in [9, 10, 11]:      # Autumn
        return random.uniform(5, 20)
    else:
        raise ValueError("Month must be between 1 and 12")

def main():
    month = int(input("Enter a month (1-12): "))
    random_temp = get_random_temp(month)
    print(f"The temperature in the month {month} is {random_temp} degrees Celsius.")
    if random_temp < 0:
        print("Brrr, that’s freezing! Wear some extra layers today.")
    elif 0 <= random_temp < 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 <= random_temp < 24:
        print("Nice weather.")
    elif 24 <= random_temp < 33:
        print("A bit warm, stay hydrated.")
    elif 33 <= random_temp < 40:
        print("It’s really hot! Stay cool.")

main()

#Exercise 8: Pizza Toppings
## Instructions
# Write a loop that asks the user to enter pizza toppings one by one.
# Stop the loop when the user types 'quit'.
# For each topping entered, print:
# "Adding [topping] to your pizza."
# After exiting the loop, print all the toppings and the total cost of the pizza.
# The base price is $10, and each topping adds $2.50.

toppings = []
while True:
    topping = input("Enter a pizza topping (or type 'quit' to finish): ")
    if topping.lower() == 'quit':
        break
    toppings.append(topping)
    print(f"Adding {topping} to your pizza.")

base_price = 10
topping_price = 2.5
total_cost = base_price + len(toppings) * topping_price
print(f"Your pizza toppings: {', '.join(toppings)}")
print(f"The total cost of your pizza is: ${total_cost:.2f}")