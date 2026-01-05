from app.game.states.game_state import GameState
from app.game.commands.roll_dice import RollDiceCommand


class PlayingState(GameState):
    def execute(self, command, game, player):
        if isinstance(command, RollDiceCommand):
            return command.execute(game, player)

        return command.execute(game, player)
