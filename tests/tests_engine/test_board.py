import pytest
from engine.game.board import Board
from engine.game.entities.resource_type import ResourceType


@pytest.fixture
def board():
    return Board()


def test_board_initialization(board):
    summary = board.debug_summary()
    assert summary["tiles"] == 7
    assert summary["nodes"] > 0
    assert summary["edges"] > 0


def test_get_tiles_nodes_edges(board):
    assert len(board.get_tiles()) == 7
    assert len(board.get_nodes()) == len(board.nodes)
    assert len(board.get_edges()) == len(board.edges)


def test_longest_road_empty(board):
    class DummyPlayer:
        roads = []

    assert board.longest_road(DummyPlayer()) == 0


def test_produce_resources_for_player(board):
    player_name = "Test"
    node = next(iter(board.nodes.values()))
    node.owner = player_name
    tile = board.tiles[0]
    tile.number = 8
    tile.resource = ResourceType.WOOD
    produced = board.produce_resources(8, player_name)
    assert ResourceType.WOOD in produced


def test_valid_settlement_node(board):
    class DummyPlayer:
        roads = []
        name = "Test"

    node_pos = next(pos for pos, node in board.nodes.items() if node.owner is None)
    assert not board.valid_settlement_node(node_pos, DummyPlayer())
    DummyPlayer.roads = [(node_pos, (0, 0))]
    assert board.valid_settlement_node(node_pos, DummyPlayer)


def test_edge_connected_to_network_and_settlement(board):
    class DummyEdge:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class DummyPlayer:
        settlements = set()
        roads = []
        name = "Test"

    # Pick two nodes
    nodes = list(board.nodes.keys())
    a, b = nodes[0], nodes[1]
    player = DummyPlayer()
    player.settlements = {a}
    player.roads = [(a, b)]
    edge = DummyEdge(a, b)
    # Should be connected to network and settlement
    assert board.edge_connected_to_network(edge, player)
    assert board.edge_connected_to_settlement(edge, player)
    # Should be False if not connected
    edge2 = DummyEdge(nodes[2], nodes[3])
    assert not board.edge_connected_to_network(edge2, player)
    assert not board.edge_connected_to_settlement(edge2, player)


def test_node_has_adjacent_settlement(board):
    node_pos = next(iter(board.nodes.keys()))
    for edge in board.edges.values():
        if node_pos in (edge.a, edge.b):
            other = edge.b if edge.a == node_pos else edge.a
            board.nodes[other].owner = "Test"
            break
    assert board.node_has_adjacent_settlement(node_pos)


def test_node_connected_to_player_road(board):
    class DummyPlayer:
        roads = []

    node_pos = next(iter(board.nodes.keys()))
    player = DummyPlayer()
    player.roads = [(node_pos, (0, 0))]
    assert board.node_connected_to_player_road(node_pos, player)
    player.roads = [((1, 1), (2, 2))]
    assert not board.node_connected_to_player_road(node_pos, player)


def test_debug_summary_main(monkeypatch, capsys):
    import runpy

    runpy.run_path("engine/game/board.py", run_name="__main__")
    out = capsys.readouterr().out
    assert "tiles" in out and "nodes" in out and "edges" in out
