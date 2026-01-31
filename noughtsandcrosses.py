"""
Noughts and Crosses (Tic-Tac-Toe)
Student Name: Janit Saru Magar
Student ID: 2603768
"""

import random
import os
import json


def draw_board(board):
    """
    Display the noughts and crosses board.
    """
    print("      -----------")
    for row in board:
        print(f"      | {row[0]} | {row[1]} | {row[2]} |")
        print("      -----------")


def welcome(board):
    """
    Display welcome message and initial board layout.
    """
    print("-" * 60)
    print("Welcome to Noughts and Crosses")
    print("Board layout is shown below:")
    draw_board(board)
    print("Enter a number between 1 and 9 to choose a square.")
    print("-" * 60)


def initialise_board(board):
    """
    Reset all board cells to a single space ' '.
    """
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '
    return board


def get_player_move(board):
    """
    Ask the player to choose a valid square (1-9).
    Return row and column indices.
    """
    while True:
        try:
            choice = int(input("Choose square (1-9): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice < 1 or choice > 9:
            print("Number must be between 1 and 9.")
            continue

        row = (choice - 1) // 3
        col = (choice - 1) % 3

        if board[row][col] != ' ':
            print("Square already taken. Choose another.")
            continue

        return row, col


def choose_computer_move(board):
    """
    Choose the best move for the computer (O).
    Strategy:
    1. Win if possible.
    2. Block player win.
    3. Take centre.
    4. Take corner.
    5. Random move.
    """
    # 1. Try to win
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                if check_for_win(board, 'O'):
                    board[row][col] = ' '
                    return row, col
                board[row][col] = ' '

    # 2. Block player win
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'X'
                if check_for_win(board, 'X'):
                    board[row][col] = ' '
                    return row, col
                board[row][col] = ' '

    # 3. Take centre
    if board[1][1] == ' ':
        return 1, 1

    # 4. Take a corner
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    empty_corners = [
        (row, col) for row, col in corners
        if board[row][col] == ' '
    ]
    if empty_corners:
        return random.choice(empty_corners)

    # 5. Random move (remaining spaces)
    empty_spaces = [
        (row, col)
        for row in range(3)
        for col in range(3)
        if board[row][col] == ' '
    ]
    return random.choice(empty_spaces)


def check_for_win(board, mark):
    """
    Return True if the given mark has won.
    """
    # Check rows and columns
    for index in range(3):
        if all(board[index][col] == mark for col in range(3)):
            return True
        if all(board[row][index] == mark for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == mark for i in range(3)):
        return True
    if all(board[i][2 - i] == mark for i in range(3)):
        return True

    return False


def check_for_draw(board):
    """
    Return True if board is full, False otherwise.
    """
    return all(
        board[row][col] != ' '
        for row in range(3)
        for col in range(3)
    )


def play_game(board):
    """
    Play a full game.
    Returns:
        1  -> Player win
        0  -> Draw
        -1 -> Computer win
    """
    initialise_board(board)
    draw_board(board)

    while True:
        # Player turn
        print("\nYour turn (X)")
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)

        if check_for_win(board, 'X'):
            print("You won!")
            return 1

        if check_for_draw(board):
            print("It's a draw!")
            return 0

        # Computer turn
        print("\nComputer's turn (O)")
        row, col = choose_computer_move(board)
        board[row][col] = 'O'
        draw_board(board)

        if check_for_win(board, 'O'):
            print("Computer won!")
            return -1

        if check_for_draw(board):
            print("It's a draw!")
            return 0


def menu():
    """
    Display the main menu and return valid choice.
    """
    print("-" * 60)
    print("1 - Play the game")
    print("2 - Save score")
    print("3 - Show leaderboard")
    print("q - Quit")
    print("-" * 60)

    while True:
        choice = input("Enter 1, 2, 3 or q: ").lower()
        if choice in ('1', '2', '3', 'q'):
            return choice
        print("Invalid choice. Please try again.")


def load_scores():
    """
    Load leaderboard scores from leaderboard.txt.
    Return dictionary.
    """
    if not os.path.exists("leaderboard.txt"):
        return {}

    try:
        with open("leaderboard.txt", "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_score(score):
    """
    Ask for player name and save/update score.
    """
    while True:
        name = input("Enter your name: ").strip()
        if name:
            break
        print("Name cannot be empty.")

    leaders = load_scores()
    leaders[name] = leaders.get(name, 0) + score

    with open("leaderboard.txt", "w", encoding="utf-8") as file:
        json.dump(leaders, file)

    print(f"Score saved for {name}.")


def display_leaderboard(leaders):
    """
    Display leaderboard sorted by highest score.
    """
    print("-" * 30)

    if not leaders:
        print("No scores yet. Play some games first.")
    else:
        print(f"{'Name':<15}{'Score'}")
        print("-" * 25)

        sorted_scores = sorted(
            leaders.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for name, score in sorted_scores:
            print(f"{name:<15}{score}")

    print("-" * 30)
