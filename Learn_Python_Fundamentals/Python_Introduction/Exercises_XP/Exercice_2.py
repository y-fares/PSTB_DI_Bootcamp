output = []

def human_years():
    human_age = int(input("Enter the age of the dog in human years: "))
    if human_years < 0:
        print("Age cannot be negative.")
    else:
        cat_age = cat_years(human_age)
        dog_age = dog_years(human_age)  
        output.append(human_age)
        output.append(cat_age)
        output.append(dog_age)
        return output

def cat_years(human_age):
    cat_age = 0
    if human_age == 1:
        cat_age = 15
    elif human_age == 2:
        cat_age = 24
    else:
        cat_age = 24 + (cat_years - 2) * 4
    return cat_age

def dog_years(human_age):
        dog_age = 0
    if human_age == 1:
        dog_age = 15
    elif human_age == 2:
        dog_age = 24
    else:
        dog_age = 24 + (cat_years - 2) * 5
    return dog_age