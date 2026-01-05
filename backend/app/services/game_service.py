from typing import Tuple
from app.game.game import Game
from app.game.board import Board
from app.game.players.player import Player
from app.game.commands.roll_dice import RollDiceCommand
from app.game.commands.place_road import PlaceRoadCommand
from app.game.commands.trade_with_bank import TradeWithBankCommand
from app.game.commands.place_settlement import PlaceSettlementCommand
from app.utils.exceptions.state_not_found_exception import StateNotFoundException
from app.game.entities.resource_type import ResourceType


class GameService:
    """
    Orchestrates game creation and command execution.
    """

    def __init__(self):
        self.game: Game | None = None

    # Game lifecycle
    def start_game(self, difficulty: str):
        """
        Initializes a new game.
        """
        # Create players (for now: 1 human + 1 AI placeholder)
        human = Player(name="Human")
        ai = Player(name="AI")

        board = Board()
        self.game = Game(players=[human, ai], board=board)

        return self.get_state()

    def end_game(self):
        """
        Ends the current game.
        """
        self.game = None
        return {"message": "Game ended successfully."}

    def end_turn(self):
        """
        Ends the current player's turn.
        """
        self._ensure_game_started()

        next_player = self.game.next_player()

        return self.get_state(extra={"current_player": next_player.name})

    # Commands
    def roll_dice(self):
        self._ensure_game_started()

        command = RollDiceCommand()
        player = self.game.current_player()
        result = self.game.execute_command(command, player)
        return self.get_state(
            extra={"current_player": player.name, "dice_value": result}
        )

    def trade_with_bank(self, give: str, receive: str):
        self._ensure_game_started()

        command = TradeWithBankCommand(
            give=ResourceType(give),
            receive=ResourceType(receive),
        )

        player = self._human_player()
        self.game.execute_command(command, player)

        return self.get_state()

    def place_settlement(self, position: Tuple[float, float]):
        self._ensure_game_started()

        command = PlaceSettlementCommand(position=position)
        player = self.game.current_player()
        self.game.execute_command(command, player)
        return self.get_state()

    def place_road(self, a: tuple, b: tuple):
        command = PlaceRoadCommand(a, b)
        player = self._human_player()
        self.game.execute_command(command, player)
        return self.get_state()

    # State retrieval
    def get_state(self, extra: dict | None = None):
        """
        Returns a serializable snapshot of the game.
        """
        if self.game is None:
            raise StateNotFoundException("Game has not been started")
        state = {
            "state": self.game.state.__class__.__name__,
            "board": [tile.model_dump() for tile in self.game.board.tiles],
            "players": [
                {
                    "name": p.name,
                    "victory_points": p.victory_points,
                    "resources": {r.value: v for r, v in p.resources.items()},
                }
                for p in self.game.players
            ],
        }

        if extra:
            state.update(extra)

        return state

    # Helpers
    def _human_player(self) -> Player:
        return self.game.players[0]

    def _ensure_game_started(self):
        if self.game is None:
            raise RuntimeError("Game has not been started")
