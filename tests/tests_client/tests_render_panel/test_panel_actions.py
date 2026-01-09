import pytest
from client.render.panel import panel_actions


def test_get_button_definitions_main():
    state = {"state": "PlayingMainState"}
    defs = panel_actions.get_button_definitions(state, True, True, True)
    assert any("Settlement" in d[0] for d in defs)


def test_get_button_definitions_cancel():
    state = {"state": "PlayingPlaceSettlementState"}
    defs = panel_actions.get_button_definitions(state, False, False, False)
    assert defs[0][0] == "Cancel"


def test_get_button_colors_variants():
    # test all button color branches
    for key in ["end_turn_button", "cancel_placement_button", "other"]:
        c = panel_actions.get_button_colors(key, True, True)
        assert isinstance(c, tuple)
    c = panel_actions.get_button_colors("other", False, False)
    assert isinstance(c, tuple)
