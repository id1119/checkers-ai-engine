import copy

from dataclasses import dataclass
from dataclasses import field

import relic

@dataclass
class GameState:
    board: list
    turn: str = "white"
    draw_counter: int = 0
    relic_road: object = field(default_factory=relic.create_relic_road)
    relic_cycle_index: int = 0

    def opponent_color(self):
        return "black" if self.turn == "white" else "white"

    def switch_turn(self):
        self.turn = self.opponent_color()

    def get_winner(self):
        has_white_piece = any(piece is not None and piece.color == "white" for piece in self.board)
        has_black_piece = any(piece is not None and piece.color == "black" for piece in self.board)

        if not has_white_piece:
            return "black"
        if not has_black_piece:
            return "white"
        return None

    def is_draw(self):
        return self.draw_counter >= 40

    def count_pieces(self):
        return sum(piece is not None for piece in self.board)

    def reduce_armor_for_opponent_pieces(self):
        for piece in self.board:
            if piece is not None and piece.color != self.turn and piece.armor_turns > 0:
                piece.armor_turns -= 1

    def add_relic_for_turn(self):
        new_relic, self.relic_cycle_index = relic.next_relic(self.relic_cycle_index)
        relic.add_relic_to_front(self.relic_road, new_relic)
        return new_relic

    def take_relic(self, side):
        if side == "front":
            return relic.take_front_relic(self.relic_road)
        elif side == "rear":
            return relic.take_rear_relic(self.relic_road)
        return None

    def reduce_hesitation_for_current_player(self):
        for piece in self.board:
            if piece is not None and piece.color == self.turn and piece.hesitation_turns > 0:
                piece.hesitation_turns -= 1

    def copy(self):
        return copy.deepcopy(self)
