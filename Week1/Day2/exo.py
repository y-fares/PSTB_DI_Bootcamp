# Download this text file http://www.practicepython.org/assets/nameslist.txt and do the following steps
# Read the file line by line
# Read only the 5th line of the file
# Read only the 5 first characters of the file
# Read all the file and return it as a list of strings. Then split each word into letters
# Find out how many occurences of the names "Darth", "Luke" and "Lea" are in the file
# Append your first name at the end of the file
# Append "SkyWalker" next to each first name "Luke"

with open("nameslist.txt", "r") as file:
    lines = file.readlines()
    print("5th line:", lines[4].strip())
    file.seek(0)  # Go back to the beginning of the file
    first_five_chars = file.read(5)
    print("First 5 characters:", first_five_chars)
    file.seek(0)  # Go back to the beginning of the file
    all_lines = file.readlines()
    all_words = [line.strip() for line in all_lines]
    all_letters = [list(word) for word in all_words]
    print("All words split into letters:", all_letters)
    file.seek(0)  # Go back to the beginning of the file
    content = file.read()
    darth_count = content.count("Darth")
    luke_count = content.count("Luke")
    lea_count = content.count("Lea")
    print(f"Occurrences - Darth: {darth_count}, Luke: {luke_count}, Lea: {lea_count}")