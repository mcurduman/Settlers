def edge_connected_to_settlement(edge, board, player_id):
    a, b = edge["a"], edge["b"]
    for node in board["nodes"]:
        if (
            node["position"] in (a, b)
            and str(node.get("owner", "")).lower() == player_id.lower()
        ):
            return True
    return False


def is_valid_settlement_node(board, node, player_id):
    if node["owner"] is not None:
        return False

    pos = node["position"]

    if not _distance_rule_satisfied(board, pos):
        return False

    if _connected_to_player_road(board, pos, player_id):
        return True

    return False

def _distance_rule_satisfied(board, pos):
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

def _connected_to_player_road(board, pos, player_id):
    for edge in board["edges"]:
        if edge["owner"] == player_id and (edge["a"] == pos or edge["b"] == pos):
            return True
    return False


def edge_connected_to_network(edge, board, player_id):
    if edge_connected_to_settlement(edge, board, player_id):
        return True

    a, b = edge["a"], edge["b"]
    for other in board["edges"]:
        if str(other.get("owner", "")).lower() != player_id.lower():
            continue
        if other["a"] in (a, b) or other["b"] in (a, b):
            return True

    return False
