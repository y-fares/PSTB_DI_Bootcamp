
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

class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
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

class PetDog(Dog):
    def __init__(self, name, age, weight): 
        super().__init__(name, age, weight)
        self.trained = False

    def train(self): 
        print(self.bark())
        self.trained = True

    def play(self, *args):
        dog_names = ", ".join([dog for dog in args])
        print(f"{self.name}, {dog_names} all play together")

    def do_a_trick(self):
        import random
        if self.trained:
            tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
            print(f"{self.name} {random.choice(tricks)}")

class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age
        self.last_name = "" # should be initialized as an empty string

    def is_18(self):
        return self.age >= 18

class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = [] # should be initialized as an empty list

    def born(self, first_name, age):
        new_member = Person(first_name, age)
        new_member.last_name = self.last_name
        self.members.append(new_member)

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                info = f"{member.first_name}, You are over 18, your parents Jane and John accept that you will go out with your friends" if member.is_18() else f"Sorry {member.first_name}, you are not allowed to go out with your friends."
                print(info)
        # print(f"No member found with the name {first_name}")

    def family_presentation(self):
        print(f"Family Last Name: {self.last_name}")
        for member in self.members:
            print(f"{member.first_name}, Age: {member.age}")

if __name__ == "__main__":
    
    bengal_obj = Bengal("BengalCat", 3)
    chartreux_obj = Chartreux("ChartreuxCat", 4)
    siamese_obj = Siamese("SiameseCat", 2)

    all_cats = [bengal_obj, chartreux_obj, siamese_obj]
    
    print("On s'aoccupe des chats de Sara")
    sara_pets = Pets(all_cats)

    dog1 = Dog("Rex", 5, 20)
    dog2 = Dog("Buddy", 3, 15)
    dog3 = Dog("Max", 4, 25)

    print(dog1.bark())
    print(dog2.run_speed())
    print(dog1.fight(dog2))
    print(dog2.fight(dog3))

    print(sara_pets.walk())

    my_dog = PetDog("Fido", 2, 10)
    my_dog.train()
    my_dog.play("Buddy", "Max")
    my_dog.do_a_trick()

    print("Creating the Smith family")
    smith_family = Family("Smith")
    smith_family.born("Alice", 30)
    smith_family.born("Bob", 16)
    smith_family.check_majority("Alice")
    smith_family.check_majority("Bob")
    smith_family.family_presentation()
    smith_family.check_majority("Charlie")  # Testing a non-existing member