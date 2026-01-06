from collections import defaultdict
import random
from typing import Dict, Tuple, List

from engine.game.entities.hex_tile import HexTile
from engine.game.entities.node import Node
from engine.game.entities.edge import Edge
from engine.game.entities.resource_type import ResourceType, build_resources, NUMBERS


def normalize(point: Tuple[float, float], precision: int = 2) -> Tuple[float, float]:
    """
    Rounds the coordinates of a point to avoid floating-point precision issues.
    """
    return (round(point[0], precision), round(point[1], precision))


class Board:
    def __init__(self, size: float = 1.0):
        self.size = size

        self.tiles: List[HexTile] = self._generate_tiles()
        self.nodes: Dict[Tuple[float, float], Node] = self._generate_nodes()
        self.edges: Dict[Tuple[Tuple[float, float], Tuple[float, float]], Edge] = (
            self._generate_edges()
        )

    def _generate_tiles(self) -> List[HexTile]:
        resources = build_resources()
        random.shuffle(resources)

        numbers = NUMBERS.copy()
        random.shuffle(numbers)
        number_index = 0

        # axial coordinates(center + 6 neighbors)
        positions = [
            (0, 0),  # center
            (0, -1),  # top-left
            (1, -1),  # top-right
            (1, 0),  # right
            (0, 1),  # bottom-right
            (-1, 1),  # bottom-left
            (-1, 0),  # left
        ]

        tiles: List[HexTile] = []

        for q, r in positions:
            resource = resources.pop()

            number = None
            if resource != ResourceType.DESERT:
                number = numbers[number_index]
                number_index += 1

            tiles.append(HexTile(q=q, r=r, resource=resource, number=number))

        return tiles

    def _generate_nodes(self) -> Dict[Tuple[float, float], Node]:
        nodes: Dict[Tuple[float, float], Node] = {}

        for tile in self.tiles:
            for corner in tile.corners(self.size):
                key = normalize(corner)

                if key not in nodes:
                    nodes[key] = Node(position=key)

        return nodes

    def _generate_edges(
        self,
    ) -> Dict[Tuple[Tuple[float, float], Tuple[float, float]], Edge]:
        edges: Dict[Tuple[Tuple[float, float], Tuple[float, float]], Edge] = {}

        for tile in self.tiles:
            corners = [normalize(c) for c in tile.corners(self.size)]

            for i in range(6):
                a = corners[i]
                b = corners[(i + 1) % 6]

                key = tuple(sorted((a, b)))

                if key not in edges:
                    edges[key] = Edge(a=a, b=b)

        return edges

    def get_tiles(self) -> List[HexTile]:
        return self.tiles

    def get_nodes(self) -> List[Node]:
        return list(self.nodes.values())

    def get_edges(self) -> List[Edge]:
        return list(self.edges.values())

    def longest_road(self, player) -> int:
        graph = defaultdict(list)

        if not player.roads:
            return 0

        for a, b in player.roads:
            graph[a].append(b)
            graph[b].append(a)

        def dfs(node, visited_edges):
            max_len = 0
            for neighbor in graph[node]:
                edge = tuple(sorted((node, neighbor)))
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    max_len = max(max_len, 1 + dfs(neighbor, visited_edges))
                    visited_edges.remove(edge)
            return max_len

        return max(dfs(node, set()) for node in graph)

    def produce_resources(self, dice_value: int) -> List[ResourceType]:
        produced_resources: List[ResourceType] = []

        for tile in self.tiles:
            if tile.number == dice_value:
                for corner in tile.corners(self.size):
                    key = normalize(corner)
                    node = self.nodes.get(key)

                    if node and node.owner is not None:
                        produced_resources.append(tile.resource)

        return produced_resources

    def debug_summary(self) -> dict:
        return {
            "tiles": len(self.tiles),
            "nodes": len(self.nodes),
            "edges": len(self.edges),
        }


if __name__ == "__main__":
    board = Board()
    print(board.debug_summary())
