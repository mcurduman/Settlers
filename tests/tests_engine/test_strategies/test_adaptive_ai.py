from unittest.mock import Mock, patch

import pytest

from engine.game.strategies.adaptive_ai import AdaptiveAIStrategy


@pytest.fixture
def dummy_ai_player():
    player = Mock()
    player.victory_points = 4
    return player


@pytest.fixture
def dummy_human_player():
    player = Mock()
    player.victory_points = 5
    return player


@pytest.fixture
def dummy_game_state():
    return {"state": "PlayingMainState"}


@pytest.fixture
def dummy_player():
    return Mock()


def test_update_strategy_switches_to_hard(dummy_ai_player, dummy_human_player):
    ai = AdaptiveAIStrategy()
    ai.update_strategy(dummy_ai_player, dummy_human_player)
    assert ai.current.__class__.__name__ == "HardAIStrategy"


def test_update_strategy_switches_to_easy(dummy_ai_player, dummy_human_player):
    ai = AdaptiveAIStrategy()
    dummy_ai_player.victory_points = 6
    ai.update_strategy(dummy_ai_player, dummy_human_player)
    assert ai.current.__class__.__name__ == "EasyAIStrategy"


def test_choose_action_delegates_to_current(dummy_game_state, dummy_player):
    ai = AdaptiveAIStrategy()
    with patch.object(
        ai.current, "choose_action", return_value={"command": "end_turn", "kwargs": {}}
    ) as mock_choose:
        result = ai.choose_action(dummy_game_state, dummy_player)
    mock_choose.assert_called_once_with(dummy_game_state, dummy_player)
    assert result["command"] == "end_turn"


def test_name_property(dummy_ai_player, dummy_human_player):
    ai = AdaptiveAIStrategy()
    ai.update_strategy(dummy_ai_player, dummy_human_player)
    assert ai.name == "hard"
    dummy_ai_player.victory_points = 10
    ai.update_strategy(dummy_ai_player, dummy_human_player)
    assert ai.name == "easy"
