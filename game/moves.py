import board

def legal_moves(game_board, turn):
    if turn == "white":
        for piece in game_board:
            if piece == "w":
                print(game_board[piece])

