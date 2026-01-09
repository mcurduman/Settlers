import json
from datetime import datetime

from engine.game.board import Board
from engine.game.commands.command_factory import CommandFactory
from engine.game.game import Game
from engine.game.players.ai_player import AIPlayer
from engine.game.players.human_player import HumanPlayer
from engine.services.ai_action_describer import describe_ai_action
from engine.utils.exceptions.game_not_started_exception import \
    GameNotStartedException


class GameService:
    """
    Orchestrates game creation and command execution.
    """

    def __init__(self):
        """
        Initializes the GameService instance.
        """
        self._game: Game | None = None

    def start_game(self):
        """
        Initializes a new game.
        """
        human = HumanPlayer(name="Human")
        ai = AIPlayer(name="AI")
        board = Board()
        self._game = Game(players=[human, ai], board=board)

    def end_game(self):
        """
        Ends the current game and saves scores as JSON with date.
        """
        if self._game:
            scores = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "players": [
                    {"name": p.name, "victory_points": p.victory_points}
                    for p in self._game.players
                ],
            }
            try:
                with open("scores.json", "r") as f:
                    all_scores = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_scores = []
            all_scores.append(scores)
            with open("scores.json", "w") as f:
                json.dump(all_scores, f, indent=2)
        self._game = None
        return {"message": "Game ended successfully."}

    def execute_command_by_name(self, command_name: str, **kwargs):
        """
        Executes a command by its name.
        """
        self._ensure_game_started()

        command = CommandFactory.create(command_name, game=self._game, **kwargs)
        print(
            f"Executing command: {command_name} with args {kwargs} for player {self._game.current_player().name}"
        )
        player = self._game.current_player()
        import traceback

        try:
            self._game.execute_command(command, player)
        except Exception as e:
            print(f"Error executing command '{command_name}': {e}")
            traceback.print_exc()
            self._game.error = str(e)

    def execute_ai_command(self, command_name: str, **kwargs):
        """
        Executes a command on behalf of the AI player.
        """
        self.execute_command_by_name(command_name, **kwargs)

    def _ensure_game_started(self):
        """
        Ensures a game is currently started.
        """
        if not self._game:
            raise GameNotStartedException(
                "No game in progress. Please start a new game."
            )

    def get_state(self):
        """
        Returns the current game state.
        """
        self._ensure_game_started()
        return self._game.get_state()

    def handle_ai_turn(self):
        """
        Handles the AI player's turn.
        """

        player = self._game.current_player()
        if not player.is_ai():
            print("Current player is not AI. Skipping AI turn.")
            return

        action = self._game.handle_ai_strategy(player)
        if action:
            self.execute_ai_command(action["command"], **action["kwargs"])
            self._game.ai_action_description = describe_ai_action(
                self._game, action["command"], action["kwargs"]
            )
        else:
            print("No action returned by AI strategy.")
