from rich.console import Console

console = Console(force_terminal=True, color_system="truecolor")

BOARD_WIDTH = 8
BOARD_HEIGHT = 8

CELL_WIDTH = 9
CELL_HEIGHT = 3

LIGHT_SQUARE = "#F0D9B5"
DARK_SQUARE = "#B58863"

# Brazde iz specifikacije projekta
BRAZDE = {(3, 0), (4, 7)}


def is_dark_square(row, column):

    return (row + column) % 2 == 1


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
        board[square] = "b"

    for square in range(20, 32):
        board[square] = "w"


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

                    if piece == "w":
                        text = f"●{index:02}"
                        text_color = "bright_white"
                    elif piece == "b":
                        text = f"●{index:02}"
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
    board = [None] * 32
    starting_board(board)
    print_board(board)