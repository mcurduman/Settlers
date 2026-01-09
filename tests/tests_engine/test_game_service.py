import os

import pytest

from engine.services.game_service import GameService
from engine.utils.exceptions.game_not_started_exception import \
    GameNotStartedException


@pytest.fixture
def game_service(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    service = GameService()
    return service


def test_start_game_creates_game(game_service):
    game_service.start_game()
    state = game_service.get_state()
    assert state["state"] == "SetupRollState"
    assert len(state["players"]) == 2
    assert "board" in state


def test_end_game_saves_scores(game_service):
    game_service.start_game()
    result = game_service.end_game()
    assert result["message"] == "Game ended successfully."
    assert os.path.exists("scores.json")
    import json

    with open("scores.json") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert "players" in data[-1]


def test_get_state_raises_if_not_started(game_service):
    with pytest.raises(GameNotStartedException):
        game_service.get_state()


def test_execute_command_by_name_roll_dice(game_service):
    game_service.start_game()
    game_service.execute_command_by_name("roll_dice")
    state = game_service.get_state()
    assert "state" in state


def test_handle_ai_turn_executes(monkeypatch, game_service):
    game_service.start_game()
    game_service._game.current_player_index = 1
    game_service.handle_ai_turn()
    assert hasattr(game_service._game, "ai_action_description")


def test_end_game_no_game(monkeypatch):
    service = GameService()
    result = service.end_game()
    assert result["message"] == "Game ended successfully."


def test_handle_ai_turn_not_ai(game_service, capsys):
    game_service.start_game()
    game_service._game.current_player_index = 0  # Human
    game_service.handle_ai_turn()
    out = capsys.readouterr().out
    assert "not AI" in out


def test_handle_ai_turn_no_action(monkeypatch, game_service, capsys):
    game_service.start_game()
    game_service._game.current_player_index = 1
    game_service._game.handle_ai_strategy = lambda player: None
    game_service.handle_ai_turn()
    out = capsys.readouterr().out
    assert "No action returned" in out
