from typing import Tuple
from engine.game.commands.command import Command


class PlaceSettlementCommand(Command):
    def __init__(self, node_position: Tuple[float, float]):
        self.node_position = tuple(node_position)

    def execute(self, game, player):
        game.handle_place_settlement(player, self.node_position)
