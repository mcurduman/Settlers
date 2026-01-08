def edge_connected_to_settlement(edge, board, player_id):
    """Check if the edge is connected to any settlement owned by the player."""
    a, b = edge["a"], edge["b"]
    for node in board["nodes"]:
        if (
            node["position"] in (a, b)
            and str(node.get("owner", "")).lower() == player_id.lower()
        ):
            return True
    return False


def _is_distance_rule_satisfied(board, pos):
    """Check if there are no adjacent settlements violating the distance rule"""
    for edge in board["edges"]:
        other = None
        if edge["a"] == pos:
            other = edge["b"]
        elif edge["b"] == pos:
            other = edge["a"]
        if other is not None:
            for n in board["nodes"]:
                # Check if there's a settlement at the other node
                if n["position"] == other and n["owner"] is not None:
                    return False
    return True


def _connected_to_player_road(board, pos, player_id):
    """Check if the position is connected to the player's road network."""
    for edge in board["edges"]:
        if edge["owner"] == player_id and (edge["a"] == pos or edge["b"] == pos):
            return True
    return False


def is_valid_settlement_node(board, node, player_id):
    """Check if the node is a valid settlement spot for the player."""
    if node["owner"] is not None:
        return False

    pos = node["position"]
    if not _is_distance_rule_satisfied(board, pos):
        return False

    if _connected_to_player_road(board, pos, player_id):
        return True

    return False


def edge_connected_to_network(edge, board, player_id):
    """Check if the edge is connected to the player's existing road network or settlements."""
    if edge_connected_to_settlement(edge, board, player_id):
        return True

    a, b = edge["a"], edge["b"]
    for other in board["edges"]:
        # Skip self
        if str(other.get("owner", "")).lower() != player_id.lower():
            continue
        # Check if connected
        if other["a"] in (a, b) or other["b"] in (a, b):
            return True

    return False


def _is_connected_to_player_road(board, pos, player_name):
    """Check if the position is connected to the player's road network."""
    for edge in board["edges"]:
        if edge["owner"] == player_name and (edge["a"] == pos or edge["b"] == pos):
            return True
    return False


def has_valid_settlement_spot(board, player_name):
    """ "Check if the player has at least one valid spot to place a settlement."""
    for node in board["nodes"]:
        if node["owner"] is not None:
            continue

        pos = node["position"]

        if not _is_distance_rule_satisfied(board, pos):
            continue

        if _is_connected_to_player_road(board, pos, player_name):
            return True

    return False
