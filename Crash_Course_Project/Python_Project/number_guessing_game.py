import random

# Fonction pour le jeu de devinette
def number_guessing_game():
    # On génère un nombre aléatoire entre 1 et 100
    random_number = random.randint(1, 100)
    # On fixe le nombre maximum de tentatives à 7
    max_attempts = 7
    # Instanciation de la variable du nombre de tentatives
    attempt = 0
    for attempt in range(max_attempts):
        guess = int(input("Enter your guess (1-100): "))
        if guess < random_number:
            print("Too low!")
        elif guess > random_number:
            print("Too high!")
        else:
            print(f"Congratulations! You've guessed the number {random_number} correctly in {attempt} tries !")
            break
        attempt += 1

    if attempt == max_attempts:
        print(f"Sorry, you've used all your attempts. The number was {random_number}.")

if __name__ == "__main__":
    number_guessing_game()