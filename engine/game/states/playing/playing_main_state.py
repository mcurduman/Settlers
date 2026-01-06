from engine.game.states.game_state import GameState
from engine.game.commands.end_turn import EndTurnCommand
from engine.game.commands.place_road import PlaceRoadCommand
from engine.game.commands.place_settlement import PlaceSettlementCommand
from engine.game.commands.trade_with_bank import TradeWithBankCommand
from engine.utils.exceptions.invalid_command_exception import InvalidCommandException


class PlayingMainState(GameState):
    def execute(self, command, game, player):
        if isinstance(command, PlaceRoadCommand):
            return command.execute(game, player)
        elif isinstance(command, PlaceSettlementCommand):
            return command.execute(game, player)
        elif isinstance(command, TradeWithBankCommand):
            return command.execute(game, player)
        elif isinstance(command, EndTurnCommand):
            command.execute()
            game.next_player()
            return
        else:
            raise InvalidCommandException("Command not allowed in PlayingMainState.")
