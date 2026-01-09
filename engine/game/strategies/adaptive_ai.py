from engine.game.strategies.easy_ai import EasyAIStrategy
from engine.game.strategies.hard_ai import HardAIStrategy


class AdaptiveAIStrategy:
    """
    Chooses between Easy and Hard AI strategies dynamically
    based on Victory Points.
    """

    def __init__(self):
        self.easy = EasyAIStrategy()
        self.hard = HardAIStrategy()
        self.current = self.easy  # default

    def update_strategy(self, ai_player, human_player):
        """
        Decide which strategy to use.
        """
        if ai_player.victory_points < human_player.victory_points:
            self.current = self.hard
        else:
            self.current = self.easy

    def choose_action(self, game_state, player):
        print(f"Adaptive AI using {self.current.__class__.__name__} strategy.")
        return self.current.choose_action(game_state, player)

    @property
    def name(self):
        return "hard" if self.current is self.hard else "easy"
