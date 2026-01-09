from unittest.mock import Mock

from client.render.board import board_renderer


def test_draw_board(monkeypatch):
    screen = Mock()
    state = {
        "board": {"tiles": [], "edges": [], "nodes": []},
        "state": "",
        "current_player": "",
    }
    board_rect = Mock()
    monkeypatch.setattr(board_renderer, "load_tile_icons", Mock(return_value={}))
    monkeypatch.setattr(board_renderer, "draw_tiles", Mock())
    monkeypatch.setattr(board_renderer, "draw_edges", Mock())
    monkeypatch.setattr(board_renderer, "draw_nodes", Mock())
    board_renderer.draw_board(screen, state, board_rect)
    board_renderer.draw_tiles.assert_called()
    board_renderer.draw_edges.assert_called()
    board_renderer.draw_nodes.assert_called()
