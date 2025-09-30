import random

def number_guessing_game():
    random_number = random.randint(1, 100)
    max_attempts = 7
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