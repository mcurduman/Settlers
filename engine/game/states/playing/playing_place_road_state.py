from engine.game.states.game_state import GameState
from engine.game.commands.place_road import PlaceRoadCommand
from engine.game.commands.exit_place_road_command import ExitPlaceRoadCommand
from engine.utils.exceptions.invalid_command_exception import InvalidCommandException
from engine.game.states.state_factory import get_state


class PlayingPlaceRoadState(GameState):
    def execute(self, command, game, player):
        if isinstance(command, PlaceRoadCommand):
            command.execute(game, player)
            if game.check_if_won():
                game.set_state(get_state("FinishedState"))
            else:
                game.set_state(get_state("PlayingMainState"))
        elif isinstance(command, ExitPlaceRoadCommand):
            game.set_state(get_state("PlayingMainState"))
        else:
            raise InvalidCommandException(
                "Command not allowed in PlayingPlaceRoadState."
            )
