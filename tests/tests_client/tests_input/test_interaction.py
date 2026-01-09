import pytest
from unittest.mock import Mock
import types
import sys


# Patch pygame.Rect for board_rect
class DummyRect:
    pass


@pytest.fixture(autouse=True)
def patch_imports(monkeypatch):
    # Patch all imported handlers with mocks
    import client.input.interaction as interaction

    monkeypatch.setattr(interaction, "handle_setup_place_settlement", Mock())
    monkeypatch.setattr(interaction, "handle_setup_place_road", Mock())
    monkeypatch.setattr(interaction, "handle_playing_place_road", Mock())
    monkeypatch.setattr(interaction, "handle_playing_place_settlement", Mock())
    monkeypatch.setattr(interaction, "handle_trade_with_bank", Mock())
    monkeypatch.setattr(interaction, "handle_cancel_placement_ui", Mock())
    monkeypatch.setattr(interaction, "handle_roll_and_main_state_ui", Mock())
    yield


def make_event():
    return object()


def make_state(state_name):
    return {"state": state_name}


def test_handle_interaction_setup_place_settlement():
    from client.input.interaction import (
        handle_interaction,
        handle_setup_place_settlement,
    )

    event = make_event()
    state = make_state("SetupPlaceSettlementState")
    game = object()
    board_rect = DummyRect()
    handle_interaction(event, state, game, board_rect)
    handle_setup_place_settlement.assert_called_once()


def test_handle_interaction_setup_place_road():
    from client.input.interaction import handle_interaction, handle_setup_place_road

    event = make_event()
    state = make_state("SetupPlaceRoadState")
    game = object()
    board_rect = DummyRect()
    handle_interaction(event, state, game, board_rect)
    handle_setup_place_road.assert_called_once()


def test_handle_interaction_playing_main_and_roll_states():
    from client.input.interaction import (
        handle_interaction,
        handle_roll_and_main_state_ui,
    )

    event = make_event()
    for s in ["PlayingMainState", "SetupRollState", "PlayingRollState"]:
        state = make_state(s)
        game = object()
        board_rect = DummyRect()
        handle_interaction(event, state, game, board_rect)
        handle_roll_and_main_state_ui.assert_called()
        handle_roll_and_main_state_ui.reset_mock()


def test_handle_interaction_playing_place_states():
    from client.input.interaction import (
        handle_interaction,
        handle_cancel_placement_ui,
        handle_playing_place_road,
        handle_playing_place_settlement,
    )

    event = make_event()
    for s in ["PlayingPlaceRoadState", "PlayingPlaceSettlementState"]:
        state = make_state(s)
        game = object()
        board_rect = DummyRect()
        handle_interaction(event, state, game, board_rect)
        handle_cancel_placement_ui.assert_called()
        if s == "PlayingPlaceRoadState":
            handle_playing_place_road.assert_called()
            handle_playing_place_road.reset_mock()
        if s == "PlayingPlaceSettlementState":
            handle_playing_place_settlement.assert_called()
            handle_playing_place_settlement.reset_mock()
        handle_cancel_placement_ui.reset_mock()


def test_handle_interaction_playing_trade_with_bank():
    from client.input.interaction import handle_interaction, handle_trade_with_bank

    event = make_event()
    state = make_state("PlayingTradeWithBankState")
    game = object()
    board_rect = DummyRect()
    handle_interaction(
        event, state, game, board_rect, trade_ui=object(), trade_state=object()
    )
    handle_trade_with_bank.assert_called_once()
