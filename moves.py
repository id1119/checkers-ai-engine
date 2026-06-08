import board

KING_STEPS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def is_enemy_piece(piece, enemy_color):
    return piece is not None and piece.color == enemy_color


def is_own_piece(piece, own_color):
    return piece is not None and piece.color == own_color


def can_capture(piece):
    return piece.hesitation_turns == 0


def can_topuz_capture(piece, enemy_color):
    return is_enemy_piece(piece, enemy_color) and piece.armor_turns == 0


def remove_captured_piece(game_board, captured_index):
    captured_piece = game_board[captured_index]

    if captured_piece is not None and captured_piece.armor_turns > 0:
        captured_piece.armor_turns -= 1
        return

    game_board[captured_index] = None


def get_move_steps(row, column, row_step):
    if (column,row) in board.LEFT_SIDE:
        return [(row_step, 1)]
    elif (column,row) in board.RIGHT_SIDE:
        return [(row_step, -1)]
    return [(row_step, -1), (row_step, 1)]


def add_move_if_legal(index, row, column, row_step, column_step, game_board, simple_moves):
    check_index = board.row_column_to_index(row + row_step, column + column_step)

    if (check_index is not None and
            game_board[check_index] is None):
        simple_moves.append((index, check_index))


def add_sarac_move_if_legal(index, row, column, row_step, column_step, game_board, simple_moves, own_color):
    check_index = board.row_column_to_index(row + row_step, column + column_step)
    landing_index = board.row_column_to_index(row + row_step * 2, column + column_step * 2)

    if (check_index is not None and
            landing_index is not None and
            is_own_piece(game_board[check_index], own_color) and
            game_board[landing_index] is None):
        simple_moves.append((index, landing_index))


def find_capture_chains(game_board, index, row, column, piece, enemy_color, row_step,
                        capture_moves, path, captured_pieces):
    found_capture = False

    for step_row, step_column in get_move_steps(row, column, row_step):
        check_index = board.row_column_to_index(row + step_row, column + step_column)
        check_index_2 = board.row_column_to_index(row + step_row * 2, column + step_column * 2)

        if (check_index is not None and
                check_index_2 is not None and
                is_enemy_piece(game_board[check_index], enemy_color) and
                game_board[check_index_2] is None):
            found_capture = True

            new_board = game_board.copy()
            new_board[index] = None
            new_board[check_index] = None
            new_board[check_index_2] = piece

            new_row, new_column = board.index_to_row_column(check_index_2)
            find_capture_chains(
                new_board,
                check_index_2,
                new_row,
                new_column,
                piece,
                enemy_color,
                row_step,
                capture_moves,
                path + [check_index_2],
                captured_pieces + [check_index],
            )

    if not found_capture and captured_pieces:
        capture_moves.append((path, captured_pieces))


def find_topuz_capture_chains(game_board, index, row, column, piece, enemy_color, row_step,
                              capture_moves, path, captured_pieces):
    found_capture = False

    for step_row, step_column in get_move_steps(row, column, row_step):
        check_index = board.row_column_to_index(row + step_row, column + step_column)

        if check_index is not None and can_topuz_capture(game_board[check_index], enemy_color):
            found_capture = True

            new_board = game_board.copy()
            new_board[index] = None
            new_board[check_index] = piece

            new_row, new_column = board.index_to_row_column(check_index)
            find_capture_chains(
                new_board,
                check_index,
                new_row,
                new_column,
                piece,
                enemy_color,
                row_step,
                capture_moves,
                path + [check_index],
                captured_pieces + [check_index],
            )

            find_topuz_capture_chains(
                new_board,
                check_index,
                new_row,
                new_column,
                piece,
                enemy_color,
                row_step,
                capture_moves,
                path + [check_index],
                captured_pieces + [check_index],
            )

    if not found_capture and captured_pieces:
        capture_moves.append((path, captured_pieces))


def add_king_simple_moves(index, row, column, game_board, simple_moves):
    for row_step, column_step in KING_STEPS:
        current_row = row + row_step
        current_column = column + column_step

        while True:
            current_index = board.row_column_to_index(current_row, current_column)

            if current_index is None or game_board[current_index] is not None:
                break

            simple_moves.append((index, current_index))
            current_row += row_step
            current_column += column_step


