#!/usr/bin/env python3

from typing import List, Optional, Tuple

def initialize_board() -> List[List[str]]:
    """Creates and returns an empty 3x3 game board."""
    return [[' ' for _ in range(3)] for _ in range(3)]

def display_board(board: List[List[str]]) -> None:
    """Displays the current state of the game board."""
    print("\n   1   2   3")
    for i, row in enumerate(board):
        print(f"{i + 1}  {' | '.join(row)} ")
        if i < 2:
            print("  ---+---+---")
    print()

def get_player_input(player: str, board: List[List[str]]) -> Tuple[int, int]:
    """Prompts the player for a move and validates the input."""
    while True:
        try:
            move = input(f"Player {player}, enter your move (row and column): ")
            x_str, y_str = move.strip().split()
            x, y = int(x_str) - 1, int(y_str) - 1
            if x not in range(3) or y not in range(3):
                print("Coordinates must be between 1 and 3.")
                continue
            if board[x][y] != ' ':
                print("That cell is already occupied.")
                continue
            return x, y
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")

def check_win(board: List[List[str]], player: str) -> bool:
    """Checks if the specified player has won the game."""
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) \
           or all(board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    if (board[0][0] == board[1][1] == board[2][2] == player) \
       or (board[0][2] == board[1][1] == board[2][0] == player):
        return True
    return False

def check_draw(board: List[List[str]]) -> bool:
    """Checks if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def switch_player(current_player: str) -> str:
    """Switches the turn to the other player."""
    return 'O' if current_player == 'X' else 'X'

def play_game() -> None:
    """Runs a single game of Tic-Tac-Toe."""
    board = initialize_board()
    current_player = 'X'
    while True:
        display_board(board)
        x, y = get_player_input(current_player, board)
        board[x][y] = current_player
        if check_win(board, current_player):
            display_board(board)
            print(f"Congratulations! Player {current_player} wins!")
            break
        if check_draw(board):
            display_board(board)
            print("The game is a draw.")
            break
        current_player = switch_player(current_player)

def main() -> None:
    """Main function to manage game sessions."""
    print("Welcome to Tic-Tac-Toe!")
    while True:
        play_game()
        replay = input("Would you like to play again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thank you for playing!")
            break

if __name__ == "__main__":
    main()