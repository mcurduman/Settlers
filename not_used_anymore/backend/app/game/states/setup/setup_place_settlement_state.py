from app.game.states.game_state import GameState
from app.game.states.state_factory import get_state
from app.game.commands.place_settlement import PlaceSettlementCommand
from app.utils.exceptions.setup_exception import SetupException


class SetupPlaceSettlementState(GameState):
    def execute(self, command, game, player):
        expected = game.setup_order[game.setup_index]

        if player != expected:
            raise SetupException("Not your turn.")

        if not isinstance(command, PlaceSettlementCommand):
            raise SetupException("You must place a settlement.")

        command.execute(game, player)
        game.set_state(get_state("SetupPlaceRoadState"))
