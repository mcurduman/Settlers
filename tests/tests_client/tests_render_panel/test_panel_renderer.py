import pytest
from unittest.mock import Mock, patch
import sys


def setup_pygame_mocks():
    sys.modules["pygame"] = Mock()
    sys.modules["pygame.draw"] = Mock()
    sys.modules["pygame.font"] = Mock()
    sys.modules["pygame.mouse"] = Mock()
    sys.modules["pygame.Surface"] = Mock()


def test_draw_panel_main():
    setup_pygame_mocks()
    with patch(
        "client.render.panel.panel_header.draw_panel_header", return_value=50
    ), patch(
        "client.render.panel.player_card.draw_player_card",
        return_value=(100, None, None),
    ), patch(
        "client.render.panel.panel_actions.draw_panel_action_buttons", return_value=None
    ), patch(
        "client.render.panel.trade_panel.draw_trade_with_bank_panel",
        return_value=({}, None),
    ), patch(
        "client.render.panel.buttons.draw_cancel_button", return_value=Mock()
    ):
        from client.render.panel import panel_renderer

        screen = Mock()
        rect = Mock()
        rect.x, rect.y, rect.width = 0, 0, 200
        state = {
            "state": "PlayingMainState",
            "players": [{"name": "human"}],
            "current_player": "human",
        }
        trade_state = {}
        panel_ui, _ = panel_renderer.draw_panel(screen, state, rect, trade_state)
        assert isinstance(panel_ui, dict)
