from enum import Enum


class ResourceType(str, Enum):
    WOOD = "wood"
    BRICK = "brick"
    SHEEP = "sheep"
    WHEAT = "wheat"
    DESERT = "desert"


RESOURCE_DISTRIBUTION = {
    ResourceType.WOOD: 2,
    ResourceType.BRICK: 2,
    ResourceType.SHEEP: 1,
    ResourceType.WHEAT: 1,
    ResourceType.DESERT: 1,
}

NUMBERS = [1, 2, 3, 4, 5, 6]


def build_resources():
    resources = []
    for resource, count in RESOURCE_DISTRIBUTION.items():
        resources.extend([resource] * count)
    return resources
