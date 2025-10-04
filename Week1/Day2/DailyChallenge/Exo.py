# Challenge
# Ask a user for a word.
a_word = input("Please enter a word : ")
# Write a program that creates a dictionary. This dictionary stores the indexes of each letter in a list.
a_dict = {}

for index, letter in enumerate(a_word):
    if letter in a_dict:
        a_dict[letter].append(index)
    else:
        a_dict[letter] = [index]
# Make sure the letters are the keys.
# Make sure the letters are strings.
# Make sure the indexes are stored in a list, and those lists are values.

# Examples
# “dodo” ➞ { “d”: [0, 2], “o”: [1, 3] }
# “froggy” ➞ { “f”: [0], “r”: [1], “o”: [2], “g”: [3, 4], “y”: [5] }
# “grapes” ➞ { “g”: [0], “r”: [1], “a”: [2], “p”: [3] }

print(a_dict)