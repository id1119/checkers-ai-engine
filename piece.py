from dataclasses import dataclass


@dataclass
class Piece:
    color: str
    kind: str
    armor_turns: int = 0
    hesitation_turns: int = 0
    has_topuz: bool = False
    has_sarac: bool = False
    has_blessing: bool = False
    has_wine: bool = False

    def promote(self):
        self.kind = "king"

    def is_marko(self):
        return (
            self.kind == "king"
            and self.has_blessing
            and self.has_sarac
            and self.has_topuz
            and self.has_wine
        )
