from unittest.mock import Mock, patch

import pytest

from engine.game.strategies.easy_ai import EasyAIStrategy


@pytest.fixture
def dummy_game_state():
    return {
        "state": "SetupPlaceSettlementState",
        "board": {
            "nodes": [
                {"position": (0, 0), "owner": None},
                {"position": (1, 1), "owner": None},
            ],
            "edges": [
                {"a": (0, 0), "b": (1, 1), "owner": None},
            ],
            "tiles": [
                {"q": 0, "r": 0, "resource": "wood", "number": 5},
                {"q": 1, "r": 1, "resource": "brick", "number": 6},
            ],
        },
    }


@pytest.fixture
def dummy_player():
    player = Mock()
    player.settlements = [(0, 0)]
    player.roads = [((0, 0), (1, 1))]
    return player


def test_choose_action_setup_place_settlement(dummy_game_state, dummy_player):
    ai = EasyAIStrategy()
    with patch.object(ai, "pick_bad_but_not_terrible_node", return_value=(0, 0)):
        result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "place_settlement"
    assert result["kwargs"]["position"] == (0, 0)


def test_choose_action_roll_dice(dummy_game_state, dummy_player):
    ai = EasyAIStrategy()
    dummy_game_state["state"] = "SetupRollState"
    result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "roll_dice"


def test_choose_action_place_road(dummy_game_state, dummy_player):
    ai = EasyAIStrategy()
    dummy_game_state["state"] = "SetupPlaceRoadState"
    with patch.object(ai, "pick_random_connected_road", return_value=((0, 0), (1, 1))):
        result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "place_road"
    assert result["kwargs"]["a"] == (0, 0)
    assert result["kwargs"]["b"] == (1, 1)


def test_choose_action_playing_main(dummy_game_state, dummy_player):
    ai = EasyAIStrategy()
    dummy_game_state["state"] = "PlayingMainState"
    with patch(
        "engine.game.strategies.easy_ai.get_player_resources",
        return_value={"wood": 1, "brick": 1},
    ):
        with patch("engine.game.strategies.easy_ai.can_try_road", return_value=True):
            with patch(
                "engine.game.strategies.easy_ai.can_try_settlement", return_value=False
            ):
                with patch(
                    "engine.game.strategies.easy_ai.can_try_trade", return_value=False
                ):
                    result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] in (
        "end_turn",
        "place_road",
        "place_settlement",
        "trade_with_bank",
    )


def test_choose_action_default(dummy_game_state, dummy_player):
    ai = EasyAIStrategy()
    dummy_game_state["state"] = "UnknownState"
    result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "end_turn"
