import board
import game_state
import moves
import relic


if __name__ == '__main__':
    current_game = game_state.GameState([None] * 32)
    undo_stack = []
    skip_relic_add = False
    board.starting_board(current_game.board)

    while True:
        winner = current_game.get_winner()
        if winner is not None:
            print(f"Pobednik: {winner}")
            break

        if skip_relic_add:
            skip_relic_add = False
        else:
            new_relic = current_game.add_relic_for_turn()
            print(f"Nova relikvija na Carevom drumu: {new_relic}")

        board.print_board(current_game.board)
        simple_moves, capture_moves = moves.legal_moves(current_game.board, current_game.turn)
        if not simple_moves and not capture_moves:
            print(f"Nema legalnih poteza. Pobednik: {current_game.opponent_color()}")
            break

        selected_move = moves.choose_move(simple_moves, capture_moves)
        if selected_move is None:
            print("Igra je prekinuta.")
            break

        if selected_move == "undo":
            if undo_stack:
                current_game = undo_stack.pop()
                print("Potez je ponisten.")
            else:
                print("Nema poteza za undo.")
            skip_relic_add = True
            continue

        undo_stack.append(current_game.copy())

        if capture_moves:
            was_promoted, destination_index = moves.apply_capture_move(current_game.board, selected_move)
            current_game.draw_counter = 0
        elif simple_moves:
            was_promoted, destination_index = moves.apply_simple_move(current_game.board, selected_move)
            if was_promoted:
                current_game.draw_counter = 0
            else:
                current_game.draw_counter += 1

        destination_row, destination_column = board.index_to_row_column(destination_index)
        if (destination_row, destination_column) in board.BRAZDE:
            relic_side = relic.choose_relic_side(current_game.relic_road)
            if relic_side is None:
                print("Aktivacija relikvije je prekinuta.")
                break

            selected_relic = current_game.take_relic(relic_side)
            relic.apply_relic(current_game.board, destination_index, selected_relic)
            print(f"Aktivirana relikvija: {selected_relic}")

        if current_game.is_draw():
            print("Remi - 40 poteza bez promocije i jedenja.")
            break

        current_game.reduce_hesitation_for_current_player()
        current_game.switch_turn()