def add_king_sarac_moves(index, row, column, game_board, simple_moves, own_color):
    for row_step, column_step in KING_STEPS:
        current_row = row + row_step
        current_column = column + column_step

        while True:
            check_index = board.row_column_to_index(current_row, current_column)

            if check_index is None:
                break

            if game_board[check_index] is None:
                current_row += row_step
                current_column += column_step
                continue

            landing_row = current_row + row_step
            landing_column = current_column + column_step
            landing_index = board.row_column_to_index(landing_row, landing_column)

            if (is_own_piece(game_board[check_index], own_color) and
                    landing_index is not None and
                    game_board[landing_index] is None):
                simple_moves.append((index, landing_index))

            break


def find_king_capture_chains(game_board, index, row, column, piece, enemy_color,
                             capture_moves, path, captured_pieces):
    found_capture = False

    for row_step, column_step in KING_STEPS:
        current_row = row + row_step
        current_column = column + column_step

        while True:
            check_index = board.row_column_to_index(current_row, current_column)

            if check_index is None:
                break

            if game_board[check_index] is None:
                current_row += row_step
                current_column += column_step
                continue

            if not is_enemy_piece(game_board[check_index], enemy_color):
                break

            landing_row = current_row + row_step
            landing_column = current_column + column_step

            while True:
                landing_index = board.row_column_to_index(landing_row, landing_column)

                if landing_index is None or game_board[landing_index] is not None:
                    break

                found_capture = True

                new_board = game_board.copy()
                new_board[index] = None
                new_board[check_index] = None
                new_board[landing_index] = piece

                find_king_capture_chains(
                    new_board,
                    landing_index,
                    landing_row,
                    landing_column,
                    piece,
                    enemy_color,
                    capture_moves,
                    path + [landing_index],
                    captured_pieces + [check_index],
                )

                landing_row += row_step
                landing_column += column_step

            break

    if not found_capture and captured_pieces:
        capture_moves.append((path, captured_pieces))


def find_king_topuz_capture_chains(game_board, index, row, column, piece, enemy_color,
                                   capture_moves, path, captured_pieces):
    found_capture = False

    for row_step, column_step in KING_STEPS:
        current_row = row + row_step
        current_column = column + column_step

        while True:
            check_index = board.row_column_to_index(current_row, current_column)

            if check_index is None:
                break

            if game_board[check_index] is None:
                current_row += row_step
                current_column += column_step
                continue

            if not can_topuz_capture(game_board[check_index], enemy_color):
                break

            found_capture = True

            new_board = game_board.copy()
            new_board[index] = None
            new_board[check_index] = piece

            new_row, new_column = board.index_to_row_column(check_index)
            find_king_capture_chains(
                new_board,
                check_index,
                new_row,
                new_column,
                piece,
                enemy_color,
                capture_moves,
                path + [check_index],
                captured_pieces + [check_index],
            )

            find_king_topuz_capture_chains(
                new_board,
                check_index,
                new_row,
                new_column,
                piece,
                enemy_color,
                capture_moves,
                path + [check_index],
                captured_pieces + [check_index],
            )
            break

    if not found_capture and captured_pieces:
        capture_moves.append((path, captured_pieces))


