# Settlers (Mini Catan) – Example with Design Patterns

## How to Run the Project

1. Install dependencies:
```sh
pip install -r requirements.txt
```

2. Start the game:
```sh
python -m client.main
```
or (on some systems)
```sh
py -m client.main
```

## Technical Requirements

- Python 3.9+
- Project is organized into modules and packages (e.g., `client/`, `engine/`)

## Functionality

This application is a mini Catan-style game with a graphical interface built using pygame. The player competes against an AI with adaptable difficulty and can place roads, build settlements, roll dice, trade with the bank, and end their turn.

## Design Patterns Used

### 1. Command Pattern
- Why: The game has many different actions triggered by the player or AI. To keep the code clear, each action is handled separately as its own object.
- Where:
  - `engine/game/commands/`
  - `engine/services/game_service.py`
- What it solves: Separates the logic of each action from the main game logic, making the code easier to read, test, and extend with new actions.

### 2. State Pattern
- Why: The game operates in different phases, and the rules are not the same in each phase. A clear way is needed to control what is allowed at any given time.
- Where:
  - `engine/game/states/`
- What it solves: Each state manages its own rules so users cannot call certain commands if the state doesnt permit it. Transitioning between phases is clear, and changes can be made without affecting the rest of the game.

### 3. Factory Pattern
- Why: Commands and states are created in multiple places. To avoid duplicate code, their creation is centralized.
- Where:
  - `engine/game/commands/command_factory.py`
  - `engine/game/states/state_factory.py`
- What it solves: Object creation is controlled from a single place. Adding new commands or states is quick and does not require major changes, also the introduction of the factories fixed issues regarding circular imports.

### 4. Strategy Pattern
- Why: The AI uses different strategies (easy, hard, adaptive) that can be swapped at runtime depending on the game situation or difficulty setting. This allows flexible and extensible AI behavior.
- Where:
  - `engine/game/strategies/`
  - `engine/game/players/ai_player.py`
- What it solves: Encapsulates different AI algorithms and makes it easy to add or change strategies without modifying the main game or player logic. For this mini-game I have chosen that when the user has less victory points the AI strategy will change to the easier one.

## Testing

To run all tests and check code coverage, use (49%):

```
pytest --cov=engine --cov=client --cov-report=term-missing
```

If you do not have pytest or pytest-cov installed, install them with:

```
py -m pip install pytest pytest-cov
```

All tests are located in the `tests/` directory. The test suite includes unit tests for engine, client, and all major modules, with extensive coverage for AI, input, rendering, and panel logic. Most tests use mocks for pygame and other dependencies, so you do not need pygame installed to run the tests.