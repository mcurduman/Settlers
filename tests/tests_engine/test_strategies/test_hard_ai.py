import pytest
from unittest.mock import Mock, patch
from engine.game.strategies.hard_ai import HardAIStrategy


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


def test_choose_action_roll_state(dummy_game_state, dummy_player):
    ai = HardAIStrategy()
    dummy_game_state["state"] = "SetupRollState"
    assert ai.choose_action(dummy_game_state, dummy_player)["command"] == "roll_dice"


def test_choose_action_setup_place_settlement(dummy_game_state, dummy_player):
    ai = HardAIStrategy()
    with patch.object(ai, "pick_best_node", return_value=(0, 0)):
        result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "place_settlement"
    assert result["kwargs"]["position"] == (0, 0)


def test_choose_action_setup_place_road(dummy_game_state, dummy_player):
    ai = HardAIStrategy()
    dummy_game_state["state"] = "SetupPlaceRoadState"
    with patch.object(ai, "pick_setup_target_node", return_value=(1, 1)):
        with patch.object(
            ai, "pick_road_towards_target", return_value=((0, 0), (1, 1))
        ):
            result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "place_road"


def test_choose_action_playing_main(dummy_game_state, dummy_player):
    ai = HardAIStrategy()
    dummy_game_state["state"] = "PlayingMainState"
    with patch.object(
        ai, "_play_main", return_value={"command": "end_turn", "kwargs": {}}
    ) as mock_play:
        result = ai.choose_action(dummy_game_state, dummy_player)
    mock_play.assert_called_once_with(dummy_game_state, dummy_player)
    assert result["command"] == "end_turn"


def test_choose_action_playing_place_road(dummy_game_state, dummy_player):
    ai = HardAIStrategy()
    dummy_game_state["state"] = "PlayingPlaceRoadState"
    with patch.object(ai, "choose_target_node", return_value=(1, 1)):
        with patch.object(
            ai, "pick_road_towards_target", return_value=((0, 0), (1, 1))
        ):
            result = ai.choose_action(dummy_game_state, dummy_player)
    assert result["command"] == "place_road"


def test_pick_best_node(dummy_game_state):
    ai = HardAIStrategy()
    with patch.object(ai, "score_node", return_value=10):
        node = ai.pick_best_node(dummy_game_state)
    assert node in [(0, 0), (1, 1)]


def test_score_node(dummy_game_state):
    ai = HardAIStrategy()
    score = ai.score_node(dummy_game_state, (0, 0))
    assert isinstance(score, (int, float))


def test_distance_to_network(dummy_player):
    ai = HardAIStrategy()
    dist = ai.distance_to_network(dummy_player, (2, 2))
    assert isinstance(dist, (int, float))


def test_reached_target(dummy_player):
    ai = HardAIStrategy()
    assert ai.reached_target(dummy_player, (0, 0))


def test_pick_road_towards_target(dummy_game_state, dummy_player):
    ai = HardAIStrategy()
    edge = ai.pick_road_towards_target(dummy_game_state, dummy_player, (1, 1))
    assert edge is None or isinstance(edge, tuple)


def test_smart_trade():
    ai = HardAIStrategy()
    resources = {"wood": 0, "brick": 3, "wheat": 0, "sheep": 0}
    trade = ai.smart_trade(resources)
    if trade:
        assert set(trade.keys()) == {"give", "receive", "rate"}


def test_dist_static():
    assert HardAIStrategy.dist((0, 0), (3, 4)) == 5
