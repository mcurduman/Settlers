from client.input import helpers


def test_point_near_segment_on_segment():
    assert helpers.point_near_segment((1, 1), (0, 0), (2, 2), 1.5)


def test_point_near_segment_far():
    assert not helpers.point_near_segment((10, 10), (0, 0), (2, 2), 1.0)


def test_point_near_segment_zero_length():
    assert helpers.point_near_segment((0, 0), (0, 0), (0, 0), 0.1)


def test_edge_connected_to_player_settlement():
    board = {"nodes": [{"position": (1, 2), "owner": "p1"}], "edges": []}
    edge = {"a": (1, 2), "b": (3, 4)}
    assert helpers.edge_connected_to_player(edge, board, "p1")


def test_edge_connected_to_player_road():
    board = {
        "nodes": [{"position": (1, 2), "owner": None}],
        "edges": [{"a": (1, 2), "b": (3, 4), "owner": "p1"}],
    }
    edge = {"a": (1, 2), "b": (3, 4)}
    assert helpers.edge_connected_to_player(edge, board, "p1")


def test_edge_connected_to_player_none():
    board = {
        "nodes": [{"position": (1, 2), "owner": None}],
        "edges": [{"a": (1, 2), "b": (3, 4), "owner": "p2"}],
    }
    edge = {"a": (1, 2), "b": (3, 4)}
    assert not helpers.edge_connected_to_player(edge, board, "p1")
