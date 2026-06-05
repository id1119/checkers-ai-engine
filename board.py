from rich.console import Console
from piece import Piece

console = Console(force_terminal=True, color_system="truecolor")

BOARD_WIDTH = 8
BOARD_HEIGHT = 8

CELL_WIDTH = 9
CELL_HEIGHT = 3

LIGHT_SQUARE = "#F0D9B5"
DARK_SQUARE = "#B58863"

board = [None] * 32

BRAZDE = {(3, 0), (4, 7)}

LEFT_SIDE = {
    (0, 1), (0, 3), (0, 5), (0, 7),
}

RIGHT_SIDE = {
    (7, 0), (7, 2), (7, 4), (7, 6),
}

SIDE_SQUARES = {
    (1, 0), (3, 0), (5, 0), (7, 0),
    (0, 1), (0, 3), (0, 5), (0, 7),
    (7, 0), (7, 2), (7, 4), (7, 6),
    (0, 7), (2, 7), (4, 7), (6, 7),
}

def is_inside_board(row, column):

    return 0 <= row < BOARD_HEIGHT and 0 <= column < BOARD_WIDTH

def is_dark_square(row, column):

    return is_inside_board(row, column) and (row + column) % 2 == 1

def row_column_to_index(row, column):

    if not is_dark_square(row, column):
        return None

    return row * 4 + column // 2


def index_to_row_column(index):

    row = index // 4
    row_position = index % 4

    if row % 2 == 0:
        column = row_position * 2 + 1
    else:
        column = row_position * 2

    return row, column


def starting_board(board):

    for i in range(32):
        board[i] = None

    for square in range(12):
        board[square] = Piece("black", "pawn")

    for square in range(20, 32):
        board[square] = Piece("white", "pawn")


def print_square(text, background_color, text_color="black"):
    text = text.center(CELL_WIDTH)
    console.print(text, style=f"{text_color} on {background_color}", end="")


def print_board(board):
    console.print()

    console.print("    ", end="")
    for column in range(BOARD_WIDTH):
        console.print(str(column).center(CELL_WIDTH), end="")
    console.print()

    for row in range(BOARD_HEIGHT):

        for line in range(CELL_HEIGHT):

            if line == 1:
                console.print(f"{row}   ", end="")
            else:
                console.print("    ", end="")

            for column in range(BOARD_WIDTH):
                dark = is_dark_square(row, column)

                if dark:
                    background = DARK_SQUARE
                else:
                    background = LIGHT_SQUARE

                text = ""
                text_color = "black"

                if line == 1 and dark:
                    index = row_column_to_index(row, column)
                    piece = board[index]

                    if piece is not None and piece.color == "white" and piece.kind == "pawn":
                        text = f"●{index:02}"
                        text_color = "bright_white"
                    elif piece is not None and piece.color == "black" and piece.kind == "pawn":
                        text = f"●{index:02}"
                        text_color = "black"
                    elif piece is not None and piece.color == "white" and piece.kind == "king":
                        text = f"♛{index:02}"
                        text_color = "bright_white"
                    elif piece is not None and piece.color == "black" and piece.kind == "king":
                        text = f"♛{index:02}"
                        text_color = "black"
                    else:
                        text = f"{index:02}"
                        if (row, column) in BRAZDE:
                            text_color = "bright_red"
                        else:
                            text_color = "cyan"

                print_square(text, background, text_color)

            if line == 1:
                console.print(f"   {row}")
            else:
                console.print()

    console.print("    ", end="")
    for column in range(BOARD_WIDTH):
        console.print(str(column).center(CELL_WIDTH), end="")
    console.print()
    console.print()


if __name__ == "__main__":

    starting_board(board)
    print_board(board)
