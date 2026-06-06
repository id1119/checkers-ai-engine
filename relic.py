from collections import deque

import board


TOKA = "Toka od celika"
VINO = "Mesina rujnog vina"
TOPUZ = "Topuz"
SARAC = "Sarac"
BLAGO = "Tri tovara blaga"

RELIC_CYCLE = [
    TOKA,
    VINO,
    TOPUZ,
    SARAC,
    BLAGO,
]

RELIC_ROAD_CAPACITY = 5


def create_relic_road():
    return deque(maxlen=RELIC_ROAD_CAPACITY)


def next_relic(cycle_index):
    new_relic = RELIC_CYCLE[cycle_index]
    next_index = (cycle_index + 1) % len(RELIC_CYCLE)
    return new_relic, next_index


def add_relic_to_front(relic_road, new_relic):
    relic_road.appendleft(new_relic)


def take_front_relic(relic_road):
    if not relic_road:
        return None
    return relic_road.popleft()


def take_rear_relic(relic_road):
    if not relic_road:
        return None
    return relic_road.pop()


def find_nearest_enemy_piece(game_board, source_index):
    source_piece = game_board[source_index]
    source_row, source_column = board.index_to_row_column(source_index)
    nearest_index = None
    nearest_distance = None

    for index, piece in enumerate(game_board):
        if piece is None or piece.color == source_piece.color:
            continue

        row, column = board.index_to_row_column(index)
        distance = abs(source_row - row) + abs(source_column - column)

        if nearest_distance is None or distance < nearest_distance:
            nearest_index = index
            nearest_distance = distance

    return nearest_index


def apply_relic(game_board, source_index, selected_relic):
    piece = game_board[source_index]

    if selected_relic == BLAGO:
        piece.has_blessing = True
        piece.promote()
    elif selected_relic == TOPUZ:
        piece.has_topuz = True
    elif selected_relic == SARAC:
        piece.has_sarac = True
    elif selected_relic == VINO:
        piece.has_wine = True
        enemy_index = find_nearest_enemy_piece(game_board, source_index)
        if enemy_index is not None and not game_board[enemy_index].is_marko():
            game_board[enemy_index].hesitation_turns = 2
    elif selected_relic == TOKA:
        if piece.is_marko():
            piece.armor_turns = 2
        else:
            piece.armor_turns = 1


def choose_relic_side(relic_road):
    if not relic_road:
        print("Carev drum je prazan.")
        return None

    print("Carev drum:")
    print(f"0: front - {relic_road[0]}")
    print(f"1: rear  - {relic_road[-1]}")

    while True:
        try:
            chosen_side = int(input("Izaberi relikviju koju zelis: "))
        except ValueError:
            print("Unos mora biti broj.")
            continue
        except EOFError:
            return None

        if chosen_side == 0:
            return "front"
        if chosen_side == 1:
            return "rear"

        print("Izaberi 0 za front ili 1 za rear.")
