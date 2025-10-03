from datetime import datetime

while True:
    s = input("Enter your birthdate (DD/MM/YYYY) : ")
    try:
        birthdate = datetime.strptime(s, "%d/%m/%Y").date()
        break
    except ValueError:
        print("Invalid date. Use DD/MM/YYYY, e.g. 31/12/2000.")

last_digit = int(birthdate.strftime("%d")[-1])
print(last_digit)
def display_cake(last_digit):
    #print(last_digit)
    print("\n")
    if last_digit == 0:
        print("\t    ___________")
    elif last_digit == 1:
        print("\t    _____i_____")
    elif last_digit == 2:
        print("\t    ____ii_____")
    elif last_digit == 3:
        print("\t    ____iii____")
    elif last_digit == 4:
        print("\t    ___iiii____")
    elif last_digit == 5:
        print("\t    ___iiiii___")
    elif last_digit == 6:
        print("\t    __iiiiii___")
    elif last_digit == 7:
        print("\t    __iiiiiii__")
    elif last_digit == 8:
        print("\t    _iiiiiiii__")
    elif last_digit == 9:
        print("\t    _iiiiiiiii_")
    print("\t   |:H:a:p:p:y:|")
    print("\t __|___________|__")
    print("\t|^^^^^^^^^^^^^^^^^|")
    print("\t|:B:i:r:t:h:d:a:y:|")
    print("\t|                 |")
    print("\t~~~~~~~~~~~~~~~~~~~")
    print("\n")

display_cake(last_digit)
if int(birthdate.strftime("%Y"))%4 == 0:
    display_cake(last_digit)