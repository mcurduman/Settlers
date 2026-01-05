from app.game.game import Game
from app.game.board import Board
from app.game.players.player import Player
from app.game.states.setup_state import SetupState
from app.game.states.playing_state import PlayingState

from app.game.commands.roll_dice import RollDiceCommand
from app.game.commands.trade_with_bank import TradeWithBankCommand
from app.game.commands.place_settlement import PlaceSettlementCommand

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

        # Initial state
        self.game.set_state(SetupState())

        return self.get_state()

    # Commands
    def roll_dice(self):
        self._ensure_game_started()

        command = RollDiceCommand()
        player = self._human_player()

        result = self.game.execute_command(command, player)
        return self.get_state(extra={"dice": result})

    def trade_with_bank(self, give: str, receive: str):
        self._ensure_game_started()

        command = TradeWithBankCommand(
            give=ResourceType(give),
            receive=ResourceType(receive),
        )

        player = self._human_player()
        self.game.execute_command(command, player)

        return self.get_state()

    def place_settlement(self, position: int):
        self._ensure_game_started()

        command = PlaceSettlementCommand(position=position)
        player = self._human_player()

        self.game.execute_command(command, player)
        return self.get_state()

    # State retrieval
    def get_state(self, extra: dict | None = None):
        """
        Returns a serializable snapshot of the game.
        """
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
