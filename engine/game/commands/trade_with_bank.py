from engine.game.commands.command import Command
from engine.game.entities.resource_type import ResourceType


class TradeWithBankCommand(Command):
    def __init__(self, give: ResourceType, receive: ResourceType):
        self.give = give
        self.receive = receive

    def execute(self, game, player):
        game.trade_with_bank(player, self.give, self.receive)
