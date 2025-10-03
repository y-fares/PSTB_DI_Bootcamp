def exo1():
    my_month = int(input("Enter a month (1-12): "))
    if my_month in (12, 1, 2):
        print("Winter")
    elif 3 <= my_month <= 5:
        print("Spring")
    elif 6 <= my_month <= 8:
        print("Summer")
    elif 9 <= my_month <= 11:
        print("Autumn")
    else:
        print("Invalid month")

def exo2():
    for i in range(1, 21):
        print(i)
    for i in range(1, 21):
        if i % 2 == 0:
            print(i)

def exo3():
    my_name = "Moi"
    your_name = ""
    while my_name != your_name:
        your_name = str(input("What is your name ? "))
        if my_name == your_name:
            break

def exo4():
    names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']
    check_names = str(input("Enter a name: "))
    if check_names in names:
        print(names.index(check_names))

def exo5():
    a = int(input("Entre un premier chiffre : "))
    b = int(input("Entre un deuxième chiffre : "))
    c = int(input("Entre un premietroisième chiffre : "))
    list = []
    list.append(a)
    list.append(b)
    list.append(c)
    # ou list = [a, b, c]
    print(f"le plus grand chiffre entre {a}, {b} et {c} est {max(list)}")

def exo6():
    isOk = False
    nb = 0
    while not isOk:
        nb = int(input("Entre un chiffre entre 1 et 9 inclus : "))
        if(1 <= nb <= 9):
            isOk = True
    print(f"Merci, vous avez entré le chiffre {nb}")
    import random
    random_nb = random.randint(1, 9)
    if nb == random_nb:
        print("Winner")
    else:
        print(f"Better luck next time.")

if __name__ == "__main__":
    # exo1()
    # exo2()
    # exo3()
    # exo4()
    # exo5()
    exo6()