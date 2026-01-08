def point_near_segment(p, a, b, tolerance):
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
    for res, amt in cost.items():
        if resources.get(res, 0) < amt:
            return False
    return True


def edge_connected_to_network(edge, board, player_id):
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


def is_valid_settlement_node(board, node, player_id):
    if node["owner"] is not None:
        return False

    pos = node["position"]

    # distance rule
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

    # connected to player's road
    for edge in board["edges"]:
        if str(edge["owner"]).lower() == str(player_id).lower() and (
            edge["a"] == pos or edge["b"] == pos
        ):
            return True

    return False


def can_trade_3_1(resources: dict) -> bool:
    return any(v >= 3 for v in resources.values())
