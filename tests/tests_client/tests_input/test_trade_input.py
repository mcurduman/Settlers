import pytest
from unittest.mock import Mock
import types
import sys


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    import sys

    sys.modules["pygame"] = types.SimpleNamespace(MOUSEBUTTONDOWN=1, mouse=Mock())
    yield


def make_event(type_=1, button=1):
    return types.SimpleNamespace(type=type_, button=button)


def test_handle_trade_with_bank_give_receive(monkeypatch):
    from client.input import trade_input

    event = make_event()
    trade_ui = {
        "trade_give": {"wood": Mock(collidepoint=Mock(return_value=True))},
        "trade_receive": {"brick": Mock(collidepoint=Mock(return_value=True))},
    }
    trade_state = {"give": None, "receive": None}
    game = Mock()
    trade_input.handle_trade_with_bank(event, game, trade_ui, trade_state)
    assert trade_state["give"] == "wood"
    assert trade_state["receive"] == "brick"


def test_handle_trade_with_bank_confirm(monkeypatch):
    from client.input import trade_input

    event = make_event()
    trade_ui = {
        "trade_give": {},
        "trade_receive": {},
        "confirm_trade": Mock(collidepoint=Mock(return_value=True)),
    }
    trade_state = {"give": "wood", "receive": "brick"}
    game = Mock()
    trade_input.handle_trade_with_bank(event, game, trade_ui, trade_state)
    game.execute_command_by_name.assert_called_with(
        "trade_with_bank", give="wood", receive="brick"
    )
    assert trade_state["give"] is None and trade_state["receive"] is None


def test_handle_trade_with_bank_cancel(monkeypatch):
    from client.input import trade_input

    event = make_event()
    trade_ui = {
        "trade_give": {},
        "trade_receive": {},
        "cancel_trade": Mock(collidepoint=Mock(return_value=True)),
    }
    trade_state = {"give": "wood", "receive": "brick"}
    game = Mock()
    trade_input.handle_trade_with_bank(event, game, trade_ui, trade_state)
    game.execute_command_by_name.assert_called_with("exit_trade_with_bank")
    assert trade_state["give"] is None and trade_state["receive"] is None
