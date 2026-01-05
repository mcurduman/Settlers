from app.game.states.game_state import GameState
from app.game.states.state_factory import get_state
from app.game.commands.place_road import PlaceRoadCommand
from app.utils.exceptions.setup_exception import SetupException


class SetupPlaceRoadState(GameState):
    def execute(self, command, game, player):
        expected = game.setup_order[game.setup_index]

        if player != expected:
            raise SetupException("Not your turn.")

        if not isinstance(command, PlaceRoadCommand):
            raise SetupException("You must place a road.")

        command.execute(game, player)

        game.setup_index += 1

        if game.setup_index >= len(game.setup_order):
            game.set_state(get_state("PlayingState"))
        else:
            game.set_state(get_state("SetupPlaceSettlementState"))
