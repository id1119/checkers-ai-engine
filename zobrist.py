import random


RANDOM_SEED = 20260607
MAX_COUNTER_VALUE = 40
RANDOM_GENERATOR = random.Random(RANDOM_SEED)
ZOBRIST_KEYS = {}


def get_zobrist_key(token):
    if token not in ZOBRIST_KEYS:
        ZOBRIST_KEYS[token] = RANDOM_GENERATOR.getrandbits(64)
    return ZOBRIST_KEYS[token]


def hash_game_state(current_game):
    position_hash = 0

    for index, piece in enumerate(current_game.board):
        if piece is None:
            continue

        position_hash ^= get_zobrist_key((
            "piece",
            index,
            piece.color,
            piece.kind,
            piece.armor_turns,
            piece.hesitation_turns,
            piece.has_topuz,
            piece.has_sarac,
            piece.has_blessing,
            piece.has_wine,
        ))

    position_hash ^= get_zobrist_key(("turn", current_game.turn))
    position_hash ^= get_zobrist_key(("draw_counter", min(current_game.draw_counter, MAX_COUNTER_VALUE)))
    position_hash ^= get_zobrist_key(("relic_cycle_index", current_game.relic_cycle_index))

    for index, selected_relic in enumerate(current_game.relic_road):
        position_hash ^= get_zobrist_key(("relic_road", index, selected_relic))

    return position_hash
