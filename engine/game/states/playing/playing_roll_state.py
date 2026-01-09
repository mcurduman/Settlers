from engine.game.commands.roll_dice import RollDiceCommand
from engine.game.states.game_state import GameState
from engine.game.states.state_factory import get_state
from engine.utils.exceptions.invalid_command_exception import \
    InvalidCommandException


class PlayingRollState(GameState):
    def execute(self, command, game, player):
        if isinstance(command, RollDiceCommand):
            command.execute(game, player)
            game.set_state(get_state("PlayingMainState"))
        else:
            raise InvalidCommandException("Command not allowed in PlayingRollState.")
