import ai
import board
import game_state
import history
import moves
import relic


def get_move_destinations(simple_moves, capture_moves):
    if capture_moves:
        return {capture_move[0][-1] for capture_move in capture_moves}
    return {simple_move[-1] for simple_move in simple_moves}


def choose_game_mode():
    print("Izaberi mod igre:")
    print("1: Covek protiv coveka")
    print("2: Covek protiv AI")

    while True:
        try:
            selected_mode = int(input("Unesi mod igre: "))
        except ValueError:
            print("Unos mora biti broj.")
            continue
        except EOFError:
            return None

        if selected_mode == 1:
            return "human_vs_human"
        if selected_mode == 2:
            return "human_vs_ai"

        print("Izaberi 1 ili 2.")


if __name__ == '__main__':
    game_mode = choose_game_mode()
    if game_mode is None:
        print("Igra je prekinuta.")
        raise SystemExit

    current_game = game_state.GameState([None] * 32)
    undo_stack = []
    skip_relic_add = False
    board.starting_board(current_game.board)
    history_root = history.HistoryNode(current_game.copy())
    current_history_node = history_root

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

        simple_moves, capture_moves = moves.legal_moves(current_game.board, current_game.turn)
        highlighted_indexes = get_move_destinations(simple_moves, capture_moves)
        board.print_board(current_game.board, highlighted_indexes)
        if not simple_moves and not capture_moves:
            print(f"Nema legalnih poteza. Pobednik: {current_game.opponent_color()}")
            break

        is_ai_turn = game_mode == "human_vs_ai" and current_game.turn == "black"
        if is_ai_turn:
            selected_move, selected_relic_side = ai.choose_iterative_deepening_move(current_game)
            if selected_move is None:
                print("AI nema legalan potez.")
                break
            print(f"AI je odigrao potez: {selected_move}")
        else:
            selected_move = moves.choose_move(simple_moves, capture_moves)
            selected_relic_side = None
            if selected_move is None:
                print("Igra je prekinuta.")
                break

            if selected_move == "undo":
                undo_steps = 2 if game_mode == "human_vs_ai" else 1
                undone_steps = 0
                undo_from_history_node = current_history_node

                while undo_stack and undone_steps < undo_steps:
                    current_game = undo_stack.pop()
                    if current_history_node.parent is not None:
                        current_history_node = current_history_node.parent
                    undone_steps += 1

                if undone_steps == 0:
                    print("Nema poteza za undo.")
                elif undone_steps == 1:
                    print("Potez je ponisten.")
                else:
                    print("Potezi su ponisteni.")

                if undone_steps > 0:
                    undo_from_history_node.add_child(
                        current_game.copy(),
                        f"UNDO x{undone_steps}",
                    )

                skip_relic_add = True
                continue

        undo_stack.append(current_game.copy())
        piece_count_before_move = current_game.count_pieces()

        if capture_moves:
            was_promoted, destination_index = moves.apply_capture_move(current_game.board, selected_move)
        elif simple_moves:
            was_promoted, destination_index = moves.apply_simple_move(current_game.board, selected_move)

        piece_count_after_move = current_game.count_pieces()
        if was_promoted or piece_count_after_move != piece_count_before_move:
            current_game.draw_counter = 0
        else:
            current_game.draw_counter += 1

        selected_relic = None
        relic_side = None
        destination_row, destination_column = board.index_to_row_column(destination_index)
        if (destination_row, destination_column) in board.BRAZDE:
            if is_ai_turn:
                relic_side = selected_relic_side
                print(f"AI je izabrao relikviju sa strane: {relic_side}")
            else:
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
        current_game.reduce_armor_for_opponent_pieces()
        current_game.switch_turn()
        current_history_node = current_history_node.add_child(
            current_game.copy(),
            selected_move,
            relic_side,
            selected_relic,
        )

    if history.choose_replay_history():
        history.replay_history(history_root)
