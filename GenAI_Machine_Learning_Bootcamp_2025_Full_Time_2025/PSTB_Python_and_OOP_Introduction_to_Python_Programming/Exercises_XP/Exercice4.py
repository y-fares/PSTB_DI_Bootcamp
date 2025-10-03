def exo4():
    your_size = int(input("Quel taille (en cm) fais-tu ? "))
    size_min = 145
    if your_size >= size_min:
        print("C'est bon tu peux passer")
    else:
        print("You Shall Not Pass !!!!")

if __name__ == '__main__':
    exo4()
