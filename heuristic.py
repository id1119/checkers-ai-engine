import board

PAWN_VALUE = 100
KING_VALUE = 300
MARKO_VALUE = 600
TOPUZ_VALUE = 35
SARAC_VALUE = 30
ARMOR_VALUE = 25
WINE_VALUE = 25
BLESSING_VALUE = 20
EDGE_VALUE = 10
BRAZDA_VALUE = 15
TERMINAL_WIN_VALUE = 100000


def evaluate_game_state(current_game, player_color):
    winner = current_game.get_winner()

    if winner == player_color:
        return TERMINAL_WIN_VALUE
    if winner is not None:
        return -TERMINAL_WIN_VALUE

    return evaluate_board(current_game.board, player_color)


def evaluate_board(game_board, player_color):
    score = 0

    for index, piece in enumerate(game_board):
        if piece is None:
            continue

        piece_score = evaluate_piece(piece, index)

        if piece.color == player_color:
            score += piece_score
        else:
            score -= piece_score

    return score


def evaluate_piece(piece, index):
    row, column = board.index_to_row_column(index)

    if piece.is_marko():
        score = MARKO_VALUE
    elif piece.kind == "king":
        score = KING_VALUE
    else:
        score = PAWN_VALUE

    if piece.has_topuz:
        score += TOPUZ_VALUE
    if piece.has_sarac:
        score += SARAC_VALUE
    if piece.armor_turns > 0:
        score += ARMOR_VALUE
    if piece.has_wine:
        score += WINE_VALUE
    if piece.has_blessing:
        score += BLESSING_VALUE
    if (column, row) in board.SIDE_SQUARES:
        score += EDGE_VALUE
    if (row, column) in board.BRAZDE:
        score += BRAZDA_VALUE

    return score
