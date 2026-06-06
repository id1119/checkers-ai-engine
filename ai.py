import board
import heuristic
import moves
import relic


RELIC_SIDES = ("front", "rear")


def choose_best_move(current_game):
    available_moves, is_capture_move = get_available_moves(current_game.board, current_game.turn)

    if not available_moves:
        return None, None

    best_move = None
    best_relic_side = None
    best_score = float("-inf")

    for selected_move in available_moves:
        possible_outcomes = simulate_move_outcomes(current_game, selected_move, is_capture_move)

        for simulated_game, relic_side in possible_outcomes:
            score = heuristic.evaluate_game_state(simulated_game, current_game.turn)

            if score > best_score:
                best_score = score
                best_move = selected_move
                best_relic_side = relic_side

    return best_move, best_relic_side


def get_available_moves(game_board, turn):
    simple_moves, capture_moves = moves.legal_moves(game_board, turn)

    if capture_moves:
        return capture_moves, True
    return simple_moves, False


def simulate_move_outcomes(current_game, selected_move, is_capture_move):
    simulated_game = current_game.copy()
    was_promoted, destination_index = apply_move_on_simulation(
        simulated_game,
        selected_move,
        is_capture_move,
    )

    if is_capture_move or was_promoted:
        simulated_game.draw_counter = 0
    else:
        simulated_game.draw_counter += 1

    destination_row, destination_column = board.index_to_row_column(destination_index)
    if (destination_row, destination_column) not in board.BRAZDE:
        return [(simulated_game, None)]

    return simulate_relic_choices(simulated_game, destination_index)


def apply_move_on_simulation(simulated_game, selected_move, is_capture_move):
    if is_capture_move:
        return moves.apply_capture_move(simulated_game.board, selected_move)
    return moves.apply_simple_move(simulated_game.board, selected_move)


def simulate_relic_choices(simulated_game, destination_index):
    if not simulated_game.relic_road:
        return [(simulated_game, None)]

    outcomes = []

    for relic_side in RELIC_SIDES:
        relic_game = simulated_game.copy()
        selected_relic = relic_game.take_relic(relic_side)

        if selected_relic is None:
            continue

        relic.apply_relic(relic_game.board, destination_index, selected_relic)
        outcomes.append((relic_game, relic_side))

    return outcomes
