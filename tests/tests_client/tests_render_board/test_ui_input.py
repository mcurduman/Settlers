import sys
import types
from unittest.mock import Mock

import pytest


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    sys.modules["pygame"] = types.SimpleNamespace(MOUSEBUTTONDOWN=1, mouse=Mock())
    yield


def make_event(type_=1, button=1):
    return types.SimpleNamespace(type=type_, button=button)


def test_handle_roll_and_main_state_ui_roll(monkeypatch):
    from client.input import ui_input

    event = make_event()
    panel_ui = {"roll_button": Mock(collidepoint=Mock(return_value=True))}
    game = Mock()
    ui_input.handle_roll_and_main_state_ui(event, "SetupRollState", panel_ui, game)
    game.execute_command_by_name.assert_called_with("roll_dice")


def test_handle_roll_and_main_state_ui_main(monkeypatch):
    from client.input import ui_input

    event = make_event()
    panel_ui = {}
    game = Mock()
    monkeypatch.setattr(ui_input, "handle_main_action_buttons", Mock())
    ui_input.handle_roll_and_main_state_ui(event, "PlayingMainState", panel_ui, game)
    ui_input.handle_main_action_buttons.assert_called()


def test_handle_main_action_buttons(monkeypatch):
    from client.input import ui_input

    mouse = (1, 2)
    panel_ui = {
        "place_settlement_button": Mock(collidepoint=Mock(return_value=True)),
        "place_road_button": Mock(collidepoint=Mock(return_value=False)),
        "trade_with_bank_button": Mock(collidepoint=Mock(return_value=False)),
        "end_turn_button": Mock(collidepoint=Mock(return_value=False)),
    }
    game = Mock()
    monkeypatch.setattr(
        ui_input,
        "pygame",
        types.SimpleNamespace(mouse=Mock(get_pos=Mock(return_value=mouse))),
    )
    ui_input.handle_main_action_buttons(mouse, panel_ui, game)
    game.execute_command_by_name.assert_called_with("start_place_settlement")


def test_handle_cancel_placement_ui_road(monkeypatch):
    from client.input import ui_input

    event = make_event()
    panel_ui = {"cancel_placement_button": Mock(collidepoint=Mock(return_value=True))}
    game = Mock()
    ui_input.handle_cancel_placement_ui(event, "PlayingPlaceRoadState", panel_ui, game)
    game.execute_command_by_name.assert_called_with("exit_place_road")


def test_handle_cancel_placement_ui_settlement(monkeypatch):
    from client.input import ui_input

    event = make_event()
    panel_ui = {"cancel_placement_button": Mock(collidepoint=Mock(return_value=True))}
    game = Mock()
    ui_input.handle_cancel_placement_ui(
        event, "PlayingPlaceSettlementState", panel_ui, game
    )
    game.execute_command_by_name.assert_called_with("exit_place_settlement")
