import board
import game_state
import moves


if __name__ == '__main__':
    current_game = game_state.GameState([None] * 32)
    board.starting_board(current_game.board)

    while True:
        board.print_board(current_game.board)
        simple_moves, capture_moves = moves.legal_moves(current_game.board, current_game.turn)
        if not simple_moves and not capture_moves:
            print("Nema legalnih poteza")
            break

        selected_move = moves.choose_move(simple_moves, capture_moves)
        if selected_move is None:
            print("Igra je prekinuta.")
            break

        if capture_moves:
            moves.apply_capture_move(current_game.board, selected_move)
            current_game.draw_counter = 0
        elif simple_moves:
            was_promoted = moves.apply_simple_move(current_game.board, selected_move)
            if was_promoted:
                current_game.draw_counter = 0
            else:
                current_game.draw_counter += 1

        if current_game.is_draw():
            print("Remi - 40 poteza bez promocije i jedenja.")
            break

        current_game.switch_turn()
