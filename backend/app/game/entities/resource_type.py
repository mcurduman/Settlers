from enum import Enum


class ResourceType(str, Enum):
    FOREST = "forest"
    CLAY = "clay"
    SHEEP = "sheep"
    WHEAT = "wheat"
    DESERT = "desert"


RESOURCE_DISTRIBUTION = {
    ResourceType.FOREST: 2,
    ResourceType.CLAY: 2,
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
