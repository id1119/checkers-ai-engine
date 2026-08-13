# Checkers AI Engine — Junački Megdan

A Python strategy-game engine built on top of checkers, combining adversarial search, state-space optimization and deterministic custom mechanics inspired by Serbian epic tradition.

The project is more than a standard checkers implementation: the AI searches game trees under a move-time budget while the game introduces a rotating relic system that changes movement, capture and promotion behavior.

## Highlights

- **Minimax** adversarial search
- **Alpha-beta pruning** for reducing the explored game tree
- **Iterative deepening** under a per-move time budget
- **Transposition table** for caching previously evaluated positions
- **Zobrist hashing** for efficient game-state identification
- Custom heuristic evaluation
- Mandatory captures and multi-jump move generation
- Undo support with stored `GameState` snapshots
- N-ary move-history tree with full branch replay
- Human vs. human and human vs. AI modes
- Deterministic relic mechanics integrated into AI simulation

## AI search

The AI uses iterative deepening on top of alpha-beta search. It repeatedly searches deeper levels while a monotonic deadline is still available, preserving the best move from the deepest completed search.

```text
Iterative Deepening
        │
        ▼
Alpha-Beta Search
        │
        ├── Heuristic Evaluation
        ├── Zobrist Hash
        └── Transposition Table
```

The engine also models relic decisions during search, so the AI evaluates both the board move and the possible relic choice when a move ends on a relic-activation square.

## Game model

The board is represented as a one-dimensional array containing the 32 playable squares of an 8×8 checkers board.

Core rules include:

- diagonal piece movement
- mandatory captures
- complete multi-capture sequences
- promotion to king
- draw detection after 40 consecutive moves without a capture or promotion

## Custom relic system

The game includes **Carev drum**, a deque with capacity for five deterministic relics. A new relic enters the front of the deque each turn.

Landing on one of the special **Brazde** squares allows a player to activate either the front or rear relic.

Implemented relics include:

- **Toka od čelika** — temporary armor against capture
- **Mešina rujnog vina** — applies hesitation to the nearest opponent
- **Topuz** — enables a special direct capture mechanic
- **Šarac** — enables a special positioning jump
- **Tri tovara blaga** — immediately promotes a piece

Relic state is part of the simulated position, which means the AI must account for these mechanics during search rather than treating them as post-move effects.

## State and history architecture

Several data structures are used for different parts of the engine:

```text
32-element array      board representation
stack                 undo snapshots
n-ary tree            complete move / undo history
bounded deque         Carev drum relic system
hash table            transposition cache
Zobrist hash          compact state identification
```

The history tree preserves branches created by undo operations and can replay the complete decision history after the game.

## Project structure

```text
main.py          Game loop, modes, undo and replay integration
ai.py            Minimax, alpha-beta and iterative deepening
heuristic.py     Position evaluation
zobrist.py       Zobrist state hashing
board.py         Board representation and rendering
moves.py         Move generation and capture rules
game_state.py    Complete mutable game state
piece.py         Piece state and promotion logic
relic.py         Carev drum and relic mechanics
history.py       N-ary history tree and replay
```

## Running

Requires Python 3.

```bash
python3 main.py
```

Choose between:

```text
1. Human vs. Human
2. Human vs. AI
```

During a human turn, the game also supports undoing previous moves. In human-vs-AI mode, undo rolls back both the player's move and the AI response when possible.

## What this project demonstrates

- adversarial search and game-tree exploration
- pruning and time-bounded search
- state hashing and memoization
- non-trivial move generation
- practical use of stacks, deques, trees and hash tables
- integrating custom game mechanics into an AI search space

## Status

Complete academic algorithms-and-data-structures project maintained as a portfolio implementation of game AI, search optimization and state modeling.
