from app.game.states.game_state import GameState
from app.game.states.state_factory import get_state
from app.game.commands.roll_dice import RollDiceCommand
from app.utils.exceptions.setup_exception import SetupException


class SetupRollState(GameState):
    def __init__(self):
        self.rolls = {}

    def execute(self, command, game, player):
        if not isinstance(command, RollDiceCommand):
            raise SetupException("You must roll dice first.")

        if game.current_player_index != game.players.index(player):
            raise SetupException("Not your turn to roll.")

        if player in self.rolls:
            raise SetupException("Player already rolled.")

        value = command.execute(game, player)
        self.rolls[player] = value

        if len(self.rolls) == len(game.players):
            # decide order
            game.setup_order = sorted(
                game.players, key=lambda p: self.rolls[p], reverse=True
            )
            game.setup_index = 0
            game.set_state(get_state("SetupPlaceSettlementState"))

        return value
