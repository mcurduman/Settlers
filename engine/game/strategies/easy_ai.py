from engine.game.strategies.strategy_ai import StrategyAI


class EasyAIStrategy(StrategyAI):
    """
    A simple AI strategy for Settlers. Makes random or basic moves.
    """

    def choose_action(self, game_state, player):
        # Example: always end turn if possible
        return "end_turn"

    # Add more methods as needed for integration
