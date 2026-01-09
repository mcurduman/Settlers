import pytest

from engine.game.strategies.strategy_ai import StrategyAI


class DummyStrategy(StrategyAI):
    def choose_action(self, game_state, player):
        return {"command": "dummy", "kwargs": {}}


def test_strategy_ai_is_abstract():
    with pytest.raises(TypeError):
        StrategyAI()


def test_dummy_strategy_choose_action():
    dummy = DummyStrategy()
    result = dummy.choose_action({}, None)
    assert isinstance(result, dict)
    assert "command" in result
    assert "kwargs" in result
