import math


def _dist(a, b):
    """Return Euclidean distance between two points."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def _adjacent_tiles_for_node(game_state, node_pos, threshold=1.2):
    """Return tiles adjacent to a node within a threshold distance."""
    tiles = game_state["board"]["tiles"]
    result = []

    for tile in tiles:
        center = (tile["q"], tile["r"])
        if _dist(center, node_pos) <= threshold:
            result.append(tile)

    return result


def is_desert_plus_resource(game_state, node_pos):
    """Check if a node is adjacent to both a desert and a resource tile."""
    tiles = _adjacent_tiles_for_node(game_state, node_pos)

    has_desert = any(t["resource"] == "desert" for t in tiles)
    has_resource = any(t["resource"] not in (None, "desert") for t in tiles)

    return has_desert and has_resource


def free_edges(game_state):
    """Return all free (unowned) edges on the board."""
    return [
        (tuple(e["a"]), tuple(e["b"]))
        for e in game_state["board"]["edges"]
        if e["owner"] is None
    ]


def edges_touching_network(game_state, player):
    """Return all free edges that touch the player's network."""
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


def is_valid_setup_settlement_node(game_state, node_pos, min_dist=2.0):
    """Check if a node is a valid settlement spot by distance rule."""
    for node in game_state["board"]["nodes"]:
        if node["owner"] is None:
            continue

        other_pos = tuple(node["position"])

        if _dist(node_pos, other_pos) < min_dist:
            return False

    return True


def is_valid_settlement_node(board, node, player_id):
    """
    Returns True if the node is a valid settlement spot for the player:
    - Node is empty
    - Distance rule is satisfied (no adjacent settlements)
    - Connected to player's road network
    """
    if node["owner"] is not None:
        return False

    pos = node["position"]

    if not _distance_rule_ok(board, pos):
        return False

    if _connected_to_players_road(board, pos, player_id):
        return True

    return False


def _distance_rule_ok(board, pos):
    """
    Returns True if there are no settlements adjacent to pos (distance rule satisfied).
    """
    for edge in board["edges"]:
        other = None
        if edge["a"] == pos:
            other = edge["b"]
        elif edge["b"] == pos:
            other = edge["a"]
        if other is not None:
            for n in board["nodes"]:
                if n["position"] == other and n["owner"] is not None:
                    return False
    return True


def _connected_to_players_road(board, pos, player_id):
    """
    Returns True if pos is connected to any road owned by the player.
    Used for settlement placement validation.
    """
    for edge in board["edges"]:
        if str(edge["owner"]).lower() == str(player_id).lower() and (
            edge["a"] == pos or edge["b"] == pos
        ):
            return True
    return False


def get_player_resources(game_state, player):
    """Return the resources of the given player from game state."""
    for p in game_state["players"]:
        if p["name"] == player.name:
            return p["resources"]
    return {}


def can_try_settlement(resources):
    """Check if resources are enough to build a settlement."""
    return (
        resources.get("wood", 0) >= 1
        and resources.get("brick", 0) >= 1
        and resources.get("wheat", 0) >= 1
        and resources.get("sheep", 0) >= 1
    )


def can_try_road(resources):
    """Check if resources are enough to build a road."""
    return resources.get("wood", 0) >= 1 and resources.get("brick", 0) >= 1


def can_try_trade(resources, rate=3):
    """Check if any resource can be traded at the given rate."""
    return any(v >= rate for v in resources.values())
