import pytest
from unittest.mock import Mock
import types
import sys


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    sys.modules["pygame"] = types.SimpleNamespace(
        MOUSEBUTTONDOWN=1, mouse=Mock(get_pos=Mock(return_value=(0, 0)))
    )
    yield


def make_event(type_=1, button=1):
    return types.SimpleNamespace(type=type_, button=button)


def test_handle_playing_place_settlement(monkeypatch):
    from client.input import board_input

    event = make_event()
    state = {
        "board": {"nodes": [{"owner": None, "position": (0, 0)}]},
        "current_player": "p1",
    }
    game = Mock()
    board_rect = Mock()
    monkeypatch.setattr(board_input, "world_to_screen", Mock(return_value=(0, 0)))
    monkeypatch.setattr(
        board_input, "is_valid_settlement_node", Mock(return_value=True)
    )
    board_input.handle_playing_place_settlement(event, state, game, board_rect)
    game.execute_command_by_name.assert_called_with("place_settlement", position=(0, 0))
