def point_near_segment(p, a, b, tolerance):
    """
    Check if point p is within a certain distance (tolerance) of the segment ab.
    Useful for detecting clicks near a road/edge.
    """
    px, py = p
    ax, ay = a
    bx, by = b

    # vector AB
    abx = bx - ax
    aby = by - ay

    # vector AP
    apx = px - ax
    apy = py - ay

    ab_len_sq = abx * abx + aby * aby
    if ab_len_sq == 0:
        # a == b
        return (apx * apx + apy * apy) <= tolerance * tolerance

    # proiecție scalară
    t = (apx * abx + apy * aby) / ab_len_sq
    t = max(0.0, min(1.0, t))

    # punctul cel mai apropiat
    cx = ax + t * abx
    cy = ay + t * aby

    dx = px - cx
    dy = py - cy

    return (dx * dx + dy * dy) <= tolerance * tolerance


def edge_connected_to_player(edge, board, player_id):
    """
    Returns True if the edge is connected to any settlement or road owned by the player.
    Used to check if a new road can be placed.
    """
    # noduri conectate de edge
    a, b = edge["a"], edge["b"]

    # 1. settlement la capete
    for node in board["nodes"]:
        if node["position"] in (a, b) and str(node["owner"]).lower() == player_id:
            return True

    # 2. drum adiacent
    for other in board["edges"]:
        if str(other["owner"]).lower() != player_id:
            continue

        if other["a"] in (a, b) or other["b"] in (a, b):
            return True

    return False


def has_resources(resources, cost: dict) -> bool:
    """
    Returns True if the player has at least the required amount of each resource in cost.
    Used for build/trade validation.
    """
    for res, amt in cost.items():
        if resources.get(res, 0) < amt:
            return False
    return True


def edge_connected_to_network(edge, board, player_id):
    """
    Returns True if the edge is connected to the player's road network or settlements.
    Used to validate road placement in the main phase.
    """
    a, b = edge["a"], edge["b"]

    # settlement
    for node in board["nodes"]:
        if (
            node["position"] in (a, b)
            and str(node.get("owner", "")).lower() == player_id
        ):
            return True

    # road
    for other in board["edges"]:
        if str(other.get("owner", "")).lower() != player_id:
            continue
        if other["a"] in (a, b) or other["b"] in (a, b):
            return True

    return False


def _dist(a, b):
    """Calculate Euclidean distance between two positions."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def is_valid_setup_settlement_node(board, node_pos):
    return _distance_rule_ok(board, node_pos)


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


def can_trade_3_1(resources: dict) -> bool:
    """
    Returns True if the player can trade 3 of any resource for 1 (bank trade).
    """
    return any(v >= 3 for v in resources.values())
