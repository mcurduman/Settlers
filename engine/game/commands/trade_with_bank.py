from engine.game.commands.command import Command
from engine.game.entities.resource_type import ResourceType


class TradeWithBankCommand(Command):
    def __init__(self, give: ResourceType, receive: ResourceType, rate: int):
        self.rate = rate
        self.give = give
        self.receive = receive

    def execute(self, game, player):
        game.handle_trade_with_bank(player, self.give, self.receive, self.rate)
