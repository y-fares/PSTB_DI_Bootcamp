class Dog():
    # Initializer / Instance Attributes
    def __init__(self, name_of_the_dog):
        print("A new dog has been initialized !")
        print("His name is", name_of_the_dog)
        self.name = name_of_the_dog

    def bark(self):
        print(f"{self.name} barks ! WAF")

    def rename(self, new_age):
        self.age = new_age
        print(f"The dog's new age is {self.age}")

    def infos(self):
        print(f"NAME = {self.name}, AGE = {self.age}")


my_dog = Dog("Rex")
my_dog.bark()
my_dog.rename(5)a
my_dog.infos()