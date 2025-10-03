my_name = "Moi"

def check_name():
    your_name = str(input("What is your name ? "))
    if my_name == your_name:
        print("hey, we have the same name !!!!")
    else:
        print(f"Hello {your_name}, nice to meet you, I'm {my_name}")

if __name__ == '__main__':
    check_name()
