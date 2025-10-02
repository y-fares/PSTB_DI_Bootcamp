list = [("name", "Elie"), ("job", "Instructor")]
dict_from_list = {k: v for k, v in list}
print(dict_from_list)

state = ["CA", "NJ", "RI"]
cities = ["California", "New Jersey", "Rhode Island"]
dict_state_cities = {k: v for k, v in zip(state, cities)}
print(dict_state_cities)

keys_vowesl = "aeiou"
values_vowels = [0,0,0,0,0]
dict_vowels = {k: v for k, v in zip(keys_vowesl, values_vowels)}
print(dict_vowels)

alphabet_dict = {i: chr(64 + i) for i in range(1, 27)}
print(alphabet_dict)

my_str = "awesome sauce"
vowels = "aeiou"

init_vowels = {v: 0 for v in vowels}
for letter in my_str:
    if letter in init_vowels:
        init_vowels[letter] += 1
print(init_vowels)