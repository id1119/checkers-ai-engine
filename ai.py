import time

import board
import heuristic
import moves
import relic


RELIC_SIDES = ("front", "rear")
DEFAULT_MOVE_TIME_LIMIT = 3


def choose_best_move(current_game):
    next_states = generate_next_states(current_game)

    if not next_states:
        return None, None

    best_move = None
    best_relic_side = None
    best_score = float("-inf")

    for next_game, selected_move, relic_side in next_states:
        score = heuristic.evaluate_game_state(next_game, current_game.turn)

        if score > best_score:
            best_score = score
            best_move = selected_move
            best_relic_side = relic_side

    return best_move, best_relic_side


def choose_minimax_move(current_game, depth=3):
    next_states = generate_next_states(current_game)

    if not next_states:
        return None, None

    player_color = current_game.turn
    best_move = None
    best_relic_side = None
    best_score = float("-inf")

    for next_game, selected_move, relic_side in next_states:
        score = minimax(next_game, depth - 1, player_color)

        if score > best_score:
            best_score = score
            best_move = selected_move
            best_relic_side = relic_side

    return best_move, best_relic_side


def choose_alpha_beta_move(current_game, depth=3):
    next_states = generate_next_states(current_game)

    if not next_states:
        return None, None

    player_color = current_game.turn
    best_move = None
    best_relic_side = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for next_game, selected_move, relic_side in next_states:
        score = alpha_beta(next_game, depth - 1, player_color, alpha, beta)

        if score > best_score:
            best_score = score
            best_move = selected_move
            best_relic_side = relic_side

        alpha = max(alpha, best_score)

    return best_move, best_relic_side


def choose_iterative_deepening_move(current_game, time_limit=DEFAULT_MOVE_TIME_LIMIT):
    deadline = time.monotonic() + time_limit
    depth = 1
    best_move = None
    best_relic_side = None

    while time.monotonic() < deadline:
        move, relic_side, completed = choose_alpha_beta_move_with_deadline(
            current_game,
            depth,
            deadline,
        )

        if not completed:
            break

        if move is not None:
            best_move = move
            best_relic_side = relic_side

        depth += 1

    return best_move, best_relic_side


def choose_alpha_beta_move_with_deadline(current_game, depth, deadline):
    next_states = generate_next_states(current_game)

    if not next_states:
        return None, None, True

    player_color = current_game.turn
    best_move = None
    best_relic_side = None
    best_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for next_game, selected_move, relic_side in next_states:
        if time.monotonic() >= deadline:
            return best_move, best_relic_side, False

        score, completed = alpha_beta_with_deadline(
            next_game,
            depth - 1,
            player_color,
            alpha,
            beta,
            deadline,
        )

        if not completed:
            return best_move, best_relic_side, False

        if score > best_score:
            best_score = score
            best_move = selected_move
            best_relic_side = relic_side

        alpha = max(alpha, best_score)

    return best_move, best_relic_side, True


def minimax(current_game, depth, player_color):
    if current_game.is_draw():
        return 0

    winner = current_game.get_winner()
    if winner == player_color:
        return heuristic.TERMINAL_WIN_VALUE
    if winner is not None:
        return -heuristic.TERMINAL_WIN_VALUE

    if depth == 0:
        return heuristic.evaluate_game_state(current_game, player_color)

    next_states = generate_next_states(current_game)
    if not next_states:
        if current_game.turn == player_color:
            return -heuristic.TERMINAL_WIN_VALUE
        return heuristic.TERMINAL_WIN_VALUE

    if current_game.turn == player_color:
        best_score = float("-inf")

        for next_game, selected_move, relic_side in next_states:
            score = minimax(next_game, depth - 1, player_color)
            best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for next_game, selected_move, relic_side in next_states:
        score = minimax(next_game, depth - 1, player_color)
        best_score = min(best_score, score)

    return best_score


def alpha_beta(current_game, depth, player_color, alpha, beta):
    if current_game.is_draw():
        return 0

    winner = current_game.get_winner()
    if winner == player_color:
        return heuristic.TERMINAL_WIN_VALUE
    if winner is not None:
        return -heuristic.TERMINAL_WIN_VALUE

    if depth == 0:
        return heuristic.evaluate_game_state(current_game, player_color)

    next_states = generate_next_states(current_game)
    if not next_states:
        if current_game.turn == player_color:
            return -heuristic.TERMINAL_WIN_VALUE
        return heuristic.TERMINAL_WIN_VALUE

    if current_game.turn == player_color:
        best_score = float("-inf")

        for next_game, selected_move, relic_side in next_states:
            score = alpha_beta(next_game, depth - 1, player_color, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    best_score = float("inf")

    for next_game, selected_move, relic_side in next_states:
        score = alpha_beta(next_game, depth - 1, player_color, alpha, beta)
        best_score = min(best_score, score)
        beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score


def alpha_beta_with_deadline(current_game, depth, player_color, alpha, beta, deadline):
    if time.monotonic() >= deadline:
        return 0, False

    if current_game.is_draw():
        return 0, True

    winner = current_game.get_winner()
    if winner == player_color:
        return heuristic.TERMINAL_WIN_VALUE, True
    if winner is not None:
        return -heuristic.TERMINAL_WIN_VALUE, True

    if depth == 0:
        return heuristic.evaluate_game_state(current_game, player_color), True

    next_states = generate_next_states(current_game)
    if not next_states:
        if current_game.turn == player_color:
            return -heuristic.TERMINAL_WIN_VALUE, True
        return heuristic.TERMINAL_WIN_VALUE, True

    if current_game.turn == player_color:
        best_score = float("-inf")

        for next_game, selected_move, relic_side in next_states:
            score, completed = alpha_beta_with_deadline(
                next_game,
                depth - 1,
                player_color,
                alpha,
                beta,
                deadline,
            )

            if not completed:
                return best_score, False

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score, True

    best_score = float("inf")

    for next_game, selected_move, relic_side in next_states:
        score, completed = alpha_beta_with_deadline(
            next_game,
            depth - 1,
            player_color,
            alpha,
            beta,
            deadline,
        )

        if not completed:
            return best_score, False

        best_score = min(best_score, score)
        beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score, True


def generate_next_states(current_game):
    available_moves, is_capture_move = get_available_moves(current_game.board, current_game.turn)
    next_states = []

    for selected_move in available_moves:
        possible_outcomes = simulate_move_outcomes(current_game, selected_move, is_capture_move)

        for simulated_game, relic_side in possible_outcomes:
            simulated_game.reduce_hesitation_for_current_player()
            simulated_game.switch_turn()
            next_states.append((simulated_game, selected_move, relic_side))

    return next_states


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
