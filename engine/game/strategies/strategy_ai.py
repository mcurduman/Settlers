from abc import ABC, abstractmethod


class StrategyAI(ABC):
    """
    Abstract base class (interface + shared helpers) for AI strategies.
    """

    @abstractmethod
    def choose_action(self, game_state, player):
        """
        Must return a dict:
        {
            "command": str,
            "kwargs": dict
        }
        """
        pass

    # ...existing code...
