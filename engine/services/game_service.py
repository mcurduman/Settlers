import json
from datetime import datetime
from engine.game.game import Game
from engine.game.board import Board
from engine.game.players.player import Player
from engine.utils.exceptions.game_not_started_exception import GameNotStartedException


class GameService:
    """
    Orchestrates game creation and command execution.
    """

    def __init__(self):
        self._game: Game | None = None

    def start_game(self, difficulty: str):
        """
        Initializes a new game.
        """
        human = Player(name="Human")
        ai = Player(name="AI")
        board = Board()
        self._game = Game(players=[human, ai], board=board, difficulty=difficulty)

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

        :param self:
        :param command_name: Name of the command to execute.
        :type command_name: str
        :param kwargs: Additional arguments for the command.
        """
        self._ensure_game_started()
        from engine.game.commands.command_factory import CommandFactory

        command = CommandFactory.create(command_name, game=self._game, **kwargs)
        player = self._game.current_player()
        import traceback

        try:
            self._game.execute_command(command, player)
        except Exception as e:
            print(f"Error executing command '{command_name}': {e}")
            traceback.print_exc()
            self._game.error = str(e)

    def _ensure_game_started(self):
        if not self._game:
            raise GameNotStartedException(
                "No game in progress. Please start a new game."
            )

    def get_state(self):
        self._ensure_game_started()
        return self._game.get_state()
