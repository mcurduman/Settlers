from unittest.mock import Mock

from client.render.board import edge_renderer


def test_draw_edges(monkeypatch):
    screen = Mock()
    edges = [
        {"a": (0, 0), "b": (1, 1), "owner": None},
        {"a": (2, 2), "b": (3, 3), "owner": "ai"},
    ]
    board = Mock()
    board_rect = Mock()
    monkeypatch.setattr(edge_renderer, "world_to_screen", Mock(return_value=(0, 0)))
    monkeypatch.setattr(
        edge_renderer, "edge_connected_to_network", Mock(return_value=True)
    )
    monkeypatch.setattr(
        edge_renderer, "edge_connected_to_settlement", Mock(return_value=True)
    )
    monkeypatch.setattr(
        edge_renderer,
        "pygame",
        Mock(
            draw=Mock(),
            PALETTE={"mint": (0, 0, 0), "ai": (0, 0, 0), "human": (0, 0, 0)},
        ),
    )
    edge_renderer.draw_edges(
        screen, edges, board, "PlayingPlaceRoadState", "human", board_rect
    )
    edge_renderer.draw_edges(
        screen, edges, board, "SetupPlaceRoadState", "human", board_rect
    )
    edge_renderer.draw_edges(screen, edges, board, "OtherState", "ai", board_rect)
