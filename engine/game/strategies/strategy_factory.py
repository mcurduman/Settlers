from engine.game.strategies.easy_ai import EasyAIStrategy
from engine.game.strategies.hard_ai import HardAIStrategy


def get_ai_strategy(difficulty: str):
    """
    Factory function to return the correct AI strategy instance based on difficulty.
    Accepts 'easy' or 'hard' (case-insensitive).
    """
    if str(difficulty).lower() == "hard":
        return HardAIStrategy()
    return EasyAIStrategy()
