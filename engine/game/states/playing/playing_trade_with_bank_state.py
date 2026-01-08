from engine.game.states.game_state import GameState
from engine.game.commands.trade_with_bank import TradeWithBankCommand
from engine.game.commands.exit_trade_with_bank_command import ExitTradeWithBankCommand
from engine.utils.exceptions.invalid_command_exception import InvalidCommandException
from engine.game.states.state_factory import get_state


class PlayingTradeWithBankState(GameState):
    def execute(self, command, game, player):
        if isinstance(command, TradeWithBankCommand):
            command.execute(game, player)
            game.set_state(get_state("PlayingMainState"))
        elif isinstance(command, ExitTradeWithBankCommand):
            game.set_state(get_state("PlayingMainState"))
        else:
            raise InvalidCommandException(
                "Command not allowed in PlayingTradeWithBankState."
            )
