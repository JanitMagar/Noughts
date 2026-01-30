"""
Noughts and Crosses(Tic-Tac-Toe)
Student Name: Janit Saru Magar
Student ID: 2603768
"""

import random
import os.path
import json

random.seed()


def draw_board(board):
    """
    Display the noughts and crosses game board.
    """
    print("      -----------")
    for i in range(3):
        print("      |", board[i][0], "|", board[i][1], "|", board[i][2], "|")
        print("      -----------")


def welcome(board):
    """
    Display the welcome message, show the initial board layout,
    and explain how to enter moves.

    Args:
        board (list[list[str]]): The 3x3 game board (list of lists).

    Returns:
        None
    """
    print("-" * 60)
    print('Welcome to Noughts and Crosses')
    print("Board layout is shown below:")
    draw_board(board)
    print("Enter number 1 to 9 when asked.")
    print("-" * 60)


def initialise_board(board):
    """
    Reset the board by filling all cells with a single space ' '.

    Args:
        board (list[list[str]]): The 3x3 game board to be cleared.

    Returns:
        list[list[str]]: The cleared board (same object, modified in place).
    """
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '
    return board


def get_player_move(board):
    """
    Prompt the player to choose a square (1-9) and return its row and column.

    Keeps asking until a valid, empty square is chosen.

    Args:
        board (list[list[str]]): The current 3x3 game board.

    Returns:
        tuple[int, int]: (row, col) indices (0-based) of the chosen square.
    """
    while True:
        print("-" * 30)
        try:
            num = int(input("Choose square 1-9: "))
        except ValueError:
            print("Please enter a number.")
            continue

        if num < 1 or num > 9:
            print("Number must be between 1 and 9.")
            continue

        row = (num - 1) // 3
        col = (num - 1) % 3

        if board[row][col] != ' ':
            print("This square is already taken.")
            continue

        return row, col


def choose_computer_move(board):
    """
    Select a random empty square for the computer's move (O).

    Args:
        board (list[list[str]]): The current 3x3 game board.

    Returns:
        tuple[int, int]: (row, col) indices of the chosen empty square.
    """
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == ' ':
            return row, col


def check_for_win(board, mark):
    """
    Check if the given mark ('X' or 'O') has three in a row, column, or diagonal.

    Args:
        board (list[list[str]]): The current 3x3 game board.
        mark (str): The symbol to check ('X' or 'O').

    Returns:
        bool: True if the mark has won, False otherwise.
    """
    # rows
    for r in range(3):
        if board[r][0] == mark and board[r][1] == mark and board[r][2] == mark:
            return True

    # columns
    for c in range(3):
        if board[0][c] == mark and board[1][c] == mark and board[2][c] == mark:
            return True

    # diagonals
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        return True
    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
        return True

    return False


def check_for_draw(board):
    """
    Check if the game is a draw (board is full with no winner).

    Args:
        board (list[list[str]]): The current 3x3 game board.

    Returns:
        bool: True if the board is completely filled, False if any empty cell remains.
    """
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                return False
    return True


def play_game(board):
    """
    Run a complete game of Noughts and Crosses between player (X) and computer (O).

    Args:
        board (list[list[str]]): The 3x3 game board to play on.

    Returns:
        int: 1 if player wins, -1 if computer wins, 0 if draw.
    """
    initialise_board(board)
    draw_board(board)

    while True:
        print("-" * 30)
        print("Your turn (X)")
        row, col = get_player_move(board)
        board[row][col] = "X"
        draw_board(board)

        if check_for_win(board, "X"):
            print("You Won!")
            return 1

        if check_for_draw(board):
            print("It's a draw!")
            return 0

        print("-" * 30)
        print("Computer's turn (O)")
        row, col = choose_computer_move(board)
        board[row][col] = "O"
        draw_board(board)

        if check_for_win(board, "O"):
            print("Computer Won!")
            return -1

        if check_for_draw(board):
            print("It's a draw!")
            return 0


def menu():
    """
    Display the main menu and get the user's choice.

    Returns:
        str: The user's selected option ('1', '2', '3', or 'q').
    """
    print("-" * 60)
    print("1 - Play the game")
    print("2 - Save score")
    print("3 - Show leaderboard")
    print("q - Quit")
    print("-" * 60)

    while True:
        choice = input("Enter 1, 2, 3 or q: ")
        if choice in ["1", "2", "3", "q"]:
            return choice
        print("Wrong choice. Please enter 1, 2, 3 or q.")


def load_scores():
    """
    Load player scores from 'leaderboard.txt' if the file exists.

    Returns:
        dict: Dictionary of {player_name: score} or empty dict if file missing/invalid.
    """
    leaders = {}
    if os.path.exists('leaderboard.txt'):
        try:
            with open("leaderboard.txt", 'r', encoding='utf-8') as file:
                leaders = json.load(file)
        except:
            leaders = {}
    return leaders


def save_score(score):
    """
    Ask for player name and save/update their score in 'leaderboard.txt'.

    Args:
        score (int): The score to add (usually 1 for win, 0 for draw/loss).

    Returns:
        None
    """
    while True:
        name = input("Enter your name: ")
        if name != '':
            break
        print("Name cannot be empty.")

    leaders = load_scores()

    if name in leaders:
        leaders[name] += score
    else:
        leaders[name] = score

    with open("leaderboard.txt", 'w', encoding='utf-8') as f:
        json.dump(leaders, f)

    print("Score saved for", name)


def display_leaderboard(leaders):
    """
    Print the leaderboard showing all saved player names and scores.

    Args:
        leaders (dict): Dictionary of {player_name: score}.

    Returns:
        None
    """
    print("-" * 30)
    if len(leaders) == 0:
        print("No scores yet. Play some games first.")
    else:
        print("Name       Score")
        print("-" * 20)
        for name in leaders:
            print(name, "   ", leaders[name])
    print("-" * 30)
