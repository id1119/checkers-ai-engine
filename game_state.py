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

    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def is_draw(self):
        return self.draw_counter >= 40

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
