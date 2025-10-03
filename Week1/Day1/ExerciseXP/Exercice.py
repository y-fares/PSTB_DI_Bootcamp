def Exo1():
    str = "Hello world"
    for i in range(1,5):
        print(str)

def Exo2():
    def my_pow(a:int, b:int, c:int):
        return (a**b)*c
    a = int(input("a = "))
    b = int(input("b = "))
    c = int(input("c = "))
    print(f"({a}^{b})*{c} = {my_pow(a,b,c)}")

def Exo3():
    my_name = "Moi"
    def check_name():
        your_name = str(input("What is your name ? "))
        if my_name == your_name:
            print("hey, we have the same name !!!!")
        else:
            print(f"Hello {your_name}, nice to meet you, I'm {my_name}")

def Exo4():
    your_size = int(input("Quel taille (en cm) fais-tu ? "))
    size_min = 145
    if your_size >= size_min:
        print("C'est bon tu peux passer")
    else:
        print("You Shall Not Pass !!!!")

def Exo5():
    my_fav_numbers = set()
    my_fav_numbers.add(1)
    print(my_fav_numbers)
    my_fav_numbers.add(2)
    my_fav_numbers.add(3)
    print(my_fav_numbers)
    my_fav_numbers.discard(3)
    print(my_fav_numbers)
    friend_fav_numbers = set()
    friend_fav_numbers.add(int(input("Enter your friend's favorite number: ")))
    our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
    print(our_fav_numbers)

def Exo6():
    my_tuple_1 = (1, 2, 3)
    #print(my_tuple_1[0])
    #my_tuple_1[3] = 4 ==> error car les tuples sont immuables
    autre_tuple = (4, 5, 6)
    my_tuple_1 = my_tuple_1 + autre_tuple
    print(my_tuple_1)

def Exo7():
    basket = ["Banana", "Apples", "Oranges", "Blueberries"]
    #1. Remove "Banana" from the list.
    basket.remove("Banana")
    #2. Remove "Blueberries" from the list.
    basket.remove("Blueberries")
    #3. Add "Kiwi" to the end of the list.
    basket.append("Kiwi")
    #4. Add "Apples" to the beginning of the list.
    basket.insert(0, "Apples")
    #5. Count how many apples are in the basket.
    print(basket.count("Apples"))
    #6. Empty the basket.
    basket.clear()
    #7. Print the basket.
    print(basket)

def Exo8():

    sandwich_orders = ["Tuna sandwich", "Pastrami sandwich", "Avocado sandwich", "Pastrami sandwich", "Egg sandwich", "Chicken sandwich", "Pastrami sandwich"]
    finished_sandwiches = []
    
    while "Pastrami sandwich" in sandwich_orders:
        sandwich_orders.remove("Pastrami sandwich")

    while sandwich_orders:
        current_sandwich = sandwich_orders.pop(0)
        print(f"I made your {current_sandwich}")
        finished_sandwiches.append(current_sandwich)
        
    print(f"sandwich_orders = {sandwich_orders}")
    print(f"finished_sandwiches = {finished_sandwiches}")

if __name__ == '__main__':
    Exo1()
    Exo2()
    Exo3()
    Exo4()
    Exo5()
    Exo6()
    Exo7()
    Exo8()