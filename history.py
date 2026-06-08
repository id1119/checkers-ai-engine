import time

import board

from dataclasses import dataclass
from dataclasses import field


@dataclass
class HistoryNode:
    game_state: object
    move: object = None
    relic_side: object = None
    selected_relic: object = None
    parent: object = None
    children: list = field(default_factory=list)

    def add_child(self, game_state, move=None, relic_side=None, selected_relic=None):
        child = HistoryNode(
            game_state=game_state,
            move=move,
            relic_side=relic_side,
            selected_relic=selected_relic,
            parent=self,
        )
        self.children.append(child)
        return child


def replay_history(root, pause_seconds=1):
    print("Reprodukcija istorije poteza:")
    board.print_board(root.game_state.board)

    for child_index, child in enumerate(root.children, start=1):
        replay_branch(child, str(child_index), pause_seconds)


def replay_branch(node, branch_path, pause_seconds):
    time.sleep(pause_seconds)
    print(f"Grana {branch_path}")
    print(f"Potez: {node.move}")

    if node.selected_relic is not None:
        print(f"Relikvija: {node.selected_relic} ({node.relic_side})")

    board.print_board(node.game_state.board)

    for child_index, child in enumerate(node.children, start=1):
        replay_branch(child, f"{branch_path}.{child_index}", pause_seconds)


def choose_replay_history():
    while True:
        try:
            user_input = input("Da li zelis reprodukciju istorije? 1-da, 0-ne: ")
        except EOFError:
            return False

        if user_input == "1":
            return True
        if user_input == "0":
            return False

        print("Izaberi 1 ili 0.")
