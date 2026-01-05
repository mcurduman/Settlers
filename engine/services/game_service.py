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
        self.game.execute_command(command, player)
        return self.get_state()

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

    def _state_specific_extra(self):
        self._ensure_game_started()
        extra = {}
        if self.game.state.__class__.__name__ == "SetupRollState":
            extra["rolls"] = {
                player.name: roll for player, roll in self.game.state.rolls.items()
            }
        elif self.game.state.__class__.__name__ == "SetupPlaceSettlementState":
            extra["setup_phase"] = "placing settlements"
        return extra

    # State retrieval
    def get_state(self, extra: dict | None = None):
        """
        Returns a serializable snapshot of the game.
        """
        print("Getting game state...")
        print(f"Game: {self.game.state.__class__.__name__ if self.game else 'None'}")
        if self.game is None:
            raise StateNotFoundException("Game has not been started")
        state = {
            "state": self.game.state.__class__.__name__,
            "board": {
                "tiles": [tile.model_dump() for tile in self.game.board.tiles],
                "nodes": [node.model_dump() for node in self.game.board.nodes.values()],
                "edges": [edge.model_dump() for edge in self.game.board.edges.values()],
            },
            "players": [
                {
                    "name": p.name,
                    "victory_points": p.victory_points,
                    "resources": {r.value: v for r, v in p.resources.items()},
                    "settlements": list(p.settlements),
                    "roads": list(p.roads),
                    "longest_road": self.game.board.longest_road(p),
                    "last_dice_roll": p.last_dice_roll,
                }
                for p in self.game.players
            ],
            "current_player": self.game.current_player().name,
        }

        state_specific = self._state_specific_extra()
        state.update(state_specific)
        if extra:
            state.update(extra)

        return state

    # Helpers
    def _human_player(self) -> Player:
        return self.game.players[0]

    def _ensure_game_started(self):
        if self.game is None:
            raise RuntimeError("Game has not been started")