def legal_moves(game_board, turn):
    simple_moves = []
    capture_moves = []
    if turn == "white":
        enemy_color = "black"
        own_color = "white"
        for index, piece in enumerate(game_board):
            row, column = board.index_to_row_column(index)
            if piece is None or piece.color != "white":
                continue

            if piece.kind == "king":
                add_king_simple_moves(index, row, column, game_board, simple_moves)
                if piece.has_sarac:
                    add_king_sarac_moves(index, row, column, game_board, simple_moves, own_color)
                if can_capture(piece):
                    find_king_capture_chains(game_board, index, row, column, piece, enemy_color,
                                             capture_moves, [index], [])
                    if piece.has_topuz:
                        find_king_topuz_capture_chains(game_board, index, row, column, piece, enemy_color,
                                                       capture_moves, [index], [])
                continue

            if (column,row) in board.LEFT_SIDE:
                add_move_if_legal(index, row, column, -1, 1, game_board, simple_moves)
                if piece.has_sarac:
                    add_sarac_move_if_legal(index, row, column, -1, 1, game_board, simple_moves, own_color)

            elif (column,row) in board.RIGHT_SIDE:
                add_move_if_legal(index, row, column, -1, -1, game_board, simple_moves)
                if piece.has_sarac:
                    add_sarac_move_if_legal(index, row, column, -1, -1, game_board, simple_moves, own_color)

            else:
                add_move_if_legal(index, row, column, -1, -1, game_board, simple_moves)
                add_move_if_legal(index, row, column, -1, 1, game_board, simple_moves)
                if piece.has_sarac:
                    add_sarac_move_if_legal(index, row, column, -1, -1, game_board, simple_moves, own_color)
                    add_sarac_move_if_legal(index, row, column, -1, 1, game_board, simple_moves, own_color)

            if can_capture(piece):
                find_capture_chains(game_board, index, row, column, piece, enemy_color, -1,
                                    capture_moves, [index], [])
                if piece.has_topuz:
                    find_topuz_capture_chains(game_board, index, row, column, piece, enemy_color, -1,
                                              capture_moves, [index], [])
    elif turn == "black":
        enemy_color = "white"
        own_color = "black"
        for index, piece in enumerate(game_board):
            row, column = board.index_to_row_column(index)
            if piece is None or piece.color != "black":
                continue

            if piece.kind == "king":
                add_king_simple_moves(index, row, column, game_board, simple_moves)
                if piece.has_sarac:
                    add_king_sarac_moves(index, row, column, game_board, simple_moves, own_color)
                if can_capture(piece):
                    find_king_capture_chains(game_board, index, row, column, piece, enemy_color,
                                             capture_moves, [index], [])
                    if piece.has_topuz:
                        find_king_topuz_capture_chains(game_board, index, row, column, piece, enemy_color,
                                                       capture_moves, [index], [])
                continue

            if (column,row) in board.LEFT_SIDE:
                add_move_if_legal(index, row, column, 1, 1, game_board, simple_moves)
                if piece.has_sarac:
                    add_sarac_move_if_legal(index, row, column, 1, 1, game_board, simple_moves, own_color)

            elif (column,row) in board.RIGHT_SIDE:
                add_move_if_legal(index, row, column, 1, -1, game_board, simple_moves)
                if piece.has_sarac:
                    add_sarac_move_if_legal(index, row, column, 1, -1, game_board, simple_moves, own_color)

            else:
                add_move_if_legal(index, row, column, 1, -1, game_board, simple_moves)
                add_move_if_legal(index, row, column, 1, 1, game_board, simple_moves)
                if piece.has_sarac:
                    add_sarac_move_if_legal(index, row, column, 1, -1, game_board, simple_moves, own_color)
                    add_sarac_move_if_legal(index, row, column, 1, 1, game_board, simple_moves, own_color)

            if can_capture(piece):
                find_capture_chains(game_board, index, row, column, piece, enemy_color, 1,
                                    capture_moves, [index], [])
                if piece.has_topuz:
                    find_topuz_capture_chains(game_board, index, row, column, piece, enemy_color, 1,
                                              capture_moves, [index], [])

    if capture_moves:
        simple_moves = []

    return simple_moves,capture_moves


def should_promote_move(piece, destination_index):
    row, column = board.index_to_row_column(destination_index)
    return (
        piece.kind == "pawn" and
        (
            piece.color == "white" and row == 0 or
            piece.color == "black" and row == 7
        )
    )


def promote_piece(piece, destination_index):
    if should_promote_move(piece, destination_index):
        piece.promote()

    return piece


def apply_simple_move(game_board, move):
    start_index, destination_index = move[0], move[-1]
    piece = game_board[start_index]
    was_promoted = should_promote_move(piece, destination_index)

    game_board[start_index] = None
    game_board[destination_index] = promote_piece(piece, destination_index)

    return was_promoted, destination_index


def apply_capture_move(game_board, capture_move):
    path, captured_pieces = capture_move
    start_index = path[0]
    destination_index = path[-1]

    piece = game_board[start_index]
    was_promoted = should_promote_move(piece, destination_index)

    game_board[start_index] = None

    for index in captured_pieces:
        remove_captured_piece(game_board, index)

    game_board[destination_index] = promote_piece(piece, destination_index)

    return was_promoted, destination_index


def choose_move(simple_moves, capture_moves):
    if capture_moves:
        available_moves = capture_moves
        print("Capture moves:")
        for index, capture_move in enumerate(capture_moves):
            print(f"{index}: {capture_move[0]}, {capture_move[1]}")
    elif simple_moves:
        available_moves = simple_moves
        print("Simple moves:")
        for index, simple_move in enumerate(simple_moves):
            print(f"{index}: {simple_move[0]}, {simple_move[1]}")
    else:
        return None

    while True:
        try:
            user_input = input("Unesite potez koji zelite ili 'u' za undo: ")
        except EOFError:
            return None

        if user_input == "u":
            return "undo"

        try:
            chosen_move = int(user_input)
        except ValueError:
            print("Unos mora biti broj.")
            continue

        if 0 <= chosen_move < len(available_moves):
            return available_moves[chosen_move]

        print("Ne postoji potez sa tim brojem.")
