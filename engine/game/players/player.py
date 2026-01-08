from abc import ABC
from collections import defaultdict
from typing import Set, Tuple

from engine.game.entities.resource_type import ResourceType


class Player(ABC):
    def __init__(self, name: str):
        self.name = name
        self.victory_points = 0
        self.resources = defaultdict(int)
        self.settlements: Set[Tuple[float, float]] = set()
        self.roads: Set[Tuple[Tuple[float, float], Tuple[float, float]]] = set()
        self.last_dice_roll = 0

    def is_ai(self) -> bool:
        return False

    def roll_dice(self, value: int):
        self.last_dice_roll = value

    def add_resource(self, resource: ResourceType, amount: int = 1):
        self.resources[resource] += amount

    def remove_resource(self, resource: ResourceType, amount: int = 1):
        if self.resources[resource] >= amount:
            self.resources[resource] -= amount
        else:
            raise ValueError(f"Not enough {resource} to remove")

    def add_settlement(self, position: Tuple[float, float]):
        self.settlements.add(position)

    def remove_resource_for_settlement(self):
        # remove wood, brick, wheat, and sheep resources for building the settlement
        self.remove_resource(ResourceType.WOOD)
        self.remove_resource(ResourceType.BRICK)
        self.remove_resource(ResourceType.WHEAT)
        self.remove_resource(ResourceType.SHEEP)

    def add_road(self, a: Tuple[float, float], b: Tuple[float, float]):
        # normalize ordering so (a,b) == (b,a)
        self.roads.add(tuple(sorted((a, b))))

    def remove_resource_for_road(self):
        # remove wood and brick resources for building the road
        self.remove_resource(ResourceType.WOOD)
        self.remove_resource(ResourceType.BRICK)

    def trade_with_bank(
        self, give_resource: ResourceType, receive_resource: ResourceType, rate: int = 3
    ):
        if self.resources[give_resource] >= rate:
            self.remove_resource(give_resource, rate)
            self.add_resource(receive_resource)
        else:
            raise ValueError(f"Not enough {give_resource} to trade with bank")
