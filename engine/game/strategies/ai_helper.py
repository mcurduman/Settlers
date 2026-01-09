import math


def _dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def _adjacent_tiles_for_node(game_state, node_pos, threshold=1.2):
    tiles = game_state["board"]["tiles"]
    result = []

    for tile in tiles:
        center = (tile["q"], tile["r"])
        if _dist(center, node_pos) <= threshold:
            result.append(tile)

    return result


def is_desert_plus_resource(game_state, node_pos):
    tiles = _adjacent_tiles_for_node(game_state, node_pos)

    has_desert = any(t["resource"] == "desert" for t in tiles)
    has_resource = any(t["resource"] not in (None, "desert") for t in tiles)

    return has_desert and has_resource


def free_edges(game_state):
    return [
        (tuple(e["a"]), tuple(e["b"]))
        for e in game_state["board"]["edges"]
        if e["owner"] is None
    ]


def edges_touching_network(game_state, player):
    owned_nodes = getattr(player, "settlements", [])
    owned_roads = [tuple(r) for r in getattr(player, "roads", [])]

    network_nodes = set(owned_nodes)

    for a, b in owned_roads:
        network_nodes.add(a)
        network_nodes.add(b)

    edges = []
    for e in game_state["board"]["edges"]:
        if e["owner"] is not None:
            continue

        a = tuple(e["a"])
        b = tuple(e["b"])

        if a in network_nodes or b in network_nodes:
            edges.append((a, b))

    return edges
