from typing import Tuple

from engine.game.commands.command import Command


class PlaceRoadCommand(Command):
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float]):
        self.a = tuple(a)
        self.b = tuple(b)

    def execute(self, game, player):
        game.handle_place_road(player, self.a, self.b)
