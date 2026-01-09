from unittest.mock import Mock

from client.render.board import node_renderer


def test_draw_nodes(monkeypatch):
    screen = Mock()
    nodes = [{"position": (0, 0), "owner": None}, {"position": (1, 1), "owner": "ai"}]
    board_rect = Mock()
    # Provide a real dict for board to support subscript
    board = {"dummy": 1}
    monkeypatch.setattr(node_renderer, "world_to_screen", Mock(return_value=(0, 0)))
    monkeypatch.setattr(
        node_renderer, "is_valid_settlement_node", Mock(return_value=True)
    )
    monkeypatch.setattr(
        node_renderer, "is_valid_setup_settlement_node", Mock(return_value=True)
    )
    monkeypatch.setattr(
        node_renderer,
        "pygame",
        Mock(
            draw=Mock(),
            font=Mock(),
            PALETTE={"mint": (0, 0, 0), "ai": (0, 0, 0), "human": (0, 0, 0)},
        ),
    )
    node_renderer.draw_nodes(
        screen, nodes, "PlayingPlaceSettlementState", board_rect, board, "human"
    )
    node_renderer.draw_nodes(
        screen, nodes, "SetupPlaceSettlementState", board_rect, board, "human"
    )
    node_renderer.draw_nodes(screen, nodes, "OtherState", board_rect, board, "human")
    node_renderer.draw_nodes(
        screen, nodes, "PlayingPlaceSettlementState", board_rect, board, "ai"
    )
