import pytest
from engine.game.strategies import ai_helper


@pytest.fixture
def dummy_game_state():
    return {
        "board": {
            "nodes": [
                {"position": (0, 0), "owner": None},
                {"position": (3, 3), "owner": "p1"},
            ],
            "edges": [
                {"a": (0, 0), "b": (3, 3), "owner": None},
                {"a": (3, 3), "b": (2, 2), "owner": "p1"},
            ],
            "tiles": [
                {"q": 0, "r": 0, "resource": "wood"},
                {"q": 0, "r": 1, "resource": "desert"},
            ],
        }
    }


@pytest.fixture
def dummy_player():
    class Player:
        settlements = [(0, 0)]
        roads = [((0, 0), (1, 1))]

    return Player()


def test_dist():
    assert ai_helper._dist((0, 0), (3, 4)) == 5


def test_adjacent_tiles_for_node(dummy_game_state):
    tiles = ai_helper._adjacent_tiles_for_node(dummy_game_state, (0, 0))
    assert isinstance(tiles, list)


def test_is_desert_plus_resource(dummy_game_state):
    assert ai_helper.is_desert_plus_resource(dummy_game_state, (0, 0))


def test_free_edges(dummy_game_state):
    edges = ai_helper.free_edges(dummy_game_state)
    assert ((0, 0), (3, 3)) in edges


def test_edges_touching_network(dummy_game_state, dummy_player):
    edges = ai_helper.edges_touching_network(dummy_game_state, dummy_player)
    assert ((0, 0), (3, 3)) in edges


def test_is_valid_setup_settlement_node(dummy_game_state):
    assert ai_helper.is_valid_setup_settlement_node(dummy_game_state, (0, 0))
    assert not ai_helper.is_valid_setup_settlement_node(dummy_game_state, (3, 3))
