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
        if not player.roads:
            return 0

        blocked_nodes = {
            pos
            for pos, node in self.nodes.items()
            if node.owner is not None and node.owner != player.name
        }

        graph = defaultdict(list)
        for a, b in player.roads:
            graph[a].append(b)
            graph[b].append(a)

        def dfs(node, visited_edges):
            max_len = 0
            for neighbor in graph[node]:
                edge = tuple(sorted((node, neighbor)))
                if edge in visited_edges:
                    continue

                if neighbor in blocked_nodes:
                    continue

                visited_edges.add(edge)
                max_len = max(max_len, 1 + dfs(neighbor, visited_edges))
                visited_edges.remove(edge)

            return max_len

        return max(dfs(node, set()) for node in graph)

    def produce_resources(
        self, dice_value: int, player_name: str
    ) -> List[ResourceType]:
        """
        Return resources produced for the given player only (for their settlements).
        """
        produced_resources: List[ResourceType] = []

        for tile in self.tiles:
            if tile.number == dice_value:
                for corner in tile.corners(self.size):
                    key = normalize(corner)
                    node = self.nodes.get(key)

                    if node and node.owner == player_name:
                        produced_resources.append(tile.resource)

        return produced_resources

    def edge_connected_to_network(self, edge, player):
        a, b = edge.a, edge.b if hasattr(edge, "a") else (edge["a"], edge["b"])

        # 1. settlement la capăt
        for pos in player.settlements:
            if pos == a or pos == b:
                return True

        # 2. drum adiacent
        for ra, rb in player.roads:
            if a in (ra, rb) or b in (ra, rb):
                return True

        return False

    def edge_connected_to_settlement(self, edge, player):
        a, b = edge.a, edge.b if hasattr(edge, "a") else (edge["a"], edge["b"])

        for pos in player.settlements:
            if pos == a or pos == b:
                return True

        return False

    def node_has_adjacent_settlement(self, node_pos):
        for edge in self.edges.values():
            a, b = edge.a, edge.b
            if node_pos == a:
                other = b
            elif node_pos == b:
                other = a
            else:
                continue

            if other in self.nodes and self.nodes[other].owner is not None:
                return True

        return False

    def node_connected_to_player_road(self, node_pos, player):
        for a, b in player.roads:
            if node_pos == a or node_pos == b:
                return True
        return False

    def valid_settlement_node(self, node_pos, player):
        node = self.nodes.get(node_pos)
        if node is None or node.owner is not None:
            return False

        # distance rule (indiferent de owner)
        if self.node_has_adjacent_settlement(node_pos):
            return False

        # must connect to at least ONE of your roads
        if not self.node_connected_to_player_road(node_pos, player):
            return False

        return True

    def debug_summary(self) -> dict:
        return {
            "tiles": len(self.tiles),
            "nodes": len(self.nodes),
            "edges": len(self.edges),
        }


if __name__ == "__main__":
    board = Board()
    print(board.debug_summary())
