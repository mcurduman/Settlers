from engine.game.commands.roll_dice import RollDiceCommand
from engine.game.commands.place_road import PlaceRoadCommand
from engine.game.commands.end_turn import EndTurnCommand
from engine.game.commands.trade_with_bank import TradeWithBankCommand
from engine.game.commands.start_trade_with_bank_command import StartTradeWithBankCommand
from engine.game.commands.exit_trade_with_bank_command import ExitTradeWithBankCommand
from engine.game.commands.place_settlement import PlaceSettlementCommand
from engine.game.commands.start_place_settlement_command import (
    StartPlaceSettlementCommand,
)
from engine.game.commands.exit_place_settlement_command import (
    ExitPlaceSettlementCommand,
)
from engine.game.commands.start_place_road_command import StartPlaceRoadCommand
from engine.game.commands.exit_place_road_command import ExitPlaceRoadCommand
from engine.game.entities.resource_type import ResourceType


class CommandFactory:
    @staticmethod
    def create(command_name, **kwargs):

        mapping = {
            "roll_dice": lambda: RollDiceCommand(),
            "place_road": lambda: PlaceRoadCommand(kwargs["a"], kwargs["b"]),
            "end_turn": lambda: EndTurnCommand(game=kwargs["game"]),
            "trade_with_bank": lambda: TradeWithBankCommand(
                give=ResourceType(kwargs["give"]),
                receive=ResourceType(kwargs["receive"]),
                rate=kwargs.get("rate", 3),
            ),
            "start_trade_with_bank": lambda: StartTradeWithBankCommand(),
            "exit_trade_with_bank": lambda: ExitTradeWithBankCommand(),
            "place_settlement": lambda: PlaceSettlementCommand(kwargs["position"]),
            "start_place_settlement": lambda: StartPlaceSettlementCommand(),
            "exit_place_settlement": lambda: ExitPlaceSettlementCommand(),
            "start_place_road": lambda: StartPlaceRoadCommand(),
            "exit_place_road": lambda: ExitPlaceRoadCommand(),
        }
        if command_name not in mapping:
            raise ValueError(f"Unknown command: {command_name}")
        return mapping[command_name]()
