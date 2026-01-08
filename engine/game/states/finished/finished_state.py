from engine.game.states.game_state import GameState
from engine.utils.exceptions.game_ended_exception import GameEndedException


class FinishedState(GameState):
    """
    State representing the end of the game. No commands can be executed in this state.
    """

    def execute(self, command_name, *args, **kwargs):
        raise GameEndedException(
            "No commands can be executed in FinishedState. The game is over."
        )
