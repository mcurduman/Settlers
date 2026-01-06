from engine.game.states.game_state import GameState
from engine.game.states.state_factory import get_state
from engine.game.commands.place_road import PlaceRoadCommand
from engine.utils.exceptions.setup_exception import SetupException
from engine.utils.exceptions.invalid_command_exception import InvalidCommandException


class SetupPlaceRoadState(GameState):
    def execute(self, command, game, player):
        expected = game.setup_order[game.setup_index]

        if player != expected:
            raise SetupException("Not your turn.")

        if not isinstance(command, PlaceRoadCommand):
            raise InvalidCommandException(
                "In SetupPlaceRoadState, you must place a road."
            )

        command.execute(game, player)

        game.setup_index += 1
        game.next_player()

        if game.setup_index >= len(game.setup_order):
            game.set_state(get_state("PlayingRollState"))
        else:
            game.set_state(get_state("SetupPlaceSettlementState"))
