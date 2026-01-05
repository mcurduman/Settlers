from app.game.commands.command import Command


class PlaceSettlementCommand(Command):
    def __init__(self, position: int):
        self.position = position

    def execute(self, game, player):
        game.handle_place_settlement(player, self.position)
