# Exercise 1: Cars
# Copy the following string into your code: Volkswagen, Toyota, Ford Motor, Honda, Chevrolet.
# Convert it into a list using Python (don’t do it by hand!).
# Print out a message saying how many manufacturers/companies are in the list.
# Print the list of manufacturers in reverse/descending order (Z-A).
# Using loops or list comprehension:
# Find out how many manufacturers’ names have the letter o in them.
# Find out how many manufacturers’ names do not have the letter i in them.
# Bonus:

# There are a few duplicates in this list: ["Honda", "Volkswagen", "Toyota", "Ford Motor", "Honda", "Chevrolet", "Toyota"]
# Remove these programmatically. (Hint: you can use a set to help you).
# Print out the companies without duplicates, in a comma-separated string with no line-breaks (e.g., “Acura, Alfa Romeo, Aston Martin, …”), also print out a message saying how many companies are now in the list.
# Bonus:

# Print out the list of manufacturers in ascending order (A-Z), but reverse the letters of each manufacturer’s name.

info = "Volkswagen, Toyota, Ford Motor, Honda, Chevrolet"
companies = info.split(", ")
type(companies)
print(f"There are {len(companies)} manufacturers/companies in the list.")
companies.sort(reverse=True)
print(companies)
count_o = sum(1 for company in companies if 'o' in company.lower())
print(f"There are {count_o} manufacturers' names that have the letter 'o' in them.")
count_no_i = sum(1 for company in companies if 'i' not in company.lower())
print(f"There are {count_no_i} manufacturers' names that do not have the letter 'i' in them.")
# Bonus 1
niou_companies = ["Honda", "Volkswagen", "Toyota", "Ford Motor", "Honda", "Chevrolet", "Toyota"]
unique_companies = set(niou_companies)
print(f"Companies without duplicates: {', '.join(unique_companies)}")
print(f"There are now {len(unique_companies)} companies in the list.")
# Bonus 2
reversed_companies = [company[::-1] for company in sorted(unique_companies)]
print("List of manufacturers in ascending order with reversed letters:")
print(reversed_companies)

# Exercise 2: What’s your name?
# Write a function called get_full_name() that takes three arguments: 1: first_name, 2: middle_name, 3: last_name.
# middle_name should be optional; if it’s omitted by the user, the name returned should only contain the first and the last name.
# For example, get_full_name(first_name="john", middle_name="hooker", last_name="lee") will return “John Hooker Lee”.
# But get_full_name(first_name="bruce", last_name="lee") will return “Bruce Lee”.
def get_full_name(first_name: str, last_name: str, middle_name: str = "") -> str:
    if middle_name:
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"
    return full_name.title()

print(get_full_name(first_name="john", middle_name="hooker", last_name="lee"))  # Output: John Hooker Lee
print(get_full_name(first_name="bruce", last_name="lee"))  # Output: Bruce Lee

# Exercise 3: From English to Morse
# Write a function that converts English text to Morse code and another one that does the opposite.
# Hint: Check the internet for a translation table, every letter is separated with a space and every word is separated with a slash /.

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----',
}

def english_to_morse(text: str) -> str:
    morse_code = []
    for char in text.upper():
        if char == ' ':
            morse_code.append('/')  # Word separator
        elif char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
    return ' '.join(morse_code)

def morse_to_english(morse: str) -> str:
    morse_words = morse.split(' / ')
    english_text = []
    for word in morse_words:
        letters = word.split()
        english_word = ''.join(next((k for k, v in MORSE_CODE_DICT.items() if v == letter), '') for letter in letters)
        english_text.append(english_word)
    return ' '.join(english_text)

print(english_to_morse("Hello World"))  # Output: ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
print(morse_to_english(".... . .-.. .-.. --- / .-- --- .-. .-.. -.."))  # Output: "HELLO WORLD"