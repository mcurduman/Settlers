from engine.game.commands.end_turn import EndTurnCommand
from engine.game.commands.place_road import PlaceRoadCommand
from engine.game.commands.place_settlement import PlaceSettlementCommand
from engine.game.commands.start_place_road_command import StartPlaceRoadCommand
from engine.game.commands.start_place_settlement_command import \
    StartPlaceSettlementCommand
from engine.game.commands.start_trade_with_bank_command import \
    StartTradeWithBankCommand
from engine.game.commands.trade_with_bank import TradeWithBankCommand
from engine.game.states.game_state import GameState
from engine.game.states.state_factory import get_state
from engine.utils.exceptions.invalid_command_exception import \
    InvalidCommandException


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
            game.set_state(get_state("PlayingRollState"))
        elif isinstance(command, StartPlaceRoadCommand):
            return game.set_state(get_state("PlayingPlaceRoadState"))
        elif isinstance(command, StartPlaceSettlementCommand):
            return game.set_state(get_state("PlayingPlaceSettlementState"))
        elif isinstance(command, StartTradeWithBankCommand):
            return game.set_state(get_state("PlayingTradeWithBankState"))
        else:
            raise InvalidCommandException("Command not allowed in PlayingMainState.")
