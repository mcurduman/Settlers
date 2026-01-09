import pytest
from unittest.mock import patch, Mock
import sys


def setup_pygame_mocks():
    sys.modules["pygame"] = Mock()
    sys.modules["pygame.draw"] = Mock()
    sys.modules["pygame.font"] = Mock()
    sys.modules["pygame.mouse"] = Mock()
    sys.modules["pygame.Surface"] = Mock()


def test_draw_roll_button():
    setup_pygame_mocks()
    with patch("pygame.mouse.get_pos", return_value=(10, 10)), patch(
        "client.render.tooltip.draw_tooltip"
    ):
        from client.render.panel import buttons

        screen = Mock()
        rect = Mock()
        rect.collidepoint.return_value = True
        buttons.draw_roll_button(screen, rect, enabled=True)
        buttons.draw_roll_button(screen, rect, enabled=False)


def test_draw_cancel_button():
    setup_pygame_mocks()
    with patch("pygame.mouse.get_pos", return_value=(10, 10)), patch(
        "client.render.tooltip.draw_tooltip"
    ):
        from client.render.panel import buttons

        screen = Mock()
        rect = Mock()
        rect.x, rect.y, rect.width, rect.height = 0, 0, 100, 100
        rect_btn = buttons.draw_cancel_button(screen, rect)
        assert rect_btn is not None
