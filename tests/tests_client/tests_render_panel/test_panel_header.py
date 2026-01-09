import pytest
from unittest.mock import Mock, patch
import sys


def setup_pygame_mocks():
    sys.modules["pygame"] = Mock()
    sys.modules["pygame.draw"] = Mock()
    sys.modules["pygame.font"] = Mock()
    sys.modules["pygame.mouse"] = Mock()
    sys.modules["pygame.Surface"] = Mock()


def test_draw_panel_header_basic():
    setup_pygame_mocks()
    from client.render.panel import panel_header

    screen = Mock()
    state = {"state": "SetupRollState"}
    x, y = 10, 20
    result_y = panel_header.draw_panel_header(screen, state, x, y)
    assert isinstance(result_y, int)


def test_draw_panel_header_with_helper_and_error():
    setup_pygame_mocks()
    from client.render.panel import panel_header

    screen = Mock()
    state = {"state": "PlayingMainState", "error": "Some error"}
    x, y = 0, 0
    result_y = panel_header.draw_panel_header(screen, state, x, y)
    assert isinstance(result_y, int)
