class StrategyAI:
    """
    Base class for AI strategies in Settlers. All AI strategies should inherit from this.
    """

    def choose_settlement_location(
        self,
        game_state,
        player,
    ):
        raise NotImplementedError(
            "AI strategy must implement choose_settlement_location."
        )

    def choose_road_location(self, game_state, player):
        raise NotImplementedError("AI strategy must implement choose_road_location.")

    def choose_action(self, game_state, player):
        raise NotImplementedError("AI strategy must implement choose_action.")
