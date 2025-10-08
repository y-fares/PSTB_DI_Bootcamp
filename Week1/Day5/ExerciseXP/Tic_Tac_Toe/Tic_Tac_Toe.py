#  What you will create
# Create a TicTacToe game in python, where two users can play together.

# tic-tac-toe

# Instructions
# The game is played on a grid that’s 3 squares by 3 squares.
# Players take turns putting their marks (O or X) in empty squares.
# The first player to get 3 of their marks in a row (up, down, across, or diagonally) is the winner.
# When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.


# Hint
# To do this project, you basically need to create four functions:

# display_board() – To display the Tic Tac Toe board (GUI).
# player_input(player) – To get the position from the player.
# check_win() – To check whether there is a winner or not.
# play() – The main function, which calls all the functions created above.
# Note: The 4 functions above are just an example. You can implement many more helper functions or choose a completely different appoach if you want.

# Tips : Consider the following:
# What functionality will need to accur every turn to make this program work?
# After contemplating the question above, think about splitting your code into smaller pieces (functions).
# Remember to follow the single responsibility principle! each function should do one thing and do it well!


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # A list to hold the board state
        self.current_winner = None  # Keep track of the winner!

    def display_board(self):
        """Affiche le plateau."""
        rows = [self.board[i:i+3] for i in range(0, 9, 3)]
        print("\n")
        print("┌───┬───┬───┐")
        for r, row in enumerate(rows):
            print(f"│ {row[0]} │ {row[1]} │ {row[2]} │")
            if r < 2:
                print("├───┼───┼───┤")
        print("└───┴───┴───┘")

    def player_input(self, player):
        """
        Demande une position (1-9) au joueur.
        Retourne l'index (0-8) valide et place le coup.
        """
        while True:
            raw = input(f"Joueur {player}, choisis une case (1-9) : ").strip()
            if not raw.isdigit():
                print("Entrée invalide. Tape un nombre entre 1 et 9.")
                continue
            pos = int(raw)
            if not (1 <= pos <= 9):
                print("Hors plateau. Choisis entre 1 et 9.")
                continue
            idx = pos - 1
            if self.board[idx] != ' ':
                print("Case déjà prise. Choisis une autre case.")
                continue
            self.board[idx] = player
            return idx  # utile si tu veux exploiter l'index

    def check_win(self):
        """
        Vérifie s'il y a un gagnant.
        Met à jour self.current_winner et retourne True/False.
        """
        b = self.board
        lignes = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),        # lignes
            (0, 3, 6), (1, 4, 7), (2, 5, 8),        # colonnes
            (0, 4, 8), (2, 4, 6)                    # diagonales
        ]
        for a, c, d in lignes:
            if b[a] != ' ' and b[a] == b[c] == b[d]:
                self.current_winner = b[a]
                return True
        return False

    def play(self):
        """
        Boucle principale du jeu.
        Alterne X et O, affiche, détecte victoire/égalité.
        """
        print("Positions (référence) :")
        print("┌───┬───┬───┐")
        print("│ 1 │ 2 │ 3 │")
        print("├───┼───┼───┤")
        print("│ 4 │ 5 │ 6 │")
        print("├───┼───┼───┤")
        print("│ 7 │ 8 │ 9 │")
        print("└───┴───┴───┘")

        player = 'X'
        for turn in range(9):  # max 9 coups
            self.display_board()
            self.player_input(player)
            if self.check_win():
                self.display_board()
                print(f"Victoire de {player} !")
                return
            player = 'O' if player == 'X' else 'X'

        self.display_board()
        print("Match nul.")


if __name__ == "__main__":
    game = TicTacToe()
    game.play()