from engine.game.commands.place_settlement import PlaceSettlementCommand
from engine.game.states.game_state import GameState
from engine.game.states.state_factory import get_state
from engine.utils.exceptions.invalid_command_exception import \
    InvalidCommandException
from engine.utils.exceptions.setup_exception import SetupException


class SetupPlaceSettlementState(GameState):
    def execute(self, command, game, player):
        expected = game.setup_order[game.setup_index]

        if player != expected:
            raise SetupException("Not your turn.")

        if not isinstance(command, PlaceSettlementCommand):
            raise InvalidCommandException(
                "In SetupPlaceSettlementState, you must place a settlement."
            )

        command.execute(game, player)
        game.set_state(get_state("SetupPlaceRoadState"))
