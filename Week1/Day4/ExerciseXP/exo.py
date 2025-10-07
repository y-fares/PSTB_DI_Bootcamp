#  Exercise 1: Pets
# Instructions:
# Use the provided Pets and Cat classes to create a Siamese breed, instantiate cat objects, and use the Pets class to manage them.
# See the example below, before diving in.

# Example:
class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'


# Step 1: Create the Siamese Class
# Create a class called Siamese that inherits from the Cat class.
# You can add any specific attributes or methods for the Siamese breed, or leave it as is if there are no unique behaviors.

class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'


# Step 2: Create a List of Cat Instances
# Create a list called all_cats that contains instances of Bengal, Chartreux, and Siamese cats.
# Example: all_cats = [bengal_obj, chartreux_obj, siamese_obj]
# Give each cat a name and age.

bengal_obj = Bengal("BengalCat", 3)
chartreux_obj = Chartreux("ChartreuxCat", 4)
siamese_obj = Siamese("SiameseCat", 2)

all_cats = [bengal_obj, chartreux_obj, siamese_obj]

# Step 3: Create a Pets Instance
# Create an instance of the Pets class called sara_pets, passing the all_cats list as an argument.
print("On s'aoccupe des chats de Sara")
sara_pets = Pets(all_cats)

# Step 4: Take Cats for a Walk
# # Call the walk() method on the sara_pets instance.
# This should print the result of calling the walk() method on each cat in the list.
print(sara_pets.walk())

# Exercise 2: Dogs
# Goal: Create a Dog class with methods for barking, running speed, and fighting.
# Instructions:

# Step 1: Create the Dog Class
# Create a class called Dog with name, age, and weight attributes.
# Implement a bark() method that returns “ is barking”.
# Implement a run_speed() method that returns weight / age * 10.
# Implement a fight(other_dog) method that returns a string indicating which dog won the fight, based on run_speed * weight.

class Dog:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return f"{self.name} is barking"

    def run_speed(self):
        return (self.weight / self.age) * 10

    def fight(self, other_dog):
        if (self.run_speed() * self.weight) > (other_dog.run_speed() * other_dog.weight):
            return f"The winner is {self.name}"
        else:
            return f"The winner is {other_dog.name}"


# Step 2: Create Dog Instances
# Create three instances of the Dog class with different names, ages, and weights.
dog1 = Dog("Rex", 5, 20)
dog2 = Dog("Buddy", 3, 15)
dog3 = Dog("Max", 4, 25)


# Step 3: Test Dog Methods
# Call the bark(), run_speed(), and fight() methods on the dog instances to test their functionality.
print(dog1.bark())
print(dog2.run_speed())
print(dog1.fight(dog2))
print(dog2.fight(dog3))

# 🌟 Exercise 3: Dogs Domesticated
# Goal: Create a PetDog class that inherits from Dog and adds training and tricks.



# Key Python Topics:

# Inheritance
# super() function
# *args
# Random module


# Instructions:

# Step 1: Import the Dog Class

# In a new Python file, import the Dog class from the previous exercise.


# Step 2: Create the PetDog Class

# Create a class called PetDog that inherits from the Dog class.
# Add a trained attribute to the __init__ method, with a default value of False.
# trained means that the dog is trained to do some tricks.
# Implement a train() method that prints the output of bark() and sets trained to True.
# Implement a play(*args) method that prints “ all play together”.
# *args on this method is a list of dog instances.
# Implement a do_a_trick() method that prints a random trick if trained is True.
# Use this list for the ramdom tricks:
# tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
# Choose a rendom index from it each time the method is called.


# Step 3: Test PetDog Methods

# Create instances of the PetDog class and test the train(), play(*args), and do_a_trick() methods.


# Example:

# # In a new file
# # import the Dog class

# class PetDog(Dog):
#     def __init__(self, name, age, weight): <mark> no need to put the details in the function, you are giving the solution</mark>
#         super().__init__(name, age, weight)
#         self.trained = False

#     def train(self): <mark> no need to put the details in the function, you are giving the solution</mark>
#         print(self.bark())
#         self.trained = True

#     def play(self, *args):
#         # ... code to print play message ...

#     def do_a_trick(self): <mark> no need to put the details in the function, you are giving the solution</mark>
#         if self.trained:
#             tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
#             print(f"{self.name} {random.choice(tricks)}")

# # Test PetDog methods
# my_dog = PetDog("Fido", 2, 10)
# my_dog.train()
# my_dog.play("Buddy", "Max")
# my_dog.do_a_trick()


# 🌟 Exercise 4: Family and Person Classes
# Goal:

# Practice working with classes and object interactions by modeling a family and its members.



# Key Python Topics:

# Classes and objects
# Instance methods
# Object interaction
# Lists and loops
# Conditional statements (if/else)
# String formatting (f-strings)


# Instructions:

# Step 1: Create the Person Class

# Define a Person class with the following attributes:
# first_name
# age
# last_name (string, should be initialized as an empty string)
# Add a method called is_18():
# It should return True if the person is 18 or older, otherwise False.


# Step 2: Create the Family Class

# Define a Family class with:
# A last_name attribute
# A members list that will store Person objects (should be initialized as an empty list)


# Add a method called born(first_name, age):
# It should create a new Person object with the given first name and age.
# It should assign the family’s last name to the person.
# It should add this new person to the members list.


# Add a method called check_majority(first_name):
# It should search the members list for a person with that first_name.
# If the person exists, call their is_18() method.
# If the person is over 18, print:
# "You are over 18, your parents Jane and John accept that you will go out with your friends"
# Otherwise, print:
# "Sorry, you are not allowed to go out with your friends."


# Add a method called family_presentation():
# It should print the family’s last name.
# Then, it should print each family member’s first name and age.


# Expected Behavior:

# Once implemented, your program should allow you to:

# Create a family with a last name.
# Add members to the family using the born() method.
# Use check_majority() to see if someone is allowed to go out.
# Display family information with family_presentation().
# Don’t forget to test your classes by creating an instance of Family, adding members, and calling each method to see the expected output.