# Checkers AI Engine

A Python implementation of a modified checkers game with an AI opponent, heuristic evaluation and optimized game-state search.

## Highlights

- Game-state representation and move generation
- AI decision logic with heuristic evaluation
- Zobrist hashing for efficient state identification
- Move/history tracking
- Modular separation between board, pieces, rules and AI logic

## Project structure

```text
main.py          # Application entry point
board.py         # Board representation
piece.py         # Piece model
moves.py         # Move generation and rules
ai.py            # AI decision logic
heuristic.py     # Position evaluation
zobrist.py       # Zobrist hashing
history.py       # Game history
relic.py         # Modified-game mechanics
game_state.py    # State representation
```

## Running

```bash
python3 main.py
```

## Tech stack

- Python
- Game-tree search concepts
- Heuristic evaluation
- State hashing

## Status

Academic/experimental AI project focused on game logic and search-oriented state evaluation.
