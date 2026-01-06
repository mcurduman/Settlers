from abc import ABC
from collections import defaultdict
from typing import Set, Tuple

from engine.game.entities.resource_type import ResourceType


class Player(ABC):
    def __init__(self, name: str):
        self.name = name
        self.victory_points = 0
        self.resources = defaultdict(int)

        # OWNERSHIP
        self.settlements: Set[Tuple[float, float]] = set()
        self.roads: Set[Tuple[Tuple[float, float], Tuple[float, float]]] = set()

        self.last_dice_roll = 0

    def roll_dice(self, value: int):
        self.last_dice_roll = value

    def add_resource(self, resource: ResourceType, amount: int = 1):
        self.resources[resource] += amount

    def add_settlement(self, position: Tuple[float, float]):
        self.settlements.add(position)

    def add_road(self, a: Tuple[float, float], b: Tuple[float, float]):
        # normalize ordering so (a,b) == (b,a)
        self.roads.add(tuple(sorted((a, b))))
